"""Independently reconstruct both originals and check a structural eight-case exclusion."""

from collections import Counter, deque
from hashlib import sha256
import json


def load(path):
    return json.loads(path.read_bytes())


def canonical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def inspect(original, profile):
    graph = original["graph"]
    spine = ["s:0", "s:1"]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    expected = [tuple(spine)]
    for i, section in enumerate(profile):
        for j, quota in enumerate(section):
            center = f"b:{i}:{j}"
            roles[center] = {"kind": "branch", "section": i, "branch": j}
            expected.append((spine[i], center))
            for k in range(quota):
                leaf = f"l:{i}:{j}:{k}"
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
                expected.append((center, leaf))
    assert graph["schema_version"] == 1 and graph["roles"] == roles and graph["profile"] == profile
    assert graph["spine"] == spine and Counter(graph["vertices"]) == Counter(list(roles))
    assert Counter(tuple(sorted(e)) for e in graph["edges"]) == Counter(tuple(sorted(e)) for e in expected)
    assert len(expected) == len(roles)-1
    assert original["graph_digest"] == canonical_hash({"vertices": sorted(roles),
        "edges": sorted(sorted(e) for e in expected), "spine": spine, "roles": roles, "profile": profile})
    neighbors = {v: set() for v in roles}
    for u, v in expected:
        neighbors[u].add(v)
        neighbors[v].add(u)
    distance, queue = {"s:0": 0}, deque(["s:0"])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]-distance.keys():
            distance[v] = distance[u]+1
            queue.append(v)
    assert set(distance) == set(neighbors)
    lows = {v for v in distance if distance[v] % 2 == 0}
    assert all((u in lows) != (v in lows) for u, v in expected)
    return neighbors, lows


def reconstruct_reduction(original, reduction):
    neighbors, lows = inspect(original, [[4, 3], [2]])
    highs = set(neighbors)-lows
    assert len(lows) == 9 and len(highs) == 5
    degrees = {v: len(adj) for v, adj in neighbors.items()}
    counts = {"s:0": 3, "s:1": 2, "b:0:0": 5, "b:0:1": 4, "b:1:0": 3}
    assert degrees == {v: counts.get(v, 1) for v in neighbors}
    assert reduction["degree_vector"] == degrees
    assert reduction["low_names"] == sorted(lows) and reduction["high_names"] == sorted(highs)
    coeff = {v: (1-degree if v in lows else degree-1) for v, degree in counts.items()}
    baseline = sum(range(len(lows), len(neighbors)))-sum(range(len(lows)))
    required = sum(range(1, len(neighbors)))
    leftover = required-(baseline+coeff["s:1"]*12)
    assert reduction["signed_excess"] == coeff
    assert (reduction["baseline_signed_sum"], reduction["constant_with_exit"],
            reduction["required_sum"], reduction["right_hand_side"]) == (baseline, 31, required, leftover)
    assert coeff["b:0:1"] % 2 and all(coeff[v] % 2 == 0 for v in ("s:0", "b:0:0", "b:1:0"))
    free_highs = set(range(9, 14))-{12}
    b, = [value for value in free_highs if value % 2 == leftover % 2]
    assert reduction["B"] == b == 10
    assert reduction["possible_A"] == sorted(free_highs-{b})
    pairs = {w: [[hi, hi-w] for hi in range(13, 8, -1) if 0 <= hi-w < 9] for w in range(10, 14)}
    for w, p in pairs.items():
        assert set(map(tuple, reduction["extremal_representations"][str(w)])) == set(map(tuple, p))
    assert pairs[13] == [[13,0]]
    first_leaves = sorted(neighbors["b:0:0"]-{"s:0"})
    right_leaves = sorted(neighbors["b:1:0"]-{"s:1"})
    assert first_leaves == [f"l:0:0:{i}" for i in range(4)]
    assert right_leaves == ["l:1:0:0", "l:1:0:1"]
    assert all(neighbors[v] == {"b:0:0"} for v in first_leaves)
    assert all(neighbors[v] == {"b:1:0"} for v in right_leaves)
    fixed = {}
    for w in range(13, 9, -1):
        remaining = [pair for pair in pairs[w] if pair[1] not in fixed or fixed[pair[1]] == pair[0]]
        assert remaining == [[13,13-w]]
        if w > 10:
            fixed[13-w] = 13
    return neighbors, first_leaves, pairs


