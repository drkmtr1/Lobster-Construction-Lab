
"""Standalone documentary freeze and parse-only preflight. Imports no task module."""
import argparse
import ast
from collections import Counter
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile


KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
D = ROOT/"evidence/validation"
EVIDENCE = D/"LCL_ORDINARY_SPINE_EXCEPTIONAL_ALTERNATE_EXTERIOR_MATCHED_001_PREP"
D170 = D/"LCL_ORDINARY_SPINE_EXCEPTIONAL_ROLE_MENU_COVERAGE_001"
D171 = D/"LCL_ORDINARY_SPINE_EXCEPTIONAL_P_GROWTH_001"
HISTORY = ROOT/"evidence/runs/d164-exceptional-four-first-001"
EXCLUDED = {(1,1,2,4),(1,1,4,4),(1,2,3,4),(1,3,4,4)}
CONTROL_IDS = ("target-0060","target-0428","target-0057")


def digest(data):
    return sha256(data).hexdigest()


def compact(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()


def read(path):
    return json.loads(path.read_bytes())


def save_once(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode())


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)


def binding(path):
    data = path.read_bytes()
    if path.suffix == ".md":
        data = data.replace(b"\r\n",b"\n")
    return {"bytes":len(data),"sha256":digest(data)}


def exact_runtime(config):
    runtime = config["runtime"]
    exe = ROOT/runtime["venv"]
    base = Path(sys._base_executable).absolute()
    found = {"venv":exe,"cfg":ROOT/runtime["cfg"],"base":base,"dll":base.with_name(runtime["dll"])}
    if (sys.version.split()[0] != runtime["version"] or Path(sys.executable).absolute()!=exe
            or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize)
            or {key:digest(path.read_bytes()) for key,path in found.items()} != runtime["sha256"]):
        raise ValueError("unexpected preparation runtime")
    return {"runtime":runtime,"flags":["-I","-S","-B"]}


def no_execution_paths(config):
    paths = (config["approval"],config["output"],"evidence/runs/d172-exceptional-alternate-exterior-001")
    if any(os.path.lexists(ROOT/p) for p in paths):
        raise ValueError("execution path already exists")
    return list(paths)


def original_digest(graph):
    """Check stored original names and incidences against their physical profile."""
    profile = graph["profile"]
    spine = [f"s:{i}" for i in range(len(profile))]
    edges = [sorted((a,b)) for a,b in zip(spine,spine[1:])]
    expected = {name:{"kind":"spine","section":i} for i,name in enumerate(spine)}
    for i, section in enumerate(profile):
        for j, quota in enumerate(section):
            assert type(quota) is int and quota >= 0
            b = f"b:{i}:{j}"
            expected[b] = {"kind":"branch","section":i,"branch":j}
            edges.append(sorted((spine[i],b)))
            for t in range(quota):
                leaf = f"l:{i}:{j}:{t}"
                expected[leaf] = {"kind":"leaf","section":i,"branch":j,"leaf":t}
                edges.append(sorted((b,leaf)))
    normalized = sorted(edges)
    assert sorted(graph["vertices"]) == sorted(expected) and graph["spine"] == spine
    assert graph["roles"] == expected and sorted(map(sorted,graph["edges"])) == normalized
    assert graph["schema_version"] == 1
    return digest(compact(dict(vertices=sorted(expected),edges=normalized,spine=spine,roles=expected,profile=profile)))


