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


def symbolic_arithmetic():
    # Coefficients in increasing powers of b, doubled to avoid fractions.
    twice_required = (110, 21, 1)       # (b+10)(b+11)
    twice_low_sum = (20, 9, 1)         # (b+4)(b+5)
    twice_high_sum = (90, 12, 0)       # 2 sum of b+5 through b+10
    twice_port_excess = (4, 2, 0)      # 2 ((b+10) - 2*4)
    twice_center_excess = tuple(required + low - high - ports
                                for required, low, high, ports in zip(
                                    twice_required, twice_low_sum, twice_high_sum,
                                    twice_port_excess, strict=True))
    assert twice_center_excess == (36, 16, 2)  # 2 (3(b+6) + b(b+5))
    return {"center_excess_polynomial_constant_first": [18, 8, 1],
            "variable_edge_band": [1, "b"],
            "fixed_edge_offsets_from_b": list(range(1, 11)),
            "right_terminal_weights": ["b+7", "b+8", "b+9"],
            "right_attachment_weight": "b+10"}


def archived_controls(root, cfg, controls, original, edges):
    checks = []
    retained = zip((("positive_d087", 5, "regression"), ("positive_d086", 4, "state")),
                   controls["retained_positives"], strict=True)
    for (key, b, record), saved in retained:
        path = cfg[key]
        match_prior_manifest(root, cfg, path, ("original.json", "result.json"))
        old = load(root / path / "original.json")
        old_side, _, old_edges, _ = inspect(old, [[2, b], [2]])
        report = load(root / path / "result.json")
        row = report[record]
        assert report["status"] == "PASS" and row["status"] == "WITNESSED" and row["pair"] == [3, 4]
        cert = row["certificate"]
        weights, identifier = ledger(old, cert["labels"], old_side, old_edges, b+4, (3, 4))
        assert cert["graph_digest"] == row["graph_digest"] == old["graph_digest"] == saved["graph_digest"]
        assert cert["ledger_id"] == saved["ledger_id"] == identifier and saved["b"] == b
        assert cert["cut"] == b+4 and cert["port_labels"] == [3, b+8]
        assert cert["witness"] == ["s:0", "s:1"] and cert["physical_ports"] == cert["witness"]
        assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(old_edges, weights, strict=True)]
        assert cert["checker"] == saved["checker"]
        assert saved["checker"]["valid"] and saved["checker"]["edge_differences"] == weights
        checks.append({"b": b, "ledger_id": identifier, "graph_digest": old["graph_digest"]})

    path = cfg["negative_d088"]
    match_prior_manifest(root, cfg, path, ("original.json", "result.json", "command_receipt.json"))
    earlier = load(root / path / "original.json")
    _, _, prior_edges, prior_roles = inspect(earlier, [[3, 2], [2]])
    report = load(root / path / "result.json")
    receipt = load(root / path / "command_receipt.json")
    assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert report["disposition"] == "EXCLUDED" and report["domain"] == {
        "min_b": 2, "exact_integer": True, "offsets": [4, 4]}
    assert report["boundary_graph_digest"] == earlier["graph_digest"] != original["graph_digest"]
    assert receipt["result_sha256"] == cfg["source_hashes"][f"{path}/result.json"]
    assert controls["d088_negative"] == {
        "domain": report["domain"], "graph_digest": earlier["graph_digest"],
        "receipt_sha256": cfg["source_hashes"][f"{path}/command_receipt.json"], "new_replay_visits": 0}
    extra_leaf = "l:1:0:2"
    new_roles = original["graph"]["roles"]
    assert {v: r for v, r in new_roles.items() if v != extra_leaf} == prior_roles
    assert edges == prior_edges + [["b:1:0", extra_leaf]]
    return checks


def adverse_audit(controls, original, labels, edges):
    tests = controls["adverse"]
    false_digest = tests["digest"]
    assert false_digest["expected"] == "0"*64 != original["graph_digest"]
    assert not false_digest["checker"]["valid"]
    assert false_digest["checker"]["errors"] == ["original graph digest mismatch"]
    port = tests["port"]
    assert port == {"valid": False, "reason": "physical offset mismatch",
                    "declared": [4, 4], "actual": [labels["s:0"], labels["s:1"]-7]}
    u, v = tests["difference"]["swap"]
    assert (u, v) == ("l:0:0:0", "l:0:1:0")
    modified = dict(labels)
    modified[u], modified[v] = labels[v], labels[u]
    assert sorted(modified.values()) == list(range(13))
    weights = [abs(modified[x]-modified[y]) for x, y in edges]
    counts = Counter(weights)
    repeated = {str(w): count for w, count in counts.items() if count > 1}
    missing = [w for w in range(1, 13) if not counts[w]]
    difference = tests["difference"]
    assert difference["duplicates"] == repeated == {"3": 2, "6": 2}
    assert difference["missing"] == missing == [2, 7]
    check = difference["checker"]
    assert not check["valid"] and "edge differences repeat" in check["errors"]
    assert check["graph_digest"] == original["graph_digest"] and check["edge_differences"] == weights
    return {"repeated": repeated, "missing": missing}


def check(root, here, cfg, boundary, controls):
    for path, expected in cfg["source_hashes"].items():
        assert sha256((root / path).read_bytes()).hexdigest() == expected
    original = load(here / "original.json")
    side, degrees, edges, _ = inspect(original, [[3, 2], [3]])
    assert len(edges) == 12 and len(side) == 13 and sum(side.values()) == 6
    assert boundary["b"] == 2 and boundary["pair"] == [4, 5]
    assert boundary["status"] == "WITNESSED" and boundary["port_labels"] == [4, 12]
    cert = boundary["certificate"]
    labels = cert["labels"]
    weights, identifier = ledger(original, labels, side, edges, 7, (4, 5))
    assert labels == {
        "s:0": 4, "s:1": 12, "b:0:0": 8, "b:0:1": 7, "b:1:0": 0,
        "l:0:0:0": 1, "l:0:0:1": 2, "l:0:0:2": 3, "l:0:1:0": 5, "l:0:1:1": 6,
        "l:1:0:0": 9, "l:1:0:1": 10, "l:1:0:2": 11}
    assert weights == [8, 4, 7, 6, 5, 3, 2, 1, 12, 9, 10, 11]
    assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
    assert cert["ledger_id"] == identifier
    assert cert["cut"] == 7 and cert["port_labels"] == [4, 12]
    assert cert["witness"] == ["s:0", "s:1"] and cert["physical_ports"] == cert["witness"]
    assert boundary["graph_digest"] == cert["graph_digest"] == original["graph_digest"]
    assert cert["checker"]["graph_digest"] == original["graph_digest"]
    assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
    signed = sum(degrees[v]*label*(2*side[v]-1) for v, label in labels.items())
    degree_excess = {v: (d-1)*(2*side[v]-1) for v, d in degrees.items() if d > 1}
    assert degree_excess == {"s:0": -2, "s:1": 1, "b:0:0": 3, "b:0:1": 2, "b:1:0": -3}
    assert signed == sum(weights) == 78
    return {"status": "PASS", "graph_digest": original["graph_digest"], "ledger_id": identifier,
            "edge_weights": weights, "signed_degree_sum": signed, "degree_excess": degree_excess,
            "symbolic_arithmetic": symbolic_arithmetic(),
            "retained_positives": archived_controls(root, cfg, controls, original, edges),
            "adverse": adverse_audit(controls, original, labels, edges),
            "new_graph_identities": 0, "solver_calls": 0, "enumeration_visits": 0}
