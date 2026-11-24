"""One parse-only preflight of frozen D125 sources and retained evidence."""

from time import process_time

CPU_START = process_time()

import ast
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def check(cfg, receipt):
    vacant = ("preflight_receipt.json", "result.json", "command_receipt.json",
              "verification_supervision.json", "verification_stderr.txt", "__pycache__")
    assert __debug__ and sys.dont_write_bytecode
    assert all(not (HERE / name).exists() for name in vacant)
    runtime = Path(sys.executable).resolve()
    runtime_path = runtime.relative_to(ROOT).as_posix()
    assert runtime_path == ".venv/Scripts/python.exe" and sys.version_info[:2] in {(3, 12), (3, 13)}
    assert digest(runtime) == cfg["runtime_sha256"]
    receipt["runtime"] = {"path": runtime_path, "version": sys.version, "sha256": digest(runtime)}
    for name, expected in cfg["source_hashes"].items():
        assert digest(ROOT / name) == expected, name
    for name, expected in cfg["task_source_hashes"].items():
        path = HERE / name
        raw = path.read_bytes()
        receipt["input_hashes"][name] = sha256(raw).hexdigest()
        assert receipt["input_hashes"][name] == expected, name
        if name in cfg["functions"]:
            tree = ast.parse(raw, filename=name)
            definitions = sorted(node.name for node in ast.walk(tree)
                                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
            assert definitions == sorted(cfg["functions"][name]), name
            assert len(definitions) == len(set(definitions)), name
            receipt["parsed_functions"][name] = definitions
    assert set(receipt["parsed_functions"]) == set(cfg["functions"])
    assert all(not (HERE / name).exists() for name in ("original.json", "preparation_receipt.json"))
    evidence = cfg["retained_inputs"]
    assert all(cfg["source_hashes"][name] == expected for name, expected in evidence.items())
    receipt["retained_inputs"] = evidence
    assert set(receipt["input_hashes"]) == set(cfg["preflight_inputs"])
    receipt.update(source_pins_checked=len(cfg["source_hashes"]), vacant_outputs=list(vacant))


def main():
    receipt = {"status": "INCOMPLETE", "preflights": 1, "task_module_imports": 0,
               "argv": sys.orig_argv, "input_hashes": {}, "parsed_functions": {}}
    try:
        cfg_path = HERE / "config.json"
        config_hash = digest(cfg_path)
        cfg = json.loads(cfg_path.read_bytes())
        receipt.update(task=cfg["task"], parent=cfg["parent"])
        receipt["input_hashes"]["config.json"] = config_hash
        assert len(sys.argv) == 2 and config_hash == sys.argv[1]
        check(cfg, receipt)
        receipt["status"] = "PASS"
    except (Exception, KeyboardInterrupt) as error:
        receipt["error"] = f"{type(error).__name__}: {error}"
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    with (HERE / "preflight_receipt.json").open("xb") as output:
        output.write((json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode())
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
