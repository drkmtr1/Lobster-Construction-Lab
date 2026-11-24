"""Reconstruct both original incidence sets independently of the production graph builder."""

from collections import Counter
from hashlib import sha256
import json


def load(path):
    return json.loads(path.read_bytes())


def canonical_digest(data):
    return sha256(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def multiset(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def inspect(original, cert, profile):
    graph, labels = original["graph"], cert["labels"]
    roles = {"s:0": {"kind": "spine", "section": 0}, "s:1": {"kind": "spine", "section": 1}}
    expected = [("s:0", "s:1")]
    for section, quotas in enumerate(profile):
        for branch, count in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            expected.append((f"s:{section}", center))
            for k in range(count):
                v = f"l:{section}:{branch}:{k}"
                roles[v] = {"kind": "leaf", "section": section, "branch": branch, "leaf": k}
                expected.append((center, v))
    assert graph["schema_version"] == 1 and graph["roles"] == roles and graph["profile"] == profile
    assert graph["spine"] == cert["witness"] == ["s:0", "s:1"]
    assert Counter(graph["vertices"]) == Counter(list(roles))
    assert multiset(expected) == multiset(graph["edges"])
    n = len(roles)
    assert n == 13 and len(expected) == n-1
    digest = canonical_digest({"vertices": sorted(roles), "edges": sorted(sorted(e) for e in expected),
                               "profile": profile, "spine": ["s:0", "s:1"], "roles": roles})
    assert digest == original["graph_digest"] == cert["graph_digest"]
    ledger = canonical_digest({"graph_digest": digest, "labels": sorted(labels.items())})
    assert ledger == cert["ledger_id"]
    assert set(labels) == set(roles) and all(type(value) is int for value in labels.values())
    low = {"s:0", "b:1:0"} | {v for v in roles if v.startswith("l:0:")}
    low_labels = sorted(labels[v] for v in low)
    high_labels = sorted(labels[v] for v in set(roles)-low)
    assert cert["cut"] == 8 and low_labels == list(range(8)) and high_labels == list(range(8, 13))
    assert all((u in low) != (v in low) for u, v in expected)
    assert [labels["s:0"], labels["s:1"], labels["b:1:0"]] == [3, 12, 0]
    weights = {tuple(sorted((u, v))): abs(labels[u]-labels[v]) for u, v in expected}
    rows = [[u, v, weights[tuple(sorted((u, v)))]] for u, v in graph["edges"]]
    assert rows == cert["edge_rows"] and sorted(weights.values()) == list(range(1, n))
    return {"graph_digest": digest, "ledger_id": ledger, "edge_rows": rows,
            "low_labels": low_labels, "high_labels": high_labels,
            "unused_labels": sorted(set(range(n))-set(labels.values())),
            "unused_differences": sorted(set(range(1, n))-set(weights.values()))}


def check(root, cfg, original, cert, transport, adverse):
    retained = load(root / cfg["retained"]["original"])
    source_cert = load(root / cfg["retained"]["result"])["state"]["certificate"]
    source = inspect(retained, source_cert, [[2, 4], [2]])
    target = inspect(original, cert, [[4, 2], [2]])
    assert source["graph_digest"] != target["graph_digest"] and source["ledger_id"] != target["ledger_id"]
    expected = {"s:0": 3, "s:1": 12, "b:0:0": 8, "b:0:1": 9, "b:1:0": 0,
                "l:0:0:0": 4, "l:0:0:1": 5, "l:0:0:2": 6, "l:0:0:3": 7,
                "l:0:1:0": 1, "l:0:1:1": 2, "l:1:0:0": 10, "l:1:0:1": 11}
    labels = cert["labels"]
    assert labels == expected and cert["offsets"] == [3, 4]
    explicit = {"s:0": "s:0", "s:1": "s:1", "b:1:0": "b:1:0",
                "l:1:0:0": "l:1:0:0", "l:1:0:1": "l:1:0:1",
                "b:0:0": "b:0:1", "l:0:0:0": "l:0:1:0", "l:0:0:1": "l:0:1:1",
                "b:0:1": "b:0:0", "l:0:1:0": "l:0:0:0", "l:0:1:1": "l:0:0:1",
                "l:0:1:2": "l:0:0:2", "l:0:1:3": "l:0:0:3"}
    reverse = {target_name: source_name for source_name, target_name in explicit.items()}
    assert transport == {"forward": explicit, "inverse": reverse}
    assert all(source_cert["labels"][v] == labels[w] for v, w in explicit.items())
    mapped = [[explicit[u], explicit[v], w] for u, v, w in source["edge_rows"]]
    unmapped = [[reverse[u], reverse[v], w] for u, v, w in target["edge_rows"]]
    def edge_weights(rows):
        return Counter((tuple(sorted((u, v))), w) for u, v, w in rows)
    assert edge_weights(mapped) == edge_weights(target["edge_rows"])
    assert edge_weights(unmapped) == edge_weights(source["edge_rows"])
    assert adverse["graph_identity"]["declared_digest"] == source["graph_digest"]
    rejected_identity = adverse["graph_identity"]["checker"]
    assert not rejected_identity["valid"] and rejected_identity["errors"] == ["original graph digest mismatch"]
    assert adverse["physical_ports"] == {"declared": [3, 3], "valid": False, "error": "Physical offset mismatch"}
    bad_map = adverse["transport"]
    u, v = "l:0:0:0", "l:0:1:0"
    assert bad_map["exchanged_source_names"] == [u, v]
    assert bad_map["map"] == explicit | {u: explicit[v], v: explicit[u]}
    assert Counter(bad_map["map"].values()) == Counter(explicit.values())
    bad_edges = multiset((bad_map["map"][x], bad_map["map"][y]) for x, y, _ in source["edge_rows"])
    target_edges = multiset((x, y) for x, y, _ in target["edge_rows"])
    extra = sorted((bad_edges-target_edges).elements())
    missing = sorted((target_edges-bad_edges).elements())
    assert len(extra) == len(missing) == 2 and not bad_map["valid"]
    assert bad_map["error"] == "Named transport changes original edge incidences"
    rows = target["edge_rows"]
    bands = [[w for _, v, w in rows if v.startswith("l:0:0:")],
             [w for u, v, w in rows if [u, v] == ["s:0", "b:0:0"]],
             [w for u, v, w in rows if [u, v] == ["s:0", "b:0:1"]],
             [w for _, v, w in rows if v.startswith("l:0:1:")], [rows[0][2]],
             [w for _, v, w in rows if v.startswith("l:1:0:")],
             [w for u, v, w in rows if [u, v] == ["s:1", "b:1:0"]]]
    bands = [sorted(band) for band in bands]
    assert bands == [[1, 2, 3, 4], [5], [6], [7, 8], [9], [10, 11], [12]]
    archived = {key: load(root / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert archived == {"D083_original": "INCOMPLETE", "D083_versioned": "PASS",
                        "D093_original": "INCOMPLETE", "D093_versioned": "PASS"}
    return {"status": "PASS", "source": source, "target": target, "source_edges_mapped": mapped,
            "target_edges_mapped_back": unmapped, "ascending_target_weight_groups": bands,
            "corrupted_transport_extra_edges": extra, "corrupted_transport_missing_edges": missing,
            "archived_execution_statuses": archived}
