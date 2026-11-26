"""Verify frozen inputs and AST entry points without importing task algorithms."""

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _identity(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def _source_tree(path):
    return ast.parse(path.read_text(encoding="utf-8"), filename=path.name)


def main():
    start = time.process_time()
    stop_start = time.monotonic()
    bindings_path = HERE / "SOURCE_BINDINGS.json"
    bindings = json.loads(bindings_path.read_bytes())
    for name, row in bindings.items():
        raw = (ROOT / name).read_bytes()
        if row["convention"] == "canonical-lf":
            raw = raw.replace(b"\r\n", b"\n")
        if _identity(raw) != row["identity"]:
            raise ValueError(f"Source mismatch: {name}")

    config = json.loads((HERE / "config.json").read_bytes())
    if (config["execution_authorized"] is not False or config["execution_entry"] is not None
            or config["disposition"] != "SYMBOLICALLY_RESOLVED / NO_EXECUTION_NEEDED"):
        raise ValueError("Preparation config is not closed")
    vacant = config["required_vacant_paths"]
    if any((ROOT / path).exists() for path in vacant):
        raise ValueError("An execution path is occupied")
    if (HERE / "__pycache__").exists():
        raise ValueError("Task bytecode cache existed before or during parse-only check")
    if not sys.flags.dont_write_bytecode or not sys.flags.isolated or not sys.flags.no_site:
        raise ValueError("Use isolated, no-site, no-bytecode Python")

    overview = {}
    for file, required in config["parse_only_entry_definitions"].items():
        tree = _source_tree(HERE / file)
        types = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        names = Counter(node.name for node in ast.walk(tree) if isinstance(node, types))
        direct = {node.name for node in tree.body if isinstance(node, types)}
        if any(count != 1 for count in names.values()) or not set(required) <= direct:
            raise ValueError(f"Missing or ambiguous entry in {file}")
        if file == "audit.py":
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
            if any("primary" in ast.unparse(node) for node in imports):
                raise ValueError("Independent audit imports the primary")
        overview[file] = sorted(direct)

    for key, row in config["bound_inputs"].items():
        raw = (ROOT / row["path"]).read_bytes()
        if _identity(raw) != {k: row[k] for k in ("bytes", "sha256")}:
            raise ValueError(f"Input mismatch: {key}")
        json.loads(raw)
    runtime = json.loads((HERE / "RUNTIME.json").read_bytes())
    if runtime["python_version"] != list(sys.version_info[:3]):
        raise ValueError("Interpreter version drift")
    binaries = {"launcher": Path(sys.executable), "base_executable": Path(sys._base_executable)}
    if "windows_dll" in runtime["binaries"]:
        dll_name = f"python{sys.version_info.major}{sys.version_info.minor}.dll"
        binaries["windows_dll"] = Path(sys.base_prefix) / dll_name
    for key, path in binaries.items():
        if _identity(path.read_bytes()) != runtime["binaries"][key]:
            raise ValueError(f"Interpreter binary drift: {key}")

    receipt = dict(status="PARSE_ONLY_PASS", parsed_top_level_definitions=overview,
                   source_bindings=len(bindings), bound_inputs=len(config["bound_inputs"]),
                   required_vacant_paths=vacant, algorithm_imports=0, task_bytecode_files=0,
                   original_checker_invocations=0, numerical_labeling_search_nodes=0,
                   solver_allocation_states=0, official_campaigns=0, historical_replays=0,
                   process_cpu_seconds=time.process_time() - start, wall_seconds=time.monotonic() - stop_start)
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
