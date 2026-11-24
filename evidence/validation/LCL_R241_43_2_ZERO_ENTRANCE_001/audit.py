"""Independent named-incidence audit for the frozen D103 original."""

from collections import Counter, deque
from hashlib import sha256
import json


def topology(original, expected_digest):
    graph = original["graph"]
    profile = [[4, 3], [2]]
    spine = ["s:0", "s:1"]
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    expected = Counter([tuple(spine)])
    for section, quotas in enumerate(profile):
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            expected[tuple(sorted((spine[section], center)))] += 1
            for leaf in range(quota):
                terminal = f"l:{section}:{branch}:{leaf}"
                roles[terminal] = {"kind": "leaf", "section": section, "branch": branch, "leaf": leaf}
                expected[tuple(sorted((center, terminal)))] += 1
    edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    assert edges == expected and len(edges) == sum(edges.values()) == 13
    assert sorted(graph["vertices"]) == sorted(roles) and len(roles) == 14
    assert graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
    payload = {"vertices": sorted(roles), "edges": sorted(edges.elements()),
               "profile": profile, "spine": spine, "roles": roles}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    digest = sha256(raw).hexdigest()
    assert digest == original["graph_digest"] == expected_digest

    neighbors = {v: set() for v in roles}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    color = {"s:0": 0}
    pending = deque(color)
    while pending:
        u = pending.popleft()
        for v in neighbors[u]:
            if v not in color:
                color[v] = 1 - color[u]
                pending.append(v)
            assert color[u] != color[v]
    low = {v for v, side in color.items() if side == 0}
    high = set(color) - low
    assert low == {"s:0", "b:1:0"} | {v for v in roles if v.startswith("l:0:")}
    assert high == {"s:1", "b:0:0", "b:0:1", "l:1:0:0", "l:1:0:1"}
    assert low | high == set(roles) and (len(low), len(high)) == (9, 5)
    return edges, neighbors, low, high


def obstruction(original, digest, reductions, cases):
    edges, neighbors, low, high = topology(original, digest)
    entry, exit_name = original["graph"]["spine"]
    left_a, left_b, right = "b:0:0", "b:0:1", "b:1:0"
    roles = original["graph"]["roles"]
    maxima = [left_a, left_b, exit_name]
    assert set(maxima) == neighbors[entry] and neighbors[entry] <= high
    maximum, cut = len(edges), len(low)
    assert (maximum, cut) == (13, 9)

    # Bind the four individually named fixed edges, then recover both terminal edge groups.
    fixed_pairs = [[entry, exit_name], [entry, left_a], [entry, left_b], [exit_name, right]]
    terminal_groups = {}
    for center in (left_a, left_b, right):
        terminals = sorted(v for v in neighbors[center] if roles[v]["kind"] == "leaf")
        assert all(neighbors[v] == {center} for v in terminals)
        terminal_groups[center] = [[center, terminal] for terminal in terminals]
    listed = fixed_pairs + [edge for group in terminal_groups.values() for edge in group]
    assert Counter(tuple(sorted(edge)) for edge in listed) == edges
    assert [len(terminal_groups[v]) for v in (left_a, left_b, right)] == [4, 3, 2]
    right_names = {v for _, v in terminal_groups[right]}
    left_names = {v for center in (left_a, left_b) for _, v in terminal_groups[center]}
    assert right_names == high - set(maxima)
    assert left_names == low - {entry, right}

    # Derive the signed coefficients from high-low incidence counts.
    signed = Counter()
    for u, v in edges:
        lo, hi = (u, v) if u in low else (v, u)
        signed[hi] += 1
        signed[lo] -= 1
    degrees = {v: abs(signed[v]) for v in low | high}
    excess = {v: signed[v] - (1 if v in high else -1) for v in signed}
    corrections = {v: coefficient for v, coefficient in excess.items() if coefficient}
    assert corrections == {entry: -2, exit_name: 1, left_a: 4, left_b: 3, right: -2}
    alphabet = set(range(maximum+1))
    low_labels = set(range(cut))
    high_labels = alphabet-low_labels
    baseline = sum(high_labels)-sum(low_labels)
    spectrum = alphabet-{0}
    needed = sum(spectrum)
    assert (baseline, needed) == (19, 91)
    assert set(signed) == low | high

    # A valid triple is unique and has a unique maximum position.
    # There are exactly 4*3 distinct possible pairs for the other two slots.
    triples = {tuple(row["triple"]) for row in reductions}
    assert len(triples) == len(reductions) == 36
    assert all(len(t) == len(set(t)) == 3 and set(t) <= high_labels and maximum in t for t in triples)
    slot_counts = [sum(triple[i] == maximum for triple in triples) for i in range(3)]
    assert slot_counts == [12, 12, 12]
    independently_surviving = {}
    for row in reductions:
        triple = tuple(row["triple"])
        twice_z = baseline-needed + sum(excess[v]*label for v, label in zip(maxima, triple, strict=True))
        assert row["twice_z"] == twice_z and excess[right] == -2
        if twice_z % 2:
            assert row["verdict"] == "odd" and "z" not in row
        elif twice_z < 2 or twice_z > 2*(cut-1):
            assert row["verdict"] == "out_of_range" and "z" not in row
        else:
            z = twice_z//2
            assert row["verdict"] == "survives" and row["z"] == z
            independently_surviving[triple] = z
    assert len(cases) == len(independently_surviving) == 7
    assert {tuple(case["triple"]): case["z"] for case in cases} == independently_surviving

    inspected = []
    for case in cases:
        a, b, y = case["triple"]
        z = case["z"]
        by_name = dict(zip(maxima, (a, b, y), strict=True)) | {entry: 0, right: z}
        right_palette = sorted(high_labels - {a, b, y})
        left_palette = sorted(low_labels - {0, z})
        assert case["right_palette"] == right_palette and case["left_palette"] == left_palette
        fixed_by_edge = [(pair, abs(by_name[pair[0]]-by_name[pair[1]])) for pair in fixed_pairs]
        weights = [w for _, w in fixed_by_edge] + [label-by_name[right] for label in right_palette]
        repeat_counts = {str(w): n for w, n in Counter(weights).items() if n > 1}
        assert weights == case["fixed_weights"] and repeat_counts == case["fixed_repeat_multiplicities"]
        possible = {center: sorted(by_name[center]-label for label in left_palette)
                    for center in (left_a, left_b)}
        missing = sorted(spectrum - set(weights) - set(possible[left_a]) - set(possible[left_b]))
        witness = case["witness"]
        w = witness["weight"]
        if witness["kind"] == "missing_weight":
            assert w in missing
            assert witness["required_left_terminal_labels"] == [by_name[left_a]-w, by_name[left_b]-w]
        else:
            assert witness["kind"] == "repeated_weight" and repeat_counts[str(w)] >= 2
            witnesses = witness["edges"]
            assert len(witnesses) == 2 and len({tuple(sorted(pair)) for pair in witnesses}) == 2
            assert witnesses == [[entry, left_b], [exit_name, right]]
            assert all((pair, w) in fixed_by_edge for pair in witnesses)
        inspected.append({"triple": case["triple"], "z": z, "fixed_named_incidence_weights": fixed_by_edge,
                          "right_terminal_label_weights": [[label, label-z] for label in right_palette],
                          "possible_left_weights_by_center": possible, "necessarily_missing_weights": missing,
                          "fixed_repeat_multiplicities": repeat_counts, "verified_witness": witness})
    return {"status": "PASS", "graph_digest": digest, "fixed_named_edges": fixed_pairs,
            "terminal_edge_groups": terminal_groups, "low_vertices": sorted(low), "high_vertices": sorted(high),
            "degrees": degrees, "physical_spine": [entry, exit_name], "max_weight_pair": [maximum, 0],
            "possible_maximum_label_vertices": sorted(neighbors[entry]), "signed_excess": corrections,
            "degree_one_contribution": baseline, "required_sum": needed,
            "triple_slot_order": maxima, "triple_counts_by_max_position": slot_counts,
            "scalar_triples_audited": len(reductions), "surviving_case_audits": inspected}


