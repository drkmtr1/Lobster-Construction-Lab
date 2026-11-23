"""Independent arithmetic and original-bound audit. Uses the standard library only."""

from collections import Counter, deque
from hashlib import sha256
import json


def load(path):
    return json.loads(path.read_bytes())


def digest(obj):
    return sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def inspect(record, profile):
    graph = record["graph"]
    sections = [f"s:{i}" for i in range(len(profile))]
    parents = dict(zip(sections[1:], sections[:-1], strict=True))
    roles = {}
    for i, quotas in enumerate(profile):
        s = sections[i]
        roles[s] = {"kind": "spine", "section": i}
        for j, quota in enumerate(quotas):
            b = f"b:{i}:{j}"
            parents[b] = s
            roles[b] = {"kind": "branch", "section": i, "branch": j}
            for k in range(quota):
                leaf = f"l:{i}:{j}:{k}"
                parents[leaf] = b
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
    edges = [[p, child] for child, p in parents.items()]
    assert Counter(tuple(sorted(e)) for e in edges) == Counter(tuple(sorted(e)) for e in graph["edges"])
    assert len(roles) == len(edges)+1
    assert graph == {"schema_version": 1, "vertices": list(roles), "edges": edges,
                     "spine": sections, "roles": roles, "profile": profile}
    assert record["graph_digest"] == digest({"vertices": sorted(roles), "edges": sorted(sorted(e) for e in edges),
                                            "roles": roles, "spine": sections, "profile": profile})
    adjacency = {v: [] for v in roles}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    side = {sections[0]: 0}
    queue = deque(side)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in side:
                side[v] = 1-side[u]
                queue.append(v)
            assert side[u] != side[v]
    assert side.keys() == roles.keys()
    for v, role in roles.items():
        u, distance = v, 0
        while u in parents and u not in sections:
            u, distance = parents[u], distance+1
        assert u == sections[role["section"]]
        assert distance == {"spine": 0, "branch": 1, "leaf": 2}[role["kind"]]
    return side, {v: len(adjacency[v]) for v in side}, edges, roles


def match_prior_manifest(root, cfg, folder, names):
    manifest_path = f"{folder}/MANIFEST.json"
    entries = {row["path"]: row for row in load(root / manifest_path)["files"]}
    for name in names:
        relative = f"{folder}/{name}"
        assert sha256((root / relative).read_bytes()).hexdigest() == entries[name]["sha256"] == cfg["source_hashes"][relative]
        assert (root / relative).stat().st_size == entries[name]["bytes"]


def signed_degree(side, degrees, cuts, physical):
    lows, highs = cuts
    s0, s1 = physical
    assert degrees == {v: {"s:0": 2, "s:1": 2, "b:0:0": 5, "b:1:0": 4}.get(v, 1) for v in side}
    excess = {v: (d-1)*(2*side[v]-1) for v, d in degrees.items() if d > 1}
    assert excess == {"s:0": -1, "s:1": 1, "b:0:0": 4, "b:1:0": -3}
    low_sum, high_sum = sum(lows), sum(highs)
    ports = excess["s:0"]*s0 + excess["s:1"]*s1
    base = high_sum-low_sum+ports
    required = sum(range(1, len(side)))
    assert (high_sum, low_sum, ports, base, required) == (40, 15, 4, 29, 55)
    a_coef, z_coef = excess["b:0:0"], -excess["b:1:0"]
    rhs = required-base
    assert rhs == 26
    cases = []
    low_choices = lows - {s0}
    for a in sorted(highs - {s1}):
        numerator = a_coef*a-rhs
        quotient, remainder = divmod(numerator, z_coef)
        z = quotient if remainder == 0 and quotient in low_choices else None
        cases.append({"first_center": a, "numerator_for_second_center": numerator,
                      "denominator": z_coef, "admissible_second_center": z})
    assert [(row["first_center"], row["numerator_for_second_center"]) for row in cases] == [
        (6, -2), (7, 2), (8, 6), (10, 14)]
    survivors = [(row["first_center"], row["admissible_second_center"]) for row in cases
                 if row["admissible_second_center"] is not None]
    assert survivors == [(8, 2)]
    return {"low_alphabet_sum": low_sum, "high_alphabet_sum": high_sum, "spine_excess": ports,
            "fixed_term": base, "required_sum": required, "degree_excess_coefficients": excess,
            "required_center_term": rhs, "cases": cases, "forced_centers": dict(zip(("b:0:0", "b:1:0"),
                                                                                survivors[0], strict=True))}


