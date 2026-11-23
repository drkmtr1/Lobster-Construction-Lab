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


def extremal_audit(adjacency, lows, highs):
    zero_candidates = adjacency["s:1"] - {"s:0"}
    assert zero_candidates == {"b:1:0"}
    center, = zero_candidates
    right_terminals = adjacency[center] - {"s:1"}
    assert right_terminals == {"l:1:0:0", "l:1:0:1"}
    assert all(adjacency[v] == {center} for v in right_terminals)
    assert adjacency["s:1"] == {"s:0", center}
    neighbor_labels_of_exit = {5, 0}  # The required edge of weight nine forces the second entry.
    forced_right_labels = []
    levels = []
    for weight in (9, 8, 7, 6):
        rows = []
        for low in range(10-weight):
            high = weight+low
            assert low in lows and high in highs
            if high == 9:
                possible = low in neighbor_labels_of_exit
                reason = "right attachment forced by weight nine" if possible else "exit has neighbors only 5 and 0"
            elif high in forced_right_labels:
                possible = low == 0
                reason = "already forced right terminal is adjacent only to zero"
            else:
                assert low == 0
                possible = len(forced_right_labels) < len(right_terminals)
                reason = "vacant position at zero" if possible else "all neighbors of zero already occupied"
            rows.append({"labels_high_low": [high, low], "possible_under_previous_forcing": possible,
                         "reason": reason})
        allowed = [r["labels_high_low"] for r in rows if r["possible_under_previous_forcing"]]
        assert allowed == ([[weight, 0]] if weight >= 7 else [])
        if weight in (8, 7):
            forced_right_labels.append(weight)
        levels.append({"weight": weight, "pairs": rows})
    count = sum(len(level["pairs"]) for level in levels)
    assert count == 10 and forced_right_labels == [8, 7]
    return {"representations": count, "levels": levels, "zero_at": center,
            "right_terminal_names": sorted(right_terminals), "right_terminal_palette": sorted(forced_right_labels),
            "terminal_order": "both bijections of the palette onto the two named leaves",
            "missing_required_weight": 6}


def weighted_audit(side, degrees, adjacency, lows, highs, extremal):
    correction = {v: (d-1)*(2*side[v]-1) for v, d in degrees.items() if d > 1}
    assert degrees == {v: {"s:0": 2, "s:1": 2, "b:0:0": 5, "b:1:0": 3}.get(v, 1) for v in side}
    assert correction == {"s:0": -1, "s:1": 1, "b:0:0": 4, "b:1:0": -2}
    high_sum, low_sum = sum(highs), sum(lows)
    fixed = high_sum-low_sum + correction["s:0"]*5 + correction["s:1"]*9
    target = sum(range(1, 10))
    center_equation_rhs = target-fixed
    first_center_coefficient = correction["b:0:0"]
    assert (high_sum, low_sum, fixed, target, center_equation_rhs, first_center_coefficient) == (30, 15, 19, 45, 26, 4)
    assert center_equation_rhs % first_center_coefficient != 0

    right_palette = set(extremal["right_terminal_palette"])
    center_label, = set(highs) - {9} - right_palette
    left_palette = set(lows) - {0, 5}
    assert len(left_palette) == len(adjacency["b:0:0"] - {"s:0"})
    assert center_label == 6 and left_palette == {1, 2, 3, 4}
    groups = {"spine": [9-5], "left_attachment": [center_label-5], "right_attachment": [9],
              "left_terminal_edges": sorted(center_label-v for v in left_palette),
              "right_terminal_edges": sorted(right_palette)}
    spectrum = sorted(w for g in groups.values() for w in g)
    repeated = {str(w): c for w, c in Counter(spectrum).items() if c > 1}
    missing = sorted(set(range(1, 10)) - set(spectrum))
    assert len(spectrum) == 9 and repeated == {"4": 2} and missing == [6]
    assert sum(spectrum) == fixed + first_center_coefficient*center_label == 43
    return {"degree_excess_coefficients": correction, "high_sum": high_sum, "low_sum": low_sum,
            "fixed_term": fixed, "required_total": target, "shared_zero_host": extremal["zero_at"],
            "forced_first_center_rational": {"numerator": 13, "denominator": 2},
            "integer_solution_after_zero_forcing": False,
            "extremal_palette_diagnostic": {
                "note": "First center 6 comes from the three largest required weights, not the signed sum",
                "left_center": center_label, "left_terminal_palette": sorted(left_palette),
                "difference_groups": groups, "sorted_differences": spectrum, "sum": sum(spectrum),
                "repeated": repeated, "missing": missing}}


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
    assert (u, v) == ("l:0:0:0", "l:0:1:0")
    swapped = dict(labels)
    swapped[u], swapped[v] = labels[v], labels[u]
    wrong_weights = [abs(swapped[x]-swapped[y]) for x, y in edges]
    counts = Counter(wrong_weights)
    duplicates = {str(w): c for w, c in counts.items() if c > 1}
    missing = [w for w in range(1, 24) if not counts[w]]
    assert sorted(swapped.values()) == list(range(24))
    assert adverse["invalid_labeling"]["repeated"] == duplicates == {"16": 2, "18": 2}
    assert adverse["invalid_labeling"]["missing"] == missing == [15, 19]
    rejection = adverse["invalid_labeling"]["checker"]
    assert rejection == saved["checker"] | {"valid": False, "edge_differences": wrong_weights,
                                              "errors": ["edge differences repeat", "edge differences are not exactly 1..m"]}
    return {"positive": "D090", "graph_digest": original["graph_digest"], "ledger_id": identifier,
            "adverse_rejections": 3, "swap_repeated": duplicates, "swap_missing": missing}


def check(root, here, cfg, controls):
    for path, expected in cfg["source_hashes"].items():
        assert sha256((root / path).read_bytes()).hexdigest() == expected
    for source, folder in cfg["retained_without_replay"].items():
        match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json"))
        saved = load(root / folder / "result.json")
        assert saved["status"] == "PASS"
        if source == "D088":
            assert saved["disposition"] == "EXCLUDED"
    original = load(here / "original.json")
    side, degrees, edges, _ = inspect(original, [[4], [2]])
    assert len(side) == 10 and len(edges) == 9
    lows = range(6)
    highs = range(6, 10)
    names_low = {v for v in side if not side[v]}
    names_high = set(side) - names_low
    assert names_low == {"s:0", "b:1:0", *(f"l:0:0:{j}" for j in range(4))}
    assert names_high == {"s:1", "b:0:0", "l:1:0:0", "l:1:0:1"}
    adjacency = {v: set() for v in side}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert cfg["domain"]["cut"] == len(lows) == len(names_low)
    assert cfg["domain"]["port_labels"] == [5, 9] and 5 in lows and 9 in highs
    assert cfg["domain"]["ports"] == original["graph"]["spine"] == ["s:0", "s:1"]
    assert cfg["domain"]["offsets"] == [5, 9-len(lows)]
    extremal = extremal_audit(adjacency, lows, highs)
    weighted = weighted_audit(side, degrees, adjacency, lows, highs, extremal)
    return {"status": "PASS", "graph_digest": original["graph_digest"], "degrees": degrees,
            "physical_classes": {"low": sorted(names_low), "high": sorted(names_high)},
            "extremal": extremal, "weighted_degree": weighted,
            "controls": audit_control(root, cfg, controls),
            "retained_without_replay": sorted(cfg["retained_without_replay"]),
            "new_graph_identities": 0, "solver_calls": 0, "enumeration_visits": 0}
