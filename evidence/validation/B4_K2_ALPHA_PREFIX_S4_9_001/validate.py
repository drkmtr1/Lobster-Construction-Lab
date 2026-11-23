"""Verify the analytically supplied certificate on the induced original prefix."""
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

from lcl.model import graph_digest
from lcl.verify import verify_certificate, verify_graph, verify_partial

PARENT = "dbb63fbe99d9aa21e3893b60e7aa633f81997571"
PROFILE = [[2], [2], [2], [2], []]
SUFFIX = {"s:5", "s:6"}
PENDING = [["s:4", "s:5"], ["s:5", "s:6"]]
LOW = {"s:1","s:3","b:0:0","b:2:0","l:1:0:0","l:1:0:1","l:3:0:0","l:3:0:1"}
HIGH = {"s:0","s:2","s:4","b:1:0","b:3:0","l:0:0:0","l:0:0:1","l:2:0:0","l:2:0:1"}
OUTPUTS = ("prefix_original.json","freeze.json","certificates.json","result.json","audit_result.json")
F = {
    "s:0":10,"s:1":2,"s:2":16,"s:3":7,"s:4":9,
    "b:0:0":6,"l:0:0:0":12,"l:0:0:1":13,
    "b:1:0":14,"l:1:0:0":1,"l:1:0:1":4,
    "b:2:0":0,"l:2:0:0":15,"l:2:0:1":11,
    "b:3:0":8,"l:3:0:0":3,"l:3:0:1":5,
}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(name, value, config):
    data = json.dumps(value,indent=2,sort_keys=True).encode()+b"\n"
    cap = config["limits"]
    require(len(data)<=cap["max_record_bytes"]
            and sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(data)<=cap["max_total_bytes"],
            f"byte caps: {name}")
    with (HERE/name).open("xb") as out:
        out.write(data)


def source(config,key):
    return read(ROOT/config["sources"][key]["path"])


def inputs(config):
    archive = {ref["path"]:sha(ROOT/ref["path"]) for ref in config["sources"].values()}
    require(archive=={r["path"]:r["sha256"] for r in config["sources"].values()}, "retained raw source identity")
    production = {p:sha(ROOT/p) for p in config["production_sha256"]}
    require(production==config["production_sha256"], "production source identity")
    task = {name:sha(HERE/name) for name in ("INTAKE.md","commands.json","config.json","validate.py","audit.py")}
    task["research/B4_K2_ALPHA_PREFIX_S4_9.md"] = sha(ROOT/"research/B4_K2_ALPHA_PREFIX_S4_9.md")
    return {"archives":archive,"production":production,"task":task}


def target(config):
    rec = source(config,"target")
    graph = rec["graph"]
    ck = verify_graph(graph)
    require(ck["valid"] and ck["graph_digest"]==rec["graph_digest"]==config["target_digest"]
            and graph["profile"]==PROFILE+[[],[]] and (ck["n"],ck["m"])==(19,18), "retained target identity")
    return rec


def ledger_id(digest, labels):
    payload = {"graph_digest":digest,"labels":sorted(labels.items())}
    return sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def freeze(config,started):
    require(not any((HERE/name).exists() for name in OUTPUTS),"occupied output path")
    require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()==PARENT,"parent checkout")
    bound = inputs(config)
    t = target(config)["graph"]
    retained = [v for v in t["vertices"] if v not in SUFFIX]
    edges = [e for e in t["edges"] if SUFFIX.isdisjoint(e)]
    require([e for e in t["edges"] if not SUFFIX.isdisjoint(e)]==PENDING,"only actual suffix omitted")
    p = {"schema_version":1,"profile":PROFILE,"vertices":retained,"edges":edges,
         "spine":t["spine"][:-2],"roles":{v:t["roles"][v] for v in retained}}
    pre = {"graph":p,"graph_digest":graph_digest(p)}
    receipt = verify_graph(p)
    require(receipt["valid"] and receipt["graph_digest"]==pre["graph_digest"]
            and (receipt["n"],receipt["m"])==(17,16), "induced prefix original")
    save("prefix_original.json",pre,config)
    save("freeze.json",{"parent":PARENT,"target_reference":config["sources"]["target"],
                        "prefix_sha256":sha(HERE/"prefix_original.json"),"inputs":bound,"prefix_graph_receipt":receipt,
                        "new_prefix_originals":1,"new_target_originals":0,"cpu_seconds":process_time()-started,
                        "runtime":{"version":sys.version,"implementation":sys.implementation.name,
                                   "platform":sys.platform,"utf8_mode":sys.flags.utf8_mode}},config)
    print("Froze the single induced P original and bound the retained T.")


def named_edges(graph, labels):
    return [{"edge":e,"difference":abs(labels[e[0]]-labels[e[1]])} for e in graph["edges"]]


def alpha_errors(graph, labels, receipt):
    errors = []
    if not receipt["valid"]:
        errors.append("ordinary certificate rejected")
    if labels.get("s:4") != 9:
        errors.append("physical s:4 is not 9")
    if sorted(labels[v] for v in LOW)!=list(range(8)) or sorted(labels[v] for v in HIGH)!=list(range(8,17)):
        errors.append("prescribed alpha-class alphabets fail")
    if any((labels[u]<8)==(labels[v]<8) for u,v in graph["edges"]):
        errors.append("an original edge fails the cutoff-8 test")
    return errors


