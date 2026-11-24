"""Verify D122 on two positive originals and a reservation-independent obstruction."""

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

H, L, C, RIGHT = "b:0:0", "b:0:1", "b:0:2", "b:1:0"


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


def classify(q, a, c):
    if any(type(x) is not int for x in (q, a, c)):
        raise ValueError("Require exact integer quotas")
    if q < 6 or a < 3 or c < 2 or q % 2 or a % 2 != 1 or c % 2:
        raise ValueError("Require even q >= 6 and c >= 2, and odd a >= 3")
    if a >= 5:
        return "II"
    return "I" if c <= q-4 else "adverse"


def core_labels(m):
    return {"s:0": 0, "s:1": m, H: m-4, L: 2, C: m-6, RIGHT: 1,
            "l:0:0:0": m-5, "l:0:1:0": m-3, "l:1:0:0": m-1, "l:1:0:1": m-2}


def positive_formula(q, a, c, branch, core):
    m = q+a+c+7
    t = (m-2)//2
    if branch == "I":
        assert a == 3 and c <= q-4
        b, e = t-c-1, t+c+1
        r_b = list(range(b, e+1, 2))
        lower_b = [t-1, e]
    else:
        assert branch == "II" and a >= 5
        k = c//2
        b, e = t-k-2, t+k+2
        r_b = [x for x in range(b, e+1) if x != t]
        lower_b = [t-2, t-1, e-1, e]
    lower_quota = len(lower_b)
    assert 5 <= b <= e <= m-7 and b+e == 2*t
    assert t not in r_b and len(r_b) == c+lower_quota
    marks = bytearray(m+1)
    for x in r_b:
        marks[x] = 1
    r_a = [x for x in range(3, m-6) if not marks[x]]
    d_b = [x-2 for x in r_b]
    d_a = [d for d in range(3, m-6) if not marks[d+2]]
    reps = [x for x in r_a if 5 <= x < t]
    j = (a-1-lower_quota)//2
    assert len(reps) == (q+a-lower_quota-5)//2 and len(reps)-j == (q-4)//2 and j >= 0
    selected = bytearray(m+1)
    for x in reps[len(reps)-j:] if j else []:
        selected[x] = selected[2*t-x] = 1
    batch_a = {"labels": r_a, "differences": d_a,
               "slots": {L: [f"l:0:1:{i}" for i in range(lower_quota+1, a)],
                         H: [f"l:0:0:{i}" for i in range(1, q)]},
               "allocation": {L: [x for x in r_a if selected[x]], H: [x for x in r_a if not selected[x]]}}
    batch_b = {"labels": r_b, "differences": d_b,
               "slots": {L: [f"l:0:1:{i}" for i in range(1, lower_quota+1)],
                         C: [f"l:0:2:{i}" for i in range(c)]},
               "allocation": {L: lower_b, C: [x for x in r_b if x not in lower_b]}}
    labels = dict(core)
    for batch in (batch_a, batch_b):
        for host, slots in batch["slots"].items():
            labels.update(zip(slots, batch["allocation"][host], strict=True))
    return {"A": batch_a, "B": batch_b}, labels


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
             "only_shared_host_L": set(batches["A"]["slots"]) & set(batches["B"]["slots"]) == {L}}
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


def retained_positive(binding, counts):
    path = ROOT / binding["original"]
    original = read_json(path)
    assert digest_file(path) == binding["original_sha256"]
    assert digest_file(ROOT / binding["result"]) == binding["result_sha256"]
    digest, graph = binding["graph_digest"], original["graph"]
    result = read_json(ROOT / binding["result"])
    cert = result["certificate"]
    assert result["status"] == "PASS" and cert["kind"] == "ordinary_graceful"
    assert cert["graph_digest"] == original["graph_digest"] == digest
    assert cert["ledger_id"] == binding["ledger_id"] and graph["profile"] == binding["profile"]
    counts["retained_positive_rechecks"] += 1
    checker = verify_certificate(graph, cert["labels"], digest)
    assert checker["valid"] and checker == cert["checker"]
    assert graph["profile"] == [[5, 3, 4], [2]]
    return {"source": binding, "checker": checker, "role": "outside_domain_comparison",
            "formula_evaluated": False}


def move_midpoint(core, batch, source, target, midpoint):
    assert midpoint in batch["allocation"][source]
    assert len(batch["slots"]) == 2 and set(batch["slots"]) == {source, target}
    assert abs(core[source]-midpoint) == abs(core[target]-midpoint)
    return batch | {"allocation": {
        source: [x for x in batch["allocation"][source] if x != midpoint],
        target: [*batch["allocation"][target], midpoint]}}


