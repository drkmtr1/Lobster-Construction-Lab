"""Reconstruct the named graph and audit the same 12 saved certificates."""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_graph, verify_partial

CASES = [[1, 1, 1], [1, 1, 4], [2, 1, 1], [2, 2, 3], [3, 1, 5], [5, 3, 2],
         [1, 2, 1], [1, 2, 3], [1, 4, 7], [2, 5, 1], [3, 5, 6], [8, 13, 9]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b3_unpadded_k1.py")
LIMITS = {"max_cases": 12, "max_vertices": 38, "max_output_bytes": 2_000_000, "workers": 1}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_case(q, r, t, case):
    require(case["parameters"] == {"q": q, "r": r, "t": t}, "case identity mismatch")
    m, p = q + r + t + 7, q + t + 4
    require(m + 1 <= LIMITS["max_vertices"], "vertex limit")
    spine = [f"s:{i}" for i in range(5)]
    groups = [[f"l:{i}:0:{j}" for j in range(n)] for i, n in enumerate((q, r, t))]
    edges = {tuple(sorted(edge)) for edge in zip(spine, spine[1:])}
    for i, leaves in enumerate(groups):
        center = f"b:{i}:0"
        edges.add(tuple(sorted((spine[i], center))))
        edges.update(tuple(sorted((center, leaf))) for leaf in leaves)

    # Derive the named values from the sorted alpha blocks.
    low = ["b:1:0", "s:0", *groups[0], "s:4", "s:2", *groups[2]]
    high = ["b:2:0", "s:3", "b:0:0", "s:1", *groups[1]]
    vertices = set(low) | set(high)
    require(len(low) == p and len(high) == r + 4 and len(vertices) == m + 1,
            "alpha class sizes do not match the original target")
    expected = {vertex: label for label, vertex in enumerate(low + high)}
    graph = case["original_graph"]
    require(graph["profile"] == [[q], [r], [t], [], []]
            and len(graph["vertices"]) == len(vertices) and set(graph["vertices"]) == vertices
            and len(graph["edges"]) == len(edges) == m
            and {tuple(sorted(e)) for e in graph["edges"]} == edges,
            "saved graph differs from independently reconstructed original names or incidences")
    digest = case["original_graph_digest"]
    graph_report = verify_graph(graph)
    require(graph_report["valid"] and graph_report["graph_digest"] == digest, "original graph digest mismatch")
    low_set = set(low)
    require(all(len(low_set.intersection(edge)) == 1 for edge in edges), "original edge does not cross the alpha cut")

    prefix, full = case["prefix_labels"], case["full_labels"]
    require(full == expected and all(type(x) is int for x in full.values()), "named full labeling mismatch")
    require(sorted(full[v] for v in low) == list(range(p))
            and sorted(full[v] for v in high) == list(range(p, m + 1)),
            "full alpha label intervals mismatch")
    require(set(prefix) == vertices - {"s:4"} and all(type(x) is int for x in prefix.values())
            and all(full[v] == x for v, x in prefix.items()), "prefix assignment or preservation mismatch")
    pending = {edge for edge in edges if "s:4" in edge}
    require(pending == {("s:3", "s:4")} and case["remaining_edges"] == [["s:3", "s:4"]],
            "sole unfinished incidence is not the original edge s:3--s:4")
    edge_differences = {edge: abs(full[edge[0]] - full[edge[1]]) for edge in edges}
    require(sorted(edge_differences.values()) == list(range(1, m + 1)), "full edge spectrum mismatch")
    unused_labels = sorted(set(range(m + 1)) - set(prefix.values()))
    assigned_differences = {diff for edge, diff in edge_differences.items() if edge not in pending}
    unused_differences = sorted(set(range(1, m + 1)) - assigned_differences)
    port_label = full["s:3"]
    require(unused_labels == [q + 2] and unused_differences == [t + 3]
            and port_label == q + t + 5 and [full["s:4"]] == unused_labels
            and [edge_differences[("s:3", "s:4")]] == unused_differences
            and case["tail_difference"] == t + 3, "singleton inventories or consumption mismatch")
    require(case["singleton_trace"] == {"active_vertex": "s:3", "active_label": port_label,
                                        "unused_labels": unused_labels, "unused_differences": unused_differences},
            "saved trace differs from the arithmetic boundary")
    partial = verify_partial(graph, prefix)
    require(partial["valid"] and partial["frontier"] == ["s:3"]
            and partial["unused_labels"] == unused_labels and partial["unused_differences"] == unused_differences
            and partial == case["partial_certificate"], "saved partial certificate mismatch")
    boundary = interval_boundary(graph, prefix, "s:3")
    require(not boundary["valid"] and boundary == case["adjacent_boundary"], "adjacent predicate mismatch")
    certificate = verify_certificate(graph, full, digest)
    require(certificate["valid"] and certificate == case["independent_certificate"],
            "saved original-target certificate mismatch")
    return {"parameters": case["parameters"], "original_graph_digest": digest, "vertices": len(vertices),
            "alpha_low_class_size": p, "unused_labels": unused_labels, "unused_differences": unused_differences,
            "port": "s:3", "port_label": port_label, "tail_difference": case["tail_difference"],
            "prefix_certificate_valid": True, "full_certificate_valid": True, "adjacent_predicate_rejected": True}


def main():
    here = Path(__file__).resolve().parent
    out = here / "independent_audit_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable")
    config_path = here / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r", "t"]
            and config["fixed_parameters"] == {"K": 1} and config["padding"] == [0, 0, 0]
            and all(config[k] == v for k, v in LIMITS.items())
            and config["starting_commit"] == "a1e8a15de2f33c5de877a941612c657a62d48747",
            "configuration differs from the authorized cases and limits")
    saved_path = here / "regression_result.json"
    require(saved_path.stat().st_size <= LIMITS["max_output_bytes"], "saved result exceeds limit")
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    require(saved["run_id"] == config["run_id"] and saved["starting_commit"] == config["starting_commit"]
            and saved["classification"] == "COMPLETE" and saved["status"] == "PASS"
            and saved["limits"] == LIMITS and saved["case_count"] == len(saved["cases"]) == len(CASES),
            "saved run, status, limits or case count mismatch")
    require(sha(config_path) == saved["config_sha256_raw"]
            and sha(here / "regression.py") == saved["regression_script_sha256_raw"]
            and sha(Path(__file__)) == saved["audit_script_sha256_raw"], "harness or configuration hash mismatch")
    sources = {p.relative_to(ROOT).as_posix() for p in (ROOT / "lcl").glob("*.py")} | set(EXTRA_SOURCE)
    require(set(saved["source_sha256_raw"]) == sources, "source inventory mismatch")
    for name, expected_hash in saved["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(here / "source" / name) == expected_hash,
                "source or snapshot hash mismatch: " + name)
    started = time.perf_counter()
    checked = [audit_case(q, r, t, case) for (q, r, t), case in zip(CASES, saved["cases"])]
    result = {"task": config["run_id"] + " saved-certificate audit", "status": "PASS",
              "scope": "same 12 saved completed targets only", "case_count": len(checked), "cases": checked,
              "config_sha256_raw": sha(config_path), "saved_regression_sha256_raw": sha(saved_path),
              "script_sha256_raw": sha(Path(__file__)),
              "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                              "platform": platform.platform(), "python_optimization_level": sys.flags.optimize},
              "elapsed_seconds": time.perf_counter() - started, "limits": LIMITS,
              "starting_commit": config["starting_commit"]}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= LIMITS["max_output_bytes"], "result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": result["case_count"], "output": str(out)}))


if __name__ == "__main__":
    main()
