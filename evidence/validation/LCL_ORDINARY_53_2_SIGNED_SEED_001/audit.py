"""Independent named-incidence audit for the frozen D108 original."""

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
    n = len(roles)
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
    assert low | high == set(roles) and (len(low), len(high)) == (2+sum(profile[0]), 3+sum(profile[1]))
    return edges, neighbors, low, high

def ledger_id(digest, labels):
    payload = {"graph_digest":digest,"labels":sorted(labels.items())}
    return sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def obstruction(source, original, domain, cases):
    source_edges, _, _, _ = topology(source, [[4,3],[2]])
    edges, neighbors, even, odd = topology(original, [[5,3],[2]])
    old, new = source["graph"], original["graph"]
    fresh, a, b, center = "l:0:0:4","b:0:0","b:0:1","b:1:0"
    entry, exit_name, reversed_leaf = "s:0","s:1","l:0:0:3"
    assert len(new["vertices"])==15 and sum(edges.values())==14
    assert set(new["vertices"]) == set(old["vertices"]) | {fresh} and fresh not in old["vertices"]
    assert [v for v in new["vertices"] if v!=fresh] == old["vertices"]
    assert edges == source_edges + Counter({(a,fresh):1}) and neighbors[fresh] == {a}
    assert [edge for edge in new["edges"] if fresh not in edge] == old["edges"]
    assert all(old["roles"][v] == new["roles"][v] for v in old["vertices"])
    assert new["spine"] == old["spine"] == [entry,exit_name]
    assert domain["physical_spine_labels"] == [0,14] and domain["right_center_label"] == 1
    assert domain["reversed_edge"] == {"edge":[reversed_leaf,a],"signed_difference":-1}
    fixed = {entry:0,exit_name:14,center:1}
    assert neighbors[entry] == {exit_name,a,b} and neighbors[exit_name] == {entry,center}

    degrees = {v:len(group) for v,group in neighbors.items()}
    assert [degrees[v] for v in (entry,exit_name,a,b,center)] == [3,2,6,4,3]
    left_a,left_b,right = [neighbors[v]-set(fixed) for v in (a,b,center)]
    assert [len(group) for group in (left_a,left_b,right)] == [5,3,2]
    assert all(neighbors[leaf] == {host} for host,group in ((a,left_a),(b,left_b),(center,right)) for leaf in group)
    assert even == {entry,center} | left_a | left_b and odd == {exit_name,a,b} | right
    assert reversed_leaf in left_a and neighbors[reversed_leaf] == {a}

    # Subtract the odd unweighted labels from the total, then add pinned even excess.
    m = len(edges)
    total = m*(m+1)//2
    even_constant = total-fixed[exit_name]+sum((degrees[v]-1)*fixed[v] for v in even & fixed.keys())
    odd_constant = degrees[exit_name]*fixed[exit_name]
    required_signed = total-2
    center_a,center_b = degrees[a]+1,degrees[b]+1
    right_coefficient = 2
    rhs = required_signed+even_constant-odd_constant
    assert (total,even_constant,odd_constant,required_signed,center_a,center_b,rhs) == (105,93,28,103,7,5,168)
    assert rhs%2==0 and center_a%2==center_b%2==1
    assert abs(fixed[exit_name]-fixed[entry])==14 and abs(fixed[exit_name]-fixed[center])==13
    remaining_places = set(new["vertices"])-set(fixed)-{a,b}
    assert remaining_places == right | {reversed_leaf} | ((left_a | left_b)-{reversed_leaf})
    # A center at 13 repeats the fixed attachment weight. All left leaves outside
    # the selected sign reversal must be lower than their center of label at most 12.

    case_one = cases["label_13_right_terminal"]
    right_bound = m-2
    free = set(range(m+1))-set(fixed.values())-{m-1}
    center_values = free-{right_bound}
    odd_values = sorted(value for value in center_values if value%2)
    even_values = sorted(center_values-set(odd_values))
    rhs_one = rhs-right_coefficient*(m-1)
    threshold = rhs_one-right_coefficient*right_bound
    bound_even = center_a*even_values[-1]+center_b*even_values[-2]
    bound_odd = center_a*odd_values[-1]+center_b*odd_values[-3]
    assert bound_even==110 and bound_odd==112 and max(bound_even,bound_odd)<threshold==118
    assert case_one == {"rhs":rhs_one,"other_right_upper_bound":right_bound,
                        "center_expression_lower_bound":threshold,"even_pair_upper_bound":bound_even,
                        "other_odd_pair_upper_bound":bound_odd,"survivors":case_one["survivors"]}
    assert [(row["A"],row["B"]) for row in case_one["survivors"]] == [
        (odd_values[-1],odd_values[-2]),(odd_values[-2],odd_values[-1])]
    right_edges = [[center,v] for v in sorted(right)]
    left_attachment = [entry,b]
    assert tuple(sorted(left_attachment)) in edges
    assert all(tuple(edge) in edges and set(edge)!=set(left_attachment) for edge in right_edges)
    right_rows = []
    for row in case_one["survivors"]:
        a_label,b_label = row["A"],row["B"]
        q, rem = divmod(rhs_one-center_a*a_label-center_b*b_label,right_coefficient)
        assert rem==0 and q in free and q not in {a_label,b_label}
        weight = q-fixed[center]
        assert row == {"A":a_label,"B":b_label,"P":13,"Q":q,"repeated_weight":weight}
        assert weight==b_label-fixed[entry]
        right_rows.append({"row":row,"right_edge_witness":{"terminal_label":q,"one_of":right_edges},
                           "distinct_left_attachment":left_attachment,"repeated_weight":weight})

    case_two = cases["label_13_designated_terminal"]
    first_center = (m-1)+domain["reversed_edge"]["signed_difference"]
    available = sorted(free-{first_center})
    right_sum_bound = sum(available[-2:])
    rhs_two = rhs-center_a*first_center
    min_b = (rhs_two-right_coefficient*right_sum_bound+center_b-1)//center_b
    parity_choices = [label for label in available if label>=min_b and label%2==first_center%2]
    assert parity_choices == [10]
    second_center = parity_choices[0]
    free_top = max(set(available)-{second_center})
    assert free_top==11
    assert first_center-(m-1)==-1
    first_left_weight,second_left_sign = first_center-free_top,second_center-free_top
    assert first_left_weight==1 and second_left_sign==-1
    right_weight = free_top-fixed[center]
    assert right_weight==second_center-fixed[entry]
    assert case_two == {"A":first_center,"B":second_center,"rhs":rhs_two,"right_sum_upper_bound":right_sum_bound,
                        "forced_right_sum":(rhs_two-center_b*second_center)//right_coefficient,
                        "first_left_weight_if_11":first_left_weight,"second_left_signed_if_11":second_left_sign,
                        "repeated_weight":right_weight}
    return {"status":"PASS","graph_digest":original["graph_digest"],
            "graph_delta":{"vertex":fresh,"edge":[a,fresh],"preserved_old_vertices":14,"preserved_old_edges":13},
            "degrees":degrees,"even_class":sorted(even),"odd_class":sorted(odd),
            "degree_sum":{"even_constant":even_constant,"odd_constant":odd_constant,
                          "required_signed_sum":required_signed,"center_coefficients":[center_a,center_b],
                          "each_right_terminal_coefficient":right_coefficient,"rhs":rhs,"same_center_parity":True},
            "possible_locations_of_13":{"right_terminals":sorted(right),"designated_reversed_terminal":reversed_leaf},
            "right_terminal_case":right_rows,
            "designated_terminal_case":{"row":case_two,"minimum_B":min_b,"label_11":free_top,
                                        "first_left_exclusion":{"possible_vertices":sorted(left_a-{reversed_leaf}),
                                                                "reason":"repeat of the designated absolute weight 1"},
                                        "second_left_exclusion":{"possible_vertices":sorted(left_b),
                                                                 "reason":"second negative signed edge"},
                                        "right_edge_witness":{"terminal_label":free_top,"one_of":right_edges},
                                        "distinct_left_attachment":left_attachment}}


def retained_boundary(original, cert, positive):
    edges, _, even, odd = topology(original, [[4,3],[3]])
    labels = cert["labels"]
    assert ledger_id(original["graph_digest"],labels)==cert["ledger_id"]==positive["ledger_id"]
    assert set(labels)==even | odd and sorted(labels.values())==list(range(15))
    assert [labels[v] for v in original["graph"]["spine"]]==[0,14]
    incidence = []
    for u,v in original["graph"]["edges"]:
        tail,head = (u,v) if u in even else (v,u)
        incidence.append({"oriented_edge":[tail,head],"signed_difference":labels[head]-labels[tail]})
    weights = [abs(row["signed_difference"]) for row in incidence]
    assert len(edges)==14 and sorted(weights)==list(range(1,15))
    assert weights==positive["checker"]["edge_differences"] and positive["checker"]["valid"]
    assert [row for row in incidence if row["signed_difference"]<0] == [
        {"oriented_edge":["l:0:0:3","b:0:0"],"signed_difference":-1}]
    return {"incidences":incidence}


def controls(original, cert, adverse, positive):
    incidence = retained_boundary(original, cert, positive)
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
