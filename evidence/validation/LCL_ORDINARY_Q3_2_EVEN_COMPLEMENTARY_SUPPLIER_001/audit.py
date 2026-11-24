"""Independent reconstruction and audit of the sole frozen q=6 boundary."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json


def canonical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def topology(original):
    profile = [[6, 3], [2]]
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
    assert len(edges) == sum(edges.values()) == 15
    assert sorted(roles) == sorted(graph["vertices"]) and len(roles) == 16
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


def residual_components(core, remain_labels, remain_weights, allocation):
    lower, higher = "b:0:0", "b:0:1"
    assert core[lower] == 2 and core[higher] == 13
    host_sum = core[lower] + core[higher]
    groups = defaultdict(list)
    options = {}
    for x in sorted(remain_labels):
        assert core[lower] < x < core[higher]
        weights = {h: abs(x - core[h]) for h in (lower, higher)}
        eligible = {h: d for h, d in weights.items() if d in remain_weights}
        assert eligible
        options[x] = {"weights": weights, "eligible": eligible}
        groups[tuple(sorted(set(eligible.values())))].append(x)
    assert Counter(d for group in groups for d in group) == Counter(remain_weights)
    assert dict(groups) == {(3, 8): [5, 10], (4, 7): [6, 9], (5, 6): [7, 8], (9,): [4]}
    components = []
    for endpoints, xs in sorted(groups.items()):
        assert len(endpoints) == len(xs)
        owners = [h for h, palette in allocation.items() if set(xs) <= set(palette)]
        assert len(owners) == 1
        x = xs[0]
        if len(xs) == 1:
            assert options[x]["eligible"] == {higher: endpoints[0]} and owners == [higher]
            assert host_sum-x not in remain_labels
            kind = "forced_half_edge"
        else:
            y = xs[1]
            observed = options[x]["eligible"]
            other = options[y]["eligible"]
            assert x+y == host_sum and x != y
            assert observed == {lower: other[higher], higher: other[lower]}
            kind = "parallel_pair"
        components.append({"kind": kind, "labels": xs, "difference_vertices": list(endpoints),
                           "label_count": len(xs), "difference_count": len(endpoints), "host": owners[0]})
    c = sum(row["kind"] == "parallel_pair" for row in components)
    selected = sum(row["kind"] == "parallel_pair" and row["host"] == lower for row in components)
    assert (c, selected) == (3, 2)
    projection = [2*j for j in range(c+1)]
    assert len(allocation[lower]) == 2*selected in projection and len(allocation[higher]) == 3
    return {"options": options, "components": components, "lower_host": lower, "higher_host": higher,
            "A0": 0, "c": c, "eta": 0, "integral_projection": projection, "selected_j": selected}


def boundary(original, cert):
    edges, adjacent, distance = topology(original)
    graph = original["graph"]
    labels = cert["labels"]
    digest = original["graph_digest"]
    assert cert["graph_digest"] == digest and cert["ledger_id"] == canonical_sha(
        {"graph_digest": digest, "labels": sorted(labels.items())})
    assert set(labels) == set(adjacent) and all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(16))
    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    assert sorted(weights) == list(range(1, 16)) and weights == cert["checker"]["edge_differences"]
    a, b, right = "b:0:0", "b:0:1", "b:1:0"
    core_names = ("s:0", "s:1", a, b, right, "l:0:0:0", "l:0:0:5", "l:1:0:0", "l:1:0:1")
    core = dict(zip(core_names, (0, 15, 2, 13, 1, 3, 14, 11, 12), strict=True))
    assert core == {v: labels[v] for v in core_names}
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    occupied = [abs(core[u] - core[v]) for u, v in core_edges]
    assert set(core.values()) == {0, 1, 2, 3, 11, 12, 13, 14, 15}
    assert sorted(occupied) == [1, 2, 10, 11, 12, 13, 14, 15]
    vacant = set(labels) - set(core)
    assert all(len(adjacent[v]) == 1 and adjacent[v] <= {a, b} for v in vacant)
    slots = {h: sorted(vacant & adjacent[h]) for h in (a, b)}
    assert slots[a] == [f"l:0:0:{i}" for i in range(1, 5)]
    assert slots[b] == [f"l:0:1:{i}" for i in range(3)]
    remain_labels = set(range(16)) - set(core.values())
    remain_weights = set(range(1, 16)) - set(occupied)
    assert remain_labels == set(range(4, 11)) and remain_weights == set(range(3, 10))
    allocation = {h: [labels[v] for v in slots[h]] for h in slots}
    assert allocation == {a: [6, 7, 8, 9], b: [4, 5, 10]}
    components = residual_components(core, remain_labels, remain_weights, allocation)
    quotas = {h: len(xs) for h, xs in allocation.items()}
    assert quotas == {a: 4, b: 3}
    assert Counter(abs(core[h]-x) for h, xs in allocation.items() for x in xs) == Counter(remain_weights)

    degrees = {v: len(adjacent[v]) for v in labels}
    parity_quantity = sum((degrees[v]-1)*labels[v] for v in labels)
    assert sum(weights) == sum(labels.values()) == 120
    assert parity_quantity == 6*labels[a]+3*labels[b]+17 == 68
    assert parity_quantity % 2 == 0 and labels[b] % 2 == 1
    pins = {v: labels[v] for v in ("s:0", "s:1", right)}
    assert pins == {"s:0": 0, "s:1": len(edges), right: 1}
    assert graph["spine"] == ["s:0", "s:1"] and right not in graph["spine"]
    assert adjacent["s:1"] == {"s:0", right} and distance[right] == 1
    parity = {v: (distance[v] + graph["roles"][v]["section"]) % 2 for v in labels}
    signed = []
    for u, v in edges:
        assert parity[u] != parity[v]
        tail, head = (u, v) if parity[u] == 0 else (v, u)
        signed.append({"edge": [tail, head], "signed": labels[head]-labels[tail]})
    negatives = [row for row in signed if row["signed"] < 0]
    assert negatives == [{"edge": [f"l:0:0:{i}", a], "signed": value}
                         for i, value in enumerate((-1, -4, -5, -6, -7, -12))]
    assert sum(row["signed"] for row in signed) == 50
    return {"core": {"labels": core, "edges": core_edges, "occupied_differences": sorted(occupied)},
            "residual_labels": sorted(remain_labels), "residual_differences": sorted(remain_weights),
            "r226": components, "allocation": allocation, "actual_quotas": quotas, "slots": slots,
            "degree_vector": degrees, "parity_quantity": parity_quantity, "observed_signed_incidences": signed,
            "absolute_differences": weights, "unused_labels": [], "unused_differences": [],
            "d112_compatibility": {"spine": graph["spine"], "exit_neighbors": sorted(adjacent["s:1"]),
                                   "off_spine_host_distance": distance[right], "pins": pins}}


def controls(original, cert, probes, boundary_report):
    edges = original["graph"]["edges"]
    labels = cert["labels"]
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    wrong = probes["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["edge_differences"] == weights

    u, v = "l:0:0:1", "l:0:1:0"
    cross = labels | {u: labels[v], v: labels[u]}
    new_weights = [abs(cross[x]-cross[y]) for x, y in edges]
    changes = [[e, d, f] for e, d, f in zip(edges, weights, new_weights, strict=True) if d != f]
    assert changes == [[["b:0:0", u], 4, 2], [["b:0:1", v], 9, 7]]
    repeats = {d: count for d, count in Counter(new_weights).items() if count > 1}
    missing = sorted(set(weights)-set(new_weights))
    witnesses = {d: [edge for edge, observed in zip(edges, new_weights, strict=True) if observed == d]
                 for d in repeats}
    assert repeats == {2: 2, 7: 2} and missing == [4, 9]
    assert witnesses == {2: [["s:0", "b:0:0"], ["b:0:0", u]],
                         7: [["b:0:0", "l:0:0:4"], ["b:0:1", v]]}
    cross_record = probes["cross_center"]
    pins = ("s:0", "s:1", "b:1:0")
    assert sorted(cross.values()) == list(range(16)) and all(cross[p] == labels[p] for p in pins)
    assert cross_record["vertices"] == [u, v] and cross_record["pins"]["valid"]
    assert cross_record["pins"]["actual"] == {p: cross[p] for p in pins}
    assert not cross_record["checker"]["valid"] and cross_record["checker"]["edge_differences"] == new_weights

    pair_flip = probes["pair_flip"]
    a, b = "b:0:0", "b:0:1"
    pair = pair_flip["pair"]
    assert pair == [5, 10] and sum(pair) == labels[a]+labels[b]
    assert sorted(abs(labels[a]-x) for x in pair) == sorted(abs(labels[b]-x) for x in pair) == [3, 8]
    allocation = pair_flip["allocation"]
    assert allocation == {a: [5, 6, 7, 8, 9, 10], b: [4]}
    received = {h: len(xs) for h, xs in allocation.items()}
    allocated_labels = sorted(x for xs in allocation.values() for x in xs)
    allocated_weights = sorted(abs(labels[h]-x) for h, xs in allocation.items() for x in xs)
    assert allocated_labels == boundary_report["residual_labels"]
    assert allocated_weights == boundary_report["residual_differences"]
    assert received == {a: 6, b: 1} and received != boundary_report["actual_quotas"]
    gate = pair_flip["allocation_gate"]
    assert gate["allocated_differences"] == allocated_weights and gate["allocated_labels"] == allocated_labels
    assert gate["actual_quotas"] == received and gate["expected_quotas"] == boundary_report["actual_quotas"]
    assert gate["labels_exact"] and gate["differences_exact"] and not gate["quotas_exact"] and not gate["valid"]
    assert "checker" not in pair_flip

    complement = {x: 15-y for x, y in labels.items()}
    assert sorted(complement.values()) == list(range(16))
    assert [abs(complement[x]-complement[y]) for x, y in edges] == weights
    assert tuple(complement[x] for x in pins) == (15, 0, 14)
    assert probes["complement"]["checker"]["valid"] and probes["complement"]["checker"]["edge_differences"] == weights
    assert not probes["complement"]["pins"]["valid"]
    assert probes["complement"]["pins"]["actual"] == {x: complement[x] for x in pins}
    return {"cross_changed_weights": changes, "cross_repeats": repeats, "cross_missing": missing,
            "cross_witnesses": witnesses, "pair_flip_weights": [3, 8], "pair_flip_quotas": received,
            "complement_weights_unchanged": True}
