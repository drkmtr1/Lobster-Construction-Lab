"""Run exactly one official, sequential control and audit invocation."""
from time import monotonic, process_time

START = process_time()
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(name):
    return json.loads((HERE / name).read_bytes())


def main():
    cfg = read("config.json")
    stages = read("commands.json")["stages"]
    outputs = ("controls.json", "audit_result.json", "command_receipts.json")
    if any((HERE / name).exists() for name in outputs):
        raise SystemExit("An official output already exists; no retry")
    expected = [[".venv/Scripts/python.exe", "-B", "-X", "utf8",
                 (HERE / f"{name}.py").relative_to(ROOT).as_posix()] for name in ("verify_controls", "audit")]
    if stages != expected or cfg["setup_process_cpu_seconds"] >= 30:
        raise SystemExit("Frozen invocation or initial CPU budget mismatch")
    receipt = {"status": "INCOMPLETE", "workers": 1, "formal_runs": 1, "retries": 0,
               "setup_process_cpu_seconds": cfg["setup_process_cpu_seconds"], "stages": []}
    code = 1
    try:
        for argv in stages:
            utc = datetime.now(timezone.utc).isoformat()
            start = monotonic()
            proc = subprocess.run(argv, cwd=ROOT, capture_output=True)
            stdout = proc.stdout.decode("utf-8", errors="replace")
            stderr = proc.stderr.decode("utf-8", errors="replace")
            code = proc.returncode
            receipt["stages"].append({"argv": argv, "started_utc": utc, "wall_seconds": monotonic() - start,
                                      "exit_code": code, "stdout": stdout, "stderr": stderr})
            print(stdout, end="")
            print(stderr, end="")
            if code:
                break
        else:
            aggregate = read("audit_result.json")["combined_process_cpu_seconds"] + process_time() - START
            receipt["combined_process_cpu_seconds_with_driver"] = aggregate
            if aggregate < 30:
                receipt["status"] = "PASS"
            else:
                code = 1
    finally:
        raw = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
        total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
        if len(raw) > 2_000_000 or total + len(raw) > 10_000_000:
            raise SystemExit("Receipt byte cap")
        with (HERE / "command_receipts.json").open("xb") as out:
            out.write(raw)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
