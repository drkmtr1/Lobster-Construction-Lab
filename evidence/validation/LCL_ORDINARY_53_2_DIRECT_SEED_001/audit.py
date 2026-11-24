"""Independent incidence and resource audit, with no LCL imports."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json


def topology(original):
    graph = original["graph"]
    spine = ["s:0", "s:1"]
    profile = [[5, 3], [2]]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = [spine.copy()]
    for section, quotas in enumerate(profile):
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            edges.append([spine[section], center])
            for index in range(quota):
                leaf = f"l:{section}:{branch}:{index}"
                roles[leaf] = {"kind": "leaf", "section": section, "branch": branch, "leaf": index}
                edges.append([center, leaf])
    actual = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    expected = Counter(tuple(sorted(edge)) for edge in edges)
    assert actual == expected and len(actual) == sum(actual.values()) == 14
    assert len(roles) == 15 and sorted(roles) == sorted(graph["vertices"])
    assert graph["roles"] == roles and graph["profile"] == profile and graph["spine"] == spine
    assert graph["schema_version"] == 1
    canonical = {"vertices": sorted(roles), "edges": sorted(expected.elements()),
                 "profile": profile, "roles": roles, "spine": spine}
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert sha256(raw).hexdigest() == original["graph_digest"]
    assert graph["edges"] == edges

    adjacency = {v: set() for v in roles}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    color = {"s:0": 0}
    queue = deque(color)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in color:
                color[v] = 1 - color[u]
                queue.append(v)
            assert color[u] != color[v]
    assert set(color) == set(roles)
    distance = dict.fromkeys(spine, 0)
    queue.extend(spine)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                queue.append(v)
    expected_distance = {"spine": 0, "branch": 1, "leaf": 2}
    assert distance == {v: expected_distance[role["kind"]] for v, role in roles.items()}
    return edges, adjacency, color, distance


def residual_audit(edges, adjacency, labels, construction):
    a, b = "b:0:0", "b:0:1"
    vacancies_a = sorted(adjacency[a] - {"s:0"})
    vacancies_b = ["l:0:1:1"]
    assert vacancies_b[0] in adjacency[b] and len(vacancies_a) == 5
    excluded = set(vacancies_a + vacancies_b)
    core = {v: x for v, x in labels.items() if v not in excluded}
    assert core == construction["core"]
    assert core == {"s:0": 0, "s:1": 14, a: 12, b: 2, "b:1:0": 1, "l:0:1:0": 3,
                    "l:0:1:2": 13, "l:1:0:0": 10, "l:1:0:1": 11}
    core_edges = [edge for edge in edges if excluded.isdisjoint(edge)]
    weights = [abs(core[u] - core[v]) for u, v in core_edges]
    assert len(core) == 9 and len(core_edges) == 8 and len(set(weights)) == 8
    assert all(len(adjacency[v]) == 1 for v in excluded)
    residual = set(range(len(edges) + 1)) - set(core.values())
    remaining = set(range(1, len(edges) + 1)) - set(weights)
    assert residual == set(range(4, 10)) and remaining == set(range(3, 9))

    palettes = {a: {labels[v] for v in vacancies_a}, b: {labels[v] for v in vacancies_b}}
    assert [labels[v] for v in vacancies_a] == [4, 5, 6, 8, 9] and labels[vacancies_b[0]] == 7
    by_options = defaultdict(list)
    options = {}
    for x in sorted(residual):
        da, db = abs(core[a] - x), abs(core[b] - x)
        assert core[b] < x < core[a]
        assert (da, db) == (12 - x, x - 2) and da + db == 10
        eligible = sorted({da, db} & remaining)
        assert eligible
        by_options[tuple(eligible)].append(x)
        options[x] = {"A": da, "B": db, "eligible": eligible}
    components = {(3, 7): [5, 9], (4, 6): [6, 8], (8,): [4], (5,): [7]}
    assert dict(by_options) == components
    assert all(len(differences) == len(xs) for differences, xs in by_options.items())
    assert Counter(d for ds in by_options for d in ds) == Counter(remaining)
    residual_rows = []
    for kind, host, xs in (("reflected_pair", a, [5, 9]), ("reflected_pair", a, [6, 8]),
                           ("forced_singleton", a, [4]), ("midpoint", b, [7])):
        assert set(xs) <= palettes[host]
        chosen = "A" if host == a else "B"
        residual_rows.append({"kind": kind, "host": host, "labels": xs,
                              "weights": [options[x][chosen] for x in xs]})
        if kind == "reflected_pair":
            x, y = xs
            assert x + y == core[a] + core[b] and options[x]["A"] == options[y]["B"]
            assert options[x]["B"] == options[y]["A"]
    assert construction["allocation_groups"] == residual_rows
    assert Counter(d for row in residual_rows for d in row["weights"]) == Counter(remaining)
    return {"core_edges": core_edges, "core_labels": sorted(core.values()), "core_weights": sorted(weights),
            "R": sorted(residual), "D": sorted(remaining), "options": options, "groups": residual_rows,
            "vacancies": {a: vacancies_a, b: vacancies_b}, "allocated_quotas": {a: 5, b: 1}}


def certificate_audit(original, cert, construction):
    edges, adjacency, color, distance = topology(original)
    labels = cert["labels"]
    assert set(labels) == set(adjacency) and all(type(x) is int for x in labels.values())
    unused_labels = sorted(set(range(15)) - set(labels.values()))
    assert not unused_labels and len(set(labels.values())) == 15
    payload = {"graph_digest": original["graph_digest"], "labels": sorted(labels.items())}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    assert cert["graph_digest"] == original["graph_digest"] and cert["ledger_id"] == sha256(raw).hexdigest()

    records = []
    for u, v in edges:
        tail, head = (u, v) if color[u] == 0 else (v, u)
        signed = labels[head] - labels[tail]
        records.append({"edge": [u, v], "orientation": [tail, head], "signed": signed, "absolute": abs(signed)})
    absolute = [row["absolute"] for row in records]
    unused_differences = sorted(set(range(1, 15)) - set(absolute))
    assert not unused_differences and Counter(absolute) == Counter(range(1, 15))
    assert absolute == cert["checker"]["edge_differences"]
    allocation = residual_audit(edges, adjacency, labels, construction)

    # Describe signed incidences of this witness without adding a sign predicate.
    weighted = [sum(len(adjacency[v]) * labels[v] for v in labels if color[v] == side) for side in (0, 1)]
    signed_sequence = [row["signed"] for row in records]
    negatives = [row for row in records if row["signed"] < 0]
    a, b, p, q = (labels[v] for v in ("b:0:0", "b:0:1", "l:1:0:0", "l:1:0:1"))
    signed_sum = sum(signed_sequence)
    assert weighted == [93 - a - b - p - q, 28 + 6*a + 4*b + p + q]
    assert signed_sum == weighted[1] - weighted[0] == sum(absolute) - 2*sum(row["absolute"] for row in negatives)
    assert 7*a + 5*b + 2*(p + q) == signed_sum + 65
    return {"distances_from_spine": distance, "degree_vector": {v: len(ns) for v, ns in adjacency.items()},
            "traversal_classes": {str(i): sorted(v for v, side in color.items() if side == i) for i in (0, 1)},
            "absolute_incidence_ledger": records, "signed_sequence": signed_sequence, "negative_edges": negatives,
            "weighted_even_odd": weighted, "signed_sum": signed_sum, "signed_degree_expression": signed_sum + 65,
            "allocation": allocation, "unused_labels": unused_labels, "unused_differences": unused_differences}


def controls(original, cert, records):
    graph = original["graph"]
    labels = cert["labels"]
    edges = graph["edges"]  # Already reconstructed independently in certificate_audit.
    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    wrong = records["wrong_digest"]
    assert wrong["expected_digest"] != original["graph_digest"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert not wrong["checker"]["valid"] and wrong["checker"]["edge_differences"] == weights

    cross_u, cross_v = "l:0:0:0", "l:0:1:1"
    cross = labels | {cross_u: labels[cross_v], cross_v: labels[cross_u]}
    assert (labels[cross_u], labels[cross_v]) == (4, 7)
    assert sorted(cross.values()) == list(range(15))
    cross_edges = [abs(cross[u] - cross[v]) for u, v in edges]
    changed = [(edge, before, after) for edge, before, after in zip(edges, weights, cross_edges, strict=True)
               if before != after]
    assert changed == [(["b:0:0", cross_u], 8, 5), (["b:0:1", cross_v], 5, 2)]
    witnesses = [edge for edge, weight in zip(edges, cross_edges, strict=True) if weight == 2]
    assert witnesses == [["s:0", "b:0:1"], ["b:0:1", cross_v]]
    repeats = {weight: count for weight, count in Counter(cross_edges).items() if count > 1}
    missing = sorted(set(range(1, 15)) - set(cross_edges))
    assert repeats == {2: 2} and missing == [8]
    assert records["cross_center"]["vertices"] == [cross_u, cross_v]
    assert records["cross_center"]["checker"]["edge_differences"] == cross_edges
    assert not records["cross_center"]["checker"]["valid"] and records["cross_center"]["pins"]["valid"]

    within_v = "l:0:0:1"
    within = labels | {cross_u: labels[within_v], within_v: labels[cross_u]}
    within_edges = [abs(within[u] - within[v]) for u, v in edges]
    assert (labels[cross_u], labels[within_v]) == (4, 5)
    assert Counter(within_edges) == Counter(weights) and sorted(within.values()) == list(range(15))
    within_record = records["within_center"]
    assert within_record["vertices"] == [cross_u, within_v]
    assert within_record["checker"]["edge_differences"] == within_edges and within_record["checker"]["valid"]

    complement = {v: 14 - x for v, x in labels.items()}
    complement_edges = [abs(complement[u] - complement[v]) for u, v in edges]
    assert complement_edges == weights and sorted(complement.values()) == list(range(15))
    assert records["complement"]["checker"]["valid"]
    assert records["complement"]["checker"]["edge_differences"] == complement_edges
    expected_pins = {"s:0": 0, "s:1": 14, "b:1:0": 1}
    for name, assignment in (("cross_center", cross), ("within_center", within), ("complement", complement)):
        pins = {v: assignment[v] for v in expected_pins}
        assert records[name]["pins"] == {"actual": pins, "expected": expected_pins, "valid": pins == expected_pins}
    assert records["within_center"]["pins"]["valid"] and not records["complement"]["pins"]["valid"]
    return {"cross_center": {"changed_incidences": changed, "repeat_witnesses": witnesses,
                             "repeat_multiplicities": repeats, "missing": missing, "label_bijection": True},
            "within_center": {"edge_multiset_retained": True, "physical_pins_retained": True},
            "complement": {"edge_sequence_retained": True, "pins": records["complement"]["pins"]["actual"]}}
