"""Bounded independent-original-target checks; create one new result only."""
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    out = here / "regression_result.json"
    if out.exists():
        raise FileExistsError("Choose a new run directory; existing evidence is immutable")
    config = json.loads((here / "config.json").read_text(encoding="utf-8-sig"))
    assert len(config["cases"]) == config["max_cases"] == 12
    results = []
    started = time.perf_counter()
    for q, r, K in config["cases"]:
        assert all(type(x) is int for x in (q, r, K)) and q >= 1 and r >= 1 and K >= 2
        profile = [[q], [r]] + [[] for _ in range(K + 1)]
        retained = build_graph(profile)
        m = q + r + K + 4
        assert len(retained["vertices"]) == m + 1 <= config["max_vertices"]
        expected_edges = {frozenset((f"s:{i}", f"s:{i+1}")) for i in range(K + 2)}
        expected_edges.update((frozenset(("s:0", "b:0:0")), frozenset(("s:1", "b:1:0"))))
        expected_edges.update(frozenset(("b:0:0", f"l:0:0:{j}")) for j in range(q))
        expected_edges.update(frozenset(("b:1:0", f"l:1:0:{j}")) for j in range(r))
        assert {frozenset(edge) for edge in retained["edges"]} == expected_edges
        spec = {"method": "two_section_nonadjacent", "parameters": {"q": q, "r": r, "K": K},
                "profile": profile}
        declared, result = construction_input(spec, max_vertices=config["max_vertices"])
        digest = graph_digest(retained)
        assert declared == retained and result["graph_digest"] == digest
        prefix = result["trace"][0]["prefix_labels"]
        partial = verify_partial(retained, prefix)
        assert partial["valid"] and partial["frontier"] == ["s:2"]
        assert sorted(prefix.values()) == list(range(r + 2)) + list(range(K + r + 2, m + 1))
        assert partial["unused_labels"] == list(range(r + 2, K + r + 2))
        assert partial["unused_differences"] == list(range(1, K + 1))
        assert partial["used_differences"] == list(range(K + 1, m + 1))
        assert prefix["s:2"] == K + r + 3
        full = result["labels"]
        assert all(full[v] == x for v, x in prefix.items())
        certificate = verify_certificate(retained, full, digest)
        assert certificate["valid"], certificate["errors"]
        assert sorted(abs(full[u] - full[v]) for u, v in retained["edges"]) == list(range(1, m + 1))
        results.append({"parameters": {"q": q, "r": r, "K": K},
                        "original_graph": retained, "original_graph_digest": digest,
                        "prefix_labels": prefix, "partial_certificate": partial,
                        "full_labels": full, "independent_certificate": certificate})

    source = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / "lcl").glob("*.py"))}
    for name in ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                 "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                 "tests/test_unpadded_all_qr.py"):
        source[name] = sha(ROOT / name)
    result = {"run_id": config["run_id"], "classification": "COMPLETE", "status": "PASS",
              "case_count": len(results), "config_sha256_raw": sha(here / "config.json"),
              "regression_script_sha256_raw": sha(Path(__file__)), "source_sha256_raw": source,
              "environment": {"python": platform.python_version(), "platform": platform.platform()},
              "elapsed_seconds": time.perf_counter() - started,
              "limits": {"max_cases": 12, "max_vertices": 32, "max_output_bytes": 2000000,
                         "workers": 1}, "scope": config["scope"], "cases": results}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(encoded) > config["max_output_bytes"]:
        raise RuntimeError("result exceeds the declared output cap")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": result["status"], "cases": len(results),
                      "elapsed_seconds": result["elapsed_seconds"], "output": str(out)}))


if __name__ == "__main__":
    main()
