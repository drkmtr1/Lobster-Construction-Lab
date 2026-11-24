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
    profile = [[5, 3, 4], [2]]
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


def retained(original, cert, binding, core, batches, labels, local, checker, pins, growth):
    edges, roles, neighbors, distance, digest = reconstruct(original)
    graph = original["graph"]
    assert set(labels) == set(roles) and all(type(x) is int for x in labels.values())
    assert labels == cert["labels"] and sorted(labels.values()) == list(range(20))
    assert digest == cert["graph_digest"]
    assert hash_canonical({"graph_digest": digest, "labels": sorted(labels.items())}) == cert["ledger_id"]
    actual = [abs(labels[u]-labels[v]) for u, v in edges]
    assert sorted(actual) == list(range(1, 20)) and actual == checker["edge_differences"] and checker["valid"]
    h, low, c, right = "b:0:0", "b:0:1", "b:0:2", "b:1:0"
    ordered = {host: sorted(neighbors[host]-set(graph["spine"]), key=lambda v: roles[v]["leaf"])
               for host in (h, low, c, right)}
    quotas = {host: len(xs) for host, xs in ordered.items()}
    assert quotas == {h: 5, low: 3, c: 4, right: 2}
    assert binding["indices"] == binding["inverse"] == [0, 1, 2] and binding["valid"]
    assert binding["quota_compatible"] and binding["slots_exact"] and binding["bijective"]
    for role, host in zip("HLC", (h, low, c), strict=True):
        row = binding["rows"][role]
        assert row["center"] == host and row["actual"] == row["requested"] == ordered[host]
        assert not row["absent_from_original"] and not row["omitted_actual"]
    assert [labels[v] for v in ordered[h]] == [14, 3, 4, 6, 11]
    assert [labels[v] for v in ordered[low]] == [16, 9, 12]
    assert [labels[v] for v in ordered[c]] == [5, 7, 8, 10]
    assert [labels[v] for v in ordered[right]] == [18, 17]
    expected_core_names = {"s:0", "s:1", h, low, c, right, ordered[h][0], ordered[low][0], *ordered[right]}
    assert core == {v: labels[v] for v in expected_core_names}
    fixed = [abs(labels[u]-labels[v]) for u, v in edges if u in core and v in core]
    assert sorted(fixed) == [1, 2, *range(13, 20)]
    unused_labels = set(range(20))-set(core.values())
    unused_weights = set(range(1, 20))-set(fixed)
    assert unused_labels == unused_weights == set(range(3, 13))
    a, b = batches["A"], batches["B"]
    assert a["slots"] == {low: ordered[low][3:], h: ordered[h][1:]}
    assert b["slots"] == {low: ordered[low][1:3], c: ordered[c]}
    vacant = [(host, leaf) for batch in (a, b) for host, xs in batch["slots"].items() for leaf in xs]
    assert {v for _, v in vacant} == set(labels)-set(core) and len(vacant) == len(unused_labels)
    assert all(neighbors[leaf] == {host} for host, leaf in vacant)
    assert set(a["slots"]) & set(b["slots"]) == {low}
    for batch in (a, b):
        assert batch["allocation"] == {host: [labels[leaf] for leaf in xs] for host, xs in batch["slots"].items()}
    assert Counter(a["labels"]+b["labels"]) == Counter(unused_labels)
    assert Counter(a["differences"]+b["differences"]) == Counter(unused_weights)
    a_report = r226(core, low, h, a, local["A"])
    b_report = r226(core, low, c, b, local["B"])
    assert a_report["integral_projection"] == [0, 2]
    assert b_report["integral_projection"] == [2, 4, 6]
    assert a_report["chosen_quotas"] == {low: 0, h: 4} and b_report["chosen_quotas"] == {low: 2, c: 4}
    depth = traverse(neighbors, ["s:0"])
    signed = []
    for u, v in edges:
        assert (depth[u]-depth[v]) % 2
        tail, head = (v, u) if depth[u] % 2 else (u, v)
        signed.append({"edge": [tail, head], "difference": labels[head]-labels[tail]})
    assert [row["edge"] for row in signed if row["difference"] < 0] == [[v, low] for v in ordered[low]]
    assert sum(row["difference"] for row in signed) == 128
    assert pins["valid"] and pins["actual"] == {"s:0": 0, "s:1": 19, right: 1}
    assert growth["valid"] and graph["spine"] == ["s:0", "s:1"] and distance[right] == 1
    assert neighbors["s:1"] == {"s:0", right}
    return {"role_map": binding["indices"], "inverse": binding["inverse"], "physical_quotas": quotas,
            "checked_names": sorted(labels), "graph_digest": digest, "ledger_id": cert["ledger_id"],
            "checked_original_edges": edges, "absolute_differences": actual, "signed_incidences": signed,
            "r226": {"A": a_report, "B": b_report}, "unused_labels": [], "unused_differences": [],
            "scope": "identity_order_only"}


