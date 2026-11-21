"""Create only this project's venv. No system installs or policy changes."""
from pathlib import Path
import subprocess
import sys
import venv

root = Path(__file__).resolve().parents[1]
if sys.version_info[:2] not in ((3, 12), (3, 13)) or sys.maxsize <= 2**32:
    raise SystemExit("Use 64-bit CPython 3.12 or 3.13. Existing compatible Python is sufficient.")
target = root / ".venv"
executable = target / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
if target.exists() and not executable.is_file():
    raise SystemExit("An incomplete .venv exists. Rename it for inspection, then rerun setup.")
if not target.exists():
    venv.EnvBuilder(with_pip=True).create(target)
subprocess.run([str(executable), "-m", "lcl", "doctor"], cwd=root, check=True)
print("Core ready. Next: 01_DEMO.cmd on Windows, or .venv/bin/python -m lcl demo on Linux.")
print("Optional libraries are installed separately; core work needs none.")
