"""Bounded executable checks on the retained D111 boundary only."""

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


def indexed_formula(q):
    if type(q) is not int or q < 5 or q % 2 != 1:
        raise ValueError("Require an exact odd integer q >= 5")
    m = q + 9
    t = m // 2
    a, b = "b:0:0", "b:0:1"
    core = {"s:0": 0, "s:1": m, a: q + 7, b: 2, "b:1:0": 1,
            "l:0:1:0": 3, "l:0:1:2": q + 8, "l:1:0:0": q + 5, "l:1:0:1": q + 6}
    allocation = {a: [x for x in range(4, q + 5) if x != t], b: [t]}
    assert len(allocation[a]) == q
    labels = core | {"l:0:1:1": t}
    labels.update({f"l:0:0:{i}": x for i, x in enumerate(allocation[a])})
    return core, allocation, labels


def pins_gate(graph, labels, q):
    expected = {"s:0": 0, "s:1": q + 9, "b:1:0": 1}
    assert graph["spine"] == ["s:0", "s:1"]
    actual_edges = {frozenset(edge) for edge in graph["edges"]}
    assert frozenset(graph["spine"]) in actual_edges
    assert frozenset(("s:1", "b:1:0")) in actual_edges
    actual = {v: labels[v] for v in expected}
    return {"actual": actual, "expected": expected,
            "valid": actual == expected and all(type(x) is int for x in actual.values())}


def allocation_gate(graph, core, allocation):
    hosts = ("b:0:0", "b:0:1")
    assert set(allocation) == set(hosts) and set(hosts) <= set(core)
    m = len(graph["edges"])
    occupied = [abs(core[u] - core[v]) for u, v in graph["edges"] if u in core and v in core]
    remaining_labels = set(range(m + 1)) - set(core.values())
    remaining_weights = set(range(1, m + 1)) - set(occupied)
    vacancies = [frozenset((u, v)) for u, v in graph["edges"] if u not in core or v not in core]
    assert all(len(edge.intersection(core)) == 1 and edge.intersection(core) <= set(hosts)
               for edge in vacancies)
    expected_quotas = {h: sum(h in edge for edge in vacancies) for h in hosts}
    actual_quotas = {h: len(allocation[h]) for h in hosts}
    labels = [x for h in hosts for x in allocation[h]]
    weights = [abs(core[h] - x) for h in hosts for x in allocation[h]]
    labels_exact = Counter(labels) == Counter(remaining_labels)
    weights_exact = Counter(weights) == Counter(remaining_weights)
    quotas_exact = actual_quotas == expected_quotas
    return {"residual_labels": sorted(remaining_labels), "residual_differences": sorted(remaining_weights),
            "allocated_labels": sorted(labels), "allocated_differences": sorted(weights),
            "expected_quotas": expected_quotas, "actual_quotas": actual_quotas,
            "labels_exact": labels_exact, "differences_exact": weights_exact,
            "quotas_exact": quotas_exact, "valid": labels_exact and weights_exact and quotas_exact}


def retained_positive(binding, q, counts):
    path = ROOT / binding["original"]
    original = read_json(path)
    record = read_json(ROOT / binding["result"])
    cert, graph = record["certificate"], original["graph"]
    digest = binding["graph_digest"]
    assert digest_file(path) == record["target_original_sha256"] == binding["original_sha256"]
    assert record["status"] == "PASS" and record["proof_disposition"] == record["seed_disposition"] == "ACCEPT"
    assert graph["profile"] == [[q, 3], [2]] and graph["spine"] == cert["physical_spine"]
    assert cert["graph_digest"] == original["graph_digest"] == digest and cert["ledger_id"] == binding["ledger_id"]
    assert cert["kind"] == "ordinary_graceful"
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, cert["labels"], digest)
    gate = pins_gate(graph, cert["labels"], q)
    assert checked["valid"] and checked == cert["checker"] and gate["valid"]
    return original, record, {"original_path": binding["original"], "result_path": binding["result"],
                              "graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked, "pins": gate}


def run_controls(original, labels, q, core, allocation, counts):
    graph, digest = original["graph"], original["graph_digest"]
    wrong = "0" * 64
    counts["declared_controls"] += 1
    wrong_report = verify_certificate(graph, labels, wrong)
    assert not wrong_report["valid"] and wrong_report["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    u, v = "l:0:0:0", "l:0:1:1"
    assert (labels[u], labels[v]) == (4, 7)
    cross = labels | {u: labels[v], v: labels[u]}
    cross_report = verify_certificate(graph, cross, digest)
    cross_pins = pins_gate(graph, cross, q)
    assert sorted(cross.values()) == sorted(labels.values()) and cross_pins["valid"]
    assert not cross_report["valid"]
    assert cross_report["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]

    counts["declared_controls"] += 1
    a, b = "b:0:0", "b:0:1"
    assert allocation[b] == [7]
    moved = {a: sorted(allocation[a] + allocation[b]), b: []}
    quota_report = allocation_gate(graph, core, moved)
    assert quota_report["labels_exact"] and quota_report["differences_exact"]
    assert not quota_report["quotas_exact"] and not quota_report["valid"]

    counts["declared_controls"] += 1
    complement = {v: len(graph["edges"]) - x for v, x in labels.items()}
    complement_report = verify_certificate(graph, complement, digest)
    complement_pins = pins_gate(graph, complement, q)
    assert complement_report["valid"] and not complement_pins["valid"]
    return {"wrong_digest": {"expected_digest": wrong, "checker": wrong_report},
            "cross_center": {"vertices": [u, v], "checker": cross_report, "pins": cross_pins},
            "midpoint_flip": {"allocation": moved, "allocation_gate": quota_report},
            "complement": {"checker": complement_report, "pins": complement_pins}}


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
    scope = cfg["scope"]
    assert scope == {"symbolic_profile": [["q", 3], [2]], "minimum_exact_odd_q": 5, "boundary_q": 5}
    q = scope["boundary_q"]
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    original, record, retained = retained_positive(cfg["retained"], q, counts)
    cert = record["certificate"]
    assert type(q) is int and q == 5
    counts["retained_boundary_evaluations"] += 1
    core, allocation, formula = indexed_formula(q)
    assert formula == cert["labels"]
    gate = allocation_gate(original["graph"], core, allocation)
    assert gate["valid"]
    boundary = audit.boundary(original, record, retained)
    assert core == boundary["core"]["labels"] and allocation == boundary["allocation"]
    assert gate["actual_quotas"] == boundary["actual_quotas"]
    controls = run_controls(original, cert["labels"], q, core, allocation, counts)
    control_audit = audit.controls(original, cert, controls, boundary)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": scope,
            "runtime": runtime, "retained_positive": retained,
            "retained_boundary": boundary, "retained_allocation_gate": gate,
            "controls": controls, "control_audit": control_audit, "retained_execution_statuses": history}


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
        assert (counts["retained_positive_rechecks"], counts["declared_controls"]) == (1, 4)
        assert counts["symbolic_theorems"] == counts["retained_boundary_evaluations"] == 1
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
