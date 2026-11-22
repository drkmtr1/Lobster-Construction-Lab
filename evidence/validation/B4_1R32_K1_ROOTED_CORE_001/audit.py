"""Independently audit the same declared 1R32 K=1 graphs and comparisons."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CASES = (3,4,5)
SPINE = tuple(f"s:{j}" for j in range(6))
HOST,ZERO = "b:1:0","b:2:0"
OLD = "evidence/validation/B4_12T2_K1_ROOTED_CORE_001/validation"
OLD_CERT,OLD_GRAPH = f"{OLD}/core.json", f"{OLD}/originals/core.json"
CAP = 2_000_000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    require(len(raw) <= CAP,"result exceeds byte limit")
    return json.loads(raw)


def key(edge):
    u,v = edge
    return tuple(sorted((u,v)))


def topology(r, full):
    counts = {0:1,1:r,3:2}
    if full:
        counts[2] = 3
    roles = {s:{"kind":"spine","section":i} for i,s in enumerate(SPINE)}
    edges = list(zip(SPINE[:-1],SPINE[1:],strict=True))
    for i,n in counts.items():
        b = f"b:{i}:0"
        roles[b] = {"kind":"branch","section":i,"branch":0}
        edges.append((SPINE[i],b))
        for j in range(n):
            v = f"l:{i}:0:{j}"
            roles[v] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
            edges.append((b,v))
    return [[counts[i]] if i in counts else [] for i in range(6)],roles,edges


def graph_check(graph, digest, r, full):
    profile,roles,edges = topology(r,full)
    require(graph["schema_version"] == 1 and graph["profile"] == profile and tuple(graph["spine"]) == SPINE
            and graph["roles"] == roles and Counter(graph["vertices"]) == Counter(list(roles))
            and Counter(map(key,graph["edges"])) == Counter(map(key,edges)), "wrong graph names, roles, or edge multiplicity")
    # All edge-key dictionaries used later follow this multiplicity check.
    canonical = {"profile":profile,"spine":SPINE,"roles":roles,"vertices":sorted(roles),"edges":sorted(map(key,edges))}
    raw = json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    require(sha(raw) == digest and len(roles) == r+(16 if full else 12) <= 21
            and len(edges) == len(roles)-1, "wrong original digest or size")


def original(record,name,r,full):
    ref = record["original"]
    require(ref["path"] == f"originals/{name}.json","wrong original path")
    path = DATA/ref["path"]
    saved = read(path)
    require(sha(path.read_bytes()) == ref["sha256_raw"] and saved["graph_digest"] == ref["graph_digest"],
            "wrong original byte binding")
    graph_check(saved["graph"],ref["graph_digest"],r,full)
    return saved["graph"]


def weights(edges,labels):
    return {key((u,v)):abs(labels[u]-labels[v]) for u,v in edges if u in labels and v in labels}


def ledger(entries, expected):
    require(Counter((key(row["edge"]),row["difference"]) for row in entries) == Counter(expected.items()),
            "wrong named edge ledger")


def check_full(graph,digest,labels,receipt):
    m = len(graph["edges"])
    require(set(labels) == set(graph["vertices"]) and all(type(x) is int for x in labels.values())
            and Counter(labels.values()) == Counter(range(m+1)), "wrong complete labels")
    diff = weights(graph["edges"],labels)
    require(Counter(diff.values()) == Counter(range(1,m+1)) and receipt["valid"] is True
            and not receipt["errors"] and receipt["n"] == m+1 and receipt["m"] == m
            and receipt["graph_digest"] == digest
            and receipt["edge_differences"] == [diff[key(e)] for e in graph["edges"]], "wrong spectrum or checker result")
    return diff


def cut_check(record,labels,diff,c,b,m):
    below = {v for v,x in labels.items() if x < c}
    crossing = {edge:w for edge,w in diff.items() if len(set(edge)&below) == 1}
    other = {edge:w for edge,w in diff.items() if edge not in crossing}
    require(record["c"] == c and record["host"] == HOST and record["host_label"] == labels[HOST] == b
            and record["m"] == m and 1 <= c <= b <= m and Counter(record["below"]) == Counter(list(below))
            and record["crossing_spectrum"] == sorted(crossing.values()) == list(range(7,m+1))
            and record["noncrossing_spectrum"] == sorted(other.values()) == list(range(1,7))
            and b-c+1 == 7,"wrong complete cut condition")
    ledger(record["crossing"],crossing)
    ledger(record["noncrossing"],other)
    require(key(("s:4","s:5")) in other and other[("s:4","s:5")] == 6,"wrong final-edge classification")
    return crossing


def witness(graph,data,partial=False):
    path = SPINE[:-1] if partial else SPINE
    require(tuple(data["path"]) == path,"wrong full or truncated spine")
    pending = {"s:5"} if partial else set()
    adj = {v:set() for v in graph["vertices"] if v not in pending}
    for u,v in graph["edges"]:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    require(all(v in adj[u] for u,v in zip(path[:-1],path[1:],strict=True)),"witness nonedge")
    dist = dict.fromkeys(path,0)
    queue = deque(path)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u]+1
                queue.append(v)
    require(dist == data["distances"] and set(dist) == set(adj) and max(dist.values()) == 2
            and dist[HOST] == 1 and "s:1" in adj[HOST],"wrong witness distances")


def retained():
    path = DATA/"retained_recheck.json"
    row = read(path)
    require((row["certificate"],row["original"]) == (OLD_CERT,OLD_GRAPH),"wrong sole retained record")
    cert_path,original_path = ROOT/OLD_CERT,ROOT/OLD_GRAPH
    old,held = read(cert_path),read(original_path)
    graph,digest = held["graph"],held["graph_digest"]
    require(sha(cert_path.read_bytes()) == row["certificate_sha256_raw"]
            and sha(original_path.read_bytes()) == row["original_sha256_raw"] == old["original"]["sha256_raw"]
            and digest == row["graph_digest"] == old["original"]["graph_digest"],"wrong raw retained binding")
    graph_check(graph,digest,2,False)
    labels = old["labels"]
    diff = check_full(graph,digest,labels,row["verification"])
    ledger(old["edge_ledger"],diff)
    expected = dict(zip(SPINE,(8,0,13,1,11,5),strict=True))
    for i,(b,*leaves) in ((0,(4,3)),(1,(9,6,2)),(3,(12,10,7))):
        expected[f"b:{i}:0"] = b
        expected.update((f"l:{i}:0:{j}",x) for j,x in enumerate(leaves))
    require(labels == expected and row["root"] == old["root"] == {"vertex":"s:2","label":13},"wrong retained ledger")
    cross = cut_check(row["cut"],labels,diff,3,9,13)
    require(row["cut"] == old["returned_cut"] and len(cross)==7 and all(any(labels[v]>=3 for v in e) for e in diff),
            "wrong crossing versus upper-incidence premise")
    witness(graph,row["witness"])
    return labels,graph,row["cut"],diff,cross,sha(path.read_bytes())


def core(r,base):
    name = f"core-r{r}"
    file = DATA/f"{name}.json"
    row = read(file)
    graph = original(row,name,r,False)
    labels = row["labels"]
    diff = check_full(graph,row["original"]["graph_digest"],labels,row["verification"])
    ledger(row["edge_ledger"],diff)
    require(row["r"]==r and row["retained_recheck_sha256_raw"]==base[5]
            and row["root"] == {"vertex":"s:2","label":r+11} and labels["s:2"]==r+11,"wrong core binding/root")
    fresh = [f"l:1:0:{j}" for j in range(2,r)]
    require(set(labels)-base[0].keys() == set(fresh)
            and [labels[v] for v in fresh] == list(range(3,r+1))
            and all(labels[v] == x+(r-2 if x>=3 else 0) for v,x in base[0].items()), "wrong named core insertion")
    cross = cut_check(row["cut"],labels,diff,r+1,r+7,r+11)
    new = {key((HOST,v)) for v in fresh}
    require(set(diff)-set(base[3]) == new and set(cross)==set(base[4])|new
            and all(diff[e] == x+(r-2 if e in base[4] else 0) for e,x in base[3].items()),
            "wrong core weight transport or incidence")
    witness(graph,row["witness"])
    return labels,graph,row["cut"],diff,cross,{"r":r,"n":r+12,"sha256_raw":sha(file.read_bytes())}


def target(r,a):
    name = f"target-r{r}"
    file = DATA/f"{name}.json"
    row = read(file)
    graph = original(row,name,r,True)
    digest = row["original"]["graph_digest"]
    labels,prefix = row["labels"],row["prefix"]
    diff = check_full(graph,digest,labels,row["verification"])
    ledger(row["edge_ledger"],diff)
    require(row["parameters"] == {"r":r,"K":1,"third":3}
            and row["core"] == {"path":f"core-r{r}.json","sha256_raw":a[5]["sha256_raw"]}
            and all(labels[v] == x+1 for v,x in a[0].items())
            and all(diff[e] == x for e,x in a[3].items()), "wrong named lift or core identity")
    third = [f"l:2:0:{j}" for j in range(3)]
    required = {key(("s:2",ZERO)), *(key((ZERO,v)) for v in third)}
    require(set(diff)-set(a[3]) == required and labels[ZERO]==0 and labels["s:2"]==r+12
            and [labels[v] for v in third] == list(range(r+13,r+16))
            and sorted(diff[e] for e in required) == list(range(r+12,r+16)),"wrong restored branch")
    cross = cut_check(row["cut"],labels,diff,r+2,r+8,r+15)
    require(set(cross)==set(a[4])|required,"wrong cut transport")
    edge = ("s:4","s:5")
    pre = weights(graph["edges"],prefix)
    ledger(row["prefix_edge_ledger"],pre)
    require(set(labels)-prefix.keys()=={"s:5"} and row["remaining_vertices"]==["s:5"]
            and all(type(x) is int and labels[v]==x for v,x in prefix.items())
            and set(diff)-set(pre)=={key(row["crossing_edge"])}=={edge},"wrong preserved prefix or final edge")
    R = sorted(set(range(r+16))-set(prefix.values()))
    D = sorted(set(range(1,r+16))-set(pre.values()))
    receipt = row["partial_verification"]
    require(R == [r+4] == row["unused_labels"] == receipt["unused_labels"]
            and D == [6] == row["unused_differences"] == receipt["unused_differences"],"wrong complements")
    require(receipt["valid"] is True and receipt["complete"] is False and not receipt["errors"]
            and receipt["n"]==r+16 and receipt["m"]==r+15 and receipt["graph_digest"]==digest
            and receipt["frontier"]==["s:4"] and receipt["used_labels"]==sorted(prefix.values())
            and receipt["used_differences"]==sorted(pre.values()),"wrong partial checker receipt")
    final = row["completion"]
    require(row["port"]=={"vertex":"s:4","label":r+10} and prefix["s:4"]==r+10
            and final["vertex"]=="s:5" and final["label"]==R[0]==labels["s:5"]
            and key(final["edge"])==edge and final["difference"]==diff[edge]==D[0],"wrong singleton conclusion")
    witness(graph,row["prefix_witness"],partial=True)
    witness(graph,row["witness"])
    return labels,graph,row["cut"],diff,cross,{"r":r,"K":1,"n":r+16,"certificate":file.name,
                                              "bytes":file.stat().st_size,"sha256_raw":sha(file.read_bytes())}


def growth_stage(stage, prior, final, r, q):
    labels,graph,cut,diff,cross,_ = prior
    values,new_graph,new_cut,new_diff,new_cross,_ = final
    h = q-r
    fresh = [f"l:1:0:{j}" for j in range(r,q)]
    edges = {key((HOST,v)) for v in fresh}
    require((stage["from_r"],stage["to_r"]) == (r,q) and stage["labels"] == values and stage["cut"] == new_cut
            and set(new_graph["vertices"])-set(graph["vertices"]) == set(fresh)
            and new_cut["c"]==cut["c"]+h and new_cut["host_label"]==cut["host_label"]+h,
            "wrong saved growth stage or returned cut")
    require(set(values)-labels.keys()==set(fresh)
            and [values[v] for v in fresh]==list(range(cut["c"],cut["c"]+h))
            and all(values[v]==x+(h if x>=cut["c"] else 0) for v,x in labels.items()),"wrong named batch labels")
    require(set(new_diff)-set(diff)==edges and set(new_cross)==set(cross)|edges
            and all(new_diff[e]==w+(h if e in cross else 0) for e,w in diff.items()),"wrong inherited edge weights")


def comparisons(base,cores,targets):
    path = DATA/"growth_comparison.json"
    row = read(path)
    c,f = row["core"],row["full"]
    require(row["same_r"] == 5 and row["pointwise_equal"] is True
            and row["additional_cores"] == row["additional_targets"] == 0
            and c["direct"]==cores[5][0] and f["direct"]==targets[5][0], "wrong comparison scope")
    growth_stage(c["one_batch"],base,cores[5],2,5)
    growth_stage(f["one_batch"],targets[3],targets[5],3,5)
    previous = base
    for r,stage in zip(CASES,c["unit_stages"],strict=True):
        growth_stage(stage,previous,cores[r],r-1,r)
        previous = cores[r]
    for r,stage in zip((4,5),f["unit_stages"],strict=True):
        growth_stage(stage,targets[r-1],targets[r],r-1,r)
    routes = {"one_batch":c["one_batch"]["labels"],"unit_batches":c["unit_stages"][-1]["labels"]}
    for name,core_values in routes.items():
        lifted = f["lifts_of_core_growth"][name]
        require(lifted == targets[5][0] and all(lifted[v]==x+1 for v,x in core_values.items())
                and lifted[ZERO]==0 and [lifted[f"l:2:0:{j}"] for j in range(3)]==[18,19,20],
                "wrong lift of saved growth route")
    names = [f"l:1:0:{j}" for j in (2,3,4)]
    require(row["fresh_names"] == names and [c["direct"][v] for v in names]==[3,4,5]
            and [f["direct"][v] for v in names]==[4,5,6],"wrong final fresh labels")
    return sha(path.read_bytes())


def main():
    config = read(HERE/"config.json")
    path = DATA/"identity.json"
    identity = read(path)
    require(tuple(config["completed_r"]) == tuple(config["core_r"]) == CASES
            and config["core_orders"] == [15,16,17] and config["completed_orders"] == [19,20,21]
            and config["retained"] == OLD_CERT and config["fixed_third"] == 3 and config["workers"] == config["K"] == 1
            and config["max_vertices"] == 21 and config["max_result_bytes"] == CAP and config["solver_queries"]
            == config["computational_enumeration"] == config["historical_search_replay"] == 0,"wrong frozen scope")
    require(identity["run_id"]==config["run_id"] and identity["parent"]==config["parent"],"wrong identity")
    for name,field in (("validate.py","runner_sha256_raw"),("audit.py","audit_sha256_raw"),("config.json","config_sha256_raw")):
        require(sha((HERE/name).read_bytes())==identity[field],"wrong frozen input")
    proof = identity["proof"]
    require(sha((ROOT/proof["path"]).read_bytes())==proof["sha256_raw"],"wrong proof bytes")
    for rel,digest in identity["source_sha256_raw"].items():
        require(sha((DATA/"source"/rel).read_bytes())==digest,"wrong source snapshot")
    for rel,digest in identity["retained_sha256_raw"].items():
        raw = (ROOT/rel).read_bytes()
        lf = raw.replace(b"\r\n",b"\n")
        variants = (raw,lf,lf.replace(b"\n",b"\r\n")) if rel.endswith(".md") else (raw,)
        require(digest in {sha(item) for item in variants},"wrong retained identity")
    base = retained()
    cores = {r:core(r,base) for r in CASES}
    targets = {r:target(r,cores[r]) for r in CASES}
    completed = [case[5] for case in targets.values()]
    batch = comparisons(base,cores,targets)
    rejected = read(DATA/"domain_rejections.json")
    require([(row["type"],row["value"]) for row in rejected] == [("bool",True),("float",3.0),("str","3"),("int",2)]
            and all(type(row["value"]).__name__==row["type"] and row["error"]=="r must be an exact integer >= 3"
                    for row in rejected),"wrong domain records")
    summary = read(DATA/"summary.json")
    require(summary["status"]=="PASS" and summary["run_id"]==config["run_id"]
            and summary["identity_sha256_raw"]==sha(path.read_bytes()) and summary["retained_rechecks"]==1
            and summary["retained_recheck_sha256_raw"]==base[5] and summary["auxiliary_cores"]==list(CASES)
            and summary["completed_targets"]==completed and summary["growth_comparison_sha256_raw"]==batch
            and summary["domain_rejections"]==len(rejected)==4 and summary["solver_queries"]
            == summary["computational_enumeration"]==summary["historical_search_replay"]==0,"wrong summary")
    result = {"run_id":config["run_id"],"status":"PASS","same_retained_rechecks":1,"same_retained_recheck_sha256_raw":base[5],
              "same_auxiliary_cores":[cores[r][5] for r in CASES],"same_completed_targets":completed,
              "same_growth_comparison_sha256_raw":batch,"same_domain_rejections":4,
              "additional_cores":0,"additional_completed_targets":0,
              "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    raw = (json.dumps(result,indent=2,sort_keys=True)+"\n").encode()
    require(len(raw)<=CAP,"oversized audit output")
    with (HERE/"audit_result.json").open("xb") as output:
        output.write(raw)
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
