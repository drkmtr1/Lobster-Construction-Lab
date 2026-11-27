"""Independent endpoint audit and a host-first exhaustive traversal.

The audit does not call the primary row generator or search.
"""

from collections import Counter
from itertools import combinations

from .model import CapKey, CoreKey


def audit_specification(key, placement=()):
    """Recover independent actual index sets and the concrete host labels."""
    if isinstance(key, CoreKey):
        h = key.h
        low = {
            k: (3 if k in placement else 1)
            for k in range(1, h - 1)
        }
        high = dict(low)
        low.update(zip((h - 1, h, h + 2), key.singles, strict=True))
        counts = {("L", k): q for k, q in low.items()}
        counts.update({("H", k): q for k, q in high.items()})
        size = sum(low.values()) + sum(high.values())
        coordinates = {("C", x): x for x in range(size)}
        return h, size, counts, coordinates, dict(coordinates)

    # Work at actual old h=6, F=11, so fresh weights can be subtracted
    # directly at h=10. D228's gap proof transports this exact audit to all F.
    old_size = 11
    new_roles = (
        (("L", 1), key.left_flank), (("H", 1), key.left_high),
        (("L", 2), key.pairs[0]), (("H", 2), key.pairs[0]),
        (("L", 3), key.pairs[1]), (("H", 3), key.pairs[1]),
        (("L", 4), key.pairs[2]), (("H", 4), key.pairs[2]),
    )
    added = sum(quota for _, quota in new_roles)
    n = added // 2
    size = old_size + added
    counts = dict(new_roles)
    counts[("L", 7)] = counts[("L", 8)] = 1
    carried_input = {
        x + n for x in range(old_size) if x not in (old_size - 1, key.beta)
    }
    carried_weight = {
        w + n - 4 for w in range(old_size) if w not in (old_size - 1, key.beta - 1)
    }
    inputs = {
        (("L", i) if i < old_size + n - 1 else ("U", i - old_size)): i
        for i in range(size) if i not in carried_input
    }
    weights = {
        (("L", w) if w < old_size + n - 5 else ("U", w - old_size)): w
        for w in range(size) if w not in carried_weight
    }
    return 10, size, counts, inputs, weights


def endpoint(h, size, host, i):
    k = host[1]
    m = 2 * h + 2 + size
    center = k if host[0] == "L" else m - k
    return abs(h + 3 + i - center) - h


def core_placement(key, rows):
    count = Counter(host for host, _, _ in rows)
    placement = []
    for k in range(1, key.h - 1):
        low, high = count["L", k], count["H", k]
        if low != high or low not in (1, 3):
            raise ValueError("core certificate violates a homogeneous pair")
        if low == 3:
            placement.append(k)
    if len(placement) != key.triples:
        raise ValueError("core certificate has the wrong triple-pair count")
    return tuple(placement)


def verify_rows(key, rows, poll):
    """Raise on any invalid or wrong-key certificate, before promotion."""
    if not isinstance(key, (CoreKey, CapKey)) or type(rows) is not tuple:
        raise ValueError("unregistered certificate shape")
    for row in rows:
        poll()
        if type(row) is not tuple or len(row) != 3 or any(
            type(piece) is not tuple or len(piece) != 2
            or type(piece[0]) is not str or type(piece[1]) is not int
            for piece in row
        ):
            raise ValueError("invalid host or coordinate")
    placement = core_placement(key, rows) if isinstance(key, CoreKey) else ()
    h, size, demands, inputs, weights = audit_specification(key, placement)
    if Counter(host for host, _, _ in rows) != demands:
        raise ValueError("certificate violates host quotas")
    if sorted(i for _, i, _ in rows) != sorted(inputs):
        raise ValueError("certificate violates input inventory")
    if sorted(w for _, _, w in rows) != sorted(weights):
        raise ValueError("certificate violates weight inventory")
    for host, i, w in rows:
        poll()
        if endpoint(h, size, host, inputs[i]) != weights[w]:
            raise ValueError("certificate violates actual endpoint equation")
    if isinstance(key, CoreKey):
        anchors = (
            (("L", 3), ("C", size - 1), ("C", size - 1)),
            (("L", 4), ("C", key.beta), ("C", key.beta - 1)),
        )
        if any(anchor not in rows for anchor in anchors):
            raise ValueError("certificate is missing a requested anchor")
    return placement


