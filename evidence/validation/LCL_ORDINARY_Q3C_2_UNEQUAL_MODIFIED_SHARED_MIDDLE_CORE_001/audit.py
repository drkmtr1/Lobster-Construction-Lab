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
    assert profile in ([[6, 3, 6], [2]], [[6, 3, 8], [2]])
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


def check_profile(original, core, batches, labels, ledger, checker, local, global_report, pins, growth, *, retained):
    c = 6 if retained else 8
    edges, roles, neighbors, path_distance, digest = reconstruct(original, [[6, 3, c], [2]])
    m = len(edges)
    x, middle, z, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    expected_core = {"s:0": 0, "s:1": m, x: 2, middle: m-6, z: m-4, right: 1,
                     "l:0:0:0": m-3, "l:0:1:0": m-5, "l:1:0:0": m-1, "l:1:0:1": m-2}
    assert core == expected_core and core == {v: labels[v] for v in expected_core}
    assert set(labels) == set(roles) and all(type(label) is int for label in labels.values())
    assert Counter(labels.values()) == Counter(range(m+1))
    assert ledger == hash_canonical({"graph_digest": digest, "labels": sorted(labels.items())})
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    core_neighbors = {v: neighbors[v] & core.keys() for v in core}
    assert len(core_edges) == len(core)-1 == 9 and set(traverse(core_neighbors, ["s:0"])) == set(core)
    fixed = [abs(core[u]-core[v]) for u, v in core_edges]
    assert fixed == [m, 2, m-5, m-6, 1, m-4, m-1, m-2, m-3]
    assert sorted(core.values()) == [0, 1, 2, *range(m-6, m+1)]
    assert sorted(fixed) == [1, 2, *range(m-6, m+1)]
    residual_labels = set(range(m+1))-set(core.values())
    residual_weights = set(range(1, m+1))-set(fixed)
    assert residual_labels == residual_weights == set(range(3, m-6))

    a, b = batches["A"], batches["B"]
    assert a["slots"] == {x: [f"l:0:0:{i}" for i in range(1, 6)], middle: ["l:0:1:1"]}
    assert b["slots"] == {middle: ["l:0:1:2"], z: [f"l:0:2:{i}" for i in range(c)]}
    supplied_slots = [(host, leaf) for batch in (a, b) for host, leaves in batch["slots"].items() for leaf in leaves]
    assert len(supplied_slots) == len({leaf for _, leaf in supplied_slots}) == c+7
    assert {leaf for _, leaf in supplied_slots} == set(labels)-set(core)
    assert all(neighbors[leaf] == {host} and path_distance[host] == 1 for host, leaf in supplied_slots)
    assert set(a["slots"]) & set(b["slots"]) == {middle}
    start, end = c//2+4, c//2+10
    t = (m-2)//2
    interval = set(range(start, end+1))
    outside = residual_labels-interval
    assert len(interval) == 7 and (len(range(3, start)), len(range(end+1, m-6))) == (c//2+1, c//2-1)
    assert len(outside) == c and {t-2, t, t+2} <= interval
    assert set(a["labels"]) == interval-{t}
    assert set(a["differences"]) == {m-4-v for v in interval}-{t-4}
    assert set(b["labels"]) == outside | {t}
    assert set(b["differences"]) == {m-4-v for v in outside} | {t-4}
    assert Counter(a["labels"]+b["labels"]) == Counter(residual_labels)
    assert Counter(a["differences"]+b["differences"]) == Counter(residual_weights)
    assert global_report["valid"] and all(global_report["tests"].values())
    a_report = r226(core, x, middle, a, local["A"])
    b_report = r226(core, middle, z, b, local["B"])
    assert (a_report["A0"], a_report["c"], a_report["eta"], a_report["integral_projection"]) == (2, 1, 1, [2, 3, 4, 5])
    assert (b_report["A0"], b_report["c"], b_report["eta"], b_report["integral_projection"]) == (1, 0, 0, [1])
    observed_a = {tuple(item["labels"]): item["kind"] for item in a_report["components"]}
    assert observed_a == {(start, end-2): "parallel_pair", (t-1,): "midpoint_loop",
                          (t-2,): "forced_half_edge", (end-1,): "forced_half_edge",
                          (end,): "forced_half_edge"}
    assert a_report["eligible_options"][t-2] == {middle: t-2}
    assert a_report["eligible_options"][t-1] == {x: t-3, middle: t-3}
    chains = ((3, 5), (4, 6), (14,), (15,)) if retained else ((3, 5, 7), (4, 6), (15, 17), (16,))
    expected_b = {chain: ("tree_with_half_edge" if len(chain) > 1 else "forced_half_edge", dict.fromkeys(chain, z))
                  for chain in chains}
    expected_b[(t,)] = ("forced_half_edge", {t: middle})
    observed_b = {tuple(item["labels"]): (item["kind"], item["forced_extraction"])
                  for item in b_report["components"]}
    assert observed_b == expected_b
    assert b_report["eligible_options"][t] == {middle: t-4}
    assert b_report["eligible_options"][3] == {middle: m-9, z: m-7}
    assert b_report["eligible_options"][4] == {middle: m-10, z: m-8}
    targets = {x: [m-3, *sorted(interval-{t-2, t})], middle: [m-5, t-2, t],
               z: sorted(outside), right: [m-1, m-2]}
    quotas = {}
    for host, target in targets.items():
        leaves = sorted(neighbors[host]-{"s:0", "s:1"}, key=lambda v: roles[v]["leaf"])
        assert [labels[v] for v in leaves] == target
        quotas[host] = len(leaves)
    assert quotas == {x: 6, middle: 3, z: c, right: 2}
    for batch in batches.values():
        assert batch["allocation"] == {host: [labels[leaf] for leaf in leaves] for host, leaves in batch["slots"].items()}

    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    expected_weights = ([22, 2, 17, 5, 7, 9, 10, 11, 16, 1, 8, 6, 18, 15, 14, 13, 12, 4, 3, 21, 20, 19]
                        if retained else
                        [24, 2, 19, 6, 8, 10, 11, 12, 18, 1, 9, 7, 20, 17, 16, 15, 14, 13, 5, 4, 3, 23, 22, 21])
    assert weights == expected_weights
    assert Counter(weights) == Counter(range(1, m+1)) and checker["edge_differences"] == weights and checker["valid"]
    parity = traverse(neighbors, ["s:0"])
    signed = []
    for u, v in edges:
        assert (parity[u]-parity[v]) % 2 == 1
        tail, head = (v, u) if parity[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "difference": labels[head]-labels[tail]})
    negatives = [row for row in signed if row["difference"] < 0]
    assert negatives == [{"edge": [f"l:0:0:{i}", x], "difference": 2-value}
                         for i, value in enumerate(targets[x])] + [
                             {"edge": ["l:0:1:0", middle], "difference": -1}]
    signed_sum = sum(row["difference"] for row in signed)
    assert signed_sum == (133 if retained else 166)
    degree_parity = sum((len(neighbors[v])-1)*labels[v] for v in labels)
    assert degree_parity == 6*labels[x]+3*labels[middle]+c*labels[z]+m+2
    assert degree_parity == (192 if retained else 252)
    assert original["graph"]["spine"] == ["s:0", "s:1"] and neighbors["s:1"] == {"s:0", right}
    assert pins["valid"] and pins["actual"] == {"s:0": 0, "s:1": m, right: 1}
    assert path_distance[right] == 1 and growth["valid"] and all(growth["tests"].values())
    return {"graph_digest": digest, "ledger_id": ledger, "core_edges": core_edges, "core_differences": fixed,
            "residual_labels": sorted(residual_labels), "residual_differences": sorted(residual_weights),
            "r226": {"A": a_report, "B": b_report}, "formula_vertices": sorted(labels),
            "interval": {"b": start, "e": end, "t": t, "q": 6, "c": c},
            "named_slots": supplied_slots, "reconstructed_quotas": quotas, "absolute_differences": weights,
            "signed_incidences": signed, "signed_sum": signed_sum, "degree_parity_quantity": degree_parity,
            "unused_labels": [], "unused_differences": [], "distance_to_spine": path_distance}


