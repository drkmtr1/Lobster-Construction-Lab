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
    assert profile in ([[6, 3, 2], [2]], [[6, 3, 4], [2]], [[6, 5, 6], [2]])
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
    forced_low, pairs, loops = 0, 0, 0
    assignment = batch["allocation"]
    for endpoints, resources in sorted(groups.items()):
        assert len(endpoints) == len(resources)
        x = resources[0]
        owners = [h for h in (low, high) if set(resources) <= set(assignment[h])]
        assert len(owners) == 1
        if len(resources) == 1:
            if len(rows[x]) == 1:
                assert owners[0] in rows[x]
                forced_low += int(owners[0] == low)
                kind = "forced_half_edge"
            else:
                assert rows[x] == {low: endpoints[0], high: endpoints[0]}
                assert 2*x == core[low]+core[high]
                loops += 1
                kind = "midpoint_loop"
        else:
            assert len(resources) == 2
            y = resources[1]
            assert len(rows[x]) == len(rows[y]) == 2 and x+y == core[low]+core[high]
            assert rows[x][low] == rows[y][high] and rows[x][high] == rows[y][low]
            pairs += 1
            kind = "parallel_pair"
        half_edges = int(kind == "forced_half_edge")
        ordinary_edges = len(resources)-half_edges
        assert ordinary_edges+half_edges == len(endpoints)
        components.append({"kind": kind, "labels": resources, "differences": list(endpoints),
                           "balance": {"label_resources": len(resources), "difference_vertices": len(endpoints),
                                       "ordinary_edges_including_loops": ordinary_edges, "half_edges": half_edges},
                           "assigned_host": owners[0]})
    assert 0 <= loops <= 1
    projection = [forced_low+2*k+bit for k in range(pairs+1) for bit in range(loops+1)]
    actual = {host: len(assignment[host]) for host in (low, high)}
    quotas = {host: len(batch["slots"][host]) for host in (low, high)}
    assigned_labels = Counter(x for labels in assignment.values() for x in labels)
    assigned_weights = Counter(abs(core[h]-x) for h, labels in assignment.items() for x in labels)
    assert assigned_labels == Counter(batch["labels"]) and assigned_weights == Counter(batch["differences"])
    assert actual == quotas == local["actual_quotas"] == local["expected_quotas"] and quotas[low] in projection
    assert local["valid"]
    return {"hosts": [low, high], "weight_options": weight_options, "eligible_options": rows,
            "components": components, "A0": forced_low, "c": pairs, "eta": loops,
            "integral_projection": projection, "chosen_quotas": quotas}


def core_audit(core, edges, neighbors, m, q, a, c):
    h, low, third, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    assert core == {"s:0": 0, "s:1": m, h: m-4, low: 2, third: m-6, right: 1,
                    "l:0:0:0": m-5, "l:0:1:0": m-3, "l:1:0:0": m-1, "l:1:0:1": m-2}
    center_neighbors = {host: neighbors[host]-{"s:0", "s:1"} for host in (h, low, third, right)}
    assert tuple(len(xs) for xs in center_neighbors.values()) == (q, a, c, 2)
    core_edges = [[u, v] for u, v in edges if u in core and v in core]
    assert len(core_edges) == 9 and len(core) == 10
    subgraph = {v: neighbors[v] & core.keys() for v in core}
    assert set(traverse(subgraph, ["s:0"])) == set(core)
    fixed = [abs(core[u]-core[v]) for u, v in core_edges]
    assert sorted(core.values()) == [0, 1, 2, *range(m-6, m+1)]
    assert sorted(fixed) == [1, 2, *range(m-6, m+1)]
    unused_labels = set(range(m+1))-set(core.values())
    unused_weights = set(range(1, m+1))-set(fixed)
    assert unused_labels == unused_weights == set(range(3, m-6))
    degree_parity = sum((len(neighbors[v])-1)*x for v, x in core.items())
    assert degree_parity == q*core[h]+a*core[low]+c*core[third]+m+2
    assert degree_parity % 2 == 0
    return core_edges, fixed, unused_labels, unused_weights, degree_parity


