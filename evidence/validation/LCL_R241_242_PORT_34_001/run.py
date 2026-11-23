"""Check the D086 original, one prescribed state and retained controls."""

from time import process_time

START = process_time()

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import perf_counter
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


def ledger_id(digest, labels):
    data = {"graph_digest": digest, "labels": sorted(labels.items())}
    return sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def physical_ports(labels, cut, declared):
    actual = [labels["s:0"], labels["s:1"] - cut]
    if declared != actual:
        raise ValueError("physical offset mismatch")
    return [labels["s:0"], labels["s:1"]]


def witness(original, labels, offsets, cut):
    graph, digest = original["graph"], original["graph_digest"]
    port_labels = physical_ports(labels, cut, offsets)
    assert all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"], checked
    return {"labels": labels, "checker": checked, "graph_digest": digest,
            "ledger_id": ledger_id(digest, labels), "port_labels": port_labels, "cut": cut,
            "physical_ports": ["s:0", "s:1"],
            "witness": graph["spine"],
            "edge_rows": [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]}


def controls(cfg, original, labels):
    base = ROOT / cfg["retained_d082"]
    d084_dir = ROOT / cfg["retained_d084"]
    d085_dir = ROOT / cfg["retained_d085"]
    d084 = read(d084_dir / "result.json")
    d085 = read(d085_dir / "result.json")
    before = [(84, read(base / "strict_original.json"), d084["menu"]["pairs"], 6),
              (85, read(d085_dir / "original.json"), d085["pairs"], 7)]
    positive = []
    for decision, retained, rows, cut in before:
        row, = [row for row in rows if row["pair"] == [3, 4] and row["status"] == "WITNESSED"]
        archived = row["certificate"]
        verified = witness(retained, archived["labels"], [3, 4], cut)
        assert verified == archived
        positive.append({"decision": decision, "pair": [3, 4], "ledger_id": verified["ledger_id"],
                         "checker": verified["checker"]})
    archived = read(base / "audit_result.json")
    assert archived["status"] == "PASS" and archived["visits_certified"] == 2880
    assert archived["positive_certificates"] == 0
    negative = {"pair": [1, 0], "graph_digest": before[0][1]["graph_digest"],
                "historical_visits": 2880, "positive_certificates": 0, "new_replay_visits": 0,
                "historical_receipt_sha256": archived["raw_receipts"]["enumeration.json"]}
    graph, identity = original["graph"], original["graph_digest"]
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]
    try:
        physical_ports(labels, 8, [3, 3])
    except ValueError as error:
        wrong_port = {"valid": False, "reason": str(error), "declared": [3, 3], "actual": [3, 4]}
    else:
        raise AssertionError("False port accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    wrong_diff = verify_certificate(graph, swapped, identity)
    assert not wrong_diff["valid"] and "edge differences repeat" in wrong_diff["errors"]
    return {"retained_positives": positive, "d082_negative": negative,
            "adverse": {"digest": {"expected": "0"*64, "checker": wrong_digest},
                        "port": wrong_port, "difference": {"swap": [u, v], "checker": wrong_diff}}}


def verify_inputs(cfg):
    assert cfg["profile"] == [[2, 4], [2]] and cfg["cut"] == 8 and cfg["pair"] == [3, 4]
    assert cfg["limits"] == {
        "workers": 1, "max_new_original_identities": 1, "offset_states": 1,
        "max_ordered_center_cases": 12, "assignment_visits": 0,
        "recorded_assignment_states": 0, "search_nodes": 0, "solver_calls": 0, "max_ledgers": 1,
        "adverse_checks": 3, "cpu_seconds": 30, "bytes_per_record": 2_000_000, "bytes_total": 8_000_000,
        "official_sequences": 1, "retries": 0, "restarts": 0, "replays": 0, "joins": 0}
    exe = Path(sys.executable)
    assert sys.version_info[:2] in {(3, 12), (3, 13)}
    assert hash_file(exe) == cfg["runtime_sha256"]
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected
    return {"path": exe.relative_to(ROOT).as_posix(), "sha256": hash_file(exe), "version": sys.version}


def main(cfg):
    runtime = verify_inputs(cfg)
    # Save the sole new original before opening its supplied label map.
    graph = build_graph(cfg["profile"])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    supplied = read(HERE / "candidate.json")
    assert supplied["pair"] == cfg["pair"]
    cert = witness(original, supplied["labels"], supplied["pair"], 8)
    state = {"pair": [3, 4], "status": "WITNESSED", "port_labels": [3, 12],
             "graph_digest": original["graph_digest"], "certificate": cert}
    checked_controls = controls(cfg, original, supplied["labels"])
    report = audit.check(ROOT, HERE, cfg, supplied, state, checked_controls)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "state": state,
            "runtime": runtime, "source_hashes": cfg["source_hashes"], "original_sha256": original_hash,
            "graph_digest": original["graph_digest"], "controls": checked_controls, "audit": report}


def write_record(name, value, limits):
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if len(data) > limits["bytes_per_record"]:
        raise RuntimeError("Evidence record exceeds byte limit")
    if len(data) + sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) > limits["bytes_total"]:
        raise RuntimeError("Evidence bundle exceeds byte limit")
    with (HERE / name).open("xb") as stream:
        stream.write(data)
    return sha256(data).hexdigest()


def execute():
    if not __debug__:
        raise RuntimeError("Enabled assertions are required")
    if any((HERE / file).exists() for file in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be empty")
    started = datetime.now(timezone.utc).isoformat()
    wall_start = perf_counter()
    cfg = read(HERE / "config.json")
    limits = cfg["limits"]
    inputs = {name: hash_file(HERE / name) for name in ("run.py", "audit.py", "config.json", "candidate.json")}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": started, "limits": limits, "local_inputs": inputs,
               "counts": {"official_sequences": 1, "workers": 1, "joins": 0,
                          "named_assignment_visits": 0, "recorded_assignment_states": 0, "search_nodes": 0,
                          "solver_calls": 0, "replays": 0, "retries": 0, "restarts": 0}}
    try:
        result = main(cfg)
        if process_time() - START >= limits["cpu_seconds"]:
            raise TimeoutError("Verification process CPU budget reached")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        receipt.update(status="PASS", exit_code=0)
        receipt["counts"].update(offset_states=1, ordered_center_cases=result["audit"]["ordered_center_cases_checked"], new_ledgers=1,
                                 retained_positive_rechecks=2, adverse_checks=3)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["counts"]["new_original_identities"] = int((HERE / "original.json").exists())
    receipt["combined_process_cpu_seconds"] = process_time() - START
    receipt["wall_seconds"] = perf_counter() - wall_start
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
