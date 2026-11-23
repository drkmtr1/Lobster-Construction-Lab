"""Enumerate the three frozen named alpha products on two exact originals."""

from time import process_time

START = process_time()

from collections import Counter, deque
from hashlib import sha256
from itertools import permutations, product
import json
from math import factorial
from pathlib import Path
import subprocess
import sys

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def write(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    existing = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
    need(len(raw) <= 2_000_000 and existing + len(raw) <= 6_000_000, "evidence byte cap")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)


def parity_classes(graph):
    adjacent = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacent[u].append(v)
        adjacent[v].append(u)
    queue = deque(["s:0"])
    depth = {"s:0": 0}
    while queue:
        u = queue.popleft()
        for v in adjacent[u]:
            if v not in depth:
                depth[v] = depth[u]+1
                queue.append(v)
    need(len(depth) == len(adjacent), "disconnected original")
    return [[v for v in graph["vertices"] if depth[v] % 2 == k] for k in (0, 1)]


def audit_ports(labels, p):
    return [labels["s:0"], labels["s:1"] - p]


def matching_offsets(predecessor, successor):
    y = predecessor["labels"]["s:1"] - predecessor["low_size"]
    x = successor["labels"]["s:0"]
    need(y == x, "R241 requires y_B=x_A at the actual ports")


def ledger_id(digest, labels):
    payload = {"graph_digest": digest, "labels": sorted(labels.items())}
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def first_duplicate(edges, labels):
    previous = {}
    for i, (u, v) in enumerate(edges):
        w = abs(labels[u]-labels[v])
        if w in previous:
            return [previous[w], i, w]
        previous[w] = i
    return None


def enumerate_case(case, originals, total, limit):
    name, graph_id, pins, expected = case
    original = originals[graph_id]
    graph = original["graph"]
    classes = original["classes"]
    p = len(classes[0])
    bands = [range(p), range(p, len(graph["vertices"]))]
    for vertices, labels in zip(classes, bands, strict=True):
        need(all(pins[v] in labels for v in pins if v in vertices), "pin class")
    need(pins.keys() <= set(graph["vertices"]) and len(set(pins.values())) == len(pins), "pins")
    names = [[v for v in vertices if v not in pins] for vertices in classes]
    values = [[a for a in band if a not in pins.values()] for band in bands]
    need(factorial(len(values[0])) * factorial(len(values[1])) == expected, "declared product size")
    rows, counts = [], Counter()
    status = "INCOMPLETE"
    try:
        for lo, hi in product(permutations(values[0]), permutations(values[1])):
            need(total + len(rows) < limit, "assignment cap")
            need(process_time()-START < 25, "producer CPU reserve")
            labels = pins | dict(zip(names[0], lo, strict=True)) | dict(zip(names[1], hi, strict=True))
            repeat = first_duplicate(graph["edges"], labels)
            rows.append([lo, hi, repeat])
            if repeat is None:
                counts[tuple(audit_ports(labels, p))] += 1
        need(len(rows) == expected, "incomplete product")
        status = "COMPLETE"
    finally:
        write(f"{name}.json", {"graph_id": graph_id, "graph_digest": original["graph_digest"],
                               "pins": pins, "free_names": names, "free_labels": values,
                               "rows": rows, "status": status, "visited": len(rows),
                               "positive": sum(counts.values()),
                               "port_histogram": [[x, y, count] for (x, y), count in sorted(counts.items())]})
    return len(rows), sum(counts.values())


def identity(config):
    relative = HERE.relative_to(ROOT).as_posix()
    paths = config["sources"] + [f"{relative}/{name}" for name in
        ("INTAKE.md", "config.json", "commands.json", "run.py", "audit.py", "driver.py")]
    hashes = {p: raw_hash(ROOT / p) for p in sorted(paths)}
    packet = config["authorization"]
    need(hashes[packet["path"]] == packet["sha256"], "authorization raw hash mismatch")
    return {"parent": config["parent"], "sources": hashes,
            "runtime": {"python": sys.version, "path": Path(sys.executable).relative_to(ROOT).as_posix(),
                        "sha256": raw_hash(Path(sys.executable))}}


def control(original, labels):
    p = len(original["classes"][0])
    graph, digest = original["graph"], original["graph_digest"]
    checker = verify_certificate(graph, labels, digest)
    need(checker["valid"] and checker["graph_digest"] == digest, str(checker["errors"]))
    need(all((labels[u] < p) != (labels[v] < p) for u, v in graph["edges"]), "control alpha cut")
    edge_rows = [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]
    return {"graph_digest": digest, "ledger_id": ledger_id(digest, labels),
            "labels": labels, "checker": checker, "edge_rows": edge_rows,
            "low_size": p, "offsets": audit_ports(labels, p),
            "physical_ports": ["s:0", "s:1"], "witness": graph["spine"]}


def main():
    config = read(HERE / "config.json")
    need(Path.cwd() == ROOT and sys.version_info[:2] in ((3, 12), (3, 13)), "project Python")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    need(head == config["parent"], "expected parent")
    write("identity.json", identity(config))
    originals = {}
    for profile_id, profile in config["profiles"].items():
        graph = build_graph(profile)
        data = {"graph": graph, "graph_digest": graph_digest(graph), "classes": parity_classes(graph)}
        name = f"{profile_id}_original.json"
        write(name, data)
        originals[profile_id] = read(HERE / name)
    need(len({v["graph_digest"] for v in originals.values()}) == 2, "two exact originals")
    total, counts = 0, {}
    for case in config["cases"]:
        visits, positives = enumerate_case(case, originals, total, config["limits"]["assignments"])
        total += visits
        counts[case[0]] = {"visits": visits, "positive": positives}
    controls = {k: control(original, config["controls"][k]) for k, original in originals.items()}
    wrong = verify_certificate(originals["small"]["graph"], controls["small"]["labels"], "0"*64)
    need(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "wrong digest")
    try:
        matching_offsets(controls["small"], controls["neighbor"])
    except ValueError as exc:
        need(str(exc) == "R241 requires y_B=x_A at the actual ports", "wrong offset rejection")
        rejected = {"valid": False, "reason": str(exc), "y_B": controls["small"]["offsets"][1],
                    "x_A": controls["neighbor"]["offsets"][0],
                    "U_B": ["small", "s:1"], "L_A": ["neighbor", "s:0"]}
    else:
        raise ValueError("offset mismatch accepted")
    write("certificates.json", {"positive_controls": controls, "adverse":
          {"expected_digest": "0"*64, "checker": wrong, "offset": rejected}})
    write("result.json", {"status": "COMPLETE", "assignments": total, "counts": counts, "originals": 2,
                          "positive_controls": 2, "adverse_controls": 2, "solver_calls": 0,
                          "replays": 0, "producer_process_cpu_seconds": process_time()-START})


if __name__ == "__main__":
    main()
