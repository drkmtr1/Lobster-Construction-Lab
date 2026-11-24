"""Independent named-incidence audit for the frozen D105 original."""

from collections import Counter, deque
from hashlib import sha256
import json


def topology(original, expected_digest):
    graph = original["graph"]
    profile = [[4, 3], [2]]
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
    assert edges == expected and len(edges) == sum(edges.values()) == 13
    assert sorted(graph["vertices"]) == sorted(roles) and len(roles) == 14
    assert graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
    payload = {"vertices": sorted(roles), "edges": sorted(edges.elements()),
               "profile": profile, "spine": spine, "roles": roles}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    digest = sha256(raw).hexdigest()
    assert digest == original["graph_digest"] == expected_digest

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
    assert high == {"s:1", "b:0:0", "b:0:1", "l:1:0:0", "l:1:0:1"}
    assert low | high == set(roles) and (len(low), len(high)) == (9, 5)
    return edges, neighbors, low, high


def certificate_audit(original, expected_digest, certificate):
    edges, neighbors, even, odd = topology(original, expected_digest)
    graph = original["graph"]
    labels = certificate["labels"]
    alphabet = set(range(len(edges)+1))
    assert certificate["kind"] == "ordinary_graceful" and set(labels) == even | odd
    assert all(type(v) is int for v in labels.values()) and len(set(labels.values())) == len(labels) == 14
    unused_labels = sorted(alphabet-set(labels.values()))
    assert not unused_labels and set(labels.values()) == alphabet
    assert certificate["graph_digest"] == expected_digest
    canonical = json.dumps({"graph_digest":expected_digest,"labels":sorted(labels.items())},
                           sort_keys=True,separators=(",",":")).encode()
    assert certificate["ledger_id"] == sha256(canonical).hexdigest()
    actual_spine = [labels[v] for v in graph["spine"]]
    assert certificate["physical_spine"] == graph["spine"] == ["s:0","s:1"]
    assert certificate["physical_spine_labels"] == actual_spine == [0,13]
    assert tuple(graph["spine"]) in edges

    incidence = []
    for pair in graph["edges"]:
        a,b = pair
        tail, head = (a,b) if a in even else (b,a)
        assert tail in even and head in odd
        signed = labels[head]-labels[tail]
        incidence.append({"original_edge":pair,"oriented_edge":[tail,head],
                          "oriented_labels":[labels[tail],labels[head]],
                          "signed_difference":signed,"difference":abs(signed)})
    weights = [row["difference"] for row in incidence]
    expected_order = [13,10,8,7,2,1,9,5,4,3,12,6,11]
    assert weights == certificate["checker"]["edge_differences"] == expected_order
    assert certificate["checker"]["valid"] and not certificate["checker"]["errors"]
    unused_weights = sorted((alphabet-{0})-set(weights))
    assert not unused_weights and Counter(weights) == Counter(range(1,14))

    even_values, odd_values = sorted(labels[v] for v in even), sorted(labels[v] for v in odd)
    assert even_values == [0,1,2,3,4,5,6,8,11] and odd_values == [7,9,10,12,13]
    separations = {"even_before_odd":max(even_values)<min(odd_values),
                   "odd_before_even":max(odd_values)<min(even_values)}
    assert not any(separations.values())
    reversed_edges = [row for row in incidence if row["signed_difference"] < 0]
    assert len(reversed_edges) == 1
    assert reversed_edges[0]["oriented_edge"] == ["l:0:0:3","b:0:0"]
    assert reversed_edges[0]["signed_difference"] == -1
    degrees = {v:len(neighbors[v]) for v in labels}
    even_sum = sum(degrees[v]*labels[v] for v in even)
    odd_sum = sum(degrees[v]*labels[v] for v in odd)
    signed_sum = sum(row["signed_difference"] for row in incidence)
    negative_magnitude = sum(row["difference"] for row in reversed_edges)
    assert (even_sum,odd_sum,sum(weights),negative_magnitude) == (42,131,91,1)
    assert signed_sum == odd_sum-even_sum == sum(weights)-2*negative_magnitude == 89
    return {"status":"PASS","graph_digest":expected_digest,"incidences":incidence,
            "unused_vertex_labels":unused_labels,"unused_edge_differences":unused_weights,
            "physical_spine_labels":actual_spine,"even_vertices":sorted(even),"odd_vertices":sorted(odd),
            "even_labels":even_values,"odd_labels":odd_values,"separation_tests":separations,
            "degrees":degrees,"weighted_even_sum":even_sum,"weighted_odd_sum":odd_sum,
            "signed_degree_sum":signed_sum,"absolute_difference_sum":sum(weights),
            "reversed_edges":reversed_edges,"reversed_total_magnitude":negative_magnitude}


