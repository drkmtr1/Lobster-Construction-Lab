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


def archived_controls(root, cfg, controls):
    base = cfg["retained_d082"]
    d084 = cfg["retained_d084"]
    d085 = cfg["retained_d085"]
    match_prior_manifest(root, cfg, base, ("strict_original.json", "audit_result.json", "config.json", "enumeration.json"))
    match_prior_manifest(root, cfg, d084, ("result.json",))
    match_prior_manifest(root, cfg, d085, ("original.json", "result.json"))
    retained = load(root / base / "strict_original.json")
    prior = load(root / base / "audit_result.json")
    pins = load(root / base / "config.json")
    assert pins["profile"] == [[2, 2], [2]] and pins["cut"] == 6 and pins["pins"] == {"s:0": 1, "s:1": 6}
    assert prior["status"] == "PASS" and prior["positive_certificates"] == 0
    assert prior["visits_certified"] == prior["duplicate_edge_receipts"] == 2880
    assert prior["raw_receipts"]["strict_original.json"] == cfg["source_hashes"][f"{base}/strict_original.json"]
    archived_hash = cfg["source_hashes"][f"{base}/enumeration.json"]
    assert archived_hash == prior["raw_receipts"]["enumeration.json"]
    assert controls["d082_negative"] == {"pair": [1, 0], "graph_digest": retained["graph_digest"],
                                        "historical_visits": 2880, "positive_certificates": 0,
                                        "new_replay_visits": 0, "historical_receipt_sha256": archived_hash}
    first = load(root / d084 / "result.json")
    second = load(root / d085 / "result.json")
    original_085 = load(root / d085 / "original.json")
    archives = [(84, first, first["menu"]["pairs"], retained, [[2, 2], [2]], 6),
                (85, second, second["pairs"], original_085, [[2, 3], [2]], 7)]
    cert_085 = None
    for group, checked in zip(archives, controls["retained_positives"], strict=True):
        decision, record, rows, original, profile, cut = group
        assert record["status"] == "PASS" and record["graph_digest"] == original["graph_digest"]
        row, = [row for row in rows if row["pair"] == [3, 4] and row["status"] == "WITNESSED"]
        old = row["certificate"]
        side, _, edges, _ = inspect(original, profile)
        weights, identity = ledger(original, old["labels"], side, edges, cut, (3, 4))
        assert old["ledger_id"] == identity and old["graph_digest"] == original["graph_digest"]
        assert checked == {"decision": decision, "pair": [3, 4], "ledger_id": identity, "checker": old["checker"]}
        assert checked["checker"]["valid"] and checked["checker"]["edge_differences"] == weights
        assert checked["checker"]["graph_digest"] == original["graph_digest"]
        if decision == 85:
            cert_085 = old
    return original_085, cert_085, [retained["graph_digest"], original_085["graph_digest"]]


