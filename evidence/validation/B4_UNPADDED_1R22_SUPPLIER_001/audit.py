"""Independently reconstruct and audit the same saved 1R22 certificates."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CASES = ((2, 2), (2, 3), (3, 4), (4, 5))
SEEDS = (2, 3, 4)
CAP = 2_000_000
W = ("b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(file):
    raw = file.read_bytes()
    require(len(raw) <= CAP, "result over byte cap")
    return json.loads(raw)


def edgekey(edge):
    return tuple(sorted(edge))


def original(r, length):
    spine = [f"s:{i}" for i in range(5 + length)]
    counts = [1, r, 2, 2]
    profile = [[count] for count in counts] + [[] for _ in range(length + 1)]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = [(spine[i-1], spine[i]) for i in range(1, len(spine))]
    for i, count in enumerate(counts):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(count):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
    return profile, spine, roles, edges


def check_graph(graph, claimed, r, length):
    profile, spine, roles, edges = original(r, length)
    require(graph["schema_version"] == 1 and graph["profile"] == profile
            and graph["spine"] == spine and graph["roles"] == roles
            and Counter(graph["vertices"]) == Counter(list(roles)), "wrong original names or roles")
    require(Counter(map(edgekey, graph["edges"])) == Counter(map(edgekey, edges)), "wrong original incidences")
    canonical = {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles),
                 "edges": sorted(map(edgekey, edges))}
    digest = sha(json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    require(digest == claimed and len(roles) == r + length + 14 <= 23, "wrong digest or size")


def original_record(record, name, r, K):
    ref = record["original"]
    require(ref["path"] == f"originals/{name}.json", "wrong original path")
    file = DATA / ref["path"]
    retained = read(file)
    require(retained["graph_digest"] == ref["graph_digest"] and sha(file.read_bytes()) == ref["sha256_raw"],
            "wrong original byte binding")
    check_graph(retained["graph"], ref["graph_digest"], r, K)
    return retained["graph"]


def weights(edges, labels):
    return {edgekey((u, v)): abs(labels[u] - labels[v]) for u, v in edges if u in labels and v in labels}


def ledger(rows, expected):
    require(Counter((edgekey(row["edge"]), row["difference"]) for row in rows)
            == Counter(expected.items()), "wrong named edge ledger")


def full(graph, graph_hash, labels, report):
    m = len(graph["edges"])
    require(set(labels) == set(graph["vertices"]) and all(type(x) is int for x in labels.values())
            and Counter(labels.values()) == Counter(range(m + 1)), "wrong full labels")
    actual = weights(graph["edges"], labels)
    require(Counter(actual.values()) == Counter(range(1, m+1)), "wrong full differences")
    require(report["valid"] is True and not report["errors"] and report["n"] == m+1 and report["m"] == m
            and report["graph_digest"] == graph_hash
            and report["edge_differences"] == [actual[edgekey(e)] for e in graph["edges"]], "wrong checker receipt")
    return actual


def audit_seed(r):
    name = f"normalized-r{r}"
    file = DATA / f"{name}.json"
    saved = read(file)
    graph = original_record(saved, name, r, 0)
    labels = saved["labels"]
    differences = full(graph, saved["original"]["graph_digest"], labels, saved["verification"])
    ledger(saved["edge_ledger"], differences)
    p = r + 6
    lows = ["s:1", "s:3", "b:0:0", "b:2:0", "l:3:0:0", "l:3:0:1"]
    lows += [f"l:1:0:{j}" for j in range(r)]
    highs = set(labels).difference(lows)
    alpha = saved["alpha"]
    require(len(lows) == p and len(highs) == 8 and set(alpha["low"]) == set(lows)
            and set(alpha["high"]) == highs and alpha["low_size"] == p
            and all(labels[v] < p for v in lows) and all(labels[v] >= p for v in highs)
            and all((u in highs) != (v in highs) for u,v in graph["edges"]), "wrong alpha split")
    expected = {
        **dict(zip(graph["spine"], (13, 1, 12, 6, 8), strict=True)),
        "b:0:0": 5, "l:0:0:0": 10, "b:1:0": 14, "b:2:0": 2, "l:2:0:0": 9, "l:2:0:1": 11,
        "b:3:0": 7, "l:3:0:0": 3, "l:3:0:1": 4,
    }
    expected = {v: x+r-1 for v, x in expected.items()}
    expected["l:1:0:0"] = 0
    expected.update({f"l:1:0:{j}": r-j for j in range(1,r)})
    require(labels == expected and saved["r"] == r, "wrong normalized formula")
    require(saved["state"] == {"n":r+14, "p":p, "L":W[0], "x":labels[W[0]], "U":W[-1], "y":labels[W[-1]]-p}
            and labels[W[0]] == r+4 and labels[W[-1]] == p+1, "wrong physical ports")
    adj = {v: [] for v in labels}
    for u,v in graph["edges"]:
        adj[u].append(v)
        adj[v].append(u)
    require(tuple(saved["witness"]) == W and all(v in adj[u] for u,v in zip(W[:-1],W[1:],strict=True)),
            "wrong witness")
    queue = deque(W)
    dist = dict.fromkeys(W, 0)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u]+1
                queue.append(v)
    require(dist == saved["witness_distances"] and max(dist.values()) == 2 and dist["b:1:0"] == 1,
            "wrong witness distances")
    pred = saved["lower_predicate"]
    selected = [v for v, x in labels.items() if x < 1]
    incident = {edge: w for edge,w in differences.items() if set(edge).intersection(selected)}
    require(pred["threshold"] == 1 and selected == pred["selected_vertices"] == ["l:1:0:0"]
            and pred["host"] == "b:1:0" and pred["host_label"] == labels["b:1:0"] == r+13
            and incident == {edgekey(("b:1:0","l:1:0:0")): r+13}, "wrong lower-block premise")
    ledger(pred["incident"], incident)
    return labels, {"r":r, "n": r+14, "sha256_raw": sha(file.read_bytes())}


def sequence(K):
    if K == 2:
        return [3,1,0]
    if K == 3:
        return [4,1,0,2]
    if K == 4:
        return [5,1,2,0,3]
    return [K+1,1,K-1,0] + [K-2-x for x in sequence(K-3)[1:]]


def audit_full(r, K, normalized):
    name = f"target-r{r}-K{K}"
    file = DATA / f"{name}.json"
    saved = read(file)
    require(saved["parameters"] == {"r":r,"K":K} and saved["normalized"] == f"normalized-r{r}.json", "wrong parameters")
    graph = original_record(saved, name, r, K)
    labels, prefix = saved["labels"], saved["prefix"]
    digest = saved["original"]["graph_digest"]
    differences = full(graph, digest, labels, saved["verification"])
    ledger(saved["edge_ledger"], differences)
    p, m = r+6, len(graph["edges"])
    expected = {v: x+(K if x >= p else 0) for v,x in normalized.items()}
    require(prefix == expected and all(labels[v] == x for v,x in prefix.items()), "wrong shift or changed prefix")
    prefix_weights = weights(graph["edges"], prefix)
    ledger(saved["prefix_edge_ledger"], prefix_weights)
    R = sorted(set(range(m+1)) - set(prefix.values()))
    D = sorted(set(range(1,m+1)) - set(prefix_weights.values()))
    partial = saved["partial_verification"]
    require(R == partial["unused_labels"] == saved["unused_labels"] == list(range(p,p+K))
            and D == partial["unused_differences"] == saved["unused_differences"] == list(range(1,K+1)),
            "wrong inventory complements")
    require(partial["valid"] is True and partial["complete"] is False and not partial["errors"]
            and partial["n"] == m+1 and partial["m"] == m and partial["graph_digest"] == digest
            and partial["used_labels"] == sorted(prefix.values())
            and partial["used_differences"] == sorted(prefix_weights.values())
            and partial["frontier"] == ["s:4"], "wrong partial receipt")
    path = graph["spine"][4:]
    pending_edges = {edgekey(edge) for edge in zip(path[:-1],path[1:],strict=True)}
    remainder = {edge:w for edge,w in differences.items() if edge not in prefix_weights}
    ledger(saved["suffix_edge_ledger"], remainder)
    require(set(labels) - prefix.keys() == set(path[1:]) and saved["remaining_vertices"] == path[1:]
            and len(path) == K+1 and saved["path"] == path and set(remainder) == pending_edges
            and {edge for edge in remainder if set(edge) & prefix.keys()} == {edgekey(saved["crossing_edge"])}
            == {("s:4","s:5")} and sorted(remainder.values()) == D, "wrong original remainder")
    require(saved["port"] == {"vertex":"s:4","label": p+K+1}
            and saved["path_labels"] == [labels[v] for v in path] == [p+x for x in sequence(K)],
            "wrong physical port or recurrence translation")
    return {"r":r, "K":K, "n":m+1, "certificate":file.name,
            "sha256_raw":sha(file.read_bytes()), "bytes":file.stat().st_size}


def audit_retained():
    records = read(DATA/"retained.json")
    require([row["side"] for row in records] == ["adjacent","nonadjacent"], "wrong retained scope")
    for row in records:
        path = ROOT / row["source"]
        require(path.name == f'1122-{row["side"]}.json' and sha(path.read_bytes()) == row["source_sha256_raw"],
                "wrong retained bytes")
        saved = read(path)
        graph, digest = saved["original_graph"], saved["original_graph_digest"]
        check_graph(graph, digest, 1, 0)
        labels = saved["solver_result"]["witness"]
        diffs = full(graph, digest, labels, row["check"])
        host, exit_label = {"adjacent":(11,7), "nonadjacent":(14,8)}[row["side"]]
        require(row["host_label"] == labels["b:1:0"] == host and row["exit_label"] == labels["s:4"] == exit_label
                and all((labels[u]<7) != (labels[v]<7) for u,v in graph["edges"]), "wrong retained alpha anchors")
        require([cut["c"] for cut in row["cuts"]] == list(range(1,8)), "wrong retained cut range")
        for cut in row["cuts"]:
            c = cut["c"]
            selected = sorted(v for v in labels if labels[v]<c)
            actual = sorted(w for edge,w in diffs.items() if set(selected).intersection(edge))
            required = list(range(host-c+1,15))
            require(selected == cut["selected"] and actual == cut["weights"]
                    and required == cut["required"] and actual != required, "wrong retained obstruction")
    return len(records)


def main():
    config = read(HERE/"config.json")
    identity = read(DATA/"identity.json")
    require(tuple(map(tuple,config["completed_r_K"])) == CASES and tuple(config["normalized_r"]) == SEEDS
            and config["workers"] == 1 and config["max_vertices"] == 23 and config["max_result_bytes"] == CAP
            and config["solver_queries"] == config["labeling_enumeration"] == 0, "wrong scope")
    require(identity["run_id"] == config["run_id"] and identity["parent"] == config["parent"], "wrong identity")
    for name, key in (("validate.py","runner_sha256_raw"),("audit.py","audit_sha256_raw"),("config.json","config_sha256_raw")):
        require(sha((HERE/name).read_bytes()) == identity[key], "wrong run inputs")
    recorded = identity["proof"]
    require(sha((ROOT/recorded["path"]).read_bytes()) == recorded["sha256_raw"], "wrong proof bytes")
    for path, digest in identity["source_sha256_raw"].items():
        require(sha((DATA/"source"/path).read_bytes()) == digest, "wrong dependency snapshot")
    for path, digest in identity["retained_sha256_raw"].items():
        raw = (ROOT/path).read_bytes()
        lf = raw.replace(b"\r\n",b"\n")
        variants = (raw, lf, lf.replace(b"\n",b"\r\n")) if path.endswith(".md") else (raw,)
        require(digest in {sha(value) for value in variants}, "wrong retained source")
    seeds = {r:audit_seed(r) for r in SEEDS}
    cases = [audit_full(r,K,seeds[r][0]) for r,K in CASES]
    retained = audit_retained()
    rejections = read(DATA/"domain_rejections.json")
    expected = Counter((key,type(value).__name__,value) for key in ("r","K") for value in (True,2.0,"2",1))
    require(Counter((row["parameter"],row["type"],row["value"]) for row in rejections) == expected
            and all(type(row["value"]).__name__ == row["type"] and row["error"] ==
                    f'{row["parameter"]} must be an exact integer >= 2' for row in rejections), "wrong rejected probes")
    summary = read(DATA/"summary.json")
    require(summary["completed_targets"] == cases and summary["normalized_prefixes"] == list(SEEDS)
            and summary["identity_sha256_raw"] == sha((DATA/"identity.json").read_bytes())
            and summary["retained_rechecks"] == retained == 2 and summary["domain_rejections"] == len(rejections) == 8
            and summary["solver_queries"] == summary["labeling_enumeration"] == 0, "wrong summary")
    result = {"run_id":config["run_id"], "status":"PASS", "same_completed_targets":cases,
              "same_normalized_prefixes":[seeds[r][1] for r in SEEDS], "same_retained_rechecks":retained,
              "same_domain_rejections":len(rejections), "additional_completed_targets":0,
              "additional_normalized_prefixes":0, "solver_queries":0, "labeling_enumeration":0}
    raw = (json.dumps(result,indent=2,sort_keys=True)+"\n").encode()
    require(len(raw) <= CAP, "wrong audit output size")
    with (HERE/"audit_result.json").open("xb") as output:
        output.write(raw)
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
