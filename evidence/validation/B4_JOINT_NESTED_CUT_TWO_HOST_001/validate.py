"""Validate the two declared named targets and save the batch routes without search."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
PARENT = "67130f845fe327175a9d6d1821ec54652f55fe70"
PROOF = "research/B4_JOINT_NESTED_CUT_TWO_HOST.md"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
LIMITS = {"workers":1, "solver_queries":0, "labeling_enumeration_nodes":0, "max_cut_checks":64,
          "max_process_cpu_seconds":30, "max_new_originals":2, "max_order":20, "max_record_bytes":2_000_000,
          "max_total_bytes":10_000_000, "automatic_retries":0}
CASES = [{"id":"core-q3-r4","q":3,"r":4,"t":None,"order":18},
         {"id":"lift-q3-r4-t1","q":3,"r":4,"t":1,"order":20}]

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


class Records:
    def __init__(self, started):
        self.started = started
        self.total_bytes = 0

    def write(self, name, raw):
        require(process_time()-self.started<=LIMITS["max_process_cpu_seconds"], "process CPU cap")
        require(len(raw)<=LIMITS["max_record_bytes"] and self.total_bytes+len(raw)<=LIMITS["max_total_bytes"], "byte caps")
        path = OUT/name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(raw)
        self.total_bytes += len(raw)

    def save(self, name, value):
        self.write(name, (json.dumps(value,sort_keys=True,indent=2)+"\n").encode())


def certificate(original, labels):
    graph = original["graph"]
    result = verify_certificate(graph,labels,original["graph_digest"])
    require(result["valid"] is True, "unchanged original-bound checker")
    return {"labels":labels,"graph_digest":original["graph_digest"],"checker":result,"witness":graph["spine"],
            "ledger":[{"edge":[u,v],"difference":abs(labels[u]-labels[v])} for u,v in graph["edges"]]}


def formula(seed, q, r):
    require(type(q) is int and type(r) is int and min(q,r)>=2, "exact q,r")
    h,k = q-2,r-2
    original = {v:x+h*(x>=7)+k*(x>=13) for v,x in seed.items()}
    return {**original,**{f"l:0:0:{j}":j+5 for j in range(2,q)},
            **{f"l:1:0:{j}":h+11+j for j in range(2,r)}}


def grow(labels, center, cut, first_index, amount):
    shifted = {v:x+amount if x>=cut else x for v,x in labels.items()}
    fresh = {f"l:{center}:0:{first_index+j}":cut+j for j in range(amount)}
    require(not (shifted.keys() & fresh.keys()), "fresh names")
    return {**shifted,**fresh}


def check_routes(seed, expected):
    first = grow(seed,0,7,2,1)
    second = grow(seed,1,13,2,2)
    fs = grow(first,1,14,2,2)
    sf = grow(second,0,7,2,1)
    unit = grow(seed,1,13,2,1)
    mixed = grow(unit,0,7,2,1)
    interleaved = grow(mixed,1,15,3,1)
    require(fs==sf==interleaved==expected, "pointwise named order agreement")
    return {"first_only":first,"second_only":second,"one_second":unit,"mixed_prefix":mixed,
            "first_then_second":fs,"second_then_first":sf,"second_first_second":interleaved}


def lifted(core,t,original):
    require(type(t) is int and t>=1,"exact t")
    graph = original["graph"]
    m = len(core)-1
    prefix = {v:x+1 for v,x in core.items() if v!="s:5"}
    prefix.update({"b:2:0":0,**{f"l:2:0:{j}":m+2+j for j in range(t)}})
    missing = set(graph["vertices"])-prefix.keys()
    pending = [edge for edge in graph["edges"] if missing.intersection(edge)]
    ls = sorted(prefix.values())
    ds = sorted(abs(prefix[u]-prefix[v]) for u,v in graph["edges"] if u in prefix and v in prefix)
    M = len(graph["edges"])
    R = sorted(set(range(M+1)).difference(ls))
    D = sorted(set(range(1,M+1)).difference(ds))
    require(missing=={"s:5"} and pending==[["s:4","s:5"]] and prefix["s:4"]==11
            and R==[12] and D==[1] and abs(prefix["s:4"]-R[0])==D[0], "exact singleton")
    return {**prefix,"s:5":R[0]}, {"prefix":prefix,"pending":pending,"used_labels":ls,
             "used_differences":ds,"R":R,"D":D,"port":["s:4",11]}


def main():
    started = process_time()
    config = read(HERE/"config.json")
    require(config["parent"]==PARENT==git("rev-parse","HEAD").decode().strip()
            and config["limits"]==LIMITS and config["cases"]==CASES
            and config["seed"]["cuts"]==[7,13] and config["seed"]["hosts"]==["b:0:0","b:1:0"]
            and config["seed"]["host_labels"]==[1,2] and sys.version_info[:2] in ((3,12),(3,13))
            and sys.flags.utf8_mode==1, "starting scope and runtime")
    OUT.mkdir()
    record = Records(started)
    retained = {}
    for name in [*(config[key][field] for key in ("seed","control") for field in ("original","certificate")),
                 *config["negative"].values()]:
        raw = (ROOT/name).read_bytes()
        require(raw==git("show",f"{PARENT}:{name}"),name)
        retained[name] = sha(raw)
    seed_ref = config["seed"]["original"]
    seed_original = read(ROOT/seed_ref)
    record.save("seed-binding.json",{"retained_original":seed_ref,"raw_sha256":retained[seed_ref],
                                    "graph_digest":seed_original["graph_digest"],"order":15})

    sources = {}
    for name in SOURCES:
        raw = (ROOT/name).read_bytes()
        require(raw.replace(b"\r\n",b"\n")==git("show",f"{PARENT}:{name}").replace(b"\r\n",b"\n"),name)
        record.write("source/"+name,raw)
        sources[name] = sha(raw)
    inputs = [HERE/name for name in ("config.json","commands.json","validate.py","audit.py","scope-intake.md")] + [ROOT/PROOF]
    record.save("identity.json",{"id":config["id"],"parent":PARENT,"retained_sha256":retained,"source_sha256":sources,
                 "inputs_sha256":{p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in inputs},
                 "runtime":{"version":sys.version,"platform":platform.platform(),"utf8_mode":sys.flags.utf8_mode,
                            "implementation":sys.implementation.name,"optional_dependencies":[]}})

    controls = {}
    for key, profile, root in (("seed",[[2],[2],[],[2],[],[]],14),("control",[[2],[3],[],[2],[],[]],15)):
        spec = config[key]
        original = seed_original if key=="seed" else read(ROOT/spec["original"])
        old = read(ROOT/spec["certificate"])
        cert = certificate(original,old["labels"])
        require(original["graph"]["profile"]==profile and cert["labels"]["s:2"]==root
                and all(cert[k]==old[k] for k in ("labels","graph_digest","checker","ledger")), "retained positive")
        controls[key] = cert
    neg = config["negative"]
    prior = read(ROOT/neg["audit"])
    manifest = read(ROOT/neg["manifest"])
    require(manifest["files"]["audit_result.json"]["sha256"]==retained[neg["audit"]]
            and prior["status"]=="PASS" and prior["second_cut_matches_q2"]==prior["second_cut_matches_q3"]==[], "D059 retention")
    record.save("controls.json",{"positive":controls,"D059_negative":{"path":neg["audit"],
                "sha256":retained[neg["audit"]],"replayed":False,"old_matches":[[],[]]}})
    seed = controls["seed"]["labels"]
    require(seed["b:0:0"]==1 and seed["b:1:0"]==2 and formula(seed,2,2)==seed, "same physical seed")
    adverse = verify_certificate(seed_original["graph"],seed,"0"*64)
    require(adverse["valid"] is False and adverse["errors"]==["original graph digest mismatch"], "adverse digest")
    record.save("adverse.json",{"expected_digest":"0"*64,"checker":adverse})

    core = formula(seed,3,4)
    routes = check_routes(seed,core)
    record.save("batch-routes.json",routes)
    for case in CASES:
        name,q,r,t = case["id"],case["q"],case["r"],case["t"]
        graph = build_graph([[q],[r],[] if t is None else [t],[2],[],[]])
        require(len(graph["vertices"])==case["order"]<=LIMITS["max_order"],"new original scope")
        original = {"graph":graph,"graph_digest":graph_digest(graph)}
        record.save(name+"-original.json",original)
        if t is None:
            result = certificate(original,core)
        else:
            labels,interface = lifted(core,t,original)
            result = {**certificate(original,labels),"interface":interface}
        record.save(name+".json",result)
    cpu = process_time()-started
    record.save("summary.json",{"status":"PASS","new_originals":2,"retained_originals":2,"adverse_tests":1,
                  "cut_checks_in_validator":0,"solver_queries":0,"labeling_enumeration_nodes":0,"cpu_seconds":cpu})
    print(f"PASS: both retained controls, three named batch routes, core and t=1 lift ({cpu:.6f} CPU seconds)")


if __name__=="__main__":
    main()