def check_adverse(original, edges, labels, controls):
    adverse = controls["adverse"]
    assert set(adverse) == {"digest", "port", "difference"}
    wrong = adverse["digest"]
    assert wrong["expected"] == "0"*64 != original["graph_digest"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["graph_digest"] == original["graph_digest"]
    assert adverse["port"] == {"valid": False, "reason": "physical offset mismatch", "declared": [3, 3],
                               "actual": [labels["s:0"], labels["s:1"]-8]}
    swap = adverse["difference"]
    u, v = swap["swap"]
    assert [u, v] == ["l:0:0:0", "l:0:1:0"]
    altered = labels | {u: labels[v], v: labels[u]}
    assert sorted(altered.values()) == list(range(13))
    differences = [abs(altered[x]-altered[y]) for x, y in edges]
    repeated = {w: n for w, n in Counter(differences).items() if n > 1}
    assert repeated == {5: 2, 7: 2}
    check = swap["checker"]
    assert not check["valid"] and "edge differences repeat" in check["errors"]
    assert check["graph_digest"] == original["graph_digest"] and check["edge_differences"] == differences
    return repeated


def compare(old_original, old_labels, original, labels):
    old_graph, graph = old_original["graph"], original["graph"]
    added = "l:0:1:3"
    assert set(labels) - set(old_labels) == {added} and old_labels.keys() <= labels.keys()
    assert {v: graph["roles"][v] for v in old_labels} == old_graph["roles"]
    old_edges = list(map(tuple, old_graph["edges"]))
    new_edges = list(map(tuple, graph["edges"]))
    assert Counter(new_edges) == Counter(old_edges)+Counter([("b:0:1", added)])
    stable = ["s:0", "b:1:0", "l:0:0:0", "l:0:0:1"]
    raised = ["s:1", "b:0:0", "b:0:1", "l:1:0:0", "l:1:0:1"]
    indexed = ["l:0:1:0", "l:0:1:1", "l:0:1:2"]
    assert set(stable+raised+indexed) == set(old_labels)
    assert all(labels[v] == old_labels[v] for v in stable)
    assert all(labels[v] == old_labels[v]+1 for v in raised)
    before = [old_labels[v] for v in indexed]
    after = [labels[v] for v in indexed+[added]]
    assert before == [6, 5, 4] and after == [4, 5, 6, 7]
    return {"old_graph_digest": old_original["graph_digest"], "unchanged_labels": stable,
            "raised_by_one": raised, "old_quota_three_labels_by_index": before,
            "new_quota_four_labels_by_index": after, "added_edge": ["b:0:1", added]}


def check(root, here, cfg, supplied, state, controls):
    original = load(here / "original.json")
    side, degrees, edges, _ = inspect(original, [[2, 4], [2]])
    low = {v for v in side if side[v] == 0}
    assert low == {"s:0", "b:1:0", "l:0:0:0", "l:0:0:1", "l:0:1:0", "l:0:1:1", "l:0:1:2", "l:0:1:3"}
    assert len(side) == 13 and len(edges) == 12 and sum(degrees.values()) == 24
    correction = {v: (2*side[v]-1)*(d-1) for v, d in degrees.items() if d > 1}
    assert correction == {"s:0": -2, "s:1": 1, "b:0:0": 2, "b:0:1": 4, "b:1:0": -2}
    lows, highs = list(range(8)), list(range(8, 13))
    target = sum(range(1, 13))
    x, e = 3, 12
    alphabet_difference = sum(highs)-sum(lows)
    fixed = alphabet_difference+correction["s:0"]*x+correction["s:1"]*e
    assert (sum(highs), sum(lows), alphabet_difference, fixed, target) == (50, 28, 22, 28, 78)
    neighbors = {v if u == "s:1" else u for u, v in edges if "s:1" in (u, v)}
    assert e == len(edges) and x != 0 and neighbors == {"s:0", "b:1:0"}
    root_zero = next(iter(neighbors - {"s:0"}))
    assert root_zero == "b:1:0"
    free_highs = set(highs)-{e}
    cases = []
    for b in sorted(free_highs):
        a, rest = divmod(target-fixed-correction["b:0:1"]*b, correction["b:0:0"])
        assert rest == 0
        cases.append({"B": b, "forced_A": a, "allowed": a in free_highs-{b}})
    survivor, = [row for row in cases if row["allowed"]]
    assert survivor == {"B": 8, "forced_A": 9, "allowed": True}

    assert state["status"] == "WITNESSED" and state["pair"] == cfg["pair"] == [3, 4]
    assert state["port_labels"] == [x, e] and state["graph_digest"] == original["graph_digest"]
    cert = state["certificate"]
    labels = cert["labels"]
    assert labels == supplied["labels"] and supplied["pair"] == [3, 4]
    assert (labels["b:0:0"], labels["b:0:1"], labels[root_zero]) == (9, 8, 0)
    assert sorted(labels[v] for v in ("l:1:0:0", "l:1:0:1")) == [10, 11]
    fixed_names = {v for v in side if not v.startswith("l:0:")}
    mandatory = [[u, v, abs(labels[u]-labels[v])] for u, v in edges if u in fixed_names and v in fixed_names]
    assert sorted(w for _, _, w in mandatory) == [5, 6, 9, 10, 11, 12]
    remaining_labels = sorted(set(lows)-{labels["s:0"], labels[root_zero]})
    remaining_weights = sorted(set(range(1, 13))-{w for _, _, w in mandatory})
    assert remaining_labels == [1, 2, 4, 5, 6, 7] and remaining_weights == [1, 2, 3, 4, 7, 8]
    weights, identity = ledger(original, labels, side, edges, 8, (3, 4))
    assert cert["edge_rows"] == [edge+[w] for edge, w in zip(edges, weights, strict=True)]
    assert cert["cut"] == 8 and cert["physical_ports"] == cert["witness"] == ["s:0", "s:1"]
    assert cert["port_labels"] == [x, e]
    assert cert["ledger_id"] == identity and cert["graph_digest"] == original["graph_digest"]
    verified = cert["checker"]
    assert verified["valid"] and verified["errors"] == [] and verified["graph_digest"] == original["graph_digest"]
    assert (verified["n"], verified["m"], verified["edge_differences"]) == (13, 12, weights)

    old_original, old_cert, graph_ids = archived_controls(root, cfg, controls)
    assert len(set(graph_ids+[original["graph_digest"]])) == 3
    comparison = compare(old_original, old_cert["labels"], original, labels)
    duplicates = check_adverse(original, edges, labels, controls)
    return {"status": "PASS", "roles_by_side": {"low": sorted(low), "high": sorted(set(side)-low)},
            "degrees": degrees, "signed_corrections": correction, "alphabet_difference_sum": alphabet_difference,
            "fixed_signed_sum": fixed, "required_sum": target, "original_weight_twelve_edge": ["s:1", root_zero],
            "ordered_center_cases": cases, "ordered_center_cases_checked": len(cases),
            "mandatory_edges": mandatory, "remaining_labels": remaining_labels, "remaining_weights": remaining_weights,
            "d085_comparison": comparison, "adverse_duplicate_weights": duplicates,
            "verified_adverse_rejections": 3, "named_assignment_visits": 0, "retained_replay_visits": 0}
