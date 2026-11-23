"""Run the frozen producer and independent audit sequentially, once."""

from time import monotonic, process_time

START = process_time()

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXECUTABLE = ".venv/Scripts/python.exe"


def read(name):
    return json.loads((HERE / name).read_bytes())


def main():
    if not __debug__:
        raise RuntimeError("driver requires assertions")
    outputs = ("prefix_original.json", "k2_original.json", "k5_original.json", "controls.json",
               "config.json", "certificates.json", "run_result.json",
               "audit_result.json", "command_receipts.json")
    if any((HERE / name).exists() for name in outputs):
        raise SystemExit("An official output already exists")
    commands = read("commands.json")
    args = [EXECUTABLE, "-B", "-X", "utf8"]
    relative = HERE.relative_to(ROOT).as_posix()
    expected = [args + ["-m", relative.replace("/", ".") + ".run"],
                args + [relative + "/audit.py"]]
    frozen_sequence = [expected[0] + ["--freeze"], *expected]
    assert [commands["freeze"], *commands["stages"]] == frozen_sequence
    receipt = {"status": "INCOMPLETE", "workers": 1, "formal_runs": 1, "retries": 0,
               "stages": []}
    code = 1
    try:
        for argv in frozen_sequence:
            utc = datetime.now(timezone.utc).isoformat()
            start = monotonic()
            proc = subprocess.run(argv, cwd=ROOT, capture_output=True)
            stage = {"argv": argv, "started_utc": utc, "wall_seconds": monotonic() - start,
                     "exit_code": proc.returncode, "stdout": proc.stdout.decode("utf-8", errors="replace"),
                     "stderr": proc.stderr.decode("utf-8", errors="replace")}
            receipt["stages"].append(stage)
            print(stage["stdout"], end="")
            print(stage["stderr"], end="")
            code = proc.returncode
            if code:
                break
        else:
            elapsed = read("audit_result.json")["combined_process_cpu_seconds"] + process_time() - START
            receipt["combined_process_cpu_seconds_with_driver"] = elapsed
            if elapsed <= 30:
                receipt["status"] = "PASS"
            else:
                code = 1
    finally:
        raw = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
        total = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
        assert len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000
        with (HERE / "command_receipts.json").open("xb") as stream:
            stream.write(raw)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
