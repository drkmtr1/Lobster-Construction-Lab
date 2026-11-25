"""Parse all lexical task definitions and verify frozen input data without task imports."""
import ast
from collections import Counter
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import platform
import sys

KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_MATCHED_001_PREP"


def ordinary(path):
    if any(os.path.lexists(item) and (item.is_symlink() or
           getattr(item.lstat(),"st_file_attributes",0)&0x400) for item in (path,*path.parents)):
        raise ValueError("nonordinary frozen path")
    return path


def sha(raw):
    return sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()


def definitions(tree):
    kinds=(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)
    result = []

    def visit(node,scope,seen):
        if isinstance(node,kinds):
            if node.name in seen:
                raise ValueError("duplicate lexical definition: "+scope+node.name)
            seen.add(node.name)
            name=scope+node.name
            result.append(name)
            inner=set()
            for entry in node.body:
                visit(entry,name+".",inner)
        else:
            for child in ast.iter_child_nodes(node):
                visit(child,scope,seen)
    visit(tree,"",set())
    return result


def expected_parameters():
    firsts = []
    for total in range(4,17,2):
        for head in product(range(1,5),repeat=3):
            final = total-sum(head)
            if 1<=final<=4:
                firsts.append(head+(final,))
    seconds = [(a,total-a) for total in range(3,12,2) for a in range(1,7) if 1<=total-a<=6]
    return sorted(a+b for a in firsts for b in seconds)


def verify_original(graph):
    profile=graph["profile"]
    spine=[f"s:{i}" for i in range(len(profile))]
    parents={node:spine[i-1] for i,node in enumerate(spine) if i}
    roles={node:{"kind":"spine","section":i} for i,node in enumerate(spine)}
    for i,section in enumerate(profile):
        for j,count in enumerate(section):
            host=f"b:{i}:{j}"
            parents[host]=spine[i]
            roles[host]={"kind":"branch","section":i,"branch":j}
            for k in range(count):
                leaf=f"l:{i}:{j}:{k}"
                parents[leaf]=host
                roles[leaf]={"kind":"leaf","section":i,"branch":j,"leaf":k}
    edges=sorted(sorted([node,parent]) for node,parent in parents.items())
    if (graph["schema_version"]!=1 or graph["spine"]!=spine or graph["roles"]!=roles
            or sorted(graph["vertices"])!=sorted(roles)
            or sorted(sorted(edge) for edge in graph["edges"])!=edges):
        raise ValueError("parse-only independently reconstructed original")
    return sha(encoded({"vertices":sorted(roles),"edges":edges,"roles":roles,
                        "spine":spine,"profile":profile})[:-1])


def corpus(config):
    root = EVIDENCE/"input"
    index=json.loads((root/"corpus_index.json").read_bytes())
    raw=(root/"prefix.json").read_bytes()
    prefix=json.loads(raw)
    graph=prefix["graph"]
    labels=prefix["actual_labels"]
    if ((prefix["n"],prefix["c"],prefix["d"],prefix["actual_cut"],prefix["frontier"],prefix["polarity"])!=
            (74,36,38,39,"s:27","maximum") or verify_original(graph)!=prefix["digest"]
            or sha(raw)!=config["retained_sha256"][config["retained_prefix"]]
            or labels["s:27"]!=74 or sorted(labels.values())!=list(range(75))
            or set(labels)!=set(graph["vertices"])):
        raise ValueError("parse-only prefix byte or graph identity")
    crossings,nons=[],[]
    for a,b in graph["edges"]:
        (crossings if (labels[a]<39)!=(labels[b]<39) else nons).append(abs(labels[a]-labels[b]))
    if sorted(crossings)!=list(range(37,75)) or sorted(nons)!=list(range(1,37)):
        raise ValueError("parse-only prefix spectra")
    expected=expected_parameters()
    paths=sorted(root.glob("targets-*.json"))
    if len(paths)!=72 or len(expected)!=2304:
        raise ValueError("target lattice or shard count")
    found,identities,firsts,seconds=[],set(),set(),set()
    strata=Counter()
    for number,path in enumerate(paths):
        records=json.loads(path.read_bytes())
        if path.name!=f"targets-{number:03d}.json" or len(records)!=32:
            raise ValueError("shard order/size")
        for item in records:
            first=tuple(item["parameters"][:4])
            second=tuple(item["parameters"][4:])
            firsts.add(first)
            seconds.add(second)
            T1,T2=sum(first),sum(second)
            K=(T1+T2+9)//2
            gap_T=4 in first and T2>=5
            gap_E=gap_T and T2>=7 and K>=10
            T_basis=None if gap_T else ("T2_3_PHYSICAL_COUNT" if 4 in first else "NO_NEUTRAL_QUOTA_FOUR")
            E_basis=None if gap_E else "RAW_EPLUS_K_LT_10" if K<10 else T_basis or "T2_5_NO_EXTERIOR_TERMINALS"
            target=item["graph"]
            digest=verify_original(target)
            suffix=[list(first),list(second)+[0]]
            if (item["id"]!=f"target-{len(found)+1:04d}" or tuple(item["parameters"])!=expected[len(found)]
                    or item["suffix"]!=suffix or target["profile"]!=graph["profile"]+suffix
                    or item["digest"]!=digest or digest in identities or len(target["edges"])!=74+2*K
                    or (item["K"],item["T1"],item["T2"])!=(K,T1,T2) or not 8<=K<=18
                    or item["quota_four_count"]!=first.count(4)
                    or item["quota_parities"]!=[q%2 for q in first+second]
                    or item["raw_exterior"]!={"T":"PRESENT","E+":"PRESENT" if K>=10 else "ABSENT"}
                    or item["symbolic_basis"]!={"T":T_basis,"E+":E_basis} or K<10 and gap_T):
                raise ValueError("frozen original, policy or lexical binding")
            identities.add(digest)
            entry={key:value for key,value in item.items() if key!="graph"}
            if entry["shard"]!=path.name:
                raise ValueError("record shard name")
            found.append({**entry,"record_sha256":sha(encoded(item))})
            strata["both_excluded"] += not gap_T and not gap_E
            strata["additional_Eplus_excluded"] += gap_T and not gap_E
            strata["eligible_separation"] += gap_T and gap_E
            strata["remaining_T"] += gap_T
            strata["remaining_Eplus"] += gap_E
            strata["symbolic_arm_dispositions"] += (not gap_T)+(not gap_E)
            strata["raw_Eplus_absent"] += K<10
    fc=[sum(a.count(4)==j for a in firsts) for j in range(5)]
    sc=[sum(sum(b)==j for b in seconds) for j in (3,5,7,9,11)]
    if (found!=index["targets"] or index["count"]!=2304 or fc!=[41,52,30,4,1]
            or sc!=[2,4,6,4,2] or fc!=index["first_by_quota_four"] or sc!=index["second_by_total"]
            or strata!=index["symbolic_strata"]):
        raise ValueError("full corpus index or census")
    return prefix["digest"],fc,sc,strata