def exhaust_placement(key, placement, budget):
    """Return a contrary witness, or None only after the full traversal."""
    h, size, demands, inputs, weights = audit_specification(key, placement)
    fixed = ()
    if isinstance(key, CoreKey):
        fixed = (
            (("L", 3), ("C", size - 1), ("C", size - 1)),
            (("L", 4), ("C", key.beta), ("C", key.beta - 1)),
        )
        for host, i, w in fixed:
            del inputs[i]
            del weights[w]
            demands[host] -= 1
    by_weight = {actual: coord for coord, actual in weights.items()}
    choices = {}
    for host, quota in demands.items():
        if not quota:
            continue
        candidates = []
        for i, actual in inputs.items():
            budget.poll()
            w = by_weight.get(endpoint(h, size, host, actual))
            if w is not None:
                candidates.append((host, i, w))
        choices[host] = tuple(candidates)
    rank = tuple(sorted(choices, key=lambda host: (len(choices[host]), host)))
    selected = []

    def visit(level, used_input, used_weight):
        budget.charge()
        if level == len(rank):
            if len(used_input) == len(inputs) and len(used_weight) == len(weights):
                return fixed + tuple(selected)
            return None
        host = rank[level]
        remaining = tuple(
            row for row in choices[host]
            if row[1] not in used_input and row[2] not in used_weight
        )
        for group in combinations(remaining, demands[host]):
            # Charge even rejected non-injective quota subsets.
            budget.charge()
            new_input = {row[1] for row in group}
            new_weight = {row[2] for row in group}
            if len(new_input) != len(group) or len(new_weight) != len(group):
                continue
            selected.extend(group)
            witness = visit(level + 1, used_input | new_input, used_weight | new_weight)
            if witness is not None:
                return witness
            del selected[-len(group):]
        return None

    return visit(0, set(), set())


def independent_exhaustion(key, budget):
    if not isinstance(key, CoreKey):
        return exhaust_placement(key, (), budget)
    # Bit-vector placement traversal independent of the primary combinations.
    for mask in range(1 << (key.h - 2)):
        budget.poll()
        if mask.bit_count() != key.triples:
            continue
        placement = tuple(k for k in range(1, key.h - 1) if mask & (1 << (k - 1)))
        witness = exhaust_placement(key, placement, budget)
        if witness is not None:
            return witness
    return None


def verify_named(profile, labels, poll):
    """Independently expand the original profile and its two changed edges."""
    spine = tuple("s:" + str(i) for i in range(4))
    originals = list(zip(spine[:-1], spine[1:], strict=True))
    for i, section in enumerate(profile):
        for a, quota in enumerate(section):
            center = f"b:{i}:{a}"
            originals.append((spine[i], center))
            for e in range(quota):
                poll()
                originals.append((center, f"l:{i}:{a}:{e}"))
    moves = {
        ("s:0", "b:0:0"): ("s:1", "b:0:0"),
        ("s:3", "b:3:0"): ("s:2", "b:3:0"),
    }
    fold = [moves.get(edge, edge) for edge in originals]
    vertices = {v for edge in originals for v in edge}
    if (set(labels) != vertices
            or any(type(label) is not int for label in labels.values())
            or sorted(labels.values()) != list(range(len(originals) + 1))):
        raise ValueError("named vertex inventory mismatch")
    for edges in (originals, fold):
        weights = []
        for u, v in edges:
            poll()
            weights.append(abs(labels[u] - labels[v]))
        if sorted(weights) != list(range(1, len(edges) + 1)):
            raise ValueError("named endpoint inventory mismatch")
    old = [abs(labels[u] - labels[v]) for u, v in moves.values()]
    restored = [abs(labels[u] - labels[v]) for u, v in moves]
    if restored != old[::-1]:
        raise ValueError("literal exterior exchange mismatch")
    return originals, fold