def audit_cases(rows, neighbors, first_leaves):
    assert [(c["A"],c["B"],c["x"],c["z"]) for c in rows] == [
        (9,10,3,0), (11,10,7,0), (13,10,3,8), (13,10,4,7),
        (13,10,5,6), (13,10,6,5), (13,10,7,4), (13,10,8,3)]
    verified = []
    for row in rows:
        a,b,x,z = (row[k] for k in ("A","B","x","z"))
        assert 4*a+3*b-2*x-2*z == 60 and x != z and 0 <= x <= 8 and 0 <= z <= 8
        attachment = [a-x, b-x, 12-z]
        right_labels = sorted(set(range(9, 14))-{a,b,12})
        right_edges = [label-z for label in right_labels]
        named_weights = {"s:0--s:1": 12-x, "s:0--b:0:0": attachment[0], "s:0--b:0:1": attachment[1],
                         "s:1--b:1:0": attachment[2], **{f"b:1:0 to label {hi}": hi-z for hi in right_labels}}
        assert row["spine_weight"] == 12-x and row["attachment_weights"] == attachment
        assert row["right_terminal_labels"] == right_labels and row["right_terminal_weights"] == right_edges
        residue = set(range(1, 14))-set(named_weights.values())
        remaining_lows = set(range(9))-{x,z}
        expected = row["obstruction"]
        if a != 13:
            assert z == 0 and 13 in right_labels
            bound = max(a,b)-min(remaining_lows)
            missing = max(a,b)
            assert missing in residue and missing > bound
            assert expected == {"kind": "missing_weight", "weight": missing, "largest_possible_left_terminal_weight": bound}
        else:
            assert row["forced_minimum_first_terminal_palette"] == [0,1,2] and row["weight_10_pair"] == [13,3]
            assert {0,1,2} <= remaining_lows
            remaining_lows -= {0,1,2}
            if z == 3:
                assert "b:1:0" not in neighbors["b:0:0"] and 10 in residue
                assert expected == {"kind": "missing_weight", "weight": 10, "required_nonedge": ["b:0:0","b:1:0"]}
            elif x == 3:
                banned = [label for label in sorted(remaining_lows) if b-label in named_weights.values()]
                slots = len(first_leaves)-3
                assert len(banned) > slots and 13-x == 10
                assert expected == {"kind": "terminal_capacity", "residual_lows": sorted(remaining_lows),
                                    "forbidden_second_center_lows": banned, "conflicting_right_weights": [b-v for v in banned],
                                    "remaining_first_slots": slots}
            elif x == 4:
                assert 3 in remaining_lows
                second_palette = sorted(remaining_lows-{3})
                cap = sorted(set(b-v for v in second_palette) & set([attachment[2],*right_edges]))
                assert len(second_palette) == 3 and cap == [2,4,5]
                assert expected == {"kind": "duplicate_terminal_palette", "forced_first_terminal_lows": [0,1,2,3],
                                    "forced_second_terminal_lows": second_palette, "duplicate_weights": cap}
            else:
                named_repeat = [w for w,c in Counter(named_weights.values()).items() if c > 1]
                assert named_repeat == [expected["weight"]] and expected["kind"] == "duplicate_weight"
                if "fixed_edges" in expected:
                    u,v = ("--".join(e) for e in expected["fixed_edges"])
                    assert u != v and named_weights[u] == named_weights[v] == expected["weight"]
                else:
                    fixed_edge = "--".join(expected["fixed_edge"])
                    assert named_weights[fixed_edge] == named_weights[f"b:1:0 to label {expected['right_terminal_label']}"]
        verified.append({"A":a, "B":b, "x":x, "z":z, "fixed_incidence_weights":named_weights,
                         "unassigned_terminal_low_labels_after_forcing":sorted(remaining_lows), "obstruction":expected})
    return verified


def audit_controls(root, cfg, positive, adverse):
    original = load(root / cfg["retained"]["d098_original"])
    cert = load(root / cfg["retained"]["d098_result"])["certificate"]
    graph, labels = original["graph"], cert["labels"]
    _, low = inspect(original, [[4, 2], [2]])
    assert set(labels) == set(graph["vertices"]) and sorted(labels.values()) == list(range(13))
    assert sorted(labels[v] for v in low) == list(range(8))
    assert (labels["s:0"],labels["s:1"]) == (3,12)
    assert positive["ledger_id"] == canonical_hash({"graph_digest": original["graph_digest"], "labels": sorted(labels.items())})
    assert positive["graph_digest"] == original["graph_digest"] and positive["checker"]["valid"]
    weights = [abs(labels[u]-labels[v]) for u,v in graph["edges"]]
    assert sorted(weights) == list(range(1, 13)) and weights == positive["checker"]["edge_differences"]
    wrong = adverse["graph_digest"]["checker"]
    assert adverse["graph_digest"]["claimed"] == "0"*64 and not wrong["valid"]
    assert wrong["errors"] == ["original graph digest mismatch"]
    assert adverse["physical_port"] == {"claimed": [3,3], "valid": False, "error": "Physical offset mismatch"}
    swap = adverse["label_swap"]
    u,v = swap["vertices"]
    actual = labels | {u:labels[v],v:labels[u]}
    assert (u,v) == ("l:0:0:0","l:0:1:0") and swap["labels"] == actual
    assert sorted(actual.values()) == list(range(13))
    damaged = [abs(actual[u]-actual[v]) for u,v in graph["edges"]]
    assert not swap["checker"]["valid"] and swap["checker"]["edge_differences"] == damaged
    repeats = sorted(w for w, n in Counter(damaged).items() if n > 1)
    gaps = sorted(set(range(1,13))-set(damaged))
    assert repeats == [5,7] and gaps == [4,8]
    return {"repeat_weights":repeats, "missing_weights":gaps, "retained_graph_digest":original["graph_digest"]}


def check(root, cfg, original, reduction, rows, positive, adverse):
    neighbors, first_leaves, pairs = reconstruct_reduction(original, reduction)
    audited = audit_cases(rows, neighbors, first_leaves)
    control = audit_controls(root, cfg, positive, adverse)
    archives = {key: load(root / path)["status"] for key,path in cfg["status_receipts"].items()}
    assert archives == {"D083_original":"INCOMPLETE", "D083_versioned":"PASS",
                        "D093_original":"INCOMPLETE", "D093_versioned":"PASS"}
    return {"status":"PASS", "verified_scalar_cases":audited, "extreme_representations":pairs,
            "corrupted_control":control, "archived_execution_statuses":archives,
            "target_graph_digest":original["graph_digest"]}
