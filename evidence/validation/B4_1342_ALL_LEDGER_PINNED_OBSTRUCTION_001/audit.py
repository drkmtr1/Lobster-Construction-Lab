"""Independent arithmetic and custody audit of the two retained originals."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "41f4e42fb73ab87a93abe1f7c348e8442fdd47b7"
PROOF = "research/B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md"
PRIOR = "evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation"
NEG = "evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation"
POS = "evidence/validation/B4_UNPADDED_Q1T2_001/validation"
QUERY = "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001"
HOST, ZERO, EXIT = "b:0:0", "b:2:0", "s:4"
PINS = {HOST: 1, ZERO: 0, EXIT: 10}
BAD = (True, 10, 19, 12.0, "12")
THRESHOLDS = tuple(range(11, 19))
SOURCES = {"lcl/__init__.py", "lcl/verify.py", "pyproject.toml", "requirements.txt"}
NEG_PATHS = {"original": f"{PRIOR}/originals/1342.json", "source_original": f"{NEG}/originals/normalized-r3-t4.json",
             "certificate": f"{NEG}/normalized-r3-t4.json"}
POS_PATHS = {"original": f"{QUERY}/original_graph.json", "bound_query": f"{QUERY}/query_record.json",
             "certificate": f"{POS}/retained_seed.json", "threshold": 9}
SEEDS = {
    "1342": ((12, 7, 17, 4, 10), (1, 13), (9, 6, 5, 8), (0, 14, 15, 16, 18), (11, 2, 3)),
    "1122": ((9, 1, 12, 5, 8), (4, 10), (11, 2), (0, 13, 14), (7, 3, 6)),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path, root=DATA):
    return {"path": path, "sha256_raw": sha(root / path)}


def edge_key(edge):
    return tuple(sorted(edge))


def named_original(branch_counts, graph):
    spine = [f"s:{j}" for j in range(5)]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, terminal_count in enumerate(branch_counts):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(terminal_count):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
    profile = [[count] for count in branch_counts] + [[]]
    require(Counter(graph["vertices"]) == Counter(roles.keys())
            and Counter(map(edge_key, graph["edges"])) == Counter(map(edge_key, edges)), "original name or edge multiplicity")
    require(graph["spine"] == spine and graph["roles"] == roles and graph["profile"] == profile
            and type(graph["schema_version"]) is int and graph["schema_version"] == 1
            and len(roles) == len(edges) + 1 <= 19, "ordered topology or graph cap")
    canonical = {"vertices": sorted(roles), "edges": sorted(map(edge_key, edges)),
                 "spine": spine, "profile": profile, "roles": roles}
    digest = hashlib.sha256(json.dumps(canonical, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()
    return roles, edges, spine, digest


def weight(edge, labels):
    u, v = edge
    return abs(labels[u] - labels[v])


def checked_ledger(rows, edges, labels):
    require(Counter(edge_key(row["edge"]) for row in rows) == Counter(map(edge_key, edges)), "ledger named multiplicity")
    require(all(row["difference"] == weight(row["edge"], labels) for row in rows), "ledger weight")


def control(name, graph, paths, record, p, pins):
    roles, edges, spine, digest = named_original(tuple(int(s) for s in name), graph)
    # Alpha side is determined by path parity from the pinned high exit.
    depth = {"spine": 0, "branch": 1, "leaf": 2}
    high = sorted(v for v, role in roles.items() if (4 - role["section"] + depth[role["kind"]]) % 2 == 0)
    low = sorted(set(roles) - set(high))
    require(record["bipartition"] == {"high": high, "low": low}
            and all((u in high) != (v in high) for u, v in edges) and EXIT in high, "physical alpha sides")
    seed = SEEDS[name]
    expected = dict(zip(spine, seed[0]))
    for i, row in enumerate(seed[1:]):
        expected[f"b:{i}:0"] = row[0]
        expected.update({f"l:{i}:0:{j}": value for j, value in enumerate(row[1:])})
    labels = record["labels"]
    n = len(roles)
    require(labels == expected and all(type(g) is int for g in labels.values())
            and sorted(labels[v] for v in high) == list(range(p, n))
            and sorted(labels[v] for v in low) == list(range(p))
            and record["pins"] == pins == {v: labels[v] for v in pins}, "retained labels or pin values")
    require(record["state"] == {"n": n, "p": p, "x": pins[HOST], "y": pins[EXIT] - p, "L": HOST, "U": EXIT}
            and record["original"] == {**ref(paths["original"], ROOT), "graph_digest": digest}
            and record["source_certificate"] == ref(paths["certificate"], ROOT), "control state or raw binding")
    distances = {v: depth[role["kind"]] - int(v == HOST or role["kind"] == "leaf" and role["section"] == 0)
                 for v, role in roles.items()}
    require(record["witness"] == {"path": [HOST, *spine], "distances": distances}
            and distances[HOST] == 0 and distances[ZERO] == 1, "physical witness")
    differences = [weight(edge, labels) for edge in graph["edges"]]
    require(sorted(differences) == list(range(1, n)), "retained graceful differences")
    checked_ledger(record["edge_ledger"], edges, labels)
    receipt = record["verification"]
    require(receipt["valid"] is True and receipt["errors"] == []
            and receipt["graph_digest"] == digest and receipt["n"] == n and receipt["m"] == n - 1
            and receipt["edge_differences"] == differences, "original verifier receipt")
    return high, edges, labels, digest


def check_proof_data(record, negative, base):
    high, edges, labels, digest = base
    m = len(edges)
    n = m + 1
    require(record["original"] == negative["original"] and record["pin_scope"] == PINS
            and record["alpha_labels"] == {"low": [0, 8], "high": [9, 18]}
            and (len(high), n - len(high), n, m) == (10, 9, 19, 18), "pinned claim domain")
    incidence = {v: [] for v in high}
    for u, v in edges:
        upper, lower = (u, v) if u in high else (v, u)
        require(upper in incidence and lower not in incidence, "exact-one-high edge invariant")
        incidence[upper].append(lower)
    degrees = Counter(v for edge in edges for v in edge)
    eligible = {v: degrees[v] for v in high if v != EXIT}
    high_degree = {v: degrees[v] for v in high}
    ones = sorted(v for v in eligible if degrees[v] == 1)
    twos = [v for v in eligible if degrees[v] == 2]
    bigger = sorted(v for v in eligible if degrees[v] > 2)
    zero_neighbors = sorted(v for v in high if ZERO in incidence[v])
    zero_terminals = sorted(set(zero_neighbors).intersection(ones))
    require(sum(high_degree.values()) == m and high_degree[EXIT] == 1 and sorted(eligible.values()) == [1]*5 + [2, 3, 3, 4]
            and twos == ["s:0"] and bigger == ["b:1:0", "b:3:0", "s:2"]
            and zero_neighbors == [*zero_terminals, "s:2"]
            and zero_terminals == [f"l:2:0:{j}" for j in range(4)]
            and all(incidence[v] == [ZERO] for v in zero_terminals)
            and "s:0" not in zero_neighbors, "census or descending premise")
    census = {"high_degree": high_degree, "high_incidence": {v: sorted(adj) for v, adj in incidence.items()},
              "eligible_degree": eligible, "sorted_eligible_degrees": sorted(eligible.values()), "degree_one_vertices": ones,
              "degree_two_vertex": twos[0], "degree_above_two_vertices": bigger,
              "zero_neighbors": zero_neighbors, "zero_terminal_neighbors": zero_terminals, "unselected_exit": EXIT}
    require(record["census"] == census, "saved census")
    allowed = tuple(range(PINS[EXIT] + 1, n))
    require(allowed == THRESHOLDS and [row["c"] for row in record["threshold_cases"]] == list(allowed), "strict threshold band")
    bounds = {}
    for c, row in zip(allowed, record["threshold_cases"]):
        k = n - c
        band = list(range(c - PINS[HOST], n))
        require(row["selected_vertex_count"] == k and row["required_edge_count"] == len(band) == k + 1
                and row["required_spectrum"] == band, "necessary selected cardinality")
        if c <= 12:
            # Omit the largest available degrees to bound a k-vertex sum from below.
            size_of_omission = len(eligible) - k
            minimum = sum(eligible.values()) - sum(sorted(eligible.values(), reverse=True)[:size_of_omission])
            require(row["least_degree_sum"] == minimum > k + 1 and row["reason"] == "degree lower bound", "degree minimum")
            bounds[str(c)] = minimum
        else:
            # In excess-degree units (d-1), k+1 has one unit above k.
            extra = len(band) - k
            require(extra == 1 and row["reason"] == "degree pattern contradicts descending differences"
                    and row["required_degree_two"] == twos[0] and row["required_number_degree_one"] == k - 1
                    and row["excluded_degree_above_two"] == bigger and row["forced_terminal_neighbors"] == zero_terminals
                    and row["descending_differences"] == list(reversed(range(c, n))), "conditional degree and descent record")
    require(bounds == {"11": 13, "12": 10} and min(allowed) > 8 and m - 0 == 18
            and EXIT not in eligible and "s:2" in bigger, "descending base and edge-source conditions")
    descending = record["descending"]
    require(descending == {
        "zero_host": ZERO, "base_difference": m, "base_pair": [0, m], "excluded_nonterminal_zero_neighbor": "s:2",
        "higher_endpoint_rule": "larger forced terminals contribute only their own differences to zero",
        "equal_endpoint_rule": "high label j is required for difference j and forces low label zero",
        "contradicts_required_vertex": twos[0]}, "recorded descending implication")
    # In the basis (1, h, h(h-1)/2), one uniquely shifted edge contributes
    # h. Fresh differences start at c-1 and the required new band at m+1.
    # Their quadratic coefficients cancel, and the linear coefficients
    # differ by s_c + c - (m + 2) = s_c + c - 20.
    original_sum = sum(range(1, n))
    require(original_sum == sum(weight(edge, labels) for edge in edges) == 171 and n == 19 and m + 2 == 20
            and record["sum_identity"] == {"old_sum": original_sum, "basis": ["1", "h", "h*(h-1)/2"],
                "actual_coefficients": [original_sum, "s_c+c-1", 1], "required_coefficients": [original_sum, n, 1],
                "difference": "h*(s_c+c-20)", "domain": "integer h>=1"}, "all-positive symbolic sum identity")
    return bounds


def typed(items):
    return [(type(v).__name__, v) for v in items]


def main():
    run = "B4-1342-ALL-LEDGER-PINNED-OBSTRUCTION-001-20261122"
    config = read(HERE / "config.json")
    require(config == {"run_id": run, "parent": PARENT, "workers": 1, "max_vertices": 19, "max_result_bytes": 2_000_000,
                       "solver_queries": 0, "labeling_enumeration": 0, "historical_replay": 0, "new_graph_records": 0,
                       "new_graceful_targets": 0, "new_attempted_enlarged_graphs": 0, "pins": PINS,
                       "thresholds": list(THRESHOLDS), "invalid_thresholds": list(BAD),
                       "1342": NEG_PATHS, "1122": POS_PATHS}
            and typed(config["invalid_thresholds"]) == typed(BAD), "exact declared configuration")
    neg = read(DATA / "retained_1342.json")
    original = read(ROOT / NEG_PATHS["original"])
    base = control("1342", original["graph"], NEG_PATHS, neg, 9, PINS)
    digest = base[3]
    ncert = read(ROOT / NEG_PATHS["certificate"])
    require(original == read(ROOT / NEG_PATHS["source_original"]) and original["graph_digest"] == digest
            and neg["source_original"] == ref(NEG_PATHS["source_original"], ROOT)
            and ncert["original"]["sha256_raw"] == neg["source_original"]["sha256_raw"]
            and ncert["original"]["graph_digest"] == digest and ncert["labels"] == neg["labels"]
            and ncert["edge_ledger"] == neg["edge_ledger"] and ncert["verification"] == neg["verification"],
            "1342 certificate chain")
    pos = read(DATA / "retained_1122.json")
    graph = read(ROOT / POS_PATHS["original"])
    p_high, p_edges, p_labels, p_digest = control("1122", graph, POS_PATHS, pos, 7, {HOST: 4, ZERO: 0, EXIT: 8})
    saved, query = read(ROOT / POS_PATHS["certificate"]), read(ROOT / POS_PATHS["bound_query"])
    require(query["original_graph"] == graph and query["classification"] == "SAT"
            and query["original_graph_digest"] == p_digest and query["result"]["witness"] == p_labels
            and query["certificate"] == saved["certificate"] == pos["verification"]
            and saved["source"] == {**ref(POS_PATHS["bound_query"], ROOT), "graph_digest": p_digest}
            and pos["source_query_record"] == ref(POS_PATHS["bound_query"], ROOT)
            and saved["normalized"]["labels"] == p_labels, "1122 certificate chain")
    c = POS_PATHS["threshold"]
    selected = sorted(v for v in p_high if p_labels[v] >= c)
    selected_edges = [edge for edge in p_edges if len(set(edge).intersection(selected)) == 1]
    weights = sorted(weight(edge, p_labels) for edge in selected_edges)
    predicate = pos["predicate"]
    require(p_labels[EXIT] < c <= 14 and len(selected_edges) == 10
            and weights == list(range(c - p_labels[HOST], 15)) == saved["normalized"]["selected_spectrum"]
            and predicate["c"] == c and predicate["selected_vertices"] == selected
            and predicate["selected_spectrum"] == weights, "positive incidence band")
    checked_ledger(predicate["selected_ledger"], selected_edges, p_labels)

    bounds = check_proof_data(read(DATA / "structural.json"), neg, base)
    probes = read(DATA / "invalid_thresholds.json")
    require(typed(row["input"] for row in probes) == typed(BAD), "invalid threshold inputs")
    require(all(row["type"] == type(row["input"]).__name__ and row["evaluation_calls"] == 0
                and row["error"] == "c must be an exact integer from 11 through 18" for row in probes), "pre-evaluation guards")
    ident = read(DATA / "identity.json")
    runtime = ident["runtime"]
    require(ident["run_id"] == run and ident["parent"] == PARENT and ident["proof"] == ref(PROOF, ROOT)
            and runtime["implementation"] == "cpython" and runtime["utf8_mode"] == 1
            and runtime["python"].startswith(("3.12.", "3.13.")) and runtime["python_executable"] == ".venv/Scripts/python.exe"
            and runtime["optional_dependencies"] == [] and bool(runtime["platform"]), "source or runtime identity")
    for name, k in (("config.json", "config_sha256_raw"), ("validate.py", "runner_sha256_raw"), ("audit.py", "audit_sha256_raw")):
        require(ident[k] == sha(HERE / name), "executable evidence hash")
    raw_paths = [*NEG_PATHS.values(), *(v for v in POS_PATHS.values() if isinstance(v, str))]
    require(ident["retained_sha256_raw"] == {path: sha(ROOT / path) for path in raw_paths}
            and set(ident["source_sha256_raw"]) == SOURCES, "retained inventory or bindings")
    for rel, digest in ident["source_sha256_raw"].items():
        snapshot = DATA / "source" / rel
        require(sha(snapshot) == digest
                and snapshot.read_bytes().replace(b"\r\n", b"\n") == (ROOT / rel).read_bytes().replace(b"\r\n", b"\n"),
                "executable source snapshot")
    summary = read(DATA / "summary.json")
    require(summary == {"status": "PASS", "run_id": run, "identity": ref("identity.json"),
                        "retained_controls": [ref("retained_1342.json"), ref("retained_1122.json")],
                        "structural": ref("structural.json"), "invalid_thresholds": ref("invalid_thresholds.json"),
                        "distinct_graph_records": 2, "threshold_cases": 8, "input_rejections": 5,
                        "solver_queries": 0, "labeling_enumeration": 0, "historical_replay": 0, "new_graph_records": 0,
                        "new_graceful_targets": 0, "new_attempted_enlarged_graphs": 0}, "record scope")
    require({p.name for p in DATA.iterdir()} == {"source", "identity.json", "retained_1342.json", "retained_1122.json",
                                                  "structural.json", "invalid_thresholds.json", "summary.json"}
            and all(p.stat().st_size <= 2_000_000 for p in DATA.rglob("*") if p.is_file()), "result byte cap or unexpected records")
    require(sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "audit runtime")
    result = {"status": "PASS", "run_id": run, "same_retained_graphs": 2, "same_structural_data": ref("structural.json"),
              "threshold_cases": 8, "guard_rejections": 5, "minimum_counts": bounds, "positive_selected_count": 10,
              "new_graph_records": 0, "new_attempted_assignments": 0, "labeling_enumeration": 0, "solver_queries": 0}
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= 2_000_000, "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as f:
        f.write(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
