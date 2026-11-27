"""Inactive D205 width-coordinate consumer for the exact two-input menu."""

from itertools import accumulate, combinations, product

from .budget import Budget, LimitReached


# X: upper/upper, Y: upper/lower, Z: lower/upper indexed arms.
CASES = (
    (14, 18, 1, 3, 0),
    (14, 19, 0, 2, 2),
    (15, 18, 2, 2, 0),
    (15, 19, 1, 1, 2),
    (16, 18, 3, 1, 0),
    (16, 19, 2, 0, 2),
)


def width_parts(units, slots):
    for bars in combinations(range(units + slots - 1), slots - 1):
        points = (-1, *bars, units + slots - 1)
        yield tuple(right - left - 1 for left, right in zip(points, points[1:]))


def upper_widths(h, cut, vacancies):
    interior = 32 - h
    if (h, cut) == (16, 18):
        for tail in range(5):
            for lead, first, top in width_parts(vacancies - tail, 3):
                for rest in width_parts(tail, interior - 1):
                    yield lead, (first, *rest), top
        return
    forced_first_zero = (h, cut) == (14, 19)
    interior_totals = {
        (14, 18): range(2),
        (14, 19): (2,),
        (15, 18): range(3),
        (15, 19): (2, 3),
        (16, 19): range(vacancies + 1),
    }[h, cut]
    for units in interior_totals:
        for lead, top in width_parts(vacancies - units, 2):
            for middle in width_parts(units, interior - int(forced_first_zero)):
                yield lead, ((0, *middle) if forced_first_zero else middle), top


def width_rows(h, cut):
    lower_vacancies = cut - 1 - h
    upper_vacancies = 8 + h - cut  # Excludes required vacancy 41.
    for left, *middle, tail in width_parts(lower_vacancies, h + 1):
        for lead, right, top in upper_widths(h, cut, upper_vacancies):
            yield left + 1, (0, *middle, tail + lead, *right), top + 1


def old_resources(h, cut, a, gaps, b, intervals, budget):
    cumulative = tuple(accumulate(gaps, initial=0))
    labels = tuple(a + x + cumulative[x + 1] for x in range(33))
    threshold = cut + 2
    assert labels[h - 1] < cut <= labels[h] and labels[-1] == 41 - b
    used = []
    for rank, first, last in intervals:
        budget.count("fixed_edge_checks")
        value = rank + cumulative[last + 1] - cumulative[first]
        if (value >= threshold) != (first <= h <= last):
            return None
        used.append(value)
    if len(set(used)) != 32:
        return None
    budget.count("fixed_edge_checks")
    if a in used or a >= cut or a >= threshold:
        return None
    fresh = frozenset(range(1, 42)) - set(labels)
    free = frozenset(range(1, 42)) - set(used) - {a}
    order = "rank_preserving" if all(x < y for x, y in zip(used, used[1:])) else "rank_changing"
    return labels, fresh, free, order


def role_plans(fresh, weights, cut, x, y, z, budget):
    lower = fresh & set(range(1, cut))
    upper = fresh - lower
    threshold = cut + 2
    for chosen_lower in combinations(sorted(lower), z):
        for chosen_upper in combinations(sorted(upper - {41}), x + y - 1):
            budget.count("placement_attempts")
            budget.check_time()
            low_children = frozenset(chosen_lower)
            high_children = frozenset((*chosen_upper, 41))
            children = low_children | high_children
            for center in children:
                budget.count("fixed_edge_checks")
                if center not in weights or (center >= cut) != (center >= threshold):
                    break
            else:
                low_terminals = lower - low_children
                upper_terminals = upper - high_children
                terminal_weights = weights - children
                lo = frozenset(d for d in terminal_weights if d < threshold)
                hi = terminal_weights - lo
                if len(lo) != x:
                    continue
                for upper_x in combinations(sorted(high_children), x):
                    upper_y = high_children - set(upper_x)
                    for terminal_z in combinations(sorted(upper_terminals), z):
                        budget.count("placement_attempts")
                        budget.check_time()
                        terminal_x = upper_terminals - set(terminal_z)
                        if sum(hi) != sum(upper_y) - sum(low_terminals) + sum(terminal_z) - sum(low_children):
                            continue
                        imbalance = sum(terminal_x) - sum(upper_x)
                        if not any(sum(sign * d for sign, d in zip(signs, sorted(lo))) == imbalance
                                   for signs in product((-1, 1), repeat=x)):
                            continue
                        groups = [
                            (upper_x, tuple(sorted(terminal_x)), False),
                            (tuple(sorted(upper_y)), tuple(sorted(low_terminals)), True),
                            (tuple(sorted(low_children)), terminal_z, True),
                        ]
                        plan = sorted((c, candidates, crosses)
                                      for children_in_group, candidates, crosses in groups
                                      for c in children_in_group)
                        yield tuple(plan), terminal_weights


def match_plan(plan, depth, used_terminals, residual, threshold, budget):
    budget.count("allocation_states")
    budget.live(3 + depth)
    budget.check_time()
    if depth == len(plan):
        return () if not residual else None
    center, candidates, crosses = plan[depth]
    for terminal in candidates:
        if terminal in used_terminals:
            continue
        budget.count("pair_trials")
        d = abs(center - terminal)
        if d not in residual or (d >= threshold) != crosses:
            continue
        suffix = match_plan(plan, depth + 1, used_terminals | {terminal}, residual - {d},
                            threshold, budget)
        if suffix is not None:
            return ((center, terminal), *suffix)
    return None


def primary_search(menu, limits):
    """Only callable in a future separately authorized run with the frozen menu."""
    budget = Budget(limits)
    by_stream = {}
    try:
        for variant in ("B", "C"):
            prefix = menu[variant]
            old = prefix["state"]["minimum_labels"]
            names = sorted(old, key=old.__getitem__)
            intervals = tuple((r["rank"], r["first_cut"], r["last_cut"])
                              for r in prefix["minimum_rank_intervals"])
            for h, cut, x, y, z in CASES:
                stream = {"geometry_entries": 0, "rank_preserving": 0, "rank_changing": 0}
                by_stream[f"{variant}:{h}:{cut}"] = stream
                for a, gaps, b in width_rows(h, cut):
                    budget.count("geometry_entries")
                    stream["geometry_entries"] += 1
                    budget.live(1)
                    budget.check_time()
                    old_data = old_resources(h, cut, a, gaps, b, intervals, budget)
                    if old_data is None:
                        continue
                    images, fresh, weights, rank = old_data
                    stream[rank] += 1
                    for plan, terminal_weights in role_plans(fresh, weights, cut, x, y, z, budget):
                        pairs = match_plan(plan, 0, frozenset(), terminal_weights, cut + 2, budget)
                        if pairs is None:
                            continue
                        labels = dict(zip(names, images, strict=True))
                        labels["s:6"] = 0
                        for j, (center, terminal) in enumerate(pairs):
                            labels[f"b:6:{j}"] = center
                            labels[f"l:6:{j}:0"] = terminal
                        return {"status": "CANDIDATE", "variant": variant, "labels": labels,
                                "cut": cut, "induced_old_cut": h, "rank_class": rank,
                                "streams": by_stream, "counters": budget.receipt()}
        return {"status": "EXHAUSTED", "streams": by_stream, "counters": budget.receipt()}
    except LimitReached as error:
        return {"status": "INCOMPLETE", "limit": str(error), "streams": by_stream,
                "counters": budget.receipt()}
