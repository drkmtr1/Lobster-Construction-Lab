"""Check the 12 declared original B3 targets and their singleton boundaries."""
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


def check_case(q, r, t):
    require(all(type(x) is int and x >= 1 for x in (q, r, t)), "invalid declared parameters")
    m = q + r + t + 7
    require(m + 1 <= LIMITS["max_vertices"], "vertex limit")
    profile = [[q], [r], [t], [], []]
    original = build_graph(profile)
    digest = graph_digest(original)
    spec = {"method": "three_section_k1", "parameters": {"q": q, "r": r, "t": t}, "profile": profile}
    declared, constructed = construction_input(spec, max_vertices=LIMITS["max_vertices"])
    require(declared == original and constructed["graph_digest"] == digest, "original graph identity mismatch")
    require(original["profile"] == profile and len(original["vertices"]) == m + 1
            and len(original["edges"]) == m, "original profile or counts mismatch")

    trace = constructed["trace"][0]
    prefix, full = trace["prefix_labels"], constructed["labels"]
    require(set(original["vertices"]) - set(prefix) == {"s:4"}, "prefix vertex set mismatch")
    remaining_edges = sorted(sorted(e) for e in original["edges"] if not set(e) <= set(prefix))
    require(remaining_edges == [["s:3", "s:4"]], "unfinished incidence mismatch")
    unused = {"unused_labels": [q + 2], "unused_differences": [t + 3],
              "active_vertex": "s:3", "active_label": q + t + 5}
    require(all(trace[k] == v for k, v in unused.items()), "singleton trace mismatch")
    partial = verify_partial(original, prefix)
    require(partial["valid"] and partial["graph_digest"] == digest and partial["frontier"] == ["s:3"]
            and prefix["s:3"] == unused["active_label"]
            and partial["unused_labels"] == unused["unused_labels"]
            and partial["unused_differences"] == unused["unused_differences"],
            "original-target singleton boundary mismatch")
    boundary = interval_boundary(original, prefix, "s:3")
    require(not boundary["valid"], "adjacent predicate accepted the singleton difference t+3")
    require(all(full[v] == x for v, x in prefix.items()), "completed labeling changed the prefix")
    difference = abs(full["s:3"] - full["s:4"])
    require(full["s:4"] == q + 2 and difference == t + 3, "original final edge did not consume both singletons")
    certificate = verify_certificate(original, full, digest)
    require(certificate["valid"], "unchanged original-target checker rejected the construction")
    return {"parameters": spec["parameters"], "original_graph": original, "original_graph_digest": digest,
            "prefix_labels": prefix, "singleton_trace": unused, "partial_certificate": partial,
            "remaining_edges": remaining_edges, "adjacent_boundary": boundary,
            "full_labels": full, "tail_difference": difference, "independent_certificate": certificate}


def main():
    here = Path(__file__).resolve().parent
    out = here / "regression_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable")
    config_path = here / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r", "t"]
            and config["fixed_parameters"] == {"K": 1} and config["padding"] == [0, 0, 0]
            and all(config[k] == v for k, v in LIMITS.items())
            and config["starting_commit"] == "a1e8a15de2f33c5de877a941612c657a62d48747",
            "configuration differs from the authorized cases and limits")
    source = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / "lcl").glob("*.py"))}
    source.update({name: sha(ROOT / name) for name in EXTRA_SOURCE})
    started = time.perf_counter()
    cases = [check_case(q, r, t) for q, r, t in config["cases"]]
    result = {"run_id": config["run_id"], "starting_commit": config["starting_commit"],
              "classification": "COMPLETE", "status": "PASS", "case_count": len(cases),
              "config_sha256_raw": sha(config_path), "regression_script_sha256_raw": sha(Path(__file__)),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"), "source_sha256_raw": source,
              "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                              "platform": platform.platform(), "python_optimization_level": sys.flags.optimize},
              "limits": LIMITS, "elapsed_seconds": time.perf_counter() - started,
              "scope": config["scope"], "cases": cases}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= LIMITS["max_output_bytes"], "result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": result["case_count"], "output": str(out)}))


if __name__ == "__main__":
    main()
