"""Independent arithmetic and original-bound audit. Uses the standard library only."""

from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
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
    return side, {v: len(adjacency[v]) for v in side}, edges


def prove_case(x, y, a, b, edges):
    e = 6+y
    z = a+b-x-12+y//2
    result = {"centers": [a, b], "forced_z": z}
    if z not in range(6) or z == x:
        return result | {"code": "L"}
    c, d = sorted(set(range(6, 11)) - {a, b, e})
    partial = {"s:0": x, "s:1": e, "b:0:0": a, "b:0:1": b, "b:1:0": z,
               "l:1:0:0": c, "l:1:0:1": d}
    mandatory = [abs(partial[u]-partial[v]) for u, v in edges if u in partial and v in partial]
    assert len(mandatory) == 6
    result["mandatory"] = mandatory
    for k, value in enumerate(mandatory):
        if value in mandatory[:k]:
            return result | {"code": f"R{value}"}
    terminal_labels = set(range(6)) - {x, z}
    residual = sorted(set(range(1, 11)) - set(mandatory))
    result.update(free_lows=sorted(terminal_labels), residual=residual)
    for w in residual:
        if a-w not in terminal_labels and b-w not in terminal_labels:
            return result | {"code": f"M{w}"}
    return result | {"code": "W"}


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


