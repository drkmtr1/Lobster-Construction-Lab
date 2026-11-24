"""Independent named-incidence audit for the frozen D102 original."""

from collections import Counter, deque
from hashlib import sha256
import json


def topology(original, expected_digest):
    graph = original["graph"]
    profile = [[4, 3], [2]]
    spine = ["s:0", "s:1"]
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    expected = Counter([tuple(spine)])
    for section, quotas in enumerate(profile):
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            expected[tuple(sorted((spine[section], center)))] += 1
            for leaf in range(quota):
                terminal = f"l:{section}:{branch}:{leaf}"
                roles[terminal] = {"kind": "leaf", "section": section, "branch": branch, "leaf": leaf}
                expected[tuple(sorted((center, terminal)))] += 1
    edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    assert edges == expected and len(edges) == sum(edges.values()) == 13
    assert sorted(graph["vertices"]) == sorted(roles) and len(roles) == 14
    assert graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
    payload = {"vertices": sorted(roles), "edges": sorted(edges.elements()),
               "profile": profile, "spine": spine, "roles": roles}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    digest = sha256(raw).hexdigest()
    assert digest == original["graph_digest"] == expected_digest

    neighbors = {v: set() for v in roles}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    color = {"s:0": 0}
    pending = deque(color)
    while pending:
        u = pending.popleft()
        for v in neighbors[u]:
            if v not in color:
                color[v] = 1 - color[u]
                pending.append(v)
            assert color[u] != color[v]
    low = {v for v, side in color.items() if side == 0}
    high = set(color) - low
    assert low == {"s:0", "b:1:0"} | {v for v in roles if v.startswith("l:0:")}
    assert high == {"s:1", "b:0:0", "b:0:1", "l:1:0:0", "l:1:0:1"}
    assert low | high == set(roles) and (len(low), len(high)) == (9, 5)
    return edges, neighbors, low, high


def obstruction(original, digest, reported_cases):
    edges, neighbors, low, high = topology(original, digest)
    left_a, left_b, zero = "b:0:0", "b:0:1", "b:1:0"
    groups = {"spine": {("s:0", "s:1")}}
    for center in (left_a, left_b, zero):
        groups[center] = {edge for edge in edges if center in edge}
    assert Counter(edge for group in groups.values() for edge in group) == edges
    assert {k: len(v) for k, v in groups.items()} == {"spine": 1, left_a: 5, left_b: 4, zero: 3}
    assert neighbors[zero] == high - {left_a, left_b}
    assert neighbors[left_a] <= low - {zero} and neighbors[left_b] <= low - {zero}
    # The widest difference uses both ends of the full label interval.
    minimum, maximum = 0, len(edges)
    assert maximum - minimum == 13
    # At zero the edge weights are its high neighbors' labels, none a left center.
    # At a left center the low labels are positive, so the weights are below M.
    # The partition leaves only the spine. Its oriented weight is Y-x.
    degrees = {v: len(adjacent) for v, adjacent in neighbors.items()}
    excess = {v: (degrees[v]-1)*(1 if v in high else -1) for v in degrees}
    nonzero_excess = {v: coef for v, coef in excess.items() if coef}
    assert nonzero_excess == {"s:0": -2, "s:1": 1, left_a: 4, left_b: 3, zero: -2}
    cut = len(low)
    baseline = sum(range(cut, maximum + 1)) - sum(range(cut))
    required = maximum * (maximum + 1) // 2
    # Substitute x = Y - M and z = 0 in the signed sum.
    exit_coefficient = excess["s:1"] + excess["s:0"]
    max_coefficient = -excess["s:0"]
    constant = required - baseline
    assert (baseline, required, exit_coefficient, max_coefficient, constant) == (19, 91, -1, 2, 72)
    rows = []
    for greater in (left_a, left_b):
        lower = left_b if greater == left_a else left_a
        coefficients = {left_a: excess[left_a], left_b: excess[left_b]}
        coefficients[greater] += max_coefficient
        bounds = {greater: cut + 1, lower: cut}
        assert all(value > 0 for value in coefficients.values())
        smallest = sum(coefficients[name]*bound for name, bound in bounds.items())
        largest = constant - exit_coefficient*maximum
        assert smallest > largest
        rows.append({"larger_center": greater, "coefficients": coefficients,
                     "center_lower_bounds": bounds, "lhs_lower_bound": smallest,
                     "rhs_upper_bound": largest, "strict_gap": smallest-largest})
    assert rows == reported_cases
    return {"status": "PASS", "graph_digest": digest, "named_edge_groups": {k: sorted(v) for k,v in groups.items()},
            "low_vertices": sorted(low), "high_vertices": sorted(high), "degrees": degrees,
            "maximum_weight_endpoints": [minimum, maximum], "possible_maximum_label_vertices": sorted(neighbors[zero]),
            "mandatory_spine_weight": "Y-x=max(A,B)", "signed_excess": nonzero_excess,
            "degree_one_contribution": baseline, "required_sum": required, "substituted_constant": constant,
            "substituted_exit_coefficient": exit_coefficient, "substituted_maximum_coefficient": max_coefficient,
            "order_cases": rows}


def controls(original, cert, positive, adverse):
    graph = original["graph"]
    labels = cert["labels"]
    differences = [abs(labels[u]-labels[v]) for u, v in graph["edges"]]
    payload = {"graph_digest": original["graph_digest"], "labels": sorted(labels.items())}
    ledger = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert ledger == cert["ledger_id"] == positive["ledger_id"]
    assert set(labels) == set(graph["vertices"]) and sorted(labels.values()) == list(range(13))
    assert sorted(differences) == list(range(1, 13)) and differences == positive["checker"]["edge_differences"]
    assert all((labels[u] < 8) != (labels[v] < 8) for u, v in graph["edges"])
    assert cert["cut"] == 8 and cert["offsets"] == [labels["s:0"], labels["s:1"]-8] == [3, 4]
    host = "b:1:0"
    assert labels[host] == 0 and set(v for edge in graph["edges"] if host in edge for v in edge if v != host) == {
        "s:1", "l:1:0:0", "l:1:0:1"}
    wrong = adverse["wrong_digest"]
    assert not wrong["checker"]["valid"] and wrong["expected"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    false_host = adverse["false_zero_host"]
    assert false_host["vertex"] == host and false_host["declared"] == 0
    assert false_host["actual"] == labels["s:0"] == 3 and false_host["valid"] is False
    assert false_host["error"] == "The physical right center does not carry zero"
    swap = adverse["terminal_swap"]
    u, v = "l:0:0:0", "l:0:1:0"
    assert swap["vertices"] == [u, v]
    changed = labels | {u: labels[v], v: labels[u]}
    assert swap["labels"] == changed and sorted(changed.values()) == list(range(13))
    modified = [abs(changed[i]-changed[j]) for i, j in graph["edges"]]
    repeats = {str(w): n for w, n in Counter(modified).items() if n > 1}
    missing = sorted(set(range(1, 13))-set(modified))
    assert repeats == {"5": 2, "7": 2} and missing == [4, 8]
    assert not swap["checker"]["valid"] and swap["checker"]["edge_differences"] == modified
    assert swap["checker"]["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"status": "PASS", "d098_ledger_id": ledger, "swap_repeat_multiplicities": repeats,
            "swap_missing_weights": missing, "swap_original_edge_differences": modified}
