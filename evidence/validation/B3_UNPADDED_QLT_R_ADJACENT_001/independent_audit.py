"""Audit saved adjacent B3 certificates and raw custody without constructing labels."""
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

CASES = [[1, 2, 1, 1], [1, 2, 2, 1], [1, 2, 1, 2], [1, 3, 2, 3],
         [2, 3, 1, 1], [2, 3, 3, 2], [2, 5, 2, 4], [3, 4, 4, 1],
         [3, 7, 2, 5], [5, 6, 6, 6], [5, 9, 3, 7], [8, 13, 9, 11]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b3_unpadded_qlt_r_adjacent.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    out = here / "independent_audit_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable; choose a new run directory")
    config = json.loads((here / "config.json").read_text(encoding="utf-8-sig"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r", "t", "K"]
            and config["padding"] == [0, 0, 0] and config["max_cases"] == 12
            and config["starting_commit"] == "aac7f84dc8d2c3518248e8aeae109ec23decbbae"
            and config["max_vertices"] == 48 and config["max_output_bytes"] == 2000000
            and config["workers"] == 1, "configuration differs from declared task")
    saved_path = here / "regression_result.json"
    require(saved_path.stat().st_size <= config["max_output_bytes"], "saved result exceeds limit")
    saved = json.loads(saved_path.read_text(encoding="utf-8-sig"))
    require(saved["run_id"] == config["run_id"] and saved["classification"] == "COMPLETE"
            and saved["status"] == "PASS" and saved["case_count"] == len(saved["cases"]) == 12,
            "saved status or case count mismatch")
    require(sha(here / "config.json") == saved["config_sha256_raw"], "config hash mismatch")
    require(sha(here / "regression.py") == saved["regression_script_sha256_raw"], "regression hash mismatch")
    require(sha(Path(__file__)) == saved["audit_script_sha256_raw"], "audit script hash mismatch")
    names = {p.relative_to(ROOT).as_posix() for p in (ROOT / "lcl").glob("*.py")} | set(EXTRA_SOURCE)
    require(set(saved["source_sha256_raw"]) == names, "source inventory mismatch")
    for name, expected_hash in saved["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(here / "source" / name) == expected_hash,
                "source or snapshot hash mismatch: " + name)
    started = time.perf_counter()
    checked = []
    for (q, r, t, K), case in zip(config["cases"], saved["cases"]):
        require(all(type(v) is int for v in (q, r, t, K)) and 1 <= q < r and 1 <= t <= q + 1 and K >= 1,
                "invalid declared parameters")
        require(case["parameters"] == {"q": q, "r": r, "t": t, "K": K}, "case identity mismatch")
        m, a = q + r + t + K + 6, q + t + 3
        require(m + 1 <= config["max_vertices"], "vertex limit")
        vertices = {f"s:{i}" for i in range(K + 4)} | {f"b:{i}:0" for i in range(3)}
        for i, count in enumerate((q, r, t)):
            vertices |= {f"l:{i}:0:{j}" for j in range(count)}
        edges = {tuple(sorted((f"s:{i}", f"s:{i+1}"))) for i in range(K + 3)}
        edges |= {tuple(sorted((f"s:{i}", f"b:{i}:0"))) for i in range(3)}
        for i, count in enumerate((q, r, t)):
            edges |= {tuple(sorted((f"b:{i}:0", f"l:{i}:0:{j}"))) for j in range(count)}
        graph = case["original_graph"]
        require(graph["profile"] == [[q], [r], [t]] + [[] for _ in range(K + 1)]
                and len(graph["vertices"]) == len(vertices) == m + 1 and set(graph["vertices"]) == vertices
                and len(graph["edges"]) == len(edges) == m
                and {tuple(sorted(e)) for e in graph["edges"]} == edges, "named original target mismatch")
        graph_report = verify_graph(graph)
        digest = case["original_graph_digest"]
        require(graph_report["valid"] and graph_report["graph_digest"] == digest, "graph digest mismatch")
        prefix, labels = case["prefix_labels"], case["full_labels"]
        suffix = {f"s:{i}" for i in range(4, K + 4)}
        require(set(prefix) == vertices - suffix and all(type(v) is int for v in prefix.values()),
                "prefix domain or integer type mismatch")
        named = {"s:0": t, "s:1": K + a + t + 2, "s:2": a - 1, "s:3": K + a,
                 "b:0:0": K + a + 2, "b:1:0": 0, "b:2:0": K + a + 1}
        first_lows = (value for value in range(1, q + 2) if value != t)
        middle_highs = (value for value in range(K + a + 3, m + 1) if value != K + a + t + 2)
        named.update({f"l:0:0:{j}": value for j, value in enumerate(first_lows)})
        named.update({f"l:1:0:{j}": value for j, value in enumerate(middle_highs)})
        named.update({f"l:2:0:{j}": q + 2 + j for j in range(t)})
        require(prefix == named, "named prefix formula mismatch")
        require(set(labels) == vertices and all(type(v) is int for v in labels.values())
                and sorted(labels.values()) == list(range(m+1)), "vertex bijection mismatch")
        require(all(labels[v] == value for v, value in prefix.items()), "prefix changed")
        remaining = {tuple(sorted((f"s:{i}", f"s:{i+1}"))) for i in range(3, K+3)}
        incident = {edge for edge in edges if suffix.intersection(edge)}
        require(remaining == incident, "unfinished physical path mismatch")
        crossing = {edge for edge in edges if (edge[0] in prefix) != (edge[1] in prefix)}
        require(crossing == {("s:3", "s:4")}, "physical frontier mismatch")
        prefix_diffs = [abs(prefix[u] - prefix[v]) for u, v in edges if u in prefix and v in prefix]
        require(len(prefix_diffs) == len(set(prefix_diffs))
                and set(prefix_diffs) == set(range(K+1, m+1))
                and set(range(m+1)) - set(prefix.values()) == set(range(a, a+K)),
                "arithmetic prefix inventories mismatch")
        partial = verify_partial(graph, prefix)
        require(partial["valid"] and partial["frontier"] == ["s:3"]
                and partial["unused_labels"] == list(range(a, a+K))
                and partial["unused_differences"] == list(range(1, K+1))
                and partial == case["partial_certificate"], "partial verifier mismatch")
        boundary = interval_boundary(graph, prefix, "s:3")
        require(boundary["valid"] and boundary["active_label"] == a + K
                and boundary["interval"] == [a, a + K - 1]
                and boundary == case["adjacent_boundary"], "saved adjacent boundary mismatch")
        tail = [labels[f"s:{i}"] for i in range(3, K + 4)]
        require(sorted(tail[1:]) == list(range(a, a + K)), "suffix label bijection mismatch")
        require(tail[1:] == [a + (i - 1) // 2 if i % 2 else a + K - i // 2
                             for i in range(1, K + 1)], "suffix assignment formula mismatch")
        tail_differences = [abs(u - v) for u, v in zip(tail, tail[1:])]
        require(tail_differences == list(range(K, 0, -1)) == case["tail_differences"],
                "descending path differences mismatch")
        differences = [abs(labels[u] - labels[v]) for u, v in edges]
        require(sorted(differences) == list(range(1, m+1)), "edge bijection mismatch")
        certificate = verify_certificate(graph, labels, digest)
        require(certificate["valid"] and certificate == case["independent_certificate"],
                "saved full certificate mismatch")
        checked.append({"q": q, "r": r, "t": t, "K": K, "graph_digest": digest,
                        "certificate_valid": True, "tail_differences": tail_differences,
                        "actual_edge_differences": sorted(differences)})
    result = {"task": "B3-UNPADDED-QLT-R-ADJACENT-001 saved-certificate audit", "status": "PASS",
              "scope": "12 saved named targets; no constructor, solver, search, or counting",
              "case_count": len(checked), "cases": checked,
              "config_sha256_raw": sha(here / "config.json"),
              "saved_regression_sha256_raw": sha(saved_path), "script_sha256_raw": sha(Path(__file__)),
              "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                              "platform": platform.platform(),
                              "python_optimization_level": sys.flags.optimize},
              "limits": {key: config[key] for key in ("max_cases", "max_vertices", "max_output_bytes", "workers")},
              "elapsed_seconds": time.perf_counter() - started}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= config["max_output_bytes"], "audit result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": len(checked), "output": str(out)}))


if __name__ == "__main__":
    main()
