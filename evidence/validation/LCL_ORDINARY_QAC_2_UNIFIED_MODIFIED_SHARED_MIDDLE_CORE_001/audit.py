"""Independent boundary incidence, R226, inventory and control checks."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json


def hash_canonical(payload):
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(data).hexdigest()


def traverse(neighbors, starts):
    distances = dict.fromkeys(starts, 0)
    queue = deque(starts)
    while queue:
        vertex = queue.popleft()
        for nxt in neighbors[vertex] - distances.keys():
            distances[nxt] = distances[vertex] + 1
            queue.append(nxt)
    return distances


def reconstruct(original, profile):
    graph = original["graph"]
    assert profile in ([[6, 5, 8], [2]], [[6, 3, 4], [2]], [[4, 5, 4], [2]])
    m = 5+sum(profile[0])+sum(profile[1])
    spine = ["s:0", "s:1"]
    roles = {name: {"kind": "spine", "section": section} for section, name in enumerate(spine)}
    edges = [spine.copy()]
    for section, quotas in enumerate(profile):
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            edges.append([spine[section], center])
            for index in range(quota):
                leaf = f"l:{section}:{branch}:{index}"
                roles[leaf] = {"kind": "leaf", "section": section, "branch": branch, "leaf": index}
                edges.append([center, leaf])
    incidence = Counter(tuple(sorted(edge)) for edge in edges)
    assert incidence == Counter(tuple(sorted(edge)) for edge in graph["edges"])
    assert graph["edges"] == edges and len(incidence) == len(edges) == m
    assert Counter(graph["vertices"]) == Counter(roles.keys()) and len(roles) == m+1
    assert graph["schema_version"] == 1 and graph["roles"] == roles
    assert graph["spine"] == spine and graph["profile"] == profile
    digest = hash_canonical({"vertices": sorted(roles), "edges": sorted(incidence.elements()),
                             "roles": roles, "spine": spine, "profile": profile})
    assert digest == original["graph_digest"]
    neighbors = {v: set() for v in roles}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    path_distance = traverse(neighbors, spine)
    depths = {"spine": 0, "branch": 1, "leaf": 2}
    assert path_distance == {v: depths[role["kind"]] for v, role in roles.items()}
    return edges, roles, neighbors, path_distance, digest


def eligible_multigraph(core, low, high, batch):
    inventory = set(batch["differences"])
    labels = batch["labels"]
    assert len(inventory) == len(batch["differences"]) == len(labels) == len(set(labels))
    assert all(type(d) is int and d > 0 for d in inventory) and core[low] < core[high]
    assert all(type(x) is int and x not in (core[low], core[high]) for x in labels)
    weights, rows = {}, {}
    neighbors = {d: set() for d in inventory}
    incidence = {d: set() for d in inventory}
    links = defaultdict(list)
    for x in labels:
        options = {host: abs(x-core[host]) for host in (low, high)}
        eligible = {host: d for host, d in options.items() if d in inventory}
        assert eligible
        weights[x], rows[x] = options, eligible
        endpoints = sorted(set(eligible.values()))
        for d in endpoints:
            incidence[d].add(x)
        if len(endpoints) == 2:
            a, b = endpoints
            neighbors[a].add(b)
            neighbors[b].add(a)
            links[(a, b)].append(x)
    return weights, rows, neighbors, incidence, links


def extract_tree(vertices, root_label, rows, neighbors, links):
    root_host, root = next(iter(rows[root_label].items()))
    forced = {root_label: root_host}
    visited, queue = {root}, deque([root])
    while queue:
        parent = queue.popleft()
        for child in neighbors[parent] - visited:
            labels = links[tuple(sorted((parent, child)))]
            assert len(labels) == 1
            x = labels[0]
            hosts = [host for host, d in rows[x].items() if d == child]
            assert len(hosts) == 1 and x not in forced
            forced[x] = hosts[0]
            visited.add(child)
            queue.append(child)
    assert visited == vertices and len(forced) == len(vertices)
    assert Counter(rows[x][host] for x, host in forced.items()) == Counter(vertices)
    return forced


def r226(core, low, high, batch, local):
    weights, rows, neighbors, incidence, links = eligible_multigraph(core, low, high, batch)
    assert rows == local["eligible_options"]
    assignment = batch["allocation"]
    assert Counter(x for xs in assignment.values() for x in xs) == Counter(rows.keys())
    owners = {x: host for host, xs in assignment.items() for x in xs}
    assert all(owners[x] in row for x, row in rows.items())
    assert Counter(rows[x][host] for x, host in owners.items()) == Counter(neighbors.keys())
    remaining = set(neighbors)
    components = []
    forced_low, pairs, loops = 0, 0, 0
    for start in sorted(neighbors):
        if start not in remaining:
            continue
        vertices = set(traverse(neighbors, [start]))
        remaining.difference_update(vertices)
        resources = sorted(set().union(*(incidence[d] for d in vertices)))
        half_edges = [x for x in resources if len(rows[x]) == 1]
        loop_edges = [x for x in resources if len(rows[x]) == 2 and len(set(rows[x].values())) == 1]
        ordinary_edges = [x for x in resources if x not in half_edges and x not in loop_edges]
        assert len(ordinary_edges)+len(loop_edges)+len(half_edges) == len(vertices)
        forced = {}
        if half_edges:
            assert len(half_edges) == 1 and not loop_edges
            assert len(ordinary_edges) == len(vertices)-1
            forced = extract_tree(vertices, half_edges[0], rows, neighbors, links)
            assert set(forced) == set(resources) and all(owners[x] == host for x, host in forced.items())
            forced_low += sum(host == low for host in forced.values())
            kind = "tree_with_half_edge" if ordinary_edges else "forced_half_edge"
        elif loop_edges:
            assert len(vertices) == len(resources) == len(loop_edges) == 1
            x = loop_edges[0]
            assert 2*x == core[low]+core[high]
            loops += 1
            kind = "midpoint_loop"
        else:
            assert len(vertices) == len(ordinary_edges) == 2
            x, y = ordinary_edges
            assert x+y == core[low]+core[high]
            assert rows[x][low] == rows[y][high] and rows[x][high] == rows[y][low]
            assert owners[x] == owners[y]
            pairs += 1
            kind = "parallel_pair"
        components.append({"kind": kind, "labels": resources, "differences": sorted(vertices),
                           "ordinary_edges": ordinary_edges, "loops": loop_edges, "half_edges": half_edges,
                           "host_tagged_options": {x: rows[x] for x in resources},
                           "assigned_hosts": {x: owners[x] for x in resources}, "forced_extraction": forced,
                           "balance": {"n": len(vertices), "e": len(ordinary_edges)+len(loop_edges),
                                       "t": len(half_edges)}})
    assert not remaining and 0 <= loops <= 1
    assert Counter(x for component in components for x in component["labels"]) == Counter(rows.keys())
    assert Counter(d for component in components for d in component["differences"]) == Counter(neighbors.keys())
    projection = [forced_low+2*j+bit for j in range(pairs+1) for bit in range(loops+1)]
    actual = {host: len(assignment[host]) for host in (low, high)}
    quotas = {host: len(batch["slots"][host]) for host in (low, high)}
    assert actual == quotas == local["actual_quotas"] == local["expected_quotas"] and quotas[low] in projection
    assert local["valid"]
    return {"hosts": [low, high], "weight_options": weights, "eligible_options": rows,
            "components": components, "A0": forced_low, "c": pairs, "eta": loops,
            "integral_projection": projection, "chosen_quotas": quotas}


def check_instance(original, profile, core, batches, labels, ledger, checker, local, global_report, pins, growth):
    edges, roles, neighbors, path_distance, digest = reconstruct(original, profile)
    x, middle, z, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    q, a_quota, c = profile[0]
    m = len(edges)
    assert m == q + a_quota + c + 7
    expected_core = {
        "s:0": 0, "s:1": m, x: 2, middle: m - 6, z: m - 4, right: 1,
        "l:0:0:0": m - 3, "l:0:1:0": m - 5, "l:1:0:0": m - 1, "l:1:0:1": m - 2,
    }
    assert core == expected_core == {v: labels[v] for v in expected_core}
    assert set(labels) == set(roles) and all(type(label) is int for label in labels.values())
    assert Counter(labels.values()) == Counter(range(m + 1))
    assert ledger == hash_canonical({"labels": sorted(labels.items()), "graph_digest": digest})
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    core_neighbors = {v: neighbors[v] & core.keys() for v in core}
    assert len(core_edges) == len(core) - 1 == 9 and set(traverse(core_neighbors, ["s:0"])) == set(core)
    fixed = [abs(core[u] - core[v]) for u, v in core_edges]
    assert fixed == [m, 2, m - 5, m - 6, 1, m - 4, m - 1, m - 2, m - 3]
    assert sorted(core.values()) == [0, 1, 2, *range(m - 6, m + 1)]
    assert sorted(fixed) == [1, 2, *range(m - 6, m + 1)]
    residual_labels = set(range(m + 1)) - set(core.values())
    residual_weights = set(range(1, m + 1)) - set(fixed)
    assert residual_labels == residual_weights == set(range(3, m - 6))

    a, b = batches["A"], batches["B"]
    named_terminals = {
        host: sorted((v for v in neighbors[host] if roles[v]["kind"] == "leaf"), key=lambda v: roles[v]["leaf"])
        for host in (x, middle, z, right)
    }
    assert a["slots"] == {x: named_terminals[x][1:], middle: named_terminals[middle][1:-1]}
    assert b["slots"] == {middle: named_terminals[middle][-1:], z: named_terminals[z]}
    supplied_slots = [(host, leaf) for batch in (a, b) for host, leaves in batch["slots"].items() for leaf in leaves]
    assert len(supplied_slots) == len({leaf for _, leaf in supplied_slots}) == m - 9
    assert {leaf for _, leaf in supplied_slots} == set(labels) - set(core)
    assert all(neighbors[leaf] == {host} and path_distance[host] == 1 for host, leaf in supplied_slots)
    assert set(a["slots"]) & set(b["slots"]) == {middle}
    targets = {host: [labels[v] for v in leaves] for host, leaves in named_terminals.items()}
    quotas = {host: len(values) for host, values in targets.items()}
    assert quotas == {x: q, middle: a_quota, z: c, right: 2}
    for batch in batches.values():
        assert batch["allocation"] == {host: [labels[leaf] for leaf in leaves] for host, leaves in batch["slots"].items()}
        assert all(values == sorted(values) for values in batch["allocation"].values())
    assert targets[right] == [m - 1, m - 2]

    t = (m - 2) // 2
    start, end = 4 + c // 2, m - 2 - (4 + c // 2)
    interval = set(range(start, end + 1))
    outside = residual_labels - interval
    z_label = core[z]
    assert {t - 2, t, t + 2} <= interval and len(outside) == c
    assert set(a["labels"]) == interval - {t}
    assert set(a["differences"]) == {z_label - label for label in interval} - {t - 4}
    assert set(b["labels"]) == outside | {t}
    assert set(b["differences"]) == {z_label - label for label in outside} | {t - 4}
    assert Counter(a["labels"] + b["labels"]) == Counter(residual_labels)
    assert Counter(a["differences"] + b["differences"]) == Counter(residual_weights)
    assert global_report["valid"] and all(global_report["tests"].values())
    a_report = r226(core, x, middle, a, local["A"])
    b_report = r226(core, middle, z, b, local["B"])
    pair_count = (q + a_quota - 7) // 2
    assert (a_report["A0"], a_report["c"], a_report["eta"]) == (2, pair_count, 1)
    assert a_report["integral_projection"] == list(range(2, 4 + 2 * pair_count))
    assert (b_report["A0"], b_report["c"], b_report["eta"], b_report["integral_projection"]) == (1, 0, 0, [1])
    assert a_report["chosen_quotas"] == {x: q - 1, middle: a_quota - 2}
    assert b_report["chosen_quotas"] == {middle: 1, z: c}
    a_components = {tuple(item["labels"]): item for item in a_report["components"]}
    assert a_components[(t - 2,)]["forced_extraction"] == {t - 2: middle}
    assert a_components[(end - 1,)]["forced_extraction"] == {end - 1: x}
    assert a_components[(end,)]["forced_extraction"] == {end: x}
    assert a_components[(t - 1,)]["kind"] == "midpoint_loop"
    assert a_components[(t - 1,)]["assigned_hosts"] == {t - 1: x}
    pairs = sorted(key for key, item in a_components.items() if item["kind"] == "parallel_pair")
    assert [key[0] for key in pairs] == list(range(start, t - 2))
    for index, pair in enumerate(pairs):
        host = x if index < (q - 4) // 2 else middle
        assert a_components[pair]["assigned_hosts"] == dict.fromkeys(pair, host)
    chains = []
    for label in sorted(outside):
        if label - 2 not in outside:
            chain = []
            while label in outside:
                chain.append(label)
                label += 2
            chains.append(tuple(chain))
    assert len(chains) == (3 if c == 4 else 4)
    b_components = {tuple(item["labels"]): item for item in b_report["components"]}
    assert set(b_components) == {*chains, (t,)}
    assert b_components[(t,)]["forced_extraction"] == {t: middle}
    for chain in chains:
        component = b_components[chain]
        assert component["half_edges"] == [chain[-1]] and component["ordinary_edges"] == list(chain[:-1])
        assert component["forced_extraction"] == dict.fromkeys(chain, z)

    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    assert Counter(weights) == Counter(range(1, m + 1)) and checker["edge_differences"] == weights and checker["valid"]
    distance = traverse(neighbors, ["s:0"])
    signed = []
    for u, v in edges:
        assert (distance[u] - distance[v]) % 2 == 1
        tail, head = (v, u) if distance[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "difference": labels[head] - labels[tail]})
    negatives = [row for row in signed if row["difference"] < 0]
    assert negatives == [{"edge": [leaf, x], "difference": 2 - labels[leaf]} for leaf in named_terminals[x]] + [
        {"edge": ["l:0:1:0", middle], "difference": -1}]
    head_sum = sum(len(neighbors[v]) * labels[v] for v in labels if distance[v] % 2)
    tail_sum = sum(len(neighbors[v]) * labels[v] for v in labels if not distance[v] % 2)
    signed_sum = sum(row["difference"] for row in signed)
    assert signed_sum == head_sum - tail_sum
    degree_parity = sum((len(neighbors[v]) - 1) * labels[v] for v in labels)
    assert degree_parity == q * labels[x] + a_quota * labels[middle] + c * labels[z] + m + 2 and degree_parity % 2 == 0
    assert original["graph"]["spine"] == ["s:0", "s:1"] and neighbors["s:1"] == {"s:0", right}
    assert pins["valid"] and pins["actual"] == {"s:0": 0, "s:1": m, right: 1}
    assert path_distance[right] == 1 and growth["valid"] and all(growth["tests"].values())
    return {
        "graph_digest": digest, "ledger_id": ledger, "core_edges": core_edges, "core_differences": fixed,
        "residual_labels": sorted(residual_labels), "residual_differences": sorted(residual_weights),
        "r226": {"A": a_report, "B": b_report}, "terminal_lists": targets,
        "interval": {"b": start, "e": end, "t": t, "h": end - t, "complement": sorted(outside)},
        "named_slots": supplied_slots, "reconstructed_quotas": quotas, "absolute_differences": weights,
        "signed_incidences": signed, "signed_sum": signed_sum, "weighted_degree_sums": {"head": head_sum, "tail": tail_sum},
        "degree_parity_quantity": degree_parity, "unused_labels": [], "unused_differences": [],
        "distance_to_spine": path_distance, "physical_pins": pins, "growth_premises": growth,
    }


def check_new_boundary(audit):
    x, middle, z, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    assert audit["interval"] == {"b": 8, "e": 16, "t": 12, "h": 4, "complement": [3, 4, 5, 6, 7, 17, 18, 19]}
    assert audit["terminal_lists"] == {
        x: [23, 8, 11, 14, 15, 16], middle: [21, 9, 10, 13, 12],
        z: [3, 4, 5, 6, 7, 17, 18, 19], right: [25, 24],
    }
    assert audit["absolute_differences"] == [
        26, 2, 21, 6, 9, 12, 13, 14, 20, 1, 11, 10, 7, 8, 22, 19, 18, 17, 16, 15, 5, 4, 3, 25, 24, 23,
    ]
    assert audit["signed_sum"] == 199 and audit["degree_parity_quantity"] == 316
    a, b = audit["r226"]["A"], audit["r226"]["B"]
    assert sorted(a["eligible_options"]) == [8, 9, 10, 11, 13, 14, 15, 16]
    assert sorted(d for part in a["components"] for d in part["differences"]) == [6, 7, 9, 10, 11, 12, 13, 14]
    assert sorted(b["eligible_options"]) == [3, 4, 5, 6, 7, 12, 17, 18, 19]
    assert sorted(d for part in b["components"] for d in part["differences"]) == [3, 4, 5, 8, 15, 16, 17, 18, 19]
    assert {tuple(part["labels"]) for part in b["components"]} == {(3, 5, 7), (4, 6), (17, 19), (18,), (12,)}


def controls(original, labels, core, batches, reports, positive_a):
    x, middle, z = "b:0:0", "b:0:1", "b:0:2"
    graph = original["graph"]
    edges = graph["edges"]
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    wrong = reports["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["edge_differences"] == weights

    first, second = "l:0:0:1", "l:0:2:4"
    cross = labels | {first: labels[second], second: labels[first]}
    assert first in batches["A"]["slots"][x] and second in batches["B"]["slots"][z]
    assert (labels[first], labels[second]) == (8, 7) and Counter(cross.values()) == Counter(labels.values())
    observed = [abs(cross[u]-cross[v]) for u, v in edges]
    repeated = {d: count for d, count in Counter(observed).items() if count > 1}
    missing = sorted(set(weights)-set(observed))
    witnesses = {d: [edge for edge, w in zip(edges, observed, strict=True) if w == d] for d in repeated}
    assert repeated == {5: 2, 14: 2} and missing == [6, 15]
    assert witnesses == {5: [[x, first], [z, "l:0:2:5"]], 14: [[x, "l:0:0:5"], [z, second]]}
    assert all(len({frozenset(edge) for edge in group}) == repeated[d] for d, group in witnesses.items())
    changed = [[edge, before, after] for edge, before, after in zip(edges, weights, observed, strict=True)
               if before != after]
    assert changed == [[[x, first], 6, 5], [[z, second], 15, 14]]
    cross_report = reports["cross_center"]
    assert cross_report["vertices"] == [first, second] and cross_report["pins"]["valid"]
    assert cross_report["pins"]["actual"] == {p: cross[p] for p in ("s:0", "s:1", "b:1:0")}
    assert cross_report["checker"]["edge_differences"] == observed and not cross_report["checker"]["valid"]
    physical_quotas = Counter()
    for u, v in edges:
        if graph["roles"][u]["kind"] == "branch" and graph["roles"][v]["kind"] == "leaf":
            physical_quotas[u] += 1
    assert physical_quotas == {x: 6, middle: 5, z: 8, "b:1:0": 2}
    assert set(cross) == set(labels) == set(graph["vertices"])

    quota = reports["pair_move"]
    a, b = batches["A"], batches["B"]
    moved = quota["batch"]
    pair = set(quota["labels"])
    assert pair == {8, 14} and all(moved[key] == a[key] for key in ("labels", "differences", "slots"))
    assert set(moved["allocation"][x]) == set(a["allocation"][x]) - pair
    assert set(moved["allocation"][middle]) == set(a["allocation"][middle]) | pair
    assert Counter(v for values in moved["allocation"].values() for v in values) == Counter(a["labels"])
    used_weights = Counter(abs(core[host]-v) for host, values in moved["allocation"].items() for v in values)
    assert used_weights == Counter(a["differences"])
    before = {v: abs(core[x]-v) for v in pair}
    after = {v: abs(core[middle]-v) for v in pair}
    assert before == {8: 6, 14: 12} and after == {8: 12, 14: 6}
    moved_component = next(c for c in positive_a["components"] if set(c["labels"]) == pair)
    assert moved_component["kind"] == "parallel_pair" and moved_component["assigned_hosts"] == {8: x, 14: x}
    assert quota["local"]["actual_quotas"] == {x: 3, middle: 5}
    assert quota["local"]["expected_quotas"] == {x: 5, middle: 3} and not quota["local"]["valid"]
    assert quota["local"]["tests"] == {"labels_exact": True, "differences_exact": True,
                                      "eligible": True, "quotas_exact": False}

    overlap = reports["global_overlap"]
    altered, unchanged = overlap["batches"]["A"], overlap["batches"]["B"]
    assert unchanged == b and altered["slots"] == a["slots"]
    assert sorted(altered["labels"]) == [7, 9, 10, 11, 13, 14, 15, 16]
    assert sorted(altered["differences"]) == [5, 7, 9, 10, 11, 12, 13, 14]
    assert altered["allocation"] == {x: [7, 11, 14, 15, 16], middle: [9, 10, 13]}
    local_a = r226(core, x, middle, altered, overlap["local"]["A"])
    local_b = r226(core, middle, z, unchanged, overlap["local"]["B"])
    assert local_a["chosen_quotas"] == {x: 5, middle: 3} and local_b["chosen_quotas"] == {middle: 1, z: 8}
    assert {tuple(item["labels"]): item["kind"] for item in local_a["components"]} == {
        (7, 15): "parallel_pair", (9, 13): "parallel_pair", (11,): "midpoint_loop",
        (10,): "forced_half_edge", (14,): "forced_half_edge", (16,): "forced_half_edge"}
    assert local_a["eligible_options"][7] == {x: 5, middle: 13}
    assert local_a["eligible_options"][15] == {x: 13, middle: 5}
    assert local_a["eligible_options"][14] == {x: 12}
    label_counts = Counter(altered["labels"]+unchanged["labels"])
    diff_counts = Counter(altered["differences"]+unchanged["differences"])
    repeated_labels = {v: n for v, n in label_counts.items() if n > 1}
    repeated_weights = {d: n for d, n in diff_counts.items() if n > 1}
    missing_labels = sorted(set(a["labels"]+b["labels"])-label_counts.keys())
    missing_weights = sorted(set(a["differences"]+b["differences"])-diff_counts.keys())
    global_report = overlap["global"]
    assert repeated_labels == global_report["repeated_labels"] == {7: 2}
    assert repeated_weights == global_report["repeated_differences"] == {5: 2}
    assert missing_labels == global_report["missing_labels"] == [8]
    assert missing_weights == global_report["missing_differences"] == [6]
    assert not global_report["valid"] and global_report["tests"]["slots_exact"]
    return {"swap_physical_quotas": physical_quotas, "swap_repeats": repeated, "swap_missing": missing,
            "swap_witnesses": witnesses, "swap_changed_weights": changed,
            "pair_move": {"labels": sorted(pair), "weights_before": before, "weights_after": after,
                          "quotas": quota["local"]["actual_quotas"], "numerical_inventories_preserved": True},
            "overlap_A": local_a, "overlap_B": local_b, "overlap_label_multiplicities": repeated_labels,
            "overlap_difference_multiplicities": repeated_weights, "overlap_missing_labels": missing_labels,
            "overlap_missing_differences": missing_weights}
