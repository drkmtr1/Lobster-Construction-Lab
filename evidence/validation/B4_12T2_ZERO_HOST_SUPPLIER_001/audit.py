"""Reconstruct the exact saved originals and audit 12T2 without LCL imports."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CASES = ((3,2),(3,3),(4,4),(5,5))
SEEDS = (3,4,5)
CAP = 2_000_000
L, U, Z = "b:0:0", "s:4", "b:2:0"
W = (L,"s:0","s:1","s:2","s:3",U)
CONTROL = "evidence/validation/B4_UNPADDED_1R22_SUPPLIER_001/validation"
CONTROL_CERT = f"{CONTROL}/normalized-r2.json"
CONTROL_GRAPH = f"{CONTROL}/originals/normalized-r2.json"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    require(len(raw) <= CAP, "result exceeds byte cap")
    return json.loads(raw)


def edgekey(edge):
    u,v = edge
    return tuple(sorted((u,v)))


def topology(t, K):
    spine = [f"s:{i}" for i in range(K+5)]
    counts = {0:1,1:2,2:t,3:2}
    profile = [[counts[i]] if i in counts else [] for i in range(len(spine))]
    roles = {v:{"kind":"spine","section":i} for i,v in enumerate(spine)}
    edges = list(zip(spine[:-1],spine[1:],strict=True))
    for i,n in counts.items():
        hub = f"b:{i}:0"
        roles[hub] = {"kind":"branch","section":i,"branch":0}
        edges.append((spine[i],hub))
        for j in range(n):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
            edges.append((hub,leaf))
    return profile,spine,roles,edges


def graph_check(graph, digest, t, K):
    profile,spine,roles,edges = topology(t,K)
    require(graph["schema_version"] == 1 and graph["profile"] == profile and graph["spine"] == spine
            and graph["roles"] == roles and Counter(graph["vertices"]) == Counter(list(roles))
            and Counter(map(edgekey,graph["edges"])) == Counter(map(edgekey,edges)), "wrong original identities")
    canonical = {"profile":profile,"spine":spine,"roles":roles,"vertices":sorted(roles),
                 "edges":sorted(map(edgekey,edges))}
    raw = json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    require(sha(raw) == digest and len(roles) == t+K+14 <= 24 and len(edges) == len(roles)-1, "wrong digest or size")


def original(record, name, t, K):
    ref = record["original"]
    require(ref["path"] == f"originals/{name}.json", "wrong original path")
    file = DATA / ref["path"]
    held = read(file)
    require(sha(file.read_bytes()) == ref["sha256_raw"] and held["graph_digest"] == ref["graph_digest"],
            "wrong original byte binding")
    graph_check(held["graph"],held["graph_digest"],t,K)
    return held["graph"]


def weights(edges, labels):
    return {edgekey((u,v)):abs(labels[u]-labels[v]) for u,v in edges if u in labels and v in labels}


def ledger(rows, expected):
    require(Counter((edgekey(row["edge"]),row["difference"]) for row in rows) == Counter(expected.items()),
            "wrong edge ledger")


def complete(graph, digest, labels, receipt):
    m = len(graph["edges"])
    require(set(labels) == set(graph["vertices"]) and all(type(x) is int for x in labels.values())
            and Counter(labels.values()) == Counter(range(m+1)), "wrong complete labels")
    diff = weights(graph["edges"],labels)
    require(Counter(diff.values()) == Counter(range(1,m+1)), "wrong original weights")
    require(receipt["valid"] is True and not receipt["errors"] and receipt["graph_digest"] == digest
            and receipt["n"] == m+1 and receipt["m"] == m
            and receipt["edge_differences"] == [diff[edgekey(e)] for e in graph["edges"]], "wrong checker receipt")
    return diff


def alpha_and_witness(graph, labels, record):
    lows = {"s:1","s:3","b:0:0","b:2:0","l:1:0:0","l:1:0:1","l:3:0:0","l:3:0:1"}
    highs = set(graph["vertices"]) - lows
    alpha = record["alpha"]
    require(Counter(alpha["low"]) == Counter(list(lows)) and Counter(alpha["high"]) == Counter(list(highs))
            and alpha["low_size"] == 8 and set(labels[v] for v in lows) == set(range(8))
            and all((u in lows) != (v in lows) for u,v in graph["edges"]), "wrong alpha classes")
    require(tuple(record["witness"]) == W, "wrong witness")
    adjacency = {v:set() for v in labels}
    for u,v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(all(v in adjacency[u] for u,v in zip(W[:-1],W[1:],strict=True)), "witness has a nonedge")
    dist = dict.fromkeys(W,0)
    queue = deque(W)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in dist:
                dist[v] = dist[u]+1
                queue.append(v)
    require(dist == record["witness_distances"] and set(dist) == set(labels) and max(dist.values()) == 2
            and dist[Z] == 1 and "s:2" in adjacency[Z], "wrong witness distances")


def seed(t):
    name = f"normalized-t{t}"
    file = DATA/f"{name}.json"
    rec = read(file)
    graph = original(rec,name,t,0)
    labels = rec["labels"]
    diff = complete(graph,rec["original"]["graph_digest"],labels,rec["verification"])
    ledger(rec["edge_ledger"],diff)
    alpha_and_witness(graph,labels,rec)
    expected = dict(zip(graph["spine"],(11,7,16,4,9),strict=True))
    for i, (hub,*leaves) in ((0,(1,12)),(1,(8,6,5)),(2,(0,13,14,15)),(3,(10,2,3))):
        expected[f"b:{i}:0"] = hub
        expected.update((f"l:{i}:0:{j}",value) for j,value in enumerate(leaves))
    expected.update(zip((f"l:2:0:{j}" for j in range(3,t)),range(17,t+14),strict=True))
    require(labels == expected and rec["t"] == t
            and rec["state"] == {"n":t+14,"p":8,"x":1,"y":1,"L":L,"U":U,"Z":Z,"host_label":0}
            and (labels[L],labels[U],labels[Z]) == (1,9,0), "wrong seed or physical state")
    return labels,graph,rec,{"t":t,"n":t+14,"sha256_raw":sha(file.read_bytes())}


def sequence(k):
    bases = {2:[3,1,0],3:[4,1,0,2],4:[5,1,2,0,3]}
    if k in bases:
        return bases[k]
    return [k+1,1,k-1,0] + [k-2-x for x in sequence(k-3)[1:]]


def target(t, K, normalized):
    name = f"target-t{t}-K{K}"
    file = DATA/f"{name}.json"
    rec = read(file)
    require(rec["parameters"] == {"t":t,"K":K}
            and rec["normalized"] == {"path":f"normalized-t{t}.json","sha256_raw":normalized[3]["sha256_raw"]},
            "wrong parameters or shared seed")
    graph = original(rec,name,t,K)
    digest = rec["original"]["graph_digest"]
    prefix,labels = rec["prefix"],rec["labels"]
    diff = complete(graph,digest,labels,rec["verification"])
    ledger(rec["edge_ledger"],diff)
    expected = {v:x+(K if x>=8 else 0) for v,x in normalized[0].items()}
    require(prefix == expected and all(type(x) is int and labels[v] == x for v,x in prefix.items()),
            "wrong shift or altered prefix")
    prefix_diff = weights(graph["edges"],prefix)
    ledger(rec["prefix_edge_ledger"],prefix_diff)
    m = t+K+13
    R = sorted(set(range(m+1))-set(prefix.values()))
    D = sorted(set(range(1,m+1))-set(prefix_diff.values()))
    part = rec["partial_verification"]
    require(R == list(range(8,K+8)) == rec["unused_labels"] == part["unused_labels"]
            and D == list(range(1,K+1)) == rec["unused_differences"] == part["unused_differences"],
            "wrong inventory complements")
    require(part["valid"] is True and part["complete"] is False and not part["errors"]
            and part["graph_digest"] == digest and part["frontier"] == [U] and part["n"] == m+1 and part["m"] == m
            and part["used_labels"] == sorted(prefix.values()) and part["used_differences"] == sorted(prefix_diff.values()),
            "wrong partial checker receipt")
    path = graph["spine"][4:]
    suffix_diff = {edge:x for edge,x in diff.items() if edge not in prefix_diff}
    ledger(rec["suffix_edge_ledger"],suffix_diff)
    require(set(labels)-prefix.keys() == set(path[1:]) and rec["path"] == path
            and rec["remaining_vertices"] == path[1:] and len(path) == K+1
            and set(suffix_diff) == {edgekey(edge) for edge in zip(path[:-1],path[1:],strict=True)}
            and {edge for edge in suffix_diff if set(edge) & prefix.keys()}
            == {edgekey(rec["crossing_edge"])} == {("s:4","s:5")} and sorted(suffix_diff.values()) == D,
            "wrong original suffix or crossing")
    require(rec["port"] == {"vertex":U,"label":K+9}
            and rec["path_labels"] == [labels[v] for v in path] == [8+x for x in sequence(K)]
            and sorted(labels[v] for v in path[1:]) == R, "wrong physical numeric binding")
    return {"t":t,"K":K,"n":m+1,"certificate":file.name,"bytes":file.stat().st_size,"sha256_raw":sha(file.read_bytes())}


def retained_control():
    receipt_path = DATA/"retained_control.json"
    rec = read(receipt_path)
    require(rec["certificate"] == CONTROL_CERT and rec["original"] == CONTROL_GRAPH, "wrong sole retained control")
    cert_path, graph_path = ROOT/CONTROL_CERT, ROOT/CONTROL_GRAPH
    saved,held = read(cert_path),read(graph_path)
    require(sha(cert_path.read_bytes()) == rec["certificate_sha256_raw"]
            and sha(graph_path.read_bytes()) == rec["original_sha256_raw"] == saved["original"]["sha256_raw"]
            and rec["graph_digest"] == held["graph_digest"] == saved["original"]["graph_digest"], "wrong control identity")
    graph,labels = held["graph"],saved["labels"]
    graph_check(graph,rec["graph_digest"],2,0)
    diff = complete(graph,rec["graph_digest"],labels,rec["check"])
    alpha_and_witness(graph,labels,saved)
    require(rec["port"] == {"vertex":U,"label":9} and rec["host"] == {"vertex":Z,"label":3}
            and rec["p"] == 8 and (labels[U],labels[Z]) == (9,3), "wrong retained anchors")
    cuts = rec["cuts"]
    require([row["c"] for row in cuts] == list(range(10,16)), "wrong retained threshold domain")
    for row in cuts:
        selected = sorted(v for v,x in labels.items() if x>=row["c"])
        incident = {edge:x for edge,x in diff.items() if set(edge).intersection(selected)}
        ledger(row["incident"],incident)
        actual,required = sorted(incident.values()),list(range(row["c"]-3,16))
        require(row["selected"] == selected and row["spectrum"] == actual
                and row["required"] == required and actual != required, "wrong fixed-ledger conclusion")
    require([len(row["spectrum"]) for row in cuts] == [11,10,9,8,5,3]
            and cuts[4]["selected"] == ["b:1:0","s:0"]
            and cuts[4]["spectrum"] == [8,12,13,14,15], "wrong retained proof cases")
    return sha(receipt_path.read_bytes())


def batches(seeds):
    file = DATA/"batch_comparison.json"
    rec = read(file)
    three,four,five = (seeds[t][0] for t in SEEDS)
    require((rec["base_t"],rec["via_t"],rec["same_prefix_t"]) == (3,4,5)
            and rec["fresh_names"] == ["l:2:0:3","l:2:0:4"] and rec["pointwise_equal"] is True
            and rec["additional_prefixes"] == rec["additional_targets"] == 0, "wrong batch scope")
    for old,new in ((3,4),(3,5),(4,5)):
        prev, graph, state, _ = seeds[old]
        later, extended, after, _ = seeds[new]
        fresh = [f"l:2:0:{j}" for j in range(old,new)]
        require(set(later)-prev.keys() == set(fresh) and all(later[v] == x for v,x in prev.items())
                and [later[v] for v in fresh] == list(range(old+14,new+14)), "wrong named growth")
        require(state["witness"] == after["witness"] == rec["same_witness"]
                and all(prev[v] == later[v] == rec["ports_and_host"][v] for v in (L,U,Z)), "wrong fixed anchors")
        edges,more = ({edgekey(edge) for edge in g["edges"]} for g in (graph,extended))
        require(edges < more and more-edges == {edgekey((Z,v)) for v in fresh}, "wrong growth incidences")
    require(rec["intermediate"] == four
            and rec["direct"] == rec["one_batch"] == rec["successive_batches"] == five
            and three[Z] == four[Z] == five[Z] == 0, "wrong batch agreement")
    return sha(file.read_bytes())


def main():
    config = read(HERE/"config.json")
    identity_file = DATA/"identity.json"
    identity = read(identity_file)
    require(tuple(map(tuple,config["completed_t_K"])) == CASES and tuple(config["normalized_t"]) == SEEDS
            and config["completed_orders"] == [19,20,22,24] and config["retained"] == CONTROL_CERT
            and config["exit_offset"] == config["workers"] == 1 and config["max_vertices"] == 24
            and config["max_result_bytes"] == CAP and config["solver_queries"] ==
            config["computational_enumeration"] == config["historical_search_replay"] == 0, "wrong scope")
    require(identity["run_id"] == config["run_id"] and identity["parent"] == config["parent"], "wrong run identity")
    for name,key in (("validate.py","runner_sha256_raw"),("audit.py","audit_sha256_raw"),("config.json","config_sha256_raw")):
        require(sha((HERE/name).read_bytes()) == identity[key], "wrong frozen input")
    proof = identity["proof"]
    require(sha((ROOT/proof["path"]).read_bytes()) == proof["sha256_raw"], "wrong proof bytes")
    for rel,digest in identity["source_sha256_raw"].items():
        require(sha((DATA/"source"/rel).read_bytes()) == digest, "wrong snapshot")
    for rel,digest in identity["retained_sha256_raw"].items():
        raw = (ROOT/rel).read_bytes()
        lf = raw.replace(b"\r\n",b"\n")
        variants = (raw,lf,lf.replace(b"\n",b"\r\n")) if rel.endswith(".md") else (raw,)
        require(digest in {sha(item) for item in variants}, "wrong retained input")
    adjacent = identity["parent_adjacent_argument"]
    require(adjacent["git_revision_path"] == f'{config["parent"]}:research/PROOF_OBLIGATIONS.md'
            and sha(subprocess.check_output(["git","show",adjacent["git_revision_path"]],cwd=ROOT))
            == adjacent["sha256_raw"], "wrong parent adjacent argument")
    seeds = {t:seed(t) for t in SEEDS}
    cases = [target(t,K,seeds[t]) for t,K in CASES]
    retained_hash, batch_hash = retained_control(), batches(seeds)
    rejects = read(DATA/"domain_rejections.json")
    expected = Counter((key,type(value).__name__,value) for key,values in
                       (("t",(True,3.0,"3",2)),("K",(True,2.0,"2",1))) for value in values)
    require(Counter((r["parameter"],r["type"],r["value"]) for r in rejects) == expected
            and all(type(r["value"]).__name__ == r["type"] and
                    r["error"] == f'{r["parameter"]} must be an exact integer >= {3 if r["parameter"]=="t" else 2}'
                    for r in rejects), "wrong rejection receipts")
    summary = read(DATA/"summary.json")
    require(summary["status"] == "PASS" and summary["run_id"] == config["run_id"]
            and summary["identity_sha256_raw"] == sha(identity_file.read_bytes())
            and summary["completed_targets"] == cases and summary["normalized_prefixes"] == list(SEEDS)
            and summary["fixed_seed_t"] == 3 and summary["domain_rejections"] == len(rejects) == 8
            and summary["retained_rechecks"] == 1 and summary["retained_control_sha256_raw"] == retained_hash
            and summary["batch_comparison_sha256_raw"] == batch_hash and summary["solver_queries"]
            == summary["computational_enumeration"] == summary["historical_search_replay"] == 0, "wrong summary")
    report = {"run_id":config["run_id"],"status":"PASS","same_completed_targets":cases,
              "same_normalized_prefixes":[seeds[t][3] for t in SEEDS],"same_retained_rechecks":1,
              "same_retained_control_sha256_raw":retained_hash,"same_domain_rejections":8,
              "same_batch_comparison_sha256_raw":batch_hash,"additional_prefixes":0,"additional_completed_targets":0,
              "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    raw = (json.dumps(report,indent=2,sort_keys=True)+"\n").encode()
    require(len(raw) <= CAP,"oversized audit output")
    with (HERE/"audit_result.json").open("xb") as output:
        output.write(raw)
    print(json.dumps(report,sort_keys=True))


if __name__ == "__main__":
    main()
