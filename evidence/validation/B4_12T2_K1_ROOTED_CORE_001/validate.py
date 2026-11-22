"""Check one retained core, its named cut insertion, and the declared singletons."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

RUN = "B4-12T2-K1-ROOTED-CORE-001-20261121"
PARENT = "78b20e7687ad7c414ada38a60d4b69996dc14829"
OUTPUT = HERE / "validation"
CAP = 2_000_000
CUT, HOST, FRESH = 2, "b:1:0", "l:1:0:1"
CORE_PROFILE = [[1], [2], [], [2], [], []]
OLD_CORE = "evidence/validation/B4_THIRD_ZERO_HOST_K1_DIRECT_001/validation"
OLD_CERT, OLD_GRAPH = f"{OLD_CORE}/core_certificate.json", f"{OLD_CORE}/originals/core.json"
PROOFS = ("research/ORDINARY_CUT_LEAF_INSERTION.md", "research/B4_12T2_K1_ROOTED_CORE.md")
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "requirements.txt", "pyproject.toml")
RETAINED = (
    "research/B4_12T2_ZERO_HOST_SUPPLIER.md", "research/B4_THIRD_ZERO_HOST_K1_DIRECT.md",
    "research/B4_Q1T2_K1_ROOTED_CORE.md", "research/B4_1R22_K1_ROOTED_CORE.md",
    "research/ALPHA_LOWER_BLOCK_LEAF_INSERTION.md", "research/B4_UNPADDED_QR12.md",
    "research/B4_UNPADDED_1R22_SUPPLIER.md", OLD_CERT, OLD_GRAPH,
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, record):
    raw = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= CAP, f"record exceeds byte limit: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(raw)
    return sha(raw)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def plan(t):
    if type(t) is not int or t < 3:
        raise ValueError("t must be an exact integer >= 3")
    return t + 15


def hold(name, profile, size):
    require(size <= 21, "declared graph would exceed order limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == size and len(graph["edges"]) == size-1, "wrong graph count")
    digest = graph_digest(graph)
    file = OUTPUT / "originals" / f"{name}.json"
    record_hash = save(file, {"graph": graph, "graph_digest": digest})
    return graph, {"path": f"originals/{file.name}", "graph_digest": digest, "sha256_raw": record_hash}


def ledger(graph, labels):
    return [{"edge": [u,v], "difference": abs(labels[u]-labels[v])}
            for u,v in graph["edges"] if u in labels and v in labels]


def cuts(graph, labels, c):
    crossing, other = [], []
    for row in ledger(graph, labels):
        u,v = row["edge"]
        (crossing if (labels[u]<c) != (labels[v]<c) else other).append(row)
    crossing_spectrum = sorted(row["difference"] for row in crossing)
    require(crossing_spectrum == list(range(labels[HOST]-c+1,len(graph["edges"])+1)), "wrong cut premise")
    return {"c":c, "host":HOST, "host_label":labels[HOST], "m":len(graph["edges"]),
            "below":sorted(v for v,x in labels.items() if x<c),
            "crossing":crossing,"crossing_spectrum":crossing_spectrum,
            "noncrossing":other,"noncrossing_spectrum":sorted(row["difference"] for row in other)}


def witness(graph, prefix=False):
    path = graph["spine"][:-1] if prefix else graph["spine"]
    edges = {frozenset(edge) for edge in graph["edges"]}
    require(path == [f"s:{i}" for i in range(5 if prefix else 6)]
            and all(frozenset(edge) in edges for edge in zip(path[:-1],path[1:],strict=True)), "wrong spine")
    distances = dict.fromkeys(path,0)
    for name,role in graph["roles"].items():
        s = f"s:{role['section']}"
        if role["kind"] == "branch":
            require(s in path and frozenset((s,name)) in edges,"wrong center incidence")
            distances[name] = 1
        elif role["kind"] == "leaf":
            b = f"b:{role['section']}:0"
            require(s in path and frozenset((s,b)) in edges and frozenset((b,name)) in edges,
                    "wrong terminal incidence")
            distances[name] = 2
    require(set(distances) == set(graph["vertices"]) - ({"s:5"} if prefix else set()), "witness incomplete")
    return {"path":path,"distances":distances}


def check_retained():
    cert_raw, graph_raw = (ROOT/OLD_CERT).read_bytes(), (ROOT/OLD_GRAPH).read_bytes()
    cert, graph = json.loads(cert_raw), json.loads(graph_raw)
    digest = graph_digest(graph)
    labels = cert["labels"]
    require(graph["profile"] == [[1],[1],[],[2],[],[]] and len(graph["vertices"]) == 13
            and digest == cert["original"]["graph_digest"] and sha(graph_raw) == cert["original"]["sha256_raw"],
            "wrong retained graph")
    verification = verify_certificate(graph,labels,digest)
    require(verification["valid"] and labels["s:2"] == 12 and (labels[HOST],labels["s:1"],labels["s:3"]) == (8,0,1)
            and cert["edge_ledger"] == ledger(graph,labels), "wrong retained ledger or root")
    cut = cuts(graph,labels,CUT)
    require(cut["crossing_spectrum"] == list(range(7,13)) and cut["below"] == ["s:1","s:3"], "wrong initial cut")
    w = witness(graph)
    require(w["distances"][HOST] == 1, "wrong retained host distance")
    return graph, labels, {"certificate":OLD_CERT,"certificate_sha256_raw":sha(cert_raw),
                           "original":OLD_GRAPH,"original_sha256_raw":sha(graph_raw),"graph_digest":digest,
                           "root":{"vertex":"s:2","label":12},"cut":cut,"witness":w,"verification":verification}


def new_core(original, old_graph, old_labels, retained_hash, old_cut):
    graph, ref = original
    old_edges, edges = ({frozenset(e) for e in item["edges"]} for item in (old_graph,graph))
    require(set(graph["vertices"]) == set(old_labels) | {FRESH} and old_edges < edges
            and edges-old_edges == {frozenset((HOST,FRESH))}, "wrong one-leaf original")
    labels = {v:x+(x>=CUT) for v,x in old_labels.items()}
    labels[FRESH] = CUT
    expected = {"s:0":8,"s:1":0,"s:2":13,"s:3":1,"s:4":11,"s:5":5,
                "b:0:0":4,"l:0:0:0":3,"b:1:0":9,"l:1:0:0":6,"l:1:0:1":2,
                "b:3:0":12,"l:3:0:0":10,"l:3:0:1":7}
    verification = verify_certificate(graph,labels,ref["graph_digest"])
    require(labels == expected and verification["valid"], "wrong new core or physical root")
    cut = cuts(graph,labels,CUT+1)
    require({frozenset(row["edge"]) for row in cut["crossing"]}
            == {frozenset(row["edge"]) for row in old_cut["crossing"]} | {frozenset((HOST,FRESH))}
            and cut["crossing_spectrum"] == list(range(7,14)) and cut["host_label"] == 9,
            "wrong returned crossing set")
    return {"original":ref,"labels":labels,"edge_ledger":ledger(graph,labels),
            "root":{"vertex":"s:2","label":13},"returned_cut":cut,"witness":witness(graph),
            "insertion":{"h":1,"fresh_leaf":FRESH,"edge":[HOST,FRESH],"fresh_label":2,
                         "retained_recheck_sha256_raw":retained_hash},
            "verification":verification}


def supply_prefix(t, core):
    plan(t)
    require(core["s:2"] == 13, "wrong maximum-rooted core")
    prefix = {v:x+1 for v,x in core.items() if v!="s:5"}
    prefix["b:2:0"] = 0
    prefix.update({f"l:2:0:{j}":15+j for j in range(t)})
    return prefix


def check_target(t, original, core, core_hash):
    graph,ref = original
    prefix = supply_prefix(t,core["labels"])
    pending = [edge for edge in graph["edges"] if set(edge).difference(prefix)]
    require(set(graph["vertices"])-prefix.keys() == {"s:5"} and pending == [["s:4","s:5"]],
            "wrong physical remainder")
    partial = verify_partial(graph,prefix)
    a = core["labels"]
    port,label,weight = a["s:4"]+1,a["s:5"]+1,abs(a["s:4"]-a["s:5"])
    require((port,label,weight) == (12,6,6) and prefix["s:4"] == port
            and partial["valid"] and not partial["complete"] and partial["graph_digest"] == ref["graph_digest"]
            and partial["frontier"] == ["s:4"] and partial["unused_labels"] == [label]
            and partial["unused_differences"] == [weight] and abs(port-label) == weight, "wrong resources")
    full = {**prefix,"s:5":label}
    result = verify_certificate(graph,full,ref["graph_digest"])
    require(result["valid"], "full certificate failed")
    return {"parameters":{"t":t,"K":1},"original":ref,"core":{"path":"core.json","sha256_raw":core_hash},
            "prefix":prefix,"prefix_edge_ledger":ledger(graph,prefix),"partial_verification":partial,
            "prefix_witness":witness(graph,prefix=True),"port":{"vertex":"s:4","label":port},
            "crossing_edge":pending[0],"remaining_vertices":["s:5"],
            "unused_labels":partial["unused_labels"],"unused_differences":partial["unused_differences"],
            "completion":{"vertex":"s:5","label":label,"edge":pending[0],"difference":weight},
            "labels":full,"edge_ledger":ledger(graph,full),"witness":witness(graph),"verification":result}


def append_zero(labels, t, h):
    require(labels["b:2:0"] == 0 and len(labels) == t+15, "wrong growth premise")
    fresh = {f"l:2:0:{t+i}":len(labels)+i for i in range(h)}
    require(not labels.keys() & fresh.keys(), "fresh name collision")
    return {**labels,**fresh}


def batch_check(cases, originals):
    first, middle, last = (cases[t]["labels"] for t in (3,4,5))
    intermediate = append_zero(first,3,1)
    one_batch = append_zero(first,3,2)
    repeated = append_zero(intermediate,4,1)
    require(intermediate == middle and one_batch == repeated == last, "named batch disagreement")
    for old,new in ((3,4),(3,5),(4,5)):
        before,after = (originals[t][0] for t in (old,new))
        fresh = {f"l:2:0:{j}" for j in range(old,new)}
        old_edges,new_edges = ({frozenset(edge) for edge in graph["edges"]} for graph in (before,after))
        require(set(before["vertices"]) < set(after["vertices"])
                and set(after["vertices"])-set(before["vertices"]) == fresh and old_edges < new_edges
                and new_edges-old_edges == {frozenset(("b:2:0",v)) for v in fresh}, "wrong growth incidence")
    return {"base_t":3,"via_t":4,"same_target_t":5,"fresh_names":["l:2:0:3","l:2:0:4"],
            "intermediate":intermediate,"one_batch":one_batch,"successive_batches":repeated,"direct":last,
            "pointwise_equal":True,"additional_targets":0}


def rejections():
    rejected = []
    for value in (True,3.0,"3",2):
        try:
            plan(value)
        except ValueError as error:
            require(str(error) == "t must be an exact integer >= 3", "wrong rejection")
            rejected.append({"value":value,"type":type(value).__name__,"error":str(error)})
        else:
            raise ValueError("invalid input admitted")
    return rejected


def main():
    cfg = HERE/"config.json"
    config = json.loads(cfg.read_bytes())
    require(config == {"run_id":RUN,"parent":PARENT,"workers":1,"max_vertices":21,"max_result_bytes":CAP,
                       "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0,"retained":OLD_CERT,
                       "new_core_profile":CORE_PROFILE,"cut":CUT,"host":HOST,"insertion_size":1,
                       "K":1,"completed_t":[3,4,5,6],"completed_orders":[18,19,20,21]}, "changed campaign")
    require(git("rev-parse","HEAD").decode().strip() == PARENT, "unexpected parent")
    require(not git("diff","HEAD","--name-only","--","lcl","references"), "protected source changed")
    require(sys.implementation.name=="cpython" and sys.version_info[:2] in {(3,12),(3,13)}, "wrong project runtime")
    OUTPUT.mkdir(exist_ok=False)
    source_hashes = {}
    for rel in SOURCES:
        raw = (ROOT/rel).read_bytes()
        path = OUTPUT/"source"/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        source_hashes[rel] = sha(raw)
    identity = {"run_id":RUN,"parent":PARENT,"config_sha256_raw":sha(cfg.read_bytes()),
                "runner_sha256_raw":sha(Path(__file__).read_bytes()),"audit_sha256_raw":sha((HERE/"audit.py").read_bytes()),
                "proof_sha256_raw":{rel:sha((ROOT/rel).read_bytes()) for rel in PROOFS},"source_sha256_raw":source_hashes,
                "retained_sha256_raw":{rel:sha((ROOT/rel).read_bytes()) for rel in RETAINED},
                "runtime":{"implementation":sys.implementation.name,"python":sys.version,
                           "executable":Path(sys.executable).relative_to(ROOT).as_posix(),"platform":platform.platform(),
                           "utf8_mode":sys.flags.utf8_mode,"third_party_imports":[]}}
    identity_hash = save(OUTPUT/"identity.json",identity)
    held_core = hold("core",CORE_PROFILE,14)
    targets = {}
    for t,n in zip(config["completed_t"],config["completed_orders"],strict=True):
        require(plan(t)==n,"wrong declared order")
        targets[t] = hold(f"target-t{t}",[[1],[2],[t],[2],[],[]],n)
    rejected = rejections()
    save(OUTPUT/"domain_rejections.json",rejected)
    old_graph,old_labels,retained = check_retained()
    retained_hash = save(OUTPUT/"retained_recheck.json",retained)
    core = new_core(held_core,old_graph,old_labels,retained_hash,retained["cut"])
    core_hash = save(OUTPUT/"core.json",core)
    cases, completed = {}, []
    for t,original in targets.items():
        case = check_target(t,original,core,core_hash)
        path = OUTPUT/f"target-t{t}.json"
        digest = save(path,case)
        cases[t] = case
        completed.append({"t":t,"K":1,"n":case["verification"]["n"],"certificate":path.name,
                          "sha256_raw":digest,"bytes":path.stat().st_size})
    batch_hash = save(OUTPUT/"batch_comparison.json",batch_check(cases,targets))
    summary = {"run_id":RUN,"identity_sha256_raw":identity_hash,"status":"PASS","retained_rechecks":1,
               "retained_recheck_sha256_raw":retained_hash,"core_sha256_raw":core_hash,"auxiliary_cores":1,
               "completed_targets":completed,"batch_comparison_sha256_raw":batch_hash,"domain_rejections":len(rejected),
               "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    save(OUTPUT/"summary.json",summary)
    print(json.dumps(summary,sort_keys=True))


if __name__ == "__main__":
    main()
