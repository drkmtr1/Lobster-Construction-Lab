
"""D174 topology freeze and independent parse-only preflight."""
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
import types
from zipfile import ZipFile


KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
VALID = ROOT/"evidence/validation"
EVIDENCE = VALID/"LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_FIRST_DIRECT_PLACEMENT_MATCHED_001_PREP"
D164 = VALID/"LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_MATCHED_001_PREP/input"
D170 = VALID/"LCL_ORDINARY_SPINE_EXCEPTIONAL_ROLE_MENU_COVERAGE_001"
D172 = ROOT/"evidence/runs/d172-exceptional-alternate-exterior-001"
D172_PREP = VALID/"LCL_ORDINARY_SPINE_EXCEPTIONAL_ALTERNATE_EXTERIOR_MATCHED_001_PREP"
D173 = VALID/"LCL_ORDINARY_SPINE_EXCEPTIONAL_ALTERNATE_EXTERIOR_RESIDUE_GROWTH_001"


def sha(raw):
    return sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()


def read(path):
    return json.loads(path.read_bytes())


def write_once(path, value, compact=False):
    data = canonical(value) if compact else json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False).encode()
    with path.open("xb") as stream:
        stream.write(data+b"\n")


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)


def binding(path):
    raw = path.read_bytes()
    if path.suffix == ".md" or path.name == ".gitattributes":
        raw = raw.replace(b"\r\n",b"\n")
    return {"bytes":len(raw),"sha256":sha(raw)}


def runtime(config):
    keys = config["runtime"]
    base = Path(sys._base_executable).absolute()
    exe = ROOT/keys["venv"]
    files = dict(venv=exe,cfg=ROOT/keys["cfg"],base=base,dll=base.with_name(keys["dll"]))
    assert Path(sys.executable).absolute()==exe and sys.version.split()[0]==keys["version"]
    assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
    assert {role:sha(p.read_bytes()) for role,p in files.items()}==keys["sha256"]
    return {"bound":keys,"flags":["-I","-S","-B"]}


def vacant(config):
    paths = [config["approval"],config["output"],"evidence/runs/d174-exceptional-five-first-direct-001"]
    assert not any(os.path.lexists(ROOT/name) for name in paths)
    return paths


def independent_digest(graph):
    """Rebuild expected named incidence from the stored physical profile."""
    profile = graph["profile"]
    spine = [f"s:{j}" for j in range(len(profile))]
    parents = {node:spine[j-1] for j,node in enumerate(spine) if j}
    roles = {node:{"kind":"spine","section":j} for j,node in enumerate(spine)}
    for j, quotas in enumerate(profile):
        for b, quota in enumerate(quotas):
            assert type(quota) is int and quota>=0
            center = f"b:{j}:{b}"
            parents[center] = spine[j]
            roles[center] = {"kind":"branch","section":j,"branch":b}
            for t in range(quota):
                terminal = f"l:{j}:{b}:{t}"
                parents[terminal] = center
                roles[terminal] = {"kind":"leaf","section":j,"branch":b,"leaf":t}
    edges = sorted(sorted((child,parent)) for child,parent in parents.items())
    payload = dict(vertices=sorted(roles),edges=edges,roles=roles,spine=spine,profile=profile)
    assert graph["schema_version"]==1 and graph["spine"]==spine and graph["roles"]==roles
    assert sorted(graph["vertices"])==payload["vertices"] and sorted(map(sorted,graph["edges"]))==edges
    return sha(canonical(payload))


