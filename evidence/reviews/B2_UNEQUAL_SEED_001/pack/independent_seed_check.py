"""Independent, bounded audit of B2-UNEQUAL-SEED-001 only.

Uses Python's standard library and the seven explicit original edges. It does
not import LCL, change its target, quotient named assignments, or test p=5/6/7.
Run: python independent_seed_check.py --supplied supplied --out independent_seed_check.json
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from itertools import permutations
import json
from pathlib import Path
import platform
import time


LOW = ("s:1", "b:0:0", "l:1:0:0", "l:1:0:1")
HIGH_FREE = ("s:0", "b:1:0", "l:0:0:0")
PORT = "s:2"
EDGES = (
    ("s:0", "s:1"),
    ("s:0", "b:0:0"),
    ("b:0:0", "l:0:0:0"),
    ("s:1", "b:1:0"),
    ("b:1:0", "l:1:0:0"),
    ("b:1:0", "l:1:0:1"),
    ("s:1", "s:2"),
)
MAX_ASSIGNMENTS = 144
TIME_LIMIT_SECONDS = 2.0


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--supplied", type=Path, default=Path(__file__).parent / "supplied")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    supplied = args.supplied.resolve()
    inputs = {
        name: json.loads((supplied / name).read_text(encoding="utf-8-sig"))
        for name in (
            "examples/unequal_seed.json",
            "examples/unequal_seed_pins.json",
            "examples/unequal_seed_domains.json",
            "configs/unequal_seed_limits.json",
        )
    }
    assert inputs["examples/unequal_seed.json"] == {"profile": [[1], [2], []]}
    assert inputs["examples/unequal_seed_pins.json"] == {PORT: 4}
    expected_domains = {v: [0, 1, 2, 3] for v in LOW}
    expected_domains.update({v: [4, 5, 6, 7] for v in (*HIGH_FREE, PORT)})
    assert inputs["examples/unequal_seed_domains.json"] == expected_domains
    vertices = set(LOW) | set(HIGH_FREE) | {PORT}
    edge_set = {tuple(sorted(e)) for e in EDGES}
    assert len(vertices) == 8 and len(edge_set) == 7
    assert all((u in LOW) != (v in LOW) for u, v in EDGES)
    record_graphs = []
    for path in sorted((supplied / "runs").glob("*/record.json")):
        record = json.loads(path.read_text(encoding="utf-8-sig"))
        graph = record["original_graph"]
        assert graph["profile"] == [[1], [2], []]
        assert set(graph["vertices"]) == vertices and len(graph["vertices"]) == 8
        assert {tuple(sorted(e)) for e in graph["edges"]} == edge_set
        assert len(graph["edges"]) == 7
        assert record["expected_restrictions"] == {
            "pins": {PORT: 4}, "domains": expected_domains,
        }
        record_graphs.append({
            "path": path.relative_to(supplied).as_posix(),
            "reported_graph_digest": record["original_graph_digest"],
            "original_topology_and_restrictions_match": True,
        })
    assert len(record_graphs) == 2

    started = time.monotonic()
    rows = []
    witnesses = []
    case_rows = []
    identity_errors = []
    forced_one_errors = []
    reason = "EXHAUSTED"
    for low_values in permutations(range(4)):
        for high_values in permutations((5, 6, 7)):
            if len(rows) >= MAX_ASSIGNMENTS:
                reason = "ASSIGNMENT_LIMIT"
                break
            if time.monotonic() - started >= TIME_LIMIT_SECONDS:
                reason = "TIME_LIMIT"
                break
            labels = dict(zip(LOW, low_values))
            labels.update(zip(HIGH_FREE, high_values))
            labels[PORT] = 4
            assert sorted(labels.values()) == list(range(8))
            differences = [abs(labels[u] - labels[v]) for u, v in EDGES]
            a, b, c = (labels[v] for v in HIGH_FREE)
            y, x, u, v = (labels[w] for w in LOW)
            general_sum = a + 2 * b - x - 2 * y + 16
            if sum(differences) != general_sum:
                identity_errors.append(labels)
            one_edges = [i + 1 for i, d in enumerate(differences) if d == 1]
            if one_edges != ([7] if y == 3 else []):
                forced_one_errors.append(labels)
            graceful = sorted(differences) == list(range(1, 8))
            row = {"labels": labels, "edge_differences": differences,
                   "sum": sum(differences), "graceful": graceful}
            rows.append(row)
            if graceful:
                witnesses.append(labels)
            if y == 3 and sum(differences) == 28:
                case_rows.append({
                    "a": a, "b": b, "c": c, "x": x, "u": u, "v": v,
                    "edge_differences": differences,
                    "repeated_differences": {str(d): count for d, count in
                                             sorted(Counter(differences).items()) if count > 1},
                })
        if reason != "EXHAUSTED":
            break
    elapsed = time.monotonic() - started
    exhausted = len(rows) == MAX_ASSIGNMENTS
    if exhausted:
        assert len({tuple(r["labels"][w] for w in (*LOW, *HIGH_FREE, PORT)) for r in rows}) == 144
        assert len([r for r in rows if r["labels"]["s:1"] == 3]) == 36
        assert len(case_rows) == 6
        assert sorted({(r["a"], r["b"], r["x"]) for r in case_rows}) == [
            (5, 7, 1), (6, 7, 2), (7, 6, 1),
        ]
        assert not witnesses and not identity_errors and not forced_one_errors
        assert all(r["repeated_differences"].get("4", 0) >= 2 for r in case_rows)
    result = {
        "task": "B2-UNEQUAL-SEED-001 independent review replay",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": platform.python_version(),
                        "implementation": platform.python_implementation(),
                        "platform": platform.platform()},
        "script_sha256": sha256(Path(__file__).read_bytes()),
        "input_raw_file_sha256": {name: sha256((supplied / name).read_bytes()) for name in inputs},
        "original_edges_in_difference_order": EDGES,
        "domains": expected_domains,
        "pins": {PORT: 4},
        "record_topology_checks": record_graphs,
        "limits": {"max_assignments": MAX_ASSIGNMENTS, "max_seconds_cooperative": TIME_LIMIT_SECONDS,
                   "workers": 1, "max_output_bytes": 2_000_000},
        "exhausted": exhausted,
        "status": "EXHAUSTED_NO_SOLUTION" if exhausted and not witnesses else "INCOMPLETE",
        "reason": "EXHAUSTED" if exhausted else reason,
        "attempted_named_assignments": len(rows),
        "expected_named_assignments": MAX_ASSIGNMENTS,
        "count": len(witnesses) if exhausted else None,
        "witnesses": witnesses,
        "elapsed_seconds": elapsed,
        "general_sum_identity": "S = a + 2*b - x - 2*y + 16",
        "general_sum_identity_mismatches": len(identity_errors),
        "difference_one_forcing_mismatches": len(forced_one_errors),
        "y_equals_3_assignments": sum(r["labels"]["s:1"] == 3 for r in rows),
        "necessary_sum_case_assignments": case_rows,
        "all_named_assignments": rows,
        "scope": "The prescribed p=4 alpha seed only; no successor pin sweep; no universal claim.",
    }
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(encoded) > 2_000_000:
        raise RuntimeError("Review record exceeds declared output cap")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("xb") as handle:
        handle.write(encoded)
    print(json.dumps({k: result[k] for k in (
        "status", "exhausted", "attempted_named_assignments", "count",
        "y_equals_3_assignments", "general_sum_identity_mismatches",
        "difference_one_forcing_mismatches", "elapsed_seconds", "environment",
    )}, indent=2))


if __name__ == "__main__":
    main()
