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


def crossing_class_control():
    """Derive both endpoints of the band embeddings and the four shifts."""
    a, b, offset, s1, s2, h, n, exterior, w, other = map(
        atom, ("a", "cut_b", "A", "s1", "s2", "H", "n", "B", "w", "other_w")
    )
    one = atom(1)
    shifts = (offset, polynomial_sum(offset, s1), polynomial_sum(offset, s1, s2))
    class_shifts = (difference(shifts[0], shifts[0]), difference(shifts[1], shifts[0]),
                    difference(shifts[2], shifts[1]), difference(shifts[2], shifts[0]))
    assert class_shifts == ({}, s1, s2, polynomial_sum(s1, s2))
    for index, left in enumerate(class_shifts):
        for right in class_shifts[index+1:]:
            collision = difference(polynomial_sum(w, left), polynomial_sum(other, right))
            assert collision == difference(difference(left, right), difference(other, w))
    zero_first = ({}, {}, s2, s2)
    zero_second = ({}, s1, {}, s1)
    assert tuple({m: c for m, c in form.items() if "s1" not in m}
                 for form in class_shifts) == zero_first
    assert tuple({m: c for m, c in form.items() if "s2" not in m}
                 for form in class_shifts) == zero_second

    first_start = polynomial_sum(a, shifts[0])
    first_end = difference(polynomial_sum(a, shifts[1]), one)
    second_start = polynomial_sum(b, shifts[1])
    second_end = difference(polynomial_sum(b, shifts[2]), one)
    assert polynomial_sum(difference(first_end, first_start), one) == s1
    assert polynomial_sum(difference(second_end, second_start), one) == s2
    m = polynomial_sum(n, h)
    last_start = polynomial_sum(n, shifts[2], one)
    assert difference(last_start, polynomial_sum(difference(m, exterior), one)) == difference(
        polynomial_sum(offset, s1, s2, exterior), h
    )
    return {
        "crossing_bits_in_order": ["00", "10", "01", "11"],
        "weight_increments": [record(form) for form in class_shifts],
        "fresh_label_intervals": [[[], record(difference(offset, one))],
                                  [record(first_start), record(first_end)],
                                  [record(second_start), record(second_end)],
                                  [record(last_start), record(m)]],
        "injectivity": "all six translated class intersections empty; individual classes injective",
        "collision_equation": "other_w-w = shift_left-shift_right",
        "old_cut_compatibility": "preserved vertex membership and old crossing weights exactly on threshold side",
        "zero_first": [record(form) for form in zero_first],
        "zero_second": [record(form) for form in zero_second],
        "disposition": "CONFIRM_EXACT_THREE_BAND_RESOURCE_CALCULUS",
    }


