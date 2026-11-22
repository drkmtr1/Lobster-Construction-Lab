"""Independent arithmetic and receipt audit. No solver or production imports."""

from collections import Counter
import hashlib
import json
from math import isclose
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
PARENT = "bb7927bcf85d6d32b9bde5b1904c6b43ec6b6a8e"
PROOF = "research/B4_1342_RELAXED_HOST_SEED.md"
RESULT = "research/B4_1342_RELAXED_HOST_SEED_RESULT.md"
TARGET = "evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation/originals/1342.json"
NEG = "evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/normalized-r3-t4.json"
POS = "evidence/validation/B4_UNPADDED_Q1T2_001/validation/retained_seed.json"
QUERY = "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001"
H, Z, U = "b:0:0", "b:2:0", "s:4"
LIMITS = {"workers": 1, "max_vertices": 22, "max_assignment_nodes": 200_000,
          "max_search_seconds": 20, "max_result_bytes": 2_000_000, "max_pairs": 23}
SOURCES = {"lcl/__init__.py", "lcl/verify.py", "lcl/model.py", "pyproject.toml", "requirements.txt"}
BAD = [(True, 18), (2.0, 18), ("2", 18), (1, 18), (9, 18),
       (2, True), (2, 18.0), (2, "18"), (2, 10), (2, 19)]


def require(ok, context):
    if not ok:
        raise AssertionError(context)


def read(path):
    return json.loads(path.read_bytes())


def file_ref(path, root):
    return {"path": path.relative_to(root).as_posix(), "sha256_raw": hashlib.sha256(path.read_bytes()).hexdigest()}


def ref(name, root=OUT):
    return file_ref(root / name, root)


def edge_key(edge):
    return tuple(sorted(edge))


def original(graph, counts):
    spine = [f"s:{i}" for i in range(5)]
    edges = list(zip(spine, spine[1:]))
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    alphabet = [[count] for count in counts] + [[]]
    for i, count in enumerate(counts):
        branch = f"b:{i}:0"
        roles[branch] = {"kind": "branch", "branch": 0, "section": i}
        edges.append((spine[i], branch))
        for j in range(count):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "branch": 0, "leaf": j, "section": i}
            edges.append((branch, leaf))
    require(Counter(graph["vertices"]) == Counter(roles.keys())
            and Counter(map(edge_key, graph["edges"])) == Counter(map(edge_key, edges)),
            "original named vertex or edge multiplicities")
    require(graph["profile"] == alphabet and graph["spine"] == spine and graph["roles"] == roles
            and type(graph["schema_version"]) is int and graph["schema_version"] == 1
            and len(roles) == len(edges) + 1 <= LIMITS["max_vertices"], "original scope or vertex cap")
    canonical = {"profile": alphabet, "spine": spine, "roles": roles, "vertices": sorted(roles),
                 "edges": sorted(map(edge_key, edges))}
    digest = hashlib.sha256(json.dumps(canonical, separators=(",", ":"), sort_keys=True,
                                      ensure_ascii=False).encode("utf-8")).hexdigest()
    depth = {"spine": 0, "branch": 1, "leaf": 2}
    high = {v for v, r in roles.items() if (4 - r["section"] + depth[r["kind"]]) % 2 == 0}
    require(all((u in high) != (v in high) for u, v in edges)
            and U in high and H not in high and Z not in high, "physical alpha orientation")
    return edges, high, digest


def weight(edge, labels):
    u, v = edge
    return abs(labels[u] - labels[v])


def ledger(rows, edges, labels):
    require(Counter(edge_key(row["edge"]) for row in rows) == Counter(map(edge_key, edges)),
            "named ledger multiplicities")
    require(all(row["difference"] == weight(row["edge"], labels) for row in rows), "named ledger differences")


def graceful(graph, high, digest, labels, record, pins):
    n, p = len(graph["vertices"]), len(graph["vertices"]) - len(high)
    low = set(graph["vertices"]) - high
    require(Counter(labels.keys()) == Counter(graph["vertices"]) and all(type(g) is int for g in labels.values())
            and sorted(labels[v] for v in high) == list(range(p, n))
            and sorted(labels[v] for v in low) == list(range(p))
            and {v: labels[v] for v in pins} == pins, "certificate labels, alpha, or physical pins")
    ds = [weight(edge, labels) for edge in graph["edges"]]
    require(sorted(ds) == list(range(1, n)) and record["graph_digest"] == digest
            and record["n"] == n and record["m"] == n - 1 and record["valid"] is True and record["errors"] == []
            and record["edge_differences"] == ds, "certificate differences or original-bound receipt")


