"""Independent arithmetic audit of the fixed-profile nonadjacent composition."""
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASES = (2,3,4,5,8)
EXPECTED_P = {
    "s:0":10,"s:1":2,"s:2":16,"s:3":7,"s:4":9,
    "b:0:0":6,"l:0:0:0":12,"l:0:0:1":13,"b:1:0":14,"l:1:0:0":1,"l:1:0:1":4,
    "b:2:0":0,"l:2:0:0":15,"l:2:0:1":11,"b:3:0":8,"l:3:0:0":3,"l:3:0:1":5,
}


def need(ok,why):
    if not ok:
        raise ValueError(why)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def canonical_hash(payload):
    return sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def reconstruct(record, spine_count):
    graph = record["graph"]
    spine = [f"s:{i}" for i in range(spine_count)]
    profile = [[2] for _ in range(4)]+[[] for _ in range(spine_count-4)]
    roles = {v:{"kind":"spine","section":i} for i,v in enumerate(spine)}
    edges = list(zip(spine,spine[1:]))
    for section in range(4):
        hub = f"b:{section}:0"
        roles[hub] = {"kind":"branch","section":section,"branch":0}
        edges.append((spine[section],hub))
        for j in (0,1):
            name = f"l:{section}:0:{j}"
            roles[name] = {"kind":"leaf","section":section,"branch":0,"leaf":j}
            edges.append((hub,name))
    actual = [tuple(e) for e in graph["edges"]]
    expected = Counter(tuple(sorted(e)) for e in edges)
    need(graph["schema_version"]==1 and graph["profile"]==profile and graph["spine"]==spine
         and graph["roles"]==roles and Counter(graph["vertices"])==Counter(roles.keys())
         and Counter(tuple(sorted(e)) for e in actual)==expected,"named original multiplicities and roles")
    reached = set(spine)
    frontier = set(spine)
    for _ in range(2):
        frontier = ({v for u,v in actual if u in frontier}|{u for u,v in actual if v in frontier})-reached
        reached.update(frontier)
    need(reached==set(roles) and len(actual)+1==len(roles),"original spine witness")
    identity = canonical_hash({"vertices":sorted(roles),"edges":sorted(expected.elements()),
                               "profile":profile,"spine":spine,"roles":roles})
    need(record["graph_digest"]==identity,"reconstructed graph digest")
    return roles,actual


def weights(labels,edges):
    return [max(labels[u],labels[v])-min(labels[u],labels[v]) for u,v in edges]


def full_receipt(original,roles,edges,labels,checker):
    n = len(roles)
    ds = weights(labels,edges)
    need(set(labels)==set(roles) and all(type(v) is int for v in labels.values())
         and sorted(labels.values())==list(range(n)) and sorted(ds)==list(range(1,n)),"exact integer label and weight spectra")
    need(checker["valid"] is True and checker["errors"]==[] and checker["graph_digest"]==original["graph_digest"]
         and (checker["n"],checker["m"])==(n,n-1) and ds==checker["edge_differences"],"unchanged full verifier receipt")
    return ds


def check_bytes(path,ref):
    raw = path.read_bytes()
    actual = sha256(raw).hexdigest()
    if ref["line_endings"]=="checkout_crlf":
        need(actual in (ref["git_sha256"],ref["raw_sha256"])
             and sha256(raw.replace(b"\r\n",b"\n")).hexdigest()==ref["git_sha256"], "normalized archive binding")
    else:
        need(ref["line_endings"]=="exact" and actual==ref["raw_sha256"]==ref["git_sha256"], "exact raw archive binding")
    return actual


