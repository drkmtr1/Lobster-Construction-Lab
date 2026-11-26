"""Inactive D204 primary: width vectors, exact old ranks, forced children."""

from itertools import accumulate, combinations

from .budget import Budget, LimitReached


def weak_parts(total, count):
    for bars in combinations(range(total + count - 1), count - 1):
        boundaries = (-1, *bars, total + count - 1)
        yield tuple(right - left - 1 for left, right in zip(boundaries, boundaries[1:]))


def width_rows():
    # C=18: lower parts are A-1, gaps 1..13 and the lower part of gap 14.
    # Upper parts are the upper part of gap 14, gaps 15..32 and B-1.
    for lower in weak_parts(3, 15):
        for upper in weak_parts(4, 20):
            yield 18, lower[0] + 1, upper[-1] + 1, (
                0, *lower[1:-1], lower[-1] + upper[0], *upper[1:-1]
            )
    # C=19: all three upper vacancies other than 41 are gaps at 17..32.
    for lower in weak_parts(4, 15):
        for upper in weak_parts(3, 16):
            yield 19, lower[0] + 1, 1, (0, *lower[1:], 0, 0, *upper)


def old_geometry(origin, lower_exterior, upper_exterior, gaps, intervals, budget):
    cumulative = tuple(accumulate(gaps, initial=0))
    old_labels = tuple(lower_exterior + x + cumulative[x + 1] for x in range(33))
    if origin == 19 and old_labels[13] < 18 <= old_labels[14]:
        # The complete C=18 generator also visits this geometry.
        return None
    cuts = set()
    if old_labels[13] < 18 <= old_labels[14]:
        cuts.add(18)
    if upper_exterior == 1 and old_labels[14:17] == (19, 20, 21):
        cuts.add(19)
    if not cuts:
        return None
    old_weights = []
    for rank, first, last in intervals:
        budget.count("fixed_edge_checks")
        weight = rank + cumulative[last + 1] - cumulative[first]
        old_weights.append(weight)
        crosses = first <= 14 <= last
        cuts = {cut for cut in cuts if crosses == (weight >= cut + 2)}
        if not cuts:
            return None
    if len(set(old_weights)) != 32:
        return None
    free_weights = frozenset(range(1, 42)) - set(old_weights)
    budget.count("fixed_edge_checks")
    if lower_exterior not in free_weights:
        return None
    cuts = frozenset(cut for cut in cuts if lower_exterior < cut + 2 and lower_exterior < cut)
    if not cuts:
        return None
    free_labels = frozenset(range(1, 41)) - set(old_labels)
    # 41 is fresh and w=0; both endpoint vacancies are guaranteed by A,B.
    arm_labels = free_labels | {41}
    return old_labels, tuple(old_weights), arm_labels, free_weights - {lower_exterior}, cuts


def forced_plans(cut, arm_labels, weights, budget):
    lower = frozenset(x for x in arm_labels if x < cut)
    upper = arm_labels - lower
    lo_weights = frozenset(w for w in weights if w < cut + 2)
    hi_weights = weights - lo_weights
    if cut == 18 and len(lower) == 3 and len(upper) == 5 and len(lo_weights) == 1:
        low_weight, = lo_weights
        total = 2 * sum(upper) - sum(lower) - sum(hi_weights)
        for sign in (-1, 1):
            budget.count("placement_attempts")
            numerator = total - sign * low_weight
            if numerator % 3:
                continue
            terminal = numerator // 3
            parent = terminal + sign * low_weight
            if terminal != 41 and terminal in upper and parent in upper:
                yield tuple(sorted(upper - {terminal})), ((parent, terminal),)
    elif cut == 19 and len(lower) == len(upper) == 4 and len(lo_weights) == 2:
        budget.count("placement_attempts")
        other = sum(hi_weights) - sum(upper) + sum(lower) - 41
        if lo_weights <= lower and other in upper - {41}:
            yield tuple(sorted(lo_weights | {41, other})), ()


def compatible_cuts(cuts, first, second, weight):
    return frozenset(
        cut for cut in cuts
        if ((first < cut) != (second < cut)) == (weight >= cut + 2)
    )


def remove_fixed(centers, fixed_pairs, weights, cuts, budget):
    for first, second in (*((0, x) for x in centers), *fixed_pairs):
        budget.count("fixed_edge_checks")
        weight = abs(first - second)
        cuts = compatible_cuts(cuts, first, second, weight)
        if weight not in weights or not cuts:
            return None
        weights = weights - {weight}
    return weights, cuts


def terminal_match(centers, terminals, weights, cuts, budget, depth=0):
    budget.count("allocation_states")
    budget.live(3 + depth)
    budget.check_time()
    if not centers:
        return () if not terminals and not weights else None
    child, *rest = centers
    for terminal in sorted(terminals):
        # Every remaining terminal edge in either cut's plan crosses.
        pair_cuts = frozenset(cut for cut in cuts if (child < cut) != (terminal < cut))
        if not pair_cuts:
            continue
        budget.count("pair_trials")
        weight = abs(child - terminal)
        pair_cuts = compatible_cuts(pair_cuts, child, terminal, weight)
        if weight in weights and pair_cuts:
            tail = terminal_match(rest, terminals - {terminal}, weights - {weight},
                                  pair_cuts, budget, depth + 1)
            if tail is not None:
                return ((child, terminal), *tail)
    return None


def primary_search(prefix, limits):
    """Only invoke under separately granted Owner authorization for the frozen input."""
    ordered_names = tuple(sorted(prefix["state"]["minimum_labels"],
                                 key=prefix["state"]["minimum_labels"].__getitem__))
    intervals = tuple((row["rank"], row["first_cut"], row["last_cut"])
                      for row in prefix["rank_intervals"])
    budget = Budget(limits)
    compatible = {"rank_preserving": 0, "rank_changing": 0}
    try:
        for origin, a, b, gaps in width_rows():
            budget.count("geometry_entries")
            budget.live(1)
            budget.check_time()
            old = old_geometry(origin, a, b, gaps, intervals, budget)
            if old is None:
                continue
            labels, weights, arms, free, cuts = old
            kind = ("rank_preserving" if all(x < y for x, y in zip(weights, weights[1:]))
                    else "rank_changing")
            compatible[kind] += 1
            for cut in sorted(cuts):
                for children, fixed in forced_plans(cut, arms, free, budget):
                    budget.check_time()
                    reserved = remove_fixed(children, fixed, free, frozenset({cut}), budget)
                    if reserved is None:
                        continue
                    residual, mask = reserved
                    fixed_children = {x for x, _ in fixed}
                    fixed_terminals = {y for _, y in fixed}
                    parents = tuple(x for x in children if x not in fixed_children)
                    remaining = arms - set(children) - fixed_terminals
                    matching = terminal_match(parents, remaining, residual, mask, budget)
                    if matching is not None:
                        assignment = dict(zip(ordered_names, labels, strict=True))
                        assignment["s:6"] = 0
                        for i, (child, terminal) in enumerate(sorted((*fixed, *matching))):
                            assignment[f"b:6:{i}"] = child
                            assignment[f"l:6:{i}:0"] = terminal
                        return {"status": "CANDIDATE", "labels": assignment, "cut": cut,
                                "admissible_old_cuts": sorted(cuts), "rank_class": kind,
                                "compatible_rank_counts": compatible, "counters": budget.receipt()}
        return {"status": "EXHAUSTED", "compatible_rank_counts": compatible,
                "counters": budget.receipt()}
    except LimitReached as error:
        return {"status": "INCOMPLETE", "limit": str(error),
                "compatible_rank_counts": compatible, "counters": budget.receipt()}
