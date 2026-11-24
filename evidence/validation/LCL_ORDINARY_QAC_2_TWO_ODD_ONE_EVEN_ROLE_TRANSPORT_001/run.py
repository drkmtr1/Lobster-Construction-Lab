"""Transport D119 onto original physical names and verify the retained boundary."""

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

RIGHT = "b:1:0"


def read_json(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence size cap exceeded")
    with (HERE / name).open("xb") as output:
        output.write(raw)
    return sha256(raw).hexdigest()


def select_roles(quotas):
    if len(quotas) != 3 or any(type(x) is not int for x in quotas):
        raise ValueError("Require three exact integer quotas")
    even = [i for i, x in enumerate(quotas) if x % 2 == 0]
    eligible_high = [i for i, x in enumerate(quotas) if x % 2 and x >= 5]
    if len(even) != 1 or not eligible_high:
        raise ValueError("Require two odd quotas and exactly one even quota")
    i_c, i_h = even[0], eligible_high[0]
    i_l = next(i for i in range(3) if i not in (i_h, i_c))
    if quotas[i_c] < 2 or quotas[i_l] < 3:
        raise ValueError("Require even quota >= 2 and both odd quotas >= 3")
    return i_h, i_l, i_c


def role_binding(graph, indices, role_quotas):
    index_counts = Counter(indices)
    bijective = (len(indices) == 3 and all(type(i) is int for i in indices)
                 and index_counts == Counter(range(3)))
    report = {"indices": list(indices), "requested_quotas": list(role_quotas),
              "bijective": bijective, "repeated_indices": sorted(i for i, n in index_counts.items() if n > 1),
              "omitted_indices": sorted(set(range(3))-index_counts.keys()),
              "quota_compatible": None, "slots_exact": None, "valid": False}
    if not bijective:
        return report
    physical = graph["profile"][0]
    actual_quotas = [physical[i] for i in indices]
    rows = {}
    for role, index, quota in zip("HLC", indices, role_quotas, strict=True):
        center = f"b:0:{index}"
        proposed = {f"l:0:{index}:{k}" for k in range(quota)}
        actual = {v if u == center else u for u, v in graph["edges"] if center in (u, v)}-{"s:0"}
        rows[role] = {"center": center, "requested": sorted(proposed), "actual": sorted(actual),
                      "absent_from_original": sorted(proposed-actual), "omitted_actual": sorted(actual-proposed)}
    slots_exact = all(row["requested"] == row["actual"] for row in rows.values())
    quota_compatible = actual_quotas == list(role_quotas)
    inverse = [indices.index(index) for index in range(3)]
    report.update(actual_quotas=actual_quotas, quota_compatible=quota_compatible, slots_exact=slots_exact,
                  inverse=inverse, rows=rows, valid=quota_compatible and slots_exact)
    return report


def indexed_formula(q, a, c, indices):
    # D119 numerical kernel with the symbolic role map applied at emission.
    i_h, i_l, i_c = indices
    H, L, C = (f"b:0:{index}" for index in indices)
    m = q+a+c+7
    core = {"s:0": 0, "s:1": m, H: m-4, L: 2, C: m-6, RIGHT: 1,
            f"l:0:{i_h}:0": m-5, f"l:0:{i_l}:0": m-3, "l:1:0:0": m-1, "l:1:0:1": m-2}
    k = c//2
    reserved_labels = bytearray(m+1)
    reserved_differences = bytearray(m+1)
    for i in range(k+1):
        reserved_labels[5+2*i] = reserved_labels[m-7-2*i] = 1
        reserved_differences[3+2*i] = reserved_differences[m-9-2*i] = 1
    residual = range(3, m-6)
    r_b = [x for x in residual if reserved_labels[x]]
    d_b = [d for d in residual if reserved_differences[d]]
    r_a = [x for x in residual if not reserved_labels[x]]
    d_a = [d for d in residual if not reserved_differences[d]]
    assert len(r_b) == len(d_b) == c+2
    reps = [x for x in r_a if x >= 5 and x < m-2-x]
    j = (a-3)//2
    assert len(reps) == (q+a-6)//2 and len(reps)-j == (q-3)//2
    chosen = reps[len(reps)-j:] if j else []
    lower_a = bytearray(m+1)
    for x in chosen:
        lower_a[x] = lower_a[m-2-x] = 1
    batch_a = {"labels": r_a, "differences": d_a,
               "slots": {L: [f"l:0:{i_l}:{k}" for k in range(3, a)], H: [f"l:0:{i_h}:{k}" for k in range(1, q)]},
               "allocation": {L: [x for x in r_a if lower_a[x]], H: [x for x in r_a if not lower_a[x]]}}
    batch_b = {"labels": r_b, "differences": d_b,
               "slots": {L: [f"l:0:{i_l}:1", f"l:0:{i_l}:2"], C: [f"l:0:{i_c}:{i}" for i in range(c)]},
               "allocation": {L: [c+5, m-7], C: [x for x in r_b if x not in (c+5, m-7)]}}
    labels = dict(core)
    for batch in (batch_a, batch_b):
        for host, slots in batch["slots"].items():
            labels.update(zip(slots, batch["allocation"][host], strict=True))
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


def global_gate(graph, core, batches, lower):
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
             "only_shared_host_L": set(batches["A"]["slots"]) & set(batches["B"]["slots"]) == {lower}}
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


