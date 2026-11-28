"""Dormant one-shot D233 entry point. Preparation permits static parsing only."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from time import monotonic, process_time

from research.d231_unequal_pair_kernel.driver import (
    AuditConflict, Budget, Evidence, PlacementLimit, SharedLimit, directory, read_bytes,
)


def admit(root, here, args, registration_raw, budget):
    if (sys.implementation.name != "cpython" or sys.version_info[:2] not in ((3, 12), (3, 13))
            or not sys.dont_write_bytecode or sys.prefix == sys.base_prefix
            or not Path(sys.executable).resolve().is_relative_to(root)):
        raise ValueError("project-local CPython 3.12 or 3.13 with -B required")
    raw = read_bytes(args.admission, 65536)
    if sha256(raw).hexdigest() != args.admission_sha256:
        raise ValueError("admission receipt SHA-256 mismatch")
    receipt = json.loads(raw)
    if (receipt.get("decision") != "AUTHORIZE_D233_EXECUTION"
            or receipt.get("run_id") != budget.limits["run_id"]):
        raise ValueError("separate D233 execution authorization required")
    for field in ("director_review", "owner_authorization", "qualified_supervision"):
        if type(receipt.get(field)) is not str or not receipt[field].strip():
            raise ValueError("missing approval or supervision identity")
    for field in ("verified_checkpoint", "execution_checkout"):
        if type(receipt.get(field)) is not str or re.fullmatch("[0-9a-f]{40}", receipt[field]) is None:
            raise ValueError("missing exact checkout identity")
    manifest = read_bytes(here / "source_manifest.json", 65536)
    manifest_sha = sha256(manifest).hexdigest()
    registration_sha = sha256(registration_raw).hexdigest()
    if (receipt.get("source_manifest_sha256") != manifest_sha
            or receipt.get("registration_sha256") != registration_sha):
        raise ValueError("receipt does not bind manifest and registration")
    bindings = json.loads(manifest)["sha256"]
    registration = (here / "registration.json").relative_to(root).as_posix()
    if bindings.get(registration) != registration_sha:
        raise ValueError("manifest does not bind this registration")
    for relative, expected in bindings.items():
        budget.poll()
        if sha256(read_bytes(directory(root, relative), 1024 * 1024)).hexdigest() != expected:
            raise ValueError(f"binding mismatch: {relative}")
    output = directory(root, budget.limits["output"])
    archive = directory(root, budget.limits["archive"])
    if output.exists() or archive.exists() or output == archive:
        raise FileExistsError("output and archive must be distinct and vacant")
    return output, receipt, manifest_sha


def register(limits):
    from .registry import aggregates, placements

    groups = tuple((key, placements(key)) for key in aggregates(limits["aggregate_rule"]))
    if (len(groups) != limits["aggregate_keys"]
            or sum(len(orders) for _, orders in groups) != limits["ordered_placements"]
            or max(4 + sum(key) for key, _ in groups) != limits["max_packet_rows"]
            or any(not orders for _, orders in groups)):
        raise ValueError("exact registered domain mismatch")
    return groups


def process(key_index, index, placement, evidence, budget):
    from research.d229_homogeneous_pair_kernel.search import solve_problem
    from .audit import exhaust, reconstruct
    from .model import problem

    base = f"key-{key_index:03d}-placement-{index:03d}"
    identity = {"key_index": key_index, "placement_index": index, "placement": placement}
    budget.start("primary")
    try:
        rows = solve_problem(problem(placement, budget), budget)
    except PlacementLimit as error:
        evidence.write(base + "-primary.json", {**identity, "status": "INCOMPLETE", "reason": str(error)})
        return "UNRESOLVED"
    record = {**identity, "counters": budget.snapshot()}
    if rows is None:
        record["status"] = "EXHAUSTION_PENDING_AUDIT"
    else:
        record.update(status="WITNESS_PENDING_AUDIT", rows=rows)
    evidence.write(base + "-primary.json", record)

    budget.start("audit")
    if rows is not None:
        try:
            certificate = reconstruct(placement, rows, budget.poll)
        except (ValueError, TypeError, KeyError) as error:
            evidence.write(base + "-audit.json", {**identity, "status": "REJECTED", "reason": str(error)})
            raise AuditConflict("positive certificate rejected") from error
        evidence.write(base + "-audit.json", {
            **identity, "status": "VERIFIED_POSITIVE", "certificate": certificate,
            "counters": budget.snapshot(),
        })
        return "VERIFIED_POSITIVE"

    try:
        contrary = exhaust(placement, budget)
    except PlacementLimit as error:
        evidence.write(base + "-audit.json", {**identity, "status": "INCOMPLETE", "reason": str(error)})
        return "UNRESOLVED"
    if contrary is not None:
        evidence.write(base + "-audit.json", {**identity, "status": "CONTRADICTION", "rows": contrary})
        raise AuditConflict("primary and independent traversals disagree")
    evidence.write(base + "-audit.json", {
        **identity, "status": "CORROBORATED_EXCLUSION", "counters": budget.snapshot(),
    })
    return "CORROBORATED_EXCLUSION"


def execute(groups, evidence, budget):
    status_lists = [[] for _ in groups]
    completed = Counter()
    finished = set()
    stop = None
    try:
        for index in range(max(len(orders) for _, orders in groups)):
            for key_index, (key, orders) in enumerate(groups):
                if key_index in finished or index >= len(orders):
                    continue
                budget.poll()
                statuses = status_lists[key_index]
                result = process(key_index, index, orders[index], evidence, budget)
                statuses.append(result)
                if result == "VERIFIED_POSITIVE":
                    disposition = "COVERED"
                elif len(statuses) < len(orders):
                    continue
                elif all(s == "CORROBORATED_EXCLUSION" for s in statuses):
                    disposition = "ARCHITECTURE_EXCLUDED"
                else:
                    disposition = "UNRESOLVED"
                evidence.write(f"key-{key_index:03d}.json", {
                    "aggregate": key, "placement_count": len(orders), "statuses": statuses,
                    "disposition": disposition,
                    "positive_placement_index": index if disposition == "COVERED" else None,
                })
                finished.add(key_index)
                completed[disposition] += 1
    except (AuditConflict, SharedLimit, KeyboardInterrupt) as error:
        stop = str(error) or type(error).__name__
    return completed, stop


def main():
    cpu_start, wall_start = process_time(), monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--admission", required=True, type=Path)
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    here = Path(__file__).resolve().parent
    if here != root / "research" / "d233_unit_partner_kernel":
        raise ValueError("run from LCL root")
    raw = read_bytes(here / "registration.json", 65536)
    limits = json.loads(raw)
    if limits["schema"] != "lcl.d233.unit-partner-return-kernel.registration.v1" or limits["workers"] != 1:
        raise ValueError("wrong frozen registration")
    budget = Budget(limits, cpu_start, wall_start)
    output, receipt, manifest_sha = admit(root, here, args, raw, budget)
    groups = register(limits)

    from lcl.records import atomic_json

    budget.poll()
    output.mkdir(exist_ok=False)
    evidence = Evidence(output, budget, atomic_json)
    evidence.write("session.json", {
        "run_id": limits["run_id"], "source_manifest_sha256": manifest_sha,
        "registration_sha256": sha256(raw).hexdigest(),
        "admission_sha256": args.admission_sha256, "admission": receipt,
        "python": sys.version, "interpreter": str(Path(sys.executable).relative_to(root)),
    })
    completed, stop = execute(groups, evidence, budget)
    evidence.write("summary.json", {
        "completed_by_disposition": dict(completed),
        "unfinished_aggregates": limits["aggregate_keys"] - sum(completed.values()),
        "complete_positive_coverage": completed["COVERED"] == limits["aggregate_keys"],
        "stop_reason": stop, "counters_before_summary": budget.snapshot(),
        "evidence_before_summary": {"records": evidence.records, "bytes": evidence.bytes},
    }, terminal=True)
    return int(stop is not None)


if __name__ == "__main__":
    sys.exit(main())
