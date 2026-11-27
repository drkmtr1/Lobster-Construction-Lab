"""Conditional future entry. The current task authorizes parse-only review."""

import argparse
from collections import Counter
from dataclasses import asdict
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from time import monotonic, process_time


class LimitReached(RuntimeError):
    pass


class Budget:
    def __init__(self, registration, cpu_started, wall_started):
        self.limits = registration
        self.cpu_started = cpu_started
        self.wall_started = wall_started
        self.nodes = 0
        self.key_started = 0
        self.key_limit = None

    def mark_key(self, limit):
        self.key_started = self.nodes
        self.key_limit = limit

    def poll(self):
        if process_time() - self.cpu_started >= self.limits["max_cpu_seconds"]:
            raise LimitReached("CPU")
        if monotonic() - self.wall_started >= self.limits["max_wall_seconds"]:
            raise LimitReached("WALL")

    def charge(self):
        self.poll()
        if self.nodes >= self.limits["max_all_nodes"]:
            raise LimitReached("SHARED_NODES")
        if self.key_limit is not None and self.nodes - self.key_started >= self.key_limit:
            raise LimitReached("PRIMARY_KEY_NODES")
        self.nodes += 1

    def receipt(self):
        return {
            "process_cpu_seconds": process_time() - self.cpu_started,
            "foreground_wall_seconds": monotonic() - self.wall_started,
            "charged_nodes": self.nodes,
        }


class Evidence:
    def __init__(self, path, registration, budget, atomic_json):
        self.path = path
        self.budget = budget
        self.atomic_json = atomic_json
        self.registration = registration
        self.count = 0
        self.bytes = 0

    def write(self, name, value):
        self.budget.poll()
        encoded = json.dumps(
            value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False,
        ).encode("utf-8") + b"\n"
        if len(encoded) > self.registration["max_record_bytes"]:
            raise LimitReached("RECORD_BYTES")
        if self.count == self.registration["max_records"]:
            raise LimitReached("RECORDS")
        if self.bytes + len(encoded) > self.registration["max_evidence_bytes"]:
            raise LimitReached("EVIDENCE_BYTES")
        # The immutable project writer has one temporary file and renames it
        # into a previously vacant destination. Check before the first write.
        self.atomic_json(
            self.path / name, value, max_bytes=self.registration["max_record_bytes"],
        )
        self.count += 1
        self.bytes += len(encoded)


def bounded_bytes(path, max_size):
    with path.open("rb") as stream:
        data = stream.read(max_size + 1)
    if len(data) > max_size:
        raise ValueError("registration or admission input exceeds byte bound")
    return data


def hash_source(root, relative):
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError("source path escapes the project")
    return sha256(bounded_bytes(target, 1024 * 1024)).hexdigest()


def admit(root, here, approval, expected_hash, registration_sha, budget):
    approved_bytes = bounded_bytes(approval, 65536)
    if sha256(approved_bytes).hexdigest() != expected_hash:
        raise ValueError("later admission receipt hash mismatch")
    receipt = json.loads(approved_bytes)
    if receipt.get("decision") != "AUTHORIZE_D229_EXECUTION":
        raise ValueError("separate execution receipt required")
    if receipt.get("run_id") != budget.limits["run_id"]:
        raise ValueError("authorization for another registration")
    for field in ("director_review", "owner_authorization", "verified_checkpoint"):
        if type(receipt.get(field)) is not str or not receipt[field].strip():
            raise ValueError("admission identity field missing")
    manifest_file = here / "source_manifest.json"
    manifest_bytes = bounded_bytes(manifest_file, 65536)
    manifest_sha = sha256(manifest_bytes).hexdigest()
    if manifest_sha != receipt.get("source_manifest_sha256"):
        raise ValueError("approval does not name this exact source manifest")
    manifest = json.loads(manifest_bytes)
    bound_path = (here / "registration.json").relative_to(root).as_posix()
    if manifest["sha256"].get(bound_path) != registration_sha:
        raise ValueError("loaded registration differs from the binding")
    for relative, digest in manifest["sha256"].items():
        budget.poll()
        if hash_source(root, relative) != digest:
            raise ValueError(f"bound source changed: {relative}")
    output = root / budget.limits["output"]
    if output.exists() or (root / budget.limits["archive"]).exists():
        raise FileExistsError("registered output or archive already exists")
    return output, receipt, manifest_sha


