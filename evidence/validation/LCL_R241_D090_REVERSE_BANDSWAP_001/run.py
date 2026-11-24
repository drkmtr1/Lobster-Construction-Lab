"""Verify the sole D093 reversal certificate and its retained D090 source."""

from time import process_time

START = process_time()

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
import subprocess
from time import perf_counter
import traceback

from collections import Counter

import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def read(path):
    return json.loads(path.read_bytes())


def hash_file(path):
    return sha256(path.read_bytes()).hexdigest()


def ledger_id(digest, labels):
    data = {"graph_digest": digest, "labels": sorted(labels.items())}
    return sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def require_ports(original, labels, port_names, cut, offsets):
    spine = original["graph"]["spine"]
    if port_names != [spine[0], spine[-1]]:
        raise ValueError("physical endpoint names mismatch")
    actual = [labels[port_names[0]], labels[port_names[1]]-cut]
    if offsets != actual:
        raise ValueError("physical offset mismatch")
    return actual


def d090_labels(a, b):
    if type(a) is not int or type(b) is not int or a < 2 or b < 2:
        raise ValueError("both quotas must be integers at least two")
    labels = {"s:0": 3, "s:1": a+b+19, "s:2": a+8, "s:3": a+b+14,
              "b:0:0": a+b+16, "b:0:1": a+b+15, "b:1:0": 0,
              "b:2:0": a+b+10, "b:2:1": a+b+9, "b:3:0": a+4}
    terminal_groups = ((0, 0, 2, 1), (0, 1, a, 4), (1, 0, 2, a+b+17),
                       (2, 0, 3, a+5), (2, 1, b, a+9), (3, 0, 3, a+b+11))
    for section, branch, quota, first in terminal_groups:
        for j in range(quota):
            labels[f"l:{section}:{branch}:{j}"] = first+j
    return labels


def reverse_section(name):
    kind, raw_section, *indices = name.split(":")
    return ":".join([kind, str(3-int(raw_section)), *indices])


def source_control(cfg, labels):
    folder = ROOT / cfg["retained"]["D090"]
    original = read(folder / "original.json")
    report = read(folder / "result.json")
    receipt = read(folder / "command_receipt.json")
    cert = report["certificate"]
    assert report["boundary"] == [2, 2] and original["graph"]["profile"] == [[2, 2], [2], [3, 2], [3]]
    assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert receipt["result_sha256"] == hash_file(folder / "result.json")
    assert cert["labels"] == labels
    checked = verify_certificate(original["graph"], labels, original["graph_digest"])
    assert checked["valid"] and checked == cert["checker"]
    assert cert["graph_digest"] == original["graph_digest"]
    assert cert["ledger_id"] == ledger_id(original["graph_digest"], labels)
    assert cert["cut"] == 13
    assert require_ports(original, labels, cert["ports"], 13, cert["offsets"]) == [3, 5]
    return original, {"graph_digest": original["graph_digest"], "ledger_id": cert["ledger_id"], "checker": checked}


def inventories(graph, labels, weights, cut):
    m = len(graph["edges"])
    difference_bands = {"former_D087": [], "connector": [], "former_D089": []}
    for (u, v), weight in zip(graph["edges"], weights, strict=True):
        left, right = graph["roles"][u]["section"], graph["roles"][v]["section"]
        if left >= 2 and right >= 2:
            group = "former_D087"
        elif left < 2 and right < 2:
            group = "former_D089"
        else:
            assert [u, v] == ["s:1", "s:2"]
            group = "connector"
        difference_bands[group].append(weight)
    return {"low_labels": sorted(x for x in labels.values() if x < cut),
            "high_labels": sorted(x for x in labels.values() if x >= cut),
            "difference_bands": {key: sorted(values) for key, values in difference_bands.items()},
            "unused_labels": sorted(set(range(m+1))-set(labels.values())),
            "unused_differences": sorted(set(range(1, m+1))-set(weights))}


def target_certificate(original, source, f, a, b):
    graph = original["graph"]
    order, old_cut = a+b+20, a+b+9
    cut = order-old_cut
    name_map = {v: reverse_section(v) for v in source["graph"]["vertices"]}
    assert name_map.keys() == f.keys() and len(set(name_map.values())) == order
    assert set(name_map.values()) == set(graph["vertices"])
    labels = {name_map[v]: label-old_cut if label >= old_cut else label+cut for v, label in f.items()}
    offsets = require_ports(original, labels, ["s:0", "s:3"], cut, [5, 3])
    checked = verify_certificate(graph, labels, original["graph_digest"])
    assert checked["valid"] and all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    weights = checked["edge_differences"]
    ledger = inventories(graph, labels, weights, cut)
    assert ledger["low_labels"] == list(range(11)) and ledger["high_labels"] == list(range(11, order))
    assert ledger["difference_bands"] == {"former_D087": list(range(1, a+9)), "connector": [a+9],
                                           "former_D089": list(range(a+10, order))}
    assert ledger["unused_labels"] == ledger["unused_differences"] == []
    source_edges = source["graph"]["edges"]
    expected_edges = Counter(tuple(sorted([name_map[u], name_map[v]])) for u, v in source_edges)
    assert expected_edges == Counter(tuple(sorted(edge)) for edge in graph["edges"])
    return {"labels": labels, "checker": checked, "graph_digest": original["graph_digest"],
            "ledger_id": ledger_id(original["graph_digest"], labels),
            "spine_labels": [labels[v] for v in graph["spine"]], "cut": cut, "offsets": offsets,
            "ports": ["s:0", "s:3"], "witness": graph["spine"], "source_cut": old_cut,
            "connector": {"edge": ["s:1", "s:2"], "weight": abs(labels["s:1"]-labels["s:2"])},
            "name_map": name_map, "inventories": ledger,
            "edge_rows": [[u, v, w] for (u, v), w in zip(graph["edges"], weights, strict=True)]}


