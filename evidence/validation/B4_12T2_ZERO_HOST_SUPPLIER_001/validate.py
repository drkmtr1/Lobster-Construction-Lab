"""Bounded search-free 12T2 validation on independently retained originals."""

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

RUN = "B4-12T2-ZERO-HOST-SUPPLIER-001-20261121"
PARENT = "2ac6611d8051d944a4d6723fbc271ddc6935ae07"
OUTPUT = HERE / "validation"
CAP = 2_000_000
P = 8
L, U, Z = "b:0:0", "s:4", "b:2:0"
W = [L, "s:0", "s:1", "s:2", "s:3", U]
PROOF = "research/B4_12T2_ZERO_HOST_SUPPLIER.md"
CONTROL = "evidence/validation/B4_UNPADDED_1R22_SUPPLIER_001/validation"
CONTROL_CERT = f"{CONTROL}/normalized-r2.json"
CONTROL_GRAPH = f"{CONTROL}/originals/normalized-r2.json"
SOURCE = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "lcl/consumers.py",
          "requirements.txt", "pyproject.toml")
RETAINED = (
    "research/B4_1R22_K1_ROOTED_CORE.md", "research/B4_UNPADDED_1R22_SUPPLIER.md",
    "research/ALPHA_ZERO_HOST_LEAF_EXTENSION.md", "research/ALPHA_UPPER_BLOCK_GENERAL_HOST.md",
    "research/B4_THIRD_ZERO_HOST_NONADJACENT.md", "research/B2_NONADJACENT_CONSUMER.md",
    "research/B4_UNPADDED_QR12.md", CONTROL_CERT, CONTROL_GRAPH,
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


def domain(name, value, lower):
    if type(value) is not int or value < lower:
        raise ValueError(f"{name} must be an exact integer >= {lower}")


def order(t, K):
    domain("t", t, 3)
    domain("K", K, 2)
    return t + K + 14


def normalized(t):
    domain("t", t, 3)
    labels = {
        "s:0": 11, "s:1": 7, "s:2": 16, "s:3": 4, "s:4": 9,
        "b:0:0": 1, "l:0:0:0": 12,
        "b:1:0": 8, "l:1:0:0": 6, "l:1:0:1": 5,
        "b:2:0": 0, "b:3:0": 10, "l:3:0:0": 2, "l:3:0:1": 3,
    }
    labels.update({f"l:2:0:{j}": (13 if j < 3 else 14) + j for j in range(t)})
    return labels


def hold(name, profile, n):
    require(n <= 24, "campaign order limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == n and len(graph["edges"]) == n-1, "wrong order")
    digest = graph_digest(graph)
    path = OUTPUT / "originals" / f"{name}.json"
    raw_hash = save(path, {"graph": graph, "graph_digest": digest})
    return graph, {"path": f"originals/{path.name}", "graph_digest": digest, "sha256_raw": raw_hash}


def ledger(graph, labels):
    return [{"edge":[u,v], "difference":abs(labels[u]-labels[v])}
            for u,v in graph["edges"] if u in labels and v in labels]


def witness_distances(graph):
    adj = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    require(all(v in adj[u] for u,v in zip(W[:-1],W[1:],strict=True)), "wrong witness path")
    distances = dict.fromkeys(W, 0)
    for depth in (1, 2):
        frontier = [v for v,d in distances.items() if d == depth-1]
        for v in frontier:
            for u in adj[v]:
                distances.setdefault(u, depth)
    require(set(distances) == set(graph["vertices"]) and distances[Z] == 1, "wrong witness distance")
    return distances


def check_seed(t, original):
    graph, ref = original
    labels = normalized(t)
    check = verify_certificate(graph, labels, ref["graph_digest"])
    require(check["valid"] and all((labels[u] < P) != (labels[v] < P) for u,v in graph["edges"]),
            "wrong alpha certificate")
    require((labels[L], labels[U], labels[Z]) == (1,9,0), "wrong physical ports or host")
    return {"t":t, "original":ref, "labels":labels, "edge_ledger":ledger(graph,labels),
            "alpha":{"low_size":P, "low":sorted(v for v in labels if labels[v]<P),
                     "high":sorted(v for v in labels if labels[v]>=P)},
            "state":{"n":t+14,"p":P,"x":1,"y":1,"L":L,"U":U,"Z":Z,"host_label":0},
            "witness":W, "witness_distances":witness_distances(graph), "verification":check}


def check_target(t, K, original, seed, seed_hash):
    graph, ref = original
    prefix = {v: x+K if x>=P else x for v,x in seed["labels"].items()}
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
            and partial["frontier"] == [U] and partial["unused_labels"] == list(range(P,P+K))
            and partial["unused_differences"] == list(range(1,K+1)) and prefix[U] == P+K+1, "wrong resources")
    sequence = _nonadjacent_path_labels(K,P)
    require(len(sequence) == K+1 and sequence[0] == prefix[U], "wrong sequence binding")
    labels = {**prefix, **dict(zip(path[1:],sequence[1:],strict=True))}
    check = verify_certificate(graph,labels,ref["graph_digest"])
    require(check["valid"], "full check failed on retained original")
    return {"parameters":{"t":t,"K":K}, "original":ref,
            "normalized":{"path":f"normalized-t{t}.json","sha256_raw":seed_hash},
            "prefix":prefix,"prefix_edge_ledger":ledger(graph,prefix),"partial_verification":partial,
            "port":{"vertex":U,"label":prefix[U]},"crossing_edge":crossing[0],
            "unused_labels":partial["unused_labels"],"unused_differences":partial["unused_differences"],
            "remaining_vertices":path[1:],"path":path,"path_labels":sequence,
            "suffix_edge_ledger":ledger({"edges":actual},labels),"labels":labels,
            "edge_ledger":ledger(graph,labels),"verification":check}


def append_zero(old, t, h):
    require(old[Z] == 0 and len(old) == t+14, "wrong supplied growth premise")
    fresh = {f"l:2:0:{t+i}":len(old)+i for i in range(h)}
    require(not old.keys() & fresh.keys(), "fresh name collision")
    return {**old, **fresh}


def batch_check(records, originals):
    three,four,five = (records[t]["labels"] for t in (3,4,5))
    intermediate = append_zero(three,3,1)
    one_batch = append_zero(three,3,2)
    repeated = append_zero(intermediate,4,1)
    require(intermediate == four and one_batch == repeated == five, "wrong named batch labels")
    for old,new in ((3,4),(3,5),(4,5)):
        before,after = (originals[t][0] for t in (old,new))
        fresh = {f"l:2:0:{j}" for j in range(old,new)}
        old_edges,new_edges = ({frozenset(e) for e in graph["edges"]} for graph in (before,after))
        require(set(before["vertices"]) < set(after["vertices"])
                and set(after["vertices"])-set(before["vertices"]) == fresh and old_edges < new_edges
                and new_edges-old_edges == {frozenset((Z,v)) for v in fresh}, "wrong growth incidence")
    return {"base_t":3,"via_t":4,"same_prefix_t":5,"fresh_names":["l:2:0:3","l:2:0:4"],
            "intermediate":intermediate,"one_batch":one_batch,"successive_batches":repeated,"direct":five,
            "ports_and_host":{v:five[v] for v in (L,U,Z)},"same_witness":W,"pointwise_equal":True,
            "additional_prefixes":0,"additional_targets":0}


def check_control():
    cert_raw = (ROOT/CONTROL_CERT).read_bytes()
    orig_raw = (ROOT/CONTROL_GRAPH).read_bytes()
    prior, held = json.loads(cert_raw), json.loads(orig_raw)
    graph, digest = held["graph"], held["graph_digest"]
    labels = prior["labels"]
    require(graph["profile"] == [[1],[2],[2],[2],[]] and len(graph["vertices"]) == 16
            and graph_digest(graph) == digest == prior["original"]["graph_digest"]
            and prior["original"]["sha256_raw"] == sha(orig_raw), "wrong retained original")
    check = verify_certificate(graph,labels,digest)
    require(check["valid"] and (labels[Z],labels[U]) == (3,9)
            and all((labels[u]<P) != (labels[v]<P) for u,v in graph["edges"]), "wrong retained alpha or anchors")
    occur = []
    for c in range(10,16):
        selected = sorted(v for v,x in labels.items() if x>=c)
        incident = [row for row in ledger(graph,labels) if set(row["edge"]).intersection(selected)]
        values = sorted(row["difference"] for row in incident)
        required = list(range(c-3,16))
        require(values != required, "retained ledger supplies the disputed premise")
        occur.append({"c":c,"selected":selected,"incident":incident,"spectrum":values,"required":required})
    require([len(row["spectrum"]) for row in occur] == [11,10,9,8,5,3]
            and occur[4]["spectrum"] == [8,12,13,14,15], "wrong proof comparison")
    return {"certificate":CONTROL_CERT,"certificate_sha256_raw":sha(cert_raw),"original":CONTROL_GRAPH,
            "original_sha256_raw":sha(orig_raw),"graph_digest":digest,"check":check,
            "p":P,"port":{"vertex":U,"label":9},"host":{"vertex":Z,"label":3},"cuts":occur}


def reject_inputs():
    records = []
    for name,low,values in (("t",3,(True,3.0,"3",2)),("K",2,(True,2.0,"2",1))):
        for value in values:
            args = {"t":3,"K":2,name:value}
            try:
                order(**args)
            except ValueError as error:
                require(str(error) == f"{name} must be an exact integer >= {low}", "wrong rejection")
                records.append({"parameter":name,"value":value,"type":type(value).__name__,"error":str(error)})
            else:
                raise ValueError("invalid case admitted")
    return records


def main():
    cfg = HERE/"config.json"
    config = json.loads(cfg.read_bytes())
    require(config == {"run_id":RUN,"parent":PARENT,"workers":1,"max_vertices":24,"max_result_bytes":CAP,
                       "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0,
                       "normalized_t":[3,4,5],"completed_t_K":[[3,2],[3,3],[4,4],[5,5]],
                       "completed_orders":[19,20,22,24],"retained":CONTROL_CERT,"exit_offset":1},
            "campaign configuration changed")
    require(subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip() == PARENT, "unexpected parent")
    require(not subprocess.check_output(["git","diff","HEAD","--name-only","--","lcl","references"],cwd=ROOT),
            "protected source changed")
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in {(3,12),(3,13)}, "wrong project Python")
    OUTPUT.mkdir(exist_ok=False)
    sources = {}
    for rel in SOURCE:
        raw = (ROOT/rel).read_bytes()
        path = OUTPUT/"source"/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        sources[rel] = sha(raw)
    adjacent = f"{PARENT}:research/PROOF_OBLIGATIONS.md"
    adjacent_raw = subprocess.check_output(["git","show",adjacent],cwd=ROOT)
    identity = {"run_id":RUN,"parent":PARENT,"config_sha256_raw":sha(cfg.read_bytes()),
                "runner_sha256_raw":sha(Path(__file__).read_bytes()),"audit_sha256_raw":sha((HERE/"audit.py").read_bytes()),
                "proof":{"path":PROOF,"sha256_raw":sha((ROOT/PROOF).read_bytes())},"source_sha256_raw":sources,
                "retained_sha256_raw":{rel:sha((ROOT/rel).read_bytes()) for rel in RETAINED},
                "parent_adjacent_argument":{"git_revision_path":adjacent,"sha256_raw":sha(adjacent_raw)},
                "runtime":{"implementation":sys.implementation.name,"python":sys.version,
                           "executable":Path(sys.executable).relative_to(ROOT).as_posix(),
                           "platform":platform.platform(),"utf8_mode":sys.flags.utf8_mode,"third_party_imports":[]}}
    identity_hash = save(OUTPUT/"identity.json",identity)
    seeds = {t:hold(f"normalized-t{t}",[[1],[2],[t],[2],[]],t+14) for t in config["normalized_t"]}
    targets = {}
    for (t,K),n in zip(config["completed_t_K"],config["completed_orders"],strict=True):
        require(order(t,K) == n,"wrong declared order")
        targets[t,K] = hold(f"target-t{t}-K{K}",[[1],[2],[t],[2]]+[[] for _ in range(K+1)],n)
    retained_hash = save(OUTPUT/"retained_control.json", check_control())
    rejections = reject_inputs()
    save(OUTPUT/"domain_rejections.json",rejections)
    normalized_records, normalized_hashes = {}, {}
    for t,original in seeds.items():
        normalized_records[t] = check_seed(t,original)
        normalized_hashes[t] = save(OUTPUT/f"normalized-t{t}.json",normalized_records[t])
    batch_hash = save(OUTPUT/"batch_comparison.json",batch_check(normalized_records,seeds))
    completed = []
    for (t,K),original in targets.items():
        case = check_target(t,K,original,normalized_records[t],normalized_hashes[t])
        path = OUTPUT/f"target-t{t}-K{K}.json"
        digest = save(path,case)
        completed.append({"t":t,"K":K,"n":case["verification"]["n"],"certificate":path.name,
                          "bytes":path.stat().st_size,"sha256_raw":digest})
    summary = {"run_id":RUN,"identity_sha256_raw":identity_hash,"status":"PASS",
               "completed_targets":completed,"normalized_prefixes":sorted(seeds),"fixed_seed_t":3,
               "retained_rechecks":1,"retained_control_sha256_raw":retained_hash,
               "batch_comparison_sha256_raw":batch_hash,"domain_rejections":len(rejections),
               "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    save(OUTPUT/"summary.json",summary)
    print(json.dumps(summary,sort_keys=True))


if __name__ == "__main__":
    main()
