"""Reconcile the already completed D161 records. This file never searches."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import time
import types
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).absolute().parents[3]
CLOSE = Path(__file__).absolute().parent
RUN = ROOT / "runs/d161-exceptional-quota-four-001"
APPROVAL = ROOT / "runs/d161-exceptional-quota-four-001-authorization.json"
PREP = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_QUOTA_FOUR_MATCHED_001_PREP"
MANIFEST_SHA = "3839c60a588a7e8c0eeee3b62c107e8182fffa24cd06bf649b3faa9c32997fdf"
TASK = "LCL-ORDINARY-SPINE-EXCEPTIONAL-FIVE-HOST-QUOTA-FOUR-MATCHED-001-PREP"


def checked(test, description):
    if not test:
        raise ValueError(description)


def read(path):
    return json.loads(path.read_bytes())


def encoded(data, pretty=False):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True,
                       **({"indent":2} if pretty else {"separators":(",",":")}))+"\n").encode()


def stamp(data):
    return {"sha256":sha256(data).hexdigest(),"bytes":len(data)}


def verifier():
    source = ROOT/"lcl/verify.py"
    raw = source.read_bytes()
    checked(stamp(raw)["sha256"]=="230b852035a49eb2973a42730f31a5b94c733a92886dcc9158b50c3e94649909", "checker bytes")
    module = types.ModuleType("d161_closeout_unchanged_checker")
    module.__file__ = str(source)
    exec(compile(raw,str(source),"exec"),vars(module))
    return module


def original_rows():
    index = read(PREP/"input/corpus_index.json")["targets"]
    rows = {}
    for i in range(0,len(index),12):
        batch = index[i:i+12]
        observed = read(PREP/"input"/batch[0]["shard"])
        for item,entry in zip(observed,batch,strict=True):
            checked(stamp(encoded(item))["sha256"]==entry["record_sha256"], "frozen corpus record bytes")
            checked({k:v for k,v in item.items() if k!="graph"}==
                    {k:v for k,v in entry.items() if k!="record_sha256"}, "frozen original metadata")
            checked(item["id"] not in rows, "duplicated frozen target")
            rows[item["id"]] = item
    checked(list(rows)==[f"target-{i:03d}" for i in range(1,100)], "frozen order")
    return rows


def check_positive(item, record, prefix, checker):
    graph = item["graph"]
    audit = record["audit"]
    solution = record["result"]["solution"]
    n,c,d,K = prefix["n"],prefix["c"],prefix["d"],item["K"]
    A,B = solution["A"],solution["B"]
    s,m,cut = 2*K-A-B,n+2*K,n+2*K+1-c-K
    reduced,actual = audit["reduced"],audit["actual_labels"]
    v,u,w = graph["spine"][-3:]
    u_index = graph["roles"][u]["section"]
    w_index = u_index+1
    direct = f"b:{w_index}:2"
    first_centers = [f"b:{u_index}:{i}" for i in range(3)]
    second_centers = [f"b:{w_index}:{i}" for i in range(2)]
    hosts = first_centers+second_centers+[w]
    parent = {u:v,w:u,**dict.fromkeys(first_centers,u),**dict.fromkeys(second_centers+[direct],w)}
    parent.update({leaf:f"b:{role['section']}:{role['branch']}" for leaf,role in graph["roles"].items()
                   if role["kind"]=="leaf" and role["section"]>=u_index})
    checked(audit["status"]=="PASS_INDEPENDENT_RECONSTRUCTION" and audit["original"]==graph and
            audit["graph_digest"]==item["digest"] and (audit["cut"],audit["polarity"])==(cut,"maximum") and
            reduced==solution["reduced"] and actual[w]==m, "positive custody")
    certificate = checker.verify_certificate(graph,actual,expected_graph_digest=item["digest"])
    checked(certificate["valid"] and certificate==audit["certificate"], "unchanged checker replay")
    checked(all(actual[name]==label+B+(s if label>=prefix["actual_cut"] else 0) and
                (actual[name]<cut)==(label<prefix["actual_cut"]) for name,label in prefix["actual_labels"].items()),
            "old transport")
    checked(set(reduced).issubset({*parent,v}) and {v,u,w,*first_centers,*second_centers}.issubset(reduced) and
            sorted(reduced.values())==list(range(A+B+1)) and (reduced[v],reduced[u],reduced[w])==(A,A+1,0) and
            s>=K and n>=2*K, "reduced slots")
    ext_edges = [(name,parent[name]) for name in reduced if name!=v]
    reduced_weights = sorted(abs(reduced[x]-reduced[y]) for x,y in ext_edges)
    checked(reduced_weights==list(range(1,A+B+1))==audit["reduced_weights"] and
            {tuple(edge) for edge in audit["exterior_edges"]}==set(ext_edges) and
            all((reduced[x]<=A)!=(reduced[y]<=A) for x,y in ext_edges), "reduced incidences and spectrum")
    expanded = {name:m-label-(n+s if label>A else 0) for name,label in reduced.items()}
    checked(expanded==audit["expanded_exterior_actual"] and all(actual[name]==label for name,label in expanded.items()),
            "expanded exterior")
    terminals = {name:role for name,role in graph["roles"].items() if name in reduced and role["kind"]=="leaf"}
    e1 = sum(role["section"]==u_index for role in terminals.values())
    e2 = len(terminals)-e1
    h = int(direct in reduced)
    checked((A,B)==(4+e2,3+e1+h) and (record["arm"]=="E+")==bool(terminals), "arm and exterior widths")
    checked(sorted(abs(actual[x]-actual[y]) for x,y in ext_edges)==list(range(n+s+1,m+1)) and
            all((actual[x]<cut)!=(actual[y]<cut) for x,y in ext_edges), "expanded exterior crossing spectrum")
    gap = audit["gap"]
    checked([row["source"] for row in gap]==list(range(s)) and
            sorted(row["image"] for row in gap)==list(range(s)) and
            {row["leaf"] for row in gap}==set(parent)-set(reduced), "gap permutations and names")
    quotas = dict.fromkeys(hosts,0)
    x_count=y_count=0
    for i,row in enumerate(gap):
        leaf,host,image = (row[key] for key in ("leaf","host","image"))
        label = A+c+i
        weight = abs(actual[leaf]-actual[host])
        crosses = (actual[leaf]<cut)!=(actual[host]<cut)
        checked(host in quotas and parent[leaf]==host and host in reduced and m-actual[leaf]==label==row["label_oriented"] and
                weight==d-1+image==row["weight"] and crosses==row["crossing"]==(image>=K) and
                [host,image]==solution["assignment"][i], "gap parent, exact image and crossing")
        quotas[host] += 1
        x_count += crosses and i<K-A
        y_count += crosses and i>=K-A
    checked(quotas==audit["gap_quotas"] and
            audit["crossing_counts"]=={"lower_source_upper_host":x_count,"upper_source_lower_host":y_count} and
            x_count+y_count==s-K, "gap inventories")
    threshold = d+K-1
    scored = [(a,b,abs(actual[a]-actual[b]),(actual[a]<cut)!=(actual[b]<cut)) for a,b in graph["edges"]]
    checked(sorted(edge[2] for edge in scored if edge[3])==list(range(threshold,m+1))==audit["crossing"] and
            sorted(edge[2] for edge in scored if not edge[3])==list(range(1,threshold))==audit["noncrossing"],
            "exact S_-1 crossing and noncrossing spectra")
    partial = {node for node,role in graph["roles"].items() if role["section"]<=u_index}
    used = [edge for edge in scored if edge[0] in partial and edge[1] in partial]
    pending = [edge for edge in scored if edge not in used]
    connector, = [edge for edge in pending if (edge[0] in partial)!=(edge[1] in partial)]
    resources = {"used_labels":sorted(actual[name] for name in partial),
                 "remaining_labels":sorted(actual[name] for name in set(actual)-partial),
                 "used_weights":sorted(edge[2] for edge in used),"remaining_weights":sorted(edge[2] for edge in pending),
                 "used_crossing":sorted(edge[2] for edge in used if edge[3]),
                 "remaining_crossing":sorted(edge[2] for edge in pending if edge[3]),
                 "used_noncrossing":sorted(edge[2] for edge in used if not edge[3]),
                 "remaining_noncrossing":sorted(edge[2] for edge in pending if not edge[3])}
    checked(resources==audit["resources"] and {u,w}==set(connector[:2]) and connector[3] and
            audit["connector"]=={"ends":[u,w],"labels":[actual[u],actual[w]],"weight":connector[2],"crossing":True} and
            connector[2]==n+s+A+1, "intermediate resources and actual connector")
    return {"A":A,"B":B,"s":s,"h":h,"e1":e1,"e2":e2,"x":x_count,"y":y_count,
            "exterior_terminals":[{"name":name,"host":parent[name],"label":reduced[name],
                                   "parent_label":reduced[parent[name]]} for name in sorted(terminals)],
            "gap_quotas":quotas,"neutral":next(name for name in first_centers if reduced[name]==A-1),
            "upper_index_two":next(name for name in second_centers if reduced[name]==A+2),
            "direct_gap_coordinate":next((row["source"] for row in gap if row["leaf"]==direct),None),
            "connector_weight":connector[2]}


def check_negative(item,record):
    result,audit = record["result"],record["audit"]
    basis = result["basis"]
    if basis=="T2_2_PHYSICAL_COUNT":
        checked(item["T2"]==2 and audit["status"]=="SYMBOLIC_QUALIFICATION", "T2=2 symbolic audit")
    elif basis=="T2_4_NO_EXTERIOR_TERMINALS":
        checked(item["T2"]==4 and record["arm"]=="E+" and audit["status"]=="SYMBOLIC_QUALIFICATION",
                "T2=4 symbolic audit")
    else:
        checked(audit["status"]=="PASS_INDEPENDENT_EXHAUSTION" and audit["basis"]==basis and
                result["counts"]["qualified_exteriors"]==audit["counts"]["qualified_exteriors"] and
                (basis=="NECESSARY_GAP_EXCLUSIONS" and audit["counts"]["qualified_exteriors"]==0 or
                 basis=="ALLOCATION_EXHAUSTED" and audit["counts"]["qualified_exteriors"]>0),
                "separate exhaustive rejection")
    if audit["status"]=="SYMBOLIC_QUALIFICATION":
        checked(all(value==0 for value in record["meter_delta"].values()), "symbolic arm executed search")
    return basis


def reconcile(files,authorization):
    manifest = (PREP/"MANIFEST.json").read_bytes()
    checked(stamp(manifest)["sha256"]==MANIFEST_SHA, "accepted manifest")
    prep = json.loads(manifest)
    for row in prep["files"]:
        checked(stamp((ROOT/row["path"]).read_bytes())=={"sha256":row["sha256"],"bytes":row["bytes"]},
                "frozen preparation member")
    checked(json.loads(authorization)=={"task":TASK,"manifest_sha256":MANIFEST_SHA,
                                         "status":"AUTHORIZED_FOR_OFFICIAL_RUN"}, "authorization record")
    claim = json.loads(files["CLAIM.json"])
    checked(claim=={"approval_sha256":stamp(authorization)["sha256"],"manifest_sha256":MANIFEST_SHA,
                    "status":"CLAIMED_ONCE"} and files["WORKER"]==b"D161 one worker\n", "frozen claim")
    summary,supervision = (json.loads(files[name]) for name in ("SUMMARY.json","SUPERVISION.json"))
    checked(summary["status"]==supervision["status"]=="COMPLETE" and summary["reason"] is None and
            supervision["reason"] is None and supervision["worker_exit"]==0 and
            summary["cpu_seconds"]==supervision["worker_cpu"] and
            summary["active_target"] is None and summary["active_arm"] is None, "terminal receipts")
    checker = verifier()
    prefix = read(PREP/"input/prefix.json")
    checked(checker.verify_certificate(prefix["graph"],prefix["actual_labels"],
                                      expected_graph_digest=prefix["digest"])["valid"], "common input certificate")
    originals = original_rows()
    pairs,negative,patterns = Counter(),{"T":Counter(),"E+":Counter()},Counter()
    measured = Counter()
    included = {"CLAIM.json","WORKER","SUMMARY.json","SUPERVISION.json"}
    separators = []
    records = []
    for name,item in originals.items():
        A = {}
        for arm,suffix in (("T","T"),("E+","Eplus")):
            file = f"{name}-{suffix}.json"
            included.add(file)
            record = json.loads(files[file])
            checked((record["target"],record["digest"],record["arm"],record["parameters"],record["K"])==
                    (name,item["digest"],arm,item["parameters"],item["K"]) and
                    record["raw_exterior"]=="PRESENT_SYMBOLIC_D160", "official arm record identity")
            measured.update(record["meter_delta"])
            claim = record["result"]["claim"]
            checked(claim in ("YES","NO"), "arm claim")
            A[arm] = {"claim":claim,"file":file,**stamp(files[file])}
            if claim=="YES":
                feats = check_positive(item,record,prefix,checker)
                pattern = (arm,feats["A"],feats["B"],feats["e1"],feats["e2"],feats["h"])
                patterns[pattern]+=1
                A[arm]["feature"]=feats
            else:
                basis = check_negative(item,record)
                negative[arm][basis] += 1
                A[arm]["basis"] = basis
        pair_file = name+"-PAIR.json"
        included.add(pair_file)
        pair = json.loads(files[pair_file])
        T,Eplus = (A[arm]["claim"] for arm in ("T","E+"))
        sep = T=="NO" and Eplus=="YES"
        checked(pair=={"target":name,"graph_digest":item["digest"],"arms":{"T":T,"E+":Eplus},
                       "E":"YES" if "YES" in (T,Eplus) else "NO","separating":sep}, "matched pair inference")
        pairs[T+"/"+Eplus]+=1
        row = {"target":name,"parameters":item["parameters"],"digest":item["digest"],
               "T1":item["T1"],"T2":item["T2"],"arms":A,
               "pair":{"file":pair_file,**stamp(files[pair_file])},"separating":sep}
        records.append(row)
        if sep:
            separators.append(row)
    checked(included==set(files) and summary["paired_audits"]==len(originals)==99 and
            summary["completed_arms"]==198 and summary["separating"]==len(separators) and
            summary["finite_hypothesis"]==("SUPPORTED" if separators else "FALSIFIED_FINITE"), "complete frozen scope")
    checked(summary["entered"]["targets"]==99 and summary["entered"]["dispositions"]==198 and
            all(summary["entered"][k]==measured[k] for k in ("exterior_nodes","transfer_states","transitions")),
            "scientific counters from arm deltas")
    for key,count in summary["entered"].items():
        checked(count<=prep["execution_limits"][key], "bound: "+key)
    before = (len(manifest)+sum(row["bytes"] for row in prep["files"])+len(authorization)+
              sum(len(payload) for name,payload in files.items() if name not in ("SUMMARY.json","SUPERVISION.json")))
    checked(before==summary["bytes_before_summary"], "byte accounting before summary")
    prep_super = read(PREP/"PREPARATION_SUPERVISION.json")
    checked(abs(prep_super["cpu_seconds"]+supervision["supervisor_cpu"]+supervision["worker_cpu"]-
                supervision["combined_cpu"])<1e-8, "supervised combined CPU")
    total = before+len(files["SUMMARY.json"])+len(files["SUPERVISION.json"])
    checked(total<=prep["execution_limits"]["evidence_bytes"] and
            max(map(len,files.values()))<=prep["execution_limits"]["record_bytes"],"evidence ceilings")
    return {"task":TASK,"status":"PASS_SAVED_RECORD_RECONCILIATION","manifest_sha256":MANIFEST_SHA,
            "prepared_head":"e26f80d950a9c316a4c059a0eb98a843e1aec23c","summary":summary,"supervision":supervision,"arm_negative_bases":negative,
            "paired_distribution":pairs,"separators":[row["target"] for row in separators],
            "retained_positive_patterns":[{"arm":arm,"A":A,"B":B,"e1":e1,"e2":e2,"h":h,"records":num}
                                          for (arm,A,B,e1,e2,h),num in sorted(patterns.items())],
            "rows":records,"raw_members":[{"name":name,**stamp(data)} for name,data in files.items()],
            "raw_member_bytes":sum(map(len,files.values())),"max_raw_member_bytes":max(map(len,files.values())),
            "approval":stamp(authorization),"actual_evidence_bytes":total,
            "positive_rechecks":sum(patterns.values()),"negative_audits_reviewed_without_search":sum(
                count for sub in negative.values() for basis,count in sub.items() if not basis.startswith("T2_"))}


def main():
    checked(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,"isolated closeout runtime")
    started = time.process_time()
    files = {p.name:p.read_bytes() for p in sorted(RUN.iterdir())}
    authorization = APPROVAL.read_bytes()
    report = reconcile(files,authorization)
    with (CLOSE/"OFFICIAL_RAW.zip").open("xb") as stream:
        with ZipFile(stream,"w",compression=ZIP_DEFLATED,compresslevel=9) as archive:
            for name,payload in files.items():
                meta = ZipInfo(name)
                meta.compress_type=ZIP_DEFLATED
                archive.writestr(meta,payload,compresslevel=9)
    with ZipFile(CLOSE/"OFFICIAL_RAW.zip") as archive:
        checked(archive.namelist()==list(files) and archive.testzip() is None and
                all(archive.read(name)==data for name,data in files.items()), "raw ZIP byte reconciliation")
    with (CLOSE/"AUTHORIZATION.json").open("xb") as stream:
        stream.write(authorization)
    report["raw_archive"] = stamp((CLOSE/"OFFICIAL_RAW.zip").read_bytes())
    report["read_only_reconciliation_cpu_seconds"] = time.process_time()-started
    with (CLOSE/"RECONCILIATION.json").open("xb") as stream:
        stream.write(encoded(report,pretty=True))
    output = {k:v for k,v in report.items() if k not in ("rows","raw_members")}
    print(json.dumps(output,sort_keys=True))


if __name__=="__main__":
    main()
