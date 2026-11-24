"""Evaluate only the prescribed maximum-host structural cases."""

from time import process_time

START = process_time()

from collections import Counter
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
    if (len(raw) > limits["bytes_per_record"]
            or len(raw)+sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) > limits["bytes_total"]):
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as out:
        out.write(raw)
    return sha256(raw).hexdigest()


def require_maximum_host(graph, labels, host, declared):
    role = {"kind": "branch", "section": 0, "branch": 1}
    if host != "b:0:1" or graph["roles"].get(host) != role or ["s:0", host] not in graph["edges"]:
        raise ValueError("Wrong physical maximum host")
    if declared != max(labels.values()) or labels[host] != declared:
        raise ValueError("The physical host does not carry the declared maximum")


def control_and_adverses(original, report, cfg):
    graph, digest = original["graph"], original["graph_digest"]
    cert = report["certificate"]
    labels = cert["labels"]
    assert report["status"] == "PASS" and cert["cut"] == 8
    assert cert["ledger_id"] == cfg["positive_ledger_id"] and cert["graph_digest"] == digest
    assert cert["witness"] == graph["spine"] == ["s:0", "s:1"]
    assert all((labels[u] < 8) != (labels[v] < 8) for u,v in graph["edges"])
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"] and checked == cert["checker"]
    bad = verify_certificate(graph, labels, "0"*64)
    assert not bad["valid"] and bad["errors"] == ["original graph digest mismatch"]
    try:
        require_maximum_host(graph, labels, "b:0:1", 12)
    except ValueError as exc:
        assert str(exc) == "The physical host does not carry the declared maximum"
        host = {"claimed_vertex": "b:0:1", "claimed_label": 12, "actual_label": labels["b:0:1"],
                "valid": False, "error": str(exc)}
    else:
        raise AssertionError("False maximum-host declaration accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    swapped = labels | {u: labels[v], v: labels[u]}
    assert sorted(swapped.values()) == list(range(13))
    corrupt_check = verify_certificate(graph, swapped, digest)
    assert not corrupt_check["valid"]
    assert corrupt_check["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return ({"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked},
            {"bad_digest": {"claimed": "0"*64, "checker": bad}, "false_maximum_host": host,
             "terminal_swap": {"vertices": [u,v], "labels": swapped, "checker": corrupt_check}})