def incidence_audit(edges, roles, cuts, physical, signed):
    lows, highs = cuts
    s0, s1 = physical
    centers = signed["forced_centers"]
    a, z = centers["b:0:0"], centers["b:1:0"]
    left_names = sorted(v for v,r in roles.items() if r["kind"] == "leaf" and r["section"] == 0)
    right_names = sorted(v for v,r in roles.items() if r["kind"] == "leaf" and r["section"] == 1)
    adjacency = {v: [] for v in roles}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    assert all(adjacency[v] == ["b:0:0"] for v in left_names)
    assert all(adjacency[v] == ["b:1:0"] for v in right_names)
    assert ["s:0", "s:1"] in edges and ["s:0", "b:0:0"] in edges and ["s:1", "b:1:0"] in edges
    left_labels = sorted(lows - {s0, z})
    right_labels = sorted(highs - {s1, a})
    assert len(left_names) == len(left_labels) == 4 and len(right_names) == len(right_labels) == 3
    assert left_labels == [0, 1, 3, 4] and right_labels == [6, 7, 10]

    spine_weight = s1-s0
    terminal_weight = min(right_labels)-z
    assert spine_weight == terminal_weight == 4
    assert all(v not in adjacency[u] for u in left_names for v in right_names)
    assert 0 in left_labels and 10 in right_labels and max(highs)-min(lows) == 10
    groups = {"spine": [spine_weight], "left_attachment": [a-s0],
              "right_attachment": [s1-z], "left_terminal_edges": sorted(a-v for v in left_labels),
              "right_terminal_edges": sorted(v-z for v in right_labels)}
    spectrum = sorted(d for weights in groups.values() for d in weights)
    assert len(spectrum) == len(edges) and sum(spectrum) == signed["required_sum"]
    assert spectrum == [3, 4, 4, 4, 5, 5, 7, 7, 8, 8]
    repeated = {str(w): times for w, times in Counter(spectrum).items() if times > 1}
    missing = sorted(set(range(1, 11))-set(spectrum))
    return {"left_terminal_names": left_names, "right_terminal_names": right_names,
            "left_terminal_labels": left_labels, "right_terminal_labels": right_labels,
            "duplicate_four": {"spine": ["s:0", "s:1"], "right_edge_center": "b:1:0",
                               "right_edge_leaf_label": 6, "each_candidate_leaf_has_only_the_right_center": True},
            "missing_ten": {"only_label_pair": [0, 10], "left_and_right_terminals_adjacent": False},
            "difference_groups": groups, "sorted_differences": spectrum, "repeated": repeated, "missing": missing}


