"""Independent named-incidence audit for the frozen D109 original."""

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
        1,-1,"any_left_terminal")
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
    required_signed = total-2
    center_a,center_b = degrees[a]+1,degrees[b]+1
    right_coefficient = 2
    rhs = required_signed+even_constant-odd_constant
    assert (total,even_constant,odd_constant,required_signed,center_a,center_b,rhs) == (105,93,28,103,7,5,168)
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

    left_groups = {a:sorted(left_a),b:sorted(left_b)}
    attached = {a:[entry,a],b:[entry,b]}
    coefficients = {a:center_a,b:center_b}
    assert all(tuple(sorted(edge)) in edges for edge in attached.values())
    terminal_cases = []
    for high_center, key in ((a,"label_13_first_left_reversal"),(b,"label_13_second_left_reversal")):
        other = b if high_center==a else a
        major = m-1+domain["negative_signed_difference"]
        assert major==12 and major-(m-1)==-1
        available = sorted(free-{major})
        right_bound = sum(available[-2:])
        reduced_rhs = rhs-coefficients[high_center]*major
        lower = (reduced_rhs-right_coefficient*right_bound+coefficients[other]-1)//coefficients[other]
        other_values = [value for value in available if value>=lower and value%2==major%2]
        assert other_values == [10]
        centers = {high_center:major,other:other_values[0]}
        remaining_max = max(set(available)-set(centers.values()))
        assert remaining_max==11
        first_delta,second_delta = centers[a]-remaining_max,centers[b]-remaining_max
        assert centers[high_center]-remaining_max==1 and centers[other]-remaining_max==-1
        weight = remaining_max-fixed[center]
        assert weight==centers[other]-fixed[entry]
        assert all(set(edge)!=set(attached[other]) for edge in right_edges)
        right_sum,rem = divmod(reduced_rhs-coefficients[other]*centers[other],right_coefficient)
        assert rem==0
        record = {"A":centers[a],"B":centers[b],"rhs":reduced_rhs,"right_sum_upper_bound":right_bound,
                  "forced_right_sum":right_sum,"first_left_signed_if_11":first_delta,
                  "second_left_signed_if_11":second_delta,"repeated_weight":weight}
        assert cases[key]==record
        terminal_cases.append({"case":key,"row":record,"reversed_center":high_center,
                               "possible_reversed_terminals":left_groups[high_center],"minimum_other_center":lower,
                               "label_11":remaining_max,
                               "left_exclusions":{"repeat_weight_one":{"center":high_center,
                                                    "candidate_group":left_groups[high_center],"condition":"terminal distinct from the one carrying 13"},
                                                   "second_negative":{"center":other,"terminals":left_groups[other]}},
                               "right_edge_witness":{"terminal_label":remaining_max,"one_of":right_edges},
                               "distinct_left_attachment":attached[other]})
    return {"status":"PASS","graph_digest":original["graph_digest"],"degrees":degrees,
            "physical_spine":graph["spine"],"even_class":sorted(even),"odd_class":sorted(odd),
            "degree_sum":{"even_constant":even_constant,"odd_constant":odd_constant,
                          "required_signed_sum":required_signed,"center_coefficients":[center_a,center_b],
                          "each_right_terminal_coefficient":right_coefficient,"rhs":rhs,"same_center_parity":True},
            "left_terminal_groups":left_groups,"possible_locations_of_13":{"right_terminals":sorted(right),
                "left_terminals_if_reversed":left_groups},
            "right_terminal_case":right_rows,"left_terminal_cases":terminal_cases}


def signed_deltas(graph, labels, even):
    signed = []
    for u,v in graph["edges"]:
        tail,head = (u,v) if u in even else (v,u)
        signed.append({"edge":[tail,head],"signed_difference":labels[head]-labels[tail]})
    return signed


def audit_gate(graph, neighbors, labels, signed, gate):
    pins = {v:labels[v] for v in ("s:0","s:1","b:1:0")}
    pins_valid = tuple(pins.values()) == (0,14,1)
    negatives = [row for row in signed if row["signed_difference"]<0]
    left_pairs = {(v,next(iter(neighbors[v]))) for v,role in graph["roles"].items()
                  if role["kind"]=="leaf" and role["section"]==0 and len(neighbors[v])==1}
    membership = {tuple(row["edge"]) for row in negatives}
    magnitudes = {row["signed_difference"] for row in negatives}
    signed_tests = {"one_negative_edge":len(negatives)==1,"negative_magnitude_one":magnitudes=={-1},
                    "negative_edges_are_left_terminal_incidence":bool(negatives) and membership<=left_pairs}
    pattern_valid = all(signed_tests.values())
    assert gate == {"physical_pins":pins,"negative_edges":negatives,"pins_valid":pins_valid,
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
    audit_gate(graph,neighbors,labels,signed,positive["signed_gate"])
    assert positive["signed_gate"]["valid"]

    wrong = recorded["wrong_digest"]
    assert wrong["expected"]!=digest and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"]==["original graph digest mismatch"]
    u,v,w = "l:0:0:0","l:0:1:0","l:0:0:3"
    cross,within = recorded["cross_swap"],recorded["within_swap"]
    assert cross["vertices"]==[u,v] and cross["labels"]==labels | {u:labels[v],v:labels[u]}
    assert within["vertices"]==[u,w] and within["labels"]==labels | {u:labels[w],w:labels[u]}
    assert sorted(cross["labels"].values())==sorted(within["labels"].values())==alphabet
    cross_weights = [abs(row["signed_difference"]) for row in signed_deltas(graph,cross["labels"],even)]
    repeats = {str(w):n for w,n in Counter(cross_weights).items() if n>1}
    missing = sorted(set(spectrum)-set(cross_weights))
    assert repeats=={"6":2,"7":2} and missing==[5,8]
    assert not cross["checker"]["valid"] and cross["checker"]["edge_differences"]==cross_weights
    assert cross["checker"]["errors"]==["edge differences repeat","edge differences are not exactly 1..m"]

    complemented = recorded["complement"]
    assert complemented["labels"]=={v:len(edges)-label for v,label in labels.items()}
    for row in (within,complemented):
        changed = signed_deltas(graph,row["labels"],even)
        changed_weights = [abs(edge["signed_difference"]) for edge in changed]
        assert row["checker"]["valid"] and row["checker"]["edge_differences"]==changed_weights
        assert sorted(changed_weights)==spectrum
        audit_gate(graph,neighbors,row["labels"],changed,row["gate"])
    assert within["gate"]["valid"]
    assert within["gate"]["negative_edges"] == [{"edge":[u,"b:0:0"],"signed_difference":-1}]
    complement_signed = [row["signed_difference"] for row in signed_deltas(graph,complemented["labels"],even)]
    assert complement_signed == [-row["signed_difference"] for row in signed]
    assert not complemented["gate"]["pins_valid"] and not complemented["gate"]["pattern_valid"]
    assert not complemented["gate"]["valid"] and sorted(w for w in complement_signed if w<0)==list(range(-14,-1))
    return {"status":"PASS","cross_swap_repeat_multiplicities":repeats,"cross_swap_missing_weights":missing,
            "within_swap_ordinary":True,"within_swap_relaxed_interface":True,
            "complement_ordinary":True,"complement_pins":False,"complement_pattern":False,
            "complement_signed_differences":complement_signed,"complement_negative_count":13}
