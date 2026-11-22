"""Check declared 1R32 core and singleton cases without a solver."""

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

RUN = "B4-1R32-K1-ROOTED-CORE-001-20261121"
PARENT = "648ec01f4eaca4a8f71aa162f057a870485dd93c"
OUTPUT = HERE / "validation"
CAP = 2_000_000
HOST, ZERO = "b:1:0", "b:2:0"
PROOF = "research/B4_1R32_K1_ROOTED_CORE.md"
OLD = "evidence/validation/B4_12T2_K1_ROOTED_CORE_001/validation"
OLD_CERT, OLD_GRAPH = f"{OLD}/core.json", f"{OLD}/originals/core.json"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "requirements.txt", "pyproject.toml")
RETAINED = (
    "research/ORDINARY_CUT_LEAF_INSERTION.md", "research/B4_12T2_K1_ROOTED_CORE.md",
    "research/B4_1R32_MINIMUM_HIGH_SUPPLIER.md", "research/B4_THIRD_ZERO_HOST_K1_DIRECT.md",
    "research/B4_UNPADDED_Q1T2.md", "research/B4_12T2_ZERO_HOST_SUPPLIER.md",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/raw_result.json",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json", OLD_CERT, OLD_GRAPH,
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, data):
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= CAP, f"oversized record: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(raw)
    return sha(raw)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def plan(r):
    if type(r) is not int or r < 3:
        raise ValueError("r must be an exact integer >= 3")
    return r+16


