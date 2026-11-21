"""Cooperative, reproducible limits. These are not OS memory containment."""
from dataclasses import dataclass, asdict
from time import monotonic

class BudgetExceeded(RuntimeError):
    pass

@dataclass(frozen=True)
class Limits:
    max_nodes: int = 200_000
    time_limit: float = 5.0
    max_vertices: int = 16
    max_states: int = 20_000

    def __post_init__(self):
        for name in ("max_nodes", "max_vertices", "max_states"):
            value = getattr(self, name)
            if type(value) is not int or value < 1:
                raise ValueError(name + " must be a positive integer")
        import math
        if (isinstance(self.time_limit, bool)
                or not isinstance(self.time_limit, (int, float))
                or not math.isfinite(self.time_limit) or self.time_limit <= 0):
            raise ValueError("time_limit must be a positive finite number")
        if self.max_vertices > 100:
            raise ValueError("Starter exact engines cap max_vertices at 100; constructors are separate")

    @classmethod
    def from_mapping(cls, values=None):
        values = {} if values is None else dict(values)
        unknown = set(values) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError("Unknown limit keys: " + ", ".join(sorted(unknown)))
        return cls(**values)

    def to_dict(self):
        return asdict(self)

class Budget:
    def __init__(self, limits):
        self.limits = limits
        self.started = monotonic()
        self.nodes = 0

    def check(self):
        if monotonic() - self.started >= self.limits.time_limit:
            raise BudgetExceeded("time_limit")

    def tick(self):
        self.check()
        if self.nodes >= self.limits.max_nodes:
            raise BudgetExceeded("max_nodes")
        self.nodes += 1

    def elapsed(self):
        return monotonic() - self.started

