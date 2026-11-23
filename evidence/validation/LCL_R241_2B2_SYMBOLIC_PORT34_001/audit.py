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


def ledger(original, labels, side, edges, cut, pair):
    assert labels.keys() == side.keys() and all(type(v) is int for v in labels.values())
    assert sorted(labels.values()) == list(range(len(side)))
    assert all(side[v] == int(label >= cut) for v, label in labels.items())
    assert (labels["s:0"], labels["s:1"]-cut) == pair
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    assert sorted(weights) == list(range(1, len(side)))
    identifier = digest({"graph_digest": original["graph_digest"], "labels": sorted(labels.items())})
    return weights, identifier


def match_prior_manifest(root, cfg, folder, names):
    manifest_path = f"{folder}/MANIFEST.json"
    entries = {row["path"]: row for row in load(root / manifest_path)["files"]}
    for name in names:
        relative = f"{folder}/{name}"
        assert sha256((root / relative).read_bytes()).hexdigest() == entries[name]["sha256"] == cfg["source_hashes"][relative]
        assert (root / relative).stat().st_size == entries[name]["bytes"]


def palette_comparison(b, original, labels):
    graph = original["graph"]
    fixed = {"s:0": 3, "s:1": b+8, "b:0:0": b+5, "b:0:1": b+4, "b:1:0": 0}
    assert all(labels[v] == value for v, value in fixed.items())
    palettes = {(0, 0): (1, 2), (0, 1): tuple(range(4, b+4)), (1, 0): (b+6, b+7)}
    edges = graph["edges"]
    changes = []
    for (section, branch), expected in palettes.items():
        center = f"b:{section}:{branch}"
        names = [f"l:{section}:{branch}:{j}" for j in range(len(expected))]
        actual = [labels[v] for v in names]
        assert sorted(actual) == list(expected)
        assert all([center, v] in edges for v in names)
        assert sorted(abs(labels[center]-value) for value in actual) == sorted(
            abs(labels[center]-value) for value in expected)
        changes.extend({"name": v, "retained": value, "indexed_formula": new}
                       for v, value, new in zip(names, actual, expected, strict=True) if value != new)
    return changes


def archived_controls(root, cfg, controls):
    base = cfg["negative_archive"]
    match_prior_manifest(root, cfg, base, ("strict_original.json", "config.json", "audit_result.json", "enumeration.json"))
    copies = []
    for b, saved in zip((2, 3, 4), controls["retained_positives"], strict=True):
        inputs = cfg["retained"][str(b)]
        result_path = inputs["result"]
        archive_dir = result_path.rsplit("/", 1)[0]
        names = ("result.json",) if b == 2 else ("result.json", "original.json")
        match_prior_manifest(root, cfg, archive_dir, names)
        original = load(root / inputs["original"])
        report = load(root / result_path)
        assert report["status"] == "PASS" and report["graph_digest"] == original["graph_digest"]
        if b == 2:
            menu = report["menu"]["pairs"]
        elif b == 3:
            menu = report["pairs"]
        else:
            menu = [report["state"]]
        row, = [row for row in menu if row["pair"] == [3, 4] and row["status"] == "WITNESSED"]
        cert = row["certificate"]
        side, _, edges, _ = inspect(original, [[2, b], [2]])
        weights, identity = ledger(original, cert["labels"], side, edges, b+4, (3, 4))
        assert cert["graph_digest"] == original["graph_digest"] and cert["ledger_id"] == identity
        assert cert["physical_ports"] == cert["witness"] == ["s:0", "s:1"]
        assert cert["port_labels"] == [3, b+8] and cert["cut"] == b+4
        assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
        assert saved == {"b": b, "pair": [3, 4], "graph_digest": original["graph_digest"],
                         "ledger_id": identity, "checker": cert["checker"]}
        changes = palette_comparison(b, original, cert["labels"])
        assert len(changes) == {2: 4, 3: 2, 4: 0}[b]
        copies.append({"b": b, "graph_digest": original["graph_digest"], "retained_ledger_id": identity,
                       "ports_match": True, "palettes_match": True, "index_differences": changes})

    neg = load(root / base / "audit_result.json")
    pins = load(root / base / "config.json")
    assert pins["profile"] == [[2, 2], [2]] and pins["cut"] == 6 and pins["pins"] == {"s:0": 1, "s:1": 6}
    assert neg["status"] == "PASS" and neg["positive_certificates"] == 0
    assert neg["visits_certified"] == neg["duplicate_edge_receipts"] == 2880
    assert neg["raw_receipts"]["strict_original.json"] == cfg["source_hashes"][f"{base}/strict_original.json"]
    archived_hash = cfg["source_hashes"][f"{base}/enumeration.json"]
    assert neg["raw_receipts"]["enumeration.json"] == archived_hash
    assert controls["d082_negative"] == {"pair": [1, 0], "graph_digest": copies[0]["graph_digest"],
                                        "historical_visits": 2880, "positive_certificates": 0,
                                        "new_replay_visits": 0, "historical_receipt_sha256": archived_hash}
    return copies