def positive(original, branch, core, batches, labels, ledger, checker, local, pins, growth):
    profile = [[6, 3, 2], [2]] if branch == "I" else [[6, 5, 6], [2]]
    edges, roles, neighbors, path_distance, digest = reconstruct(original, profile)
    q, a, c = profile[0]
    m = len(edges)
    h, low, third, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    core_edges, fixed, unused_labels, unused_weights, parity = core_audit(core, edges, neighbors, m, q, a, c)
    assert len(labels) == m+1 and set(labels) == set(roles) and all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(m+1)) and all(labels[v] == n for v, n in core.items())
    assert ledger == hash_canonical({"graph_digest": digest, "labels": sorted(labels.items())})
    if branch == "I":
        expected_lists = ([13, 3, 4, 6, 8, 10], [15, 7, 11], [5, 9], [17, 16])
        resources_a = ([3, 4, 6, 8, 10], [4, 6, 8, 10, 11])
        resources_b = ([5, 7, 9, 11], [3, 5, 7, 9])
        expected_weights = [18, 14, 1, 11, 10, 8, 6, 4, 2, 13, 5, 9, 12, 7, 3, 17, 16, 15]
        negatives, signed_sum, expected_parity, s = [-13, -5, -9], 117, 134, 2
        assert c == q-4
    else:
        expected_lists = ([19, 3, 4, 5, 11, 17], [21, 9, 10, 15, 16], [6, 7, 8, 12, 13, 14], [23, 22])
        resources_a = ([3, 4, 5, 11, 17], [3, 9, 15, 16, 17])
        resources_b = ([6, 7, 8, 9, 10, 12, 13, 14, 15, 16], [4, 5, 6, 7, 8, 10, 11, 12, 13, 14])
        expected_weights = [24, 20, 1, 17, 16, 15, 9, 3, 2, 19, 7, 8, 13, 14, 18, 12, 11, 10, 6, 5, 4, 23, 22, 21]
        negatives, signed_sum, expected_parity, s = [-19, -7, -8, -13, -14], 178, 264, 4
        assert c > q+a-7
    assert parity == expected_parity
    ordered = {host: sorted(neighbors[host]-{"s:0", "s:1"}, key=lambda v: roles[v]["leaf"])
               for host in (h, low, third, right)}
    for host, expected in zip(ordered, expected_lists, strict=True):
        assert [labels[v] for v in ordered[host]] == expected
    a_batch, b_batch = batches["A"], batches["B"]
    assert (a_batch["labels"], a_batch["differences"]) == resources_a
    assert (b_batch["labels"], b_batch["differences"]) == resources_b
    assert a_batch["slots"] == {low: ordered[low][s+1:], h: ordered[h][1:]}
    assert b_batch["slots"] == {low: ordered[low][1:s+1], third: ordered[third]}
    slots = [(host, leaf) for batch in (a_batch, b_batch) for host, leaves in batch["slots"].items() for leaf in leaves]
    assert len(slots) == len(unused_labels) and {v for _, v in slots} == set(labels)-set(core)
    assert all(neighbors[v] == {host} and path_distance[host] == 1 for host, v in slots)
    for batch in batches.values():
        assert batch["allocation"] == {host: [labels[v] for v in leaves] for host, leaves in batch["slots"].items()}
    assert Counter(a_batch["labels"]+b_batch["labels"]) == Counter(unused_labels)
    assert Counter(a_batch["differences"]+b_batch["differences"]) == Counter(unused_weights)
    local_a = r226(core, low, h, a_batch, local["A"])
    local_b = r226(core, low, third, b_batch, local["B"])
    assert (local_a["A0"], local_a["c"], local_a["eta"], local_a["integral_projection"]) == (0, 1, 1, [0, 1, 2, 3])
    assert (local_b["A0"], local_b["c"], local_b["eta"]) == (s-1, c//2, 1)
    assert local_b["integral_projection"] == list(range(s-1, s+c+1))
    assert local_a["chosen_quotas"] == {low: 0, h: q-1} and local_b["chosen_quotas"] == {low: s, third: c}
    t = (m-2)//2
    for report, label, host in ((local_a, t, h), (local_b, t-1, low)):
        loops = [row for row in report["components"] if row["kind"] == "midpoint_loop"]
        assert len(loops) == 1 and loops[0]["labels"] == [label] and loops[0]["assigned_host"] == host
        assert loops[0]["differences"] == [label-2]
    forced_b = [row["labels"][0] for row in local_b["components"] if row["kind"] == "forced_half_edge"]
    assert sorted(forced_b) == ([11] if branch == "I" else [9, 15, 16])
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    assert weights == expected_weights and Counter(weights) == Counter(range(1, m+1))
    assert checker["valid"] and checker["edge_differences"] == weights
    traversal = traverse(neighbors, ["s:0"])
    signed = []
    for u, v in edges:
        assert (traversal[u]-traversal[v]) % 2 == 1
        tail, head = (v, u) if traversal[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "difference": labels[head]-labels[tail]})
    assert [row for row in signed if row["difference"] < 0] == [
        {"edge": [v, low], "difference": d} for v, d in zip(ordered[low], negatives, strict=True)]
    assert sum(row["difference"] for row in signed) == signed_sum
    assert pins["valid"] and pins["actual"] == {"s:0": 0, "s:1": m, right: 1}
    assert growth["valid"] and neighbors["s:1"] == {"s:0", right} and path_distance[right] == 1
    return {"graph_digest": digest, "ledger_id": ledger, "core_edges": core_edges, "core_differences": fixed,
            "residual_labels": sorted(unused_labels), "residual_differences": sorted(unused_weights),
            "r226": {"A": local_a, "B": local_b}, "absolute_differences": weights, "signed_incidences": signed,
            "degree_parity_quantity": parity, "signed_sum": signed_sum, "original_terminal_slots": ordered,
            "counted_original_vertices": len(roles), "unused_labels": [], "unused_differences": []}


