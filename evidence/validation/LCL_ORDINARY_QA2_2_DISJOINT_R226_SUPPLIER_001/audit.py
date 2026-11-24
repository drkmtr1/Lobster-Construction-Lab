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


def reconstruct(original):
    graph = original["graph"]
    profile = [[5, 3, 2], [2]]
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
    assert graph["edges"] == edges and len(incidence) == len(edges) == 17
    assert Counter(graph["vertices"]) == Counter(roles.keys()) and len(roles) == 18
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


def r226(core, low, high, batch, local):
    inventory = set(batch["differences"])
    assert len(inventory) == len(batch["differences"]) == len(batch["labels"]) == len(set(batch["labels"]))
    assert 0 not in inventory and min(inventory) > 0 and core[low] < core[high]
    assert all(x not in (core[low], core[high]) for x in batch["labels"])
    weight_options, rows, groups = {}, {}, defaultdict(list)
    for x in batch["labels"]:
        options = {h: abs(x-core[h]) for h in (low, high)}
        eligible = {h: d for h, d in options.items() if d in inventory}
        assert eligible
        weight_options[x], rows[x] = options, eligible
        groups[tuple(sorted(set(eligible.values())))].append(x)
    assert rows == local["eligible_options"]
    assert Counter(d for group in groups for d in group) == Counter(inventory)
    components = []
    forced_low, pairs = 0, 0
    assignment = batch["allocation"]
    for endpoints, resources in sorted(groups.items()):
        assert len(endpoints) == len(resources)
        x = resources[0]
        owners = [h for h in (low, high) if set(resources) <= set(assignment[h])]
        assert len(owners) == 1
        if len(resources) == 1:
            assert len(rows[x]) == 1 and owners[0] in rows[x]
            forced_low += int(owners[0] == low)
            kind = "forced_half_edge"
        else:
            y = resources[1]
            assert len(rows[x]) == len(rows[y]) == 2 and x+y == core[low]+core[high]
            assert rows[x][low] == rows[y][high] and rows[x][high] == rows[y][low]
            pairs += 1
            kind = "parallel_pair"
        components.append({"kind": kind, "labels": resources, "differences": list(endpoints),
                           "balance": {"label_resources": len(resources), "difference_vertices": len(endpoints)},
                           "assigned_host": owners[0]})
    assert (core[low]+core[high]) % 2 == 1
    projection = [forced_low+2*k for k in range(pairs+1)]
    actual = {host: len(assignment[host]) for host in (low, high)}
    quotas = {host: len(batch["slots"][host]) for host in (low, high)}
    assigned_labels = Counter(x for labels in assignment.values() for x in labels)
    assigned_weights = Counter(abs(core[h]-x) for h, labels in assignment.items() for x in labels)
    assert assigned_labels == Counter(batch["labels"]) and assigned_weights == Counter(batch["differences"])
    assert actual == quotas == local["actual_quotas"] == local["expected_quotas"] and quotas[low] in projection
    assert local["valid"]
    return {"hosts": [low, high], "weight_options": weight_options, "eligible_options": rows,
            "components": components, "A0": forced_low, "c": pairs, "eta": 0,
            "integral_projection": projection, "chosen_quotas": quotas}


