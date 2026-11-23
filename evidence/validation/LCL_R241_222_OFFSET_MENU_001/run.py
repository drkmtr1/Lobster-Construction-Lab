"""Verify only the two declared ledgers and the 30 D084 proof records."""

from time import process_time

START = process_time()

from collections import Counter
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


def witness(original, labels, offsets):
    graph, digest = original["graph"], original["graph_digest"]
    port_labels = physical_ports(labels, 6, offsets)
    assert all((labels[u] < 6) != (labels[v] < 6) for u, v in graph["edges"])
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"], checked
    return {"labels": labels, "checker": checked, "graph_digest": digest,
            "ledger_id": ledger_id(digest, labels), "port_labels": port_labels, "cut": 6,
            "physical_ports": ["s:0", "s:1"],
            "witness": graph["spine"],
            "edge_rows": [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]}


def controls(cfg, original, labels):
    posdir = ROOT / cfg["control_archive"]
    f2 = read(posdir / "f2_original.json")
    archived = read(posdir / "certificates.json")["controls"]["f2"]
    positive = verify_certificate(f2["graph"], archived["labels"], f2["graph_digest"])
    assert positive["valid"] and positive == archived["checker"]
    assert physical_ports(archived["labels"], 5, [1, 0]) == [1, 5]
    assert ledger_id(f2["graph_digest"], archived["labels"]) == archived["ledger_id"]

    negdir = ROOT / cfg["negative_archive"]
    d082_audit = read(negdir / "audit_result.json")
    assert d082_audit["status"] == "PASS" and d082_audit["visits_certified"] == 2880
    assert d082_audit["positive_certificates"] == 0
    negative = {"pair": [1, 0], "graph_digest": original["graph_digest"],
                "historical_visits": d082_audit["visits_certified"], "positive": 0,
                "new_replay_visits": 0,
                "receipt_sha256": d082_audit["raw_receipts"]["enumeration.json"]}

    bad_digest = "0"*64
    wrong_digest = verify_certificate(original["graph"], labels, bad_digest)
    assert wrong_digest["errors"] == ["original graph digest mismatch"] and not wrong_digest["valid"]
    try:
        physical_ports(labels, 6, [1, 0])
    except ValueError as error:
        wrong_port = {"valid": False, "reason": str(error), "declared": [1, 0], "actual": [2, 0]}
    else:
        raise AssertionError("Mismatched port accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    perturbed = labels | {u: labels[v], v: labels[u]}
    wrong_weights = verify_certificate(original["graph"], perturbed, original["graph_digest"])
    assert not wrong_weights["valid"]
    assert "edge differences repeat" in wrong_weights["errors"]
    return {"d081_f2": positive, "d082_strict": negative, "adverse": {
        "digest": {"expected": bad_digest, "checker": wrong_digest},
        "port": wrong_port, "duplicate_difference": {"swap": [u, v], "checker": wrong_weights}}}


def verify_inputs(cfg):
    assert cfg["profile"] == [[2, 2], [2]] and cfg["cut"] == 6
    assert cfg["limits"] == {
        "workers": 1, "new_original_identities": 0, "offset_states": 30, "assignment_visits": 0,
        "recorded_assignment_states": 0, "search_nodes": 0, "solver_calls": 0, "max_ledgers": 30,
        "adverse_checks": 3, "cpu_seconds": 30, "bytes_per_record": 2_000_000, "bytes_total": 8_000_000,
        "official_sequences": 1, "retries": 0, "replays": 0}
    exe = Path(sys.executable)
    assert sys.version_info[:2] in {(3, 12), (3, 13)}
    assert hash_file(exe) == cfg["runtime_sha256"]
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected
    return {"path": exe.relative_to(ROOT).as_posix(), "sha256": hash_file(exe), "version": sys.version}


def main(cfg):
    runtime = verify_inputs(cfg)
    original = read(ROOT / cfg["original"])
    source = read(HERE / "menu_source.json")
    assert set(source["ledgers"]) == {"2,0", "3,4"}
    rows = []
    for x in range(6):
        for y in range(5):
            key = f"{x},{y}"
            row = {"pair": [x, y], "port_labels": [x, 6+y], "graph_digest": original["graph_digest"]}
            if key in source["ledgers"]:
                row.update(status="WITNESSED", proof="explicit-ledger",
                           certificate=witness(original, source["ledgers"][key], [x, y]))
            elif y % 2:
                row.update(status="EXCLUDED", proof="signed-degree-parity")
            else:
                claims = source["proof_table"][key]
                status = "UNRESOLVED" if "W" in claims else "EXCLUDED"
                row.update(status=status, proof="mandatory-weight-table", claims=claims)
            rows.append(row)
    menu = {"pairs": rows, "counts": dict(Counter(row["status"] for row in rows))}
    menu["counts"].setdefault("UNRESOLVED", 0)
    checked_controls = controls(cfg, original, source["ledgers"]["2,0"])
    audit_result = audit.check(ROOT, cfg, source, menu, checked_controls)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"],
            "runtime": runtime, "source_hashes": cfg["source_hashes"],
            "original": cfg["original"], "graph_digest": original["graph_digest"],
            "menu": menu, "controls": checked_controls, "audit": audit_result}


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
    if any((HERE / file).exists() for file in ("result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be empty")
    started = datetime.now(timezone.utc).isoformat()
    wall_start = perf_counter()
    cfg = read(HERE / "config.json")
    limits = cfg["limits"]
    inputs = {name: hash_file(HERE / name) for name in ("run.py", "audit.py", "config.json", "menu_source.json")}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": started, "limits": limits, "local_inputs": inputs,
               "counts": {"official_sequences": 1, "workers": 1, "new_original_identities": 0,
                          "named_assignment_visits": 0, "recorded_assignment_states": 0, "search_nodes": 0,
                          "solver_calls": 0, "replays": 0, "retries": 0}}
    try:
        result = main(cfg)
        if process_time() - START >= limits["cpu_seconds"]:
            raise TimeoutError("Verification process CPU budget reached")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        receipt.update(status="PASS", exit_code=0)
        receipt["counts"].update(offset_records=30, checked_ledgers=2, adverse_checks=3)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["combined_process_cpu_seconds"] = process_time() - START
    receipt["wall_seconds"] = perf_counter() - wall_start
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
