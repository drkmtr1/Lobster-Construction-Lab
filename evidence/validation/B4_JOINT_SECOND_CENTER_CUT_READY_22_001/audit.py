"""Independently audit exact named originals, repeatability and the boundary."""

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
PARENT = "ea444f9ae68505596fc3cc84dbdb2e848eeec446"
PROOF = "research/B4_JOINT_SECOND_CENTER_CUT_READY_22.md"
HOST = "b:1:0"


def check(condition, context):
    if not condition:
        raise ValueError(context)


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def reconstruct(record, r, t, order):
    graph = record["graph"]
    spine = [f"s:{i}" for i in range(6)]
    roles = {v:{"kind":"spine","section":i} for i,v in enumerate(spine)}
    pairs = list(zip(spine,spine[1:]))
    profile = [[2],[r],[] if t is None else [t],[2],[],[]]
    for i, section in enumerate(profile):
        if not section:
            continue
        b = f"b:{i}:0"
        roles[b] = {"kind":"branch","branch":0,"section":i}
        pairs.append((spine[i],b))
        for j in range(section[0]):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind":"leaf","branch":0,"section":i,"leaf":j}
            pairs.append((b,leaf))
    canonical = [tuple(sorted(e)) for e in pairs]
    check(Counter(graph["vertices"])==Counter(roles.keys())
          and Counter(tuple(sorted(e)) for e in graph["edges"])==Counter(canonical), "named multiplicities")
    check(graph["profile"]==profile and graph["roles"]==roles and graph["spine"]==spine
          and graph["schema_version"]==1 and len(pairs)+1==len(roles)==order, "named roles and order")
    payload = {"vertices":sorted(roles),"edges":sorted(canonical),"roles":roles,"spine":spine,"profile":profile}
    raw = json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    check(sha256(raw).hexdigest()==record["graph_digest"], "canonical graph digest")
    return graph["edges"]


def ledger(original, edges, cert):
    m = len(edges)
    labels = cert["labels"]
    check(set(labels)==set(original["graph"]["vertices"]) and all(type(x) is int for x in labels.values())
          and sorted(labels.values())==list(range(m+1)), "label bijection")
    rows = [{"edge":[u,v],"difference":abs(labels[u]-labels[v])} for u,v in edges]
    weights = [r["difference"] for r in rows]
    verdict = cert["checker"]
    check(rows==cert["ledger"] and cert["witness"]==original["graph"]["spine"]
          and verdict["valid"] is True and verdict["errors"]==[]
          and sorted(weights)==list(range(1,m+1)) and weights==verdict["edge_differences"]
          and verdict["n"]==m+1 and verdict["m"]==m
          and cert["graph_digest"]==verdict["graph_digest"]==original["graph_digest"], "original-bound receipt")
    return rows


def source_identity(config, identity):
    expected = {spec[key] for spec in config["controls"] for key in ("original","certificate")}
    expected |= set(config["retained_D059"].values())
    inputs = {(HERE/name).relative_to(ROOT).as_posix() for name in ("config.json","commands.json","validate.py","audit.py")}
    check(config["parent"]==identity["parent"]==PARENT and config["id"]==identity["id"]
          and identity["inputs_sha256"]=={name:digest(ROOT/name) for name in inputs|{PROOF}}
          and set(identity["retained_sha256"])==expected
          and set(identity["source_sha256"])=={"lcl/__init__.py","lcl/model.py","lcl/verify.py","pyproject.toml","requirements.txt"}
          and identity["runtime"]=={"version":sys.version,"platform":platform.platform(),"utf8_mode":1,
               "implementation":sys.implementation.name,"optional_dependencies":[]}, "source and runtime identity")
    for path, expected_digest in identity["retained_sha256"].items():
        old = subprocess.check_output(["git","show",f"{PARENT}:{path}"],cwd=ROOT)
        check(digest(ROOT/path)==expected_digest and (ROOT/path).read_bytes()==old, path)
    for path, expected_digest in identity["source_sha256"].items():
        old = subprocess.check_output(["git","show",f"{PARENT}:{path}"],cwd=ROOT)
        snapshot = DATA/"source"/path
        check(digest(snapshot)==digest(ROOT/path)==expected_digest
              and snapshot.read_bytes().replace(b"\r\n",b"\n")==old.replace(b"\r\n",b"\n"), path)