def inputs(config):
    source = ROOT/config["D164_input"]
    path = source/"corpus_index.json"
    raw = path.read_bytes()
    assert digest(raw) == "909a836c19c6bb1b4bb38e14d1d9e84185a492aae2b1d316fc7511a01f282147"
    assert git("hash-object",str(path)).decode().strip() == "2502eb5d902b07c37e5878f782e5b559cdcd9bec"
    index = json.loads(raw)["targets"]
    assert len(index)==2304
    frozen_prefix = source/"prefix.json"
    prefix = read(frozen_prefix)
    historical_prefix = D/"LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_QUOTA_FOUR_MATCHED_001_PREP/input/prefix.json"
    assert frozen_prefix.read_bytes()==historical_prefix.read_bytes()
    assert prefix["digest"]==original_digest(prefix["graph"])
    assert tuple(prefix[k] for k in ("n","c","d","frontier","actual_cut","polarity"))==(74,36,38,"s:27",39,"maximum")
    actual = prefix["actual_labels"]
    assert actual["s:27"]==74 and sorted(actual.values())==list(range(75))
    assert set(actual)==set(prefix["graph"]["vertices"])
    assert prefix["oriented_labels"]=={n:74-value for n,value in actual.items()}
    crossed, same = [], []
    for a,b in prefix["graph"]["edges"]:
        target = crossed if (actual[a]<39)!=(actual[b]<39) else same
        target.append(abs(actual[a]-actual[b]))
    assert sorted(crossed)==prefix["crossing"]==list(range(37,75))
    assert sorted(same)==prefix["noncrossing"]==list(range(1,37))
    return source, index, prefix


def selection(config):
    source,index,prefix = inputs(config)
    rec = read(HISTORY/"RECONCILIATION.json")
    completed = {r["target"] for r in rec["rows"]}
    assert len(completed) == 428 and rec["summary"]["status"] == "INCOMPLETE"
    assert rec["summary"]["finite_hypothesis"] == "UNDECIDED"
    assert rec["summary"]["paired_distribution"] == {"YES/YES":108,"YES/NO":48,"NO/YES":0,"NO/NO":272}
    expected = set()
    for first in product(range(1,5), repeat=4):
        if 4 not in first or sum(first)%2 or tuple(sorted(first)) in EXCLUDED:
            continue
        for p, q in product(range(1,7),repeat=2):
            R = p+q
            if R>=7 and R%2:
                expected.add(first+(p,q))
    selected, shards, identities = [], {}, set()
    counts, totals, orders = Counter(), Counter(), {}
    for entry in index:
        raw = entry["parameters"]
        assert all(type(p) is int for p in raw)
        f, second = raw[:4],raw[4:]
        F,R = sum(f),sum(second)
        if (not all(1<=p<=4 for p in f) or not all(1<=p<=6 for p in second)
                or F%2 or 4 not in f or tuple(sorted(f)) in EXCLUDED or R<7 or not R%2):
            continue
        row = bind_original(source,entry,shards)
        assert entry["id"] not in completed and entry["digest"] not in identities
        assert row["suffix"] == [f,second+[0]]
        assert row["graph"]["profile"] == prefix["graph"]["profile"]+row["suffix"]
        assert row["T1"]==F and row["T2"]==R and 2*row["K"]==F+R+9
        assert 74>=2*row["K"] and len(row["graph"]["edges"])==74+2*row["K"]
        key = tuple(sorted(f))
        counts[key] += 1
        totals[R] += 1
        orders.setdefault(key,set()).add(tuple(f))
        identities.add(entry["digest"])
        selected.append({key:entry[key] for key in ("id","shard","record_sha256","parameters","digest","K","suffix")}
                        | {"F":F,"R":R,"first_inventory":list(key),
                           "M_symbolic":"EVEN_FIRST_MENU_TRANSLATION_PARITY" if all(p%2==0 for p in f) else None})
    assert len(selected)==len(expected)==396 and {tuple(e["parameters"]) for e in selected}==expected
    assert [tuple(e["parameters"]) for e in selected]==sorted(expected)
    assert [e["id"] for e in selected]==sorted(e["id"] for e in selected)
    assert dict(counts)=={(2,2,2,4):48,(2,2,4,4):72,(2,3,3,4):144,(2,4,4,4):48,(3,3,4,4):72,(4,4,4,4):12}
    assert [len(orders[key]) for key in sorted(orders)]==[4,6,12,4,6,1]
    assert dict(totals)=={7:198,9:132,11:66}
    assert sum(e["M_symbolic"] is not None for e in selected)==180
    assert all(e["id"]!="target-0429" for e in selected)
    first,last = selected[0],selected[-1]
    assert (first["id"],first["digest"],first["record_sha256"])==(
        "target-0777","1306312ac9aec8c0daea96865c439e44e0cdb9af0682b7b1cd0878b2ca6814ee",
        "ecc4a03aa64e4aef6d5e0bce4f6a67c010c465dbaa8774c139e8dce91674c6b8")
    assert (last["id"],last["digest"],last["record_sha256"])==(
        "target-2304","40feaa84a25ba358a080bc92a6c4c794937b2731c3bd895188a8d80ca733109c",
        "b87628e8e58151a821f5e650470dd02c889a5a8764a687566f96e1482224ffc1")
    execution = sorted(selected,key=lambda row:(row["M_symbolic"] is None,row["K"],row["id"]))
    return dict(schema_version=1,census=[
        dict(first=list(k),first_orders=len(orders[k]),originals=counts[k]) for k in sorted(counts)],
        totals=dict(totals),expected_symbolic_M=180,mixed_parity=216,historical_completed_pairs=0,
        prefix_digest=prefix["digest"],lexical_order_ids=[r["id"] for r in selected],execution_order=execution)


