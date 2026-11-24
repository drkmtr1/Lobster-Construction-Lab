"""Independent reconstruction and arithmetic for the D097 boundary and frozen controls."""

from collections import Counter
from hashlib import sha256
import json


def load(path):
    return json.loads(path.read_bytes())


def canonical_hash(data):
    return sha256(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def inspect(original, cert, quotas):
    q, a, r = quotas
    profile = [[q, a], [r]]
    graph, labels = original["graph"], cert["labels"]
    roles = {"s:0": {"kind": "spine", "section": 0}, "s:1": {"kind": "spine", "section": 1}}
    edges = [("s:0", "s:1")]
    groups = {"spine": [("s:0", "s:1")]}
    for section, branch, count, group in ((0, 0, q, "left_first"), (0, 1, a, "left_second"), (1, 0, r, "right")):
        center = f"b:{section}:{branch}"
        roles[center] = {"kind": "branch", "section": section, "branch": branch}
        attach = (f"s:{section}", center)
        edges.append(attach)
        groups[group+"_attachment"] = [attach]
        groups[group+"_terminals"] = []
        for index in range(count):
            name = f"l:{section}:{branch}:{index}"
            roles[name] = {"kind": "leaf", "section": section, "branch": branch, "leaf": index}
            edges.append((center, name))
            groups[group+"_terminals"].append((center, name))
    expected_key = lambda edge: tuple(sorted(edge))
    assert graph["profile"] == profile and graph["roles"] == roles and graph["schema_version"] == 1
    assert graph["spine"] == cert["witness"] == cert["physical_ports"] == ["s:0", "s:1"]
    assert Counter(graph["vertices"]) == Counter(list(roles))
    assert Counter(map(expected_key, graph["edges"])) == Counter(map(expected_key, edges))
    n, p = len(roles), q+a+2
    assert n == q+a+r+5 and len(edges) == n-1 and cert["cut"] == p
    digest = canonical_hash({"vertices": sorted(roles), "edges": sorted(sorted(edge) for edge in edges),
                             "roles": roles, "profile": profile, "spine": ["s:0", "s:1"]})
    assert digest == original["graph_digest"] == cert["graph_digest"]
    ledger = canonical_hash({"graph_digest": digest, "labels": sorted(labels.items())})
    assert ledger == cert["ledger_id"]
    assert set(labels) == set(roles) and all(type(value) is int for value in labels.values())
    lows = {"s:0", "b:1:0"} | {v for v in roles if v.startswith("l:0:")}
    highs = set(roles)-lows
    low_values, high_values = sorted(labels[v] for v in lows), sorted(labels[v] for v in highs)
    assert low_values == list(range(p)) and high_values == list(range(p, n))
    assert all((u in lows) != (v in lows) for u, v in edges)
    assert [labels["s:0"], labels["s:1"]-p, labels["b:1:0"]] == [q+1, q+2, 0]
    weights = {expected_key((u, v)): abs(labels[u]-labels[v]) for u, v in edges}
    rows = [[u, v, weights[expected_key((u, v))]] for u, v in graph["edges"]]
    assert rows == cert["edge_rows"]
    assert sorted(weights.values()) == list(range(1, n))
    right = groups["right_terminals"]
    groups["right_terminals"] = right[:q]
    groups["fresh_right_terminals"] = right[q:]
    bands = {key: sorted(weights[expected_key(edge)] for edge in values) for key, values in groups.items()}
    assert bands == {"left_second_terminals": list(range(1, a+1)), "left_second_attachment": [a+1],
                     "left_first_attachment": [a+2], "left_first_terminals": list(range(a+3, a+q+3)),
                     "spine": [a+q+3], "right_terminals": list(range(a+q+4, a+2*q+4)),
                     "right_attachment": [a+2*q+4], "fresh_right_terminals": list(range(a+2*q+5, n))}
    return {"graph_digest": digest, "ledger_id": ledger, "alpha_labels": {"low": low_values, "high": high_values},
            "edge_rows": rows, "difference_bands": bands,
            "unused_labels": sorted(set(range(n))-set(labels.values())),
            "unused_differences": sorted(set(range(1, n))-set(weights.values()))}


def check(root, original, cert, controls, adverse, cfg):
    expected = {"s:0": 5, "s:1": 14, "b:0:0": 9, "b:0:1": 8, "b:1:0": 0,
                "l:0:0:0": 1, "l:0:0:1": 2, "l:0:0:2": 3, "l:0:0:3": 4,
                "l:0:1:0": 6, "l:0:1:1": 7,
                "l:1:0:0": 10, "l:1:0:1": 11, "l:1:0:2": 12, "l:1:0:3": 13}
    assert cert["labels"] == expected and cert["offsets"] == [5, 6]
    report = inspect(original, cert, [4, 2, 4])
    assert adverse["graph_identity"]["declared_digest"] == "0"*64
    digest_probe = adverse["graph_identity"]["checker"]
    assert not digest_probe["valid"] and digest_probe["errors"] == ["original graph digest mismatch"]
    assert adverse["physical_port"] == {"declared": [5, 5], "valid": False, "error": "Physical offset mismatch"}
    u, v = adverse["label_swap"]["vertices"]
    assert (u, v) == ("l:0:0:0", "l:0:1:0")
    broken = expected | {u: expected[v], v: expected[u]}
    differences = [abs(broken[x]-broken[y]) for x, y, _ in report["edge_rows"]]
    checker = adverse["label_swap"]["checker"]
    assert not checker["valid"] and checker["edge_differences"] == differences
    repeated = sorted(weight for weight, count in Counter(differences).items() if count > 1)
    missing = sorted(set(range(1, 15))-set(differences))
    assert repeated == [3, 7] and missing == [2, 8]
    audited = {}
    for name in ("D089", "D096"):
        spec = cfg["controls"][name]
        folder = root / spec["folder"]
        source = load(folder / "result.json")
        prior = source["boundary"]["certificate"] if name == "D089" else source["certificate"]
        quotas = [3, 2, 3] if name == "D089" else [2, 2, 3]
        audited[name] = inspect(load(folder / "original.json"), prior, quotas)
        assert controls[name]["ledger_id"] == audited[name]["ledger_id"]
        assert controls[name]["graph_digest"] == audited[name]["graph_digest"]
    assert audited["D089"]["difference_bands"]["fresh_right_terminals"] == []
    assert audited["D096"]["difference_bands"]["fresh_right_terminals"] == [11]
    archives = {key: load(root / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert archives == {"D083_original": "INCOMPLETE", "D083_versioned": "PASS",
                        "D093_original": "INCOMPLETE", "D093_versioned": "PASS"}
    report.update(status="PASS", retained_controls=audited, archived_execution_statuses=archives,
                  swap={"repeated": repeated, "missing": missing})
    return report
