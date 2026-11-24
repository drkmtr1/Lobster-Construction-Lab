"""Single bounded producer and independent-audit invocation for D108."""

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


def structural_cases(counts):
    # The proof exhausts the cases by bounds on the two left centers.
    counts["structural_cases"] += 1
    case_one = {"rhs":142,"other_right_upper_bound":12,"center_expression_lower_bound":142-2*12,
                "even_pair_upper_bound":7*10+5*8,"other_odd_pair_upper_bound":7*11+5*7,"survivors":[]}
    for a,b in ((11,9),(9,11)):
        twice_q = case_one["rhs"]-7*a-5*b
        q, rem = divmod(twice_q,2)
        assert rem == 0 and q-1 == b
        case_one["survivors"].append({"A":a,"B":b,"P":13,"Q":q,"repeated_weight":q-1})
        counts["surviving_scalar_rows"] += 1

    counts["structural_cases"] += 1
    counts["surviving_scalar_rows"] += 1
    case_two = {"A":12,"B":10,"rhs":168-7*12,"right_sum_upper_bound":11+10,
                "forced_right_sum":(168-7*12-5*10)//2,
                "first_left_weight_if_11":12-11,"second_left_signed_if_11":10-11,
                "repeated_weight":11-1}
    return {"label_13_right_terminal":case_one,"label_13_designated_terminal":case_two}


def produce(cfg, counts):
    runtime = validate_inputs(cfg)
    domain = cfg["domain"]
    assert domain == {"profile":[[5,3],[2]],"physical_spine_labels":[0,14],"right_center_label":1,
                      "reversed_edge":{"edge":["l:0:0:3","b:0:0"],"signed_difference":-1}}
    history = {key:read_json(ROOT/path)["status"] for key,path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    source = read_json(ROOT/cfg["source_original"])
    source_digest = source["graph_digest"]
    assert source_digest == graph_digest(source["graph"]) == cfg["source_digest"]
    graph = build_graph(domain["profile"])
    counts["new_graph_identities"] += 1
    digest = graph_digest(graph)
    assert digest != cfg["source_digest"]
    original = {"graph":graph,"graph_digest":digest}
    rows = structural_cases(counts)
    structural = audit.obstruction(source, original, domain, rows)

    binding = cfg["positive"]
    assert binding["r"] == 3
    control_original = read_json(ROOT/binding["original"])
    control_record = read_json(ROOT/binding["result"])
    assert control_record["status"] == "PASS" and control_record["proof_disposition"] == "ACCEPT"
    assert digest_file(ROOT/binding["original"]) == control_record["target_original_sha256"]
    positive = retained_positive(control_original, control_record, binding, counts)
    cert = control_record["certificate"]
    reversal = {"edge":["l:0:0:3","b:0:0"],"signed_difference":-1}
    interface = {"physical_spine_labels":[0,14],"reversed_edge":reversal}
    require_signed_interface(inspect_signed_interface(control_original["graph"],cert["labels"]),interface)
    probes = adverse_controls(control_original["graph"],cert["labels"],control_original["graph_digest"],interface,counts)
    checked = audit.controls(control_original, cert, probes, positive)
    return original, {"status":"PASS","proof_disposition":"ACCEPT","interface_disposition":"REJECT",
                      "task":cfg["task"],"parent":cfg["parent"],"domain":domain,"runtime":runtime,
                      "source_graph_digest":source_digest,"target_graph_digest":digest,
                      "structural_cases":rows,"structural_audit":structural,"retained_positive":positive,
                      "adverses":probes,"control_audit":checked,"retained_execution_statuses":history}


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
        assert counts["new_certificates"] == 0 and counts["new_graph_identities"] == 1
        assert (counts["structural_cases"],counts["surviving_scalar_rows"]) == (2,3)
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