def controls(original, labels, core, batches, reports, positive_b):
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
    assert repeated == {5: 2, 12: 2} and missing == [6, 13]
    assert witnesses == {5: [[x, first], [z, "l:0:2:5"]], 12: [[x, "l:0:0:5"], [z, second]]}
    assert all(len({frozenset(edge) for edge in group}) == repeated[d] for d, group in witnesses.items())
    changed = [[edge, before, after] for edge, before, after in zip(edges, weights, observed, strict=True)
               if before != after]
    assert changed == [[[x, first], 6, 5], [[z, second], 13, 12]]
    cross_report = reports["cross_center"]
    assert cross_report["vertices"] == [first, second] and cross_report["pins"]["valid"]
    assert cross_report["pins"]["actual"] == {p: cross[p] for p in ("s:0", "s:1", "b:1:0")}
    assert cross_report["checker"]["edge_differences"] == observed and not cross_report["checker"]["valid"]
    physical_quotas = Counter()
    for u, v in edges:
        if graph["roles"][u]["kind"] == "branch" and graph["roles"][v]["kind"] == "leaf":
            physical_quotas[u] += 1
    assert physical_quotas == {x: 6, middle: 3, z: 8, "b:1:0": 2}
    assert set(cross) == set(labels) == set(graph["vertices"])

    quota = reports["chain_forcing"]
    a, b = batches["A"], batches["B"]
    moved = quota["batch"]
    label = quota["moved_label"]
    assert label == 3 and all(moved[key] == b[key] for key in ("labels", "differences", "slots"))
    assert set(moved["allocation"][middle]) == set(b["allocation"][middle]) | {label}
    assert set(moved["allocation"][z]) == set(b["allocation"][z])-{label}
    assert Counter(v for values in moved["allocation"].values() for v in values) == Counter(b["labels"])
    used = defaultdict(list)
    for host, values in moved["allocation"].items():
        for v in values:
            used[abs(core[host]-v)].append({"host": host, "label": v})
    chain_repeats = {d: len(rows) for d, rows in used.items() if len(rows) > 1}
    chain_missing = sorted(set(b["differences"])-used.keys())
    assert set(used) <= set(b["differences"])
    assert chain_repeats == {15: 2} and chain_missing == [17]
    assert used[15] == [{"host": middle, "label": 3}, {"host": z, "label": 5}]
    assert quota["local"]["eligible_options"][3] == {middle: 15, z: 17}
    root_chain = next(item for item in positive_b["components"] if label in item["labels"])
    assert root_chain["labels"] == [3, 5, 7] and root_chain["forced_extraction"][3] == z
    assert quota["local"]["actual_quotas"] == {middle: 2, z: 7}
    assert quota["local"]["expected_quotas"] == {middle: 1, z: 8} and not quota["local"]["valid"]
    assert quota["local"]["tests"] == {"labels_exact": True, "differences_exact": False,
                                      "eligible": True, "quotas_exact": False}

    overlap = reports["global_overlap"]
    altered, unchanged = overlap["batches"]["A"], overlap["batches"]["B"]
    assert unchanged == b and altered["slots"] == a["slots"]
    assert altered["labels"] == [7, 9, 10, 12, 13, 14] and altered["differences"] == [5, 8, 9, 10, 11, 12]
    assert altered["allocation"] == {x: [7, 10, 12, 13, 14], middle: [9]}
    local_a = r226(core, x, middle, altered, overlap["local"]["A"])
    local_b = r226(core, middle, z, unchanged, overlap["local"]["B"])
    assert local_a["chosen_quotas"] == {x: 5, middle: 1} and local_b["chosen_quotas"] == {middle: 1, z: 8}
    assert {tuple(item["labels"]): item["kind"] for item in local_a["components"]} == {
        (7, 13): "parallel_pair", (10,): "midpoint_loop", (9,): "forced_half_edge",
        (12,): "forced_half_edge", (14,): "forced_half_edge"}
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
            "chain_eligible_move": {"label": label, "reserved_weight_at_M": 15,
                                    "forced_host": root_chain["forced_extraction"][label],
                                    "repeated_weights": chain_repeats, "missing_weights": chain_missing,
                                    "label_host_witnesses": used[15], "quotas": quota["local"]["actual_quotas"]},
            "overlap_A": local_a, "overlap_B": local_b, "overlap_label_multiplicities": repeated_labels,
            "overlap_difference_multiplicities": repeated_weights, "overlap_missing_labels": missing_labels,
            "overlap_missing_differences": missing_weights}
