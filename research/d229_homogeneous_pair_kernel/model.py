"""Frozen key domains and primary row model. No module-level search."""

from dataclasses import dataclass
from itertools import combinations, product

CORE_SIZES = (6, 7, 8, 9)
BETAS = (1, 2)
QUOTAS = (1, 3)
Host = tuple[str, int]
Coord = tuple[str, int]
Row = tuple[Host, Coord, Coord]


@dataclass(frozen=True)
class CoreKey:
    h: int
    triples: int
    singles: tuple[int, int, int]
    beta: int

    def __post_init__(self):
        if type(self.h) is not int or self.h not in CORE_SIZES:
            raise ValueError("unregistered core size")
        if type(self.triples) is not int or not 0 <= self.triples <= self.h - 2:
            raise ValueError("unregistered triple-pair count")
        if (type(self.singles) is not tuple or len(self.singles) != 3
                or any(type(q) is not int or q not in QUOTAS for q in self.singles)):
            raise ValueError("unregistered single quotas")
        if type(self.beta) is not int or self.beta not in BETAS:
            raise ValueError("unregistered source state")


@dataclass(frozen=True)
class CapKey:
    left_flank: int
    left_high: int
    pairs: tuple[int, int, int]
    beta: int

    def __post_init__(self):
        quotas = (self.left_flank, self.left_high)
        if type(self.pairs) is not tuple or len(self.pairs) != 3:
            raise ValueError("unregistered cap pair vector")
        if any(type(q) is not int or q not in QUOTAS for q in quotas + self.pairs):
            raise ValueError("unregistered cap quotas")
        if type(self.beta) is not int or self.beta not in BETAS:
            raise ValueError("unregistered source state")


@dataclass(frozen=True)
class Problem:
    inputs: tuple[Coord, ...]
    weights: tuple[Coord, ...]
    demands: dict[Host, int]
    rows: tuple[Row, ...]
    fixed: tuple[Row, ...] = ()


def core_keys():
    for h in CORE_SIZES:
        for triples in range(h - 1):
            for singles in product(QUOTAS, repeat=3):
                for beta in BETAS:
                    yield CoreKey(h, triples, singles, beta)


def cap_keys():
    for left_flank, left_high in product(QUOTAS, repeat=2):
        for pairs in product(QUOTAS, repeat=3):
            for beta in BETAS:
                yield CapKey(left_flank, left_high, pairs, beta)


def placements(key):
    return combinations(range(1, key.h - 1), key.triples)


def core_problem(key, placement, poll):
    demands = {}
    for k in range(1, key.h - 1):
        demands["L", k] = demands["H", k] = 3 if k in placement else 1
    for k, quota in zip((key.h - 1, key.h, key.h + 2), key.singles, strict=True):
        demands["L", k] = quota
    size = sum(demands.values())
    fixed = (
        (("L", 3), ("C", size - 1), ("C", size - 1)),
        (("L", 4), ("C", key.beta), ("C", key.beta - 1)),
    )
    inputs = tuple(("C", i) for i in range(size) if i not in (size - 1, key.beta))
    weights = tuple(("C", w) for w in range(size) if w not in (size - 1, key.beta - 1))
    available = set(weights)
    for host, _, _ in fixed:
        demands[host] -= 1
    rows = []
    for host, demand in demands.items():
        if not demand:
            continue
        kind, k = host
        for i in inputs:
            poll()
            w = ("C", i[1] + 3 - k if kind == "L" else size - 1 - k - i[1])
            if w in available:
                rows.append((host, i, w))
    return Problem(inputs, weights, demands, tuple(rows), fixed)


def cap_problem(key, poll):
    demands = {("L", 1): key.left_flank, ("H", 1): key.left_high}
    for k, quota in enumerate(key.pairs, 2):
        demands["L", k] = demands["H", k] = quota
    n = sum(demands.values()) // 2
    demands["L", 7] = demands["L", 8] = 1
    inputs = tuple(
        [("L", i) for i in range(n)] + [("L", n + key.beta)]
        + [("U", i) for i in range(n - 1, 2 * n)]
    )
    weights = tuple(
        [("L", w) for w in range(n - 4)] + [("L", n + key.beta - 5)]
        + [("U", w) for w in range(n - 5, 2 * n)]
    )
    available = set(weights)
    rows = []
    for host in demands:
        kind, k = host
        for side, value in inputs:
            poll()
            if kind == "L":
                w = (side, value + 3 - k)
            else:
                w = ("U" if side == "L" else "L", 2 * n - 1 - k - value)
            if w in available:
                rows.append((host, (side, value), w))
    return Problem(inputs, weights, demands, tuple(rows))
