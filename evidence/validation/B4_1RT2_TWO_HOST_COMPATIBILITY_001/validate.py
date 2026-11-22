"""Bounded deterministic validation for the exact 1RT2 two-host task."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUT = HERE / "validation"
PARENT = "eb5745483186287b20bcf155cf4e5265dbfc20a5"
PROOFS = ("research/ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md", "research/B4_1RT2_TWO_HOST_COMPATIBILITY.md")
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "lcl/consumers.py",
           "lcl/states.py", "pyproject.toml", "requirements.txt")
L, U, H, Z = "b:0:0", "s:4", "b:1:0", "b:2:0"
WITNESS = (L, "s:0", "s:1", "s:2", "s:3", U)
sys.path.insert(0, str(ROOT))

from lcl.consumers import _nonadjacent_path_labels
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(path, data, cap):
    raw = (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    put(path, raw, cap)
    return sha(raw)


def put(path, raw, cap):
    require(len(raw) <= cap, f"byte cap exceeded for {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def git(*args):
    return subprocess.check_output(("git", *args), cwd=ROOT)


def profile(r, t, K):
    return [[1], [r], [t], [2]] + [[] for _ in range(K + 1)]


def plan(r, t, K):
    for name, value, minimum in (("r", r, 3), ("t", t, 4), ("K", K, 2)):
        if type(value) is not int or value < minimum:
            raise ValueError(f"{name} must be an exact integer >= {minimum}")
    return K + r + t + 12


def hold(name, r, t, K, order, config):
    require(order <= config["max_vertices"], "vertex cap before graph expansion")
    graph = build_graph(profile(r, t, K))
    require(len(graph["vertices"]) == order, "wrong order")
    digest = graph_digest(graph)
    original_path = OUTPUT / "originals" / name
    raw_hash = save(original_path, {"graph": graph, "graph_digest": digest}, config["max_result_bytes"])
    return graph, {"path": f"originals/{name}", "graph_digest": digest, "sha256_raw": raw_hash}


def hold_target(r, t, K, config):
    order = plan(r, t, K)
    return hold(f"target-r{r}-t{t}-k{K}.json", r, t, K, order, config)


def direct(r, t):
    labels = dict(zip(("s:0", "s:1", "s:2", "s:3", U), (r + 9, 7, r + 14, 4, r + 7)))
    labels.update({L: 1, "l:0:0:0": r + 10, H: r + 6, "l:1:0:0": 6, "l:1:0:1": 5, Z: 0,
                   "b:3:0": r + 8, "l:3:0:0": 2, "l:3:0:1": 3})
    labels.update({f"l:1:0:{j}": j + 6 for j in range(2, r)})
    labels.update({f"l:2:0:{j}": r + 11 + j for j in range(3)})
    labels.update({f"l:2:0:{j}": r + 12 + j for j in range(3, t)})
    return labels


def edges_of(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def ledger(edges, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]


def witness_distances(graph, path):
    neighbors = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].append(v)
        neighbors[v].append(u)
    require(len(set(path)) == len(path) and all(v in neighbors[u] for u, v in zip(path, path[1:])),
            "not the declared physical path")
    distances = dict.fromkeys(path, 0)
    queue = deque(path)
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)
    require(len(distances) == len(neighbors) and max(distances.values()) <= 2, "witness does not cover graph")
    return distances


def alpha(graph, labels, r, t):
    n, p = r + t + 12, r + 6
    require(Counter(graph["vertices"]) == Counter(labels.keys())
            and sorted(labels.values()) == list(range(n)), "invalid normalized label alphabet")
    edge_rows = ledger(graph["edges"], labels)
    require(sorted(row["difference"] for row in edge_rows) == list(range(1, n)), "invalid normalized difference alphabet")
    low = sorted(v for v, value in labels.items() if value < p)
    high = sorted(v for v, value in labels.items() if value >= p)
    require((len(low), len(high)) == (p, t + 6)
            and all((labels[u] < p) != (labels[v] < p) for u, v in graph["edges"]), "wrong alpha cut")
    anchors = {v: labels[v] for v in (L, U, H, Z)}
    require(anchors == {L: 1, U: p + 1, H: p, Z: 0}, "wrong physical anchors")
    distances = witness_distances(graph, WITNESS)
    require(distances[H] == distances[Z] == 1, "wrong host distances")
    return {"state": {"n": n, "p": p, "x": 1, "y": 1, "L": L, "U": U, "H": H, "Z": Z},
            "anchors": anchors, "alpha": {"low": low, "high": high, "low_size": p},
            "witness": list(WITNESS), "witness_distances": distances}


def checked(graph, labels, digest):
    result = verify_certificate(graph, labels, digest)
    require(result["valid"], f"original-target check failed: {result['errors']}")
    return result


def normalized_record(graph, labels, ref, r, t):
    return {"parameters": {"r": r, "t": t}, "original": ref, "labels": labels,
            **alpha(graph, labels, r, t), "edge_ledger": ledger(graph["edges"], labels),
            "verification": checked(graph, labels, ref["graph_digest"])}


def retained_record(control, cap):
    cert_path, orig_path = (ROOT / control[k] for k in ("certificate", "original"))
    cert, orig = read(cert_path), read(orig_path)
    r, t, n = (control[k] for k in ("r", "t", "n"))
    graph, digest = orig["graph"], orig["graph_digest"]
    hash_orig = sha(orig_path.read_bytes())
    require(graph["profile"] == profile(r, t, 0) and len(graph["vertices"]) == n
            and graph_digest(graph) == digest == cert["original"]["graph_digest"]
            and hash_orig == cert["original"]["sha256_raw"], "incorrect retained original")
    ref = {"path": control["original"], "graph_digest": digest, "sha256_raw": hash_orig}
    labels = cert["labels"]
    require(labels == direct(r, t), "retained boundary disagrees with direct normalized formula")
    record = normalized_record(graph, labels, ref, r, t)
    for key in ("alpha", "edge_ledger", "witness", "witness_distances", "verification"):
        require(record[key] == cert[key], f"retained certificate changed: {key}")
    record["retained"] = {"certificate": control["certificate"], "sha256_raw": sha(cert_path.read_bytes())}
    path = OUTPUT / f"retained-r{r}-t{t}.json"
    return graph, record, {"path": path.name, "sha256_raw": save(path, record, cap)}


def transition(axis, count, before_key, before, after_key, after):
    graph, record, ref = before
    next_graph, next_record, next_ref = after
    r, t = before_key
    require(after_key == ((r + count, t) if axis == "H" else (r, t + count))
            and axis in ("H", "Z") and count > 0, "route does not follow declared intermediate")
    labels = record["labels"]
    n, cut = record["state"]["n"], record["state"]["p"]
    if axis == "H":
        host, section, start, first_label = H, 1, r, cut
        moved = {v: label + count if label >= cut else label for v, label in labels.items()}
    else:
        host, section, start, first_label = Z, 2, t, n
        moved = labels.copy()
    fresh = {f"l:{section}:0:{start + i}": first_label + i for i in range(count)}
    fresh_edges = [[host, v] for v in fresh]
    candidate = {**moved, **fresh}
    require(not set(fresh).intersection(labels)
            and Counter(next_graph["vertices"]) == Counter(graph["vertices"]) + Counter(fresh.keys())
            and edges_of(next_graph["edges"]) == edges_of(graph["edges"]) + edges_of(fresh_edges)
            and all(next_graph["roles"][v] == role for v, role in graph["roles"].items()),
            "transition changes original named incidence or role")
    require(candidate == next_record["labels"] and alpha(next_graph, candidate, *after_key) ==
            {key: next_record[key] for key in ("state", "anchors", "alpha", "witness", "witness_distances")},
            "pointwise agreement or returned state failed")
    return {"from": list(before_key), "to": list(after_key), "input_certificate": ref,
            "output_certificate": next_ref, "operation": axis, "count": count,
            "new_leaf_assignments": fresh, "new_edges": fresh_edges,
            "shifted_old_labels": {v: [labels[v], label] for v, label in moved.items() if labels[v] != label},
            "state": next_record["state"], "anchors": next_record["anchors"], "alpha": next_record["alpha"],
            "edge_spectrum": sorted(row["difference"] for row in next_record["edge_ledger"]),
            "witness": next_record["witness"], "witness_distances": next_record["witness_distances"]}


def compare(routes, states):
    records = []
    for route in routes:
        key = tuple(route["start"])
        steps = []
        for axis, count, r, t in route["steps"]:
            dest = (r, t)
            steps.append(transition(axis, count, key, states[key], dest, states[dest]))
            key = dest
        records.append({"name": route["name"], "steps": steps, "endpoint": states[key][2]})
    final = states[(5, 5)][2]
    z_end = states[(2, 5)][2]
    require(all(route["endpoint"] == final for route in records[:4])
            and records[4]["endpoint"] == records[1]["steps"][0]["output_certificate"] == z_end,
            "routes and same-host subdivisions do not agree")
    return {"routes": records, "direct": final, "H_subdivision_endpoint": final,
            "Z_subdivision_endpoint": z_end, "additional_graph_cases": 0}


def complete(r, t, K, original, normalized):
    graph, ref = original
    prefix_graph, seed, seed_ref = normalized
    p = seed["state"]["p"]
    require(p == r + 6, "wrong updated cut")
    prefix = {v: label + K if label >= p else label for v, label in seed["labels"].items()}
    partial = verify_partial(graph, prefix)
    path = [f"s:{i}" for i in range(4, K + 5)]
    suffix = path[1:]
    suffix_edges = [[u, v] for u, v in zip(path, suffix)]
    pending = [edge for edge in graph["edges"] if not all(v in prefix for v in edge)]
    crossing = [edge for edge in pending if sum(v in prefix for v in edge) == 1]
    m = len(graph["edges"])
    require(partial["valid"] and partial["graph_digest"] == ref["graph_digest"]
            and partial["used_labels"] == list(range(p)) + list(range(p + K, m + 1))
            and partial["used_differences"] == list(range(K + 1, m + 1))
            and partial["unused_labels"] == list(range(p, p + K))
            and partial["unused_differences"] == list(range(1, K + 1))
            and partial["frontier"] == [U] and prefix[U] == p + K + 1, "wrong boundary resources")
    require(Counter(graph["vertices"]) == Counter(prefix.keys()) + Counter(suffix)
            and edges_of(pending) == edges_of(suffix_edges)
            and edges_of(crossing) == edges_of([[U, "s:5"]])
            and edges_of(graph["edges"]) == edges_of(prefix_graph["edges"]) + edges_of(suffix_edges),
            "not the original unfinished B4 path")
    sequence = _nonadjacent_path_labels(K, p)
    require(len(sequence) == K + 1 and sequence[0] == prefix[U], "numerical sequence does not match port")
    labels = {**prefix, **dict(zip(suffix, sequence[1:]))}
    path_weights = ledger(suffix_edges, labels)
    require(sorted(sequence[1:]) == partial["unused_labels"]
            and sorted(row["difference"] for row in path_weights) == partial["unused_differences"]
            and all(labels[v] == label for v, label in prefix.items()), "suffix did not use exactly both resources")
    witness = list(WITNESS) + suffix
    return {"parameters": {"r": r, "t": t, "K": K}, "original": ref, "normalized": seed_ref,
            "high_shift_cut": p, "prefix_labels": prefix, "partial_verification": partial,
            "port": {"physical_vertex": U, "label": prefix[U]},
            "pending_vertices": suffix, "pending_edges": pending, "crossing_edges": crossing,
            "path": path, "numeric_sequence": sequence, "path_edge_ledger": path_weights, "labels": labels,
            "edge_ledger": ledger(graph["edges"], labels), "witness": witness,
            "witness_distances": witness_distances(graph, witness),
            "verification": checked(graph, labels, ref["graph_digest"])}


def reject(config):
    receipts = []
    with patch(__name__ + ".build_graph", side_effect=AssertionError("invalid input reached graph builder")) as builder:
        for values in config["invalid"]:
            try:
                hold_target(*values, config)
            except ValueError as error:
                receipts.append({"arguments": values, "types": [type(v).__name__ for v in values],
                                 "rejected": True, "reason": str(error), "graph_builder_calls": builder.call_count})
            else:
                raise ValueError("invalid input accepted")
        require(builder.call_count == 0 and len(receipts) == 12, "invalid probe accounting")
    return receipts


def main():
    config_path = HERE / "config.json"
    config = read(config_path)
    cap = config["max_result_bytes"]
    require(git("rev-parse", "HEAD").decode().strip() == PARENT == config["parent"], "unexpected accepted parent")
    require(config["workers"] == 1 and config["max_vertices"] == 27 and cap == 2_000_000
            and config["solver_queries"] == config["computational_enumeration"] == config["historical_search_replay"] == 0
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1,
            "unsupported runtime or run limits")
    OUTPUT.mkdir()
    snapshots = {}
    for rel in SOURCES:
        raw = (ROOT / rel).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{rel}").replace(b"\r\n", b"\n"),
                f"source differs from accepted parent: {rel}")
        put(OUTPUT / "source" / rel, raw, cap)
        snapshots[rel] = sha(raw)
    retained_paths = sorted({case[key] for case in config["controls"] for key in ("certificate", "original")})
    identity = {"config_sha256_raw": sha(config_path.read_bytes()), "parent": PARENT, "run_id": config["run_id"],
                "runner_sha256_raw": sha(Path(__file__).read_bytes()), "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
                "proofs_sha256_raw": {name: sha((ROOT / name).read_bytes()) for name in PROOFS},
                "retained_sha256_raw": {name: sha((ROOT / name).read_bytes()) for name in retained_paths},
                "source_sha256_raw": snapshots, "runtime": {"python": sys.version, "implementation": sys.implementation.name,
                                                           "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
                                                           "optional_dependencies": [], "python_executable": ".venv/Scripts/python.exe"}}
    identity_hash = save(OUTPUT / "identity.json", identity, cap)
    invalid_hash = save(OUTPUT / "domain_rejections.json", reject(config), cap)
    prefix_originals = {(r, t): hold(f"normalized-r{r}-t{t}.json", r, t, 0, order, config)
                        for r, t, order in config["prefixes"]}
    target_originals = {}
    for r, t, K, order in config["targets"]:
        require(plan(r, t, K) == order, "declared completed order mismatch")
        target_originals[(r, t, K)] = hold_target(r, t, K, config)
    states = {}
    for control in config["controls"]:
        states[(control["r"], control["t"])] = retained_record(control, cap)
    controls = [entry[2] for entry in states.values()]
    prefix_refs = []
    for (r, t), (graph, ref) in prefix_originals.items():
        record = normalized_record(graph, direct(r, t), ref, r, t)
        path = OUTPUT / f"normalized-r{r}-t{t}.json"
        saved = {"path": path.name, "sha256_raw": save(path, record, cap)}
        prefix_refs.append(saved)
        states[(r, t)] = graph, record, saved
    route_ref = save(OUTPUT / "routes.json", compare(config["routes"], states), cap)
    targets = []
    for (r, t, K), original in target_originals.items():
        record = complete(r, t, K, original, states[(r, t)])
        path = OUTPUT / f"target-r{r}-t{t}-k{K}.json"
        digest = save(path, record, cap)
        targets.append({"path": path.name, "n": record["verification"]["n"],
                        "bytes": path.stat().st_size, "sha256_raw": digest})
    summary = {"status": "PASS", "run_id": config["run_id"], "identity_sha256_raw": identity_hash,
               "controls": controls, "prefixes": prefix_refs, "targets": targets,
               "routes_sha256_raw": route_ref, "domain_rejections_sha256_raw": invalid_hash,
               "domain_rejections": 12, "checked_graph_records": 11, "new_graph_records": 7,
               "solver_queries": 0, "computational_enumeration": 0, "historical_search_replay": 0}
    save(OUTPUT / "summary.json", summary, cap)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
