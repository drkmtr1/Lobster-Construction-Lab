"""Parse and bind frozen inputs. No task module is imported or executed."""
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
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_PARITY_COMPATIBLE_TWO_FIRST_CENTER_001"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path):
    for entry in reversed((path, *path.parents)):
        if os.path.lexists(entry) and (entry.is_symlink() or getattr(entry.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError("nonordinary parse or output binding")
    return path


def definitions(tree):
    names = set()

    def walk(node, scope):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            scope = (*scope, node.name)
            name = ".".join(scope)
            if name in names:
                raise ValueError(f"duplicate qualified definition: {name}")
            names.add(name)
        for child in ast.iter_child_nodes(node):
            walk(child, scope)

    walk(tree, ())
    return sorted(names)


def check_corpus(config, root):
    raw_index = json.loads((root/"corpus_index.json").read_bytes())
    rows = raw_index["targets"]
    receipt = json.loads((root/"corpus_receipt.json").read_bytes())
    prefix = json.loads((root/"prefix.json").read_bytes())
    if (raw_index["count"] != 256 or len(rows) != 256 or prefix["n"] != 54
            or sha((root/"prefix.json").read_bytes()) != config["retained_sha256"][config["retained_prefix"]]
            or receipt["status"] != "FROZEN_UNLABELED_CORPUS_ONLY" or receipt["originals_checked"] != 256
            or receipt["config_sha256"] != sha((KIT/"config.json").read_bytes())
            or any(receipt[k] for k in ("new_target_labelings", "exterior_nodes", "transfer_states",
                                        "transitions", "dispositions", "solver_calls"))):
        raise ValueError("unlabeled corpus receipt or retained prefix")
    paths = {"corpus_index.json", "corpus_receipt.json", "prefix.json"}
    seen = set()
    for start in range(0, len(rows), 16):
        name = f"targets-{start//16:02d}.json"
        paths.add(name)
        records = json.loads(ordinary(root/name).read_bytes())
        if len(records) != 16:
            raise ValueError("shard size")
        for offset, item in enumerate(records):
            index = start+offset
            entry = rows[index]
            r, t, p, q = (1+(index//place)%4 for place in (64, 16, 4, 1))
            suffix = [[2*r, 2*t], [2*p, 2*q+1, 0]]
            raw = (json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False)+"\n").encode()
            if (item["target_id"] != f"target-{index+1:04d}" or item["shard"] != name
                    or item["param"] != [r, t, p, q] or item["suffix"] != suffix
                    or item["graph"]["profile"] != prefix["graph"]["profile"]+suffix
                    or item["fresh"] != 2*(r+t+p+q+4) or item["digest"] in seen
                    or len(item["graph"]["edges"]) != prefix["n"]+item["fresh"] or item["fresh"] > prefix["n"]
                    or {k:v for k,v in item.items() if k != "graph"} !=
                       {k:v for k,v in entry.items() if k != "record_sha256"}
                    or sha(raw) != entry["record_sha256"]):
                raise ValueError(f"exact ordered original binding: {index}")
            seen.add(item["digest"])
    if {path.name for path in root.iterdir()} != paths:
        raise ValueError("orphan corpus member")
    return 256


def main():
    started = time.process_time()
    initial = set(sys.modules)
    config = json.loads((KIT/"config.json").read_bytes())
    rt = config["runtime"]
    base = ordinary(Path(sys._base_executable).absolute())
    paths = {"base":base, "dll":base.with_name(rt["dll"]), "venv":ROOT/rt["venv"], "cfg":ROOT/rt["cfg"]}
    runtime = {key:sha(ordinary(path).read_bytes()) for key,path in paths.items()}
    if (runtime != {key:rt[key+"_sha"] for key in runtime} or platform.python_version() != config["python_version"]
            or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode)
            or Path(sys.executable).absolute() != base or base.name.casefold() != rt["base"].casefold()):
        raise ValueError("preflight runtime or flags")
    for field in ("output", "approval"):
        if os.path.lexists(ordinary(ROOT/config[field])):
            raise ValueError("official path is occupied")
    if any(not path.is_file() for path in KIT.iterdir()):
        raise ValueError("unexpected kit subdirectory")
    root = EVIDENCE/"input"
    count = check_corpus(config, root)
    bindings = sorted(KIT.iterdir()) + sorted(root.iterdir()) + [ROOT/name for name in config["retained_sha256"]]
    files, observed = [], {}
    for path in bindings:
        raw = ordinary(path).read_bytes()
        name = path.relative_to(ROOT).as_posix()
        if len(raw) > config["limits"]["record_bytes"] or (name in config["retained_sha256"]
                and sha(raw) != config["retained_sha256"][name]):
            raise ValueError(f"record bound/identity drift: {name}")
        files.append({"path":name, "bytes":len(raw), "sha256":sha(raw)})
        if path.suffix == ".py":
            observed[name] = definitions(ast.parse(raw, filename=name))
    if observed != json.loads((KIT/"DEFINITIONS.json").read_bytes()):
        raise ValueError("reviewed definition inventory mismatch")
    prohibited = {"lcl", "d154", "generator", "bindings", "independent", "campaign", "audit", "engine"}
    if any(name.split(".")[0] in prohibited or name.startswith("d154_") for name in initial|set(sys.modules)):
        raise ValueError("preflight task import")
    for directory in (KIT, EVIDENCE):
        if any(path.name == "__pycache__" or path.suffix in (".pyc", ".pyo") for path in directory.rglob("*")):
            raise ValueError("unexpected bytecode emitted")
    receipt = {"status":"PASS_PARSE_ONLY", "files":files, "definitions":observed, "runtime":runtime,
               "python_version":platform.python_version(), "flags":{"isolated":True,"no_site":True,"no_bytecode":True},
               "count":count, "no_task_imports":True, "no_task_bytecode":True,
               "official_outputs_vacant":True, "approval_vacant":True,
               "cpu_seconds":time.process_time()-started}
    payload = (json.dumps(receipt, sort_keys=True, separators=(",", ":"))+"\n").encode()
    if len(payload) > config["limits"]["record_bytes"]:
        raise ValueError("preflight record cap")
    with ordinary(EVIDENCE/"PREFLIGHT.json").open("xb") as stream:
        stream.write(payload)
    print(json.dumps({"status":receipt["status"], "count":count, "cpu_seconds":receipt["cpu_seconds"]}))


if __name__ == "__main__":
    main()
