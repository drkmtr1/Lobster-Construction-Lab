"""Single bounded producer and independent-audit invocation for D105."""

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


def direct_labels():
    labels = {"s:0":0, "s:1":13, "b:0:0":10, "b:0:1":9, "b:1:0":1}
    groups = ((0,0,(2,3,8,11)), (0,1,(4,5,6)), (1,0,(7,12)))
    for section, branch, palette in groups:
        for k, label in enumerate(palette):
            labels[f"l:{section}:{branch}:{k}"] = label
    return labels


def require_physical_spine(graph, labels, declared):
    spine = graph["spine"]
    assert spine == ["s:0", "s:1"]
    assert [spine[0], spine[1]] in graph["edges"]
    actual = [labels[v] for v in spine]
    if actual != declared:
        raise ValueError("Declared physical spine labels differ from the original")
    return actual


def retained_positive(original, cert, cfg, counts):
    graph, digest = original["graph"], original["graph_digest"]
    assert graph["profile"] == [[4,2],[2]] and digest == graph_digest(graph) == cfg["control_digest"]
    assert cert["graph_digest"] == digest and cert["ledger_id"] == cfg["control_ledger"]
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, cert["labels"], digest)
    assert checked["valid"] and checked == cert["checker"]
    return {"graph_digest":digest, "ledger_id":cert["ledger_id"], "checker":checked}


def adverse_controls(graph, labels, digest, counts):
    counts["adverse_controls"] += 1
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]

    counts["adverse_controls"] += 1
    bad_declared = [0,12]
    try:
        require_physical_spine(graph, labels, bad_declared)
    except ValueError as exc:
        spine = graph["spine"]
        wrong_spine = {"vertices":spine, "declared":bad_declared,
                       "actual":[labels[v] for v in spine], "valid":False, "error":str(exc)}
    else:
        raise AssertionError("False spine declaration passed")

    counts["adverse_controls"] += 1
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u:labels[v], v:labels[u]}
    assert sorted(swapped.values()) == list(range(14))
    check = verify_certificate(graph, swapped, digest)
    assert not check["valid"]
    assert check["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"wrong_digest":{"expected":"0"*64,"checker":wrong_digest},
            "wrong_spine":wrong_spine,"terminal_swap":{"vertices":[u,v],"labels":swapped,"checker":check}}


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
    assert cfg["domain"] == {"kind":"ordinary_graceful","physical_spine_labels":[0,13]}
    paths = cfg["retained"]
    target = read_json(ROOT / paths["target_original"])
    graph, digest = target["graph"], target["graph_digest"]
    assert graph["profile"] == [[4,3],[2]] and digest == graph_digest(graph) == cfg["target_digest"]
    original_sha = digest_file(ROOT / paths["target_original"])
    source = read_json(ROOT / paths["source_original"])
    source_report = read_json(ROOT / paths["source_result"])
    assert source_report["status"] == "PASS"
    assert source_report["original_sha256"] == digest_file(ROOT / paths["source_original"])
    prior = read_json(ROOT / cfg["prior_alpha_result"])
    history = {key:read_json(ROOT/path)["status"] for key,path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    labels = direct_labels()
    physical = require_physical_spine(graph, labels, cfg["domain"]["physical_spine_labels"])
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"] and (checked["n"],checked["m"]) == (14,13)
    ledger_raw = json.dumps({"graph_digest":digest,"labels":sorted(labels.items())},
                            sort_keys=True,separators=(",",":")).encode()
    certificate = {"kind":"ordinary_graceful", "graph_digest":digest, "labels":labels,
                   "ledger_id":sha256(ledger_raw).hexdigest(), "checker":checked,
                   "physical_spine":graph["spine"], "physical_spine_labels":physical}
    counts["new_certificates"] += 1
    retained = retained_positive(source, source_report["certificate"], cfg, counts)
    probes = adverse_controls(graph, labels, digest, counts)
    incidence = audit.certificate_audit(target, cfg["target_digest"], certificate)
    control_audit = audit.controls(target, certificate, probes, source, source_report["certificate"], retained)
    scope = audit.reconcile_alpha_scope(target, original_sha, prior, incidence)
    return {"status":"PASS","proof_disposition":"ACCEPT","state_disposition":"ACCEPT",
            "task":cfg["task"],"parent":cfg["parent"],"domain":cfg["domain"],"runtime":runtime,
            "target_original":paths["target_original"],"target_graph_digest":digest,"target_original_sha256":original_sha,
            "certificate":certificate,"incidence_audit":incidence,"retained_positive":retained,
            "adverses":probes,"control_audit":control_audit,"retained_execution_statuses":history,"scope":scope}


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
        assert counts["new_certificates"] == 1
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
