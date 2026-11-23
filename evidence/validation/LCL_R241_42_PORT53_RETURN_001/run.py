"""Check the D091 original, retained certificate and adverse controls."""

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


def require_ports(original, labels, port_names, cut, offsets):
    spine = original["graph"]["spine"]
    if port_names != [spine[0], spine[-1]]:
        raise ValueError("physical endpoint names mismatch")
    actual = [labels[port_names[0]], labels[port_names[1]]-cut]
    if offsets != actual:
        raise ValueError("physical offset mismatch")
    return actual


def controls(cfg):
    folder = ROOT / cfg["control_d090"]
    original = read(folder / "original.json")
    report = read(folder / "result.json")
    receipt = read(folder / "command_receipt.json")
    cert = report["certificate"]
    labels, graph, identity = cert["labels"], original["graph"], original["graph_digest"]
    assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert receipt["result_sha256"] == hash_file(folder / "result.json")
    assert report["boundary"] == [2, 2] and graph["profile"] == [[2, 2], [2], [3, 2], [3]]
    checked = verify_certificate(graph, labels, identity)
    assert checked["valid"] and checked == cert["checker"]
    assert cert["graph_digest"] == identity
    assert cert["ledger_id"] == ledger_id(identity, labels)
    assert cert["cut"] == 13 and cert["offsets"] == [3, 5]
    require_ports(original, labels, cert["ports"], cert["cut"], cert["offsets"])

    wrong_digest = "0"*64
    rejected_digest = verify_certificate(graph, labels, wrong_digest)
    assert not rejected_digest["valid"] and rejected_digest["errors"] == ["original graph digest mismatch"]
    declared = [3, 4]
    try:
        require_ports(original, labels, cert["ports"], cert["cut"], declared)
    except ValueError as exc:
        assert str(exc) == "physical offset mismatch"
        rejected_port = {"ports": cert["ports"], "cut": cert["cut"], "declared": declared,
                         "actual": cert["offsets"], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("false physical offset accepted")

    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    differences = Counter(abs(swapped[x]-swapped[y]) for x, y in graph["edges"])
    repeated = {str(w): count for w, count in differences.items() if count > 1}
    missing = sorted(set(range(1, len(graph["vertices"]))) - differences.keys())
    assert repeated == {"16": 2, "18": 2} and missing == [15, 19]
    rejected_swap = verify_certificate(graph, swapped, identity)
    assert not rejected_swap["valid"] and "edge differences repeat" in rejected_swap["errors"]
    return {"D090": {"graph_digest": identity, "ledger_id": cert["ledger_id"], "checker": checked},
            "adverse": {"digest": {"expected": wrong_digest, "checker": rejected_digest},
                        "physical_ports": rejected_port,
                        "invalid_labeling": {"swap": [u, v], "repeated": repeated, "missing": missing,
                                             "checker": rejected_swap}}}


def verify_inputs(cfg):
    assert cfg["domain"] == {"profile": [[4], [2]], "cut": 6, "ports": ["s:0", "s:1"],
                             "offsets": [5, 3], "port_labels": [5, 9], "entrance_is_low": True}
    assert cfg["limits"] == {
        "workers": 1, "max_new_original_identities": 1, "prescribed_offset_pairs": 1,
        "max_new_certificates": 1, "max_extremal_representations": 10, "assignment_visits": 0,
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
    graph = build_graph(cfg["domain"]["profile"])
    named = {"graph": graph, "graph_digest": graph_digest(graph)}
    original_hash = write_record("original.json", named, cfg["limits"])
    checked = controls(cfg)
    report = audit.check(ROOT, HERE, cfg, checked)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "disposition": "EXCLUDED", "graph_digest": named["graph_digest"], "runtime": runtime,
            "source_hashes": cfg["source_hashes"], "original_sha256": original_hash,
            "controls": checked, "audit": report}


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
        receipt["counts"].update(prescribed_offset_pairs=1, new_certificates=0,
                                 extremal_representations=result["audit"]["extremal"]["representations"],
                                 retained_positive_rechecks=1, adverse_checks=3)
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