def adverse_controls(original, cert):
    graph, labels = original["graph"], cert["labels"]
    wrong_digest = "0"*64
    rejected_digest = verify_certificate(graph, labels, wrong_digest)
    assert not rejected_digest["valid"] and rejected_digest["errors"] == ["original graph digest mismatch"]
    declared = [5, 4]
    try:
        require_ports(original, labels, cert["ports"], cert["cut"], declared)
    except ValueError as exc:
        assert str(exc) == "physical offset mismatch"
        rejected_port = {"ports": cert["ports"], "cut": cert["cut"], "declared": declared,
                         "actual": cert["offsets"], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("false physical offset accepted")

    u, v = "l:0:0:0", "l:2:0:0"
    assert [labels[u], labels[v]] == [2, 8]
    swapped = labels | {u: labels[v], v: labels[u]}
    differences = Counter(abs(swapped[x]-swapped[y]) for x, y in graph["edges"])
    repeated = {str(w): count for w, count in differences.items() if count > 1}
    missing = sorted(set(range(1, len(graph["vertices"]))) - differences.keys())
    assert repeated == {"9": 3} and missing == [3, 15]
    rejected_swap = verify_certificate(graph, swapped, original["graph_digest"])
    assert not rejected_swap["valid"] and "edge differences repeat" in rejected_swap["errors"]
    return {"digest": {"expected": wrong_digest, "checker": rejected_digest},
            "physical_ports": rejected_port,
            "invalid_labeling": {"swap": [u, v], "before_labels": [labels[u], labels[v]],
                                 "repeated": repeated, "missing": missing, "checker": rejected_swap}}


def verify_inputs(cfg):
    assert cfg["boundary"] == [2, 2] and cfg["domain"] == {"min_a": 2, "min_b": 2, "exact_integers": True}
    assert cfg["limits"] == {
        "workers": 1, "symbolic_families": 1, "max_new_original_identities": 1,
        "max_new_certificates": 1, "assignment_visits": 0, "recorded_assignment_states": 0,
        "search_nodes": 0, "solver_calls": 0, "joins": 0, "adverse_checks": 3,
        "cpu_seconds": 30, "bytes_per_record": 2_000_000, "bytes_total": 8_000_000,
        "official_sequences": 1, "retries": 0, "restarts": 0, "replays": 0}
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    exe = Path(sys.executable)
    assert sys.version_info[:2] in {(3, 12), (3, 13)}
    assert hash_file(exe) == cfg["runtime_sha256"]
    for path, expected in cfg["source_hashes"].items():
        assert hash_file(ROOT / path) == expected
    return {"path": exe.relative_to(ROOT).as_posix(), "sha256": hash_file(exe), "version": sys.version}


def main(cfg):
    runtime = verify_inputs(cfg)
    a, b = cfg["boundary"]
    graph = build_graph([[3], [3, b], [2], [2, a]])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    f = d090_labels(a, b)
    source, control = source_control(cfg, f)
    cert = target_certificate(original, source, f, a, b)
    adverse = adverse_controls(original, cert)
    report = audit.check(ROOT, HERE, cfg, cert, control, adverse)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "boundary": cfg["boundary"], "certificate": cert, "runtime": runtime,
            "source_hashes": cfg["source_hashes"], "original_sha256": original_hash,
            "controls": {"D090": control, "adverse": adverse}, "audit": report}


def write_record(name, value, limits):
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if len(data) > limits["bytes_per_record"]:
        raise RuntimeError("Evidence record exceeds byte limit")
    if len(data) + sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) > limits["bytes_total"]:
        raise RuntimeError("Evidence bundle exceeds byte limit")
    with (HERE / name).open("xb") as stream:
        stream.write(data)
    return sha256(data).hexdigest()


def execute():
    if not __debug__:
        raise RuntimeError("Enabled assertions are required")
    if any((HERE / file).exists() for file in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be empty")
    started = datetime.now(timezone.utc).isoformat()
    wall_start = perf_counter()
    cfg = read(HERE / "config.json")
    limits = cfg["limits"]
    inputs = {name: hash_file(HERE / name) for name in ("run.py", "audit.py", "config.json")}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": started, "limits": limits, "local_inputs": inputs,
               "counts": {"official_sequences": 1, "workers": 1, "joins": 0,
                          "named_assignment_visits": 0, "recorded_assignment_states": 0, "search_nodes": 0,
                          "solver_calls": 0, "replays": 0, "retries": 0, "restarts": 0}}
    try:
        result = main(cfg)
        if process_time() - START >= limits["cpu_seconds"]:
            raise TimeoutError("Verification process CPU budget reached")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        receipt.update(status="PASS", exit_code=0)
        receipt["counts"].update(symbolic_families=1, new_certificates=1,
                                 retained_positive_rechecks=1, adverse_checks=3)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["counts"]["new_original_identities"] = int((HERE / "original.json").exists())
    receipt["combined_process_cpu_seconds"] = process_time() - START
    receipt["wall_seconds"] = perf_counter() - wall_start
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