def controls(original, cert, formula, reports):
    graph = original["graph"]
    edges = graph["edges"]
    labels = cert["labels"]
    spectrum = [abs(labels[u]-labels[v]) for u, v in edges]
    wrong = reports["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["edge_differences"] == spectrum
    invalid = reports["nonbijective"]
    assert invalid["indices"] == [0, 0, 2] and not invalid["bijective"] and not invalid["valid"]
    assert invalid["repeated_indices"] == [0] and invalid["omitted_indices"] == [1]
    assert invalid["quota_compatible"] is None and invalid["slots_exact"] is None and "rows" not in invalid
    bad = reports["quota_incompatible"]
    assert bad["indices"] == [2, 1, 0] and bad["inverse"] == [2, 1, 0] and bad["bijective"]
    assert bad["requested_quotas"] == [5, 3, 4] and bad["actual_quotas"] == [4, 3, 5]
    assert not bad["quota_compatible"] and not bad["slots_exact"] and not bad["valid"]
    rows = bad["rows"]
    expected = {"H": (2, 5), "L": (1, 3), "C": (0, 4)}
    for role, (index, quota) in expected.items():
        host = f"b:0:{index}"
        actual = {leaf for leaf, attrs in graph["roles"].items()
                  if attrs["kind"] == "leaf" and attrs["section"] == 0 and attrs["branch"] == index}
        assert all([host, leaf] in edges for leaf in actual)
        required = {f"l:0:{index}:{k}" for k in range(quota)}
        assert rows[role]["center"] == host and rows[role]["actual"] == sorted(actual)
        assert rows[role]["requested"] == sorted(required)
        assert rows[role]["absent_from_original"] == sorted(required-actual)
        assert rows[role]["omitted_actual"] == sorted(actual-required)
    assert rows["H"]["absent_from_original"] == ["l:0:2:4"] and rows["C"]["omitted_actual"] == ["l:0:0:4"]
    u, v = "l:0:0:1", "l:0:0:2"
    swapped = labels | {u: labels[v], v: labels[u]}
    observed = [abs(swapped[x]-swapped[y]) for x, y in edges]
    changes = [[edge, old, new] for edge, old, new in zip(edges, spectrum, observed, strict=True) if old != new]
    assert changes == [[["b:0:0", u], 12, 11], [["b:0:0", v], 11, 12]]
    assert Counter(observed) == Counter(spectrum)
    good = reports["within_host"]
    assert good["checker"]["valid"] and good["checker"]["edge_differences"] == observed
    expected_pins = {"s:0": 0, "s:1": 19, "b:1:0": 1}
    assert {v: swapped[v] for v in expected_pins} == expected_pins
    assert good["pins"]["valid"] and good["pins"]["actual"] == expected_pins
    assert good["growth"]["valid"] and set(good["growth"]["actual_exit_neighbors"]) == {"s:0", "b:1:0"}
    assert graph["spine"] == ["s:0", "s:1"] and good["vertices"] == [u, v]
    mismatches = sorted(name for name in formula if formula[name] != swapped[name])
    assert mismatches == [u, v] == good["mismatches"] and not good["pointwise_agreement"]
    return {"binding_only_slot_witnesses": {"absent": rows["H"]["absent_from_original"],
                                           "omitted": rows["C"]["omitted_actual"]},
            "within_host_changed_weights": changes, "within_host_spectrum_preserved": True,
            "within_host_mismatches": mismatches}
