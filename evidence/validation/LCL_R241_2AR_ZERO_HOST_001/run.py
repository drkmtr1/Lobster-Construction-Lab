"""Produce and verify only the frozen D096 boundary certificate."""

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


def write_record(name, data, limits):
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    if (len(raw) > limits["bytes_per_record"]
            or len(raw) + sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) > limits["bytes_total"]):
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)
    return sha256(raw).hexdigest()


def supplied_labels(a, r):
    if any(type(q) is not int or q < 2 for q in (a, r)):
        raise ValueError("Both quotas must be exact integers at least two")
    labels = {"s:0": 3, "s:1": a+8, "b:0:0": a+5, "b:0:1": a+4, "b:1:0": 0}
    for section, branch, quota, first in ((0, 0, 2, 1), (0, 1, a, 4), (1, 0, 2, a+6)):
        for k in range(quota):
            labels[f"l:{section}:{branch}:{k}"] = first+k
    for k in range(2, r):
        labels[f"l:1:0:{k}"] = a+7+k
    return labels


def require_interface(graph, labels, cut, offsets):
    if graph["spine"] != ["s:0", "s:1"]:
        raise ValueError("wrong original spine")
    if offsets != [labels["s:0"], labels["s:1"]-cut]:
        raise ValueError("physical offset mismatch")
    if labels["b:1:0"] != 0 or ["s:1", "b:1:0"] not in graph["edges"]:
        raise ValueError("the prescribed center is not a zero host adjacent to the spine")
    if any((labels[u] < cut) == (labels[v] < cut) for u, v in graph["edges"]):
        raise ValueError("an original edge fails the alpha cut")


def retained_positive(cfg):
    paths = cfg["retained"]
    report = read(ROOT / paths["d084_result"])
    positive, = [row["certificate"] for row in report["menu"]["pairs"]
                 if row["pair"] == [3, 4] and row["status"] == "WITNESSED"]
    original = read(ROOT / paths["d084_original"])
    assert report["original"] == paths["d084_original"]
    graph, digest = original["graph"], original["graph_digest"]
    labels = positive["labels"]
    assert graph["profile"] == [[2, 2], [2]] and digest == positive["graph_digest"]
    assert positive["cut"] == 6 and positive["physical_ports"] == graph["spine"]
    require_interface(graph, labels, 6, [3, 4])
    check = verify_certificate(graph, labels, digest)
    assert check["valid"] and check == positive["checker"]
    return {"graph_digest": digest, "ledger_id": positive["ledger_id"], "checker": check, "labels": labels}


def adverse_checks(graph, digest, labels):
    bad_digest = verify_certificate(graph, labels, "0"*64)
    assert not bad_digest["valid"] and bad_digest["errors"] == ["original graph digest mismatch"]
    try:
        require_interface(graph, labels, 6, [1, 0])
    except ValueError as exc:
        assert str(exc) == "physical offset mismatch"
        bad_port = {"declared": [1, 0], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("false physical ports were accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    bad_labels = labels | {u: labels[v], v: labels[u]}
    bad_edges = verify_certificate(graph, bad_labels, digest)
    assert not bad_edges["valid"]
    assert bad_edges["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"graph_digest": bad_digest, "physical_offsets": bad_port,
            "label_swap": {"vertices": [u, v], "checker": bad_edges}}


def verify_inputs(cfg):
    assert cfg["boundary"] == [2, 3]
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    preflight = read(HERE / "preflight_receipt.json")
    assert preflight["status"] == "PASS" and preflight["task"] == cfg["task"]
    assert preflight["parent"] == cfg["parent"]
    assert preflight["input_hashes"] == {name: hash_file(HERE / name) for name in cfg["local_inputs"]}
    assert preflight["runtime"]["sha256"] == cfg["runtime_sha256"] == hash_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected, path
    return preflight


def produce(cfg, counts):
    preflight = verify_inputs(cfg)
    a, r = cfg["boundary"]
    graph = build_graph([[2, a], [r]])
    digest = graph_digest(graph)
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": digest}, cfg["limits"])
    original = read(HERE / "original.json")
    counts["new_original_identities"] = 1
    labels = supplied_labels(a, r)
    require_interface(graph, labels, a+4, [3, 4])
    check = verify_certificate(original["graph"], labels, original["graph_digest"])
    assert check["valid"], check
    canonical = json.dumps({"graph_digest": digest, "labels": sorted(labels.items())},
                           sort_keys=True, separators=(",", ":")).encode()
    certificate = {"labels": labels, "cut": a+4, "graph_digest": digest,
                   "ledger_id": sha256(canonical).hexdigest(), "checker": check,
                   "physical_ports": graph["spine"], "offsets": [3, 4],
                   "witness": graph["spine"],
                   "edge_rows": [[u, v, w] for (u, v), w in zip(graph["edges"], check["edge_differences"], strict=True)]}
    positive = retained_positive(cfg)
    counts["retained_positive_rechecks"] = 1
    adverse = adverse_checks(graph, digest, labels)
    counts["adverse_checks"] = 3
    audited = audit.check(ROOT, cfg, original, certificate, positive, adverse)
    counts["new_certificates"] = 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "boundary": cfg["boundary"],
            "runtime": preflight["runtime"], "original_sha256": original_hash, "certificate": certificate,
            "retained_control": positive, "adverse": adverse, "audit": audited}


def execute():
    if not __debug__ or not sys.dont_write_bytecode:
        raise RuntimeError("Use enabled assertions and -B")
    if any((HERE / name).exists() for name in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be vacant")
    cfg = read(HERE / "config.json")
    limits = cfg["limits"]
    counts = {"official_sequences": 1, "workers": 1, "new_original_identities": 0,
              "new_certificates": 0, "retained_positive_rechecks": 0, "adverse_checks": 0,
              "joins": 0, "solver_calls": 0, "assignment_visits": 0, "search_nodes": 0,
              "assignment_states": 0, "retries": 0, "restarts": 0, "historical_replays": 0}
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
