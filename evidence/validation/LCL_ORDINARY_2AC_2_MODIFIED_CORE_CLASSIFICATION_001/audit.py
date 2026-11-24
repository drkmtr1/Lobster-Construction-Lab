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
    assert profile in ([[2, 5, 6], [2]], [[2, 5, 4], [2]], [[6, 5, 8], [2]])
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


def inspect_core(edges, neighbors, core):
    m = len(edges)
    expected = {
        "s:0": 0, "s:1": m, "b:0:0": 2, "b:0:1": m - 6, "b:0:2": m - 4, "b:1:0": 1,
        "l:0:0:0": m - 3, "l:0:1:0": m - 5, "l:1:0:0": m - 1, "l:1:0:1": m - 2,
    }
    assert core == expected and all(type(v) is int for v in core.values())
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    core_neighbors = {v: neighbors[v] & core.keys() for v in core}
    assert len(core_edges) == len(core) - 1 == 9
    assert set(traverse(core_neighbors, ["s:0"])) == set(core)
    weights = [abs(core[u] - core[v]) for u, v in core_edges]
    assert weights == [m, 2, m - 5, m - 6, 1, m - 4, m - 1, m - 2, m - 3]
    assert sorted(core.values()) == [0, 1, 2, *range(m - 6, m + 1)]
    assert sorted(weights) == [1, 2, *range(m - 6, m + 1)]
    residual = set(range(m + 1)) - set(core.values())
    differences = set(range(1, m + 1)) - set(weights)
    assert residual == differences == set(range(3, m - 6))
    hosts = ("b:0:0", "b:0:1", "b:0:2")
    vacancies = {host: sorted(neighbors[host] - core.keys()) for host in hosts}
    assert {v for leaves in vacancies.values() for v in leaves} == set(neighbors) - set(core)
    assert all(neighbors[leaf] == {host} for host, leaves in vacancies.items() for leaf in leaves)
    return core_edges, weights, residual, vacancies


def check_adverse(original, core, binding):
    profile = [[2, 5, 4], [2]]
    edges, roles, neighbors, _, digest = reconstruct(original, profile)
    assert binding["graph_digest"] == digest and binding["profile"] == profile
    core_edges, weights, residual, vacancies = inspect_core(edges, neighbors, core)
    m = len(edges)
    t = (m - 2) // 2
    x, middle, z = "b:0:0", "b:0:1", "b:0:2"
    assert m == 18 and t == 8 and len(roles) == 19
    assert vacancies == {x: ["l:0:0:1"], middle: [f"l:0:1:{k}" for k in range(1, 5)],
                         z: [f"l:0:2:{k}" for k in range(4)]}
    assert all(2 < label < core[middle] < core[z] for label in residual)
    reference = {label: core[z] - label for label in residual}
    assert Counter(reference.values()) == Counter(residual)
    for label, weight in reference.items():
        deltas = [abs(core[host] - label) - weight for host in (x, middle, z)]
        assert deltas == [2 * (label - t), -2, 0]
    m_count = len(vacancies[middle])
    required_x = t + m_count
    assert profile[0][1] >= profile[0][2] + 1
    assert (required_x, max(residual)) == (12, 11) and required_x not in residual
    return {"status": "FIXED_CORE_INFEASIBLE", "original": binding, "core": core, "core_edges": core_edges,
            "core_weights": weights, "residual_labels": sorted(residual), "residual_weights": sorted(residual),
            "vacancies": vacancies, "t": t, "M_count": m_count, "required_X_label": required_x,
            "maximum_residual_label": max(residual), "reference_weight_sum": sum(reference.values()),
            "scope": "specified D123 labeled core only", "candidate_labeling_attempted": False}


def check_complete(edges, roles, digest, labels, ledger, checker):
    assert set(labels) == set(roles) and all(type(label) is int for label in labels.values())
    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    m = len(edges)
    assert Counter(labels.values()) == Counter(range(m + 1))
    assert Counter(weights) == Counter(range(1, m + 1)) and checker["valid"]
    assert checker["edge_differences"] == weights and checker["graph_digest"] == digest
    assert ledger == hash_canonical({"labels": sorted(labels.items()), "graph_digest": digest})
    return weights


def check_retained(original, certificate, checker):
    edges, roles, neighbors, distances, digest = reconstruct(original, [[6, 5, 8], [2]])
    labels, ledger = certificate["labels"], certificate["ledger_id"]
    weights = check_complete(edges, roles, digest, labels, ledger, checker)
    assert (labels["s:0"], labels["s:1"], labels["b:1:0"]) == (0, 26, 1)
    assert neighbors["s:1"] == {"s:0", "b:1:0"} and distances["b:1:0"] == 1
    return {"graph_digest": digest, "ledger_id": ledger, "weights": weights, "historical_formula_evaluated": False}


