"""Independent arithmetic and original-bound audit. Uses the standard library only."""

from collections import Counter, deque
from hashlib import sha256
from itertools import permutations
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


def center_case(x, e, a, b, base, required, edges):
    result = {"centers": [a, b]}
    z, remainder = divmod(base+e+2*a+3*b-2*x-required, 2)
    if remainder:
        return result | {"code": "P"}
    result["forced_z"] = z
    if z not in range(7) or z == x:
        return result | {"code": "L"}
    c, d = sorted(set(range(7, 12))-{a, b, e})
    captured = {"s:0": x, "s:1": e, "b:0:0": a, "b:0:1": b, "b:1:0": z,
                "l:1:0:0": c, "l:1:0:1": d}
    mandatory = [abs(captured[u]-captured[v]) for u, v in edges if u in captured and v in captured]
    assert len(mandatory) == 6
    result["mandatory"] = mandatory
    for index, weight in enumerate(mandatory):
        if weight in mandatory[:index]:
            return result | {"code": f"R{weight}"}
    free = sorted(set(range(7))-{x, z})
    residual = sorted(set(range(1, 12))-set(mandatory))
    assert len(free) == len(residual) == 5
    result.update(free_lows=free, residual=residual)
    for weight in residual:
        missing = a-weight not in free and b-weight not in free
        if missing:
            return result | {"code": f"M{weight}"}
    return result | {"code": "S"}


def check_controls(root, cfg, original, edges, labels, controls):
    old = cfg["retained_d082"]
    previous = cfg["retained_d084"]
    match_prior_manifest(root, cfg, old, ("strict_original.json", "audit_result.json", "config.json", "enumeration.json"))
    match_prior_manifest(root, cfg, previous, ("result.json",))
    retained = load(root / old / "strict_original.json")
    assert retained["graph_digest"] != original["graph_digest"]
    side, _, retained_edges, _ = inspect(retained, [[2, 2], [2]])
    archive = load(root / previous / "result.json")
    assert archive["status"] == "PASS" and archive["graph_digest"] == retained["graph_digest"]
    positive = [r for r in archive["menu"]["pairs"] if r["status"] == "WITNESSED"]
    assert [r["pair"] for r in positive] == [[2, 0], [3, 4]]
    for old_row, checked in zip(positive, controls["d084_positives"], strict=True):
        pair = old_row["pair"]
        cert = old_row["certificate"]
        weights, identity = ledger(retained, cert["labels"], side, retained_edges, 6, tuple(pair))
        assert checked == {"pair": pair, "ledger_id": identity, "checker": cert["checker"]}
        assert cert["ledger_id"] == identity and checked["checker"]["graph_digest"] == retained["graph_digest"]
        assert checked["checker"]["valid"] and checked["checker"]["edge_differences"] == weights
    prior = load(root / old / "audit_result.json")
    prior_config = load(root / old / "config.json")
    assert prior_config["pins"] == {"s:0": 1, "s:1": 6} and prior_config["cut"] == 6
    assert prior_config["profile"] == [[2, 2], [2]]
    assert prior["status"] == "PASS" and prior["positive_certificates"] == 0
    assert prior["visits_certified"] == prior["duplicate_edge_receipts"] == 2880
    assert prior["raw_receipts"]["strict_original.json"] == cfg["source_hashes"][f"{old}/strict_original.json"]
    archived_hash = cfg["source_hashes"][f"{old}/enumeration.json"]
    assert archived_hash == prior["raw_receipts"]["enumeration.json"]
    assert controls["d082_negative"] == {"pair": [1, 0], "graph_digest": retained["graph_digest"],
                                        "historical_visits": 2880, "positive_certificates": 0,
                                        "new_replay_visits": 0, "historical_receipt_sha256": archived_hash}
    adverse = controls["adverse"]
    assert set(adverse) == {"digest", "port", "difference"}
    bad = adverse["digest"]
    assert bad["expected"] == "0"*64 != original["graph_digest"]
    assert not bad["checker"]["valid"] and bad["checker"]["errors"] == ["original graph digest mismatch"]
    assert bad["checker"]["graph_digest"] == original["graph_digest"]
    assert adverse["port"] == {"valid": False, "reason": "physical offset mismatch", "declared": [2, 0],
                               "actual": [labels["s:0"], labels["s:1"]-7]}
    swap = adverse["difference"]
    u, v = swap["swap"]
    assert [u, v] == ["l:0:0:0", "l:0:1:2"]
    altered = labels | {u: labels[v], v: labels[u]}
    weights = [abs(altered[a]-altered[b]) for a, b in edges]
    assert sorted(altered.values()) == list(range(12))
    assert {w: n for w, n in Counter(weights).items() if n > 1} == {4: 2, 6: 2}
    checker = swap["checker"]
    assert not checker["valid"] and "edge differences repeat" in checker["errors"]
    assert checker["graph_digest"] == original["graph_digest"] and checker["edge_differences"] == weights


