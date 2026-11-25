"""Reconcile the saved official D164 records. This file never searches."""
from collections import Counter
from hashlib import sha256
import re
import json
from pathlib import Path
import sys
import time
import types
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).absolute().parents[3]
CLOSE = Path(__file__).absolute().parent
RUN = ROOT / "runs/d164-exceptional-four-first-001"
APPROVAL = ROOT / "runs/d164-exceptional-four-first-001-authorization.json"
PREP = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_MATCHED_001_PREP"
MANIFEST_SHA = "0c0d62a398506fc04e44de9d1e98ddbc47fb8b9765c289d277f17f3d5661b1ef"
TASK = "LCL-ORDINARY-SPINE-EXCEPTIONAL-FOUR-FIRST-CENTER-MATCHED-001-PREP"


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
    module = types.ModuleType("d164_closeout_unchanged_checker")
    module.__file__ = str(source)
    exec(compile(raw,str(source),"exec"),vars(module))
    return module


def original_rows():
    index = read(PREP/"input/corpus_index.json")["targets"]
    rows = {}
    for i in range(0,len(index),32):
        batch = index[i:i+32]
        observed = read(PREP/"input"/batch[0]["shard"])
        for item,entry in zip(observed,batch,strict=True):
            checked(stamp(encoded(item))["sha256"]==entry["record_sha256"], "frozen corpus record bytes")
            checked({k:v for k,v in item.items() if k!="graph"}==
                    {k:v for k,v in entry.items() if k!="record_sha256"}, "frozen original metadata")
            checked(item["id"] not in rows, "duplicated frozen target")
            rows[item["id"]] = item
    checked(list(rows)==[f"target-{i:04d}" for i in range(1,2305)], "frozen order")
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
    first_centers = [f"b:{u_index}:{i}" for i in range(4)]
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
    checked((A,B)==(5+e2,3+e1+h) and (record["arm"]=="E+")==bool(terminals), "arm and exterior widths")
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

    neutral, = (name for name in first_centers if reduced[name]==A-1)
    pinned, = (name for name in second_centers if reduced[name]==A+2)
    terminal_roles = [{"terminal":name,"parent":parent[name],"reduced":reduced[name],
                       "parent_reduced":reduced[parent[name]]} for name in terminals]
    displacements = {
        host: ({"kind":"translation","offset":A-1-reduced[host]} if reduced[host]<A
               else {"kind":"reflection","intercept":s+reduced[host]-A+1})
        for host in hosts
    }
    structure = {"A":A,"B":B,"s":s,"e1":e1,"e2":e2,"h":h,"neutral":neutral,"upper_index_two":pinned,
                 "upper_index_two_gap_quota":quotas[pinned],"displacements":displacements}
    reported = dict(audit["exterior_structure"])
    recorded_terminals = reported.pop("terminals")
    checked(structure==reported and
            sorted(recorded_terminals,key=lambda row:row["terminal"])==
            sorted(terminal_roles,key=lambda row:row["terminal"]), "independent exterior structure")
    checked(quotas[neutral]==4 and all(gap[i]["host"]==neutral and gap[i]["image"]==i for i in range(4)) and
            gap[-1]["host"]==pinned and gap[-1]["image"]==4 and
            (B!=4 or gap[K-A]["host"]==pinned), "forced physical reservations")
    direct_gap = next(({"source":row["source"],"image":row["image"],"crossing":row["crossing"]}
                       for row in gap if row["leaf"]==direct),None)
    used_moves = sorted({(row["host"],row["source"]<K-A,row["crossing"]) for row in gap})
    return {**structure,"terminals":terminal_roles,"gap_quotas":quotas,"x":x_count,"y":y_count,
            "direct_gap":direct_gap,"used_host_side_crossing_types":used_moves,
            "connector_weight":connector[2]}


def count_qualified(counts):
    number,strata = (counts[key] for key in ("qualified_exteriors","qualified_strata"))
    checked(type(number) is int and 0<=number and isinstance(strata,dict) and
            all(type(value) is int and value>0 for value in strata.values()) and
            number==sum(strata.values()), "qualified representative totals")
    for key in strata:
        A,B,e1,e2,h,neutral,pinned = key.split(",")
        A,B,e1,e2,h = (int(value) for value in (A,B,e1,e2,h))
        checked((A,B)==(5+e2,3+e1+h) and B>=4 and h in (0,1) and
                neutral.startswith("b:28:") and pinned.startswith("b:29:"), "qualified physical stratum")
    return number,strata


