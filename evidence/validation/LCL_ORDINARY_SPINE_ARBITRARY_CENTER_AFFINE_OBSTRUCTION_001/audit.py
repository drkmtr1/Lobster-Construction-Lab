"""Independent retained spine-state and formal affine arithmetic audit."""

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


def add_forms(*terms):
    return tuple(sum(group) for group in zip(*terms, strict=True))


def subtract_forms(left, right):
    return add_forms(left, tuple(-coefficient for coefficient in right))


def symbolic_checks():
    """Check symbolic coefficient identities for the three structural controls."""
    # Basis coordinates are n, h, Q, kappa, high index i, center label j, constant.
    n, h, q_total, kappa, i, j, one = tuple(tuple(int(x == y) for y in range(7)) for x in range(7))
    zero = subtract_forms(one, one)
    two = add_forms(one, one)
    m = add_forms(n, h, q_total, one)
    old_frontier = add_forms(h, kappa)
    new_frontier = add_forms(n, h, one, kappa)
    assert subtract_forms(new_frontier, old_frontier) == add_forms(n, one)
    assert subtract_forms(m, new_frontier) == subtract_forms(q_total, kappa)
    coordinate = subtract_forms(add_forms(i, h), add_forms(one, j))
    first_upper_weight = add_forms(kappa, h)
    largest_lower_candidate = subtract_forms(first_upper_weight, two)
    last_lower_weight = subtract_forms(kappa, one)
    smallest_upper_candidate = add_forms(kappa, one)
    assert subtract_forms(first_upper_weight, largest_lower_candidate) == two
    assert subtract_forms(smallest_upper_candidate, last_lower_weight) == two

    # Control 2. Substitute the equality n=h+Q before comparing integer bounds.
    within_interval_width = add_forms(h, q_total)
    n_at_equality = add_forms(h, q_total)
    smallest_new_weight = add_forms(n_at_equality, one)
    equality_gap = subtract_forms(smallest_new_weight, within_interval_width)
    assert equality_gap == one

    # Control 3. Positive slack in either band breaks its exact sum identity.
    lower_increment = subtract_forms(coordinate, i)
    upper_extremum = subtract_forms(add_forms(i, h), one)
    upper_loss = subtract_forms(upper_extremum, coordinate)
    lower_nonnegative_slack = subtract_forms(h, add_forms(two, j))
    upper_nonnegative_slack = subtract_forms(j, one)
    assert lower_increment == add_forms(one, lower_nonnegative_slack)
    assert upper_loss == add_forms(one, upper_nonnegative_slack)
    # Both slacks are nonnegative under 1 <= j <= h-2.

    # Control 4. Substitute h=2 symbolically without instantiating any section.
    h_two = two
    intermediate_upper = subtract_forms(h_two, two)
    assert intermediate_upper == zero and subtract_forms(one, intermediate_upper) == one
    low_count = add_forms(subtract_forms(last_lower_weight, zero), one)
    two_center_upper_first = add_forms(kappa, h_two)
    two_center_upper_last = subtract_forms(add_forms(q_total, h_two), one)
    high_count = add_forms(subtract_forms(two_center_upper_last, two_center_upper_first), one)
    assert low_count == kappa and high_count == subtract_forms(q_total, kappa)
    assert add_forms(low_count, high_count) == q_total
    return {
        "basis": ["n", "h", "Q", "kappa", "i", "j", "constant"],
        "normalized_terminal_coordinate": coordinate,
        "forced_connector": subtract_forms(new_frontier, old_frontier),
        "hypothetical_return": subtract_forms(m, new_frontier),
        "equality_boundary": {
            "assumption": "n=h+Q", "within_interval_upper_bound": within_interval_width,
            "minimum_new_weight": smallest_new_weight, "strict_gap": equality_gap,
            "disposition": "WITHIN_INTERVAL_EDGE_EXCLUDED",
        },
        "intermediate_host": {
            "assumption": "1<=j<=h-2",
            "lower_increment": lower_increment, "upper_loss": upper_loss,
            "lower_nonnegative_slack": lower_nonnegative_slack,
            "upper_nonnegative_slack": upper_nonnegative_slack,
            "positive_decompositions": ["1+(h-2-j)", "1+(j-1)"],
            "disposition": "BOTH_EXACT_BAND_SUMS_FORBID_INTERMEDIATE_HOSTS",
        },
        "two_center_specialization": {
            "assumption": "h=2", "intermediate_interval": [1, 0],
            "center_one_quota": low_count, "center_zero_quota": high_count,
            "disposition": "D132_QUOTA_MATCHING",
        },
    }
