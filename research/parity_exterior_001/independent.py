"""Independent count-first exterior traversal and certificate audit."""
from itertools import combinations, permutations, product


def physical_groups(row, prefix, retained):
    parents, roles, core, optional, sides, v, u, w = retained.shape(row, prefix)
    profile = row["suffix"]
    if tuple((sum(q > 0 for q in part), part.count(0)) for part in profile) != ((2, 0), (2, 1)):
        raise ValueError("independent physical topology outside study")
    centers = tuple(
        tuple(sorted((name for name in core if parents[name] == spine and roles[name]["kind"] == "branch"),
                     key=lambda name: roles[name]["branch"]))
        for spine in (u, w)
    )
    if tuple(map(len, centers)) != (2, 2):
        raise ValueError("independent centers")
    direct, = (name for name in optional if roles[name]["kind"] == "branch")
    if parents[direct] != w:
        raise ValueError("independent direct parent")
    groups = {host: tuple(sorted((name for name in optional if roles[name]["kind"] == "leaf"
                                 and parents[name] == host), key=lambda name: roles[name]["leaf"]))
              for pair in centers for host in pair}
    return parents, roles, optional, v, u, w, centers, direct, groups


def negative(row, prefix, arm, meter, retained):
    if arm not in ("T", "E"):
        raise ValueError("unknown independent arm")
    parents, _, _, v, u, w, centers, direct, groups = physical_groups(row, prefix, retained)
    hosts = centers[0] + centers[1]
    K = row["fresh"]//2
    attempted_counts = (range(1) if arm == "T" else range(len(groups[host])+1) for host in hosts)
    completed = 0
    for a0, a1, b0, b1 in product(*attempted_counts):
        for e in (0, 1):
            meter.tick("exterior_nodes")
            A, B = 3+b0+b1, 3+e+a0+a1
            if A+B > K:
                continue
            s = 2*K-A-B
            high_named = centers[1] + ((direct,) if e else ())
            for low_centers in permutations(range(1, A), 2):
                meter.tick("exterior_nodes")
                low_free = tuple(j for j in range(1, A) if j not in low_centers)
                for high_centers in permutations(range(A+2, A+B+1), len(high_named)):
                    meter.tick("exterior_nodes")
                    high_free = tuple(j for j in range(A+2, A+B+1) if j not in high_centers)
                    fixed = {v: A, u: A+1, w: 0, **dict(zip(centers[0], low_centers)),
                             **dict(zip(high_named, high_centers))}
                    for low_first in combinations(low_free, b0):
                        meter.tick("exterior_nodes")
                        low_last = tuple(j for j in low_free if j not in low_first)
                        for high_first in combinations(high_free, a0):
                            meter.tick("exterior_nodes")
                            high_last = tuple(j for j in high_free if j not in high_first)
                            partitions = (high_first, high_last, low_first, low_last)
                            reduced = dict(fixed)
                            for host, labels in zip(hosts, partitions):
                                reduced.update(zip(groups[host], labels))
                            weights = sorted(abs(value - reduced[parents[name]]) for name, value in reduced.items()
                                             if name != v)
                            if weights != list(range(1, A+B+1)):
                                continue
                            completed += 1
                            quotas = [0]*(A+B)
                            quotas[0] = 1-e
                            for host, selected in zip(hosts, partitions):
                                label = fixed[host]
                                quotas[label if label < A else label-1] = len(groups[host])-len(selected)
                            if retained.raw_support(A, B, s, quotas, meter):
                                raise ValueError("independent exact audit found feasible support for a claimed negative")
    return {"audit": "independent-exhaustion", "independent_representative_exteriors": completed}


def positive(row, prefix, arm, witness, verify_certificate, retained):
    checked = retained.positive(row, prefix, arm, witness, verify_certificate)
    parents, roles, _, _, _, _, _, _, _ = physical_groups(row, prefix, retained)
    reduced = witness["reduced"]
    k_total = row["fresh"]//2
    exterior_edges = [
        {"child": name, "parent": parents[name], "weight": abs(label-reduced[parents[name]])}
        for name, label in sorted(reduced.items()) if name != prefix["frontier"]
    ]
    hosts = {}
    for name, host, _, image in witness["gap"]:
        summary = hosts.setdefault(host, {"crossing": 0, "noncrossing": 0, "gap_leaves": 0})
        summary["gap_leaves"] += 1
        summary["crossing" if image >= k_total else "noncrossing"] += 1
    terminals = {}
    for name in reduced:
        if roles[name]["kind"] == "leaf":
            host = parents[name]
            terminals[host] = terminals.get(host, 0)+1
    checked.update(reduced_edges=exterior_edges, gap_by_parent=hosts, exterior_terminals_by_parent=terminals,
                   noncrossing_weights=list(range(1, prefix["d"]+k_total)))
    return checked
