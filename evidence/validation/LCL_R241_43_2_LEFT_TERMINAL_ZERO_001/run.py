"""Single bounded producer and independent-audit invocation for D104."""

from time import perf_counter, process_time

WALL_START = perf_counter()
CPU_START = process_time()

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from itertools import permutations
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


def require_zero_terminal(graph, labels, name, declared):
    role = graph["roles"].get(name)
    if not role or role["kind"] != "leaf" or role["section"] != 0:
        raise ValueError("Wrong physical left terminal")
    center = f"b:0:{role['branch']}"
    assert [center, name] in graph["edges"]
    if type(declared) is not int or declared != 0 or labels[name] != declared:
        raise ValueError("The physical left terminal does not carry zero")


def controls(original, cert, cfg, counts):
    graph, digest = original["graph"], original["graph_digest"]
    labels = cert["labels"]
    assert graph["profile"] == [[4, 2], [2]] and digest == graph_digest(graph) == cfg["control_digest"]
    assert cert["graph_digest"] == digest and cert["ledger_id"] == cfg["control_ledger"]
    assert cert["witness"] == graph["spine"]
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"] and checked == cert["checker"]

    counts["adverse_controls"] += 1
    wrong = verify_certificate(graph, labels, "0"*64)
    assert not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"]

    counts["adverse_controls"] += 1
    terminal = "l:0:0:0"
    try:
        require_zero_terminal(graph, labels, terminal, 0)
    except ValueError as exc:
        false_terminal = {"vertex": terminal, "declared": 0, "actual": labels[terminal],
                          "valid": False, "error": str(exc)}
    else:
        raise AssertionError("The false zero-terminal claim passed")

    counts["adverse_controls"] += 1
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    assert sorted(swapped.values()) == list(range(13))
    invalid = verify_certificate(graph, swapped, digest)
    assert not invalid["valid"]
    assert invalid["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return ({"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked},
            {"wrong_digest": {"expected": "0"*64, "checker": wrong},
             "false_zero_terminal": false_terminal,
             "terminal_swap": {"vertices": [u, v], "labels": swapped, "checker": invalid}})


def scalar_cases(original, cfg, counts):
    graph = original["graph"]
    degree = Counter(vertex for edge in graph["edges"] for vertex in edge)
    cut = cfg["domain"]["cut"]
    maximum = len(graph["edges"])
    high = range(cut, maximum+1)
    low = {"s:0", "b:1:0"} | {name for name in graph["vertices"] if name.startswith("l:0:")}
    assert (len(low), cut, maximum) == (9, 9, 13)
    assert all((u in low) != (v in low) for u, v in graph["edges"])
    constant = sum(range(1, maximum+1)) - (sum(high)-sum(range(cut)))
    assert constant == 72
    assert degree["s:0"] == degree["b:1:0"] == 3 and degree["s:1"] == 2
    left = ("b:0:0", "b:0:1")
    rows = []
    for i, center in enumerate(left):
        other = left[1-i]
        quota = degree[center]-1
        for c, y in permutations(range(cut, maximum), 2):
            counts["role_pairs"] += 1
            total = quota*maximum + (degree[other]-1)*c + y - constant
            checks = []
            for x in range(1, quota+1):
                counts["scalar_checks"] += 1
                twice_z = total-2*x
                z, parity = divmod(twice_z, 2)
                check = {"x": x, "twice_z": twice_z}
                if parity:
                    check["verdict"] = "odd"
                elif not x < z < cut:
                    check["verdict"] = "out_of_range"
                else:
                    check.update(verdict="survives", z=z)
                checks.append(check)
            rows.append({"max_center": center, "quota": quota, "C": c, "Y": y,
                         "twice_x_plus_z": total, "checks": checks})
    return rows


def case_witnesses(reductions, counts):
    missing_claims = {
        ("b:0:0",9,11): {1:1,2:2,3:3,4:4},
        ("b:0:0",10,12): {3:2,4:1},
        ("b:0:0",11,9): {3:3,4:1},
        ("b:0:1",9,11): {1:3,2:4,3:9},
        ("b:0:1",10,9): {1:1,2:1,3:1},
        ("b:0:1",10,11): {1:2,2:1,3:1},
        ("b:0:1",11,9): {2:3,3:1},
    }
    cases = []
    for role in reductions:
        center, c, y = role["max_center"], role["C"], role["Y"]
        a, b = (13, c) if center == "b:0:0" else (c, 13)
        right = sorted(set(range(9, 14))-{a, b, y})
        for check in role["checks"]:
            if check["verdict"] != "survives":
                continue
            counts["surviving_cases"] += 1
            x, z = check["x"], check["z"]
            remaining = sorted(set(range(x+1, 9))-{z})
            fixed = [y-x, a-x, b-x, y-z, *(label-z for label in right)]
            forced = list(range(13, 13-x, -1))
            multiplicities = {str(weight): n for weight, n in Counter(fixed+forced).items()}
            w = missing_claims[center, c, y][x]
            endpoints = [13-w, c-w]
            assert str(w) not in multiplicities and set(endpoints).isdisjoint(remaining)
            cases.append({"max_center": center, "A": a, "B": b, "C": c, "Y": y, "x": x, "z": z,
                          "right_palette": right, "forced_max_terminal_palette": list(range(x)),
                          "residual_low_palette": remaining, "six_fixed_weights": fixed,
                          "forced_max_terminal_weights": forced, "W_multiplicities": multiplicities,
                          "W_repeats": {weight:n for weight,n in multiplicities.items() if n > 1},
                          "missing_weight": w, "candidate_low_endpoints_at_max_and_other": endpoints})
    return cases


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
    assert cfg["domain"] == {"cut": 9, "zero_location": "any_left_terminal", "free_spine_ports": True}
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
    reductions = scalar_cases(target, cfg, counts)
    cases = case_witnesses(reductions, counts)
    positive, adverse = controls(source, cert, cfg, counts)
    arithmetic = audit.obstruction(target, cfg["target_digest"], reductions, cases)
    control_audit = audit.controls(source, cert, positive, adverse)
    earlier = {key: read_json(ROOT / path) for key, path in cfg["prior_alpha_results"].items()}
    closure = audit.alpha_scope(target, digest_file(ROOT / retained["target_original"]), arithmetic, earlier)
    return {"status": "PASS", "proof_disposition": "ACCEPT", "state_disposition": "REJECT",
            "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"], "runtime": runtime,
            "target_original": retained["target_original"], "target_graph_digest": target["graph_digest"],
            "target_original_sha256": digest_file(ROOT / retained["target_original"]),
            "scalar_reductions": reductions, "case_witnesses": cases, "retained_positive": positive, "adverses": adverse,
            "arithmetic_audit": arithmetic, "control_audit": control_audit, "retained_execution_statuses": history,
            "alpha_scope": closure}


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
        assert (counts["role_pairs"], counts["scalar_checks"], counts["surviving_cases"]) == (24, 84, 19)
        assert (counts["retained_positive_rechecks"], counts["adverse_controls"]) == (1, 3)
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
