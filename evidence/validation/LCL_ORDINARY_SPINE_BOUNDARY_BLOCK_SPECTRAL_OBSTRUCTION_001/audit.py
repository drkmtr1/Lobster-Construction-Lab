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
    """Check the seven formal controls without constructing a new original."""
    half_n, p, pp, h, q, t, a, k_half, r, low_weight, gamma, n0, prior_total = map(
        atom, ("half_n", "p", "p_prime", "h", "Q", "t", "a", "K", "r",
               "q_min", "gamma", "n0", "t0_plus_b_plus_z")
    )
    one, two, three, four = map(atom, (1, 2, 3, 4))
    n = polynomial_product(two, half_n)
    c = difference(half_n, p)
    d = polynomial_sum(half_n, one)
    H = polynomial_sum(h, q, one)
    m = polynomial_sum(n, H)
    lower_shift, block_shift, upper_shift = h, polynomial_sum(h, t), polynomial_sum(h, q)
    p_shift = difference(block_shift, lower_shift)
    r_shift = difference(upper_shift, block_shift)
    outer_shift = difference(upper_shift, lower_shift)
    assert p_shift == t and r_shift == difference(q, t) and outer_shift == q
    gap1_first = polynomial_sum(h, a)
    gap1_last = difference(polynomial_sum(h, a, t), one)
    gap2_first = polynomial_sum(h, c, t)
    gap2_last = difference(polynomial_sum(h, c, q), one)
    exit_connector = difference(m, h)
    min_terminal = difference(gap1_first, difference(h, one))
    assert polynomial_sum(difference(gap1_last, gap1_first), one) == t
    assert polynomial_sum(difference(gap2_last, gap2_first), one) == r_shift
    assert difference(gap2_first, gap1_last) == polynomial_sum(difference(c, a), one)
    assert min_terminal == polynomial_sum(a, one)
    assert exit_connector == polynomial_sum(n, q, one)
    assert polynomial_sum(n, upper_shift, one) == m

    required_max = polynomial_sum(r, q)
    own_max = polynomial_sum(r, r_shift)
    assert difference(required_max, own_max) == t
    assert difference(required_max, polynomial_sum(difference(d, one), t)) == polynomial_sum(
        difference(r, d), r_shift, one
    )
    assert difference(exit_connector, required_max) == polynomial_sum(difference(n, r), one)
    max_margin = difference(required_max, gap2_last)
    assert max_margin == difference(r, difference(polynomial_sum(h, c), one))
    cut_size = polynomial_product(two, polynomial_sum(half_n, k_half))
    placed_cut = polynomial_sum(half_n, k_half, pp, one)
    upper_fresh = difference(difference(cut_size, placed_cut), difference(n, c))
    assert upper_fresh == difference(difference(difference(k_half, p), pp), one)
    assert difference(polynomial_sum(h, upper_fresh), k_half) == difference(
        h, polynomial_sum(p, pp, one)
    )
    compatible_h = polynomial_sum(p, pp, one)
    compatible_limit = difference(polynomial_sum(compatible_h, c), one)
    assert compatible_limit == difference(polynomial_sum(d, pp), one)
    assert polynomial_sum(difference(compatible_limit, d), one) == pp

    assert difference(polynomial_sum(low_weight, t), low_weight) == t
    assert difference(polynomial_sum(d, k_half), low_weight) == polynomial_sum(
        difference(d, low_weight), k_half
    )
    assert difference(min_terminal, low_weight) == difference(polynomial_sum(a, one), low_weight)
    assert difference(d, gap1_first) == difference(polynomial_sum(half_n, one), polynomial_sum(h, a))

    singleton_cut = difference(half_n, one)
    singleton = difference(singleton_cut, one)
    assert polynomial_sum(singleton, d) == difference(n, one)
    assert difference(d, singleton) == three
    assert difference(polynomial_sum(three, singleton), d) == {}

    # The source upper strip is fully occupied by fresh crossing terminals.
    q0 = polynomial_product(two, prior_total)
    k0 = polynomial_sum(prior_total, two)
    strip_size = difference(q0, k0)
    assert strip_size == difference(prior_total, two)
    assert difference(strip_size, two) == difference(prior_total, four)
    cin, m0, t0 = map(atom, ("c_in", "m0", "t0"))
    C0 = polynomial_sum(three, cin, k0)
    top_low = difference(m0, C0)
    bottom_of_strip = difference(m0, difference(polynomial_sum(three, cin, q0), one))
    assert polynomial_sum(difference(top_low, bottom_of_strip), one) == strip_size
    assert difference(k0, difference(t0, one)) == polynomial_sum(difference(prior_total, t0), three)
    prep_strip = difference(atom(8), atom(6))
    assert prep_strip == two

    N = polynomial_product(three, gamma)
    twice_T = difference(polynomial_sum(N, one), n0)
    gamma_margin = difference(difference(gamma, n0), one)
    assert difference(twice_T, polynomial_product(two, polynomial_sum(gamma, one))) == gamma_margin
    assert difference(polynomial_product(two, difference(polynomial_product(two, gamma), n0)),
                      twice_T) == gamma_margin
    initial_Q = polynomial_sum(gamma, two)
    initial_n = polynomial_sum(N, initial_Q, four)
    initial_C = polynomial_sum(three, gamma, initial_Q)
    initial_c = difference(polynomial_sum(initial_n, one), initial_C)
    initial_d = polynomial_sum(gamma, two, initial_Q)
    twice_gamma = polynomial_product(two, gamma)
    assert initial_n == polynomial_sum(polynomial_product(four, gamma), atom(6))
    assert initial_c == polynomial_sum(twice_gamma, two)
    assert initial_d == polynomial_sum(twice_gamma, four)
    boundary = difference(polynomial_sum(N, one), gamma)
    left_prelabel = polynomial_sum(difference(N, gamma), one)
    right_prelabel = difference(N, gamma)
    left = difference(polynomial_sum(N, one), left_prelabel)
    right = difference(polynomial_sum(N, one), right_prelabel)
    assert boundary == difference(initial_c, one)
    assert left == gamma and right == polynomial_sum(gamma, one)
    path_weight = difference(boundary, left)
    assert path_weight == polynomial_sum(gamma, one)
    assert difference(boundary, right) == gamma
    assert difference(polynomial_sum(a, one), path_weight) == difference(a, gamma)
    assert difference(initial_d, polynomial_sum(three, gamma)) == polynomial_sum(gamma, one)

    conjugated = tuple(difference(difference(m, n), shift)
                       for shift in (upper_shift, block_shift, lower_shift))
    assert conjugated == (one, polynomial_sum(one, r_shift), polynomial_sum(one, q))
    assert difference(conjugated[1], conjugated[0]) == r_shift
    assert difference(conjugated[2], conjugated[1]) == t

    return {
        "four_class_resources": {
            "classes": ["00", "10 (P)", "01 (R)", "11"],
            "increments": [[], record(p_shift), record(r_shift), record(outer_shift)],
            "designated_noncrossing": ["00", "P"], "designated_crossing": ["R", "11"],
            "test": "all four translated weight classes pairwise disjoint",
            "fresh_label_gaps": [[record(gap1_first), record(gap1_last)],
                                 [record(gap2_first), record(gap2_last)]],
            "fresh_difference_inventory": "exact complement of four translated sets in [1,m]",
            "terminal_bounds": [record(min_terminal), record(gap2_last)],
            "connector_and_attachment_band": [record(exit_connector), record(m)],
            "disposition": "CONFIRM_EXACT_ACTUAL_INCIDENCE_RESOURCES",
        },
        "maximum_crossing_obstruction": {
            "required_weight": record(required_max), "shifted_original": record(own_max),
            "W00_and_P_shift_below": "both below d+Q",
            "R_exclusion": "every shifted R at most r+Q-t",
            "W11_exclusion": "r has a unique original incidence in R",
            "connector_margin_even_at_r_n": record(difference(exit_connector, required_max)),
            "terminal_margin": record(max_margin), "endpoint": "r=h+c-1 passes this necessary bound",
            "upper_fresh_count": record(upper_fresh),
            "crossing_compatibility": "h+upper_fresh_count=K forces h=p+p_prime+1",
            "necessary_interval": [record(d), record(compatible_limit)],
            "count_capacity": record(pp),
            "disposition": "CONFIRM_MAXIMUM_EXCEPTIONAL_CROSSING_CAPACITY",
        },
        "minimum_noncrossing_obstruction": {
            "necessary": "min P >= a+1 when P is nonempty",
            "reason": "W00 lacks q_min, P+t is strictly above q_min, retained crossings are at least d+K",
            "empty_class": "P empty leaves all [1,d-1] in W00",
            "first_gap_label": record(gap1_first),
            "collision": "if h+a<d, its terminal must repeat an unchanged noncrossing weight",
            "disposition": "CONFIRM_NONCROSSING_EXCLUSIONS",
        },
        "singleton_rigidity": {
            "scope": "p=p_prime=1, h=3, k=1",
            "P": "any such weight at most a=c-1, forcing P empty",
            "R": "by connectedness and p_prime capacity exactly one actual edge with weight d",
            "boundary_label": record(singleton), "neighbor_label": record(polynomial_sum(singleton, d)),
            "physical_scope": "degree one and exact actual neighbor; named host if off-spine",
            "disposition": "CONFIRM_SINGLETON_DEGREE_ONE_NECESSITY",
        },
        "retained_leaf_strips": {
            "D140": {"Q0": record(q0), "K0": record(k0), "leaf_strip_length": record(strip_size),
                     "lower_bound": "prior_total=t0+b+z>=4 gives Q0>=8 and strip at least two",
                     "source_hole": "t0-1<K0 leaves every upper source coordinate",
                     "physical_strip": "named crossing terminals from placements [C0,3+c_in+Q0-1]",
                     "oriented_low_bounds": [record(bottom_of_strip), record(top_low)]},
            "D139_preparation": {"Q0": 8, "K0": 6, "leaf_strip_length": record(prep_strip)},
            "general_limit": "if top L low labels are actual crossing terminal leaves and L>p_prime, a block containing a non-leaf would include at least L distinct incidences in R",
            "disposition": "EXCLUDE_LENGTH_AT_LEAST_TWO_FOR_P_PRIME_ONE_ON_THE_DECLARED_STRIPS",
        },
        "independent_nonleaf_family": {
            "inherited_parity": "gamma+1-n0 even and nonnegative with all p=1 initialization conditions",
            "twice_T": record(twice_T), "twice_T_margin_over_gamma_plus_one": record(gamma_margin),
            "n": record(initial_n), "c": record(initial_c), "d": record(initial_d),
            "actual_path_neighbors": [record(left), record(right)],
            "boundary_vertex": record(boundary),
            "weights": [record(path_weight), record(difference(boundary, right))],
            "all_low_low_endpoints": "at least gamma by old seed and alternating path bounds; new frontier only crosses",
            "case_a_gt_gamma": {"witness": "actual gamma-to-(2gamma+1) path edge lies in P",
                                "deficit_to_required_minimum": record(difference(polynomial_sum(a, one), path_weight))},
            "case_a_le_gamma": {"P": "empty by physical endpoint bound",
                                 "first_gap_label_at_most": "3+gamma",
                                 "margin_to_d": record(difference(initial_d, polynomial_sum(three, gamma)))},
            "disposition": "EXCLUDE_ALL_PERMITTED_A_AND_T_ON_THE_ADVERSE_FAMILY",
        },
        "positive_compatibility_and_polarity": {
            "D139_D140": "P empty and R={d}; first gap starts at d so strict collision test inapplicable",
            "positive_scope": "retained D139 and D140 transitions unchanged",
            "conjugated_cut_order": ["n+1-c", "n+1-a"],
            "conjugated_shifts": [record(form) for form in conjugated],
            "scope": "canonical oriented exteriors, two positive gaps, exact D134 half-spectrum and preserved cut",
            "open": ["alternative exterior placements", "more cuts", "nonextreme frontier", "other crossing spectra"],
            "disposition": "CONFIRM_RETAINED_POSITIVE_SCOPE_AND_BOTH_POLARITIES",
        },
    }