def prefix_check(config):
    path = ROOT/config["prefix"]
    raw = path.read_bytes()
    assert sha(raw)==config["prefix_sha256"]
    d164 = json.loads(raw)
    assert independent_digest(d164["graph"])==d164["digest"]==config["prefix_digest"]
    assert tuple(d164[k] for k in ("n","c","d","frontier","actual_cut","polarity"))==(74,36,38,"s:27",39,"maximum")
    actual = d164["actual_labels"]
    assert actual["s:27"]==74 and sorted(actual.values())==list(range(75))
    assert set(actual)==set(d164["graph"]["vertices"])
    assert d164["oriented_labels"]=={v:74-x for v,x in actual.items()}
    a,b = [],[]
    for u,v in d164["graph"]["edges"]:
        (a if (actual[u]<39)!=(actual[v]<39) else b).append(abs(actual[u]-actual[v]))
    assert sorted(a)==d164["crossing"]==list(range(37,75))
    assert sorted(b)==d164["noncrossing"]==list(range(1,37))
    return d164


def profiles():
    for first in product(range(1,5),repeat=5):
        if 4 not in first or sum(first)%2:
            continue
        for p,q in product(range(1,7),repeat=2):
            if p+q>=8 and (p+q)%2==0:
                yield [list(first),[p,q,0]]


def expected_parameters():
    # Separate order/count reconstruction via prescribed sums and forced last coordinates.
    first = set()
    for total in range(8,21,2):
        for head in product(range(1,5),repeat=4):
            fifth = total-sum(head)
            if 1<=fifth<=4 and 4 in (*head,fifth):
                first.add((*head,fifth))
    second = {(p,R-p) for R in (8,10,12) for p in range(1,7) if 1<=R-p<=6}
    assert len(first)==391 and len(second)==9
    return sorted(f+q for f in first for q in second)


def metadata(number,suffix,digest,prefix_digest,shard):
    first,second = suffix
    F,R = sum(first),sum(second)
    return dict(id=f"target-{number+1:04d}",shard=shard,suffix=suffix,
                parameters=first+second[:2],F=F,R=R,K=(F+R+10)//2,digest=digest,
                prefix_digest=prefix_digest,quota_four_count=first.count(4),
                all_even=all(p%2==0 for p in first+second[:2]))


def complete_index(entries):
    four = dict(sorted(Counter(e["quota_four_count"] for e in entries).items()))
    totals = dict(sorted(Counter(e["R"] for e in entries).items()))
    assert four=={1:1845,2:1170,3:450,4:45,5:9} and totals=={8:1955,10:1173,12:391}
    assert len(entries)==len({e["digest"] for e in entries})==3519
    first = {tuple(e["suffix"][0]) for e in entries}
    assert Counter(s.count(4) for s in first)=={1:205,2:130,3:50,4:5,5:1}
    assert sum(all(q%2==0 for q in s) for s in first)==31
    assert sum(e["all_even"] for e in entries)==186
    assert min(e["K"] for e in entries)==13 and max(e["K"] for e in entries)==21
    order = sorted(entries,key=lambda e:(not e["all_even"],e["K"],e["id"]))
    return dict(schema_version=1,count=3519,all_even=186,quota_four_counts=four,second_total_counts=totals,
                prefix_digest=entries[0]["prefix_digest"],targets=entries,execution_order=[e["id"] for e in order])


