"""Independent retained spine-state and cut and symbolic displacement arithmetic audit."""

from collections import Counter, deque
from hashlib import sha256
import json


def canonical_digest(payload):
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(raw).hexdigest()


def distances(neighbors, sources):
    seen = dict.fromkeys(sources, 0)
    queue = deque(sources)
    while queue:
        u = queue.popleft()
        for v in neighbors[u] - seen.keys():
            seen[v] = seen[u] + 1
            queue.append(v)
    return seen


def state_gate(graph, labels, frontier, delta):
    """Each frontier predicate is checked separately on a retained original."""
    spine = graph["spine"]
    n = len(graph["edges"])
    exact_label = type(labels.get(frontier)) is int
    tests = {
        "physical_frontier": bool(spine) and frontier == spine[-1],
        "frontier_label_in_alphabet": exact_label and 0 <= labels[frontier] <= n,
        "exact_deficit_in_bounds": type(delta) is int and 0 <= delta <= n,
        "deficit_agrees_at_claimed_vertex": exact_label and type(delta) is int and delta == n - labels[frontier],
    }
    return {"frontier": frontier, "claimed_deficit": delta, "tests": tests, "valid": all(tests.values())}


def inspect_seed(original, binding, certificate, checker):
    graph = original["graph"]
    profile = binding["profile"]
    assert profile in ([[4, 3], [2]], [[2, 5, 6], [2]])
    assert all(type(q) is int for section in profile for q in section)
    spine = [f"s:{index}" for index in range(len(profile))]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = [[u, v] for u, v in zip(spine, spine[1:])]
    for section, quotas in enumerate(profile):
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            edges.append([spine[section], center])
            for index in range(quota):
                leaf = f"l:{section}:{branch}:{index}"
                roles[leaf] = {"kind": "leaf", "section": section, "branch": branch, "leaf": index}
                edges.append([center, leaf])
    n = len(edges)
    incidence = Counter(tuple(sorted(edge)) for edge in edges)
    assert graph["edges"] == edges and all(count == 1 for count in incidence.values())
    assert graph["schema_version"] == 1 and graph["profile"] == profile and graph["spine"] == spine
    assert graph["roles"] == roles and Counter(graph["vertices"]) == Counter(roles.keys())
    assert len(roles) == n + 1
    neighbors = {v: set() for v in roles}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    depth = distances(neighbors, spine)
    by_role = {"spine": 0, "branch": 1, "leaf": 2}
    assert depth == {v: by_role[role["kind"]] for v, role in roles.items()}
    from_start = distances(neighbors, [spine[0]])
    assert set(from_start) == set(roles)
    digest = canonical_digest({"vertices": sorted(roles), "edges": sorted(incidence.elements()),
                               "roles": roles, "spine": spine, "profile": profile})
    assert digest == original["graph_digest"] == binding["graph_digest"] == checker["graph_digest"]
    labels = certificate["labels"]
    assert set(labels) == set(roles) and all(type(value) is int for value in labels.values())
    assert Counter(labels.values()) == Counter(range(n + 1))
    weighted_edges = [{"edge": [u, v], "weight": abs(labels[u] - labels[v])} for u, v in edges]
    weights = [row["weight"] for row in weighted_edges]
    assert Counter(weights) == Counter(range(1, n + 1)) and weights == checker["edge_differences"]
    assert checker["valid"] and checker["m"] == n and checker["n"] == n + 1
    ledger = canonical_digest({"graph_digest": digest, "labels": sorted(labels.items())})
    assert ledger == certificate["ledger_id"] == binding["ledger_id"]

    frontier, predecessor = spine[-1], spine[-2]
    host = "b:1:0"
    pins = {"predecessor_label": labels[predecessor], "exit_label": labels[frontier], "off_spine_label": labels[host]}
    assert frontier == "s:1" and predecessor == "s:0"
    assert certificate["physical_spine"] == spine and neighbors[frontier] == {predecessor, host}
    assert host not in spine and depth[host] == 1
    assert pins == {"predecessor_label": 0, "exit_label": n, "off_spine_label": 1}
    delta = n - labels[frontier]
    state = state_gate(graph, labels, frontier, delta)
    assert state["valid"] and delta == 0

    classes = [[labels[v] for v in roles if from_start[v] % 2 == parity] for parity in (0, 1)]
    assert all((from_start[u] - from_start[v]) % 2 for u, v in edges)
    separation = max(classes[0]) < min(classes[1]) or max(classes[1]) < min(classes[0])
    return {
        "graph_digest": digest, "ledger_id": ledger, "profile": profile, "edge_count": n,
        "label_inventory": sorted(labels.values()), "difference_inventory": sorted(weights), "named_weights": weighted_edges,
        "ordered_spine": spine, "distance_to_spine": depth, "exit_neighbors": sorted(neighbors[frontier]),
        "D112_premises": True, "D112_pins": pins, "deficit_state": state,
        "certificate_has_alpha_separation": separation, "historical_formula_evaluated": False,
    }


