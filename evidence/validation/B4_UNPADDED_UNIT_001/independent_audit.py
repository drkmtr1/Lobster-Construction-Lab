"""Reconstruct the named graph and audit the same 12 completed certificates."""
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

CASES = [1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 64]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b4_unpadded_unit.py")
LIMITS = {"max_cases": 12, "max_vertices": 77, "max_output_bytes": 2_000_000, "workers": 1}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_case(K, case):
    require(type(K) is int and 1 <= K and K + 13 <= LIMITS["max_vertices"]
            and case["parameters"] == {"K": K}, "case identity or vertex limit mismatch")
    m = K + 12
    spine = [f"s:{i}" for i in range(K + 5)]
    centers = [f"b:{i}:0" for i in range(4)]
    leaves = [f"l:{i}:0:0" for i in range(4)]
    vertices = set(spine + centers + leaves)
    edges = {frozenset(e) for e in zip(spine, spine[1:])}
    edges.update(frozenset(e) for e in zip(spine[:4], centers))
    edges.update(frozenset(e) for e in zip(centers, leaves))
    graph = case["original_graph"]
    require(graph["profile"] == [[1], [1], [1], [1]] + [[] for _ in range(K + 1)]
            and len(graph["vertices"]) == len(vertices) == m + 1 and set(graph["vertices"]) == vertices
            and len(graph["edges"]) == len(edges) == m and {frozenset(e) for e in graph["edges"]} == edges,
            "saved graph differs from independently reconstructed names or incidences")
    digest = case["original_graph_digest"]
    graph_report = verify_graph(graph)
    require(graph_report["valid"] and graph_report["graph_digest"] == digest, "original graph digest mismatch")

    # Generate the two known prefix blocks in label order, then insert the
    # odd and even suffix vertices in their own label order.
    tail = spine[4:]
    low_order = ["b:0:0", "l:1:0:0", "s:1", "b:2:0", "l:3:0:0", "s:3", *tail[1::2]]
    high_order = [*reversed(tail[2::2]), "s:4", "b:3:0", "l:2:0:0",
                  "s:2", "b:1:0", "l:0:0:0", "s:0"]
    expected = {v: label for label, v in enumerate(low_order + high_order)}
    p = 6 + (K + 1) // 2
    low, high = set(low_order), set(high_order)
    require(len(low_order) == len(low) == p and len(high_order) == len(high) == m + 1 - p
            and low.isdisjoint(high) and low | high == vertices
            and all(len(low.intersection(e)) == 1 for e in edges), "alpha divide or class sizes mismatch")
    prefix, full = case["prefix_labels"], case["full_labels"]
    unassigned = set(tail[1:])
    prefix_vertices = vertices - unassigned
    require(full == expected and all(type(x) is int for x in full.values())
            and sorted(full[v] for v in low) == list(range(p))
            and sorted(full[v] for v in high) == list(range(p, m + 1))
            and case["alpha_low_class_size"] == p
            and case["alpha_low_vertices"] == sorted(low) and case["alpha_high_vertices"] == sorted(high),
            "named certificate or alpha evidence mismatch")
    require(set(prefix) == prefix_vertices and all(type(x) is int for x in prefix.values())
            and all(full[v] == x for v, x in prefix.items())
            and sorted(prefix.values()) == [*range(6), *range(K + 6, m + 1)], "original prefix mismatch")
    tail_edges = {frozenset(e) for e in zip(tail, tail[1:])}
    pending = {e for e in edges if unassigned.intersection(e)}
    crossing = {e for e in pending if len(e.intersection(unassigned)) == 1}
    require(pending == tail_edges and crossing == {frozenset(("s:4", "s:5"))}
            and case["crossing_edge"] == ["s:4", "s:5"], "unfinished original incidences differ")
    differences = {frozenset((u, v)): abs(full[u] - full[v]) for u, v in edges}
    used_differences = sorted(differences[e] for e in edges - pending)
    unused_labels = sorted(set(range(m + 1)) - set(prefix.values()))
    unused_differences = sorted(set(range(1, m + 1)) - set(used_differences))
    require(sorted(differences.values()) == list(range(1, m + 1))
            and used_differences == list(range(K + 1, m + 1)), "full or prefix edge spectrum mismatch")
    resources = {"active_vertex": "s:4", "active_label": K + 6, "unused_labels": unused_labels,
                 "unused_differences": unused_differences}
    require(unused_labels == list(range(6, K + 6)) and unused_differences == list(range(1, K + 1))
            and prefix["s:4"] == K + 6 and case["prefix_trace"] == resources, "adjacent resources mismatch")
    partial = verify_partial(graph, prefix)
    boundary = interval_boundary(graph, prefix, "s:4")
    require(partial["valid"] and partial["frontier"] == ["s:4"] and partial == case["partial_certificate"]
            and boundary["valid"] and boundary == case["adjacent_boundary"], "saved prefix checks mismatch")
    tail_differences = [differences[frozenset((u, v))] for u, v in zip(tail, tail[1:])]
    require(tail_differences == list(range(K, 0, -1)) and tail_differences == case["tail_differences"],
            "ordered suffix differences mismatch")
    completion = [{"operation": "next_spine", "parent": u, "vertex": v, "label": full[v],
                   "difference": difference} for u, v, difference in zip(tail, tail[1:], tail_differences)]
    require(case["completion_trace"] == completion, "suffix trace mismatch")
    certificate = verify_certificate(graph, full, digest)
    require(certificate["valid"] and certificate == case["independent_certificate"],
            "saved original-target certificate mismatch")
    return {"parameters": case["parameters"], "original_graph_digest": digest, "vertices": len(vertices),
            "alpha_low_class_size": p, "prefix_trace": resources, "tail_differences": tail_differences,
            "prefix_certificate_valid": True, "full_certificate_valid": True, "adjacent_boundary_valid": True}