def check_adverse(original, edges, labels, checks):
    assert set(checks) == {"digest", "port", "difference"}
    wrong = checks["digest"]
    assert wrong["expected"] == "0"*64 != original["graph_digest"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["graph_digest"] == original["graph_digest"]
    assert checks["port"] == {"valid": False, "reason": "physical offset mismatch",
                               "declared": [3, 3], "actual": [labels["s:0"], labels["s:1"]-9]}
    swap = checks["difference"]
    u, v = swap["swap"]
    assert [u, v] == ["l:0:0:0", "l:0:1:0"]
    altered = labels | {u: labels[v], v: labels[u]}
    assert sorted(altered.values()) == list(range(14))
    difference = [abs(altered[x]-altered[y]) for x, y in edges]
    repeated = {w: count for w, count in Counter(difference).items() if count > 1}
    assert repeated == {6: 2, 8: 2}
    check = swap["checker"]
    assert not check["valid"] and "edge differences repeat" in check["errors"]
    assert check["graph_digest"] == original["graph_digest"] and check["edge_differences"] == difference
    assert sorted(set(range(1, 14))-set(difference)) == [5, 9]
    return repeated


def check(root, here, cfg, regression, controls):
    original = load(here / "original.json")
    b = 5
    side, degree, edges, _ = inspect(original, [[2, b], [2]])
    assert len(side) == b+9 and len(edges) == b+8
    assert sum(value == 0 for value in side.values()) == b+4
    assert regression["b"] == b == cfg["regression_b"]
    assert regression["status"] == "WITNESSED" and regression["pair"] == [3, 4]
    assert regression["port_labels"] == [3, b+8] and regression["graph_digest"] == original["graph_digest"]
    cert = regression["certificate"]
    labels = cert["labels"]
    assert palette_comparison(b, original, labels) == []
    weights, identity = ledger(original, labels, side, edges, b+4, (3, 4))
    assert cert["edge_rows"] == [edge+[w] for edge, w in zip(edges, weights, strict=True)]
    assert cert["physical_ports"] == cert["witness"] == ["s:0", "s:1"]
    assert cert["port_labels"] == [3, b+8] and cert["cut"] == b+4
    assert cert["ledger_id"] == identity and cert["graph_digest"] == original["graph_digest"]
    verified = cert["checker"]
    assert verified["valid"] and verified["errors"] == [] and verified["graph_digest"] == original["graph_digest"]
    assert (verified["n"], verified["m"], verified["edge_differences"]) == (14, 13, weights)
    indexed_weights = [w for (_, v), w in zip(edges, weights, strict=True) if v.startswith("l:0:1:")]
    other_weights = sorted(w for (_, v), w in zip(edges, weights, strict=True) if not v.startswith("l:0:1:"))
    assert indexed_weights == list(range(b, 0, -1)) and other_weights == list(range(b+1, b+9))
    correction = {v: (2*side[v]-1)*(n-1) for v, n in degree.items() if n > 1}
    assert correction == {"s:0": -2, "s:1": 1, "b:0:0": 2, "b:0:1": b, "b:1:0": -2}
    signed_sum = sum((2*side[v]-1)*degree[v]*labels[v] for v in labels)
    assert signed_sum == sum(range(1, b+9)) == 91
    center_sum = 2*labels["b:0:0"]+b*labels["b:0:1"]-2*labels["b:1:0"]
    assert center_sum == b*b+6*b+10
    retained = archived_controls(root, cfg, controls)
    assert len({row["graph_digest"] for row in retained} | {original["graph_digest"]}) == 4
    duplicates = check_adverse(original, edges, labels, controls["adverse"])
    return {"status": "PASS", "regression_indexed_weights": indexed_weights,
            "regression_other_weights": other_weights, "regression_signed_degree_sum": signed_sum,
            "regression_center_identity": center_sum, "retained_comparisons": retained,
            "adverse_duplicate_weights": duplicates, "verified_adverse_rejections": 3,
            "named_assignment_visits": 0, "retained_replay_visits": 0}
