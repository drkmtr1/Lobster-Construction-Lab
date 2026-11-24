"""One direct construction and independent audit of the D111 ordinary seed."""

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


def pins_gate(graph, labels, required):
    assert graph["spine"] == ["s:0", "s:1"]
    assert graph["roles"]["b:1:0"] == {"kind": "branch", "section": 1, "branch": 0}
    actual_edges = {frozenset(edge) for edge in graph["edges"]}
    assert frozenset(graph["spine"]) in actual_edges
    assert frozenset(("s:1", "b:1:0")) in actual_edges
    pins = {vertex: labels[vertex] for vertex in required}
    return {"actual": pins, "expected": required, "valid": pins == required}


def construct(graph, pins, counts):
    counts["construction_attempts"] += 1
    core = pins | {"b:0:0": 12, "b:0:1": 2, "l:0:1:0": 3, "l:0:1:2": 13,
                   "l:1:0:0": 10, "l:1:0:1": 11}
    m = len(graph["edges"])
    core_weights = [abs(core[u] - core[v]) for u, v in graph["edges"] if u in core and v in core]
    assert len(core_weights) == len(set(core_weights)) == 8
    residual_labels = set(range(m + 1)) - set(core.values())
    residual_weights = set(range(1, m + 1)) - set(core_weights)
    a, b = "b:0:0", "b:0:1"
    midpoint = (core[a] + core[b]) // 2
    groups = [
        ("reflected_pair", a, [5, 2 * midpoint - 5]),
        ("reflected_pair", a, [6, 2 * midpoint - 6]),
        ("forced_singleton", a, [4]),
        ("midpoint", b, [midpoint]),
    ]
    assignments = {a: [], b: []}
    records = []
    for kind, host, values in groups:
        counts["residual_groups"] += 1
        weights = [abs(core[host] - value) for value in values]
        assert len(values) == len(set(values)) and set(values) <= residual_labels
        assert len(weights) == len(set(weights)) and set(weights) <= residual_weights
        residual_labels.difference_update(values)
        residual_weights.difference_update(weights)
        assignments[host].extend(values)
        records.append({"kind": kind, "host": host, "labels": values, "weights": weights})
    assert not residual_labels and not residual_weights
    labels = dict(core)
    for host, values in assignments.items():
        section, branch = host.split(":")[1:]
        prefix = f"l:{section}:{branch}:"
        vacancies = sorted(v for v in graph["vertices"] if v.startswith(prefix) and v not in core)
        labels.update(zip(vacancies, sorted(values), strict=True))
    return labels, {"core": core, "allocation_groups": records}


def retained_positive(cfg, counts):
    binding = cfg["positive"]
    original = read_json(ROOT / binding["original"])
    record = read_json(ROOT / binding["result"])
    cert = record["certificate"]
    assert record["status"] == "PASS" and record["proof_disposition"] == "ACCEPT"
    assert record["target_original_sha256"] == digest_file(ROOT / binding["original"])
    assert original["graph"]["profile"] == [[4, 3], [binding["r"]]]
    assert cert["graph_digest"] == original["graph_digest"] == binding["graph_digest"]
    assert cert["ledger_id"] == binding["ledger_id"]
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(original["graph"], cert["labels"], binding["graph_digest"])
    assert checked["valid"] and checked == cert["checker"]
    return {"graph_digest": binding["graph_digest"], "ledger_id": cert["ledger_id"], "checker": checked}


def run_controls(graph, labels, digest, pins, counts):
    wrong = "0" * 64
    counts["declared_controls"] += 1
    wrong_check = verify_certificate(graph, labels, wrong)
    assert not wrong_check["valid"] and wrong_check["errors"] == ["original graph digest mismatch"]
    records = {"wrong_digest": {"expected_digest": wrong, "checker": wrong_check}}

    u = "l:0:0:0"
    for kind, v in (("cross_center", "l:0:1:1"), ("within_center", "l:0:0:1")):
        counts["declared_controls"] += 1
        modified = labels | {u: labels[v], v: labels[u]}
        checked = verify_certificate(graph, modified, digest)
        gate = pins_gate(graph, modified, pins)
        assert sorted(modified.values()) == sorted(labels.values()) and gate["valid"]
        if kind == "cross_center":
            assert not checked["valid"]
            assert checked["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
        else:
            assert checked["valid"]
        records[kind] = {"vertices": [u, v], "checker": checked, "pins": gate}

    counts["declared_controls"] += 1
    complement = {v: len(graph["edges"]) - value for v, value in labels.items()}
    checked = verify_certificate(graph, complement, digest)
    gate = pins_gate(graph, complement, pins)
    assert checked["valid"] and not gate["valid"]
    records["complement"] = {"checker": checked, "pins": gate}
    return records


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
    domain = cfg["domain"]
    pins = domain["physical_pins"]
    assert domain == {"profile": [[5, 3], [2]], "physical_pins": {"s:0": 0, "s:1": 14, "b:1:0": 1}}
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    original = read_json(ROOT / cfg["target_original"])
    graph, digest = original["graph"], original["graph_digest"]
    raw_hash = digest_file(ROOT / cfg["target_original"])
    assert digest == cfg["target_digest"] and raw_hash == cfg["target_original_sha256"]
    assert graph["profile"] == domain["profile"]
    prior = read_json(ROOT / cfg["prior_result"])
    assert prior["status"] == "PASS" and prior["proof_disposition"] == "ACCEPT"
    assert prior["interface_disposition"] == "REJECT" and prior["target_original_sha256"] == raw_hash
    assert prior["target_graph_digest"] == digest

    labels, construction = construct(graph, pins, counts)
    checked = verify_certificate(graph, labels, digest)
    gate = pins_gate(graph, labels, pins)
    assert checked["valid"] and (checked["n"], checked["m"]) == (15, 14) and gate["valid"]
    ledger_raw = json.dumps({"graph_digest": digest, "labels": sorted(labels.items())},
                            sort_keys=True, separators=(",", ":")).encode()
    cert = {"kind": "ordinary_graceful", "graph_digest": digest, "labels": labels,
            "ledger_id": sha256(ledger_raw).hexdigest(), "checker": checked, "pins": gate,
            "physical_spine": graph["spine"]}
    incidence = audit.certificate_audit(original, cert, construction)
    retained = retained_positive(cfg, counts)
    probes = run_controls(graph, labels, digest, pins, counts)
    control_audit = audit.controls(original, cert, probes)
    counts["new_certificates"] += 1
    return {"status": "PASS", "proof_disposition": "ACCEPT", "seed_disposition": "ACCEPT",
            "task": cfg["task"], "parent": cfg["parent"], "domain": domain, "runtime": runtime,
            "target_original_sha256": raw_hash, "target_graph_digest": digest,
            "certificate": cert, "construction": construction, "incidence_audit": incidence,
            "controls": probes, "control_audit": control_audit, "retained_positive": retained,
            "retained_execution_statuses": history}


def execute():
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = {key: 0 for key in cfg["count_keys"]}
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
        assert (counts["construction_attempts"], counts["residual_groups"], counts["new_certificates"]) == (1, 4, 1)
        assert (counts["retained_positive_rechecks"], counts["declared_controls"]) == (1, 4)
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
