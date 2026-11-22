"""Audit the exact named originals and cut states with standard-library arithmetic."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "67130f845fe327175a9d6d1821ec54652f55fe70"
PROOF = "research/B4_JOINT_NESTED_CUT_TWO_HOST.md"


def check(condition, detail):
    if not condition:
        raise ValueError(detail)


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def reconstruct(record, profile, order):
    graph = record["graph"]
    spine = [f"s:{i}" for i in range(6)]
    edges = list(zip(spine,spine[1:]))
    roles = {v:{"kind":"spine","section":i} for i,v in enumerate(spine)}
    for i, row in enumerate(profile):
        if not row:
            continue
        center = f"b:{i}:0"
        edges.append((spine[i],center))
        roles[center] = {"kind":"branch","section":i,"branch":0}
        for j in range(row[0]):
            leaf = f"l:{i}:0:{j}"
            edges.append((center,leaf))
            roles[leaf] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
    canonical = [tuple(sorted(e)) for e in edges]
    check(Counter(graph["vertices"])==Counter(roles.keys())
          and Counter(tuple(sorted(e)) for e in graph["edges"])==Counter(canonical), "physical incidence multiplicities")
    check(graph["roles"]==roles and graph["profile"]==profile and graph["spine"]==spine
          and graph["schema_version"]==1 and len(edges)+1==len(roles)==order, "named structure and spine")
    body = {"vertices":sorted(roles),"edges":sorted(canonical),"profile":profile,"spine":spine,"roles":roles}
    raw = json.dumps(body,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    check(sha256(raw).hexdigest()==record["graph_digest"], "canonical graph digest")
    return graph["edges"]


def ledger(edges, f):
    return [{"edge":[u,v],"difference":abs(f[u]-f[v])} for u,v in edges]


def certify(original, edges, cert):
    m = len(edges)
    f = cert["labels"]
    check(set(f)==set(original["graph"]["vertices"]) and all(type(v) is int for v in f.values())
          and sorted(f.values())==list(range(m+1)), "complete label bijection")
    rows = ledger(edges,f)
    weights = [row["difference"] for row in rows]
    result = cert["checker"]
    check(rows==cert["ledger"] and cert["witness"]==original["graph"]["spine"]
          and sorted(weights)==list(range(1,m+1)) and weights==result["edge_differences"]
          and result["valid"] is True and result["errors"]==[] and result["n"]==m+1 and result["m"]==m
          and cert["graph_digest"]==result["graph_digest"]==original["graph_digest"], "original-bound certificate")
    return rows


def verify_sources(config, ident):
    expected_kept = {config[key][field] for key in ("seed","control") for field in ("original","certificate")}
    expected_kept |= set(config["negative"].values())
    inputs = {(HERE/name).relative_to(ROOT).as_posix() for name in
              ("config.json","commands.json","validate.py","audit.py","scope-intake.md")}
    check(config["parent"]==ident["parent"]==PARENT and config["id"]==ident["id"]
          and ident["inputs_sha256"]=={name:digest(ROOT/name) for name in inputs|{PROOF}}
          and set(ident["retained_sha256"])==expected_kept
          and set(ident["source_sha256"])=={"lcl/__init__.py","lcl/model.py","lcl/verify.py","pyproject.toml","requirements.txt"}
          and ident["runtime"]=={"version":sys.version,"platform":platform.platform(),"utf8_mode":1,
                               "implementation":sys.implementation.name,"optional_dependencies":[]}, "source identity")
    for name, hash_value in ident["retained_sha256"].items():
        parent = subprocess.check_output(["git","show",f"{PARENT}:{name}"],cwd=ROOT)
        check(digest(ROOT/name)==hash_value and (ROOT/name).read_bytes()==parent,name)
    for name, hash_value in ident["source_sha256"].items():
        parent = subprocess.check_output(["git","show",f"{PARENT}:{name}"],cwd=ROOT)
        snapshot = DATA/"source"/name
        check(digest(snapshot)==digest(ROOT/name)==hash_value
              and snapshot.read_bytes().replace(b"\r\n",b"\n")==parent.replace(b"\r\n",b"\n"),name)


def verify_controls(config):
    controls = read(DATA/"controls.json")
    check(set(controls["positive"])=={"seed","control"}, "two retained positives")
    for key, r, n in (("seed",2,15),("control",3,16)):
        spec = config[key]
        original = read(ROOT/spec["original"])
        prior = read(ROOT/spec["certificate"])
        edges = reconstruct(original,[[2],[r],[],[2],[],[]],n)
        record = controls["positive"][key]
        certify(original,edges,record)
        check(all(record[name]==prior[name] for name in ("labels","graph_digest","checker","ledger"))
              and record["labels"]["s:2"]==n-1, "retained max root and exact evidence")
    spec = config["seed"]
    seed = controls["positive"]["seed"]
    original = read(ROOT/spec["original"])
    check(read(DATA/"seed-binding.json")=={"retained_original":spec["original"],"raw_sha256":digest(ROOT/spec["original"]),
                   "graph_digest":original["graph_digest"],"order":15}, "frozen seed binding")
    neg = config["negative"]
    old = read(ROOT/neg["audit"])
    manifest = read(ROOT/neg["manifest"])
    sha = digest(ROOT/neg["audit"])
    check(manifest["files"]["audit_result.json"]["sha256"]==sha
          and old["status"]=="PASS" and old["threshold_evaluations"]==49
          and old["second_cut_matches_q2"]==old["second_cut_matches_q3"]==[]
          and controls["D059_negative"]=={"path":neg["audit"],"sha256":sha,"replayed":False,"old_matches":[[],[]]},
          "preserved D059 fixed-ledger negative")
    adverse = read(DATA/"adverse.json")
    check(adverse["expected_digest"]=="0"*64!=seed["graph_digest"] and adverse["checker"]==
          {**seed["checker"],"valid":False,"errors":["original graph digest mismatch"]}, "one adverse digest")
    return seed, original["graph"]["edges"]


def inventory(start, stop):
    return list(range(start,stop+1))


def state_check(f, seed, enclosing_edges, old_edges, h, k, counter, cap):
    """Check a named label map on edges of the one declared core."""
    # Select existing edges by their endpoints. No intermediate original is constructed.
    first = {f"l:0:0:{j}" for j in range(2,h+2)}
    second = {f"l:1:0:{j}" for j in range(2,k+2)}
    new_names = first|second
    check(set(f)==set(seed)|new_names and all(type(v) is int for v in f.values()),"prescribed names")
    for v, old in seed.items():
        extra = 0 if old<7 else h if old<13 else h+k
        check(f[v]==old+extra,"old-vertex shift")
    check(all(f[v]==int(v.split(":")[-1])+5 for v in first)
          and all(f[v]==h+11+int(v.split(":")[-1]) for v in second),"fresh named label rule")
    m = 14+h+k
    check(sorted(f.values())==inventory(0,m) and f["s:2"]==m,"root and label bijection")
    edges = [e for e in enclosing_edges if all(v in f for v in e)]
    rows = ledger(edges,f)
    check(sorted(row["difference"] for row in rows)==inventory(1,m),"full named edge differences")

    parts = {"old_same":[],"first":[],"old_middle":[],"second":[],"old_high":[]}
    old_set = {tuple(sorted(e)) for e in old_edges}
    for row in rows:
        u,v = row["edge"]
        d = row["difference"]
        if u in first or v in first:
            check("b:0:0" in (u,v),"first incidence")
            parts["first"].append(d)
        elif u in second or v in second:
            check("b:1:0" in (u,v),"second incidence")
            parts["second"].append(d)
        else:
            check(tuple(sorted((u,v))) in old_set,"preserved named edge")
            old_weight = abs(seed[u]-seed[v])
            part = "old_same" if old_weight<=5 else "old_middle" if old_weight<=10 else "old_high"
            parts[part].append(d)
    bands = {part:sorted(weights) for part,weights in parts.items()}
    check(bands=={"old_same":inventory(1,5),"first":inventory(6,5+h),"old_middle":inventory(6+h,10+h),
                   "second":inventory(11+h,10+h+k),"old_high":inventory(11+h+k,m)}, "five actual weight groups")
    cuts = []
    for host,c,host_label in (("b:0:0",7+h,1),("b:1:0",13+h+k,2)):
        counter["checks"]+=1
        check(counter["checks"]<=cap,"cut budget")
        crossing = [row for row in rows if min(f[v] for v in row["edge"])<c<=max(f[v] for v in row["edge"])]
        weights = sorted(row["difference"] for row in crossing)
        check(f[host]==host_label and weights==inventory(c-host_label,m),"full returned cut tail")
        cuts.append({"host":host,"host_label":host_label,"c":c,"edges":crossing,"weights":weights})
    return {"h":h,"k":k,"m":m,"difference_bands":bands,"cuts":cuts}


def check_lift(core, original, cert, edges):
    rows = certify(original,edges,cert)
    f = cert["labels"]
    check(all(f[v]==x+1 for v,x in core.items()) and f["s:2"]==18
          and {v:f[v] for v in f.keys()-core.keys()}=={"b:2:0":0,"l:2:0:0":19}, "exact translation and zero-host lift")
    pending = [row for row in rows if "s:5" in row["edge"]]
    prefix = {v:x for v,x in f.items() if v!="s:5"}
    ls = sorted(prefix.values())
    ds = sorted(row["difference"] for row in rows if row not in pending)
    R = sorted(set(range(20))-set(ls))
    D = sorted(set(range(1,20))-set(ds))
    check(pending==[{"edge":["s:4","s:5"],"difference":1}] and R==[12] and D==[1]
          and f["s:4"]==11 and f["s:5"]==12 and cert["interface"]==
          {"prefix":prefix,"pending":[["s:4","s:5"]],"used_labels":ls,"used_differences":ds,
           "R":R,"D":D,"port":["s:4",11]}, "exact physical boundary")


def main():
    started = process_time()
    config = read(HERE/"config.json")
    limits = config["limits"]
    check(limits=={"workers":1,"solver_queries":0,"labeling_enumeration_nodes":0,"max_cut_checks":64,
          "max_process_cpu_seconds":30,"max_new_originals":2,"max_order":20,"max_record_bytes":2_000_000,
          "max_total_bytes":10_000_000,"automatic_retries":0} and config["cases"]==
          [{"id":"core-q3-r4","q":3,"r":4,"t":None,"order":18},{"id":"lift-q3-r4-t1","q":3,"r":4,"t":1,"order":20}],
          "exact run scope")
    verify_sources(config,read(DATA/"identity.json"))
    seed,old_edges = verify_controls(config)
    f0 = seed["labels"]
    check([f0[f"s:{i}"] for i in range(6)]==[13,0,14,3,9,10]
          and [f0[v] for v in ("b:0:0","l:0:0:0","l:0:0:1","b:1:0","l:1:0:0","l:1:0:1","b:3:0","l:3:0:0","l:3:0:1")]
            ==[1,11,8,2,5,6,12,4,7],"exact supplied ledger")
    orig = read(DATA/"core-q3-r4-original.json")
    edges = reconstruct(orig,[[3],[4],[],[2],[],[]],18)
    core_cert = read(DATA/"core-q3-r4.json")
    certify(orig,edges,core_cert)
    core = core_cert["labels"]
    routes = read(DATA/"batch-routes.json")
    check(routes["first_then_second"]==routes["second_then_first"]==routes["second_first_second"]==core,
          "pointwise named agreement of all three routes")
    counter = {"checks":0}
    states = {}
    specs = [("seed",f0,0,0),("first_only",routes["first_only"],1,0),("second_only",routes["second_only"],0,2),
             ("one_second",routes["one_second"],0,1),("mixed_prefix",routes["mixed_prefix"],1,1),("final",core,1,2)]
    for name,f,h,k in specs:
        states[name] = state_check(f,f0,edges,old_edges,h,k,counter,limits["max_cut_checks"])
    check(counter["checks"]==12,"exact cut count")
    lift_original = read(DATA/"lift-q3-r4-t1-original.json")
    lift_edges = reconstruct(lift_original,[[3],[4],[1],[2],[],[]],20)
    check_lift(core,lift_original,read(DATA/"lift-q3-r4-t1.json"),lift_edges)
    summary = read(DATA/"summary.json")
    cpu_before = summary["cpu_seconds"]
    check(summary=={"status":"PASS","new_originals":2,"retained_originals":2,"adverse_tests":1,
                   "cut_checks_in_validator":0,"solver_queries":0,"labeling_enumeration_nodes":0,"cpu_seconds":cpu_before}
          and 0<=cpu_before<=limits["max_process_cpu_seconds"],"validator scope")
    hashes = {p.relative_to(DATA).as_posix():digest(p) for p in sorted(DATA.rglob("*")) if p.is_file()}
    sizes = [(DATA/name).stat().st_size for name in hashes]
    cpu = cpu_before+process_time()-started
    check(cpu<=limits["max_process_cpu_seconds"],"total process CPU cap")
    report = {"status":"PASS","cut_checks":counter["checks"],"states":states,"new_originals":2,
              "retained_originals":2,"adverse_tests":1,"solver_queries":0,"labeling_enumeration_nodes":0,
              "cpu_seconds_total":cpu,"audited_sha256":hashes}
    raw = (json.dumps(report,sort_keys=True,indent=2)+"\n").encode()
    check(max([len(raw),*sizes])<=limits["max_record_bytes"]
          and len(raw)+sum(sizes)<=limits["max_total_bytes"],"output bytes")
    with (HERE/"audit_result.json").open("xb") as out:
        out.write(raw)
    print(f"PASS: 12 cut checks, three pointwise routes, two new originals and zero searches ({cpu:.6f} total CPU seconds)")


if __name__=="__main__":
    main()
