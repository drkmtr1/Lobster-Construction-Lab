"""Verify the D090 R241 composition on the sole named boundary original."""

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


def physical_ports(labels, cut, declared):
    actual = [labels["s:0"], labels["s:1"] - cut]
    if declared != actual:
        raise ValueError("physical offset mismatch")
    return [labels["s:0"], labels["s:1"]]


def witness(original, labels, offsets, cut):
    graph, digest = original["graph"], original["graph_digest"]
    port_labels = physical_ports(labels, cut, offsets)
    assert all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    checked = verify_certificate(graph, labels, digest)
    assert checked["valid"], checked
    return {"labels": labels, "checker": checked, "graph_digest": digest,
            "ledger_id": ledger_id(digest, labels), "port_labels": port_labels, "cut": cut,
            "physical_ports": ["s:0", "s:1"],
            "witness": graph["spine"],
            "edge_rows": [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]}


def block_labels(quota, fixed):
    labels = {"s:0": fixed+1, "s:1": quota+2*fixed+4,
              "b:0:0": quota+fixed+3, "b:0:1": quota+fixed+2, "b:1:0": 0}
    for j in range(fixed):
        labels[f"l:0:0:{j}"] = 1+j
        labels[f"l:1:0:{j}"] = quota+fixed+4+j
    for j in range(quota):
        labels[f"l:0:1:{j}"] = fixed+2+j
    return labels


def move_section(vertex):
    parts = vertex.split(":")
    parts[1] = str(int(parts[1])+2)
    return ":".join(parts)


def interface_gate(graph, blocks, connector):
    old, new = blocks["B"], blocks["A"]
    names_B, names_A = old["labels"].keys(), new["labels"].keys()
    if names_B & names_A or names_B | names_A != set(graph["vertices"]):
        raise ValueError("components must partition the target names")
    if (old["ports"] + new["ports"] != graph["spine"]
            or connector != [old["ports"][1], new["ports"][0]]):
        raise ValueError("connector must be the actual U_B--L_A spine edge")
    cross = [[u, v] for u, v in graph["edges"] if (u in names_B) != (v in names_B)]
    if cross != [connector]:
        raise ValueError("expected exactly the declared original connector")
    if old["labels"][connector[0]]-old["cut"] != new["labels"][connector[1]]:
        raise ValueError("physical port offsets do not match")


def inventory_gate(graph, labels, blocks, connector, claimed):
    local_B, local_A = blocks["B"]["labels"], blocks["A"]["labels"]
    m = len(graph["edges"])
    p_B = blocks["B"]["cut"]
    p_A = blocks["A"]["cut"]
    n_A = len(local_A)
    group_labels = {"B_low": [], "A_low": [], "A_high": [], "B_high": []}
    for vertex, label in labels.items():
        side, local, local_cut = ("B", local_B, p_B) if vertex in local_B else ("A", local_A, p_A)
        band = side + ("_low" if local[vertex] < local_cut else "_high")
        group_labels[band].append(label)
    label_bands = {key: sorted(values) for key, values in group_labels.items()}

    differences = {"A_internal": [], "connector": [], "B_internal": []}
    for u, v in graph["edges"]:
        if [u, v] == connector:
            band = "connector"
        else:
            band = "B_internal" if u in local_B and v in local_B else "A_internal"
        differences[band].append(abs(labels[u]-labels[v]))
    difference_bands = {key: sorted(values) for key, values in differences.items()}
    if claimed != difference_bands:
        raise ValueError("claimed difference inventory disagrees with the original edges")
    if difference_bands != {"A_internal": list(range(1, n_A)), "connector": [n_A],
                            "B_internal": list(range(n_A+1, m+1))}:
        raise ValueError("R241 difference bands do not partition the alphabet")
    cut = p_A+p_B
    if label_bands != {"B_low": list(range(p_B)), "A_low": list(range(p_B, cut)),
                       "A_high": list(range(cut, p_B+n_A)), "B_high": list(range(p_B+n_A, m+1))}:
        raise ValueError("R241 label bands do not partition the alphabet")
    unused_labels = sorted(set(range(m+1))-set(labels.values()))
    unused_differences = sorted(set(range(1, m+1))-{w for band in difference_bands.values() for w in band})
    return {"labels": label_bands, "differences": difference_bands,
            "unused_labels": unused_labels, "unused_differences": unused_differences}


