"""Parse-only custody verification for the resolved D198 preparation."""

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def identity(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load_object(path):
    return json.loads(path.read_bytes())


def main():
    cpu = time.process_time()
    wall = time.monotonic()
    bindings = load_object(HERE / "SOURCE_BINDINGS.json")
    for name, row in bindings.items():
        raw = (ROOT / name).read_bytes()
        if row["convention"] == "canonical-lf":
            raw = raw.replace(b"\r\n", b"\n")
        elif row["convention"] != "raw":
            raise ValueError(f"Unknown binding convention for {name}")
        if identity(raw) != row["identity"]:
            raise ValueError(f"Frozen source or evidence changed: {name}")

    config = load_object(HERE / "config.json")
    if (config["execution_authorized"] is not False or config["execution_entry"] is not None
            or config["disposition"] != "SYMBOLICALLY_RESOLVED / NO_EXECUTION_NEEDED"
            or any(config["official_limits"].values())):
        raise ValueError("D198 closed state changed")
    vacant = config["required_vacant_paths"]
    if any((ROOT / item).exists() for item in vacant):
        raise ValueError("At least one frozen official output path is occupied")
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise ValueError("Expected isolated, no-site, no-bytecode interpreter")
    if list(HERE.rglob("*.pyc")) or list(HERE.rglob("__pycache__")):
        raise ValueError("Task bytecode exists")

    expected = config["parse_only_entry_definitions"]
    if {p.name for p in HERE.glob("*.py")} != set(expected):
        raise ValueError("Unexpected executable task source")
    static = {}
    for filename, names in expected.items():
        tree = ast.parse((HERE / filename).read_text(encoding="utf-8"), filename=filename)
        types = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        counts = Counter(node.name for node in ast.walk(tree) if isinstance(node, types))
        outer = {node.name for node in tree.body if isinstance(node, types)}
        if any(count != 1 for count in counts.values()) or outer != set(names):
            raise ValueError("Static definition uniqueness failed")
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                root = node.module if isinstance(node, ast.ImportFrom) else node.names[0].name
                if root not in {"ast", "collections", "hashlib", "json", "pathlib", "sys", "time"}:
                    raise ValueError("Unexpected task import")
        static[filename] = sorted(outer)

    objects = {}
    for kind, binding in config["bound_inputs"].items():
        raw = (ROOT / binding["path"]).read_bytes()
        if identity(raw) != {key: binding[key] for key in ("bytes", "sha256")}:
            raise ValueError(f"Input binding differs: {kind}")
        objects[kind] = json.loads(raw)
    records = objects["originals"]["records"]
    if set(records) != {"odd", "even", "relaxed_control", "multi_gap_control"}:
        raise ValueError("Wrong input scope")
    if objects["symbolic_controls"]["main_disposition"] != "SYMBOLIC_POSITIVE_NO_EXECUTION_NEEDED":
        raise ValueError("Wrong symbolic disposition")
    for name, record in records.items():
        if objects["prefixes"]["prefixes"][name]["prefix_digest"] != record["prefix_digest"]:
            raise ValueError("Independent prefix digest mismatch")
        if objects["symbolic_controls"]["controls"][name]["graph_digest"] != record["original_digest"]:
            raise ValueError("Placed control graph digest mismatch")

    runtime = load_object(HERE / "RUNTIME.json")
    if runtime["python_version"] != list(sys.version_info[:3]) or runtime["platform"] != sys.platform:
        raise ValueError("Runtime identity differs")
    binaries = {"launcher": Path(sys.executable), "base_executable": Path(sys._base_executable)}
    if "windows_dll" in runtime["binaries"]:
        version = sys.version_info
        binaries["windows_dll"] = Path(sys.base_prefix) / f"python{version.major}{version.minor}.dll"
    for kind, path in binaries.items():
        if identity(path.read_bytes()) != runtime["binaries"][kind]:
            raise ValueError("Runtime binary identity differs")

    receipt = {
        "status": "PARSE_ONLY_PASS", "source_bindings": len(bindings),
        "raw_bound_inputs": len(objects), "unique_static_entries": static, "vacant_paths": vacant,
        "task_algorithm_imports": 0, "task_bytecode_files": 0, "numerical_labeling_search_nodes": 0,
        "solver_allocation_states": 0, "original_checker_invocations": 0,
        "official_campaign_executions": 0, "historical_replays": 0,
        "process_cpu_seconds": time.process_time() - cpu, "wall_seconds": time.monotonic() - wall,
    }
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
