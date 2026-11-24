"""Independently reconstruct named graphs and evaluate a fresh-label rank insertion."""

from collections import Counter
from hashlib import sha256
import json


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":"), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def inspect(original, profile):
    graph = original["graph"]
    spine = ["s:0", "s:1"]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = [tuple(spine)]
    for section, quotas in enumerate(profile):
        for branch, n in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            edges.append((spine[section], center))
            for index in range(n):
                leaf = f"l:{section}:{branch}:{index}"
                roles[leaf] = {"kind": "leaf", "section": section, "branch": branch, "leaf": index}
                edges.append((center, leaf))
    assert graph["schema_version"] == 1 and graph["profile"] == profile
    assert graph["spine"] == spine and graph["roles"] == roles
    assert Counter(graph["vertices"]) == Counter(list(roles))
    named_edges = Counter(tuple(sorted(e)) for e in edges)
    assert Counter(tuple(sorted(e)) for e in graph["edges"]) == named_edges
    canonical = {"vertices": sorted(roles), "edges": sorted(sorted(e) for e in edges),
                 "spine": spine, "roles": roles, "profile": profile}
    assert original["graph_digest"] == digest(canonical)
    return named_edges


def edge_rows(graph, labels):
    return [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]


def check_state(graph, labels, p, x, y, b, state):
    low = {"s:0", "b:1:0"} | {v for v in graph["vertices"] if v.startswith("l:0:")}
    high = set(graph["vertices"])-low
    assert set(labels) == low | high and all(type(label) is int for label in labels.values())
    assert sorted(labels[v] for v in low) == list(range(p))
    assert sorted(labels[v] for v in high) == list(range(p, len(labels)))
    assert all((u in low) != (v in low) for u, v in graph["edges"])
    assert labels["s:0"] == x and labels["s:1"] == p+y and labels["b:0:1"] == b
    assert state == {"cut": p, "physical_labels": [x, p+y], "offsets": [x, y], "host_label": b,
                     "witness": ["s:0", "s:1"], "edge_crossing": True, "host_spine_distance": 1}


def inspect_row(old_graph, new_graph, target_digest, old_labels, ledger, c, x, y, b, row):
    assert (row["ledger"], row["threshold"]) == (ledger, c)
    s = {v for v in old_graph["vertices"] if old_labels[v] in range(c)}
    old_edges = edge_rows(old_graph, old_labels)
    selected = [item for item in old_edges if len(s.intersection(item[:2])) == 1]
    assert row["selected_vertices"] == sorted(s) and row["selected_edges"] == selected
    old_weights = Counter(w for _, _, w in selected)
    wanted = Counter(range(b+1-c, 13))
    assert row["actual_premise"] == sorted(old_weights.elements()) and row["required_premise"] == sorted(wanted.elements())
    assert row["extra_premise"] == sorted((old_weights-wanted).elements())
    assert row["absent_premise"] == sorted((wanted-old_weights).elements())
    assert row["theorem_applies"] == (old_weights == wanted)

    order = sorted(old_labels, key=old_labels.__getitem__)
    order.insert(c, "l:0:1:2")
    labels = {v: i for i, v in enumerate(order)}
    assert row["labels"] == labels and row["label_inventory"] == list(range(14))
    check_state(new_graph, labels, 9, x, y, b+1, row["interface"])
    calculated = edge_rows(new_graph, labels)
    assert row["edge_rows"] == calculated
    by_edge = {tuple(sorted((u, v))): w for u, v, w in calculated}
    for u, v, w in old_edges:
        assert by_edge[tuple(sorted((u, v)))] == w+int(u in s or v in s)
    leaf = "l:0:1:2"
    new_weight = by_edge[("b:0:1", leaf)]
    assert row["new_leaf"] == [leaf, c, new_weight] and new_weight == b+1-c
    weights = [w for _, _, w in calculated]
    counts = Counter(weights)
    repeated = [[w, count] for w, count in sorted(counts.items()) if count > 1]
    missing = sorted(set(range(1, 14))-counts.keys())
    assert row["difference_inventory"] == sorted(weights)
    assert row["repeated_differences"] == repeated and row["missing_differences"] == missing
    checker = row["checker"]
    valid = sorted(weights) == list(range(1, 14))
    assert checker["valid"] == valid and checker["graph_digest"] == target_digest
    assert checker["edge_differences"] == weights and (checker["n"], checker["m"]) == (14, 13)
    if repeated:
        assert checker["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"ledger": ledger, "threshold": c, "selected_edge_count": len(selected),
            "repeated": repeated, "missing": missing, "valid": valid}


