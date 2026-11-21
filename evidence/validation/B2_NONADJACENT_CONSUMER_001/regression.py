"""Bounded original-path cross-check; save one new JSON result exclusively."""
from __future__ import annotations

import copy
import hashlib
import json
import platform
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from lcl.consumers import complete_nonadjacent_path
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference(K):
    """Separate direct definition, used only for this bounded regression."""
    bases = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3)}
    if K in bases:
        return bases[K]
    old = reference(K - 3)
    return (K + 1, 1, K - 1, 0, *(K - 2 - x for x in old[1:]))


def main():
    here = Path(__file__).resolve().parent
    output = here / "regression_result.json"
    if output.exists():
        raise FileExistsError("Choose a new run directory; results are immutable")
    config = json.loads((here / "config.json").read_text(encoding="utf-8"))
    results = []
    started = time.perf_counter()
    for K in range(config["K_min"], config["K_max"] + 1):
        ell = config["ell"]
        graph = build_graph([[] for _ in range(K + 3)])
        original = copy.deepcopy(graph)
        expected_edges = {frozenset((f"s:{i}", f"s:{i+1}")) for i in range(K + 2)}
        assert {frozenset(e) for e in original["edges"]} == expected_edges
        prefix = {"s:0": K + 1, "s:1": 0, "s:2": K + 2}
        saved_prefix = dict(prefix)
        full = complete_nonadjacent_path(graph, prefix, K, ell)
        path_labels = [full[f"s:{i}"] for i in range(2, K + 3)]
        actual_differences = [abs(full[u] - full[v]) for u, v in original["edges"]]
        certificate = verify_certificate(original, full, graph_digest(original))
        assert graph == original and prefix == saved_prefix
        assert all(full[v] == value for v, value in prefix.items())
        assert path_labels == [ell + value for value in reference(K)]
        assert sorted(full.values()) == list(range(K + 3))
        assert sorted(actual_differences) == list(range(1, K + 3))
        assert certificate["valid"], certificate["errors"]
        results.append({"K": K, "original_graph": original, "graph_digest": graph_digest(original),
                        "prefix_labels": prefix, "labels": full,
                        "original_edge_differences": actual_differences,
                        "independent_certificate": certificate})
    assert len(results) == config["case_count"]
    source = {p.relative_to(ROOT).as_posix(): sha(p)
              for p in sorted((ROOT / "lcl").glob("*.py"))}
    for name in ("pyproject.toml", "requirements.txt", "requirements-graph.txt",
                 "requirements-optional.txt", "requirements-smt.txt", "requirements-symbolic.txt",
                 "tests/test_nonadjacent_consumer.py"):
        source[name] = sha(ROOT / name)
    result = {"run_id": config["run_id"], "classification": "COMPLETE",
              "status": "PASS", "cases_completed": len(results),
              "config_sha256_raw": sha(here / "config.json"),
              "regression_script_sha256_raw": sha(Path(__file__)),
              "source_sha256_raw": source,
              "environment": {"python": platform.python_version(), "platform": platform.platform()},
              "elapsed_seconds": time.perf_counter() - started,
              "limits": {"case_count": 31, "max_vertices": 35, "workers": 1},
              "claim": config["scope"], "cases": results}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(encoded) > 2_000_000:
        raise RuntimeError("output exceeds the 2 MB cap")
    with output.open("xb") as out:
        out.write(encoded)
    print(json.dumps({"status": result["status"], "cases": len(results),
                      "elapsed_seconds": result["elapsed_seconds"], "output": str(output)}))


if __name__ == "__main__":
    main()