def main():
    here = Path(__file__).resolve().parent
    out = here / "independent_audit_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable")
    config_path = here / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["K"]
            and config["fixed_branch_sizes"] == [1, 1, 1, 1] and config["padding"] == [0, 0, 0, 0]
            and config["seed_profile"] == [[1], [1], [1], [1], []]
            and all(config[key] == value for key, value in LIMITS.items())
            and config["starting_commit"] == "a5a58fe1ad2b58e93ea1a4dc9a74d956973adcad",
            "configuration differs from the declared cases and limits")
    saved_path = here / "regression_result.json"
    require(saved_path.stat().st_size <= LIMITS["max_output_bytes"], "saved result exceeds limit")
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    require(saved["run_id"] == config["run_id"] and saved["starting_commit"] == config["starting_commit"]
            and saved["classification"] == "COMPLETE" and saved["status"] == "PASS"
            and saved["limits"] == LIMITS and saved["case_count"] == len(saved["cases"]) == len(CASES),
            "saved run identity, status, limits or case count mismatch")
    require(sha(config_path) == saved["config_sha256_raw"]
            and sha(here / "regression.py") == saved["regression_script_sha256_raw"]
            and sha(Path(__file__)) == saved["audit_script_sha256_raw"]
            and saved["seed_result"] == "seed_result.json"
            and sha(here / "seed_result.json") == saved["seed_result_sha256_raw"],
            "harness, configuration or separate seed hash mismatch")
    sources = {p.relative_to(ROOT).as_posix() for p in (ROOT / "lcl").glob("*.py")} | set(EXTRA_SOURCE)
    require(set(saved["source_sha256_raw"]) == sources, "source inventory mismatch")
    for name, expected_hash in saved["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(here / "source" / name) == expected_hash,
                "source or snapshot hash mismatch: " + name)
    started = time.perf_counter()
    checked = [audit_case(K, case) for K, case in zip(CASES, saved["cases"])]
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
    print(json.dumps({"status": "PASS", "cases": len(checked), "output": str(out)}))


if __name__ == "__main__":
    main()
