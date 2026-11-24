"""Produce the sole D097 boundary original and verify it and two retained controls."""

from time import process_time

START = process_time()

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import traceback

import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def read(path):
    return json.loads(path.read_bytes())


def hash_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, value, limits):
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    if (len(raw) > limits["bytes_per_record"]
            or len(raw) + sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) > limits["bytes_total"]):
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)
    return sha256(raw).hexdigest()


def supply(q, a, r):
    if any(type(n) is not int for n in (q, a, r)) or q < 2 or a < 2 or r < q:
        raise ValueError("Require exact integers q,a >= 2 and r >= q")
    p = q+a+2
    labels = {"s:0": q+1, "s:1": p+q+2, "b:0:0": p+1, "b:0:1": p, "b:1:0": 0}
    for j in range(q):
        labels[f"l:0:0:{j}"] = 1+j
    for j in range(a):
        labels[f"l:0:1:{j}"] = q+2+j
    for k in range(q):
        labels[f"l:1:0:{k}"] = p+2+k
    for k in range(q, r):
        labels[f"l:1:0:{k}"] = p+3+k
    return labels


def require_ports(graph, labels, cut, offsets):
    if graph["spine"] != ["s:0", "s:1"] or ["s:0", "s:1"] not in graph["edges"]:
        raise ValueError("Incorrect physical witnessing path")
    if offsets != [labels["s:0"], labels["s:1"]-cut]:
        raise ValueError("Physical offset mismatch")
    if labels["b:1:0"] != 0 or ["s:1", "b:1:0"] not in graph["edges"]:
        raise ValueError("Incorrect physical zero host")
    if any((labels[u] < cut) == (labels[v] < cut) for u, v in graph["edges"]):
        raise ValueError("An actual edge does not cross the cut")


def retained_checks(cfg):
    checks = {}
    for key, spec in cfg["controls"].items():
        folder = ROOT / spec["folder"]
        original = read(folder / "original.json")
        report = read(folder / "result.json")
        assert report["status"] == "PASS"
        cert = report["boundary"]["certificate"] if key == "D089" else report["certificate"]
        q, a, r = spec["quotas"]
        graph, digest = original["graph"], original["graph_digest"]
        assert cert["graph_digest"] == digest and graph["profile"] == [[q, a], [r]]
        assert cert["labels"] == supply(q, a, r) and cert["cut"] == q+a+2
        require_ports(graph, cert["labels"], cert["cut"], [q+1, q+2])
        checker = verify_certificate(graph, cert["labels"], digest)
        assert checker["valid"] and checker == cert["checker"]
        checks[key] = {"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checker,
                       "quotas": spec["quotas"], "pointwise_label_match": True}
    return checks


def adverse_checks(graph, digest, labels, cut):
    wrong_digest = "0"*64
    rejected_digest = verify_certificate(graph, labels, wrong_digest)
    assert not rejected_digest["valid"] and rejected_digest["errors"] == ["original graph digest mismatch"]
    try:
        require_ports(graph, labels, cut, [5, 5])
    except ValueError as exc:
        assert str(exc) == "Physical offset mismatch"
        rejected_port = {"declared": [5, 5], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("Incorrect port accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    rejected_swap = verify_certificate(graph, swapped, digest)
    assert not rejected_swap["valid"]
    assert rejected_swap["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"graph_identity": {"declared_digest": wrong_digest, "checker": rejected_digest},
            "physical_port": rejected_port, "label_swap": {"vertices": [u, v], "checker": rejected_swap}}


def preflight_binding(cfg):
    assert cfg["boundary"] == [4, 2, 4]
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    preflight = read(HERE / "preflight_receipt.json")
    assert preflight["status"] == "PASS" and preflight["task"] == cfg["task"] and preflight["parent"] == cfg["parent"]
    assert preflight["input_hashes"] == {name: hash_file(HERE / name) for name in cfg["local_inputs"]}
    assert preflight["runtime"]["sha256"] == cfg["runtime_sha256"] == hash_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected, path
    return preflight


def produce(cfg, counts):
    preflight = preflight_binding(cfg)
    q, a, r = cfg["boundary"]
    graph = build_graph([[q, a], [r]])
    digest = graph_digest(graph)
    frozen_hash = write_record("original.json", {"graph": graph, "graph_digest": digest}, cfg["limits"])
    original = read(HERE / "original.json")
    counts["new_original_identities"] = 1
    labels, cut, offsets = supply(q, a, r), q+a+2, [q+1, q+2]
    require_ports(graph, labels, cut, offsets)
    checker = verify_certificate(original["graph"], labels, original["graph_digest"])
    assert checker["valid"], checker
    canonical = json.dumps({"graph_digest": digest, "labels": sorted(labels.items())},
                           sort_keys=True, separators=(",", ":")).encode()
    cert = {"labels": labels, "cut": cut, "offsets": offsets, "graph_digest": digest, "checker": checker,
            "ledger_id": sha256(canonical).hexdigest(), "physical_ports": graph["spine"], "witness": graph["spine"],
            "edge_rows": [[u, v, w] for (u, v), w in zip(graph["edges"], checker["edge_differences"], strict=True)]}
    controls = retained_checks(cfg)
    counts["retained_positive_rechecks"] = len(controls)
    adverse = adverse_checks(graph, digest, labels, cut)
    counts["adverse_checks"] = len(adverse)
    verified = audit.check(ROOT, original, cert, controls, adverse, cfg)
    counts["new_certificates"] = 1
    return {"task": cfg["task"], "parent": cfg["parent"], "boundary": cfg["boundary"],
            "original_sha256": frozen_hash, "runtime": preflight["runtime"], "status": "PASS",
            "certificate": cert, "controls": controls, "adverse": adverse, "audit": verified}


def execute():
    if not __debug__ or not sys.dont_write_bytecode:
        raise RuntimeError("Use enabled assertions and -B")
    if any((HERE / name).exists() for name in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be vacant")
    cfg = read(HERE / "config.json")
    limits = cfg["limits"]
    counts = {"official_sequences": 1, "workers": 1, "new_original_identities": 0, "new_certificates": 0,
              "retained_positive_rechecks": 0, "adverse_checks": 0, "joins": 0, "solver_calls": 0,
              "assignment_visits": 0, "search_nodes": 0, "assignment_states": 0,
              "retries": 0, "restarts": 0, "historical_replays": 0}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits,
               "inputs": {name: hash_file(HERE / name) for name in (*cfg["local_inputs"], "preflight_receipt.json")}}
    try:
        report = produce(cfg, counts)
        if process_time()-START >= limits["process_cpu_seconds"]:
            raise TimeoutError("Process-CPU cap exceeded")
        receipt["result_sha256"] = write_record("result.json", report, limits)
        receipt.update(status="PASS", exit_code=0)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["process_cpu_seconds"] = process_time()-START
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
