"""Run the single official producer and independent audit sequence."""

from time import monotonic, process_time

START = process_time()

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONFIG_SHA = "39ae1cb803c4f4bf8b3863e59a0d36d4c1e08f4ca8c87e8afefbcb0c8bd1aacc"


def read(name):
    return json.loads((HERE / name).read_bytes())


def main():
    static = {"commands.json", "config.json"}
    if any(p.name not in static for p in HERE.glob("*.json")):
        raise SystemExit("An official output already exists")
    result = {"status": "INCOMPLETE", "workers": 1, "runs": 1, "retries": 0, "stages": []}
    code = 1
    try:
        relative = HERE.relative_to(ROOT).as_posix()
        python = [".venv/Scripts/python.exe", "-B", "-X", "utf8"]
        stages = [python + ["-m", relative.replace("/", ".")+".run"],
                  python + [relative+"/audit.py"]]
        if sha256((HERE/"config.json").read_bytes()).hexdigest() != CONFIG_SHA:
            raise ValueError("frozen config hash")
        if read("commands.json") != {"driver": python+[relative+"/driver.py"], "stages": stages}:
            raise ValueError("command identity")
        for argv in stages:
            utc = datetime.now(timezone.utc).isoformat()
            wall = monotonic()
            completed = subprocess.run(argv, cwd=ROOT, capture_output=True)
            code = completed.returncode
            result["stages"].append({"argv": argv, "utc": utc, "wall_seconds": monotonic()-wall,
                "exit_code": code, "stdout": completed.stdout.decode("utf-8", errors="replace"),
                "stderr": completed.stderr.decode("utf-8", errors="replace")})
            if code:
                break
        else:
            combined = read("audit_result.json")["producer_and_audit_cpu_seconds"] + process_time()-START
            result["combined_process_cpu_seconds"] = combined
            result["status"] = "COMPLETE" if combined <= 30 else "INCOMPLETE"
            code = 0 if combined <= 30 else 1
    except (OSError, ValueError, KeyboardInterrupt) as exc:
        result["interruption"] = str(exc) or type(exc).__name__
        code = 1
    finally:
        raw = (json.dumps(result, sort_keys=True, indent=2)+"\n").encode()
        total = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
        if len(raw) > 2_000_000 or total+len(raw) > 8_000_000:
            raise SystemExit("Receipt byte cap")
        with (HERE/"command_receipts.json").open("xb") as stream:
            stream.write(raw)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
