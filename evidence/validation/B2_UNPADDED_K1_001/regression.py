"""Record the declared 12 original-target K=1 construction checks once."""
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

CASES = [[1, 1], [1, 2], [2, 1], [1, 8], [8, 1], [2, 3],
         [3, 2], [3, 3], [4, 9], [9, 4], [17, 31], [31, 17]]
EXTRA_SOURCE = ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                "tests/test_unpadded_k1.py")


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
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r"]
            and config["K"] == 1 and config["z0"] == config["z1"] == 0
            and config["max_cases"] == 12 and config["max_vertices"] == 54
            and config["max_output_bytes"] == 2000000 and config["workers"] == 1,
            "configuration differs from the declared bounded task")
    started = time.perf_counter()
    results = []
    for q, r in config["cases"]:
        require(type(q) is int and type(r) is int and q >= 1 and r >= 1, "invalid parameters")
        profile = [[q], [r], [], []]
        original = build_graph(profile)
        m = q + r + 5
        require(len(original["vertices"]) == m + 1 <= config["max_vertices"], "vertex limit")
        expected = {frozenset((f"s:{i}", f"s:{i+1}")) for i in range(3)}
        expected.update((frozenset(("s:0", "b:0:0")), frozenset(("s:1", "b:1:0"))))
        expected.update(frozenset(("b:0:0", f"l:0:0:{j}")) for j in range(q))
        expected.update(frozenset(("b:1:0", f"l:1:0:{j}")) for j in range(r))
        require(len(expected) == m and {frozenset(e) for e in original["edges"]} == expected
                and set(original["vertices"]) == set().union(*expected), "original named target mismatch")
        spec = {"method": "two_section_k1", "parameters": {"q": q, "r": r}, "profile": profile}
        declared, constructed = construction_input(spec, max_vertices=config["max_vertices"])
        digest = graph_digest(original)
        require(declared == original and constructed["graph_digest"] == digest, "target identity mismatch")
        prefix = constructed["trace"][0]["prefix_labels"]
        full = constructed["labels"]
        partial = verify_partial(original, prefix)
        require(partial["valid"] and set(prefix) == set(original["vertices"]) - {"s:3"}
                and partial["frontier"] == ["s:2"] and prefix["s:2"] == 1
                and partial["unused_labels"] == [q + 4]
                and partial["unused_differences"] == [q + 3], "prefix contract mismatch")
        require(all(full[v] == x for v, x in prefix.items()) and full["s:3"] == q + 4,
                "completion or prefix changed")
        require(set(full) == set(original["vertices"]) and all(type(x) is int for x in full.values())
                and sorted(full.values()) == list(range(m + 1)), "vertex bijection mismatch")
        require(sorted(abs(full[u] - full[v]) for u, v in (tuple(e) for e in expected))
                == list(range(1, m + 1)), "edge bijection mismatch")
        certificate = verify_certificate(original, full, digest)
        require(certificate["valid"], "independent original-target verifier rejected labeling")
        results.append({"parameters": {"q": q, "r": r, "K": 1}, "original_graph": original,
                        "original_graph_digest": digest, "prefix_labels": prefix,
                        "partial_certificate": partial, "full_labels": full,
                        "independent_certificate": certificate})
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
