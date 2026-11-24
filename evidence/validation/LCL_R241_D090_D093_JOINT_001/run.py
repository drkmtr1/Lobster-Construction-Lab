"""Verify the one D094 binary composition and its retained originals."""

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


def shift_section(name, amount):
    kind, raw_section, *indices = name.split(":")
    return ":".join([kind, str(int(raw_section)+amount), *indices])


def d093_labels(c, d):
    source = d090_labels(c, d)
    cut = c+d+9
    return {reverse_section(v): label-cut if label >= cut else label+11
            for v, label in source.items()}


def retained_controls(cfg, supplies):
    controls = {}
    graphs = {}
    for source, profile, cut, offsets in (
            ("D090", [[2, 2], [2], [3, 2], [3]], 13, [3, 5]),
            ("D093", [[3], [3, 2], [2], [2, 2]], 11, [5, 3])):
        folder = ROOT / cfg["retained"][source]
        original = read(folder / "original.json")
        report = read(folder / "result.json")
        receipt = read(folder / "command_receipt.json")
        cert = report["certificate"]
        graph, digest = original["graph"], original["graph_digest"]
        assert report["boundary"] == [2, 2] and graph["profile"] == profile
        assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
        assert receipt["result_sha256"] == hash_file(folder / "result.json")
        labels = supplies[source]
        assert labels == cert["labels"] and cert["graph_digest"] == digest
        check = verify_certificate(graph, labels, digest)
        assert check["valid"] and check == cert["checker"]
        assert cert["cut"] == cut and cert["offsets"] == offsets
        assert require_ports(original, labels, cert["ports"], cut, offsets) == offsets
        assert all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
        assert cert["ledger_id"] == ledger_id(digest, labels)
        controls[source] = {"graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": check}
        graphs[source] = graph
    return controls, graphs


def interface_gate(graph, blocks, declared):
    old, new = blocks["B"], blocks["A"]
    names_B, names_A = old["labels"].keys(), new["labels"].keys()
    if names_B & names_A or names_B | names_A != set(graph["vertices"]):
        raise ValueError("components must partition the target names")
    if old["witness"] + new["witness"] != graph["spine"]:
        raise ValueError("component witnesses must concatenate in target spine order")
    expected = [old["witness"][-1], new["witness"][0]]
    if declared != expected:
        raise ValueError("connector must be the actual U_B--L_A spine edge")
    cross = [[u, v] for u, v in graph["edges"] if (u in names_B) != (v in names_B)]
    if cross != [expected]:
        raise ValueError("expected exactly the declared original connector")
    if old["labels"][expected[0]]-old["cut"] != new["labels"][expected[1]]:
        raise ValueError("physical port offsets do not match")


def inventory_gate(graph, labels, blocks, connector, declared):
    old, new = blocks["B"], blocks["A"]
    p_B, p_A = old["cut"], new["cut"]
    n_A, m = len(new["labels"]), len(graph["edges"])
    collected_labels = {"B_low": [], "A_low": [], "A_high": [], "B_high": []}
    for key, block in blocks.items():
        for vertex, local_value in block["labels"].items():
            band = "low" if local_value < block["cut"] else "high"
            collected_labels[f"{key}_{band}"].append(labels[vertex])
    label_bands = {key: sorted(values) for key, values in collected_labels.items()}
    cut = p_B+p_A
    if label_bands != {"B_low": list(range(p_B)), "A_low": list(range(p_B, cut)),
                       "A_high": list(range(cut, p_B+n_A)), "B_high": list(range(p_B+n_A, m+1))}:
        raise ValueError("R241 label bands do not partition the alphabet")
    collected_weights = {"A_internal": [], "connector": [], "B_internal": []}
    for u, v in graph["edges"]:
        group = "connector" if [u, v] == connector else (
            "B_internal" if u in old["labels"] and v in old["labels"] else "A_internal")
        collected_weights[group].append(abs(labels[u]-labels[v]))
    difference_bands = {key: sorted(values) for key, values in collected_weights.items()}
    if declared != difference_bands:
        raise ValueError("claimed difference inventory disagrees with the original edges")
    if difference_bands != {"A_internal": list(range(1, n_A)), "connector": [n_A],
                            "B_internal": list(range(n_A+1, m+1))}:
        raise ValueError("R241 difference bands do not partition the alphabet")
    return {"labels": label_bands, "differences": difference_bands,
            "unused_labels": sorted(set(range(m+1))-set(labels.values())),
            "unused_differences": sorted(set(range(1, m+1))-{w for band in difference_bands.values() for w in band})}


