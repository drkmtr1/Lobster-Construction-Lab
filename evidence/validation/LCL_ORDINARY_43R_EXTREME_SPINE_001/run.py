"""Single bounded producer and independent-audit invocation for D107."""

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


def inspect_signed_interface(graph, labels):
    adjacent = {v:[] for v in graph["vertices"]}
    for u,v in graph["edges"]:
        adjacent[u].append(v)
        adjacent[v].append(u)
    entry = graph["spine"][0]
    colors = {entry:0}
    pending = [entry]
    for v in pending:
        for neighbor in adjacent[v]:
            if neighbor not in colors:
                colors[neighbor] = 1-colors[v]
                pending.append(neighbor)
            assert colors[v] != colors[neighbor]
    assert set(colors) == set(graph["vertices"])
    negatives = []
    for u,v in graph["edges"]:
        tail,head = (u,v) if colors[u] == 0 else (v,u)
        signed = labels[head]-labels[tail]
        if signed < 0:
            negatives.append({"edge":[tail,head],"signed_difference":signed})
    return {"physical_spine_labels":[labels[v] for v in graph["spine"]],"negative_edges":negatives}


def require_signed_interface(actual, domain):
    if actual["physical_spine_labels"] != domain["physical_spine_labels"]:
        raise ValueError("Physical spine labels differ from the requested interface")
    if actual["negative_edges"] != [domain["reversed_edge"]]:
        raise ValueError("Negative edge differs from the requested named interface")


def retained_positive(original, record, expected, counts):
    graph, digest = original["graph"], original["graph_digest"]
    cert = record["certificate"]
    assert graph["profile"] == [[4,3],[expected["r"]]]
    assert cert["graph_digest"] == digest == graph_digest(graph) == expected["graph_digest"]
    assert cert["ledger_id"] == expected["ledger_id"]
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, cert["labels"], digest)
    assert checked["valid"] and checked == cert["checker"]
    return {"r":expected["r"],"graph_digest":digest,"ledger_id":cert["ledger_id"],"checker":checked}


def adverse_controls(graph, labels, digest, domain, counts):
    counts["adverse_controls"] += 1
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]

    counts["adverse_controls"] += 1
    u,v = "l:0:0:0","l:0:1:0"
    cross = labels | {u:labels[v],v:labels[u]}
    assert sorted(cross.values()) == list(range(len(graph['vertices'])))
    cross_check = verify_certificate(graph, cross, digest)
    assert not cross_check["valid"]
    assert cross_check["errors"] == ["edge differences repeat","edge differences are not exactly 1..m"]

    counts["adverse_controls"] += 1
    w = "l:0:0:3"
    within = labels | {u:labels[w],w:labels[u]}
    assert sorted(within.values()) == list(range(15))
    within_check = verify_certificate(graph, within, digest)
    assert within_check["valid"] and not within_check["errors"]
    actual = inspect_signed_interface(graph, within)
    try:
        require_signed_interface(actual, domain)
    except ValueError as exc:
        assert str(exc) == "Negative edge differs from the requested named interface"
        gate = {"valid":False,"error":str(exc),"actual":actual}
    else:
        raise AssertionError("Wrong physical reversed edge passed the signed-interface gate")
    return {"wrong_digest":{"expected":"0"*64,"checker":wrong_digest},
            "cross_swap":{"vertices":[u,v],"labels":cross,"checker":cross_check},
            "within_swap":{"vertices":[u,w],"labels":within,"checker":within_check,"signed_interface_gate":gate}}


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
    assert cfg["domain"] == {"fixed_left_quotas":[4,3],"right_minimum":2,"exact_integer":True}
    expected = cfg["boundaries"]
    assert [row["r"] for row in expected] == [2,3]
    history = {key:read_json(ROOT/path)["status"] for key,path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    originals, certificates, reports, positives = [], [], [], []
    for binding in expected:
        original = read_json(ROOT/binding["original"])
        record = read_json(ROOT/binding["result"])
        raw_sha = digest_file(ROOT/binding["original"])
        assert raw_sha == record["target_original_sha256"]
        assert record["status"] == "PASS" and record["proof_disposition"] == "ACCEPT"
        cert = record["certificate"]
        positive = retained_positive(original, record, binding, counts)
        report = audit.boundary(original, cert, positive)
        reports.append(report)
        originals.append(original)
        certificates.append(cert)
        positives.append(positive)
    step = audit.retained_step(originals, certificates, reports)
    d106, cert = originals[1], certificates[1]
    reverse = {"edge":["l:0:0:3","b:0:0"],"signed_difference":-1}
    interface = {"physical_spine_labels":[0,14],"reversed_edge":reverse}
    actual = inspect_signed_interface(d106["graph"], cert["labels"])
    require_signed_interface(actual, interface)
    probes = adverse_controls(d106["graph"], cert["labels"], d106["graph_digest"], interface, counts)
    checked = audit.controls(d106, cert, probes, reports[1])
    return {"status":"PASS","proof_disposition":"ACCEPT","task":cfg["task"],"parent":cfg["parent"],
            "domain":cfg["domain"],"runtime":runtime,"boundary_rechecks":positives,"boundary_audits":reports,
            "archived_induction_step":step,"adverses":probes,"control_audit":checked,
            "retained_execution_statuses":history,
            "scope":"The executable audit uses only retained r=2 and r=3 originals. The proof supplies the quantified induction."}


def execute():
    assert __debug__ and sys.dont_write_bytecode
    assert all(not (HERE / name).exists() for name in ("original.json", "result.json", "command_receipt.json", "__pycache__"))
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
        assert counts["new_certificates"] == counts["new_graph_identities"] == 0
        assert (counts["retained_positive_rechecks"], counts["adverse_controls"]) == (2, 3)
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
