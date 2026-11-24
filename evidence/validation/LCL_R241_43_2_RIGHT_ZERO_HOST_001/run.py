"""Single bounded producer and independent-audit invocation for D102."""

from time import perf_counter, process_time

WALL_START = perf_counter()
CPU_START = process_time()

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
import traceback

import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.model import graph_digest
from lcl.verify import verify_certificate


def read_json(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, indent=2, sort_keys=True)+"\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)
    return sha256(raw).hexdigest()


def require_zero_host(graph, labels, name, declared):
    expected_role = {"kind": "branch", "section": 1, "branch": 0}
    if name != "b:1:0" or graph["roles"].get(name) != expected_role:
        raise ValueError("Wrong physical zero host")
    assert graph["spine"] == ["s:0", "s:1"]
    assert any(set(edge) == {"s:1", name} for edge in graph["edges"])
    if type(declared) is not int or declared != 0 or labels[name] != declared:
        raise ValueError("The physical right center does not carry zero")


def controls(original, cert, cfg, counts):
    graph, digest = original["graph"], original["graph_digest"]
    labels = cert["labels"]
    assert graph["profile"] == [[4, 2], [2]] and digest == graph_digest(graph) == cfg["control_digest"]
    assert cert["graph_digest"] == digest and cert["ledger_id"] == cfg["control_ledger"]
    assert cert["witness"] == graph["spine"]
    require_zero_host(graph, labels, "b:1:0", 0)
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"] and checked == cert["checker"]

    counts["adverse_controls"] += 1
    wrong = verify_certificate(graph, labels, "0"*64)
    assert not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"]

    counts["adverse_controls"] += 1
    host = "b:1:0"
    wrong_host = labels | {host: labels["s:0"], "s:0": labels[host]}
    try:
        require_zero_host(graph, wrong_host, host, 0)
    except ValueError as exc:
        false_host = {"vertex": host, "declared": 0, "actual": wrong_host[host],
                      "valid": False, "error": str(exc)}
    else:
        raise AssertionError("The false zero-host case passed")

    counts["adverse_controls"] += 1
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    assert sorted(swapped.values()) == list(range(13))
    invalid = verify_certificate(graph, swapped, digest)
    assert not invalid["valid"]
    assert invalid["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return ({"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked},
            {"wrong_digest": {"expected": "0"*64, "checker": wrong},
             "false_zero_host": false_host,
             "terminal_swap": {"vertices": [u, v], "labels": swapped, "checker": invalid}})


def order_bounds(original, cfg, counts):
    graph = original["graph"]
    left_a, left_b, right = "b:0:0", "b:0:1", "b:1:0"
    degree = Counter(vertex for edge in graph["edges"] for vertex in edge)
    cut = cfg["domain"]["cut"]
    low = {"s:0", right} | {v for v in graph["vertices"] if v.startswith("l:0:")}
    maximum = len(graph["edges"])
    assert len(low) == cut == 9 and maximum == 13
    assert all((u in low) != (v in low) for u, v in graph["edges"])
    first, second = degree[left_a]-1, degree[left_b]-1
    max_coefficient = degree["s:0"]-1
    assert degree["s:1"] == 2 and max_coefficient == 2
    rhs = sum(range(1, maximum+1)) - (sum(range(cut, maximum+1)) - sum(range(cut))) + maximum
    rows = []
    for greater, smaller in ((left_a, left_b), (left_b, left_a)):
        counts["order_cases"] += 1
        coefficients = {left_a: first, left_b: second}
        coefficients[greater] += max_coefficient
        bounds = {greater: cut+1, smaller: cut}
        lhs = sum(coefficients[v]*bound for v, bound in bounds.items())
        rows.append({"larger_center": greater, "coefficients": coefficients,
                     "center_lower_bounds": bounds, "lhs_lower_bound": lhs,
                     "rhs_upper_bound": rhs, "strict_gap": lhs-rhs})
    assert [row["lhs_lower_bound"] for row in rows] == [87, 86] and rhs == 85
    return rows


def validate_inputs(cfg):
    receipt = read_json(HERE / "preflight_receipt.json")
    assert receipt["status"] == "PASS" and receipt["task"] == cfg["task"]
    assert receipt["parent"] == cfg["parent"] and receipt["preflight_invocations"] == 1
    assert receipt["input_hashes"] == {name: digest_file(HERE / name) for name in cfg["local_inputs"]}
    assert receipt["runtime"]["sha256"] == cfg["runtime_sha256"] == digest_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert digest_file(ROOT / path) == expected, path
    return receipt["runtime"]


def produce(cfg, counts):
    runtime = validate_inputs(cfg)
    assert cfg["domain"] == {"cut": 9, "host": "b:1:0", "host_label": 0, "free_spine_ports": True}
    retained = cfg["retained"]
    target = read_json(ROOT / retained["target_original"])
    assert target["graph"]["profile"] == [[4, 3], [2]]
    assert target["graph_digest"] == graph_digest(target["graph"]) == cfg["target_digest"]
    source = read_json(ROOT / retained["source_original"])
    report = read_json(ROOT / retained["source_result"])
    assert report["status"] == "PASS" and report["original_sha256"] == digest_file(ROOT / retained["source_original"])
    cert = report["certificate"]
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    rows = order_bounds(target, cfg, counts)
    positive, adverse = controls(source, cert, cfg, counts)
    arithmetic = audit.obstruction(target, cfg["target_digest"], rows)
    control_audit = audit.controls(source, cert, positive, adverse)
    return {"status": "PASS", "proof_disposition": "ACCEPT", "state_disposition": "REJECT",
            "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"], "runtime": runtime,
            "target_original": retained["target_original"], "target_graph_digest": target["graph_digest"],
            "target_original_sha256": digest_file(ROOT / retained["target_original"]),
            "order_cases": rows, "retained_positive": positive, "adverses": adverse,
            "arithmetic_audit": arithmetic, "control_audit": control_audit, "retained_execution_statuses": history}


def execute():
    assert __debug__ and sys.dont_write_bytecode
    assert all(not (HERE / name).exists() for name in ("result.json", "command_receipt.json", "__pycache__"))
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = {key: 0 for key in cfg["count_keys"]}
    counts.update(workers=1, official_invocations=1, preflights=1)
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits}
    try:
        receipt["input_hashes"] = {name: digest_file(HERE / name)
                                   for name in (*cfg["local_inputs"], "preflight_receipt.json")}
        result = produce(cfg, counts)
        assert all(value <= limits[key] for key, value in counts.items())
        assert (counts["order_cases"], counts["retained_positive_rechecks"], counts["adverse_controls"]) == (2, 1, 3)
        if process_time()-CPU_START >= limits["process_cpu_seconds"] or perf_counter()-WALL_START >= limits["wall_seconds"]:
            raise TimeoutError("Official time cap exceeded")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        receipt.update(status="PASS", exit_code=0)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["process_cpu_seconds"] = process_time()-CPU_START
    receipt["wall_seconds"] = perf_counter()-WALL_START
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
