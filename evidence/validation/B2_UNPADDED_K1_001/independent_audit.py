"""Audit saved K=1 certificates and raw source custody without constructing labels."""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from lcl.verify import verify_certificate, verify_graph, verify_partial

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
    out = here / "independent_audit_result.json"
    if out.exists():
        raise FileExistsError("Existing evidence is immutable; choose a new run directory")
    config = json.loads((here / "config.json").read_text(encoding="utf-8-sig"))
    require(config["cases"] == CASES and config["parameter_order"] == ["q", "r"]
            and config["K"] == 1 and config["z0"] == config["z1"] == 0
            and config["max_cases"] == 12 and config["max_vertices"] == 54
            and config["max_output_bytes"] == 2000000 and config["workers"] == 1,
            "configuration differs from the declared bounded task")
    saved_path = here / "regression_result.json"
    require(saved_path.stat().st_size <= config["max_output_bytes"], "saved result exceeds limit")
    saved = json.loads(saved_path.read_text(encoding="utf-8-sig"))
    require(saved["run_id"] == config["run_id"] and saved["classification"] == "COMPLETE"
            and saved["status"] == "PASS" and saved["case_count"] == len(saved["cases"]) == 12,
            "saved status or case count mismatch")
    require(sha(here / "config.json") == saved["config_sha256_raw"], "config hash mismatch")
    require(sha(here / "regression.py") == saved["regression_script_sha256_raw"],
            "regression script hash mismatch")
    require(sha(Path(__file__)) == saved["audit_script_sha256_raw"], "audit script hash mismatch")
    names = {p.relative_to(ROOT).as_posix() for p in (ROOT / "lcl").glob("*.py")} | set(EXTRA_SOURCE)
    require(set(saved["source_sha256_raw"]) == names, "source inventory mismatch")
    for name, expected_hash in saved["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(here / "source" / name) == expected_hash,
                "source or snapshot hash mismatch: " + name)
    started = time.perf_counter()
    checked = []
    for (q, r), case in zip(config["cases"], saved["cases"]):
        require(type(q) is int and type(r) is int and q >= 1 and r >= 1, "invalid parameters")
        require(case["parameters"] == {"q": q, "r": r, "K": 1}, "case identity mismatch")
        m = q + r + 5
        require(m + 1 <= config["max_vertices"], "vertex limit")
        vertices = {f"s:{i}" for i in range(4)} | {"b:0:0", "b:1:0"}
        vertices |= {f"l:0:0:{j}" for j in range(q)} | {f"l:1:0:{j}" for j in range(r)}
        edges = {tuple(sorted((f"s:{i}", f"s:{i + 1}"))) for i in range(3)}
        edges |= {tuple(sorted(("s:0", "b:0:0"))), tuple(sorted(("s:1", "b:1:0")))}
        edges |= {tuple(sorted(("b:0:0", f"l:0:0:{j}"))) for j in range(q)}
        edges |= {tuple(sorted(("b:1:0", f"l:1:0:{j}"))) for j in range(r)}
        graph = case["original_graph"]
        require(graph["profile"] == [[q], [r], [], []] and len(graph["vertices"]) == len(vertices) == m + 1
                and set(graph["vertices"]) == vertices and len(graph["edges"]) == len(edges) == m
                and {tuple(sorted(e)) for e in graph["edges"]} == edges, "named original target mismatch")
        graph_report = verify_graph(graph)
        digest = case["original_graph_digest"]
        require(graph_report["valid"] and graph_report["graph_digest"] == digest, "graph digest mismatch")
        prefix, labels = case["prefix_labels"], case["full_labels"]
        require(set(prefix) == vertices - {"s:3"} and prefix["s:2"] == 1
                and all(type(x) is int for x in prefix.values()), "prefix domain or port mismatch")
        require(set(labels) == vertices and all(type(x) is int for x in labels.values())
                and sorted(labels.values()) == list(range(m + 1)), "label bijection mismatch")
        require(all(labels[v] == x for v, x in prefix.items()) and labels["s:3"] == q + 4,
                "prefix or completion mismatch")
        prefix_edges = [(u, v) for u, v in edges if u in prefix and v in prefix]
        prefix_diffs = [abs(prefix[u] - prefix[v]) for u, v in prefix_edges]
        require(set(range(m + 1)) - set(prefix.values()) == {q + 4}
                and len(prefix_diffs) == len(set(prefix_diffs))
                and set(range(1, m + 1)) - set(prefix_diffs) == {q + 3},
                "arithmetic singleton inventories mismatch")
        crossing = {(u, v) for u, v in edges if (u in prefix) != (v in prefix)}
        require(crossing == {("s:2", "s:3")}, "unfinished physical edge mismatch")
        partial = verify_partial(graph, prefix)
        require(partial["valid"] and partial["frontier"] == ["s:2"]
                and partial["unused_labels"] == [q + 4] and partial["unused_differences"] == [q + 3]
                and partial == case["partial_certificate"], "partial verifier mismatch")
        differences = [abs(labels[u] - labels[v]) for u, v in edges]
        require(sorted(differences) == list(range(1, m + 1)), "edge bijection mismatch")
        certificate = verify_certificate(graph, labels, digest)
        require(certificate["valid"] and certificate == case["independent_certificate"],
                "saved full certificate mismatch")
        checked.append({"q": q, "r": r, "K": 1, "graph_digest": digest,
                        "certificate_valid": True, "actual_edge_differences": sorted(differences)})
    result = {"task": "B2-UNPADDED-K1-001 saved-certificate audit", "status": "PASS",
              "scope": "12 saved named targets; no constructor, solver, or search",
              "case_count": len(checked), "cases": checked,
              "config_sha256_raw": sha(here / "config.json"),
              "saved_regression_sha256_raw": sha(saved_path),
              "script_sha256_raw": sha(Path(__file__)),
              "environment": {"python": platform.python_version(), "platform": platform.platform(),
                              "python_optimization_level": sys.flags.optimize},
              "limits": {key: config[key] for key in ("max_cases", "max_vertices", "max_output_bytes", "workers")},
              "elapsed_seconds": time.perf_counter() - started}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(len(encoded) <= config["max_output_bytes"], "audit result exceeds output limit")
    with out.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "cases": len(checked), "output": str(out)}))


if __name__ == "__main__":
    main()
