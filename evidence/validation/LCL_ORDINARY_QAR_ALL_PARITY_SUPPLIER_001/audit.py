"""Reconstruct both archived boundaries and verify controls without producer imports."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json


def canonical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def distances(adjacent, starts):
    distance = dict.fromkeys(starts, 0)
    queue = deque(starts)
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacent[vertex] - distance.keys():
            distance[neighbor] = distance[vertex] + 1
            queue.append(neighbor)
    return distance


def topology(original):
    graph = original["graph"]
    profile = graph["profile"]
    assert profile in ([[5, 3], [2]], [[6, 3], [2]])
    spine = ["s:0", "s:1"]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    expected = [spine.copy()]
    for section, branch_quotas in enumerate(profile):
        for index, quota in enumerate(branch_quotas):
            host = f"b:{section}:{index}"
            roles[host] = {"kind": "branch", "section": section, "branch": index}
            expected.append([spine[section], host])
            for k in range(quota):
                leaf = f"l:{section}:{index}:{k}"
                roles[leaf] = {"kind": "leaf", "section": section, "branch": index, "leaf": k}
                expected.append([host, leaf])
    edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    assert edges == Counter(tuple(sorted(edge)) for edge in expected)
    assert len(edges) == sum(edges.values()) == len(roles) - 1
    assert Counter(graph["vertices"]) == Counter(roles.keys())
    assert graph["roles"] == roles and graph["schema_version"] == 1
    assert graph["spine"] == spine and graph["edges"] == expected
    payload = {"vertices": sorted(roles), "edges": sorted(edges.elements()),
               "roles": roles, "profile": profile, "spine": spine}
    assert canonical_sha(payload) == original["graph_digest"]
    adjacent = {vertex: set() for vertex in roles}
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    distance = distances(adjacent, spine)
    depths = {"spine": 0, "branch": 1, "leaf": 2}
    assert distance == {v: depths[role["kind"]] for v, role in roles.items()}
    return expected, adjacent, distance


def residual_components(core, remaining_labels, remaining_weights, allocation, lower, higher):
    options = {}
    groups = defaultdict(list)
    host_sum = core[lower] + core[higher]
    for x in sorted(remaining_labels):
        assert core[lower] < x < core[higher]
        weights = {h: abs(core[h]-x) for h in (lower, higher)}
        eligible = {h: d for h, d in weights.items() if d in remaining_weights}
        assert eligible
        options[x] = {"weights": weights, "eligible": eligible}
        groups[tuple(sorted(set(eligible.values())))].append(x)
    assert Counter(d for endpoints in groups for d in endpoints) == Counter(remaining_weights)
    components, pair_representatives, chosen_pairs, midpoint = [], [], [], []
    forced = []
    for endpoints, xs in sorted(groups.items()):
        assert len(endpoints) == len(xs)
        owners = [h for h in (lower, higher) if set(xs) <= set(allocation[h])]
        assert len(owners) == 1
        owner = owners[0]
        x = xs[0]
        row = options[x]["eligible"]
        if len(xs) == 2:
            y = xs[1]
            other = options[y]["eligible"]
            assert len(row) == len(other) == 2 and x+y == host_sum
            assert row == {lower: other[higher], higher: other[lower]}
            kind = "parallel_pair"
            pair_representatives.append(x)
            if owner == lower:
                chosen_pairs.append(x)
        elif len(row) == 1:
            assert row == {higher: endpoints[0]} and owner == higher
            assert host_sum-x not in remaining_labels
            forced.append(x)
            kind = "forced_half_edge"
        else:
            assert len(row) == 2 and row[lower] == row[higher] and 2*x == host_sum
            midpoint.append((x, owner))
            kind = "midpoint_loop"
        components.append({"kind": kind, "labels": xs, "difference_vertices": list(endpoints),
                           "label_count": len(xs), "difference_count": len(endpoints), "host": owner})
    assert forced == [4] and len(midpoint) == int(host_sum % 2 == 0)
    pairs = sorted(pair_representatives)
    assert pairs == [x for x in sorted(remaining_labels) if x != 4 and 2*x < host_sum]
    j = len(chosen_pairs)
    assert sorted(chosen_pairs) == pairs[len(pairs)-j:]
    c, eta = len(pairs), len(midpoint)
    epsilon = sum(owner == lower for _, owner in midpoint)
    projection = [2*k+bit for k in range(c+1) for bit in range(eta+1)]
    assert len(allocation[lower]) == 2*j+epsilon in projection
    return {"components": components, "options": options, "A0": 0, "c": c, "eta": eta,
            "selected_j": j, "selected_epsilon": epsilon, "integral_projection": projection}


def boundary(original, cert, checker):
    edges, adjacent, distance = topology(original)
    graph, labels = original["graph"], cert["labels"]
    digest = original["graph_digest"]
    assert cert["graph_digest"] == digest and cert["ledger_id"] == canonical_sha(
        {"graph_digest": digest, "labels": sorted(labels.items())})
    q, a = graph["profile"][0]
    r = graph["profile"][1][0]
    n, m = q+a+6, len(edges)
    assert r == 2 and m == n and len(labels) == m+1
    assert set(labels) == set(adjacent) and all(type(x) is int for x in labels.values())
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    assert sorted(labels.values()) == list(range(m+1)) and sorted(weights) == list(range(1, m+1))
    assert weights == checker["edge_differences"] and checker["valid"]

    hosts = ("b:0:0", "b:0:1")
    lower, higher = sorted(hosts, key=labels.__getitem__)
    assert (lower == hosts[0]) == (q % 2 == 0)
    spine, right = graph["spine"], "b:1:0"
    pins = {v: labels[v] for v in (*spine, right)}
    assert pins == {"s:0": 0, "s:1": m, right: 1}
    assert adjacent["s:1"] == {"s:0", right} and right not in spine and distance[right] == 1

    terminals = {h: sorted(adjacent[h]-set(spine), key=lambda v: graph["roles"][v]["leaf"])
                 for h in (*hosts, right)}
    assert tuple(len(terminals[h]) for h in (*hosts, right)) == (q, a, r)
    assert all(adjacent[v] == {h} for h, leaves in terminals.items() for v in leaves)
    ell, h = len(terminals[lower]), len(terminals[higher])
    core = pins | {lower: 2, higher: n-2, terminals[lower][0]: 3,
                   terminals[lower][-1]: n-1, terminals[right][0]: n-4, terminals[right][1]: n-3}
    assert core == {v: labels[v] for v in core}
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    occupied = [abs(core[u]-core[v]) for u, v in core_edges]
    assert len(core) == 9 and len(core_edges) == 8
    assert sorted(core.values()) == [0, 1, 2, 3, *range(n-4, n+1)]
    assert sorted(occupied) == [1, 2, *range(n-5, n+1)]
    remaining_labels = set(range(n+1))-set(core.values())
    remaining_weights = set(range(1, n+1))-set(occupied)
    assert remaining_labels == set(range(4, n-4)) and remaining_weights == set(range(3, n-5))
    slots = {lower: terminals[lower][1:-1], higher: terminals[higher]}
    assert set(labels)-set(core) == {v for leaves in slots.values() for v in leaves}
    allocation = {host: [labels[v] for v in leaves] for host, leaves in slots.items()}
    assert all(xs == sorted(xs) for xs in allocation.values())
    assert Counter(x for xs in allocation.values() for x in xs) == Counter(remaining_labels)
    assert Counter(abs(core[k]-x) for k, xs in allocation.items() for x in xs) == Counter(remaining_weights)
    quotas = {host: len(xs) for host, xs in allocation.items()}
    assert quotas == {lower: ell-2, higher: h}
    r226 = residual_components(core, remaining_labels, remaining_weights, allocation, lower, higher)
    c, j, eta, epsilon = (r226[k] for k in ("c", "selected_j", "eta", "selected_epsilon"))
    assert epsilon == int(q % 2 == a % 2 == 1) and 2*(c-j) == h-1-eta+epsilon
    selection = {"n": n, "m": m, "lower": lower, "higher": higher, "ell": ell, "h": h,
                 "u": c+4, "c": c, "j": j, "eta": eta, "epsilon": epsilon}

    parity = distances(adjacent, ["s:0"])
    signed = []
    for u, v in edges:
        assert (parity[u]-parity[v]) % 2 == 1
        tail, head = (v, u) if parity[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "signed": labels[head]-labels[tail]})
    negatives = [row["edge"] for row in signed if row["signed"] < 0]
    assert negatives == [[v, lower] for v in terminals[lower]]
    changed = {frozenset(spine), frozenset(("s:1", right))}
    unchanged = [d for e, d in zip(edges, weights, strict=True) if frozenset(e) not in changed]
    assert sorted(unchanged) == list(range(1, n-1)) and labels["s:1"]-labels[right] == m-1
    assert not terminals[right][2:] and not list(range(n, m)) and not list(range(n-1, m-1))
    return {"core": {"labels": core, "edges": core_edges, "occupied_differences": sorted(occupied)},
            "actual_quotas": quotas, "slots": slots, "allocation": allocation, "selection": selection,
            "residual_labels": sorted(remaining_labels), "residual_differences": sorted(remaining_weights),
            "r226": r226, "checked_formula_vertices": sorted(labels), "observed_signed_incidences": signed,
            "absolute_differences": weights, "unused_labels": [], "unused_differences": [],
            "growth_partition": {"unchanged_weights": sorted(unchanged), "inserted_labels": [],
                                 "inserted_differences": [], "right_attachment": m-1, "spine": m},
            "d112_compatibility": {"spine": spine, "exit_neighbors": sorted(adjacent["s:1"]),
                                   "off_spine_host_distance": distance[right], "pins": pins}}


def controls(odd_original, odd_cert, even_original, even_cert, even_boundary, probes):
    odd_edges, odd_labels = odd_original["graph"]["edges"], odd_cert["labels"]
    odd_weights = [abs(odd_labels[u]-odd_labels[v]) for u, v in odd_edges]
    wrong = probes["wrong_digest_D111"]
    assert wrong["expected_digest"] != odd_original["graph_digest"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["edge_differences"] == odd_weights

    u, v = "l:0:0:0", "l:0:0:1"
    assert (odd_labels[u], odd_labels[v]) == (4, 5)
    within = odd_labels | {u: odd_labels[v], v: odd_labels[u]}
    within_weights = [abs(within[x]-within[y]) for x, y in odd_edges]
    within_changes = [[e, d, f] for e, d, f in zip(odd_edges, odd_weights, within_weights, strict=True) if d != f]
    assert within_changes == [[["b:0:0", u], 8, 7], [["b:0:0", v], 7, 8]]
    assert sorted(within.values()) == list(range(15)) and sorted(within_weights) == list(range(1, 15))
    within_report = probes["within_D111"]
    assert within_report["checker"]["valid"] and within_report["checker"]["edge_differences"] == within_weights
    pins = ("s:0", "s:1", "b:1:0")
    assert tuple(within[k] for k in pins) == (0, 14, 1) and within_report["growth_premises"]["valid"]
    assert not within_report["pointwise_agreement"]
    assert within_report["vertices"] == within_report["disagreements"] == sorted(
        k for k in within if within[k] != odd_labels[k]) == [u, v]

    even_edges, even_labels = even_original["graph"]["edges"], even_cert["labels"]
    even_weights = [abs(even_labels[x]-even_labels[y]) for x, y in even_edges]
    u, v = "l:0:0:1", "l:0:1:1"
    assert (even_labels[u], even_labels[v]) == (6, 5)
    cross = even_labels | {u: even_labels[v], v: even_labels[u]}
    cross_weights = [abs(cross[x]-cross[y]) for x, y in even_edges]
    changes = [[e, d, f] for e, d, f in zip(even_edges, even_weights, cross_weights, strict=True) if d != f]
    assert changes == [[["b:0:0", u], 4, 3], [["b:0:1", v], 8, 7]]
    repeats = {d: count for d, count in Counter(cross_weights).items() if count > 1}
    missing = sorted(set(even_weights)-set(cross_weights))
    witnesses = {d: [edge for edge, obs in zip(even_edges, cross_weights, strict=True) if obs == d]
                 for d in repeats}
    assert repeats == {3: 2, 7: 2} and missing == [4, 8]
    assert witnesses == {3: [["b:0:0", u], ["b:0:1", "l:0:1:2"]],
                         7: [["b:0:0", "l:0:0:4"], ["b:0:1", v]]}
    cross_report = probes["cross_D114"]
    assert sorted(cross.values()) == list(range(16)) and tuple(cross[k] for k in pins) == (0, 15, 1)
    assert cross_report["vertices"] == [u, v] and cross_report["pins"]["valid"]
    assert cross_report["pins"]["actual"] == {k: cross[k] for k in pins}
    assert not cross_report["checker"]["valid"] and cross_report["checker"]["edge_differences"] == cross_weights
    assert cross_report["checker"]["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    slots = even_boundary["slots"]
    allocation = {host: [cross[leaf] for leaf in leaves] for host, leaves in slots.items()}
    quotas = {host: len(xs) for host, xs in allocation.items()}
    assert quotas == even_boundary["actual_quotas"] == {"b:0:0": 4, "b:0:1": 3}
    gate = cross_report["allocation_gate"]
    assert gate["actual_quotas"] == gate["expected_quotas"] == quotas
    assert gate["labels_exact"] and gate["quotas_exact"] and not gate["differences_exact"] and not gate["valid"]
    assert gate["allocated_labels"] == sorted(x for xs in allocation.values() for x in xs)
    assert gate["allocated_differences"] == sorted(abs(cross[h]-x) for h, xs in allocation.items() for x in xs)

    complement = {vertex: len(even_edges)-label for vertex, label in even_labels.items()}
    complement_report = probes["complement_D114"]
    assert sorted(complement.values()) == list(range(16))
    assert [abs(complement[x]-complement[y]) for x, y in even_edges] == even_weights
    assert tuple(complement[k] for k in pins) == (15, 0, 14)
    assert complement_report["checker"]["valid"] and complement_report["checker"]["edge_differences"] == even_weights
    assert complement_report["pins"]["actual"] == {k: complement[k] for k in pins}
    assert not complement_report["pins"]["valid"] and not complement_report["growth_premises"]["valid"]
    assert {k for k, passed in complement_report["growth_premises"]["tests"].items() if not passed} == {"required_labels"}
    return {"within_changed_weights": within_changes, "cross_changed_weights": changes, "cross_repeats": repeats,
            "cross_missing": missing, "cross_witnesses": witnesses, "cross_residual_quotas": quotas,
            "complement_weights_unchanged": True}
