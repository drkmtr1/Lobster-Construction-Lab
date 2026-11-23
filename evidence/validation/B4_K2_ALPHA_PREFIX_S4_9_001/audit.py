"""Arithmetic audit independent of the producer and the production verifier."""
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P_PROFILE = [[2],[2],[2],[2],[]]
PENDING = [("s:4","s:5"),("s:5","s:6")]
EXPECTED_P = {
    "s:0":10,"s:1":2,"s:2":16,"s:3":7,"s:4":9,
    "b:0:0":6,"l:0:0:0":12,"l:0:0:1":13,
    "b:1:0":14,"l:1:0:0":1,"l:1:0:1":4,
    "b:2:0":0,"l:2:0:0":15,"l:2:0:1":11,
    "b:3:0":8,"l:3:0:0":3,"l:3:0:1":5,
}


def need(ok,why):
    if not ok:
        raise ValueError(why)


def checksum(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def canonical_hash(payload):
    return sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def reconstruct(original, spine_count, branches):
    graph = original["graph"]
    spine = [f"s:{i}" for i in range(spine_count)]
    profile = [[2] if i in branches else [] for i in range(spine_count)]
    roles = {v:{"kind":"spine","section":i} for i,v in enumerate(spine)}
    named = [(spine[i],spine[i+1]) for i in range(spine_count-1)]
    for i in branches:
        center = f"b:{i}:0"
        roles[center] = {"kind":"branch","section":i,"branch":0}
        named.append((spine[i],center))
        for j in (0,1):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
            named.append((center,leaf))
    edges = [tuple(e) for e in graph["edges"]]
    multiset = Counter(tuple(sorted(e)) for e in named)
    need(graph["schema_version"]==1 and graph["profile"]==profile and graph["spine"]==spine
         and graph["roles"]==roles and Counter(graph["vertices"])==Counter(roles.keys()),"named vertices, roles and profile")
    need(Counter(tuple(sorted(e)) for e in edges)==multiset and len(edges)+1==len(roles),"named edge multiplicities")
    distances = {v:0 for v in spine}
    frontier = set(spine)
    for d in (1,2):
        neighbors = {v for u,v in edges if u in frontier} | {u for u,v in edges if v in frontier}
        frontier = neighbors - distances.keys()
        distances.update((v,d) for v in frontier)
    need(distances=={v:{"spine":0,"branch":1,"leaf":2}[role["kind"]] for v,role in roles.items()},
         "actual named spine witness and distances")
    digest = canonical_hash({"vertices":sorted(roles),"edges":sorted(multiset.elements()),
                             "profile":profile,"spine":spine,"roles":roles})
    need(original["graph_digest"]==digest,"independent original digest")
    return roles,edges


def weights(labels,edges):
    return [max(labels[u],labels[v])-min(labels[u],labels[v]) for u,v in edges]


def good_certificate(original,roles,edges,labels,receipt):
    n = len(roles)
    ds = weights(labels,edges)
    need(set(labels)==set(roles) and all(type(x) is int for x in labels.values())
         and sorted(labels.values())==list(range(n)) and sorted(ds)==list(range(1,n)), "exact label/difference bijections")
    need(receipt["valid"] is True and receipt["errors"]==[] and receipt["edge_differences"]==ds
         and (receipt["n"],receipt["m"])==(n,n-1) and receipt["graph_digest"]==original["graph_digest"],
         "original-bound unchanged checker receipt")
    return ds


def named_rows(edges,ds):
    return [{"edge":list(e),"difference":d} for e,d in zip(edges,ds,strict=True)]


def verify_custody(config, frozen):
    paths = {key:ROOT/ref["path"] for key,ref in config["sources"].items()}
    current = {ref["path"]:checksum(paths[name]) for name,ref in config["sources"].items()}
    need(current=={ref["path"]:ref["sha256"] for ref in config["sources"].values()}
         and current==frozen["inputs"]["archives"],"retained archive hash bindings")
    source_hashes = {p:checksum(ROOT/p) for p in config["production_sha256"]}
    need(source_hashes==config["production_sha256"]==frozen["inputs"]["production"],"production source hashes")
    hashes = {name:checksum(HERE/name) for name in ("INTAKE.md","commands.json","config.json","validate.py","audit.py")}
    hashes["research/B4_K2_ALPHA_PREFIX_S4_9.md"] = checksum(ROOT/"research/B4_K2_ALPHA_PREFIX_S4_9.md")
    need(hashes==frozen["inputs"]["task"] and frozen["parent"]==config["parent"]
         and frozen["target_reference"]==config["sources"]["target"]
         and frozen["prefix_sha256"]==checksum(HERE/"prefix_original.json")
         and (frozen["new_prefix_originals"],frozen["new_target_originals"])==(1,0),"frozen task identity")

    sources = (
        ("nested_manifest","nested_proof",("nested_original","nested_certificate","nested_audit","nested_sources")),
        ("d063_manifest","d063_proof",("target","d063_validation","d063_audit","d063_log","d063_controls")),
        ("d064_manifest","d064_proof",("d064_validation","d064_audit","d064_log","d064_controls")),
        ("d065_manifest","d065_proof",("d065_result","d065_audit","d065_logL","d065_logR")),
    )
    for manifest_key,proof_key,keys in sources:
        mf = read(paths[manifest_key])
        table = {x["path"]:x for x in mf["files"]}
        for k in keys:
            path = paths[k]
            relative = path.relative_to(paths[manifest_key].parent).as_posix()
            need(table[relative]==dict(path=relative,bytes=path.stat().st_size,sha256=checksum(path)),
                 f"historical manifest entry: {k}")
        need(mf["external_proof"]==dict(**config["sources"][proof_key],bytes=paths[proof_key].stat().st_size),
             f"historical proof binding: {proof_key}")
    need(read(paths["nested_audit"])["status"]=="PASS"
         and all(read(paths[k])["scientific_status"]=="EXHAUSTED_RESTRICTED_NEGATIVE"
                 for k in ("d063_audit","d064_audit","d065_audit"))
         and all(read(paths[k])["status"]=="INCOMPLETE" for k in ("joint_incomplete","third_zero_incomplete")),
         "historical scientific scope")
    return paths


def orientations(roles,edges):
    adjacency = {v:[] for v in roles}
    for u,v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    bit = {"s:4":1}
    queue = deque(bit)
    while queue:
        at = queue.popleft()
        for other in adjacency[at]:
            if other not in bit:
                bit[other] = 1-bit[at]
                queue.append(other)
            need(bit[at]!=bit[other],"original bipartition")
    need(set(bit)==set(roles),"connected original prefix")
    return {v for v in bit if bit[v]==0},{v for v in bit if bit[v]==1}


def verify_controls(paths,prefix,p_roles,p_edges,target,certificates):
    controls = certificates["controls"]
    retained = read(paths["core_original"])
    seed = read(paths["core_certificate"])
    names,edges = reconstruct(retained,6,(0,1,3))
    good_certificate(retained,names,edges,seed["labels"],controls["retained_D061"])
    need(controls["retained_D061"]==seed["checker"],"retained core receipt")
    old = read(paths["k1_original"])
    kn,ke = reconstruct(old,6,(0,1,2,3))
    lifted = {v:k+1 for v,k in seed["labels"].items()}
    lifted.update({"b:2:0":0,"l:2:0:0":16,"l:2:0:1":17})
    good_certificate(old,kn,ke,lifted,controls["retained_D062_K1"])
    archived = read(paths["d063_controls"])["k1"]
    need(archived["labels"]==lifted and archived["checker"]==controls["retained_D062_K1"],"retained D062 receipt")
    wrong = controls["wrong_digest"]
    good = certificates["prefix"]["checker"]
    need(wrong["expected"]==target["graph_digest"]!=prefix["graph_digest"] and wrong["checker"]=={
         **good,"valid":False,"errors":["original graph digest mismatch"]},"wrong graph digest control")
    complement = {v:16-x for v,x in EXPECTED_P.items()}
    bad = controls["complement"]
    good_certificate(prefix,p_roles,p_edges,complement,bad["checker"])
    low,high = orientations(p_roles,p_edges)
    class_valid = (sorted(complement[v] for v in low)==list(range(8))
                   and sorted(complement[v] for v in high)==list(range(8,17)))
    need(bad["labels"]==complement and complement["s:4"]==7 and bad["supplier_valid"] is False
         and not class_valid and any((complement[u]<8)==(complement[v]<8) for u,v in p_edges)
         and set(bad["supplier_rejections"])=={"physical s:4 is not 9","prescribed alpha-class alphabets fail",
                                               "an original edge fails the cutoff-8 test"},
         "graceful complement rejected by the prescribed alpha/port filter")


def main():
    started = process_time()
    need(sys.version_info[:2] in {(3,12),(3,13)} and not (HERE/"audit_result.json").exists(),"fresh audit environment")
    config,freeze,result,cert = [read(HERE/name) for name in ("config.json","freeze.json","result.json","certificates.json")]
    paths = verify_custody(config,freeze)
    p,t = read(HERE/"prefix_original.json"),read(paths["target"])
    pn,pe = reconstruct(p,5,(0,1,2,3))
    tn,te = reconstruct(t,7,(0,1,2,3))
    rest = [e for e in te if any(v not in pn for v in e)]
    assigned = [e for e in te if e not in rest]
    need(set(tn)-set(pn)=={"s:5","s:6"} and Counter(assigned)==Counter(pe) and rest==PENDING
         and all(tn[v]==pn[v] for v in pn) and t["graph_digest"]==config["target_digest"]
         and (len(pn),len(pe),len(tn),len(te))==(17,16,19,18), "exact induced original and physical suffix")
    need(freeze["prefix_graph_receipt"]==dict(valid=True,errors=[],n=17,m=16,graph_digest=p["graph_digest"]),
         "frozen original checker receipt")

    low,high = orientations(pn,pe)
    a = config["alpha"]
    need(len(low)==8 and len(high)==9 and low.isdisjoint(high) and low|high==pn.keys()
         and set(a["low"])==low and set(a["high"])==high
         and (a["cutoff"],a["port_vertex"],a["port_label"])==(8,"s:4",9), "actual alpha classes")
    f = cert["prefix"]["labels"]
    need(f==EXPECTED_P and sorted(f[v] for v in low)==list(range(8))
         and sorted(f[v] for v in high)==list(range(8,17)) and f["s:4"]==9, "analytic supplier and port")
    ds = good_certificate(p,pn,pe,f,cert["prefix"]["checker"])
    need(cert["prefix"]["named_edges"]==named_rows(pe,ds),"prefix edge ledger")
    for key,original in (("prefix",p),("target",t)):
        rec = cert[key]
        need(rec["graph_digest"]==original["graph_digest"]
             and rec["ledger_id"]==canonical_hash({"graph_digest":rec["graph_digest"],"labels":sorted(rec["labels"].items())})
             and rec["ledger_id"]!=rec["graph_digest"],"independent graph and ledger identities")
    shifted = cert["shifted_prefix"]
    g = {name:f[name] if name in low else f[name]+2 for name in pn}
    prefix_weights = weights(g,assigned)
    need(shifted["labels"]==g and prefix_weights==[d+2 for d in ds]
         and sorted(g.values())==list(range(8))+list(range(10,19)) and sorted(prefix_weights)==list(range(3,19)),
         "conditionally translated labels and actual weights")
    R = sorted(set(range(19))-set(g.values()))
    D = sorted(set(range(1,19))-set(prefix_weights))
    need(shifted["pending"]==[list(e) for e in rest] and shifted["port"]==["s:4",11]
         and R==shifted["R"]==[8,9] and D==shifted["D"]==[1,2],"exact pending resources")
    partial = shifted["checker"]
    need(partial["valid"] is True and partial["complete"] is False and partial["errors"]==[]
         and partial["graph_digest"]==t["graph_digest"] and partial["frontier"]==["s:4"]
         and partial["used_labels"]==sorted(g.values()) and partial["used_differences"]==sorted(prefix_weights)
         and partial["unused_labels"]==R and partial["unused_differences"]==D,"unchanged partial checker")
    result_labels = dict(g,**{"s:5":9,"s:6":8})
    tail = weights(result_labels,rest)
    need(tail==[2,1] and cert["target"]["labels"]==result_labels,"physical completion")
    final_weights = good_certificate(t,tn,te,result_labels,cert["target"]["checker"])
    need(cert["target"]["named_edges"]==named_rows(te,final_weights),"completed actual edge ledger")
    verify_controls(paths,p,pn,pe,t,cert)

    query = result["query"]
    need(result["status"]=="VERIFIED_FINITE_SUPPLY_PENDING_INDEPENDENT_AUDIT"
         and result["route"]=="direct_analytic_prefix" and query["status"]=="NOT_RUN"
         and (query["calls"],query["visited_nodes"])==(0,0)
         and result["certificates_sha256"]==checksum(HERE/"certificates.json")
         and (result["new_prefix_originals"],result["new_target_originals"])==(1,0),"result scope and receipt")
    cpu = freeze["cpu_seconds"]+result["cpu_seconds"]+process_time()-started
    lim = config["limits"]
    need(cpu<=lim["max_cpu_seconds"],"combined process CPU cap")
    report = {"status":"PASS","scientific_status":"SUPPLIED_EXACT_FINITE_WITNESS","query":query,
              "new_prefix_originals":1,"new_target_originals":0,"combined_cpu_seconds":cpu,
              "runtime":{"python":sys.version,"platform":sys.platform},
              "prefix_digest":p["graph_digest"],"target_digest":t["graph_digest"],
              "prefix_ledger_id":cert["prefix"]["ledger_id"],"target_ledger_id":cert["target"]["ledger_id"],
              "P":{"L":sorted(low),"H":sorted(high),"port":f["s:4"],"named_weights":named_rows(pe,ds)},
              "T_prefix":{"R":R,"D":D,"port":g["s:4"],"pending":named_rows(rest,tail)},
              "controls":"PASS","raw_sha256":{p:checksum(HERE/p) for p in
                              ("prefix_original.json","freeze.json","certificates.json","result.json","audit.py")}}
    payload = json.dumps(report,sort_keys=True,indent=2).encode()+b"\n"
    sizes = [p.stat().st_size for p in HERE.iterdir() if p.is_file()]+[len(payload)]
    need(max(sizes)<=lim["max_record_bytes"] and sum(sizes)<=lim["max_total_bytes"],"evidence byte caps")
    with (HERE/"audit_result.json").open("xb") as out:
        out.write(payload)
    print("PASS: independently verified the finite P supplier, exact shifted inventories and original T completion.")


if __name__ == "__main__":
    main()
