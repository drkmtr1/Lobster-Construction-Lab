"""Independent checks on the archived original graphs and ledger comparisons."""

from collections import Counter, deque
from hashlib import sha256
import json


def canonical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def read_archived(triple):
    original, record, report = triple
    graph = original["graph"]
    cert = record["certificate"]
    labels = cert["labels"]
    vertices = set(graph["vertices"])
    edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    assert len(vertices) == len(graph["vertices"]) == len(edges) + 1
    assert all(count == 1 for count in edges.values())
    assert all(a != b and {a, b} <= vertices for a, b in edges)
    assert set(graph["roles"]) == vertices == set(labels) and all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(len(vertices)))
    digest_data = {"vertices": sorted(vertices), "edges": sorted(edges.elements()),
                   "roles": graph["roles"], "profile": graph["profile"], "spine": graph["spine"]}
    assert canonical_sha(digest_data) == cert["graph_digest"] == original["graph_digest"] == report["graph_digest"]
    ledger = {"graph_digest": cert["graph_digest"], "labels": sorted(labels.items())}
    assert canonical_sha(ledger) == cert["ledger_id"] == report["ledger_id"]
    differences = {edge: abs(labels[edge[0]] - labels[edge[1]]) for edge in edges}
    assert Counter(differences.values()) == Counter(range(1, len(vertices)))
    assert [differences[tuple(sorted(e))] for e in graph["edges"]] == report["checker"]["edge_differences"]
    return graph, labels, vertices, edges, differences


def neighbors_at(edges, vertex):
    return {b if a == vertex else a for a, b in edges if vertex in (a, b)}


def spine_distances(vertices, edges, path):
    assert path and len(set(path)) == len(path) and set(path) <= vertices
    assert all(tuple(sorted(edge)) in edges for edge in zip(path, path[1:]))
    distances = dict.fromkeys(path, 0)
    queue = deque(path)
    while queue:
        vertex = queue.popleft()
        for neighbor in neighbors_at(edges, vertex):
            if neighbor not in distances:
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)
    assert set(distances) == vertices
    return distances


def archived_transition(source, target):
    old, f, old_vertices, old_edges, old_weights = read_archived(source)
    new, g, new_vertices, new_edges, new_weights = read_archived(target)
    assert old["profile"] == [[4, 3], [2]] and new["profile"] == [[4, 3], [3]]
    assert old["spine"] == new["spine"] == ["s:0", "s:1"]
    u, v, c, w = "s:0", "s:1", "b:1:0", "l:1:0:2"
    fresh = (c, w)
    assert new_vertices - old_vertices == {w} and not old_vertices - new_vertices
    assert new_edges - old_edges == Counter([fresh]) and not old_edges - new_edges
    assert neighbors_at(new_edges, w) == {c}
    assert all(old["roles"][name] == new["roles"][name] for name in old_vertices)
    assert new["roles"][w] == {"kind": "leaf", "section": 1, "branch": 0, "leaf": 2}
    assert target[1]["source_graph_digest"] == source[0]["graph_digest"]
    assert target[1]["source_ledger_id"] == source[1]["certificate"]["ledger_id"]
    assert target[1]["source_original_sha256"] == source[2]["original_sha256"]
    m = len(old_edges)
    for labels, edges, size in ((f, old_edges, m), (g, new_edges, m+1)):
        assert neighbors_at(edges, v) == {u, c} and (labels[u], labels[v], labels[c]) == (0, size, 1)
    old_distance = spine_distances(old_vertices, old_edges, old["spine"])
    new_distance = spine_distances(new_vertices, new_edges, new["spine"])
    assert max(old_distance.values()) == 2 and new_distance == old_distance | {w: 2}
    assert {name for name in old_vertices if f[name] != g[name]} == {v} and g[w] == m
    changed = {edge: (old_weights[edge], new_weights[edge])
               for edge in old_edges if old_weights[edge] != new_weights[edge]}
    expected = {tuple(sorted((u, v))): (m, m+1), tuple(sorted((v, c))): (m-1, m)}
    assert m == 13 and changed == expected and new_weights[fresh] == m-1
    unaffected = sorted(weight for edge, weight in old_weights.items() if edge not in changed)
    assert unaffected == list(range(1, m-1))
    return {"spine": old["spine"], "preserved_original_vertices": sorted(old_vertices),
            "preserved_original_edges": sorted(old_edges), "preserved_original_roles": old["roles"],
            "new_terminal": w, "new_edge": list(fresh), "fresh_label": g[w], "fresh_weight": new_weights[fresh],
            "fresh_distance": new_distance[w], "only_old_label_change": {v: [f[v], g[v]]},
            "changed_weights": [{"edge": list(edge), "old": a, "new": b} for edge, (a, b) in sorted(changed.items())],
            "unchanged_weights": unaffected}


