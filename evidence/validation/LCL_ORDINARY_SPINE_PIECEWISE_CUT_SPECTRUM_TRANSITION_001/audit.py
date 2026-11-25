"""Independent retained spine-state and cut and symbolic piecewise arithmetic audit."""

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


def retained_cut_rejection(report):
    """Infer the sole p from the observed crossing minimum and declared cut."""
    n = report["n"]
    cut = report["oriented_cut"]
    d = report["crossing_spectrum"][0]
    p = d - cut - 1
    h = 2 * p + 1
    assert report["actual_cut"] == n and cut == 1 and d == n - 1
    assert p == n - 3 and p >= 1 and h > n
    # Any positive terminal quotas would imply Q>=h and therefore n>=2h.
    return {"n": n, "actual_cut": report["actual_cut"], "oriented_cut": cut,
            "d": d, "required_p": p, "required_h": h, "minimum_n_for_positive_quotas": 2 * h,
            "disposition": "DECLARED_CUT_FAILS_LARGE_PREFIX_STATE"}


def symbolic_checks():
    """Prove coefficient identities for controls without evaluating a profile or allocation."""
    # Basis coordinates are A, c, s, x, i, ell, k, constant.
    a, c, s, x, i, distance, k, one = tuple(tuple(int(u == v) for v in range(8)) for u in range(8))
    low_max = subtract_forms(add_forms(a, c), one)
    high_min = add_forms(a, c, s)
    label_gap = subtract_forms(high_min, low_max)
    assert label_gap == add_forms(s, one)
    shifted_crossing = add_forms(x, s)
    unchanged_noncrossing = add_forms(x, s)
    old_weight_multiset = Counter((shifted_crossing, unchanged_noncrossing))
    assert old_weight_multiset == Counter({shifted_crossing: 2})

    lower_endpoint = i
    upper_endpoint = add_forms(i, distance)
    # The swap is forced by the offsets +ell and -ell in the normalized weight rule.
    lower_coordinate = add_forms(lower_endpoint, distance)
    upper_coordinate = subtract_forms(upper_endpoint, distance)
    assert lower_coordinate == upper_endpoint and upper_coordinate == lower_endpoint
    assert Counter((lower_coordinate, upper_coordinate)) == Counter((lower_endpoint, upper_endpoint))
    lower_membership_gap = subtract_forms(k, lower_endpoint)
    upper_membership_gap = subtract_forms(upper_endpoint, k)
    assert add_forms(lower_membership_gap, upper_membership_gap) == distance
    # Under i<k<=i+ell, the crossing incidence is at the upper gap index but has lower coordinate i.
    return {
        "basis": ["A", "c", "s", "x", "i", "ell", "k", "constant"],
        "old_weight_collision": {
            "assumptions": ["s>=1", "x crosses", "x+s does not cross", "x+s<=n"],
            "band_label_gap": label_gap, "shifted_crossing": shifted_crossing,
            "unchanged_noncrossing": unchanged_noncrossing, "weight_multiplicity": old_weight_multiset[shifted_crossing],
            "disposition": "DUPLICATE_OLD_DIFFERENCE_DESPITE_INJECTIVE_LABELS",
        },
        "split_crossing_transposition": {
            "assumptions": ["i<k", "k<=i+ell", "ell>=1"],
            "lower_gap_index": lower_endpoint, "upper_gap_index": upper_endpoint,
            "split_minus_lower_index": lower_membership_gap, "upper_index_minus_split": upper_membership_gap,
            "removed_upper_coordinate": upper_endpoint, "inserted_lower_coordinate": upper_coordinate,
            "complete_coordinate_multiset_preserved": True,
            "disposition": "REJECT_RETURN_CROSSING_BAND",
        },
    }