def controls(config):
    record = read(DATA/"controls.json")
    originals = {}
    check(set(record["positive"])=={"C22","C23"}, "two controls")
    for spec,r in zip(config["controls"],(2,3),strict=True):
        orig = read(ROOT/spec["original"])
        old = read(ROOT/spec["certificate"])
        check(spec["id"]==f"C2{r}" and spec["r"]==r, "control case")
        cert = record["positive"][spec["id"]]
        edges = reconstruct(orig,r,None,r+13)
        ledger(orig,edges,cert)
        check(all(cert[key]==old[key] for key in ("labels","ledger","checker","graph_digest"))
              and cert["labels"]["s:2"]==r+12, "control binding")
        originals[r] = orig
    ref = config["retained_D059"]
    retained = read(ROOT/ref["audit"])
    manifest = read(ROOT/ref["manifest"])
    check(digest(ROOT/ref["audit"])==manifest["files"]["audit_result.json"]["sha256"]
          and retained["status"]=="PASS" and retained["threshold_evaluations"]==49
          and retained["second_cut_matches_q2"]==retained["second_cut_matches_q3"]==[]
          and record["D059_negative"]=={"path":ref["audit"],"sha256":digest(ROOT/ref["audit"]),
                  "second_cut_matches_q2":[],"second_cut_matches_q3":[],"replayed":False}, "D059 no replay")
    return originals, record["positive"]


def cut_row(c, labels, rows):
    m = len(rows)
    b = labels[HOST]
    crossing = [row for row in rows if min(labels[v] for v in row["edge"])<c<=max(labels[v] for v in row["edge"])]
    actual = sorted(r["difference"] for r in crossing)
    d0 = max(c-b,b-c+1)
    demand = list(range(d0,m+1))
    return {"c":c,"host":HOST,"b":b,"host_side":"below" if b<c else "at_or_above","d0":d0,
            "crossing_edges":crossing,"spectrum":actual,"required":demand,"matches":actual==demand,
            "missing":sorted(set(demand)-set(actual)),"excess":sorted(set(actual)-set(demand))}


def check_grown(seed, labels, r, rows, original):
    m = r+12
    check(all(labels[v]==value+(r-2 if v in {"s:0","s:2"} else 0) for v,value in seed.items())
          and {v:labels[v] for v in labels.keys()-seed.keys()}=={f"l:1:0:{j}":11+j for j in range(2,r)}
          and labels["s:2"]==m and labels[HOST]==2, "full named growth formula")
    latest = cut_row(r+11,labels,rows)
    check(latest["matches"] and latest["spectrum"]==list(range(r+9,r+13)), "updated cut")
    neighbors = sorted(v if u=="s:2" else u for u,v in original["graph"]["edges"] if "s:2" in (u,v))
    check(neighbors==["s:1","s:3"] and labels["s:1"]==0, "root and zero neighbor")
    return latest


