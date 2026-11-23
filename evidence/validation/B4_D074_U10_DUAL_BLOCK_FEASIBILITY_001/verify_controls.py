"""Verify two retained complete ledgers on their shared archived original."""
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


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    cfg = read(HERE / "config.json")
    parent = git("rev-parse", "HEAD").decode().strip()
    need(parent == cfg["parent"] and sys.version_info[:2] in {(3, 12), (3, 13)}
         and cfg["runtime"] == {"python": sys.version, "platform": sys.platform,
                                "executable_sha256": sha(Path(sys.executable).read_bytes())}, "frozen parent/runtime")
    for ref in cfg["sources"].values():
        path = ref["path"]
        raw = (ROOT / path).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], f"frozen bytes: {path}")
        if "git_sha256" in ref:
            blob = git("show", f"{parent}:{path}")
            need(raw == blob and sha(blob) == ref["git_sha256"], f"parent blob: {path}")

    def archive(k):
        return read(ROOT / cfg["sources"][k]["path"])

    original = archive("original")
    graph, digest = original["graph"], original["graph_digest"]
    need(graph["profile"] == [[2], [2], [2], [2], []]
         and digest == "35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4", "exact original")
    saved = {}
    for name, cert in (("D066", archive("d066_certs")["prefix"]), ("D070", archive("d070_seed"))):
        labels = cert["labels"]
        receipt = verify_certificate(graph, labels, digest)
        payload = {"graph_digest": digest, "labels": sorted(labels.items())}
        ledger = sha(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
        need(receipt["valid"] and receipt == cert["checker"]
             and ledger == cert["ledger_id"] != digest and cert["graph_digest"] == digest, "original-bound control")
        saved[name] = {"checker": receipt, "graph_digest": digest, "ledger_id": ledger}
    seed = archive("d070_seed")
    ref = cfg["sources"]["original"]
    need(seed["original"] == {k: ref[k] for k in ("bytes", "sha256", "path")}
         and saved["D066"]["ledger_id"] != saved["D070"]["ledger_id"], "co-original ledger bindings")
    bad = verify_certificate(graph, seed["labels"], "0" * 64)
    need(not bad["valid"] and bad["errors"] == ["original graph digest mismatch"], "actual digest adverse")
    cpu = process_time() - START
    need(cpu < 30, "producer CPU cap")
    result = {"status": "PASS", "retained": saved, "wrong_digest": {"expected": "0" * 64, "checker": bad},
              "process_cpu_seconds": cpu, "solver_calls": 0, "assignment_nodes": 0, "new_originals": 0}
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000, "output cap")
    with (HERE / "controls.json").open("xb") as out:
        out.write(raw)
    print("PASS: two original-bound controls and one actual wrong-digest rejection")


if __name__ == "__main__":
    main()
