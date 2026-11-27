"""Inactive D205 audit using raw labels and the actual original endpoints."""

from itertools import combinations

from .budget import Budget, LimitReached


def raw_upper(h, cut):
    # Choose the first and last actual old labels. Interior omissions are counted
    # by physical span. No index gap vector is reconstructed.
    count = 33 - h
    for first in range(cut, 42 - count):
        for last in range(first + count - 1, 41):
            interior_omissions = last - first - (count - 1)
            if h == 14 and cut == 18 and interior_omissions > 1:
                continue
            if h == 15 and cut == 18 and interior_omissions > 2:
                continue
            if h == 15 and cut == 19 and interior_omissions not in (2, 3):
                continue
            if h == 14 and cut == 19:
                if interior_omissions != 2:
                    continue
                second = first + 1
                for body in combinations(range(second + 1, last), count - 3):
                    yield first, second, *body, last
            elif h == 16 and cut == 18:
                for second in range(first + 1, last - (count - 2) + 1):
                    if last - second - (count - 2) > 4:
                        continue
                    for body in combinations(range(second + 1, last), count - 3):
                        yield first, second, *body, last
            else:
                for body in combinations(range(first + 1, last), count - 2):
                    yield first, *body, last


def physical_difference(u, v, cut):
    d = abs(u - v)
    crossing = min(u, v) < cut <= max(u, v)
    return d if crossing == (d >= cut + 2) else None


def differences(labels, edges, cut, frontier, budget):
    used = set()
    signature = []
    for u, v in edges:
        budget.count("fixed_edge_checks")
        d = physical_difference(labels[u], labels[v], cut)
        if d is None or d in used:
            return None
        used.add(d)
        signature.append(d)
    budget.count("fixed_edge_checks")
    connector = physical_difference(labels[frontier], 0, cut)
    if connector is None or connector in used:
        return None
    order = ("rank_preserving" if all(d < e for d, e in zip(signature, signature[1:]))
             else "rank_changing")
    return frozenset(range(1, 42)) - used - {connector}, order


def can_finish(unused, after, quotas, cut):
    x, y, z = quotas
    if x + y + z == 0:
        return not unused
    if 41 not in unused or after >= 41 or x + y == 0:
        return False
    lower = {v for v in unused if v < cut}
    upper = unused - lower
    return (len(lower) == y + z and len(upper) == 2*x + y + z
            and sum(v > after for v in lower) >= z
            and sum(v > after for v in upper - {41}) >= x + y - 1)


def place_pairs(unused, residual, cut, quotas, last, depth, budget):
    budget.count("allocation_states")
    budget.live(2 + depth)
    budget.check_time()
    if depth == 4:
        return () if not unused and not residual and not any(quotas) else None
    for center in sorted(unused):
        if center <= last or (center == 41) != (depth == 3):
            continue
        budget.count("placement_attempts")
        for tip in sorted(unused - {center, 41}):
            if center >= cut:
                category = 0 if tip >= cut else 1
            elif tip >= cut:
                category = 2
            else:
                continue
            if not quotas[category]:
                continue
            budget.count("pair_trials")
            attach = physical_difference(0, center, cut)
            tail = physical_difference(center, tip, cut)
            if attach not in residual or tail not in residual or attach == tail:
                continue
            remaining = unused - {center, tip}
            next_quotas = tuple(q - (i == category) for i, q in enumerate(quotas))
            if not can_finish(remaining, center, next_quotas, cut):
                continue
            suffix = place_pairs(remaining, residual - {attach, tail}, cut, next_quotas,
                                 center, depth + 1, budget)
            if suffix is not None:
                return ((center, tip), *suffix)
    return None


def audit_search(menu, incoming_graph, limits):
    """Independently inspect the frozen raw old subsets in a future authorized run."""
    budget = Budget(limits)
    records = {}
    frontier = incoming_graph["spine"][-1]
    shape = {
        (14, 18): (1, 3, 0), (14, 19): (0, 2, 2),
        (15, 18): (2, 2, 0), (15, 19): (1, 1, 2),
        (16, 18): (3, 1, 0), (16, 19): (2, 0, 2),
    }
    try:
        for variant in ("B", "C"):
            old = menu[variant]["state"]["minimum_labels"]
            names = sorted(old, key=old.__getitem__)
            edges = sorted(incoming_graph["edges"], key=lambda edge: abs(old[edge[0]] - old[edge[1]]))
            for (h, cut), quotas in shape.items():
                stream = {"geometry_entries": 0, "rank_preserving": 0, "rank_changing": 0}
                records[f"{variant}:{h}:{cut}"] = stream
                for lower in combinations(range(1, cut), h):
                    for upper in raw_upper(h, cut):
                        budget.count("geometry_entries")
                        stream["geometry_entries"] += 1
                        budget.live(1)
                        budget.check_time()
                        labels = dict(zip(names, (*lower, *upper), strict=True))
                        old_data = differences(labels, edges, cut, frontier, budget)
                        if old_data is None:
                            continue
                        weights, rank = old_data
                        stream[rank] += 1
                        vacant = frozenset(range(1, 42)) - set(labels.values())
                        pairs = place_pairs(vacant, weights, cut, quotas, -1, 0, budget)
                        if pairs is not None:
                            labels["s:6"] = 0
                            for index, (center, tip) in enumerate(pairs):
                                labels[f"b:6:{index}"] = center
                                labels[f"l:6:{index}:0"] = tip
                            return {"status": "CANDIDATE", "variant": variant, "labels": labels,
                                    "cut": cut, "induced_old_cut": h, "rank_class": rank,
                                    "streams": records, "counters": budget.receipt()}
        return {"status": "EXHAUSTED", "streams": records, "counters": budget.receipt()}
    except LimitReached as error:
        return {"status": "INCOMPLETE", "limit": str(error), "streams": records,
                "counters": budget.receipt()}
