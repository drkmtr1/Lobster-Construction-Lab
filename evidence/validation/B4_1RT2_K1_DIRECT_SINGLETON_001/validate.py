"""Deterministic bounded original-target checks for the 1RT2 singleton."""

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
PARENT = "3e10c022f834cfae053aaef9581697bf6c21002d"
PROOF = "research/B4_1RT2_K1_DIRECT_SINGLETON.md"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
H, Z = "b:1:0", "b:2:0"
PORT, FINAL = "s:4", "s:5"
FINAL_EDGE = [PORT, FINAL]
SPINE = [f"s:{i}" for i in range(6)]

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def put(path, raw, cap):
    require(len(raw) <= cap, f"byte cap exceeded for {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def save(path, data, cap):
    raw = (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    put(path, raw, cap)
    return {"path": path.name, "sha256_raw": sha(raw)}


def git(*args):
    return subprocess.check_output(("git", *args), cwd=ROOT)


def profile(r, t):
    return [[1], [r], [t] if t is not None else [], [2], [], []]


def plan(r, t):
    for name, value, minimum in (("r", r, 3), ("t", t, 4)):
        if type(value) is not int or value < minimum:
            raise ValueError(f"{name} must be an exact integer >= {minimum}")
    return r + t + 13


def hold_target(r, t, config):
    n = plan(r, t)
    require(n <= config["max_vertices"], "order cap before graph expansion")
    graph = build_graph(profile(r, t))
    require(len(graph["vertices"]) == n, "declared original order mismatch")
    name = f"target-r{r}-t{t}.json"
    digest = graph_digest(graph)
    receipt = save(OUTPUT / "originals" / name, {"graph": graph, "graph_digest": digest}, config["max_result_bytes"])
    return graph, {**receipt, "path": f"originals/{name}", "graph_digest": digest}


def core_formula(r, include_final):
    spine_prefix = (r + 6, 0, r + 11, 1, r + 9)
    labels = dict(zip(SPINE[:-1], spine_prefix))
    labels.update({"b:0:0": r + 2, "l:0:0:0": r + 1, H: r + 7, "l:1:0:0": r + 4,
                   "b:3:0": r + 10, "l:3:0:0": r + 8, "l:3:0:1": r + 5})
    labels.update({f"l:1:0:{j}": j + 1 for j in range(1, r)})
    if include_final:
        labels[FINAL] = r + 3
    return labels


def direct_prefix(r, t):
    labels = {v: value + 1 for v, value in core_formula(r, include_final=False).items()}
    labels[Z] = 0
    labels.update({f"l:2:0:{j}": r + 13 + j for j in range(t)})
    return labels


def edges_of(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def ledger(edges, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]


def spectrum(rows):
    return sorted(row["difference"] for row in rows)


def witness(graph, assigned):
    edges = [edge for edge in graph["edges"] if all(v in assigned for v in edge)]
    path = [v for v in SPINE if v in assigned]
    neighbors = {v: [] for v in assigned}
    for u, v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    require(all(v in neighbors[u] for u, v in zip(path, path[1:])), "original witness incidence")
    distances = dict.fromkeys(path, 0)
    todo = deque(path)
    while todo:
        u = todo.popleft()
        for v in neighbors[u]:
            if v not in distances:
                distances[v] = distances[u] + 1
                todo.append(v)
    require(len(distances) == len(neighbors) and all(
        distances[v] == {"spine": 0, "branch": 1, "leaf": 2}[graph["roles"][v]["kind"]]
        for v in neighbors), "wrong original witness distances")
    return {"path": path, "distances": distances}


def cut_state(graph, labels, cut):
    below = sorted(v for v, label in labels.items() if label < cut)
    crossing, other = [], []
    for row in ledger(graph["edges"], labels):
        u, v = row["edge"]
        (crossing if (labels[u] < cut) != (labels[v] < cut) else other).append(row)
    m = len(graph["edges"])
    require(1 <= cut <= labels[H] <= m and labels[H] - cut + 1 == 7
            and spectrum(crossing) == list(range(7, m + 1)) and spectrum(other) == list(range(1, 7)),
            "incomplete ordinary crossing-cut premise")
    require(any(row["edge"] == FINAL_EDGE and row["difference"] == 6 for row in other),
            "final edge is not a six-weight noncrossing incidence")
    return {"c": cut, "host": H, "host_label": labels[H], "m": m, "below": below,
            "crossing": crossing, "crossing_spectrum": spectrum(crossing),
            "noncrossing": other, "noncrossing_spectrum": spectrum(other)}


def bound_full(graph, labels, digest):
    outcome = verify_certificate(graph, labels, digest)
    require(outcome["valid"], f"original-target check failed: {outcome['errors']}")
    return outcome


def load_retained(config, filename, r, t, n):
    base = ROOT / config["retained_bundle"]
    cert_path = base / filename
    cert = read(cert_path)
    orig_path = base / "originals" / filename
    orig = read(orig_path)
    graph, digest = orig["graph"], orig["graph_digest"]
    orig_hash = sha(orig_path.read_bytes())
    cert_hash = sha(cert_path.read_bytes())
    require(len(graph["vertices"]) == n <= config["max_vertices"] and graph["profile"] == profile(r, t)
            and graph_digest(graph) == digest and cert["original"] == {
                "path": f"originals/{filename}", "graph_digest": digest, "sha256_raw": orig_hash},
            "retained original binding or profile failed")
    require(max(cert_path.stat().st_size, orig_path.stat().st_size) <= config["max_result_bytes"],
            "retained record byte cap")
    return graph, {"path": orig_path.relative_to(ROOT).as_posix(), "graph_digest": digest, "sha256_raw": orig_hash}, {
        "path": cert_path.relative_to(ROOT).as_posix(), "sha256_raw": cert_hash}, cert


def recheck_core(config, r, n):
    filename = f"core-r{r}.json"
    graph, original, saved, cert = load_retained(config, filename, r, None, n)
    labels = cert["labels"]
    require(cert["r"] == r and labels == core_formula(r, include_final=True)
            and labels["s:2"] == r + 11 == max(labels.values()), "retained core formula or physical maximum")
    root = {"vertex": "s:2", "label": r + 11}
    checked = {"edge_ledger": ledger(graph["edges"], labels), "witness": witness(graph, labels),
               "verification": bound_full(graph, labels, original["graph_digest"]),
               "cut": cut_state(graph, labels, r + 1), "root": root}
    require(all(cert[key] == result for key, result in checked.items()), "retained core check differs from archive")
    old_crossing = [row for row in checked["cut"]["crossing"]
                    if not any(v.startswith("l:1:0:") and int(v.rsplit(":", 1)[1]) >= 2 for v in row["edge"])]
    inserted = [row for row in checked["cut"]["crossing"] if row not in old_crossing]
    bands = {"old_noncrossing": checked["cut"]["noncrossing_spectrum"],
             "new_second_terminal_edges": spectrum(inserted), "shifted_original_crossings": spectrum(old_crossing)}
    require(bands["new_second_terminal_edges"] == list(range(7, r + 5))
            and bands["shifted_original_crossings"] == list(range(r + 5, r + 12)), "core difference bands")
    record = {"r": r, "original": original, "saved_certificate": saved,
              "labels": labels, "core_difference_bands": bands, **checked}
    ref = save(OUTPUT / f"recheck-core-r{r}.json", record, config["max_result_bytes"])
    return graph, record, ref


def finish(r, t, graph, original, prefix, core):
    core_graph, core_record, core_ref = core
    n, m = len(graph["vertices"]), len(graph["edges"])
    require(n == m + 1 == r + t + 13, "incorrect full original order")
    # Check the retained core-to-original map by name before consuming resources.
    third_leaves = [f"l:2:0:{j}" for j in range(t)]
    restored_edges = [["s:2", Z], *[[Z, v] for v in third_leaves]]
    require(Counter(graph["vertices"]) == Counter(core_graph["vertices"]) + Counter([Z, *third_leaves])
            and edges_of(graph["edges"]) == edges_of(core_graph["edges"]) + edges_of(restored_edges)
            and all(graph["roles"][v] == role for v, role in core_graph["roles"].items()),
            "incorrect third-branch lift on original")
    require(all(prefix[v] == g + 1 for v, g in core_record["labels"].items() if v != FINAL)
            and prefix[Z] == 0 and [prefix[v] for v in third_leaves] == list(range(r + 13, m + 1)),
            "incorrect shift or third labels")
    pending = [edge for edge in graph["edges"] if not all(v in prefix for v in edge)]
    require(Counter(graph["vertices"]) == Counter(prefix.keys()) + Counter([FINAL])
            and edges_of(pending) == edges_of([FINAL_EDGE]) and PORT in prefix,
            "incorrect singleton original boundary")
    partial = verify_partial(graph, prefix)
    placed = ledger([edge for edge in graph["edges"] if all(v in prefix for v in edge)], prefix)
    unused_labels = sorted(set(range(m + 1)) - set(prefix.values()))
    unused_differences = sorted(set(range(1, m + 1)) - set(spectrum(placed)))
    require(partial["valid"] and partial["graph_digest"] == original["graph_digest"]
            and partial["unused_labels"] == unused_labels == [r + 4]
            and partial["unused_differences"] == unused_differences == [6]
            and partial["frontier"] == [PORT] and prefix[PORT] == r + 10,
            "wrong physical singleton resources")
    final_label = unused_labels[0]
    difference = abs(prefix[PORT] - final_label)
    require(difference == unused_differences[0], "final assignment does not consume missing difference")
    labels = {**prefix, FINAL: final_label}
    require(labels[FINAL] == core_record["labels"][FINAL] + 1
            and all(labels[v] == value for v, value in prefix.items()), "completion changed old labels")
    cut = cut_state(graph, labels, r + 2)
    crossing = edges_of(row["edge"] for row in cut["crossing"])
    require(crossing == edges_of(row["edge"] for row in core_record["cut"]["crossing"]) + edges_of(restored_edges),
            "ordinary cut is not the translated core cut plus the restored edges")
    return {"parameters": {"r": r, "t": t, "K": 1}, "original": original, "labels": labels,
            "core": {"saved_certificate": core_record["saved_certificate"], "recheck": core_ref,
                     "graph_digest": core_record["original"]["graph_digest"]},
            "verification": bound_full(graph, labels, original["graph_digest"]),
            "witness": witness(graph, labels), "edge_ledger": ledger(graph["edges"], labels),
            "zero_host": {"vertex": Z, "label": labels[Z]},
            "cut": cut, "prefix": prefix, "partial_verification": partial, "prefix_edge_ledger": placed,
            "prefix_witness": witness(graph, prefix), "remaining_vertices": [FINAL], "crossing_edge": FINAL_EDGE,
            "unused_labels": unused_labels, "unused_differences": unused_differences,
            "port": {"vertex": PORT, "label": prefix[PORT]},
            "completion": {"vertex": FINAL, "label": final_label, "edge": FINAL_EDGE, "difference": difference}}


def recheck_control(config, r, t, K, n, core):
    graph, original, saved, cert = load_retained(config, f"target-r{r}.json", r, t, n)
    require(cert["parameters"] == {"r": r, "third": t, "K": K}
            and cert["core"] == {"path": f"core-r{r}.json", "sha256_raw": core[1]["saved_certificate"]["sha256_raw"]},
            "retained complete control is not bound to the retained core")
    require(cert["prefix"] == direct_prefix(r, t), "retained control differs from symbolic prefix")
    record = finish(r, t, graph, original, cert["prefix"], core)
    inherited = set(record).intersection(cert) - {"parameters", "original", "core"}
    require(all(record[key] == cert[key] for key in inherited), "retained completed certificate differs")
    record["saved_certificate"] = saved
    ref = save(OUTPUT / f"recheck-target-r{r}-t{t}.json", record, config["max_result_bytes"])
    return graph, record, ref


def step(source, destination, r, t, end_t):
    before_graph, before, before_ref = source
    graph, after, after_ref = destination
    order = len(before_graph["vertices"])
    names = [f"l:2:0:{j}" for j in range(t, end_t)]
    fresh = {v: order + i for i, v in enumerate(names)}
    new_edges = [[Z, v] for v in names]
    grown = {**before["labels"], **fresh}
    require(Counter(graph["vertices"]) == Counter(before_graph["vertices"]) + Counter(names)
            and edges_of(graph["edges"]) == edges_of(before_graph["edges"]) + edges_of(new_edges)
            and all(graph["roles"][v] == role for v, role in before_graph["roles"].items()),
            "growth changes original names, roles or incidences")
    require(grown == after["labels"] and grown[Z] == 0
            and sorted(grown.values()) == list(range(r + end_t + 13))
            and spectrum(ledger(graph["edges"], grown)) == list(range(1, r + end_t + 13))
            and cut_state(graph, grown, r + 2) == after["cut"]
            and spectrum(ledger(new_edges, grown)) == list(range(order, order + len(names))),
            "growth partition, returned hosts or named equality failed")
    for key in ("zero_host", "port", "unused_labels", "unused_differences", "completion"):
        require(before[key] == after[key], f"growth changed {key}")
    return {"from_t": t, "to_t": end_t, "before": before_ref, "after": after_ref,
            "fresh": fresh, "edges": new_edges, "label_spectrum": sorted(grown.values()),
            "difference_spectrum": spectrum(ledger(graph["edges"], grown)),
            "crossing_spectrum": after["cut"]["crossing_spectrum"],
            **{key: after[key] for key in ("zero_host", "port", "unused_labels", "unused_differences", "completion")}}


def compare(config, states):
    route_records = []
    for route in config["growth_routes"]:
        stages = [step(states[a], states[b], 3, a, b) for a, b in zip(route, route[1:])]
        require(stages[-1]["after"] == states[5][2], "growth route does not end on direct r=3,t=5")
        route_records.append({"t_values": route, "stages": stages})
    require({v: states[5][1]["labels"][v] for v in ("l:2:0:3", "l:2:0:4")} ==
            {"l:2:0:3": 19, "l:2:0:4": 20}, "wrong final third terminal labels")
    return {"r": 3, "K": 1, "direct": states[5][2], "routes": route_records, "additional_graph_records": 0}


def reject_inputs(config):
    receipts = []
    with patch(__name__ + ".build_graph", side_effect=AssertionError("invalid input reached graph builder")) as builder:
        for values in config["invalid"]:
            try:
                hold_target(*values, config)
            except ValueError as error:
                receipts.append({"arguments": values, "types": [type(v).__name__ for v in values],
                                 "error": str(error), "graph_builder_calls": builder.call_count})
            else:
                raise ValueError("invalid parameters accepted")
        require(builder.call_count == 0 and len(receipts) == 8, "invalid-input scope")
    return receipts


def wrong_digest(target, config):
    graph, record, ref = target
    actual = record["original"]["graph_digest"]
    wrong = ("1" if actual[0] == "0" else "0") + actual[1:]
    check = verify_certificate(graph, record["labels"], wrong)
    require(check == {**record["verification"], "valid": False, "errors": ["original graph digest mismatch"]},
            "wrong-digest claim was not rejected as expected")
    require(config["adverse"]["kind"] == "mismatched original-graph digest"
            and {k: config["adverse"][k] for k in ("r", "t", "K")} == record["parameters"], "wrong adverse target")
    return {"parameters": record["parameters"], "kind": config["adverse"]["kind"], "certificate": ref,
            "gist": "Same original named graph and labels with only the expected digest changed",
            "actual_graph_digest": actual, "supplied_graph_digest": wrong, "verification": check,
            "additional_graph_records": 0}


def main():
    config_path = HERE / "config.json"
    config = read(config_path)
    cap = config["max_result_bytes"]
    require(git("rev-parse", "HEAD").decode().strip() == PARENT == config["parent"], "unexpected accepted parent")
    require(config["worker_count"] == 1 and config["max_vertices"] == 24 and cap == 2_000_000 and config["K"] == 1
            and config["solver_queries"] == config["labeling_enumeration"] == config["historical_replays"] == 0
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "wrong limits or runtime")
    OUTPUT.mkdir()
    snapshots = {}
    for name in SOURCES:
        raw = (ROOT / name).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{name}").replace(b"\r\n", b"\n"),
                f"source differs from parent: {name}")
        put(OUTPUT / "source" / name, raw, cap)
        snapshots[name] = sha(raw)
    retained_names = [f"core-r{r}.json" for r, _ in config["retained_cores"]]
    retained_names.append(f"target-r{config['retained_control'][0]}.json")
    retained_paths = [f"{config['retained_bundle']}{where}/{name}"
                      for name in retained_names for where in ("", "/originals")]
    identity = {"run_id": config["run_id"], "parent": PARENT, "source_sha256_raw": snapshots,
                "config_sha256_raw": sha(config_path.read_bytes()),
                "runner_sha256_raw": sha(Path(__file__).read_bytes()), "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
                "proof": {"path": PROOF, "sha256_raw": sha((ROOT / PROOF).read_bytes())},
                "retained_sha256_raw": {path: sha((ROOT / path).read_bytes()) for path in retained_paths},
                "runtime": {"python": sys.version, "implementation": sys.implementation.name,
                            "optional_dependencies": [], "platform": platform.platform(),
                            "python_executable": ".venv/Scripts/python.exe", "utf8_mode": sys.flags.utf8_mode}}
    identity_ref = save(OUTPUT / "identity.json", identity, cap)
    invalid = save(OUTPUT / "domain_rejections.json", reject_inputs(config), cap)
    originals = {}
    for r, t, K, n in config["targets"]:
        require(K == 1 and plan(r, t) == n, "declared target or order mismatch")
        originals[(r, t)] = hold_target(r, t, config)
    cores = {r: recheck_core(config, r, n) for r, n in config["retained_cores"]}
    r0, t0, K0, n0 = config["retained_control"]
    control = recheck_control(config, r0, t0, K0, n0, cores[r0])
    targets = {}
    completed = []
    for (r, t), (graph, original) in originals.items():
        record = finish(r, t, graph, original, direct_prefix(r, t), cores[r])
        path = OUTPUT / f"target-r{r}-t{t}.json"
        ref = save(path, record, cap)
        targets[(r, t)] = graph, record, ref
        completed.append({**ref, "n": record["verification"]["n"], "bytes": path.stat().st_size})
    growth = save(OUTPUT / "growth.json", compare(config, {3: control, 4: targets[(3, 4)], 5: targets[(3, 5)]}), cap)
    adverse = save(OUTPUT / "adverse.json", wrong_digest(targets[(3, 4)], config), cap)
    summary = {"status": "PASS", "run_id": config["run_id"], "identity": identity_ref,
               "retained_cores": [item[2] for item in cores.values()], "retained_completed_control": control[2],
               "new_completed_targets": completed, "graph_records": 8, "growth": growth, "invalid_inputs": invalid,
               "adverse": adverse, "domain_rejections": 8, "adverse_checks": 1,
               "solver_queries": 0, "labeling_enumeration": 0, "historical_replays": 0}
    save(OUTPUT / "summary.json", summary, cap)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
