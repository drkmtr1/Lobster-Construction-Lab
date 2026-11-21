"""Reproduce the bounded release checks in a NEW output directory.

Uses the invoking Python. Each subprocess has a 30 second validation stop;
mathematical engine limits remain their separate declared budgets.
"""
from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lcl.engines import dependency_versions
from lcl.model import build_graph, branched_prefix_profile
from lcl.oracle import permutation_oracle
from lcl.records import atomic_json, environment, save_single, source_inventory
from lcl.states import b2_restrictions


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output")
    args = p.parse_args()
    output = Path(args.output) if args.output else ROOT / "runs" / datetime.now(timezone.utc).strftime("validation-%Y%m%dT%H%M%SZ")
    output.mkdir(parents=True, exist_ok=False)
    commands = [
        ("unit_tests", ["-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("demo", ["-m", "lcl", "demo", "--out", str(output / "demo")]),
        ("composed", ["-m", "lcl", "construct", "examples/two_section_padded.json", "--out", str(output / "composed")]),
        ("balanced", ["-m", "lcl", "construct", "examples/two_section_balanced.json", "--out", str(output / "balanced")]),
        ("allocation", ["-m", "lcl", "allocate", "examples/r226.json", "--out", str(output / "allocation")]),
        ("p4_dfs", ["-m", "lcl", "solve", "examples/p4.json", "--engine", "dfs", "--count", "--out", str(output / "p4_dfs")]),
        ("p4_dp", ["-m", "lcl", "solve", "examples/p4.json", "--engine", "dp", "--out", str(output / "p4_dp")]),
        ("p4_oracle", ["-m", "lcl", "solve", "examples/p4.json", "--engine", "oracle", "--out", str(output / "p4_oracle")]),
        ("p4_restricted", ["-m", "lcl", "solve", "examples/p4.json", "--pins", "examples/p4_bad_core_pins.json", "--count", "--out", str(output / "p4_restricted")]),
        ("p6_dfs", ["-m", "lcl", "solve", "examples/p6.json", "--count", "--out", str(output / "p6_dfs")]),
        ("spider_dfs", ["-m", "lcl", "solve", "examples/spider_221.json", "--count", "--out", str(output / "spider_dfs")]),
        ("pilot", ["-m", "lcl", "pilot", "configs/b2_pilot.json", "--out", str(output / "pilot")]),
    ]
    if dependency_versions()["z3-solver"]:
        commands.append(("p4_z3", ["-m", "lcl", "solve", "examples/p4.json", "--engine", "z3", "--out", str(output / "p4_z3")]))
    commands.append(("diagnostics", ["-m", "lcl", "diagnostics"]))
    events = []
    for name, argv in commands:
        start = time.monotonic()
        try:
            process = subprocess.run([sys.executable] + argv, cwd=ROOT, text=True,
                                     capture_output=True, timeout=30)
            (output / (name + ".log")).write_text(process.stdout + process.stderr, encoding="utf-8")
            event = {"name": name, "argv": [sys.executable] + argv, "returncode": process.returncode,
                     "elapsed_seconds": time.monotonic()-start, "log": name + ".log"}
        except subprocess.TimeoutExpired:
            event = {"name": name, "argv": [sys.executable] + argv, "returncode": None,
                     "elapsed_seconds": time.monotonic()-start, "status": "VALIDATION_TIMEOUT"}
        events.append(event)
        print(json.dumps(event), flush=True)
        if event["returncode"] != 0:
            atomic_json(output / "summary.json", {"status": "FAILED", "events": events,
                        "environment": environment(), "source": source_inventory(ROOT)})
            return 2
    # Independent direct enumeration resolves the main pilot control's finite
    # negative without trusting DFS pruning. This is <=8!=40320 permutations.
    graph = build_graph(branched_prefix_profile(1, 1, 0, 0, 1))
    pins, domains = b2_restrictions(graph, 1, 1, "above")
    result = permutation_oracle(graph, pins=pins, domains=domains,
                                max_vertices=8, max_permutations=40320, time_limit=5.0)
    save_single(ROOT, output / "b2_negative_oracle", graph, result,
                {"purpose": "independent fixed-interval control", "pins": pins, "domains": domains,
                 "max_vertices": 8, "max_permutations": 40320, "time_limit": 5.0},
                expected_pins=pins, expected_domains=domains)
    checks = {"b2_negative_oracle_exact_zero": result.get("exhausted") is True and result.get("count") == 0}
    for name, expected in (("p4_dfs",4),("p4_dp",4),("p4_oracle",4),("p4_restricted",0),
                           ("p6_dfs",24),("spider_dfs",16)):
        record = json.loads((output / name / "record.json").read_text())
        checks[name + "_exact_count"] = record["result"].get("count") == expected
    for name in ("demo", "composed", "balanced", "allocation"):
        record = json.loads((output / name / "record.json").read_text())
        checks[name + "_verified"] = (record["classification"] != "QUARANTINED"
                                       and bool(record["certificate"] and record["certificate"]["valid"]))
    status = "PASSED" if all(checks.values()) else "FAILED"
    atomic_json(output / "summary.json", {"status": status, "events": events, "semantic_checks": checks,
                "environment": environment(), "source": source_inventory(ROOT),
                "windows_execution": False, "lean_execution": False,
                "scope": "bounded software and finite evidence validation; no new universal theorem"})
    print(json.dumps({"status": status, "output": str(output.resolve()), "semantic_checks": checks}))
    return 0 if status == "PASSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
