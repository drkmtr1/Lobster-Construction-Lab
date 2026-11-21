"""Check one fixed base prefix and the 12 declared completed original targets."""
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

CASES = [[3, 2], [3, 3], [3, 4], [3, 5], [4, 2], [4, 6],
         [5, 3], [5, 7], [8, 4], [8, 8], [13, 11], [21, 14]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b3_unpadded_q1_r2.py")
LIMITS = {"max_cases": 12, "max_vertices": 45, "max_output_bytes": 2_000_000, "workers": 1}
BASE_LABELS = {"s:0": 0, "s:1": 10, "s:2": 4, "s:3": 6,
               "b:0:0": 9, "b:1:0": 3, "b:2:0": 5,
               "l:0:0:0": 1, "l:1:0:0": 7, "l:1:0:1": 8, "l:2:0:0": 2}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(edges, labels):
    return sorted(abs(labels[u] - labels[v]) for u, v in edges)


def write_result(path, result):
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= LIMITS["max_output_bytes"], "result exceeds output limit")
    with path.open("xb") as stream:
        stream.write(encoded)


def check_base(profile, identity):
    started = time.perf_counter()
    graph = build_graph(profile)
    digest = graph_digest(graph)
    certificate = verify_certificate(graph, BASE_LABELS, digest)
    low = {"s:0", "s:2", "b:1:0", "l:0:0:0", "l:2:0:0"}
    high = set(graph["vertices"]) - low
    require(certificate["valid"] and certificate["n"] == 11 and certificate["m"] == 10,
            "base-prefix certificate rejected")
    require(sorted(BASE_LABELS[v] for v in low) == list(range(5))
            and sorted(BASE_LABELS[v] for v in high) == list(range(5, 11))
            and all(len(low.intersection(e)) == 1 for e in graph["edges"])
            and BASE_LABELS["b:2:0"] == min(BASE_LABELS[v] for v in high)
            and BASE_LABELS["s:3"] == BASE_LABELS["b:2:0"] + 1,
            "base-prefix alpha classes or physical offsets mismatch")
    return {**identity, "classification": "VERIFIED_BASE_PREFIX", "status": "PASS",
            "base_prefix_certificate_count": 1, "completed_target_count": 0,
            "parameters": {"q": 1, "r": 2, "t": 1}, "seed_graph": graph,
            "seed_graph_digest": digest, "seed_labels": BASE_LABELS, "seed_certificate": certificate,
            "elapsed_seconds": time.perf_counter() - started}


def check_completed(t, K):
    require(type(t) is int and type(K) is int and t >= 3 and K >= 2, "invalid declared parameters")
    a, M, m = t + 4, t + 9, t + K + 9
    require(m + 1 <= LIMITS["max_vertices"], "vertex limit")
    profile = [[1], [2], [t]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    spec = {"method": "three_section_q1_r2", "parameters": {"t": t, "K": K}, "profile": profile}
    declared, constructed = construction_input(spec, max_vertices=LIMITS["max_vertices"])
    digest = graph_digest(original)
    require(declared == original and constructed["graph_digest"] == digest,
            "original graph identity mismatch")
    trace = constructed["trace"][0]
    seed, prefix, full = trace["seed_labels"], trace["prefix_labels"], constructed["labels"]
    prefix_graph = build_graph([[1], [2], [t], []])
    tail = [f"s:{i}" for i in range(3, K + 4)]
    suffix = set(tail[1:])
    prefix_vertices = set(original["vertices"]) - suffix
    original_edges = {frozenset(e) for e in original["edges"]}
    prefix_edges = {e for e in original_edges if e <= prefix_vertices}
    tail_edges = {frozenset(e) for e in zip(tail, tail[1:])}
    require(len(original["vertices"]) == m + 1 and len(original["edges"]) == len(original_edges) == m
            and original_edges - prefix_edges == tail_edges
            and set(prefix_graph["vertices"]) == prefix_vertices
            and {frozenset(e) for e in prefix_graph["edges"]} == prefix_edges,
            "original prefix and path incidence mismatch")
    seed_report = verify_certificate(prefix_graph, seed, graph_digest(prefix_graph))
    require(seed_report["valid"] and differences(prefix_edges, seed) == list(range(1, M + 1)),
            "seed certificate or edge spectrum mismatch")
    low = {"s:0", "s:2", "b:1:0", "l:0:0:0"} | {f"l:2:0:{j}" for j in range(t)}
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
    return {"parameters": spec["parameters"], "original_graph": original, "original_graph_digest": digest,
            "seed_graph": prefix_graph, "seed_labels": seed, "seed_certificate": seed_report,
            "prefix_labels": prefix, "partial_certificate": partial, "adjacent_boundary": boundary,
            "full_labels": full, "tail_differences": [abs(full[u] - full[v]) for u, v in zip(tail, tail[1:])],
            "independent_certificate": certificate}


def main():
    here = Path(__file__).resolve().parent
    base_out = here / "base_prefix_result.json"
    out = here / "regression_result.json"
    if base_out.exists() or out.exists():
        raise FileExistsError("Existing evidence is immutable")
    config_path = here / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["t", "K"]
            and config["fixed_parameters"] == {"q": 1, "r": 2} and config["padding"] == [0, 0, 0]
            and config["base_prefix_profile"] == [[1], [2], [1], []]
            and all(config[k] == v for k, v in LIMITS.items())
            and config["starting_commit"] == "e74285d893408b5474319bcfcbe6aad2fd1297a3",
            "configuration differs from the authorized cases and limits")
    source = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / "lcl").glob("*.py"))}
    source.update({name: sha(ROOT / name) for name in EXTRA_SOURCE})
    identity = {"run_id": config["run_id"], "starting_commit": config["starting_commit"],
                "config_sha256_raw": sha(config_path), "regression_script_sha256_raw": sha(Path(__file__)),
                "source_sha256_raw": source,
                "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                                "platform": platform.platform(), "python_optimization_level": sys.flags.optimize},
                "limits": LIMITS}
    base = check_base(config["base_prefix_profile"], identity)
    write_result(base_out, base)
    started = time.perf_counter()
    results = [check_completed(t, K) for t, K in config["cases"]]
    result = {**identity, "classification": "COMPLETE", "status": "PASS", "case_count": len(results),
              "base_prefix_result": base_out.name, "base_prefix_sha256_raw": sha(base_out),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"),
              "elapsed_seconds": time.perf_counter() - started,
              "scope": "12 declared completed targets, with the fixed base prefix recorded separately",
              "cases": results}
    write_result(out, result)
    print(json.dumps({"status": "PASS", "cases": result["case_count"],
                      "base_prefix_certificates": base["base_prefix_certificate_count"],
                      "base_prefix_output": str(base_out), "output": str(out)}))


if __name__ == "__main__":
    main()
