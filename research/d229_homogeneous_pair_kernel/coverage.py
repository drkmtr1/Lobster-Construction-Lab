"""Deterministic projection from checked numerical keys to physical count types."""

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product

from .model import BETAS, QUOTAS, CapKey, CoreKey


@dataclass(frozen=True)
class PhysicalKey:
    h: int
    left: int
    right: int
    p: int
    t: int
    left_triple: int
    right_triple: int


@dataclass(frozen=True)
class Join:
    core: CoreKey
    cap: CapKey
    left_triple_pairs: int


def physical_keys():
    for h in range(10, 14):
        for left in range(2, 2 * h - 5, 2):
            right = 2 * h - 3 - left
            for p, t in product(QUOTAS, repeat=2):
                for a in range(left + 1):
                    for b in range(right + 1):
                        yield PhysicalKey(h, left, right, p, t, a, b)


def joins(key):
    h0 = key.h - 4
    c = key.right_triple % 2
    right_pairs = (key.right_triple - c) // 2
    for a, b in product((0, 1), repeat=2):
        leftover = key.left_triple - a - b
        if leftover % 2 or not 0 <= leftover <= key.left - 2:
            continue
        left_pairs = leftover // 2
        for cap_pairs in product(QUOTAS, repeat=3):
            cap_triples = cap_pairs.count(3)
            g0 = left_pairs + right_pairs - cap_triples
            if not 0 <= g0 <= h0 - 2:
                continue
            for beta in BETAS:
                yield Join(
                    CoreKey(h0, g0, (1 + 2 * b, key.t, 1 + 2 * c), beta),
                    CapKey(key.p, 1 + 2 * a, cap_pairs, beta),
                    left_pairs,
                )


def decide(key, states, poll):
    """Use witness-only lower and proof-conservative upper relations."""
    possible = False
    for join in joins(key):
        poll()
        core = states.get(join.core, "UNRESOLVED")
        cap = states.get(join.cap, "UNRESOLVED")
        if core == cap == "POSITIVE":
            return "COVERED", join
        if core != "NEGATIVE" and cap != "NEGATIVE":
            possible = True
    return ("UNRESOLVED" if possible else "ARCHITECTURE_EXCLUDED"), None


def profile_for(key):
    return (
        (key.p,),
        (3,) * key.left_triple + (1,) * (key.left - key.left_triple),
        (3,) * key.right_triple + (1,) * (key.right - key.right_triple),
        (key.t,),
    )


def transport(core, cap, beta):
    size = len(core)
    n = (len(cap) - 2) // 2
    omitted = {
        (("L", 3), ("C", size - 1), ("C", size - 1)),
        (("L", 4), ("C", beta), ("C", beta - 1)),
    }
    old_rows = tuple(
        ((kind, k + 4), i + n, w + n - 4)
        for (kind, k), (_, i), (_, w) in core
        if ((kind, k), ("C", i), ("C", w)) not in omitted
    )
    new_rows = tuple(
        (host, i + (size if input_side == "U" else 0),
         w + (size if weight_side == "U" else 0))
        for host, (input_side, i), (weight_side, w) in cap
    )
    return old_rows + new_rows


def role_assignment(key, rows, join):
    h = key.h
    quotas = Counter(host for host, _, _ in rows)
    triple = [k for k in range(2, h - 1) if quotas["L", k] == 3]
    unit = [k for k in range(2, h - 1) if quotas["L", k] == 1]
    left_unit = (key.left - 2) // 2 - join.left_triple_pairs
    left_pairs = set(triple[:join.left_triple_pairs] + unit[:left_unit])
    by_section = [[("L", 1)], [("H", 1), ("L", h - 1)], [("L", h + 2)], [("L", h)]]
    for k in range(2, h - 1):
        by_section[1 if k in left_pairs else 2].extend((("L", k), ("H", k)))
    pools = defaultdict(list)
    for i, hosts in enumerate(by_section):
        for host in sorted(hosts):
            pools[i, quotas[host]].append(host)
    positions = Counter()
    assignments = {}
    for i, section in enumerate(profile_for(key)):
        for a, quota in enumerate(section):
            group = (i, quota)
            assignments[f"b:{i}:{a}"] = pools[group][positions[group]]
            positions[group] += 1
    if set(assignments.values()) != set(quotas) or len(assignments) != len(quotas):
        raise ValueError("role assignment failed to cover the numerical host set")
    return assignments


def emit_labels(h, rows, assignments):
    size = len(rows)
    m = 2 * h + 2 + size
    grouped = defaultdict(list)
    for host, i, _ in rows:
        grouped[host].append(h + 3 + i)
    labels = {"s:0": m - h + 1, "s:1": 0, "s:2": m, "s:3": h + 1}
    for name, host in assignments.items():
        kind, k = host
        labels[name] = k if kind == "L" else m - k
        for e, value in enumerate(sorted(grouped[host])):
            labels["l" + name[1:] + f":{e}"] = value
    return labels