def verify_custody(config,freeze):
    paths = {key:ROOT/ref["path"] for key,ref in config["sources"].items()}
    archives = {ref["path"]:check_bytes(paths[key],ref) for key,ref in config["sources"].items()}
    runtime_sources = {path:check_bytes(ROOT/path,ref) for path,ref in config["production"].items()}
    task = {name:digest(HERE/name) for name in ("INTAKE.md","config.json","commands.json","validate.py","audit.py")}
    task["research/B4_2222_NONADJACENT_ALL_K.md"] = digest(ROOT/"research/B4_2222_NONADJACENT_ALL_K.md")
    need(freeze["inputs"]=={"archives":archives,"production":runtime_sources,"task":task}
         and freeze["parent"]==config["parent"] and freeze["new_originals"]==4,"frozen source and scope identities")
    chains = (
        ("nested_manifest","nested_proof",("nested_original","nested_certificate","nested_audit","nested_sources")),
        ("d063_manifest","d063_proof",("target","d063_validation","d063_audit","d063_log")),
        ("d064_manifest","d064_proof",("d064_validation","d064_audit","d064_log")),
        ("d065_manifest","d065_proof",("d065_result","d065_audit","d065_logL","d065_logR")),
        ("d066_manifest","d066_proof",("d066_original","d066_cert","d066_audit","d066_freeze")),
    )
    for manifest,proof,entries in chains:
        saved = read(paths[manifest])
        by_path = {entry["path"]:entry for entry in saved["files"]}
        for key in entries:
            loc = paths[key]
            rel = loc.relative_to(paths[manifest].parent).as_posix()
            need(by_path[rel]=={"path":rel,"sha256":digest(loc),"bytes":loc.stat().st_size},"historical manifest source binding")
        need(saved["external_proof"]=={"path":config["sources"][proof]["path"],"sha256":digest(paths[proof]),
                                      "bytes":paths[proof].stat().st_size},"historical proof bytes")
    need(read(paths["d066_audit"])["scientific_status"]=="SUPPLIED_EXACT_FINITE_WITNESS"
         and all(read(paths[k])["scientific_status"]=="EXHAUSTED_RESTRICTED_NEGATIVE"
                 for k in ("d063_audit","d064_audit","d065_audit"))
         and all(read(paths[k])["status"]=="INCOMPLETE" for k in ("joint_incomplete","third_zero_incomplete")),
         "retained scope without replay")
    return paths


def prefix_source(paths,control):
    original = read(paths["d066_original"])
    roles,edges = reconstruct(original,5)
    cert = read(paths["d066_cert"])["prefix"]
    f = cert["labels"]
    ds = full_receipt(original,roles,edges,f,cert["checker"])
    need(f==EXPECTED_P
         and cert["named_edges"]==[{"edge":list(e),"difference":d} for e,d in zip(edges,ds,strict=True)],
         "actual archived D066 named ledger")
    adj = {v:set() for v in roles}
    for u,v in edges:
        adj[u].add(v)
        adj[v].add(u)
    bit = {"s:4":1}
    q = deque(bit)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in bit:
                bit[v] = 1-bit[u]
                q.append(v)
            need(bit[v]!=bit[u],"all original alpha crossings")
    low = {v for v,b in bit.items() if b==0}
    high = set(bit)-low
    need(len(low)==8 and len(high)==9 and low|high==roles.keys()
         and sorted(f[v] for v in low)==list(range(8)) and sorted(f[v] for v in high)==list(range(8,17))
         and f["s:4"]==9,"actual alpha classes and physical port")
    p_digest = original["graph_digest"]
    identity = canonical_hash({"graph_digest":p_digest,"labels":sorted(f.items())})
    need(cert["graph_digest"]==p_digest and cert["ledger_id"]==identity!=p_digest,"distinct P graph and label-ledger IDs")
    need(control=={"graph":{"valid":True,"errors":[],"n":17,"m":16,"graph_digest":p_digest},
                  "ledger_id":identity,"weights":ds,"low":sorted(low),"high":sorted(high),"port":["s:4",9]},
         "saved original P audit binding")
    return roles,edges,f,high,p_digest,identity


