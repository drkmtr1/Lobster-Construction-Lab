"""Independent named-incidence audit for the frozen D110 original."""

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


def obstruction(original, domain, cases):
    edges, neighbors, even, odd = topology(original, [[5,3],[2]])
    graph = original["graph"]
    a,b,center = "b:0:0","b:0:1","b:1:0"
    entry,exit_name = "s:0","s:1"
    assert len(graph["vertices"])==15 and sum(edges.values())==14
    assert graph["spine"] == [entry,exit_name]
    assert domain["physical_pins"]=={entry:0,exit_name:14,center:1}
    assert (domain["negative_edge_count"],domain["negative_signed_difference"],domain["location"]) == (
        1,-2,"any_left_terminal")
    fixed = domain["physical_pins"]
    assert neighbors[entry] == {exit_name,a,b} and neighbors[exit_name] == {entry,center}

    degrees = {v:len(group) for v,group in neighbors.items()}
    assert [degrees[v] for v in (entry,exit_name,a,b,center)] == [3,2,6,4,3]
    left_a,left_b,right = [neighbors[v]-set(fixed) for v in (a,b,center)]
    assert [len(group) for group in (left_a,left_b,right)] == [5,3,2]
    assert all(neighbors[leaf] == {host} for host,group in ((a,left_a),(b,left_b),(center,right)) for leaf in group)
    assert even == {entry,center} | left_a | left_b and odd == {exit_name,a,b} | right

    # Subtract the odd unweighted labels from the total, then add pinned even excess.
    m = len(edges)
    total = m*(m+1)//2
    even_constant = total-fixed[exit_name]+sum((degrees[v]-1)*fixed[v] for v in even & fixed.keys())
    odd_constant = degrees[exit_name]*fixed[exit_name]
    required_signed = total+2*domain["negative_signed_difference"]
    center_a,center_b = degrees[a]+1,degrees[b]+1
    right_coefficient = 2
    rhs = required_signed+even_constant-odd_constant
    assert (total,even_constant,odd_constant,required_signed,center_a,center_b,rhs) == (105,93,28,101,7,5,166)
    assert rhs%2==0 and center_a%2==center_b%2==1
    assert abs(fixed[exit_name]-fixed[entry])==14 and abs(fixed[exit_name]-fixed[center])==13
    remaining_places = set(graph["vertices"])-set(fixed)-{a,b}
    assert remaining_places == right | left_a | left_b
    # A center at 13 repeats the fixed attachment weight. All left leaves outside
    # the sole sign reversal must be lower than their center of label at most 12.

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
    assert bound_even==110 and bound_odd==112 and max(bound_even,bound_odd)<threshold==116
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
        assert rem==0 and q in free and q==b_label
        assert row == {"A":a_label,"B":b_label,"P":13,"Q":q,"collision_label":q}
        assert b not in right
        right_rows.append({"row":row,"left_center_vertex":b,"colliding_right_terminal_one_of":sorted(right)})

    left_groups = {a:sorted(left_a),b:sorted(left_b)}
    reversed_center_label = m-1+domain["negative_signed_difference"]
    assert reversed_center_label==11 and reversed_center_label-(m-1)==-2
    available = sorted(free-{reversed_center_label})
    best_right_labels = available[-2:]
    right_sum_bound = sum(best_right_labels)
    assert best_right_labels==[10,12] and right_sum_bound==22
    other_center_values = [label for label in available if label%2==reversed_center_label%2]
    assert max(other_center_values)==9
    reduced_first = rhs-center_a*reversed_center_label
    min_b = (reduced_first-right_coefficient*right_sum_bound+center_b-1)//center_b
    forced_b = [label for label in other_center_values if label>=min_b]
    assert min_b==9 and forced_b==[9]
    b_label = forced_b[0]
    right_sum,rem = divmod(reduced_first-center_b*b_label,right_coefficient)
    assert rem==0 and right_sum==right_sum_bound and b_label not in best_right_labels
    assert len(set(best_right_labels))==2 and sorted(available)[-2:]==best_right_labels

    left_weights = {reversed_center_label-fixed[entry]:[entry,a],b_label-fixed[entry]:[entry,b]}
    right_weights = sorted(label-fixed[center] for label in best_right_labels)
    assert sorted(left_weights)==right_weights==[9,11]
    left_edges = {tuple(sorted(edge)) for edge in left_weights.values()}
    assert len(left_edges)==2 and left_edges<=set(edges)
    right_pairs = {tuple(edge) for edge in right_edges}
    assert len(right_pairs)==2 and right_pairs<=set(edges) and left_edges.isdisjoint(right_pairs)
    repeats = {str(weight):n for weight,n in Counter([*left_weights,*right_weights]).items() if n>1}
    assert repeats=={"9":2,"11":2}
    first = cases["label_13_first_left_reversal"]
    assert first == {"A":reversed_center_label,"B":b_label,"rhs":reduced_first,
                     "right_sum_upper_bound":right_sum_bound,"right_labels":best_right_labels,
                     "forced_repeat_multiplicities":repeats}
    witnesses = [{"weight":label-fixed[center],"left_attachment":left_weights[label-fixed[center]],
                 "right_terminal_label":label,"right_edge_one_of":right_edges} for label in best_right_labels]

    reduced_second = rhs-center_b*reversed_center_label
    a_bound = max(other_center_values)
    lhs_bound = center_a*a_bound+right_coefficient*right_sum_bound
    assert lhs_bound==107 and reduced_second==111 and lhs_bound<reduced_second
    second = cases["label_13_second_left_reversal"]
    assert second == {"B":reversed_center_label,"rhs":reduced_second,"A_upper_bound":a_bound,
                      "right_sum_upper_bound":right_sum_bound,"lhs_upper_bound":lhs_bound,"survivors":[]}

    return {"status":"PASS","graph_digest":original["graph_digest"],"degrees":degrees,
            "physical_spine":graph["spine"],"even_class":sorted(even),"odd_class":sorted(odd),
            "degree_sum":{"even_constant":even_constant,"odd_constant":odd_constant,
                          "required_signed_sum":required_signed,"center_coefficients":[center_a,center_b],
                          "each_right_terminal_coefficient":right_coefficient,"rhs":rhs,"same_center_parity":True},
            "left_terminal_groups":left_groups,"possible_locations_of_13":{"right_terminals":sorted(right),
                "left_terminals_if_reversed":left_groups},
            "right_terminal_case":right_rows,
            "first_left_reversal_case":{"row":first,"forced_repeat_witnesses":witnesses},
            "second_left_reversal_case":second}


