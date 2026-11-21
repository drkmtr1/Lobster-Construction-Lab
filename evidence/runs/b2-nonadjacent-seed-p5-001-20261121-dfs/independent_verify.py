"""Check the saved seed and fixed construction on original named graphs.

No search or solver is called. The output is new and created exclusively.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from lcl.consumers import complete_nonadjacent_path
from lcl.ingest import graph_input
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    output = here / "independent_verification.json"
    if output.exists():
        raise FileExistsError("Choose a new output; prior results are immutable")
    graph_path = ROOT / "examples/unequal_seed.json"
    domain_path = ROOT / "examples/unequal_seed_domains.json"
    pin_path = ROOT / "examples/nonadjacent_seed_p5_001_pins.json"
    limit_path = ROOT / "configs/unequal_seed_limits.json"
    original = graph_input(graph_path)
    domains = json.loads(domain_path.read_text(encoding="utf-8-sig"))
    pins = json.loads(pin_path.read_text(encoding="utf-8-sig"))
    record = json.loads((here / "record.json").read_text(encoding="utf-8-sig"))
    h = record["result"]["witness"]
    edges = [("s:0", "s:1"), ("s:0", "b:0:0"), ("b:0:0", "l:0:0:0"),
             ("s:1", "b:1:0"), ("b:1:0", "l:1:0:0"),
             ("b:1:0", "l:1:0:1"), ("s:1", "s:2")]
    assert original["profile"] == [[1], [2], []]
    assert {frozenset(e) for e in original["edges"]} == {frozenset(e) for e in edges}
    assert graph_digest(original) == record["original_graph_digest"]
    assert original == record["original_graph"]
    assert pins == {"s:2": 5} and record["config"]["pins"] == pins
    assert record["config"]["domains"] == domains
    assert all(type(h[v]) is int and h[v] in allowed for v, allowed in domains.items())
    assert h["s:2"] == 5 and sorted(h.values()) == list(range(8))
    differences = [abs(h[u] - h[v]) for u, v in edges]
    assert sorted(differences) == list(range(1, 8))
    seed_certificate = verify_certificate(original, h, graph_digest(original))
    assert seed_certificate["valid"], seed_certificate["errors"]
    assert record["result"]["status"] == "SAT" and record["result"]["exhausted"] is False

    cases = []
    for K in (2, 3, 6, 10):
        target = build_graph([[1], [2]] + [[] for _ in range(K + 1)])
        prefix = {"s:0": K + 6, "s:1": 1, "s:2": K + 5,
                  "b:0:0": 0, "l:0:0:0": K + 7, "b:1:0": K + 4,
                  "l:1:0:0": 2, "l:1:0:1": 3}
        partial = verify_partial(target, prefix)
        assert partial["valid"] and partial["unused_labels"] == list(range(4, K + 4))
        assert partial["unused_differences"] == list(range(1, K + 1))
        assert prefix["s:2"] == 4 + K + 1
        labels = complete_nonadjacent_path(target, prefix, K, 4)
        certificate = verify_certificate(target, labels, graph_digest(target))
        assert certificate["valid"], certificate["errors"]
        assert all(labels[v] == x for v, x in prefix.items())
        cases.append({"K": K, "original_graph": target, "original_graph_digest": graph_digest(target),
                      "prefix": prefix, "labels": labels, "certificate": certificate})

    pilot_path = ROOT / ("evidence/validation/release_final/pilot/cases/"
                         "31da62597181ea39545cd89689e591113261ea7c9c7af56e60383894da947a57.attempt-0001.json")
    pilot = json.loads(pilot_path.read_text(encoding="utf-8-sig"))
    original_k1 = build_graph([[1], [2], [], []])
    assert pilot["original_graph"] == original_k1
    k1_certificate = verify_certificate(original_k1, pilot["result"]["witness"], graph_digest(original_k1))
    assert k1_certificate["valid"], k1_certificate["errors"]
    assert pilot["result"]["witness"]["s:2"] == 2 and pilot["result"]["witness"]["s:3"] == 1

    inputs = {p.relative_to(ROOT).as_posix(): sha(p)
              for p in (graph_path, domain_path, pin_path, limit_path, pilot_path)}
    result = {"task": "B2-NONADJACENT-SEED-P5-001 independent positive verification",
              "status": "PASS", "scope": "one saved p=5 witness and deterministic construction checks; no search",
              "python": platform.python_version(), "platform": platform.platform(),
              "script_sha256_raw": sha(Path(__file__)), "input_sha256_raw": inputs,
              "dfs_record_sha256_raw": sha(here / "record.json"),
              "seed_graph_digest": graph_digest(original), "seed_labels": h,
              "seed_original_edges": edges, "seed_edge_differences": differences,
              "seed_certificate": seed_certificate, "deterministic_cases": cases,
              "existing_K1_pilot_sha256_raw": sha(pilot_path), "existing_K1_certificate": k1_certificate}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(encoded) > 2_000_000:
        raise RuntimeError("verification result exceeds 2 MB")
    with output.open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": result["status"], "seed_differences": differences,
                      "deterministic_K": [c["K"] for c in cases], "output": str(output)}))


if __name__ == "__main__":
    main()
