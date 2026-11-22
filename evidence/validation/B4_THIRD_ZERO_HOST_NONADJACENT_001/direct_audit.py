"""Independent arithmetic audit of the four saved B4 completions."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "direct_checks"
ROOT = HERE.parents[2]
EXPECTED_CASES = [(2, 2), (3, 3), (4, 4), (3, 5)]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def named_edges(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def original_for(t, K):
    spine = tuple(f"s:{i}" for i in range(K + 5))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = list(zip(spine, spine[1:]))
    for i, count in enumerate((1, 1, t, 2)):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(count):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
    return {"profile": [[1], [1], [t], [2], *([[]] * (K + 1))],
            "spine": list(spine), "roles": roles,
            "vertices": sorted(roles), "edges": sorted(sorted(edge) for edge in edges)}


def canonical_digest(graph):
    data = json.dumps(graph, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def translated_sequence(K):
    # Direct recurrence as written in the proof, independent of the generator loop.
    bases = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3)}
    if K in bases:
        return tuple(7 + x for x in bases[K])
    earlier = translated_sequence(K - 3)
    return (K + 8, 8, K + 6, 7, *(K + 12 - x for x in earlier[1:]))


def audit_case(case, base, params):
    t, K = params
    graph = original_for(t, K)
    saved = case["original_graph"]
    digest = canonical_digest(graph)
    require(case["parameters"] == {"t": t, "K": K} and saved["profile"] == graph["profile"]
            and saved["spine"] == graph["spine"] and saved["roles"] == graph["roles"]
            and Counter(saved["vertices"]) == Counter(graph["vertices"])
            and named_edges(saved["edges"]) == named_edges(graph["edges"])
            and case["original_graph_digest"] == digest, "retained original named graph")
    path = graph["spine"][4:]
    future = set(path[1:])
    suffix_edges = list(zip(path, path[1:]))
    actual = [e for e in graph["edges"] if future.intersection(e)]
    crossing = [e for e in actual if len(future.intersection(e)) == 1]
    require(named_edges(actual) == named_edges(suffix_edges)
            and named_edges(crossing) == named_edges([("s:4", "s:5")])
            and case["path_vertices"] == path, "original path and physical crossing")

    normalized = case["normalized_extension"]
    expected = dict(base)
    for label in range(15, t + 13):
        expected[f"l:2:0:{label - 13}"] = label
    require(normalized == expected and set(graph["vertices"]) - normalized.keys() == future
            and sorted(normalized.values()) == list(range(t + 13))
            and case["normalized_ports"] == {"b:0:0": 4, "s:4": 8}
            and case["normalized_port_offsets"] == [4, 1], "normalized seed preservation, ports and exact leaves")
    normalized_edges = [e for e in saved["edges"] if not future.intersection(e)]
    normalized_diff = [abs(normalized[u] - normalized[v]) for u, v in normalized_edges]
    require(sorted(normalized_diff) == list(range(1, t + 13))
            and case["normalized_edge_differences"] == normalized_diff
            and all((normalized[u] < 7) != (normalized[v] < 7) for u, v in normalized_edges),
            "normalized alpha spectrum")

    shifted = case["shifted_prefix"]
    require(shifted == {v: x + K * (x >= 7) for v, x in expected.items()}, "high shift")
    m = t + K + 12
    used = sorted(abs(shifted[u] - shifted[v]) for u, v in normalized_edges)
    R = sorted(set(range(m + 1)) - set(shifted.values()))
    D = sorted(set(range(1, m + 1)) - set(used))
    require(used == list(range(K + 1, m + 1))
            and sorted(shifted.values()) == list(range(7)) + list(range(K + 7, m + 1))
            and R == list(range(7, K + 7)) and D == list(range(1, K + 1))
            and shifted["s:4"] == K + 8
            and case["suffix_interface"] == {"unused_labels": R, "unused_differences": D, "port_vertex": "s:4",
                                             "port_label": K + 8, "crossing_edge": ["s:4", "s:5"]},
            "exact used and unused inventories")
    partial = case["partial_certificate"]
    require(partial["valid"] and partial["graph_digest"] == digest and partial["frontier"] == ["s:4"]
            and partial["used_differences"] == used and partial["unused_labels"] == R
            and partial["unused_differences"] == D, "partial check receipt")

    final = case["full_labels"]
    values = translated_sequence(K)
    require(case["path_labels"] == list(values) == [final[v] for v in path]
            and sorted(values[1:]) == R and all(final[v] == x for v, x in shifted.items()),
            "independent recurrence and prefix preservation")
    steps = [{"edge": [u, v], "new_label": final[v], "difference": abs(final[u] - final[v])}
             for u, v in suffix_edges]
    require(case["completion_trace"] == steps and sorted(step["difference"] for step in steps) == D,
            "original edges and difference inventory of suffix")
    if K == 5:
        bridge = steps[3]
        require(bridge["edge"] == ["s:7", "s:8"] and bridge["difference"] == 2, "first recursive bridge")
    require(len(graph["edges"]) == m and set(final) == set(graph["vertices"])
            and all(type(x) is int for x in final.values())
            and sorted(final.values()) == list(range(m + 1)), "full labels")
    weights = [abs(final[u] - final[v]) for u, v in saved["edges"]]
    cert = case["certificate"]
    require(sorted(weights) == list(range(1, m + 1)) and cert["valid"]
            and cert["edge_differences"] == weights and cert["graph_digest"] == digest
            and (cert["n"], cert["m"]) == (m + 1, m)
            and case["claim"] == "ordinary gracefulness on this exact named target", "original graceful certificate")

    W = ["b:0:0", *graph["spine"][:5]]
    extended = W + path[1:]
    require(case["witness"] == W and case["extended_witness"] == extended
            and named_edges(zip(extended, extended[1:])) <= named_edges(graph["edges"]),
            "extended witness incidences")
    distances = dict.fromkeys(extended, 0)
    for level in (1, 2):
        boundary = {v for e in graph["edges"] if set(e).intersection(distances) for v in e} - distances.keys()
        distances.update(dict.fromkeys(boundary, level))
    require(distances == case["witness_distances"] and set(distances) == set(final)
            and distances["b:2:0"] == 1, "actual witness distances")
    return digest


def main():
    query = read(HERE / "query_record.json")
    seed_audit = read(HERE / "audit_result.json")
    preflight = read(HERE / "preflight.json")
    plan = read(HERE / "config.json")["conditional_direct_checks"]
    identity = read(OUTPUT / "identity.json")
    summary_path = OUTPUT / "summary.json"
    summary = read(summary_path)
    require(summary["status"] == "PASS" and summary["completed_targets"] == len(summary["cases"]) == 4
            and summary["run_id"] == identity["run_id"] and summary["new_queries"] == 0
            and summary["identity_sha256_raw"] == sha(OUTPUT / "identity.json")
            and identity["seed_query_sha256_raw"] == sha(HERE / "query_record.json")
            and identity["seed_audit_sha256_raw"] == sha(HERE / "audit_result.json")
            and identity["runner_sha256_raw"] == sha(HERE / "direct.py")
            and identity["config_sha256_raw"] == sha(HERE / "config.json")
            and identity["proof_sha256_raw"] == sha(ROOT / identity["proof"])
            and identity["source"] == preflight["source"]
            and all(sha(HERE / "source" / name) == digest for name, digest in identity["source"]["files"].items())
            and identity["limits"] == plan == preflight["conditional_targets"]
            and [tuple(row) for row in plan["cases"]] == EXPECTED_CASES
            and plan["workers"] == 1 and plan["max_vertices"] == 21
            and plan["max_result_bytes"] == 2_000_000 and plan["search"] is False
            and query["classification"] == "SAT" and query["certificate"]["valid"]
            and seed_audit["status"] == "PASS", "fixed four-case identity and verified seed")
    cases = []
    for params, entry in zip(EXPECTED_CASES, summary["cases"], strict=True):
        path = OUTPUT / entry["file"]
        record = read(path)
        require(entry["sha256_raw"] == sha(path) and entry["parameters"] == record["parameters"]
                and path.stat().st_size == entry["bytes"] <= plan["max_result_bytes"]
                and entry["vertices"] == sum(params) + 13 <= plan["max_vertices"], "case custody and caps")
        digest = audit_case(record, query["result"]["witness"], params)
        require(digest == entry["original_graph_digest"], "case digest")
        cases.append({"parameters": record["parameters"], "original_graph_digest": digest,
                      "case_sha256_raw": entry["sha256_raw"], "status": "PASS"})

    report = {"status": "PASS", "run_id": identity["run_id"] + "-audit",
              "summary_sha256_raw": sha(summary_path), "audit_sha256_raw": sha(Path(__file__)),
              "same_completed_targets": len(cases), "additional_completed_targets": 0, "new_queries": 0,
              "runtime": {"python": sys.version, "platform": platform.platform()}, "cases": cases}
    encoded = (json.dumps(report, indent=2) + "\n").encode()
    require(len(encoded) <= plan["max_result_bytes"], "audit size")
    with (HERE / "direct_audit_result.json").open("xb") as out:
        out.write(encoded)
    print("PASS: same 4 saved completed targets; 0 additional targets or queries")


if __name__ == "__main__":
    main()
