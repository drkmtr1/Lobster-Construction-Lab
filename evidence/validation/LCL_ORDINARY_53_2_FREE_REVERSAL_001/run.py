"""Single bounded producer and independent-audit invocation for D109."""

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


def signed_interface_gate(graph, labels):
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
    assert graph["spine"] == ["s:0","s:1"]
    expected_pins = {"s:0":0,"s:1":14,"b:1:0":1}
    pins = {v:labels[v] for v in expected_pins}
    actual_left = set()
    for leaf, role in graph["roles"].items():
        if role["kind"] == "leaf" and role["section"] == 0:
            center = f"b:0:{role['branch']}"
            if adjacent[leaf] == [center] and colors[leaf] == 0 and colors[center] == 1:
                actual_left.add((leaf,center))
    signed_tests = {"one_negative_edge":len(negatives)==1,
                    "negative_magnitude_one":bool(negatives) and all(row["signed_difference"]==-1 for row in negatives),
                    "negative_edges_are_left_terminal_incidence":bool(negatives) and all(
                        tuple(row["edge"]) in actual_left for row in negatives)}
    pins_valid = pins == expected_pins
    pattern_valid = all(signed_tests.values())
    return {"physical_pins":pins,"negative_edges":negatives,"pins_valid":pins_valid,
            "signed_tests":signed_tests,"pattern_valid":pattern_valid,"valid":pins_valid and pattern_valid}


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


def run_controls(graph, labels, digest, counts):
    counts["declared_controls"] += 1
    wrong_digest = verify_certificate(graph, labels, "0"*64)
    assert not wrong_digest["valid"] and wrong_digest["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    u,v = "l:0:0:0","l:0:1:0"
    cross = labels | {u:labels[v],v:labels[u]}
    assert sorted(cross.values()) == sorted(labels.values())
    cross_check = verify_certificate(graph, cross, digest)
    assert not cross_check["valid"]
    assert cross_check["errors"] == ["edge differences repeat","edge differences are not exactly 1..m"]

    counts["declared_controls"] += 1
    w = "l:0:0:3"
    within = labels | {u:labels[w],w:labels[u]}
    within_check = verify_certificate(graph, within, digest)
    within_gate = signed_interface_gate(graph, within)
    assert within_check["valid"] and within_gate["valid"]

    counts["declared_controls"] += 1
    maximum = len(graph["edges"])
    complement = {v:maximum-value for v,value in labels.items()}
    complement_check = verify_certificate(graph, complement, digest)
    complement_gate = signed_interface_gate(graph, complement)
    assert complement_check["valid"]
    assert not complement_gate["pins_valid"] and not complement_gate["pattern_valid"]
    assert not complement_gate["valid"]
    return {"wrong_digest":{"expected":"0"*64,"checker":wrong_digest},
            "cross_swap":{"vertices":[u,v],"labels":cross,"checker":cross_check},
            "within_swap":{"vertices":[u,w],"labels":within,"checker":within_check,"gate":within_gate},
            "complement":{"labels":complement,"checker":complement_check,"gate":complement_gate}}


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
    counts["structural_cases"] += 1
    right_case = {"rhs":142,"other_right_upper_bound":12,"center_expression_lower_bound":118,
                  "even_pair_upper_bound":110,"other_odd_pair_upper_bound":112,"survivors":[]}
    for a,b in ((11,9),(9,11)):
        q, rem = divmod(right_case["rhs"]-7*a-5*b,2)
        assert rem==0 and q-1==b
        right_case["survivors"].append({"A":a,"B":b,"P":13,"Q":q,"repeated_weight":b})
        counts["surviving_scalar_rows"] += 1

    counts["structural_cases"] += 2
    counts["surviving_scalar_rows"] += 2
    first_case = {"A":12,"B":10,"rhs":84,"right_sum_upper_bound":21,"forced_right_sum":17,
                  "first_left_signed_if_11":1,"second_left_signed_if_11":-1,"repeated_weight":10}
    second_case = {"A":10,"B":12,"rhs":108,"right_sum_upper_bound":21,"forced_right_sum":19,
                   "first_left_signed_if_11":-1,"second_left_signed_if_11":1,"repeated_weight":10}
    return {"label_13_right_terminal":right_case,
            "label_13_first_left_reversal":first_case,"label_13_second_left_reversal":second_case}


def produce(cfg, counts):
    runtime = validate_inputs(cfg)
    domain = cfg["domain"]
    assert domain == {"profile":[[5,3],[2]],"physical_pins":{"s:0":0,"s:1":14,"b:1:0":1},
                      "negative_edge_count":1,"negative_signed_difference":-1,"location":"any_left_terminal"}
    history = {key:read_json(ROOT/path)["status"] for key,path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    original = read_json(ROOT/cfg["target_original"])
    digest = original["graph_digest"]
    assert digest == graph_digest(original["graph"]) == cfg["target_digest"]
    original_hash = digest_file(ROOT/cfg["target_original"])
    prior = read_json(ROOT/cfg["prior_result"])
    assert prior["status"]=="PASS" and prior["proof_disposition"]=="ACCEPT"
    assert prior["interface_disposition"]=="REJECT" and prior["target_original_sha256"]==original_hash
    assert prior["target_graph_digest"]==digest
    rows = structural_cases(counts)
    structural = audit.obstruction(original, domain, rows)

    binding = cfg["positive"]
    assert binding["r"] == 3
    control_original = read_json(ROOT/binding["original"])
    control_record = read_json(ROOT/binding["result"])
    assert control_record["status"]=="PASS" and control_record["proof_disposition"]=="ACCEPT"
    assert digest_file(ROOT/binding["original"])==control_record["target_original_sha256"]
    positive = retained_positive(control_original, control_record, binding, counts)
    cert = control_record["certificate"]
    gate = signed_interface_gate(control_original["graph"],cert["labels"])
    assert gate["valid"]
    positive["signed_gate"] = gate
    controls = run_controls(control_original["graph"],cert["labels"],control_original["graph_digest"],counts)
    checked = audit.controls(control_original,cert,controls,positive)
    return {"status":"PASS","proof_disposition":"ACCEPT","interface_disposition":"REJECT",
            "task":cfg["task"],"parent":cfg["parent"],"domain":domain,"runtime":runtime,
            "target_original_sha256":original_hash,"target_graph_digest":digest,"structural_cases":rows,
            "structural_audit":structural,"retained_positive":positive,"controls":controls,
            "control_audit":checked,"retained_execution_statuses":history}


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
        assert (counts["structural_cases"],counts["surviving_scalar_rows"]) == (3,4)
        assert (counts["retained_positive_rechecks"], counts["declared_controls"]) == (1,4)
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