def disposition(item,record,prefix,checker):
    target,arm = item["id"],record["arm"]
    checked(arm in ("T","E+") and (record["target"],record["digest"],record["parameters"],record["K"])==
            (target,item["digest"],item["parameters"],item["K"]) and
            all(record[key]==item[key] for key in ("quota_four_count","quota_parities","T1","T2")) and
            record["raw_exterior"]==item["raw_exterior"][arm], "frozen named arm identity")
    result,audit = record["result"],record["audit"]
    declared = item["symbolic_basis"][arm]
    if declared:
        category = "RAW_EXTERIOR_ABSENT" if item["raw_exterior"][arm]=="ABSENT" else "RAW_PRESENT_SYMBOLIC_GAP_EXCLUSION"
        checked(result=={"claim":"NO","basis":declared} and
                audit=={"status":"SYMBOLIC_QUALIFICATION","original":prefix["frontier"]} and
                not any(record["meter_delta"].values()) and record["category"]==category,
                "symbolic scope and zero evaluator activity")
        return {"claim":"NO","basis":declared,"category":category}
    number,strata = count_qualified(result["counts"])
    if result["claim"]=="YES":
        checked(number>0 and record["category"]=="COMPATIBLE_COMPLETION","positive qualification")
        return {"claim":"YES","category":record["category"],"primary_qualified_exteriors":number,
                "feature":check_positive(item,record,prefix,checker)}
    basis = "ALLOCATION_EXHAUSTED" if number else "NO_QUALIFIED_EXTERIOR"
    checked(result["claim"]=="NO" and basis==record["category"]==result["basis"]==audit["basis"] and
            audit["status"]=="PASS_INDEPENDENT_EXHAUSTION" and (number,strata)==count_qualified(audit["counts"]),
            "complete independent rejection basis and physical strata")
    return {"claim":"NO","basis":basis,"category":basis,"qualified_exteriors":number,"strata":strata}


