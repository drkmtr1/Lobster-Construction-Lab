"""Reviewed strict-phase algorithms. This module has no campaign entry point."""

from itertools import product


def exterior_representatives(record, charge):
    """Yield complete parent-first reduced embeddings with exact edge spectrum."""
    if record["phase"] != "S0":
        raise ValueError("strict-phase records only")
    graph = record["graph"]
    v, u, w = graph["spine"][-3:]
    fixed = []
    hosts = []
    by_host = {}
    for row, spine in zip(record["suffix"], (u, w)):
        section = graph["roles"][spine]["section"]
        for i, quota in enumerate(row):
            child = f"b:{section}:{i}"
            fixed.append((child, spine, spine == w))
            if quota:
                hosts.append((child, spine == w))
                by_host[child] = [f"l:{section}:{i}:{t}" for t in range(quota)]
    lower = [host for host, upper in hosts if not upper]
    upper = [host for host, upper in hosts if upper]
    quotas = [len(by_host[host]) for host in upper]
    R = sum(quotas)
    K = record["fresh_edges"] // 2
    B = len(record["suffix"][1]) + 2
    for first in lower:
        for counts in product(*(range(q + 1) for q in quotas)):
            charge("primary_exterior_attempts")
            e2 = sum(counts)
            if not 1 <= e2 <= R // 2 - 2:
                continue
            A = 4 + e2
            s = 2 * K - A - B
            if s < K or not A <= K <= A + s:
                continue
            selected = {first: 1, **dict(zip(upper, counts))}
            vertices = [*fixed]
            gap = {}
            for host, is_upper in hosts:
                count = selected.get(host, 0)
                vertices.extend((name, host, not is_upper) for name in by_host[host][:count])
                gap[host] = by_host[host][count:]
            labels = {v: A, u: A + 1, w: 0}
            free = (set(range(1, A)), set(range(A + 2, A + B + 1)))
            used = {1, A + 1}

            def place(depth):
                if depth == len(vertices):
                    if len(used) == A + B:
                        yield A, B, s, labels.copy(), gap
                    return
                name, parent, is_upper = vertices[depth]
                for value in sorted(free[is_upper]):
                    charge("primary_exterior_attempts")
                    weight = abs(labels[parent] - value)
                    if weight in used:
                        continue
                    labels[name] = value
                    free[is_upper].remove(value)
                    used.add(weight)
                    yield from place(depth + 1)
                    used.remove(weight)
                    free[is_upper].add(value)
                    del labels[name]

            yield from place(0)


def exact_support(A, B, s, reduced, gap, charge, live):
    """Finite Boolean support using a full image mask and exact remaining quotas."""
    K = (A + B + s) // 2
    hosts = tuple(sorted(gap))
    initial = tuple(len(gap[host]) for host in hosts)
    arcs = {}
    for i in range(s):
        choices = []
        for h, host in enumerate(hosts):
            charge("primary_transitions")
            j = reduced[host]
            upper = j > A
            image = s + (j - A) - i if upper else i + A - 2 - j
            crossing = (i < K - A) == upper
            if initial[h] and 0 <= image < s and (image >= K) == crossing:
                choices.append((h, image))
        arcs[i] = choices
    order = sorted(arcs, key=lambda i: (len(arcs[i]), i))
    dead = set()
    assignment = []

    def extend(depth, mask, remaining):
        key = (depth, mask, remaining)
        charge("primary_states")
        live(len(dead) + depth + 1)
        if key in dead:
            return False
        if depth == s:
            return mask == (1 << s) - 1 and not any(remaining)
        source = order[depth]
        for h, image in arcs[source]:
            charge("primary_transitions")
            bit = 1 << image
            if mask & bit or remaining[h] == 0:
                continue
            updated = list(remaining)
            updated[h] -= 1
            assignment.append((source, hosts[h], image))
            if extend(depth + 1, mask | bit, tuple(updated)):
                return True
            assignment.pop()
        if key not in dead:
            live(len(dead) + depth + 2)
            dead.add(key)
        return False

    if extend(0, 0, initial):
        return sorted(assignment)
    return None


def named_witness(record, prefix, exterior, assignment):
    """Expand a successful normalized assignment on the exact original."""
    A, B, s, reduced, gap = exterior
    K = record["fresh_edges"] // 2
    n, c = prefix["edges"], prefix["minimum_cut"]
    m = n + 2 * K
    minimum = {}
    for name, actual in prefix["actual_labels"].items():
        value = n - actual
        minimum[name] = value + A + (s if value >= c else 0)
    minimum.update({name: value + (n + s if value > A else 0) for name, value in reduced.items()})
    next_leaf = {host: iter(names) for host, names in gap.items()}
    arrows = []
    for source, host, image in sorted(assignment):
        leaf = next(next_leaf[host])
        minimum[leaf] = A + c + source
        arrows.append([leaf, host, source, image])
    return {"A": A, "B": B, "s": s, "reduced": reduced, "gap": arrows,
            "labels": {name: m - value for name, value in minimum.items()}}