def check(root, cfg, source, target, ledgers, rows, adverse):
    old_edges = inspect(source, [[4, 2], [2]])
    new_edges = inspect(target, [[4, 3], [2]])
    old, new = source["graph"], target["graph"]
    added = ("b:0:1", "l:0:1:2")
    assert new_edges == old_edges+Counter([added])
    assert Counter(new["vertices"]) == Counter(old["vertices"])+Counter([added[1]])
    assert {v: new["roles"][v] for v in old["vertices"]} == old["roles"]
    assert (len(old["vertices"]), sum(old_edges.values()), len(new["vertices"]), sum(new_edges.values())) == (13, 12, 14, 13)

    trunk = {"s:0": 3, "s:1": 12, "b:0:0": 8, "b:0:1": 9, "b:1:0": 0}
    direct = trunk | dict(zip(("l:0:0:0", "l:0:0:1", "l:0:0:2", "l:0:0:3", "l:0:1:0",
                              "l:0:1:1", "l:1:0:0", "l:1:0:1"), (4, 5, 6, 7, 1, 2, 10, 11), strict=True))
    lows = {v for v in direct if direct[v] < 8}
    reflection = {v: 7-direct[v] if v in lows else 20-direct[v] for v in direct}
    source_rows = {}
    for key, labels, x, y, b in (("I", direct, 3, 4, 9), ("II", reflection, 4, 0, 11)):
        data = ledgers[key]
        assert data["labels"] == labels and data["graph_digest"] == source["graph_digest"]
        assert data["ledger_id"] == digest({"graph_digest": source["graph_digest"], "labels": sorted(labels.items())})
        check_state(old, labels, 8, x, y, b, data["interface"])
        weights = [w for _, _, w in edge_rows(old, labels)]
        assert sorted(weights) == list(range(1, 13))
        assert data["checker"]["valid"] and data["checker"]["edge_differences"] == weights
        source_rows[key] = weights
    assert source_rows["II"] == [13-w for w in source_rows["I"]]
    assert ledgers["I"]["ledger_id"] == cfg["source_ledger_id"]
    requested = [("I", c, 3, 4, 9) for c in (4, 5, 6, 7, 8)]+[("II", c, 4, 0, 11) for c in (5, 6, 7, 8)]
    independent = [inspect_row(old, new, target["graph_digest"], ledgers[key]["labels"], key, c, x, y, b, row)
                   for (key, c, x, y, b), row in zip(requested, rows, strict=True)]

    fake = adverse["graph_digest"]
    assert fake["declared"] == "0"*64 and not fake["checker"]["valid"]
    assert fake["checker"]["errors"] == ["original graph digest mismatch"]
    assert adverse["physical_port"] == {"declared": [3, 3], "valid": False, "error": "Physical offset mismatch"}
    wrong = adverse["incidence"]
    assert wrong == {"claimed_edge": ["b:0:0", added[1]], "replaced_edge": list(added),
                     "valid": False, "error": "Incorrect new original incidence"}
    assert tuple(wrong["claimed_edge"]) not in new_edges and tuple(wrong["replaced_edge"]) in new_edges
    archived = {key: json.loads((root / path).read_bytes())["status"] for key, path in cfg["status_receipts"].items()}
    assert archived == {"D083_original": "INCOMPLETE", "D083_versioned": "PASS",
                        "D093_original": "INCOMPLETE", "D093_versioned": "PASS"}
    return {"status": "PASS", "threshold_audits": independent, "added_incidence": list(added),
            "source_edge_differences": source_rows, "archived_execution_statuses": archived}
