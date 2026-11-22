"""Check the fixed alpha seed and 12 declared original completed targets."""
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

CASES = [[1, 1], [2, 1], [3, 1], [1, 2], [2, 2], [1, 3], [3, 4], [5, 5],
         [8, 8], [13, 16], [5, 31], [2, 64]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b4_fourth_2_supply.py")
LIMITS = {"max_cases": 12, "max_vertices": 79, "max_output_bytes": 2_000_000, "workers": 1}
SEED = {"s:0": 13, "s:1": 0, "s:2": 8, "s:3": 6, "s:4": 7,
        "b:0:0": 1, "l:0:0:0": 12, "b:1:0": 10, "l:1:0:0": 3,
        "b:2:0": 2, "l:2:0:0": 11, "b:3:0": 9, "l:3:0:0": 4, "l:3:0:1": 5}
WITNESS = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]


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


def certify(profile, labels, low_size, witness):
    graph = build_graph(profile)
    digest = graph_digest(graph)
    certificate = verify_certificate(graph, labels, digest)
    require(certificate["valid"] and all((labels[u] < low_size) != (labels[v] < low_size)
                                         for u, v in graph["edges"]), "alpha certificate")
    edges = {frozenset(edge) for edge in graph["edges"]}
    require(all(frozenset(e) in edges for e in zip(witness, witness[1:])), "witness path")
    reached = set(witness)
    for _ in range(2):
        reached |= {v for e in graph["edges"] if reached.intersection(e) for v in e}
    require(reached == set(graph["vertices"]), "witness distance")
    return {"graph": graph, "graph_digest": digest, "labels": labels, "certificate": certificate,
            "alpha_low_class_size": low_size, "witness_path": witness,
            "ports": {v: labels[v] for v in (witness[0], witness[-1])}}


def check_seed(profile, identity):
    record = certify(profile, SEED, 7, WITNESS)
    selected = {v for v, x in SEED.items() if x >= 12}
    incident = [e for e in record["graph"]["edges"] if selected.intersection(e)]
    weights = sorted(abs(SEED[u] - SEED[v]) for u, v in incident)
    require(record["certificate"]["n"] == 14 and record["certificate"]["m"] == 13
            and record["ports"] == {"b:0:0": 1, "s:4": 7}
            and selected == {"s:0", "l:0:0:0"} and weights == [11, 12, 13],
            "seed ports or full incident predicate")
    return {**identity, **record, "status": "PASS", "classification": "VERIFIED_FIXED_SEED",
            "threshold": 12, "selected_upper_vertices": sorted(selected), "upper_incident_edges": incident,
            "upper_incident_differences": weights, "port_offsets": [1, 0],
            "seed_certificate_count": 1, "completed_target_count": 0}


def check_completed(q, K):
    m = q + K + 12
    a = 7
    require(m + 1 <= LIMITS["max_vertices"], "target exceeds declared vertex limit")
    profile = [[q], [1], [1], [2]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    digest = graph_digest(original)
    params = {"q": q, "K": K}
    spec = {"method": "four_section_q112", "parameters": params, "profile": profile}
    declared, constructed = construction_input(spec, max_vertices=LIMITS["max_vertices"])
    require(declared == original and constructed["graph"] == original and constructed["graph_digest"] == digest
            and len(original["vertices"]) == m + 1 and len(original["edges"]) == m, "original graph mismatch")
    trace = constructed["trace"][0]
    prefix, full = trace["prefix_labels"], constructed["labels"]
    expected = {v: x + (K if x >= 7 else 0) + (q - 1 if x >= 12 else 0) for v, x in SEED.items()}
    expected.update({f"l:0:0:{j}": K + 11 + j for j in range(1, q)})
    require(prefix == expected and all(type(x) is int for x in prefix.values()), "exact named prefix")
    expected_low = {v for v, x in expected.items() if x < a}
    for j in range(2):
        leaf = f"l:3:0:{j}"
        require([e for e in original["edges"] if leaf in e] == [["b:3:0", leaf]], "fourth leaf attachment")
    tail = [f"s:{i}" for i in range(4, K + 5)]
    pending = set(tail[1:])
    tail_edges = {frozenset(e) for e in zip(tail, tail[1:])}
    incident = {frozenset(e) for e in original["edges"] if pending.intersection(e)}
    crossing = {e for e in incident if len(e.intersection(pending)) == 1}
    require(set(original["vertices"]) - set(prefix) == pending and incident == tail_edges
            and crossing == {frozenset(("s:4", "s:5"))}, "original suffix or crossing incidence mismatch")

    resources = {"active_vertex": "s:4", "active_label": K + a,
                 "unused_labels": list(range(a, K + a)), "unused_differences": list(range(1, K + 1))}
    require(all(trace[key] == value for key, value in resources.items())
            and trace["prefix_difference_interval"] == [K + 1, m], "saved trace differs from contract")
    partial = verify_partial(original, prefix)
    require(partial["valid"] and partial["graph_digest"] == digest and partial["frontier"] == ["s:4"]
            and partial["used_differences"] == list(range(K + 1, m + 1))
            and all(partial[key] == resources[key] for key in ("unused_labels", "unused_differences")),
            "original prefix certificate or unused inventories mismatch")
    boundary = interval_boundary(original, prefix, "s:4")
    require(boundary["valid"] and boundary["interval"] == [a, K + a - 1]
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
    p = a + (K + 1) // 2
    expected_low |= set(tail[1::2])
    low = {v for v, x in full.items() if x < p}
    high = set(full) - low
    require(constructed["claim_scope"]["alpha_low_class_size"] == p
            and low == expected_low and len(low) == p
            and sorted(full[v] for v in low) == list(range(p))
            and sorted(full[v] for v in high) == list(range(p, m + 1))
            and all(len(low.intersection(e)) == 1 for e in original["edges"]), "full alpha cut mismatch")
    certificate = verify_certificate(original, full, digest)
    require(certificate["valid"], "unchanged original-target checker rejected the construction")
    return {"parameters": params, "original_graph": original, "original_graph_digest": digest,
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
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "K"]
            and config["seed_profile"] == [[1], [1], [1], [2], []]
            and all(config[key] == value for key, value in LIMITS.items())
            and config["starting_commit"] == "18f1961b464ec3aa6537cbdf078a4a21421a8632",
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
    cases = [check_completed(*params) for params in config["cases"]]
    result = {**identity, "classification": "COMPLETE", "status": "PASS", "case_count": len(cases),
              "seed_result": seed_out.name, "seed_result_sha256_raw": sha(seed_out),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"),
              "elapsed_seconds": time.perf_counter() - started, "scope": config["scope"], "cases": cases}
    write_result(out, result)
    print(json.dumps({"status": "PASS", "cases": len(cases), "seed_certificates": 1,
                      "seed_output": str(seed_out), "output": str(out)}))


if __name__ == "__main__":
    main()