def controls(original, cert, positive, adverse):
    graph = original["graph"]
    labels = cert["labels"]
    differences = [abs(labels[u]-labels[v]) for u, v in graph["edges"]]
    payload = {"graph_digest": original["graph_digest"], "labels": sorted(labels.items())}
    ledger = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert ledger == cert["ledger_id"] == positive["ledger_id"]
    assert set(labels) == set(graph["vertices"]) and sorted(labels.values()) == list(range(13))
    assert sorted(differences) == list(range(1, 13)) and differences == positive["checker"]["edge_differences"]
    assert all((labels[u] < 8) != (labels[v] < 8) for u, v in graph["edges"])
    assert cert["cut"] == 8 and cert["offsets"] == [labels["s:0"], labels["s:1"]-8] == [3, 4]
    host = "b:1:0"
    assert labels[host] == 0 and set(v for edge in graph["edges"] if host in edge for v in edge if v != host) == {
        "s:1", "l:1:0:0", "l:1:0:1"}
    wrong = adverse["wrong_digest"]
    assert not wrong["checker"]["valid"] and wrong["expected"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    false_entrance = adverse["false_zero_entrance"]
    assert graph["spine"][0] == "s:0" and false_entrance["vertex"] == graph["spine"][0]
    assert false_entrance["declared"] == 0 and false_entrance["actual"] == labels["s:0"] == 3
    assert false_entrance["valid"] is False and false_entrance["error"] == "The physical entrance does not carry zero"
    swap = adverse["terminal_swap"]
    u, v = "l:0:0:0", "l:0:1:0"
    assert swap["vertices"] == [u, v]
    changed = labels | {u: labels[v], v: labels[u]}
    assert swap["labels"] == changed and sorted(changed.values()) == list(range(13))
    modified = [abs(changed[i]-changed[j]) for i, j in graph["edges"]]
    repeats = {str(w): n for w, n in Counter(modified).items() if n > 1}
    missing = sorted(set(range(1, 13))-set(modified))
    assert repeats == {"5": 2, "7": 2} and missing == [4, 8]
    assert not swap["checker"]["valid"] and swap["checker"]["edge_differences"] == modified
    assert swap["checker"]["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"status": "PASS", "d098_ledger_id": ledger, "swap_repeat_multiplicities": repeats,
            "swap_missing_weights": missing, "swap_original_edge_differences": modified}
