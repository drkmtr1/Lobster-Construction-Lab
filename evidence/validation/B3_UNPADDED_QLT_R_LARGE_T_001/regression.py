"""Record the 12 declared large-t B3 original-target construction checks."""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial

CASES = [[1, 3, 3, 2], [1, 3, 3, 3], [1, 3, 3, 4], [1, 4, 3, 5],
         [1, 7, 8, 6], [2, 3, 4, 2], [2, 6, 7, 7], [3, 4, 5, 3],
         [3, 8, 9, 8], [4, 5, 6, 4], [5, 6, 7, 11], [8, 13, 12, 14]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b3_unpadded_qlt_r_large_t.py")
LIMITS = {"max_cases": 12, "max_vertices": 54, "max_output_bytes": 2_000_000, "workers": 1}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(edges, labels):
    return sorted(abs(labels[u] - labels[v]) for u, v in edges)


def main():
    here = Path(__file__).resolve().parent
    out = here / "regression_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable")
    config = json.loads((here / "config.json").read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r", "t", "K"]
            and config["padding"] == [0, 0, 0] and all(config[k] == v for k, v in LIMITS.items())
            and config["starting_commit"] == "db72b4dc45510c830c582bc994543d539c223a13",
            "configuration differs from the authorized cases and limits")
    started = time.perf_counter()
    results = []
    for q, r, t, K in config["cases"]:
        require(all(type(v) is int for v in (q, r, t, K))
                and 1 <= q < r and r >= 3 and t >= q + 2 and K >= 2, "invalid declared parameters")
        M, a = q + r + t + 6, q + t + 3
        m = M + K
        require(m + 1 <= LIMITS["max_vertices"], "vertex limit")
        profile = [[q], [r], [t]] + [[] for _ in range(K + 1)]
        original = build_graph(profile)
        spec = {"method": "three_section_qltr_large_t", "parameters": {"q": q, "r": r, "t": t, "K": K},
                "profile": profile}
        declared, constructed = construction_input(spec, max_vertices=LIMITS["max_vertices"])
        digest = graph_digest(original)
        require(declared == original and constructed["graph_digest"] == digest,
                "original graph identity mismatch")
        trace = constructed["trace"][0]
        seed, prefix, full = trace["seed_labels"], trace["prefix_labels"], constructed["labels"]
        prefix_graph = build_graph([[q], [r], [t], []])
        suffix = {f"s:{i}" for i in range(4, K + 4)}
        prefix_vertices = set(original["vertices"]) - suffix
        original_edges = {frozenset(e) for e in original["edges"]}
        prefix_edges = {e for e in original_edges if e <= prefix_vertices}
        tail = [f"s:{i}" for i in range(3, K + 4)]
        tail_edges = {frozenset(e) for e in zip(tail, tail[1:])}
        require(len(original["vertices"]) == m + 1 and len(original_edges) == m
                and original_edges - prefix_edges == tail_edges
                and set(prefix_graph["vertices"]) == prefix_vertices
                and {frozenset(e) for e in prefix_graph["edges"]} == prefix_edges,
                "original prefix and path incidence mismatch")
        seed_report = verify_certificate(prefix_graph, seed, graph_digest(prefix_graph))
        require(seed_report["valid"] and differences(prefix_edges, seed) == list(range(1, M + 1)),
                "seed certificate or edge spectrum mismatch")
        low = {"s:0", "s:2", "b:1:0"}
        low.update(f"l:0:0:{j}" for j in range(q))
        low.update(f"l:2:0:{j}" for j in range(t))
        require(sorted(seed[v] for v in low) == list(range(a))
                and sorted(seed[v] for v in prefix_vertices - low) == list(range(a, M + 1))
                and all(len(e & low) == 1 for e in prefix_edges), "seed alpha cut mismatch")
        require(set(prefix) == prefix_vertices
                and all(prefix[v] == seed[v] + (0 if v in low else K) for v in prefix_vertices)
                and differences(prefix_edges, prefix) == list(range(K + 1, m + 1)),
                "high-side shift mismatch")
        partial = verify_partial(original, prefix)
        require(partial["valid"] and partial["frontier"] == ["s:3"] and prefix["s:3"] == a + K + 1
                and partial["unused_labels"] == list(range(a, a + K))
                and partial["unused_differences"] == list(range(1, K + 1)), "prefix contract mismatch")
        boundary = interval_boundary(original, prefix, "s:3")
        require(not boundary["valid"], "adjacent predicate accepted nonadjacent port")
        require(all(full[v] == x for v, x in prefix.items()), "completed labeling changed the prefix")
        require(sorted(full[v] for v in suffix) == list(range(a, a + K))
                and differences(tail_edges, full) == list(range(1, K + 1)), "suffix inventories mismatch")
        certificate = verify_certificate(original, full, digest)
        require(certificate["valid"], "unchanged original-target checker rejected the construction")
        results.append({"parameters": spec["parameters"], "original_graph": original,
                        "original_graph_digest": digest, "seed_graph": prefix_graph, "seed_labels": seed,
                        "seed_certificate": seed_report, "prefix_labels": prefix,
                        "partial_certificate": partial, "adjacent_boundary": boundary, "full_labels": full,
                        "tail_differences": [abs(full[u] - full[v]) for u, v in zip(tail, tail[1:])],
                        "independent_certificate": certificate})
    source = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / "lcl").glob("*.py"))}
    source.update({name: sha(ROOT / name) for name in EXTRA_SOURCE})
    result = {"run_id": config["run_id"], "starting_commit": config["starting_commit"],
              "classification": "COMPLETE", "status": "PASS", "case_count": len(results),
              "config_sha256_raw": sha(here / "config.json"),
              "regression_script_sha256_raw": sha(Path(__file__)),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"),
              "source_sha256_raw": source,
              "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                              "platform": platform.platform(),
                              "python_optimization_level": sys.flags.optimize},
              "elapsed_seconds": time.perf_counter() - started,
              "limits": LIMITS,
              "scope": config["scope"], "cases": results}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= LIMITS["max_output_bytes"], "result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": result["case_count"], "output": str(out)}))


if __name__ == "__main__":
    main()
