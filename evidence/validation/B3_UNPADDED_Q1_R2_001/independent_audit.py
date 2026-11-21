"""Audit the same 12 completed-target certificates without invoking the constructor."""
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

CASES = [[3, 2], [3, 3], [3, 4], [3, 5], [4, 2], [4, 6],
         [5, 3], [5, 7], [8, 4], [8, 8], [13, 11], [21, 14]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b3_unpadded_q1_r2.py")
LIMITS = {"max_cases": 12, "max_vertices": 45, "max_output_bytes": 2_000_000, "workers": 1}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(edges, labels):
    return sorted(abs(labels[u] - labels[v]) for u, v in edges)


def named_seed(t):
    # Reconstruct the fixed low assignments and the consecutive named high block.
    low = {"s:0": 0, "l:0:0:0": 1, "l:2:0:0": 2, "b:1:0": 3, "s:2": 4}
    low.update({f"l:2:0:{j}": x for j, x in enumerate(range(5, t + 4), start=1)})
    high_order = ("b:2:0", "s:3", "l:1:0:0", "l:1:0:1", "b:0:0", "s:1")
    high = dict(zip(high_order, range(t + 4, t + 10)))
    return low | high, set(low)


def normalized_path(K):
    bases = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3)}
    if K in bases:
        return bases[K]
    reflected = tuple(K - 2 - x for x in normalized_path(K - 3))
    return (K + 1, 1, K - 1, *reflected)


def audit_case(t, K, case):
    require(case["parameters"] == {"t": t, "K": K}, "case identity mismatch")
    a, M, m = t + 4, t + 9, t + K + 9
    require(m + 1 <= LIMITS["max_vertices"], "vertex limit")
    spine = [f"s:{i}" for i in range(K + 4)]
    vertices = set(spine)
    edges = {tuple(sorted(e)) for e in zip(spine, spine[1:])}
    for i, count in enumerate((1, 2, t)):
        center = f"b:{i}:0"
        leaves = {f"l:{i}:0:{j}" for j in range(count)}
        vertices |= {center} | leaves
        edges.add(tuple(sorted((spine[i], center))))
        edges.update(tuple(sorted((center, leaf))) for leaf in leaves)
    original = case["original_graph"]
    require(original["profile"] == [[1], [2], [t]] + [[] for _ in range(K + 1)]
            and len(original["vertices"]) == len(vertices) == m + 1
            and len(original["edges"]) == len(edges) == m
            and set(original["vertices"]) == vertices
            and {tuple(sorted(e)) for e in original["edges"]} == edges,
            "saved graph differs from independently reconstructed original vertices or edges")
    digest = case["original_graph_digest"]
    report = verify_graph(original)
    require(report["valid"] and report["graph_digest"] == digest, "original graph check or digest mismatch")
    tail = spine[3:]
    prefix_vertices = vertices - set(tail[1:])
    prefix_edges = {e for e in edges if set(e) <= prefix_vertices}
    tail_edges = {tuple(sorted(e)) for e in zip(tail, tail[1:])}
    require(edges - prefix_edges == tail_edges, "unfinished incidences do not form the original s:3 path")
    seed_graph, seed = case["seed_graph"], case["seed_labels"]
    require(seed_graph["profile"] == [[1], [2], [t], []]
            and len(seed_graph["vertices"]) == len(prefix_vertices) == M + 1
            and len(seed_graph["edges"]) == len(prefix_edges) == M
            and set(seed_graph["vertices"]) == prefix_vertices
            and {tuple(sorted(e)) for e in seed_graph["edges"]} == prefix_edges,
            "saved seed graph differs from the induced original prefix")
    expected, low = named_seed(t)
    require(set(seed) == prefix_vertices and all(type(x) is int for x in seed.values())
            and seed == expected
            and sorted(seed[v] for v in low) == list(range(a))
            and sorted(seed[v] for v in prefix_vertices - low) == list(range(a, M + 1))
            and all(len(low.intersection(e)) == 1 for e in prefix_edges),
            "named seed assignments or alpha partition mismatch")
    require(differences(prefix_edges, seed) == list(range(1, M + 1)), "seed edge spectrum mismatch")
    seed_report = verify_certificate(seed_graph, seed, case["seed_certificate"]["graph_digest"])
    require(seed_report["valid"] and seed_report == case["seed_certificate"], "saved seed certificate mismatch")
    prefix, full = case["prefix_labels"], case["full_labels"]
    require(set(prefix) == prefix_vertices and all(type(x) is int for x in prefix.values())
            and all(prefix[v] == seed[v] + (0 if v in low else K) for v in prefix_vertices)
            and sorted(prefix.values()) == [*range(a), *range(a + K, m + 1)]
            and differences(prefix_edges, prefix) == list(range(K + 1, m + 1))
            and prefix["s:3"] == a + K + 1, "shifted prefix inventories or port mismatch")
    partial = verify_partial(original, prefix)
    require(partial["valid"] and partial["frontier"] == ["s:3"]
            and partial["unused_labels"] == list(range(a, a + K))
            and partial["unused_differences"] == list(range(1, K + 1))
            and partial == case["partial_certificate"], "saved partial certificate mismatch")
    boundary = interval_boundary(original, prefix, "s:3")
    require(not boundary["valid"] and boundary == case["adjacent_boundary"], "adjacent predicate mismatch")
    require(set(full) == vertices and all(type(x) is int for x in full.values())
            and sorted(full.values()) == list(range(m + 1))
            and all(full[v] == prefix[v] for v in prefix_vertices), "full labels or prefix preservation mismatch")
    tail_differences = [abs(full[u] - full[v]) for u, v in zip(tail, tail[1:])]
    require(tuple(full[v] - a for v in tail) == normalized_path(K)
            and tail_differences == case["tail_differences"]
            and sorted(tail_differences) == list(range(1, K + 1))
            and differences(edges, full) == list(range(1, m + 1)), "suffix or full spectrum mismatch")
    certificate = verify_certificate(original, full, digest)
    require(certificate["valid"] and certificate == case["independent_certificate"],
            "saved original-target certificate mismatch")
    return {"parameters": case["parameters"], "original_graph_digest": digest,
            "vertices": len(vertices), "seed_certificate_valid": True,
            "prefix_certificate_valid": True, "full_certificate_valid": True,
            "adjacent_predicate_rejected": True, "tail_differences": tail_differences}


