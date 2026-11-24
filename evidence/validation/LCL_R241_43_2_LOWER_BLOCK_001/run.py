"""Check the nine prescribed lower-block placements on one original target."""

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


def load(path):
    return json.loads(path.read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, indent=2, sort_keys=True)+"\n").encode()
    total = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(raw)
    if len(raw) > limits["bytes_per_record"] or total > limits["bytes_total"]:
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as out:
        out.write(raw)
    return sha256(raw).hexdigest()


def ledger_id(digest, labels):
    payload = {"graph_digest": digest, "labels": sorted(labels.items())}
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def edges(graph):
    return Counter(tuple(sorted(edge)) for edge in graph["edges"])


def require_extension(source, target, host, leaf):
    if source["profile"] != [[4, 2], [2]] or target["profile"] != [[4, 3], [2]]:
        raise ValueError("Incorrect original profile")
    if (Counter(target["vertices"]) != Counter(source["vertices"])+Counter([leaf])
            or target["spine"] != source["spine"]
            or {v: target["roles"][v] for v in source["vertices"]} != source["roles"]
            or target["roles"][leaf] != {"kind": "leaf", "section": 0, "branch": 1, "leaf": 2}):
        raise ValueError("Incorrect extension names, roles or spine")
    if edges(target) != edges(source)+Counter([tuple(sorted((host, leaf)))]):
        raise ValueError("Incorrect new original incidence")


def interface(graph, labels, cut, offsets, host):
    witness = graph["spine"]
    if witness != ["s:0", "s:1"] or tuple(witness) not in edges(graph):
        raise ValueError("Incorrect original spine witness")
    physical = [labels[v] for v in witness]
    if offsets != [physical[0], physical[1]-cut]:
        raise ValueError("Physical offset mismatch")
    if not (0 <= offsets[0] < cut <= labels[host] < len(labels)
            and 0 <= offsets[1] < len(labels)-cut
            and tuple(sorted(("s:0", host))) in edges(graph)):
        raise ValueError("High host or port range mismatch")
    crossing = all((labels[u] < cut) != (labels[v] < cut) for u, v in graph["edges"])
    if not crossing or sorted(labels.values()) != list(range(len(graph["vertices"]))):
        raise ValueError("Alpha orientation or vertex bijection failed")
    return {"cut": cut, "physical_labels": physical, "offsets": offsets, "host_label": labels[host],
            "witness": witness, "edge_crossing": crossing, "host_spine_distance": 1}


def source_ledgers(original, archived, cfg):
    graph, digest = original["graph"], original["graph_digest"]
    cert = archived["certificate"]
    assert archived["status"] == "PASS" and cert["graph_digest"] == digest == cfg["source_graph_digest"]
    assert cert["cut"] == 8 and cert["witness"] == graph["spine"] and cert["offsets"] == [3, 4]
    direct = cert["labels"]
    reflected = {v: (7-u if u < 8 else 20-u) for v, u in direct.items()}
    result = {}
    for key, labels in (("I", direct), ("II", reflected)):
        offsets = cfg["ledgers"][key]["offsets"]
        state = interface(graph, labels, 8, offsets, cfg["host"])
        checker = verify_certificate(graph, labels, digest)
        assert checker["valid"] and checker["graph_digest"] == digest
        result[key] = {"labels": labels, "interface": state, "checker": checker,
                       "ledger_id": ledger_id(digest, labels), "graph_digest": digest}
        assert result[key]["ledger_id"] != "" and state["host_label"] == cfg["ledgers"][key]["host_label"]
    assert result["I"]["ledger_id"] == cert["ledger_id"] == cfg["source_ledger_id"]
    assert result["I"]["checker"] == cert["checker"]
    assert result["II"]["ledger_id"] != result["I"]["ledger_id"]
    assert result["II"]["checker"]["edge_differences"] == [13-w for w in cert["checker"]["edge_differences"]]
    return result


def placement(source, target, ledger, key, c, cfg):
    old = ledger["labels"]
    host, leaf = cfg["host"], cfg["leaf"]
    x, y = ledger["interface"]["offsets"]
    b = old[host]
    assert type(c) is int and 1 <= c <= 8 and x < c
    selected = sorted(v for v in old if old[v] < c)
    selected_edges = [[u, v, abs(old[u]-old[v])] for u, v in source["edges"]
                      if u in selected or v in selected]
    actual = sorted(w for _, _, w in selected_edges)
    required = list(range(b-c+1, 13))
    extra = sorted((Counter(actual)-Counter(required)).elements())
    absent = sorted((Counter(required)-Counter(actual)).elements())
    transformed = {v: value+int(value >= c) for v, value in old.items()}
    transformed[leaf] = c
    state = interface(target["graph"], transformed, 9, [x, y], host)
    checker = verify_certificate(target["graph"], transformed, target["graph_digest"])
    rows = [[u, v, w] for (u, v), w in zip(target["graph"]["edges"], checker["edge_differences"], strict=True)]
    histogram = Counter(w for _, _, w in rows)
    missing = sorted(set(range(1, 14))-histogram.keys())
    repeats = [[w, count] for w, count in sorted(histogram.items()) if count > 1]
    leaf_weight = abs(transformed[host]-transformed[leaf])
    assert leaf_weight == b+1-c
    return {"ledger": key, "threshold": c, "selected_vertices": selected, "selected_edges": selected_edges,
            "actual_premise": actual, "required_premise": required, "extra_premise": extra, "absent_premise": absent,
            "theorem_applies": actual == required, "new_leaf": [leaf, c, leaf_weight], "labels": transformed,
            "label_inventory": sorted(transformed.values()), "edge_rows": rows,
            "difference_inventory": sorted(histogram.elements()), "missing_differences": missing,
            "repeated_differences": repeats, "interface": state, "checker": checker}


