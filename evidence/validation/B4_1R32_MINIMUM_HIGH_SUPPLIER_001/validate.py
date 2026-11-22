"""Search-free validation of the declared 1R32 originals and shared prefixes."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.consumers import _nonadjacent_path_labels
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

RUN = "B4-1R32-MINIMUM-HIGH-SUPPLIER-001-20261121"
PARENT = "5b8de6e2f6ef1b271311cfa4bfe151b92308e3bf"
OUTPUT = HERE / "validation"
CAP = 2_000_000
L, U, H, Z = "b:0:0", "s:4", "b:1:0", "b:2:0"
W = [L, "s:0", "s:1", "s:2", "s:3", U]
PROOF = "research/B4_1R32_MINIMUM_HIGH_SUPPLIER.md"
OLD = "evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/validation"
OLD_CERT, OLD_GRAPH = f"{OLD}/normalized-t3.json", f"{OLD}/originals/normalized-t3.json"
SOURCE = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "lcl/consumers.py",
          "requirements.txt", "pyproject.toml")
RETAINED = (
    "research/B4_12T2_ZERO_HOST_SUPPLIER.md", "research/ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md",
    "research/ALPHA_ZERO_HOST_LEAF_EXTENSION.md", "research/B2_NONADJACENT_CONSUMER.md",
    "research/B4_UNPADDED_Q1T2.md", "research/B4_12T2_K1_ROOTED_CORE.md",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/raw_result.json",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json", OLD_CERT, OLD_GRAPH,
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    raw = (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= CAP, f"oversized result: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def domain(name, value, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an exact integer >= {minimum}")


def order(r, K):
    domain("r", r, 3)
    domain("K", K, 2)
    return r + K + 15


def normalized(r):
    domain("r", r, 3)
    labels = {
        "s:0": r+9, "s:1": 7, "s:2": r+14, "s:3": 4, "s:4": r+7,
        "b:0:0": 1, "l:0:0:0": r+10,
        "b:1:0": r+6, "l:1:0:0": 6, "l:1:0:1": 5,
        "b:2:0": 0, "l:2:0:0": r+11, "l:2:0:1": r+12, "l:2:0:2": r+13,
        "b:3:0": r+8, "l:3:0:0": 2, "l:3:0:1": 3,
    }
    labels.update({f"l:1:0:{j}": j+6 for j in range(2,r)})
    return labels


def hold(name, profile, n):
    require(n <= 25, "campaign order limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == n and len(graph["edges"]) == n-1, "wrong order")
    digest = graph_digest(graph)
    path = OUTPUT / "originals" / f"{name}.json"
    raw_hash = save(path, {"graph": graph, "graph_digest": digest})
    return graph, {"path": f"originals/{path.name}", "graph_digest": digest, "sha256_raw": raw_hash}


def ledger(graph, labels):
    return [{"edge":[u,v], "difference":abs(labels[u]-labels[v])}
            for u,v in graph["edges"] if u in labels and v in labels]


def alpha_state(graph, labels, r):
    p = r+6
    require((labels[L],labels[U],labels[H],labels[Z]) == (1,p+1,p,0)
            and sorted(x for x in labels.values() if x<p) == list(range(p))
            and all((labels[u]<p) != (labels[v]<p) for u,v in graph["edges"]), "wrong alpha/host state")
    adj = {v:set() for v in graph["vertices"]}
    for u,v in graph["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    require(all(v in adj[u] for u,v in zip(W[:-1],W[1:],strict=True)), "wrong witness path")
    distances = dict.fromkeys(W,0)
    for depth in (1,2):
        frontier = [v for v,d in distances.items() if d == depth-1]
        for v in frontier:
            for u in adj[v]:
                distances.setdefault(u,depth)
    require(set(distances) == set(graph["vertices"]) and distances[H] == distances[Z] == 1
            and H in adj["s:1"] and Z in adj["s:2"], "wrong physical host witness")
    return {"state":{"n":r+15,"p":p,"x":1,"y":1,"L":L,"U":U,"H":H,"Z":Z,
                     "minimum_high_label":p,"zero_label":0},
            "alpha":{"low_size":p,"low":sorted(v for v in labels if labels[v]<p),
                     "high":sorted(v for v in labels if labels[v]>=p)},
            "witness":W,"witness_distances":distances}


def check_retained():
    cert_raw, original_raw = (ROOT/OLD_CERT).read_bytes(), (ROOT/OLD_GRAPH).read_bytes()
    cert, old = json.loads(cert_raw), json.loads(original_raw)
    graph,digest = old["graph"], old["graph_digest"]
    labels = cert["labels"]
    require(graph["profile"] == [[1],[2],[3],[2],[]] and len(graph["vertices"]) == 17
            and graph_digest(graph) == digest == cert["original"]["graph_digest"]
            and cert["original"]["sha256_raw"] == sha(original_raw), "wrong retained original")
    check = verify_certificate(graph,labels,digest)
    require(check["valid"] and cert["edge_ledger"] == ledger(graph,labels)
            and (labels["l:1:0:0"],labels["l:1:0:1"]) == (6,5), "wrong retained labels or spectrum")
    state = alpha_state(graph,labels,2)
    require(all(state[key] == cert[key] for key in ("alpha","witness","witness_distances")),
            "retained classes or witness disagree")
    receipt = {"certificate":OLD_CERT,"certificate_sha256_raw":sha(cert_raw),"original":OLD_GRAPH,
               "original_sha256_raw":sha(original_raw),"graph_digest":digest,"verification":check,**state}
    return graph,labels,receipt


def check_seed(r, original, retained_hash):
    graph,ref = original
    labels = normalized(r)
    check = verify_certificate(graph,labels,ref["graph_digest"])
    require(check["valid"], "wrong normalized certificate")
    return {"r":r,"original":ref,"labels":labels,"edge_ledger":ledger(graph,labels),
            "retained_recheck_sha256_raw":retained_hash,"verification":check,**alpha_state(graph,labels,r)}


def check_target(r, K, original, seed, seed_hash):
    graph,ref = original
    p = seed["state"]["p"]
    require(p == r+6, "wrong updated high cut")
    prefix = {v:x+K if x>=p else x for v,x in seed["labels"].items()}
    path = [f"s:{i}" for i in range(4,K+5)]
    pending = set(path[1:])
    required = {frozenset(edge) for edge in zip(path[:-1],path[1:],strict=True)}
    actual = [edge for edge in graph["edges"] if pending.intersection(edge)]
    require(set(graph["vertices"])-prefix.keys() == pending and len(actual) == K
            and set(map(frozenset,actual)) == required, "wrong unfinished path")
    crossing = [edge for edge in actual if set(edge) & prefix.keys()]
    require(crossing == [["s:4","s:5"]], "wrong crossing")
    partial = verify_partial(graph,prefix)
    require(partial["valid"] and not partial["complete"] and partial["graph_digest"] == ref["graph_digest"]
            and partial["frontier"] == [U] and partial["unused_labels"] == list(range(p,p+K))
            and partial["unused_differences"] == list(range(1,K+1)) and prefix[U] == p+K+1, "wrong resources")
    sequence = _nonadjacent_path_labels(K,p)
    require(len(sequence) == K+1 and sequence[0] == prefix[U], "wrong sequence binding")
    labels = {**prefix, **dict(zip(path[1:],sequence[1:],strict=True))}
    check = verify_certificate(graph,labels,ref["graph_digest"])
    require(check["valid"], "full check failed on retained original")
    return {"parameters":{"r":r,"K":K}, "original":ref,
            "normalized":{"path":f"normalized-r{r}.json","sha256_raw":seed_hash},
            "shift_cut":p,"prefix":prefix,"prefix_edge_ledger":ledger(graph,prefix),"partial_verification":partial,
            "port":{"vertex":U,"label":prefix[U]},"crossing_edge":crossing[0],
            "unused_labels":partial["unused_labels"],"unused_differences":partial["unused_differences"],
            "remaining_vertices":path[1:],"path":path,"path_labels":sequence,
            "suffix_edge_ledger":ledger({"edges":actual},labels),"labels":labels,
            "edge_ledger":ledger(graph,labels),"verification":check}


def append_minimum_high(labels, r, h):
    p = r+6
    require(len(labels) == r+15 and labels[H] == p, "wrong minimum-high growth premise")
    fresh = {f"l:1:0:{r+i}": p+i for i in range(h)}
    require(not labels.keys() & fresh.keys(), "fresh name collision")
    moved = {v:x+(h if x>=p else 0) for v,x in labels.items()}
    return {**moved,**fresh}


def batch_check(old_graph, old_labels, seeds, originals):
    unit = old_labels
    from_graph = old_graph
    stages = []
    for r in (3,4,5):
        unit = append_minimum_high(unit,r-1,1)
        to_graph,ref = originals[r]
        require(unit == seeds[r]["labels"], "unit batch disagrees with declared named labels")
        before,after = ({frozenset(e) for e in g["edges"]} for g in (from_graph,to_graph))
        fresh = f"l:1:0:{r-1}"
        require(set(to_graph["vertices"])-set(from_graph["vertices"]) == {fresh}
                and before < after and after-before == {frozenset((H,fresh))}, "wrong named unit-batch growth")
        predicates = alpha_state(to_graph,unit,r)
        require(all(seeds[r][key] == value for key,value in predicates.items()), "wrong intermediate state")
        stages.append({"r":r,"fresh_leaf":fresh,"fresh_label":unit[fresh],"original":ref,
                       "labels":unit,"state":predicates["state"]})
        from_graph = to_graph
    final = seeds[5]["labels"]
    one_batch = append_minimum_high(old_labels,2,3)
    require(one_batch == unit == final and [final[f"l:1:0:{j}"] for j in (2,3,4)] == [8,9,10],
            "wrong final named labels")
    return {"base_r":2,"same_prefix_r":5,"unit_stages":stages,
            "direct":final,"one_batch":one_batch,"unit_batches":unit,"pointwise_equal":True,
            "additional_prefixes":0,"additional_targets":0}


def reject_inputs():
    records = []
    for r,K in ((True,2),(3.0,2),("3",2),(2,2),(3,True),(3,2.0),(3,"2"),(3,1)):
        try:
            order(r,K)
        except ValueError as error:
            records.append({"r":r,"K":K,"r_type":type(r).__name__,"K_type":type(K).__name__,"error":str(error)})
        else:
            raise ValueError("invalid pair admitted")
    return records


def main():
    cfg = HERE/"config.json"
    config = json.loads(cfg.read_bytes())
    require(config == {"run_id":RUN,"parent":PARENT,"workers":1,"max_vertices":25,"max_result_bytes":CAP,
                       "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0,"fixed_third":3,
                       "normalized_r":[3,4,5],"completed_r_K":[[3,2],[3,3],[4,4],[5,5]],
                       "completed_orders":[20,21,23,25],"retained":OLD_CERT,"exit_offset":1},
            "campaign configuration changed")
    require(subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip() == PARENT, "unexpected parent")
    require(not subprocess.check_output(["git","diff","HEAD","--name-only","--","lcl","references"],cwd=ROOT),
            "protected source changed")
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in {(3,12),(3,13)}, "wrong Python")
    OUTPUT.mkdir(exist_ok=False)
    sources = {}
    for rel in SOURCE:
        raw = (ROOT/rel).read_bytes()
        path = OUTPUT/"source"/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open("xb") as f:
            f.write(raw)
        sources[rel] = sha(raw)
    identity = {"run_id":RUN,"parent":PARENT,"config_sha256_raw":sha(cfg.read_bytes()),
                "runner_sha256_raw":sha(Path(__file__).read_bytes()),"audit_sha256_raw":sha((HERE/"audit.py").read_bytes()),
                "proof":{"path":PROOF,"sha256_raw":sha((ROOT/PROOF).read_bytes())},"source_sha256_raw":sources,
                "retained_sha256_raw":{rel:sha((ROOT/rel).read_bytes()) for rel in RETAINED},
                "runtime":{"implementation":sys.implementation.name,"python":sys.version,
                           "executable":Path(sys.executable).relative_to(ROOT).as_posix(),"platform":platform.platform(),
                           "utf8_mode":sys.flags.utf8_mode,"third_party_imports":[]}}
    ident_hash = save(OUTPUT/"identity.json",identity)
    rejects = reject_inputs()
    save(OUTPUT/"domain_rejections.json",rejects)
    originals = {r:hold(f"normalized-r{r}",[[1],[r],[3],[2],[]],r+15) for r in config["normalized_r"]}
    targets = {}
    for (r,K),n in zip(config["completed_r_K"],config["completed_orders"],strict=True):
        require(order(r,K) == n, "wrong declared order")
        targets[r,K] = hold(f"target-r{r}-K{K}",[[1],[r],[3],[2]]+[[] for _ in range(K+1)],n)
    old_graph,old_labels,retained = check_retained()
    retained_hash = save(OUTPUT/"retained_recheck.json",retained)
    seeds,hashes = {},{}
    for r,original in originals.items():
        seeds[r] = check_seed(r,original,retained_hash)
        hashes[r] = save(OUTPUT/f"normalized-r{r}.json",seeds[r])
    batch_hash = save(OUTPUT/"batch_comparison.json",batch_check(old_graph,old_labels,seeds,originals))
    completed = []
    for (r,K),original in targets.items():
        case = check_target(r,K,original,seeds[r],hashes[r])
        path = OUTPUT/f"target-r{r}-K{K}.json"
        digest = save(path,case)
        completed.append({"r":r,"K":K,"n":case["verification"]["n"],"certificate":path.name,
                          "bytes":path.stat().st_size,"sha256_raw":digest})
    summary = {"run_id":RUN,"identity_sha256_raw":ident_hash,"status":"PASS",
               "completed_targets":completed,"normalized_prefixes":sorted(seeds),"retained_rechecks":1,
               "retained_recheck_sha256_raw":retained_hash,"batch_comparison_sha256_raw":batch_hash,
               "domain_rejections":len(rejects),"solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    save(OUTPUT/"summary.json",summary)
    print(json.dumps(summary,sort_keys=True))


if __name__ == "__main__":
    main()
