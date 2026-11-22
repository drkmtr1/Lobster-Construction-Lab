"""Check the enlarged fixed alpha seed and 12 declared original completed targets."""
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

CASES = [1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 64]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b4_unpadded_2111.py")
LIMITS = {"max_cases": 12, "max_vertices": 78, "max_output_bytes": 2_000_000, "workers": 1}
SEED = {"s:0": 12, "s:1": 2, "s:2": 9, "s:3": 5, "s:4": 6,
        "b:0:0": 0, "l:0:0:0": 11, "l:0:0:1": 13, "b:1:0": 10, "l:1:0:0": 1,
        "b:2:0": 3, "l:2:0:0": 8, "b:3:0": 7, "l:3:0:0": 4}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_result(path, result):
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= LIMITS["max_output_bytes"], "result exceeds output limit")
    with path.open("xb") as stream:
        stream.write(encoded)


def check_seed(profile, identity):
    graph = build_graph(profile)
    digest = graph_digest(graph)
    certificate = verify_certificate(graph, SEED, digest)
    low = {v for v, x in SEED.items() if x < 6}
    require(certificate["valid"] and certificate["n"] == 14 and certificate["m"] == 13
            and len(low) == 6 and all(len(low.intersection(e)) == 1 for e in graph["edges"])
            and SEED["b:0:0"] == 0 and SEED["s:4"] == 6,
            "fixed seed certificate, alpha cut or original ports mismatch")
    new_leaf = "l:0:0:1"
    witness = ["b:0:0"] + [f"s:{i}" for i in range(5)]
    edges = {frozenset(edge) for edge in graph["edges"]}
    require(all(frozenset(edge) in edges for edge in zip(witness, witness[1:])), "seed witness path")
    require([edge for edge in graph["edges"] if new_leaf in edge] == [["b:0:0", new_leaf]]
            and SEED[new_leaf] == 13 and SEED["s:0"] == 12, "prescribed maximum-labeled leaf")
    old_edges = [edge for edge in graph["edges"] if new_leaf not in edge]
    require(sorted(SEED[v] for v in SEED if v != new_leaf) == list(range(13))
            and sorted(abs(SEED[u] - SEED[v]) for u, v in old_edges) == list(range(1, 13)),
            "unit skeleton inventories")
    return {**identity, "classification": "VERIFIED_FIXED_SEED", "status": "PASS",
            "seed_certificate_count": 1, "completed_target_count": 0,
            "seed_graph": graph, "seed_graph_digest": digest, "seed_labels": SEED,
            "alpha_low_class_size": 6, "seed_certificate": certificate,
            "witness_path": witness, "added_leaf_edge": ["b:0:0", new_leaf]}


