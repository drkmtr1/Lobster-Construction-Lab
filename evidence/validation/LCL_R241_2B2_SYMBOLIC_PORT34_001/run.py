"""Check the D087 indexed supplier on the bounded original and retained controls."""

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


def formula(b):
    if type(b) is not int or b < 2:
        raise ValueError("b must be an integer at least two")
    labels = {"s:0": 3, "s:1": b+8, "b:0:0": b+5, "b:0:1": b+4, "b:1:0": 0,
              "l:0:0:0": 1, "l:0:0:1": 2, "l:1:0:0": b+6, "l:1:0:1": b+7}
    for j in range(b):
        labels[f"l:0:1:{j}"] = 4+j
    return labels


def controls(cfg, original, labels):
    retained_checks = []
    for b in (2, 3, 4):
        pinned = cfg["retained"][str(b)]
        old_graph = read(ROOT / pinned["original"])
        result = read(ROOT / pinned["result"])
        if b == 2:
            row, = [row for row in result["menu"]["pairs"] if row["pair"] == [3, 4]]
        elif b == 3:
            row, = [row for row in result["pairs"] if row["pair"] == [3, 4]]
        else:
            row = result["state"]
        assert row["status"] == "WITNESSED" and row["pair"] == [3, 4]
        archived = row["certificate"]
        verified = witness(old_graph, archived["labels"], [3, 4], b+4)
        assert verified == archived
        retained_checks.append({"b": b, "pair": [3, 4], "graph_digest": verified["graph_digest"],
                                "ledger_id": verified["ledger_id"], "checker": verified["checker"]})

    negative = read(ROOT / cfg["negative_archive"] / "audit_result.json")
    assert negative["status"] == "PASS" and negative["visits_certified"] == 2880
    assert negative["positive_certificates"] == 0
    negative_record = {"pair": [1, 0], "graph_digest": retained_checks[0]["graph_digest"],
                       "historical_visits": 2880, "positive_certificates": 0, "new_replay_visits": 0,
                       "historical_receipt_sha256": negative["raw_receipts"]["enumeration.json"]}
    graph, identity = original["graph"], original["graph_digest"]
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]
    try:
        physical_ports(labels, 9, [3, 3])
    except ValueError as error:
        wrong_port = {"valid": False, "reason": str(error), "declared": [3, 3], "actual": [3, 4]}
    else:
        raise AssertionError("False port accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    wrong_diff = verify_certificate(graph, swapped, identity)
    assert not wrong_diff["valid"] and "edge differences repeat" in wrong_diff["errors"]
    return {"retained_positives": retained_checks, "d082_negative": negative_record,
            "adverse": {"digest": {"expected": "0"*64, "checker": wrong_digest},
                        "port": wrong_port, "difference": {"swap": [u, v], "checker": wrong_diff}}}


def verify_inputs(cfg):
    assert cfg["domain"] == {"min_b": 2, "exact_integer": True, "offsets": [3, 4]}
    assert cfg["regression_b"] == 5 and set(cfg["retained"]) == {"2", "3", "4"}
    assert cfg["limits"] == {
        "workers": 1, "theorems": 1, "max_new_original_identities": 1,
        "max_new_certificates": 1, "assignment_visits": 0,
        "recorded_assignment_states": 0, "search_nodes": 0, "solver_calls": 0,
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
    b = cfg["regression_b"]
    # Freeze the sole new original before instantiating its indexed labels.
    graph = build_graph([[2, b], [2]])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    labels = formula(b)
    cert = witness(original, labels, [3, 4], b+4)
    regression = {"b": b, "pair": [3, 4], "status": "WITNESSED", "port_labels": [3, b+8],
                  "graph_digest": original["graph_digest"], "certificate": cert}
    checked_controls = controls(cfg, original, labels)
    report = audit.check(ROOT, HERE, cfg, regression, checked_controls)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "regression": regression, "runtime": runtime, "source_hashes": cfg["source_hashes"],
            "original_sha256": original_hash, "graph_digest": original["graph_digest"],
            "controls": checked_controls, "audit": report}


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
    inputs = {name: hash_file(HERE / name) for name in ("run.py", "audit.py", "config.json")}
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
        receipt["counts"].update(theorem_domains=1, new_certificates=1, regression_b=5,
                                 retained_positive_rechecks=3, adverse_checks=3)
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
