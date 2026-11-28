"""D233 primary complete reflected row model."""

from research.d229_homogeneous_pair_kernel.model import Problem


def problem(placement, budget):
    lows, highs = placement
    n, odd = divmod(sum(lows) + sum(highs), 2)
    if odd or not 6 <= n <= 32:
        raise ValueError("unregistered width")
    inputs = tuple(("L", i) for i in range(n) if i != 2) + (("L", n + 2),)
    inputs += tuple(("U", i) for i in range(-2, n - 2))
    weights = tuple(("L", w) for w in range(n - 4) if w != 1) + (("L", n - 3),)
    weights += tuple(("U", w) for w in range(-2, n + 2))
    available = set(weights)
    demands = {
        (kind, k): quota
        for kind, quotas in (("L", lows), ("H", highs))
        for k, quota in enumerate(quotas, 1)
    }
    demands["L", 3] -= 1
    demands["L", 4] -= 1
    demands["L", 7] = demands["L", 8] = 1
    rows = []
    for (kind, k), demand in demands.items():
        if not demand:
            continue
        for block, x in inputs:
            budget.row_attempt("primary")
            shift = (3 - k) if block == "L" else (k - 3)
            if kind == "L":
                output = block, x + shift
            else:
                output = ("U" if block == "L" else "L"), x - shift
            if output in available:
                rows.append(((kind, k), (block, x), output))
    if len(inputs) != len(weights) or len(inputs) != sum(demands.values()):
        raise ValueError("packet resource mismatch")
    return Problem(inputs, weights, demands, tuple(rows))
