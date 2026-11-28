"""D233 exact aggregate identity and placement enumeration."""

from itertools import combinations_with_replacement, permutations, product


def aggregates(rule):
    for t in (2, 3, 4):
        for values in combinations_with_replacement(rule[str(t)], t):
            yield (1,) * (4 - t) + values


def placements(key):
    """Keep every distinct assignment and orientation; prefer H3 first."""
    choices = set()
    for order in set(permutations(key)):
        signs = ((False, True) if q != 1 else (False,) for q in order)
        for high in product(*signs):
            lows = tuple(1 if bit else q for q, bit in zip(order, high, strict=True))
            highs = tuple(q if bit else 1 for q, bit in zip(order, high, strict=True))
            choices.add((lows, highs))

    def preference(placement):
        lows, highs = placement
        return (
            -highs[2],
            sum(q > 1 for q in highs),
            sum(abs(3 - k) for k, q in enumerate(lows, 1) if q > 1),
            placement,
        )

    return tuple(sorted(choices, key=preference))