def controls(config, pre, full, f_receipt):
    core = source(config,"core_original")
    source_cert = source(config,"core_certificate")
    old_f = source_cert["labels"]
    prior = verify_certificate(core["graph"],old_f,core["graph_digest"])
    require(prior["valid"] and prior==source_cert["checker"], "retained D061 positive")
    known_lift = {v:x+1 for v,x in old_f.items()}
    known_lift.update({"b:2:0":0,"l:2:0:0":16,"l:2:0:1":17})
    k1 = source(config,"k1_original")
    lift = verify_certificate(k1["graph"],known_lift,k1["graph_digest"])
    baseline = source(config,"d063_controls")["k1"]
    require(lift["valid"] and lift==baseline["checker"] and known_lift==baseline["labels"], "retained D062 positive")
    wrong = verify_certificate(pre["graph"],F,full["graph_digest"])
    require(not wrong["valid"] and wrong["errors"]==f_receipt["errors"]+["original graph digest mismatch"],
            "wrong original digest control")
    inverted = {v:16-x for v,x in F.items()}
    ordinary = verify_certificate(pre["graph"],inverted,pre["graph_digest"])
    defeats = alpha_errors(pre["graph"],inverted,ordinary)
    require(ordinary["valid"] and "physical s:4 is not 9" in defeats
            and "prescribed alpha-class alphabets fail" in defeats,"adverse alpha/port control")
    return {"retained_D061":prior,"retained_D062_K1":lift,"wrong_digest":{"checker":wrong,"expected":full["graph_digest"]},
            "complement":{"labels":inverted,"checker":ordinary,"supplier_valid":False,"supplier_rejections":defeats}}


def check(config,started):
    require(not any((HERE/name).exists() for name in OUTPUTS[2:]),"occupied certificate output path")
    frozen = read(HERE/"freeze.json")
    p = read(HERE/"prefix_original.json")
    t = target(config)
    require(frozen["inputs"]==inputs(config) and frozen["target_reference"]==config["sources"]["target"]
            and frozen["prefix_sha256"]==sha(HERE/"prefix_original.json"),"frozen input bindings")
    require(set(p["graph"]["vertices"])==LOW|HIGH and len(LOW)==8 and len(HIGH)==9 and LOW.isdisjoint(HIGH)
            and all((u in LOW)!=(v in LOW) for u,v in p["graph"]["edges"]),"exact classes on original edges")
    f_ck = verify_certificate(p["graph"],F,p["graph_digest"])
    require(not alpha_errors(p["graph"],F,f_ck),"supplied original alpha prefix")
    g = {v:x+(2 if v in HIGH else 0) for v,x in F.items()}
    partial = verify_partial(t["graph"],g)
    require(partial["valid"] and partial["graph_digest"]==t["graph_digest"]
            and partial["unused_labels"]==[8,9] and partial["unused_differences"]==[1,2]
            and partial["frontier"]==["s:4"] and g["s:4"]==11, "exact T prefix inventories")
    complete = {**g,"s:5":9,"s:6":8}
    g_ck = verify_certificate(t["graph"],complete,t["graph_digest"])
    require(g_ck["valid"],"original completed T checker")
    all_control = controls(config,p,t,f_ck)
    elapsed = process_time()-started
    require(frozen["cpu_seconds"]+elapsed<=config["limits"]["max_cpu_seconds"],"CPU cap")
    prefix_id = ledger_id(p["graph_digest"],F)
    target_id = ledger_id(t["graph_digest"],complete)
    save("certificates.json",{"prefix":{"labels":F,"graph_digest":p["graph_digest"],"ledger_id":prefix_id,
                                      "checker":f_ck,"named_edges":named_edges(p["graph"],F)},
                              "shifted_prefix":{"labels":g,"checker":partial,"port":["s:4",11],"R":[8,9],"D":[1,2],
                                                "pending":PENDING},
                              "target":{"labels":complete,"graph_digest":t["graph_digest"],"ledger_id":target_id,
                                        "checker":g_ck,"named_edges":named_edges(t["graph"],complete)},
                              "controls":all_control},config)
    save("result.json",{"status":"VERIFIED_FINITE_SUPPLY_PENDING_INDEPENDENT_AUDIT",
                        "route":"direct_analytic_prefix","query":{"status":"NOT_RUN","reason":"analytic seed supplied",
                                                                  "calls":0,"visited_nodes":0},
                        "cpu_seconds":elapsed,"new_prefix_originals":1,"new_target_originals":0,
                        "certificates_sha256":sha(HERE/"certificates.json")},config)
    print("Verified one supplied alpha P and its exact K=2 completion on original T. No search.")


def main():
    started = process_time()
    require(sys.version_info[:2] in {(3,12),(3,13)}, "project-local Python required")
    cfg = read(HERE/"config.json")
    a = cfg["alpha"]
    numeric = [*cfg["parameters"], *cfg["limits"].values(), a["cutoff"], a["port_label"]]
    numeric.extend(x for section in cfg["prefix_profile"] for x in section)
    require(all(type(x) is int for x in numeric),"exact integer configuration")
    require(cfg["parent"]==PARENT and cfg["route"]=="direct_analytic_prefix" and cfg["parameters"]==[2]*4
            and cfg["prefix_profile"]==PROFILE and cfg["suffix"]==["s:5","s:6"]
            and len(a["low"])==8 and set(a["low"])==LOW and len(a["high"])==9 and set(a["high"])==HIGH
            and (a["cutoff"],a["port_vertex"],a["port_label"])==(8,"s:4",9),"exact task")
    require(cfg["limits"]==dict(workers=1,max_prefix_originals=1,max_new_target_originals=0,max_nodes=250000,
                              max_queries=1,max_cpu_seconds=30,max_record_bytes=2000000,max_total_bytes=10000000,
                              retries=0),"task caps")
    require(len(sys.argv)==2 and sys.argv[1] in ("freeze","check"),"select freeze or check")
    if sys.argv[1]=="freeze":
        freeze(cfg,started)
    else:
        check(cfg,started)


if __name__ == "__main__":
    main()
