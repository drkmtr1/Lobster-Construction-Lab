"""Parse and hash the exact recovery sources without importing either task module."""

import ast
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUTS = ("original.json", "result.json", "command_receipt.json")
FUNCTIONS = {
    "run.py": ("read", "hash_file", "ledger_id", "require_ports", "d090_labels",
               "reverse_section", "source_control", "inventories", "target_certificate",
               "adverse_controls", "verify_inputs", "main", "write_record", "execute"),
    "audit.py": ("load", "digest", "inspect", "match_prior_manifest", "retained_source",
                 "scoped_negatives", "reversal_ledger", "adverse_audit", "check"),
}


def hash_bytes(data):
    return sha256(data).hexdigest()


def verify(config, receipt):
    runtime = Path(sys.executable)
    receipt["runtime"] = {"path": runtime.relative_to(ROOT).as_posix(), "version": sys.version,
                          "sha256": hash_bytes(runtime.read_bytes())}
    if sys.version_info[:2] not in {(3, 12), (3, 13)} or receipt["runtime"]["sha256"] != config["runtime_sha256"]:
        raise ValueError("Project-local runtime identity mismatch")
    for path, expected in config["source_hashes"].items():
        if hash_bytes((ROOT / path).read_bytes()) != expected:
            raise ValueError(f"Retained source identity mismatch: {path}")
    if set(config["preflight_source_hashes"]) != set(FUNCTIONS) | {"preflight.py"}:
        raise ValueError("Unexpected preflight source list")
    if any((HERE / name).exists() for name in OUTPUTS) or (HERE / "__pycache__").exists():
        raise FileExistsError("Recovery output or cache path already exists")
    for name, expected in config["preflight_source_hashes"].items():
        raw = (HERE / name).read_bytes()
        receipt["input_hashes"][name] = hash_bytes(raw)
        if receipt["input_hashes"][name] != expected:
            raise ValueError(f"Recovery source identity mismatch: {name}")
        if name in FUNCTIONS:
            tree = ast.parse(raw, filename=name)
            names = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if Counter(names) != Counter(FUNCTIONS[name]):
                raise ValueError(f"Missing, extra or duplicate top-level functions: {name}")
            receipt["parsed_functions"][name] = names
    if (HERE / "__pycache__").exists():
        raise ValueError("Unexpected bytecode cache")
    receipt["vacant_official_outputs"] = list(OUTPUTS)
    receipt["bytecode_cache_absent"] = True


def main():
    receipt = {"status": "FAIL", "argv": sys.orig_argv, "preflight_invocations": 1,
               "input_hashes": {}, "parsed_functions": {}, "task_module_imports": 0}
    try:
        raw = (HERE / "config.json").read_bytes()
        receipt["input_hashes"]["config.json"] = hash_bytes(raw)
        if len(sys.argv) != 2 or receipt["input_hashes"]["config.json"] != sys.argv[1]:
            raise ValueError("Recovery configuration identity mismatch")
        config = json.loads(raw)
        receipt.update(task=config["task"], parent=config["parent"])
        verify(config, receipt)
        receipt["status"] = "PASS"
    except Exception as error:
        receipt["error"] = f"{type(error).__name__}: {error}"
    with (HERE / "preflight_receipt.json").open("xb") as output:
        output.write((json.dumps(receipt, indent=2, sort_keys=True)+"\n").encode())
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
