"""Independent arithmetic audit of the same Q1T2 originals and saved certificates."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
CASES = [(2, 2, 2), (2, 3, 3), (3, 2, 4), (3, 3, 5), (4, 5, 2), (5, 4, 5)]
H, Z = "b:0:0", "b:2:0"


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(text.encode()).hexdigest()


def edge_multiset(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def reconstruct(profile):
    spine = [f"s:{i}" for i in range(len(profile))]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = list(zip(spine, spine[1:]))
    for i, section in enumerate(profile):
        for branch, total in enumerate(section):
            parent = f"b:{i}:{branch}"
            roles[parent] = {"kind": "branch", "section": i, "branch": branch}
            edges.append((spine[i], parent))
            for j in range(total):
                leaf = f"l:{i}:{branch}:{j}"
                roles[leaf] = {"kind": "leaf", "section": i, "branch": branch, "leaf": j}
                edges.append((parent, leaf))
    return {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles),
            "edges": sorted(sorted(edge) for edge in edges)}


def match_original(original, profile):
    expected = reconstruct(profile)
    need(all(original[key] == expected[key] for key in ("profile", "spine", "roles"))
         and Counter(original["vertices"]) == Counter(expected["vertices"])
         and edge_multiset(original["edges"]) == edge_multiset(expected["edges"]), "exact original graph")
    return canonical(expected)


def ranked_labels(q, t):
    # Physical vertices in increasing normalized label order.
    low = ["b:2:0", "s:1", "l:1:0:0", "l:3:0:0", "b:0:0", "s:3", "l:3:0:1"]
    high = ["b:3:0", "s:4"]
    high += [f"l:0:0:{j}" for j in range(1, q)]
    high += ["s:0", "l:0:0:0", "b:1:0", "s:2"]
    high += [f"l:2:0:{j}" for j in range(t)]
    return {v: i for i, v in enumerate(low + high)}


def ledger(labels, edges):
    return [{"edge": list(edge), "difference": abs(labels[edge[0]] - labels[edge[1]])}
            for edge in edges]


def witness_distances(vertices, incidences):
    W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
    need(edge_multiset(zip(W, W[1:])) <= edge_multiset(incidences), "original witness edges")
    distances = dict.fromkeys(W, 0)
    for d in (1, 2):
        layer = {v for e in incidences if set(e).intersection(distances) for v in e} - distances.keys()
        distances.update(dict.fromkeys(layer, d))
    need(set(distances) == set(vertices) and distances[H] == 0 and distances[Z] == 1, "witness distances")
    return W, distances


def check_state(saved, original, q, t):
    labels = ranked_labels(q, t)
    n = q + t + 12
    threshold = q + 8
    actual_edges = [(u, v) for u, v in original["edges"] if u in labels and v in labels]
    normalized = reconstruct([[q], [1], [t], [2], []])
    need(set(labels) == set(normalized["vertices"])
         and edge_multiset(actual_edges) == edge_multiset(normalized["edges"])
         and saved["labels"] == labels and sorted(labels.values()) == list(range(n)),
         "normalized original and named label formula")
    low = {v for v, x in labels.items() if x < 7}
    high = set(labels) - low
    chosen = {v for v, x in labels.items() if x >= threshold}
    weights = ledger(labels, actual_edges)
    selected = [row for row in weights if chosen.intersection(row["edge"])]
    other = [row for row in weights if not chosen.intersection(row["edge"])]
    selected_bag = sorted(row["difference"] for row in selected)
    other_bag = sorted(row["difference"] for row in other)
    W, distances = witness_distances(labels, actual_edges)
    need(saved["order"] == n and len(low) == saved["alpha_low_size"] == 7
         and saved["low_vertices"] == sorted(low) and saved["high_vertices"] == sorted(high)
         and all((u in low) != (v in low) for u, v in actual_edges)
         and sorted(row["difference"] for row in weights) == list(range(1, n))
         and saved["ports"] == {"L": {"name": H, "label": labels[H]},
                               "U": {"name": "s:4", "label": labels["s:4"]}, "offsets": [4, 1]}
         and saved["hosts"] == {H: 4, Z: 0} and saved["witness"] == W
         and saved["witness_distances"] == distances and saved["threshold"] == threshold
         and saved["selected_vertices"] == sorted(chosen)
         and saved["selected_incident_edges"] == selected and saved["other_edges"] == other
         and saved["selected_spectrum"] == selected_bag == list(range(q + 4, n))
         and saved["other_spectrum"] == other_bag == list(range(1, q + 4)),
         "actual alpha state, port labels and complete incident predicates")
    return labels


def sequence(K):
    bases = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3)}
    if K in bases:
        return bases[K]
    return (K + 1, 1, K - 1, 0, *(K - 2 - x for x in sequence(K - 3)[1:]))


def graceful(original, labels, report, graph_id):
    rows = ledger(labels, original["edges"])
    m = len(rows)
    need(set(labels) == set(original["vertices"]) and all(type(x) is int for x in labels.values())
         and sorted(labels.values()) == list(range(m + 1))
         and sorted(row["difference"] for row in rows) == list(range(1, m + 1))
         and report["valid"] and not report["errors"]
         and report["edge_differences"] == [row["difference"] for row in rows]
         and report["graph_digest"] == graph_id and (report["n"], report["m"]) == (m + 1, m),
         "original-target certificate by direct arithmetic")
    return rows


def check_case(record, original, graph_id, params):
    q, t, K = params
    n = q + t + K + 12
    need(record["parameters"] == dict(zip(("q", "t", "K"), params))
         and len(original["vertices"]) == n and len(original["edges"]) == n - 1,
         "exact declared completed case")
    norm = check_state(record["normalized"], original, q, t)
    prefix = {v: x + K * (x >= 7) for v, x in norm.items()}
    path = original["spine"][4:]
    suffix = set(path[1:])
    tail_edges = list(zip(path, path[1:]))
    actual = [edge for edge in original["edges"] if suffix.intersection(edge)]
    crossing = [edge for edge in actual if len(suffix.intersection(edge)) == 1]
    need(prefix == record["shifted_prefix"] and set(original["vertices"]) - prefix.keys() == suffix
         and edge_multiset(actual) == edge_multiset(tail_edges)
         and edge_multiset(crossing) == edge_multiset([("s:4", "s:5")])
         and path == record["original_suffix_vertices"], "shifted physical suffix identity")
    used = sorted(abs(prefix[u] - prefix[v]) for u, v in original["edges"] if u in prefix and v in prefix)
    R = sorted(set(range(n)) - set(prefix.values()))
    D = sorted(set(range(1, n)) - set(used))
    partial = record["partial_certificate"]
    need(prefix["s:4"] == K + 8 and R == list(range(7, K + 7)) and D == list(range(1, K + 1))
         and sorted(prefix.values()) == list(range(7)) + list(range(K + 7, n))
         and used == list(range(K + 1, n)) and partial["valid"]
         and partial["graph_digest"] == graph_id and partial["frontier"] == ["s:4"]
         and partial["unused_labels"] == R and partial["unused_differences"] == D
         and partial["used_differences"] == used
         and record["interface"] == {"R": R, "D": D, "physical_port": "s:4", "port_label": K + 8,
                                     "crossing_edge": ["s:4", "s:5"]}, "both unused label and difference inventories")
    full = record["full_labels"]
    translated = [7 + x for x in sequence(K)]
    trace = ledger(full, tail_edges)
    need(translated == [full[v] for v in path] == record["path_labels"]
         and all(full[v] == x for v, x in prefix.items()) and trace == record["completion_trace"]
         and sorted(row["difference"] for row in trace) == D
         and record["claim"] == "ordinary gracefulness on this exact named target",
         "original recurrence, bridge and preserved prefix")
    need(record["original_edge_ledger"] == graceful(original, full, record["certificate"], graph_id),
         "full original edge ledger")


def check_controls(config):
    seed_meta, control_meta = config["retained_seed"], config["retained_control"]
    seed_path, control_path = ROOT / seed_meta["path"], ROOT / control_meta["path"]
    seed, control = read(seed_path), read(control_path)
    need(sha(seed_path) == seed_meta["sha256_raw"] and sha(control_path) == control_meta["sha256_raw"], "retained hashes")
    seed_original, control_original = seed["original_graph"], control["original_graph"]
    seed_check = read(OUT / "retained_seed.json")
    control_check = read(OUT / "retained_control.json")
    seed_id = match_original(seed_original, [[1], [1], [2], [2], []])
    need(seed_check["source"] == seed_meta and seed_id == seed_meta["graph_digest"]
         == seed["original_graph_digest"] and seed["classification"] == "SAT"
         and seed_check["certificate"] == seed["certificate"]
         and seed_check["kind"] == "retained_seed_recheck" and seed_check["new_targets"] == seed_check["new_solver_queries"] == 0,
         "retained seed record")
    labels = check_state(seed_check["normalized"], seed_original, 1, 2)
    need(labels == seed["result"]["witness"], "exact retained seed labels")
    graceful(seed_original, labels, seed["certificate"], seed_id)

    ctrl_id = match_original(control_original, [[1], [1], [3], [2]] + [[] for _ in range(6)])
    norm = ranked_labels(1, 3)
    shift = {v: x + 5 * (x >= 7) for v, x in norm.items()}
    path = control_original["spine"][4:]
    values = [7 + x for x in sequence(5)]
    full = shift | dict(zip(path[1:], values[1:]))
    need(control_meta["parameters"] == [1, 3, 5] and control["parameters"] == {"t": 3, "K": 5}
         and ctrl_id == control["original_graph_digest"] and control_check["source"] == control_meta
         and control["normalized_extension"] == norm and control["shifted_prefix"] == shift
         and control["full_labels"] == full and control["path_labels"] == values
         and control_check["certificate"] == control["certificate"] and control_check["pointwise_agreement"] is True
         and control_check["kind"] == "retained_completed_control_recheck"
         and control_check["new_targets"] == control_check["new_solver_queries"] == 0, "retained q=1 pointwise agreement")
    graceful(control_original, full, control["certificate"], ctrl_id)


def check_same_target(original, final_norm):
    saved = read(OUT / "same_target_growth.json")
    input_map = {"seed": (1, 2), "upper_batch": (3, 2), "zero_first": (1, 3),
                 "upper_then_zero": (3, 3), "zero_then_upper": (3, 3),
                 "upper_one": (2, 2), "upper_two": (3, 2), "split_then_zero": (3, 3)}
    need(set(saved["states"]) == set(input_map)
         and saved["parameters"] == {"q": 3, "t": 3, "K": 5}
         and saved["names"] == {H: ["l:0:0:1", "l:0:0:2"], Z: ["l:2:0:2"]}
         and saved["agrees_pointwise"] is True and saved["additional_targets"] == 0,
         "declared same-target comparisons")
    checked = {name: check_state(saved["states"][name], original, *bounds) for name, bounds in input_map.items()}
    need(checked["upper_batch"] == checked["upper_two"]
         and checked["upper_then_zero"] == checked["zero_then_upper"] == checked["split_then_zero"] == final_norm,
         "both orders and chronological batch pointwise")


def main():
    config_path = HERE / "config.json"
    config = read(config_path)
    identity_path, summary_path = OUT / "identity.json", OUT / "summary.json"
    identity, summary = read(identity_path), read(summary_path)
    caps = {"workers": 1, "max_vertices": 26, "max_result_bytes": 2_000_000}
    need(summary["status"] == "PASS" and summary["new_completed_targets"] == len(summary["cases"]) == 6
         and summary["retained_seed_rechecks"] == summary["retained_completed_controls"] == 1
         and summary["new_solver_queries"] == identity["new_solver_queries"] == config["new_solver_queries"] == 0
         and summary["additional_targets_from_comparisons"] == 0 and config["enumeration"] is False
         and summary["run_id"] == identity["run_id"] == config["run_id"]
         and [tuple(row) for row in config["cases"]] == CASES
         and identity["limits"] == {key: config[key] for key in caps} == caps
         and summary["identity_sha256_raw"] == sha(identity_path)
         and identity["config_sha256_raw"] == sha(config_path) and identity["runner_sha256_raw"] == sha(HERE / "validate.py")
         and all(sha(ROOT / name) == digest for name, digest in identity["proof_sha256_raw"].items())
         and identity["source"]["sha256"] == canonical(identity["source"]["files"])
         and all(sha(HERE / "source" / name) == digest for name, digest in identity["source"]["files"].items())
         and all(sha(OUT / name) == digest for name, digest in summary["auxiliary_sha256_raw"].items()),
         "configuration, proof, snapshot and auxiliary custody")
    hist = config["historical_incomplete"]
    raw, bound = read(ROOT / hist["raw"]), read(ROOT / hist["bound"])
    need(sha(ROOT / hist["raw"]) == hist["raw_sha256"] and sha(ROOT / hist["bound"]) == hist["bound_sha256"]
         and bound["classification"] == raw["status"] == "INCOMPLETE" and raw["reason"] == "max_nodes"
         and raw["nodes"] == 100_000 and raw["exhausted"] is False and raw["count"] is None
         and raw["count_lower_bound"] == 0 and raw["witness"] is None and bound["result"] == raw
         and bound["certificate"] is None, "unchanged historical incomplete receipts")
    check_controls(config)
    rejects = read(OUT / "domain_rejections.json")
    need(summary["domain_rejections"] == len(rejects["rejections"]) == 12
         and rejects["completed_targets"] == rejects["new_solver_queries"] == 0, "focused rejection count")
    for index, minimum in enumerate((1, 2, 2)):
        probes = [r for r in rejects["rejections"] if r["invalid_index"] == index]
        need([type(r["arguments"][index]).__name__ for r in probes] == [r["type"] for r in probes]
             == ["bool", "float", "str", "int"]
             and probes[-1]["arguments"][index] == minimum - 1
             and all(r["arguments"][:index] + r["arguments"][index + 1:] == [2, 2] for r in probes),
             "exact rejection scope")

    cases = []
    for params, entry in zip(CASES, summary["cases"], strict=True):
        q, t, K = params
        path, original_path = OUT / entry["certificate"], OUT / entry["original"]["path"]
        record, original = read(path), read(original_path)
        graph_id = match_original(original, [[q], [1], [t], [2]] + [[] for _ in range(K + 1)])
        need(sha(path) == entry["sha256_raw"] and sha(original_path) == entry["original"]["sha256_raw"]
             and path.stat().st_size <= caps["max_result_bytes"] and original_path.stat().st_size <= caps["max_result_bytes"]
             and graph_id == entry["original"]["graph_digest"] and record["original"] == entry["original"]
             and record["parameters"] == entry["parameters"]
             and entry["original"]["vertices"] == len(original["vertices"]) == sum(params) + 12 <= caps["max_vertices"],
             "same saved case identity and caps")
        check_case(record, original, graph_id, params)
        if list(params) == config["same_target_comparison"]:
            check_same_target(original, record["normalized"]["labels"])
        cases.append({"parameters": entry["parameters"], "graph_digest": graph_id,
                      "certificate_sha256_raw": entry["sha256_raw"], "status": "PASS"})
    audit = {"status": "PASS", "run_id": summary["run_id"] + "-arithmetic-audit",
             "audit_source_sha256_raw": sha(Path(__file__)), "summary_sha256_raw": sha(summary_path),
             "same_new_completed_targets": 6, "same_retained_seed": 1, "same_retained_completed_control": 1,
             "same_domain_rejections": 12, "additional_targets": 0, "additional_queries": 0,
             "runtime": {"python": sys.version, "platform": platform.platform()}, "cases": cases}
    data = (json.dumps(audit, indent=2) + "\n").encode()
    need(len(data) <= caps["max_result_bytes"], "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(data)
    print("PASS: same 6 completed targets, retained seed and control, comparisons and 12 rejections; 0 added targets or queries")


if __name__ == "__main__":
    main()
