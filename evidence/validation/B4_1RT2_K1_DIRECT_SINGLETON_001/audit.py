"""Independent standard-library audit of the eight saved 1RT2 records."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "3e10c022f834cfae053aaef9581697bf6c21002d"
OLD = "evidence/validation/B4_1R32_K1_ROOTED_CORE_001/validation"
PROOF = "research/B4_1RT2_K1_DIRECT_SINGLETON.md"
TARGETS = ((3, 4, 1, 20), (3, 5, 1, 21), (4, 4, 1, 21), (5, 6, 1, 24))
CORES = ((3, 15), (4, 16), (5, 17))
CONTROL = (3, 3, 1, 19)
ROUTES = ((3, 5), (3, 4, 5))
BAD = ((True, 4), (3.0, 4), ("3", 4), (2, 4), (3, True), (3, 4.0), (3, "4"), (3, 3))
H, Z = "b:1:0", "b:2:0"
PORT, LAST = "s:4", "s:5"
EDGE = [PORT, LAST]
SEED = {
    "s:0": 8, "s:1": 0, "s:2": 13, "s:3": 1, PORT: 11, LAST: 5,
    "b:0:0": 4, "l:0:0:0": 3, H: 9, "l:1:0:0": 6, "l:1:0:1": 2,
    "b:3:0": 12, "l:3:0:0": 10, "l:3:0:1": 7,
}
SOURCE_SET = {"lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "requirements.txt", "pyproject.toml"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_ref(path):
    return {"path": path.name, "sha256_raw": sha(path)}


def span(lo, hi):
    return list(range(lo, hi + 1))


def typed(values):
    return [(type(value).__name__, value) for value in values]


def pair(edge):
    return tuple(sorted(edge))


def multiplicity(edges):
    return Counter(pair(edge) for edge in edges)


def topology(r, t):
    spine = [f"s:{i}" for i in range(6)]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    profile = [[] for _ in spine]
    counts = {0: 1, 1: r, 3: 2}
    if t is not None:
        counts[2] = t
    for i, terminals in counts.items():
        profile[i] = [terminals]
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(terminals):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
    return roles, edges, spine, profile


def original(path, ref, r, t, n):
    saved = read(path)
    graph = saved["graph"]
    roles, named_edges, spine, profile = topology(r, t)
    # Account for every raw vertex and edge occurrence before set/map checks.
    require(Counter(graph["vertices"]) == Counter(roles.keys())
            and multiplicity(graph["edges"]) == multiplicity(named_edges), "original named multiplicities")
    require(graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
            and type(graph["schema_version"]) is int and graph["schema_version"] == 1, "original roles or sections")
    canonical = {"vertices": sorted(roles), "edges": sorted(map(pair, named_edges)),
                 "roles": roles, "spine": spine, "profile": profile}
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    require(ref["graph_digest"] == saved["graph_digest"] == digest and ref["sha256_raw"] == sha(path)
            and len(roles) == n == len(named_edges) + 1 <= 24, "original digest, binding or order")
    return graph, digest


def difference(u, v, labels):
    return abs(labels[u] - labels[v])


def weights(edges, labels):
    return [difference(u, v, labels) for u, v in edges]


def check_ledger(rows, edges, labels):
    require(Counter(pair(row["edge"]) for row in rows) == multiplicity(edges), "edge ledger multiplicities")
    require(all(row["difference"] == difference(*row["edge"], labels) for row in rows), "edge ledger weight")


def graceful(record, graph, digest):
    labels, receipt = record["labels"], record["verification"]
    n = len(graph["vertices"])
    require(Counter(graph["vertices"]) == Counter(labels.keys()) and all(type(g) is int for g in labels.values())
            and sorted(labels.values()) == span(0, n - 1), "complete label alphabet")
    differences = weights(graph["edges"], labels)
    require(sorted(differences) == span(1, n - 1), "original complete difference alphabet")
    check_ledger(record["edge_ledger"], graph["edges"], labels)
    require(receipt["valid"] is True and receipt["errors"] == [] and receipt["n"] == n
            and receipt["m"] == n - 1 and receipt["graph_digest"] == digest
            and receipt["edge_differences"] == differences, "full unchanged-verifier receipt")
    return labels


def witness(record, graph, prefix=False):
    omitted = [LAST] if prefix else []
    expected = {v: {"spine": 0, "branch": 1, "leaf": 2}[role["kind"]]
                for v, role in graph["roles"].items() if v not in omitted}
    require(record == {"path": [v for v in graph["spine"] if v not in omitted], "distances": expected},
            "physical spine witness or distances")
    require(expected[H] == 1 and (Z not in expected or expected[Z] == 1), "host witness distance")


def check_cut(record, graph, labels, c, b):
    below = sorted(v for v, g in labels.items() if g < c)
    crossing = [(u, v) for u, v in graph["edges"] if (u in below) != (v in below)]
    other = [(u, v) for u, v in graph["edges"] if (u in below) == (v in below)]
    m = len(graph["edges"])
    crossing_band, other_band = sorted(weights(crossing, labels)), sorted(weights(other, labels))
    require(record["c"] == c and record["host"] == H and record["host_label"] == labels[H] == b
            and record["m"] == m and record["below"] == below and 1 <= c <= b <= m
            and crossing_band == record["crossing_spectrum"] == span(b - c + 1, m)
            and other_band == record["noncrossing_spectrum"] == span(1, 6)
            and pair(EDGE) in multiplicity(other) and difference(*EDGE, labels) == 6, "ordinary cut premise")
    check_ledger(record["crossing"], crossing, labels)
    check_ledger(record["noncrossing"], other, labels)
    return crossing, other


def historical(record, filename):
    source = ROOT / OLD / filename
    orig_path = f"{OLD}/originals/{filename}"
    old = read(source)
    binding = {"path": f"{OLD}/{filename}", "sha256_raw": sha(source)}
    require(record["saved_certificate"] == binding and record["original"]["path"] == orig_path
            and old["original"] == {**record["original"], "path": f"originals/{filename}"},
            "historical source and original binding")
    same = set(old).intersection(record) - {"original", "core", "parameters"}
    require(all(old[key] == record[key] for key in same), "historical certificate changed")
    return old, ROOT / orig_path


def core(r, n):
    file = DATA / f"recheck-core-r{r}.json"
    record = read(file)
    old, orig_path = historical(record, f"core-r{r}.json")
    graph, digest = original(orig_path, record["original"], r, None, n)
    labels = graceful(record, graph, digest)
    require(record["r"] == old["r"] == r and record["root"] == {"vertex": "s:2", "label": n - 1}
            and labels["s:2"] == n - 1, "physical maximum of retained core")
    require(all(labels[v] == g + (r - 2 if g >= 3 else 0) for v, g in SEED.items())
            and [labels[f"l:1:0:{j}"] for j in range(2, r)] == span(3, r), "retained core formula")
    crossing, other = check_cut(record["cut"], graph, labels, r + 1, r + 7)
    new_edges = [(H, f"l:1:0:{j}") for j in range(2, r)]
    require(not (multiplicity(new_edges) - multiplicity(crossing)), "fresh second edges not in the crossing set")
    original_crossing = [edge for edge in crossing if pair(edge) not in multiplicity(new_edges)]
    bands = {"old_noncrossing": sorted(weights(other, labels)),
             "new_second_terminal_edges": sorted(weights(new_edges, labels)),
             "shifted_original_crossings": sorted(weights(original_crossing, labels))}
    require(record["core_difference_bands"] == bands == {
        "old_noncrossing": span(1, 6), "new_second_terminal_edges": span(7, r + 4),
        "shifted_original_crossings": span(r + 5, r + 11)}, "core difference bands")
    witness(record["witness"], graph)
    return graph, record, file_ref(file)


def target(r, t, K, n, core_data, retained=False):
    name = f"target-r{r}-t{t}.json"
    file = DATA / (f"recheck-{name}" if retained else name)
    record = read(file)
    ref = record["original"]
    require(record["parameters"] == {"r": r, "t": t, "K": K}, "completed declared parameters")
    cg, cr, checked_core = core_data
    require(record["core"] == {"saved_certificate": cr["saved_certificate"], "recheck": checked_core,
                               "graph_digest": cr["original"]["graph_digest"]}, "core reference")
    if retained:
        old, orig_path = historical(record, f"target-r{r}.json")
        require(old["parameters"] == {"r": r, "third": t, "K": K}
                and old["core"] == {"path": f"core-r{r}.json", "sha256_raw": cr["saved_certificate"]["sha256_raw"]},
                "retained control core link or parameters")
    else:
        require(ref["path"] == f"originals/{name}", "new original retention path")
        orig_path = DATA / ref["path"]
    graph, digest = original(orig_path, ref, r, t, n)
    labels = graceful(record, graph, digest)
    m = n - 1
    third_names = [f"l:2:0:{j}" for j in range(t)]
    restored = [("s:2", Z), *[(Z, v) for v in third_names]]
    require(Counter(graph["vertices"]) == Counter(cg["vertices"]) + Counter([Z, *third_names])
            and multiplicity(graph["edges"]) == multiplicity(cg["edges"]) + multiplicity(restored)
            and all(graph["roles"][v] == role for v, role in cg["roles"].items()), "original core topology in lifted target")
    require(labels[Z] == 0 and record["zero_host"] == {"vertex": Z, "label": 0}
            and labels["s:2"] == r + 12 and all(labels[v] == value + 1 for v, value in cr["labels"].items())
            and [labels[v] for v in third_names] == span(r + 13, m), "core translation and prescribed third labels")
    require(sorted(weights(cg["edges"], labels)) == span(1, r + 11)
            and weights(restored, labels) == span(r + 12, m), "lift difference partition")
    crossing, _ = check_cut(record["cut"], graph, labels, r + 2, r + 8)
    require(multiplicity(crossing) == multiplicity(row["edge"] for row in cr["cut"]["crossing"])
            + multiplicity(restored), "lifted cut crossing set")
    prefix = record["prefix"]
    require(Counter(graph["vertices"]) == Counter(prefix.keys()) + Counter([LAST])
            and all(labels[v] == f for v, f in prefix.items()), "prefix preservation")
    placed = [edge for edge in graph["edges"] if all(v in prefix for v in edge)]
    pending = [edge for edge in graph["edges"] if edge not in placed]
    R = sorted(set(span(0, m)) - set(prefix.values()))
    D = sorted(set(span(1, m)) - set(weights(placed, prefix)))
    require(multiplicity(pending) == multiplicity([EDGE]) == multiplicity([record["crossing_edge"]])
            and record["remaining_vertices"] == [LAST] and record["unused_labels"] == R == [r + 4]
            and record["unused_differences"] == D == [6] and record["port"] == {"vertex": PORT, "label": r + 10}
            and prefix[PORT] == r + 10 and record["completion"] == {"vertex": LAST, "label": labels[LAST],
                                                                 "edge": EDGE, "difference": difference(*EDGE, labels)}
            and labels[LAST] == R[0] and difference(*EDGE, labels) == D[0], "original singleton contract")
    check_ledger(record["prefix_edge_ledger"], placed, prefix)
    partial = record["partial_verification"]
    require(partial["valid"] is True and partial["errors"] == [] and partial["graph_digest"] == digest
            and partial["n"] == n and partial["m"] == m and partial["complete"] is False and partial["frontier"] == [PORT]
            and partial["used_labels"] == sorted(prefix.values()) and partial["used_differences"] == sorted(weights(placed, prefix))
            and partial["unused_labels"] == R and partial["unused_differences"] == D, "partial verifier receipt")
    witness(record["witness"], graph)
    witness(record["prefix_witness"], graph, prefix=True)
    if (r, t) == (3, 4):
        require(weights(graph["edges"], labels) == [9, 14, 13, 11, 6, 4, 1, 10, 3, 8, 7,
                                                   15, 16, 17, 18, 19, 12, 2, 5], "smallest declared original ledger")
    return graph, record, file_ref(file)


def growth(states):
    path = DATA / "growth.json"
    receipts = read(path)
    direct = states[5][2]
    require(receipts["r"] == 3 and receipts["K"] == 1 and receipts["direct"] == direct
            and receipts["additional_graph_records"] == 0
            and [tuple(row["t_values"]) for row in receipts["routes"]] == list(ROUTES), "growth scope")
    for route, receipt in zip(ROUTES, receipts["routes"]):
        require(len(receipt["stages"]) == len(route) - 1, "growth stage count")
        for t, next_t, stage in zip(route, route[1:], receipt["stages"]):
            graph, before, start = states[t]
            grown_graph, after, finish = states[next_t]
            new_names = [f"l:2:0:{j}" for j in range(t, next_t)]
            fresh = dict(zip(new_names, span(len(graph["vertices"]), len(grown_graph["vertices"]) - 1)))
            additions = [(Z, v) for v in new_names]
            require(after["labels"] == {**before["labels"], **fresh}
                    and Counter(grown_graph["vertices"]) == Counter(graph["vertices"]) + Counter(new_names)
                    and multiplicity(grown_graph["edges"]) == multiplicity(graph["edges"]) + multiplicity(additions)
                    and all(grown_graph["roles"][v] == role for v, role in graph["roles"].items()), "growth named equality")
            require(stage["from_t"] == t and stage["to_t"] == next_t and stage["before"] == start and stage["after"] == finish
                    and stage["fresh"] == fresh and multiplicity(stage["edges"]) == multiplicity(additions)
                    and stage["label_spectrum"] == sorted(after["labels"].values())
                    and stage["difference_spectrum"] == sorted(weights(grown_graph["edges"], after["labels"]))
                    and stage["crossing_spectrum"] == after["cut"]["crossing_spectrum"], "growth receipt")
            require(all(stage[key] == after[key] == before[key]
                        for key in ("zero_host", "port", "unused_labels", "unused_differences", "completion")),
                    "growth singleton invariance")
        require(receipt["stages"][-1]["after"] == direct, "growth endpoint")
    require(states[5][1]["labels"]["l:2:0:3"] == 19 and states[5][1]["labels"]["l:2:0:4"] == 20,
            "named additions on r=3,t=5")
    return file_ref(path)


def adverse(data):
    _, record, ref = data
    path = DATA / "adverse.json"
    wrong = read(path)
    old = record["original"]["graph_digest"]
    modified = ("1" if old.startswith("0") else "0") + old[1:]
    require(wrong["parameters"] == {"r": 3, "t": 4, "K": 1} and wrong["certificate"] == ref
            and wrong["kind"] == "mismatched original-graph digest"
            and wrong["actual_graph_digest"] == old and wrong["supplied_graph_digest"] == modified
            and wrong["verification"] == {**record["verification"], "valid": False,
                                          "errors": ["original graph digest mismatch"]}
            and wrong["additional_graph_records"] == 0, "single adverse original-digest receipt")
    return file_ref(path)


def main():
    config = read(HERE / "config.json")
    run = "B4-1RT2-K1-DIRECT-SINGLETON-001-20261121"
    require(config == {"run_id": run, "parent": PARENT, "worker_count": 1, "max_vertices": 24, "max_result_bytes": 2_000_000,
                       "solver_queries": 0, "labeling_enumeration": 0, "historical_replays": 0, "K": 1, "retained_bundle": OLD,
                       "retained_cores": [list(row) for row in CORES], "retained_control": list(CONTROL),
                       "targets": [list(row) for row in TARGETS], "growth_routes": [list(row) for row in ROUTES],
                       "invalid": [list(row) for row in BAD],
                       "adverse": {"r": 3, "t": 4, "K": 1, "kind": "mismatched original-graph digest"}}
            and [typed(pair) for pair in config["invalid"]] == [typed(pair) for pair in BAD], "exact recorded configuration")
    probes = DATA / "domain_rejections.json"
    rows = read(probes)
    require(len(rows) == 8, "domain probe count")
    for i, (row, pair_values) in enumerate(zip(rows, BAD)):
        field, minimum = ("r", 3) if i < 4 else ("t", 4)
        require(typed(row["arguments"]) == typed(pair_values)
                and row["types"] == [type(v).__name__ for v in pair_values]
                and row["graph_builder_calls"] == 0 and row["error"] == f"{field} must be an exact integer >= {minimum}",
                "pre-expansion domain rejection")
    ident_file = DATA / "identity.json"
    identity = read(ident_file)
    runtime = identity["runtime"]
    require(identity["run_id"] == run and identity["parent"] == PARENT
            and runtime["implementation"] == "cpython" and runtime["utf8_mode"] == 1
            and runtime["python"].startswith(("3.12.", "3.13.")) and runtime["optional_dependencies"] == []
            and runtime["python_executable"] == ".venv/Scripts/python.exe" and bool(runtime["platform"]), "runtime or parent identity")
    for filename, key in (("config.json", "config_sha256_raw"), ("validate.py", "runner_sha256_raw"),
                          ("audit.py", "audit_sha256_raw")):
        require(sha(HERE / filename) == identity[key], "source or configuration hash")
    require(identity["proof"] == {"path": PROOF, "sha256_raw": sha(ROOT / PROOF)}, "proof bytes")
    names = ("core-r3.json", "core-r4.json", "core-r5.json", "target-r3.json")
    historical_paths = [f"{OLD}{where}/{name}" for name in names for where in ("", "/originals")]
    require(identity["retained_sha256_raw"] == {rel: sha(ROOT / rel) for rel in historical_paths}, "retained inputs raw hashes")
    require(set(identity["source_sha256_raw"]) == SOURCE_SET, "source snapshot inventory")
    for rel, digest in identity["source_sha256_raw"].items():
        snap = DATA / "source" / rel
        require(sha(snap) == digest
                and snap.read_bytes().replace(b"\r\n", b"\n") == (ROOT / rel).read_bytes().replace(b"\r\n", b"\n"),
                "source snapshot custody")
    cores = {r: core(r, n) for r, n in CORES}
    control = target(*CONTROL, cores[3], retained=True)
    targets = {(r, t): target(r, t, K, n, cores[r]) for r, t, K, n in TARGETS}
    routed = growth({3: control, 4: targets[(3, 4)], 5: targets[(3, 5)]})
    negative = adverse(targets[(3, 4)])
    completed = []
    for data in targets.values():
        ref = data[2]
        completed.append({**ref, "n": len(data[0]["vertices"]), "bytes": (DATA / ref["path"]).stat().st_size})
    summary = read(DATA / "summary.json")
    require(summary == {"status": "PASS", "run_id": run, "identity": file_ref(ident_file),
                        "retained_cores": [data[2] for data in cores.values()], "retained_completed_control": control[2],
                        "new_completed_targets": completed, "graph_records": 8, "growth": routed,
                        "invalid_inputs": file_ref(probes), "adverse": negative, "domain_rejections": 8, "adverse_checks": 1,
                        "solver_queries": 0, "labeling_enumeration": 0, "historical_replays": 0}, "summary accounting")
    require(len(list((DATA / "originals").glob("*.json"))) == 4 and len(list(DATA.glob("target-*.json"))) == 4
            and len(list(DATA.glob("recheck-core-*.json"))) == 3 and len(list(DATA.glob("recheck-target-*.json"))) == 1
            and all(file.stat().st_size <= 2_000_000 for file in DATA.rglob("*") if file.is_file()), "actual records and byte cap")
    report = {"status": "PASS", "run_id": run, "same_graph_records": 8, "same_retained_cores": summary["retained_cores"],
              "same_retained_completed_control": control[2], "same_new_completed_targets": completed,
              "same_domain_rejections": 8, "same_growth_routes": routed, "same_adverse_digest": negative,
              "additional_graph_records": 0, "solver_queries": 0}
    require(sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "audit runtime")
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= 2_000_000, "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as receipt:
        receipt.write(raw)
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
