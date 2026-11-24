"""Verify one binary self-composition of the independently supplied D094 state."""

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


def d094_labels(a, b, c, d):
    if any(type(q) is not int or q < 2 for q in (a, b, c, d)):
        raise ValueError("D094 quotas must be exact integers at least two")
    n, p_B = a+b+c+d+40, a+b+9
    spine = (3, n-1, a+8, n-6, p_B+5, p_B+c+19, p_B+10, p_B+14)
    labels = {f"s:{i}": label for i, label in enumerate(spine)}
    groups = (
        (0, 0, 2, n-4, 1), (0, 1, a, n-5, 4), (1, 0, 2, 0, n-3),
        (2, 0, 3, n-10, a+5), (2, 1, b, n-11, a+9), (3, 0, 3, a+4, n-9),
        (4, 0, 3, p_B+c+15, p_B+2), (5, 0, 3, p_B+1, p_B+c+16),
        (5, 1, d, p_B, p_B+c+20), (6, 0, 2, p_B+11, p_B+8),
        (7, 0, 2, p_B+7, p_B+12), (7, 1, c, p_B+6, p_B+15),
    )
    for section, branch, quota, center, first_terminal in groups:
        labels[f"b:{section}:{branch}"] = center
        for k in range(quota):
            labels[f"l:{section}:{branch}:{k}"] = first_terminal+k
    return labels


def shift_section(name):
    kind, raw_section, *indices = name.split(":")
    return ":".join([kind, str(int(raw_section)+8), *indices])


def retained_control(cfg, supplies):
    folder = ROOT / cfg["retained"]["D094"]
    original = read(folder / "original.json")
    report = read(folder / "result.json")
    receipt = read(folder / "command_receipt.json")
    certificate = report["certificate"]
    graph, digest = original["graph"], original["graph_digest"]
    assert report["boundary"] == [2, 2, 2, 2]
    assert graph["profile"] == [[2, 2], [2], [3, 2], [3], [3], [3, 2], [2], [2, 2]]
    assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert receipt["result_sha256"] == hash_file(folder / "result.json")
    labels = certificate["labels"]
    assert supplies["B"] == supplies["A"] == labels and certificate["graph_digest"] == digest
    check = verify_certificate(graph, labels, digest)
    assert check["valid"] and check == certificate["checker"]
    assert certificate["cut"] == 24 and certificate["offsets"] == [3, 3]
    assert require_ports(original, labels, certificate["ports"], 24, [3, 3]) == [3, 3]
    assert all((labels[u] < 24) != (labels[v] < 24) for u, v in graph["edges"])
    assert certificate["ledger_id"] == ledger_id(digest, labels)
    return {"graph_digest": digest, "ledger_id": certificate["ledger_id"], "checker": check}, graph


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


def compose(original, supplies, retained_graph, parameters):
    a, b, c, d, e, f, g, h = parameters
    p_B, p_A, n_A = a+b+20, e+f+20, e+f+g+h+40
    graph = original["graph"]
    later = {v: shift_section(v) for v in supplies["A"]}
    old = supplies["B"]
    new = {later[v]: label for v, label in supplies["A"].items()}
    blocks = {"B": {"source": "D094", "labels": old, "cut": p_B, "witness": retained_graph["spine"]},
              "A": {"source": "D094", "labels": new, "cut": p_A,
                    "witness": [later[v] for v in retained_graph["spine"]]}}
    connector = ["s:7", "s:8"]
    interface_gate(graph, blocks, connector)
    old_edges = retained_graph["edges"]
    expected = old_edges + [[later[u], later[v]] for u, v in old_edges] + [connector]
    assert Counter(tuple(sorted(edge)) for edge in graph["edges"]) == Counter(tuple(sorted(edge)) for edge in expected)
    labels = {v: label+(n_A if label >= p_B else 0) for v, label in old.items()}
    labels.update({v: label+p_B for v, label in new.items()})
    cut = p_B+p_A
    returned_ports = ["s:0", "s:15"]
    offsets = require_ports(original, labels, returned_ports, cut, [3, 3])
    assert all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    check = verify_certificate(graph, labels, original["graph_digest"])
    assert check["valid"], check
    declared = {"A_internal": list(range(1, n_A)), "connector": [n_A],
                "B_internal": list(range(n_A+1, len(graph["vertices"])))}
    inventory = inventory_gate(graph, labels, blocks, connector, declared)
    assert inventory["unused_labels"] == inventory["unused_differences"] == []
    return {"labels": labels, "graph_digest": original["graph_digest"],
            "ledger_id": ledger_id(original["graph_digest"], labels),
            "checker": check, "cut": cut, "ports": returned_ports, "offsets": offsets,
            "spine_labels": [labels[v] for v in graph["spine"]], "witness": graph["spine"],
            "blocks": blocks, "A_name_embedding": later, "inventories": inventory,
            "connector": {"edge": connector, "weight": abs(labels["s:7"]-labels["s:8"])},
            "edge_rows": [[u, v, w] for (u, v), w in zip(graph["edges"], check["edge_differences"], strict=True)]}


def adverse_controls(original, cert):
    graph, labels = original["graph"], cert["labels"]
    wrong_digest = "0"*64
    rejected = verify_certificate(graph, labels, wrong_digest)
    assert not rejected["valid"] and rejected["errors"] == ["original graph digest mismatch"]
    wrong_connector = ["s:7", "s:9"]
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
    assert cfg["boundary"] == [2]*8
    assert cfg["domain"] == {"minimum_quota": 2, "exact_integers": True, "parameters": list("abcdefgh")}
    assert cfg["orientation"] == {"old_B": "D094", "new_A": "D094"} and cfg["connector"] == ["s:7", "s:8"]
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
    a, b, c, d, e, f, g, h = cfg["boundary"]
    graph = build_graph([[2, a], [2], [3, b], [3], [3], [3, d], [2], [2, c],
                         [2, e], [2], [3, f], [3], [3], [3, h], [2], [2, g]])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    supplies = {"B": d094_labels(a, b, c, d), "A": d094_labels(e, f, g, h)}
    control, retained_graph = retained_control(cfg, supplies)
    cert = compose(original, supplies, retained_graph, cfg["boundary"])
    adverse = adverse_controls(original, cert)
    report = audit.check(ROOT, HERE, cfg, cert, control, adverse)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "boundary": cfg["boundary"], "certificate": cert, "runtime": runtime, "original_sha256": original_hash,
            "source_hashes": cfg["source_hashes"], "controls": {"D094": control}, "adverse": adverse, "audit": report}


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
                                 retained_positive_rechecks=1, component_embeddings=2, adverse_checks=3)
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
