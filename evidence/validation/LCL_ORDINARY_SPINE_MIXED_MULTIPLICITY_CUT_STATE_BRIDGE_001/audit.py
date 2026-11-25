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
    """Audit the three formal controls without instantiating any transition."""
    p, pp, half_n, k, s, b, i, image = map(
        atom, ("p", "p_prime", "n_half", "K", "s", "B", "i", "pi_i")
    )
    one, two = atom(1), atom(2)
    n = polynomial_product(two, half_n)
    fresh_size = polynomial_product(two, k)
    m = polynomial_sum(n, fresh_size)
    c = difference(half_n, p)
    d = polynomial_sum(half_n, one)
    lower_shift = difference(difference(fresh_size, s), b)

    # Same-polarity w=0 would use the inherited old frontier label as its weight.
    connector_if_zero = lower_shift
    half_n_slack = difference(half_n, k)
    gap_slack = difference(s, k)
    assert difference(difference(d, one), connector_if_zero) == polynomial_sum(
        half_n_slack, gap_slack, b
    )

    # The number of upper fresh vertices also follows by subtracting upper old labels.
    outgoing_cut = polynomial_sum(half_n, k, pp, one)
    upper_count = polynomial_sum(difference(m, outgoing_cut), difference(c, n))
    assert upper_count == difference(difference(difference(k, p), pp), one)
    outgoing_multiplicity = polynomial_sum(polynomial_product(two, pp), one)
    required_if_equal = polynomial_sum(outgoing_multiplicity, upper_count)
    mismatch = difference(required_if_equal, k)
    assert mismatch == difference(pp, p)
    assert difference({}, mismatch) == difference(p, pp)

    h = polynomial_sum(p, pp, one)
    q = difference(difference(fresh_size, h), one)
    split = k
    upper_capacity = difference(q, split)
    assert difference(q, polynomial_sum(h, one)) == polynomial_product(two, upper_capacity)
    actual_connector = difference(m, h)
    assert actual_connector == polynomial_sum(n, q, one)
    host = difference(polynomial_sum(pp, i), image)
    terminal_label = polynomial_sum(h, c, i)
    terminal_weight = difference(terminal_label, host)
    assert difference(image, i) == difference(pp, host)
    assert terminal_weight == polynomial_sum(d, image)
    assert polynomial_sum(h, upper_count) == k

    cut = polynomial_sum(h, c, split)
    assert cut == outgoing_cut
    returned_cut = difference(polynomial_sum(m, one), cut)
    returned_threshold = polynomial_sum(d, split)
    returned_size_gap = difference(m, polynomial_product(two, returned_cut))
    returned_offset = difference(returned_threshold, returned_cut)
    assert returned_cut == polynomial_sum(c, k, difference(p, pp))
    assert returned_size_gap == polynomial_product(two, pp)
    assert returned_offset == polynomial_sum(pp, one)

    return {
        "same_polarity_connector": {
            "assumptions": ["w=0", "n/2>=K", "s>=K", "B>=0", "A=2K-s-B>=0"],
            "attempted_connector": record(connector_if_zero),
            "nonnegative_slack_terms_to_d_minus_one": [
                record(half_n_slack), record(gap_slack), record(b)
            ],
            "positive_weight_already_consumed": "[1,d-1]",
            "zero_case": "label collision and weight zero outside the alphabet",
            "disposition": "REJECT_SAME_POLARITY",
        },
        "outgoing_multiplicity_mismatch": {
            "assumptions": ["h=2*p_prime+1", "p_prime!=p", "all fresh centers below the cut"],
            "fresh_upper_count": record(upper_count),
            "new_crossing_count_minus_required": record(mismatch),
            "p_prime_gt_p": "too many actual crossing edges",
            "p_prime_lt_p": "too few actual crossing edges",
            "disposition": "REJECT_MIXED_STATE_WITH_OUTGOING_MULTIPLICITY",
        },
        "distinct_state_canonical_bridge": {
            "assumptions": ["p_prime!=p", "h=p+p_prime+1", "Q>=h+1", "H=2K",
                            "both allocation bands permuted"],
            "upper_band_capacity": record(upper_capacity),
            "connector": record(actual_connector),
            "physical_host": record(host),
            "terminal_difference": record(terminal_weight),
            "split": record(split), "returned_cut": record(returned_cut),
            "returned_threshold": record(returned_threshold),
            "returned_size_gap": record(returned_size_gap),
            "returned_cut_offset": record(returned_offset),
            "disposition": "CONFIRM_CONDITIONAL_BRIDGE_IDENTITIES",
        },
    }
