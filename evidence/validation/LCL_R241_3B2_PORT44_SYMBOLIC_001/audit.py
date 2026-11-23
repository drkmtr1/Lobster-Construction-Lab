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


def extremal_audit(side, edges, m):
    low = {v for v in side if side[v] == 0}
    high = set(side)-low
    right = {"l:1:0:0", "l:1:0:1"}
    left = {"b:0:0", "b:0:1"}
    assert high == {"s:1"} | right | left
    adjacent = {frozenset((u, v)) for u, v in edges}
    neighbors = {v: {w for w in side if frozenset((v, w)) in adjacent} for v in side}
    assert neighbors["s:1"] == {"s:0", "b:1:0"}
    assert all(neighbors[v] == {"b:1:0"} for v in right)

    # High labels are represented by their deficits from m. Before both right
    # places are forced, keep both names available for any individual right label.
    known = {0: {"s:1"}}
    zero_at = None
    representations = []
    for k in range(4):
        supports = []
        occupied_right = len(known)-1
        unforced = left | (right if occupied_right < 2 else set())
        for smaller in range(k+1):
            deficit = k-smaller
            high_names = known.get(deficit, unforced)
            low_names = {zero_at} if smaller == 0 and zero_at else low-{"s:0", zero_at}
            possible = [[u, v] for u in sorted(high_names) for v in sorted(low_names)
                        if frozenset((u, v)) in adjacent]
            row = {"required_weight_deficit": k, "high_label_deficit": deficit,
                   "low_label": smaller, "boundary_high_label": m-deficit,
                   "boundary_weight": m-k, "possible_named_edges": possible}
            representations.append(row)
            if possible:
                supports.append(row)
        if k == 0:
            only, = supports
            assert only["possible_named_edges"] == [["s:1", "b:1:0"]]
            zero_at = "b:1:0"
        elif k in {1, 2}:
            only, = supports
            assert only["high_label_deficit"] == k and only["low_label"] == 0
            assert only["possible_named_edges"] == [[u, zero_at] for u in sorted(right)]
            known[k] = right
        else:
            assert not supports and occupied_right == 2
            assert all(zero_at not in neighbors[v] for v in left)
    assert len(representations) == len({(r["high_label_deficit"], r["low_label"]) for r in representations}) == 10
    return representations


