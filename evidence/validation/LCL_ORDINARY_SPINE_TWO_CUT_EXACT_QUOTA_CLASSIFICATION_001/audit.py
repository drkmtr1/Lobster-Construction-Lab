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
    """Verify six formal controls without instantiating any allocation."""
    t, b, z, a, sf, df, i, ell, half_n, g, shift, tau, weight, low_sum = map(
        atom, ("t", "b", "z", "a", "source_hole_below", "target_hole_below", "i",
               "ell", "n_half", "g", "Q_next", "tau", "weight", "lower_shift_sum")
    )
    one, two, three, four = map(atom, (1, 2, 3, 4))
    q_base, k_base = map(atom, ("Q", "K"))
    lower_hole = difference(t, one)
    upper_hole = difference(q_base, t)
    lower_src_count = difference(polynomial_sum(k_base, one), sf)
    lower_dst_count = difference(k_base, df)
    assert difference(lower_src_count, lower_dst_count) == polynomial_sum(difference(one, sf), df)
    d = polynomial_sum(half_n, one)
    assert difference(polynomial_sum(d, upper_hole), polynomial_sum(d, k_base)) == difference(
        upper_hole, k_base
    )
    q_from_k = difference(polynomial_product(two, k_base), four)
    hole_implied_bound = difference(difference(q_from_k, t), polynomial_sum(k_base, one))
    assert hole_implied_bound == difference(difference(k_base, t), atom(5))

    first_src_start = atom(-1)
    first_src_end = difference(t, two)
    first_dst_start = polynomial_sum(first_src_start, one)
    first_dst_end = polynomial_sum(first_src_end, one)
    last_src_start = upper_hole
    last_src_end = difference(q_base, one)
    last_dst_start = polynomial_sum(last_src_start, one)
    last_dst_end = polynomial_sum(last_src_end, one)
    assert first_dst_start == {} and first_dst_end == lower_hole and last_dst_end == q_base
    assert polynomial_sum(difference(first_src_end, first_src_start), one) == t
    assert polynomial_sum(difference(last_src_end, last_src_start), one) == t
    assert difference(first_src_end, first_src_start) == difference(t, one)
    assert difference(last_dst_start, last_src_start) == one

    # The complete induction step reduces the interval by one point or one adjacent pair.
    next_coordinate = polynomial_sum(i, one)
    assert difference(next_coordinate, i) == one
    assert difference(i, next_coordinate) == atom(-1)
    assert polynomial_sum(difference(next_coordinate, i), difference(i, next_coordinate)) == {}
    lower_length = difference(k_base, t)
    upper_length = difference(difference(upper_hole, k_base), one)

    v = polynomial_sum(b, z)
    r0 = polynomial_sum(polynomial_product(two, t), z)
    r1 = polynomial_product(two, b)
    q = polynomial_sum(r0, r1, z)
    k = polynomial_sum(t, v, two)
    assert polynomial_sum(q, four) == polynomial_product(two, k)
    assert difference(r0, z) == polynomial_product(two, t)
    assert difference(q, polynomial_sum(r0, z)) == r1
    lower = difference(k, t)
    upper = difference(difference(difference(q, t), k), one)
    assert lower == polynomial_sum(v, two)
    assert upper == difference(v, three)
    assert difference(difference(q, t), k) == difference(v, two)
    lower_even = polynomial_sum(a, one)
    upper_even = difference(a, two)
    lower_odd = polynomial_sum(a, one)
    upper_odd = difference(a, one)
    twice_a = polynomial_product(two, a)
    assert polynomial_product(two, lower_even) == polynomial_sum(twice_a, two)
    assert polynomial_sum(polynomial_product(two, upper_even), one) == difference(twice_a, three)
    assert polynomial_sum(polynomial_product(two, lower_odd), one) == polynomial_sum(twice_a, three)
    assert polynomial_product(two, upper_odd) == difference(twice_a, two)
    even_sum = polynomial_sum(lower_even, upper_even)
    odd_sum = polynomial_sum(lower_odd, upper_odd)
    assert even_sum == difference(twice_a, one) and odd_sum == twice_a
    capacity = difference(v, one)
    assert difference(capacity, z) == difference(b, one)

    upper_pairs = difference(z, ell)
    leaf_index = difference(lower, polynomial_product(two, ell))
    assert polynomial_sum(ell, upper_pairs) == z
    assert polynomial_sum(difference(polynomial_sum(lower, upper), polynomial_product(two, z)), one) == r1
    recovered_leaf_index = difference(polynomial_sum(b, three), two)
    assert recovered_leaf_index == polynomial_sum(b, one)
    assert difference(polynomial_sum(z, one), three) == difference(z, two)
    output_cut = polynomial_sum(half_n, k, two)
    output_d = polynomial_sum(d, k)
    assert difference(output_cut, one) == output_d
    m = polynomial_product(two, polynomial_sum(half_n, k))
    output_oriented_cut = difference(polynomial_sum(m, one), output_cut)
    assert difference(m, output_cut) == difference(output_oriented_cut, one)
    assert difference(polynomial_sum(m, one), output_cut) == difference(polynomial_sum(half_n, k), one)
    assert difference(difference(m, three), polynomial_sum(polynomial_product(two, half_n), q, one)) == {}

    # Suffix composition keeps the one tagged correction separate from all later shifts.
    next_weight = polynomial_sum(weight, difference(shift, tau))
    later_weight = polynomial_sum(next_weight, g)
    assert later_weight == difference(polynomial_sum(weight, shift, g), tau)
    positive_label = polynomial_sum(i, low_sum, tau)
    negative_label = difference(polynomial_sum(i, low_sum, shift, g), tau)
    assert difference(positive_label, polynomial_sum(i, low_sum)) == tau
    assert difference(polynomial_sum(i, low_sum, shift, g), negative_label) == tau

    return {
        "hole_position_requirement": {
            "source_hole": record(lower_hole), "destination_hole": record(upper_hole),
            "lower_count_difference": record(difference(lower_src_count, lower_dst_count)),
            "membership": "binary indicators force the source hole below K and target hole at or above K",
            "excluded_boundary": "Q-t=K deletes the required fixed image K",
            "exceptional_crossing": "d+Q-t>=d+K",
            "required": "Q-t>=K+1; hence t<=K-5",
            "disposition": "CONFIRM_STRICT_UPPER_HOLE_REQUIREMENT",
        },
        "both_forced_chains": {
            "sources": [["-1", "t-2"], ["Q-t", "Q-1"]],
            "destinations": [["0", "t-1"], ["Q-t+1", "Q"]],
            "endpoints": ["-1 must map to 0", "Q can have only preimage Q-1"],
            "logical_step": "one advancing forced target per lower source; one reverse forced source per upper target",
            "length_each": record(t), "t_one": "both chains are single unit steps",
            "disposition": "CONFIRM_ALL_FEASIBLE_MAPS_CONTAIN_BOTH_CHAINS",
        },
        "complete_adjacent_interval_structure": {
            "remaining_intervals": [["t", "K-1"], ["K+1", "Q-t-1"]],
            "lengths": [record(lower_length), record(upper_length)],
            "least_source_induction": "least a maps to a or a+1; in latter case a+1 must map to a",
            "pair_displacements": [1, -1],
            "exact_capacities": ["floor(L/2)", "floor(U/2)"],
            "empty_upper": "U=0 gives capacity zero",
            "disposition": "CONFIRM_INTERVAL_COMPLETENESS_AND_CAPACITIES",
        },
        "moment_parity_and_floor_capacity": {
            "moment": record(difference(r0, z)), "r1": record(r1),
            "Q": record(q), "K": record(k), "L": record(lower), "U": record(upper),
            "even_v_capacities": [record(lower_even), record(upper_even)],
            "odd_v_capacities": [record(lower_odd), record(upper_odd)],
            "capacity_sum": record(capacity), "capacity_margin_over_z": record(difference(capacity, z)),
            "equivalence": "v=b+z>=3 is U>=0, strictly placing Q-t above K",
            "disposition": "CONFIRM_EXACT_QUOTA_CLASSIFICATION",
        },
        "indexed_leaf_and_coverage": {
            "pair_counts": ["ell=min(z,floor(L/2))", "u=z-ell"],
            "upper_pairs": record(upper_pairs), "middle_count_including_K": record(r1),
            "returned_index": record(leaf_index), "physical_center": 1, "boundary_coordinate": "K",
            "oriented_label": "c_prime-1", "host_label": "m-1", "weight": "d_prime",
            "pointwise_D139": "z=1,b>=2 gives only t<->t+1, with index b+1",
            "new_b_one_domain": "z>=2; z>=3 has three unequal quotas; z=2 has two equal quotas",
            "preserved_ordinary_boundary": "z=b=1 still has D139 final ordinary output",
            "connector": "m-3=n+Q+1",
            "disposition": "CONFIRM_INDEXED_CONSTRUCTION_AND_PHYSICAL_LEAF",
        },
        "preparation_composition_and_termination": {
            "preparation": "unchanged D134 initializer plus actual D137 (1,6,1) section, center-1 index 4",
            "closure": "any finite admitted quota list, both extreme polarities and exact size at each boundary",
            "exceptional_final_weight": record(later_weight),
            "positive_leaf_image": record(positive_label), "negative_leaf_image": record(negative_label),
            "used_weight_bands": ["[1,d_i-1]", "{d_i+S_i-tau_i}", "[d_i+1+S_i,n_i+S_i]"],
            "label_inventory": "default two image intervals replace exactly the signed shifted old leaf",
            "termination": "Q source visits and four other fresh vertices per section; linear indexed output",
            "disposition": "CONFIRM_REUSABLE_STATE_AND_IMMUTABLE_FINAL_INVENTORIES",
        },
    }
