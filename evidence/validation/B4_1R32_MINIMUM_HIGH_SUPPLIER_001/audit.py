"""Rebuild the named originals and audit the frozen 1R32 evidence without LCL."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CASES = ((3,2),(3,3),(4,4),(5,5))
SEEDS = (3,4,5)
CAP = 2_000_000
L,U,H,Z = "b:0:0","s:4","b:1:0","b:2:0"
W = (L,"s:0","s:1","s:2","s:3",U)
OLD = "evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/validation"
OLD_CERT, OLD_GRAPH = f"{OLD}/normalized-t3.json", f"{OLD}/originals/normalized-t3.json"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    require(len(raw) <= CAP, "over byte cap")
    return json.loads(raw)


def key(edge):
    u,v = edge
    return tuple(sorted((u,v)))


def topology(r, K):
    spine = [f"s:{i}" for i in range(5+K)]
    counts = {0:1,1:r,2:3,3:2}
    profile = [[counts[i]] if i in counts else [] for i in range(len(spine))]
    roles = {v:{"kind":"spine","section":i} for i,v in enumerate(spine)}
    edges = list(zip(spine[:-1],spine[1:],strict=True))
    for i,n in counts.items():
        b = f"b:{i}:0"
        roles[b] = {"kind":"branch","section":i,"branch":0}
        edges.append((spine[i],b))
        for j in range(n):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
            edges.append((b,leaf))
    return profile,spine,roles,edges


def check_graph(graph, claimed, r, K):
    profile,spine,roles,edges = topology(r,K)
    require(graph["schema_version"] == 1 and graph["profile"] == profile and graph["spine"] == spine
            and graph["roles"] == roles and Counter(graph["vertices"]) == Counter(list(roles))
            and Counter(map(key,graph["edges"])) == Counter(map(key,edges)), "wrong named graph or edge multiplicity")
    # Canonicalization and later edge-key dictionaries follow the multiplicity check.
    canonical = {"profile":profile,"spine":spine,"roles":roles,"vertices":sorted(roles),"edges":sorted(map(key,edges))}
    raw = json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    require(sha(raw) == claimed and len(roles) == r+K+15 <= 25 and len(edges) == len(roles)-1, "wrong graph digest or order")


def original(record,name,r,K):
    ref = record["original"]
    require(ref["path"] == f"originals/{name}.json", "wrong original path")
    file = DATA/ref["path"]
    saved = read(file)
    require(sha(file.read_bytes()) == ref["sha256_raw"] and saved["graph_digest"] == ref["graph_digest"],
            "wrong original byte binding")
    check_graph(saved["graph"],ref["graph_digest"],r,K)
    return saved["graph"]


def weights(edges,labels):
    return {key((u,v)):abs(labels[u]-labels[v]) for u,v in edges if u in labels and v in labels}


def ledger(rows,expected):
    require(Counter((key(row["edge"]),row["difference"]) for row in rows) == Counter(expected.items()),
            "wrong complete edge ledger")


def full(graph,digest,labels,receipt):
    m = len(graph["edges"])
    require(set(labels) == set(graph["vertices"]) and all(type(x) is int for x in labels.values())
            and Counter(labels.values()) == Counter(range(m+1)), "wrong full label spectrum")
    diff = weights(graph["edges"],labels)
    require(Counter(diff.values()) == Counter(range(1,m+1)), "wrong full edge spectrum")
    require(receipt["valid"] is True and not receipt["errors"] and receipt["graph_digest"] == digest
            and receipt["n"] == m+1 and receipt["m"] == m
            and receipt["edge_differences"] == [diff[key(edge)] for edge in graph["edges"]],
            "wrong checker receipt")
    return diff


def state(graph,labels,record,r):
    p = r+6
    lows = {"s:1","s:3","b:0:0","b:2:0","l:3:0:0","l:3:0:1"} | {f"l:1:0:{j}" for j in range(r)}
    highs = set(graph["vertices"])-lows
    actual = record["alpha"]
    require(Counter(actual["low"]) == Counter(list(lows)) and Counter(actual["high"]) == Counter(list(highs))
            and actual["low_size"] == len(lows) == p and len(highs) == 9
            and {labels[v] for v in lows} == set(range(p)) and all((u in lows)!=(v in lows) for u,v in graph["edges"]),
            "wrong alpha classes")
    require(record["state"] == {"n":r+15,"p":p,"x":1,"y":1,"L":L,"U":U,"H":H,"Z":Z,
                                "minimum_high_label":p,"zero_label":0} and
            (labels[L],labels[U],labels[H],labels[Z]) == (1,p+1,p,0), "wrong physical ports or hosts")
    adjacency = {v:set() for v in graph["vertices"]}
    for u,v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(tuple(record["witness"]) == W and all(v in adjacency[u] for u,v in zip(W[:-1],W[1:],strict=True)),
            "wrong witness path")
    distances = dict.fromkeys(W,0)
    queue = deque(W)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in distances:
                distances[v] = distances[u]+1
                queue.append(v)
    require(distances == record["witness_distances"] and set(distances) == set(graph["vertices"])
            and max(distances.values()) == 2 and distances[H] == distances[Z] == 1
            and "s:1" in adjacency[H] and "s:2" in adjacency[Z], "wrong witness distances or anchors")


def retained():
    path = DATA/"retained_recheck.json"
    rec = read(path)
    require((rec["certificate"],rec["original"]) == (OLD_CERT,OLD_GRAPH), "wrong retained scope")
    cert,source = ROOT/OLD_CERT,ROOT/OLD_GRAPH
    saved,held = read(cert),read(source)
    require(sha(cert.read_bytes()) == rec["certificate_sha256_raw"]
            and sha(source.read_bytes()) == rec["original_sha256_raw"] == saved["original"]["sha256_raw"]
            and rec["graph_digest"] == held["graph_digest"] == saved["original"]["graph_digest"],
            "wrong retained identities")
    graph,labels = held["graph"],saved["labels"]
    check_graph(graph,rec["graph_digest"],2,0)
    differences = full(graph,rec["graph_digest"],labels,rec["verification"])
    ledger(saved["edge_ledger"],differences)
    state(graph,labels,rec,2)
    require(all(rec[k] == saved[k] for k in ("alpha","witness","witness_distances")), "wrong retained predicates")
    expected = dict(zip(graph["spine"],(11,7,16,4,9),strict=True))
    for i,(b,*leaves) in ((0,(1,12)),(1,(8,6,5)),(2,(0,13,14,15)),(3,(10,2,3))):
        expected[f"b:{i}:0"] = b
        expected.update((f"l:{i}:0:{j}",label) for j,label in enumerate(leaves))
    require(labels == expected, "wrong retained ledger")
    return labels,graph,differences,sha(path.read_bytes())


def seed(r, base):
    name = f"normalized-r{r}"
    file = DATA/f"{name}.json"
    rec = read(file)
    graph = original(rec,name,r,0)
    labels = rec["labels"]
    diff = full(graph,rec["original"]["graph_digest"],labels,rec["verification"])
    ledger(rec["edge_ledger"],diff)
    state(graph,labels,rec,r)
    require(rec["r"] == r and rec["retained_recheck_sha256_raw"] == base[3], "wrong seed identity")
    fresh = [f"l:1:0:{j}" for j in range(2,r)]
    require(all(labels[v] == x+(r-2 if x>=8 else 0) for v,x in base[0].items())
            and [labels[v] for v in fresh] == list(range(8,r+6)), "wrong named insertion")
    require(all(diff[edge] == x+r-2 for edge,x in base[2].items())
            and [diff[key((H,v))] for v in fresh] == list(range(r-2,0,-1)), "wrong seed weight partition")
    return labels,graph,rec,{"r":r,"n":r+15,"sha256_raw":sha(file.read_bytes())}


def sequence(K):
    bases = {2:[3,1,0],3:[4,1,0,2],4:[5,1,2,0,3]}
    if K in bases:
        return bases[K]
    return [K+1,1,K-1,0]+[K-2-x for x in sequence(K-3)[1:]]


def target(r,K,normalized):
    name = f"target-r{r}-K{K}"
    file = DATA/f"{name}.json"
    rec = read(file)
    require(rec["parameters"] == {"r":r,"K":K}
            and rec["normalized"] == {"path":f"normalized-r{r}.json","sha256_raw":normalized[3]["sha256_raw"]},
            "wrong parameters or shared normalized certificate")
    graph = original(rec,name,r,K)
    digest = rec["original"]["graph_digest"]
    labels,prefix = rec["labels"],rec["prefix"]
    diff = full(graph,digest,labels,rec["verification"])
    ledger(rec["edge_ledger"],diff)
    p,m = r+6,r+K+14
    expected = {v:x+(K if x>=p else 0) for v,x in normalized[0].items()}
    require(rec["shift_cut"] == p and prefix == expected and all(type(x) is int and labels[v]==x for v,x in prefix.items()),
            "wrong updated shift or changed prefix")
    diff_prefix = weights(graph["edges"],prefix)
    ledger(rec["prefix_edge_ledger"],diff_prefix)
    R = sorted(set(range(m+1))-set(prefix.values()))
    D = sorted(set(range(1,m+1))-set(diff_prefix.values()))
    partial = rec["partial_verification"]
    require(R == list(range(p,p+K)) == rec["unused_labels"] == partial["unused_labels"]
            and D == list(range(1,K+1)) == rec["unused_differences"] == partial["unused_differences"], "wrong complements")
    require(partial["valid"] is True and partial["complete"] is False and not partial["errors"]
            and partial["graph_digest"] == digest and partial["frontier"] == [U] and partial["n"] == m+1
            and partial["m"] == m and partial["used_labels"] == sorted(prefix.values())
            and partial["used_differences"] == sorted(diff_prefix.values()), "wrong partial checker record")
    path = graph["spine"][4:]
    suffix = {edge:w for edge,w in diff.items() if edge not in diff_prefix}
    ledger(rec["suffix_edge_ledger"],suffix)
    require(set(labels)-prefix.keys() == set(path[1:]) and rec["remaining_vertices"] == path[1:]
            and rec["path"] == path and len(path) == K+1
            and set(suffix) == {key(edge) for edge in zip(path[:-1],path[1:],strict=True)}
            and {edge for edge in suffix if set(edge) & prefix.keys()} == {key(rec["crossing_edge"])} == {("s:4","s:5")}
            and sorted(suffix.values()) == D, "wrong original suffix")
    require(rec["port"] == {"vertex":U,"label":p+K+1}
            and rec["path_labels"] == [labels[v] for v in path] == [p+x for x in sequence(K)]
            and sorted(labels[v] for v in path[1:]) == R, "wrong physical sequence mapping")
    return {"r":r,"K":K,"n":m+1,"certificate":file.name,"bytes":file.stat().st_size,"sha256_raw":sha(file.read_bytes())}


def batches(base,seeds):
    path = DATA/"batch_comparison.json"
    rec = read(path)
    require((rec["base_r"],rec["same_prefix_r"]) == (2,5) and rec["pointwise_equal"] is True
            and rec["additional_prefixes"] == rec["additional_targets"] == 0
            and [stage["r"] for stage in rec["unit_stages"]] == list(SEEDS), "wrong declared batch scope")
    old,graph = base[:2]
    for stage,r in zip(rec["unit_stages"],SEEDS,strict=True):
        new,expanded,saved,_ = seeds[r]
        fresh = f"l:1:0:{r-1}"
        require(stage["fresh_leaf"] == fresh and stage["fresh_label"] == new[fresh] == r+5
                and set(new)-old.keys() == {fresh} and all(new[v] == x+(1 if x>=r+5 else 0) for v,x in old.items()),
                "wrong unit growth")
        before,after = ({key(edge) for edge in item["edges"]} for item in (graph,expanded))
        require(before < after and after-before == {key((H,fresh))}, "wrong named growth incidence")
        require(stage["labels"] == new and stage["original"] == saved["original"] and stage["state"] == saved["state"],
                "wrong intermediate normalized state")
        old,graph = new,expanded
    last = seeds[5][0]
    require(rec["direct"] == rec["one_batch"] == rec["unit_batches"] == last
            and [last[f"l:1:0:{j}"] for j in (2,3,4)] == [8,9,10], "wrong final named comparison")
    return sha(path.read_bytes())


def main():
    config = read(HERE/"config.json")
    identity_file = DATA/"identity.json"
    identity = read(identity_file)
    require(tuple(map(tuple,config["completed_r_K"])) == CASES and tuple(config["normalized_r"]) == SEEDS
            and config["completed_orders"] == [20,21,23,25] and config["retained"] == OLD_CERT
            and config["fixed_third"] == 3 and config["exit_offset"] == config["workers"] == 1 and
            config["max_vertices"] == 25 and config["max_result_bytes"] == CAP and config["solver_queries"]
            == config["computational_enumeration"] == config["historical_search_replay"] == 0, "wrong scope")
    require(identity["run_id"] == config["run_id"] and identity["parent"] == config["parent"],"wrong run identity")
    for name,field in (("validate.py","runner_sha256_raw"),("audit.py","audit_sha256_raw"),("config.json","config_sha256_raw")):
        require(sha((HERE/name).read_bytes()) == identity[field], "wrong frozen input")
    proof = identity["proof"]
    require(sha((ROOT/proof["path"]).read_bytes()) == proof["sha256_raw"], "wrong proof bytes")
    for rel,digest in identity["source_sha256_raw"].items():
        require(sha((DATA/"source"/rel).read_bytes()) == digest,"wrong frozen source")
    for rel,digest in identity["retained_sha256_raw"].items():
        raw = (ROOT/rel).read_bytes()
        lf = raw.replace(b"\r\n",b"\n")
        variants = (raw,lf,lf.replace(b"\n",b"\r\n")) if rel.endswith(".md") else (raw,)
        require(digest in {sha(item) for item in variants}, "wrong retained identity")
    base = retained()
    seeds = {r:seed(r,base) for r in SEEDS}
    cases = [target(r,K,seeds[r]) for r,K in CASES]
    batch_hash = batches(base,seeds)
    rejects = read(DATA/"domain_rejections.json")
    bad = ((True,2),(3.0,2),("3",2),(2,2),(3,True),(3,2.0),(3,"2"),(3,1))
    for i,(row,(r,K)) in enumerate(zip(rejects,bad,strict=True)):
        require(type(row["r"]) is type(r) and type(row["K"]) is type(K) and
                (row["r"],row["K"],row["r_type"],row["K_type"]) == (r,K,type(r).__name__,type(K).__name__)
                and row["error"] == ("r must be an exact integer >= 3" if i<4 else "K must be an exact integer >= 2"),
                "wrong rejection receipt")
    summary = read(DATA/"summary.json")
    require(summary["status"] == "PASS" and summary["run_id"] == config["run_id"]
            and summary["identity_sha256_raw"] == sha(identity_file.read_bytes())
            and summary["completed_targets"] == cases and summary["normalized_prefixes"] == list(SEEDS)
            and summary["retained_rechecks"] == 1 and summary["retained_recheck_sha256_raw"] == base[3]
            and summary["batch_comparison_sha256_raw"] == batch_hash and summary["domain_rejections"] == len(rejects) == 8
            and summary["solver_queries"] == summary["computational_enumeration"] == summary["historical_search_replay"] == 0,
            "wrong summary")
    result = {"run_id":config["run_id"],"status":"PASS","same_completed_targets":cases,
              "same_normalized_prefixes":[seeds[r][3] for r in SEEDS],"same_retained_rechecks":1,
              "same_retained_recheck_sha256_raw":base[3],"same_batch_comparison_sha256_raw":batch_hash,
              "same_domain_rejections":8,"additional_prefixes":0,"additional_completed_targets":0,
              "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    raw = (json.dumps(result,indent=2,sort_keys=True)+"\n").encode()
    require(len(raw) <= CAP,"audit result exceeds cap")
    with (HERE/"audit_result.json").open("xb") as out:
        out.write(raw)
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