def run_controls(original, labels, role_quotas, counts):
    graph, digest = original["graph"], original["graph_digest"]
    counts["declared_controls"] += 1
    wrong = "0"*64
    wrong_report = verify_certificate(graph, labels, wrong)
    assert not wrong_report["valid"] and wrong_report["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    repeated = role_binding(graph, (0, 0, 2), role_quotas)
    assert not repeated["bijective"] and not repeated["valid"]
    assert repeated["quota_compatible"] is None and repeated["slots_exact"] is None

    counts["declared_controls"] += 1
    incompatible = role_binding(graph, (2, 1, 0), role_quotas)
    assert incompatible["bijective"] and not incompatible["quota_compatible"] and not incompatible["slots_exact"]
    assert not incompatible["valid"]

    counts["declared_controls"] += 1
    u, v = "l:0:0:1", "l:0:0:2"
    assert (labels[u], labels[v]) == (3, 4)
    swapped = labels | {u: labels[v], v: labels[u]}
    checker = verify_certificate(graph, swapped, digest)
    pins, growth = physical_gates(graph, swapped)
    mismatches = sorted(name for name in labels if labels[name] != swapped[name])
    assert checker["valid"] and pins["valid"] and growth["valid"]
    assert mismatches == [u, v]
    return {"wrong_digest": {"expected_digest": wrong, "checker": wrong_report},
            "nonbijective": repeated, "quota_incompatible": incompatible,
            "within_host": {"vertices": [u, v], "checker": checker, "pins": pins,
                            "growth": growth, "pointwise_agreement": not mismatches, "mismatches": mismatches}}


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
    source = cfg["retained"]["D119"]
    assert digest_file(ROOT / source["original"]) == source["original_sha256"]
    assert digest_file(ROOT / source["result"]) == source["result_sha256"]
    original = read_json(ROOT / source["original"])
    archived = read_json(ROOT / source["result"])
    cert = archived["certificate"]
    graph, digest = original["graph"], original["graph_digest"]
    assert archived["status"] == "PASS" and cert["kind"] == "ordinary_graceful"
    assert digest == cert["graph_digest"] == source["graph_digest"] and cert["ledger_id"] == source["ledger_id"]
    assert graph["profile"] == source["profile"] == [[5, 3, 4], [2]]
    quotas = tuple(graph["profile"][0])
    indices = select_roles(quotas)
    role_quotas = tuple(quotas[i] for i in indices)
    binding = role_binding(graph, indices, role_quotas)
    assert indices == (0, 1, 2) and binding["valid"]

    counts["retained_formula_evaluations"] += 1
    core, batches, labels = indexed_formula(*role_quotas, indices)
    counts["reserved_batches"] += len(batches)
    counts["retained_positive_rechecks"] += 1
    checker = verify_certificate(graph, cert["labels"], digest)
    assert checker["valid"] and checker == cert["checker"]
    assert labels == cert["labels"] and core == archived["core"] and batches == archived["batches"]
    local = {name: local_gate(core, batch) for name, batch in batches.items()}
    compatibility = global_gate(graph, core, batches, f"b:0:{indices[1]}")
    pins, growth = physical_gates(graph, labels)
    assert all(report["valid"] for report in local.values()) and compatibility["valid"]
    assert pins["valid"] and growth["valid"]
    independent = audit.retained(original, cert, binding, core, batches, labels, local, checker, pins, growth)
    probes = run_controls(original, labels, role_quotas, counts)
    independent_controls = audit.controls(original, cert, labels, probes)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "runtime": runtime,
            "retained_source": source, "binding": binding, "pointwise_formula_agreement": True,
            "core": core, "batches": batches, "local": local, "global": compatibility,
            "checker": checker, "pins": pins, "growth_premises": growth, "independent": independent,
            "controls": probes, "independent_controls": independent_controls, "retained_execution_statuses": history}


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
        prior_cpu = read_json(HERE / "preflight_receipt.json")["process_cpu_seconds"]
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