def numeric_sequence(k):
    # Bottom-up reflection of the entire old sequence, including its port.
    base = 2+(k-2)%3
    items = {2:(3,1,0),3:(4,1,0,2),4:(5,1,2,0,3)}[base]
    for size in range(base+3,k+1,3):
        items = (size+1,1,size-1)+tuple(size-2-v for v in items)
    return list(items)


def check_case(k,paths,freeze,result,p_roles,p_edges,f,high):
    saved = read(HERE/f"k{k}_certificate.json")
    rec = freeze["originals"][str(k)]
    if k==2:
        file = paths["target"]
        origin = {"origin":"retained","path":rec["reference"]["path"],"sha256":digest(file)}
        need((ROOT/origin["path"]).resolve()==file.resolve(),"retained K=2 reference")
    else:
        file = HERE/f"k{k}_original.json"
        origin = {"origin":"new","path":file.name,"sha256":digest(file)}
    original = read(file)
    digest_t = original["graph_digest"]
    roles,edges = reconstruct(original,k+5)
    need(rec=={"reference":origin,"receipt":{"valid":True,"errors":[],"n":17+k,"m":16+k,"graph_digest":digest_t}}
         and saved["original"]==origin and saved["graph_digest"]==digest_t and saved["K"]==k,"frozen original binding")
    need(result["cases"][str(k)]=={"origin":origin["origin"],"certificate_sha256":digest(HERE/f"k{k}_certificate.json")},
         "raw certificate hash")
    assigned = [e for e in edges if all(v in p_roles for v in e)]
    remaining = [e for e in edges if e not in assigned]
    path = [f"s:{i}" for i in range(4,k+5)]
    need(Counter(assigned)==Counter(p_edges) and all(roles[v]==role for v,role in p_roles.items())
         and set(roles)-set(p_roles)==set(path[1:]) and remaining==list(zip(path,path[1:])),
         "retained named prefix and only the actual suffix path")
    shifted = {v:x+k*(v in high) for v,x in f.items()}
    ds = weights(shifted,assigned)
    R = sorted(set(range(k+17))-set(shifted.values()))
    D = sorted(set(range(1,k+17))-set(ds))
    need(sorted(shifted.values())==list(range(8))+list(range(k+8,k+17))
         and sorted(ds)==list(range(k+1,k+17)) and R==list(range(8,k+8)) and D==list(range(1,k+1)),
         "original T alphabet complements")
    need(saved["prefix"]==shifted and saved["R"]==R and saved["D"]==D
         and saved["physical_port"]==["s:4",k+9] and shifted["s:4"]==k+9
         and saved["path"]==path and saved["pending"]==[list(e) for e in remaining],"saved physical boundary")
    need(saved["partial_checker"]=={"valid":True,"errors":[],"n":17+k,"m":16+k,
         "graph_digest":digest_t,"used_labels":sorted(shifted.values()),"used_differences":sorted(ds),
         "unused_labels":R,"unused_differences":D,"frontier":["s:4"],"complete":False,
         "claim":"partial assignment only; no completion or independent-supplier claim"},"actual partial verification")
    c = numeric_sequence(k)
    translated = [x+8 for x in c]
    complete = {**shifted,**dict(zip(path[1:],translated[1:],strict=True))}
    tail_ds = weights(complete,remaining)
    need(c==saved["C_K"] and translated==saved["translated_path"] and translated[0]==shifted["s:4"]
         and sorted(translated[1:])==R and sorted(tail_ds)==D and tail_ds==saved["pending_weights"]
         and saved["labels"]==complete,"independent suffix recurrence and assignment")
    full_ds = full_receipt(original,roles,edges,complete,saved["checker"])
    need(saved["named_edges"]==[{"edge":list(e),"difference":d} for e,d in zip(edges,full_ds,strict=True)],
         "every named completed edge ledger")
    if k==2:
        d066 = read(paths["d066_cert"])
        need(d066["target"]["labels"]==complete and d066["target"]["checker"]==saved["checker"]
             and d066["shifted_prefix"]["labels"]==shifted,"unchanged retained K=2 witness")
    return {"kind":origin["origin"],"graph_digest":digest_t,"n":len(roles),"m":len(edges),"port":shifted["s:4"],
            "R":R,"D":D,"C_K":c,"pending_weights":tail_ds}


