"""Dormant D231 normalized scope and primary reflected row model."""

from itertools import combinations_with_replacement, permutations

from research.d229_homogeneous_pair_kernel.model import Problem


def aggregates():
    """Yield the 29 unresolved aggregates in lexicographic order."""
    for b, c, d in combinations_with_replacement(range(1, 10, 2), 3):
        if d <= 7 and d > 1 or d == 9 and b >= 3:
            yield 1, b, c, d


def placements(key):
    return tuple(sorted(set(permutations(key))))


def problem(quotas, budget):
    n = sum(quotas)
    lower_inputs = tuple(i for i in range(n) if i != 2) + (n + 2,)
    lower_weights = tuple(w for w in range(n - 4) if w != 1) + (n - 3,)
    if n == 4:
        lower_weights = ()
    inputs = tuple(("L", x) for x in lower_inputs) + tuple(
        ("U", y) for y in range(-2, n - 2)
    )
    weights = tuple(("L", x) for x in lower_weights) + tuple(
        ("U", y) for y in range(-2, n + 2)
    )
    demands = {
        (kind, k): count for k, count in enumerate(quotas, 1)
        for kind in ("L", "H")
    }
    demands["L", 3] -= 1
    demands["L", 4] -= 1
    demands["L", 7] = demands["L", 8] = 1
    available = set(weights)
    rows = []
    for host, demand in demands.items():
        if not demand:
            continue
        kind, k = host
        for side, value in inputs:
            budget.row_attempt("primary")
            shift = (3 - k) if side == "L" else (k - 3)
            if kind == "L":
                output = (side, value + shift)
            else:
                output = ("U" if side == "L" else "L", value - shift)
            if output in available:
                rows.append((host, (side, value), output))
    if len(inputs) != len(weights) or len(inputs) != sum(demands.values()):
        raise ValueError("mismatched row inventories")
    return Problem(inputs, weights, demands, tuple(rows))
