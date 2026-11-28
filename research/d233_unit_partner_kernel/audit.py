"""D233 independent endpoint model and host-subset exhaustion."""

from collections import Counter
from itertools import combinations

from lcl.records import digest
from research.d229_homogeneous_pair_kernel.audit import verify_named, verify_rows
from research.d229_homogeneous_pair_kernel.coverage import emit_labels
from research.d229_homogeneous_pair_kernel.model import CoreKey
from research.d229_homogeneous_pair_kernel.retained import known_core


# Geometry and edge sets are frozen in the independently specified ORIGINALS.md.
ROLE_SECTIONS = (
    (("L", 1),),
    (("H", 1), ("L", 9)),
    (("L", 2), ("L", 3), ("L", 4), ("H", 2), ("H", 3), ("H", 4),
     ("L", 5), ("L", 6), ("L", 7), ("L", 8), ("L", 12),
     ("H", 5), ("H", 6), ("H", 7), ("H", 8)),
    (("L", 10),),
)


def original_profile(placement):
    lows, highs = placement
    a1, a2, a3, a4 = lows
    b1, b2, b3, b4 = highs
    return ((a1,), (b1, 1), (a2, a3, a4, b2, b3, b4) + (1,) * 9, (1,))


def physical_hosts(placement):
    assignments, quotas = {}, {}
    for i, (roles, section) in enumerate(zip(ROLE_SECTIONS, original_profile(placement), strict=True)):
        for k, (host, count) in enumerate(zip(roles, section, strict=True)):
            assignments[f"b:{i}:{k}"] = host
            quotas[host] = count
    return assignments, quotas


def source_rows(poll):
    old_key = CoreKey(6, 0, (1, 1, 1), 2)
    old = known_core(old_key)
    verify_rows(old_key, old, poll)
    return old


def carried(n, poll):
    return [
        ((kind, k + 4), i + n, w + n - 4)
        for (kind, k), (_, i), (_, w) in source_rows(poll)
        if (kind, k, i, w) not in (("L", 3, 10, 10), ("L", 4, 2, 1))
    ]


def endpoints(placement, poll):
    """Construct vacancies from actual endpoint coordinates, not reflected formulas."""
    _, quotas = physical_hosts(placement)
    size = sum(quotas.values())
    n = (size - 11) // 2
    inherited = carried(n, poll)
    returns = ((("L", 3), size - 1, size - 1), (("L", 4), 2, 1))
    used_inputs = {i for _, i, _ in inherited + list(returns)}
    used_weights = {w for _, _, w in inherited + list(returns)}
    if len(used_inputs) != 11 or len(used_weights) != 11:
        raise ValueError("audit transport/return collision")
    by_input = {
        (("L", i) if i < 11 + n - 1 else ("U", size - 4 - i)): i
        for i in range(size) if i not in used_inputs
    }
    by_weight = {
        (("L", w) if w < 11 + n - 5 else ("U", size - 4 - w)): w
        for w in range(size) if w not in used_weights
    }
    demands = Counter(quotas)
    for host, _, _ in inherited + list(returns):
        demands[host] -= 1
    if sum(demands.values()) != len(by_input) or len(by_input) != len(by_weight):
        raise ValueError("audit resource mismatch")
    return size, by_input, by_weight, demands, inherited, returns


def weight(host, i, size):
    kind, k = host
    center = k if kind == "L" else size + 22 - k
    return abs(13 + i - center) - 10


def reverse_name(vertex):
    kind, index, *suffix = vertex.split(":")
    return ":".join((kind, str(3 - int(index)), *suffix))


def reconstruct(placement, rows, poll):
    size, inputs, weights, demands, inherited, returns = endpoints(placement, poll)
    counts, seen_i, seen_w = Counter(), set(), set()
    complete = inherited + list(returns)
    for host, source, target in rows:
        poll()
        if any(type(tag) is not str or type(value) is not int for tag, value in (host, source, target)):
            raise ValueError("invalid tagged row")
        if not demands[host] or source not in inputs or target not in weights:
            raise ValueError("undeclared row")
        if source in seen_i or target in seen_w:
            raise ValueError("repeated tagged resource")
        i, w = inputs[source], weights[target]
        if weight(host, i, size) != w:
            raise ValueError("incorrect actual endpoint")
        counts[host] += 1
        seen_i.add(source)
        seen_w.add(target)
        complete.append((host, i, w))
    if counts != demands or seen_i != inputs.keys() or seen_w != weights.keys():
        raise ValueError("missing resource or wrong residual quotas")
    if (sorted(i for _, i, _ in complete) != list(range(size))
            or sorted(w for _, _, w in complete) != list(range(size))):
        raise ValueError("incorrect complete allocation")
    assignments, quotas = physical_hosts(placement)
    if Counter(host for host, _, _ in complete) != Counter(quotas):
        raise ValueError("wrong actual quotas")
    for host, i, w in complete:
        poll()
        if weight(host, i, size) != w:
            raise ValueError("incorrect inherited or return weight")
    profile = original_profile(placement)
    labels = emit_labels(10, complete, assignments)
    original, fold = verify_named(profile, labels, poll)
    reverse = {reverse_name(name): value for name, value in labels.items()}
    reverse_original, reverse_fold = verify_named(profile[::-1], reverse, poll)
    return {
        "profile": profile,
        "labels": labels,
        "edges": size + 22,
        "original_sha256": digest({"edges": original, "labels": labels}),
        "fold_sha256": digest({"edges": fold, "labels": labels}),
        "reverse_original_sha256": digest({"edges": reverse_original, "labels": reverse}),
        "reverse_fold_sha256": digest({"edges": reverse_fold, "labels": reverse}),
    }


def exhaust(placement, budget):
    """Independently traverse exact host-quota subsets of actual endpoints."""
    size, inputs, weights, demands, _, _ = endpoints(placement, budget.poll)
    by_weight = {actual: tag for tag, actual in weights.items()}
    choices = {}
    for host, count in demands.items():
        if not count:
            continue
        candidates = []
        for tag, actual in inputs.items():
            budget.row_attempt("audit")
            output = by_weight.get(weight(host, actual, size))
            if output is not None:
                candidates.append((host, tag, output))
        choices[host] = tuple(candidates)
    rank = tuple(sorted(choices, key=lambda host: (len(choices[host]), host)))
    selected = []

    def visit(level, used_inputs, used_weights):
        budget.charge()
        if level == len(rank):
            if len(used_inputs) == len(inputs) and len(used_weights) == len(weights):
                return tuple(selected)
            return None
        host = rank[level]
        available = (r for r in choices[host] if r[1] not in used_inputs and r[2] not in used_weights)
        for group in combinations(available, demands[host]):
            budget.charge()
            new_inputs = {r[1] for r in group}
            new_weights = {r[2] for r in group}
            if len(new_inputs) != len(group) or len(new_weights) != len(group):
                continue
            selected.extend(group)
            result = visit(level + 1, used_inputs | new_inputs, used_weights | new_weights)
            if result is not None:
                return result
            del selected[-len(group):]
        return None

    return visit(0, set(), set())
