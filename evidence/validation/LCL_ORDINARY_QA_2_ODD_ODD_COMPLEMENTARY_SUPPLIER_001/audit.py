"""Independent reconstruction of the retained (q,a)=(5,3) boundary."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json


def canonical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def topology(original):
    profile = [[5, 3], [2]]
    spine = ["s:0", "s:1"]
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    reconstructed = [spine.copy()]
    for section, branches in enumerate(profile):
        for branch, quota in enumerate(branches):
            host = f"b:{section}:{branch}"
            roles[host] = {"kind": "branch", "section": section, "branch": branch}
            reconstructed.append([spine[section], host])
            for k in range(quota):
                vertex = f"l:{section}:{branch}:{k}"
                roles[vertex] = {"kind": "leaf", "section": section, "branch": branch, "leaf": k}
                reconstructed.append([host, vertex])
    graph = original["graph"]
    edges = Counter(tuple(sorted(e)) for e in graph["edges"])
    assert edges == Counter(tuple(sorted(e)) for e in reconstructed)
    assert len(edges) == sum(edges.values()) == 14
    assert sorted(roles) == sorted(graph["vertices"]) and len(roles) == 15
    assert graph["roles"] == roles and graph["profile"] == profile and graph["spine"] == spine
    assert graph["schema_version"] == 1 and graph["edges"] == reconstructed
    digest = canonical_sha({"vertices": sorted(roles), "edges": sorted(edges.elements()),
                            "roles": roles, "profile": profile, "spine": spine})
    assert digest == original["graph_digest"]
    adjacent = {name: set() for name in roles}
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    distance = dict.fromkeys(spine, 0)
    queue = deque(spine)
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacent[vertex] - distance.keys():
            distance[neighbor] = distance[vertex] + 1
            queue.append(neighbor)
    role_distance = {"spine": 0, "branch": 1, "leaf": 2}
    assert distance == {v: role_distance[role["kind"]] for v, role in roles.items()}
    return reconstructed, adjacent, distance


def residual_components(core, remain_labels, remain_weights):
    a, b = "b:0:0", "b:0:1"
    host_sum = core[a] + core[b]
    host_gap = core[a] - core[b]
    components = defaultdict(list)
    options = {}
    for x in sorted(remain_labels):
        assert core[b] < x < core[a]
        absolute = {h: abs(core[h] - x) for h in (a, b)}
        assert sum(absolute.values()) == host_gap
        eligible = {h: d for h, d in absolute.items() if d in remain_weights}
        assert eligible
        options[x] = {"weights": absolute, "eligible": eligible}
        components[tuple(sorted(set(eligible.values())))].append(x)
    assert Counter(d for group in components for d in group) == Counter(remain_weights)
    decomposition = []
    for group, labels in sorted(components.items()):
        assert len(group) == len(labels)
        x = labels[0]
        eligible = options[x]["eligible"]
        if len(group) == 2:
            y = labels[1]
            assert x + y == host_sum and x != y and len(eligible) == 2
            assert eligible == {a: options[y]["eligible"][b], b: options[y]["eligible"][a]}
            kind, lower_counts = "parallel_pair", [0, 2]
        elif len(eligible) == 2:
            assert 2*x == host_sum and eligible[a] == eligible[b]
            kind, lower_counts = "midpoint_loop", [0, 1]
        else:
            assert eligible == {a: group[0]} and host_sum-x in core.values()
            kind, lower_counts = "forced_half_edge", [0]
        decomposition.append({"kind": kind, "labels": labels, "difference_vertices": list(group),
                              "label_count": len(labels), "difference_count": len(group),
                              "attainable_lower_counts": lower_counts})
    observed = {row["kind"]: [] for row in decomposition}
    for row in decomposition:
        observed[row["kind"]].append(row["labels"])
    assert observed == {"parallel_pair": [[5, 9], [6, 8]], "midpoint_loop": [[7]], "forced_half_edge": [[4]]}
    c = len(observed["parallel_pair"])
    eta = len(observed["midpoint_loop"])
    projection = sorted({2*j + epsilon for j in range(c+1) for epsilon in range(eta+1)})
    assert projection == list(range(6))
    return {"options": options, "components": decomposition, "lower_host": b, "higher_host": a,
            "A0": 0, "c": c, "eta": eta, "integral_projection": projection, "selected_j": 0, "selected_epsilon": 1}


def boundary(original, record, retained):
    edges, adjacent, distance = topology(original)
    cert = record["certificate"]
    labels = cert["labels"]
    digest = original["graph_digest"]
    assert cert["graph_digest"] == retained["graph_digest"] == digest
    assert cert["ledger_id"] == retained["ledger_id"] == canonical_sha(
        {"graph_digest": digest, "labels": sorted(labels.items())})
    assert set(labels) == set(adjacent) and all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(15))
    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    assert sorted(weights) == list(range(1, 15)) and weights == retained["checker"]["edge_differences"]
    a, b, right = "b:0:0", "b:0:1", "b:1:0"
    first_quota, second_quota = original["graph"]["profile"][0]
    m = len(edges)
    assert (first_quota, second_quota, m) == (5, 3, first_quota + second_quota + 6)
    core_names = ("s:0", "s:1", a, b, right, "l:0:1:0", f"l:0:1:{second_quota-1}", "l:1:0:0", "l:1:0:1")
    core = dict(zip(core_names, (0, m, m-2, 2, 1, 3, m-1, m-4, m-3), strict=True))
    assert core == {v: labels[v] for v in core_names} == record["construction"]["core"]
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    occupied = [abs(core[u] - core[v]) for u, v in core_edges]
    assert set(core.values()) == {0, 1, 2, 3, 10, 11, 12, 13, 14}
    assert sorted(occupied) == [1, 2, 9, 10, 11, 12, 13, 14]
    vacant = set(labels) - set(core)
    assert all(len(adjacent[v]) == 1 and adjacent[v] <= {a, b} for v in vacant)
    slots = {h: sorted(vacant & adjacent[h]) for h in (a, b)}
    assert slots[a] == [f"l:0:0:{i}" for i in range(first_quota)]
    assert slots[b] == [f"l:0:1:{i}" for i in range(1, second_quota-1)]
    remain_labels = set(range(15)) - set(core.values())
    remain_weights = set(range(1, 15)) - set(occupied)
    assert remain_labels == set(range(4, 10)) and remain_weights == set(range(3, 9))
    components = residual_components(core, remain_labels, remain_weights)
    t, j = m//2, (second_quota-3)//2
    lo, hi = (first_quota+9)//2, (first_quota+2*second_quota+3)//2
    assert 0 <= j <= components["c"] and (lo, hi) == (t-j, t+j)
    interval = set(range(lo, hi+1))
    assert interval <= set(range(5, m-4)) and {m-x for x in interval} == interval
    assert len(interval) == second_quota-2 and len(remain_labels-interval) == first_quota
    low_weights = Counter(abs(core[b]-x) for x in interval)
    assert low_weights == Counter(abs(core[a]-x) for x in interval)
    actual = {h: [labels[v] for v in slots[h]] for h in slots}
    assert actual == {a: sorted(remain_labels-interval), b: sorted(interval)}
    selected_pairs = [row for row in components["components"]
                      if row["kind"] == "parallel_pair" and set(row["labels"]) <= interval]
    assert len(selected_pairs) == j == components["selected_j"]
    assert t in interval and components["selected_epsilon"] == 1
    saved_groups = {tuple(sorted(row["labels"])): (row["host"], sorted(row["weights"]))
                    for row in record["construction"]["allocation_groups"]}
    expected_groups = {tuple(row["labels"]): (b if row["kind"] == "midpoint_loop" else a, row["difference_vertices"])
                       for row in components["components"]}
    assert saved_groups == expected_groups
    quotas = {h: len(xs) for h, xs in actual.items()}
    assert quotas == {a: 5, b: 1} and quotas[b] in components["integral_projection"]
    assert Counter(abs(core[h] - x) for h, xs in actual.items() for x in xs) == Counter(remain_weights)

    assert adjacent["s:1"] == {"s:0", right} and distance[right] == 1
    pins = {v: labels[v] for v in ("s:0", "s:1", right)}
    assert pins == {"s:0": 0, "s:1": len(edges), right: 1}
    roles = original["graph"]["roles"]
    parity = {v: (distance[v] + roles[v]["section"]) % 2 for v in labels}
    signed = []
    for u, v in edges:
        assert parity[u] != parity[v]
        tail, head = (u, v) if parity[u] == 0 else (v, u)
        signed.append({"edge": [tail, head], "signed": labels[head] - labels[tail]})
    negatives = [row for row in signed if row["signed"] < 0]
    expected_signs = [-1, *(2-x for x in sorted(interval)), 3-m]
    assert negatives == [{"edge": [leaf, b], "signed": value} for leaf, value in
                         zip(("l:0:1:0", "l:0:1:1", "l:0:1:2"), expected_signs, strict=True)]
    return {"core": {"labels": core, "edges": core_edges, "occupied_differences": sorted(occupied)},
            "residual_labels": sorted(remain_labels), "residual_differences": sorted(remain_weights),
            "r226": components, "midpoint": t, "j": j, "lower_interval": [lo, hi], "allocation": actual, "actual_quotas": quotas, "slots": slots,
            "checked_formula_vertices": sorted(labels), "vertex_bijection": True, "difference_bijection": True,
            "unused_labels": [], "unused_differences": [], "observed_negative_incidences": negatives,
            "d112_compatibility": {"spine": ["s:0", "s:1"], "exit_neighbors": sorted(adjacent["s:1"]),
                                   "off_spine_host_distance": distance[right], "pins": pins}}


def controls(original, cert, probes, boundary_report):
    edges = original["graph"]["edges"]
    labels = cert["labels"]
    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    wrong = probes["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["edge_differences"] == weights

    p, q = "l:0:0:0", "l:0:1:1"
    cross = labels | {p: labels[q], q: labels[p]}
    new_weights = [abs(cross[u] - cross[v]) for u, v in edges]
    changes = [[e, d, f] for e, d, f in zip(edges, weights, new_weights, strict=True) if d != f]
    assert changes == [[["b:0:0", p], 8, 5], [["b:0:1", q], 5, 2]]
    repeats = {d: count for d, count in Counter(new_weights).items() if count > 1}
    missing = sorted(set(weights) - set(new_weights))
    witnesses = [edge for edge, d in zip(edges, new_weights, strict=True) if d == 2]
    assert repeats == {2: 2} and missing == [8]
    assert witnesses == [["s:0", "b:0:1"], ["b:0:1", q]]
    cross_record = probes["cross_center"]
    pins = ("s:0", "s:1", "b:1:0")
    assert sorted(cross.values()) == list(range(15)) and all(cross[v] == labels[v] for v in pins)
    assert cross_record["vertices"] == [p, q] and cross_record["pins"]["valid"]
    assert cross_record["pins"]["actual"] == {v: cross[v] for v in pins}
    assert not cross_record["checker"]["valid"] and cross_record["checker"]["edge_differences"] == new_weights

    flip = probes["pair_flip"]
    high, low = "b:0:0", "b:0:1"
    pair = flip["pair"]
    assert pair == [5, 9] and sum(pair) == labels[high] + labels[low]
    assert sorted(abs(labels[high]-x) for x in pair) == sorted(abs(labels[low]-x) for x in pair) == [3, 7]
    allocation = flip["allocation"]
    assert allocation == {high: [4, 6, 8], low: [5, 7, 9]}
    assert boundary_report["midpoint"] == 7 and 7 in allocation[low]
    received = {h: len(xs) for h, xs in allocation.items()}
    allocated_labels = sorted(x for xs in allocation.values() for x in xs)
    allocated_weights = sorted(abs(labels[h] - x) for h, xs in allocation.items() for x in xs)
    assert allocated_labels == boundary_report["residual_labels"]
    assert allocated_weights == boundary_report["residual_differences"]
    assert received == {high: 3, low: 3} and received != boundary_report["actual_quotas"]
    gate = flip["allocation_gate"]
    assert gate["allocated_differences"] == allocated_weights and gate["allocated_labels"] == allocated_labels
    assert gate["actual_quotas"] == received and gate["expected_quotas"] == boundary_report["actual_quotas"]
    assert gate["labels_exact"] and gate["differences_exact"] and not gate["quotas_exact"] and not gate["valid"]
    assert "checker" not in flip

    complement = {v: 14 - x for v, x in labels.items()}
    assert sorted(complement.values()) == list(range(15))
    assert [abs(complement[u] - complement[v]) for u, v in edges] == weights
    assert tuple(complement[v] for v in pins) == (14, 0, 13)
    assert probes["complement"]["checker"]["valid"] and probes["complement"]["checker"]["edge_differences"] == weights
    assert not probes["complement"]["pins"]["valid"]
    assert probes["complement"]["pins"]["actual"] == {v: complement[v] for v in pins}
    return {"cross_changed_weights": changes, "cross_repeats": repeats, "cross_missing": missing,
            "cross_witnesses": witnesses, "pair_flip_resource_inventories_exact": True, "pair_weights": [3, 7],
            "pair_flip_quota_counts": received, "complement_weights_unchanged": True}