def check_positive(original, core, batches, labels, ledger, checker, local, global_report, pins, growth):
    edges, roles, neighbors, path_distance, digest = reconstruct(original, [[2, 5, 6], [2]])
    x, middle, z, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    m = len(edges)
    assert m == 20
    weights = check_complete(edges, roles, digest, labels, ledger, checker)
    core_edges, fixed, residual, vacancies = inspect_core(edges, neighbors, core)
    assert core == {v: labels[v] for v in core}
    a, b = batches["A"], batches["B"]
    assert a["slots"] == {x: vacancies[x], middle: vacancies[middle][:-1]}
    assert b["slots"] == {middle: vacancies[middle][-1:], z: vacancies[z]}
    assert set(a["slots"]) & set(b["slots"]) == {middle}
    slots = [(host, leaf) for batch in (a, b) for host, leaves in batch["slots"].items() for leaf in leaves]
    assert len(slots) == len({leaf for _, leaf in slots}) == m - 9
    assert {leaf for _, leaf in slots} == set(labels) - set(core)
    assert all(neighbors[leaf] == {host} and path_distance[host] == 1 for host, leaf in slots)
    assert Counter(a["labels"] + b["labels"]) == Counter(residual)
    assert Counter(a["differences"] + b["differences"]) == Counter(residual)
    assert global_report["valid"] and all(global_report["tests"].values())
    assert a["labels"] == [7, 9, 11, 13] and a["differences"] == [3, 5, 7, 11]
    assert b["labels"] == [3, 4, 5, 6, 8, 10, 12] and b["differences"] == [4, 6, 8, 9, 10, 12, 13]
    assert a["allocation"] == {x: [13], middle: [7, 9, 11]}
    assert b["allocation"] == {middle: [5], z: [3, 4, 6, 8, 10, 12]}
    a_report = r226(core, x, middle, a, local["A"])
    b_report = r226(core, middle, z, b, local["B"])
    assert (a_report["A0"], a_report["c"], a_report["eta"], a_report["integral_projection"]) == (1, 1, 0, [1, 3])
    assert (b_report["A0"], b_report["c"], b_report["eta"], b_report["integral_projection"]) == (1, 0, 0, [1])
    assert a_report["chosen_quotas"] == {x: 1, middle: 3}
    assert b_report["chosen_quotas"] == {middle: 1, z: 6}
    assert a_report["eligible_options"] == {
        7: {x: 5, middle: 7}, 9: {x: 7, middle: 5}, 11: {middle: 3}, 13: {x: 11},
    }
    assert b_report["eligible_options"] == {
        3: {z: 13}, 4: {middle: 10, z: 12}, 5: {middle: 9}, 6: {middle: 8, z: 10},
        8: {middle: 6, z: 8}, 10: {middle: 4, z: 6}, 12: {z: 4},
    }
    a_components = {tuple(item["labels"]): item for item in a_report["components"]}
    assert set(a_components) == {(7, 9), (11,), (13,)}
    assert a_components[(7, 9)]["kind"] == "parallel_pair"
    assert a_components[(7, 9)]["assigned_hosts"] == {7: middle, 9: middle}
    assert a_components[(11,)]["forced_extraction"] == {11: middle}
    assert a_components[(13,)]["forced_extraction"] == {13: x}
    b_components = {tuple(item["labels"]): item for item in b_report["components"]}
    chain = (4, 6, 8, 10, 12)
    assert set(b_components) == {(3,), (5,), chain}
    assert b_components[chain]["ordinary_edges"] == list(chain[:-1])
    assert b_components[chain]["half_edges"] == [12]
    assert b_components[chain]["forced_extraction"] == dict.fromkeys(chain, z)
    assert b_components[(3,)]["forced_extraction"] == {3: z}
    assert b_components[(5,)]["forced_extraction"] == {5: middle}

    named_terminals = {host: sorted((v for v in neighbors[host] if roles[v]["kind"] == "leaf"),
                                    key=lambda v: roles[v]["leaf"]) for host in (x, middle, z, right)}
    terminal_values = {host: [labels[v] for v in leaves] for host, leaves in named_terminals.items()}
    assert terminal_values == {x: [17, 13], middle: [15, 7, 9, 11, 5],
                               z: [3, 4, 6, 8, 10, 12], right: [19, 18]}
    for batch in (a, b):
        assert batch["allocation"] == {host: [labels[leaf] for leaf in leaves]
                                        for host, leaves in batch["slots"].items()}
    permutation = {labels[leaf]: core[z] - abs(labels[leaf] - core[host]) for host, leaf in slots}
    assert set(permutation) == residual and Counter(permutation.values()) == Counter(residual)
    orbit = [13, 5, 7, 9, 11]
    assert all(permutation[u] == v for u, v in zip(orbit, orbit[1:] + orbit[:1], strict=True))
    assert all(permutation[v] == v for v in residual - set(orbit))
    assert weights == [20, 2, 15, 11, 14, 1, 7, 5, 3, 9, 16, 13, 12, 10, 8, 6, 4, 19, 18, 17]
    distance = traverse(neighbors, ["s:0"])
    signed = []
    for u, v in edges:
        assert (distance[u] - distance[v]) % 2 == 1
        tail, head = (v, u) if distance[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "difference": labels[head] - labels[tail]})
    negatives = [entry for entry in signed if entry["difference"] < 0]
    assert negatives == [{"edge": ["l:0:0:0", x], "difference": -15},
                         {"edge": ["l:0:0:1", x], "difference": -11},
                         {"edge": ["l:0:1:0", middle], "difference": -1}]
    head_sum = sum(len(neighbors[v]) * labels[v] for v in labels if distance[v] % 2)
    tail_sum = sum(len(neighbors[v]) * labels[v] for v in labels if not distance[v] % 2)
    signed_sum = sum(row["difference"] for row in signed)
    degree_parity = sum((len(neighbors[v]) - 1) * labels[v] for v in labels)
    assert (head_sum, tail_sum) == (279, 123) and signed_sum == head_sum - tail_sum == 156
    assert degree_parity == 2 * labels[x] + 5 * labels[middle] + 6 * labels[z] + m + 2 == 192
    assert original["graph"]["spine"] == ["s:0", "s:1"] and neighbors["s:1"] == {"s:0", right}
    assert pins["valid"] and pins["actual"] == {"s:0": 0, "s:1": m, right: 1}
    assert path_distance[right] == 1 and growth["valid"] and all(growth["tests"].values())
    return {
        "graph_digest": digest, "ledger_id": ledger, "core_edges": core_edges, "core_differences": fixed,
        "residual_labels": sorted(residual), "residual_differences": sorted(residual),
        "r226": {"A": a_report, "B": b_report}, "terminal_lists": terminal_values, "named_slots": slots,
        "coordinate_permutation": permutation, "nontrivial_cycle": orbit, "absolute_differences": weights,
        "signed_incidences": signed, "signed_sum": signed_sum, "weighted_degree_sums": {"head": head_sum, "tail": tail_sum},
        "degree_parity_quantity": degree_parity, "unused_labels": [], "unused_differences": [],
        "distance_to_spine": path_distance, "physical_pins": pins, "growth_premises": growth,
    }