def bind_original(source, entry, shards):
    file = entry["shard"]
    assert Path(file).name==file and file.startswith("targets-")
    if file not in shards:
        shards[file] = {r["id"]:r for r in read(source/file)}
    row = shards[file][entry["id"]]
    assert {k:v for k,v in row.items() if k!="graph"} == {k:v for k,v in entry.items() if k!="record_sha256"}
    assert digest(compact(row)+b"\n")==entry["record_sha256"]
    assert original_digest(row["graph"])==entry["digest"]
    return row


def historical_controls(config):
    source,index,_ = inputs(config)
    reconcile = read(HISTORY/"RECONCILIATION.json")
    archive = HISTORY/"OFFICIAL_RAW.zip"
    raw = archive.read_bytes()
    assert digest(raw)=="6ecb659aaefc4a574f39d1da8c3bb88b53517ea9381cc25fa332144f822a7c19"
    records = {row["target"]:row for row in reconcile["rows"]}
    coverage = read(D170/"COVERAGE.json")
    rows = {row["target"]:row for row in coverage["verified_records"]}
    pop = {row["target"]:row for row in read(D170/"POPULATION.json")["population"]}
    assert len(rows)==len(pop)==108 and rows.keys()==pop.keys()
    assert all(all(rows[t][k]==value for k,value in r.items()) for t,r in pop.items())
    matches,shards = {},{}
    index_by_name = {r["id"]:r for r in index}
    members = {r["name"]:r for r in reconcile["raw_members"]}
    with zipfile.ZipFile(archive) as stream:
        assert len(stream.namelist())==len(members)==1288 and set(stream.namelist())==set(members)
        assert not any(name.startswith("target-0429") for name in members)
        for target in CONTROL_IDS:
            entry = index_by_name[target]
            original = bind_original(source,entry,shards)
            rec = records[target]
            e_record = {k:rec["arms"]["E+"][k] for k in ("file","bytes","sha256")}
            pair_record = rec["pair"]
            for link in (e_record,pair_record):
                data = stream.read(link["file"])
                assert (len(data),digest(data))==(link["bytes"],link["sha256"])
                assert (link["bytes"],link["sha256"])==(members[link["file"]]["bytes"],members[link["file"]]["sha256"])
            pair = json.loads(stream.read(pair_record["file"]))
            arm = json.loads(stream.read(e_record["file"]))
            assert (arm["target"],arm["digest"]) == (target,entry["digest"])
            assert pair["target"]==target and pair["graph_digest"]==entry["digest"]
            out = dict(original_record=entry,e_plus=e_record,pair=pair_record)
            if target == "target-0057":
                assert coverage["adverse_control"]["e_plus"]==e_record and pair["arms"]["E+"]=="NO"
                assert arm["audit"]["status"]=="PASS_INDEPENDENT_EXHAUSTION"
                assert arm["result"]["counts"]["qualified_exteriors"]==arm["audit"]["counts"]["qualified_exteriors"]==66
                assert arm["result"]["counts"]["qualified_strata"]==arm["audit"]["counts"]["qualified_strata"]
                out.update(expected_M="NO",expected_A="NO",proof="Accepted historical full E+ negative, 66 qualified representatives.")
            else:
                frozen = rows[target]
                assert pop[target]["e_plus"]==e_record and pop[target]["original_record_sha256"]==entry["record_sha256"]
                assert frozen["reduced"]==arm["audit"]["reduced"] and arm["audit"]["original"]==original["graph"]
                assert arm["result"]["claim"]=="YES" and arm["audit"]["status"]=="PASS_INDEPENDENT_RECONSTRUCTION"
                reduced = frozen["reduced"]
                role = frozen["physical_roles"]
                assert {r:reduced[role[r]] for r in role} == dict(v=6,u=7,w=0,b=2,a=3,c1=4,Z=5,Q=8,P=10)
                assert frozen["direct_leaf"] not in reduced and sorted(reduced.values())==list(range(11))
                assert sorted((t["reduced"],t["parent_reduced"],t["parent"]) for t in frozen["terminals"])==[
                    (1,10,role["P"]),(9,3,role["a"])]
                out.update(expected_M="YES",expected_A="UNSPECIFIED",saved_candidate_excluded_from_A=True,
                           reduced=frozen["reduced"],terminals=frozen["terminals"],physical_roles=frozen["physical_roles"],
                           direct_leaf=frozen["direct_leaf"])
            matches[target]=out
    return {"historical":matches,
            "abstract":{"D167_common_hole":"False despite aggregate moments. Retain both zero-flow edges at a common hole.",
                        "D168_unequal_boundaries":"Fold sources and images separately. Test absent cells and zero quotas.",
                        "D168_residue_paths":"Per-residue forced recurrence and far-edge closure. No new allocation or fixture evaluation."},
            "in_domain_verified_A_separator":None}