def reconcile(files,authorization):
    manifest = (PREP/"MANIFEST.json").read_bytes()
    checked(stamp(manifest)["sha256"]==MANIFEST_SHA,"accepted frozen manifest")
    prep = json.loads(manifest)
    for row in prep["files"]:
        checked(stamp((ROOT/row["path"]).read_bytes())=={"sha256":row["sha256"],"bytes":row["bytes"]},
                "frozen member bytes")
    checked(json.loads(authorization)=={"task":TASK,"manifest_sha256":MANIFEST_SHA,
                                         "status":"AUTHORIZED_FOR_OFFICIAL_RUN"}, "authorization")
    checked(json.loads(files["CLAIM.json"])=={"approval_sha256":stamp(authorization)["sha256"],
            "manifest_sha256":MANIFEST_SHA,"status":"CLAIMED_ONCE"} and files["WORKER"]==b"D164 one worker\n",
            "exclusive claim and worker marker")
    summary,supervision = (json.loads(files[name]) for name in ("SUMMARY.json","SUPERVISION.json"))
    checked(summary["status"]==supervision["status"]=="INCOMPLETE" and
            summary["reason"]=="LIMIT: retained per-candidate state ceiling" and
            (summary["active_target"],summary["active_arm"])==("target-0429","T") and
            supervision["worker_exit"]==1 and supervision["worker_cpu"]==summary["cpu_seconds"] and
            supervision["reason"]=="worker or combined cap", "exact stopping receipts")
    checker = verifier()
    prefix = read(PREP/"input/prefix.json")
    checked(checker.verify_certificate(prefix["graph"],prefix["actual_labels"],
                                      expected_graph_digest=prefix["digest"])["valid"],"common input certificate")
    originals = original_rows()
    pairs,patterns,measured = Counter(),Counter(),Counter()
    categories = {arm:Counter() for arm in ("T","E+")}
    bases = {arm:Counter() for arm in ("T","E+")}
    primary_negative,primary_positive = Counter(),Counter()
    negative_count,positive_count = 0,0
    included = {"CLAIM.json","WORKER","SUMMARY.json","SUPERVISION.json"}
    separators,records = [],[]
    absent_arms,unresolved_arms,symbolic_remaining = Counter(),Counter(),Counter()
    unresolved_pairs = 0
    for index,(name,item) in enumerate(originals.items(),start=1):
        if index>summary["paired_audits"]:
            absent_arms.update(("T","E+"))
            unresolved = [arm for arm,basis in item["symbolic_basis"].items() if basis is None]
            unresolved_arms.update(unresolved)
            unresolved_pairs += bool(unresolved)
            symbolic_remaining.update(arm for arm,basis in item["symbolic_basis"].items() if basis is not None)
            continue
        arms = {}
        for arm,suffix in (("T","T"),("E+","Eplus")):
            file = f"{name}-{suffix}.json"
            included.add(file)
            record = json.loads(files[file])
            checked(record["arm"]==arm,"physical arm order")
            delta=record["meter_delta"]
            checked(set(delta)==set(summary["entered"]) and delta["targets"]==delta["dispositions"]==0 and
                    all(type(value) is int and value>=0 for value in delta.values()), "completed-arm meter delta")
            measured.update(delta)
            outcome = disposition(item,record,prefix,checker)
            arms[arm] = {"file":file,**stamp(files[file]),**outcome}
            categories[arm][outcome["category"]] += 1
            if outcome["claim"]=="YES":
                positive_count += 1
                primary_positive[arm] += outcome["primary_qualified_exteriors"]
                f = outcome["feature"]
                patterns[(arm,f["A"],f["B"],f["e1"],f["e2"],f["h"])] += 1
            else:
                bases[arm][outcome["basis"]] += 1
                if "qualified_exteriors" in outcome:
                    negative_count += 1
                    primary_negative[arm] += outcome["qualified_exteriors"]
        pair_file = name+"-PAIR.json"
        included.add(pair_file)
        T,Eplus = (arms[arm]["claim"] for arm in ("T","E+"))
        separated = T=="NO" and Eplus=="YES"
        checked(json.loads(files[pair_file])=={"target":name,"graph_digest":item["digest"],"arms":{"T":T,"E+":Eplus},
            "E":"YES" if "YES" in (T,Eplus) else "NO","separating":separated}, "matched-arm outcome")
        pairs[T+"/"+Eplus]+=1
        if separated:
            separators.append(name)
        records.append({"target":name,"parameters":item["parameters"],"digest":item["digest"],
                        "arms":arms,"pair":{"file":pair_file,**stamp(files[pair_file])},"separating":separated})
    distribution=dict.fromkeys(("YES/YES","YES/NO","NO/YES","NO/NO"),0)
    distribution.update(pairs)
    checked(included==set(files) and len(records)==summary["paired_audits"]==428 and
            summary["completed_arms"]==2*len(records)==856 and summary["entered"]["targets"]==len(records)+1 and
            summary["entered"]["dispositions"]==2*len(records)+1 and
            summary["separating"]==len(separators)==0 and summary["paired_distribution"]==distribution and
            summary["finite_hypothesis"]=="UNDECIDED", "partial coverage, segregation and outcome")
    counters=("exterior_nodes","transfer_states","transitions")
    remaining_meter={key:summary["entered"][key]-measured[key] for key in counters}
    checked(all(value>=0 for value in remaining_meter.values()),"unfinished-arm residual meter")
    limits=prep["future_execution_limits"]
    for key,count in summary["entered"].items():
        checked(count<=limits[key],"official limit "+key)
    before=len(manifest)+sum(row["bytes"] for row in prep["files"])+len(authorization)+sum(
        len(data) for name,data in files.items() if name not in ("SUMMARY.json","SUPERVISION.json"))
    checked(before==summary["bytes_before_summary"],"byte accounting through ordinary evidence")
    total=before+len(files["SUMMARY.json"])+len(files["SUPERVISION.json"])
    checked(total<=limits["evidence_bytes"] and max(map(len,files.values()))<=limits["record_bytes"],
            "official evidence ceilings")
    pc,pw = (prep[key] for key in ("measured_preparation_cpu_seconds","measured_preparation_wall_seconds"))
    checked(abs(pc-supervision["measured_preparation_cpu"])<1e-8 and
            abs(pw-supervision["measured_preparation_wall"])<1e-8 and
            abs(pc+supervision["supervisor_cpu"]+supervision["worker_cpu"]-supervision["combined_cpu"])<1e-8,
            "frozen measured preparation and combined process CPU")
    blocked=originals[summary["active_target"]]
    return {"task":TASK,"status":"PASS_SAVED_RECORD_RECONCILIATION","manifest_sha256":MANIFEST_SHA,
            "prepared_head":"52086a1a3ec48e752fd6dbea72991739cfbe893a","summary":summary,"supervision":supervision,
            "paired_distribution":distribution,"categories":categories,"arm_negative_bases":bases,
            "separators":separators,"positive_rechecks":positive_count,
            "negative_audits_reviewed_without_search":negative_count,
            "primary_positive_qualified_exteriors_seen_before_success":primary_positive,
            "matched_negative_qualified_exterior_totals":primary_negative,
            "completed_arms_scientific_meter":{key:measured[key] for key in counters},
            "unfinished_arm_residual_scientific_meter":remaining_meter,
            "unmatched_originals":len(originals)-len(records),"official_arm_records_absent":absent_arms,
            "absent_arms_already_symbolically_decided":symbolic_remaining,
            "arms_unresolved_after_frozen_symbolic_qualifications":unresolved_arms,
            "originals_with_unresolved_arms_after_frozen_symbolic_qualifications":unresolved_pairs,
            "active_original":{key:blocked[key] for key in ("id","parameters","K","T1","T2","digest")},
            "retained_positive_patterns":[{"arm":arm,"A":A,"B":B,"e1":e1,"e2":e2,"h":h,"records":num}
                                           for (arm,A,B,e1,e2,h),num in sorted(patterns.items())],
            "rows":records,"raw_members":[{"name":name,**stamp(data)} for name,data in files.items()],
            "raw_member_bytes":sum(map(len,files.values())),"max_raw_member_bytes":max(map(len,files.values())),
            "approval":stamp(authorization),"actual_evidence_bytes":total}