def verify_controls(cfg, graph, high, digest):
    receipts = read(OUT / "controls.json")
    negative = read(ROOT / NEG)
    n = receipts["1342"]
    pins = {H: 1, Z: 0, U: 10}
    graceful(graph, high, digest, n["labels"], n["verification"], pins)
    require(negative["labels"] == n["labels"] and negative["original"]["graph_digest"] == digest
            and negative["verification"] == n["verification"] and n["source_certificate"] == ref(NEG, ROOT)
            and n["host_one_excluded_without_search"] is True, "a=1 control source")
    ledger(negative["edge_ledger"], graph["edges"], n["labels"])
    positive = receipts["1122"]
    source = read(ROOT / POS)
    pgraph = read(ROOT / f"{QUERY}/original_graph.json")
    query = read(ROOT / f"{QUERY}/query_record.json")
    edges, p_high, p_digest = original(pgraph, (1, 1, 2, 2))
    labels = positive["labels"]
    graceful(pgraph, p_high, p_digest, labels, positive["verification"], {H: 4, Z: 0, U: 8})
    require(query["classification"] == "SAT" and query["original_graph"] == pgraph
            and query["original_graph_digest"] == p_digest and query["result"]["witness"] == labels
            and source["source"] == {**ref(f"{QUERY}/query_record.json", ROOT), "graph_digest": p_digest}
            and source["certificate"] == query["certificate"] == positive["verification"]
            and source["normalized"]["labels"] == labels, "positive source chain")
    checked_state = {"n": 15, "p": 7, "L": H, "H": H, "U": U, "Z": Z, "x": 4, "y": 1}
    selected = {v for v in p_high if labels[v] >= 9}
    selected_edges = [edge for edge in edges if selected.intersection(edge)]
    other = [edge for edge in edges if not selected.intersection(edge)]
    require(positive["a"] == 4 and positive["c"] == 9 and positive["state"] == checked_state
            and positive["selected_vertices"] == sorted(selected) and positive["high"] == sorted(p_high)
            and positive["low"] == sorted(set(pgraph["vertices"]) - p_high)
            and positive["selected_weights"] == sorted(weight(edge, labels) for edge in selected_edges) == list(range(5, 15))
            and positive["unselected_weights"] == sorted(weight(edge, labels) for edge in other) == list(range(1, 5)),
            "positive control full incidence predicate")
    ledger(positive["edge_ledger"], edges, labels)
    ledger(positive["selected_edges"], selected_edges, labels)
    ledger(positive["unselected_edges"], other, labels)
    path = [H, *pgraph["spine"]]
    role_distance = {"spine": 0, "branch": 1, "leaf": 2}
    distances = {v: role_distance[r["kind"]] - int(v == H or r["kind"] == "leaf" and r["section"] == 0)
                 for v, r in pgraph["roles"].items()}
    require(positive["witness"] == path and positive["witness_distances"] == distances, "positive witness")


def prefilter(edges, high):
    degree = Counter(v for edge in edges for v in edge)
    vertices = sorted(high - {U})
    zero = {v for edge in edges if Z in edge for v in edge if v != Z}
    require(len(vertices) == 9 and zero == {"s:2", *[f"l:2:0:{i}" for i in range(4)]}
            and all(degree[v] == 1 for v in zero - {"s:2"})
            and [degree[v] for v in ("s:0", "s:2", U, "b:1:0", "b:3:0")] == [2, 3, 1, 4, 3],
            "structural pruning premises")
    # Independently enumerate only subsets of physical highs using bit masks.
    choices = [[] for _ in range(10)]
    for mask in range(1, 1 << len(vertices)):
        subset = tuple(v for i, v in enumerate(vertices) if mask & (1 << i))
        choices[len(subset)].append(subset)
    computed = []
    for c in reversed(range(11, 19)):
        k = 19 - c
        for a in range(2, 9):
            fixed = [part for part in choices[k] if "s:2" in part]
            excess = [part for part in fixed if sum(degree[v] for v in part) == k + a]
            slots = [d for d in range(9, 19) if d != 10 and d < c - a]
            admitted = [list(part) for part in sorted(excess) if len(zero.difference(part)) <= len(slots)]
            if not excess:
                rejection = "no size-k subset containing s:2 has the required excess degree"
            elif not admitted:
                rejection = "all size-and-excess subsets lack slots for unselected Z neighbors"
            else:
                rejection = None
            computed.append({"a": a, "c": c, "k": k, "subsets_of_size_k": len(choices[k]), "subsets_with_s2": len(fixed),
                             "subsets_with_required_excess": len(excess), "slots_for_unselected_zero_neighbors": slots,
                             "subsets": admitted, "exclusion": rejection})
    require(read(OUT / "prefilter.json") == {"initial_pairs": 56, "excluded_pairs": 33, "eligible_pairs": 23,
                                           "pairs": computed}, "complete independently filtered pair list")
    return [row for row in computed if row["subsets"]]