def controls(original, labels, core, batches, reports, positive_a):
    x, middle, z = "b:0:0", "b:0:1", "b:0:2"
    graph = original["graph"]
    edges = graph["edges"]
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    wrong = reports["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["edge_differences"] == weights

    first, second = "l:0:0:1", "l:0:2:5"
    cross = labels | {first: labels[second], second: labels[first]}
    assert first in batches["A"]["slots"][x] and second in batches["B"]["slots"][z]
    assert (labels[first], labels[second]) == (13, 12) and Counter(cross.values()) == Counter(labels.values())
    observed = [abs(cross[u]-cross[v]) for u, v in edges]
    repeated = {d: count for d, count in Counter(observed).items() if count > 1}
    missing = sorted(set(weights)-set(observed))
    witnesses = {d: [edge for edge, w in zip(edges, observed, strict=True) if w == d] for d in repeated}
    assert repeated == {3: 2, 10: 2} and missing == [4, 11]
    assert witnesses == {10: [[x, first], [z, "l:0:2:2"]], 3: [[middle, "l:0:1:3"], [z, second]]}
    assert all(len({frozenset(edge) for edge in group}) == repeated[d] for d, group in witnesses.items())
    changed = [[edge, before, after] for edge, before, after in zip(edges, weights, observed, strict=True)
               if before != after]
    assert changed == [[[x, first], 11, 10], [[z, second], 4, 3]]
    cross_report = reports["cross_center"]
    assert cross_report["vertices"] == [first, second] and cross_report["pins"]["valid"]
    assert cross_report["pins"]["actual"] == {p: cross[p] for p in ("s:0", "s:1", "b:1:0")}
    assert cross_report["checker"]["edge_differences"] == observed and not cross_report["checker"]["valid"]
    physical_quotas = Counter()
    for u, v in edges:
        if graph["roles"][u]["kind"] == "branch" and graph["roles"][v]["kind"] == "leaf":
            physical_quotas[u] += 1
    assert physical_quotas == {x: 2, middle: 5, z: 6, "b:1:0": 2}
    assert set(cross) == set(labels) == set(graph["vertices"])

    quota = reports["pair_move"]
    a, b = batches["A"], batches["B"]
    moved = quota["batch"]
    pair = set(quota["labels"])
    assert pair == {7, 9} and all(moved[key] == a[key] for key in ("labels", "differences", "slots"))
    assert set(moved["allocation"][x]) == set(a["allocation"][x]) | pair
    assert set(moved["allocation"][middle]) == set(a["allocation"][middle]) - pair
    assert Counter(v for values in moved["allocation"].values() for v in values) == Counter(a["labels"])
    used_weights = Counter(abs(core[host]-v) for host, values in moved["allocation"].items() for v in values)
    assert used_weights == Counter(a["differences"])
    before = {v: abs(core[middle]-v) for v in pair}
    after = {v: abs(core[x]-v) for v in pair}
    assert before == {7: 7, 9: 5} and after == {7: 5, 9: 7}
    moved_component = next(c for c in positive_a["components"] if set(c["labels"]) == pair)
    assert moved_component["kind"] == "parallel_pair" and moved_component["assigned_hosts"] == {7: middle, 9: middle}
    assert quota["local"]["actual_quotas"] == {x: 3, middle: 1}
    assert quota["local"]["expected_quotas"] == {x: 1, middle: 3} and not quota["local"]["valid"]
    assert quota["local"]["tests"] == {"labels_exact": True, "differences_exact": True,
                                      "eligible": True, "quotas_exact": False}

    overlap = reports["global_overlap"]
    altered, unchanged = overlap["batches"]["A"], overlap["batches"]["B"]
    assert unchanged == b and altered["slots"] == a["slots"]
    assert sorted(altered["labels"]) == [7, 9, 11, 12]
    assert sorted(altered["differences"]) == [3, 5, 7, 10]
    assert altered["allocation"] == {x: [12], middle: [7, 9, 11]}
    local_a = r226(core, x, middle, altered, overlap["local"]["A"])
    local_b = r226(core, middle, z, unchanged, overlap["local"]["B"])
    assert local_a["chosen_quotas"] == {x: 1, middle: 3} and local_b["chosen_quotas"] == {middle: 1, z: 6}
    assert {tuple(item["labels"]): item["kind"] for item in local_a["components"]} == {
        (7, 9): "parallel_pair", (11,): "forced_half_edge", (12,): "forced_half_edge"}
    assert local_a["eligible_options"][12] == {x: 10}
    assert local_a["eligible_options"][11] == {middle: 3}
    label_counts = Counter(altered["labels"]+unchanged["labels"])
    diff_counts = Counter(altered["differences"]+unchanged["differences"])
    repeated_labels = {v: n for v, n in label_counts.items() if n > 1}
    repeated_weights = {d: n for d, n in diff_counts.items() if n > 1}
    missing_labels = sorted(set(a["labels"]+b["labels"])-label_counts.keys())
    missing_weights = sorted(set(a["differences"]+b["differences"])-diff_counts.keys())
    global_report = overlap["global"]
    assert repeated_labels == global_report["repeated_labels"] == {12: 2}
    assert repeated_weights == global_report["repeated_differences"] == {10: 2}
    assert missing_labels == global_report["missing_labels"] == [13]
    assert missing_weights == global_report["missing_differences"] == [11]
    assert not global_report["valid"] and global_report["tests"]["slots_exact"]
    return {"swap_physical_quotas": physical_quotas, "swap_repeats": repeated, "swap_missing": missing,
            "swap_witnesses": witnesses, "swap_changed_weights": changed,
            "pair_move": {"labels": sorted(pair), "weights_before": before, "weights_after": after,
                          "quotas": quota["local"]["actual_quotas"], "numerical_inventories_preserved": True},
            "overlap_A": local_a, "overlap_B": local_b, "overlap_label_multiplicities": repeated_labels,
            "overlap_difference_multiplicities": repeated_weights, "overlap_missing_labels": missing_labels,
            "overlap_missing_differences": missing_weights}
