"""Read-only syntax and input preflight for the exact frozen D102 run."""

import ast
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def check(cfg, receipt):
    outputs = ("original.json", "result.json", "command_receipt.json", "invocation_failure.json", "__pycache__")
    if not sys.dont_write_bytecode or any((HERE / name).exists() for name in outputs):
        raise RuntimeError("Require -B and vacant official output paths")
    runtime = Path(sys.executable)
    digest = sha256(runtime.read_bytes()).hexdigest()
    if sys.version_info[:2] not in {(3, 12), (3, 13)} or digest != cfg["runtime_sha256"]:
        raise ValueError("Project-local Python runtime mismatch")
    receipt["runtime"] = {"path": runtime.relative_to(ROOT).as_posix(), "sha256": digest, "version": sys.version}
    for path, expected in cfg["source_hashes"].items():
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Retained source hash mismatch: {path}")
    for name, expected in cfg["task_source_hashes"].items():
        raw = (HERE / name).read_bytes()
        receipt["input_hashes"][name] = sha256(raw).hexdigest()
        if receipt["input_hashes"][name] != expected:
            raise ValueError(f"Task source hash mismatch: {name}")
        if name in cfg["functions"]:
            tree = ast.parse(raw, filename=name)
            names = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if sorted(names) != sorted(cfg["functions"][name]):
                raise ValueError(f"Missing, unexpected or duplicate functions in {name}")
            receipt["parsed_functions"][name] = names
    if set(receipt["input_hashes"]) != set(cfg["local_inputs"]):
        raise ValueError("Unexpected preflight input set")
    receipt.update(vacant_outputs=list(outputs), source_pins_checked=len(cfg["source_hashes"]))


def main():
    receipt = {"status": "FAIL", "argv": sys.orig_argv, "preflight_invocations": 1,
               "input_hashes": {}, "parsed_functions": {}, "task_module_imports": 0}
    try:
        raw = (HERE / "config.json").read_bytes()
        actual = sha256(raw).hexdigest()
        receipt["input_hashes"]["config.json"] = actual
        if len(sys.argv) != 2 or sys.argv[1] != actual:
            raise ValueError("Frozen configuration hash mismatch")
        cfg = json.loads(raw)
        receipt.update(task=cfg["task"], parent=cfg["parent"])
        check(cfg, receipt)
        receipt["status"] = "PASS"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
    with (HERE / "preflight_receipt.json").open("xb") as stream:
        stream.write((json.dumps(receipt, indent=2, sort_keys=True)+"\n").encode())
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
