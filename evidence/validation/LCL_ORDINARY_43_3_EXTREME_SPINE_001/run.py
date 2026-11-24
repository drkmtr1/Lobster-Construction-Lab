"""Single bounded producer and independent-audit invocation for D106."""

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

from lcl.model import build_graph, graph_digest
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


def extend_certificate(source, source_cert, cfg, counts):
    assert source["profile"] == [[4,3],[2]] and source["spine"] == ["s:0","s:1"]
    target = build_graph(cfg["domain"]["profile"])
    counts["new_graph_identities"] += 1
    leaf = cfg["domain"]["added_terminal"]
    assert len(target["vertices"]) == 15 and len(target["edges"]) == 14
    assert target["spine"] == source["spine"]
    assert target["vertices"] == [*source["vertices"],leaf]
    assert target["edges"] == [*source["edges"],["b:1:0",leaf]]
    assert all(target["roles"][v] == source["roles"][v] for v in source["vertices"])
    labels = source_cert["labels"]
    assert [labels[v] for v in source["spine"]] == [0,13] and labels["b:1:0"] == 1
    return target, labels | {"s:1":14,leaf:13}


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


def retained_positive(original, cert, cfg, counts):
    graph, digest = original["graph"], original["graph_digest"]
    assert graph["profile"] == [[4,3],[2]] and digest == graph_digest(graph) == cfg["source_digest"]
    assert cert["graph_digest"] == digest and cert["ledger_id"] == cfg["source_ledger"]
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, cert["labels"], digest)
    assert checked["valid"] and checked == cert["checker"]
    return {"graph_digest":digest,"ledger_id":cert["ledger_id"],"checker":checked}


def adverse_controls(graph, labels, digest, domain, counts):
    counts["adverse_controls"] += 1
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]

    counts["adverse_controls"] += 1
    u,v = "l:0:0:0","l:0:1:0"
    cross = labels | {u:labels[v],v:labels[u]}
    assert sorted(cross.values()) == list(range(15))
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
    domain = cfg["domain"]
    assert domain == {"profile":[[4,3],[3]],"physical_spine_labels":[0,14],"added_terminal":"l:1:0:2",
                      "reversed_edge":{"edge":["l:0:0:3","b:0:0"],"signed_difference":-1}}
    source_original = read_json(ROOT / cfg["source_original"])
    source_record = read_json(ROOT / cfg["source_result"])
    source_raw_hash = digest_file(ROOT / cfg["source_original"])
    assert source_record["status"] == "PASS" and source_record["proof_disposition"] == "ACCEPT"
    assert source_record["target_original_sha256"] == source_raw_hash
    source_cert = source_record["certificate"]
    history = {key:read_json(ROOT/path)["status"] for key,path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    retained = retained_positive(source_original, source_cert, cfg, counts)
    graph, labels = extend_certificate(source_original["graph"], source_cert, cfg, counts)
    digest = graph_digest(graph)
    assert digest != source_original["graph_digest"]
    original = {"graph":graph,"graph_digest":digest}
    interface = inspect_signed_interface(graph, labels)
    require_signed_interface(interface, domain)
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"] and (checked["n"],checked["m"]) == (15,14)
    ledger_raw = json.dumps({"graph_digest":digest,"labels":sorted(labels.items())},
                            sort_keys=True,separators=(",",":")).encode()
    certificate = {"kind":"ordinary_graceful","graph_digest":digest,"labels":labels,
                   "ledger_id":sha256(ledger_raw).hexdigest(),"checker":checked,
                   "physical_spine":graph["spine"],"signed_interface":interface}
    counts["new_certificates"] += 1
    probes = adverse_controls(graph, labels, digest, domain, counts)
    incidence = audit.certificate_audit(source_original, source_cert, original, certificate)
    control_audit = audit.controls(original, certificate, probes, retained, incidence)
    return original, {"status":"PASS","proof_disposition":"ACCEPT","state_disposition":"ACCEPT",
                      "task":cfg["task"],"parent":cfg["parent"],"domain":domain,"runtime":runtime,
                      "target_graph_digest":digest,"source_original_sha256":source_raw_hash,
                      "source_graph_digest":source_original["graph_digest"],"source_ledger_id":source_cert["ledger_id"],
                      "certificate":certificate,"incidence_audit":incidence,"retained_positive":retained,
                      "adverses":probes,"control_audit":control_audit,"retained_execution_statuses":history}


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
        original, result = produce(cfg, counts)
        assert all(value <= limits[key] for key, value in counts.items())
        assert counts["new_certificates"] == counts["new_graph_identities"] == 1
        assert (counts["retained_positive_rechecks"], counts["adverse_controls"]) == (1, 3)
        if process_time()-CPU_START >= limits["process_cpu_seconds"] or perf_counter()-WALL_START >= limits["wall_seconds"]:
            raise TimeoutError("Official time cap exceeded")
        receipt["original_sha256"] = write_record("original.json", original, limits)
        result["target_original_sha256"] = receipt["original_sha256"]
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
