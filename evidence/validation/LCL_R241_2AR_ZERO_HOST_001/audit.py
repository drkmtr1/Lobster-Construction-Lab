"""Independently reconstruct the D096 originals from physical names and quotas."""

from collections import Counter
from hashlib import sha256
import json


def load(path):
    return json.loads(path.read_bytes())


def canonical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def reconstruct(profile):
    spine = ["s:0", "s:1"]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = [tuple(spine)]
    for i, section in enumerate(profile):
        for j, quota in enumerate(section):
            center = f"b:{i}:{j}"
            roles[center] = {"kind": "branch", "section": i, "branch": j}
            edges.append((spine[i], center))
            for k in range(quota):
                leaf = f"l:{i}:{j}:{k}"
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
                edges.append((center, leaf))
    return roles, edges


def inspect(original, labels, profile):
    graph = original["graph"]
    roles, edges = reconstruct(profile)
    assert graph["profile"] == profile and graph["spine"] == ["s:0", "s:1"]
    assert graph["schema_version"] == 1 and graph["roles"] == roles
    assert Counter(graph["vertices"]) == Counter(list(roles))
    assert Counter(tuple(sorted(edge)) for edge in graph["edges"]) == Counter(tuple(sorted(edge)) for edge in edges)
    n = len(roles)
    assert len(edges) == n-1
    digest = canonical_hash({"vertices": sorted(roles), "edges": sorted(sorted(e) for e in edges),
                             "profile": profile, "roles": roles, "spine": ["s:0", "s:1"]})
    assert digest == original["graph_digest"]
    assert set(labels) == set(roles) and all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(n))
    lows = {"s:0", "b:1:0"} | {name for name in roles if name.startswith("l:0:")}
    assert sorted(labels[v] for v in lows) == list(range(6))
    assert sorted(labels[v] for v in roles.keys()-lows) == list(range(6, n))
    assert all((u in lows) != (v in lows) for u, v in edges)
    rows = [[u, v, abs(labels[u]-labels[v])] for u, v in edges]
    differences = [w for _, _, w in rows]
    assert sorted(differences) == list(range(1, n))
    ledger = canonical_hash({"graph_digest": digest, "labels": sorted(labels.items())})
    return {"graph_digest": digest, "ledger_id": ledger, "edge_rows": rows,
            "unused_labels": sorted(set(range(n))-set(labels.values())),
            "unused_differences": sorted(set(range(1, n))-set(differences))}


def check_archives(root, cfg, new_digest):
    archived = {key: load(root / path) for key, path in cfg["retained"].items() if key.startswith("archive_")}
    same_original = archived["archive_d083_original"]
    assert same_original["graph_digest"] == new_digest
    roles, edges = reconstruct([[2, 2], [3]])
    graph = same_original["graph"]
    assert graph["profile"] == [[2, 2], [3]] and graph["roles"] == roles
    assert set(graph["vertices"]) == set(roles) and graph["spine"] == ["s:0", "s:1"]
    assert Counter(tuple(sorted(e)) for e in graph["edges"]) == Counter(tuple(sorted(e)) for e in edges)
    pins = archived["archive_d083_config"]["pins"]
    assert pins == {"s:0": 1, "s:1": 6} and archived["archive_d083_config"]["cut"] == 6
    assert archived["archive_d083_failure"]["status"] == "INCOMPLETE"
    assert archived["archive_d083_closeout"]["status"] == "PASS"
    assert archived["archive_d093_failure"]["status"] == "INCOMPLETE"
    assert archived["archive_d093_recovery"]["status"] == "PASS"
    return {"D083": {"graph_digest": new_digest, "pins": pins, "offsets": [1, 0], "disposition": "EXCLUDED",
                     "official_execution": "INCOMPLETE", "audit_closeout": "PASS"},
            "D093": {"official_execution": "INCOMPLETE", "versioned_recovery": "PASS"}}


def check(root, cfg, original, certificate, positive, adverse):
    labels = certificate["labels"]
    expected = {"s:0": 3, "s:1": 10, "b:0:0": 7, "b:0:1": 6, "b:1:0": 0,
                "l:0:0:0": 1, "l:0:0:1": 2, "l:0:1:0": 4, "l:0:1:1": 5,
                "l:1:0:0": 8, "l:1:0:1": 9, "l:1:0:2": 11}
    assert labels == expected
    audit = inspect(original, labels, [[2, 2], [3]])
    assert certificate["edge_rows"] == audit["edge_rows"]
    assert (certificate["graph_digest"], certificate["ledger_id"]) == (audit["graph_digest"], audit["ledger_id"])
    assert certificate["cut"] == 6 and certificate["offsets"] == [3, 4]
    assert certificate["physical_ports"] == certificate["witness"] == ["s:0", "s:1"]
    assert [labels["s:0"], labels["s:1"]-6] == [3, 4]
    base = load(root / cfg["retained"]["d084_original"])
    inherited = inspect(base, positive["labels"], [[2, 2], [2]])
    assert all(inherited[k] == positive[k] for k in ("ledger_id", "graph_digest"))
    new_name = "l:1:0:2"
    old_rows = [row for row in audit["edge_rows"] if new_name not in row[:2]]
    added, = [row for row in audit["edge_rows"] if new_name in row[:2]]
    assert added == ["b:1:0", new_name, 11]
    assert sorted(w for _, _, w in old_rows) == list(range(1, 11))
    assert sorted(v for k, v in labels.items() if k != new_name) == list(range(11))
    assert Counter(tuple(sorted(row[:2])) for row in old_rows) == Counter(tuple(sorted(row[:2])) for row in inherited["edge_rows"])
    for v in base["graph"]["vertices"]:
        if not v.startswith(("l:0:1:", "l:1:0:")):
            assert labels[v] == positive["labels"][v]
    for prefix in ("l:0:1:", "l:1:0:"):
        names = [v for v in base["graph"]["vertices"] if v.startswith(prefix)]
        assert sorted(labels[v] for v in names) == sorted(positive["labels"][v] for v in names)
    assert adverse["graph_digest"]["errors"] == ["original graph digest mismatch"] and not adverse["graph_digest"]["valid"]
    assert adverse["physical_offsets"] == {"declared": [1, 0], "valid": False, "error": "physical offset mismatch"}
    u, v = adverse["label_swap"]["vertices"]
    assert (u, v) == ("l:0:0:0", "l:0:1:0")
    swapped = labels | {u: labels[v], v: labels[u]}
    weights = [abs(swapped[u]-swapped[v]) for u, v, _ in audit["edge_rows"]]
    checker = adverse["label_swap"]["checker"]
    assert checker["edge_differences"] == weights and not checker["valid"]
    repeated = {w: count for w, count in sorted(Counter(weights).items()) if count > 1}
    missing = sorted(set(range(1, 12))-set(weights))
    assert repeated == {3: 2, 5: 2} and missing == [2, 6]
    audit.update(status="PASS", old_labels=list(range(11)), old_differences=list(range(1, 11)),
                 new_labels=[11], new_differences=[11], new_edge=added, expected_boundary=expected,
                 inherited_control=inherited, swap={"repeat_counts": repeated, "missing": missing},
                 archived=check_archives(root, cfg, audit["graph_digest"]))
    return audit
