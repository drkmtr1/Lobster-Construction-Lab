"""Reconstruct and verify the exact named originals and receipts with stdlib."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
CORE = [[2], [2], [], [2], [], []]
LIFT = [[2], [2], [2], [2], [], []]


def check(condition, detail):
    if not condition:
        raise ValueError(detail)


def load(path):
    return json.loads(path.read_bytes())


def hash_file(path):
    return sha256(path.read_bytes()).hexdigest()


def original(record, profile, order):
    graph = record["graph"]
    spine = [f"s:{i}" for i in range(6)]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = list(zip(spine, spine[1:]))
    for i, section in enumerate(profile):
        if not section:
            continue
        center = f"b:{i}:0"
        edges.append((spine[i], center))
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(section[0]):
            leaf = f"l:{i}:0:{j}"
            edges.append((center, leaf))
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    canonical = [tuple(sorted(e)) for e in edges]
    check(Counter(graph["vertices"]) == Counter(roles.keys())
          and Counter(tuple(sorted(e)) for e in graph["edges"]) == Counter(canonical), "named edge and vertex multiplicities")
    check(graph["profile"] == profile and graph["spine"] == spine and graph["roles"] == roles
          and graph["schema_version"] == 1 and len(roles) == order and len(edges) == order - 1, "physical roles and order")
    body = {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles), "edges": sorted(canonical)}
    canonical_bytes = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    check(sha256(canonical_bytes).hexdigest() == record["graph_digest"], "original digest")
    return [tuple(e) for e in graph["edges"]]


def edges_and_weights(edges, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]


def inventory(rows, labels, m):
    weights = Counter(row["difference"] for row in rows)
    return {"used_labels": sorted(labels.values()), "unused_labels": sorted(set(range(m + 1)).difference(labels.values())),
            "used_differences": sorted(weights.elements()), "unused_differences": sorted(set(range(1, m + 1)).difference(weights)),
            "repeated_differences": {str(w): count for w, count in weights.items() if count > 1}}


def checker(graph, labels, edges, record, errors):
    rows = edges_and_weights(edges, labels)
    outputs = record["checker"]
    m = len(edges)
    check(set(labels) == set(graph["graph"]["vertices"]) and all(type(x) is int for x in labels.values())
          and sorted(labels.values()) == list(range(m + 1)) and record["ledger"] == rows, "named certificate ledger")
    check(outputs["valid"] is (not errors) and outputs["errors"] == errors
          and outputs["graph_digest"] == graph["graph_digest"] and outputs["n"] == m + 1 and outputs["m"] == m
          and outputs["edge_differences"] == [row["difference"] for row in rows], "unchanged checker receipt")
    return rows


def source_check(config, identity):
    expected_sources = {"lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt"}
    retained_paths = {config["pilot_original"], config["historical_incomplete"],
                      *(s[k] for s in config["controls"] for k in ("original", "certificate"))}
    inputs = {p.relative_to(ROOT).as_posix() for p in
              (HERE / "validate.py", HERE / "audit.py", HERE / "commands.json", HERE / "config.json")}
    inputs.add("research/B4_JOINT_22_DIRECT_LEDGER.md")
    check(identity["parent"] == config["parent"] == "e3138ed2804883396fb548f824316155fc859974" and identity["id"] == config["id"]
          and set(identity["source_sha256"]) == expected_sources
          and set(identity["retained_sha256"]) == retained_paths and set(identity["inputs_sha256"]) == inputs,
          "source scope")
    check(identity["inputs_sha256"] == {p: hash_file(ROOT / p) for p in inputs}
          and identity["runtime"] == {"python": sys.version, "implementation": sys.implementation.name,
                     "platform": platform.platform(), "utf8_mode": 1, "optional_dependencies": []}
          and sys.flags.utf8_mode == 1, "runtime and input hashes")
    for path, digest in identity["retained_sha256"].items():
        raw = (ROOT / path).read_bytes()
        base = subprocess.check_output(["git", "show", f'{config["parent"]}:{path}'], cwd=ROOT)
        check(raw == base and hash_file(ROOT / path) == digest, path)
    for path, digest in identity["source_sha256"].items():
        snapshot = DATA / "source" / path
        base = subprocess.check_output(["git", "show", f'{config["parent"]}:{path}'], cwd=ROOT)
        check(hash_file(snapshot) == hash_file(ROOT / path) == digest
              and snapshot.read_bytes().replace(b"\r\n", b"\n") == base.replace(b"\r\n", b"\n"), path)


def check_controls(config):
    controls = load(DATA / "controls.json")
    check([item["id"] for item in controls] == ["q2", "r2"], "two retained records")
    for spec, receipt, profile in zip(config["controls"], controls,
            ([[2],[1],[],[2],[],[]], [[1],[2],[],[2],[],[]]), strict=True):
        saved = load(ROOT / spec["certificate"])
        record = load(ROOT / spec["original"])
        edges = original(record, profile, 14)
        g = saved["labels"]
        rows = checker(record, g, edges, receipt, [])
        check(rows == saved["edge_ledger"] and g == receipt["labels"] and g["s:2"] == 13
              and sorted(row["difference"] for row in rows) == list(range(1, 14))
              and receipt["id"] == spec["id"] and receipt["checker"] == saved["verification"]
              and receipt["graph_digest"] == saved["original"]["graph_digest"] == record["graph_digest"]
              and saved["original"]["sha256_raw"] == hash_file(ROOT / spec["original"]), "retained named core and root")


def main():
    started = process_time()
    config = load(HERE / "config.json")
    limits = config["limits"]
    check(limits == {"workers": 1, "solver_queries": 0, "labeling_enumeration_nodes": 0,
          "candidates_max": 4, "per_case_max": 2, "max_order": 18, "max_bytes": 2_000_000,
          "cpu_seconds": 30, "max_graph_records": 4, "automatic_retries": 0} and config["lift_t"] == 2,
          "frozen validation limits")
    source_check(config, load(DATA / "identity.json"))
    check_controls(config)
    historical = load(ROOT / config["historical_incomplete"])
    check(historical["status"] == "INCOMPLETE" and historical["nodes"] == 100000 and historical["reason"] == "max_nodes"
          and historical["exhausted"] is False and historical["witness"] is None, "historical pilot status")

    record = load(DATA / "core_original.json")
    core_edges = original(record, CORE, 15)
    check(record == load(ROOT / config["pilot_original"])
          and {v if u == "s:2" else u for u, v in core_edges if "s:2" in (u, v)} == {"s:1", "s:3"},
          "physical maximum neighbors")
    check(len(config["candidates"]) == 2, "one candidate per case")
    for spec, case, zero in zip(config["candidates"], ("A","B"), ("s:1","s:3"), strict=True):
        saved = load(DATA / f"candidate_{case}.json")
        labels = spec["labels"]
        errors = ["edge differences repeat", "edge differences are not exactly 1..m"] if case == "A" else []
        rows = checker(record, labels, core_edges, saved, errors)
        weights = [row["difference"] for row in rows]
        expected = ([7,14,13,12,11,3,1,5,10,4,2,2,9,8] if case == "A"
                    else [12,13,14,7,2,11,10,9,8,5,1,6,3,4])
        check(weights == expected and saved["inventories"] == inventory(rows, labels, 14)
              and saved["graph_digest"] == record["graph_digest"] and saved["physical_s2"] == labels["s:2"] == 14
              and labels[zero] == 0 and saved["labels"] == labels
              and saved["choices"] == spec["choices"] and saved["case"] == spec["case"] == case
              and saved["zero"] == spec["zero"] == zero, "complete scoped candidate record")
        if case == "A":
            repeated = next(rows[i] for i, w in enumerate(weights) if w in weights[:i])
            check(repeated == saved["first_repeated_edge"] and saved["inventories"]["unused_differences"] == [6]
                  and saved["inventories"]["repeated_differences"] == {"2": 2}, "precise failed candidate")
        else:
            check(sorted(weights) == list(range(1, 15)) and saved["first_repeated_edge"] is None, "graceful seed")
            core = labels
            core_certificate = saved["checker"]
    adverse = load(DATA / "adverse.json")
    check(adverse["expected_digest"] == "0" * 64 != record["graph_digest"] == adverse["actual_digest"]
          and adverse["checker"] == {**core_certificate, "valid": False, "errors": ["original graph digest mismatch"]},
          "one digest adverse check")

    target = load(DATA / "lift_original.json")
    target_edges = original(target, LIFT, 18)
    saved = load(DATA / "lift.json")
    completed = saved["labels"]
    rows = checker(target, completed, target_edges, saved, [])
    check({v: completed[v] - 1 for v in core} == core
          and {v: completed[v] for v in completed.keys() - core.keys()} ==
              {"b:2:0": 0, "l:2:0:0": 16, "l:2:0:1": 17}
          and sorted(row["difference"] for row in rows) == list(range(1, 18))
          and saved["t"] == 2 and saved["graph_digest"] == target["graph_digest"], "lift arithmetic")
    prefix = saved["prefix"]
    missing = completed.keys() - prefix.keys()
    pending = [list(e) for e in target_edges if any(v in missing for v in e)]
    assigned_rows = [row for row in rows if all(v in prefix for v in row["edge"])]
    counts = inventory(assigned_rows, prefix, 17)
    check(missing == {"s:5"} and all(completed[v] == x for v, x in prefix.items())
          and pending == saved["pending_edges"] == [["s:4", "s:5"]]
          and saved["port"] == {"vertex": "s:4", "label": 8} and prefix["s:4"] == 8
          and counts == saved["prefix_inventories"] and counts["unused_labels"] == [6]
          and counts["unused_differences"] == [2] and completed["s:5"] == 6, "both supplies and final edge")
    bad = [{"input": v, "type": type(v).__name__, "rejected": True} for v in (True, 0, 2.0, "2")]
    check(json.dumps(saved["invalid_t_inputs"], sort_keys=True) == json.dumps(bad, sort_keys=True), "four input guards")
    summary = load(DATA / "summary.json")
    elapsed = summary["validation_cpu_seconds"]
    check(summary == {"status": "PASS", "validation_cpu_seconds": elapsed, "graph_records": 4,
         "retained_controls": 2, "candidates": 2, "accepted_candidates": 1, "failed_candidates": 1,
         "solver_queries": 0, "labeling_enumeration_nodes": 0, "completed_t2": 1}, "exact scope receipt")
    outputs = {p.relative_to(DATA).as_posix(): hash_file(p) for p in sorted(DATA.rglob("*")) if p.is_file()}
    check(all((DATA / name).stat().st_size <= limits["max_bytes"] for name in outputs), "per-result byte cap")
    cpu = process_time() - started
    check(0 <= elapsed and elapsed + cpu <= limits["cpu_seconds"], "shared validation CPU cap")
    report = {"status": "PASS", "graphs": 4, "candidates": 2, "adverse_checks": 1, "invalid_t_checks": 4,
              "solver_queries": 0, "labeling_enumeration_nodes": 0, "shared_cpu_seconds": elapsed + cpu,
              "audited_sha256": outputs}
    data = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    check(len(data) <= limits["max_bytes"], "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as handle:
        handle.write(data)
    print(f"PASS: four named graphs, both candidate ledgers, adverse digest and physical lift ({elapsed + cpu:.6f} CPU seconds)")


if __name__ == "__main__":
    main()