def main():
    checked(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,"isolated closeout runtime")
    start_cpu,start_wall=time.process_time(),time.monotonic()
    files={}
    privacy = re.compile(rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----|github_pat_[a-z0-9_]{16,}|\bgh[pousr]_[a-z0-9]{20,}|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|\bsk-(?:proj-)?[a-z0-9_-]{22,}|authorization\s*:\s*(?:Bearer|Basic)\s+\S+|\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|[A-Z]:\\+Users\\+",re.I)
    for path in sorted(RUN.iterdir()):
        metadata=path.lstat()
        checked(path.is_file() and not path.is_symlink() and not getattr(metadata,"st_file_attributes",0)&0x400,
                "ordinary official record")
        raw=path.read_bytes()
        checked(not privacy.search(raw),"publication review pattern in "+path.name)
        files[path.name]=raw
    authorization=APPROVAL.read_bytes()
    checked(not privacy.search(authorization),"publication review pattern in authorization")
    report=reconcile(files,authorization)
    for output in ("OFFICIAL_RAW.zip","AUTHORIZATION.json","RECONCILIATION.json"):
        checked(not (CLOSE/output).exists(),"vacant preservation path "+output)
    with (CLOSE/"OFFICIAL_RAW.zip").open("xb") as stream:
        with ZipFile(stream,"w",compression=ZIP_DEFLATED,compresslevel=9) as archive:
            for name,payload in files.items():
                meta=ZipInfo(name)
                meta.compress_type=ZIP_DEFLATED
                archive.writestr(meta,payload,compresslevel=9)
    with ZipFile(CLOSE/"OFFICIAL_RAW.zip") as archive:
        checked(archive.namelist()==list(files) and archive.testzip() is None and
                all(archive.read(name)==data for name,data in files.items()),"raw ZIP byte reconciliation")
    with (CLOSE/"AUTHORIZATION.json").open("xb") as stream:
        stream.write(authorization)
    report["raw_archive"]=stamp((CLOSE/"OFFICIAL_RAW.zip").read_bytes())
    report["closeout_cpu_through_archive_verification"]=time.process_time()-start_cpu
    report["closeout_wall_through_archive_verification"]=time.monotonic()-start_wall
    with (CLOSE/"RECONCILIATION.json").open("xb") as stream:
        stream.write(encoded(report))
    print(json.dumps({key:value for key,value in report.items() if key not in ("rows","raw_members")},sort_keys=True))


if __name__=="__main__":
    main()