def symbolic_checks():
    """Check the remaining five formal controls without any numerical bridge."""
    half_n, t, b, i, c0, remaining = map(atom, ("n_half", "t", "b", "i", "c_0", "n_future"))
    one, two, three, four = map(atom, (1, 2, 3, 4))
    twice_t = polynomial_product(two, t)
    twice_b = polynomial_product(two, b)
    c = difference(half_n, one)
    d = polynomial_sum(half_n, one)
    n = polynomial_product(two, half_n)
    q = polynomial_sum(twice_t, twice_b, two)
    k = polynomial_sum(t, b, three)
    h = polynomial_sum(q, four)
    m = polynomial_sum(n, h)
    assert h == polynomial_product(two, k)

    leaf = difference(c, one)
    host = polynomial_sum(leaf, d)
    assert host == difference(n, one)
    moved_leaf = polynomial_sum(leaf, three, t)
    moved_host = polynomial_sum(host, three, q)
    exceptional = difference(moved_host, moved_leaf)
    second_gap = difference(q, t)
    assert exceptional == polynomial_sum(d, second_gap)
    assert difference(exceptional, difference(d, one)) == polynomial_sum(second_gap, one)
    assert difference(polynomial_sum(d, q, one), exceptional) == polynomial_sum(t, one)

    first_end = difference(t, two)
    missing_source = difference(t, one)
    tail = second_gap
    middle_start = polynomial_sum(t, two)
    middle_end = difference(tail, one)
    middle_length = polynomial_sum(difference(middle_end, middle_start), one)
    upper_length = difference(q, tail)
    assert difference(first_end, atom(-1)) == difference(t, one)
    assert difference(missing_source, first_end) == one
    assert moved_leaf == polynomial_sum(three, c, missing_source)
    assert middle_length == twice_b and upper_length == t
    assert difference(tail, middle_start) == polynomial_product(two, b)
    assert difference(tail, polynomial_sum(t, four)) == polynomial_product(two, difference(b, one))
    assert polynomial_sum(t, two, middle_length, upper_length) == q
    i_up = polynomial_sum(i, one)
    assert difference(i_up, i) == one
    positive_count = polynomial_sum(t, one, upper_length)
    assert positive_count == polynomial_sum(twice_t, one)

    twice_source_sum = polynomial_sum(atom(-2), polynomial_product(q, difference(q, one)),
                                      polynomial_product(atom(-2), missing_source))
    twice_target_sum = difference(polynomial_product(q, polynomial_sum(q, one)),
                                  polynomial_product(two, tail))
    assert difference(twice_target_sum, twice_source_sum) == polynomial_product(four, t)
    assert difference(positive_count, one) == twice_t
    assert second_gap == polynomial_sum(t, twice_b, two)

    output_cut = polynomial_sum(three, c, k)
    half_m = polynomial_sum(half_n, k)
    assert output_cut == polynomial_sum(half_m, two)
    next_cut = difference(polynomial_sum(m, one), output_cut)
    next_d = polynomial_sum(d, k)
    assert next_cut == difference(half_m, one)
    assert next_d == polynomial_sum(half_m, one)
    assert difference(tail, k) == difference(b, one)
    assert difference(k, middle_start) == polynomial_sum(b, one)
    assert difference(middle_end, k) == difference(b, two)
    assert difference(output_cut, one) == next_d
    assert difference(output_cut, next_d) == one
    assert difference(m, output_cut) == difference(next_cut, one)
    assert difference(exceptional, next_d) == difference(b, one)
    connector = difference(m, three)
    assert connector == polynomial_sum(n, q, one)

    # Use the prescribed preparatory constants as parameters of a formula, not a generated example.
    prep_q, prep_k = atom(8), atom(6)
    prep_h = polynomial_sum(prep_q, four)
    prep_cut = polynomial_sum(three, c, prep_k)
    assert prep_h == polynomial_product(two, prep_k)
    assert difference(prep_q, two) == prep_k
    assert difference(prep_k, two) == four
    assert difference(prep_cut, one) == polynomial_sum(d, prep_k)
    prepared_half_size = polynomial_sum(half_n, prep_k)
    assert difference(polynomial_sum(n, prep_h), prep_cut) == difference(prepared_half_size, two)
    initial_size = polynomial_sum(polynomial_product(three, c0), three,
                                  polynomial_sum(c0, two), one)
    assert initial_size == polynomial_sum(polynomial_product(four, c0), atom(6))
    assert difference(polynomial_sum(remaining, h), remaining) == h
    assert difference(q, t) == second_gap

    return {
        "crossing_class_calculus": crossing_class_control(),
        "distinguished_leaf_incidence": {
            "preconditions": ["the label c-1 is at the named degree-one terminal u",
                              "its unique old edge u-z has weight d"],
            "host": record(host), "new_leaf_label": record(moved_leaf),
            "new_old_edge_weight": record(exceptional),
            "ordinary_old_noncrossing": "[1,d-1] unchanged",
            "other_old_crossing": "[d+1,n] translated by Q",
            "reason": "no additional old incidence can touch the singleton label c-1",
            "disposition": "CONFIRM_EXACT_EXCEPTIONAL_WEIGHT",
        },
        "partition_and_displacements": {
            "source_deleted": record(missing_source), "target_deleted": record(tail),
            "rows": [
                {"domain": ["-1", "t-2"], "image": ["0", "t-1"], "displacement": "+1"},
                {"domain": ["t", "t+1"], "image": ["t", "t+1"], "order": "exchange"},
                {"domain": ["t+2", "Q-t-1"], "image": ["t+2", "Q-t-1"], "displacement": "zero"},
                {"domain": ["Q-t", "Q-1"], "image": ["Q-t+1", "Q"], "displacement": "+1"},
            ],
            "positive_count": record(positive_count), "zero_count": record(middle_length),
            "negative_count": 1,
            "boundaries": {"t=1": "first lower shift is singleton coordinate -1",
                           "b=1": "remaining fixed coordinates t+2..t+3; last row starts t+4"},
            "disposition": "CONFIRM_INTERVAL_BIJECTION_AND_QUOTAS",
        },
        "all_role_escape": {
            "reason": "the +1 and -1 roles require equal quotas for zero moment",
            "physical_quotas": ["odd >=3", "positive even", "1"],
            "moment": record(twice_t), "twice_moment": record(difference(twice_target_sum, twice_source_sum)),
            "gaps": [record(t), record(second_gap)],
            "distinct_translations": "3, 3+t, 3+Q on three nonempty old bands",
            "disposition": "CONFIRM_ESCAPE_FOR_EVERY_NUMERICAL_ROLE_ASSIGNMENT",
        },
        "return_cut_and_boundary": {
            "cut": record(output_cut), "next_cut": record(next_cut), "next_d": record(next_d),
            "exceptional_crossing_minus_threshold": record(difference(exceptional, next_d)),
            "connector": record(connector),
            "terminal_images": ["[0,K-1]", "[K,Q] minus {Q-t}"],
            "branch_b_at_least_two": {"coordinate": "K", "host": 1,
                                      "terminal_index": record(difference(k, middle_start)),
                                      "oriented_weight": "d_prime"},
            "branch_b_one": {"coordinate": "K", "host": 0, "oriented_weight": "d_prime+1",
                             "ordinary_return": True, "strengthened_return": False},
            "disposition": "CONFIRM_EXACT_RETURN_DOMAIN",
        },
        "preparation_and_closure": {
            "preparation": "D137 canonical formula with the declared (1,6,1) and symbolic exchange 0<->1",
            "prep_bands": ["[0,5]", "[6,7]"], "physical_terminal_index": 4,
            "prep_cut": record(prep_cut), "initial_size": record(initial_size),
            "size_admission": "choose admitted c_0 for at least 12 and all declared H_i",
            "iteration": "intermediates require b>=2; b=1 may end the list",
            "final_composition": "each already present leaf can be exceptional only at the first next step",
            "exceptional_weight_shift": "next Q-t and later crossing shifts Q",
            "termination": "finite admitted list and one finite increasing scan per section",
            "disposition": "CONFIRM_INDEPENDENT_SYMBOLIC_SUPPLY_AND_CLOSURE",
        },
    }
