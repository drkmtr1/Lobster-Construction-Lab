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


def read_control(root, cfg, control):
    folder = cfg["retained"]["D094"]
    match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json", "preflight_receipt.json"))
    original = load(root / folder / "original.json")
    report = load(root / folder / "result.json")
    receipt = load(root / folder / "command_receipt.json")
    preflight = load(root / folder / "preflight_receipt.json")
    a_profile = [[2, 2], [2], [3, 2], [3], [3], [3, 2], [2], [2, 2]]
    colors, _, edges, roles = inspect(original, a_profile)
    cert = report["certificate"]
    local = cert["labels"]
    assert report["boundary"] == [2]*4 and report["status"] == receipt["status"] == preflight["status"] == "PASS"
    assert receipt["exit_code"] == 0 and receipt["result_sha256"] == cfg["source_hashes"][f"{folder}/result.json"]
    assert local.keys() == roles.keys() and all(type(v) is int for v in local.values())
    assert sorted(local.values()) == list(range(48))
    assert all(colors[v] == int(value >= 24) for v, value in local.items())
    assert cert["witness"] == original["graph"]["spine"] == [f"s:{i}" for i in range(8)]
    assert cert["ports"] == ["s:0", "s:7"] and cert["cut"] == 24
    assert cert["offsets"] == [local["s:0"], local["s:7"]-24] == [3, 3]
    weights = [abs(local[u]-local[v]) for u, v in edges]
    assert Counter(weights) == Counter(range(1, 48))
    assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
    identifier = digest({"graph_digest": original["graph_digest"], "labels": sorted(local.items())})
    assert cert["ledger_id"] == identifier and cert["graph_digest"] == original["graph_digest"]
    assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
    assert control == {"graph_digest": original["graph_digest"], "ledger_id": identifier, "checker": cert["checker"]}
    return original, local, edges, roles


def verify_d093_custody(root, cfg):
    failed = cfg["retained"]["D093_original_failure"]
    recovery = cfg["retained"]["D093_recovery"]
    failed_manifest = load(root / failed / "MANIFEST.json")
    match_prior_manifest(root, cfg, failed, tuple(row["path"] for row in failed_manifest["files"]))
    failed_receipt = load(root / failed / "external_failure_receipt.json")
    assert failed_manifest["execution_status"] == failed_receipt["status"] == "INCOMPLETE"
    assert failed_receipt["process_cpu_seconds"] is None
    assert all(not (root / failed / name).exists() for name in failed_receipt["absent_internal_outputs"])
    match_prior_manifest(root, cfg, recovery, ("original.json", "result.json", "command_receipt.json", "preflight_receipt.json"))
    recovered = load(root / recovery / "command_receipt.json")
    recovery_manifest = load(root / recovery / "MANIFEST.json")
    assert recovery_manifest["frozen_attempt"]["path"] == failed
    assert recovery_manifest["frozen_attempt"]["status"] == "INCOMPLETE"
    assert recovery_manifest["official_execution"] == recovered["status"] == "PASS"
    assert recovered["exit_code"] == 0 and recovered["result_sha256"] == cfg["source_hashes"][f"{recovery}/result.json"]
    return {"original_attempt": "INCOMPLETE", "versioned_recovery": "PASS", "replayed": False}


def joint_ledger(cert, spine, colors, edges, roles, control):
    old_original, local, old_edges, old_roles = control
    prefixes = {"spine": "s", "branch": "b", "leaf": "l"}
    labels = cert["labels"]
    name_maps = {"B": {}, "A": {}}
    blocks = {}
    label_bands = {"B_low": [], "A_low": [], "A_high": [], "B_high": []}
    partition = {}
    for v, role in roles.items():
        component = "B" if role["section"] < 8 else "A"
        section = role["section"] % 8
        name_parts = [prefixes[role["kind"]], str(section)]
        if "branch" in role:
            name_parts.append(str(role["branch"]))
        if "leaf" in role:
            name_parts.append(str(role["leaf"]))
        source_name = ":".join(name_parts)
        assert old_roles[source_name] == role | {"section": section}
        assert source_name not in name_maps[component]
        name_maps[component][source_name] = v
        partition[v] = component
        value = local[source_name]
        low = value < 24
        assert low == (colors[v] == 0)
        shift = 24 if component == "A" else (0 if low else 48)
        assert labels[v] == value+shift
        label_bands[f"{component}_{'low' if low else 'high'}"].append(labels[v])
    assert cert["A_name_embedding"] == name_maps["A"]
    expected_edge_weights = {}
    for key, mapping in name_maps.items():
        assert mapping.keys() == old_roles.keys()
        witness = [mapping[v] for v in old_original["graph"]["spine"]]
        blocks[key] = {"source": "D094", "labels": {mapping[v]: value for v, value in local.items()},
                       "cut": 24, "witness": witness}
        for u, v in old_edges:
            pair = tuple(sorted([mapping[u], mapping[v]]))
            assert pair not in expected_edge_weights
            expected_edge_weights[pair] = abs(local[u]-local[v]) + (48 if key == "B" else 0)
    assert blocks == cert["blocks"] and blocks["B"]["witness"]+blocks["A"]["witness"] == spine
    u, v = blocks["B"]["witness"][-1], blocks["A"]["witness"][0]
    assert [u, v] == ["s:7", "s:8"]
    assert blocks["B"]["labels"][u]-24 == blocks["A"]["labels"][v] == 3
    connector = [u, v]
    edge_multiset = Counter(tuple(sorted(e)) for e in edges)
    assert edge_multiset == Counter(expected_edge_weights.keys()) + Counter({tuple(connector): 1})
    assert (labels[u], labels[v]) == (75, 27)
    assert cert["connector"] == {"edge": connector, "weight": labels[u]-labels[v]}
    groups = {"A_internal": [], "connector": [], "B_internal": []}
    rows = []
    for u, v in edges:
        weight = abs(labels[u]-labels[v])
        if partition[u] != partition[v]:
            assert [u, v] == connector and weight == 48
            group = "connector"
        else:
            assert weight == expected_edge_weights[tuple(sorted([u, v]))]
            group = f"{partition[u]}_internal"
        groups[group].append(weight)
        rows.append([u, v, weight])
    bands = {key: sorted(values) for key, values in groups.items()}
    label_bands = {key: sorted(values) for key, values in label_bands.items()}
    assert label_bands == {"B_low": list(range(24)), "A_low": list(range(24, 48)),
                           "A_high": list(range(48, 72)), "B_high": list(range(72, 96))}
    assert bands == {"A_internal": list(range(1, 48)), "connector": [48],
                     "B_internal": list(range(49, 96))}
    weights = [row[2] for row in rows]
    inventory = {"labels": label_bands, "differences": bands,
                 "unused_labels": sorted(set(range(96))-set(labels.values())),
                 "unused_differences": sorted(set(range(1, 96))-set(weights))}
    assert inventory == cert["inventories"] and inventory["unused_labels"] == inventory["unused_differences"] == []
    return inventory, rows, weights


