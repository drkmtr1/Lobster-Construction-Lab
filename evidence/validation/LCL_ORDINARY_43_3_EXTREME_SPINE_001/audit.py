"""Independent named-incidence audit for the frozen D106 original."""

from collections import Counter, deque
from hashlib import sha256
import json


def topology(original, profile):
    graph = original["graph"]
    spine = ["s:0", "s:1"]
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    expected = Counter([tuple(spine)])
    for section, quotas in enumerate(profile):
        for branch, quota in enumerate(quotas):
            center = f"b:{section}:{branch}"
            roles[center] = {"kind": "branch", "section": section, "branch": branch}
            expected[tuple(sorted((spine[section], center)))] += 1
            for leaf in range(quota):
                terminal = f"l:{section}:{branch}:{leaf}"
                roles[terminal] = {"kind": "leaf", "section": section, "branch": branch, "leaf": leaf}
                expected[tuple(sorted((center, terminal)))] += 1
    edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    n = 5+sum(sum(section) for section in profile)
    assert graph["schema_version"] == 1 and edges == expected and len(edges) == sum(edges.values()) == n-1
    assert sorted(graph["vertices"]) == sorted(roles) and len(roles) == n
    assert graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
    payload = {"vertices": sorted(roles), "edges": sorted(edges.elements()),
               "profile": profile, "spine": spine, "roles": roles}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    digest = sha256(raw).hexdigest()
    assert digest == original["graph_digest"]

    neighbors = {v: set() for v in roles}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    color = {"s:0": 0}
    pending = deque(color)
    while pending:
        u = pending.popleft()
        for v in neighbors[u]:
            if v not in color:
                color[v] = 1 - color[u]
                pending.append(v)
            assert color[u] != color[v]
    low = {v for v, side in color.items() if side == 0}
    high = set(color) - low
    assert low == {"s:0", "b:1:0"} | {v for v in roles if v.startswith("l:0:")}
    assert high == {"s:1", "b:0:0", "b:0:1"} | {v for v in roles if v.startswith("l:1:")}
    assert low | high == set(roles) and (len(low), len(high)) == (9, n-9)
    return edges, neighbors, low, high

def ledger_id(digest, labels):
    payload = {"graph_digest":digest,"labels":sorted(labels.items())}
    return sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def transition(source, original):
    old_edges, old_adj, even_old, odd_old = topology(source, [[4,3],[2]])
    new_edges, new_adj, even, odd = topology(original, [[4,3],[3]])
    leaf, center = "l:1:0:2","b:1:0"
    old, new = source["graph"], original["graph"]
    assert original["graph_digest"] != source["graph_digest"]
    assert set(new["vertices"])-set(old["vertices"]) == {leaf} and set(old["vertices"]) < set(new["vertices"])
    assert all(old["roles"][v] == new["roles"][v] for v in old["vertices"])
    assert new_edges == old_edges + Counter({(center,leaf):1})
    assert new["spine"] == old["spine"] == ["s:0","s:1"]
    assert new_adj[leaf] == {center} and "s:1" in new_adj[center]
    assert old_adj["s:1"] == new_adj["s:1"] == {"s:0",center}
    assert even == even_old and odd == odd_old | {leaf}
    return old_edges, new_edges, new_adj, even, odd


