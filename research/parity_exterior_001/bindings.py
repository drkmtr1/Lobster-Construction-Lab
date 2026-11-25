"""Read-only preparation and worker source bindings."""
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import types

KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_PARITY_COMPATIBLE_TWO_FIRST_CENTER_001"
LEGACY = ROOT / "research/matched_exterior_001"
TASK = "LCL-ORDINARY-SPINE-PARITY-COMPATIBLE-TWO-FIRST-CENTER-001"


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def ordinary(path):
    for entry in reversed((path, *path.parents)):
        if os.path.lexists(entry) and (entry.is_symlink() or getattr(entry.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError(f"nonordinary path: {entry}")
    return path


def write_new(path, value, limit):
    payload = encoded(value)
    if len(payload) > limit:
        raise ValueError(f"record exceeds its bound: {path.name}")
    with ordinary(path).open("xb") as stream:
        stream.write(payload)
    return len(payload)


def load_exact(key, path):
    """Compile raw frozen source, bypassing every existing bytecode cache."""
    if key in sys.modules:
        raise ValueError(f"duplicate runtime module identity: {key}")
    path = ordinary(path)
    module = types.ModuleType(key)
    module.__file__ = str(path)
    sys.modules[key] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def exact_runtime(config, base_process):
    paths = config["runtime"]
    base = ordinary(Path(sys._base_executable).absolute())
    found = {"base": base, "dll": base.with_name(paths["dll"]), "cfg": ROOT / paths["cfg"],
             "venv": ROOT / paths["venv"]}
    hashes = {key: sha(ordinary(file).read_bytes()) for key, file in found.items()}
    expected_executable = base if base_process else found["venv"]
    if (base.name.casefold() != paths["base"].casefold()
            or hashes != {key: paths[key + "_sha"] for key in hashes}
            or ordinary(Path(sys.executable).absolute()) != expected_executable
            or platform.python_version() != config["python_version"]
            or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode)):
        raise ValueError("frozen Python runtime identity or flags")
    return hashes
