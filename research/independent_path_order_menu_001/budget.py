"""Counters for the inactive, single-worker D204 consumers."""

from time import monotonic, process_time


class LimitReached(Exception):
    """A separately approved execution stopped without deciding existence."""


class Budget:
    def __init__(self, limits):
        self.limits = dict(limits)
        self.counts = {
            "geometry_entries": 0,
            "placement_attempts": 0,
            "allocation_states": 0,
            "fixed_edge_checks": 0,
            "pair_trials": 0,
        }
        self.started_wall = monotonic()
        self.started_cpu = process_time()
        self.peak_live_records = 0

    def check_time(self):
        if monotonic() - self.started_wall >= self.limits["wall_seconds"]:
            raise LimitReached("wall_seconds")
        if process_time() - self.started_cpu >= self.limits["cpu_seconds"]:
            raise LimitReached("cpu_seconds")

    def count(self, key):
        if self.counts[key] >= self.limits[key]:
            raise LimitReached(key)
        self.counts[key] += 1

    def live(self, records):
        if records > self.limits["live_records"]:
            raise LimitReached("live_records")
        self.peak_live_records = max(self.peak_live_records, records)

    def receipt(self):
        return {
            **self.counts,
            "process_cpu_seconds": process_time() - self.started_cpu,
            "wall_seconds": monotonic() - self.started_wall,
            "peak_live_records": self.peak_live_records,
        }
