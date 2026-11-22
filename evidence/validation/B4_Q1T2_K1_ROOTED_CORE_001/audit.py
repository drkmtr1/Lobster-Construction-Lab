"""Independent standard-library audit of the saved originals and certificates."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RECORDS = HERE / "validation"
CASES = ((2, 2), (2, 3), (3, 2), (4, 3))
CORES = (2, 3, 4)
MAX_BYTES = 2_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    require(len(raw) <= MAX_BYTES, f"oversized {path.name}")
    return json.loads(raw)


def original(q, t):
    counts = {0: q, 1: 1, 3: 2}
    if t is not None:
        counts[2] = t
    spine = [f"s:{i}" for i in range(6)]
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    edges = [tuple(pair) for pair in zip(spine[:-1], spine[1:], strict=True)]
    for i, count in counts.items():
        hub = f"b:{i}:0"
        roles[hub] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], hub))
        for ordinal in range(count):
            leaf = f"l:{i}:0:{ordinal}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": ordinal}
            edges.append((hub, leaf))
    return [[counts[i]] if i in counts else [] for i in range(6)], spine, roles, edges


def edge_key(edge):
    a, b = edge
    return tuple(sorted((a, b)))


def check_original(record, name, q, t):
    ref = record["original"]
    require(ref["path"] == f"originals/{name}.json", "wrong original path")
    source = RECORDS / ref["path"]
    require(digest(source.read_bytes()) == ref["sha256_raw"], "original byte binding")
    saved = read(source)
    graph = saved["graph"]
    profile, spine, roles, edges = original(q, t)
    require(graph["schema_version"] == 1 and graph["profile"] == profile and graph["spine"] == spine,
            "wrong graph schema, spine, or ordered profile")
    require(graph["roles"] == roles and Counter(graph["vertices"]) == Counter(list(roles)),
            "wrong named vertices, roles, or multiplicities")
    require(Counter(map(edge_key, graph["edges"])) == Counter(map(edge_key, edges)),
            "wrong original incidences or multiplicities")
    canonical = {"profile": profile, "spine": spine, "roles": roles,
                 "vertices": sorted(roles), "edges": sorted(map(edge_key, edges))}
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    require(saved["graph_digest"] == ref["graph_digest"] == digest(raw), "wrong original digest")
    require(len(roles) <= 20 and len(edges) + 1 == len(roles), "original count or limit")
    return graph


def exact_map(actual, expected, context):
    require(all(type(value) is int for value in actual.values()) and actual == expected, context)


def by_edge(edges, labels):
    return {edge_key((u, v)): abs(labels[u] - labels[v])
            for u, v in edges if u in labels and v in labels}


def check_ledger(ledger, differences):
    counts = Counter((edge_key(row["edge"]), row["difference"]) for row in ledger)
    require(counts == Counter(differences.items()), "named edge ledger mismatch")


def check_bijections(record, graph, expected):
    labels = record["labels"]
    exact_map(labels, expected, "wrong named labeling")
    m = len(graph["edges"])
    require(Counter(labels.values()) == Counter(range(m + 1)), "wrong full label inventory")
    differences = by_edge(graph["edges"], labels)
    require(Counter(differences.values()) == Counter(range(1, m + 1)), "wrong full difference inventory")
    check_ledger(record["edge_ledger"], differences)
    check = record["verification"]
    require(check["valid"] is True and not check["errors"] and check["n"] == m + 1 and check["m"] == m
            and check["graph_digest"] == record["original"]["graph_digest"]
            and check["edge_differences"] == [differences[edge_key(edge)] for edge in graph["edges"]],
            "saved original-target checker disagrees with arithmetic")
    return differences


def expected_core(q):
    groups = [
        (tuple(f"s:{i}" for i in range(6)), (q + 10, 1, q + 11, 0, 5, 4)),
        (("b:0:0", "l:0:0:0"), (2, 10)),
        (("b:1:0", "l:1:0:0"), (8, 6)),
        (("b:3:0", "l:3:0:0", "l:3:0:1"), (3, 9, 7)),
        (tuple(f"l:0:0:{j}" for j in range(1, q)), tuple(range(11, q + 10))),
    ]
    return {name: value for names, values in groups for name, value in zip(names, values, strict=True)}


def check_core(q):
    name = f"core-q{q}"
    path = RECORDS / f"{name}.json"
    record = read(path)
    graph = check_original(record, name, q, None)
    require(record["q"] == q and len(graph["vertices"]) == q + 12, "auxiliary core identity")
    weights = check_bijections(record, graph, expected_core(q))
    require(record["physical_root"] == {"vertex": "s:2", "label": q + 11}, "wrong physical root")
    crossing = [w for edge, w in weights.items() if {"s:0", "s:2"} & set(edge)]
    first_leaves = [weights[edge_key(("b:0:0", f"l:0:0:{j}"))] for j in range(1, q)]
    require(sorted(crossing) == list(range(q + 8, q + 12))
            and first_leaves == list(range(9, q + 8)), "wrong core partition")
    return record["labels"], {"q": q, "n": q + 12, "sha256_raw": digest(path.read_bytes())}


def check_target(q, t, old_labels):
    name = f"target-q{q}-t{t}"
    path = RECORDS / f"{name}.json"
    record = read(path)
    graph = check_original(record, name, q, t)
    m = q + t + 12
    require(len(graph["vertices"]) == m + 1 and record["parameters"] == {"q": q, "t": t, "K": 1}
            and record["core_certificate"] == f"core-q{q}.json", "wrong target identity")
    expected = {v: x + 1 for v, x in old_labels.items()}
    expected["b:2:0"] = 0
    expected.update({f"l:2:0:{j}": m - t + 1 + j for j in range(t)})
    weights = check_bijections(record, graph, expected)
    new_host_edges = {edge: weight for edge, weight in weights.items() if "b:2:0" in edge}
    require(new_host_edges[edge_key(("s:2", "b:2:0"))] == q + 12
            and sorted(new_host_edges.values()) == list(range(q + 12, m + 1)),
            "wrong restoration weights")
    prefix = record["prefix"]
    exact_map(prefix, {v: x for v, x in expected.items() if v != "s:5"}, "wrong prefix or it changed")
    boundary = edge_key(("s:4", "s:5"))
    prefix_weights = by_edge(graph["edges"], prefix)
    check_ledger(record["prefix_edge_ledger"], prefix_weights)
    require(set(graph["vertices"]) - prefix.keys() == {"s:5"}
            and set(weights) - set(prefix_weights) == {boundary}
            and edge_key(record["crossing_edge"]) == boundary
            and record["remaining_vertices"] == ["s:5"], "wrong remaining original incidence")
    r = sorted(set(range(m + 1)) - set(prefix.values()))
    d = sorted(set(range(1, m + 1)) - set(prefix_weights.values()))
    partial = record["partial_verification"]
    require(r == record["unused_labels"] == partial["unused_labels"] == [5]
            and d == record["unused_differences"] == partial["unused_differences"] == [1],
            "wrong resource complement")
    require(partial["valid"] is True and partial["complete"] is False and not partial["errors"]
            and partial["graph_digest"] == record["original"]["graph_digest"] and partial["frontier"] == ["s:4"]
            and partial["n"] == m + 1 and partial["m"] == m
            and partial["used_labels"] == sorted(prefix.values())
            and partial["used_differences"] == sorted(prefix_weights.values()),
            "saved partial verification disagrees with arithmetic")
    require(record["port"] == {"vertex": "s:4", "label": 6}, "wrong physical port")
    final = record["completion"]
    require(final["vertex"] == "s:5" and final["label"] == r[0]
            and edge_key(final["edge"]) == boundary and final["difference"] == weights[boundary] == d[0],
            "wrong completion step")
    return {"parameters": [q, t], "n": m + 1, "certificate": path.name,
            "sha256_raw": digest(path.read_bytes()), "bytes": path.stat().st_size}


def main():
    config = read(HERE / "config.json")
    require(tuple(map(tuple, config["completed_q_t"])) == CASES and tuple(config["auxiliary_core_q"]) == CORES
            and config["K"] == config["workers"] == 1 and config["max_vertices"] == 20
            and config["max_result_bytes"] == MAX_BYTES and config["solver_queries"] == config["enumeration"] == 0,
            "wrong frozen task scope")
    identity_path = RECORDS / "identity.json"
    identity = read(identity_path)
    require(identity["parent"] == config["parent"] and identity["run_id"] == config["run_id"],
            "wrong run or parent identity")
    for name, key in (("audit.py", "audit_sha256_raw"), ("validate.py", "runner_sha256_raw"),
                      ("config.json", "config_sha256_raw")):
        require(digest((HERE / name).read_bytes()) == identity[key], "wrong input bytes")
    proof = identity["proof"]
    require(digest((ROOT / proof["path"]).read_bytes()) == proof["sha256_raw"], "wrong proof bytes")
    for rel, reference in identity["source_sha256_raw"].items():
        require(digest((RECORDS / "source" / rel).read_bytes()) == reference, "wrong snapshot bytes")
    for rel, reference in identity["retained_sha256_raw"].items():
        # Only the audit machine's retained copies may differ in Windows text line endings.
        raw = (ROOT / rel).read_bytes()
        variants = {raw, raw.replace(b"\r\n", b"\n"), raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")}
        matches = {digest(raw)} if rel.endswith(".json") else {digest(item) for item in variants}
        require(reference in matches, "wrong retained input: " + rel)
    auxiliary = {q: check_core(q) for q in CORES}
    completed = [check_target(q, t, auxiliary[q][0]) for q, t in CASES]
    summary = read(RECORDS / "summary.json")
    rejection_records = read(RECORDS / "domain_rejections.json")
    require(Counter((row["parameter"], row["type"]) for row in rejection_records) ==
            Counter((p, k) for p in ("q", "t") for k in ("bool", "float", "str", "int", "int")),
            "unexpected domain-rejection coverage")
    for row in rejection_records:
        value = row["value"]
        require(type(value).__name__ == row["type"] and (type(value) is not int or value < 2)
                and row["error"] == f'{row["parameter"]} must be an exact integer >= 2', "wrong rejection receipt")
    require(summary["status"] == "PASS" and summary["run_id"] == config["run_id"]
            and summary["identity_sha256_raw"] == digest(identity_path.read_bytes())
            and summary["completed_targets"] == completed
            and summary["auxiliary_cores"] == list(CORES)
            and summary["domain_rejections"] == len(rejection_records) == 10
            and summary["solver_queries"] == summary["enumeration"] == 0,
            "wrong summary or case accounting")
    result = {"run_id": config["run_id"], "status": "PASS", "same_completed_targets": completed,
              "same_auxiliary_cores": [auxiliary[q][1] for q in CORES], "additional_targets": 0,
              "additional_cores": 0, "solver_queries": 0, "enumeration": 0}
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= MAX_BYTES, "audit output size")
    with (HERE / "audit_result.json").open("xb") as stream:
        stream.write(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
