"""Run one sequential official verification on an unoccupied evidence path."""

from time import monotonic, process_time

START = process_time()

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
APP = ".venv/Scripts/python.exe"
CONFIG_SHA256 = "bbc12472966059943bca34f09fea6b85734a6571bfbb37dcd07df750555a798c"


def read(name):
    return json.loads((HERE / name).read_bytes())


def main():
    if sha256((HERE / "config.json").read_bytes()).hexdigest() != CONFIG_SHA256:
        raise SystemExit("Configuration identity mismatch")
    relative = HERE.relative_to(ROOT).as_posix()
    python = [APP, "-B", "-X", "utf8"]
    stages = [python + ["-m", relative.replace("/", ".") + ".run"],
              python + [relative + "/audit.py"]]
    commands = read("commands.json")
    if commands != {"driver": python + [relative + "/driver.py"], "stages": stages}:
        raise SystemExit("Command identity mismatch")
    protected = ("identity.json", "adverse.json", "result.json", "audit_result.json", "command_receipts.json")
    if any((HERE / name).exists() for name in protected) or any(HERE.glob("T*.json")):
        raise SystemExit("An official output already exists")
    receipt = {"status": "INCOMPLETE", "workers": 1, "runs": 1, "retries": 0, "stages": []}
    code = 1
    try:
        for argv in stages:
            utc = datetime.now(timezone.utc).isoformat()
            start = monotonic()
            proc = subprocess.run(argv, cwd=ROOT, capture_output=True)
            code = proc.returncode
            receipt["stages"].append({"argv": argv, "started_utc": utc, "wall_seconds": monotonic()-start,
                                      "exit_code": code, "stdout": proc.stdout.decode("utf-8", errors="replace"),
                                      "stderr": proc.stderr.decode("utf-8", errors="replace")})
            if code:
                break
        else:
            total = read("audit_result.json")["producer_and_audit_cpu_seconds"] + process_time()-START
            receipt["combined_process_cpu_seconds"] = total
            if total <= 30:
                receipt["status"] = "PASS"
            else:
                code = 1
    finally:
        raw = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
        existing = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
        if len(raw) > 2_000_000 or existing + len(raw) > 10_000_000:
            raise SystemExit("Evidence byte cap")
        with (HERE / "command_receipts.json").open("xb") as stream:
            stream.write(raw)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
