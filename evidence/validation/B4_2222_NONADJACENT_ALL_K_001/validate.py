"""Bounded B4 recurrence checks on frozen named originals."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if Path.cwd() != ROOT:
    raise SystemExit("Run from the repository root.")
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_graph, verify_partial

PARENT = "c0dc9245616eb5b43dca14af2605473ead1a99d5"
PREFIX_PROFILE = [[2],[2],[2],[2],[]]
LOW = {"s:1","s:3","b:0:0","b:2:0","l:1:0:0","l:1:0:1","l:3:0:0","l:3:0:1"}
RETAINED, NEW = 2, (3,4,5,8)
CASES = (RETAINED,*NEW)
BASES = {2:(3,1,0),3:(4,1,0,2),4:(5,1,2,0,3)}
OUTPUTS = ("freeze.json","prefix_control.json","adverse.json","result.json","audit_result.json",
           *(f"k{k}_original.json" for k in NEW),*(f"k{k}_certificate.json" for k in CASES))


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def checksum(raw):
    return sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(name, value, limits):
    payload = json.dumps(value,indent=2,sort_keys=True).encode()+b"\n"
    require(len(payload)<=limits["max_record_bytes"]
            and sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(payload)<=limits["max_total_bytes"],
            f"byte caps: {name}")
    with (HERE/name).open("xb") as out:
        out.write(payload)


def archive(cfg,key):
    return read(ROOT/cfg["sources"][key]["path"])


def bind_bytes(path, ref):
    raw = path.read_bytes()
    actual = checksum(raw)
    if ref["line_endings"]=="checkout_crlf":
        require(actual in (ref["raw_sha256"],ref["git_sha256"])
                and checksum(raw.replace(b"\r\n",b"\n"))==ref["git_sha256"], f"normalized source: {path.name}")
    else:
        require(ref["line_endings"]=="exact" and actual==ref["raw_sha256"]==ref["git_sha256"], f"raw source: {path.name}")
    return actual


def bindings(cfg):
    task = {name:checksum((HERE/name).read_bytes()) for name in ("INTAKE.md","config.json","commands.json","validate.py","audit.py")}
    task["research/B4_2222_NONADJACENT_ALL_K.md"] = checksum((ROOT/"research/B4_2222_NONADJACENT_ALL_K.md").read_bytes())
    return {"task":task,
            "archives":{ref["path"]:bind_bytes(ROOT/ref["path"],ref) for ref in cfg["sources"].values()},
            "production":{p:bind_bytes(ROOT/p,ref) for p,ref in cfg["production"].items()}}


def profile(k):
    return PREFIX_PROFILE+[[] for _ in range(k)]


def target_record(cfg,k):
    if k==RETAINED:
        ref = cfg["sources"]["target"]
        return read(ROOT/ref["path"]), {"origin":"retained","path":ref["path"],"sha256":ref["raw_sha256"]}
    name = f"k{k}_original.json"
    raw = (HERE/name).read_bytes()
    return json.loads(raw), {"origin":"new","path":name,"sha256":checksum(raw)}


def check_shape(record,k):
    graph = record["graph"]
    checked = verify_graph(graph)
    require(checked["valid"] and checked["graph_digest"]==record["graph_digest"]
            and (checked["n"],checked["m"])==(17+k,16+k) and graph["profile"]==profile(k)
            and graph["spine"]==[f"s:{i}" for i in range(k+5)], "exact original target")
    return checked


def freeze(cfg,started):
    require(not any((HERE/p).exists() for p in OUTPUTS),"occupied output path")
    require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()==PARENT,"parent checkpoint")
    bound = bindings(cfg)
    snapshots = {}
    for k in CASES:
        if k!=RETAINED:
            graph = build_graph(profile(k))
            save(f"k{k}_original.json",{"graph":graph,"graph_digest":graph_digest(graph)},cfg["limits"])
        original, ref = target_record(cfg,k)
        snapshots[str(k)] = {"reference":ref,"receipt":check_shape(original,k)}
        require(process_time()-started<=cfg["limits"]["max_cpu_seconds"],"freeze CPU cap")
    save("freeze.json",{"parent":PARENT,"inputs":bound,"originals":snapshots,
                        "new_originals":len(NEW),"cpu_seconds":process_time()-started,
                        "runtime":{"version":sys.version,"implementation":sys.implementation.name,
                                   "platform":sys.platform,"utf8_mode":sys.flags.utf8_mode}},cfg["limits"])
    print("Bound retained K=2 and froze K=3,4,5,8 before checking any full certificate.")


def differences(edges,labels):
    return [abs(labels[u]-labels[v]) for u,v in edges]


def alpha_prefix(cfg):
    original = archive(cfg,"d066_original")
    cert = archive(cfg,"d066_cert")["prefix"]
    graph, f = original["graph"],cert["labels"]
    checked = verify_graph(graph)
    digest = original["graph_digest"]
    require(checked["valid"] and graph["profile"]==PREFIX_PROFILE and digest==cert["graph_digest"]
            and digest==checked["graph_digest"] and (checked["n"],checked["m"])==(17,16),"retained P identity")
    high = set(graph["vertices"])-LOW
    require(set(f)==set(graph["vertices"]) and len(high)==9 and len(LOW)==8
            and all(type(x) is int for x in f.values()) and sorted(f[v] for v in LOW)==list(range(8))
            and sorted(f[v] for v in high)==list(range(8,17)) and f["s:4"]==9,"retained alpha label classes")
    ds = differences(graph["edges"],f)
    require(all((u in LOW)!=(v in LOW) for u,v in graph["edges"]) and sorted(ds)==list(range(1,17))
            and ds==cert["checker"]["edge_differences"],"all original P edges and differences")
    pairs = {"graph_digest":digest,"labels":sorted(f.items())}
    identity = checksum(json.dumps(pairs,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode())
    require(identity==cert["ledger_id"] and identity!=digest,"retained label-ledger identity")
    return original, f, high, {"graph":checked,"ledger_id":identity,"low":sorted(LOW),"high":sorted(high),
                               "weights":ds,"port":["s:4",9]}


def sequence(k):
    if k in BASES:
        return BASES[k]
    tail = sequence(k-3)[1:]
    return (k+1,1,k-1,0,*(k-2-x for x in tail))


def numerical_contract(k,unused_labels,unused_weights,port):
    require(type(k) is int and k>=2,"nonadjacent consumer requires exact integer K>=2")
    require(unused_labels==list(range(8,k+8)) and unused_weights==list(range(1,k+1))
            and port==k+9,"incorrect original nonadjacent inventories or port")


def path_contract(original,k,labels,path):
    graph = original["graph"]
    expected = [f"s:{i}" for i in range(4,k+5)]
    require(path==expected,"expected original named path after s:4")
    pending = [e for e in graph["edges"] if set(e)-labels.keys()]
    require(set(graph["vertices"])-labels.keys()==set(path[1:])
            and pending==[list(e) for e in zip(path,path[1:])],"wrong actual unassigned incidences")
    checked = verify_partial(graph,labels)
    require(checked["valid"] and checked["graph_digest"]==original["graph_digest"]
            and checked["frontier"]==["s:4"],"invalid original-bound B4 prefix")
    numerical_contract(k,checked["unused_labels"],checked["unused_differences"],labels["s:4"])
    return checked,pending


def reject(operation, expected):
    try:
        operation()
    except ValueError as error:
        require(str(error)==expected,f"unexpected control rejection: {error}")
        return str(error)
    raise ValueError("an adverse state was accepted")


def adverse(original,prefix):
    digest = verify_certificate(original["graph"],{},"0"*64)
    require(not digest["valid"] and digest["graph_digest"]==original["graph_digest"]
            and "original graph digest mismatch" in digest["errors"],"wrong expected digest")
    path = ["s:2","s:5","s:6"]
    wrong_path = reject(lambda:path_contract(original,2,prefix,path),"expected original named path after s:4")
    wrong_D = reject(lambda:numerical_contract(2,[8,9],[1,3],11),"incorrect original nonadjacent inventories or port")
    k1 = reject(lambda:numerical_contract(1,[8],[1],10),"nonadjacent consumer requires exact integer K>=2")
    return {"wrong_digest":{"expected":"0"*64,"labels":{},"checker":digest},
            "wrong_path":{"attempt":path,"rejection":wrong_path},
            "wrong_D":{"R":[8,9],"D":[1,3],"port":11,"rejection":wrong_D},
            "k1":{"R":[8],"D":[1],"port":10,"forced_weight":abs(10-8),"rejection":k1,"graph_generated":False}}


def check(cfg,started):
    require(not any((HERE/p).exists() for p in ("prefix_control.json","adverse.json","result.json","audit_result.json",
                                                *(f"k{k}_certificate.json" for k in CASES))),"occupied certificate output")
    freeze_report = read(HERE/"freeze.json")
    require(freeze_report["inputs"]==bindings(cfg) and freeze_report["parent"]==PARENT,"frozen inputs")
    p,f,high,control = alpha_prefix(cfg)
    save("prefix_control.json",control,cfg["limits"])
    count = 0
    checked_cases = {}
    for k in CASES:
        original,ref = target_record(cfg,k)
        graph = original["graph"]
        require(freeze_report["originals"][str(k)]=={"reference":ref,"receipt":check_shape(original,k)},"frozen target")
        assigned = [e for e in graph["edges"] if set(e)<=f.keys()]
        require(assigned==p["graph"]["edges"] and graph["spine"][:5]==p["graph"]["spine"]
                and all(graph["roles"][v]==p["graph"]["roles"][v] for v in f),"same original named prefix")
        shifted = {v:x+(k if v in high else 0) for v,x in f.items()}
        path = [f"s:{i}" for i in range(4,k+5)]
        partial,pending = path_contract(original,k,shifted,path)
        normalized = sequence(k)
        suffix = [8+x for x in normalized]
        require(suffix[0]==shifted["s:4"]
                and sorted(suffix[1:])==partial["unused_labels"],"translated path labels")
        labels = dict(shifted)
        labels.update(zip(path[1:],suffix[1:],strict=True))
        weights = differences(graph["edges"],labels)
        suffix_weights = differences(pending,labels)
        require(sorted(suffix_weights)==partial["unused_differences"],"actual pending differences")
        count += 1
        require(count<=cfg["limits"]["full_certificates"],"full certificate cap")
        receipt = verify_certificate(graph,labels,original["graph_digest"])
        require(receipt["valid"] and receipt["edge_differences"]==weights,"full certificate checker")
        if k==RETAINED:
            archived = archive(cfg,"d066_cert")
            require(archived["target"]["labels"]==labels and archived["target"]["checker"]==receipt
                    and archived["shifted_prefix"]["labels"]==shifted,"unchanged D066 K=2 control")
            save("adverse.json",adverse(original,shifted),cfg["limits"])
        name = f"k{k}_certificate.json"
        save(name,{"K":k,"original":ref,"graph_digest":original["graph_digest"],"prefix":shifted,
                   "partial_checker":partial,"physical_port":["s:4",shifted["s:4"]],
                   "R":partial["unused_labels"],"D":partial["unused_differences"],
                   "path":path,"C_K":normalized,"translated_path":suffix,"pending":pending,"pending_weights":suffix_weights,
                   "labels":labels,"named_edges":[{"edge":e,"difference":d} for e,d in zip(graph["edges"],weights,strict=True)],
                   "checker":receipt},cfg["limits"])
        checked_cases[str(k)] = {"origin":ref["origin"],"certificate_sha256":checksum((HERE/name).read_bytes())}
        require(freeze_report["cpu_seconds"]+process_time()-started<=cfg["limits"]["max_cpu_seconds"],"CPU cap")
    require(count==5,"completed all authorized full cases")
    save("result.json",{"status":"PASS_PENDING_INDEPENDENT_AUDIT","full_certificates":count,
                        "retained_K":RETAINED,"new_originals":len(NEW),"cases":checked_cases,
                        "solver_queries":0,"enumeration_nodes":0,"cpu_seconds":process_time()-started},cfg["limits"])
    print("Verified five original full certificates, including retained K=2. No queries or enumeration.")


def main():
    started = process_time()
    require(sys.version_info[:2] in {(3,12),(3,13)},"project-local Python 3.12 or 3.13")
    cfg = read(HERE/"config.json")
    ints = [*cfg["fixed_branch_sizes"],cfg["retained_K"],*cfg["new_K"],cfg["ell"],*cfg["limits"].values()]
    require(all(type(x) is int for x in ints) and cfg["parent"]==PARENT and cfg["fixed_branch_sizes"]==[2]*4
            and (cfg["retained_K"],tuple(cfg["new_K"]),cfg["ell"],cfg["physical_port"])==(2,NEW,8,"s:4"),
            "exact frozen scope")
    require(cfg["limits"]==dict(workers=1,new_originals=4,full_certificates=5,solver_queries=0,enumeration_nodes=0,
                              max_cpu_seconds=30,max_record_bytes=2000000,max_total_bytes=10000000,retries=0),"exact limits")
    require(len(sys.argv)==2 and sys.argv[1] in ("freeze","check"),"select freeze or check")
    if sys.argv[1]=="freeze":
        freeze(cfg,started)
    else:
        check(cfg,started)


if __name__=="__main__":
    main()