def read_retained(cfg):
    files = cfg["retained"]
    source = load(ROOT / files["source_original"])
    target = load(ROOT / files["target_original"])
    for record, profile, digest in ((source, [[4,2],[2]], cfg["source_graph_digest"]),
                                     (target, [[4,3],[2]], cfg["target_graph_digest"])):
        assert record["graph"]["profile"] == profile and record["graph_digest"] == graph_digest(record["graph"]) == digest
    source_report = load(ROOT / files["source_result"])
    target_report = load(ROOT / files["target_result"])
    assert source_report["original_sha256"] == raw_hash(ROOT / files["source_original"])
    assert target_report["target_original_sha256"] == raw_hash(ROOT / files["target_original"])
    statuses = {key: load(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    return source, source_report, statuses


def reduce(original):
    graph = original["graph"]
    degree = Counter(v for edge in graph["edges"] for v in edge)
    low = {"s:0", "b:1:0"} | {v for v in graph["vertices"] if v.startswith("l:0:")}
    assert all((u in low) != (v in low) for u,v in graph["edges"])
    signed = {v: (1-n if v in low else n-1) for v,n in degree.items() if n != 1}
    assert signed == {"s:0":-2, "s:1":1, "b:0:0":4, "b:0:1":2, "b:1:0":-2}
    baseline = sum(range(8,13))-sum(range(8))
    total = sum(range(1,13))
    rhs = total-baseline-12*signed["b:0:1"]
    assert (baseline,total,rhs) == (22,78,32)
    exits = [v for v in range(8,12) if v % 2 == rhs % 2]
    pairs = {str(w): [[w+lo,lo] for lo in range(13-w)] for w in (12,11,10,9,8)}
    return {"degrees":dict(degree), "low_names":sorted(low), "signed_excess":signed,
            "baseline_signed_sum":baseline, "required_sum":total, "reduced_rhs":rhs,
            "possible_exits":exits, "entrance_bound":[0,2], "high_low_pairs":pairs}


def case_records(reduction):
    # A forced terminal witness is written by label and center, without an index.
    spine, left, right = "s:0--s:1", "s:0--b:0:0", "s:1--b:1:0"
    spec = {
        (0,8,9): ([], 1, []),
        (0,10,8): ([1,3], 6, ["b:0:0 to label 2", "b:1:0 to label 11"]),
        (0,10,9): ([1,4], 4, ["b:0:0 to label 5", "b:1:0 to label 11"]),
        (1,8,9): ([0,2], 9, []),
        (1,8,10): ([0,2], 7, ["b:0:0 to label 3", spine]),
        (1,10,8): ([0,2], 7, [left, "b:1:0 to label 11"]),
        (1,10,9): ([0,2], 5, ["b:0:0 to label 4", "b:1:0 to label 11"]),
        (2,8,9): ([0,1], 6, [spine, "b:1:0 to label 10"]),
        (2,8,10): ([0,1], 6, ["b:0:0 to label 4", spine]),
        (2,10,8): ([0,1], 6, [left, "b:1:0 to label 9"]),
        (2,10,9): ([0,1], 5, ["b:0:0 to label 4", right]),
    }
    rows = []
    for y in reduction["possible_exits"]:
        for a in sorted({8,9,10,11}-{y}):
            total = (4*a+y-reduction["reduced_rhs"])//2
            for x in range(max(0,total-7), min(2,total)+1):
                z = total-x
                assert x != z
                second, w, witnesses = spec[x,y,a]
                right_palette = sorted(set(range(8,13))-{y,a,12})
                fixed = {spine:y-x, left:a-x, "s:0--b:0:1":12-x, right:y-z,
                         **{f"b:1:0 to label {v}":v-z for v in right_palette}}
                first = sorted(set(range(8))-{x,z,*second}) if second else []
                forced = fixed | {f"b:0:0 to label {v}":a-v for v in first} | {f"b:0:1 to label {v}":12-v for v in second}
                repeats = {str(weight):n for weight,n in sorted(Counter(forced.values()).items()) if n > 1}
                if witnesses:
                    assert len(set(witnesses)) == 2 and all(forced[key] == w for key in witnesses)
                else:
                    assert w not in forced.values()
                rows.append({"x":x, "Y":y, "A":a, "B":12, "z":z, "right_terminal_palette":right_palette,
                             "first_terminal_palette":first, "second_terminal_palette":second,
                             "fixed_incidence_weights":fixed, "all_forced_incidence_weights":forced,
                             "repeat_multiplicities":repeats, "obstruction":{"weight":w, "witnesses":witnesses,
                             "kind":"duplicate" if witnesses else "missing"}})
    return sorted(rows, key=lambda row: (row["x"],row["Y"],row["A"]))


def inputs(cfg):
    assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip() == cfg["parent"]
    rec = load(HERE / "preflight_receipt.json")
    assert rec["status"] == "PASS" and rec["task"] == cfg["task"] and rec["parent"] == cfg["parent"]
    assert rec["input_hashes"] == {name:raw_hash(HERE/name) for name in cfg["local_inputs"]}
    assert rec["runtime"]["sha256"] == cfg["runtime_sha256"] == raw_hash(Path(sys.executable))
    for path,pin in cfg["source_hashes"].items():
        assert raw_hash(ROOT/path) == pin,path
    return rec


def produce(cfg, counts):
    rec = inputs(cfg)
    assert cfg["domain"] == {"cut":8,"host":"b:0:1","host_label":12,"free_spine_ports":True}
    source, retained, history = read_retained(cfg)
    positive, adverses = control_and_adverses(source, retained, cfg)
    counts.update(retained_positive_rechecks=1, adverse_controls=len(adverses))
    reduction = reduce(source)
    rows = case_records(reduction)
    counts["residual_scalar_cases"] = len(rows)
    assert len(rows) == cfg["limits"]["residual_scalar_cases"]
    verified = audit.check(source, retained["certificate"], reduction, rows, positive, adverses, history)
    return {"status":"PASS", "disposition":"REJECT", "proof_disposition":"ACCEPT", "task":cfg["task"],
            "parent":cfg["parent"], "runtime":rec["runtime"], "domain":cfg["domain"],
            "source_graph_digest":source["graph_digest"], "conditional_target_graph_digest":cfg["target_graph_digest"],
            "source_original_sha256":raw_hash(ROOT/cfg["retained"]["source_original"]),
            "reduction":reduction, "cases":rows, "retained_positive":positive, "adverses":adverses, "audit":verified,
            "conditional_extension":{"source_premise_supplied":False, "executed":False, "target_certificate":None}}


def execute():
    if not __debug__ or not sys.dont_write_bytecode:
        raise RuntimeError("Use enabled assertions and -B")
    if any((HERE/name).exists() for name in ("original.json","result.json","command_receipt.json","__pycache__")):
        raise FileExistsError("Official output paths must be vacant")
    cfg = load(HERE/"config.json")
    limits = cfg["limits"]
    counts = {"official_sequences":1,"workers":1,"new_original_identities":0,"residual_scalar_cases":0,
              "retained_positive_rechecks":0,"adverse_controls":0,"source_certificates":0,
              "conditional_target_certificates":0,"conditional_extensions":0,"solver_calls":0,
              "assignment_visits":0,"search_nodes":0,"assignment_states":0,"port_sweeps":0,
              "joins":0,"retries":0,"restarts":0,"historical_replays":0}
    receipt = {"task":cfg["task"],"parent":cfg["parent"],"argv":sys.orig_argv,
               "started_utc":datetime.now(timezone.utc).isoformat(),"counts":counts,"limits":limits,
               "inputs":{name:raw_hash(HERE/name) for name in (*cfg["local_inputs"],"preflight_receipt.json")}}
    try:
        report = produce(cfg, counts)
        if process_time()-START >= limits["process_cpu_seconds"]:
            raise TimeoutError("Process-CPU cap exceeded")
        receipt["result_sha256"] = write_record("result.json",report,limits)
        receipt.update(status="PASS",exit_code=0)
    except (Exception,KeyboardInterrupt):
        receipt.update(status="INCOMPLETE",exit_code=1,error=traceback.format_exc())
    receipt["process_cpu_seconds"] = process_time()-START
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json",receipt,limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