def certificate_audit(source, source_cert, original, certificate):
    old_edges, new_edges, adjacent, even, odd = transition(source, original)
    before, after = source_cert["labels"], certificate["labels"]
    assert set(before) == set(source["graph"]["vertices"])
    assert all(type(v) is int for v in before.values()) and sorted(before.values()) == list(range(14))
    assert set(after) == even | odd and len(after) == 15
    assert all(type(v) is int for v in after.values()) and sorted(after.values()) == list(range(15))
    digest = original["graph_digest"]
    assert source_cert["ledger_id"] == ledger_id(source["graph_digest"], before)
    assert certificate["ledger_id"] == ledger_id(digest, after) and certificate["graph_digest"] == digest
    assert certificate["kind"] == "ordinary_graceful"
    assert {v for v in before if before[v] != after[v]} == {"s:1"}
    assert before["s:1"] == after["l:1:0:2"] == 13 and after["s:1"] == 14
    retained_labels = sorted(after[v] for v in before if v != "s:1")
    assert retained_labels == list(range(13))

    old_weights = {edge:abs(before[edge[0]]-before[edge[1]]) for edge in old_edges}
    assert sorted(old_weights.values()) == list(range(1,14))
    incidence = []
    for edge in original["graph"]["edges"]:
        a,b = edge
        tail,head = (a,b) if a in even else (b,a)
        assert tail in even and head in odd
        delta = after[head]-after[tail]
        incidence.append({"original_edge":edge,"oriented_edge":[tail,head],
                          "oriented_labels":[after[tail],after[head]],"signed_difference":delta,
                          "difference":abs(delta)})
    weights = {tuple(sorted(row["original_edge"])):row["difference"] for row in incidence}
    assert set(weights) == set(new_edges)
    changed = {edge:[old,weights[edge]] for edge,old in old_weights.items() if weights[edge] != old}
    assert changed == {("s:0","s:1"):[13,14],("b:1:0","s:1"):[12,13]}
    assert weights[("b:1:0","l:1:0:2")] == 12
    retained_weights = sorted(old_weights[edge] for edge in old_weights if edge not in changed)
    assert retained_weights == list(range(1,12))
    ordered = [row["difference"] for row in incidence]
    assert ordered == [14,10,8,7,2,1,9,5,4,3,13,6,11,12]
    assert ordered == certificate["checker"]["edge_differences"] and certificate["checker"]["valid"]
    assert Counter(ordered) == Counter(range(1,15))
    unused_labels = sorted(set(range(15))-set(after.values()))
    unused_weights = sorted(set(range(1,15))-set(weights.values()))
    assert not unused_labels and not unused_weights

    even_values, odd_values = sorted(after[v] for v in even), sorted(after[v] for v in odd)
    assert even_values == [0,1,2,3,4,5,6,8,11] and odd_values == [7,9,10,12,13,14]
    separation = {"even_before_odd":max(even_values)<min(odd_values),
                  "odd_before_even":max(odd_values)<min(even_values)}
    assert not any(separation.values())
    reversal = [row for row in incidence if row["signed_difference"]<0]
    assert len(reversal) == 1 and reversal[0]["oriented_edge"] == ["l:0:0:3","b:0:0"]
    assert reversal[0]["signed_difference"] == -1
    spine = original["graph"]["spine"]
    actual = [after[v] for v in spine]
    assert certificate["physical_spine"] == spine and actual == [0,14]
    assert certificate["signed_interface"] == {"physical_spine_labels":actual,
               "negative_edges":[{"edge":reversal[0]["oriented_edge"],"signed_difference":-1}]}
    even_sum = sum(len(adjacent[v])*after[v] for v in even)
    odd_sum = sum(len(adjacent[v])*after[v] for v in odd)
    signed_sum = sum(row["signed_difference"] for row in incidence)
    assert (odd_sum,even_sum,sum(ordered)) == (146,43,105)
    assert signed_sum == odd_sum-even_sum == sum(ordered)-2*reversal[0]["difference"] == 103
    return {"status":"PASS","graph_digest":digest,"incidences":incidence,
            "graph_delta":{"added_vertex":"l:1:0:2","added_edge":["b:1:0","l:1:0:2"],
                           "preserved_old_vertices":len(before),"preserved_old_edges":len(old_edges),
                           "exit_neighbors":sorted(adjacent["s:1"])},
            "changed_old_edge_differences":[{"edge":list(pair),"source":values[0],"target":values[1]}
                                            for pair,values in sorted(changed.items())],
            "retained_label_inventory":retained_labels,"retained_difference_inventory":retained_weights,
            "unused_vertex_labels":unused_labels,"unused_edge_differences":unused_weights,
            "even_vertices":sorted(even),"odd_vertices":sorted(odd),"physical_spine_labels":actual,
            "even_labels":even_values,"odd_labels":odd_values,"separation_tests":separation,
            "weighted_even_sum":even_sum,"weighted_odd_sum":odd_sum,"signed_degree_sum":signed_sum,
            "absolute_difference_sum":sum(ordered),"reversed_edges":reversal}


def controls(original, cert, adverse, retained, incidence):
    assert retained["checker"]["valid"] and retained["graph_digest"] != original["graph_digest"]
    assert sorted(retained["checker"]["edge_differences"]) == list(range(1,14))
    wrong = adverse["wrong_digest"]
    assert wrong["expected"] != original["graph_digest"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    graph, labels = original["graph"], cert["labels"]
    u,v,w = "l:0:0:0","l:0:1:0","l:0:0:3"
    cross, within = adverse["cross_swap"], adverse["within_swap"]
    assert [labels[u],labels[v],labels[w]] == [2,4,11]
    assert cross["vertices"] == [u,v] and cross["labels"] == labels | {u:labels[v],v:labels[u]}
    assert within["vertices"] == [u,w] and within["labels"] == labels | {u:labels[w],w:labels[u]}
    assert sorted(cross["labels"].values()) == sorted(within["labels"].values()) == list(range(15))
    cross_weights = [abs(cross["labels"][a]-cross["labels"][b]) for a,b in graph["edges"]]
    repeats = {str(value):n for value,n in Counter(cross_weights).items() if n>1}
    missing = sorted(set(range(1,15))-set(cross_weights))
    assert repeats == {"6":2,"7":2} and missing == [5,8]
    assert not cross["checker"]["valid"] and cross["checker"]["edge_differences"] == cross_weights
    assert cross["checker"]["errors"] == ["edge differences repeat","edge differences are not exactly 1..m"]
    signed_within = []
    for row in incidence["incidences"]:
        tail,head = row["oriented_edge"]
        delta = within["labels"][head]-within["labels"][tail]
        signed_within.append((row["oriented_edge"],delta))
    actual = [{"edge":edge,"signed_difference":delta} for edge,delta in signed_within if delta<0]
    within_weights = [abs(delta) for _,delta in signed_within]
    assert within["checker"]["valid"] and not within["checker"]["errors"]
    assert within["checker"]["edge_differences"] == within_weights and sorted(within_weights) == list(range(1,15))
    assert actual == [{"edge":[u,"b:0:0"],"signed_difference":-1}]
    gate = within["signed_interface_gate"]
    assert gate["valid"] is False and gate["error"] == "Negative edge differs from the requested named interface"
    assert gate["actual"] == {"physical_spine_labels":[0,14],"negative_edges":actual}
    return {"status":"PASS","cross_swap_repeat_multiplicities":repeats,"cross_swap_missing_weights":missing,
            "within_swap_graceful":True,"within_swap_exact_signed_interface":False,
            "within_swap_actual_negative_edges":actual}