def check_completed(K):
    require(type(K) is int and K >= 1 and K + 14 <= LIMITS["max_vertices"],
            "invalid declared K or vertex limit")
    m = K + 13
    profile = [[2], [1], [1], [1]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    digest = graph_digest(original)
    spec = {"method": "four_section_2111", "parameters": {"K": K}, "profile": profile}
    declared, constructed = construction_input(spec, max_vertices=LIMITS["max_vertices"])
    require(declared == original and constructed["graph"] == original and constructed["graph_digest"] == digest
            and len(original["vertices"]) == m + 1 and len(original["edges"]) == m, "original graph mismatch")
    trace = constructed["trace"][0]
    prefix, full = trace["prefix_labels"], constructed["labels"]
    shifted = {v: x + (K if x >= 6 else 0) for v, x in SEED.items()}
    require(prefix == shifted and all(type(x) is int for x in prefix.values()), "exact named prefix mismatch")
    for leaf in ("l:0:0:0", "l:0:0:1"):
        require([e for e in original["edges"] if leaf in e] == [["b:0:0", leaf]],
                "first-branch leaf attached away from original center")
    tail = [f"s:{i}" for i in range(4, K + 5)]
    pending = set(tail[1:])
    tail_edges = {frozenset(e) for e in zip(tail, tail[1:])}
    incident = {frozenset(e) for e in original["edges"] if pending.intersection(e)}
    crossing = {e for e in incident if len(e.intersection(pending)) == 1}
    require(set(original["vertices"]) - set(prefix) == pending and incident == tail_edges
            and crossing == {frozenset(("s:4", "s:5"))}, "original suffix or crossing incidence mismatch")

    resources = {"active_vertex": "s:4", "active_label": K + 6,
                 "unused_labels": list(range(6, K + 6)), "unused_differences": list(range(1, K + 1))}
    require(all(trace[key] == value for key, value in resources.items())
            and trace["prefix_difference_interval"] == [K + 1, m], "saved trace differs from contract")
    partial = verify_partial(original, prefix)
    require(partial["valid"] and partial["graph_digest"] == digest and partial["frontier"] == ["s:4"]
            and partial["used_differences"] == list(range(K + 1, m + 1))
            and all(partial[key] == resources[key] for key in ("unused_labels", "unused_differences")),
            "original prefix certificate or unused inventories mismatch")
    boundary = interval_boundary(original, prefix, "s:4")
    require(boundary["valid"] and boundary["interval"] == [6, K + 5]
            and boundary["remaining_edges"] == K and boundary["all_unfinished_incidence_at_port"]
            and all(boundary[key] == value for key, value in resources.items()), "adjacent s:4 boundary mismatch")

    require(all(full[v] == x for v, x in prefix.items()), "completed labeling changed the prefix")
    tail_differences = [abs(full[u] - full[v]) for u, v in zip(tail, tail[1:])]
    require(sorted(full[v] for v in pending) == resources["unused_labels"]
            and tail_differences == list(range(K, 0, -1)), "suffix resource consumption mismatch")
    completion = [{"operation": "next_spine", "parent": u, "vertex": v,
                   "label": full[v], "difference": difference}
                  for u, v, difference in zip(tail, tail[1:], tail_differences)]
    require(constructed["trace"][1:] == completion, "expected precisely K original suffix assignments")
    p = 6 + (K + 1) // 2
    expected_low = {v for v, x in SEED.items() if x < 6} | set(tail[1::2])
    low = {v for v, x in full.items() if x < p}
    high = set(full) - low
    require(constructed["claim_scope"]["alpha_low_class_size"] == p
            and low == expected_low and len(low) == p
            and sorted(full[v] for v in low) == list(range(p))
            and sorted(full[v] for v in high) == list(range(p, m + 1))
            and all(len(low.intersection(e)) == 1 for e in original["edges"]), "full alpha cut mismatch")
    certificate = verify_certificate(original, full, digest)
    require(certificate["valid"], "unchanged original-target checker rejected the construction")
    return {"parameters": {"K": K}, "original_graph": original, "original_graph_digest": digest,
            "prefix_labels": prefix, "prefix_trace": resources, "partial_certificate": partial,
            "adjacent_boundary": boundary, "crossing_edge": ["s:4", "s:5"],
            "original_suffix_vertices": tail, "original_suffix_edges": list(zip(tail, tail[1:])),
            "full_labels": full, "completion_trace": completion, "tail_differences": tail_differences,
            "alpha_low_class_size": p, "alpha_low_vertices": sorted(low),
            "alpha_high_vertices": sorted(high), "independent_certificate": certificate}


def main():
    here = Path(__file__).resolve().parent
    seed_out = here / "seed_result.json"
    out = here / "regression_result.json"
    if any(p.exists() for p in (seed_out, out, here / "source")):
        raise FileExistsError("Existing evidence is immutable")
    config_path = here / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["K"]
            and config["fixed_branch_sizes"] == [2, 1, 1, 1] and config["padding"] == [0, 0, 0, 0]
            and config["seed_profile"] == [[2], [1], [1], [1], []]
            and all(config[key] == value for key, value in LIMITS.items())
            and config["starting_commit"] == "e29ceaf787543ab5ef430c75f071fe5c2223381b",
            "configuration differs from the declared cases and limits")
    source = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / "lcl").glob("*.py"))}
    source.update({name: sha(ROOT / name) for name in EXTRA_SOURCE})
    for name, digest in source.items():
        snapshot = here / "source" / name
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        data = (ROOT / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, "source changed during capture")
        with snapshot.open("xb") as stream:
            stream.write(data)
    identity = {"run_id": config["run_id"], "starting_commit": config["starting_commit"],
                "config_sha256_raw": sha(config_path), "regression_script_sha256_raw": sha(Path(__file__)),
                "source_sha256_raw": source,
                "environment": {"python": sys.version, "executable": sys.executable, "utf8_mode": sys.flags.utf8_mode, "implementation": platform.python_implementation(),
                                "platform": platform.platform(), "python_optimization_level": sys.flags.optimize},
                "limits": LIMITS}
    started = time.perf_counter()
    write_result(seed_out, check_seed(config["seed_profile"], identity))
    cases = [check_completed(K) for K in config["cases"]]
    result = {**identity, "classification": "COMPLETE", "status": "PASS", "case_count": len(cases),
              "seed_result": seed_out.name, "seed_result_sha256_raw": sha(seed_out),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"),
              "elapsed_seconds": time.perf_counter() - started, "scope": config["scope"], "cases": cases}
    write_result(out, result)
    print(json.dumps({"status": "PASS", "cases": len(cases), "seed_certificates": 1,
                      "seed_output": str(seed_out), "output": str(out)}))


if __name__ == "__main__":
    main()
