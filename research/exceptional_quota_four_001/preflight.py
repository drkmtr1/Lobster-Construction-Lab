"""Parse reviewed source and inspect frozen input data. No task modules are imported."""
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
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_QUOTA_FOUR_MATCHED_001_PREP"


def ordinary(path):
    if any(os.path.lexists(item) and (item.is_symlink() or
           getattr(item.lstat(),"st_file_attributes",0)&0x400) for item in (path,*path.parents)):
        raise ValueError("nonordinary preparation path")
    return path


def sha(raw):
    return sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()


def definitions(tree):
    result = []

    def collect(node, scope):
        names = set()
        for child in node.body:
            if isinstance(child,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
                name = child.name
                if name in names:
                    raise ValueError("duplicate lexical task definition: "+scope+name)
                names.add(name)
                result.append(scope+name)
                collect(child,scope+name+".")
    collect(tree,"")
    return result


def corpus():
    root = EVIDENCE/"input"
    index = json.loads((root/"corpus_index.json").read_bytes())
    prefix = json.loads((root/"prefix.json").read_bytes())
    if (prefix["n"],prefix["c"],prefix["actual_cut"],prefix["frontier"],prefix["polarity"])!=(74,36,39,"s:27","maximum"):
        raise ValueError("frozen prefix interface")
    G,L = prefix["graph"],prefix["actual_labels"]
    cut = prefix["actual_cut"]
    edges = G["edges"]
    if (set(L)!=set(G["vertices"]) or sorted(L.values())!=list(range(75))
            or sorted(abs(L[a]-L[b]) for a,b in edges if (L[a]<cut)!=(L[b]<cut))!=list(range(37,75))
            or sorted(abs(L[a]-L[b]) for a,b in edges if (L[a]<cut)==(L[b]<cut))!=list(range(1,37))):
        raise ValueError("parse-only exact prefix inventory")
    expected = []
    for location in range(3):
        for pair in product(range(1,4),repeat=2):
            q = list(pair)
            q.insert(location,4)
            for rs in product(range(1,5),repeat=2):
                T1,T2 = sum(q),sum(rs)
                if not (T1%2 or T2%2) and T1+T2>=12:
                    expected.append(tuple(q)+rs)
    expected.sort()
    rows, digests, counts = [],set(),Counter()
    for path in sorted(root.glob("targets-*.json")):
        records = json.loads(path.read_bytes())
        for item in records:
            entry = {k:v for k,v in item.items() if k!="graph"}
            g = item["graph"]
            payload = {"vertices":sorted(g["vertices"]), "edges":sorted(sorted(edge) for edge in g["edges"]),
                       **{key:g[key] for key in ("roles","profile","spine")}}
            digest = sha(encoded(payload)[:-1])
            if (entry["shard"]!=path.name or digest!=entry["digest"] or digest in digests
                    or g["profile"]!=G["profile"]+entry["suffix"]
                    or entry["suffix"]!=[entry["parameters"][:3],entry["parameters"][3:]+[0]]
                    or (sum(entry["suffix"][0]),sum(entry["suffix"][1]))!=(entry["T1"],entry["T2"])
                    or len(g["edges"])!=74+2*entry["K"] or 2*entry["K"]!=entry["T1"]+entry["T2"]+8
                    or not 10<=entry["K"]<=13):
                raise ValueError("parse-only corpus identity")
            digests.add(digest)
            counts[entry["T1"],entry["T2"]] += 1
            rows.append({**entry,"record_sha256":sha(encoded(item))})
    census = [[counts[T1,T2] for T2 in (2,4,6,8)] for T1 in (6,8,10)]
    if (rows!=index["targets"] or index["count"]!=len(expected) or len(rows)!=99
            or census!=index["census"] or census!=[[0,0,9,3],[0,27,27,9],[3,9,9,3]]
            or [tuple(row["parameters"]) for row in rows]!=expected
            or [row["id"] for row in rows]!=[f"target-{n:03d}" for n in range(1,100)]):
        raise ValueError("parse-only lexical coverage")
    return prefix["digest"], census


def main():
    config = json.loads((KIT/"config.json").read_bytes())
    runtime = config["runtime"]
    base = ordinary(Path(sys._base_executable).absolute())
    runtime_paths = {"base":base,"dll":base.with_name(runtime["dll"]),
                     "venv":ROOT/runtime["venv"],"cfg":ROOT/runtime["cfg"]}
    hashes = {name:sha(ordinary(path).read_bytes()) for name,path in runtime_paths.items()}
    if (platform.python_version()!=config["python_version"] or Path(sys.executable).absolute()!=base
            or hashes!={name:runtime[name+"_sha"] for name in runtime_paths}
            or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode)):
        raise ValueError("preflight runtime/flags")
    if any(os.path.lexists(ordinary(ROOT/config[name])) for name in ("output","approval")):
        raise ValueError("official paths are already occupied")
    if any(p.is_dir() or p.suffix==".pyc" for p in KIT.iterdir()):
        raise ValueError("unexpected task directory or bytecode")
    if any(name.startswith("d161_") for name in sys.modules):
        raise ValueError("task module imported during preflight")
    source_inventory = {path.name:definitions(ast.parse(path.read_bytes(),filename=path.name))
                        for path in sorted(KIT.glob("*.py"))}
    paths = set(KIT.iterdir())|set((EVIDENCE/"input").iterdir())
    paths.update(ROOT/name for name in config["retained_sha256"])
    files = []
    for path in sorted(paths):
        raw = ordinary(path).read_bytes()
        name = path.relative_to(ROOT).as_posix()
        if name in config["retained_sha256"] and sha(raw)!=config["retained_sha256"][name]:
            raise ValueError("retained file drift")
        files.append({"path":name,"sha256":sha(raw),"bytes":len(raw)})
    digest,census = corpus()
    record = {"status":"PASS_PARSE_ONLY","runtime":hashes,"python_version":platform.python_version(),
              "no_task_imports":True,"no_task_bytecode":True,"isolated":True,"no_site":True,
              "approval_vacant":True,"official_outputs_vacant":True,"definitions":source_inventory,
              "files":files,"count":99,"census":census,"prefix_digest":digest}
    with (EVIDENCE/"PREFLIGHT.json").open("xb") as stream:
        stream.write(encoded(record))
    print(json.dumps({"status":record["status"],"bindings":len(files),"targets":99},sort_keys=True))


if __name__ == "__main__":
    main()