def retained_custody(config):
    def immutable(path):
        data = path.read_bytes()
        tracked = git("show",config["base"]+":"+path.relative_to(ROOT).as_posix())
        assert data==tracked or (path.suffix==".md" and data.replace(b"\r\n",b"\n")==tracked),path
        return binding(path)

    prior = {}
    states = []
    for root,count,d in ((D171,5,"0b970def909bee1485cb44beea27e52a19a7034308d6cbe86bea1a18b096cff0"),
                         (D170,9,"3331679951fbdf2ad6c19f4385a85a7919a9113983f532b1baa8c4e538914704")):
        mpath = root/"MANIFEST.json"
        bound = immutable(mpath)
        assert bound["sha256"]==d
        prior[mpath.relative_to(ROOT).as_posix()] = bound
        m = read(mpath)
        assert len(m["files"])==count
        for row in m["files"]:
            found = immutable(ROOT/row["path"])
            assert found == {k:row[k] for k in ("sha256","bytes")}
            prior[row["path"]] = found
        states.append(m["state_binding"])
    assert immutable(ROOT/"STATE.md")=={"bytes":states[0]["bytes"],"sha256":states[0]["sha256"]}
    assert states[0]["sha256"]=="979c221bcff89eb2fce01635e59d842ae64f23d8edbf271eace135b91c264a33"
    assert prior[(D170/"COVERAGE.json").relative_to(ROOT).as_posix()]["sha256"]==(
        "ef3036d6d84dad330a369d1f47cb4b5a8bf41e6bcb1258e0b16f3d022b7d1786")
    assert git("rev-parse","HEAD","origin/main").decode().splitlines() == [config["base"]]*2
    assert git("rev-parse","HEAD:lcl/model.py","HEAD:lcl/verify.py").decode().splitlines()==[
        "8d1e9948e8bf5ef01e67c9afe0155412c57d79fa","d008f35f0843e1a5c770db3e7f42ed7d987360d7"]
    assert git("rev-parse","refs/tags/lcl-v0.1.0-baseline","refs/tags/lcl-v0.1.0-baseline^{}").decode().splitlines()==[
        "fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d","36ea1603602491bf3c1c5b81ed4c23aaa2210e70"]
    return {"base":config["base"],"intake_state":states[0],"previous_files":prior,
            "director_scope":"Published refs, identities and frozen index inspection. No Director-side archive decompression, checker replay or local worktree verification.",
            "local_scope":"Read-only refs, worktree, canonical index, retained bytes and selected saved members. No historical checker replay.",
            "baseline_tag":"fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d","baseline_peel":"36ea1603602491bf3c1c5b81ed4c23aaa2210e70",
            "upstream_main":{"MDL":"858a8c1fcfda87ba40bb1adee498a6131504a803",
                             "Bounded Search":"e48b94eec4091b4fe189e325cab2eda464409943"},
            "local_Bounded_Search_recovery_HEAD":"c803ecb6bd0481d31af43f7e3c194ae8ed4d1578",
            "protection":"Direct live refs, with no change to either upstream or to Codex capture refs."}


