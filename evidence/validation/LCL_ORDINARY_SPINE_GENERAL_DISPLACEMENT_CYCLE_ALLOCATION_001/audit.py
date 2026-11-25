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


def symbolic_checks():
    """Check coefficient identities for the three structural controls only."""
    basis = ["p", "Q", "pN", "k", "T", "W", "w_next", "u", "v", "shift", "M", "constant"]
    p, q, p_times_n, k, t, w, w_next, u, v, shift, moment, one = tuple(
        tuple(int(i == j) for j in range(len(basis))) for i in range(len(basis))
    )
    zero = subtract_forms(one, one)
    middle_displacement = subtract_forms(p, p)
    nearby_displacement = subtract_forms(p, subtract_forms(p, one))
    changed_moment = add_forms(subtract_forms(moment, middle_displacement), nearby_displacement)
    changed_q = add_forms(subtract_forms(q, one), one)
    assert middle_displacement == zero and nearby_displacement == one
    assert changed_q == q and subtract_forms(changed_moment, moment) == one

    # Translating a whole cycle preserves the displacement on every arc.
    translated_source = add_forms(u, shift)
    translated_target = add_forms(v, shift)
    assert subtract_forms(translated_target, translated_source) == subtract_forms(v, u)
    # Pick an upper-source to lower-image arc of the symbolic straddling cycle.
    # Its existence follows from cyclic traversal, and the reverse crossing exists too.
    upper_source_slack = subtract_forms(translated_source, k)
    lower_target_gap = subtract_forms(k, translated_target)
    assert add_forms(upper_source_slack, lower_target_gap) == subtract_forms(u, v)

    slack = subtract_forms(k, t)
    max_width = add_forms(p, p)
    integer_slack_limit = subtract_forms(max_width, one)
    assert subtract_forms(max_width, integer_slack_limit) == one
    # When a next block exists, its integer width exceeds slack by at least one.
    next_block_slack = subtract_forms(subtract_forms(w_next, slack), one)
    assert subtract_forms(integer_slack_limit, slack) == add_forms(
        subtract_forms(max_width, w_next), next_block_slack
    )
    capacity_premise_slack = subtract_forms(q, add_forms(p_times_n, integer_slack_limit))
    width_estimate_slack = subtract_forms(p_times_n, w)
    upper_space = subtract_forms(q, k)
    upper_demand = subtract_forms(w, t)
    upper_margin = subtract_forms(upper_space, upper_demand)
    assert upper_margin == add_forms(
        capacity_premise_slack, width_estimate_slack, subtract_forms(integer_slack_limit, slack)
    )
    return {
        "basis": basis,
        "quota_moment_perturbation": {
            "assumptions": ["M=0", "r_p>=2", "all physical quotas positive", "p>=1"],
            "total_after": changed_q, "moment_change": subtract_forms(changed_moment, moment),
            "positive_after": "middle quota still >=1; p-1 quota increases",
            "disposition": "REJECT_BY_QUOTA_MOMENT",
        },
        "cycle_crossing_split": {
            "assumptions": ["translate one entire nontrivial cycle into free slots in a straddling interval",
                            "u+shift>=k", "v+shift<k"],
            "source": translated_source, "image": translated_target,
            "source_minus_split": upper_source_slack, "split_minus_image": lower_target_gap,
            "edge_displacement": subtract_forms(translated_target, translated_source),
            "whole_cycle_displacements_preserved": True,
            "global_permutation_preserved": True,
            "disposition": "REJECT_RETURN_CROSSING_BAND",
        },
        "limiting_capacity": {
            "assumptions": ["if a next block exists: 0<=k-T<w_next<=2p", "W<=pN", "Q>=pN+2p-1"],
            "integer_slack_maximum": integer_slack_limit, "upper_demand": upper_demand,
            "upper_capacity": upper_space, "upper_margin": upper_margin,
            "nonnegative_margin_terms": ["Q-pN-(2p-1)", "pN-W", "(2p-1)-(k-T)"],
            "all_fit_case": "W=T; upper demand is zero",
            "disposition": "SUFFICIENT_CAPACITY_ONLY",
        },
    }