def obstruction(original, core):
    profile = [[6, 3, 4], [2]]
    edges, roles, neighbors, _, digest = reconstruct(original, profile)
    m = len(edges)
    h, low, third = "b:0:0", "b:0:1", "b:0:2"
    q, a, c = profile[0]
    core_edges, fixed, labels, weights, parity = core_audit(core, edges, neighbors, m, q, a, c)
    assert m == 20 and labels == weights == set(range(3, 14))
    assert parity == 180
    inverse = {abs(core[h]-x): x for x in labels}
    assert set(inverse) == weights and len(inverse) == len(labels)
    t = (m-2)//2
    options = {}
    preimages = {y: [] for y in labels}
    for x in sorted(labels):
        images = {host: inverse.get(abs(core[host]-x)) for host in (h, low, third)}
        arithmetic = {h: x, low: 2*t-x, third: x+2}
        assert all(images[host] == (y if y in labels else None) and (y-x) % 2 == 0
                   for host, y in arithmetic.items())
        options[x] = images
        for host, y in images.items():
            if y is not None:
                preimages[y].append({"label": x, "host": host})
    assert preimages[3] == [{"label": 3, "host": h}] and preimages[4] == [{"label": 4, "host": h}]
    capacities = {p: sorted(x for x in labels-{3, 4} if x % 2 == n) for n, p in enumerate(("even", "odd"))}
    assert capacities == {"even": [6, 8, 10, 12], "odd": [5, 7, 9, 11, 13]}
    vacant_by_host = {host: sorted(neighbors[host]-set(core)) for host in (h, low, third)}
    demand = len(vacant_by_host[low])+len(vacant_by_host[third])
    assert (len(vacant_by_host[h]), len(vacant_by_host[low]), len(vacant_by_host[third])) == (5, 2, 4)
    assert a == 3 and c >= q-2 and c % 2 == 0
    assert demand == 6 and max(map(len, capacities.values())) == 5
    return {"status": "FIXED_CORE_INFEASIBLE", "scope": "all_completions_of_the_specified_labeled_core",
            "graph_digest": digest, "core": core, "core_edges": core_edges, "core_differences": fixed,
            "degree_parity_quantity": parity, "vertices": len(roles), "edges": m,
            "residual_labels": sorted(labels), "residual_differences": sorted(weights), "t": t,
            "single_label_eligible_images": options, "forced_image_preimages": {n: preimages[n] for n in (3, 4)},
            "vacant_by_host": vacant_by_host, "available_parity_classes": capacities, "same_class_demand": demand,
            "parity_sum_identity": "N_C,p = sum of x-t for L labels of parity p",
            "split_class_obstruction": "Two L labels of opposite parity would force odd c",
            "same_class_obstruction": "All C labels share the L parity and exceed maximum capacity", "certificates": 0}


