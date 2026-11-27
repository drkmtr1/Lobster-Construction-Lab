"""D204 receipt, framing and phase rules with no native or scientific imports."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import struct
import threading

FRAME_MAX = 1 << 20
TERMINAL_RESERVE = 65536
COUNTERS = ("geometry_entries", "placement_attempts", "allocation_states",
            "pair_trials", "fixed_edge_checks")

class Rejected(RuntimeError):
    pass

def need(condition, message):
    if not condition:
        raise Rejected(message)

def binding(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")

def decode(data):
    def unique(keys):
        record = {}
        for key, value in keys:
            need(key not in record, "DUPLICATE_JSON_KEY")
            record[key] = value
        return record
    def reject_constant(value):
        raise Rejected("NONFINITE_JSON_NUMBER")
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=unique,
                          parse_constant=reject_constant)
    except (UnicodeError, ValueError, RecursionError) as error:
        raise Rejected("INVALID_JSON") from error

def exact_int(value, low, high):
    return type(value) is int and low <= value <= high

def finite(value, maximum):
    return type(value) in (int, float) and 0 <= value <= maximum and math.isfinite(value)

def read_exact(read, length, eof=False):
    need(0 <= length <= FRAME_MAX, "FRAME_BOUND")
    data = bytearray()
    while len(data) < length:
        part = read(min(4096, length - len(data)))
        need(len(part) <= length - len(data), "READ_OVERFLOW")
        if not part:
            if eof and not data:
                return None
            raise Rejected("IPC_TRUNCATED")
        data.extend(part)
    return bytes(data)

def frame(read):
    size = read_exact(read, 4, eof=True)
    if size is None:
        return None
    size = struct.unpack(">I", size)[0]
    need(1 <= size <= FRAME_MAX, "IPC_FRAME_LIMIT")
    blob = read_exact(read, size)
    return blob[:1], blob[1:]

def packet(kind, data):
    need(type(kind) is bytes and len(kind) == 1 and 1+len(data) <= FRAME_MAX, "IPC_FRAME_LIMIT")
    return struct.pack(">I", 1 + len(data)) + kind + data

class Ledger:
    """One pre-charge ledger per matrix or scientific run, with a terminal reserve."""
    def __init__(self, root, cap, reserve=TERMINAL_RESERVE, sync=os.fsync):
        need(cap >= reserve > 0, "LEDGER_CONFIGURATION")
        self.root, self.cap, self.reserve, self.sync = Path(root), cap, reserve, sync
        self.charged, self.records = 0, {}
        self.published_bytes = 0
        self.lock = threading.Lock()

    def save_all(self, entries, terminal=False, local_cap=None):
        if terminal:
            need(len(entries) == 1 and entries[0][0] == "terminal.json", "TERMINAL_SLOT")
        with self.lock:
            names = [name for name, _ in entries]
            need(len(set(names)) == len(names)
                 and all(re.fullmatch(r"[a-z0-9_-]+[.](json|bin)", name)
                         for name in names), "EVIDENCE_NAME")
            need(all(name not in self.records for name in names), "DUPLICATE_EVIDENCE")
            charge = sum(len(data) for _, data in entries)
            maximum = self.cap if local_cap is None else min(self.cap, local_cap)
            available = maximum - self.charged - (0 if terminal else self.reserve)
            need(charge <= available and (not terminal or charge <= self.reserve), "EVIDENCE_LIMIT")
            # Charge the planned bytes even when one artifact persists only partially.
            self.charged += charge
            for name, data in entries:
                with (self.root / name).open("xb") as file:
                    need(file.write(data) == len(data), "SHORT_EVIDENCE_WRITE")
                    file.flush()
                    self.sync(file.fileno())
                self.records[name] = binding(data)

    def save(self, name, data, **kwargs):
        self.save_all([(name, data)], **kwargs)

    def verify(self):
        actual = {p.name for p in self.root.iterdir() if p.is_file()}
        need(actual == set(self.records), "EVIDENCE_FILE_SET")
        for name, info in self.records.items():
            path = self.root / name
            need(path.stat().st_size == info["bytes"]
                 and binding(path.read_bytes()) == info, "EVIDENCE_RECONCILIATION")
        need(sum(info["bytes"] for info in self.records.values()) <= self.charged <= self.cap,
             "EVIDENCE_RECONCILIATION")

def reserve(path):
    # This directory is never removed or reused by the controller, including after failure.
    try:
        path.mkdir(exist_ok=False)
    except FileExistsError as error:
        raise Rejected("RUN_ALREADY_RESERVED") from error

def result_record(raw, phase, limits):
    value = decode(raw)
    need(type(value) is dict, "RESULT_SCHEMA")
    status = value.get("status")
    need(status in ("CANDIDATE", "EXHAUSTED", "INCOMPLETE"), "RESULT_STATUS")
    counts = value.get("counters")
    expected = set(COUNTERS) | {"process_cpu_seconds", "wall_seconds", "peak_live_records"}
    need(type(counts) is dict and set(counts) == expected, "COUNTER_SCHEMA")
    for key in COUNTERS:
        need(exact_int(counts[key], 0, limits[key]), "COUNTER_LIMIT")
    need(exact_int(counts["peak_live_records"], 0, limits["live_records"]), "LIVE_RECORD_LIMIT")
    for key in ("process_cpu_seconds", "wall_seconds"):
        need(finite(counts[key], limits["cpu_seconds" if key == "process_cpu_seconds" else key]),
             "IN_ENGINE_TIME")
    ranks = value.get("compatible_rank_counts")
    need(type(ranks) is dict and set(ranks) == {"rank_preserving", "rank_changing"}
         and all(exact_int(x, 0, counts["geometry_entries"]) for x in ranks.values())
         and sum(ranks.values()) <= counts["geometry_entries"], "RANK_COUNTERS")
    if status == "EXHAUSTED":
        need(counts["geometry_entries"] == limits["geometry_entries"], "PARTIAL_EXHAUSTION")
    elif status == "INCOMPLETE":
        need(type(value.get("limit")) is str and len(value["limit"]) <= 100, "INCOMPLETE_CAUSE")
    else:
        need(value.get("rank_class") in ranks
             and ranks[value["rank_class"]] >= 1
             and type(value.get("labels")) is dict
             and exact_int(value.get("cut"), 18, 19), "CANDIDATE_SCHEMA")
        if phase == "primary":
            cuts = value.get("admissible_old_cuts")
            need(type(cuts) is list and value["cut"] in cuts
                 and all(exact_int(cut, 18, 19) for cut in cuts), "PRIMARY_CUT_SCHEMA")
    return value

def verified_record(raw, context, candidate, scientific, digests):
    value = decode(raw)
    need(type(value) is dict and value.get("context") == context
         and value.get("candidate") == candidate, "VERIFICATION_BINDING")
    if value.get("error") is not None:
        need(type(value["error"]) is str and len(value["error"]) <= 512, "VERIFICATION_ERROR_SCHEMA")
        return False
    result = value.get("result")
    need(type(result) is dict and result.get("status") == "INDEPENDENTLY_VERIFIED_POSITIVE",
         "VERIFICATION_DISPOSITION")
    checks = result.get("checker_results")
    need(type(checks) is list and len(checks) == 2
         and all(type(c) is dict and c.get("valid") is True for c in checks), "CHECKER_RECEIPTS")
    if scientific:
        need([c.get("graph_digest") for c in checks] == digests
             and [c.get("m") for c in checks] == [41, 48], "CHECKER_ORIGINAL_BINDINGS")
        need(all(k in result for k in ("states", "rank_class", "rank_inversions", "gap_widths",
                                      "local_inventories", "final_inventories", "transport")),
             "SCIENTIFIC_VERIFICATION_SCHEMA")
    return True

def persist_candidate(ledger, base, raw, value, context, local_cap=None):
    identity = binding(raw)
    receipt = encode({"candidate": identity, "context": context,
                      "status": value["status"], "rank_class": value["rank_class"],
                      "cut": value["cut"], "counters": value["counters"]})
    ledger.save_all([(base + "-candidate.bin", raw), (base + "-candidate.json", receipt)],
                    local_cap=local_cap)
    return identity

def decide(phase, status, verified, measured, primary=None):
    need(phase in ("primary", "audit"), "PHASE_ID")
    if phase == "audit":
        need(primary == "ADMIT_AUDIT", "AUDIT_WITHOUT_PRIMARY_EXHAUSTION")
    else:
        need(primary is None, "PRIMARY_REENTRY")
    if measured is not True:
        return "STOP_RESOURCE_OR_CUSTODY_FAILURE"
    if status == "CANDIDATE":
        if verified is not True:
            return "STOP_VERIFICATION_FAILURE"
        return "STOP_VERIFIED_POSITIVE" if phase == "primary" else "STOP_ENGINE_DISCREPANCY"
    if status == "EXHAUSTED":
        return "ADMIT_AUDIT" if phase == "primary" else "STOP_REGISTERED_NEGATIVE"
    return "STOP_INCOMPLETE"

def remaining(now, deadline, requested):
    return max(0, min(requested, deadline - now))