def check(root, here, cfg, data, rows, controls):
    original = load(here / "original.json")
    side, degrees, edges, roles = inspect(original, [[2, 3], [2]])
    low = {v for v in side if side[v] == 0}
    assert low == {"s:0", "b:1:0", "l:0:0:0", "l:0:0:1", "l:0:1:0", "l:0:1:1", "l:0:1:2"}
    assert len(side) == 12 and len(edges) == 11 and sum(degrees.values()) == 22
    correction = {v: (2*side[v]-1)*(d-1) for v, d in degrees.items() if d > 1}
    assert correction == {"s:0": -2, "s:1": 1, "b:0:0": 2, "b:0:1": 3, "b:1:0": -2}
    base = sum(range(7, 12))-sum(range(7))
    required = sum(range(1, 12))
    assert base == 24 and required == 66
    assert [row["pair"] for row in rows] == [[2, 0], [3, 4]]
    arithmetic = {}
    for row in rows:
        x, y = row["pair"]
        e = 7+y
        assert row["port_labels"] == [x, e] and row["graph_digest"] == original["graph_digest"]
        assert required-base-e+2*x == (39 if y == 0 else 37)
        # Ordered numerical choices for two centers only, with all first terminals unassigned.
        ordered = permutations(sorted(set(range(7, 12))-{e}), 2)
        cases = [center_case(x, e, a, b, base, required, edges) for a, b in ordered]
        key = f"{x},{y}"
        assert len(cases) == 12
        assert [{k: case[k] for k in ("centers", "code")} for case in cases] == data["cases"][key]
        arithmetic[key] = cases
        survivors = [case for case in cases if case["code"] == "S"]
        if not survivors:
            assert row["status"] == "EXCLUDED" and "certificate" not in row
            continue
        unexcluded, = survivors
        assert row["status"] == "WITNESSED" and row["pair"] == data["witness"]["pair"]
        cert = row["certificate"]
        labels = cert["labels"]
        assert labels == data["witness"]["labels"]
        assert [labels["b:0:0"], labels["b:0:1"]] == unexcluded["centers"]
        assert labels["b:1:0"] == unexcluded["forced_z"] == 0
        weights, identity = ledger(original, labels, side, edges, 7, (x, y))
        assert cert["graph_digest"] == original["graph_digest"] and cert["ledger_id"] == identity
        assert cert["cut"] == 7 and cert["port_labels"] == row["port_labels"]
        assert cert["physical_ports"] == cert["witness"] == ["s:0", "s:1"]
        assert cert["edge_rows"] == [edge+[w] for edge, w in zip(edges, weights, strict=True)]
        valid = cert["checker"]
        assert valid["valid"] and valid["errors"] == [] and valid["graph_digest"] == original["graph_digest"]
        assert valid["n"] == 12 and valid["m"] == 11 and valid["edge_differences"] == weights
    assert [row["status"] for row in rows] == ["EXCLUDED", "WITNESSED"]
    check_controls(root, cfg, original, edges, rows[1]["certificate"]["labels"], controls)
    return {"status": "PASS", "degrees": degrees, "signed_corrections": correction,
            "distance_to_spine": {v: {"spine": 0, "branch": 1, "leaf": 2}[r["kind"]] for v, r in roles.items()},
            "low_vertices": sorted(low), "high_vertices": sorted(set(side)-low),
            "required_difference_sum": required, "alphabet_difference_sum": base,
            "ordered_center_cases": arithmetic, "offset_states": len(rows),
            "ordered_center_cases_checked": sum(map(len, arithmetic.values())), "verified_adverse_rejections": 3,
            "named_assignment_visits": 0, "retained_replay_visits": 0}
