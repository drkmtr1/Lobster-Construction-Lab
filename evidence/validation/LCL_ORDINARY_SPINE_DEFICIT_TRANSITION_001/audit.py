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
    """Formal affine identities only. No quota value, graph or extension is constructed."""
    # Coefficients are in the basis (n, r, delta, terminal index k, constant).
    n, r, delta, k, one = tuple(tuple(int(i == j) for j in range(5)) for i in range(5))
    two = add_forms(one, one)
    zero = subtract_forms(one, one)
    m = add_forms(n, r, two)
    old_v = add_forms(one, delta)
    new_w = add_forms(n, two, delta)
    connector = subtract_forms(new_w, old_v)
    returned = subtract_forms(m, new_w)
    assert connector == add_forms(n, one)
    assert returned == subtract_forms(r, delta)
    assert subtract_forms(new_w, m) == subtract_forms(delta, r)

    # Substitute the two equality cases without choosing n, r or k.
    first_w = add_forms(n, two, zero)
    last_w = add_forms(n, two, r)
    first_terminal = add_forms(n, two, k, one)
    last_terminal = add_forms(n, two, k)
    assert first_w == add_forms(n, two) and last_w == m
    assert subtract_forms(first_terminal, first_w) == add_forms(k, one)
    assert subtract_forms(last_w, last_terminal) == subtract_forms(r, k)
    assert subtract_forms(m, first_w) == r and subtract_forms(m, last_w) == zero

    # Control 4 substitutes delta=r+1 formally, under r+1 <= n.
    rejected_delta = add_forms(r, one)
    rejected_w = add_forms(n, two, rejected_delta)
    rejected_return = subtract_forms(m, rejected_w)
    assert rejected_w == add_forms(m, one)
    assert rejected_return == subtract_forms(zero, one)
    return {
        "basis": ["n", "r", "delta", "k", "constant"], "connector": connector, "returned_deficit": returned,
        "endpoint_cases": {"delta=0": {"frontier": first_w, "terminals": first_terminal},
                           "delta=r": {"frontier": last_w, "terminals": last_terminal}},
        "control": {"assumption": "delta=r+1 with r>=1 and r+1<=n", "delta_coefficients": rejected_delta,
                    "frontier_coefficients": rejected_w, "frontier_relative_to_m": subtract_forms(rejected_w, m),
                    "returned_deficit": rejected_return[-1], "disposition": "REJECT_BEFORE_EMISSION",
                    "numerical_extension_constructed": False},
    }
