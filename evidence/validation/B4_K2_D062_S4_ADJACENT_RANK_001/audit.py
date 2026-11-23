"""Independent arithmetic audit of the complete two-template grid."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DIGEST = "c5fd852e27ca85602e9a5a2cb39e3b14434b2783272c57523c2c1b7a317859f4"
F = {
    "s:0":14, "s:1":1, "s:2":15, "s:3":4, "s:4":10, "s:5":11,
    "b:0:0":2, "l:0:0:0":12, "l:0:0:1":9,
    "b:1:0":3, "l:1:0:0":6, "l:1:0:1":7,
    "b:2:0":0, "l:2:0:0":16, "l:2:0:1":17,
    "b:3:0":13, "l:3:0:0":5, "l:3:0:1":8,
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_bytes())


def hash_file(path):
    return sha256(path.read_bytes()).hexdigest()


def reconstruct(original, sections, centers):
    graph = original["graph"]
    spine = [f"s:{i}" for i in range(sections)]
    profile = [[2] if i in centers else [] for i in range(sections)]
    roles = {v: {"kind":"spine","section":i} for i,v in enumerate(spine)}
    edges = [sorted([spine[i],spine[i+1]]) for i in range(sections-1)]
    for i in centers:
        hub = f"b:{i}:0"
        roles[hub] = {"kind":"branch","section":i,"branch":0}
        edges.append(sorted([hub,spine[i]]))
        for j in (0,1):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind":"leaf","section":i,"branch":0,"leaf":j}
            edges.append(sorted([hub,leaf]))
    need(graph["schema_version"]==1 and graph["profile"]==profile and graph["spine"]==spine
         and graph["roles"]==roles and Counter(graph["vertices"])==Counter(roles.keys()), "original named vertices")
    need(Counter(map(tuple,edges)) == Counter(tuple(sorted(e)) for e in graph["edges"])
         and len(edges)+1==len(roles), "actual edge multiplicities")
    payload = {"vertices":sorted(roles),"edges":sorted(edges),"profile":profile,"spine":spine,"roles":roles}
    raw = json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    need(sha256(raw).hexdigest()==original["graph_digest"], "recomputed original graph digest")
    return sorted(roles), [tuple(edge) for edge in graph["edges"]]


def weight(edge, labels):
    low,high = sorted(labels[v] for v in edge)
    return high-low


def arithmetic_receipt(original,names,edges,labels,checker):
    expected = list(range(1,len(edges)+1))
    ds = [weight(edge,labels) for edge in edges]
    need(set(labels)==set(names) and all(type(x) is int for x in labels.values())
         and sorted(labels.values())==list(range(len(names))), "source integer label bijection")
    need(sorted(ds)==expected and ds==checker["edge_differences"] and checker["errors"]==[]
         and checker["valid"] is True and checker["graph_digest"]==original["graph_digest"]
         and (checker["n"],checker["m"])==(len(names),len(edges)), "source certificate")


def sources_and_controls(config, freeze, controls):
    sources = {key:ROOT/ref["path"] for key,ref in config["sources"].items()}
    for group, refs in (
        ("archive",{ref["path"]:ref["sha256"] for ref in config["sources"].values()}),
        ("production",config["production_sha256"]),
    ):
        actual = {p:hash_file(ROOT/p) for p in refs}
        need(actual==refs==freeze["inputs"][group], f"frozen {group} hashes")
    need(freeze["inputs"]["task"]=={p:hash_file(HERE/p) for p in
         ("validate.py","audit.py","commands.json","config.json","pre-run.md")}, "frozen task hashes")
    need(freeze["target"]==config["sources"]["target"] and freeze["parent"]==config["parent"]
         and freeze["new_graph_identities"]==0,"frozen archive reference")

    # Bind the retained D063 input and historical result without replay.
    previous_manifest = read(sources["d063_manifest"])
    previous_files = {entry["path"]:entry for entry in previous_manifest["files"]}
    for key in ("target","d063_validation","d063_audit","d063_log","d063_controls"):
        p = sources[key]
        ref = config["sources"][key]
        need(previous_files[p.name]==dict(path=p.name,bytes=p.stat().st_size,sha256=ref["sha256"]),
             f"D063 manifest: {key}")
    d063_proof = config["sources"]["d063_proof"]
    need(previous_manifest["external_proof"]==dict(**d063_proof,bytes=sources["d063_proof"].stat().st_size),
         "D063 proof manifest")
    d063 = read(sources["d063_validation"])
    need(d063==controls["D063"] and d063["status"]=="EXHAUSTED_RESTRICTED_NEGATIVE"
         and d063["full_candidates"]==38 and read(sources["d063_audit"])["scientific_status"]==d063["status"],
         "D063 remains a restricted negative")

    d064_manifest = read(sources["d064_manifest"])
    entries64 = {entry["path"]:entry for entry in d064_manifest["files"]}
    for key in ("d064_validation","d064_audit","d064_log","d064_controls"):
        file = sources[key]
        need(entries64[file.name]==dict(path=file.name,bytes=file.stat().st_size,sha256=hash_file(file)),
             f"retained D064 manifest: {key}")
    d064_proof = config["sources"]["d064_proof"]
    need(d064_manifest["external_proof"]==dict(**d064_proof,bytes=sources["d064_proof"].stat().st_size),
         "D064 proof manifest")
    d064 = read(sources["d064_validation"])
    stored_audit = read(sources["d064_audit"])
    need(d064==controls["D064"] and d064["status"]=="EXHAUSTED_RESTRICTED_NEGATIVE"
         and d064["full_cases"]==342 and d064["cases_sha256"]==hash_file(sources["d064_log"])
         and stored_audit["status"]=="PASS" and stored_audit["target_digest"]==DIGEST
         and stored_audit["scientific_status"]==d064["status"], "retained D064 scope")

    d062_manifest = read(sources["nested_manifest"])
    entries = {e["path"]:e for e in d062_manifest["files"]}
    for key in ("nested_original","nested_certificate","nested_audit","nested_sources"):
        p = sources[key]
        rel = p.relative_to(sources["nested_manifest"].parent).as_posix()
        need(entries[rel]==dict(path=rel,bytes=p.stat().st_size,sha256=hash_file(p)), "D062 archive bytes")
    need(d062_manifest["external_proof"]==dict(**config["sources"]["nested_proof"],
         bytes=sources["nested_proof"].stat().st_size), "D062 proof manifest")
    need(read(sources["nested_audit"])["status"]=="PASS"
         and read(sources["D059"])["second_cut_matches_q2"]==read(sources["D059"])["second_cut_matches_q3"]==[]
         and read(sources["D060"])["second_host_matches"]==[]
         and all(read(sources[k])["status"]=="INCOMPLETE" for k in ("joint_incomplete","third_zero_incomplete")),
         "historical scopes")

    core = read(sources["core_original"])
    core_names,core_edges = reconstruct(core,6,(0,1,3))
    old = read(sources["core_certificate"])
    expected_core = {v:F[v]-1 for v in core_names}
    need(old["labels"]==expected_core and old["graph_digest"]==core["graph_digest"]
         and old["checker"]==controls["D061"],"D061 exact seed")
    arithmetic_receipt(core,core_names,core_edges,expected_core,controls["D061"])
    catalog = read(sources["catalog"])
    state = next(x for x in catalog["ledgers"] if x["key"]=="alternative-22")
    other = next(x for x in catalog["ledgers"] if x["key"]=="case-b-22")
    for entry in (state,other):
        payload = {"graph_digest":entry["graph_digest"],"labels":sorted(entry["labels"].items())}
        encoded = json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
        need(sha256(encoded).hexdigest()==entry["ledger_id"], "canonical catalog ledger hash")
    need(state["labels"]==expected_core and state["graph_digest"]==other["graph_digest"]==core["graph_digest"]
         and state["ledger_id"]!=other["ledger_id"], "exact alternative ledger, distinct from Case B")
    k1 = read(sources["k1_original"])
    k1_names,k1_edges = reconstruct(k1,6,(0,1,2,3))
    k1_control = controls["D062_K1"]
    need(k1_control["labels"]==F and [F[v] for v in ("b:2:0","l:2:0:0","l:2:0:1")]==[0,16,17],
         "D062 translation and restored zero-host labels")
    arithmetic_receipt(k1,k1_names,k1_edges,F,k1_control["checker"])
    bad = controls["wrong_digest"]
    need(bad["input_labels"]=={} and bad["expected"]=="0"*64
         and bad["observed"]["valid"] is False
         and bad["reference"]["graph_digest"]==bad["observed"]["graph_digest"]==DIGEST
         and bad["observed"]["errors"]==bad["reference"]["errors"]+["original graph digest mismatch"],
         "unchanged checker rejects incorrect target identity")
    bad_label = controls["invalid_label"]
    damaged = dict(F,**{"s:5":F["s:4"]})
    damaged_weights = [weight(e,damaged) for e in k1_edges]
    damaged_receipt = bad_label["checker"]
    need(bad_label["labels"]==damaged and damaged_weights[4]==0
         and damaged_receipt["valid"] is False and "vertex labels repeat" in damaged_receipt["errors"]
         and damaged_receipt["edge_differences"]==damaged_weights
         and damaged_receipt["graph_digest"]==k1["graph_digest"], "adverse label/edge on retained K=1 original")
    need(read(sources["d064_controls"])["prefix_rank"]==controls["prefix_rank"], "retained D064 exact ranks")
    return read(sources["target"]),k1_edges


def compare_inventory(saved,weights):
    missing = [x for x in range(1,19) if x not in weights]
    repeated = [[x,weights.count(x)] for x in sorted(set(weights)) if weights.count(x)>1]
    need(saved==dict(missing=missing,repeated=repeated), "exact repeated/missing multiplicities")
    return missing,repeated


def gap_label(rank,a,b):
    # Insert a in a list of ranks, then insert b in the expanded list.
    after_a = rank+int(rank>=a)
    return after_a+int(after_a>=b)


def omitted_extreme(a,b):
    # The proof states which required difference is impossible.
    if (a,b)==(0,18):
        return 17
    if a==0 or b==18:
        return 18
    if b==17:
        return 17
    return None


def audit_template(template,rows,names,edges,assigned,pending,ranked,full_maps,started,cpu_before,limit):
    before = len(full_maps)
    valid_heads = []
    witnesses = []
    extreme = Counter()
    exhausted_pairs = 0
    cases = 0

    expected_pairs = ((a,b) for a in range(18) for b in range(a+1,19))
    for (a,b), saved in zip(expected_pairs,rows,strict=True):
        exhausted_pairs += 1
        prefix = {v:gap_label(i,a,b) for i,v in enumerate(ranked)}
        R = sorted(set(range(19))-set(prefix.values()))
        need(len(set(prefix.values()))==17 and R==[a,b]==saved["R"]
             and prefix==saved["prefix"] and saved["port"]==["s:4",prefix["s:4"]]
             and saved["template"]==template, "unique prefix rank map")
        if (a,b)==(0,18):
            need(prefix["s:4"]=={"L":10,"R":12}[template], "changed extreme-hole port")
        ds = [weight(e,prefix) for e in assigned]
        D,repeated = compare_inventory(dict(missing=saved["D"],repeated=saved["prefix_repeated"]),ds)
        distinct = repeated==[]
        need(saved["prefix_weights"]==ds and saved["valid_prefix"] is distinct and (not distinct or len(D)==2)
             and set(saved["orders"])=={"A","B"}, "prefix resources")
        if distinct:
            valid_heads.append({"R":R,"D":D,"port":prefix["s:4"],"suffix_weights":{
                "A":[abs(prefix["s:4"]-a),b-a],"B":[abs(prefix["s:4"]-b),b-a]}})
        excluded_difference = omitted_extreme(a,b)
        if excluded_difference is not None:
            extreme[excluded_difference] += 1
        for order,pair in (("A",(a,b)),("B",(b,a))):
            cases += 1
            row = saved["orders"][order]
            f = dict(prefix,**dict(zip(("s:5","s:6"),pair,strict=True)))
            identity = tuple(f[v] for v in names)
            need(sorted(identity)==list(range(19)) and identity not in full_maps and row["suffix_labels"]==list(pair),
                 "full label bijection and distinct ordered map")
            full_maps.add(identity)
            weights = [weight(e,f) for e in edges]
            tail = [weight(e,f) for e in pending]
            missing,duplicates = compare_inventory(row["inventory"],weights)
            good = sorted(weights)==list(range(1,19))
            checker = row["checker"]
            expected_errors = []
            if duplicates:
                expected_errors.append("edge differences repeat")
            if not good:
                expected_errors.append("edge differences are not exactly 1..m")
            need(row["suffix_weights"]==tail and (distinct and sorted(tail)==D)==good
                 and checker["edge_differences"]==weights and checker["errors"]==expected_errors
                 and checker["valid"] is good and checker["graph_digest"]==DIGEST
                 and (checker["n"],checker["m"])==(19,18), "exact original differences and checker")
            if excluded_difference is not None:
                need(excluded_difference in missing, "direct 18/17 obstruction corroboration")
            if good:
                witnesses.append({"R":R,"D":D,"port":prefix["s:4"],"order":order,"labels":f})
        need(cpu_before+process_time()-started<=limit, "combined CPU cap")
    need((exhausted_pairs,cases,len(full_maps)-before)==(171,342,342) and extreme==Counter({18:34,17:17}),
         "completed grid and extreme pair counts")
    return valid_heads,witnesses,{str(d):count for d,count in sorted(extreme.items())}



def main():
    started = process_time()
    need(sys.version_info[:2] in {(3,12),(3,13)} and not (HERE/"audit_result.json").exists(), "fresh audit environment")
    cfg = read(HERE/"config.json")
    freeze,control,result = [read(HERE/p) for p in ("freeze.json","controls.json","result.json")]
    lim = cfg["limits"]
    model = cfg["model"]
    need(model["apply_prefilter"] is False and model["templates"]=={"L":[9,10],"R":[10,11]}
         and cfg["parameters"]==[2]*4 and cfg["target_digest"]==DIGEST
         and (lim["templates"],lim["pairs_per_template"],lim["cases"])==(2,171,684), "declared no-pruning scope")
    original,k1_edges = sources_and_controls(cfg,freeze,control)
    names,edges = reconstruct(original,7,(0,1,2,3))
    need(original["graph_digest"]==DIGEST==freeze["graph"]["graph_digest"] and len(names)==19 and len(edges)==18,
         "one retained target identity")
    tail_names = {"s:5","s:6"}
    assigned = [e for e in edges if tail_names.isdisjoint(e)]
    pending = [e for e in edges if not tail_names.isdisjoint(e)]
    need(pending==[("s:4","s:5"),("s:5","s:6")] and edges==[tuple(e) for e in control["original_edge_order"]]
         and assigned==[tuple(e) for e in control["assigned_edges"]]
         and pending==[tuple(e) for e in control["pending_edges"]]
         and len(assigned)==16 and Counter(e for e in edges if "s:6" not in e)==Counter(k1_edges),
         "sole actual pending path and retained K=1 edges")
    ranked = [v for v in sorted(F,key=F.__getitem__) if v!="s:5"]
    need(ranked==control["prefix_rank"]==model["base_prefix_rank"] and set(ranked)==set(names)-tail_names
         and ranked[9:12]==["l:0:0:1","s:4","l:0:0:0"]
         and [F[v] for v in ranked]==list(range(11))+list(range(12,18)), "physical prefix ranks")
    templates = {"L":ranked[:9]+["s:4","l:0:0:1"]+ranked[11:],
                 "R":ranked[:10]+["l:0:0:0","s:4"]+ranked[12:]}
    need(templates==control["templates"], "two precise name exchanges")
    need(result["grid_complete"] is True and (result["full_cases"],result["distinct_full_maps"])==(684,684)
         and result["new_graph_identities"]==result["solver_queries"]==0
         and set(result["templates"])=={"L","R"}, "validator's complete grid receipt")
    cpu_before = freeze["cpu_seconds"]+result["cpu_seconds"]
    all_maps = set()
    audited = {}
    for name,ranks in templates.items():
        receipt = result["templates"][name]
        log = HERE/f"cases-{name}.jsonl"
        need(hash_file(log)==receipt["log_sha256"] and (receipt["pairs"],receipt["cases"])==(171,342), "raw template binding")
        rows = [json.loads(row) for row in log.read_bytes().splitlines()]
        heads,witnesses,excluded = audit_template(name,rows,names,edges,assigned,pending,ranks,all_maps,started,cpu_before,
                                                  lim["max_cpu_seconds"])
        need(len(heads)==receipt["valid_prefixes"] and [[*item["R"],item["order"]] for item in witnesses]==receipt["witnesses"],
             "template outcomes agree")
        audited[name] = {"valid_prefixes":heads,"duplicate_prefix_count":171-len(heads),"witnesses":witnesses,
                         "extreme_pairs_missing_required_difference":excluded,"pairs_outside_extreme_obstruction":120}
    verdict = "VERIFIED_WITNESS" if any(v["witnesses"] for v in audited.values()) else "EXHAUSTED_RESTRICTED_NEGATIVE"
    need(result["status"]==verdict and len(all_maps)==684,"complete two-template disposition")
    elapsed = process_time()-started
    need(cpu_before+elapsed<=lim["max_cpu_seconds"],"combined CPU cap at completion")
    report = {"status":"PASS","scientific_status":verdict,"target_digest":DIGEST,
              "templates":audited,"full_cases":684,"distinct_full_maps":684,"added_cases":0,
              "added_graph_identities":0,"prefilter_used":False,"solver_queries":0,
              "cpu_seconds":elapsed,"combined_cpu_seconds":cpu_before+elapsed,
              "runtime":{"version":sys.version,"platform":sys.platform},
              "raw_sha256":{p:hash_file(HERE/p) for p in
                            ("freeze.json","controls.json","cases-L.jsonl","cases-R.jsonl","result.json","audit.py")}}
    data = json.dumps(report,indent=2,sort_keys=True).encode()+b"\n"
    sizes = [p.stat().st_size for p in HERE.iterdir() if p.is_file()]+[len(data)]
    need(max(sizes)<=lim["max_record_bytes"] and sum(sizes)<=lim["max_evidence_bytes"],"evidence byte caps")
    with (HERE/"audit_result.json").open("xb") as out:
        out.write(data)
    print(f"PASS: 684 distinct maps across two exact templates. {verdict}.")


if __name__ == "__main__":
    main()