def boundary(original, core, batches, labels, ledger, checker, local, global_report, pins, growth):
    edges, roles, neighbors, path_distance, digest = reconstruct(original)
    h, low, c, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    expected_core = {"s:0": 0, "s:1": 17, h: 13, low: 2, c: 11, right: 1,
                     "l:0:0:0": 12, "l:0:1:0": 14, "l:1:0:0": 16, "l:1:0:1": 15}
    assert core == expected_core and core == {v: labels[v] for v in expected_core}
    assert set(labels) == set(roles) and all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(18))
    assert ledger == hash_canonical({"graph_digest": digest, "labels": sorted(labels.items())})
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    core_neighbors = {v: neighbors[v] & core.keys() for v in core}
    assert len(core_edges) == len(core)-1 == 9 and set(traverse(core_neighbors, ["s:0"])) == set(core)
    fixed = [abs(core[u]-core[v]) for u, v in core_edges]
    assert sorted(core.values()) == [0, 1, 2, *range(11, 18)]
    assert sorted(fixed) == [1, 2, *range(11, 18)]
    remaining_labels = set(range(18))-set(core.values())
    remaining_weights = set(range(1, 18))-set(fixed)
    assert remaining_labels == remaining_weights == set(range(3, 11))
    expected_a = {low: [], h: [f"l:0:0:{k}" for k in range(1, 5)]}
    expected_b = {low: ["l:0:1:1", "l:0:1:2"], c: ["l:0:2:0", "l:0:2:1"]}
    local_a, local_b = batches["A"], batches["B"]
    assert (local_a["slots"], local_b["slots"]) == (expected_a, expected_b)
    incidence = [(host, leaf) for groups in (expected_a, expected_b) for host, leaves in groups.items() for leaf in leaves]
    assert len(incidence) == len({leaf for _, leaf in incidence}) == 8
    assert {leaf for _, leaf in incidence} == set(labels)-set(core)
    assert all(neighbors[leaf] == {host} and path_distance[host] == 1 for host, leaf in incidence)
    assert set(expected_a) & set(expected_b) == {low}
    assert local_a["labels"] == [3, 4, 6, 9] and local_a["differences"] == [4, 7, 9, 10]
    assert local_b["labels"] == [5, 7, 8, 10] and local_b["differences"] == [3, 5, 6, 8]
    assert Counter(local_a["labels"]+local_b["labels"]) == Counter(remaining_labels)
    assert Counter(local_a["differences"]+local_b["differences"]) == Counter(remaining_weights)
    assert global_report["valid"] and all(global_report["tests"].values())
    a_report = r226(core, low, h, local_a, local["A"])
    b_report = r226(core, low, c, local_b, local["B"])
    assert (a_report["A0"], a_report["c"], a_report["integral_projection"]) == (0, 1, [0, 2])
    assert (b_report["A0"], b_report["c"], b_report["integral_projection"]) == (2, 1, [2, 4])
    assert a_report["eligible_options"][6] == {low: 4, h: 7} and a_report["eligible_options"][9] == {low: 7, h: 4}
    assert b_report["weight_options"][7][c] == 4 and b_report["eligible_options"][7] == {low: 5}
    assert b_report["weight_options"][10][c] == 1 and b_report["eligible_options"][10] == {low: 8}
    quotas = {}
    for host, target in ((h, [12, 3, 4, 6, 9]), (low, [14, 7, 10]), (c, [5, 8]), (right, [16, 15])):
        leaves = sorted(neighbors[host]-{"s:0", "s:1"}, key=lambda v: roles[v]["leaf"])
        assert [labels[v] for v in leaves] == target
        quotas[host] = len(leaves)
    for batch in batches.values():
        assert batch["allocation"] == {host: [labels[leaf] for leaf in leaves] for host, leaves in batch["slots"].items()}

    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    assert weights == [17, 13, 1, 10, 9, 7, 4, 2, 12, 5, 8, 11, 6, 3, 16, 15, 14]
    assert Counter(weights) == Counter(range(1, 18)) and checker["edge_differences"] == weights and checker["valid"]
    parity = traverse(neighbors, ["s:0"])
    signed = []
    for u, v in edges:
        assert (parity[u]-parity[v]) % 2 == 1
        tail, head = (v, u) if parity[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "difference": labels[head]-labels[tail]})
    negatives = [row for row in signed if row["difference"] < 0]
    assert negatives == [{"edge": [f"l:0:1:{k}", low], "difference": d} for k, d in enumerate((-12, -5, -8))]
    signed_sum = sum(row["difference"] for row in signed)
    assert signed_sum == 103
    degree_parity = sum((len(neighbors[v])-1)*labels[v] for v in labels)
    assert degree_parity == 5*labels[h]+3*labels[low]+2*labels[c]+17+2 == 112
    assert original["graph"]["spine"] == ["s:0", "s:1"] and neighbors["s:1"] == {"s:0", right}
    assert pins["valid"] and pins["actual"] == {"s:0": 0, "s:1": 17, right: 1}
    assert path_distance[right] == 1 and growth["valid"] and all(growth["tests"].values())
    return {"graph_digest": digest, "ledger_id": ledger, "core_edges": core_edges, "core_differences": fixed,
            "residual_labels": sorted(remaining_labels), "residual_differences": sorted(remaining_weights),
            "r226": {"A": a_report, "B": b_report}, "formula_vertices": sorted(labels),
            "reconstructed_quotas": quotas, "absolute_differences": weights, "signed_incidences": signed,
            "signed_sum": signed_sum, "degree_parity_quantity": degree_parity,
            "unused_labels": [], "unused_differences": [], "distance_to_spine": path_distance}