def compose(original, supplies, sources, parameters):
    a, b, c, d = parameters
    p_B, n_A = a+b+9, c+d+20
    graph = original["graph"]
    later = {v: shift_section(v, 4) for v in supplies["D093"]}
    old = supplies["D090"]
    new = {later[v]: label for v, label in supplies["D093"].items()}
    blocks = {"B": {"source": "D090", "labels": old, "cut": p_B, "witness": sources["D090"]["spine"]},
              "A": {"source": "D093", "labels": new, "cut": 11,
                    "witness": [later[v] for v in sources["D093"]["spine"]]}}
    connector = ["s:3", "s:4"]
    interface_gate(graph, blocks, connector)
    expected = sources["D090"]["edges"] + [[later[u], later[v]] for u, v in sources["D093"]["edges"]] + [connector]
    assert Counter(tuple(sorted(edge)) for edge in graph["edges"]) == Counter(tuple(sorted(edge)) for edge in expected)
    labels = {v: label+(n_A if label >= p_B else 0) for v, label in old.items()}
    labels.update({v: label+p_B for v, label in new.items()})
    cut = p_B+11
    returned_ports = ["s:0", "s:7"]
    offsets = require_ports(original, labels, returned_ports, cut, [3, 3])
    assert all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    check = verify_certificate(graph, labels, original["graph_digest"])
    assert check["valid"], check
    declared = {"A_internal": list(range(1, n_A)), "connector": [n_A],
                "B_internal": list(range(n_A+1, a+b+c+d+40))}
    inventory = inventory_gate(graph, labels, blocks, connector, declared)
    assert inventory["unused_labels"] == inventory["unused_differences"] == []
    return {"labels": labels, "graph_digest": original["graph_digest"],
            "ledger_id": ledger_id(original["graph_digest"], labels),
            "checker": check, "cut": cut, "ports": returned_ports, "offsets": offsets,
            "spine_labels": [labels[v] for v in graph["spine"]], "witness": graph["spine"],
            "blocks": blocks, "A_name_embedding": later, "inventories": inventory,
            "connector": {"edge": connector, "weight": abs(labels["s:3"]-labels["s:4"])},
            "edge_rows": [[u, v, w] for (u, v), w in zip(graph["edges"], check["edge_differences"], strict=True)]}


def adverse_controls(original, cert):
    graph, labels = original["graph"], cert["labels"]
    wrong_digest = "0"*64
    rejected = verify_certificate(graph, labels, wrong_digest)
    assert not rejected["valid"] and rejected["errors"] == ["original graph digest mismatch"]
    wrong_connector = ["s:3", "s:5"]
    try:
        interface_gate(graph, cert["blocks"], wrong_connector)
    except ValueError as exc:
        assert str(exc) == "connector must be the actual U_B--L_A spine edge"
        connector = {"declared": wrong_connector, "valid": False, "error": str(exc)}
    else:
        raise AssertionError("wrong physical connector was accepted")
    wrong_inventory = cert["inventories"]["differences"] | {"connector": []}
    try:
        inventory_gate(graph, labels, cert["blocks"], cert["connector"]["edge"], wrong_inventory)
    except ValueError as exc:
        assert str(exc) == "claimed difference inventory disagrees with the original edges"
        inventory = {"declared": wrong_inventory, "valid": False, "error": str(exc)}
    else:
        raise AssertionError("omitted connector difference was accepted")
    return {"digest": {"expected": wrong_digest, "checker": rejected},
            "physical_connector": connector, "difference_inventory": inventory}


def verify_inputs(cfg):
    assert cfg["boundary"] == [2, 2, 2, 2]
    assert cfg["domain"] == {"minimum_quota": 2, "exact_integers": True, "parameters": ["a", "b", "c", "d"]}
    assert cfg["orientation"] == {"old_B": "D090", "new_A": "D093"} and cfg["connector"] == ["s:3", "s:4"]
    assert cfg["limits"] == {
        "workers": 1, "symbolic_families": 1, "max_new_original_identities": 1, "connectors": 1,
        "max_new_certificates": 1, "assignment_visits": 0, "recorded_assignment_states": 0,
        "search_nodes": 0, "solver_calls": 0, "adverse_checks": 3,
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
    a, b, c, d = cfg["boundary"]
    graph = build_graph([[2, a], [2], [3, b], [3], [3], [3, d], [2], [2, c]])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    supplies = {"D090": d090_labels(a, b), "D093": d093_labels(c, d)}
    controls, sources = retained_controls(cfg, supplies)
    cert = compose(original, supplies, sources, cfg["boundary"])
    adverse = adverse_controls(original, cert)
    report = audit.check(ROOT, HERE, cfg, cert, controls, adverse)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "boundary": cfg["boundary"], "certificate": cert, "runtime": runtime, "original_sha256": original_hash,
            "source_hashes": cfg["source_hashes"], "controls": controls, "adverse": adverse, "audit": report}


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
               "counts": {"official_sequences": 1, "workers": 1,
                          "named_assignment_visits": 0, "recorded_assignment_states": 0, "search_nodes": 0,
                          "solver_calls": 0, "replays": 0, "retries": 0, "restarts": 0}}
    try:
        result = main(cfg)
        if process_time() - START >= limits["cpu_seconds"]:
            raise TimeoutError("Verification process CPU budget reached")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        receipt.update(status="PASS", exit_code=0)
        receipt["counts"].update(symbolic_families=1, new_certificates=1, connectors=1, joins=1,
                                 retained_positive_rechecks=2, adverse_checks=3)
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