def compose(original, a, b):
    if type(a) is not int or type(b) is not int or min(a, b) < 2:
        raise ValueError("both quotas must be integers at least two")
    graph = original["graph"]
    old = block_labels(a, 2)
    new = {move_section(v): label for v, label in block_labels(b, 3).items()}
    blocks = {"B": {"source": "D087", "labels": old, "cut": a+4, "ports": ["s:0", "s:1"]},
              "A": {"source": "D089", "labels": new, "cut": b+5, "ports": ["s:2", "s:3"]}}
    connector = ["s:1", "s:2"]
    interface_gate(graph, blocks, connector)
    cut = a+b+9
    labels = {v: label+(b+11 if label >= a+4 else 0) for v, label in old.items()}
    labels.update({v: label+a+4 for v, label in new.items()})
    ports = [labels[v] for v in graph["spine"]]
    if [ports[0], ports[-1]-cut] != [3, 5]:
        raise ValueError("returned physical port mismatch")
    assert all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    checked = verify_certificate(graph, labels, original["graph_digest"])
    assert checked["valid"], checked
    claim = {"A_internal": list(range(1, b+11)), "connector": [b+11],
             "B_internal": list(range(b+12, a+b+20))}
    inventories = inventory_gate(graph, labels, blocks, connector, claim)
    return {"labels": labels, "graph_digest": original["graph_digest"], "cut": cut,
            "ledger_id": ledger_id(original["graph_digest"], labels),
            "offsets": [3, 5], "ports": ["s:0", "s:3"], "spine_labels": ports,
            "witness": graph["spine"], "blocks": blocks,
            "connector": {"edge": connector, "weight": abs(labels["s:1"]-labels["s:2"])},
            "inventories": inventories, "checker": checked,
            "edge_rows": [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]}


def retained_controls(cfg):
    positives = {}
    for source, state, cut, offsets in (("D087", "regression", 9, [3, 4]), ("D089", "boundary", 7, [4, 5])):
        folder = ROOT / cfg["archives"][source]
        retained = read(folder / "original.json")
        report = read(folder / "result.json")
        assert report["status"] == "PASS"
        cert = report[state]["certificate"]
        assert witness(retained, cert["labels"], offsets, cut) == cert
        positives[source] = {"graph_digest": retained["graph_digest"], "ledger_id": cert["ledger_id"],
                             "checker": cert["checker"], "offsets": offsets}
    folder = ROOT / cfg["archives"]["D088"]
    negative = read(folder / "result.json")
    receipt = read(folder / "command_receipt.json")
    assert negative["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert negative["disposition"] == "EXCLUDED"
    assert negative["domain"] == {"min_b": 2, "exact_integer": True, "offsets": [4, 4]}
    assert negative["boundary_graph_digest"] == read(folder / "original.json")["graph_digest"]
    return {"positives": positives,
            "D088": {"domain": negative["domain"], "graph_digest": negative["boundary_graph_digest"],
                     "receipt_sha256": hash_file(folder / "command_receipt.json"), "replay_visits": 0}}


def adverse_controls(original, cert):
    graph, labels = original["graph"], cert["labels"]
    false_digest = "0"*64
    rejection = verify_certificate(graph, labels, false_digest)
    assert not rejection["valid"] and rejection["errors"] == ["original graph digest mismatch"]
    wrong_connector = ["s:1", "s:3"]
    try:
        interface_gate(graph, cert["blocks"], wrong_connector)
    except ValueError as exc:
        connector = {"declared": wrong_connector, "valid": False, "error": str(exc)}
    else:
        raise AssertionError("wrong physical connector was accepted")
    wrong_inventory = cert["inventories"]["differences"] | {"connector": []}
    try:
        inventory_gate(graph, labels, cert["blocks"], cert["connector"]["edge"], wrong_inventory)
    except ValueError as exc:
        inventory = {"declared": wrong_inventory, "valid": False, "error": str(exc)}
    else:
        raise AssertionError("missing connector difference was accepted")
    return {"digest": {"expected_digest": false_digest, "checker": rejection},
            "physical_connector": connector, "difference_inventory": inventory}


def verify_inputs(cfg):
    assert cfg["boundary"] == [2, 2] and cfg["domain"] == {"min_a": 2, "min_b": 2, "exact_integers": True}
    assert cfg["component_order"] == {"B": "D087", "A": "D089"} and cfg["connector"] == ["s:1", "s:2"]
    assert cfg["limits"] == {
        "workers": 1, "symbolic_families": 1, "max_new_original_identities": 1,
        "max_new_certificates": 1, "assignment_visits": 0, "recorded_assignment_states": 0,
        "search_nodes": 0, "solver_calls": 0, "connectors": 1, "adverse_checks": 3,
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
    graph = build_graph([[2, a], [2], [3, b], [3]])
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": graph_digest(graph)}, cfg["limits"])
    original = read(HERE / "original.json")
    cert = compose(original, a, b)
    controls = retained_controls(cfg)
    controls["adverse"] = adverse_controls(original, cert)
    report = audit.check(ROOT, HERE, cfg, cert, controls)
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "domain": cfg["domain"],
            "boundary": cfg["boundary"], "certificate": cert, "runtime": runtime, "original_sha256": original_hash,
            "source_hashes": cfg["source_hashes"], "controls": controls, "audit": report}


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
        receipt["counts"].update(symbolic_families=1, new_certificates=1, connectors=1,
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