def verify_controls(root, cfg, original, edges, labels, controls):
    pos = cfg["control_archive"]
    match_prior_manifest(root, cfg, pos, ("f2_original.json", "certificates.json"))
    f2 = load(root / pos / "f2_original.json")
    f2_state = load(root / pos / "certificates.json")["controls"]["f2"]
    side, _, f2_edges = inspect(f2, [[1, 2], [2]])
    values, identifier = ledger(f2, f2_state["labels"], side, f2_edges, 5, (1, 0))
    assert f2_state["ledger_id"] == identifier
    assert controls["d081_f2"] == f2_state["checker"] and controls["d081_f2"]["valid"]
    assert controls["d081_f2"]["edge_differences"] == values

    neg = cfg["negative_archive"]
    match_prior_manifest(root, cfg, neg, ("strict_original.json", "config.json", "audit_result.json", "enumeration.json"))
    prior = load(root / neg / "audit_result.json")
    prior_config = load(root / neg / "config.json")
    assert prior_config["pins"] == {"s:0": 1, "s:1": 6} and prior_config["cut"] == 6
    assert prior_config["profile"] == [[2, 2], [2]]
    assert prior["status"] == "PASS" and prior["positive_certificates"] == 0
    assert prior["visits_certified"] == prior["duplicate_edge_receipts"] == 2880
    assert prior["raw_receipts"]["strict_original.json"] == cfg["source_hashes"][cfg["original"]]
    assert controls["d082_strict"] == {"pair": [1, 0], "graph_digest": original["graph_digest"],
                                      "historical_visits": 2880, "positive": 0, "new_replay_visits": 0,
                                      "receipt_sha256": cfg["source_hashes"][f"{neg}/enumeration.json"]}
    assert prior["raw_receipts"]["enumeration.json"] == controls["d082_strict"]["receipt_sha256"]

    adverse = controls["adverse"]
    assert set(adverse) == {"digest", "port", "duplicate_difference"}
    wrong_digest = adverse["digest"]
    assert wrong_digest["expected"] == "0"*64 != original["graph_digest"]
    assert not wrong_digest["checker"]["valid"] and wrong_digest["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong_digest["checker"]["graph_digest"] == original["graph_digest"]
    assert adverse["port"] == {"valid": False, "reason": "physical offset mismatch",
                               "declared": [1, 0], "actual": [labels["s:0"], labels["s:1"]-6]}
    changed = adverse["duplicate_difference"]
    u, v = changed["swap"]
    assert [u, v] == ["l:0:0:0", "l:0:1:0"]
    altered = labels | {u: labels[v], v: labels[u]}
    actual = [abs(altered[a]-altered[b]) for a, b in edges]
    assert sorted(altered.values()) == list(range(11))
    assert {k: n for k, n in Counter(actual).items() if n > 1} == {6: 2, 9: 2}
    assert changed["checker"]["edge_differences"] == actual and not changed["checker"]["valid"]
    assert changed["checker"]["graph_digest"] == original["graph_digest"]
    assert "edge differences repeat" in changed["checker"]["errors"]


def check(root, cfg, source, menu, controls):
    original = load(root / cfg["original"])
    side, degrees, edges = inspect(original, [[2, 2], [2]])
    assert len(side) == 11 and len(edges) == 10 and sum(degrees.values()) == 20
    assert {v for v in side if side[v] == 0} == {"s:0", "b:1:0", "l:0:0:0", "l:0:0:1", "l:0:1:0", "l:0:1:1"}
    correction = {v: (2*side[v]-1)*(degree-1) for v, degree in degrees.items() if degree > 1}
    assert correction == {"s:0": -2, "s:1": 1, "b:0:0": 2, "b:0:1": 2, "b:1:0": -2}
    base = sum(range(6, 11)) - sum(range(6))
    assert base == 25 and base+6 == 31 and sum(range(1, 11)) == 55

    order = list(product(range(6), range(5)))
    assert [tuple(row["pair"]) for row in menu["pairs"]] == order
    assert len(source["proof_table"]) == 18
    survivors = []
    checked_cases = {}
    for row, (x, y) in zip(menu["pairs"], order, strict=True):
        assert row["graph_digest"] == original["graph_digest"] and row["port_labels"] == [x, 6+y]
        if y % 2:
            assert (55-31-y) % 2 == 1
            assert row["status"] == "EXCLUDED" and row["proof"] == "signed-degree-parity"
            continue
        candidate_centers = combinations(sorted(set(range(6, 11))-{6+y}), 2)
        cases = [prove_case(x, y, a, b, edges) for a, b in candidate_centers]
        key = f"{x},{y}"
        checked_cases[key] = cases
        assert [case["code"] for case in cases] == source["proof_table"][key]
        matching = [case for case in cases if case["code"] == "W"]
        if not matching:
            assert row["status"] == "EXCLUDED" and row["proof"] == "mandatory-weight-table"
            assert row["claims"] == source["proof_table"][key]
            continue
        assert len(matching) == 1 and row["status"] == "WITNESSED" and row["proof"] == "explicit-ledger"
        certificate = row["certificate"]
        labels = certificate["labels"]
        assert labels == source["ledgers"][key]
        assert sorted([labels["b:0:0"], labels["b:0:1"]]) == matching[0]["centers"]
        assert labels["b:1:0"] == matching[0]["forced_z"]
        weights, identifier = ledger(original, labels, side, edges, 6, (x, y))
        assert certificate["edge_rows"] == [edge+[w] for edge, w in zip(edges, weights, strict=True)]
        assert certificate["physical_ports"] == certificate["witness"] == ["s:0", "s:1"]
        assert certificate["port_labels"] == [x, 6+y] and certificate["cut"] == 6
        assert certificate["graph_digest"] == original["graph_digest"] and certificate["ledger_id"] == identifier
        checker = certificate["checker"]
        assert checker["valid"] and checker["errors"] == [] and checker["graph_digest"] == original["graph_digest"]
        assert checker["n"] == 11 and checker["m"] == 10 and checker["edge_differences"] == weights
        survivors.append({"pair": [x, y], "ledger_id": identifier})

    assert [entry["pair"] for entry in survivors] == [[2, 0], [3, 4]]
    assert len({entry["ledger_id"] for entry in survivors}) == 2
    first, reflected = (source["ledgers"][key] for key in ("2,0", "3,4"))
    assert all(reflected[v] == (5 if side[v] == 0 else 16)-first[v] for v in side)
    assert menu["counts"] == {"WITNESSED": 2, "EXCLUDED": 28, "UNRESOLVED": 0}
    verify_controls(root, cfg, original, edges, first, controls)
    return {"status": "PASS", "degrees": degrees, "signed_degree_corrections": correction,
            "alpha_classes": {"low": sorted(v for v in side if side[v] == 0),
                              "high": sorted(v for v in side if side[v] == 1)},
            "alphabet_difference": base, "fixed_constant": 31, "required_sum": 55,
            "offset_states_checked": len(order), "odd_exit_exclusions": 12,
            "center_value_cases_checked": sum(map(len, checked_cases.values())), "arithmetic_cases": checked_cases,
            "witnesses": survivors, "verified_adverse_rejections": 3, "retained_replay_visits": 0,
            "new_original_graph_identities": 0, "named_assignment_visits": 0}