def adverses(source, target, ledgers, cfg):
    old, new = source["graph"], target["graph"]
    direct = ledgers["I"]["labels"]
    host, leaf = cfg["host"], cfg["leaf"]
    bad_digest = "0"*64
    check = verify_certificate(old, direct, bad_digest)
    assert not check["valid"] and check["errors"] == ["original graph digest mismatch"]
    try:
        interface(old, direct, 8, [3, 3], host)
    except ValueError as exc:
        assert str(exc) == "Physical offset mismatch"
        port = {"declared": [3, 3], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("False port accepted")
    wrong = new | {"edges": [["b:0:0", leaf] if set(edge) == {host, leaf} else edge for edge in new["edges"]]}
    try:
        require_extension(old, wrong, host, leaf)
    except ValueError as exc:
        assert str(exc) == "Incorrect new original incidence"
        incidence = {"claimed_edge": ["b:0:0", leaf], "replaced_edge": [host, leaf], "valid": False, "error": str(exc)}
    else:
        raise AssertionError("Wrong host accepted")
    return {"graph_digest": {"declared": bad_digest, "checker": check}, "physical_port": port, "incidence": incidence}


def verify_inputs(cfg):
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == cfg["parent"]
    receipt = load(HERE / "preflight_receipt.json")
    assert receipt["status"] == "PASS" and receipt["task"] == cfg["task"] and receipt["parent"] == cfg["parent"]
    assert receipt["input_hashes"] == {name: raw_hash(HERE / name) for name in cfg["local_inputs"]}
    assert receipt["runtime"]["sha256"] == cfg["runtime_sha256"] == raw_hash(Path(sys.executable))
    for path, pin in cfg["source_hashes"].items():
        assert raw_hash(ROOT / path) == pin, path
    return receipt


def produce(cfg, counts):
    preflight = verify_inputs(cfg)
    source = load(ROOT / cfg["retained"]["original"])
    old = source["graph"]
    assert old["profile"] == cfg["source_profile"] == [[4, 2], [2]]
    ledgers = source_ledgers(source, load(ROOT / cfg["retained"]["result"]), cfg)
    counts["source_ledgers_checked"] = len(ledgers)
    counts["retained_positive_rechecks"] = 1
    graph = build_graph(cfg["target_profile"])
    require_extension(old, graph, cfg["host"], cfg["leaf"])
    digest = graph_digest(graph)
    assert digest != source["graph_digest"]
    original_hash = write_record("original.json", {"graph": graph, "graph_digest": digest}, cfg["limits"])
    counts["new_target_identities"] = 1
    target = load(HERE / "original.json")
    rows = []
    for key, ledger in ledgers.items():
        thresholds = cfg["ledgers"][key]["thresholds"]
        assert thresholds == list(range(ledger["interface"]["physical_labels"][0]+1, 9))
        for c in thresholds:
            rows.append(placement(old, target, ledger, key, c, cfg))
            counts["threshold_cases"] += 1
    assert len(rows) == cfg["limits"]["threshold_cases"]
    adverse = adverses(source, target, ledgers, cfg)
    counts["adverse_controls"] = len(adverse)
    checked = audit.check(ROOT, cfg, source, target, ledgers, rows, adverse)
    valid = [row for row in rows if row["checker"]["valid"]]
    assert len(valid) <= cfg["limits"]["accepted_certificates"]
    certificates = [{"ledger": row["ledger"], "threshold": row["threshold"],
                     "target_ledger_id": ledger_id(digest, row["labels"])} for row in valid]
    counts["accepted_certificates"] = len(certificates)
    return {"task": cfg["task"], "parent": cfg["parent"], "status": "PASS",
            "disposition": "ACCEPT" if certificates else "REJECT", "target_original_sha256": original_hash,
            "runtime": preflight["runtime"], "source_ledgers": ledgers, "threshold_rows": rows,
            "adverse": adverse, "accepted_certificates": certificates, "audit": checked}


def execute():
    if not __debug__ or not sys.dont_write_bytecode:
        raise RuntimeError("Use enabled assertions and -B")
    if any((HERE / name).exists() for name in ("original.json", "result.json", "command_receipt.json")):
        raise FileExistsError("Official output paths must be vacant")
    cfg = load(HERE / "config.json")
    limits = cfg["limits"]
    counts = {"official_sequences": 1, "workers": 1, "new_target_identities": 0, "source_ledgers_checked": 0,
              "retained_positive_rechecks": 0, "threshold_cases": 0, "accepted_certificates": 0, "adverse_controls": 0,
              "joins": 0, "solver_calls": 0, "assignment_visits": 0, "search_nodes": 0, "assignment_states": 0,
              "retries": 0, "restarts": 0, "historical_replays": 0}
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits,
               "inputs": {name: raw_hash(HERE / name) for name in (*cfg["local_inputs"], "preflight_receipt.json")}}
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