def historical(config):
    population = read(D172_PREP/"POPULATION.json")
    from_d172 = {e["id"]:e for e in population["execution_order"][:2]}
    d170 = {e["target"]:e for e in read(D170/"COVERAGE.json")["verified_records"]}
    d164_index = {e["id"]:e for e in read(D164/"corpus_index.json")["targets"]}
    controls = {}
    archive = ROOT/"evidence/runs/d164-exceptional-four-first-001/OFFICIAL_RAW.zip"
    assert sha(archive.read_bytes())=="6ecb659aaefc4a574f39d1da8c3bb88b53517ea9381cc25fa332144f822a7c19"
    with ZipFile(archive) as stored:
        for name in ("target-0060","target-0428"):
            e=d170[name]
            arm=stored.read(e["e_plus"]["file"])
            assert sha(arm)==e["e_plus"]["sha256"] and len(arm)==e["e_plus"]["bytes"]
            a=json.loads(arm)
            assert a["audit"]["status"]=="PASS_INDEPENDENT_RECONSTRUCTION" and a["result"]["claim"]=="YES"
            assert a["audit"]["exterior_structure"]["h"]==0 and e["direct_leaf"] not in a["audit"]["reduced"]
            assert independent_digest(a["audit"]["original"])==e["digest"]
            controls[name]=dict(H0="YES",H1="UNSPECIFIED",source=e["e_plus"],record_sha256=e["original_record_sha256"])
    d172_hashes = {"target-0777":"0e6bffa8b44b4f64f953f04198705492f839dc722afa29b1a73d526a52574f10",
                   "target-0780":"e1f985993d7550e507b2158ebefb166e2e492de6deabdb91ab2e48ebb080a098"}
    for name,e in from_d172.items():
        a = D172/"raw"/f"{name}-A.json"
        m = D172/"raw"/f"{name}-M.json"
        pair = D172/"raw"/f"{name}-PAIR.json"
        assert sha(a.read_bytes())==d172_hashes[name]
        i=d164_index[name]
        assert (i["digest"],i["record_sha256"])==(e["digest"],e["record_sha256"])
        assert read(m)["result"]["claim"]=="NO" and read(m)["audit"]["status"]=="SYMBOLIC"
        row=read(a)
        if name=="target-0777":
            assert read(pair)["claims"]=={"M":"NO","A":"NO"} and row["audit"]["status"]=="PASS_INDEPENDENT_EXHAUSTION"
            assert row["result"]["counts"]==row["audit"]["counts"]
            assert row["audit"]["counts"]["qualified_exteriors"]==72 and len(row["audit"]["counts"]["qualified_strata"])==6
            h0,h1="NO","NO"
        else:
            assert read(pair)["claims"]=={"M":"NO","A":"YES"}
            assert read(pair)["separator"]["arm_sha256"]==[sha(m.read_bytes()),sha(a.read_bytes())]
            assert row["audit"]["status"]=="PASS_INDEPENDENT_RECONSTRUCTION"
            assert row["audit"]["exterior_structure"]["h"]==1
            assert "b:29:2" in row["audit"]["reduced"] and independent_digest(row["audit"]["original"])==e["digest"]
            h0,h1="UNSPECIFIED","YES"
        controls[name]=dict(H0=h0,H1=h1,record_sha256=e["record_sha256"],
                            files={f.relative_to(ROOT).as_posix():binding(f) for f in (a,m,pair)})
    for name,item in controls.items():
        e=d164_index[name]
        o=next(r for r in read(D164/e["shard"]) if r["id"]==name)
        assert item["record_sha256"]==sha(canonical(o)+b"\n")==e["record_sha256"]
        assert independent_digest(o["graph"])==e["digest"]
        item["graph_digest"]=e["digest"]
        item["shard"]=e["shard"]
    return dict(historical_controls=controls,prefix_digest=config["prefix_digest"],
        symbolic_raw_H0="(7,4), e1=e2=1, direct leaf in gap, constructible reduced exterior only",
        symbolic_raw_H1="(7,5), e1=e2=1, direct leaf exterior, constructible reduced exterior only",
        D167="Common hole forces both adjacent flow bits to zero.",
        D168="Source and image folds have distinct asymmetric ends.",
        D173="The (2,4) ray and pure-P exclusion concern its specified four-first-center geometry.",
        five_first_numerical_oracles=0)


