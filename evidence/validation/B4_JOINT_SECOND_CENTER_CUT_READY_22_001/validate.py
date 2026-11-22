"""Verify the alternative supplied ledger and two bounded growth cases."""

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
PARENT = "ea444f9ae68505596fc3cc84dbdb2e848eeec446"
PROOF = "research/B4_JOINT_SECOND_CENTER_CUT_READY_22.md"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
LIMITS = {"workers":1, "authorized_dfs_queries":1, "dfs_attempted_assignments":100000,
          "dfs_seconds":6, "max_cpu_seconds":30, "max_order":20, "max_new_originals":2,
          "max_record_bytes":2_000_000, "max_total_bytes":10_000_000, "automatic_retries":0}
CASES = [{"id":"r4","r":4,"t":None,"order":17},{"id":"r4-t2","r":4,"t":2,"order":20}]
HOST = "b:1:0"

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
        self.total = 0

    def write(self, name, raw):
        require(process_time() - self.started <= LIMITS["max_cpu_seconds"], "process CPU")
        require(len(raw) <= LIMITS["max_record_bytes"] and self.total+len(raw) <= LIMITS["max_total_bytes"], "byte caps")
        path = OUT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as file:
            file.write(raw)
        self.total += len(raw)

    def save(self, name, data):
        self.write(name, (json.dumps(data,sort_keys=True,indent=2)+"\n").encode())


def certificate(original, labels):
    graph = original["graph"]
    verdict = verify_certificate(graph, labels, original["graph_digest"])
    require(verdict["valid"] is True, "original-bound checker")
    return {"labels":labels,"graph_digest":original["graph_digest"],"checker":verdict,"witness":graph["spine"],
            "ledger":[{"edge":[u,v],"difference":abs(labels[u]-labels[v])} for u,v in graph["edges"]]}


def grow(labels, cut, first, h):
    return {**{v:x+h if x>=cut else x for v,x in labels.items()},
            **{f"l:1:0:{first+j}":cut+j for j in range(h)}}


def formula(seed, r):
    require(type(r) is int and r>=2, "exact r")
    return {**seed,"s:0":r+11,"s:2":r+12,**{f"l:1:0:{j}":11+j for j in range(2,r)}}


def lift(core, r, t, graph):
    require(type(t) is int and t>=1, "exact t")
    prefix = {v:x+1 for v,x in core.items() if v!="s:5"}
    prefix.update({"b:2:0":0,**{f"l:2:0:{j}":r+14+j for j in range(t)}})
    missing = set(graph["vertices"])-prefix.keys()
    pending = [e for e in graph["edges"] if missing.intersection(e)]
    ls = sorted(prefix.values())
    ds = sorted(abs(prefix[u]-prefix[v]) for u,v in graph["edges"] if u in prefix and v in prefix)
    m = len(graph["edges"])
    r_left = sorted(set(range(m+1)).difference(ls))
    d_left = sorted(set(range(1,m+1)).difference(ds))
    require(missing=={"s:5"} and pending==[["s:4","s:5"]] and prefix["s:4"]==10
            and r_left==[11] and d_left==[1] and abs(prefix["s:4"]-r_left[0])==d_left[0], "original singleton")
    return {**prefix,"s:5":r_left[0]}, {"prefix":prefix,"pending":pending,"used_labels":ls,
             "used_differences":ds,"R":r_left,"D":d_left,"port":["s:4",10]}