def controls(target, cert, adverse, retained_original, retained_cert, positive):
    source_graph = retained_original["graph"]
    retained_labels = retained_cert["labels"]
    retained_digest = retained_original["graph_digest"]
    payload = {"graph_digest":retained_digest,"labels":sorted(retained_labels.items())}
    ledger = sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert ledger == retained_cert["ledger_id"] == positive["ledger_id"]
    assert retained_digest == positive["graph_digest"] != target["graph_digest"]
    source_weights = [abs(retained_labels[u]-retained_labels[v]) for u,v in source_graph["edges"]]
    assert positive["checker"]["valid"] and source_weights == positive["checker"]["edge_differences"]
    assert sorted(source_weights) == list(range(1,13)) and sorted(retained_labels.values()) == list(range(13))
    graph = target["graph"]
    labels = cert["labels"]
    wrong = adverse["wrong_digest"]
    assert wrong["expected"] != target["graph_digest"] and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    spine = adverse["wrong_spine"]
    assert spine["vertices"] == graph["spine"] and spine["declared"] == [0,12]
    assert spine["actual"] == [labels[v] for v in graph["spine"]] == [0,13]
    assert spine["valid"] is False and spine["error"] == "Declared physical spine labels differ from the original"

    swap = adverse["terminal_swap"]
    u,v = "l:0:0:0","l:0:1:0"
    assert swap["vertices"] == [u,v] and [labels[u],labels[v]] == [2,4]
    changed = labels | {u:labels[v],v:labels[u]}
    assert swap["labels"] == changed and sorted(changed.values()) == list(range(14))
    modified = [abs(changed[a]-changed[b]) for a,b in graph["edges"]]
    repeats = {str(w):n for w,n in Counter(modified).items() if n>1}
    missing = sorted(set(range(1,14))-set(modified))
    assert repeats == {"6":2,"7":2} and missing == [5,8]
    assert not swap["checker"]["valid"] and swap["checker"]["edge_differences"] == modified
    assert swap["checker"]["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]
    return {"status":"PASS","d098_ledger_id":ledger,"swap_repeat_multiplicities":repeats,
            "swap_missing_weights":missing,"swap_actual_edge_differences":modified}


def reconcile_alpha_scope(original, original_sha, previous, incidence):
    digest = original["graph_digest"]
    alpha = previous["alpha_scope"]
    assert previous["status"] == "PASS" and previous["proof_disposition"] == "ACCEPT"
    assert alpha["graph_digest"] == previous["target_graph_digest"] == digest
    assert alpha["original_sha256"] == previous["target_original_sha256"] == original_sha
    assert alpha["alpha_labeling"] == "EXCLUDED" and alpha["cut_9"] == "EXCLUDED"
    assert alpha["cut_5"] == "EXCLUDED_BY_COMPLEMENT" and alpha["ordinary_gracefulness"] == "UNDECIDED"
    assert incidence["graph_digest"] == digest and not any(incidence["separation_tests"].values())
    return {"status":"PASS","graph_digest":digest,"D104_alpha_labeling":"EXCLUDED",
            "D105_ordinary_gracefulness":"ESTABLISHED_WITH_PHYSICAL_LABELS_0_13",
            "reversal_scope":"This certificate only"}
