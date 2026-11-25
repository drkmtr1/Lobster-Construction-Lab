"""Parse and hash the frozen preparation. No task module is imported."""

import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time


KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_MATCHED_EXTERIOR_TWO_CENTER_001"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def definition_names(tree):
    seen = set()
    definitions = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)

    def walk(node, scope):
        if isinstance(node, definitions):
            name = ".".join((*scope,node.name))
            if name in seen:
                raise ValueError(f"duplicate definition: {name}")
            seen.add(name)
            scope = (*scope,node.name)
        for child in ast.iter_child_nodes(node):
            walk(child, scope)

    walk(tree, ())
    return sorted(seen)


def safe(path):
    for item in reversed((path, *path.parents)):
        if os.path.lexists(item) and (item.is_symlink() or getattr(item.lstat(),"st_file_attributes",0)&0x400):
            raise ValueError("unexpected symlink or reparse point")
    return path


def profile_set():
    """Independent index coverage using fresh-size equations, without building graphs."""
    expected = set()
    for a in range(2,5):
        for dl in (0,1):
            for dr in range(5):
                for K in range(6,11):
                    single = 2*K-4-a-dl-dr
                    if 3 <= single <= 8:
                        expected.add(((a,)+(0,)*dl,(single,)+(0,)*dr))
                    for b in range(1,5):
                        second = 2*K-5-a-dl-dr-b
                        if 1 <= second <= 4:
                            expected.add(((a,)+(0,)*dl,(b,second)+(0,)*dr))
    return expected


def verify_input():
    root = EVIDENCE / "input"
    index = json.loads((root / "corpus_index.json").read_bytes())
    entries = index["targets"]
    seen, digests = set(), set()
    counts = {"1":0,"2":0,"high_value":0}
    last_shard = None
    shard = {}
    order = []
    for number, entry in enumerate(entries,1):
        if entry["target_id"] != f"target-{number:04d}" or entry["shard"] != f"targets-{(number-1)//24:02d}.json":
            raise ValueError("target order/shard index")
        if entry["shard"] != last_shard:
            items = json.loads((root / entry["shard"]).read_bytes())
            if [row["target_id"] for row in items] != [
                row["target_id"] for row in entries[number-1:number+23]]:
                raise ValueError("unindexed or out-of-order shard member")
            shard = {row["target_id"]:row for row in items}
            last_shard = entry["shard"]
        row = shard[entry["target_id"]]
        record = (json.dumps(row,sort_keys=True,separators=(",", ":"),ensure_ascii=False)+"\n").encode()
        if (sha(record) != entry["record_sha256"] or
            {k:v for k,v in row.items() if k != "graph"} != {k:v for k,v in entry.items() if k != "record_sha256"}):
            raise ValueError("corpus record binding")
        left,right = (tuple(x) for x in row["suffix"])
        controls = {((3,0),(3,0)):0, ((4,),(4,)):1, ((3,),(4,0,0,0)):2}
        priority = int(len(left)==1 and sum(x>0 for x in right)==2 and right.count(0)<=2)
        centers = sum(x>0 for x in right)
        control_names = ["common","adverse","separation",None]
        control = controls.get((left,right),3)
        if row["control"] != control_names[control] or bool(priority) != row["high_value"] or centers != row["second_centers"]:
            raise ValueError("corpus role/subdivision/priority binding")
        order.append((control,not priority,-centers,row["suffix"]))
        if (left,right) in seen or row["digest"] in digests:
            raise ValueError("duplicate named original")
        seen.add((left,right))
        digests.add(row["digest"])
        counts[str(centers)] += 1
        counts["high_value"] += priority
    if seen != profile_set() or counts != index["counts"] or order != sorted(order):
        raise ValueError("independent finite domain coverage or declared order")
    got = {f.name for f in root.glob("targets-*.json")}
    if got != {entry["shard"] for entry in entries}:
        raise ValueError("orphaned corpus shard")
    receipt = json.loads((root / "corpus_receipt.json").read_bytes())
    if (receipt["status"] != "CORPUS_ONLY" or receipt["targets"] != len(entries) or receipt["counts"] != counts
        or any(receipt[key] for key in ("arm_dispositions","exterior_nodes","transfer_states","transitions"))):
        raise ValueError("non-preparation activity")
    return counts


