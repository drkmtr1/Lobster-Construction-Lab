"""Bind the two archived ledgers to their shared original and verify the digest guard."""
from time import process_time

START = process_time()
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.verify import verify_certificate

LIMITS = {"workers": 1, "numeric_triples": 168, "rank_microchecks": 0, "new_originals": 0,
          "cpu_seconds": 30, "record_bytes": 2_000_000, "total_bytes": 8_000_000,
          "queries": 0, "labeling_nodes": 0, "retries": 0}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check_config(cfg):
    head = git("rev-parse", "HEAD").decode().strip()
    require(head == cfg["parent"] and cfg["limits"] == LIMITS and sys.version_info[:2] in {(3, 12), (3, 13)}
            and cfg["runtime"] == {"version": sys.version, "platform": sys.platform,
                                  "executable_sha256": sha(Path(sys.executable).read_bytes())}, "frozen execution")
    for ref in cfg["sources"].values():
        path = ref["path"]
        raw = (ROOT / path).read_bytes()
        require(sha(raw) == ref["sha256"] and len(raw) == ref["bytes"], f"source bytes: {path}")
        if "git_sha256" in ref:
            blob = git("show", f"{head}:{path}")
            require(raw == blob and sha(blob) == ref["git_sha256"], f"Git blob: {path}")


def record(original, cert):
    labels = cert["labels"]
    original_id = original["graph_digest"]
    ledger_payload = {"graph_digest": original_id, "labels": sorted(labels.items())}
    ledger = sha(json.dumps(ledger_payload, sort_keys=True, separators=(",", ":")).encode())
    result = verify_certificate(original["graph"], labels, original_id)
    require(result["valid"] and result == cert["checker"] and original_id == cert["graph_digest"] != ledger
            and ledger == cert["ledger_id"], "complete original-bound archived certificate")
    return {"graph_digest": original_id, "ledger_id": ledger, "checker": result}


def main():
    cfg = read(HERE / "config.json")
    check_config(cfg)
    source = cfg["sources"]

    def archived(name):
        return read(ROOT / source[name]["path"])

    original = archived("seed_original")
    require(original["graph_digest"] == "35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4"
            and original["graph"]["profile"] == [[2], [2], [2], [2], []], "pinned original")
    cert66 = archived("d066_certificates")["prefix"]
    cert70 = archived("d070_seed")
    first, second = record(original, cert66), record(original, cert70)
    require(first["ledger_id"] != second["ledger_id"] and cert70["original"] ==
            {key: source["seed_original"][key] for key in ("path", "bytes", "sha256")}, "co-original ledger custody")
    wrong = verify_certificate(original["graph"], cert70["labels"], "0" * 64)
    require(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "actual digest rejection")
    cpu = process_time() - START
    require(cpu < LIMITS["cpu_seconds"], "producer CPU cap")
    receipt = {"status": "PASS", "d066": first, "d070": second,
               "adverse": {"expected": "0" * 64, "checker": wrong},
               "queries": 0, "labeling_nodes": 0, "new_originals": 0, "process_cpu_seconds": cpu}
    raw = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    require(len(raw) <= LIMITS["record_bytes"] and total + len(raw) <= LIMITS["total_bytes"], "producer byte caps")
    with (HERE / "controls.json").open("xb") as out:
        out.write(raw)
    print("PASS: both co-original identities and one genuine wrong-digest rejection")


if __name__ == "__main__":
    main()
