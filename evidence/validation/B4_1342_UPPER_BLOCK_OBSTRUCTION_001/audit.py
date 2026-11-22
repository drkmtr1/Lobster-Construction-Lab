"""Independent standard-library check of the three declared graph records."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "c83ae3b11a6bc03189dc44653881137fc014c72a"
PROOF = "research/B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md"
NEG = "evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation"
POS = "evidence/validation/B4_UNPADDED_Q1T2_001/validation"
SEED = "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001"
PROFILES = {"1342": (1, 3, 4, 2), "1122": (1, 1, 2, 2), "2342": (2, 3, 4, 2)}
HOST, EXIT, ZERO, LEAF = "b:0:0", "s:4", "b:2:0", "l:0:0:1"
ORDER = tuple(range(11, 19))
EXPECTED = (13, 10, 8, 7, 6, 5, 4, 1)
BAD = (True, 10, 19, 12.0, "12")
SOURCES = {"lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt"}
LABELS = {
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


def ref(relative):
    return {"path": relative, "sha256_raw": sha(DATA / relative)}


def source(relative):
    return {"path": relative, "sha256_raw": sha(ROOT / relative)}


def key(edge):
    return tuple(sorted(edge))


def multiplicities(edges):
    return Counter(key(edge) for edge in edges)


def topology(branches):
    spine = [f"s:{i}" for i in range(5)]
    edges = list(zip(spine[:-1], spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, count in enumerate(branches):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(count):
            terminal = f"l:{i}:0:{j}"
            roles[terminal] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, terminal))
    return spine, roles, edges, [[count] for count in branches] + [[]]


def original(name):
    path = f"originals/{name}.json"
    saved = read(DATA / path)
    graph = saved["graph"]
    spine, roles, edges, profile = topology(PROFILES[name])
    require(Counter(graph["vertices"]) == Counter(roles.keys())
            and multiplicities(graph["edges"]) == multiplicities(edges), "original undirected multiplicities")
    require(graph["profile"] == profile and graph["spine"] == spine and graph["roles"] == roles
            and type(graph["schema_version"]) is int and graph["schema_version"] == 1, "ordered sections or roles")
    canonical = {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles),
                 "edges": sorted(map(key, edges))}
    digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":"),
                                      ensure_ascii=False).encode("utf-8")).hexdigest()
    require(digest == saved["graph_digest"] and len(roles) == len(edges) + 1 <= 20, "graph digest or vertex cap")
    return graph, {**ref(path), "graph_digest": digest}


def weight(edge, labels):
    u, v = edge
    return abs(labels[u] - labels[v])


def check_ledger(rows, edges, labels):
    require(Counter(key(row["edge"]) for row in rows) == multiplicities(edges), "ledger named multiplicities")
    require(all(row["difference"] == weight(row["edge"], labels) for row in rows), "ledger weight")


def anchored_control(record, graph, original_ref, name, p, a, exit_label):
    n = len(graph["vertices"])
    labels = record["labels"]
    seed = LABELS[name]
    expected = dict(zip(graph["spine"], seed[0]))
    for i, row in enumerate(seed[1:]):
        expected[f"b:{i}:0"] = row[0]
        expected.update({f"l:{i}:0:{j}": v for j, v in enumerate(row[1:])})
    require(record["original"] == original_ref and labels == expected
            and all(type(value) is int for value in labels.values())
            and sorted(labels.values()) == list(range(n)), "wrong retained labels")
    require(record["anchors"] == {HOST: a, EXIT: exit_label, ZERO: 0}
            and {v: labels[v] for v in record["anchors"]} == record["anchors"]
            and record["state"] == {"n": n, "p": p, "x": a, "y": exit_label - p,
                                    "L": HOST, "H": HOST, "U": EXIT, "Z": ZERO}, "physical state")
    lows = sorted(["s:1", "s:3", HOST, ZERO, *[f"l:1:0:{j}" for j in range(PROFILES[name][1])],
                   "l:3:0:0", "l:3:0:1"])
    highs = sorted(set(graph["vertices"]) - set(lows))
    require(record["alpha"] == {"low": lows, "high": highs}
            and sorted(labels[v] for v in lows) == list(range(p))
            and sorted(labels[v] for v in highs) == list(range(p, n))
            and all((u in lows) != (v in lows) for u, v in graph["edges"]), "actual alpha cut")
    distances = {}
    for v, role in graph["roles"].items():
        if v == HOST or role["kind"] == "spine":
            distances[v] = 0
        elif role["kind"] == "branch" or role["section"] == 0:
            distances[v] = 1
        else:
            distances[v] = 2
    require(record["witness"] == {"path": [HOST, *graph["spine"]], "distances": distances}
            and distances[HOST] == 0 and distances[ZERO] == 1, "witness distances")
    differences = [weight(edge, labels) for edge in graph["edges"]]
    require(sorted(differences) == list(range(1, n)), "retained original multiset")
    check_ledger(record["edge_ledger"], graph["edges"], labels)
    receipt = record["verification"]
    require(receipt["valid"] is True and receipt["errors"] == []
            and receipt["graph_digest"] == original_ref["graph_digest"] and receipt["n"] == n and receipt["m"] == n - 1
            and receipt["edge_differences"] == differences, "retained unchanged-checker receipt")
    return labels


def incidence(row, graph, labels, threshold):
    p = 9 if len(graph["vertices"]) == 19 else 7
    # Use the unique high endpoint to partition the independently checked edges.
    by_high = {v: [] for v, label in labels.items() if label >= p}
    for u, v in graph["edges"]:
        head = u if labels[u] > labels[v] else v
        by_high[head].append((u, v))
    selected = {v: labels[v] for v in by_high if labels[v] >= threshold}
    edges = [edge for v in selected for edge in by_high[v]]
    actual = sorted(weight(edge, labels) for edge in edges)
    required = list(range(threshold - labels[HOST], len(graph["edges"]) + 1))
    require(row["c"] == threshold and row["selected_vertices"] == selected
            and row["actual_count"] == len(edges) and row["required_count"] == len(required)
            and row["selected_multiset"] == actual and row["required_multiset"] == required
            and row["matches"] is (Counter(actual) == Counter(required)), "complete incidence predicate")
    check_ledger(row["selected_edges"], edges, labels)
    return selected, len(edges)


def reproduce_attempt(saved, expanded, binding, labels, threshold, chosen, count):
    # Move the set certified by the independent high-endpoint calculation.
    lifted = labels.copy()
    for vertex in chosen:
        lifted[vertex] += 1
    lifted[LEAF] = threshold
    require(saved["c"] == threshold and saved["h"] == 1 and saved["original"] == binding
            and saved["labels"] == lifted and all(type(g) is int for g in saved["labels"].values())
            and sorted(lifted.values()) == saved["complete_label_alphabet"] == list(range(20))
            and saved["anchors"] == {HOST: 1, EXIT: 10, ZERO: 0}
            and {v: lifted[v] for v in saved["anchors"]} == saved["anchors"]
            and all((lifted[u] < 9) != (lifted[v] < 9) for u, v in expanded["edges"]), "adverse exact named assignment")
    check_ledger(saved["edge_ledger"], expanded["edges"], lifted)
    weights = [weight(edge, lifted) for edge in expanded["edges"]]
    observed, required = Counter(weights), Counter(range(1, 20))
    missing = sorted((required - observed).keys())
    repeated = sorted((observed - required).keys())
    require(saved["difference_multiset"] == sorted(weights)
            and saved["missing"] == [{"difference": d, "multiplicity": observed[d]} for d in missing]
            and saved["repeated"] == [{"difference": d, "multiplicity": observed[d]} for d in repeated]
            and missing and repeated, "adverse missing or repeated multiplicities")
    total = sum(weights)
    require(saved["actual_difference_sum"] == total == 171 + count + threshold - 1
            and saved["required_difference_sum"] == sum(required) == 190
            and saved["signed_defect"] == total - 190 == count + threshold - 20, "adverse total")
    receipt = saved["verification"]
    require(receipt["valid"] is False and receipt["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
            and receipt["n"] == 20 and receipt["m"] == 19 and receipt["graph_digest"] == binding["graph_digest"]
            and receipt["edge_differences"] == weights, "adverse unchanged-checker receipt")


def typed(values):
    return [(type(v).__name__, v) for v in values]


def main():
    config = read(HERE / "config.json")
    run = "B4-1342-UPPER-BLOCK-OBSTRUCTION-001-20261122"
    neg_cert, neg_original = f"{NEG}/normalized-r3-t4.json", f"{NEG}/originals/normalized-r3-t4.json"
    pos_cert, pos_original, query = f"{POS}/retained_seed.json", f"{SEED}/original_graph.json", f"{SEED}/query_record.json"
    require(config == {"run_id": run, "parent": PARENT, "workers": 1, "max_vertices": 20, "max_result_bytes": 2_000_000,
                       "solver_queries": 0, "labeling_enumeration": 0, "historical_replay": 0, "batch": 1,
                       "negative": {"certificate": neg_cert, "original": neg_original, "profile": [[1], [3], [4], [2], []],
                                    "p": 9, "host_label": 1, "exit_label": 10},
                       "positive": {"certificate": pos_cert, "original": pos_original, "bound_query": query,
                                    "profile": [[1], [1], [2], [2], []], "p": 7, "host_label": 4, "exit_label": 8, "threshold": 9},
                       "expanded_profile": [[2], [3], [4], [2], []], "thresholds": list(ORDER),
                       "invalid_thresholds": list(BAD)} and typed(config["invalid_thresholds"]) == typed(BAD), "frozen configuration")
    ngraph, nref = original("1342")
    pgraph, pref = original("1122")
    expanded, expanded_ref = original("2342")
    require(Counter(expanded["vertices"]) == Counter(ngraph["vertices"]) + Counter([LEAF])
            and multiplicities(expanded["edges"]) == multiplicities(ngraph["edges"]) + multiplicities([(HOST, LEAF)])
            and all(expanded["roles"][v] == role for v, role in ngraph["roles"].items()), "exact single expanded original")
    negative = read(DATA / "negative_1342.json")
    positive = read(DATA / "positive_1122.json")
    labels = anchored_control(negative, ngraph, nref, "1342", 9, 1, 10)
    pos_labels = anchored_control(positive, pgraph, pref, "1122", 7, 4, 8)
    neg_source = read(ROOT / neg_cert)
    old_orig = read(ROOT / neg_original)
    require(old_orig == {"graph": ngraph, "graph_digest": nref["graph_digest"]}
            and neg_source["original"]["sha256_raw"] == sha(ROOT / neg_original)
            and neg_source["original"]["graph_digest"] == nref["graph_digest"]
            and neg_source["labels"] == labels and neg_source["edge_ledger"] == negative["edge_ledger"]
            and neg_source["verification"] == negative["verification"]
            and negative["source_certificate"] == source(neg_cert)
            and negative["source_original"] == source(neg_original), "1342 retained source binding")
    pos_source, historical = read(ROOT / pos_cert), read(ROOT / query)
    require(pgraph == read(ROOT / pos_original) == historical["original_graph"]
            and pref["graph_digest"] == historical["original_graph_digest"]
            and historical["classification"] == "SAT" and historical["result"]["witness"] == pos_labels
            and historical["certificate"] == pos_source["certificate"] == positive["verification"]
            and positive["source_certificate"] == source(pos_cert) and positive["source_original"] == source(pos_original)
            and positive["source_query_record"] == source(query)
            and pos_source["source"] == {**source(query), "graph_digest": pref["graph_digest"]}, "1122 retained source binding")
    _, count = incidence(positive["predicate"], pgraph, pos_labels, 9)
    require(count == 10 and 9 > pos_labels[EXIT] and positive["predicate"]["matches"]
            and positive["predicate"]["selected_multiset"] == list(range(5, 15))
            and positive["predicate"]["selected_edges"] == pos_source["normalized"]["selected_incident_edges"]
            and pos_labels == pos_source["normalized"]["labels"], "positive 1122 certificate or exact ten incidences")

    selected = read(DATA / "thresholds.json")
    attempts = read(DATA / "one_leaf_attempts.json")
    require(tuple(range(labels[EXIT] + 1, len(labels))) == ORDER and len(selected) == len(attempts) == 8, "full strict threshold scope")
    mathematical = []
    coeffs = []
    for threshold, row, attempt, expected in zip(ORDER, selected, attempts, EXPECTED):
        chosen, count = incidence(row, ngraph, labels, threshold)
        require(count == expected and row["matches"] is False, "rejected selected premise")
        # Express each sum in the basis (1, h, h*(h-1)/2). The shift adds
        # one h per selected original edge. A run of h new consecutive
        # weights beginning at c-1 contributes (0,c-1,1). The graceful
        # target's fresh consecutive band begins at 19.
        base = sum(weight(edge, labels) for edge in ngraph["edges"])
        obtained = (base, count + threshold - labels[HOST], 1)
        wanted = (sum(range(1, 19)), 19, 1)
        delta = tuple(a - b for a, b in zip(obtained, wanted))
        require(delta == (0, count + threshold - 20, 0) and delta[1] != 0
                and row["required_count"] == 20 - threshold, "symbolic all-positive-batch sum")
        coeffs.append(delta[1])
        mathematical.append({"c": threshold, "actual_selected_edges": count,
                             "necessary_selected_edges": 20 - threshold, "coefficient_of_h": delta[1]})
        reproduce_attempt(attempt, expanded, expanded_ref, labels, threshold, chosen, count)
    require(read(DATA / "all_batch_sum.json") == {
        "old_difference_sum": 171, "inserted_linear_coefficient": "c-1", "common_quadratic_term": "h*(h-1)/2",
        "required_linear_coefficient": 19, "necessary_count": "20-c", "difference": "h*(s_c+c-20)",
        "domain": "exact integer h>=1", "thresholds": mathematical}, "symbolic receipt")
    bad = read(DATA / "invalid_thresholds.json")
    require(len(bad) == 5 and typed(row["c"] for row in bad) == typed(BAD), "invalid threshold cases")
    for row, c in zip(bad, BAD):
        require(row["type"] == type(c).__name__ and row["incidence_calls"] == 0
                and row["error"] == "c must be an exact integer from 11 through 18", "guard receipt")
    identity = read(DATA / "identity.json")
    runtime = identity["runtime"]
    require(identity["run_id"] == run and identity["parent"] == PARENT
            and runtime["implementation"] == "cpython" and runtime["utf8_mode"] == 1
            and runtime["python"].startswith(("3.12.", "3.13.")) and runtime["optional_dependencies"] == []
            and runtime["python_executable"] == ".venv/Scripts/python.exe" and bool(runtime["platform"]), "runtime identity")
    for name, field in (("config.json", "config_sha256_raw"), ("validate.py", "runner_sha256_raw"), ("audit.py", "audit_sha256_raw")):
        require(identity[field] == sha(HERE / name), "script or configuration identity")
    require(identity["proof"] == source(PROOF)
            and identity["retained_sha256_raw"] == {relative: sha(ROOT / relative)
                                                   for relative in (neg_cert, neg_original, pos_cert, pos_original, query)}
            and set(identity["source_sha256_raw"]) == SOURCES, "retained proof/config/source inventory")
    for relative, digest in identity["source_sha256_raw"].items():
        path = DATA / "source" / relative
        require(sha(path) == digest
                and path.read_bytes().replace(b"\r\n", b"\n") == (ROOT / relative).read_bytes().replace(b"\r\n", b"\n"),
                "running source snapshot")
    summary = read(DATA / "summary.json")
    require(summary == {
        "status": "PASS", "run_id": run, "identity": ref("identity.json"), "distinct_graph_records": 3,
        "retained_controls": [ref("negative_1342.json"), ref("positive_1122.json")], "attempted_original": expanded_ref,
        "threshold_evaluations": 8, "thresholds": ref("thresholds.json"), "all_batch_sum": ref("all_batch_sum.json"),
        "invalid_probes": 5, "invalid_thresholds": ref("invalid_thresholds.json"), "attempted_labelings": 8,
        "rejected_labelings": 8, "attempts": ref("one_leaf_attempts.json"), "new_graceful_targets": 0,
        "solver_queries": 0, "labeling_enumeration": 0, "historical_replay": 0}, "saved evidence scope")
    require({f.name for f in (DATA / "originals").iterdir()} == {name + ".json" for name in PROFILES}
            and all(f.stat().st_size <= 2_000_000 for f in DATA.rglob("*") if f.is_file()), "exact originals and byte cap")
    result = {"status": "PASS", "run_id": run, "same_graph_records": 3, "same_thresholds": ref("thresholds.json"),
              "same_rejected_labelings": 8, "same_attempts": ref("one_leaf_attempts.json"),
              "same_invalid_thresholds": 5, "positive_selected_count": 10, "signed_batch_coefficients": coeffs,
              "additional_graph_records": 0, "solver_queries": 0}
    require(sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "audit runtime")
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= 2_000_000, "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as stream:
        stream.write(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
