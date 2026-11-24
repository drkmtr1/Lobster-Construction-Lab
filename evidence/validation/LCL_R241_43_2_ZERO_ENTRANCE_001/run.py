"""Single bounded producer and independent-audit invocation for D103."""

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


def require_zero_entrance(graph, labels, name, declared):
    entry, exit_name = graph["spine"]
    if name != entry or graph["roles"].get(name) != {"kind": "spine", "section": 0}:
        raise ValueError("Wrong physical entrance")
    assert [entry, exit_name] in graph["edges"]
    if type(declared) is not int or declared != 0 or labels[name] != declared:
        raise ValueError("The physical entrance does not carry zero")


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
    entrance = "s:0"
    try:
        require_zero_entrance(graph, labels, entrance, 0)
    except ValueError as exc:
        false_entrance = {"vertex": entrance, "declared": 0, "actual": labels[entrance],
                          "valid": False, "error": str(exc)}
    else:
        raise AssertionError("The false zero-entrance claim passed")

    counts["adverse_controls"] += 1
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    assert sorted(swapped.values()) == list(range(13))
    invalid = verify_certificate(graph, swapped, digest)
    assert not invalid["valid"]
    assert invalid["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return ({"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked},
            {"wrong_digest": {"expected": "0"*64, "checker": wrong},
             "false_zero_entrance": false_entrance,
             "terminal_swap": {"vertices": [u, v], "labels": swapped, "checker": invalid}})


def scalar_cases(original, cfg, counts):
    graph = original["graph"]
    names = ("b:0:0", "b:0:1", "s:1")
    degree = Counter(vertex for edge in graph["edges"] for vertex in edge)
    cut = cfg["domain"]["cut"]
    maximum = len(graph["edges"])
    high = range(cut, maximum+1)
    low = {"s:0", "b:1:0"} | {name for name in graph["vertices"] if name.startswith("l:0:")}
    assert (len(low), cut, maximum) == (9, 9, 13)
    assert all((u in low) != (v in low) for u, v in graph["edges"])
    assert {v for edge in graph["edges"] if "s:0" in edge for v in edge if v != "s:0"} == set(names)
    constant = sum(range(1, maximum+1)) - (sum(high)-sum(range(cut)))
    divisor = degree["b:1:0"]-1
    coefficients = tuple(degree[name]-1 for name in names)
    assert (constant, divisor, coefficients) == (72, 2, (4, 3, 1))
    reductions = []
    for i in range(len(names)):
        for pair in permutations(range(cut, maximum), 2):
            triple = (*pair[:i], maximum, *pair[i:])
            counts["scalar_triples"] += 1
            numerator = sum(c*value for c, value in zip(coefficients, triple, strict=True))-constant
            z, parity = divmod(numerator, divisor)
            verdict = "odd" if parity else "survives" if 1 <= z < cut else "out_of_range"
            row = {"triple": list(triple), "twice_z": numerator, "verdict": verdict}
            if verdict == "survives":
                row["z"] = z
            reductions.append(row)
    return sorted(reductions, key=lambda row: row["triple"])


def case_witnesses(reductions, counts):
    missing_claims = {(9, 11, 13): 12, (9, 13, 11): 2, (10, 11, 13): 12,
                      (10, 13, 9): 2, (11, 9, 13): 12, (12, 9, 13): 1}
    cases = []
    for row in reductions:
        if row["verdict"] != "survives":
            continue
        counts["surviving_cases"] += 1
        a, b, y = row["triple"]
        z = row["z"]
        right = sorted(set(range(9, 14))-{a, b, y})
        left = sorted(set(range(1, 9))-{z})
        weights = [y, a, b, y-z, *(value-z for value in right)]
        repeats = {str(weight): count for weight, count in Counter(weights).items() if count > 1}
        if (a, b, y) == (10, 9, 13):
            assert weights[2] == weights[3] == 9 and repeats["9"] >= 2
            witness = {"kind": "repeated_weight", "weight": 9,
                       "edges": [["s:0", "b:0:1"], ["s:1", "b:1:0"]]}
        else:
            w = missing_claims[a, b, y]
            required = [a-w, b-w]
            assert w not in weights and set(required).isdisjoint(left)
            witness = {"kind": "missing_weight", "weight": w, "required_left_terminal_labels": required}
        cases.append({"triple": [a, b, y], "z": z, "right_palette": right, "left_palette": left,
                      "fixed_weights": weights, "fixed_repeat_multiplicities": repeats, "witness": witness})
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
    assert cfg["domain"] == {"cut": 9, "entrance": "s:0", "entrance_label": 0, "free_exit": True}
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
    return {"status": "PASS", "proof_disposition": "ACCEPT", "state_disposition": "REJECT",
            "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"], "runtime": runtime,
            "target_original": retained["target_original"], "target_graph_digest": target["graph_digest"],
            "target_original_sha256": digest_file(ROOT / retained["target_original"]),
            "scalar_reductions": reductions, "case_witnesses": cases, "retained_positive": positive, "adverses": adverse,
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
        assert (counts["scalar_triples"], counts["surviving_cases"]) == (36, 7)
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