def signed_deltas(graph, labels, even):
    signed = []
    for u,v in graph["edges"]:
        tail,head = (u,v) if u in even else (v,u)
        signed.append({"edge":[tail,head],"signed_difference":labels[head]-labels[tail]})
    return signed


def audit_gate(graph, neighbors, labels, signed, gate, magnitude):
    pins = {v:labels[v] for v in ("s:0","s:1","b:1:0")}
    pins_valid = tuple(pins.values()) == (0,14,1)
    negatives = [row for row in signed if row["signed_difference"]<0]
    left_pairs = {(v,next(iter(neighbors[v]))) for v,role in graph["roles"].items()
                  if role["kind"]=="leaf" and role["section"]==0 and len(neighbors[v])==1}
    membership = {tuple(row["edge"]) for row in negatives}
    magnitudes = {row["signed_difference"] for row in negatives}
    signed_tests = {"one_negative_edge":len(negatives)==1,"required_negative_magnitude":magnitudes=={-magnitude},
                    "negative_edges_are_left_terminal_incidence":bool(negatives) and membership<=left_pairs}
    pattern_valid = all(signed_tests.values())
    assert gate == {"magnitude":magnitude,"physical_pins":pins,"negative_edges":negatives,"pins_valid":pins_valid,
                    "signed_tests":signed_tests,"pattern_valid":pattern_valid,"valid":pins_valid and pattern_valid}