def controls(original, labels, core, batches, reports):
    h, low, c = "b:0:0", "b:0:1", "b:0:2"
    edges = original["graph"]["edges"]
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    wrong = reports["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["edge_differences"] == weights

    u, v = "l:0:1:1", "l:0:2:0"
    cross = labels | {u: labels[v], v: labels[u]}
    assert u in batches["B"]["slots"][low] and v in batches["B"]["slots"][c]
    assert (labels[u], labels[v]) == (7, 5) and sorted(cross.values()) == sorted(labels.values())
    observed = [abs(cross[x]-cross[y]) for x, y in edges]
    repeated = {d: count for d, count in Counter(observed).items() if count > 1}
    missing = sorted(set(weights)-set(observed))
    witnesses = {d: [edge for edge, w in zip(edges, observed, strict=True) if w == d] for d in repeated}
    assert repeated == {3: 2, 4: 2} and missing == [5, 6]
    assert witnesses == {3: [[low, u], [c, "l:0:2:1"]], 4: [[h, "l:0:0:4"], [c, v]]}
    cross_report = reports["cross_center"]
    assert cross_report["vertices"] == [u, v] and cross_report["pins"]["valid"]
    assert cross_report["pins"]["actual"] == {p: cross[p] for p in ("s:0", "s:1", "b:1:0")}
    assert cross_report["checker"]["edge_differences"] == observed and not cross_report["checker"]["valid"]

    quota = reports["local_quota_failure"]
    flip = quota["batch"]
    assert flip["labels"] == batches["B"]["labels"] and flip["differences"] == batches["B"]["differences"]
    assert flip["slots"] == batches["B"]["slots"]
    assert set(flip["allocation"][low])-set(batches["B"]["allocation"][low]) == {5, 8}
    assert flip["allocation"][c] == [] and quota["local"]["actual_quotas"] == {low: 4, c: 0}
    assert quota["local"]["expected_quotas"] == {low: 2, c: 2} and not quota["local"]["valid"]
    assert Counter(flip["allocation"][low]) == Counter(batches["B"]["labels"])
    assert Counter(abs(core[low]-x) for x in flip["allocation"][low]) == Counter(batches["B"]["differences"])

    overlap = reports["global_overlap"]
    ol_a, ol_b = overlap["batches"]["A"], overlap["batches"]["B"]
    assert ol_b == batches["B"] and ol_a["slots"] == batches["A"]["slots"]
    assert set(batches["A"]["labels"])-set(ol_a["labels"]) == {6, 9}
    assert set(ol_a["labels"])-set(batches["A"]["labels"]) == {5, 10}
    assert ol_a["differences"] == [3, 8, 9, 10] and ol_a["allocation"] == {low: [], h: [3, 4, 5, 10]}
    a_check = r226(core, low, h, ol_a, overlap["local"]["A"])
    b_check = r226(core, low, c, ol_b, overlap["local"]["B"])
    assert a_check["chosen_quotas"] == {low: 0, h: 4} and b_check["chosen_quotas"] == {low: 2, c: 2}
    global_report = overlap["global"]
    label_conflicts = Counter(ol_a["labels"]+ol_b["labels"])
    weight_conflicts = Counter(ol_a["differences"]+ol_b["differences"])
    repeated_labels = {x: count for x, count in label_conflicts.items() if count > 1}
    repeated_weights = {d: count for d, count in weight_conflicts.items() if count > 1}
    missing_labels = sorted(set(range(3, 11))-label_conflicts.keys())
    missing_weights = sorted(set(range(3, 11))-weight_conflicts.keys())
    assert repeated_labels == global_report["repeated_labels"] == {5: 2, 10: 2}
    assert repeated_weights == global_report["repeated_differences"] == {3: 2, 8: 2}
    assert missing_labels == global_report["missing_labels"] == [6, 9]
    assert missing_weights == global_report["missing_differences"] == [4, 7]
    assert not global_report["valid"] and global_report["tests"]["slots_exact"]
    return {"swap_repeats": repeated, "swap_missing": missing, "swap_witnesses": witnesses,
            "swap_batches": ["B", "B"], "quota_only_counts": quota["local"]["actual_quotas"],
            "overlap_A": a_check, "overlap_B": b_check, "overlap_label_multiplicities": repeated_labels,
            "overlap_difference_multiplicities": repeated_weights, "overlap_missing_labels": missing_labels,
            "overlap_missing_differences": missing_weights}