def retained_base(triple):
    graph, labels, vertices, edges, weights = read_archived(triple)
    assert graph["profile"] == [[5, 3], [2]] and graph["spine"] == ["s:0", "s:1"]
    assert len(edges) == 2+12 and neighbors_at(edges, "s:1") == {"s:0", "b:1:0"}
    expected = {"s:0": 0, "s:1": 2+12, "b:0:0": 12, "b:0:1": 2, "b:1:0": 1,
                "l:1:0:0": 10, "l:1:0:1": 11}
    for branch, values in ((0, (4, 5, 6, 8, 9)), (1, (3, 7, 13))):
        expected.update({f"l:0:{branch}:{i}": label for i, label in enumerate(values)})
    assert labels == expected
    distance = spine_distances(vertices, edges, graph["spine"])
    assert max(distance.values()) == 2 and distance["b:1:0"] == 1
    parity = spine_distances(vertices, edges, ["s:0"])
    signs = []
    for a, b in graph["edges"]:
        tail, head = (a, b) if parity[a] % 2 == 0 else (b, a)
        signs.append({"edge": [tail, head], "signed": labels[head] - labels[tail]})
    negatives = [row for row in signs if row["signed"] < 0]
    assert negatives == [{"edge": [f"l:0:1:{i}", "b:0:1"], "signed": value}
                         for i, value in enumerate((-1, -5, -11))]
    return {"r": 2, "pointwise_formula_agreement": True, "exit_neighbors": sorted(neighbors_at(edges, "s:1")),
            "host_distance": distance["b:1:0"], "original_edge_count": len(weights), "signed_diagnostic": signs,
            "negative_incidences": negatives}


def controls(original, cert, results):
    graph = original["graph"]
    labels = cert["labels"]
    edges = graph["edges"]
    weights = [abs(labels[a] - labels[b]) for a, b in edges]
    wrong = results["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["edge_differences"] == weights

    a, b = "l:0:0:0", "l:0:0:1"
    within = labels | {a: labels[b], b: labels[a]}
    within_weights = [abs(within[u] - within[v]) for u, v in edges]
    swaps = [[edge, old, new] for edge, old, new in zip(edges, weights, within_weights, strict=True) if old != new]
    assert swaps == [[["b:0:0", a], 8, 7], [["b:0:0", b], 7, 8]]
    within_record = results["within_center"]
    assert within_record["swapped_vertices"] == [a, b] and within_record["checker"]["valid"]
    assert within_record["checker"]["edge_differences"] == within_weights
    assert Counter(within_weights) == Counter(weights) and sorted(within.values()) == sorted(labels.values())
    assert within_record["premises"]["valid"] and all(within_record["premises"]["tests"].values())
    pins = ("s:0", "s:1", "b:1:0")
    assert within_record["premises"]["actual"] == {v: within[v] for v in pins}

    m = len(edges)
    complemented = {v: m-x for v, x in labels.items()}
    complement_weights = [abs(complemented[u] - complemented[v]) for u, v in edges]
    assert complement_weights == weights and sorted(complemented.values()) == sorted(labels.values())
    complement = results["complement"]
    assert complement["checker"]["valid"] and complement["checker"]["edge_differences"] == complement_weights
    assert tuple(complemented[v] for v in pins) == (14, 0, 13) and not complement["premises"]["valid"]
    assert complement["premises"]["actual"] == {v: complemented[v] for v in pins}
    assert not complement["premises"]["tests"]["physical_labels"]

    alternate = results["alternate_path"]
    predicate = alternate["premises"]
    path = predicate["spine"]
    edge_keys = {tuple(sorted(edge)) for edge in edges}
    assert path == list(pins) and max(spine_distances(set(labels), edge_keys, path).values()) == 2
    assert path[-1] == "b:1:0" and path[1] == "s:1" and path[-2:] != list(pins[:2])
    assert alternate["ordinary_valid"] and alternate["ordinary_source"] == "D111 retained recheck"
    assert not predicate["valid"] and predicate["tests"]["witnessing_path"]
    assert not predicate["tests"]["terminal_exit"] and not predicate["tests"]["terminal_pair"]
    assert not predicate["tests"]["host_off_path"]
    assert predicate["tests"]["exact_exit_neighbors"] and predicate["tests"]["physical_labels"]
    return {"within_center_weight_changes": swaps, "complement_pins": complement["premises"]["actual"],
            "alternate_is_witnessing_path": True, "alternate_exit_is_interior": True,
            "alternate_host_is_on_path": True, "alternate_witness_maximum_distance": 2}