def hold(name, profile, n):
    require(n <= 21, "campaign order limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == n and len(graph["edges"]) == n-1, "wrong order")
    digest = graph_digest(graph)
    path = OUTPUT/"originals"/f"{name}.json"
    raw_hash = save(path, {"graph":graph,"graph_digest":digest})
    return graph,{"path":f"originals/{path.name}","graph_digest":digest,"sha256_raw":raw_hash}


def ledger(graph, labels):
    return [{"edge":[u,v],"difference":abs(labels[u]-labels[v])}
            for u,v in graph["edges"] if u in labels and v in labels]


def cut_state(graph, labels, c):
    crossing,other = [],[]
    for row in ledger(graph,labels):
        u,v = row["edge"]
        ((crossing if (labels[u]<c)!=(labels[v]<c) else other)).append(row)
    b,m = labels[HOST],len(graph["edges"])
    crossing_weights = sorted(row["difference"] for row in crossing)
    other_weights = sorted(row["difference"] for row in other)
    require(1 <= c <= b <= m and crossing_weights == list(range(b-c+1,m+1))
            and other_weights == list(range(1,b-c+1)), "wrong complete cut spectra")
    return {"c":c,"host":HOST,"host_label":b,"m":m,"below":sorted(v for v,x in labels.items() if x<c),
            "crossing":crossing,"crossing_spectrum":crossing_weights,
            "noncrossing":other,"noncrossing_spectrum":other_weights}


def witness(graph, partial=False):
    path = graph["spine"][:-1] if partial else graph["spine"]
    edges = set(map(frozenset,graph["edges"]))
    require(path == [f"s:{j}" for j in range(5 if partial else 6)]
            and all(frozenset(e) in edges for e in zip(path[:-1],path[1:],strict=True)), "wrong spine witness")
    distances = dict.fromkeys(path,0)
    for v,role in graph["roles"].items():
        s = f"s:{role['section']}"
        b = f"b:{role['section']}:0"
        if role["kind"] == "branch":
            require(s in path and frozenset((v,s)) in edges, "wrong center incidence")
            distances[v] = 1
        elif role["kind"] == "leaf":
            require(s in path and frozenset((v,b)) in edges and frozenset((b,s)) in edges, "wrong terminal incidence")
            distances[v] = 2
    require(set(distances) == set(graph["vertices"])-({"s:5"} if partial else set())
            and distances[HOST] == 1, "wrong witness distances")
    return {"path":path,"distances":distances}


def recheck():
    cert_raw,original_raw = (ROOT/OLD_CERT).read_bytes(),(ROOT/OLD_GRAPH).read_bytes()
    cert,original = json.loads(cert_raw),json.loads(original_raw)
    graph,digest = original["graph"],original["graph_digest"]
    labels = cert["labels"]
    require(graph["profile"] == [[1],[2],[],[2],[],[]] and len(graph["vertices"]) == 14
            and graph_digest(graph) == digest == cert["original"]["graph_digest"]
            and sha(original_raw) == cert["original"]["sha256_raw"], "wrong retained original")
    checked = verify_certificate(graph,labels,digest)
    cut,w = cut_state(graph,labels,3),witness(graph)
    require(checked["valid"] and labels["s:2"] == 13 and cut["host_label"] == 9
            and cut["crossing_spectrum"] == list(range(7,14)) and len(cut["crossing"]) == 7
            and cert["edge_ledger"] == ledger(graph,labels) and cert["returned_cut"] == cut and cert["witness"] == w,
            "wrong retained cut or physical premise")
    return graph,labels,{"certificate":OLD_CERT,"certificate_sha256_raw":sha(cert_raw),"original":OLD_GRAPH,
                         "original_sha256_raw":sha(original_raw),"graph_digest":digest,
                         "root":{"vertex":"s:2","label":13},"cut":cut,"witness":w,"verification":checked}


def core_formula(r):
    plan(r)
    labels = {"s:0":r+6,"s:1":0,"s:2":r+11,"s:3":1,"s:4":r+9,"s:5":r+3,
              "b:0:0":r+2,"l:0:0:0":r+1,"b:1:0":r+7,"l:1:0:0":r+4,
              "b:3:0":r+10,"l:3:0:0":r+8,"l:3:0:1":r+5}
    labels.update({f"l:1:0:{j}":j+1 for j in range(1,r)})
    return labels


def check_core(r, original, retained_hash):
    graph,ref = original
    labels = core_formula(r)
    check = verify_certificate(graph,labels,ref["graph_digest"])
    require(check["valid"] and labels["s:2"] == r+11,"wrong core or physical root")
    return {"r":r,"original":ref,"labels":labels,"edge_ledger":ledger(graph,labels),
            "root":{"vertex":"s:2","label":r+11},"cut":cut_state(graph,labels,r+1),
            "witness":witness(graph),"retained_recheck_sha256_raw":retained_hash,"verification":check}


def lift(r, labels):
    shifted = {v:x+1 for v,x in labels.items()}
    shifted[ZERO] = 0
    shifted.update({f"l:2:0:{j}":r+13+j for j in range(3)})
    return shifted


def check_target(r, original, core, core_hash):
    graph,ref = original
    a = core["labels"]
    prefix = lift(r,{v:x for v,x in a.items() if v!="s:5"})
    pending = [edge for edge in graph["edges"] if set(edge)-prefix.keys()]
    require(set(graph["vertices"])-prefix.keys() == {"s:5"} and pending == [["s:4","s:5"]],"wrong physical remainder")
    partial = verify_partial(graph,prefix)
    port,label,weight = a["s:4"]+1,a["s:5"]+1,abs(a["s:4"]-a["s:5"])
    require((port,label,weight) == (r+10,r+4,6) and prefix["s:4"] == port and partial["valid"]
            and not partial["complete"] and partial["graph_digest"] == ref["graph_digest"]
            and partial["frontier"] == ["s:4"] and partial["unused_labels"] == [label]
            and partial["unused_differences"] == [weight] and abs(port-label) == weight, "wrong resources")
    labels = {**prefix,"s:5":label}
    checked = verify_certificate(graph,labels,ref["graph_digest"])
    require(checked["valid"],"full verification failed on original")
    return {"parameters":{"r":r,"K":1,"third":3},"original":ref,"core":{"path":f"core-r{r}.json","sha256_raw":core_hash},
            "prefix":prefix,"prefix_edge_ledger":ledger(graph,prefix),"partial_verification":partial,
            "prefix_witness":witness(graph,partial=True),"port":{"vertex":"s:4","label":port},
            "crossing_edge":pending[0],"remaining_vertices":["s:5"],
            "unused_labels":partial["unused_labels"],"unused_differences":partial["unused_differences"],
            "completion":{"vertex":"s:5","label":label,"edge":pending[0],"difference":weight},
            "labels":labels,"edge_ledger":ledger(graph,labels),"cut":cut_state(graph,labels,r+2),
            "witness":witness(graph),"verification":checked}


def grow(old_labels, old_cut, r, h):
    c = old_cut["c"]
    require(old_labels[HOST] == old_cut["host_label"], "wrong host premise")
    shifted = {v:x+(h if x>=c else 0) for v,x in old_labels.items()}
    fresh = {f"l:1:0:{r+i}":c+i for i in range(h)}
    require(not shifted.keys() & fresh.keys(),"fresh name collision")
    return {**shifted,**fresh}


def growth_step(before, after, current, expected, r, h):
    old_labels,old_cut = current["labels"],current["cut"]
    labels = grow(old_labels,old_cut,r,h)
    fresh = {f"l:1:0:{i}" for i in range(r,r+h)}
    old_edges,new_edges = ({frozenset(e) for e in graph["edges"]} for graph in (before,after))
    require(set(after["vertices"])-set(before["vertices"]) == fresh
            and set(before["vertices"]) < set(after["vertices"]) and old_edges < new_edges
            and new_edges-old_edges == {frozenset((HOST,v)) for v in fresh}, "wrong growth topology")
    returned = cut_state(after,labels,old_cut["c"]+h)
    require(labels == expected["labels"] and returned == expected["cut"]
            and witness(after) == expected["witness"], "wrong returned growth state")
    return {"from_r":r,"to_r":r+h,"labels":labels,"cut":returned}


def compare(old_graph, old_labels, retained, cores, originals, targets, target_originals):
    base = {"labels":old_labels,"cut":retained["cut"]}
    one_core = growth_step(old_graph,originals[5][0],base,cores[5],2,3)
    core_units = []
    previous,previous_graph = base,old_graph
    for r in (3,4,5):
        graph = originals[r][0]
        stage = growth_step(previous_graph,graph,previous,cores[r],r-1,1)
        core_units.append(stage)
        previous,previous_graph = stage,graph
    one_full = growth_step(target_originals[3][0],target_originals[5][0],targets[3],targets[5],3,2)
    full_units = []
    previous = targets[3]
    for r in (4,5):
        stage = growth_step(target_originals[r-1][0],target_originals[r][0],previous,targets[r],r-1,1)
        full_units.append(stage)
        previous = stage
    lifts = {"one_batch":lift(5,one_core["labels"]),"unit_batches":lift(5,core_units[-1]["labels"])}
    full = targets[5]["labels"]
    require(lifts["one_batch"] == lifts["unit_batches"] == one_full["labels"] == full_units[-1]["labels"] == full,
            "growth/lift disagreement")
    names = [f"l:1:0:{j}" for j in (2,3,4)]
    require([cores[5]["labels"][v] for v in names] == [3,4,5] and [full[v] for v in names] == [4,5,6],
            "wrong fresh named values")
    return {"same_r":5,"fresh_names":names,
            "core":{"direct":cores[5]["labels"],"one_batch":one_core,"unit_stages":core_units},
            "full":{"direct":full,"lifts_of_core_growth":lifts,"one_batch":one_full,"unit_stages":full_units},
            "pointwise_equal":True,"additional_cores":0,"additional_targets":0}


def rejections():
    rejected = []
    for value in (True,3.0,"3",2):
        try:
            plan(value)
        except ValueError as error:
            rejected.append({"value":value,"type":type(value).__name__,"error":str(error)})
        else:
            raise ValueError("invalid value admitted")
    return rejected


def main():
    cfg = HERE/"config.json"
    config = json.loads(cfg.read_bytes())
    require(config == {"run_id":RUN,"parent":PARENT,"workers":1,"max_vertices":21,"max_result_bytes":CAP,
                       "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0,"retained":OLD_CERT,
                       "core_r":[3,4,5],"core_orders":[15,16,17],"completed_r":[3,4,5],"completed_orders":[19,20,21],
                       "fixed_third":3,"K":1}, "changed configuration")
    require(git("rev-parse","HEAD").decode().strip() == PARENT,"unexpected parent")
    require(not git("diff","HEAD","--name-only","--","lcl","references"),"protected source changed")
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in {(3,12),(3,13)},"wrong Python")
    OUTPUT.mkdir(exist_ok=False)
    snapshots = {}
    for rel in SOURCES:
        raw = (ROOT/rel).read_bytes()
        path = OUTPUT/"source"/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open("xb") as f:
            f.write(raw)
        snapshots[rel] = sha(raw)
    identity = {"run_id":RUN,"parent":PARENT,"config_sha256_raw":sha(cfg.read_bytes()),
                "runner_sha256_raw":sha(Path(__file__).read_bytes()),"audit_sha256_raw":sha((HERE/"audit.py").read_bytes()),
                "proof":{"path":PROOF,"sha256_raw":sha((ROOT/PROOF).read_bytes())},"source_sha256_raw":snapshots,
                "retained_sha256_raw":{rel:sha((ROOT/rel).read_bytes()) for rel in RETAINED},
                "runtime":{"implementation":sys.implementation.name,"python":sys.version,
                           "executable":Path(sys.executable).relative_to(ROOT).as_posix(),"platform":platform.platform(),
                           "utf8_mode":sys.flags.utf8_mode,"third_party_imports":[]}}
    ident_hash = save(OUTPUT/"identity.json",identity)
    rejected = rejections()
    save(OUTPUT/"domain_rejections.json",rejected)
    originals = {r:hold(f"core-r{r}",[[1],[r],[],[2],[],[]],n)
                 for r,n in zip(config["core_r"],config["core_orders"],strict=True)}
    target_originals = {}
    for r,n in zip(config["completed_r"],config["completed_orders"],strict=True):
        require(plan(r)==n,"wrong planned order")
        target_originals[r] = hold(f"target-r{r}",[[1],[r],[3],[2],[],[]],n)
    old_graph,old_labels,retained = recheck()
    retained_hash = save(OUTPUT/"retained_recheck.json",retained)
    cores,hashes,targets,completed = {},{},{},[]
    for r,original in originals.items():
        cores[r] = check_core(r,original,retained_hash)
        hashes[r] = save(OUTPUT/f"core-r{r}.json",cores[r])
    for r,original in target_originals.items():
        targets[r] = check_target(r,original,cores[r],hashes[r])
        path = OUTPUT/f"target-r{r}.json"
        digest = save(path,targets[r])
        completed.append({"r":r,"K":1,"n":targets[r]["verification"]["n"],"certificate":path.name,
                          "bytes":path.stat().st_size,"sha256_raw":digest})
    batches = compare(old_graph,old_labels,retained,cores,originals,targets,target_originals)
    batch_hash = save(OUTPUT/"growth_comparison.json",batches)
    result = {"run_id":RUN,"status":"PASS","identity_sha256_raw":ident_hash,
              "retained_rechecks":1,"retained_recheck_sha256_raw":retained_hash,"auxiliary_cores":sorted(cores),
              "completed_targets":completed,"domain_rejections":len(rejected),"growth_comparison_sha256_raw":batch_hash,
              "solver_queries":0,"computational_enumeration":0,"historical_search_replay":0}
    save(OUTPUT/"summary.json",result)
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
