"""Verify only the eight structural cases on the frozen fixed-exit target."""

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
from lcl.model import graph_digest
from lcl.verify import verify_certificate


def load(path):
    return json.loads(path.read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, indent=2, sort_keys=True)+"\n").encode()
    total = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(raw)
    if len(raw) > limits["bytes_per_record"] or total > limits["bytes_total"]:
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as out:
        out.write(raw)
    return sha256(raw).hexdigest()


def require_interface(graph, labels, cut, offsets):
    spine = graph["spine"]
    if spine != ["s:0", "s:1"] or spine not in graph["edges"]:
        raise ValueError("Original spine mismatch")
    if offsets != [labels[spine[0]], labels[spine[-1]]-cut]:
        raise ValueError("Physical offset mismatch")
    if any((labels[u] < cut) == (labels[v] < cut) for u, v in graph["edges"]):
        raise ValueError("Original edge fails the alpha cut")


def control_and_adverses(cfg):
    retained = cfg["retained"]
    original = load(ROOT / retained["d098_original"])
    report = load(ROOT / retained["d098_result"])
    graph, digest = original["graph"], original["graph_digest"]
    cert = report["certificate"]
    labels = cert["labels"]
    assert report["status"] == "PASS" and graph["profile"] == [[4, 2], [2]]
    assert digest == graph_digest(graph) == cert["graph_digest"] == cfg["positive_graph_digest"]
    assert cert["ledger_id"] == cfg["positive_ledger_id"] and cert["cut"] == 8
    require_interface(graph, labels, 8, [3, 4])
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"] and checked == cert["checker"]
    wrong = verify_certificate(graph, labels, "0"*64)
    assert not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"]
    try:
        require_interface(graph, labels, 8, [3, 3])
    except ValueError as exc:
        assert str(exc) == "Physical offset mismatch"
        port = {"claimed": [3, 3], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("Incorrect physical offset accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    corrupted = labels | {u: labels[v], v: labels[u]}
    assert sorted(corrupted.values()) == list(range(13))
    bad = verify_certificate(graph, corrupted, digest)
    assert not bad["valid"] and bad["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    positive = {"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked}
    adverses = {"graph_digest": {"claimed": "0"*64, "checker": wrong}, "physical_port": port,
                "label_swap": {"vertices": [u, v], "labels": corrupted, "checker": bad}}
    return positive, adverses


def load_target(cfg):
    retained = cfg["retained"]
    original = load(ROOT / retained["d099_original"])
    results = load(ROOT / retained["d099_result"])
    receipt = load(ROOT / retained["d099_receipt"])
    graph = original["graph"]
    assert original["graph_digest"] == graph_digest(graph) == cfg["target_graph_digest"]
    assert graph["profile"] == [[4, 3], [2]] and graph["spine"] == ["s:0", "s:1"]
    assert (len(graph["vertices"]), len(graph["edges"])) == (14, 13)
    assert results["status"] == receipt["status"] == "PASS" and results["disposition"] == "REJECT"
    assert results["target_original_sha256"] == raw_hash(ROOT / retained["d099_original"])
    assert receipt["result_sha256"] == raw_hash(ROOT / retained["d099_result"])
    assert receipt["counts"]["threshold_cases"] == 9 and results["accepted_certificates"] == []
    return original


def reduce(original, domain):
    graph = original["graph"]
    assert domain == {"cut": 9, "exit_label": 12, "exit_offset": 3, "entrance_range": [0, 8]}
    adjacency = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacency[u].append(v)
        adjacency[v].append(u)
    degrees = {v: len(neighbors) for v, neighbors in adjacency.items()}
    low = {"s:0", "b:1:0"} | {v for v in graph["vertices"] if v.startswith("l:0:")}
    assert all((u in low) != (v in low) for u, v in graph["edges"])
    highs = set(graph["vertices"])-low
    assert len(low) == 9 and len(highs) == 5
    coefficients = {v: (1 if v in highs else -1)*(degree-1) for v, degree in degrees.items() if degree > 1}
    assert coefficients == {"s:0": -2, "s:1": 1, "b:0:0": 4, "b:0:1": 3, "b:1:0": -2}
    base = sum(range(9, 14))-sum(range(9))
    target_sum = sum(range(1, 14))
    constant = base+12*coefficients["s:1"]
    rhs = target_sum-constant
    assert (base, target_sum, constant, rhs) == (19, 91, 31, 60)
    free_high = [9, 10, 11, 13]
    even_B, = [label for label in free_high if label % 2 == rhs % 2]
    assert even_B == 10
    representations = {str(w): [[w+lo, lo] for lo in range(14-w)] for w in range(13, 9, -1)}
    return {"degree_vector": degrees, "low_names": sorted(low), "high_names": sorted(highs),
            "signed_excess": coefficients, "baseline_signed_sum": base, "constant_with_exit": constant,
            "required_sum": target_sum, "right_hand_side": rhs, "B": even_B, "possible_A": [9, 11, 13],
            "extremal_representations": representations}


def cases(original, reduction):
    graph = original["graph"]
    incidences = {frozenset(edge) for edge in graph["edges"]}
    assert len(incidences) == 13
    spine = ["s:0", "s:1"]
    first, second, right = "b:0:0", "b:0:1", "b:1:0"
    attaches = [["s:0", first], ["s:0", second], ["s:1", right]]
    assert all(frozenset(edge) in incidences for edge in [spine, *attaches])
    assert frozenset((first, right)) not in incidences
    assert sum(first in edge and "s:0" not in edge for edge in incidences) == 4
    assert sum(right in edge and "s:1" not in edge for edge in incidences) == 2
    rows = []
    b = reduction["B"]
    for a in reduction["possible_A"]:
        total = (4*a+3*b-reduction["right_hand_side"])//2
        terminal_highs = sorted({9, 10, 11, 13}-{a,b})
        entrances = (total,) if 13 in terminal_highs else range(max(0, total-8), min(8, total)+1)
        for x in entrances:
            z = total-x
            assert 0 <= x <= 8 and 0 <= z <= 8 and x != z
            row = {"A": a, "B": b, "x": x, "z": z, "right_terminal_labels": terminal_highs,
                   "spine_weight": 12-x, "attachment_weights": [a-x, b-x, 12-z],
                   "right_terminal_weights": [label-z for label in terminal_highs]}
            if 13 in terminal_highs:
                assert z == 0
                needed = 10 if a == 9 else 11
                row["obstruction"] = {"kind": "missing_weight", "weight": needed,
                                      "largest_possible_left_terminal_weight": max(a, b)-1}
            else:
                row["forced_minimum_first_terminal_palette"] = [0, 1, 2]
                row["weight_10_pair"] = [13, 3]
                if (x,z) == (3,8):
                    row["obstruction"] = {"kind": "terminal_capacity", "residual_lows": [4,5,6,7],
                                          "forbidden_second_center_lows": [6,7],
                                          "conflicting_right_weights": [4,3], "remaining_first_slots": 1}
                elif (x,z) == (4,7):
                    row["obstruction"] = {"kind": "duplicate_terminal_palette", "forced_first_terminal_lows": [0,1,2,3],
                                          "forced_second_terminal_lows": [5,6,8], "duplicate_weights": [2,4,5]}
                elif (x,z) == (5,6):
                    row["obstruction"] = {"kind": "duplicate_weight", "weight": 5,
                                          "fixed_edge": attaches[1], "right_terminal_label": 11}
                elif (x,z) == (6,5):
                    row["obstruction"] = {"kind": "duplicate_weight", "weight": 7,
                                          "fixed_edges": [attaches[0], attaches[2]]}
                elif (x,z) == (7,4):
                    row["obstruction"] = {"kind": "duplicate_weight", "weight": 5,
                                          "fixed_edge": spine, "right_terminal_label": 9}
                elif (x,z) == (8,3):
                    row["obstruction"] = {"kind": "missing_weight", "weight": 10,
                                          "required_nonedge": [first, right]}
                else:
                    raise AssertionError("Unspecified scalar case")
            rows.append(row)
    return rows


def inputs(cfg):
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    rec = load(HERE / "preflight_receipt.json")
    assert rec["status"] == "PASS" and rec["task"] == cfg["task"] and rec["parent"] == cfg["parent"]
    assert rec["input_hashes"] == {name: raw_hash(HERE / name) for name in cfg["local_inputs"]}
    assert rec["runtime"]["sha256"] == cfg["runtime_sha256"] == raw_hash(Path(sys.executable))
    for path, pin in cfg["source_hashes"].items():
        assert raw_hash(ROOT / path) == pin, path
    return rec


def produce(cfg, counts):
    preflight = inputs(cfg)
    original = load_target(cfg)
    positive, adverse = control_and_adverses(cfg)
    counts.update(adverse_controls=len(adverse), retained_positive_rechecks=1)
    reduction = reduce(original, cfg["domain"])
    rows = cases(original, reduction)
    assert len(rows) == cfg["limits"]["residual_scalar_cases"]
    counts["residual_scalar_cases"] = len(rows)
    audited = audit.check(ROOT, cfg, original, reduction, rows, positive, adverse)
    return {"status": "PASS", "disposition": "REJECT", "proof_disposition": "ACCEPT",
            "task": cfg["task"], "parent": cfg["parent"], "runtime": preflight["runtime"],
            "domain": cfg["domain"], "target_graph_digest": original["graph_digest"],
            "target_original_sha256": raw_hash(ROOT / cfg["retained"]["d099_original"]),
            "arithmetic_reduction": reduction, "residual_scalar_cases": rows,
            "retained_positive": positive, "adverse": adverse, "audit": audited, "accepted_certificates": []}


def execute():
    if not __debug__ or not sys.dont_write_bytecode:
        raise RuntimeError("Use enabled assertions and -B")
    if any((HERE / name).exists() for name in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be vacant")
    cfg = load(HERE / "config.json")
    limits = cfg["limits"]
    counts = {"official_sequences": 1, "workers": 1, "new_original_identities": 0, "residual_scalar_cases": 0,
              "retained_positive_rechecks": 0, "adverse_controls": 0, "accepted_certificates": 0,
              "solver_calls": 0, "assignment_visits": 0, "search_nodes": 0, "assignment_states": 0,
              "port_sweeps": 0, "joins": 0, "retries": 0, "restarts": 0, "historical_replays": 0}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits,
               "inputs": {name: raw_hash(HERE / name) for name in (*cfg["local_inputs"], "preflight_receipt.json")}}
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