def definitions(tree):
    kinds = (ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)
    result = []

    def walk(node, prefix, scope):
        if isinstance(node,kinds):
            if node.name in scope:
                raise ValueError("duplicate lexical definition "+prefix+node.name)
            scope.add(node.name)
            name = prefix+node.name
            result.append(name)
            fresh = set()
            for child in node.body:
                walk(child,name+".",fresh)
            return
        for child in ast.iter_child_nodes(node):
            walk(child,prefix,scope)

    walk(tree,"",set())
    return result


def parse_only(config):
    lock=read(EVIDENCE/"BINDINGS.json")
    for name, expected in (lock["source_and_config"]|lock["retained"]).items():
        assert binding(ROOT/name)==expected,name
    assert json.loads(json.dumps(selection(config)))==read(EVIDENCE/"POPULATION.json")
    assert historical_controls(config)==read(EVIDENCE/"CONTROLS.json")
    sources = [ROOT/p for p in lock["parse_sources"]]
    modules = {}
    for p in sources:
        raw = p.read_bytes()
        tree = ast.parse(raw,filename=p.name)
        names = definitions(tree)
        deps = [ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
        assert not any(label.startswith(("from lcl ","import lcl","from research","import research"))
                       for label in deps)
        modules[p.relative_to(ROOT).as_posix()] = {"lexical_definitions":names,"imports":deps}
    entries = modules[(KIT/"campaign.py").relative_to(ROOT).as_posix()]["lexical_definitions"]
    assert {"main","gate","supervise","worker"} <= set(entries)
    assert not any(name.startswith("d172_") for name in sys.modules)
    assert not any((KIT/"__pycache__").glob("*.pyc"))
    return dict(status="PASS_PARSE_ONLY",population=396,task_module_imports=0,numerical_work=0,
                vacant_paths=no_execution_paths(config),runtime=exact_runtime(config),sources=modules,
                binding_sha256=digest((EVIDENCE/"BINDINGS.json").read_bytes()))


def main():
    cpu,wall = time.process_time(),time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase",choices=("freeze","parse-only"))
    args = parser.parse_args()
    config = read(KIT/"config.json")
    exact_runtime(config)
    vacant = no_execution_paths(config)
    if args.phase == "freeze":
        pop = selection(config)
        controls = historical_controls(config)
        custody = retained_custody(config)
        custody["execution_paths_vacant"] = vacant
        EVIDENCE.mkdir(exist_ok=False)
        save_once(EVIDENCE/"POPULATION.json",pop)
        save_once(EVIDENCE/"CONTROLS.json",controls)
        custody["process_cpu_seconds"] = time.process_time()-cpu
        custody["internal_wall_seconds"] = time.perf_counter()-wall
        save_once(EVIDENCE/"CUSTODY.json",custody)
        print(f"Frozen {len(pop['execution_order'])} original bindings and {len(controls['historical'])} historical controls.")
    else:
        preflight = parse_only(config)
        preflight["process_cpu_seconds"] = time.process_time()-cpu
        preflight["internal_wall_seconds"] = time.perf_counter()-wall
        save_once(EVIDENCE/"PREFLIGHT.json",preflight)
        print(f"PASS_PARSE_ONLY: {len(preflight['sources'])} checked sources; no scientific execution.")


if __name__ == "__main__":
    main()