def controls(original, core, batches, labels, reports):
    edges = original["graph"]["edges"]
    wrong = reports["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["edge_differences"] == [abs(labels[u]-labels[v]) for u, v in edges]
    h, low, third = "b:0:0", "b:0:1", "b:0:2"
    midpoint_reports = {}
    for key, batch_key, source, destination, midpoint, weight, before, after in (
        ("A_midpoint_move", "A", h, low, 8, 6, {low: 0, h: 5}, {low: 1, h: 4}),
        ("B_midpoint_move", "B", low, third, 7, 5, {low: 2, third: 2}, {low: 1, third: 3}),
    ):
        archived = batches[batch_key]
        moved, check = reports[key]["batch"], reports[key]["local"]
        assert all(moved[k] == archived[k] for k in ("labels", "differences", "slots"))
        assert 2*midpoint == core[source]+core[destination]
        assert abs(core[source]-midpoint) == abs(core[destination]-midpoint) == weight
        assert moved["allocation"] == {
            source: [x for x in archived["allocation"][source] if x != midpoint],
            destination: [*archived["allocation"][destination], midpoint]}
        assert Counter(x for xs in moved["allocation"].values() for x in xs) == Counter(archived["labels"])
        assert Counter(abs(core[host]-x) for host, xs in moved["allocation"].items() for x in xs) == Counter(archived["differences"])
        assert check["expected_quotas"] == before and check["actual_quotas"] == after and not check["valid"]
        assert check["tests"] == {"labels_exact": True, "differences_exact": True,
                                  "eligible": True, "quotas_exact": False}
        midpoint_reports[batch_key] = {"label": midpoint, "weight": weight, "hosts": [source, destination],
                                       "original_quotas": before, "mutated_quotas": after}
    overlap = reports["global_overlap"]
    ol_a, ol_b = overlap["batches"]["A"], overlap["batches"]["B"]
    assert ol_a["slots"] == batches["A"]["slots"] and ol_b == batches["B"]
    assert ol_a["labels"] == [3, 4, 5, 8, 11] and ol_a["differences"] == [3, 6, 9, 10, 11]
    assert ol_a["allocation"] == {low: [], h: ol_a["labels"]}
    a_check = r226(core, low, h, ol_a, overlap["local"]["A"])
    b_check = r226(core, low, third, ol_b, overlap["local"]["B"])
    label_counts = Counter(ol_a["labels"]+ol_b["labels"])
    weight_counts = Counter(ol_a["differences"]+ol_b["differences"])
    repeated_labels = {x: n for x, n in label_counts.items() if n > 1}
    repeated_weights = {x: n for x, n in weight_counts.items() if n > 1}
    missing_labels = sorted(set(range(3, 12))-label_counts.keys())
    missing_weights = sorted(set(range(3, 12))-weight_counts.keys())
    conflict = overlap["global"]
    assert repeated_labels == conflict["repeated_labels"] == {5: 2, 11: 2}
    assert repeated_weights == conflict["repeated_differences"] == {3: 2, 9: 2}
    assert missing_labels == conflict["missing_labels"] == [6, 10]
    assert missing_weights == conflict["missing_differences"] == [4, 8]
    assert not conflict["valid"] and conflict["tests"]["slots_exact"]
    return {"midpoint_moves": midpoint_reports, "overlap_A": a_check, "overlap_B": b_check,
            "overlap_repeated_labels": repeated_labels, "overlap_repeated_differences": repeated_weights,
            "overlap_missing_labels": missing_labels, "overlap_missing_differences": missing_weights}