def main():
    started = process_time()
    config = read(HERE/"config.json")
    limits = config["limits"]
    check(limits=={"workers":1,"authorized_dfs_queries":1,"dfs_attempted_assignments":100000,
         "dfs_seconds":6,"max_cpu_seconds":30,"max_order":20,"max_new_originals":2,
         "max_record_bytes":2_000_000,"max_total_bytes":10_000_000,"automatic_retries":0}
         and config["new_cases"]==[{"id":"r4","r":4,"t":None,"order":17},{"id":"r4-t2","r":4,"t":2,"order":20}]
         and config["execution"]=={"method":"direct structural ledger","queries":0,"enumeration_nodes":0,
              "root_pin":{"s:2":14},"alpha":False,"terminal_order":False,"pinned_zero_side":False}
         and config["cut"]==13 and config["host"]==HOST, "bounded run declaration")
    source_identity(config,read(DATA/"identity.json"))
    originals,retained = controls(config)
    seed_record = read(DATA/"alternative-r2.json")
    seed = seed_record["labels"]
    seed_rows = ledger(originals[2],originals[2]["graph"]["edges"],seed_record)
    check(seed==config["seed"]!=retained["C22"]["labels"] and seed["s:1"]==0 and seed["s:2"]==14 and seed[HOST]==2
          and [row["difference"] for row in seed_rows]==[13,14,11,6,1,12,10,7,2,3,4,9,8,5], "explicit alternative seed")
    cuts = [cut_row(c,seed,seed_rows) for c in range(16)]
    check([row["c"] for row in cuts if row["matches"]]==[13] and cuts[13]["spectrum"]==[11,12,13,14]
          and not cuts[0]["crossing_edges"] and not cuts[-1]["crossing_edges"], "all seed cuts including endpoints")
    adverse = read(DATA/"adverse.json")
    check(adverse["expected_digest"]=="0"*64!=originals[2]["graph_digest"]
          and adverse["checker"]=={**seed_record["checker"],"valid":False,"errors":["original graph digest mismatch"]}, "adverse binding")
    r3_cert = read(DATA/"alternative-r3.json")
    r3_rows = ledger(originals[3],originals[3]["graph"]["edges"],r3_cert)
    check(r3_cert["labels"]!=retained["C23"]["labels"], "distinct ledger on same exact original")
    first_cut = check_grown(seed,r3_cert["labels"],3,r3_rows,originals[3])
    r4_original = read(DATA/"r4-original.json")
    r4_edges = reconstruct(r4_original,4,None,17)
    r4_cert = read(DATA/"r4.json")
    r4_rows = ledger(r4_original,r4_edges,r4_cert)
    r4 = r4_cert["labels"]
    final_cut = check_grown(seed,r4,4,r4_rows,r4_original)
    check(read(DATA/"batches.json")=={"cuts":[13,14,15],"r3":r3_cert["labels"],"r4_direct":r4,"r4_split":r4}
          and r4["l:1:0:2"]==13 and r4["l:1:0:3"]==14, "pointwise same-name batching")
    lifted_original = read(DATA/"r4-t2-original.json")
    lifted_edges = reconstruct(lifted_original,4,2,20)
    lifted = read(DATA/"r4-t2.json")
    lr = ledger(lifted_original,lifted_edges,lifted)
    labels = lifted["labels"]
    check(all(labels[v]==x+1 for v,x in r4.items()) and labels["s:2"]==17
          and {v:labels[v] for v in labels.keys()-r4.keys()}=={"b:2:0":0,"l:2:0:0":18,"l:2:0:1":19},
          "translation and exact zero-host leaves")
    pending = [row for row in lr if "s:5" in row["edge"]]
    prefix = {v:x for v,x in labels.items() if v!="s:5"}
    ls = sorted(prefix.values())
    ds = sorted(row["difference"] for row in lr if row not in pending)
    R = sorted(set(range(20))-set(ls))
    D = sorted(set(range(1,20))-set(ds))
    check(R==[11] and D==[1] and labels["s:5"]==11 and prefix["s:4"]==10
          and pending==[{"edge":["s:4","s:5"],"difference":1}]
          and lifted["interface"]=={"prefix":prefix,"pending":[["s:4","s:5"]],
             "used_labels":ls,"used_differences":ds,"R":R,"D":D,"port":["s:4",10]}, "physical singleton")
    prior = read(DATA/"summary.json")
    cpu_before = prior["cpu_seconds"]
    check(prior=={"status":"PASS","new_originals":2,"distinct_retained_originals":2,"retained_D059_replays":0,
          "adverse_tests":1,"dfs_queries":0,"labeling_enumeration_nodes":0,"cpu_seconds":cpu_before}
          and 0<=cpu_before<=limits["max_cpu_seconds"], "actual scope")
    hashes = {file.relative_to(DATA).as_posix():digest(file) for file in sorted(DATA.rglob("*")) if file.is_file()}
    sizes = [(DATA/path).stat().st_size for path in hashes]
    cpu = cpu_before+process_time()-started
    check(cpu<=limits["max_cpu_seconds"], "total process-CPU budget")
    report = {"status":"PASS","seed_cuts":cuts,"continued_cuts":{"r3":first_cut,"r4":final_cut},
              "new_originals":2,"retained_originals":2,"retained_D059_replays":0,"threshold_rows":18,
              "adverse_tests":1,"dfs_queries":0,"labeling_enumeration_nodes":0,
              "cpu_seconds_total":cpu,"audited_sha256":hashes}
    raw = (json.dumps(report,sort_keys=True,indent=2)+"\n").encode()
    check(max([len(raw),*sizes])<=limits["max_record_bytes"] and len(raw)+sum(sizes)<=limits["max_total_bytes"], "byte caps")
    with (HERE/"audit_result.json").open("xb") as handle:
        handle.write(raw)
    print(f"PASS: cut 13 alone; updated cuts 14,15; two new originals and zero searches ({cpu:.6f} total CPU seconds)")


if __name__=="__main__":
    main()
