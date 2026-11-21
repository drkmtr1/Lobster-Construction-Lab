"""Audit saved certificates on the declared named graphs, without a solver."""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    here = Path(__file__).resolve().parent
    out = here / "independent_audit_result.json"
    if out.exists():
        raise FileExistsError("Choose a new run directory; prior outputs are immutable")
    config = json.loads((here / "config.json").read_text(encoding="utf-8-sig"))
    saved = json.loads((here / "regression_result.json").read_text(encoding="utf-8-sig"))
    require(saved["status"] == "PASS" and len(saved["cases"]) == len(config["cases"]) == 12,
            "saved run status or case count mismatch")
    require(sha(here / "config.json") == saved["config_sha256_raw"], "config hash mismatch")
    require(sha(here / "regression.py") == saved["regression_script_sha256_raw"],
            "regression script hash mismatch")
    for name, expected_hash in saved["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(here / "source" / name) == expected_hash,
                "source or snapshot hash mismatch: " + name)

    checked = []
    start = time.perf_counter()
    for expected, case in zip(config["cases"], saved["cases"]):
        q, r, K = expected
        require(case["parameters"] == {"q": q, "r": r, "K": K}, "case identity mismatch")
        original = build_graph([[q], [r]] + [[] for _ in range(K + 1)])
        require(case["original_graph"] == original, "saved original graph mismatch")
        actual_edges = {frozenset((f"s:{i}", f"s:{i+1}")) for i in range(K + 2)}
        actual_edges.update((frozenset(("s:0", "b:0:0")), frozenset(("s:1", "b:1:0"))))
        actual_edges.update(frozenset(("b:0:0", f"l:0:0:{j}")) for j in range(q))
        actual_edges.update(frozenset(("b:1:0", f"l:1:0:{j}")) for j in range(r))
        require({frozenset(e) for e in original["edges"]} == actual_edges, "named edge mismatch")
        digest = graph_digest(original)
        require(digest == case["original_graph_digest"], "original graph digest mismatch")
        partial = verify_partial(original, case["prefix_labels"])
        require(partial["valid"] and partial["unused_labels"] == list(range(r + 2, K + r + 2))
                and partial["unused_differences"] == list(range(1, K + 1))
                and case["prefix_labels"]["s:2"] == K + r + 3, "prefix contract mismatch")
        labels = case["full_labels"]
        require(all(labels[v] == x for v, x in case["prefix_labels"].items()), "prefix changed")
        certificate = verify_certificate(original, labels, digest)
        require(certificate["valid"], "original-target certificate invalid")
        differences = [abs(labels[u] - labels[v]) for u, v in original["edges"]]
        require(sorted(differences) == list(range(1, q + r + K + 5)), "edge spectrum mismatch")
        checked.append({"q": q, "r": r, "K": K, "graph_digest": digest,
                        "certificate_valid": True, "actual_edge_differences": differences})
    result = {"task": "B2-UNPADDED-ALL-QR-001 saved-certificate audit", "status": "PASS",
              "scope": "12 already-saved named targets; no constructor, solver, K=1 case or new search",
              "case_count": len(checked), "cases": checked,
              "config_sha256_raw": sha(here / "config.json"),
              "saved_regression_sha256_raw": sha(here / "regression_result.json"),
              "script_sha256_raw": sha(Path(__file__)),
              "environment": {"python": platform.python_version(), "platform": platform.platform(),
                              "python_optimization_level": sys.flags.optimize},
              "elapsed_seconds": time.perf_counter() - start}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= config["max_output_bytes"], "audit result exceeds 2 MB")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": result["status"], "cases": len(checked), "output": str(out)}))


if __name__ == "__main__":
    main()
