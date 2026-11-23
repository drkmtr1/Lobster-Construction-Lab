"""Check the D085 original, two prescribed states and retained controls."""

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
    old = ROOT / cfg["retained_d082"]
    retained = read(old / "strict_original.json")
    previous = read(ROOT / cfg["retained_d084"] / "result.json")
    positive = []
    for row in previous["menu"]["pairs"]:
        if row["status"] != "WITNESSED":
            continue
        archived = row["certificate"]
        check = witness(retained, archived["labels"], row["pair"], 6)
        assert check == archived
        positive.append({"pair": row["pair"], "ledger_id": check["ledger_id"], "checker": check["checker"]})
    assert [row["pair"] for row in positive] == [[2, 0], [3, 4]]
    report = read(old / "audit_result.json")
    assert report["status"] == "PASS" and report["visits_certified"] == 2880
    assert report["positive_certificates"] == 0
    negative = {"pair": [1, 0], "graph_digest": retained["graph_digest"], "historical_visits": 2880,
                "positive_certificates": 0, "new_replay_visits": 0,
                "historical_receipt_sha256": report["raw_receipts"]["enumeration.json"]}
    graph, identity = original["graph"], original["graph_digest"]
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]
    try:
        physical_ports(labels, 7, [2, 0])
    except ValueError as error:
        wrong_port = {"valid": False, "reason": str(error), "declared": [2, 0], "actual": [3, 4]}
    else:
        raise AssertionError("False port accepted")
    u, v = "l:0:0:0", "l:0:1:2"
    swapped = labels | {u: labels[v], v: labels[u]}
    wrong_diff = verify_certificate(graph, swapped, identity)
    assert not wrong_diff["valid"] and "edge differences repeat" in wrong_diff["errors"]
    return {"d084_positives": positive, "d082_negative": negative,
            "adverse": {"digest": {"expected": "0"*64, "checker": wrong_digest},
                        "port": wrong_port, "difference": {"swap": [u, v], "checker": wrong_diff}}}


def verify_inputs(cfg):
    assert cfg["profile"] == [[2, 3], [2]] and cfg["cut"] == 7 and cfg["pairs"] == [[2, 0], [3, 4]]
    assert cfg["limits"] == {
        "workers": 1, "max_new_original_identities": 1, "offset_states": 2,
        "max_ordered_center_cases": 24, "assignment_visits": 0,
        "recorded_assignment_states": 0, "search_nodes": 0, "solver_calls": 0, "max_ledgers": 2,
        "adverse_checks": 3, "cpu_seconds": 30, "bytes_per_record": 2_000_000, "bytes_total": 8_000_000,
        "official_sequences": 1, "retries": 0, "replays": 0, "joins": 0}
    exe = Path(sys.executable)
    assert sys.version_info[:2] in {(3, 12), (3, 13)}
    assert hash_file(exe) == cfg["runtime_sha256"]
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected
    return {"path": exe.relative_to(ROOT).as_posix(), "sha256": hash_file(exe), "version": sys.version}


def main(cfg):
    runtime = verify_inputs(cfg)
    # Save the sole new original before passing its ledger to the checker.
    graph = build_graph(cfg["profile"])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    source = read(HERE / "cases.json")
    supplied = source["witness"]
    assert supplied["pair"] == [3, 4]
    cert = witness(original, supplied["labels"], supplied["pair"], 7)
    rows = [{"pair": [2, 0], "port_labels": [2, 7], "status": "EXCLUDED", "proof": "ordered center contradictions",
             "graph_digest": original["graph_digest"]},
            {"pair": [3, 4], "port_labels": [3, 11], "status": "WITNESSED", "proof": "explicit named ledger",
             "graph_digest": original["graph_digest"], "certificate": cert}]
    checked_controls = controls(cfg, original, supplied["labels"])
    report = audit.check(ROOT, HERE, cfg, source, rows, checked_controls)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "pairs": rows,
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
    inputs = {name: hash_file(HERE / name) for name in ("run.py", "audit.py", "config.json", "cases.json")}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": started, "limits": limits, "local_inputs": inputs,
               "counts": {"official_sequences": 1, "workers": 1, "joins": 0,
                          "named_assignment_visits": 0, "recorded_assignment_states": 0, "search_nodes": 0,
                          "solver_calls": 0, "replays": 0, "retries": 0}}
    try:
        result = main(cfg)
        if process_time() - START >= limits["cpu_seconds"]:
            raise TimeoutError("Verification process CPU budget reached")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        receipt.update(status="PASS", exit_code=0)
        receipt["counts"].update(offset_states=2, ordered_center_cases=24, new_ledgers=1,
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
