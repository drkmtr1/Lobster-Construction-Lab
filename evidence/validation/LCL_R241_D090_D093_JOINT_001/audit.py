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


def read_controls(root, cfg, controls):
    verified = {}
    profiles = {"D090": [[2, 2], [2], [3, 2], [3]], "D093": [[3], [3, 2], [2], [2, 2]]}
    for kind, cut, offsets in (("D090", 13, [3, 5]), ("D093", 11, [5, 3])):
        folder = cfg["retained"][kind]
        match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json"))
        orig = load(root / folder / "original.json")
        report = load(root / folder / "result.json")
        receipt = load(root / folder / "command_receipt.json")
        opposite, _, edges, roles = inspect(orig, profiles[kind])
        cert = report["certificate"]
        f = cert["labels"]
        assert report["boundary"] == [2, 2] and report["status"] == receipt["status"] == "PASS"
        assert receipt["exit_code"] == 0 and receipt["result_sha256"] == cfg["source_hashes"][f"{folder}/result.json"]
        assert f.keys() == roles.keys() and all(type(label) is int for label in f.values())
        assert sorted(f.values()) == list(range(24)) and cert["cut"] == cut
        assert all(opposite[v] == int(label >= cut) for v, label in f.items())
        assert cert["witness"] == orig["graph"]["spine"] == ["s:0", "s:1", "s:2", "s:3"]
        assert cert["ports"] == ["s:0", "s:3"] and cert["offsets"] == [f["s:0"], f["s:3"]-cut] == offsets
        weights = [abs(f[u]-f[v]) for u, v in edges]
        assert Counter(weights) == Counter(range(1, 24))
        assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
        identifier = digest({"graph_digest": orig["graph_digest"], "labels": sorted(f.items())})
        assert controls[kind] == {"graph_digest": orig["graph_digest"], "ledger_id": identifier,
                                  "checker": cert["checker"]}
        assert cert["ledger_id"] == identifier and cert["graph_digest"] == orig["graph_digest"]
        assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
        verified[kind] = (orig, f, edges, roles)
    assert controls["D090"]["graph_digest"] != controls["D093"]["graph_digest"]
    assert controls["D090"]["ledger_id"] != controls["D093"]["ledger_id"]
    return verified


def archived_negatives(root, cfg):
    stored = {}
    for task, quota in (("D091", 2), ("D092", 3)):
        folder = cfg["retained"][task]
        match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json"))
        orig = load(root / folder / "original.json")
        report = load(root / folder / "result.json")
        receipt = load(root / folder / "command_receipt.json")
        assert orig["graph"]["profile"] == [[4], [quota]]
        assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
        assert report["disposition"] == "EXCLUDED" and report["domain"]["offsets"] == [5, 3]
        assert report["graph_digest"] == orig["graph_digest"]
        assert receipt["result_sha256"] == cfg["source_hashes"][f"{folder}/result.json"]
        stored[task] = {"disposition": "EXCLUDED", "graph_digest": orig["graph_digest"], "replayed": False}
    folder = cfg["retained"]["D093_original_failure"]
    manifest = load(root / folder / "MANIFEST.json")
    match_prior_manifest(root, cfg, folder, tuple(row["path"] for row in manifest["files"]))
    failed = load(root / folder / "external_failure_receipt.json")
    assert manifest["execution_status"] == failed["status"] == "INCOMPLETE"
    assert failed["process_cpu_seconds"] is None and failed["observed_counts"]["new_certificates"] == 0
    assert all(not (root / folder / name).exists() for name in failed["absent_internal_outputs"])
    stored["D093_original_failure"] = {"disposition": "INCOMPLETE", "replayed": False}
    return stored


def map_components(roles, sources):
    prefixes = {"spine": "s", "branch": "b", "leaf": "l"}
    mappings = {"B": {}, "A": {}}
    partition = {}
    for v, role in roles.items():
        index = role["section"]
        block = "B" if index < 4 else "A"
        local_section = index if block == "B" else index-4
        fields = [prefixes[role["kind"]], str(local_section)]
        if "branch" in role:
            fields.append(str(role["branch"]))
        if "leaf" in role:
            fields.append(str(role["leaf"]))
        name = ":".join(fields)
        archived_roles = sources["D090" if block == "B" else "D093"][3]
        assert archived_roles[name] == role | {"section": local_section}
        assert name not in mappings[block]
        mappings[block][name] = v
        partition[v] = block
    assert mappings["B"].keys() == sources["D090"][3].keys()
    assert mappings["A"].keys() == sources["D093"][3].keys()
    return mappings, partition