def main():
    here = Path(__file__).resolve().parent
    out = here / "independent_audit_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable")
    config = json.loads((here / "config.json").read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["t", "K"]
            and config["fixed_parameters"] == {"q": 1, "r": 2} and config["padding"] == [0, 0, 0]
            and all(config[k] == v for k, v in LIMITS.items())
            and config["starting_commit"] == "e74285d893408b5474319bcfcbe6aad2fd1297a3",
            "configuration differs from the authorized cases and limits")
    saved_path = here / "regression_result.json"
    require(saved_path.stat().st_size <= LIMITS["max_output_bytes"], "saved result exceeds limit")
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    require(saved["run_id"] == config["run_id"] and saved["starting_commit"] == config["starting_commit"]
            and saved["classification"] == "COMPLETE" and saved["status"] == "PASS"
            and saved["limits"] == LIMITS and saved["case_count"] == len(saved["cases"]) == len(CASES),
            "saved run, status, limits or case count mismatch")
    require(sha(here / "config.json") == saved["config_sha256_raw"]
            and sha(here / "regression.py") == saved["regression_script_sha256_raw"]
            and sha(Path(__file__)) == saved["audit_script_sha256_raw"], "harness or configuration hash mismatch")
    sources = {p.relative_to(ROOT).as_posix() for p in (ROOT / "lcl").glob("*.py")} | set(EXTRA_SOURCE)
    require(set(saved["source_sha256_raw"]) == sources, "source inventory mismatch")
    for name, expected_hash in saved["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(here / "source" / name) == expected_hash,
                "source or snapshot hash mismatch: " + name)
    started = time.perf_counter()
    checked = [audit_case(t, K, case) for (t, K), case in zip(CASES, saved["cases"])]
    result = {"task": config["run_id"] + " saved-certificate audit", "status": "PASS",
              "scope": "same 12 saved completed targets only",
              "case_count": len(checked), "cases": checked, "config_sha256_raw": sha(here / "config.json"),
              "saved_regression_sha256_raw": sha(saved_path), "script_sha256_raw": sha(Path(__file__)),
              "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                              "platform": platform.platform(),
                              "python_optimization_level": sys.flags.optimize},
              "elapsed_seconds": time.perf_counter() - started, "limits": LIMITS,
              "starting_commit": config["starting_commit"]}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= LIMITS["max_output_bytes"], "result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": result["case_count"], "output": str(out)}))


if __name__ == "__main__":
    main()
