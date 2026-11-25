"""Supplemental parse-only inventory of definitions under every lexical suite."""
import ast
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import time

EVIDENCE = Path(__file__).absolute().parent
ROOT = EVIDENCE.parents[2]
KIT = ROOT / "research/exceptional_quota_four_001"


def qualified(tree):
    definitions = (ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)
    names = []

    def descend(node,scope,local):
        if isinstance(node,definitions):
            if node.name in local:
                raise ValueError("duplicate lexical definition: "+scope+node.name)
            local.add(node.name)
            name = scope+node.name
            names.append(name)
            inner = set()
            for entry in node.body:
                descend(entry,name+".",inner)
        else:
            for child in ast.iter_child_nodes(node):
                descend(child,scope,local)

    descend(tree,"",set())
    return names


def main():
    started = time.process_time()
    preflight = json.loads((EVIDENCE/"PREFLIGHT.json").read_bytes())
    config = json.loads((KIT/"config.json").read_bytes())
    prior = {row["path"]:row for row in preflight["files"]}
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise ValueError("supplemental runtime flags")
    if sha256(Path(sys.executable).read_bytes()).hexdigest()!=preflight["runtime"]["base"]:
        raise ValueError("supplemental interpreter drift")
    if any(os.path.lexists(ROOT/config[key]) for key in ("output","approval")):
        raise ValueError("occupied official path")
    definitions = {}
    for path in sorted(KIT.glob("*.py")):
        raw = path.read_bytes()
        binding = prior[path.relative_to(ROOT).as_posix()]
        if len(raw)!=binding["bytes"] or sha256(raw).hexdigest()!=binding["sha256"]:
            raise ValueError("task source moved since preflight")
        definitions[path.name] = qualified(ast.parse(raw,filename=path.name))
        if not set(preflight["definitions"][path.name])<=set(definitions[path.name]):
            raise ValueError("original definition inventory not included")
    if ("candidates.visit" not in definitions["primary.py"] or
            any(name.startswith("d161_") for name in sys.modules) or
            any(KIT.rglob("*.pyc"))):
        raise ValueError("incomplete supplemental definition or isolation check")
    record = {"status":"PASS_PARSE_ONLY_DEEP_DEFINITION_INVENTORY","definitions":definitions,
              "no_task_imports":True,"no_task_bytecode":True,"official_paths_vacant":True,
              "source_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
              "preflight_sha256":sha256((EVIDENCE/"PREFLIGHT.json").read_bytes()).hexdigest(),
              "process_cpu_seconds":time.process_time()-started}
    with (EVIDENCE/"DEFINITION_AUDIT.json").open("xb") as stream:
        stream.write((json.dumps(record,sort_keys=True,indent=2)+"\n").encode())


if __name__=="__main__":
    main()
