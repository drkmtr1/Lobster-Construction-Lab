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
    """Check the seven symbolic controls without allocating fresh labels."""
    gamma, a, A, B, s, t, K, j, x, y, h, hu, tlu, tul, tuu = map(
        atom, ("gamma", "a", "A", "B", "s", "t", "K", "j", "x", "y", "h",
               "h_U", "T_LU", "T_UL", "T_UU")
    )
    one, two, three, four, six = map(atom, (1, 2, 3, 4, 6))
    half_n = polynomial_sum(polynomial_product(two, gamma), three)
    n = polynomial_sum(polynomial_product(four, gamma), six)
    c = polynomial_sum(polynomial_product(two, gamma), two)
    d = polynomial_sum(polynomial_product(two, gamma), four)
    assert n == polynomial_product(two, half_n)
    assert c == difference(half_n, one) and d == polynomial_sum(half_n, one)
    H = polynomial_sum(A, B, s)
    m = polynomial_sum(n, H)
    lower, middle, upper = A, polynomial_sum(A, t), polynomial_sum(A, s)
    increments = ({}, difference(middle, lower), difference(upper, middle), difference(upper, lower))
    assert increments == ({}, t, difference(s, t), s)
    for index, u in enumerate(increments):
        for v in increments[index+1:]:
            assert difference(polynomial_sum(x, u), polynomial_sum(y, v)) == polynomial_sum(
                difference(x, y), difference(u, v)
            )
    g1_first = polynomial_sum(A, a)
    g1_last = difference(polynomial_sum(middle, a), one)
    g2_first = polynomial_sum(middle, c)
    g2_last = difference(polynomial_sum(upper, c), one)
    assert polynomial_sum(difference(g1_last, g1_first), one) == t
    assert polynomial_sum(difference(g2_last, g2_first), one) == difference(s, t)
    assert difference(g2_first, g1_last) == polynomial_sum(difference(c, a), one)
    assert polynomial_sum(n, upper, one) == polynomial_sum(difference(m, B), one)

    preliminary_N = polynomial_product(three, gamma)
    preliminary_Q0 = polynomial_sum(gamma, two)
    assert polynomial_sum(preliminary_N, preliminary_Q0, four) == n
    assert difference(polynomial_sum(preliminary_N, one), difference(preliminary_N, j)) == polynomial_sum(j, one)
    path_weight_base = polynomial_sum(preliminary_N, preliminary_Q0)
    first_R_index = difference(polynomial_product(two, a), two)
    final_R_index = difference(polynomial_product(two, gamma), two)
    r = difference(path_weight_base, first_R_index)
    assert r == difference(difference(n, polynomial_product(two, a)), two)
    assert difference(path_weight_base, final_R_index) == d
    assert path_weight_base == difference(n, four)
    assert difference(r, d) == polynomial_product(two, difference(gamma, a))
    max_p = difference(difference(c, one), gamma)
    assert max_p == polynomial_sum(gamma, one)
    unchanged_lo = polynomial_sum(max_p, one)
    assert unchanged_lo == polynomial_sum(gamma, two)

    required_shift_for_max_p = difference(d, max_p)
    assert required_shift_for_max_p == polynomial_sum(gamma, three)
    assert difference(polynomial_sum(one, required_shift_for_max_p), unchanged_lo) == two
    assert difference(d, K) == polynomial_sum(difference(half_n, K), one)
    m_for_cut = polynomial_sum(n, polynomial_product(two, K))
    same_cut = polynomial_sum(c, K)
    flipped_cut = polynomial_sum(same_cut, three)
    assert flipped_cut == difference(polynomial_sum(m_for_cut, one), same_cut)
    U = difference(difference(m_for_cut, flipped_cut), difference(n, c))
    assert U == difference(K, three)
    assert difference(flipped_cut, polynomial_sum(A, c, t)) == difference(polynomial_sum(K, three),
                                                                         polynomial_sum(A, t))
    assert difference(polynomial_sum(A, c, s), flipped_cut) == difference(polynomial_sum(A, s),
                                                                         polynomial_sum(K, three))

    sh = difference(s, t)
    r_shifted_end = polynomial_sum(r, sh)
    missing_after_r = polynomial_sum(r_shifted_end, one)
    missing_through_r = polynomial_sum(r, s)
    assert polynomial_sum(difference(missing_through_r, missing_after_r), one) == t
    final_residual_start = polynomial_sum(n, s, one)
    assert polynomial_sum(difference(m, final_residual_start), one) == polynomial_sum(A, B)
    threshold = polynomial_sum(d, K)
    short_gap_crossing_size = difference(polynomial_sum(d, sh), threshold)
    long_gap_crossing_size = difference(polynomial_sum(d, s), threshold)
    assert short_gap_crossing_size == difference(sh, K)
    assert long_gap_crossing_size == difference(s, K)
    assert difference(K, required_shift_for_max_p) == difference(difference(K, gamma), three)

    n_plus_s = polynomial_sum(n, s)
    gap_to_upper_max = difference(m, g1_first)
    assert difference(gap_to_upper_max, n_plus_s) == difference(B, a)
    assert difference(n_plus_s, g2_last) == difference(polynomial_sum(half_n, two), A)
    gap_to_gap_max = difference(g2_last, g1_first)
    assert difference(n_plus_s, gap_to_gap_max) == polynomial_sum(difference(n, c), a, one)
    connector = difference(m, A)
    assert connector == polynomial_sum(n_plus_s, B)
    terminal_m_minus_1 = difference(difference(m, one), j)
    assert difference(terminal_m_minus_1, connector) == difference(difference(A, one), j)
    assert terminal_m_minus_1 == difference(m, polynomial_sum(j, one))

    upper_fresh = polynomial_sum(one, hu, tlu, tuu)
    crossing_fresh = polynomial_sum(one, difference(h, hu), tlu, tul)
    assert difference(crossing_fresh, upper_fresh) == polynomial_sum(
        difference(h, polynomial_product(two, hu)), difference(tul, tuu)
    )
    max_missing_partner = difference(m, missing_through_r)
    min_missing_partner = difference(max_missing_partner, difference(B, one))
    assert max_missing_partner == polynomial_sum(A, B, polynomial_product(two, a), two)
    assert min_missing_partner == polynomial_sum(A, polynomial_product(two, a), three)
    assert difference(missing_through_r, gap_to_gap_max) == difference(difference(d, a), one)
    assert difference(g1_last, min_missing_partner) == difference(difference(t, a), four)
    assert difference(max_missing_partner, g2_first) == difference(
        polynomial_sum(B, polynomial_product(two, difference(a, gamma))), t
    )

    conjugate = [difference(difference(m, n), e) for e in (upper, middle, lower)]
    assert conjugate == [B, polynomial_sum(B, sh), polynomial_sum(B, s)]
    assert difference(conjugate[1], conjugate[0]) == sh
    assert difference(conjugate[2], conjugate[1]) == t
    return {
        "four_class_variable_exterior_resources": {
            "old_classes": ["W00", "P", "R", "W11"],
            "increments": [record(v) for v in increments],
            "pairwise_collision": "x-y=v-u for original weights x,y with increments u,v",
            "fresh_label_intervals": [[[], record(difference(A, one))],
                                      [record(g1_first), record(g1_last)],
                                      [record(g2_first), record(g2_last)],
                                      [record(polynomial_sum(difference(m, B), one)), record(m)]],
            "fresh_difference_complement": "complement in [1,m] of all four translated classes",
            "necessary": "old minimum crossing gains at least K; hence s>=K and A+B<=K",
            "disposition": "CONFIRM_EXACT_VARIABLE_EXTERIOR_RESOURCES",
        },
        "D141_actual_incidence_regimes": {
            "path_index_interval_for_R": [record(first_R_index), record(final_R_index)],
            "oriented_low_path_endpoint": "j+1 on the preliminary high entry N-j",
            "path_R_weights": [record(d), record(r)],
            "a_one": "all path crossings in R; r=n-4",
            "a_gamma": "only final path crossing in R; r=d",
            "other_crossings": "four actual frontier edges [n-3,n], with low endpoint zero",
            "a_le_gamma": "P empty by low-low endpoint bound",
            "a_gt_gamma": {"R": "empty", "max_P": record(max_p),
                           "unchanged_interval": [record(unchanged_lo), record(difference(d, one))]},
            "disposition": "CONFIRM_ACTUAL_SUPPLIED_INPUT_SPECTRA",
        },
        "forced_polarity_and_cut": {
            "zero_case": "A=0 repeats vertex zero; positive A repeats W00 or requires A in P",
            "large_cut_shift": record(required_shift_for_max_p),
            "zero_case_contradiction": "A+t>=d forced by unchanged interval, while membership gives A+t<=K<d",
            "forced": "w=m",
            "new_cut": record(flipped_cut), "upper_fresh": record(U),
            "membership": "A+t<=K+3<=A+s",
            "upper_exterior": "1<=B<=K-3",
            "disposition": "FORCE_MAXIMUM_ON_ORIENTED_PLACEMENT",
        },
        "exact_residual_admission": {
            "a_le_gamma": {
                "test": "membership and s-t>=K",
                "residual": ["[d,d+s-t-1]", "[r+s-t+1,r+s]", "[n+s+1,m]"],
                "crossing_first_interval_size": record(short_gap_crossing_size),
                "noncrossing_demand": "[d,d+K-1]",
                "crossing_demand": "the rest of the residual",
            },
            "a_gt_gamma": {
                "test": "membership, P+t subset [d,d+K-1], s>=K",
                "residual": ["P", "[d,d+s-1] minus (P+t)", "[n+s+1,m]"],
                "crossing_first_interval_size": record(long_gap_crossing_size),
                "noncrossing_demand": "P and [d,d+K-1] minus (P+t)",
                "crossing_demand": "[d+K,d+s-1] and [n+s+1,m]",
            },
            "scope": "exact old-image compatibility; fresh demands require an actual assignment",
            "disposition": "CONFIRM_BOTH_OLD_IMAGE_TESTS_AND_SIDE_DEMANDS",
        },
        "exterior_connectivity": {
            "assumption": "B<=a",
            "gap_upper_max_minus_n_plus_s": record(difference(gap_to_upper_max, n_plus_s)),
            "low_to_gap_margin": record(difference(n_plus_s, g2_last)),
            "gap_to_gap_margin": record(difference(n_plus_s, gap_to_gap_max)),
            "connector": record(connector),
            "tree": "A+B exterior vertices and A+B-1 exact high internal weights force a connected induced tree",
            "boundary": "A=0 forces B=1, a singleton",
            "role_rigidity": "every lower exterior vertex is a center and every upper exterior vertex other than w a terminal",
            "m_minus_one_collision": "j=A-1 repeats the connector; j<A-1 repeats attachment to j+1",
            "conclusion": "B=1, A<=h, only in the B<=a regime",
            "disposition": "CONFIRM_CONDITIONAL_EXTERIOR_RIGIDITY",
        },
        "physical_crossing_and_endpoint_exclusion": {
            "upper_vertices": record(upper_fresh), "crossing_incidences": record(crossing_fresh),
            "balance": "h-3=2*h_U+T_UU-T_UL",
            "extra_assumptions": "a<=gamma and r>A+c-1",
            "required_weight": record(missing_through_r),
            "allowable_gap_partner_interval": [record(min_missing_partner), record(max_missing_partner)],
            "first_gap_intersection_margin": record(difference(g1_last, min_missing_partner)),
            "second_gap_intersection_margin": record(difference(max_missing_partner, g2_first)),
            "B_one": "w attachment requires t>=a+4 or a=gamma,t=1",
            "scope": "excludes an empty required intersection; remaining fresh feasibility unresolved",
            "disposition": "CONFIRM_ROLE_BALANCE_AND_MISSING_WEIGHT_SUBREGION",
        },
        "retained_compatibility_and_limits": {
            "D139_D140": "named singleton leaf has P empty, R={d}; established positive input domains retain scope",
            "D141": "independent non-leaf supply and canonical three-center exclusion retained",
            "conjugated_shifts": [record(v) for v in conjugate],
            "conjugated_cuts": ["n+1-c", "n+1-a"],
            "return_limit": "a future ordinary p=1 return alone would not certify the D141 initializer incidences",
            "disposition": "CONFIRM_RETAINED_SCOPE_AND_BOTH_ACTUAL_POLARITIES",
        },
    }