def joint_ledger(original, cert, side, edges, roles, sources):
    mapping, partition = map_components(roles, sources)
    assert cert["A_name_embedding"] == mapping["A"]
    labels = cert["labels"]
    class_labels = {"B_low": [], "A_low": [], "A_high": [], "B_high": []}
    source_ledger = {}
    local_edge_weights = {}
    for block, kind, cut in (("B", "D090", 13), ("A", "D093", 11)):
        orig, local, local_edges, _ = sources[kind]
        name_map = mapping[block]
        supplied = {name_map[v]: f for v, f in local.items()}
        witness = [name_map[v] for v in orig["graph"]["spine"]]
        assert cert["blocks"][block] == {"source": kind, "labels": supplied, "cut": cut, "witness": witness}
        for v, raw in supplied.items():
            low = raw < cut
            assert low == (side[v] == 0)
            shift = 13 if block == "A" else (0 if low else 24)
            assert labels[v] == raw+shift
            class_labels[f"{block}_{'low' if low else 'high'}"].append(labels[v])
        source_ledger[block] = witness
        for u, v in local_edges:
            key = tuple(sorted((name_map[u], name_map[v])))
            assert key not in local_edge_weights
            local_edge_weights[key] = abs(local[u]-local[v])
    assert source_ledger["B"] + source_ledger["A"] == cert["witness"] == original["graph"]["spine"]
    middle = [source_ledger["B"][-1], source_ledger["A"][0]]
    assert middle == ["s:3", "s:4"]
    edge_index = Counter(tuple(sorted(e)) for e in edges)
    assert edge_index == Counter(local_edge_weights.keys()) + Counter({tuple(middle): 1})
    assert cert["blocks"]["B"]["labels"]["s:3"]-13 == cert["blocks"]["A"]["labels"]["s:4"] == 5

    weight_groups = {"A_internal": [], "connector": [], "B_internal": []}
    rows = []
    for u, v in edges:
        weight = abs(labels[u]-labels[v])
        if partition[u] != partition[v]:
            assert [u, v] == middle and weight == 24
            group = "connector"
        else:
            group = f"{partition[u]}_internal"
            source_weight = local_edge_weights[tuple(sorted([u, v]))]
            assert weight == source_weight+(24 if partition[u] == "B" else 0)
        weight_groups[group].append(weight)
        rows.append([u, v, weight])
    bands = {key: sorted(values) for key, values in weight_groups.items()}
    label_bands = {key: sorted(values) for key, values in class_labels.items()}
    assert label_bands == {"B_low": list(range(13)), "A_low": list(range(13, 24)),
                           "A_high": list(range(24, 37)), "B_high": list(range(37, 48))}
    assert bands == {"A_internal": list(range(1, 24)), "connector": [24],
                     "B_internal": list(range(25, 48))}
    weights = [row[2] for row in rows]
    inventory = {"labels": label_bands, "differences": bands,
                 "unused_labels": sorted(set(range(48))-set(labels.values())),
                 "unused_differences": sorted(set(range(1, 48))-set(weights))}
    assert inventory == cert["inventories"] and inventory["unused_labels"] == inventory["unused_differences"] == []
    assert cert["connector"] == {"edge": middle, "weight": abs(labels["s:3"]-labels["s:4"])}
    return inventory, rows, weights


def adverse_audit(original, cert, edges, weights, probes, inventory):
    wrong_digest = probes["digest"]
    assert wrong_digest["expected"] == "0"*64 != original["graph_digest"]
    assert wrong_digest["checker"] == cert["checker"] | {
        "valid": False, "errors": ["original graph digest mismatch"]}
    wrong_connector = probes["physical_connector"]
    assert wrong_connector == {"declared": ["s:3", "s:5"], "valid": False,
                               "error": "connector must be the actual U_B--L_A spine edge"}
    assert ["s:3", "s:5"] not in edges and ["s:5", "s:3"] not in edges
    wrong_inventory = probes["difference_inventory"]
    assert wrong_inventory == {"declared": inventory["differences"] | {"connector": []}, "valid": False,
                               "error": "claimed difference inventory disagrees with the original edges"}
    expected = Counter(weights)
    declared = Counter(w for interval in wrong_inventory["declared"].values() for w in interval)
    assert expected-declared == Counter({24: 1}) and not declared-expected
    return {"rejections": 3, "omitted_connector_weight": 24, "declared_connector_is_original_edge": False}


def check(root, here, cfg, cert, controls, probes):
    for path, expected in cfg["source_hashes"].items():
        assert sha256((root / path).read_bytes()).hexdigest() == expected
    sources = read_controls(root, cfg, controls)
    original = load(here / "original.json")
    side, _, edges, roles = inspect(original, [[2, 2], [2], [3, 2], [3], [3], [3, 2], [2], [2, 2]])
    assert len(roles) == 48 and len(edges) == 47 and sum(not high for high in side.values()) == 24
    labels = cert["labels"]
    assert labels.keys() == roles.keys() and all(type(value) is int for value in labels.values())
    assert sorted(labels.values()) == list(range(48))
    assert all(side[v] == int(labels[v] >= 24) for v in labels) and cert["cut"] == 24
    assert cert["witness"] == [f"s:{i}" for i in range(8)]
    assert cert["spine_labels"] == [labels[v] for v in cert["witness"]] == [3, 47, 10, 42, 18, 34, 23, 27]
    assert cert["ports"] == ["s:0", "s:7"] and cert["offsets"] == [labels["s:0"], labels["s:7"]-24] == [3, 3]
    inventory, rows, weights = joint_ledger(original, cert, side, edges, roles, sources)
    assert Counter(weights) == Counter(range(1, 48)) and cert["edge_rows"] == rows
    identifier = digest({"graph_digest": original["graph_digest"], "labels": sorted(labels.items())})
    assert cert["graph_digest"] == cert["checker"]["graph_digest"] == original["graph_digest"]
    assert cert["ledger_id"] == identifier and all(identifier != c["ledger_id"] for c in controls.values())
    assert all(original["graph_digest"] != c["graph_digest"] for c in controls.values())
    assert cert["checker"]["valid"] and cert["checker"]["edge_differences"] == weights
    return {"status": "PASS", "graph_digest": original["graph_digest"], "ledger_id": identifier,
            "cut": cert["cut"], "spine_labels": cert["spine_labels"], "connector": cert["connector"],
            "inventories": inventory, "edge_rows": rows, "adverse": adverse_audit(original, cert, edges, weights, probes, inventory),
            "negative_bindings_without_replay": archived_negatives(root, cfg),
            "new_graph_identities": 0, "solver_calls": 0, "enumeration_visits": 0}