def main():
    config=json.loads((KIT/"config.json").read_bytes())
    rt=config["runtime"]
    base=ordinary(Path(sys._base_executable).absolute())
    actual={"base":base,"dll":base.with_name(rt["dll"]),"venv":ROOT/rt["venv"],"cfg":ROOT/rt["cfg"]}
    hashes={name:sha(ordinary(path).read_bytes()) for name,path in actual.items()}
    if (platform.python_version()!=config["python_version"] or Path(sys.executable).absolute()!=base
            or hashes!={name:rt[name+"_sha"] for name in actual}
            or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode)):
        raise ValueError("frozen runtime or isolation flags")
    if any(os.path.lexists(ordinary(ROOT/config[k])) for k in ("output","approval")):
        raise ValueError("official paths occupied")
    if any(p.is_dir() or p.suffix==".pyc" for p in KIT.iterdir()) or any(
            name.startswith("d164_") for name in sys.modules):
        raise ValueError("unexpected bytecode or imported task module")
    inventory={path.name:definitions(ast.parse(path.read_bytes(),filename=path.name))
               for path in sorted(KIT.glob("*.py"))}
    if "candidates.visit" not in inventory["primary.py"] or "raw_allocation.descend" not in inventory["audit.py"]:
        raise ValueError("missing nested definitions")
    paths=set(KIT.iterdir())|set((EVIDENCE/"input").iterdir())
    paths.update(ROOT/name for name in config["retained_sha256"])
    files=[]
    for path in sorted(paths):
        raw=ordinary(path).read_bytes()
        name=path.relative_to(ROOT).as_posix()
        if name in config["retained_sha256"] and sha(raw)!=config["retained_sha256"][name]:
            raise ValueError("retained source drift")
        files.append({"path":name,"sha256":sha(raw),"bytes":len(raw)})
    digest,fc,sc,strata=corpus(config)
    receipt={"status":"PASS_PARSE_ONLY","runtime":hashes,"python_version":platform.python_version(),
             "no_task_imports":True,"no_task_bytecode":True,"isolated":True,"no_site":True,
             "approval_vacant":True,"official_outputs_vacant":True,"definitions":inventory,
             "definition_count":sum(map(len,inventory.values())),"files":files,"count":2304,"shards":72,
             "prefix_digest":digest,"first_by_quota_four":fc,"second_by_total":sc,"symbolic_strata":strata}
    with (EVIDENCE/"PREFLIGHT.json").open("xb") as stream:
        stream.write(encoded(receipt))
    print(json.dumps({"status":receipt["status"],"targets":2304,"bindings":len(files),
                      "definitions":receipt["definition_count"]},sort_keys=True))


if __name__=="__main__":
    main()
