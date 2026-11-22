"""Independent arithmetic audit of the five saved original certificates."""

from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CASES = (2, 3, 4, 5)
CAP = 2_000_000
SPINE = tuple(f"s:{i}" for i in range(6))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    require(len(raw) <= CAP, "over byte limit")
    return json.loads(raw)


def key(edge):
    u, v = edge
    return tuple(sorted((u, v)))


def named_original(r):
    counts = {0: 1, 2: 2, 3: 2}
    if r is not None:
        counts[1] = r
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(SPINE)}
    edges = list(zip(SPINE[:-1], SPINE[1:], strict=True))
    for section, count in counts.items():
        hub = f"b:{section}:0"
        roles[hub] = {"kind": "branch", "section": section, "branch": 0}
        edges.append((SPINE[section], hub))
        for j in range(count):
            leaf = f"l:{section}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": section, "branch": 0, "leaf": j}
            edges.append((hub, leaf))
    return [[counts[i]] if i in counts else [] for i in range(6)], roles, edges


def retained_original(certificate, name, r):
    ref = certificate["original"]
    require(ref["path"] == f"originals/{name}.json", "wrong original path")
    file = DATA / ref["path"]
    raw = file.read_bytes()
    original = read(file)
    profile, roles, edges = named_original(r)
    graph = original["graph"]
    require(sha(raw) == ref["sha256_raw"] and graph["schema_version"] == 1
            and graph["profile"] == profile and tuple(graph["spine"]) == SPINE
            and graph["roles"] == roles and Counter(graph["vertices"]) == Counter(list(roles))
            and Counter(map(key, graph["edges"])) == Counter(map(key, edges)), "wrong original identities")
    canonical = {"profile": profile, "spine": SPINE, "roles": roles,
                 "vertices": sorted(roles), "edges": sorted(map(key, edges))}
    digest = sha(json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    require(digest == ref["graph_digest"] == original["graph_digest"]
            and len(roles) == (14 if r is None else r + 15) <= 20
            and len(edges) == len(roles)-1, "wrong original digest or size")
    return graph


def differences(edges, labels):
    return {key((u, v)): abs(labels[u]-labels[v]) for u, v in edges if u in labels and v in labels}


def ledger(rows, expected):
    require(Counter((key(row["edge"]), row["difference"]) for row in rows) == Counter(expected.items()),
            "wrong original-edge ledger")


def witness(graph, record):
    require(tuple(record["path"]) == SPINE, "wrong spine witness")
    graph_edges = {key(edge) for edge in graph["edges"]}
    require(all(key(edge) in graph_edges for edge in zip(SPINE[:-1], SPINE[1:], strict=True)),
            "witness contains a nonedge")
    adj = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    dist = dict.fromkeys(SPINE, 0)
    queue = deque(SPINE)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    require(dist == record["distances"] and len(dist) == len(adj) and max(dist.values()) == 2,
            "wrong witness distances")


def bijections(graph, record):
    labels = record["labels"]
    require(set(labels) == set(graph["vertices"]) and all(type(x) is int for x in labels.values()),
            "wrong label domain")
    m = len(graph["edges"])
    weights = differences(graph["edges"], labels)
    require(Counter(labels.values()) == Counter(range(m+1))
            and Counter(weights.values()) == Counter(range(1,m+1)), "wrong complete spectra")
    ledger(record["edge_ledger"], weights)
    receipt = record["verification"]
    require(receipt["valid"] is True and not receipt["errors"] and receipt["n"] == m+1 and receipt["m"] == m
            and receipt["graph_digest"] == record["original"]["graph_digest"]
            and receipt["edge_differences"] == [weights[key(e)] for e in graph["edges"]], "wrong checker receipt")
    witness(graph, record["witness"])
    return weights


def inspect_core():
    file = DATA / "core.json"
    record = read(file)
    graph = retained_original(record, "core", None)
    edge_weights = bijections(graph, record)
    # The fixed table is checked directly, independent of the validation script.
    expected = dict(zip(SPINE, (13, 0, 10, 4, 8, 3), strict=True))
    for i, (hub, *leaves) in ((0, (1,12)), (2, (2,9,11)), (3, (7,5,6))):
        expected[f"b:{i}:0"] = hub
        expected.update((f"l:{i}:0:{j}", x) for j, x in enumerate(leaves))
    require(record["labels"] == expected and record["physical_root"] == {"vertex": "s:1", "label": 0}
            and expected["s:1"] == 0, "wrong rooted ledger")
    return record["labels"], edge_weights, sha(file.read_bytes())


def inspect_target(r, core):
    name = f"target-r{r}"
    file = DATA / f"{name}.json"
    record = read(file)
    graph = retained_original(record, name, r)
    require(record["parameters"] == {"r":r,"K":1}
            and record["core"] == {"path":"core.json","sha256_raw":core[2]}, "wrong target or common core")
    labels = record["labels"]
    weights = bijections(graph, record)
    require(all(labels[v] == x+r for v,x in core[0].items())
            and all(weights[edge] == x for edge,x in core[1].items()), "wrong translation or core retention")
    terminal_names = [f"l:1:0:{j}" for j in range(r)]
    require([labels[v] for v in terminal_names] == [0, *range(r-1,0,-1)]
            and labels["s:1"] == r and labels["b:1:0"] == r+14, "wrong restored labels")
    require(weights[key(("s:1","b:1:0"))] == 14
            and [weights[key(("b:1:0",v))] for v in terminal_names] == [r+14, *range(15,r+14)],
            "wrong restored weights")
    prefix = record["prefix"]
    require(set(labels)-prefix.keys() == {"s:5"} and all(type(x) is int and labels[v]==x for v,x in prefix.items())
            and record["remaining_vertices"] == ["s:5"], "wrong remaining vertex or changed prefix")
    boundary = ("s:4","s:5")
    prefix_weights = differences(graph["edges"],prefix)
    ledger(record["prefix_edge_ledger"],prefix_weights)
    require(set(weights)-set(prefix_weights) == {key(record["crossing_edge"])} == {boundary},
            "wrong original edge remainder")
    m = r+14
    R = sorted(set(range(m+1))-set(prefix.values()))
    D = sorted(set(range(1,m+1))-set(prefix_weights.values()))
    partial = record["partial_verification"]
    require(R == [r+3] == record["unused_labels"] == partial["unused_labels"]
            and D == [5] == record["unused_differences"] == partial["unused_differences"],
            "wrong resource complements")
    require(partial["valid"] is True and partial["complete"] is False and not partial["errors"]
            and partial["graph_digest"] == record["original"]["graph_digest"]
            and partial["frontier"] == ["s:4"] and partial["n"] == m+1 and partial["m"] == m
            and partial["used_labels"] == sorted(prefix.values())
            and partial["used_differences"] == sorted(prefix_weights.values()), "wrong partial receipt")
    finish = record["completion"]
    require(record["port"] == {"vertex":"s:4","label":r+8} and prefix["s:4"] == r+8
            and finish["vertex"] == "s:5" and finish["label"] == R[0] == labels["s:5"]
            and key(finish["edge"]) == boundary and finish["difference"] == weights[boundary] == D[0],
            "wrong port or completion")
    return labels, graph, {"r":r, "K":1, "n":m+1, "certificate":file.name,
                           "sha256_raw":sha(file.read_bytes()), "bytes":file.stat().st_size}


def audit_batches(records):
    path = DATA / "batch_comparison.json"
    receipt = read(path)
    require((receipt["base_r"], receipt["via_r"], receipt["same_target_r"]) == (2,3,4)
            and receipt["fresh_names"] == ["l:1:0:2","l:1:0:3"]
            and receipt["pointwise_equal"] is True and receipt["additional_targets"] == 0, "wrong batch scope")
    two, three, four = (records[r][0] for r in (2,3,4))
    zero = "l:1:0:0"
    for u,v,new in ((2,3,three),(2,4,four),(3,4,four)):
        old, old_graph = records[u][:2]
        new_graph = records[v][1]
        names = set(new)-old.keys()
        expected_names = {f"l:1:0:{j}" for j in range(u,v)}
        require(names == expected_names and all(new[name] == old[name]+(0 if name==zero else v-u) for name in old)
                and [new[f"l:1:0:{j}"] for j in range(u,v)] == list(range(v-u,0,-1)), "wrong named batch shift")
        existing = {key(edge) for edge in old_graph["edges"]}
        enlarged = {key(edge) for edge in new_graph["edges"]}
        require(existing < enlarged and enlarged-existing == {key(("b:1:0",name)) for name in names},
                "wrong growth incidence")
    require(receipt["intermediate"] == three
            and receipt["direct"] == receipt["one_batch"] == receipt["successive_batches"] == four
            and two[zero] == three[zero] == four[zero] == 0, "wrong named batch agreement")
    return sha(path.read_bytes())


def main():
    config = read(HERE/"config.json")
    identity_path = DATA/"identity.json"
    identity = read(identity_path)
    require(tuple(config["completed_r"]) == CASES and config["completed_orders"] == [17,18,19,20]
            and config["core_profile"] == named_original(None)[0]
            and config["K"] == config["workers"] == 1 and config["max_vertices"] == 20
            and config["max_result_bytes"] == CAP and config["solver_queries"] ==
            config["computational_enumeration"] == config["historical_search_replay"] == 0, "wrong frozen limits")
    require(identity["parent"] == config["parent"] and identity["run_id"] == config["run_id"], "wrong run identity")
    for name, identifier in (("validate.py","runner_sha256_raw"),("audit.py","audit_sha256_raw"),("config.json","config_sha256_raw")):
        require(sha((HERE/name).read_bytes()) == identity[identifier], "wrong frozen input")
    proof = identity["proof"]
    require(sha((ROOT/proof["path"]).read_bytes()) == proof["sha256_raw"], "wrong proof bytes")
    for rel, digest in identity["source_sha256_raw"].items():
        require(sha((DATA/"source"/rel).read_bytes()) == digest, "wrong source snapshot")
    for rel, digest in identity["retained_sha256_raw"].items():
        raw = (ROOT/rel).read_bytes()
        lf = raw.replace(b"\r\n",b"\n")
        variants = (raw,lf,lf.replace(b"\n",b"\r\n")) if rel.endswith(".md") else (raw,)
        require(digest in {sha(v) for v in variants}, "wrong retained input bytes")
    core = inspect_core()
    records = {r:inspect_target(r,core) for r in CASES}
    completed = [record[2] for record in records.values()]
    batch_hash = audit_batches(records)
    rejected = read(DATA/"domain_rejections.json")
    require([(x["type"],x["value"]) for x in rejected] == [("bool",True),("float",2.0),("str","2"),("int",1)]
            and all(type(x["value"]).__name__ == x["type"] and
                    x["error"] == "r must be an exact integer >= 2" for x in rejected), "wrong domain probes")
    summary = read(DATA/"summary.json")
    require(summary["run_id"] == config["run_id"] and summary["identity_sha256_raw"] == sha(identity_path.read_bytes())
            and summary["core_sha256_raw"] == core[2] and summary["auxiliary_cores"] == 1
            and summary["completed_targets"] == completed and summary["domain_rejections"] == len(rejected) == 4
            and summary["batch_comparison_sha256_raw"] == batch_hash
            and summary["status"] == "PASS" and summary["solver_queries"] ==
            summary["computational_enumeration"] == summary["historical_search_replay"] == 0, "wrong summary")
    report = {"run_id": config["run_id"], "status": "PASS", "same_completed_targets": completed,
              "same_core_sha256_raw": core[2], "same_auxiliary_cores": 1, "same_domain_rejections": len(rejected),
              "same_batch_comparison_sha256_raw": batch_hash, "additional_core_cases": 0,
              "additional_completed_targets": 0, "solver_queries": 0, "computational_enumeration": 0,
              "historical_search_replay": 0}
    raw = (json.dumps(report,indent=2,sort_keys=True)+"\n").encode()
    require(len(raw) <= CAP, "audit output over limit")
    with (HERE/"audit_result.json").open("xb") as output:
        output.write(raw)
    print(json.dumps(report,sort_keys=True))


if __name__ == "__main__":
    main()
