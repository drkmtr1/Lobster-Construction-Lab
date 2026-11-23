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
    for source, key, profile, cut, pair in (
            ("D087", "regression", [[2, 5], [2]], 9, (3, 4)),
            ("D089", "boundary", [[3, 2], [3]], 7, (4, 5))):
        folder = cfg["archives"][source]
        match_prior_manifest(root, cfg, folder, ("original.json", "result.json"))
        original = load(root / folder / "original.json")
        report = load(root / folder / "result.json")
        assert report["status"] == "PASS" and report[key]["status"] == "WITNESSED"
        cert = report[key]["certificate"]
        side, _, edges, _ = inspect(original, profile)
        weights, identifier = ledger(original, cert["labels"], side, edges, cut, pair)
        saved = controls["positives"][source]
        assert saved["graph_digest"] == cert["graph_digest"] == original["graph_digest"]
        assert saved["ledger_id"] == cert["ledger_id"] == identifier and saved["offsets"] == list(pair)
        assert cert["witness"] == ["s:0", "s:1"] and cert["physical_ports"] == cert["witness"]
        assert cert["port_labels"] == [pair[0], cut+pair[1]] and cert["cut"] == cut
        assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
        assert saved["checker"] == cert["checker"] and saved["checker"]["valid"]
        assert saved["checker"]["edge_differences"] == weights

    folder = cfg["archives"]["D088"]
    match_prior_manifest(root, cfg, folder, ("original.json", "result.json", "command_receipt.json"))
    original = load(root / folder / "original.json")
    inspect(original, [[3, 2], [2]])
    report = load(root / folder / "result.json")
    receipt = load(root / folder / "command_receipt.json")
    assert report["status"] == receipt["status"] == "PASS" and receipt["exit_code"] == 0
    assert report["disposition"] == "EXCLUDED" and report["domain"] == {
        "min_b": 2, "exact_integer": True, "offsets": [4, 4]}
    assert report["boundary_graph_digest"] == original["graph_digest"]
    assert receipt["result_sha256"] == cfg["source_hashes"][f"{folder}/result.json"]
    assert controls["D088"] == {"domain": report["domain"], "graph_digest": original["graph_digest"],
                               "receipt_sha256": cfg["source_hashes"][f"{folder}/command_receipt.json"],
                               "replay_visits": 0}
    return {"positive_archives": ["D087", "D089"], "scoped_negative_archive": "D088"}


def split_inventories(cert, labels, side, edges, roles):
    block = {v: "B" if role["section"] < 2 else "A" for v, role in roles.items()}
    cross = [(u, v) for u, v in edges if block[u] != block[v]]
    assert cross == [("s:1", "s:2")]
    assert cert["connector"] == {"edge": list(cross[0]), "weight": labels["s:1"]-labels["s:2"]}
    assert cert["connector"]["weight"] == 13

    # Recover the local maps by undoing the stated translations on the independently checked labels.
    recovered = {
        "B": {v: labels[v]-13*side[v] for v in block if block[v] == "B"},
        "A": {v: labels[v]-6 for v in block if block[v] == "A"},
    }
    specs = {"B": (11, 6, ["s:0", "s:1"], [3, 4], "D087"),
             "A": (13, 7, ["s:2", "s:3"], [4, 5], "D089")}
    label_bands = {}
    difference_bands = {"connector": [labels["s:1"]-labels["s:2"]]}
    input_offsets = {}
    for key, (order, cut, ports, offsets, source) in specs.items():
        local = recovered[key]
        assert sorted(local.values()) == list(range(order))
        assert all(side[v] == int(local[v] >= cut) for v in local)
        assert cert["blocks"][key] == {"source": source, "labels": local, "cut": cut, "ports": ports}
        entrance, exit_port = ports
        input_offsets[key] = [local[entrance], local[exit_port]-cut]
        assert input_offsets[key] == offsets and ports in edges
        internal = [(u, v) for u, v in edges if block[u] == block[v] == key]
        assert sorted(abs(local[u]-local[v]) for u, v in internal) == list(range(1, order))
        difference_bands[f"{key}_internal"] = sorted(abs(labels[u]-labels[v]) for u, v in internal)
        label_bands[f"{key}_low"] = sorted(labels[v] for v in local if not side[v])
        label_bands[f"{key}_high"] = sorted(labels[v] for v in local if side[v])
    assert input_offsets["B"][1] == input_offsets["A"][0] == 4
    assert label_bands == {"B_low": list(range(6)), "A_low": list(range(6, 13)),
                           "A_high": list(range(13, 19)), "B_high": list(range(19, 24))}
    assert difference_bands == {"A_internal": list(range(1, 13)), "connector": [13],
                                "B_internal": list(range(14, 24))}
    unused_labels = sorted(set(range(24)) - {value for values in label_bands.values() for value in values})
    unused_differences = sorted(set(range(1, 24)) - {value for values in difference_bands.values() for value in values})
    assert unused_labels == unused_differences == []
    checked = {"labels": label_bands, "differences": difference_bands,
               "unused_labels": unused_labels, "unused_differences": unused_differences}
    assert cert["inventories"] == checked
    return checked, input_offsets