def inspect_maximum_cut(graph, certificate):
    """Inspect the one declared cut at n on a retained maximum-frontier original."""
    labels = certificate["labels"]
    n = len(graph["edges"])
    frontier = graph["spine"][-1]
    assert labels[frontier] == n
    actual_cut = n
    oriented_cut = n + 1 - actual_cut
    actual = []
    for u, v in graph["edges"]:
        below = (labels[u] < actual_cut, labels[v] < actual_cut)
        oriented_below = (n - labels[u] < oriented_cut, n - labels[v] < oriented_cut)
        assert oriented_below == tuple(not side for side in below)
        if below[0] != below[1]:
            actual.append({"edge": [u, v], "weight": abs(labels[u] - labels[v])})
    assert actual == [
        {"edge": ["s:0", "s:1"], "weight": n},
        {"edge": ["s:1", "b:1:0"], "weight": n - 1},
    ]
    weights = sorted(row["weight"] for row in actual)
    assert weights == [n - 1, n] and oriented_cut == 1
    return {"n": n, "frontier": frontier, "frontier_label": labels[frontier],
            "actual_cut": actual_cut, "oriented_cut": oriented_cut,
            "crossing_incidence": actual, "crossing_spectrum": weights}


def atom(value):
    return {(): value} if type(value) is int else {(value,): 1}


def polynomial_sum(*terms):
    result = {}
    for term in terms:
        for monomial, coefficient in term.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_product(left, right):
    result = {}
    for a, ac in left.items():
        for b, bc in right.items():
            monomial = tuple(sorted(a + b))
            result[monomial] = result.get(monomial, 0) + ac * bc
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def difference(left, right):
    return polynomial_sum(left, polynomial_product(atom(-1), right))


def record(form):
    return [{"factors": list(monomial), "coefficient": coefficient}
            for monomial, coefficient in sorted(form.items())]