def main():
    started = process_time()
    config = read(HERE/"config.json")
    require(config["parent"]==PARENT==git("rev-parse","HEAD").decode().strip()
            and config["limits"]==LIMITS and config["new_cases"]==CASES
            and config["cut"]==13 and config["host"]==HOST
            and config["execution"]=={"method":"direct structural ledger","queries":0,"enumeration_nodes":0,
                   "root_pin":{"s:2":14},"alpha":False,"terminal_order":False,"pinned_zero_side":False}
            and [row["id"] for row in config["controls"]]==["C22","C23"]
            and sys.version_info[:2] in ((3,12),(3,13)) and sys.flags.utf8_mode==1, "frozen scope")
    OUT.mkdir()
    records = Records(started)
    retained = {}
    for name in [*(row[key] for row in config["controls"] for key in ("original","certificate")),
                 *config["retained_D059"].values()]:
        raw = (ROOT/name).read_bytes()
        require(raw==git("show",f"{PARENT}:{name}"), name)
        retained[name] = sha(raw)
    sources = {}
    for name in SOURCES:
        raw = (ROOT/name).read_bytes()
        require(raw.replace(b"\r\n",b"\n")==git("show",f"{PARENT}:{name}").replace(b"\r\n",b"\n"), name)
        records.write("source/"+name,raw)
        sources[name] = sha(raw)
    inputs = [HERE/name for name in ("config.json","validate.py","audit.py","commands.json")] + [ROOT/PROOF]
    records.save("identity.json",{"id":config["id"],"parent":PARENT,"retained_sha256":retained,
                 "source_sha256":sources,"inputs_sha256":{p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in inputs},
                 "runtime":{"version":sys.version,"platform":platform.platform(),"utf8_mode":sys.flags.utf8_mode,
                            "implementation":sys.implementation.name,"optional_dependencies":[]}})

    controls, originals = {}, {}
    for row in config["controls"]:
        original = read(ROOT/row["original"])
        prior = read(ROOT/row["certificate"])
        r = row["r"]
        control = certificate(original,prior["labels"])
        require(original["graph"]["profile"]==[[2],[r],[],[2],[],[]]
                and control["labels"]["s:2"]==r+12
                and all(control[k]==prior[k] for k in ("labels","graph_digest","checker","ledger")), "positive control")
        controls[row["id"]],originals[r] = control,original
    d059 = config["retained_D059"]
    raw_audit = read(ROOT/d059["audit"])
    manifest = read(ROOT/d059["manifest"])
    require(manifest["files"]["audit_result.json"]["sha256"]==retained[d059["audit"]]
            and raw_audit["status"]=="PASS" and raw_audit["second_cut_matches_q2"]==[]
            and raw_audit["second_cut_matches_q3"]==[], "retained D059 fixed-ledger rejection")
    records.save("controls.json",{"positive":controls,"D059_negative":{"path":d059["audit"],
                   "sha256":retained[d059["audit"]],"second_cut_matches_q2":[],"second_cut_matches_q3":[],"replayed":False}})

    seed = config["seed"]
    require(seed["s:2"]==14 and seed["s:1"]==0 and seed[HOST]==2
            and seed!=controls["C22"]["labels"], "independent rooted seed")
    proof = certificate(originals[2],seed)
    records.save("alternative-r2.json",proof)
    adverse = verify_certificate(originals[2]["graph"],seed,"0"*64)
    require(adverse["valid"] is False and adverse["errors"]==["original graph digest mismatch"], "wrong digest")
    records.save("adverse.json",{"expected_digest":"0"*64,"checker":adverse})

    r3 = grow(seed,13,2,1)
    direct = grow(seed,13,2,2)
    split = grow(r3,14,3,1)
    require(r3==formula(seed,3) and r3!=controls["C23"]["labels"] and direct==split==formula(seed,4), "actual named batches")
    records.save("alternative-r3.json",certificate(originals[3],r3))
    records.save("batches.json",{"cuts":[13,14,15],"r3":r3,"r4_direct":direct,"r4_split":split})

    for row in CASES:
        name,r,t = row["id"],row["r"],row["t"]
        graph = build_graph([[2],[r],[] if t is None else [t],[2],[],[]])
        require(len(graph["vertices"])==row["order"]<=LIMITS["max_order"], "new original graph scope")
        original = {"graph":graph,"graph_digest":graph_digest(graph)}
        records.save(name+"-original.json",original)
        if t is None:
            cert = certificate(original,direct)
        else:
            labels,interface = lift(direct,r,t,graph)
            cert = {**certificate(original,labels),"interface":interface}
        records.save(name+".json",cert)
    cpu = process_time()-started
    records.save("summary.json",{"status":"PASS","new_originals":2,"distinct_retained_originals":2,
         "retained_D059_replays":0,"adverse_tests":1,"dfs_queries":0,"labeling_enumeration_nodes":0,"cpu_seconds":cpu})
    print(f"PASS: cut-ready seed, distinct r3 on retained original, r4 core and r4,t2 lift ({cpu:.6f} CPU seconds)")


if __name__ == "__main__":
    main()
