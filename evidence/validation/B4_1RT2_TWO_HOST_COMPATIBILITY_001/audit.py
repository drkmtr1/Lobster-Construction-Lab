"""Independent standard-library audit of the exact eleven saved graph records."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "eb5745483186287b20bcf155cf4e5265dbfc20a5"
OLD_T = "evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/validation"
OLD_R = "evidence/validation/B4_1R32_MINIMUM_HIGH_SUPPLIER_001/validation"
CONTROLS = {(2, 3): (OLD_T, "normalized-t3.json"), (5, 3): (OLD_R, "normalized-r5.json"),
            (2, 4): (OLD_T, "normalized-t4.json"), (2, 5): (OLD_T, "normalized-t5.json")}
PREFIXES = ((3, 4), (3, 5), (5, 5))
TARGETS = ((3, 4, 2), (3, 4, 3), (3, 5, 4), (5, 5, 5))
ROUTES = (
    ("H3,Z2", (2, 3), (("H", 3, (5, 3)), ("Z", 2, (5, 5)))),
    ("Z2,H3", (2, 3), (("Z", 2, (2, 5)), ("H", 3, (5, 5)))),
    ("Z1,H1,Z1,H2", (2, 3), (("Z", 1, (2, 4)), ("H", 1, (3, 4)), ("Z", 1, (3, 5)), ("H", 2, (5, 5)))),
    ("H subdivision", (2, 5), (("H", 1, (3, 5)), ("H", 2, (5, 5)))),
    ("Z subdivision", (2, 3), (("Z", 1, (2, 4)), ("Z", 1, (2, 5)))),
)
BAD = ((True, 4, 2), (3.0, 4, 2), ("3", 4, 2), (2, 4, 2),
       (3, True, 2), (3, 4.0, 2), (3, "4", 2), (3, 3, 2),
       (3, 4, True), (3, 4, 2.0), (3, 4, "2"), (3, 4, 1))
L, U, H, Z = "b:0:0", "s:4", "b:1:0", "b:2:0"
SEED = {
    "s:0": 11, "s:1": 7, "s:2": 16, "s:3": 4, U: 9,
    L: 1, "l:0:0:0": 12, H: 8, "l:1:0:0": 6, "l:1:0:1": 5,
    Z: 0, "l:2:0:0": 13, "l:2:0:1": 14, "l:2:0:2": 15,
    "b:3:0": 10, "l:3:0:0": 2, "l:3:0:1": 3,
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def span(start, stop):
    return list(range(start, stop + 1))


def pair(edge):
    return tuple(sorted(edge))


def multiplicities(edges):
    return Counter(pair(edge) for edge in edges)


def topology(r, t, K):
    spine = [f"s:{i}" for i in range(K + 5)]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, size in enumerate((1, r, t, 2)):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(size):
            terminal = f"l:{i}:0:{j}"
            roles[terminal] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, terminal))
    profile = [[1], [r], [t], [2]] + [[] for _ in range(K + 1)]
    return roles, edges, spine, profile


def original(path, reference, r, t, K):
    payload = read(path)
    graph = payload["graph"]
    roles, edges, spine, profile = topology(r, t, K)
    require(Counter(graph["vertices"]) == Counter(roles.keys())
            and multiplicities(graph["edges"]) == multiplicities(edges), "original multiplicities or section names")
    require(graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
            and type(graph["schema_version"]) is int and graph["schema_version"] == 1, "original role or profile changed")
    canonical = {"vertices": sorted(roles), "edges": sorted(map(pair, edges)),
                 "roles": roles, "spine": spine, "profile": profile}
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    require(reference["graph_digest"] == payload["graph_digest"] == digest
            and reference["sha256_raw"] == sha(path) and len(roles) == len(edges) + 1 <= 27, "original digest or size")
    return graph, digest


def difference(u, v, labels):
    return abs(labels[u] - labels[v])


def check_ledger(rows, edges, labels):
    require(Counter(pair(row["edge"]) for row in rows) == multiplicities(edges), "edge ledger multiplicities")
    require(all(row["difference"] == difference(*row["edge"], labels) for row in rows), "wrong edge ledger weight")


def graceful(record, graph, digest):
    labels, receipt = record["labels"], record["verification"]
    edges = graph["edges"]
    n = len(graph["vertices"])
    require(Counter(graph["vertices"]) == Counter(labels.keys()) and all(type(g) is int for g in labels.values())
            and sorted(labels.values()) == span(0, n - 1), "complete ordinary label bijection")
    differences = [difference(u, v, labels) for u, v in edges]
    require(sorted(differences) == span(1, n - 1), "complete original difference bijection")
    check_ledger(record["edge_ledger"], edges, labels)
    require(receipt["valid"] is True and receipt["errors"] == [] and receipt["n"] == n and receipt["m"] == n - 1
            and receipt["graph_digest"] == digest and receipt["edge_differences"] == differences, "full verifier receipt")
    return labels


def distances(record, graph, K):
    # From the reconstructed graph, each terminal's specified center and
    # each center's specified spine attachment are its only route to W.
    expected = {}
    for v, role in graph["roles"].items():
        if role["kind"] == "spine" or v == L:
            expected[v] = 0
        elif role["kind"] == "branch" or role["section"] == 0:
            expected[v] = 1
        else:
            expected[v] = 2
    require(record["witness"] == [L, *[f"s:{i}" for i in range(5 + K)]]
            and record["witness_distances"] == expected and expected[H] == expected[Z] == 1,
            "physical witness or distances")


def normalized(path, r, t, control=None):
    result = read(path)
    ref = result["original"]
    require(result["parameters"] == {"r": r, "t": t}, "normalized parameters")
    if control:
        bundle, filename = control
        old_file = ROOT / bundle / filename
        orig_rel = f"{bundle}/originals/{filename}"
        require(result["retained"] == {"certificate": old_file.relative_to(ROOT).as_posix(),
                                      "sha256_raw": sha(old_file)} and ref["path"] == orig_rel,
                "retained source binding")
        old = read(old_file)
        require(all(result[name] == old[name] for name in
                    ("labels", "verification", "alpha", "edge_ledger", "witness", "witness_distances"))
                and all(ref[name] == old["original"][name] for name in ("graph_digest", "sha256_raw")),
                "retained certificate contents")
        orig_path = ROOT / orig_rel
    else:
        require(ref["path"] == f"originals/{path.name}", "new normalized original path")
        orig_path = DATA / ref["path"]
    graph, digest = original(orig_path, ref, r, t, 0)
    labels = graceful(result, graph, digest)
    p, n = r + 6, r + t + 12
    lows = sorted(["s:1", "s:3", L, Z, "l:3:0:0", "l:3:0:1", *[f"l:1:0:{i}" for i in range(r)]])
    highs = sorted(set(graph["vertices"]) - set(lows))
    require(sorted(labels[v] for v in lows) == span(0, p - 1)
            and sorted(labels[v] for v in highs) == span(p, n - 1)
            and all((u in lows) != (v in lows) for u, v in graph["edges"]), "audited alpha classes")
    require(result["state"] == {"L": L, "U": U, "H": H, "Z": Z, "p": p, "n": n, "x": 1, "y": 1}
            and result["anchors"] == {L: 1, U: p + 1, H: p, Z: 0}
            and {v: labels[v] for v in (L, U, H, Z)} == result["anchors"]
            and result["alpha"] == {"low": lows, "high": highs, "low_size": p}, "ports, hosts or cut")
    # Check the three bands via the literal seed and global insertion order.
    h = r - 2
    require(all(labels[v] == value + h * (value >= 8) for v, value in SEED.items())
            and [labels[f"l:1:0:{j}"] for j in range(2, r)] == span(8, r + 5)
            and [labels[f"l:2:0:{j}"] for j in range(3, t)] == span(r + 15, n - 1), "named normalized formula")
    seed_edges = [edge for edge in graph["edges"] if all(v in SEED for v in edge)]
    fresh_weights = lambda sec, a, b: sorted(difference(f"b:{sec}:0", f"l:{sec}:0:{i}", labels) for i in range(a, b))
    require(sorted(difference(u, v, labels) for u, v in seed_edges) == span(r - 1, r + 14)
            and fresh_weights(1, 2, r) == span(1, h) and fresh_weights(2, 3, t) == span(r + 15, n - 1),
            "named normalized difference bands")
    distances(result, graph, 0)
    return graph, result, {"path": path.name, "sha256_raw": sha(path)}


def reflected_path(K):
    if K <= 4:
        return {2: [3, 1, 0], 3: [4, 1, 0, 2], 4: [5, 1, 2, 0, 3]}[K]
    return [K + 1, 1, K - 1] + [K - 2 - value for value in reflected_path(K - 3)]


def completed(r, t, K, state):
    filename = f"target-r{r}-t{t}-k{K}.json"
    path = DATA / filename
    record = read(path)
    ref = record["original"]
    require(record["parameters"] == {"r": r, "t": t, "K": K} and ref["path"] == f"originals/{filename}",
            "completed original path or parameters")
    graph, digest = original(DATA / ref["path"], ref, r, t, K)
    labels = graceful(record, graph, digest)
    p, m = r + 6, K + r + t + 11
    norm_graph, normalized_record, normalized_ref = state
    require(record["normalized"] == normalized_ref and record["high_shift_cut"] == p, "shared normalized binding")
    prefix = record["prefix_labels"]
    require(set(prefix) == set(norm_graph["vertices"])
            and all(prefix[v] == g + (K if v in normalized_record["alpha"]["high"] else 0)
                    for v, g in normalized_record["labels"].items())
            and all(labels[v] == g for v, g in prefix.items()), "prefix or updated high shift")
    used_r = sorted(prefix.values())
    used_d = sorted(difference(u, v, prefix) for u, v in norm_graph["edges"])
    require(used_r == span(0, p - 1) + span(p + K, m) and used_d == span(K + 1, m), "used inventories")
    R, D = sorted(set(span(0, m)) - set(used_r)), sorted(set(span(1, m)) - set(used_d))
    partial = record["partial_verification"]
    require(R == span(p, p + K - 1) and D == span(1, K)
            and partial["valid"] is True and partial["complete"] is False and partial["errors"] == []
            and partial["n"] == m + 1 and partial["m"] == m and partial["graph_digest"] == digest
            and partial["used_labels"] == used_r and partial["used_differences"] == used_d
            and partial["unused_labels"] == R and partial["unused_differences"] == D
            and partial["frontier"] == [U] and record["port"] == {"physical_vertex": U, "label": p + K + 1},
            "unused resources, partial receipt, or port")
    path_vertices = graph["spine"][4:]
    path_edges = list(zip(path_vertices, path_vertices[1:]))
    pending = [edge for edge in graph["edges"] if not set(edge).issubset(prefix)]
    crossing = [edge for edge in pending if sum(v in prefix for v in edge) == 1]
    require(record["path"] == path_vertices and record["pending_vertices"] == path_vertices[1:]
            and Counter(graph["vertices"]) == Counter(prefix.keys()) + Counter(path_vertices[1:])
            and multiplicities(pending) == multiplicities(path_edges) == multiplicities(record["pending_edges"])
            and multiplicities(crossing) == multiplicities([(U, "s:5")]) == multiplicities(record["crossing_edges"])
            and multiplicities(graph["edges"]) == multiplicities(path_edges) + multiplicities(norm_graph["edges"]),
            "physical path contract")
    sequence = [labels[v] for v in path_vertices]
    require(sequence == [p + v for v in reflected_path(K)] == record["numeric_sequence"]
            and sequence[0] == prefix[U] and sorted(sequence[1:]) == R
            and sorted(difference(u, v, labels) for u, v in path_edges) == D, "physical sequence or consumption")
    check_ledger(record["path_edge_ledger"], path_edges, labels)
    distances(record, graph, K)
    return {"path": filename, "sha256_raw": sha(path), "bytes": path.stat().st_size, "n": m + 1}


def routes(states):
    record = read(DATA / "routes.json")
    require(len(record["routes"]) == len(ROUTES), "route count")
    for (name, current, steps), saved in zip(ROUTES, record["routes"]):
        require(saved["name"] == name and len(saved["steps"]) == len(steps), "route identity")
        for (op, count, destination), step in zip(steps, saved["steps"]):
            graph, before, from_ref = states[current]
            next_graph, after, to_ref = states[destination]
            r, t = current
            require(destination == (r + count, t) if op == "H" else destination == (r, t + count),
                    "batch endpoints")
            old, new = before["labels"], after["labels"]
            fresh = set(next_graph["vertices"]) - set(graph["vertices"])
            if op == "H":
                # Determine high vertices by the saved original alpha partition,
                # whose topology and numerical cut were already independently checked.
                changed = {v: [old[v], old[v] + count] for v in before["alpha"]["high"]}
                host, start, next_value = H, r, len(before["alpha"]["low"])
                expected = {f"l:1:0:{start+i}": next_value + i for i in range(count)}
            else:
                changed = {}
                host, start, next_value = Z, t, len(graph["vertices"])
                expected = {f"l:2:0:{start+i}": next_value + i for i in range(count)}
            added = [(host, v) for v in fresh]
            require(fresh == set(expected) and all(new[v] == expected[v] for v in fresh)
                    and all(new[v] == (changed[v][1] if v in changed else old[v]) for v in old)
                    and multiplicities(next_graph["edges"]) == multiplicities(graph["edges"]) + multiplicities(added),
                    "named route transition")
            require(step["operation"] == op and step["count"] == count and step["from"] == list(current)
                    and step["to"] == list(destination) and step["input_certificate"] == from_ref
                    and step["output_certificate"] == to_ref and step["new_leaf_assignments"] == expected
                    and step["shifted_old_labels"] == changed
                    and multiplicities(step["new_edges"]) == multiplicities(added)
                    and step["edge_spectrum"] == span(1, len(next_graph["edges"]))
                    and all(step[key] == after[key] for key in ("state", "anchors", "alpha", "witness", "witness_distances")),
                    "route receipt or returned state")
            current = destination
        require(saved["endpoint"] == states[current][2], "route endpoint certificate")
    final, z_end = states[(5, 5)][2], states[(2, 5)][2]
    require(record["direct"] == record["H_subdivision_endpoint"] == final
            and record["Z_subdivision_endpoint"] == z_end and record["additional_graph_cases"] == 0,
            "subdivision endpoints")
    leaves = {
        "l:1:0:2": 8, "l:1:0:3": 9, "l:1:0:4": 10, "l:2:0:3": 20, "l:2:0:4": 21,
    }
    require(all(states[(5, 5)][1]["labels"][v] == g for v, g in leaves.items()), "final fresh labels")
    mixed = record["routes"][2]["steps"]
    require(mixed[0]["new_leaf_assignments"] == {"l:2:0:3": 17}
            and mixed[1]["shifted_old_labels"]["l:2:0:3"] == [17, 18]
            and mixed[2]["new_leaf_assignments"] == {"l:2:0:4": 19}
            and mixed[3]["shifted_old_labels"]["l:2:0:3"] == [18, 20]
            and mixed[3]["shifted_old_labels"]["l:2:0:4"] == [19, 21], "mixed fresh-label trajectory")


def argument_rows(rows):
    return [tuple((type(value).__name__, value) for value in row) for row in rows]


def main():
    config = read(HERE / "config.json")
    require(config["parent"] == PARENT and config["workers"] == 1 and config["max_vertices"] == 27
            and config["max_result_bytes"] == 2_000_000
            and config["solver_queries"] == config["computational_enumeration"] == config["historical_search_replay"] == 0,
            "config bounds")
    require(config["prefixes"] == [[r, t, r + t + 12] for r, t in PREFIXES]
            and config["targets"] == [[r, t, K, r + t + K + 12] for r, t, K in TARGETS]
            and config["controls"] == [{"r": r, "t": t, "n": r + t + 12, "certificate": f"{bundle}/{filename}",
                                       "original": f"{bundle}/originals/{filename}"}
                                      for (r, t), (bundle, filename) in CONTROLS.items()]
            and config["routes"] == [{"name": name, "start": list(start),
                                      "steps": [[axis, count, *dest] for axis, count, dest in steps]}
                                     for name, start, steps in ROUTES]
            and argument_rows(config["invalid"]) == argument_rows(BAD), "config cases, routes or types")
    checks = read(DATA / "domain_rejections.json")
    require(argument_rows(row["arguments"] for row in checks) == argument_rows(BAD), "rejection arguments")
    for i, row in enumerate(checks):
        name, minimum = (("r", 3), ("t", 4), ("K", 2))[i // 4]
        require(row["types"] == [type(v).__name__ for v in BAD[i]]
                and row["rejected"] is True and row["graph_builder_calls"] == 0
                and row["reason"] == f"{name} must be an exact integer >= {minimum}", "invalid argument receipt")
    identity = read(DATA / "identity.json")
    require(identity["parent"] == PARENT and identity["run_id"] == config["run_id"]
            and identity["runtime"]["implementation"] == "cpython" and identity["runtime"]["utf8_mode"] == 1
            and identity["runtime"]["python"].startswith(("3.12.", "3.13."))
            and identity["runtime"]["optional_dependencies"] == [], "runtime identity")
    for filename, key in (("config.json", "config_sha256_raw"), ("validate.py", "runner_sha256_raw"),
                          ("audit.py", "audit_sha256_raw")):
        require(sha(HERE / filename) == identity[key], "current executable evidence hash")
    require(set(identity["proofs_sha256_raw"]) == {"research/ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md", "research/B4_1RT2_TWO_HOST_COMPATIBILITY.md"}
            and set(identity["retained_sha256_raw"]) == {f"{b}{loc}/{name}" for b, name in CONTROLS.values()
                                                        for loc in ("", "/originals")}
            and set(identity["source_sha256_raw"]) == {"lcl/__init__.py", "lcl/model.py", "lcl/verify.py",
                "lcl/consumers.py", "lcl/states.py", "pyproject.toml", "requirements.txt"}, "identity inventory")
    for key in ("proofs_sha256_raw", "retained_sha256_raw"):
        for rel, digest in identity[key].items():
            require(sha(ROOT / rel) == digest, "raw retained or proof bytes")
    for rel, digest in identity["source_sha256_raw"].items():
        raw = (DATA / "source" / rel).read_bytes()
        current = (ROOT / rel).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest
                and raw.replace(b"\r\n", b"\n") == current.replace(b"\r\n", b"\n"), "source snapshot")
    states = {(r, t): normalized(DATA / f"retained-r{r}-t{t}.json", r, t, control)
              for (r, t), control in CONTROLS.items()}
    states.update({(r, t): normalized(DATA / f"normalized-r{r}-t{t}.json", r, t) for r, t in PREFIXES})
    routes(states)
    targets = [completed(r, t, K, states[(r, t)]) for r, t, K in TARGETS]
    summary = read(DATA / "summary.json")
    routes_hash, rejections_hash = sha(DATA / "routes.json"), sha(DATA / "domain_rejections.json")
    require(summary == {"status": "PASS", "run_id": config["run_id"], "identity_sha256_raw": sha(DATA / "identity.json"),
                        "controls": [states[key][2] for key in CONTROLS],
                        "prefixes": [states[key][2] for key in PREFIXES], "targets": targets,
                        "routes_sha256_raw": routes_hash, "domain_rejections_sha256_raw": rejections_hash,
                        "domain_rejections": 12, "checked_graph_records": 11, "new_graph_records": 7,
                        "solver_queries": 0, "computational_enumeration": 0, "historical_search_replay": 0}, "summary")
    require(len(list((DATA / "originals").glob("*.json"))) == 7
            and len(list(DATA.glob("retained-*.json"))) == 4 and len(list(DATA.glob("normalized-*.json"))) == 3
            and len(list(DATA.glob("target-*.json"))) == 4
            and all(path.stat().st_size <= config["max_result_bytes"] for path in DATA.rglob("*") if path.is_file()),
            "saved case counts or byte caps")
    outcome = {"status": "PASS", "run_id": config["run_id"], "same_retained_controls": summary["controls"],
               "same_normalized_prefixes": summary["prefixes"], "same_completed_targets": targets,
               "same_route_comparisons": len(ROUTES), "same_domains_rejected": 12,
               "routes_sha256_raw": routes_hash, "domain_rejections_sha256_raw": rejections_hash,
               "additional_graph_cases": 0, "solver_queries": 0}
    require(sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "audit runtime")
    raw = (json.dumps(outcome, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= config["max_result_bytes"], "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as stream:
        stream.write(raw)
    print(json.dumps(outcome, sort_keys=True))


if __name__ == "__main__":
    main()