def signed_audit(degree, side, m):
    correction = {v: (2*side[v]-1)*(d-1) for v, d in degree.items() if d > 1}
    assert correction == {"s:0": -2, "s:1": 1, "b:0:0": 3, "b:0:1": 2, "b:1:0": -2}
    # Coefficients in ascending powers of b, after clearing the denominator 2.
    def product(a, c):
        return [a*c, a+c, 1]

    required_twice = product(9, 10)
    low_sum_twice = product(4, 5)
    high_sum_twice = [5*(5+9), 5*2, 0]
    port_twice = [2*(9-8), 2, 0]
    center_twice = [r+l-h-p for r, l, h, p in zip(
        required_twice, low_sum_twice, high_sum_twice, port_twice, strict=True)]
    assert center_twice == [38, 16, 2]
    center_coefficients = [value//2 for value in center_twice]
    boundary_constant = sum(range(1, m+1)) - sum(
        (2*side[v]-1)*degree[v]*label for v, label in {"s:0": 4, "s:1": m}.items())
    # Restore the contribution of each port at unit degree, already in the alphabets.
    boundary_constant += m-4
    boundary_constant -= sum(range(7, 12))-sum(range(7))
    assert boundary_constant == sum(coefficient*2**i for i, coefficient in enumerate(center_coefficients)) == 39

    # 3a+bd=4. d=0 is impossible; a>=2 is too large; a=1 would give bd=1.
    # Thus a=0, and we check only the proper positive divisors permitted for d.
    assert 4 % 3 and 3*2 > 4 and 2*1 > 4-3
    cases = sorted((4//d, 0, d) for d in range(1, 4) if 4 % d == 0 and 4//d >= 2)
    assert cases == [(2, 0, 2), (4, 0, 1)]
    residual = []
    for b, a, d in cases:
        A, B, e = b+5+a, b+5+d, b+9
        right = sorted(set(range(b+5, e))-{A, B})
        fixed_weights = sorted([e-4, A-4, B-4, e]+right)
        assert len(set(fixed_weights)) == 6 and B not in fixed_weights
        assert max(A, B) == B
        residual.append({"b": b, "a": a, "d": d, "A": A, "B": B, "right_labels": right,
                         "mandatory_weights": fixed_weights, "absent_weight": B, "left_terminal_upper_bound": B-1})
    assert [row["mandatory_weights"] for row in residual] == [[3,5,7,8,10,11], [5,6,9,11,12,13]]
    return {"boundary_signed_corrections": correction, "center_equation_coefficients": center_coefficients,
            "boundary_center_equation_rhs": boundary_constant, "residual_cases": residual,
            "shared_premise": "b:1:0=0 from the maximum edge"}


def check_controls(root, cfg, controls, boundary_digest):
    records = [(87, cfg["positive_d087"], "regression", 5), (86, cfg["positive_d086"], "state", 4)]
    control_digests = {boundary_digest}
    for row, saved in zip(records, controls["retained_positives"], strict=True):
        decision, folder, key, b = row
        match_prior_manifest(root, cfg, folder, ("original.json", "result.json"))
        original = load(root / folder / "original.json")
        result = load(root / folder / "result.json")
        assert result["status"] == "PASS" and result["graph_digest"] == original["graph_digest"]
        assert result[key]["status"] == "WITNESSED" and result[key]["pair"] == [3, 4]
        cert = result[key]["certificate"]
        side, _, edges, _ = inspect(original, [[2, b], [2]])
        weights, identity = ledger(original, cert["labels"], side, edges, b+4, (3, 4))
        assert cert["graph_digest"] == original["graph_digest"] and cert["ledger_id"] == identity
        assert saved == {"decision": decision, "pair": [3, 4], "graph_digest": original["graph_digest"],
                         "ledger_id": identity, "checker": cert["checker"]}
        assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
        control_digests.add(original["graph_digest"])
        if decision == 87:
            adverse_original, adverse_edges, labels = original, edges, cert["labels"]
    assert len(control_digests) == 3
    prior = cfg["negative_d082"]
    match_prior_manifest(root, cfg, prior, ("strict_original.json", "config.json", "audit_result.json", "enumeration.json"))
    negative = load(root / prior / "audit_result.json")
    pins = load(root / prior / "config.json")
    assert pins["profile"] == [[2, 2], [2]] and pins["cut"] == 6 and pins["pins"] == {"s:0": 1, "s:1": 6}
    assert negative["status"] == "PASS" and negative["positive_certificates"] == 0
    assert negative["visits_certified"] == negative["duplicate_edge_receipts"] == 2880
    assert negative["raw_receipts"]["strict_original.json"] == cfg["source_hashes"][f"{prior}/strict_original.json"]
    expected_hash = cfg["source_hashes"][f"{prior}/enumeration.json"]
    assert negative["raw_receipts"]["enumeration.json"] == expected_hash
    retained = load(root / prior / "strict_original.json")
    assert controls["d082_negative"] == {"pair": [1, 0], "graph_digest": retained["graph_digest"],
                                        "historical_visits": 2880, "positive_certificates": 0,
                                        "new_replay_visits": 0, "historical_receipt_sha256": expected_hash}
    assert controls["adverse_original_digest"] == adverse_original["graph_digest"]
    adverse = controls["adverse"]
    assert set(adverse) == {"digest", "port", "difference"}
    wrong = adverse["digest"]
    assert wrong["expected"] == "0"*64 != adverse_original["graph_digest"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert wrong["checker"]["graph_digest"] == adverse_original["graph_digest"]
    assert adverse["port"] == {"valid": False, "reason": "physical offset mismatch", "declared": [3, 3],
                               "actual": [labels["s:0"], labels["s:1"]-9]}
    swap = adverse["difference"]
    u, v = swap["swap"]
    assert [u, v] == ["l:0:0:0", "l:0:1:0"]
    altered = labels | {u: labels[v], v: labels[u]}
    assert sorted(altered.values()) == list(range(14))
    weights = [abs(altered[x]-altered[y]) for x, y in adverse_edges]
    repeated = {w: n for w, n in Counter(weights).items() if n > 1}
    assert repeated == {6: 2, 8: 2}
    assert sorted(set(range(1, 14))-set(weights)) == [5, 9]
    check = swap["checker"]
    assert not check["valid"] and "edge differences repeat" in check["errors"]
    assert check["graph_digest"] == adverse_original["graph_digest"] and check["edge_differences"] == weights
    return repeated


def check(root, here, cfg, controls):
    original = load(here / "original.json")
    b = cfg["boundary_b"]
    assert b == 2 and cfg["domain"] == {"min_b": 2, "exact_integer": True, "offsets": [4, 4]}
    side, degree, edges, _ = inspect(original, [[3, b], [2]])
    assert len(side) == b+10 and len(edges) == b+9
    assert sum(value == 0 for value in side.values()) == b+5
    representations = extremal_audit(side, edges, len(edges))
    assert len(representations) <= cfg["limits"]["max_extremal_representations"]
    assert {r["boundary_weight"] for r in representations if not r["possible_named_edges"]
            and r["required_weight_deficit"] == 3} == {8}
    signed = signed_audit(degree, side, len(edges))
    duplicates = check_controls(root, cfg, controls, original["graph_digest"])
    return {"status": "PASS", "boundary_b": b, "boundary_graph_digest": original["graph_digest"],
            "boundary_n": len(side), "boundary_m": len(edges), "boundary_cut": b+5,
            "physical_ports": {"s:0": 4, "s:1": b+9}, "spine_witness": ["s:0", "s:1"],
            "boundary_missing_difference": len(edges)-3, "symbolic_missing_weight_deficit": 3,
            "extremal_representations": representations, "signed_degree": signed,
            "verified_adverse_rejections": 3, "adverse_duplicate_weights": duplicates,
            "named_assignment_visits": 0, "retained_replay_visits": 0}
