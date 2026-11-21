"""Record the declared 12 B3 original-target construction checks once."""
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
from lcl.verify import verify_certificate, verify_partial

CASES = [[1,1,1,2], [1,1,1,3], [1,1,1,4], [1,1,1,5],
         [2,1,1,2], [2,2,1,6], [3,1,4,3], [3,2,1,4],
         [3,3,5,7], [5,2,3,8], [5,5,2,12], [8,3,7,14]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_b3_unpadded_qge_r.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    out = here / "regression_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable; choose a new run directory")
    config = json.loads((here / "config.json").read_text(encoding="utf-8-sig"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r", "t", "K"]
            and config["padding"] == [0, 0, 0] and config["max_cases"] == 12
            and config["max_vertices"] == 39 and config["max_output_bytes"] == 2000000
            and config["workers"] == 1, "configuration differs from declared task")
    started = time.perf_counter()
    results = []
    for q, r, t, K in config["cases"]:
        require(all(type(v) is int for v in (q, r, t, K)) and q >= r >= 1 and t >= 1 and K >= 2,
                "invalid declared parameters")
        profile = [[q], [r], [t]] + [[] for _ in range(K + 1)]
        original = build_graph(profile)
        m, a = q + r + t + K + 6, q + t + 3
        require(len(original["vertices"]) == m + 1 <= config["max_vertices"], "vertex limit")
        expected = {frozenset((f"s:{i}", f"s:{i+1}")) for i in range(K + 3)}
        expected.update(frozenset((f"s:{i}", f"b:{i}:0")) for i in range(3))
        for i, count in enumerate((q, r, t)):
            expected.update(frozenset((f"b:{i}:0", f"l:{i}:0:{j}")) for j in range(count))
        require(len(expected) == m and {frozenset(e) for e in original["edges"]} == expected
                and set(original["vertices"]) == set().union(*expected), "named original target mismatch")
        spec = {"method": "three_section_nonadjacent", "parameters": {"q": q, "r": r, "t": t, "K": K},
                "profile": profile}
        declared, constructed = construction_input(spec, max_vertices=config["max_vertices"])
        digest = graph_digest(original)
        require(declared == original and constructed["graph_digest"] == digest, "target identity mismatch")
        prefix = constructed["trace"][0]["prefix_labels"]
        full = constructed["labels"]
        partial = verify_partial(original, prefix)
        suffix = {f"s:{i}" for i in range(4, K + 4)}
        remaining_edges = {frozenset((f"s:{i}", f"s:{i+1}")) for i in range(3, K + 3)}
        incident = {frozenset(edge) for edge in original["edges"] if suffix.intersection(edge)}
        require(incident == remaining_edges and set(original["vertices"]) - set(prefix) == suffix,
                "original path or unassigned vertices mismatch")
        require(partial["valid"] and partial["frontier"] == ["s:3"]
                and prefix["s:3"] == a + K + 1
                and partial["unused_labels"] == list(range(a, a + K))
                and partial["unused_differences"] == list(range(1, K + 1)), "prefix contract mismatch")
        require(all(full[v] == x for v, x in prefix.items()), "prefix changed")
        require(set(full) == set(original["vertices"]) and all(type(x) is int for x in full.values())
                and sorted(full.values()) == list(range(m + 1)), "vertex bijection mismatch")
        require(sorted(abs(full[u] - full[v]) for u, v in (tuple(e) for e in expected))
                == list(range(1, m + 1)), "edge bijection mismatch")
        certificate = verify_certificate(original, full, digest)
        require(certificate["valid"], "independent original-target verifier rejected labeling")
        results.append({"parameters": {"q": q, "r": r, "t": t, "K": K},
                        "original_graph": original, "original_graph_digest": digest,
                        "prefix_labels": prefix, "partial_certificate": partial,
                        "full_labels": full, "independent_certificate": certificate})
    source = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / "lcl").glob("*.py"))}
    source.update({name: sha(ROOT / name) for name in EXTRA_SOURCE})
    result = {"run_id": config["run_id"], "classification": "COMPLETE", "status": "PASS",
              "case_count": len(results), "config_sha256_raw": sha(here / "config.json"),
              "regression_script_sha256_raw": sha(Path(__file__)),
              "audit_script_sha256_raw": sha(here / "independent_audit.py"),
              "source_sha256_raw": source,
              "environment": {"python": platform.python_version(), "platform": platform.platform(),
                              "python_optimization_level": sys.flags.optimize},
              "elapsed_seconds": time.perf_counter() - started,
              "limits": {key: config[key] for key in ("max_cases", "max_vertices", "max_output_bytes", "workers")},
              "scope": config["scope"], "cases": results}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= config["max_output_bytes"], "result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": len(results), "output": str(out)}))


if __name__ == "__main__":
    main()
