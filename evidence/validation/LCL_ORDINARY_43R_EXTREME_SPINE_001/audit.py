"""Independent named-incidence audit for the frozen D107 original."""

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


def boundary(original, certificate, positive):
    graph = original["graph"]
    profile = graph["profile"]
    assert profile in ([[4,3],[2]], [[4,3],[3]])
    r = profile[1][0]
    edges, neighbors, even, odd = topology(original, [[4,3],[r]])
    m = r+11
    digest = original["graph_digest"]
    labels = certificate["labels"]
    assert certificate["kind"] == "ordinary_graceful"
    assert set(labels) == even | odd and len(labels) == r+12
    assert all(type(value) is int for value in labels.values()) and sorted(labels.values()) == list(range(m+1))
    assert certificate["graph_digest"] == positive["graph_digest"] == digest
    assert ledger_id(digest, labels) == positive["ledger_id"] == certificate["ledger_id"]
    assert certificate["physical_spine"] == graph["spine"] == ["s:0","s:1"]
    assert [labels[v] for v in graph["spine"]] == [0,m]
    assert neighbors["s:1"] == {"s:0","b:1:0"}

    fixed = {"s:0":0,"b:0:0":10,"b:0:1":9,"b:1:0":1,
             "l:0:0:0":2,"l:0:0:1":3,"l:0:0:2":8,"l:0:0:3":11,
             "l:0:1:0":4,"l:0:1:1":5,"l:0:1:2":6,"l:1:0:0":7}
    assert all(labels[v] == value for v,value in fixed.items()) and sorted(fixed.values()) == list(range(12))
    leaves = [f"l:1:0:{k}" for k in range(1,r)]
    assert set(labels) == set(fixed) | set(leaves) | {"s:1"}
    assert all(labels[v] == 11+k for k,v in enumerate(leaves,1))
    assert [labels[v] for v in leaves] == list(range(12,r+11))

    indexed_edges = {("b:1:0",v) for v in leaves}
    right_attachment = ("b:1:0","s:1")
    spine_edge = ("s:0","s:1")
    expected_fixed = {("b:0:0","s:0"),("b:0:1","s:0"),("b:1:0","l:1:0:0")}
    expected_fixed |= {(f"b:0:{i}",f"l:0:{i}:{k}") for i,q in enumerate((4,3)) for k in range(q)}
    groups = {"fixed":expected_fixed,"indexed_right":indexed_edges,
              "right_attachment":{right_attachment},"spine":{spine_edge}}
    assert Counter(edge for group in groups.values() for edge in group) == edges

    incidence = []
    for pair in graph["edges"]:
        u,v = pair
        tail,head = (u,v) if u in even else (v,u)
        assert tail in even and head in odd
        w = labels[head]-labels[tail]
        incidence.append({"original_edge":pair,"oriented_edge":[tail,head],"signed_difference":w,"difference":abs(w)})
    absolute = {tuple(sorted(row["original_edge"])):row["difference"] for row in incidence}
    partitions = {group:sorted(absolute[edge] for edge in members) for group,members in groups.items()}
    assert partitions == {"fixed":list(range(1,11)),"indexed_right":list(range(11,r+10)),
                          "right_attachment":[r+10],"spine":[m]}
    ordered = [row["difference"] for row in incidence]
    assert ordered == positive["checker"]["edge_differences"] and Counter(ordered) == Counter(range(1,m+1))
    negatives = [row for row in incidence if row["signed_difference"]<0]
    assert len(negatives)==1 and negatives[0]["oriented_edge"] == ["l:0:0:3","b:0:0"]
    assert negatives[0]["signed_difference"] == -1
    even_sum = sum(len(neighbors[v])*labels[v] for v in even)
    odd_sum = sum(len(neighbors[v])*labels[v] for v in odd)
    assert even_sum == r+40 and odd_sum == 2*m+93+((r-1)*(r+22))//2
    signed = sum(row["signed_difference"] for row in incidence)
    assert signed == odd_sum-even_sum == m*(m+1)//2-2
    assert max(labels[v] for v in even)>min(labels[v] for v in odd)
    assert max(labels[v] for v in odd)>min(labels[v] for v in even)
    return {"status":"PASS","r":r,"graph_digest":digest,"ledger_id":certificate["ledger_id"],
            "pointwise_formula_agreement":True,"incidences":incidence,"label_inventory":sorted(labels.values()),
            "difference_partitions":partitions,"unused_label_inventory":[],"unused_difference_inventory":[],
            "weighted_even_sum":even_sum,"weighted_odd_sum":odd_sum,"signed_degree_sum":signed,
            "negative_edges":negatives,"physical_spine_labels":[0,m]}


def retained_step(originals, certificates, reports):
    source, target = [record["graph"] for record in originals]
    before, after = [certificate["labels"] for certificate in certificates]
    leaf = "l:1:0:2"
    assert target["vertices"] == [*source["vertices"],leaf]
    assert target["roles"][leaf] == {"kind":"leaf","section":1,"branch":0,"leaf":2}
    assert all(source["roles"][v] == target["roles"][v] for v in source["vertices"])
    assert target["edges"] == [*source["edges"],["b:1:0",leaf]] and target["spine"] == source["spine"]
    assert {v for v in before if before[v] != after[v]} == {"s:1"}
    assert before["s:1"]==after[leaf]==13 and after["s:1"]==14
    old,new = ({tuple(row["original_edge"]):row["signed_difference"] for row in report["incidences"]}
               for report in reports)
    changes = {edge:[old[edge],new[edge]] for edge in old if old[edge]!=new[edge]}
    assert changes == {("s:0","s:1"):[13,14],("s:1","b:1:0"):[12,13]}
    assert new["b:1:0",leaf] == 12
    unchanged = sorted(abs(weight) for edge,weight in old.items() if edge not in changes)
    assert unchanged == list(range(1,12))
    return {"status":"PASS","scope":"archived r=2 to archived r=3",
            "added_vertex":leaf,"added_edge":["b:1:0",leaf],"added_signed_difference":12,
            "changed_signed_edges":[{"edge":list(edge),"old_and_new":changes[edge]} for edge in sorted(changes)],
            "unchanged_old_difference_inventory":unchanged}


def controls(original, cert, adverse, incidence):
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