def retained_intake(config):
    roots = ((D173/"MANIFEST.json","3b4c7e33ae3c0c4da836d6411088940d09eee1079049a214a8c82d2c5812c0c6",5),
             (D172/"MANIFEST.json","f93991c329edbd5a6f6759da0042a9f402c772b9b6c0fe8093ec431f906c2990",16),
             (D172_PREP/"MANIFEST.json","2b909a94ae18c338740395f248a60011f1655f385d7f1207bde7a8ce139cb3f6",18))
    inputs = {}
    for path,expected,count in roots:
        assert sha(path.read_bytes())==expected
        inputs[path.relative_to(ROOT).as_posix()] = binding(path)
        m=read(path)
        records=m["files"]
        if isinstance(records,list):
            records={e["path"]:{k:e[k] for k in ("bytes","sha256")} for e in records}
        assert len(records)==count
        for name,record in records.items():
            assert binding(ROOT/name)==record
            inputs[name]=record
    assert inputs["research/ORDINARY_SPINE_EXCEPTIONAL_ALTERNATE_EXTERIOR_RESIDUE_GROWTH.md"]["sha256"]==(
        "6324ce5accb9a06b7774edd56641179c9da8eaff4121656014a0193a4ff11d53")
    d173=read(D173/"MANIFEST.json")
    for e in d173["authoritative_ledger_bindings"]+[d173["state_binding"]]:
        assert binding(ROOT/e["path"])=={k:e[k] for k in ("bytes","sha256")}
    assert binding(ROOT/"STATE.md")["sha256"]=="deeb6508bd1f35c034d892d55ca0623254bbb36a8b3596acc4b1845f10414411"
    base=config["base"]
    assert git("rev-parse","HEAD","origin/main").decode().splitlines()==[base,base]
    assert git("rev-parse","HEAD^").decode().strip()=="2bfcb5008f873cec5c5d2437093b4d3dee7775be"
    assert len(git("diff-tree","--no-commit-id","--name-only","-r",base).splitlines())==11
    assert git("rev-parse","HEAD:lcl/model.py","HEAD:lcl/verify.py").decode().splitlines()==[
        "8d1e9948e8bf5ef01e67c9afe0155412c57d79fa","d008f35f0843e1a5c770db3e7f42ed7d987360d7"]
    assert git("rev-parse","refs/tags/lcl-v0.1.0-baseline","refs/tags/lcl-v0.1.0-baseline^{}").decode().splitlines()==[
        "fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d","36ea1603602491bf3c1c5b81ed4c23aaa2210e70"]
    return dict(base=base,manifested_prior_bindings=inputs,starting_state=binding(ROOT/"STATE.md"),
          director_scope="Published proof, checkpoint and mathematical verification; no Director local Windows inspection or historical replay.",
          local_scope="Read-only refs and frozen evidence identity checks, then topology generation with unchanged builder and independent graph reconstruction.",
          baseline_tag="fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d",baseline_peel="36ea1603602491bf3c1c5b81ed4c23aaa2210e70",
          upstream_MDL_main="858a8c1fcfda87ba40bb1adee498a6131504a803",
          upstream_Bounded_Search_main="e48b94eec4091b4fe189e325cab2eda464409943",
          bounded_search_recovery_HEAD="c803ecb6bd0481d31af43f7e3c194ae8ed4d1578")


def freeze(config):
    prefix=prefix_check(config)
    custody=retained_intake(config)
    controls=historical(config)
    model_path=ROOT/"lcl/model.py"
    model=types.ModuleType("d174_original_builder")
    model.__file__=str(model_path)
    exec(compile(model_path.read_bytes(),model.__file__,"exec"),model.__dict__)
    EVIDENCE.mkdir(exist_ok=False)
    dest=EVIDENCE/"input"
    dest.mkdir()
    entries,shard=[],[]
    allowed=expected_parameters()
    size=config["domain"]["shard_size"]
    for number,suffix in enumerate(profiles()):
        name=f"targets-{number//size:03d}.json"
        graph=model.build_graph(prefix["graph"]["profile"]+suffix)
        digest=independent_digest(graph)
        assert digest==model.graph_digest(graph)
        row=metadata(number,suffix,digest,prefix["digest"],name)|{"graph":graph}
        assert tuple(row["parameters"])==allowed[number] and len(graph["edges"])==74+2*row["K"]
        entries.append({k:v for k,v in row.items() if k!="graph"}|{"record_sha256":sha(canonical(row)+b"\n")})
        shard.append(row)
        if len(shard)==size or number==len(allowed)-1:
            write_once(dest/name,shard,compact=True)
            shard=[]
    index=complete_index(entries)
    write_once(dest/"corpus_index.json",index)
    write_once(EVIDENCE/"CONTROLS.json",controls)
    return custody