def named_digest(profile, labels, poll):
    from lcl.records import digest
    from .audit import verify_named

    original, fold = verify_named(profile, labels, poll)
    return {
        "original": digest({"profile": profile, "edges": original, "labels": labels}),
        "fold": digest({"profile": profile, "edges": fold, "labels": labels}),
    }


def check_controls(data, budget):
    from .audit import verify_rows
    from .coverage import emit_labels, transport
    from .model import CapKey, CoreKey
    from .retained import known_cap, known_core, proved_cap_negative

    proofs = []
    for control in data:
        profile = control["profile"]
        assignments = {
            f"b:{i}:{a}": (text[0], int(text[1:]))
            for i, section in enumerate(control["roles"])
            for a, text in enumerate(section)
        }
        p, a, pairs = control["cap"]
        for beta in control["positive_betas"]:
            core_key = CoreKey(6, 0, (1, 1, 1), beta)
            cap_key = CapKey(p, a, tuple(pairs), beta)
            core = known_core(core_key)
            cap = known_cap(cap_key)
            verify_rows(core_key, core, budget.poll)
            verify_rows(cap_key, cap, budget.poll)
            rows = transport(core, cap, beta)
            labels = emit_labels(10, rows, assignments)
            proof = named_digest(profile, labels, budget.poll)
            reversed_labels = {}
            for name, value in labels.items():
                parts = name.split(":")
                parts[1] = str(3 - int(parts[1]))
                reversed_labels[":".join(parts)] = value
            proofs.append({
                "id": control["id"], "beta": beta,
                "labels": labels, "hashes": proof,
                "reversed_hashes": named_digest(profile[::-1], reversed_labels, budget.poll),
            })
        if "proof_negative_beta" in control:
            key = CapKey(p, a, tuple(pairs), control["proof_negative_beta"])
            if not proved_cap_negative(key):
                raise ValueError("control does not match the reviewed cap obstruction")
    return proofs


def collect_relations(evidence, budget, keys):
    from .audit import independent_exhaustion, verify_rows
    from .model import CoreKey
    from .retained import known_cap, known_core, proved_cap_negative
    from .search import primary

    states = {}
    witnesses = {}
    unknown = []
    pending_audit = []

    def positive(number, key, rows, source):
        placement = verify_rows(key, rows, budget.poll)
        evidence.write(f"key-{number:04d}.json", {
            "key": asdict(key), "status": "POSITIVE", "source": source,
            "rows": rows, "placement": placement, "independent_endpoint_audit": "PASS",
            **budget.receipt(),
        })
        states[key] = "POSITIVE"
        witnesses[key] = rows

    for number, key in enumerate(keys):
        budget.poll()
        rows = known_core(key) if isinstance(key, CoreKey) else known_cap(key)
        if rows is not None:
            positive(number, key, rows, "retained_formula")
        elif proved_cap_negative(key):
            evidence.write(f"key-{number:04d}.json", {
                "key": asdict(key), "status": "NEGATIVE",
                "source": "reviewed cap-X/S1 moment proof",
                **budget.receipt(),
            })
            states[key] = "NEGATIVE"
        else:
            unknown.append((number, key))

    stop = None
    for number, key in unknown:
        limit_name = "max_core_primary_nodes" if isinstance(key, CoreKey) else "max_cap_primary_nodes"
        budget.mark_key(budget.limits[limit_name])
        try:
            result = primary(key, budget)
        except LimitReached as error:
            evidence.write(f"key-{number:04d}.json", {
                "key": asdict(key), "status": "INCOMPLETE", "reason": str(error),
                "charged_in_key": budget.nodes - budget.key_started, **budget.receipt(),
            })
            if str(error) != "PRIMARY_KEY_NODES":
                stop = str(error)
                break
            continue
        if result is not None:
            positive(number, key, result, "primary_with_independent_endpoint_audit")
        else:
            evidence.write(f"key-{number:04d}.json", {
                "key": asdict(key), "status": "PRIMARY_EXHAUSTED_PENDING_AUDIT",
                "charged_in_key": budget.nodes - budget.key_started, **budget.receipt(),
            })
            pending_audit.append((number, key))

    if stop is None:
        for number, key in pending_audit:
            budget.mark_key(None)
            try:
                contrary = independent_exhaustion(key, budget)
            except LimitReached as error:
                evidence.write(f"audit-{number:04d}.json", {
                    "key": asdict(key), "status": "INCOMPLETE", "reason": str(error),
                    "charged_in_audit": budget.nodes - budget.key_started, **budget.receipt(),
                })
                stop = str(error)
                break
            if contrary is not None:
                verify_rows(key, contrary, budget.poll)
                evidence.write(f"audit-{number:04d}.json", {
                    "key": asdict(key), "status": "INCONSISTENT", "rows": contrary,
                    **budget.receipt(),
                })
                raise ValueError("independent traversal contradicted primary exhaustion")
            evidence.write(f"audit-{number:04d}.json", {
                "key": asdict(key), "status": "NEGATIVE", "source": "double exhaustion",
                "charged_in_audit": budget.nodes - budget.key_started, **budget.receipt(),
            })
            states[key] = "NEGATIVE"

    return states, witnesses, stop


