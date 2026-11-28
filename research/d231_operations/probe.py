"""Benign stdlib probe, supplied to the intended venv as stdin with -B."""
import ast
import importlib.machinery as machinery
import json
from pathlib import Path
import platform
import sys

root = Path.cwd().resolve()
base = Path(sys.base_prefix).resolve()
venv = (root / ".venv").resolve()
assert sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 13, 17)
assert sys.dont_write_bytecode and platform.machine() == "AMD64"
assert Path(sys.executable).resolve() == venv / "Scripts/python.exe"
assert Path(sys.prefix).resolve() == venv and base != venv
paths = tuple(dict.fromkeys(Path(value or ".").resolve() for value in sys.path))
assert paths[0] == root
assert set(paths) <= {root, base, base / "python313.zip", base / "DLLs", base / "Lib",
                      venv, venv / "Lib/site-packages"}
finder = machinery.PathFinder
for name in ("lcl", "research"):
    found = [spec for path in paths if (spec := finder.find_spec(name, [str(path)]))]
    assert len(found) == 1 and tuple(map(Path, found[0].submodule_search_locations)) == (root / name,)
    assert found[0].origin == (str(root / "lcl/__init__.py") if name == "lcl" else None)

readiness = json.loads((root / "evidence/validation/D231_EXECUTION_ADMISSION_RECOVERY_001/READINESS_OBSERVATIONS.json").read_bytes())
sources = readiness["runtime"]["applicable_module_files"]
standard = set()
packages = {Path(source).parent for source in sources if source.startswith("research/")}
for folder in packages:
    spec = finder.find_spec(folder.name, [str(root / folder.parent)])
    assert spec and spec.origin is None and tuple(map(Path, spec.submodule_search_locations)) == (root / folder,)
for relative in (*sources, "research/d231_operations/observe_v1.py"):
    source = root / relative
    spec = finder.find_spec(source.stem, [str(source.parent)])
    assert spec and Path(spec.origin).resolve() == source, relative
    for suffix in (".pyc", ".pyo"):
        assert not source.with_suffix(suffix).exists(), relative
        assert not tuple((source.parent / "__pycache__").glob(source.stem + ".*" + suffix)), relative
    for node in ast.walk(ast.parse(source.read_bytes())):
        if isinstance(node, ast.Import):
            standard.update(alias.name.partition(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
            standard.add(node.module.partition(".")[0])
assert standard - sys.stdlib_module_names <= {"lcl", "research", "sympy", "z3", "networkx"}
for name in standard & sys.stdlib_module_names:
    assert not finder.find_spec(name, [str(root), str(venv / "Lib/site-packages")]), name
assert not any(name.split(".")[0] in ("lcl", "research", "sitecustomize", "usercustomize") for name in sys.modules)
print(json.dumps({"implementation": sys.implementation.name, "version": sys.version,
                  "executable": sys.executable, "base_executable": sys._base_executable,
                  "prefix": sys.prefix, "base_prefix": sys.base_prefix, "machine": platform.machine(),
                  "bound_source_paths": sources, "startup_paths": sys.path,
                  "stdlib_shadow_checks": len(standard & sys.stdlib_module_names)}))