def inspect_population(config):
    prefix=prefix_check(config)
    dest=EVIDENCE/"input"
    index=read(dest/"corpus_index.json")
    all_parameters=expected_parameters()
    checked=[]
    for number,path in enumerate(sorted(dest.glob("targets-*.json"))):
        rows=read(path)
        assert path.name==f"targets-{number:03d}.json" and len(rows)==(64 if number<54 else 63)
        for row in rows:
            i=len(checked)
            suffix=row["suffix"]
            first,second=suffix
            assert len(first)==5 and len(second)==3 and second[2]==0
            assert all(type(q) is int and 1<=q<=4 for q in first)
            assert all(type(q) is int and 1<=q<=6 for q in second[:2])
            assert type(second[2]) is int and 4 in first and sum(first)%2==0 and sum(second) in (8,10,12)
            graph=row["graph"]
            assert graph["profile"]==prefix["graph"]["profile"]+suffix
            digest=independent_digest(graph)
            meta=metadata(i,suffix,digest,prefix["digest"],path.name)
            assert {k:v for k,v in row.items() if k!="graph"}==meta
            assert tuple(row["parameters"])==all_parameters[i]
            assert len(graph["edges"])==74+2*row["K"] and 74>=2*row["K"]
            checked.append(meta|{"record_sha256":sha(canonical(row)+b"\n")})
    assert json.loads(json.dumps(complete_index(checked)))==index
    return len(checked)


def ast_definitions(tree):
    kinds=(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)
    found=[]

    def visit(node, prefix, seen):
        if isinstance(node,kinds):
            assert node.name not in seen, prefix+node.name
            seen.add(node.name)
            path=prefix+node.name
            found.append(path)
            nested=set()
            for child in node.body:
                visit(child,path+".",nested)
        else:
            for child in ast.iter_child_nodes(node):
                visit(child,prefix,seen)

    visit(tree,"",set())
    return found


def parse_only(config):
    lock=read(EVIDENCE/"BINDINGS.json")
    for name,want in (lock["new"]|lock["retained"]).items():
        assert binding(ROOT/name)==want,name
    assert historical(config)==read(EVIDENCE/"CONTROLS.json")
    sources={}
    for name in lock["parse_sources"]:
        t=ast.parse((ROOT/name).read_bytes(),filename=name)
        imports=[ast.unparse(n) for n in ast.walk(t) if isinstance(n,(ast.Import,ast.ImportFrom))]
        sources[name]=dict(lexical_definitions=ast_definitions(t),imports=imports)
    names=sources[(KIT/"campaign.py").relative_to(ROOT).as_posix()]["lexical_definitions"]
    assert {"main","gate","supervise","worker"}<=set(names)
    assert not list(KIT.rglob("*.pyc"))
    assert not any(n.startswith("d174_") for n in sys.modules)
    return dict(status="PASS_PARSE_ONLY",population=inspect_population(config),task_module_imports=0,numerical_work=0,
                runtime=runtime(config),vacant_paths=vacant(config),sources=sources,
                bindings_sha256=sha((EVIDENCE/"BINDINGS.json").read_bytes()))


def main():
    cpu,wall=time.process_time(),time.perf_counter()
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=("freeze","parse-only"))
    args=parser.parse_args()
    config=read(KIT/"config.json")
    runtime(config)
    vacant(config)
    if args.mode=="freeze":
        data=freeze(config)
        leaf="CUSTODY.json"
        data["generated_originals"]=3519
        data["numerical_work"]=0
    else:
        data=parse_only(config)
        leaf="PREFLIGHT.json"
    data["process_cpu_seconds"]=time.process_time()-cpu
    data["internal_wall_seconds"]=time.perf_counter()-wall
    write_once(EVIDENCE/leaf,data)
    print(args.mode,data["process_cpu_seconds"],data["internal_wall_seconds"],"no numerical work")


if __name__=="__main__":
    main()
