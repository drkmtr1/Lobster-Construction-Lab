"""Transport a D097 boundary ledger to the sole independently built target."""

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
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def read(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, value, limits):
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    size = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
    if len(raw) > limits["bytes_per_record"] or size+len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)
    return sha256(raw).hexdigest()


def d097_source_labels(q, a, r):
    if any(type(x) is not int for x in (q, a, r)) or not q > r >= a >= 2:
        raise ValueError("Require exact integers q > r >= a >= 2")
    p = q+a+2
    labels = {"s:0": a+1, "s:1": p+a+2, "b:0:0": p+1, "b:0:1": p, "b:1:0": 0}
    for section, branch, count, first in ((0, 0, a, 1), (0, 1, q, a+2), (1, 0, a, p+2)):
        for k in range(count):
            labels[f"l:{section}:{branch}:{k}"] = first+k
    for k in range(a, r):
        labels[f"l:1:0:{k}"] = p+3+k
    return labels


def target_name(source_name):
    parts = source_name.split(":")
    if parts[0] in ("b", "l") and parts[1] == "0":
        parts[2] = str(1-int(parts[2]))
    return ":".join(parts)


def edge_multiset(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def require_transport(source, target, mapping):
    if set(mapping) != set(source["vertices"]) or Counter(mapping.values()) != Counter(target["vertices"]):
        raise ValueError("Name transport is not a bijection")
    inverse = {name: old for old, name in mapping.items()}
    mapped_edges = edge_multiset((mapping[u], mapping[v]) for u, v in source["edges"])
    if mapped_edges != edge_multiset(target["edges"]):
        raise ValueError("Named transport changes original edge incidences")
    if edge_multiset((inverse[u], inverse[v]) for u, v in target["edges"]) != edge_multiset(source["edges"]):
        raise ValueError("Inverse transport changes original edge incidences")
    if [mapping[v] for v in source["spine"]] != target["spine"]:
        raise ValueError("Name transport moves the physical spine")
    if any(name != target_name(old) for old, name in mapping.items()):
        raise ValueError("Name transport changes a prescribed role or index")
    return inverse


def require_ports(graph, labels, cut, offsets):
    if graph["spine"] != ["s:0", "s:1"] or graph["spine"] not in graph["edges"]:
        raise ValueError("Incorrect physical spine")
    if offsets != [labels["s:0"], labels["s:1"]-cut]:
        raise ValueError("Physical offset mismatch")
    if any((labels[u] < cut) == (labels[v] < cut) for u, v in graph["edges"]):
        raise ValueError("Alpha cut mismatch on original edges")


def adverses(original, source, cert, name_map):
    graph, labels = original["graph"], cert["labels"]
    source_digest = source["graph_digest"]
    assert source_digest != original["graph_digest"]
    wrong_identity = verify_certificate(graph, labels, source_digest)
    assert not wrong_identity["valid"] and wrong_identity["errors"] == ["original graph digest mismatch"]
    try:
        require_ports(graph, labels, cert["cut"], [3, 3])
    except ValueError as exc:
        assert str(exc) == "Physical offset mismatch"
        bad_offsets = {"declared": [3, 3], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("False offsets accepted")
    u, v = "l:0:0:0", "l:0:1:0"
    wrong_map = name_map | {u: name_map[v], v: name_map[u]}
    assert Counter(wrong_map.values()) == Counter(graph["vertices"])
    try:
        require_transport(source["graph"], graph, wrong_map)
    except ValueError as exc:
        assert str(exc) == "Named transport changes original edge incidences"
        bad_transport = {"exchanged_source_names": [u, v], "map": wrong_map, "valid": False, "error": str(exc)}
    else:
        raise AssertionError("False terminal transport accepted")
    return {"graph_identity": {"declared_digest": source_digest, "checker": wrong_identity},
            "physical_ports": bad_offsets, "transport": bad_transport}


def inputs(cfg):
    assert cfg["boundary"] == [4, 2, 2]
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    preflight = read(HERE / "preflight_receipt.json")
    assert preflight["status"] == "PASS" and preflight["task"] == cfg["task"] and preflight["parent"] == cfg["parent"]
    assert preflight["input_hashes"] == {name: digest_file(HERE / name) for name in cfg["local_inputs"]}
    assert preflight["runtime"]["sha256"] == cfg["runtime_sha256"] == digest_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert digest_file(ROOT / path) == expected, path
    return preflight


def produce(cfg, counts):
    preflight = inputs(cfg)
    q, a, r = cfg["boundary"]
    source = read(ROOT / cfg["retained"]["original"])
    report = read(ROOT / cfg["retained"]["result"])
    retained = report["state"]["certificate"]
    src_graph, src_digest = source["graph"], source["graph_digest"]
    assert report["status"] == "PASS" and src_graph["profile"] == [[a, q], [r]]
    assert src_digest == retained["graph_digest"]
    src_labels = d097_source_labels(q, a, r)
    assert src_labels == retained["labels"]
    p, offsets = q+a+2, [a+1, a+2]
    assert retained["cut"] == p and retained["physical_ports"] == src_graph["spine"]
    require_ports(src_graph, src_labels, p, offsets)
    check = verify_certificate(src_graph, src_labels, src_digest)
    assert check["valid"] and check == retained["checker"]
    counts["retained_positive_rechecks"] = 1

    graph = build_graph([[q, a], [r]])
    digest = graph_digest(graph)
    assert digest != src_digest
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": digest}, cfg["limits"])
    original = read(HERE / "original.json")
    counts["new_original_identities"] = 1
    name_map = {v: target_name(v) for v in src_graph["vertices"]}
    inverse = require_transport(src_graph, graph, name_map)
    labels = {v: src_labels[inverse[v]] for v in graph["vertices"]}
    require_ports(graph, labels, p, offsets)
    checker = verify_certificate(original["graph"], labels, original["graph_digest"])
    assert checker["valid"], checker
    canonical = json.dumps({"graph_digest": digest, "labels": sorted(labels.items())},
                           sort_keys=True, separators=(",", ":")).encode()
    cert = {"labels": labels, "cut": p, "offsets": offsets, "graph_digest": digest,
            "ledger_id": sha256(canonical).hexdigest(), "checker": checker, "witness": graph["spine"],
            "edge_rows": [[u, v, w] for (u, v), w in zip(graph["edges"], checker["edge_differences"], strict=True)]}
    transport = {"forward": name_map, "inverse": inverse}
    adverse = adverses(original, source, cert, name_map)
    counts["adverse_checks"] = len(adverse)
    audited = audit.check(ROOT, cfg, original, cert, transport, adverse)
    counts["new_certificates"] = 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "boundary": cfg["boundary"],
            "runtime": preflight["runtime"], "original_sha256": original_hash, "certificate": cert,
            "transport": transport, "adverse": adverse, "audit": audited,
            "retained_positive": {"graph_digest": src_digest, "ledger_id": retained["ledger_id"],
                                  "checker": check, "pointwise_d097_match": True}}


def execute():
    if not __debug__ or not sys.dont_write_bytecode:
        raise RuntimeError("Use enabled assertions and -B")
    if any((HERE / name).exists() for name in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be vacant")
    cfg = read(HERE / "config.json")
    limits = cfg["limits"]
    counts = {"official_sequences": 1, "workers": 1, "new_original_identities": 0,
              "new_certificates": 0, "retained_positive_rechecks": 0, "adverse_checks": 0,
              "joins": 0, "solver_calls": 0, "assignment_visits": 0, "search_nodes": 0,
              "assignment_states": 0, "retries": 0, "restarts": 0, "historical_replays": 0}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits,
               "inputs": {name: digest_file(HERE / name) for name in (*cfg["local_inputs"], "preflight_receipt.json")}}
    try:
        report = produce(cfg, counts)
        if process_time()-START >= limits["process_cpu_seconds"]:
            raise TimeoutError("Process-CPU cap exceeded")
        receipt["result_sha256"] = write_record("result.json", report, limits)
        receipt.update(status="PASS", exit_code=0)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["process_cpu_seconds"] = process_time()-START
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
