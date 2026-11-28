"""Dormant future D231 entry point. Preparation authorizes parsing only."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from time import monotonic, process_time


class SharedLimit(RuntimeError):
    pass


class PlacementLimit(RuntimeError):
    pass


class AuditConflict(RuntimeError):
    pass


class Budget:
    def __init__(self, limits, cpu_start, wall_start):
        self.limits = limits
        self.cpu_start = cpu_start
        self.wall_start = wall_start
        self.nodes = Counter()
        self.attempts = Counter()
        self.stage = None
        self.entry_nodes = 0

    def poll(self, terminal=False):
        prefix = "max" if terminal else "work"
        if process_time() - self.cpu_start >= self.limits[prefix + "_cpu_seconds"]:
            raise SharedLimit("CPU")
        if monotonic() - self.wall_start >= self.limits[prefix + "_wall_seconds"]:
            raise SharedLimit("WALL")

    def start(self, stage):
        self.poll()
        self.stage = stage
        self.entry_nodes = self.nodes[stage]

    def charge(self):
        self.poll()
        if sum(self.nodes.values()) >= self.limits["max_all_nodes"]:
            raise SharedLimit("SHARED_NODES")
        count = self.nodes[self.stage] - self.entry_nodes
        if count >= self.limits[f"max_{self.stage}_nodes_per_placement"]:
            raise PlacementLimit(f"{self.stage.upper()}_PLACEMENT_NODES")
        self.nodes[self.stage] += 1

    def row_attempt(self, stage):
        self.poll()
        if stage != self.stage:
            raise RuntimeError("row phase mismatch")
        if sum(self.attempts.values()) >= self.limits["max_row_attempts"]:
            raise SharedLimit("ROW_ATTEMPTS")
        self.attempts[stage] += 1

    def snapshot(self):
        return {
            "cpu_seconds": process_time() - self.cpu_start,
            "wall_seconds": monotonic() - self.wall_start,
            "nodes": dict(self.nodes),
            "row_attempts": dict(self.attempts),
        }


class Evidence:
    def __init__(self, destination, budget, writer):
        self.destination = destination
        self.budget = budget
        self.writer = writer
        self.records = 0
        self.bytes = 0

    def write(self, name, data, terminal=False):
        self.budget.poll(terminal)
        limits = self.budget.limits
        encoded = json.dumps(
            data, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False,
        ).encode("utf-8") + b"\n"
        per_record = limits["max_record_bytes"]
        if len(encoded) > per_record:
            raise SharedLimit("RECORD_BYTES")
        reserve_records = 0 if terminal else 1
        reserve_bytes = 0 if terminal else per_record
        if self.records + 1 + reserve_records > limits["max_records"]:
            raise SharedLimit("RECORDS")
        if self.bytes + len(encoded) + reserve_bytes > limits["max_evidence_bytes"]:
            raise SharedLimit("EVIDENCE_BYTES")
        self.writer(self.destination / name, data, max_bytes=per_record)
        self.records += 1
        self.bytes += len(encoded)


def read_bytes(path, maximum):
    with path.open("rb") as stream:
        content = stream.read(maximum + 1)
    if len(content) > maximum:
        raise ValueError("input exceeds bound")
    return content


def directory(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("registered path leaves project")
    return path


def admit(root, here, args, raw_registration, budget):
    if (sys.implementation.name != "cpython" or sys.version_info[:2] not in ((3, 12), (3, 13))
            or not sys.dont_write_bytecode or sys.prefix == sys.base_prefix):
        raise ValueError("project-local CPython 3.12 or 3.13 with -B required")
    if not Path(sys.executable).resolve().is_relative_to(root):
        raise ValueError("interpreter is outside the project")
    approval = read_bytes(args.admission, 65536)
    if sha256(approval).hexdigest() != args.admission_sha256:
        raise ValueError("admission receipt SHA-256 mismatch")
    receipt = json.loads(approval)
    if receipt.get("decision") != "AUTHORIZE_D231_EXECUTION":
        raise ValueError("separate D231 execution receipt required")
    if receipt.get("run_id") != budget.limits["run_id"]:
        raise ValueError("wrong authorized run")
    for name in ("director_review", "owner_authorization"):
        if type(receipt.get(name)) is not str or not receipt[name].strip():
            raise ValueError("missing approval identity")
    for name in ("verified_checkpoint", "execution_checkout"):
        if type(receipt.get(name)) is not str or re.fullmatch("[0-9a-f]{40}", receipt[name]) is None:
            raise ValueError("missing exact Git identity in admission")
    manifest_raw = read_bytes(here / "source_manifest.json", 65536)
    manifest_sha = sha256(manifest_raw).hexdigest()
    if manifest_sha != receipt.get("source_manifest_sha256"):
        raise ValueError("receipt does not name this source manifest")
    bindings = json.loads(manifest_raw)["sha256"]
    registered_path = (here / "registration.json").relative_to(root).as_posix()
    if sha256(raw_registration).hexdigest() != bindings.get(registered_path):
        raise ValueError("registration does not match its binding")
    for relative, expected in bindings.items():
        budget.poll()
        if sha256(read_bytes(directory(root, relative), 1024 * 1024)).hexdigest() != expected:
            raise ValueError(f"binding mismatch for {relative}")
    output = directory(root, budget.limits["output"])
    if output.exists() or directory(root, budget.limits["archive"]).exists():
        raise FileExistsError("registered output or archive already exists")
    return output, receipt, manifest_sha


def process_placement(key_index, placement_index, quotas, roles, evidence, budget):
    from research.d229_homogeneous_pair_kernel.search import solve_problem
    from .audit import exhaust, reconstruct
    from .model import problem

    identity = {"placement": quotas, "aggregate_index": key_index, "placement_index": placement_index}
    base = f"key-{key_index:02d}-placement-{placement_index:02d}"
    budget.start("primary")
    try:
        rows = solve_problem(problem(quotas, budget), budget)
    except PlacementLimit as error:
        evidence.write(base + "-primary.json", {**identity, "status": "INCOMPLETE", "reason": str(error)})
        return "UNRESOLVED"
    status = "WITNESS_PENDING_AUDIT" if rows is not None else "EXHAUSTION_PENDING_AUDIT"
    record = {**identity, "status": status, "counters": budget.snapshot()}
    if rows is not None:
        record["rows"] = rows
    evidence.write(base + "-primary.json", record)

    budget.start("audit")
    if rows is not None:
        try:
            certificate = reconstruct(quotas, rows, roles, budget.poll)
        except (ValueError, TypeError, KeyError) as error:
            evidence.write(base + "-audit.json", {**identity, "status": "REJECTED", "reason": str(error)})
            raise AuditConflict("positive certificate rejected") from error
        evidence.write(base + "-audit.json", {
            **identity, "status": "VERIFIED_POSITIVE", "certificate": certificate,
            "counters": budget.snapshot(),
        })
        return "VERIFIED_POSITIVE"

    try:
        contrary = exhaust(quotas, budget)
    except PlacementLimit as error:
        evidence.write(base + "-audit.json", {**identity, "status": "INCOMPLETE", "reason": str(error)})
        return "UNRESOLVED"
    if contrary is not None:
        # Preserve the original contradiction even if reconstruction itself fails.
        evidence.write(base + "-audit.json", {**identity, "status": "CONTRADICTION", "rows": contrary})
        try:
            reconstruct(quotas, contrary, roles, budget.poll)
        except (ValueError, TypeError, KeyError) as error:
            raise AuditConflict("contrary witness failed reconstruction") from error
        raise AuditConflict("primary and independent traversals disagree")
    evidence.write(base + "-audit.json", {
        **identity, "status": "CORROBORATED_EXCLUSION", "counters": budget.snapshot(),
    })
    return "CORROBORATED_EXCLUSION"


def execute(limits, evidence, budget):
    from .model import aggregates, placements

    keys = tuple((key, placements(key)) for key in aggregates())
    if (len(keys) != limits["aggregate_keys"]
            or sum(len(order) for _, order in keys) != limits["ordered_placements"]
            or max(2 * sum(key) for key, _ in keys) != limits["max_packet_rows"]):
        raise ValueError("aggregate registration count or size mismatch")
    completed = Counter()
    reason = None
    try:
        for index, (key, order) in enumerate(keys):
            statuses = []
            positive = None
            for position, quotas in enumerate(order):
                budget.poll()
                status = process_placement(index, position, quotas, limits["roles"], evidence, budget)
                statuses.append(status)
                if status == "VERIFIED_POSITIVE":
                    positive = position
                    break
            if positive is not None:
                disposition = "COVERED"
            elif all(status == "CORROBORATED_EXCLUSION" for status in statuses):
                disposition = "ARCHITECTURE_EXCLUDED"
            else:
                disposition = "UNRESOLVED"
            evidence.write(f"key-{index:02d}.json", {
                "key": key, "placements": order, "completed_statuses": statuses,
                "disposition": disposition, "positive_placement": positive,
            })
            completed[disposition] += 1
    except (SharedLimit, AuditConflict, KeyboardInterrupt) as error:
        reason = str(error) or type(error).__name__
    return completed, reason


def main():
    cpu_start, wall_start = process_time(), monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--admission", required=True, type=Path)
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    here = Path(__file__).resolve().parent
    if here != root / "research" / "d231_unequal_pair_kernel":
        raise ValueError("run from LCL root")
    raw_registration = read_bytes(here / "registration.json", 65536)
    limits = json.loads(raw_registration)
    budget = Budget(limits, cpu_start, wall_start)
    output, receipt, manifest_sha = admit(root, here, args, raw_registration, budget)

    from lcl.records import atomic_json

    budget.poll()
    output.mkdir(exist_ok=False)
    evidence = Evidence(output, budget, atomic_json)
    evidence.write("session.json", {
        "run_id": limits["run_id"], "source_manifest_sha256": manifest_sha,
        "registration_sha256": sha256(raw_registration).hexdigest(),
        "admission_sha256": args.admission_sha256, "admission": receipt,
        "python": sys.version, "interpreter": str(Path(sys.executable).relative_to(root)),
    })
    completed, reason = execute(limits, evidence, budget)
    remaining = limits["aggregate_keys"] - sum(completed.values())
    evidence.write("summary.json", {
        "completed_by_disposition": dict(completed), "unfinished_aggregates": remaining,
        "complete_positive_coverage": completed["COVERED"] == limits["aggregate_keys"],
        "stop_reason": reason, "counters_before_summary": budget.snapshot(),
        "evidence_before_summary": {"records": evidence.records, "bytes": evidence.bytes},
    }, terminal=True)
    return int(reason is not None)


if __name__ == "__main__":
    sys.exit(main())