def adverse_audit(controls, original, edges, cert, weights, inventories):
    outcomes = controls["adverse"]
    false_digest = outcomes["digest"]
    assert false_digest["expected_digest"] == "0"*64 != original["graph_digest"]
    assert false_digest["checker"] == cert["checker"] | {"valid": False,
                                                        "errors": ["original graph digest mismatch"]}
    connector = outcomes["physical_connector"]
    assert connector == {"declared": ["s:1", "s:3"], "valid": False,
                         "error": "connector must be the actual U_B--L_A spine edge"}
    assert connector["declared"] not in edges and connector["declared"] != cert["connector"]["edge"]
    resource = outcomes["difference_inventory"]
    actual = inventories["differences"]
    assert resource == {"declared": actual | {"connector": []}, "valid": False,
                        "error": "claimed difference inventory disagrees with the original edges"}
    complete = Counter(weights)
    declared = Counter(w for band in resource["declared"].values() for w in band)
    assert complete-declared == Counter({13: 1}) and not declared-complete
    return {"missing_connector_weight": 13, "valid_digest_bound": original["graph_digest"],
            "false_connector_is_original_edge": False}


def check(root, here, cfg, cert, controls):
    for path, expected in cfg["source_hashes"].items():
        assert sha256((root / path).read_bytes()).hexdigest() == expected
    original = load(here / "original.json")
    side, _, edges, roles = inspect(original, [[2, 2], [2], [3, 2], [3]])
    boundary_labels = {
        "s:0": 3, "s:1": 23, "s:2": 10, "s:3": 18,
        "b:0:0": 20, "l:0:0:0": 1, "l:0:0:1": 2, "b:0:1": 19, "l:0:1:0": 4, "l:0:1:1": 5,
        "b:1:0": 0, "l:1:0:0": 21, "l:1:0:1": 22,
        "b:2:0": 14, "l:2:0:0": 7, "l:2:0:1": 8, "l:2:0:2": 9, "b:2:1": 13, "l:2:1:0": 11, "l:2:1:1": 12,
        "b:3:0": 6, "l:3:0:0": 15, "l:3:0:1": 16, "l:3:0:2": 17,
    }
    labels = cert["labels"]
    assert labels == boundary_labels and labels.keys() == roles.keys()
    assert all(type(value) is int for value in labels.values()) and sorted(labels.values()) == list(range(24))
    assert len(edges) == 23 and len(roles) == 24 and sum(not value for value in side.values()) == 13
    assert all(side[v] == int(labels[v] >= 13) for v in labels)
    assert cert["cut"] == 13 and cert["spine_labels"] == [3, 23, 10, 18]
    assert cert["witness"] == ["s:0", "s:1", "s:2", "s:3"] and cert["ports"] == ["s:0", "s:3"]
    assert cert["offsets"] == [labels["s:0"], labels["s:3"]-13] == [3, 5]
    weights = [abs(labels[u]-labels[v]) for u, v in edges]
    assert Counter(weights) == Counter(range(1, 24))
    assert cert["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
    identifier = digest({"graph_digest": original["graph_digest"], "labels": sorted(labels.items())})
    assert cert["ledger_id"] == identifier
    checked = cert["checker"]
    assert cert["graph_digest"] == checked["graph_digest"] == original["graph_digest"]
    assert checked["valid"] and checked["edge_differences"] == weights
    inventories, input_offsets = split_inventories(cert, labels, side, edges, roles)
    return {"status": "PASS", "graph_digest": original["graph_digest"], "ledger_id": identifier,
            "cut": 13, "physical_witness": cert["witness"], "spine_labels": [labels[v] for v in cert["witness"]],
            "inventories": inventories, "connector": cert["connector"], "input_offsets": input_offsets,
            "weights_in_original_order": weights, "archived_controls": archived_controls(root, cfg, controls),
            "adverse": adverse_audit(controls, original, edges, cert, weights, inventories),
            "new_graph_identities": 0, "solver_calls": 0, "enumeration_visits": 0}
