"""Unexecuted residual-label consumer for the single frozen D197 odd target."""

from itertools import permutations

from .budget import Budget


def _geometries(budget):
    prefix = budget.prefix["minimum_labels"]
    old_edges = budget.original["prefix_graph"]["edges"]
    for r in range(1, 16):
        d_r = budget.thresholds[r]
        for a in range(16):
            for s in range(16 - a):
                b = 15 - a - s
                for frontier, cut in ((0, 14), (30, 17)):
                    budget.charge("primary", "geometries")
                    if s == 0 or (frontier == 0 and a == 0) or (frontier == 30 and b == 0):
                        continue
                    placed = {name: a + value + s * (value >= r) for name, value in prefix.items()}
                    h = sum(value < cut for value in placed.values())
                    if not 1 <= h <= 15:
                        continue
                    d_h = budget.thresholds[h]
                    if d_h < d_r:
                        continue
                    if d_h == d_r:
                        if s < 16 - d_r:
                            continue
                    elif s != 16 - d_h:
                        continue
                    actual = set()
                    for u, v in old_edges:
                        left, right = placed[u], placed[v]
                        weight = abs(left - right)
                        if weight in actual or ((left < cut) != (right < cut)) != (weight >= 16):
                            break
                        actual.add(weight)
                    else:
                        expected = set(range(1, d_r)) | set(range(d_r + s, 16 + s))
                        free = set(range(31)) - set(placed.values())
                        prescribed = (set(range(a)) | set(range(a + r, a + r + s))
                                      | set(range(16 + a + s, 31)))
                        if actual != expected or free != prescribed or frontier not in free:
                            raise ValueError("Old alphabet identity failed")
                        yield r, h, a, b, s, frontier, cut, placed, free, actual


def _residual_label_support(labels, weights, parents, quotas, cut, budget):
    """Return the parent index at each ordered residual label, or None."""
    index_of_weight = {weight: j for j, weight in enumerate(sorted(weights))}
    options = []
    for label in labels:
        row = []
        for parent, parent_label in enumerate(parents):
            budget.charge("primary", "transitions")
            weight = abs(label - parent_label)
            if weight in index_of_weight and ((label < cut) != (parent_label < cut)) == (weight >= 16):
                row.append((parent, 1 << index_of_weight[weight]))
        options.append(row)

    exhausted = set()
    assignments = []

    def visit(mask, remaining):
        budget.charge("primary", "states")
        depth = len(assignments)
        budget.observe_live("primary", len(exhausted) + depth + 1)
        if depth == len(labels):
            return mask == (1 << len(weights)) - 1 and not any(remaining)
        state = (mask, remaining)
        if state in exhausted:
            return False
        for parent, bit in options[depth]:
            budget.charge("primary", "transitions")
            if mask & bit or remaining[parent] == 0:
                continue
            after = list(remaining)
            after[parent] -= 1
            assignments.append(parent)
            if visit(mask | bit, tuple(after)):
                return True
            assignments.pop()
        budget.observe_live("primary", len(exhausted) + depth + 2)
        exhausted.add(state)
        return False

    return tuple(assignments) if visit(0, tuple(quotas)) else None


def search_primary(budget: Budget):
    """Prospective Boolean support; Budget refuses the frozen D197 contract."""
    record = budget.original
    graph = record["original"]
    w = record["receiving_spine"]
    i = graph["roles"][w]["section"]
    v = budget.prefix["frontier"]
    children = [f"b:{i}:{j}" for j in range(4)]
    profile = graph["profile"][i]
    if profile != [2, 7, 0, 1]:
        raise ValueError("Unexpected registered profile")
    positive = [j for j, quota in enumerate(profile) if quota]
    quotas = [profile[j] for j in positive]

    for r, h, a, b, s, frontier, cut, before, free, old_weights in _geometries(budget):
        slots = free - {frontier}
        for child_values in permutations(sorted(slots), 4):
            budget.charge("primary", "raw_placements")
            used = set(old_weights)
            for value in (before[v], *child_values):
                difference = abs(value - frontier)
                crosses = (value < cut) != (frontier < cut)
                if difference not in range(1, 31) or difference in used or crosses != (difference >= 16):
                    break
                used.add(difference)
            else:
                parents = [child_values[j] for j in positive]
                labels = sorted(slots - set(child_values))
                weights = set(range(1, 31)) - used
                if len(labels) != 10 or len(weights) != 10:
                    raise ValueError("Residual palette size differs")
                picks = _residual_label_support(labels, weights, parents, quotas, cut, budget)
                if picks is None:
                    continue
                full = dict(before)
                full[w] = frontier
                full.update(zip(children, child_values, strict=True))
                by_parent = [[] for _ in positive]
                for label, parent in zip(labels, picks, strict=True):
                    by_parent[parent].append(label)
                for j, picked in zip(positive, by_parent, strict=True):
                    for terminal, label in enumerate(picked):
                        full[f"l:{i}:{j}:{terminal}"] = label
                return {
                    "status": "CANDIDATE", "labels": full, "r": r, "h": h,
                    "A": a, "B": b, "s": s, "frontier_label": frontier, "output_cut": cut,
                    "original_digest": record["original_digest"],
                    "prefix_digest": record["prefix_digest"],
                }
    return {"status": "EXHAUSTED", "engine": "primary"}
