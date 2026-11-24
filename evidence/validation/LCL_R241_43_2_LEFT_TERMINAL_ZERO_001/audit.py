"""Independent named-incidence audit for the frozen D104 original."""

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


def role_domain(reductions, left, quotas, excess, high_labels, constant, low_max):
    maximum = max(high_labels)
    keys = {(row["max_center"], row["C"], row["Y"]) for row in reductions}
    assert len(keys) == len(reductions) == 24
    assert all(center in left and c != y and {c,y} <= high_labels-{maximum} for center,c,y in keys)
    assert all(sum(key[0] == center for key in keys) == 12 for center in left)
    survivor_by_key = {}
    scalar_checks = 0
    for row in reductions:
        center, c, y = row["max_center"], row["C"], row["Y"]
        other = next(v for v in left if v != center)
        quota = quotas[center]
        twice_sum = excess[center]*maximum + excess[other]*c + excess["s:1"]*y - constant
        assert row["quota"] == quota and row["twice_x_plus_z"] == twice_sum
        xs = list(range(1, quota+1))
        assert [check["x"] for check in row["checks"]] == xs
        total, odd = divmod(twice_sum, 2)
        first = max(1, total-low_max)
        last = min(quota, (total-1)//2)
        for check in row["checks"]:
            scalar_checks += 1
            x = check["x"]
            assert check["twice_z"] == twice_sum-2*x
            if odd:
                assert check["verdict"] == "odd" and "z" not in check
            elif first <= x <= last:
                z = total-x
                assert check["verdict"] == "survives" and check["z"] == z
                survivor_by_key[center,c,y,x] = z
            else:
                assert check["verdict"] == "out_of_range" and "z" not in check
    assert scalar_checks == 84 and len(survivor_by_key) == 19
    return survivor_by_key


def obstruction(original, digest, reductions, cases):
    edges, neighbors, low, high = topology(original, digest)
    entry, exit_name = original["graph"]["spine"]
    left, right = ["b:0:0", "b:0:1"], "b:1:0"
    roles = original["graph"]["roles"]
    fixed = [[entry, exit_name], [entry, left[0]], [entry, left[1]], [exit_name, right]]
    terminals = {center: sorted(v for v in neighbors[center] if roles[v]["kind"] == "leaf")
                 for center in [*left, right]}
    terminal_pairs = {center: [[center, vertex] for vertex in group] for center,group in terminals.items()}
    incidences = fixed + [edge for group in terminal_pairs.values() for edge in group]
    assert Counter(tuple(sorted(pair)) for pair in incidences) == edges
    assert all(neighbors[v] == {center} for center,group in terminals.items() for v in group)
    assert all(neighbors[center] == set(terminals[center]) | {entry} for center in left)
    assert set(terminals[right]) == high - {exit_name, *left}
    assert {v for center in left for v in terminals[center]} == low - {entry, right}
    quotas = {center:len(terminals[center]) for center in left}
    assert list(quotas.values()) == [4, 3] and len(terminals[right]) == 2
    maximum, cut = len(edges), len(low)
    assert (maximum, cut) == (13, 9)
    # The alphabet makes (13,0) the only maximum-difference pair.
    # For 13-j and a high endpoint h<13, the low endpoint h-13+j is <j.
    # The original degree-one incidences bind such previously forced low labels to 13.
    # Every j<x then uses a terminal position at 13, so x is bounded by its quota.
    signed = Counter()
    for u, v in edges:
        lo, hi = (u,v) if u in low else (v,u)
        signed[hi] += 1
        signed[lo] -= 1
    excess = {v: signed[v] - (1 if v in high else -1) for v in signed}
    corrections = {v:coefficient for v,coefficient in excess.items() if coefficient}
    assert corrections == {entry:-2, exit_name:1, left[0]:4, left[1]:3, right:-2}
    low_labels, high_labels = set(range(cut)), set(range(cut, maximum+1))
    spectrum = set(range(1, maximum+1))
    baseline, required_sum = sum(high_labels)-sum(low_labels), sum(spectrum)
    assert (baseline, required_sum) == (19, 91)
    survivors = role_domain(reductions, left, quotas, excess, high_labels, required_sum-baseline, cut-1)
    assert len(cases) == len(survivors)
    assert {(row["max_center"],row["C"],row["Y"],row["x"]):row["z"] for row in cases} == survivors
    audited = []
    for row in cases:
        center, c, y, x, z = (row[k] for k in ("max_center","C","Y","x","z"))
        other = next(v for v in left if v != center)
        labels = {center:maximum, other:c, entry:x, exit_name:y, right:z}
        assert (row["A"],row["B"]) == tuple(labels[v] for v in left)
        right_palette = sorted(high_labels - {maximum,c,y})
        forced_labels = sorted(label for label in low_labels if label < x)
        remaining = sorted(low_labels - set(forced_labels) - {x,z})
        residual_counts = {center:quotas[center]-len(forced_labels), other:quotas[other]}
        assert residual_counts[center] >= 0 and len(remaining) == sum(residual_counts.values()) == 7-x
        assert row["right_palette"] == right_palette and len(right_palette) == len(terminals[right])
        assert row["forced_max_terminal_palette"] == forced_labels and row["residual_low_palette"] == remaining
        fixed_weights = [abs(labels[u]-labels[v]) for u,v in fixed] + [w-z for w in right_palette]
        forced_weights = [maximum-j for j in forced_labels]
        assert row["six_fixed_weights"] == fixed_weights and row["forced_max_terminal_weights"] == forced_weights
        weights = Counter(fixed_weights) + Counter(forced_weights)
        assert weights.total() + sum(residual_counts.values()) == len(incidences)
        assert row["W_multiplicities"] == {str(w):n for w,n in weights.items()}
        assert row["W_repeats"] == {str(w):n for w,n in weights.items() if n > 1}
        possible = {v: {labels[v]-low_value for low_value in remaining} for v in left}
        absent = sorted(spectrum - set(weights) - possible[center] - possible[other])
        w = row["missing_weight"]
        endpoints = [maximum-w,c-w]
        assert w in absent and all(v not in remaining for v in endpoints)
        assert row["candidate_low_endpoints_at_max_and_other"] == endpoints
        audited.append({"case_key":[center,c,y,x], "z":z,
                        "fixed_edge_weights":[[pair,weight] for pair,weight in zip(fixed,fixed_weights[:4],strict=True)],
                        "right_terminal_weights_by_label":[[v,v-z] for v in right_palette],
                        "forced_max_terminal_weights_by_label":[[v,maximum-v] for v in forced_labels],
                        "residual_edge_counts_by_center":residual_counts,
                        "necessarily_missing_weights_from_palette_envelope":absent,
                        "missing_witness":w, "unavailable_endpoint_labels":endpoints})
    return {"status":"PASS","graph_digest":digest,"physical_spine":[entry,exit_name],
            "low_vertices":sorted(low),"high_vertices":sorted(high),"degrees":{v:abs(signed[v]) for v in signed},
            "fixed_named_edges":fixed,"terminal_edge_groups":terminal_pairs,"max_difference_pair":[maximum,0],
            "degree_one_contribution":baseline,"required_sum":required_sum,"signed_excess":corrections,
            "induction":{"low_endpoint_if_h_below_max":"h-13+j < j",
                         "available_forced_incidences":"terminals at the left center labeled 13",
                         "entrance_range_by_quota":quotas,"right_center_bound":"x < z <= 8"},
            "role_pairs_audited":len(reductions),"scalar_checks_audited":sum(len(r["checks"]) for r in reductions),
            "case_audits":audited}


def alpha_scope(original, original_sha256, arithmetic, earlier):
    digest = original["graph_digest"]
    low, high = arithmetic["low_vertices"], arithmetic["high_vertices"]
    right_domain = {"cut":9,"free_spine_ports":True,"host":"b:1:0","host_label":0}
    entrance_domain = {"cut":9,"entrance":"s:0","entrance_label":0,"free_exit":True}
    prior_zero_vertices = {}
    for key, domain in (("D102",right_domain),("D103",entrance_domain)):
        record = earlier[key]
        assert record["status"] == "PASS" and record["proof_disposition"] == "ACCEPT"
        assert record["state_disposition"] == "REJECT" and record["domain"] == domain
        assert record["target_graph_digest"] == digest and record["target_original_sha256"] == original_sha256
        assert record["arithmetic_audit"]["low_vertices"] == low and record["arithmetic_audit"]["high_vertices"] == high
        prior_zero_vertices[key] = domain.get("host") or domain["entrance"]
    left_terminals = sorted(v for center in ("b:0:0","b:0:1")
                            for _,v in arithmetic["terminal_edge_groups"][center])
    assert len(left_terminals) == 7 and set(left_terminals).isdisjoint(prior_zero_vertices.values())
    assert sorted([*left_terminals,*prior_zero_vertices.values()]) == low
    assert (len(low),len(high)) == (9,5)
    maximum = len(original["graph"]["edges"])
    assert {maximum-v for v in range(5,14)} == set(range(9))
    assert {maximum-v for v in range(5)} == set(range(9,14))
    return {"status":"PASS","graph_digest":digest,"original_sha256":original_sha256,
            "zero_hosts_excluded":prior_zero_vertices | {"D104":left_terminals},
            "cut_9":"EXCLUDED","cut_5":"EXCLUDED_BY_COMPLEMENT","complement":"13-f(v)",
            "alpha_labeling":"EXCLUDED","ordinary_gracefulness":"UNDECIDED","additional_cut_tests":0}


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
    false_terminal = adverse["false_zero_terminal"]
    terminal = "l:0:0:0"
    assert false_terminal["vertex"] == terminal and false_terminal["declared"] == 0
    assert graph["roles"][terminal] == {"kind":"leaf","section":0,"branch":0,"leaf":0}
    assert {v for edge in graph["edges"] if terminal in edge for v in edge if v != terminal} == {"b:0:0"}
    assert false_terminal["actual"] == labels[terminal] == 4 and false_terminal["valid"] is False
    assert false_terminal["error"] == "The physical left terminal does not carry zero"
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