def main():
    started = time.process_time()
    initial_modules = set(sys.modules)
    config = json.loads((KIT/"config.json").read_bytes())
    if not (sys.dont_write_bytecode and sys.flags.isolated and sys.flags.no_site):
        raise ValueError("parse-only interpreter flags")
    runtime = config["runtime"]
    base = safe(Path(sys._base_executable).absolute())
    paths = {"base":base, "dll":base.with_name(runtime["dll"]),
             "cfg":ROOT / runtime["cfg"], "venv":ROOT / runtime["venv"]}
    identity = {key:sha(safe(path).read_bytes()) for key,path in paths.items()}
    if (platform.python_version() != config["python_version"] or base.name.casefold() != runtime["base"]
        or Path(sys.executable).resolve() != base.resolve()
        or any(identity[key] != runtime[key+"_sha"] for key in identity)):
        raise ValueError("qualified runtime identity")
    for name in (config["output"],config["approval"]):
        if os.path.lexists(safe(ROOT/name)):
            raise ValueError("official output or execution authority already exists")
    binding_paths = sorted(path for path in KIT.iterdir() if path.is_file())
    binding_paths += sorted((EVIDENCE/"input").iterdir())
    binding_paths.append(EVIDENCE/"RAW_ORIGINAL_CHECK.json")
    raw_check = json.loads((EVIDENCE/"RAW_ORIGINAL_CHECK.json").read_bytes())
    if raw_check["status"] != "PASS_SOURCE_ONLY_ORIGINALS" or raw_check["originals_checked"] != 320:
        raise ValueError("uncached original-source custody")
    binding_paths += [ROOT / "lcl" / name for name in ("__init__.py","model.py","verify.py")]
    files = []
    parsed = {}
    for path in binding_paths:
        raw = safe(path).read_bytes()
        name = path.relative_to(ROOT).as_posix()
        if len(raw) > config["limits"]["record_bytes"]:
            raise ValueError("frozen per-record ceiling")
        files.append({"path":name,"bytes":len(raw),"sha256":sha(raw)})
        if path.suffix == ".py":
            parsed[name] = definition_names(ast.parse(raw,filename=name))
    counts = verify_input()
    expected_parse = json.loads((KIT/"DEFINITIONS.json").read_bytes())
    added = set(sys.modules)-initial_modules
    banned = {"campaign","audit","engine","prepare","check_originals","lcl"}
    if (parsed != expected_parse or
        any(name.split(".")[0] in banned for name in initial_modules|added)):
        raise ValueError("parse inventory or task import")
    for root in (KIT,EVIDENCE):
        if any(f.name == "__pycache__" or f.suffix in (".pyc",".pyo") for f in root.rglob("*")):
            raise ValueError("unexpected bytecode in kit or evidence")
    result = {"status":"PASS_PARSE_ONLY","parsed_definitions":parsed,"files":files,"runtime":identity,
              "python_version":platform.python_version(),"flags":{"isolated":True,"no_site":True,"no_bytecode":True},
              "no_task_imports":True,"official_outputs_vacant":True,"approval_vacant":True,
              "counts":counts,"cpu_seconds_before_receipt":time.process_time()-started}
    payload = (json.dumps(result,sort_keys=True,separators=(",", ":"))+"\n").encode()
    if len(payload) > config["limits"]["record_bytes"]:
        raise ValueError("parse-only receipt size")
    with (EVIDENCE/"PREFLIGHT.json").open("xb") as f:
        f.write(payload)
    print(json.dumps({"status":result["status"],"parsed":len(parsed),"counts":counts}))


if __name__ == "__main__":
    main()
