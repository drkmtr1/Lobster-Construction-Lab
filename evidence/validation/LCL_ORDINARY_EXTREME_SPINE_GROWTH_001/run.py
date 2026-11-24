"""One bounded invocation over archived D105, D106 and D111 certificates."""

from time import perf_counter, process_time

WALL_START = perf_counter()
CPU_START = process_time()

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

from lcl.verify import verify_certificate


def read_json(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)
    return sha256(raw).hexdigest()


def growth_gate(graph, labels, spine, u, v, c):
    adjacency = {vertex: set() for vertex in graph["vertices"]}
    for first, second in graph["edges"]:
        adjacency[first].add(second)
        adjacency[second].add(first)
    path_ok = (len(spine) >= 2 and len(set(spine)) == len(spine)
               and set(spine) <= set(adjacency)
               and all(b in adjacency[a] for a, b in zip(spine, spine[1:])))
    near = set(spine) if path_ok else set()
    for _ in range(2):
        near |= {neighbor for vertex in near for neighbor in adjacency[vertex]}
    actual = {vertex: labels.get(vertex) for vertex in (u, v, c)}
    expected = {u: 0, v: len(graph["edges"]), c: 1}
    tests = {
        "distinct_actual_vertices": len({u, v, c}) == 3 and {u, v, c} <= set(adjacency),
        "witnessing_path": path_ok and near == set(adjacency),
        "terminal_exit": bool(spine) and spine[-1] == v,
        "terminal_pair": spine[-2:] == [u, v],
        "host_off_path": c not in spine,
        "exact_exit_neighbors": adjacency.get(v) == {u, c} and u != c,
        "physical_labels": actual == expected and all(type(x) is int for x in actual.values()),
    }
    return {"spine": spine, "actual": actual, "expected": expected,
            "exit_neighbors": sorted(adjacency.get(v, ())), "tests": tests, "valid": all(tests.values())}


def retained_positive(binding, interface, counts):
    original_path = ROOT / binding["original"]
    original = read_json(original_path)
    record = read_json(ROOT / binding["result"])
    cert, graph = record["certificate"], original["graph"]
    digest = binding["graph_digest"]
    assert record["status"] == "PASS" and record["proof_disposition"] == "ACCEPT"
    assert record["target_original_sha256"] == binding["original_sha256"] == digest_file(original_path)
    assert graph["profile"] == binding["profile"] and graph["spine"] == cert["physical_spine"]
    assert cert["graph_digest"] == original["graph_digest"] == digest
    assert cert["ledger_id"] == binding["ledger_id"] and cert["kind"] == "ordinary_graceful"
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, cert["labels"], digest)
    gate = growth_gate(graph, cert["labels"], graph["spine"], **interface)
    assert checked["valid"] and checked == cert["checker"] and gate["valid"]
    review = {"original": binding["original"], "result": binding["result"], "ledger_id": cert["ledger_id"],
              "graph_digest": digest, "original_sha256": binding["original_sha256"], "checker": checked, "premises": gate}
    return original, record, review


def run_controls(original, cert, checker, interface, counts):
    graph, labels = original["graph"], cert["labels"]
    digest, spine = original["graph_digest"], graph["spine"]
    wrong = "0" * 64
    counts["declared_controls"] += 1
    wrong_check = verify_certificate(graph, labels, wrong)
    assert not wrong_check["valid"] and wrong_check["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    a, b = "l:0:0:0", "l:0:0:1"
    assert (labels[a], labels[b]) == (4, 5)
    within = labels | {a: labels[b], b: labels[a]}
    within_check = verify_certificate(graph, within, digest)
    within_gate = growth_gate(graph, within, spine, **interface)
    assert within_check["valid"] and within_gate["valid"]

    counts["declared_controls"] += 1
    complement = {vertex: len(graph["edges"]) - x for vertex, x in labels.items()}
    complement_check = verify_certificate(graph, complement, digest)
    complement_gate = growth_gate(graph, complement, spine, **interface)
    assert complement_check["valid"] and not complement_gate["valid"]
    assert {key for key, valid in complement_gate["tests"].items() if not valid} == {"physical_labels"}

    counts["declared_controls"] += 1
    alternate = ["s:0", "s:1", "b:1:0"]
    alternate_gate = growth_gate(graph, labels, alternate, **interface)
    assert checker["valid"] and not alternate_gate["valid"]
    assert {key for key, valid in alternate_gate["tests"].items() if not valid} == {
        "terminal_exit", "terminal_pair", "host_off_path"
    }
    return {
        "wrong_digest": {"expected_digest": wrong, "checker": wrong_check},
        "within_center": {"swapped_vertices": [a, b], "checker": within_check, "premises": within_gate},
        "complement": {"checker": complement_check, "premises": complement_gate},
        "alternate_path": {"ordinary_source": "D111 retained recheck", "ordinary_valid": checker["valid"],
                           "premises": alternate_gate},
    }


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
    interface = cfg["interface"]
    assert interface == {"u": "s:0", "v": "s:1", "c": "b:1:0"}
    assert cfg["scope"] == {"symbolic_profile": [[5, 3], ["r"]], "minimum_exact_integer_r": 2}
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    assert set(cfg["retained"]) == {"D105", "D106", "D111"}
    archived = {key: retained_positive(binding, interface, counts) for key, binding in cfg["retained"].items()}
    finite = audit.archived_transition(archived["D105"], archived["D106"])
    base = audit.retained_base(archived["D111"])
    original, record, review = archived["D111"]
    probes = run_controls(original, record["certificate"], review["checker"], interface, counts)
    probe_audit = audit.controls(original, record["certificate"], probes)
    counts.update(symbolic_theorems=1, symbolic_applications=1)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": cfg["scope"],
            "runtime": runtime, "retained_positive": {key: triple[2] for key, triple in archived.items()},
            "archived_transition": finite, "retained_application_base": base,
            "controls": probes, "control_audit": probe_audit, "retained_execution_statuses": history}


def execute():
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = dict.fromkeys(cfg["count_keys"], 0)
    counts.update(workers=1, official_invocations=1, preflights=1)
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits}
    try:
        if not __debug__ or not sys.dont_write_bytecode:
            raise RuntimeError("Require active assertions and -B")
        outputs = ("original.json", "result.json", "command_receipt.json", "supervisor_receipt.json", "__pycache__")
        assert all(not (HERE / name).exists() for name in outputs)
        receipt["input_hashes"] = {name: digest_file(HERE / name)
                                   for name in (*cfg["local_inputs"], "preflight_receipt.json")}
        result = produce(cfg, counts)
        assert all(value <= limits[key] for key, value in counts.items())
        assert (counts["retained_positive_rechecks"], counts["declared_controls"]) == (3, 4)
        assert counts["symbolic_theorems"] == counts["symbolic_applications"] == 1
        if process_time() - CPU_START >= limits["process_cpu_seconds"] or perf_counter() - WALL_START >= limits["wall_seconds"]:
            raise TimeoutError("Official time cap exceeded")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        if process_time() - CPU_START >= limits["process_cpu_seconds"] or perf_counter() - WALL_START >= limits["wall_seconds"]:
            raise TimeoutError("Official time cap exceeded after writing the result")
        receipt.update(status="PASS", exit_code=0)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    receipt["wall_seconds"] = perf_counter() - WALL_START
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
