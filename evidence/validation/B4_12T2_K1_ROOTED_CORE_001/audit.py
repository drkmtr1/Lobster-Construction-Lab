"""Independently audit the five new certificates and one retained core."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CASES = (3,4,5,6)
OLD = "evidence/validation/B4_THIRD_ZERO_HOST_K1_DIRECT_001/validation"
OLD_CERT, OLD_GRAPH = f"{OLD}/core_certificate.json", f"{OLD}/originals/core.json"
SPINE = tuple(f"s:{i}" for i in range(6))
HOST, FRESH, ZERO = "b:1:0", "l:1:0:1", "b:2:0"
CAP = 2_000_000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(file):
    raw = file.read_bytes()
    require(len(raw) <= CAP, "result exceeds cap")
    return json.loads(raw)


def key(edge):
    u,v = edge
    return tuple(sorted((u,v)))


def topology(second, third):
    counts = {0:1,1:second,3:2}
    if third is not None:
        counts[2] = third
    roles = {name:{"kind":"spine","section":i} for i,name in enumerate(SPINE)}
    edges = list(zip(SPINE[:-1],SPINE[1:],strict=True))
    for i,n in counts.items():
        b = f"b:{i}:0"
        roles[b] = {"kind":"branch","section":i,"branch":0}
        edges.append((SPINE[i],b))
        for j in range(n):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
            edges.append((b,leaf))
    return [[counts[i]] if i in counts else [] for i in range(6)],roles,edges


def graph_check(graph, claimed, second, third):
    profile,roles,edges = topology(second,third)
    require(graph["schema_version"] == 1 and graph["profile"] == profile and tuple(graph["spine"]) == SPINE
            and graph["roles"] == roles and Counter(graph["vertices"]) == Counter(list(roles))
            and Counter(map(key,graph["edges"])) == Counter(map(key,edges)), "wrong named original")
    canonical = {"profile":profile,"spine":SPINE,"roles":roles,"vertices":sorted(roles),"edges":sorted(map(key,edges))}
    raw = json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    require(sha(raw) == claimed and len(roles) <= 21 and len(edges) == len(roles)-1, "wrong graph digest or count")


def original(record,name,t):
    ref = record["original"]
    require(ref["path"] == f"originals/{name}.json", "wrong original path")
    file = DATA/ref["path"]
    data = read(file)
    require(sha(file.read_bytes()) == ref["sha256_raw"] and data["graph_digest"] == ref["graph_digest"],
            "wrong retained byte binding")
    graph_check(data["graph"],data["graph_digest"],2,t)
    return data["graph"]


def weights(edges,labels):
    return {key((u,v)):abs(labels[u]-labels[v]) for u,v in edges if u in labels and v in labels}


def ledger(saved, expected):
    require(Counter((key(row["edge"]),row["difference"]) for row in saved) == Counter(expected.items()),
            "wrong complete named edge ledger")


def full(graph,digest,labels,receipt):
    m = len(graph["edges"])
    require(set(labels) == set(graph["vertices"]) and all(type(x) is int for x in labels.values())
            and Counter(labels.values()) == Counter(range(m+1)), "wrong label bijection")
    differences = weights(graph["edges"],labels)
    require(Counter(differences.values()) == Counter(range(1,m+1)), "wrong complete difference spectrum")
    require(receipt["valid"] is True and not receipt["errors"] and receipt["graph_digest"] == digest
            and receipt["n"] == m+1 and receipt["m"] == m
            and receipt["edge_differences"] == [differences[key(edge)] for edge in graph["edges"]],
            "wrong original-target checker receipt")
    return differences


def witness(graph, data, prefix=False):
    path = SPINE[:-1] if prefix else SPINE
    require(tuple(data["path"]) == path,"wrong requested spine")
    pending = {"s:5"} if prefix else set()
    adj = {v:set() for v in graph["vertices"] if v not in pending}
    for u,v in graph["edges"]:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    require(all(v in adj[u] for u,v in zip(path[:-1],path[1:],strict=True)), "witness has a nonedge")
    dist = dict.fromkeys(path,0)
    queue = deque(path)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u]+1
                queue.append(v)
    require(dist == data["distances"] and set(dist) == set(adj) and max(dist.values()) == 2
            and dist[HOST] == 1, "wrong witness distances")


def check_cut(labels, diff, rec, threshold, host, m):
    require(rec["c"] == threshold and rec["host"] == HOST and rec["host_label"] == labels[HOST] == host
            and rec["m"] == m, "wrong cut anchors")
    below = {v for v,x in labels.items() if x < threshold}
    crossing = {edge:w for edge,w in diff.items() if len(below.intersection(edge)) == 1}
    other = {edge:w for edge,w in diff.items() if edge not in crossing}
    require(Counter(rec["below"]) == Counter(list(below))
            and rec["crossing_spectrum"] == sorted(crossing.values()) == list(range(host-threshold+1,m+1))
            and rec["noncrossing_spectrum"] == sorted(other.values()) == list(range(1,host-threshold+1)),
            "wrong complete crossing or noncrossing bands")
    ledger(rec["crossing"],crossing)
    ledger(rec["noncrossing"],other)
    return crossing


def retained():
    path = DATA/"retained_recheck.json"
    receipt = read(path)
    require((receipt["certificate"],receipt["original"]) == (OLD_CERT,OLD_GRAPH),"wrong retained scope")
    old_path, graph_path = ROOT/OLD_CERT, ROOT/OLD_GRAPH
    old,graph = read(old_path),read(graph_path)
    digest = receipt["graph_digest"]
    require(sha(old_path.read_bytes()) == receipt["certificate_sha256_raw"]
            and sha(graph_path.read_bytes()) == receipt["original_sha256_raw"] == old["original"]["sha256_raw"]
            and old["original"]["graph_digest"] == digest, "wrong retained input bytes")
    graph_check(graph,digest,1,None)
    labels = old["labels"]
    require(labels["s:2"] == 12 and receipt["root"] == old["root"] == {"vertex":"s:2","label":12},
            "wrong retained root")
    diff = full(graph,digest,labels,receipt["verification"])
    ledger(old["edge_ledger"],diff)
    old_cut = check_cut(labels,diff,receipt["cut"],2,8,12)
    require(set(receipt["cut"]["below"]) == {"s:1","s:3"} and len(old_cut) == 6
            and all(any(labels[v]>=2 for v in edge) for edge in diff), "wrong crossing vs incidence distinction")
    witness(graph,receipt["witness"])
    return labels,graph,old_cut,sha(path.read_bytes())


def core(old):
    file = DATA/"core.json"
    rec = read(file)
    graph = original(rec,"core",None)
    labels = rec["labels"]
    diff = full(graph,rec["original"]["graph_digest"],labels,rec["verification"])
    ledger(rec["edge_ledger"],diff)
    expected = dict(zip(SPINE,(8,0,13,1,11,5),strict=True))
    for i,(hub,*leaves) in ((0,(4,3)),(1,(9,6,2)),(3,(12,10,7))):
        expected[f"b:{i}:0"] = hub
        expected.update((f"l:{i}:0:{j}",value) for j,value in enumerate(leaves))
    require(labels == expected and labels["s:2"] == 13 and rec["root"] == {"vertex":"s:2","label":13},
            "wrong fixed new core or pin")
    old_edges = {key(edge) for edge in old[1]["edges"]}
    extra = key((HOST,FRESH))
    require(set(diff)-old_edges == {extra} and old_edges < set(diff) and set(labels)-old[0].keys() == {FRESH}
            and all(labels[v] == x+(1 if x >= 2 else 0) for v,x in old[0].items()) and labels[FRESH] == 2,
            "wrong named cut insertion")
    returned = check_cut(labels,diff,rec["returned_cut"],3,9,13)
    require(set(returned) == set(old[2]) | {extra} and returned[extra] == 7
            and all(returned[edge]==w+1 for edge,w in old[2].items()), "wrong returned crossing set")
    ins = rec["insertion"]
    require(ins["h"] == 1 and ins["fresh_leaf"] == FRESH and ins["fresh_label"] == 2
            and key(ins["edge"]) == extra and ins["retained_recheck_sha256_raw"] == old[3], "wrong insertion receipt")
    witness(graph,rec["witness"])
    return labels,diff,sha(file.read_bytes())


def target(t, base):
    name = f"target-t{t}"
    file = DATA/f"{name}.json"
    rec = read(file)
    graph = original(rec,name,t)
    digest = rec["original"]["graph_digest"]
    labels,prefix = rec["labels"],rec["prefix"]
    diff = full(graph,digest,labels,rec["verification"])
    ledger(rec["edge_ledger"],diff)
    require(rec["parameters"] == {"t":t,"K":1} and rec["core"] == {"path":"core.json","sha256_raw":base[2]}
            and all(labels[v] == x+1 for v,x in base[0].items())
            and all(diff[edge] == w for edge,w in base[1].items()), "wrong lift or core binding")
    new_names = [f"l:2:0:{j}" for j in range(t)]
    m = t+14
    require(labels[ZERO] == 0 and labels["s:2"] == 14 and [labels[v] for v in new_names] == list(range(15,m+1))
            and diff[key(("s:2",ZERO))] == 14 and [diff[key((ZERO,v))] for v in new_names] == list(range(15,m+1)),
            "wrong original restored branch")
    require(set(labels)-prefix.keys() == {"s:5"} and all(type(x) is int and x==labels[v] for v,x in prefix.items())
            and rec["remaining_vertices"] == ["s:5"], "wrong preserved prefix or missing vertex")
    suffix = ("s:4","s:5")
    pre_diff = weights(graph["edges"],prefix)
    ledger(rec["prefix_edge_ledger"],pre_diff)
    require(set(diff)-set(pre_diff) == {key(rec["crossing_edge"])} == {suffix}, "wrong crossing")
    R = sorted(set(range(m+1))-set(prefix.values()))
    D = sorted(set(range(1,m+1))-set(pre_diff.values()))
    pre = rec["partial_verification"]
    require(R == [6] == rec["unused_labels"] == pre["unused_labels"]
            and D == [6] == rec["unused_differences"] == pre["unused_differences"], "wrong complements")
    require(pre["valid"] is True and pre["complete"] is False and not pre["errors"] and pre["graph_digest"] == digest
            and pre["n"] == m+1 and pre["m"] == m and pre["frontier"] == ["s:4"]
            and pre["used_labels"] == sorted(prefix.values()) and pre["used_differences"] == sorted(pre_diff.values()),
            "wrong prefix checker receipt")
    final = rec["completion"]
    require(rec["port"] == {"vertex":"s:4","label":12} and prefix["s:4"] == 12
            and final["vertex"] == "s:5" and final["label"] == R[0] == labels["s:5"]
            and key(final["edge"]) == suffix and final["difference"] == diff[suffix] == D[0],"wrong final edge")
    witness(graph,rec["prefix_witness"],prefix=True)
    witness(graph,rec["witness"])
    return labels,graph,{"t":t,"K":1,"n":m+1,"certificate":file.name,
                         "sha256_raw":sha(file.read_bytes()),"bytes":file.stat().st_size}


def batches(records):
    file = DATA/"batch_comparison.json"
    rec = read(file)
    require((rec["base_t"],rec["via_t"],rec["same_target_t"]) == (3,4,5)
            and rec["fresh_names"] == ["l:2:0:3","l:2:0:4"] and rec["pointwise_equal"] is True
            and rec["additional_targets"] == 0,"wrong comparison scope")
    for a,b in ((3,4),(3,5),(4,5)):
        old,old_graph,_ = records[a]
        new,new_graph,_ = records[b]
        fresh = [f"l:2:0:{j}" for j in range(a,b)]
        require(set(new)-old.keys() == set(fresh) and all(new[v]==x for v,x in old.items())
                and [new[v] for v in fresh] == list(range(a+15,b+15)) and old[ZERO] == new[ZERO] == 0,
                "wrong preserved labels or maxima")
        before,after = ({key(edge) for edge in g["edges"]} for g in (old_graph,new_graph))
        require(before < after and after-before == {key((ZERO,v)) for v in fresh},"wrong growth edges")
    require(rec["intermediate"] == records[4][0]
            and rec["one_batch"] == rec["successive_batches"] == rec["direct"] == records[5][0],
            "wrong pointwise comparison")
    return sha(file.read_bytes())


def main():
    config = read(HERE/"config.json")
    identity_path = DATA/"identity.json"
    identity = read(identity_path)
    require(tuple(config["completed_t"]) == CASES and config["completed_orders"] == [18,19,20,21]
            and config["new_core_profile"] == topology(2,None)[0] and config["retained"] == OLD_CERT
            and config["cut"] == 2 and config["host"] == HOST and config["insertion_size"] ==
            config["workers"] == config["K"] == 1 and config["max_vertices"] == 21 and config["max_result_bytes"] == CAP
            and config["solver_queries"] == config["computational_enumeration"] == config["historical_search_replay"] == 0,
            "wrong frozen scope")
    require(identity["run_id"] == config["run_id"] and identity["parent"] == config["parent"], "wrong identity")
    for name,field in (("validate.py","runner_sha256_raw"),("audit.py","audit_sha256_raw"),("config.json","config_sha256_raw")):
        require(sha((HERE/name).read_bytes()) == identity[field],"wrong frozen input")
    for rel,digest in identity["proof_sha256_raw"].items():
        require(sha((ROOT/rel).read_bytes()) == digest,"wrong proof bytes")
    for rel,digest in identity["source_sha256_raw"].items():
        require(sha((DATA/"source"/rel).read_bytes()) == digest,"wrong source snapshot")
    for rel,digest in identity["retained_sha256_raw"].items():
        raw = (ROOT/rel).read_bytes()
        lf = raw.replace(b"\r\n",b"\n")
        variants = (raw,lf,lf.replace(b"\n",b"\r\n")) if rel.endswith(".md") else (raw,)
        require(digest in {sha(item) for item in variants},"wrong retained identity")
    old = retained()
    supplied = core(old)
    cases = {t:target(t,supplied) for t in CASES}
    completed = [case[2] for case in cases.values()]
    batch_hash = batches(cases)
    rejects = read(DATA/"domain_rejections.json")
    require([(x["type"],x["value"]) for x in rejects] == [("bool",True),("float",3.0),("str","3"),("int",2)]
            and all(type(x["value"]).__name__ == x["type"] and x["error"] == "t must be an exact integer >= 3"
                    for x in rejects),"wrong domain rejections")
    summary = read(DATA/"summary.json")
    require(summary["status"] == "PASS" and summary["run_id"] == config["run_id"]
            and summary["identity_sha256_raw"] == sha(identity_path.read_bytes())
            and summary["retained_rechecks"] == summary["auxiliary_cores"] == 1
            and summary["retained_recheck_sha256_raw"] == old[3] and summary["core_sha256_raw"] == supplied[2]
            and summary["completed_targets"] == completed and summary["batch_comparison_sha256_raw"] == batch_hash
            and summary["domain_rejections"] == len(rejects) == 4 and summary["solver_queries"]
            == summary["computational_enumeration"] == summary["historical_search_replay"] == 0,"wrong summary")
    result = {"run_id":config["run_id"],"status":"PASS","same_retained_rechecks":1,
              "same_retained_recheck_sha256_raw":old[3],"same_auxiliary_cores":1,"same_core_sha256_raw":supplied[2],
              "same_completed_targets":completed,"same_batch_comparison_sha256_raw":batch_hash,"same_domain_rejections":4,
              "additional_cores":0,"additional_completed_targets":0,
              "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    raw = (json.dumps(result,indent=2,sort_keys=True)+"\n").encode()
    require(len(raw) <= CAP,"audit output exceeds byte limit")
    with (HERE/"audit_result.json").open("xb") as output:
        output.write(raw)
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
