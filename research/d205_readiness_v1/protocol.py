"""D205 receipt, framing and phase rules with no native or scientific imports."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import struct
import threading

FRAME_MAX = 1 << 20
TERMINAL_RESERVE = 65536
COUNTERS = ("geometry_entries", "placement_attempts", "allocation_states",
            "pair_trials", "fixed_edge_checks")

RANK_CLASSES = ("rank_preserving", "rank_changing")
STREAM_COUNTS = {
    f"{variant}:{h}:{cut}": count
    for variant in ("B", "C")
    for h, cut, count in (
        (14, 18, 52360), (14, 19, 936360), (15, 18, 95608),
        (15, 19, 1955952), (16, 18, 464151), (16, 19, 4029102),
    )
}


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
        self.lock = threading.Lock()

    def save_all(self, entries, terminal=False, local_cap=None):
        if terminal:
            need(len(entries) == 1 and entries[0][0] in ("terminal.json", "seal.json"), "TERMINAL_SLOT")
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
        actual = {p.name for p in self.root.iterdir()}
        need(actual == set(self.records), "EVIDENCE_FILE_SET")
        for name, info in self.records.items():
            path = self.root / name
            before = path.lstat()
            need(stat.S_ISREG(before.st_mode)
                 and not getattr(before, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
                 and before.st_size == info["bytes"], "EVIDENCE_FILE_OBJECT")
            with path.open("rb") as file:
                during = os.fstat(file.fileno())
                need((before.st_dev, before.st_ino, before.st_size) ==
                     (during.st_dev, during.st_ino, during.st_size), "EVIDENCE_FILE_CHANGED")
                data = file.read(info["bytes"] + 1)
            need(binding(data) == info, "EVIDENCE_RECONCILIATION")
        need(sum(info["bytes"] for info in self.records.values()) <= self.charged <= self.cap,
             "EVIDENCE_RECONCILIATION")

def reserve(path):
    # This directory is never removed or reused by the controller, including after failure.
    try:
        path.mkdir(exist_ok=False)
    except FileExistsError as error:
        raise Rejected("RUN_ALREADY_RESERVED") from error

def result_record(raw, phase, limits, domain=None):
    """Validate the exact D205 stream prefix before accepting an engine receipt."""
    value = decode(raw)
    need(type(value) is dict, "RESULT_SCHEMA")
    status = value.get("status")
    fields = {"status", "counters", "streams"}
    if status == "CANDIDATE":
        fields |= {"variant", "induced_old_cut", "cut", "rank_class", "labels"}
    elif status == "INCOMPLETE":
        fields.add("limit")
    else:
        need(status == "EXHAUSTED", "RESULT_STATUS")
    if domain is None and "inert_padding" in value:
        need(status == "CANDIDATE" and type(value["inert_padding"]) is str, "INERT_PADDING")
        fields.add("inert_padding")
    need(set(value) == fields and phase in ("primary", "audit"), "RESULT_SCHEMA")
    counts = value["counters"]
    expected = set(COUNTERS) | {"process_cpu_seconds", "wall_seconds", "peak_live_records"}
    need(type(counts) is dict and set(counts) == expected, "COUNTER_SCHEMA")
    for key in COUNTERS:
        need(exact_int(counts[key], 0, limits[key]), "COUNTER_LIMIT")
    need(exact_int(counts["peak_live_records"], 0, limits["live_records"]), "LIVE_RECORD_LIMIT")
    for key in ("process_cpu_seconds", "wall_seconds"):
        need(finite(counts[key], limits["cpu_seconds" if key == "process_cpu_seconds" else key]),
             "IN_ENGINE_TIME")
    streams = value["streams"]
    need(type(streams) is dict and list(streams) == list(STREAM_COUNTS)[:len(streams)],
         "STREAM_ORDER_OR_IDENTITY")
    aggregate = 0
    last = None
    for index, (name, stream) in enumerate(streams.items()):
        cap = STREAM_COUNTS[name]
        need(type(stream) is dict and set(stream) == {"geometry_entries", *RANK_CLASSES},
             "STREAM_SCHEMA")
        visits = stream["geometry_entries"]
        need(exact_int(visits, 0, cap), "STREAM_GEOMETRY")
        if index + 1 < len(streams) or status == "EXHAUSTED":
            need(visits == cap, "INEXACT_COMPLETED_STREAM")
        need(all(exact_int(stream[r], 0, visits) for r in RANK_CLASSES)
             and sum(stream[r] for r in RANK_CLASSES) <= visits, "STREAM_RANK_COUNTERS")
        aggregate += visits
        last = name
    need(counts["geometry_entries"] == aggregate, "STREAM_AGGREGATE")
    if status == "EXHAUSTED":
        need(len(streams) == len(STREAM_COUNTS) and aggregate == sum(STREAM_COUNTS.values())
             == limits["geometry_entries"], "PARTIAL_EXHAUSTION")
    elif status == "INCOMPLETE":
        need(type(value["limit"]) is str and 0 < len(value["limit"]) <= 100, "INCOMPLETE_CAUSE")
    else:
        variant, h, cut = value["variant"], value["induced_old_cut"], value["cut"]
        rank = value["rank_class"]
        need(variant in ("B", "C") and exact_int(h, 14, 16) and exact_int(cut, 18, 19)
             and rank in RANK_CLASSES, "CANDIDATE_SCHEMA")
        need(last == f"{variant}:{h}:{cut}" and streams[last][rank] > 0, "CANDIDATE_STREAM_POSITION")
        labels = value["labels"]
        need(type(labels) is dict, "CANDIDATE_LABELS")
        if domain is not None:
            need(set(labels) == set(domain["vertices_41"]) and len(labels) == 42
                 and all(exact_int(x, 0, 41) for x in labels.values())
                 and len(set(labels.values())) == 42 and labels["s:6"] == 0, "CANDIDATE_NAMED_ALPHABET")
            old = [labels[v] for v in domain["old_order"][variant]]
            need(all(a < b for a, b in zip(old, old[1:])) and sum(x < cut for x in old) == h,
                 "CANDIDATE_OLD_EMBEDDING")
        else:
            need(labels == {"inert": 7}, "INERT_CANDIDATE_REQUIRED")
    return value


def verified_record(raw, context, candidate, scientific, digests, rank=None, exact_candidate=None):
    value = decode(raw)
    need(type(value) is dict and value.get("context") == context
         and value.get("candidate") == candidate, "VERIFICATION_BINDING")
    if value.get("error") is not None:
        need("result" not in value and type(value["error"]) is str
             and 0 < len(value["error"]) <= 512, "VERIFICATION_ERROR_SCHEMA")
        return False
    result = value.get("result")
    need(type(result) is dict and result.get("status") == "INDEPENDENTLY_VERIFIED_POSITIVE",
         "VERIFICATION_DISPOSITION")
    checks = result.get("checker_results")
    need(type(checks) is list and len(checks) == 2
         and all(type(c) is dict and c.get("valid") is True for c in checks), "CHECKER_RECEIPTS")
    if scientific:
        need("synthetic" not in result and "same_pid" not in result, "SYNTHETIC_VERIFICATION_FORBIDDEN")
        need([c.get("graph_digest") for c in checks] == digests
             and [c.get("m") for c in checks] == [41, 48]
             and [c.get("n") for c in checks] == [42, 49]
             and all(c.get("errors") == [] for c in checks), "CHECKER_ORIGINAL_BINDINGS")
        states = result.get("states")
        need(type(states) is list and len(states) == 2 and all(type(s) is dict for s in states),
             "VERIFIED_STATES")
        cut = states[0].get("actual_cut")
        need(exact_int(cut, 18, 19) and result.get("normalized_suffix") == [48, 46-cut, cut+2],
             "VERIFIED_CUTS")
        need(type(exact_candidate) is dict and cut == exact_candidate.get("cut")
             and states[0].get("actual_labels") == exact_candidate.get("labels"),
             "REPORT_DIFFERS_FROM_DURABLE_CANDIDATE")
        need(result.get("variant") == exact_candidate.get("variant")
             and exact_int(result.get("induced_old_cut"), 14, 16)
             and result["induced_old_cut"] == exact_candidate.get("induced_old_cut"),
             "VERIFIED_MENU_BINDING")
        lifted = {v: 3+x+3*(x >= cut) for v, x in exact_candidate["labels"].items()}
        lifted["s:7"] = 48
        for j, position in enumerate((0, 2, 1)):
            lifted[f"b:7:{j}"] = j
            lifted[f"l:7:{j}:0"] = cut+3+position
        need(states[1].get("actual_labels") == lifted, "VERIFIED_SUFFIX_TRANSPORT")
        for state, size, place in zip(states, (41, 48), (cut, cut+3)):
            need(state.get("size") == size and state.get("actual_cut") == place
                 and state.get("complementary_cut") == size+1-place and state.get("threshold") == cut+2,
                 "VERIFIED_STATE_GEOMETRY")
            for polarity in ("actual", "complementary"):
                labels, rows = state.get(polarity+"_labels"), state.get(polarity+"_edges")
                need(type(labels) is dict and len(labels) == size+1
                     and type(rows) is list and len(rows) == size, "VERIFIED_STATE_INVENTORY")
        for key, length in (("actual_old_edges", 32), ("old_map", 33), ("gap_widths", 32),
                            ("local_inventories", 2), ("final_inventories", 2),
                            ("changed_resources", 2), ("transport", 3)):
            need(type(result.get(key)) is list and len(result[key]) == length, "VERIFIED_ARTIFACTS")
        need(result.get("rank_class") == rank and type(result.get("rank_inversions")) is list,
             "VERIFIED_RANK_CLASS")
    else:
        need(result.get("synthetic") is True and result.get("same_pid") == context.get("pid"),
             "INERT_VERIFICATION_REQUIRED")
    return True

def persist_candidate(ledger, base, raw, value, context, local_cap=None):
    identity = binding(raw)
    stream = f"{value['variant']}:{value['induced_old_cut']}:{value['cut']}"
    receipt = encode({"candidate": identity, "context": context,
                      "status": value["status"], "rank_class": value["rank_class"],
                      "cut": value["cut"], "induced_old_cut": value["induced_old_cut"],
                      "variant": value["variant"], "stream": stream,
                      "stream_geometry_entries": value["streams"][stream]["geometry_entries"],
                      "counters": value["counters"]})
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
