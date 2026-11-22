"""Check the expanded left component, fixed alpha seed and 12 declared original completed targets."""
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

CASES = [[1, 1, 1], [1, 2, 1], [2, 1, 1], [2, 3, 1], [1, 1, 2], [1, 3, 3],
         [3, 1, 4], [2, 2, 5], [3, 4, 8], [8, 5, 15], [5, 8, 16], [2, 1, 64]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b4_unpadded_qr21.py")
LIMITS = {"max_cases": 12, "max_vertices": 79, "max_output_bytes": 2_000_000, "workers": 1}
UPPER = {"s:0": 9, "s:1": 2, "s:2": 5, "b:0:0": 0, "l:0:0:0": 8,
         "b:1:0": 4, "l:1:0:0": 3, "b:2:0": 1, "l:2:0:0": 6, "l:2:0:1": 7}
LEFT = {"s:0": 11, "s:1": 2, "s:2": 7, "b:0:0": 0, "l:0:0:0": 10,
        "b:1:0": 6, "l:1:0:0": 3, "l:1:0:1": 4, "l:1:0:2": 5,
        "b:2:0": 1, "l:2:0:0": 8, "l:2:0:1": 9}
SEED = {"s:0": 15, "s:1": 2, "s:2": 11, "s:3": 7, "s:4": 8,
        "b:0:0": 0, "l:0:0:0": 14, "l:0:0:1": 16,
        "b:1:0": 10, "l:1:0:0": 3, "l:1:0:1": 4, "l:1:0:2": 5,
        "b:2:0": 1, "l:2:0:0": 12, "l:2:0:1": 13, "b:3:0": 9, "l:3:0:0": 6}
LEFT_WITNESS = ["b:0:0", "s:0", "s:1", "s:2"]
PROFILES = {"upper": [[1], [1], [2]], "left": [[1], [3], [2]], "seed": [[2], [3], [2], [1], []]}


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


def check_upper(profile, identity):
    record = certify(profile, UPPER, 4, LEFT_WITNESS)
    threshold = 8
    selected = {v for v, label in UPPER.items() if label >= threshold}
    incident = [edge for edge in record["graph"]["edges"] if selected.intersection(edge)]
    weights = sorted(abs(UPPER[u] - UPPER[v]) for u, v in incident)
    require(record["certificate"]["n"] == 10 and record["certificate"]["m"] == 9
            and record["ports"] == {"b:0:0": 0, "s:2": 5}
            and UPPER["b:2:0"] == 1 and UPPER["b:1:0"] == 4
            and selected == {"s:0", "l:0:0:0"}
            and weights == [7, 8, 9], "third-expanded left ports or updated predicate")
    return {**identity, **record, "status": "PASS", "classification": "VERIFIED_UPPER_BLOCK_COMPONENT",
            "threshold": threshold, "upper_vertices": sorted(selected), "upper_incident_edges": incident,
            "upper_incident_differences": weights, "minimum_high_host": "b:1:0",
            "label_one_host": "b:2:0", "port_offsets": [0, 1],
            "component_certificate_count": 1, "completed_target_count": 0}


def check_left(profile, identity):
    record = certify(profile, LEFT, 6, LEFT_WITNESS)
    expanded = {v: x + (2 if x >= 4 else 0) for v, x in UPPER.items()}
    expanded.update({"l:1:0:1": 4, "l:1:0:2": 5})
    require(record["certificate"]["n"] == 12 and record["certificate"]["m"] == 11
            and record["ports"] == {"b:0:0": 0, "s:2": 7} and LEFT["b:1:0"] == 6
            and LEFT["b:2:0"] == 1 and LEFT == expanded,
            "expanded left order, hosts, transport or ports")
    return {**identity, **record, "status": "PASS", "classification": "VERIFIED_EXPANDED_LEFT",
            "minimum_high_host": "b:1:0", "label_one_host": "b:2:0", "port_offsets": [0, 1],
            "component_certificate_count": 1, "completed_target_count": 0}


def check_seed(profile, identity):
    witness = LEFT_WITNESS + ["s:3", "s:4"]
    record = certify(profile, SEED, 8, witness)
    composed = {v: x + (4 if x >= 6 else 0) for v, x in LEFT.items()}
    composed.update({"s:3": 7, "s:4": 8, "b:3:0": 9, "l:3:0:0": 6, "l:0:0:1": 16})
    require(record["certificate"]["n"] == 17 and record["certificate"]["m"] == 16
            and record["ports"] == {"b:0:0": 0, "s:4": 8} and SEED["s:0"] == 15
            and SEED == composed and ["s:2", "s:3"] in record["graph"]["edges"]
            and SEED["s:2"] - SEED["s:3"] == 4, "seed ports, R241 transport or prescribed zero-port leaf")
    return {**identity, **record, "status": "PASS", "classification": "VERIFIED_FIXED_SEED",
            "port_offsets": [0, 0], "seed_certificate_count": 1, "completed_target_count": 0}


def check_completed(q, r, K):
    m = q + r + K + 11
    a = r + 5
    require(m + 1 <= LIMITS["max_vertices"], "target exceeds declared vertex limit")
    profile = [[q], [r], [2], [1]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    digest = graph_digest(original)
    params = {"q": q, "r": r, "K": K}
    spec = {"method": "four_section_qr21", "parameters": params, "profile": profile}
    declared, constructed = construction_input(spec, max_vertices=LIMITS["max_vertices"])
    require(declared == original and constructed["graph"] == original and constructed["graph_digest"] == digest
            and len(original["vertices"]) == m + 1 and len(original["edges"]) == m, "original graph mismatch")
    trace = constructed["trace"][0]
    prefix, full = trace["prefix_labels"], constructed["labels"]
    expected_low = {"b:0:0", "b:2:0", "s:1", "s:3", "l:3:0:0"}
    expected_low.update(f"l:1:0:{j}" for j in range(r))
    first = [K + r + 11] + [K + r + 12 + j for j in range(1, q)]
    require(prefix["s:0"] == m - (q - 1)
            and [prefix[f"l:0:0:{j}"] for j in range(q)] == first
            and [prefix[f"l:1:0:{j}"] for j in range(r)] == list(range(3, r + 3))
            and [prefix["l:2:0:0"], prefix["l:2:0:1"]] == [K + r + 9, K + r + 10]
            and {v for v, x in prefix.items() if x < a} == expected_low
            and all(type(x) is int for x in prefix.values()), "exact named prefix or classes")
    for leaf in ("l:2:0:0", "l:2:0:1"):
        require([e for e in original["edges"] if leaf in e] == [["b:2:0", leaf]], "third leaf attachment")
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
    left_out = here / "left_component_result.json"
    upper_out = here / "upper_component_result.json"
    if any(p.exists() for p in (seed_out, left_out, upper_out, out, here / "source")):
        raise FileExistsError("Existing evidence is immutable")
    config_path = here / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r", "K"]
            and config["auxiliary_profiles"] == PROFILES
            and all(config[key] == value for key, value in LIMITS.items())
            and config["starting_commit"] == "2b1b71c7e589dd8a360e9addf81d096482289aa9",
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
    write_result(upper_out, check_upper(PROFILES["upper"], identity))
    write_result(left_out, check_left(PROFILES["left"], identity))
    write_result(seed_out, check_seed(PROFILES["seed"], identity))
    cases = [check_completed(*params) for params in config["cases"]]
    result = {**identity, "classification": "COMPLETE", "status": "PASS", "case_count": len(cases),
              "upper_component_result": upper_out.name, "upper_component_sha256_raw": sha(upper_out),
              "left_component_result": left_out.name, "left_component_sha256_raw": sha(left_out),
              "seed_result": seed_out.name, "seed_result_sha256_raw": sha(seed_out),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"),
              "elapsed_seconds": time.perf_counter() - started, "scope": config["scope"], "cases": cases}
    write_result(out, result)
    print(json.dumps({"status": "PASS", "cases": len(cases), "seed_certificates": 1, "expanded_left_certificates": 1, "upper_block_certificates": 1,
                      "seed_output": str(seed_out), "output": str(out)}))


if __name__ == "__main__":
    main()
