"""Independent named-incidence and inventory checks on already frozen originals."""

from collections import Counter, deque
from hashlib import sha256
import json


def digest_json(payload):
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return sha256(data.encode("utf-8")).hexdigest()


def inspect_original(original, expected_profile):
    graph = original["graph"]
    assert graph["profile"] == expected_profile and type(graph["schema_version"]) is int
    assert graph["schema_version"] == 1 and graph["spine"] == ["s:0", "s:1"]
    left, right = expected_profile
    assert len(left) == 3 and right == [2]
    assert all(type(quota) is int and quota >= 0 for quota in (*left, *right))
    spine = ["s:0", "s:1"]
    expected_edges = [spine]
    roles = {}
    for section, quotas in enumerate((left, right)):
        root = spine[section]
        roles[root] = {"kind": "spine", "section": section}
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            expected_edges.append([root, center])
            for index in range(quota):
                terminal = f"l:{section}:{branch}:{index}"
                roles[terminal] = {"kind": "leaf", "section": section, "branch": branch, "leaf": index}
                expected_edges.append([center, terminal])
    assert graph["roles"] == roles and graph["vertices"] == list(roles)
    assert graph["edges"] == expected_edges
    canonical_edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    n = sum(left)+7
    assert len(canonical_edges) == len(expected_edges) == n
    assert len(roles) == n+1
    digest = digest_json({"vertices": sorted(roles), "edges": sorted(canonical_edges.elements()),
                          "roles": roles, "spine": spine, "profile": expected_profile})
    assert digest == original["graph_digest"]
    neighbors = {v: set() for v in roles}
    for v, w in expected_edges:
        neighbors[v].add(w)
        neighbors[w].add(v)
    distance = dict.fromkeys(spine, 0)
    pending = deque(spine)
    while pending:
        v = pending.popleft()
        for w in neighbors[v]-distance.keys():
            distance[w] = distance[v]+1
            pending.append(w)
    assert distance == {v: {"spine": 0, "branch": 1, "leaf": 2}[role["kind"]] for v, role in roles.items()}
    return {"graph_digest": digest, "edges": expected_edges, "vertices": list(roles), "distance_to_spine": distance,
            "exit_neighbors": sorted(neighbors["s:1"])}


def inspect_certificate(original, certificate, structure):
    labels = certificate["labels"]
    digest = structure["graph_digest"]
    assert digest == certificate["graph_digest"] == original["graph_digest"]
    assert set(labels) == set(structure["vertices"])
    assert all(type(label) is int for label in labels.values())
    ledger = digest_json({"graph_digest": digest, "labels": sorted(labels.items())})
    assert ledger == certificate["ledger_id"]
    n = len(structure["edges"])
    weights = [abs(labels[v]-labels[w]) for v, w in structure["edges"]]
    assert Counter(labels.values()) == Counter(range(n+1))
    assert Counter(weights) == Counter(range(1, n+1))
    return {"ledger_id": ledger, "vertex_label_alphabet": sorted(labels.values()), "edge_weights": weights,
            "named_incidences": [[v, w, d] for (v, w), d in zip(structure["edges"], weights, strict=True)]}


def check_growth_premises(graph, labels, actual_n, structure):
    expected = {"s:0": 0, "s:1": actual_n, "b:1:0": 1}
    pins = {v: labels[v] for v in expected}
    tests = {"terminal_endpoint_and_predecessor": graph["spine"] == ["s:0", "s:1"],
             "actual_spine_edge": ["s:0", "s:1"] in structure["edges"],
             "exact_exit_neighbors": structure["exit_neighbors"] == ["b:1:0", "s:0"],
             "right_center_off_spine": graph["roles"]["b:1:0"] == {"kind": "branch", "section": 1, "branch": 0}
             and structure["distance_to_spine"]["b:1:0"] == 1,
             "physical_pins": pins == expected,
             "maximum_exit_label": max(labels.values()) == labels["s:1"] == actual_n}
    return {"valid": all(tests.values()), "tests": tests, "pins": pins, "exit_neighbors": structure["exit_neighbors"]}


def check_base_specialization(graph, labels, actual_n, structure):
    r = graph["profile"][1][0]
    assert r == 2 and graph["profile"][1] == [2]
    m = actual_n+r-2
    new_indices = range(2, r)
    extra_labels = range(actual_n, m)
    extra_weights = range(actual_n-1, m-1)
    assert len(new_indices) == len(extra_labels) == len(extra_weights) == 0
    assert structure["edges"] == graph["edges"] and structure["vertices"] == graph["vertices"]
    assert all(v in labels for v in structure["vertices"]) and labels["s:1"] == m == actual_n
    assert [labels[f"l:1:0:{i}"] for i in range(2)] == [actual_n-1, actual_n-2]
    return {"r": r, "seed_edge_count": actual_n, "final_edge_count": m, "added_indices": [],
            "added_label_count": len(extra_labels), "added_weight_count": len(extra_weights),
            "pointwise_identity": True, "named_original_unchanged": True,
            "right_seed_labels": [labels["l:1:0:0"], labels["l:1:0:1"]]}