def symbolic_checks():
    """Check four formal controls without instantiating a bridge or role permutation."""
    m, a, j, p, pp, k, e, bm, ba, x, y, beta_bound, base_bound = map(
        atom, ("m", "A", "j", "p", "p_prime", "K", "e",
               "b_middle", "b_adjacent", "X", "Y", "M", "b_abs_S")
    )
    one, two, three = map(atom, (1, 2, 3))
    terminal_weight = difference(difference(m, one), j)
    connector_weight = difference(m, a)
    competing_attachment = difference(m, polynomial_sum(j, one))
    connector_margin = difference(terminal_weight, connector_weight)
    assert connector_margin == difference(difference(a, one), j)
    assert difference(difference(m, one), terminal_weight) == j
    assert terminal_weight == competing_attachment

    h = polynomial_sum(p, pp, one)
    t = difference(h, a)
    first_lo = polynomial_sum(p, one)
    first_hi = difference(difference(t, e), two)
    second_lo = polynomial_sum(k, e, one)
    second_hi = difference(difference(polynomial_sum(k, p), a), one)
    first = polynomial_sum(difference(first_hi, first_lo), one)
    second = polynomial_sum(difference(second_hi, second_lo), one)
    assert first == difference(difference(difference(pp, a), e), one)
    assert second == difference(difference(difference(p, a), e), one)
    assert difference(second_lo, first_hi) == polynomial_sum(
        difference(k, t), polynomial_product(two, e), three
    )
    both_margin = difference(t, polynomial_sum(first, second))
    first_margin = difference(t, first)
    second_margin = difference(t, second)
    assert both_margin == polynomial_sum(a, polynomial_product(two, e), three)
    assert first_margin == polynomial_sum(p, e, two)
    assert second_margin == polynomial_sum(pp, e, two)
    # Restrict the same formal assertions to e=0.
    both_at_zero = difference(both_margin, polynomial_product(two, e))
    first_at_zero = difference(first_margin, e)
    second_at_zero = difference(second_margin, e)
    assert both_at_zero == polynomial_sum(a, three)
    assert first_at_zero == polynomial_sum(p, two)
    assert second_at_zero == polynomial_sum(pp, two)

    # The unchanged roles have the same two quota contributions after a role exchange.
    middle_offset = difference(pp, pp)
    adjacent_offset = difference(pp, difference(pp, one))
    assert middle_offset == {} and adjacent_offset == one
    initial_pair = polynomial_sum(polynomial_product(middle_offset, bm),
                                  polynomial_product(adjacent_offset, ba))
    swapped_fixed_pair = polynomial_sum(polynomial_product(middle_offset, ba),
                                        polynomial_product(adjacent_offset, bm))
    swapped_assigned_pair = polynomial_sum(polynomial_product(adjacent_offset, ba),
                                           polynomial_product(middle_offset, bm))
    fixed_change = difference(swapped_fixed_pair, initial_pair)
    assert fixed_change == difference(bm, ba)
    assert swapped_assigned_pair == initial_pair
    assert polynomial_sum(bm, ba) == polynomial_sum(ba, bm)

    # The two possible controlling increments have strictly positive margins.
    max_rest = polynomial_sum(polynomial_product(beta_bound, y), base_bound)
    x_margin = difference(x, max_rest)
    y_margin = difference(y, base_bound)
    assert x_margin == difference(difference(x, polynomial_product(beta_bound, y)), base_bound)
    assert y_margin == difference(y, base_bound)
    twice_offset_sum = polynomial_product(h, difference(pp, p))
    assert twice_offset_sum == difference(polynomial_product(pp, polynomial_sum(pp, one)),
                                          polynomial_product(p, polynomial_sum(p, one)))

    return {
        "upper_exterior_collision": {
            "assumptions": ["B>1", "terminal m-1 must have a lower exterior host", "0<=j<=A-1"],
            "empty_host_case": "A=0 gives no exterior host",
            "terminal_weight": record(terminal_weight),
            "terminal_minus_connector": record(connector_margin),
            "connector_case": "j=A-1 repeats the original connector",
            "attachment_case": "j<=A-2 repeats the attachment to the distinct center labeled j+1",
            "attachment_weight": record(competing_attachment),
            "disposition": "FORCE_UPPER_EXTERIOR_SINGLETON",
        },
        "gap_center_cardinality": {
            "assumptions": ["t=h-A>0", "p,p_prime>=1", "e>=0", "K>=h+1"],
            "intervals": [[record(first_lo), record(first_hi)], [record(second_lo), record(second_hi)]],
            "raw_cardinalities": [record(first), record(second)],
            "eligible_upper_bound": "sum of the two positive parts",
            "strict_deficit": {"both_positive": record(both_margin), "first_only": record(first_margin),
                               "second_only": record(second_margin), "neither": record(t)},
            "at_e_zero": {"both_positive": record(both_at_zero), "first_only": record(first_at_zero),
                          "second_only": record(second_at_zero), "neither": record(t)},
            "disposition": "EXCLUDE_POSITIVE_GAP_CENTER_COUNT",
        },
        "symbolic_role_exchange": {
            "assumptions": ["an independently admitted D137 role vector", "b_middle>b_adjacent",
                            "the physical quotas at p_prime and p_prime-1 are exchanged"],
            "fixed_moment_increase": record(fixed_change),
            "assigned_role_moment_change": record(difference(swapped_assigned_pair, initial_pair)),
            "unchanged": ["quota per numerical role", "two bands", "terminal differences",
                          "all requested physical names and terminal slots"],
            "disposition": "SUPPLY_BEYOND_FIXED_PHYSICAL_INDEX_MOMENT",
        },
        "all_role_dominance": {
            "assumptions": ["M=max(p,p_prime)", "alpha and beta distinct in [-p,p_prime]",
                            "X>M*Y+b_abs_S", "Y>b_abs_S", "b_abs_S=b*abs(S)"],
            "twice_offset_sum": record(twice_offset_sum),
            "nonzero_alpha_margin_lower_bound": record(x_margin),
            "zero_alpha_nonzero_beta_margin_lower_bound": record(y_margin),
            "parity": "vary X within the class giving even h+Q+1",
            "disposition": "EXCLUDE_EVERY_NUMERICAL_ROLE_ASSIGNMENT",
        },
    }