def run_controls(original, labels, core, batches, counts):
    graph, digest = original["graph"], original["graph_digest"]
    counts["declared_controls"] += 1
    wrong = "0"*64
    wrong_report = verify_certificate(graph, labels, wrong)
    assert not wrong_report["valid"] and wrong_report["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    moved_a = move_midpoint(core, batches["A"], H, L, 8)
    check_a = local_gate(core, moved_a)
    assert check_a["tests"] == {"labels_exact": True, "differences_exact": True,
                               "eligible": True, "quotas_exact": False}
    assert check_a["actual_quotas"] == {L: 1, H: 4} and not check_a["valid"]

    counts["declared_controls"] += 1
    moved_b = move_midpoint(core, batches["B"], L, C, 7)
    check_b = local_gate(core, moved_b)
    assert check_b["tests"] == check_a["tests"]
    assert check_b["actual_quotas"] == {L: 1, C: 3} and not check_b["valid"]

    counts["declared_controls"] += 1
    a = batches["A"]
    overlap_a = a | {"labels": [3, 4, 5, 8, 11], "differences": [3, 6, 9, 10, 11],
                     "allocation": {L: [], H: [3, 4, 5, 8, 11]}}
    overlap = {"A": overlap_a, "B": batches["B"]}
    locals_pass = {key: local_gate(core, batch) for key, batch in overlap.items()}
    conflict = global_gate(graph, core, overlap)
    assert all(row["valid"] for row in locals_pass.values())
    assert conflict["tests"] == {"label_partition": False, "difference_partition": False,
                                 "slots_exact": True, "only_shared_host_L": True}
    assert not conflict["valid"]
    return {"wrong_digest": {"expected_digest": wrong, "checker": wrong_report},
            "A_midpoint_move": {"batch": moved_a, "local": check_a},
            "B_midpoint_move": {"batch": moved_b, "local": check_b},
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
    prep = read_json(HERE / "preparation_receipt.json")
    counts["original_preparations"] = prep["original_preparations"]
    counts["new_graph_identities"] = prep["new_graph_identities"]
    records = {}
    for key in ("I", "adverse", "II"):
        frozen = prep["originals"][key]
        path = HERE / frozen["path"]
        assert digest_file(path) == frozen["raw_sha256"]
        original = read_json(path)
        graph, digest = original["graph"], original["graph_digest"]
        profile = cfg["scope"]["boundaries"][key]
        assert graph["profile"] == frozen["profile"] == profile and digest == frozen["graph_digest"]
        counts["new_numerical_boundaries"] += 1
        q, a, c = profile[0]
        branch = classify(q, a, c)
        assert branch == key
        core = core_labels(q+a+c+7)
        if branch == "adverse":
            obstruction = audit.obstruction(original, core)
            obstruction["original"] = frozen
            counts["fixed_core_obstruction_records"] += 1
            continue

        batches, labels = positive_formula(q, a, c, branch, core)
        counts["reserved_batches"] += len(batches)
        local = {name: local_gate(core, batch) for name, batch in batches.items()}
        compatibility = global_gate(graph, core, batches)
        checker = verify_certificate(graph, labels, digest)
        pins, growth = physical_gates(graph, labels)
        assert all(row["valid"] for row in local.values()) and compatibility["valid"]
        assert checker["valid"] and pins["valid"] and growth["valid"]
        ledger = canonical_digest({"graph_digest": digest, "labels": sorted(labels.items())})
        independent = audit.positive(original, branch, core, batches, labels, ledger, checker, local, pins, growth)
        certificate = {"kind": "ordinary_graceful", "graph_digest": digest, "ledger_id": ledger,
                       "labels": labels, "checker": checker, "physical_spine": graph["spine"], "physical_pins": pins}
        records[key] = {"original": frozen, "core": core, "batches": batches, "local": local,
                        "global": compatibility, "growth_premises": growth, "certificate": certificate,
                        "independent": independent}
        counts["new_certificates"] += 1
        if branch == "I":
            probes = run_controls(original, labels, core, batches, counts)
            control_audit = audit.controls(original, core, batches, labels, probes)

    retained = retained_positive(cfg["retained"]["D119"], counts)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": cfg["scope"],
            "runtime": runtime, "positive": records, "obstruction": obstruction,
            "controls": probes, "independent_controls": control_audit,
            "retained_D119": retained, "retained_execution_statuses": history}


def execute():
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = dict.fromkeys(cfg["count_keys"], 0)
    counts.update(workers=1, official_invocations=1, preflights=1)
    receipt = {"status": "INCOMPLETE", "task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "counts": counts, "limits": limits}
    try:
        assert __debug__ and sys.dont_write_bytecode
        assert all(not (HERE / name).exists() for name in ("result.json", "obstruction.json", "command_receipt.json", "__pycache__"))
        bound_names = (*cfg["preflight_inputs"], "preflight_receipt.json", "preflight_supervision.json")
        receipt["input_hashes"] = {name: digest_file(HERE / name) for name in bound_names}
        result = produce(cfg, counts)
        assert all(value == limits[key] for key, value in counts.items())
        obstruction = result.pop("obstruction")
        obstruction_sha = write_record("obstruction.json", obstruction, limits)
        result["obstruction"] = {"path": "obstruction.json", "sha256": obstruction_sha,
                                 "original": obstruction["original"]}
        receipt["obstruction_sha256"] = obstruction_sha
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