def search_outcome(cfg, eligible, digest):
    summary = read(OUT / "search_summary.json")
    require(summary["status"] == "EXHAUSTED_RESTRICTED_NEGATIVE" and summary["limits"] == LIMITS
            and summary["original"] == ref(TARGET, ROOT) and summary["original_digest"] == digest
            and summary["search_runs"] == 1 and summary["historical_replays"] == 0 and summary["exact_solution_count"] is None,
            "bounded summary scope or terminal outcome")
    for name in ("identity", "controls", "guards", "prefilter"):
        require(summary[name] == ref(name + ".json"), "summary evidence references")
    started = read(OUT / "search_started.json")
    require(started == {"run_id": cfg["run_id"], "limits": LIMITS, "prefilter": ref("prefilter.json"),
                        "original_digest": digest}, "one-shot start")
    statuses = summary["pair_statuses"]
    require(len(statuses) == len(eligible) == 23, "all pairs covered")
    folders = OUT / "pairs"
    require({p.name for p in folders.iterdir()} == {f"c{row['c']}-a{row['a']}" for row in eligible},
            "exact attempted pair folders")
    total_nodes, elapsed, subset_count = 0, 0.0, 0
    for row, pair in zip(statuses, eligible):
        a, c, subsets = pair["a"], pair["c"], pair["subsets"]
        folder = folders / f"c{c}-a{a}"
        start = read(folder / "started.json")
        result = read(folder / "result.json")
        require((row["a"], row["c"]) == (a, c) and result == row and row["status"] == "EXHAUSTED"
                and row["reason"] is None and row["seed"] is None and type(row["nodes"]) is int and row["nodes"] >= 0,
                "per-pair outcome or order")
        require(start == {k: row[k] for k in ("a", "c", "starting_nodes", "starting_elapsed_seconds", "remaining_node_cap",
                                            "remaining_time_seconds", "eligible_subsets")}
                and row["eligible_subsets"] == len(subsets) and row["starting_nodes"] == total_nodes
                and row["remaining_node_cap"] == LIMITS["max_assignment_nodes"] - total_nodes
                and isclose(row["remaining_time_seconds"], LIMITS["max_search_seconds"] - row["starting_elapsed_seconds"])
                and elapsed <= row["starting_elapsed_seconds"] <= row["ending_elapsed_seconds"] < LIMITS["max_search_seconds"],
                "pair start, limits or accounting")
        event_time, event_nodes = row["starting_elapsed_seconds"], total_nodes
        event_files = sorted(folder.glob("subset-*.json"))
        require({f.name for f in folder.iterdir()} == {"started.json", "result.json", *(f.name for f in event_files)}
                and len(event_files) == row["subset_events"] == 2 * len(subsets), "subset events and absence of candidate")
        for i, (name, vertex_set) in enumerate(zip(event_files, [part for part in subsets for _ in range(2)])):
            event = read(name)
            require(name.name == f"subset-{i:03d}.json" and event["selected"] == vertex_set
                    and event["status"] == ("STARTED" if i % 2 == 0 else "EXHAUSTED")
                    and event_time <= event["elapsed_seconds"] <= row["ending_elapsed_seconds"]
                    and type(event["total_nodes"]) is int and event_nodes <= event["total_nodes"] <= row["cumulative_nodes"]
                    and (i % 2 or event["total_nodes"] == event_nodes), "subset traversal order and counters")
            event_time, event_nodes = event["elapsed_seconds"], event["total_nodes"]
        total_nodes += row["nodes"]
        elapsed = row["ending_elapsed_seconds"]
        subset_count += len(subsets)
        require(total_nodes == row["cumulative_nodes"] == event_nodes < LIMITS["max_assignment_nodes"], "pair node sum")
    require(total_nodes == summary["assignment_nodes"] and elapsed <= summary["elapsed_seconds"] < LIMITS["max_search_seconds"]
            and {path.name for path in OUT.iterdir()} == {
                "source", "pairs", "controls.json", "guards.json", "identity.json", "prefilter.json",
                "search_started.json", "search_summary.json"}, "global limits or unexpected/positive artifacts")
    return total_nodes, subset_count


def typed(items):
    return [(type(v).__name__, v) for v in items]