def adverse_receipts(saved,k2):
    wrong = saved["wrong_digest"]
    need(wrong["expected"]=="0"*64 and wrong["labels"]=={} and wrong["checker"]["valid"] is False
         and wrong["checker"]["graph_digest"]==k2["graph_digest"]
         and "original graph digest mismatch" in wrong["checker"]["errors"],"actual wrong digest rejection")
    need(saved["wrong_path"]=={"attempt":["s:2","s:5","s:6"],"rejection":"expected original named path after s:4"}
         and saved["wrong_D"]=={"R":[8,9],"D":[1,3],"port":11,
                                "rejection":"incorrect original nonadjacent inventories or port"},"actual path and inventory rejection")
    need(saved["k1"]=={"R":[8],"D":[1],"port":10,"forced_weight":abs(10-8),"graph_generated":False,
                      "rejection":"nonadjacent consumer requires exact integer K>=2"}
         and abs(10-8)!=1,"actual K=1 contract rejection")


def main():
    started = process_time()
    need(sys.version_info[:2] in {(3,12),(3,13)} and not (HERE/"audit_result.json").exists(),"fresh audit")
    cfg,freeze,result = [read(HERE/name) for name in ("config.json","freeze.json","result.json")]
    lim = cfg["limits"]
    need(cfg["fixed_branch_sizes"]==[2]*4 and (cfg["retained_K"],tuple(cfg["new_K"]))==(2,CASES[1:])
         and (cfg["ell"],cfg["physical_port"])==(8,"s:4"),"frozen exact scope")
    paths = verify_custody(cfg,freeze)
    roles,edges,f,high,p_digest,identity = prefix_source(paths,read(HERE/"prefix_control.json"))
    need(result["status"]=="PASS_PENDING_INDEPENDENT_AUDIT" and (result["full_certificates"],result["retained_K"],
         result["new_originals"],result["solver_queries"],result["enumeration_nodes"])==(5,2,4,0,0)
         and set(result["cases"])==set(freeze["originals"])=={str(k) for k in CASES},"exact finite receipt")
    cpu_before = freeze["cpu_seconds"]+result["cpu_seconds"]
    audited = {}
    for k in CASES:
        audited[str(k)] = check_case(k,paths,freeze,result,roles,edges,f,high)
        need(cpu_before+process_time()-started<=lim["max_cpu_seconds"],"combined CPU cap")
    adverse_receipts(read(HERE/"adverse.json"),audited["2"])
    elapsed = cpu_before+process_time()-started
    need(elapsed<=lim["max_cpu_seconds"],"final combined CPU cap")
    names = ["freeze.json","result.json","prefix_control.json","adverse.json",
             *(f"k{k}_original.json" for k in CASES[1:]),*(f"k{k}_certificate.json" for k in CASES)]
    report = {"status":"PASS","full_certificates_checked":5,"new_originals":4,"retained_originals":1,"new_audit_cases":0,
              "solver_queries":0,"enumeration_nodes":0,"cases":audited,"adverse":"PASS","prefix_digest":p_digest,
              "prefix_ledger_id":identity,"combined_cpu_seconds":elapsed,"runtime":sys.version,
              "sha256":{p:digest(HERE/p) for p in names}}
    data = json.dumps(report,sort_keys=True,indent=2).encode()+b"\n"
    sizes = [p.stat().st_size for p in HERE.iterdir() if p.is_file()]+[len(data)]
    need(max(sizes)<=lim["max_record_bytes"] and sum(sizes)<=lim["max_total_bytes"],"evidence size limits")
    with (HERE/"audit_result.json").open("xb") as out:
        out.write(data)
    print("PASS: independent original-bound audit of retained K=2 and new K=3,4,5,8.")


if __name__ == "__main__":
    main()
