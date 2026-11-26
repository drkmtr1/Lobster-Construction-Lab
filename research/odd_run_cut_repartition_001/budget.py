"""Inactive shared input binding and counters for the prepared consumers."""

import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


class LimitReached(RuntimeError):
    """A stopped execution has an incomplete outcome."""


class Budget:
    """One prospective sequential worker with separately billed engines."""

    def __init__(self):
        self.cpu_start = time.process_time()
        self.wall_start = time.monotonic()
        config = json.loads((HERE / "config.json").read_bytes())
        if config["execution_authorized"] is not True or config["execution_entry"] is None:
            raise RuntimeError("D197 is symbolically resolved; official execution is disabled")
        self.caps = config["inactive_prospective_caps"]
        bindings = config["bound_inputs"]
        payloads = {}
        for key, bound in bindings.items():
            raw = (ROOT / bound["path"]).read_bytes()
            if len(raw) != bound["bytes"] or hashlib.sha256(raw).hexdigest() != bound["sha256"]:
                raise ValueError(f"Frozen D197 input binding differs for {key}")
            payloads[key] = json.loads(raw)
        self.original = payloads["originals"]["matches"]["odd"]
        self.prefix = payloads["prefixes"]["prefixes"]["odd"]
        if self.original["prefix_digest"] != self.prefix["prefix_digest"]:
            raise ValueError("Independent prefix identity mismatch")
        self.thresholds = {
            row["split"]: row["threshold"]
            for row in payloads["symbolic_controls"]["odd_prefix_all_cuts"]
        }
        self.counts = {
            engine: dict(geometries=0, raw_placements=0, states=0, transitions=0, peak_live=0)
            for engine in ("primary", "audit")
        }
        self.evidence_bytes = 0

    def poll(self):
        if time.process_time() - self.cpu_start >= self.caps["combined_process_cpu_seconds"]:
            raise LimitReached("combined_process_cpu_seconds")
        if time.monotonic() - self.wall_start >= self.caps["combined_wall_seconds"]:
            raise LimitReached("combined_wall_seconds")

    def charge(self, engine, metric):
        self.poll()
        count = self.counts[engine][metric]
        if count >= self.caps[engine][metric]:
            raise LimitReached(f"{engine}.{metric}")
        self.counts[engine][metric] = count + 1

    def observe_live(self, engine, records):
        self.poll()
        if records > self.caps[engine]["live_records"]:
            raise LimitReached(f"{engine}.live_records")
        self.counts[engine]["peak_live"] = max(self.counts[engine]["peak_live"], records)

    def charge_evidence(self, encoded_bytes, *, reconciliation=False):
        """Charge encoded bytes before writing a durable evidence record."""
        if type(encoded_bytes) is not int or encoded_bytes < 0:
            raise ValueError("encoded_bytes must be a nonnegative integer")
        cap = self.caps["new_evidence_bytes"]
        if not reconciliation:
            self.poll()
            cap -= self.caps["reconciliation_reserve_bytes"]
        if self.evidence_bytes + encoded_bytes > cap:
            raise LimitReached("new_evidence_bytes")
        self.evidence_bytes += encoded_bytes