def controls(original, cert, recorded, positive):
    graph, digest = original["graph"], original["graph_digest"]
    edges,neighbors,even,odd = topology(original, [[4,3],[3]])
    labels = cert["labels"]
    spectrum = list(range(1,len(edges)+1))
    alphabet = [0,*spectrum]
    assert set(labels)==even | odd and sorted(labels.values())==alphabet
    assert ledger_id(digest,labels)==cert["ledger_id"]==positive["ledger_id"]
    signed = signed_deltas(graph,labels,even)
    weights = [abs(row["signed_difference"]) for row in signed]
    assert sorted(weights)==spectrum and positive["checker"]["valid"] and positive["checker"]["edge_differences"]==weights

    audit_gate(graph,neighbors,labels,signed,positive["magnitude_one"],1)
    audit_gate(graph,neighbors,labels,signed,positive["magnitude_two"],2)
    assert positive["magnitude_one"]["valid"] and not positive["magnitude_two"]["valid"]
    assert positive["magnitude_two"]["pins_valid"] and not positive["magnitude_two"]["pattern_valid"]
    retained_negative = positive["magnitude_one"]["negative_edges"]
    assert retained_negative==cert["signed_interface"]["negative_edges"]==[
        {"edge":["l:0:0:3","b:0:0"],"signed_difference":-1}]

    wrong = recorded["wrong_digest"]
    assert wrong["expected"]!=digest and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"]==["original graph digest mismatch"]
    u,w,v = "l:0:0:0","l:0:0:3","l:1:0:1"
    within,complement,fixture = recorded["within_swap"],recorded["complement"],recorded["gate_only_fixture"]
    assert within["vertices"]==[u,w] and within["labels"]==labels | {u:labels[w],w:labels[u]}
    assert complement["labels"]=={key:len(edges)-label for key,label in labels.items()}
    assert fixture["vertices"]==[w,v] and [labels[w],labels[v]]==[11,12]
    assert fixture["labels"]==labels | {w:labels[v],v:labels[w]}

    audited = {}
    for name,item in (("within",within),("complement",complement),("fixture",fixture)):
        changed = item["labels"]
        assert set(changed)==set(labels) and sorted(changed.values())==alphabet
        directions = signed_deltas(graph,changed,even)
        changed_weights = [abs(row["signed_difference"]) for row in directions]
        assert item["checker"]["edge_differences"]==changed_weights
        assert item["checker"]["valid"]==(sorted(changed_weights)==spectrum)
        audit_gate(graph,neighbors,changed,directions,item["magnitude_two"],2)
        audited[name] = (directions,changed_weights)
    audit_gate(graph,neighbors,within["labels"],audited["within"][0],within["magnitude_one"],1)
    assert within["checker"]["valid"] and within["magnitude_one"]["valid"] and not within["magnitude_two"]["valid"]
    assert within["magnitude_one"]["negative_edges"] == [{"edge":[u,"b:0:0"],"signed_difference":-1}]

    complement_signed = [row["signed_difference"] for row in audited["complement"][0]]
    assert complement_signed == [-row["signed_difference"] for row in signed]
    assert sorted(weight for weight in complement_signed if weight<0)==list(range(-14,-1))
    assert complement["checker"]["valid"] and not complement["magnitude_two"]["pins_valid"]
    assert not complement["magnitude_two"]["pattern_valid"] and not complement["magnitude_two"]["valid"]

    changed_weights = audited["fixture"][1]
    repeats = {str(weight):n for weight,n in Counter(changed_weights).items() if n>1}
    missing = sorted(set(spectrum)-set(changed_weights))
    assert not fixture["checker"]["valid"] and fixture["magnitude_two"]["valid"]
    assert fixture["checker"]["errors"]==["edge differences repeat","edge differences are not exactly 1..m"]
    assert fixture["magnitude_two"]["negative_edges"]==[{"edge":[w,"b:0:0"],"signed_difference":-2}]
    assert repeats=={"2":2,"10":2} and missing==[1,11]
    fixture_changes = [{"edge":before["edge"],"signed_before":before["signed_difference"],
                        "signed_after":after["signed_difference"]}
                       for before,after in zip(signed,audited["fixture"][0],strict=True) if before!=after]
    assert fixture_changes==[{"edge":[w,"b:0:0"],"signed_before":-1,"signed_after":-2},
                             {"edge":["b:1:0",v],"signed_before":11,"signed_after":10}]
    return {"status":"PASS","retained_ordinary":True,"retained_magnitude_one":True,"retained_magnitude_two":False,
            "within_ordinary":True,"within_magnitude_one":True,"within_magnitude_two":False,
            "complement_ordinary":True,"complement_pins":False,"complement_pattern":False,
            "complement_negative_count":13,"complement_signed_differences":complement_signed,
            "fixture_ordinary":False,"fixture_magnitude_two":True,"fixture_repeat_multiplicities":repeats,
            "fixture_missing_weights":missing,"fixture_incidence_changes":fixture_changes}
