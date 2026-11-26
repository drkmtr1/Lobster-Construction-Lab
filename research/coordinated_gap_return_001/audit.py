"""Inactive D204 audit: raw subsets and actual indexed arm recursion."""

from itertools import combinations

from .budget import Budget, LimitReached


def raw_subsets():
    # Cut 18 is checked directly with fourteen old vertices below it.
    for below in combinations(range(1, 18), 14):
        for above in combinations(range(18, 41), 19):
            yield 18, below + above
    # Cut 19 requires all of 19,20,21,40 in the old upper subset.
    for below in combinations(range(1, 19), 14):
        for middle in combinations(range(22, 40), 15):
            yield 19, (*below, 19, 20, 21, *middle, 40)


def physical_weight(first, second, cut):
    value = abs(first - second)
    crosses = min(first, second) < cut <= max(first, second)
    return value if crosses == (value >= cut + 2) else None


def audit_resources(labels, old_edges, cut, frontier_name, budget):
    observed = {}
    for first, second in old_edges:
        budget.count("fixed_edge_checks")
        weight = physical_weight(labels[first], labels[second], cut)
        if weight is None or weight in observed:
            return None
        observed[weight] = (first, second)
    budget.count("fixed_edge_checks")
    connector = physical_weight(0, labels[frontier_name], cut)
    if connector is None or connector in observed:
        return None
    return (frozenset(range(1, 42)) - set(labels.values()),
            frozenset(range(1, 42)) - set(observed) - {connector})


def can_finish_order(remaining, last, index, cut):
    if index == 4:
        return not remaining
    if 41 not in remaining:
        return False
    lower_centers = max(0, 2 - index) if cut == 19 else 0
    upper_centers = 4 - index - lower_centers
    eligible_lower = sum(last < label < cut for label in remaining)
    eligible_upper = sum(max(cut - 1, last) < label < 41 for label in remaining)
    return eligible_lower >= lower_centers and eligible_upper >= upper_centers - 1


def assign_arms(remaining, weights, cut, budget, index=0, last=-1):
    budget.count("allocation_states")
    budget.live(2 + index)
    budget.check_time()
    if index == 4:
        return () if not remaining and not weights else None
    for center in sorted(remaining):
        if center <= last or (center == 41) != (index == 3):
            continue
        upper_center = cut == 18 or index >= 2
        if (center >= cut) != upper_center:
            continue
        # Count each proposed center at a frame before trying its terminals.
        budget.count("placement_attempts")
        terminals = remaining - {center, 41}
        for terminal in sorted(terminals):
            if cut == 19 and (terminal >= cut) == upper_center:
                continue
            budget.count("pair_trials")
            a = physical_weight(0, center, cut)
            b = physical_weight(center, terminal, cut)
            leftover = remaining - {center, terminal}
            if (a not in weights or b not in weights or a == b
                    or not can_finish_order(leftover, center, index + 1, cut)):
                continue
            tail = assign_arms(leftover, weights - {a, b}, cut, budget, index + 1, center)
            if tail is not None:
                return ((center, terminal), *tail)
    return None


def audit_search(prefix, incoming_graph, limits):
    """Only invoke under separately granted Owner authorization for the frozen input."""
    old = prefix["state"]["minimum_labels"]
    names = tuple(sorted(old, key=old.__getitem__))
    old_edges = tuple(tuple(edge) for edge in incoming_graph["edges"])
    incoming_ranks = tuple(sorted(old_edges, key=lambda edge: abs(old[edge[0]] - old[edge[1]])))
    frontier = incoming_graph["spine"][-1]
    budget = Budget(limits)
    compatible = {"rank_preserving": 0, "rank_changing": 0}
    try:
        for cut, subset in raw_subsets():
            budget.count("geometry_entries")
            budget.live(1)
            budget.check_time()
            labels = dict(zip(names, subset, strict=True))
            resources = audit_resources(labels, old_edges, cut, frontier, budget)
            if resources is None:
                continue
            remaining, weights = resources
            signature = [abs(labels[u] - labels[v]) for u, v in incoming_ranks]
            kind = ("rank_preserving" if all(x < y for x, y in zip(signature, signature[1:]))
                    else "rank_changing")
            compatible[kind] += 1
            assignment = assign_arms(remaining, weights, cut, budget)
            if assignment is not None:
                labels["s:6"] = 0
                for i, (center, terminal) in enumerate(assignment):
                    labels[f"b:6:{i}"] = center
                    labels[f"l:6:{i}:0"] = terminal
                return {"status": "CANDIDATE", "labels": labels, "cut": cut,
                        "rank_class": kind, "compatible_rank_counts": compatible,
                        "counters": budget.receipt()}
        return {"status": "EXHAUSTED", "compatible_rank_counts": compatible,
                "counters": budget.receipt()}
    except LimitReached as error:
        return {"status": "INCOMPLETE", "limit": str(error),
                "compatible_rank_counts": compatible, "counters": budget.receipt()}