def audit_control(root, cfg, controls):
    folder = cfg["control_d090"]
    match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json"))
    original = load(root / folder / "original.json")
    report = load(root / folder / "result.json")
    cert = report["certificate"]
    side, _, edges, _ = inspect(original, [[2, 2], [2], [3, 2], [3]])
    labels = cert["labels"]
    assert labels.keys() == side.keys() and all(type(label) is int for label in labels.values())
    assert sorted(labels.values()) == list(range(24))
    assert cert["cut"] == 13 and all(side[v] == int(label >= 13) for v, label in labels.items())
    assert cert["witness"] == original["graph"]["spine"] == ["s:0", "s:1", "s:2", "s:3"]
    assert cert["ports"] == ["s:0", "s:3"] and cert["offsets"] == [labels["s:0"], labels["s:3"]-13] == [3, 5]
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    assert Counter(weights) == Counter(range(1, 24))
    assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
    identifier = digest({"graph_digest": original["graph_digest"], "labels": sorted(labels.items())})
    saved = controls["D090"]
    assert cert["graph_digest"] == saved["graph_digest"] == original["graph_digest"]
    assert cert["ledger_id"] == saved["ledger_id"] == identifier
    assert saved["checker"] == cert["checker"] and saved["checker"]["valid"]
    assert saved["checker"]["edge_differences"] == weights

    adverse = controls["adverse"]
    assert adverse["digest"]["expected"] == "0"*64 != original["graph_digest"]
    assert adverse["digest"]["checker"] == saved["checker"] | {
        "valid": False, "errors": ["original graph digest mismatch"]}
    assert adverse["physical_ports"] == {
        "ports": cert["ports"], "cut": 13, "declared": [3, 4], "actual": [labels["s:0"], labels["s:3"]-13],
        "valid": False, "error": "physical offset mismatch"}
    u, v = adverse["invalid_labeling"]["swap"]
    assert (u, v) == ("l:0:0:1", "l:0:1:1")
    swapped = dict(labels)
    swapped[u], swapped[v] = labels[v], labels[u]
    wrong_weights = [abs(swapped[x]-swapped[y]) for x, y in edges]
    counts = Counter(wrong_weights)
    duplicates = {str(w): c for w, c in counts.items() if c > 1}
    missing = [w for w in range(1, 24) if not counts[w]]
    assert sorted(swapped.values()) == list(range(24))
    assert adverse["invalid_labeling"]["repeated"] == duplicates == {"15": 2, "17": 2}
    assert adverse["invalid_labeling"]["missing"] == missing == [14, 18]
    rejection = adverse["invalid_labeling"]["checker"]
    assert rejection == saved["checker"] | {"valid": False, "edge_differences": wrong_weights,
                                              "errors": ["edge differences repeat", "edge differences are not exactly 1..m"]}
    return {"positive": "D090", "graph_digest": original["graph_digest"], "ledger_id": identifier,
            "adverse_rejections": 3, "swap_repeated": duplicates, "swap_missing": missing}


def prior_negative(root, cfg):
    folder = cfg["frozen_d091"]
    match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json"))
    original = load(root / folder / "original.json")
    report = load(root / folder / "result.json")
    receipt = load(root / folder / "command_receipt.json")
    assert original["graph"]["profile"] == [[4], [2]] and report["graph_digest"] == original["graph_digest"]
    assert report["disposition"] == "EXCLUDED" and receipt["status"] == report["status"] == "PASS"
    assert receipt["exit_code"] == 0 and receipt["result_sha256"] == cfg["source_hashes"][f"{folder}/result.json"]
    assert report["domain"]["profile"] == [[4], [2]] and report["domain"]["offsets"] == [5, 3]
    assert report["audit"]["weighted_degree"]["forced_first_center_rational"] == {"numerator": 13, "denominator": 2}
    return {"source": "D091", "graph_digest": original["graph_digest"], "domain": report["domain"],
            "disposition": "EXCLUDED", "replay_visits": 0}


def check(root, here, cfg, controls):
    for path, expected in cfg["source_hashes"].items():
        assert sha256((root / path).read_bytes()).hexdigest() == expected
    original = load(here / "original.json")
    side, degrees, edges, roles = inspect(original, [[4], [3]])
    assert len(side) == 11 and len(edges) == 10
    low_names = {v for v in side if not side[v]}
    high_names = set(side)-low_names
    assert low_names == {"s:0", "b:1:0", *(f"l:0:0:{j}" for j in range(4))}
    assert high_names == {"s:1", "b:0:0", *(f"l:1:0:{j}" for j in range(3))}
    domain = cfg["domain"]
    assert domain["ports"] == original["graph"]["spine"] == ["s:0", "s:1"]
    assert domain["cut"] == len(low_names) == 6
    cuts = set(range(len(low_names))), set(range(len(low_names), len(side)))
    physical = domain["port_labels"]
    assert physical == [5, 9] and physical[0] in cuts[0] and physical[1] in cuts[1]
    assert domain["offsets"] == [physical[0], physical[1]-len(low_names)] == [5, 3]
    signed = signed_degree(side, degrees, cuts, physical)
    return {"status": "PASS", "graph_digest": original["graph_digest"], "degrees": degrees,
            "physical_classes": {"low": sorted(low_names), "high": sorted(high_names)},
            "signed_degree": signed, "incidence": incidence_audit(edges, roles, cuts, physical, signed),
            "controls": audit_control(root, cfg, controls), "frozen_d091": prior_negative(root, cfg),
            "new_graph_identities": 0, "solver_calls": 0, "enumeration_visits": 0}
