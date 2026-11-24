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
    assert tuple(left) in {(6, 3, 2), (6, 5, 6), (6, 3, 6), (6, 3, 8), (6, 3, 4)}
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


def check_canonical(graph, choice, binding, expected_supplier):
    quotas = graph["profile"][0]
    assert quotas[0] >= 6 and quotas[0] % 2 == 0 and quotas[2] >= 2 and quotas[2] % 2 == 0
    assert quotas[1] >= 3 and quotas[1] % 2 == 1
    assert choice["indices"] == [0, 1, 2] and choice["canonical_quotas"] == quotas
    assert choice["dispatch"] == expected_supplier
    assert binding["valid"] and binding["quota_evaluated"] and binding["inverse"] == [0, 1, 2]
    assert binding["quota_compatible"] and binding["slots_exact"]
    for j, quota in enumerate(quotas):
        center = f"b:0:{j}"
        actual = sorted(((leaf, role["leaf"]) for leaf, role in graph["roles"].items()
                         if role["kind"] == "leaf" and role["section"] == 0 and role["branch"] == j),
                        key=lambda item: item[1])
        names = [name for name, _ in actual]
        assert [k for _, k in actual] == list(range(quota))
        assert binding["rows"][j] == {"role": j, "physical_index": j, "quota": quota, "actual_quota": quota,
                                      "requested": names, "actual": names, "absent": [], "omitted": []}
        assert all([center, leaf] in graph["edges"] for leaf in names)


def check_controls(graph, cert, records):
    rejection = records["wrong_expected_digest"]["checker"]
    weights = [abs(cert["labels"][v]-cert["labels"][w]) for v, w in graph["edges"]]
    assert rejection["edge_differences"] == weights and rejection["graph_digest"] == cert["graph_digest"]
    assert rejection["errors"] == ["original graph digest mismatch"] and not rejection["valid"]
    duplicate = records["nonbijective_map"]
    assert duplicate["indices"] == [0, 0, 2] and duplicate["status"] == "NONBIJECTIVE_ROLE_MAP"
    assert duplicate["quota_evaluated"] is False and "rows" not in duplicate and not duplicate["valid"]
    wrong_quota = records["quota_incompatible_map"]
    assert wrong_quota["indices"] == [2, 1, 0] and wrong_quota["inverse"] == [2, 1, 0]
    assert wrong_quota["quota_evaluated"] and wrong_quota["bijective"] and not wrong_quota["valid"]
    assert not wrong_quota["quota_compatible"] and not wrong_quota["slots_exact"]
    assert [row["quota"] for row in wrong_quota["rows"]] == [6, 3, 4]
    assert [row["actual_quota"] for row in wrong_quota["rows"]] == [4, 3, 6]
    absent = sorted(leaf for row in wrong_quota["rows"] for leaf in row["absent"])
    omitted = sorted(leaf for row in wrong_quota["rows"] for leaf in row["omitted"])
    assert absent == ["l:0:2:4", "l:0:2:5"] and omitted == ["l:0:0:4", "l:0:0:5"]
    assert all(leaf not in graph["vertices"] for leaf in absent)
    assert all(["b:0:0", leaf] in graph["edges"] for leaf in omitted)

    direction = records["direction"]
    valid, wrong = direction["forward_check"], direction["inverse_used_as_forward"]
    forward = [1, 2, 0]
    inverse = [forward.index(h) for h in range(3)]
    assert inverse == [2, 0, 1]
    assert valid["candidate"] == forward and valid["inverse"] == inverse and valid["valid"]
    assert wrong["candidate"] == inverse and not wrong["valid"] and wrong["bijective"]
    assert wrong["mismatched_canonical_indices"] == [0, 1, 2]
    for j, row in enumerate(valid["rows"]):
        assert row["source_center_index"] == j and row["forward_center_index"] == forward[j]
        assert row["center_round_trip"] == j and row["reverse_center_round_trip"] == j
        assert row["source_terminal"] == [j, "k"]
        assert row["forward_terminal"] == [forward[j], "k"] and row["terminal_round_trip"] == [j, "k"]
        assert row["reverse_terminal_round_trip"] == [j, "k"]
    return {"wrong_quota_absent": absent, "wrong_quota_omitted": omitted,
            "index_only_forward": forward, "index_only_inverse": inverse,
            "both_center_and_terminal_round_trips": True}