def adverse_audit(original, cert, edges, weights, probes, inventory):
    wrong_digest = probes["digest"]
    assert wrong_digest["expected"] == "0"*64 != original["graph_digest"]
    assert wrong_digest["checker"] == cert["checker"] | {
        "valid": False, "errors": ["original graph digest mismatch"]}
    wrong_connector = probes["physical_connector"]
    assert wrong_connector == {"declared": ["s:7", "s:9"], "valid": False,
                               "error": "connector must be the actual U_B--L_A spine edge"}
    assert ["s:7", "s:9"] not in edges and ["s:9", "s:7"] not in edges
    wrong_inventory = probes["difference_inventory"]
    assert wrong_inventory == {"declared": inventory["differences"] | {"connector": []}, "valid": False,
                               "error": "claimed difference inventory disagrees with the original edges"}
    expected = Counter(weights)
    declared = Counter(w for interval in wrong_inventory["declared"].values() for w in interval)
    assert expected-declared == Counter({48: 1}) and not declared-expected
    return {"rejections": 3, "omitted_connector_weight": 48, "declared_connector_is_original_edge": False}


def check(root, here, cfg, cert, control, probes):
    for path, expected in cfg["source_hashes"].items():
        assert sha256((root / path).read_bytes()).hexdigest() == expected
    source = read_control(root, cfg, control)
    original = load(here / "original.json")
    profile = [[2, 2], [2], [3, 2], [3], [3], [3, 2], [2], [2, 2],
               [2, 2], [2], [3, 2], [3], [3], [3, 2], [2], [2, 2]]
    colors, _, edges, roles = inspect(original, profile)
    assert len(roles) == 96 and len(edges) == 95 and sum(not high for high in colors.values()) == 48
    labels = cert["labels"]
    spine = [f"s:{i}" for i in range(16)]
    assert labels.keys() == roles.keys() and all(type(value) is int for value in labels.values())
    assert sorted(labels.values()) == list(range(96))
    assert all(colors[v] == int(labels[v] >= 48) for v in labels) and cert["cut"] == 48
    assert cert["witness"] == spine == original["graph"]["spine"]
    assert cert["spine_labels"] == [labels[v] for v in spine] == [
        3, 95, 10, 90, 18, 82, 23, 75, 27, 71, 34, 66, 42, 58, 47, 51]
    assert cert["ports"] == ["s:0", "s:15"] and cert["offsets"] == [labels["s:0"], labels["s:15"]-48] == [3, 3]
    inventory, rows, weights = joint_ledger(cert, spine, colors, edges, roles, source)
    assert Counter(weights) == Counter(range(1, 96)) and cert["edge_rows"] == rows
    identifier = digest({"graph_digest": original["graph_digest"], "labels": sorted(labels.items())})
    assert cert["graph_digest"] == cert["checker"]["graph_digest"] == original["graph_digest"] != control["graph_digest"]
    assert cert["ledger_id"] == identifier != control["ledger_id"]
    assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
    return {"status": "PASS", "graph_digest": original["graph_digest"], "ledger_id": identifier,
            "cut": cert["cut"], "spine_labels": cert["spine_labels"], "connector": cert["connector"],
            "inventories": inventory, "edge_rows": rows, "adverse": adverse_audit(original, cert, edges, weights, probes, inventory),
            "D093_custody": verify_d093_custody(root, cfg),
            "component_embeddings_verified": 2, "new_graph_identities": 0,
            "solver_calls": 0, "enumeration_visits": 0}
