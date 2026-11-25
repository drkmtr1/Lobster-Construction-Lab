"""Build, independently reconstruct and freeze the input corpus only."""

import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys
import time


KIT = Path(__file__).resolve().parent
ROOT = KIT.parents[1]
FREEZE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_MATCHED_EXTERIOR_TWO_CENTER_001/input"
CONFIG = KIT / "config.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def reconstruct(profile):
    """Independent named graph from per-role parent relationships."""
    spine = [f"s:{i}" for i in range(len(profile))]
    roles = {}
    parents = {}
    for i, section in enumerate(profile):
        root = spine[i]
        roles[root] = {"kind": "spine", "section": i}
        if i:
            parents[root] = spine[i - 1]
        for branch, count in enumerate(section):
            host = f"b:{i}:{branch}"
            parents[host] = root
            roles[host] = {"kind": "branch", "section": i, "branch": branch}
            for terminal in range(count):
                name = f"l:{i}:{branch}:{terminal}"
                parents[name] = host
                roles[name] = {"kind": "leaf", "section": i, "branch": branch, "leaf": terminal}
    edges = sorted(sorted([name, parent]) for name, parent in parents.items())
    payload = {"vertices": sorted(roles), "edges": edges, "roles": roles,
               "profile": profile, "spine": spine}
    digest = sha(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    return payload, digest


def same_original(graph, profile, model):
    independent, digest = reconstruct(profile)
    normalized = {**graph, "vertices": sorted(graph["vertices"]),
                  "edges": sorted(sorted(edge) for edge in graph["edges"])}
    del normalized["schema_version"]
    if normalized != independent or model.graph_digest(graph) != digest:
        raise ValueError("independent original reconstruction mismatch")
    return digest


def edge_weights(graph, labels, cut):
    return sorted(abs(labels[a] - labels[b]) for a, b in graph["edges"]
                  if (labels[a] < cut) != (labels[b] < cut))


def initialize(seed_graph, seed_labels, model, verify):
    n0 = len(seed_graph["edges"])
    lower = max(3, n0 - 1, (20 - 6 + 3) // 4)
    c0 = lower + ((n0 - 1 - lower) % 2)
    if seed_labels[seed_graph["spine"][-1]] != n0:
        raise ValueError("D105 does not have the required maximum physical frontier")
    size = 3 * c0
    path_count = size - n0
    t = (size + 1 - n0) // 2
    if path_count != 2 * t - 1 or t < c0:
        raise ValueError("D134 path parameters")
    labels = {name: value + t for name, value in seed_labels.items()}
    profile = seed_graph["profile"] + [[] for _ in range(path_count)]
    for distance in range(path_count):
        section = len(profile) - 1 - distance
        labels[f"s:{section}"] = distance // 2 if distance % 2 == 0 else size - distance // 2
    path = model.build_graph(profile)
    if not verify.verify_certificate(path, labels, same_original(path, profile, model))["valid"]:
        raise ValueError("D134 alternating path")
    if edge_weights(path, labels, c0) != list(range(c0 + 2, size + 1)):
        raise ValueError("D134 path cut")
    q = c0 + 2
    n = size + q + 4
    if c0 < 3 or c0 + 1 < n0 or (c0 + 1 - n0) % 2 or q < 5 or n < 20:
        raise ValueError("D134 initializer premises")
    labels = {name: 3 + value + q * (value >= c0) for name, value in labels.items()}
    section = len(profile)
    profile = profile + [[1, q - 2, 1]]
    labels[f"s:{section}"] = n
    for j, coordinates in enumerate(([0], range(2, q), [1])):
        labels[f"b:{section}:{j}"] = j
        for l, i in enumerate(coordinates):
            labels[f"l:{section}:{j}:{l}"] = 3 + c0 + i
    graph = model.build_graph(profile)
    digest = same_original(graph, profile, model)
    if not verify.verify_certificate(graph, labels, digest)["valid"]:
        raise ValueError("initialized original certificate")
    c = c0 + q
    d = c + 2
    frontier = graph["spine"][-1]
    oriented = {name: n - value for name, value in labels.items()}
    if n != 2*c+2 or oriented[frontier] != 0 or edge_weights(graph, oriented, c) != list(range(d, n+1)):
        raise ValueError("returned D134 state")
    return {"graph": graph, "digest": digest, "actual_labels": labels, "oriented_labels": oriented,
            "n": n, "c": c, "d": d, "actual_cut": n+1-c, "frontier": frontier,
            "polarity": "maximum", "initializer": {"c0": c0, "path_count": path_count,
            "path_size": size, "t": t, "Q0": q, "seed_n": n0}}


def declared_profiles(config):
    right_centers = [(q,) for q in range(3, 9)] + list(itertools.product(range(1, 5), repeat=2))
    rows = []
    for a, dl, centers, dr in itertools.product(range(2, 5), range(2), right_centers, range(5)):
        suffix = [[a] + [0]*dl, list(centers) + [0]*dr]
        fresh = sum(1 + len(section) + sum(section) for section in suffix)
        if 12 <= fresh <= 20 and fresh % 2 == 0:
            control = next((c["name"] for c in config["controls"] if c["profile"] == suffix), None)
            rows.append({"suffix": suffix, "fresh": fresh, "second_centers": len(centers),
                         "high_value": len(centers) == 2 and dl == 0 and dr <= 2,
                         "control": control})
    order = {control["name"]: i for i, control in enumerate(config["controls"])}
    rows.sort(key=lambda row: (order.get(row["control"], len(order)), not row["high_value"],
                               -row["second_centers"], row["suffix"]))
    return rows


def main():
    started = time.process_time()
    if not sys.dont_write_bytecode or FREEZE.exists():
        raise SystemExit("preparation requires no bytecode and a vacant freeze directory")
    config = json.loads(CONFIG.read_bytes())
    if platform.python_version() != config["python_version"]:
        raise SystemExit("wrong runtime version")
    seed = config["seed"]
    raw = [(ROOT / seed[key]).read_bytes() for key in ("original", "result")]
    if any(sha(data) != seed[key+"_sha"] for data, key in zip(raw, ("original", "result"))):
        raise SystemExit("D105 artifact identity changed")
    sys.path.insert(0, str(ROOT))
    from lcl import model, verify
    seed_graph = json.loads(raw[0])["graph"]
    certificate = json.loads(raw[1])["certificate"]
    if (certificate["ledger_id"] != seed["ledger"] or
            same_original(seed_graph, seed_graph["profile"], model) != seed["digest"] or
            not verify.verify_certificate(seed_graph, certificate["labels"], seed["digest"])["valid"]):
        raise SystemExit("D105 original or certificate mismatch")
    prefix = initialize(seed_graph, certificate["labels"], model, verify)
    rows = declared_profiles(config)
    limits = config["limits"]
    if len(rows) > limits["targets"] or 2*len(rows) > limits["dispositions"]:
        raise SystemExit("corpus ceiling")
    FREEZE.mkdir()
    files = []
    size = 0

    def write(name, payload):
        nonlocal size
        raw_data = encoded(payload)
        size += len(raw_data)
        if len(raw_data) > limits["record_bytes"] or size > limits["evidence_bytes"]:
            raise ValueError("preparation evidence ceiling")
        with (FREEZE / name).open("xb") as stream:
            stream.write(raw_data)
        files.append({"file": name, "bytes": len(raw_data), "sha256": sha(raw_data)})

    write("prefix.json", prefix)
    index = []
    shard = []
    seen = set()
    for number, row in enumerate(rows, 1):
        profile = prefix["graph"]["profile"] + row["suffix"]
        graph = model.build_graph(profile)
        digest = same_original(graph, profile, model)
        if digest in seen or len(graph["edges"]) != prefix["n"] + row["fresh"]:
            raise ValueError("duplicate original or wrong fresh size")
        seen.add(digest)
        row = {**row, "target_id": f"target-{number:04d}", "digest": digest,
               "shard": f"targets-{(number-1)//24:02d}.json"}
        item = {**row, "graph": graph}
        index.append({**row, "record_sha256": sha(encoded(item))})
        shard.append(item)
        if len(shard) == 24 or number == len(rows):
            write(row["shard"], shard)
            shard = []
    counts = {str(i): sum(row["second_centers"] == i for row in rows) for i in (1, 2)}
    counts["high_value"] = sum(row["high_value"] for row in rows)
    if [row["control"] for row in index if row["control"]] != [c["name"] for c in config["controls"]]:
        raise ValueError("control not present exactly once")
    write("corpus_index.json", {"counts": counts, "targets": index})
    receipt = {"status": "CORPUS_ONLY", "files": files.copy(), "evidence_bytes_before_receipt": size,
               "counts": counts, "targets": len(rows), "arm_dispositions": 0, "exterior_nodes": 0,
               "transfer_states": 0, "transitions": 0, "bytecode_disabled": sys.dont_write_bytecode,
               "cpu_seconds_before_receipt": time.process_time()-started}
    write("corpus_receipt.json", receipt)
    print(json.dumps(receipt | {"files": len(receipt["files"])}))


if __name__ == "__main__":
    main()
