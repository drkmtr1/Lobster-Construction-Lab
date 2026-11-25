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
    """Check formal control identities without sampling a quota or a permutation."""
    p, a, b, s, i, j, u, pc, mc, up, um = map(
        atom, ("p", "a", "b", "s", "i", "j", "u", "P_a", "M_b", "U_a", "V_b")
    )
    one = atom(1)
    packet_width = polynomial_sum(p, p)
    separate_spans = polynomial_product(p, polynomial_sum(p, one))
    saved = polynomial_product(p, difference(p, one))
    assert difference(separate_spans, packet_width) == saved
    first_upper = polynomial_sum(i, p)
    second_upper = polynomial_sum(j, p)
    start_separation = difference(j, i)
    shared_span_margin = difference(first_upper, j)
    assert difference(second_upper, first_upper) == start_separation
    assert shared_span_margin == difference(p, start_separation)
    assert difference(first_upper, i) == p
    assert difference(second_upper, j) == p

    mass = polynomial_product(a, b)
    z = difference(mass, one)
    assert difference(mass, z) == one
    packet_positive_mass = polynomial_product(a, polynomial_product(u, b))
    packet_negative_mass = polynomial_product(b, polynomial_product(u, a))
    assert packet_positive_mass == packet_negative_mass == polynomial_product(u, mass)
    positive_original_mass = polynomial_product(a, pc)
    negative_original_mass = polynomial_product(b, mc)
    positive_packet_mass = polynomial_product(a, up)
    negative_packet_mass = polynomial_product(b, um)
    positive_residue = difference(positive_original_mass, positive_packet_mass)
    negative_residue = difference(negative_original_mass, negative_packet_mass)
    assert positive_residue == polynomial_product(a, difference(pc, up))
    assert negative_residue == polynomial_product(b, difference(mc, um))
    # Summation over all types conserves the original balanced moment.
    positive_total, negative_total, packet_total = map(
        atom, ("positive_total", "negative_total", "packet_total")
    )
    residual_imbalance = difference(difference(positive_total, packet_total),
                                    difference(negative_total, packet_total))
    assert residual_imbalance == difference(positive_total, negative_total)

    small_lower = difference(s, one)
    small_upper = b
    large_lower = difference(b, one)
    large_upper = s
    small_out = polynomial_sum(small_lower, a)
    small_in = difference(small_upper, b)
    large_out = polynomial_sum(large_lower, a)
    large_in = difference(large_upper, b)
    assert difference(s, small_lower) == one and difference(small_upper, s) == difference(b, s)
    assert difference(s, large_lower) == polynomial_sum(difference(s, b), one)
    assert difference(large_upper, s) == {}
    assert difference(small_out, s) == difference(a, one) and small_in == {}
    assert difference(large_out, s) == difference(difference(polynomial_sum(a, b), one), s)
    assert difference(s, large_in) == b
    assert difference(small_out, small_lower) == difference(large_out, large_lower) == a
    assert difference(small_in, small_upper) == difference(large_in, large_upper) == difference({}, b)
    return {
        "interleaved_equal_magnitude": {
            "assumptions": ["p>=2", "0<=i<j<p for distinct cycles", "a=b=p"],
            "occupied_classes": ["{i,i+p} is one residue class mod p",
                                 "duplicating that class repeats both occupied positions"],
            "separation_of_upper_endpoints": record(start_separation),
            "overlapping_span_margin": record(shared_span_margin),
            "packet_width": record(packet_width),
            "separate_span_width": record(separate_spans),
            "exact_saving": record(saved),
            "disposition": "DISTINCT_CYCLES_SHARE_SPANS_WITHOUT_COORDINATE_OVERLAP",
        },
        "rounding_and_token_custody": {
            "assumptions": ["a,b>=1", "ab>=2 for a nonempty match", "z=ab-1",
                            "U_a and V_b are total integer packet token uses",
                            "weighted matches conserve each full type's mass",
                            "original positive and negative moments agree"],
            "matched_mass": record(z), "rounded_up_excess": record(difference(mass, z)),
            "complete_packets_from_match": 0,
            "packet_mass_on_either_side": record(packet_positive_mass),
            "positive_residue_mass": record(positive_residue),
            "negative_residue_mass": record(negative_residue),
            "aggregate_custody": "per type, sum of match remainders equals magnitude times its integer residual count",
            "aggregate_balance": "each residual moment is the original moment minus the same total packet mass",
            "per_match_token_divisibility_assumed": False,
            "disposition": "REJECT_UPWARD_ROUNDING",
        },
        "packet_crossing_split": {
            "assumptions": ["1<=a,b<=p", "1<=s<a+b", "one entire packet straddles the split"],
            "s_le_b": {"lower_source": record(small_lower), "lower_image": record(small_out),
                       "upper_source": record(small_upper), "upper_image": record(small_in)},
            "s_gt_b": {"lower_source": record(large_lower), "lower_image": record(large_out),
                       "upper_source": record(large_upper), "upper_image": record(large_in)},
            "global_permutation_preserved": True,
            "displacement_multiplicities_preserved": True,
            "disposition": "REJECT_RETURN_CROSSING_BAND",
        },
    }
