"""Search-free evidence harness for the six declared Q1T2 targets."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.consumers import _nonadjacent_path_labels
from lcl.model import build_graph, graph_digest
from lcl.records import atomic_json, environment, save_source_snapshot, source_inventory, utc_now
from lcl.verify import verify_certificate, verify_graph, verify_partial

EXPECTED = {
    "run_id": "B4-UNPADDED-Q1T2-001-20261121",
    "starting_commit": "3da61c39d3444c6286b34033d6ae9fd58b20c547",
    "workers": 1,
    "max_vertices": 26,
    "max_result_bytes": 2000000,
    "new_solver_queries": 0,
    "enumeration": False,
    "cases": [
        [
            2,
            2,
            2
        ],
        [
            2,
            3,
            3
        ],
        [
            3,
            2,
            4
        ],
        [
            3,
            3,
            5
        ],
        [
            4,
            5,
            2
        ],
        [
            5,
            4,
            5
        ]
    ],
    "parameter_order": [
        "q",
        "t",
        "K"
    ],
    "same_target_comparison": [
        3,
        3,
        5
    ],
    "retained_seed": {
        "path": "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001/query_record.json",
        "sha256_raw": "4b9019e5c7cd6ef68ba5ebd07b45b1b15e0ded61398b5a7d2e8d7a7b684ea744",
        "graph_digest": "a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc"
    },
    "retained_control": {
        "path": "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001/direct_checks/case-04.json",
        "sha256_raw": "b54a14ee2b12d66ae6ce44935ba03f3a1ec445a60c9d42ed4a49e7f4a2f57ac9",
        "parameters": [
            1,
            3,
            5
        ]
    },
    "historical_incomplete": {
        "raw": "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/raw_result.json",
        "raw_sha256": "9901eecb61366cf2329ebd5639e1a8c2cd738a08d5dc48da41126a6cef201b49",
        "bound": "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json",
        "bound_sha256": "b71cf1dc26700648507e8c2d9769b44e1d4536df6b788438930c2d5585679ff6"
    }
}
BASE = {"s:0": 9, "s:1": 1, "s:2": 12, "s:3": 5, "s:4": 8, "b:0:0": 4, "l:0:0:0": 10,
        "b:1:0": 11, "l:1:0:0": 2, "b:2:0": 0, "l:2:0:0": 13, "l:2:0:1": 14,
        "b:3:0": 7, "l:3:0:0": 3, "l:3:0:1": 6}
W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
H, Z = "b:0:0", "b:2:0"
PROOFS = ("research/ALPHA_UPPER_BLOCK_GENERAL_HOST.md", "research/B4_UNPADDED_Q1T2.md")


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edgeset(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def ledger(edges, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]


def parameters(q, t, K):
    if any(type(x) is not int or x < low for x, low in zip((q, t, K), (1, 2, 2))):
        raise ValueError("q,t,K must be exact integers with q>=1, t>=2, K>=2")


def formula(q, t, K):
    parameters(q, t, K)
    labels = {"s:0": q + 8, "s:1": 1, "s:2": q + 11, "s:3": 5, "s:4": 8,
              H: 4, "l:0:0:0": q + 9, "b:1:0": q + 10, "l:1:0:0": 2,
              Z: 0, "b:3:0": 7, "l:3:0:0": 3, "l:3:0:1": 6}
    labels.update({f"l:0:0:{j}": 8 + j for j in range(1, q)})
    labels.update({f"l:2:0:{j}": q + 12 + j for j in range(t)})
    return labels


def grow_upper(labels, c, names):
    need(len(set(names)) == len(names) and not labels.keys() & set(names), "fresh upper names")
    size = len(names)
    return {v: x + size if x >= c else x for v, x in labels.items()} | {
        v: c + j for j, v in enumerate(names)}


def grow_zero(labels, names):
    need(len(set(names)) == len(names) and not labels.keys() & set(names), "fresh zero names")
    return labels | {v: len(labels) + j for j, v in enumerate(names)}


def distance_layers(edges, path):
    need(len(set(path)) == len(path) and edgeset(zip(path, path[1:])) <= edgeset(edges), "witness path")
    distances = dict.fromkeys(path, 0)
    for level in (1, 2):
        layer = {v for e in edges if set(e).intersection(distances) for v in e} - distances.keys()
        distances.update(dict.fromkeys(layer, level))
    return distances


def state(original, labels, c):
    edges = [(u, v) for u, v in original["edges"] if u in labels and v in labels]
    n = len(labels)
    all_rows = ledger(edges, labels)
    low = {v for v, x in labels.items() if x < 7}
    selected = {v for v, x in labels.items() if x >= c}
    selected_rows = [row for row in all_rows if selected.intersection(row["edge"])]
    other_rows = [row for row in all_rows if not selected.intersection(row["edge"])]
    selected_weights = sorted(row["difference"] for row in selected_rows)
    other_weights = sorted(row["difference"] for row in other_rows)
    distances = distance_layers(edges, W)
    need(set(labels) <= set(original["vertices"]) and all(type(x) is int for x in labels.values())
         and sorted(labels.values()) == list(range(n))
         and sorted(row["difference"] for row in all_rows) == list(range(1, n))
         and len(low) == 7 and all((u in low) != (v in low) for u, v in edges),
         "normalized alpha labels and original differences")
    need((labels[H], labels["s:4"], labels[Z]) == (4, 8, 0) and 8 < c < n
         and set(distances) == set(labels) and distances[H] == 0 and distances[Z] == 1,
         "physical ports, both hosts, and original witness")
    need(selected_weights == list(range(c - 4, n)) and other_weights == list(range(1, c - 4)),
         "complete selected and unselected incident multisets")
    return {"labels": labels, "order": n, "alpha_low_size": 7, "low_vertices": sorted(low),
            "high_vertices": sorted(labels.keys() - low),
            "ports": {"L": {"name": H, "label": 4}, "U": {"name": "s:4", "label": 8}, "offsets": [4, 1]},
            "hosts": {H: 4, Z: 0}, "witness": W, "witness_distances": distances,
            "threshold": c, "selected_vertices": sorted(selected),
            "selected_incident_edges": selected_rows, "other_edges": other_rows,
            "selected_spectrum": selected_weights, "other_spectrum": other_weights}


def compare_growth(original, normalized):
    first = ["l:0:0:1", "l:0:0:2"]
    third = ["l:2:0:2"]
    upper_first = grow_upper(BASE, 9, first)
    zero_first = grow_zero(BASE, third)
    upper_then_zero = grow_zero(upper_first, third)
    zero_then_upper = grow_upper(zero_first, 9, first)
    upper_one = grow_upper(BASE, 9, first[:1])
    upper_two = grow_upper(upper_one, 10, first[1:])
    split_then_zero = grow_zero(upper_two, third)
    need(upper_two == upper_first and upper_then_zero == zero_then_upper == split_then_zero == normalized,
         "named operation-order and batch equality")
    need(edgeset(e for e in original["edges"] if any(v in first + third for v in e))
         == edgeset([(H, v) for v in first] + [(Z, v) for v in third]), "prescribed incidence equality")
    return {"parameters": {"q": 3, "t": 3, "K": 5}, "agrees_pointwise": True, "additional_targets": 0,
            "names": {H: first, Z: third},
            "states": {"seed": state(original, BASE, 9), "upper_batch": state(original, upper_first, 11),
                       "zero_first": state(original, zero_first, 9), "upper_then_zero": state(original, upper_then_zero, 11),
                       "zero_then_upper": state(original, zero_then_upper, 11), "upper_one": state(original, upper_one, 10),
                       "upper_two": state(original, upper_two, 11), "split_then_zero": state(original, split_then_zero, 11)}}


def shifted(labels, K):
    return {v: x + K if x >= 7 else x for v, x in labels.items()}


def check_case(q, t, K, original, original_id):
    norm = formula(q, t, K)
    m = K + q + t + 11
    path = [f"s:{j}" for j in range(4, K + 5)]
    suffix = set(path[1:])
    actual_tail = [(u, v) for u, v in original["edges"] if suffix.intersection((u, v))]
    expected_tail = list(zip(path, path[1:]))
    crossing = [(u, v) for u, v in actual_tail if len(suffix.intersection((u, v))) == 1]
    need(original_id["vertices"] == m + 1 and original_id["edges"] == m
         and set(original["vertices"]) - norm.keys() == suffix
         and edgeset(actual_tail) == edgeset(expected_tail)
         and edgeset(crossing) == edgeset([("s:4", "s:5")]), "exact named original suffix")
    normalized = state(original, norm, q + 8)
    need(normalized["order"] == q + t + 12
         and normalized["selected_spectrum"] == list(range(q + 4, q + t + 12)), "exact returned normalized state")
    prefix = shifted(norm, K)
    R, D = list(range(7, K + 7)), list(range(1, K + 1))
    partial = verify_partial(original, prefix)
    need(partial["valid"] and partial["graph_digest"] == original_id["graph_digest"]
         and partial["frontier"] == ["s:4"] and prefix["s:4"] == K + 8
         and sorted(prefix.values()) == list(range(7)) + list(range(K + 7, m + 1))
         and partial["used_differences"] == list(range(K + 1, m + 1))
         and partial["unused_labels"] == R and partial["unused_differences"] == D,
         "both original unused inventories before calling the sequence helper")

    sequence = _nonadjacent_path_labels(K, 7)
    need(len(sequence) == len(path) and sequence[0] == prefix["s:4"]
         and sorted(sequence[1:]) == R, "existing physical port and recurrence range")
    full = prefix | dict(zip(path[1:], sequence[1:]))
    trace = ledger(expected_tail, full)
    all_rows = ledger(original["edges"], full)
    checked = verify_certificate(original, full, original_id["graph_digest"])
    need(checked["valid"] and all(full[v] == x for v, x in prefix.items())
         and sorted(row["difference"] for row in trace) == D
         and checked["edge_differences"] == [row["difference"] for row in all_rows],
         "completed original certificate and prefix preservation")
    return {"parameters": {"q": q, "t": t, "K": K}, "original": original_id,
            "normalized": normalized, "shifted_prefix": prefix, "partial_certificate": partial,
            "interface": {"R": R, "D": D, "physical_port": "s:4", "port_label": K + 8,
                          "crossing_edge": ["s:4", "s:5"]},
            "original_suffix_vertices": path, "path_labels": sequence, "completion_trace": trace,
            "full_labels": full, "original_edge_ledger": all_rows, "certificate": checked,
            "claim": "ordinary gracefulness on this exact named target"}


def check_retained(config):
    smeta, cmeta = config["retained_seed"], config["retained_control"]
    spath, cpath = ROOT / smeta["path"], ROOT / cmeta["path"]
    need(sha(spath) == smeta["sha256_raw"] and sha(cpath) == cmeta["sha256_raw"], "retained byte identities")
    seed, control = read(spath), read(cpath)
    initial, original = seed["original_graph"], control["original_graph"]
    need(seed["classification"] == "SAT" and seed["result"]["witness"] == BASE
         and initial == build_graph([[1], [1], [2], [2], []])
         and seed["original_graph_digest"] == smeta["graph_digest"], "retained seed identity")
    seed_check = verify_certificate(initial, BASE, smeta["graph_digest"])
    need(seed_check["valid"] and seed_check == seed["certificate"], "retained seed certificate")
    seed_report = {"kind": "retained_seed_recheck", "source": smeta, "certificate": seed_check,
                   "normalized": state(initial, BASE, 9), "new_targets": 0, "new_solver_queries": 0}
    q, t, K = cmeta["parameters"]
    need(original == build_graph([[q], [1], [t], [2]] + [[] for _ in range(K + 1)])
         and control["parameters"] == {"t": t, "K": K}, "retained control original")
    norm = formula(q, t, K)
    prefix = shifted(norm, K)
    path = original["spine"][4:]
    sequence = _nonadjacent_path_labels(K, 7)
    saved = control["full_labels"]
    need(norm == control["normalized_extension"] and prefix == control["shifted_prefix"]
         and sequence == control["path_labels"] and [saved[v] for v in path] == sequence
         and saved == prefix | dict(zip(path[1:], sequence[1:])), "retained q=1 pointwise agreement")
    checked = verify_certificate(original, saved, control["original_graph_digest"])
    need(checked["valid"] and checked == control["certificate"], "retained complete certificate")
    return seed_report, {"kind": "retained_completed_control_recheck", "source": cmeta,
                         "pointwise_agreement": True, "certificate": checked,
                         "new_targets": 0, "new_solver_queries": 0}


def check_history(config):
    meta = config["historical_incomplete"]
    p, b = ROOT / meta["raw"], ROOT / meta["bound"]
    need(sha(p) == meta["raw_sha256"] and sha(b) == meta["bound_sha256"], "unchanged historical receipts")
    raw, bound = read(p), read(b)
    expected = {"status": "INCOMPLETE", "reason": "max_nodes", "nodes": 100_000, "exhausted": False,
                "count": None, "count_lower_bound": 0, "witness": None}
    need(all(raw[k] == x for k, x in expected.items()) and bound["result"] == raw
         and bound["classification"] == "INCOMPLETE" and bound["certificate"] is None,
         "preserved historical incomplete status")


def reject_invalid():
    results = []
    for i, minimum in enumerate((1, 2, 2)):
        for value in (True, 2.0, "2", minimum - 1):
            args = [2, 2, 2]
            args[i] = value
            try:
                formula(*args)
            except ValueError as error:
                results.append({"arguments": args, "invalid_index": i, "type": type(value).__name__, "reason": str(error)})
            else:
                raise ValueError("admitted an invalid exact-domain probe")
    return {"rejections": results, "completed_targets": 0, "new_solver_queries": 0}


def main():
    path = HERE / "config.json"
    config = read(path)
    need(config == EXPECTED and config["new_solver_queries"] == 0 and config["enumeration"] is False,
         "declared exact bounded plan")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    diff = subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", "lcl"], cwd=ROOT, text=True)
    need(head == config["starting_commit"] and not diff, "accepted parent and unchanged core")
    check_history(config)
    output = HERE / "validation"
    output.mkdir()
    cap = config["max_result_bytes"]
    inventory = source_inventory(ROOT)
    save_source_snapshot(ROOT, HERE / "source", inventory)
    identity = {"run_id": config["run_id"], "config_sha256_raw": sha(path), "runner_sha256_raw": sha(Path(__file__)),
                "proof_sha256_raw": {name: sha(ROOT / name) for name in PROOFS}, "source": inventory,
                "runtime": {**environment(), "version": sys.version, "executable": sys.executable, "utf8_mode": sys.flags.utf8_mode},
                "limits": {k: config[k] for k in ("workers", "max_vertices", "max_result_bytes")}, "new_solver_queries": 0}
    atomic_json(output / "identity.json", identity, max_bytes=cap)
    original_ids = []
    for i, (q, t, K) in enumerate(config["cases"], 1):
        original = build_graph([[q], [1], [t], [2]] + [[] for _ in range(K + 1)])
        checked = verify_graph(original)
        need(checked["valid"] and checked["n"] <= config["max_vertices"]
             and checked["graph_digest"] == graph_digest(original), "independent original graph preflight")
        original_path = output / "originals" / f"case-{i:02}.json"
        atomic_json(original_path, original, max_bytes=cap)
        original_ids.append({"path": original_path.relative_to(output).as_posix(),
                             "sha256_raw": sha(original_path), "graph_digest": checked["graph_digest"],
                             "vertices": checked["n"], "edges": checked["m"]})
    seed, control = check_retained(config)
    atomic_json(output / "retained_seed.json", seed, max_bytes=cap)
    atomic_json(output / "retained_control.json", control, max_bytes=cap)
    atomic_json(output / "domain_rejections.json", reject_invalid(), max_bytes=cap)
    entries = []
    for i, (params, original_id) in enumerate(zip(config["cases"], original_ids, strict=True), 1):
        original = read(output / original_id["path"])
        case = check_case(*params, original, original_id)
        if params == config["same_target_comparison"]:
            atomic_json(output / "same_target_growth.json", compare_growth(original, case["normalized"]["labels"]),
                        max_bytes=cap)
        certificate = output / f"case-{i:02}.json"
        atomic_json(certificate, case, max_bytes=cap)
        entries.append({"parameters": case["parameters"], "original": original_id,
                        "certificate": certificate.name, "sha256_raw": sha(certificate)})
    linked = ("retained_seed.json", "retained_control.json", "domain_rejections.json", "same_target_growth.json")
    summary = {"status": "PASS", "run_id": config["run_id"], "completed_utc": utc_now(),
               "identity_sha256_raw": sha(output / "identity.json"), "new_completed_targets": len(entries), "cases": entries,
               "auxiliary_sha256_raw": {name: sha(output / name) for name in linked},
               "retained_seed_rechecks": 1, "retained_completed_controls": 1, "domain_rejections": 12,
               "additional_targets_from_comparisons": 0, "new_solver_queries": 0}
    atomic_json(output / "summary.json", summary, max_bytes=cap)
    print(json.dumps({"status": "PASS", "new_completed_targets": len(entries), "retained_seed_rechecks": 1,
                      "retained_completed_controls": 1, "domain_rejections": 12, "new_solver_queries": 0,
                      "vertices": [item["vertices"] for item in original_ids]}))


if __name__ == "__main__":
    main()
