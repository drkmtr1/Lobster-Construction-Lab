"""Supply and verify exactly the prepared D124 boundary and four declared probes."""

from time import process_time

CPU_START = process_time()

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import traceback

import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.verify import verify_certificate

X, M, Z, RIGHT = "b:0:0", "b:0:1", "b:0:2", "b:1:0"


def read_json(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence size cap exceeded")
    with (HERE / name).open("xb") as output:
        output.write(raw)
    return sha256(raw).hexdigest()


def indexed_formula(q, c):
    if type(q) is not int or type(c) is not int or min(q, c) < 6 or q % 2 or c % 2:
        raise ValueError("Require exact even integers q, c >= 6")
    m = q+c+10
    t = (m-2)//2
    b, e = t-q//2, t+q//2
    core = {"s:0": 0, "s:1": m, X: 2, M: m-6, Z: m-4, RIGHT: 1,
            "l:0:0:0": m-3, "l:0:1:0": m-5, "l:1:0:0": m-1, "l:1:0:1": m-2}
    interval = range(b, e+1)
    outside = [*range(3, b), *range(e+1, m-6)]
    assert b >= 7 and m-7-e == c//2-1 >= 2 and len(interval) == q+1 and len(outside) == c
    batch_a = {
        "labels": [x for x in interval if x != t],
        "differences": [d for d in range(b-2, e-1) if d != t-4],
        "slots": {X: [f"l:0:0:{i}" for i in range(1, q)], M: ["l:0:1:1"]},
        "allocation": {X: [x for x in interval if x not in (t-2, t)], M: [t-2]},
    }
    batch_b = {
        "labels": [*range(3, b), t, *range(e+1, m-6)],
        "differences": [d for d in range(3, m-6) if not b-2 <= d <= e-2 or d == t-4],
        "slots": {M: ["l:0:1:2"], Z: [f"l:0:2:{i}" for i in range(c)]},
        "allocation": {M: [t], Z: outside},
    }
    labels = dict(core)
    for batch in (batch_a, batch_b):
        for host, slots in batch["slots"].items():
            for leaf, label in zip(slots, batch["allocation"][host], strict=True):
                assert leaf not in labels
                labels[leaf] = label
    return core, {"A": batch_a, "B": batch_b}, labels


def local_gate(core, batch):
    slots, allocation = batch["slots"], batch["allocation"]
    assert len(slots) == 2 and set(slots) == set(allocation) and set(slots) <= set(core)
    labels, weights = batch["labels"], batch["differences"]
    assert len(labels) == len(weights) == len(set(labels)) == len(set(weights))
    assert all(type(x) is int and x not in (core[h] for h in slots) for x in labels)
    assert all(type(d) is int and d > 0 for d in weights)
    weight_set = set(weights)
    options = {x: {h: abs(core[h]-x) for h in slots if abs(core[h]-x) in weight_set} for x in labels}
    actual = Counter(x for xs in allocation.values() for x in xs)
    used = Counter(abs(core[h]-x) for h, xs in allocation.items() for x in xs)
    eligible = all(options.values()) and all(h in options.get(x, {}) for h, xs in allocation.items() for x in xs)
    actual_quotas = {h: len(xs) for h, xs in allocation.items()}
    expected_quotas = {h: len(vs) for h, vs in slots.items()}
    tests = {"labels_exact": actual == Counter(labels), "differences_exact": used == Counter(weights),
             "eligible": eligible, "quotas_exact": actual_quotas == expected_quotas}
    return {"tests": tests, "valid": all(tests.values()), "eligible_options": options,
            "actual_quotas": actual_quotas, "expected_quotas": expected_quotas,
            "allocated_labels": sorted(actual.elements()), "allocated_differences": sorted(used.elements())}


def global_gate(graph, core, batches):
    m = len(graph["edges"])
    fixed_weights = [abs(core[u]-core[v]) for u, v in graph["edges"] if u in core and v in core]
    assert len(fixed_weights) == len(set(fixed_weights)) == 9
    expected_labels = set(range(m+1))-set(core.values())
    expected_weights = set(range(1, m+1))-set(fixed_weights)
    reserved_labels = Counter(x for batch in batches.values() for x in batch["labels"])
    reserved_weights = Counter(d for batch in batches.values() for d in batch["differences"])
    supplied_slots = Counter((host, leaf) for batch in batches.values()
                             for host, leaves in batch["slots"].items() for leaf in leaves)
    actual_slots = Counter()
    for u, v in graph["edges"]:
        if u not in core and v not in core:
            raise AssertionError("A pendant vacancy lacks its named core host")
        if (u in core) != (v in core):
            actual_slots[(u, v) if u in core else (v, u)] += 1
    assert set(graph["vertices"])-set(core) == {leaf for (_, leaf) in actual_slots}
    tests = {"label_partition": reserved_labels == Counter(expected_labels),
             "difference_partition": reserved_weights == Counter(expected_weights),
             "slots_exact": supplied_slots == actual_slots,
             "only_shared_host_M": set(batches["A"]["slots"]) & set(batches["B"]["slots"]) == {M}}
    return {"tests": tests, "valid": all(tests.values()),
            "repeated_labels": {x: count for x, count in reserved_labels.items() if count > 1},
            "repeated_differences": {d: count for d, count in reserved_weights.items() if count > 1},
            "missing_labels": sorted(expected_labels-set(reserved_labels)),
            "missing_differences": sorted(expected_weights-set(reserved_weights))}


def physical_gates(graph, labels):
    entrance, exit_vertex = "s:0", "s:1"
    spine = [entrance, exit_vertex]
    edges = graph["edges"]
    expected = {entrance: 0, exit_vertex: len(edges), RIGHT: 1}
    actual = {v: labels[v] for v in expected}
    pins = {"valid": actual == expected and all(type(x) is int for x in actual.values()),
            "actual": actual, "expected": expected}
    neighbors = {u if v == exit_vertex else v for u, v in edges if exit_vertex in (u, v)}
    tests = {"actual_spine": graph["spine"] == spine and any(frozenset(edge) == frozenset(spine) for edge in edges),
             "exit_neighbors": neighbors == {entrance, RIGHT},
             "host_off_spine": RIGHT in graph["vertices"] and RIGHT not in graph["spine"],
             "growth_labels": pins["valid"]}
    return pins, {"tests": tests, "valid": all(tests.values()), "actual_exit_neighbors": sorted(neighbors)}


def evaluate_formula(graph, counts, *, retained):
    expected_profile = [[6, 3, 6], [2]] if retained else [[6, 3, 8], [2]]
    assert graph["profile"] == expected_profile
    q, _, c = graph["profile"][0]
    assert (q == c) is retained
    core, batches, labels = indexed_formula(q, c)
    assert set(batches) == {"A", "B"}
    evaluation_key = "retained_formula_evaluations" if retained else "new_formula_evaluations"
    batch_key = "retained_comparison_batches" if retained else "reserved_batches"
    counts[evaluation_key] += 1
    counts[batch_key] += len(batches)
    counts["evaluated_batch_objects"] += len(batches)
    return core, batches, labels


def retained_comparison(binding, counts):
    original_path, result_path = ROOT / binding["original"], ROOT / binding["result"]
    assert digest_file(original_path) == binding["original_sha256"]
    assert digest_file(result_path) == binding["result_sha256"]
    original, archive = read_json(original_path), read_json(result_path)
    graph, digest = original["graph"], original["graph_digest"]
    cert = archive["certificate"]
    assert archive["status"] == "PASS" and cert["kind"] == "ordinary_graceful"
    assert graph["profile"] == binding["profile"] == [[6, 3, 6], [2]]
    assert cert["graph_digest"] == digest == binding["graph_digest"]
    assert cert["ledger_id"] == binding["ledger_id"]
    assert archive["original"] == {"path": original_path.name, "raw_sha256": binding["original_sha256"],
                                  "graph_digest": digest}
    core, batches, labels = evaluate_formula(graph, counts, retained=True)
    assert (core, batches, labels) == (archive["core"], archive["batches"], cert["labels"])
    local = {name: local_gate(core, batch) for name, batch in batches.items()}
    global_report = global_gate(graph, core, batches)
    pins, growth = physical_gates(graph, labels)
    counts["retained_positive_rechecks"] += 1
    checker = verify_certificate(graph, cert["labels"], digest)
    assert checker["valid"] and checker == cert["checker"]
    independent = audit.check_profile(original, core, batches, labels, cert["ledger_id"],
                                      checker, local, global_report, pins, growth, retained=True)
    assert json.loads(json.dumps(independent["r226"])) == archive["independent"]["r226"]
    return {"source": binding, "checker": checker, "independent": independent,
            "pointwise_agreement": {"labels": True, "core": True, "palettes": True,
                                    "ordered_allocations": True, "named_slots": True}}


def run_controls(original, labels, core, batches, counts):
    graph, digest = original["graph"], original["graph_digest"]
    counts["declared_controls"] += 1
    wrong = "0"*64
    wrong_report = verify_certificate(graph, labels, wrong)
    assert not wrong_report["valid"] and wrong_report["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    first, second = "l:0:0:1", "l:0:2:4"
    assert (labels[first], labels[second]) == (8, 7)
    cross = labels | {first: labels[second], second: labels[first]}
    cross_check = verify_certificate(graph, cross, digest)
    pins, _ = physical_gates(graph, cross)
    assert Counter(cross.values()) == Counter(labels.values()) and pins["valid"]
    assert not cross_check["valid"]
    assert cross_check["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]

    counts["declared_controls"] += 1
    a, b = batches["A"], batches["B"]
    moved = 3
    assert moved in b["allocation"][Z] and abs(core[M]-moved) == 15
    reassigned = b | {"allocation": {M: [*b["allocation"][M], moved],
                                     Z: [x for x in b["allocation"][Z] if x != moved]}}
    quota = local_gate(core, reassigned)
    assert quota["tests"] == {"labels_exact": True, "differences_exact": False,
                              "eligible": True, "quotas_exact": False}
    assert quota["actual_quotas"] == {M: 2, Z: 7} and not quota["valid"]

    counts["declared_controls"] += 1
    assert 8 in a["labels"] and 6 in a["differences"] and 8 in a["allocation"][X]
    overlap_a = a | {"labels": [7 if x == 8 else x for x in a["labels"]],
                     "differences": [5 if d == 6 else d for d in a["differences"]],
                     "allocation": {X: [7 if x == 8 else x for x in a["allocation"][X]],
                                    M: a["allocation"][M]}}
    overlap = {"A": overlap_a, "B": b}
    locals_pass = {name: local_gate(core, batch) for name, batch in overlap.items()}
    conflict = global_gate(graph, core, overlap)
    assert all(report["valid"] for report in locals_pass.values())
    assert conflict["tests"] == {"label_partition": False, "difference_partition": False,
                                 "slots_exact": True, "only_shared_host_M": True}
    assert not conflict["valid"]
    return {"wrong_digest": {"expected_digest": wrong, "checker": wrong_report},
            "cross_center": {"vertices": [first, second], "checker": cross_check, "pins": pins},
            "chain_forcing": {"moved_label": moved, "batch": reassigned, "local": quota},
            "global_overlap": {"batches": overlap, "local": locals_pass, "global": conflict}}


def validate_inputs(cfg):
    pre = read_json(HERE / "preflight_receipt.json")
    supervised = read_json(HERE / "preflight_supervision.json")
    assert pre["status"] == supervised["status"] == "PASS"
    assert pre["task"] == supervised["task"] == cfg["task"] and pre["parent"] == cfg["parent"]
    assert supervised["receipt_sha256"] == digest_file(HERE / "preflight_receipt.json")
    assert supervised["config_sha256"] == digest_file(HERE / "config.json")
    assert pre["preflights"] == 1 and pre["task_module_imports"] == 0
    assert pre["input_hashes"] == {name: digest_file(HERE / name) for name in cfg["preflight_inputs"]}
    assert pre["runtime"]["sha256"] == cfg["runtime_sha256"] == digest_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert digest_file(ROOT / path) == expected, path
    return pre["runtime"]


def produce(cfg, counts):
    runtime = validate_inputs(cfg)
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    original = read_json(HERE / "original.json")
    prep = read_json(HERE / "preparation_receipt.json")
    graph, digest = original["graph"], original["graph_digest"]
    assert prep["graph_digest"] == digest
    assert graph["profile"] == cfg["scope"]["boundary_profile"] == [[6, 3, 8], [2]]
    counts["original_preparations"] = prep["original_preparations"]
    counts["new_graph_identities"] = prep["new_graph_identities"]
    counts["new_numerical_boundaries"] += 1
    core, batches, labels = evaluate_formula(graph, counts, retained=False)
    local = {name: local_gate(core, batch) for name, batch in batches.items()}
    global_report = global_gate(graph, core, batches)
    assert all(report["valid"] for report in local.values()) and global_report["valid"]
    pins, growth = physical_gates(graph, labels)
    checker = verify_certificate(graph, labels, digest)
    assert checker["valid"] and pins["valid"] and growth["valid"]
    ledger_id = canonical_digest({"graph_digest": digest, "labels": sorted(labels.items())})
    independent = audit.check_profile(original, core, batches, labels, ledger_id,
                                      checker, local, global_report, pins, growth, retained=False)
    retained = retained_comparison(cfg["retained"]["D123"], counts)
    probes = run_controls(original, labels, core, batches, counts)
    independent_controls = audit.controls(original, labels, core, batches, probes, independent["r226"]["B"])
    counts["symbolic_theorems"] += 1
    counts["new_certificates"] += 1
    certificate = {"kind": "ordinary_graceful", "graph_digest": digest, "ledger_id": ledger_id,
                   "labels": labels, "checker": checker, "physical_spine": graph["spine"], "physical_pins": pins}
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": cfg["scope"], "runtime": runtime,
            "original": {"path": "original.json", "raw_sha256": prep["original_sha256"], "graph_digest": digest},
            "certificate": certificate, "core": core, "batches": batches, "local": local, "global": global_report,
            "growth_premises": growth, "independent": independent, "retained_D123": retained, "controls": probes,
            "independent_controls": independent_controls, "retained_execution_statuses": history}


def execute():
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = dict.fromkeys(cfg["count_keys"], 0)
    counts.update(workers=1, official_invocations=1, preflights=1)
    receipt = {"status": "INCOMPLETE", "task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "counts": counts, "limits": limits}
    try:
        assert __debug__ and sys.dont_write_bytecode
        assert all(not (HERE / name).exists() for name in ("result.json", "command_receipt.json", "__pycache__"))
        bound_names = (*cfg["preflight_inputs"], "preflight_receipt.json", "preflight_supervision.json")
        receipt["input_hashes"] = {name: digest_file(HERE / name) for name in bound_names}
        result = produce(cfg, counts)
        assert all(value == limits[key] for key, value in counts.items())
        receipt["result_sha256"] = write_record("result.json", result, limits)
        prior_cpu = sum(read_json(HERE / name)["process_cpu_seconds"]
                        for name in ("preparation_receipt.json", "preflight_receipt.json"))
        if prior_cpu + process_time() - CPU_START >= limits["process_cpu_seconds"]:
            raise TimeoutError("Combined process CPU limit reached")
        receipt["status"] = "PASS"
    except (Exception, KeyboardInterrupt):
        receipt["error"] = traceback.format_exc()
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    write_record("command_receipt.json", receipt, limits)
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(execute())
