"""Exact R226 completion of a supplied core at two fixed physical hosts.

This is a consumer of independently supplied core labels.  It neither chooses
those labels nor treats a failed fixed-core completion as nongracefulness.
The difference multigraph is processed structurally, without solution search.
"""

from __future__ import annotations

from collections import defaultdict, deque

from .model import graph_digest, validate_graph


MDL_COMMIT = "858a8c1fcfda87ba40bb1adee498a6131504a803"
SOURCE = (f"https://github.com/drkmtr1/Math-Discovery-Lab/blob/{MDL_COMMIT}/"
          "research/candidates/volume-010.md#n226-researcher")


def complete_two_host(graph: dict, core_labels: dict[str, int], hosts: tuple[str, str]) -> dict:
    """Complete only named pendant vertices at the supplied pair of hosts.

    Return SAT with a full labeling, RESTRICTED_INFEASIBLE for an exact
    fixed-core obstruction, or INVALID_INPUT for an unsupported/malformed
    instance.  Zero quotas remain in the quota-free difference graph.  Hosts
    need not be adjacent.  The allocation stage takes O(Q log Q) time and
    O(Q) storage, where Q is the number of unassigned leaves.  Graph
    validation and identity binding add O(|V| log |V|) time for this tree.
    """
    restrictions = {
        "fixed_core_labels": dict(core_labels) if isinstance(core_labels, dict) else None,
        "hosts": list(hosts) if isinstance(hosts, (tuple, list)) else None,
        "target_incidence_preserved": True,
        "supplies_core_labels": False,
        "ordinary_nongracefulness_claim": False,
        "domain": "lobster target; connected fixed core; unassigned leaves at two hosts",
        "source": SOURCE,
    }

    def result(status: str, reason: str, *, labels: dict | None = None,
               details: dict | None = None) -> dict:
        return {"status": status, "labels": labels, "method": "r226",
                "details": {"reason": reason, **(details or {})},
                "restrictions": restrictions}

    validation = validate_graph(graph)
    if not validation["valid"]:
        return result("INVALID_INPUT", "invalid target graph", details=validation)
    restrictions["graph_digest"] = graph_digest(graph)
    vertices, m = set(graph["vertices"]), validation["m"]
    adjacency = {v: set() for v in vertices}
    for x, y in graph["edges"]:
        adjacency[x].add(y)
        adjacency[y].add(x)
    if not isinstance(core_labels, dict) or not core_labels:
        return result("INVALID_INPUT", "core_labels must be a nonempty object")
    if any(not isinstance(v, str) or v not in vertices for v in core_labels):
        return result("INVALID_INPUT", "core_labels contains an unknown/non-string vertex")
    if any(type(x) is not int or not 0 <= x <= m for x in core_labels.values()):
        return result("INVALID_INPUT", "every core label must be an integer in 0..m; booleans are rejected")
    if len(set(core_labels.values())) != len(core_labels):
        return result("INVALID_INPUT", "core labels must be injective")
    if (not isinstance(hosts, (tuple, list)) or len(hosts) != 2
            or any(not isinstance(v, str) or v not in core_labels for v in hosts)
            or hosts[0] == hosts[1]):
        return result("INVALID_INPUT", "hosts must be two distinct already-labeled actual vertices")

    core = set(core_labels)
    seen, pending = {hosts[0]}, [hosts[0]]
    while pending:
        current = pending.pop()
        for neighbor in (adjacency[current] & core) - seen:
            seen.add(neighbor)
            pending.append(neighbor)
    if seen != core:
        return result("INVALID_INPUT", "the induced labeled core must be connected")
    core_differences = [abs(core_labels[x] - core_labels[y])
                        for x, y in graph["edges"] if x in core and y in core]
    if len(set(core_differences)) != len(core_differences):
        return result("INVALID_INPUT", "actual core-edge differences must be distinct")

    u, v = sorted(hosts, key=core_labels.__getitem__)
    a, b = core_labels[u], core_labels[v]
    leaves: dict[str, list[str]] = {u: [], v: []}
    for leaf in sorted(vertices - core):
        neighbors = adjacency[leaf]
        if len(neighbors) != 1 or not neighbors <= {u, v}:
            return result("INVALID_INPUT", "every unassigned vertex must be a leaf at one of the two fixed hosts")
        leaves[next(iter(neighbors))].append(leaf)
    quota = {u: len(leaves[u]), v: len(leaves[v])}
    restrictions["host_quotas"] = quota
    restrictions["ordered_hosts_by_label"] = [u, v]
    X = sorted(set(range(m + 1)) - set(core_labels.values()))
    D = sorted(set(range(1, m + 1)) - set(core_differences))
    if len(X) != len(D) or len(X) != sum(quota.values()):
        raise ArithmeticError("validated tree/core inventories do not agree")
    detail = {"unused_labels": X, "unused_differences": D,
              "ordered_hosts": [u, v], "host_labels": [a, b], "components": []}

    # Every unused label contributes one half-edge, ordinary edge, or loop.
    # Every unused difference is retained, including isolated differences.
    options: dict[int, list[tuple[str, int]]] = {}
    ordinary: dict[int, list[tuple[int, int]]] = {d: [] for d in D}
    half_at: dict[int, list[int]] = defaultdict(list)
    loops_at: dict[int, list[int]] = defaultdict(list)
    difference_set = set(D)
    for x in X:
        row = [(host, abs(x - core_labels[host])) for host in (u, v)
               if abs(x - core_labels[host]) in difference_set]
        options[x] = row
        if not row:
            return result("RESTRICTED_INFEASIBLE", "an unused label has no eligible host/difference",
                          details={**detail, "rejected_label": x})
        if len(row) == 1:
            half_at[row[0][1]].append(x)
        elif row[0][1] == row[1][1]:
            loops_at[row[0][1]].append(x)
        else:
            d1, d2 = row[0][1], row[1][1]
            ordinary[d1].append((d2, x))
            ordinary[d2].append((d1, x))

    # Allocation maps each label VALUE to its physical host.  Actual named
    # leaves are assigned only after the two host quotas have been checked.
    forced: dict[int, str] = {}
    free_pairs: list[tuple[int, int]] = []
    midpoint: list[int] = []
    remaining = set(D)
    for start in D:
        if start not in remaining:
            continue
        component, queue = {start}, deque([start])
        while queue:
            d = queue.popleft()
            for neighbor, _ in ordinary[d]:
                if neighbor not in component:
                    component.add(neighbor)
                    queue.append(neighbor)
        remaining -= component
        edge_labels = {x for d in component for _, x in ordinary[d]}
        half_labels = sorted(x for d in component for x in half_at[d])
        loop_labels = sorted(x for d in component for x in loops_at[d])
        n, e, t = len(component), len(edge_labels) + len(loop_labels), len(half_labels)
        component_detail = {"differences": sorted(component), "n": n, "e": e, "t": t,
                            "labels": sorted(edge_labels | set(half_labels) | set(loop_labels))}
        detail["components"].append(component_detail)
        if e + t != n:
            return result("RESTRICTED_INFEASIBLE", "difference component fails label/difference balance",
                          details=detail)

        excluded: set[int] = set()
        roots: set[int]
        if t == 1:
            if loop_labels or e != n - 1:
                raise ArithmeticError("R226 tree/half-edge classification invariant failed")
            x = half_labels[0]
            host, root = options[x][0]
            forced[x] = host
            roots = {root}
            component_detail["kind"] = "tree_with_forced_half_edge"
        elif t == 0:
            if e != n:
                raise ArithmeticError("R226 unicyclic component invariant failed")
            if loop_labels:
                if len(loop_labels) != 1:
                    raise ArithmeticError("more than one midpoint in one component")
                x = loop_labels[0]
                midpoint.append(x)
                roots = {options[x][0][1]}
                component_detail["kind"] = "midpoint_loop"
                component_detail["free_midpoint"] = x
            else:
                pairs: dict[tuple[int, int], list[int]] = defaultdict(list)
                for x in sorted(edge_labels):
                    pair = tuple(sorted((options[x][0][1], options[x][1][1])))
                    pairs[pair].append(x)
                doubled = [(ends, xs) for ends, xs in pairs.items() if len(xs) == 2]
                if len(doubled) != 1 or any(len(xs) > 2 for xs in pairs.values()):
                    raise ArithmeticError("R226 geometry did not produce a unique parallel pair")
                ends, pair = doubled[0]
                x, y = pair
                if x + y != a + b:
                    raise ArithmeticError("parallel labels are not a reflected pair")
                free_pairs.append((x, y))
                roots, excluded = set(ends), set(pair)
                component_detail["kind"] = "reflected_parallel_pair"
                component_detail["free_pair"] = pair
        else:
            raise ArithmeticError("balanced connected component has more than one half-edge")

        # Rooted trees are forced outward.  On a cycle component, deleting
        # the cycle leaves trees rooted at the one or two cycle vertices.
        visited, used_edges = set(roots), set(excluded)
        queue = deque(sorted(roots))
        newly_forced = list(half_labels)
        while queue:
            d = queue.popleft()
            for neighbor, x in ordinary[d]:
                if x in used_edges:
                    continue
                used_edges.add(x)
                if neighbor in visited:
                    raise ArithmeticError("noncycle R226 edges did not form rooted trees")
                visited.add(neighbor)
                queue.append(neighbor)
                host_choices = [host for host, difference in options[x] if difference == neighbor]
                if len(host_choices) != 1:
                    raise ArithmeticError("forced edge has ambiguous destination host")
                forced[x] = host_choices[0]
                newly_forced.append(x)
        if visited != component or used_edges != edge_labels:
            raise ArithmeticError("R226 extraction did not process the complete component")
        component_detail["forced"] = [{"label": x, "host": forced[x]}
                                      for x in sorted(newly_forced)]

    if len(midpoint) > 1:
        raise ArithmeticError("two distinct midpoint labels contradict host geometry")
    c, eta = len(free_pairs), len(midpoint)
    A0 = sum(host == u for host in forced.values())
    low, high = A0, A0 + 2 * c + eta
    delta = quota[u] - A0
    epsilon = delta % 2 if eta else 0
    j = (delta - epsilon) // 2
    detail.update({"A0": A0, "c": c, "eta": eta,
                   "fractional_quota_interval": [low, high],
                   "integral_quota_rule": "A0 + 2*j + epsilon; 0<=j<=c; 0<=epsilon<=eta",
                   "requested_lower_label_host_quota": quota[u],
                   "free_pairs": [list(pair) for pair in free_pairs], "midpoint_labels": midpoint})
    if not (low <= quota[u] <= high and delta - epsilon == 2 * j and 0 <= j <= c):
        return result("RESTRICTED_INFEASIBLE", "fixed host quota fails the R226 interval/parity criterion",
                      details=detail)

    assignment = dict(forced)
    for i, pair in enumerate(free_pairs):
        for x in pair:
            assignment[x] = u if i < j else v
    if midpoint:
        assignment[midpoint[0]] = u if epsilon else v
    labels = dict(core_labels)
    for host in (u, v):
        values = sorted(x for x, assigned_host in assignment.items() if assigned_host == host)
        if len(values) != quota[host]:
            raise ArithmeticError("R226 extraction did not meet the actual host quota")
        labels.update(zip(leaves[host], values))
    # Development assertions only; the independent verifier remains mandatory
    # for accepting this returned witness as a checked certificate.
    if (set(labels) != vertices or sorted(labels.values()) != list(range(m + 1))
            or sorted(abs(labels[x] - labels[y]) for x, y in graph["edges"]) != list(range(1, m + 1))):
        raise ArithmeticError("R226 extraction violated the full target inventory")
    detail.update({"chosen_pair_count_for_lower_host": j, "chosen_midpoint_for_lower_host": epsilon,
                   "allocation": [{"label": x, "host": assignment[x]} for x in sorted(assignment)]})
    return result("SAT", "R226 structural extraction supplies the fixed target", labels=labels, details=detail)
