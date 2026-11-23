"""Check the D089 indexed supplier on the bounded original and retained controls."""

from time import process_time

START = process_time()

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
import subprocess
from time import perf_counter
import traceback

from collections import Counter

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
    labels = {"s:0": 4, "s:1": b+10, "b:0:0": b+6, "b:0:1": b+5, "b:1:0": 0}
    for j in range(3):
        labels[f"l:0:0:{j}"] = 1+j
        labels[f"l:1:0:{j}"] = b+7+j
    for j in range(b):
        labels[f"l:0:1:{j}"] = 5+j
    return labels


def controls(cfg, original, labels):
    retained_checks = []
    for key, b, record in (("positive_d087", 5, "regression"), ("positive_d086", 4, "state")):
        folder = ROOT / cfg[key]
        old_graph = read(folder / "original.json")
        report = read(folder / "result.json")
        assert report["status"] == "PASS"
        row = report[record]
        assert row["status"] == "WITNESSED" and row["pair"] == [3, 4]
        archived = row["certificate"]
        verified = witness(old_graph, archived["labels"], [3, 4], b+4)
        assert verified == archived
        retained_checks.append({"b": b, "pair": [3, 4], "graph_digest": verified["graph_digest"],
                                "ledger_id": verified["ledger_id"], "checker": verified["checker"]})

    folder = ROOT / cfg["negative_d088"]
    old_graph = read(folder / "original.json")
    negative = read(folder / "result.json")
    receipt = read(folder / "command_receipt.json")
    assert negative["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert negative["disposition"] == "EXCLUDED"
    assert negative["domain"] == {"min_b": 2, "exact_integer": True, "offsets": [4, 4]}
    assert negative["boundary_graph_digest"] == old_graph["graph_digest"] != original["graph_digest"]
    negative_record = {"domain": negative["domain"], "graph_digest": old_graph["graph_digest"],
                       "receipt_sha256": hash_file(folder / "command_receipt.json"), "new_replay_visits": 0}

    graph, identity = original["graph"], original["graph_digest"]
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]
    try:
        physical_ports(labels, 7, [4, 4])
    except ValueError as error:
        wrong_port = {"valid": False, "reason": str(error), "declared": [4, 4], "actual": [4, 5]}
    else:
        raise AssertionError("False port accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    counts = Counter(abs(swapped[a]-swapped[b]) for a, b in graph["edges"])
    duplicates = {str(weight): times for weight, times in counts.items() if times > 1}
    missing = sorted(set(range(1, len(graph["vertices"]))) - counts.keys())
    assert duplicates == {"3": 2, "6": 2} and missing == [2, 7]
    wrong_diff = verify_certificate(graph, swapped, identity)
    assert not wrong_diff["valid"] and "edge differences repeat" in wrong_diff["errors"]
    return {"retained_positives": retained_checks, "d088_negative": negative_record,
            "adverse": {"digest": {"expected": "0"*64, "checker": wrong_digest},
                        "port": wrong_port, "difference": {"swap": [u, v], "checker": wrong_diff,
                                                          "duplicates": duplicates, "missing": missing}}}


def verify_inputs(cfg):
    assert cfg["domain"] == {"min_b": 2, "exact_integer": True, "offsets": [4, 5]}
    assert cfg["boundary_b"] == 2
    assert cfg["limits"] == {
        "workers": 1, "symbolic_families": 1, "max_new_original_identities": 1,
        "max_new_certificates": 1, "assignment_visits": 0,
        "recorded_assignment_states": 0, "search_nodes": 0, "solver_calls": 0,
        "adverse_checks": 3, "cpu_seconds": 30, "bytes_per_record": 2_000_000, "bytes_total": 8_000_000,
        "official_sequences": 1, "retries": 0, "restarts": 0, "replays": 0, "joins": 0}
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    exe = Path(sys.executable)
    assert sys.version_info[:2] in {(3, 12), (3, 13)}
    assert hash_file(exe) == cfg["runtime_sha256"]
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected
    return {"path": exe.relative_to(ROOT).as_posix(), "sha256": hash_file(exe), "version": sys.version}


def main(cfg):
    runtime = verify_inputs(cfg)
    b = cfg["boundary_b"]
    # Freeze the sole new original before instantiating its indexed labels.
    graph = build_graph([[3, b], [3]])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    labels = formula(b)
    cert = witness(original, labels, [4, 5], b+5)
    boundary = {"b": b, "pair": [4, 5], "status": "WITNESSED", "port_labels": [4, b+10],
                  "graph_digest": original["graph_digest"], "certificate": cert}
    checked_controls = controls(cfg, original, labels)
    report = audit.check(ROOT, HERE, cfg, boundary, checked_controls)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "boundary": boundary, "runtime": runtime, "source_hashes": cfg["source_hashes"],
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
        receipt["counts"].update(symbolic_families=1, new_certificates=1, boundary_b=2,
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