def main():
    cfg = read(HERE / "config.json")
    require(cfg["parent"] == PARENT and cfg["limits"] == LIMITS
            and cfg["mode"] == {"first_verified_witness": True, "exact_count": False, "historical_replay": False}
            and cfg["target"] == {"profile": [[1], [3], [4], [2], []], "original": TARGET, "certificate": NEG,
                                  "pins": {Z: 0, U: 10}, "host": H, "a": [2, 8], "c": [11, 18], "low": [0, 8], "high": [9, 18]}
            and cfg["positive_control"] == {"original": f"{QUERY}/original_graph.json", "query": f"{QUERY}/query_record.json",
                                            "certificate": POS}
            and cfg["pair_order"] == "descending c then ascending a" and cfg["subset_order"] == "lexicographic named subsets",
            "exact frozen domain and limits")
    envelope = read(ROOT / TARGET)
    graph = envelope["graph"]
    edges, high, digest = original(graph, (1, 3, 4, 2))
    require(digest == envelope["graph_digest"] and len(edges) == 18 and len(high) == 10, "1342 source identity")
    verify_controls(cfg, graph, high, digest)
    eligible = prefilter(edges, high)
    review = read(HERE / "presearch_review.json")
    independent_counts = {}
    for row in eligible:
        independent_counts.setdefault(str(row["c"]), {})[str(row["a"])] = len(row["subsets"])
    require(review["disposition"] == "ACCEPT" and review["phase"] == "before labeling search"
            and review["eligible_pairs"] == 23 and review["excluded_pairs"] == 33 and review["review_solver_queries"] == 0
            and review["proof_sha256_raw"] == ref(PROOF, ROOT)["sha256_raw"]
            and review["original_sha256_raw"] == ref(TARGET, ROOT)["sha256_raw"]
            and review["independent_subset_counts_by_c_a"] == independent_counts, "reviewed prefilter binding")
    probes = read(OUT / "guards.json")
    require(len(probes) == len(BAD), "guard count")
    for i, (row, pair) in enumerate(zip(probes, BAD)):
        require(typed((row["a"], row["c"])) == typed(pair)
                and row["types"] == [type(v).__name__ for v in pair]
                and row["error"] == ("a must be an exact integer in 2..8" if i < 5 else "c must be an exact integer in 11..18"),
                "pre-search type and range guards")
    identity = read(OUT / "identity.json")
    require(identity["parent"] == PARENT and identity["run_id"] == cfg["run_id"] and identity["limits"] == LIMITS
            and identity["configuration"] == ref("config.json", HERE)
            and identity["presearch_review"] == ref("presearch_review.json", HERE)
            and identity["presearch_proof"] == ref(PROOF, ROOT)
            and identity["task_files"] == [ref(n, HERE) for n in ("run.py", "seed_search.py")]
            and identity["retained"] == [ref(n, ROOT) for n in (TARGET, NEG, f"{QUERY}/original_graph.json",
                                                                 f"{QUERY}/query_record.json", POS)]
            and set(identity["sources_sha256_raw"]) == SOURCES, "raw identity links")
    runtime = identity["runtime"]
    require(runtime["implementation"] == "cpython" and runtime["utf8_mode"] == 1
            and runtime["python"].startswith(("3.12.", "3.13."))
            and runtime["python_executable"] == ".venv/Scripts/python.exe" and runtime["optional_dependencies"] == [],
            "runtime identity")
    for rel, digest_hash in identity["sources_sha256_raw"].items():
        path = OUT / "source" / rel
        require(file_ref(path, OUT)["sha256_raw"] == digest_hash
                and path.read_bytes().replace(b"\r\n", b"\n") == (ROOT / rel).read_bytes().replace(b"\r\n", b"\n"),
                "snapshot source comparison")
    nodes, subsets = search_outcome(cfg, eligible, digest)
    require(all(p.stat().st_size <= LIMITS["max_result_bytes"] for p in OUT.rglob("*") if p.is_file()), "result byte cap")
    require(sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "audit runtime")
    result = {"status": "PASS", "audited_retained_graph_records": 2, "audited_pairs": 56, "excluded_pairs": 33,
              "exhausted_pairs": 23, "audited_exhausted_named_subsets": subsets, "assignment_nodes_in_saved_run": nodes,
              "input_rejections": len(probes), "positive_control_selected_count": 10,
              "new_graph_records": 0, "audit_solver_calls": 0, "audit_labeling_replays": 0,
              "search_summary": ref("search_summary.json"), "result_proof": ref(RESULT, ROOT),
              "auditor": ref("audit.py", HERE)}
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= LIMITS["max_result_bytes"], "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as f:
        f.write(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