def audit_coverage(evidence, budget, relations, witnesses, key_ids):
    from .coverage import decide, emit_labels, physical_keys, profile_for, role_assignment, transport

    counts = Counter()
    batch = []
    number = 0

    def persist_batch():
        nonlocal number
        evidence.write(f"coverage-{number:04d}.json", batch)
        number += 1
        batch.clear()

    for key in physical_keys():
        budget.poll()
        disposition, join = decide(key, relations, budget.poll)
        record = {"type": asdict(key), "status": disposition}
        if join is not None:
            rows = transport(witnesses[join.core], witnesses[join.cap], join.core.beta)
            assignments = role_assignment(key, rows, join)
            labels = emit_labels(key.h, rows, assignments)
            record.update({
                "core": key_ids[join.core], "cap": key_ids[join.cap],
                "left_triple_pairs": join.left_triple_pairs,
                "hashes": named_digest(profile_for(key), labels, budget.poll),
            })
        counts[disposition] += 1
        batch.append(record)
        if len(batch) == budget.limits["coverage_batch"]:
            persist_batch()
    if batch:
        persist_batch()
    if sum(counts.values()) != budget.limits["max_physical_keys"]:
        raise ValueError("coverage key registration mismatch")
    return dict(counts)


def main():
    cpu_started, wall_started = process_time(), monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--admission", required=True, type=Path)
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    registration_bytes = bounded_bytes(here / "registration.json", 65536)
    registration = json.loads(registration_bytes)
    if Path.cwd().resolve() != root or sys.implementation.name != "cpython":
        raise ValueError("use the declared project root and CPython")
    if sys.version_info.major != 3 or sys.version_info.minor not in registration["python_minors"]:
        raise ValueError("Python minor is outside the reviewed registration")
    if not sys.dont_write_bytecode:
        raise ValueError("run with -B")
    budget = Budget(registration, cpu_started, wall_started)
    output, receipt, manifest_sha = admit(
        root, here, args.admission.resolve(), args.admission_sha256,
        sha256(registration_bytes).hexdigest(), budget,
    )
    from lcl.records import atomic_json
    from .model import cap_keys, core_keys

    cores, caps = tuple(core_keys()), tuple(cap_keys())
    if (len(cores) != registration["max_core_keys"]
            or len(caps) != registration["max_cap_keys"]
            or sum(comb(key.h - 2, key.triples) for key in cores)
            != registration["max_core_placements"]):
        raise ValueError("numeric key registration mismatch")
    output.mkdir(parents=True, exist_ok=False)
    evidence = Evidence(output, registration, budget, atomic_json)
    evidence.write("session.json", {
        "registration": registration, "approval": receipt,
        "approval_sha256": args.admission_sha256, "source_manifest_sha256": manifest_sha,
        "python": sys.version, "executable": sys.executable,
    })
    try:
        controls = check_controls(
            json.loads(bounded_bytes(here / "control_originals.json", 65536)), budget,
        )
        evidence.write("controls.json", controls)
        keys = caps + cores
        relations, witnesses, stop = collect_relations(evidence, budget, keys)
        counts = audit_coverage(evidence, budget, relations, witnesses, {
            key: f"key-{number:04d}.json" for number, key in enumerate(keys)
        })
        evidence.write("summary.json", {
            "numeric_known": dict(Counter(relations.values())),
            "numeric_unresolved": len(keys) - len(relations),
            "physical_counts": counts, "search_stopped": stop,
            "records_before_summary": evidence.count,
            "bytes_before_summary": evidence.bytes,
            **budget.receipt(),
        })
    except LimitReached as error:
        # Do not overrun a limit merely to emit a late terminal record. Missing
        # records remain unresolved and completed records are immutable.
        print(f"INCOMPLETE: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
