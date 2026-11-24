"""Audit the exact original, arithmetic constraints and incidence witnesses independently."""

from collections import Counter, deque
from hashlib import sha256
import json


def inspect(original):
    graph = original["graph"]
    roles = {"s:0":{"kind":"spine","section":0}, "s:1":{"kind":"spine","section":1}}
    edges = [("s:0","s:1")]
    for i, quotas in enumerate(((4,2),(2,))):
        for j, quota in enumerate(quotas):
            center = f"b:{i}:{j}"
            roles[center] = {"kind":"branch","section":i,"branch":j}
            edges.append((f"s:{i}",center))
            for k in range(quota):
                leaf = f"l:{i}:{j}:{k}"
                roles[leaf] = {"kind":"leaf","section":i,"branch":j,"leaf":k}
                edges.append((center,leaf))
    assert graph["profile"] == [[4,2],[2]] and graph["roles"] == roles and graph["schema_version"] == 1
    assert graph["spine"] == ["s:0","s:1"] and Counter(graph["vertices"]) == Counter(list(roles))
    assert Counter(map(frozenset,graph["edges"])) == Counter(map(frozenset,edges))
    assert len(roles) == 13 and len(edges) == 12
    canonical = {"vertices":sorted(roles),"edges":sorted(sorted(edge) for edge in edges),
                 "profile":[[4,2],[2]],"spine":["s:0","s:1"],"roles":roles}
    digest = sha256(json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    assert digest == original["graph_digest"]
    adjacency = {v:set() for v in roles}
    for u,v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    depth, queue = {"s:0":0}, deque(["s:0"])
    while queue:
        v = queue.popleft()
        for u in adjacency[v]-depth.keys():
            depth[u] = depth[v]+1
            queue.append(u)
    assert len(depth) == 13
    lows = {v for v in depth if depth[v]%2 == 0}
    assert len(lows) == 8 and all((u in lows) != (v in lows) for u,v in edges)
    return adjacency, lows


def check_reduction(adj, lows, reduction, rows):
    degrees = {v:len(n) for v,n in adj.items()}
    coefficients = {v:(1 if v not in lows else -1)*(n-1) for v,n in degrees.items() if n>1}
    signed_baseline = sum(range(8,13))-sum(range(8))
    total = 12*13//2
    assert reduction["degrees"] == degrees and reduction["low_names"] == sorted(lows)
    assert reduction["signed_excess"] == coefficients == {"s:0":-2,"s:1":1,"b:0:0":4,"b:0:1":2,"b:1:0":-2}
    assert reduction["baseline_signed_sum"] == signed_baseline == 22
    assert reduction["required_sum"] == total == 78
    assert reduction["reduced_rhs"] == total-signed_baseline-12*coefficients["b:0:1"] == 32
    assert reduction["possible_exits"] == [8,10] and reduction["entrance_bound"] == [0,2]
    pairs = {w:{(h,h-w) for h in range(8,13) if 0 <= h-w < 8} for w in range(8,13)}
    assert all(pairs[w] == set(map(tuple,reduction["high_low_pairs"][str(w)])) for w in pairs)
    host_leaves = adj["b:0:1"]-{"s:0"}
    assert host_leaves == {"l:0:1:0","l:0:1:1"}
    assert all(adj[v] == {"b:0:1"} for v in host_leaves)
    # If x>2, the two required host leaves with 0 and 1 block the alternatives
    # at weights 11 and 10 using those low labels with another high endpoint.
    assert pairs[12] == {(12,0)}
    assert pairs[11]-{(11,0)} == {(12,1)}
    assert pairs[10]-{(11,1),(10,0)} == {(12,2)}
    assert len(host_leaves) == 2 and adj["b:0:1"] == host_leaves | {"s:0"}
    sums = {(y,a):2*a+y//2-16 for y in (8,10) for a in set(range(8,12))-{y}}
    assert sums == {(8,9):6,(8,10):8,(8,11):10,(10,8):5,(10,9):7,(10,11):11}
    exact = {(x,y,a,t-x) for (y,a),t in sums.items()
             for x in range(max(0,t-7),min(2,t)+1) if x != t-x}
    observed = [(r["x"],r["Y"],r["A"],r["z"]) for r in rows]
    assert observed == sorted(exact) and len(exact) == 11 and all(r["B"] == 12 for r in rows)
    return pairs


def supported_pairs(pairs, locations, adjacency):
    return sorted((h,l) for h,l in pairs if any(adjacency[v] & locations[l] for v in locations[h]))


def force_palettes(row, pairs, adj, leaves):
    x,y,a,z = (row[k] for k in ("x","Y","A","z"))
    right = sorted(set(range(8,13))-{y,a,12})
    unplaced_low = set(range(8))-{x,z}
    assert row["right_terminal_palette"] == right and len(right) == len(leaves["b:1:0"]) == 2
    locations = {x:{"s:0"},y:{"s:1"},a:{"b:0:0"},12:{"b:0:1"},z:{"b:1:0"}}
    locations.update({v:leaves["b:1:0"] for v in right})
    locations.update({v:leaves["b:0:0"]|leaves["b:0:1"] for v in unplaced_low})
    if x == 0 and y == 8:
        weights = ()
    elif x == 0:
        weights = (11,9 if a == 8 else 8)
    else:
        weights = (12,10 if x == 1 else 11)
    trace, second = {}, set()
    for w in weights:
        supported = supported_pairs(pairs[w],locations,adj)
        assert len(supported) == 1
        high,low = supported[0]
        assert high == 12 and low in unplaced_low-second
        locations[low] = leaves["b:0:1"]
        trace[str(w)] = [high,low]
        second.add(low)
    first = unplaced_low-second if second else set()
    assert not second or (len(second),len(first)) == (2,4)
    assert row["second_terminal_palette"] == sorted(second)
    assert row["first_terminal_palette"] == sorted(first)
    return right, first, second, locations, trace


def verify_cases(rows, adjacency, pairs):
    centers = ("b:0:0","b:0:1","b:1:0")
    leaves = {v:adjacency[v]-{"s:0","s:1"} for v in centers}
    assert [len(leaves[v]) for v in centers] == [4,2,2]
    assert all(adjacency[u] == {v} for v in centers for u in leaves[v])
    fixed_edges = (("s:0","s:1"),("s:0","b:0:0"),("s:0","b:0:1"),("s:1","b:1:0"))
    verified = []
    for row in rows:
        right, first, second, locations, trace = force_palettes(row,pairs,adjacency,leaves)
        fixed_labels = {next(iter(sites)):label for label,sites in locations.items() if len(sites)==1}
        weights, incidences = {}, {}
        for u,v in fixed_edges:
            assert v in adjacency[u]
            key = f"{u}--{v}"
            weights[key] = abs(fixed_labels[u]-fixed_labels[v])
            incidences[key] = {frozenset((u,v))}
        assert all(u in adjacency["b:1:0"] for u in leaves["b:1:0"])
        for value in right:
            key = f"b:1:0 to label {value}"
            weights[key] = value-fixed_labels["b:1:0"]
            incidences[key] = {frozenset(("b:1:0",u)) for u in leaves["b:1:0"]}
        assert weights == row["fixed_incidence_weights"]
        for c,palette in zip(centers[:2],(first,second),strict=True):
            for value in palette:
                key = f"{c} to label {value}"
                weights[key] = fixed_labels[c]-value
                incidences[key] = {frozenset((c,u)) for u in leaves[c]}
        counts = Counter(weights.values())
        assert row["all_forced_incidence_weights"] == weights
        assert row["repeat_multiplicities"] == {str(w):n for w,n in sorted(counts.items()) if n>1}
        ob = row["obstruction"]
        weight = ob["weight"]
        witnesses = []
        if ob["kind"] == "duplicate":
            a,b = ob["witnesses"]
            assert counts[weight] >= 2
            assert weights[a] == weights[b] == weight and incidences[a].isdisjoint(incidences[b])
            witnesses = [{"incidence":key,"eligible_edges":[sorted(edge) for edge in sorted(incidences[key], key=sorted)],
                          "weight":weight} for key in (a,b)]
        else:
            assert ob["kind"] == "missing" and not ob["witnesses"]
            assert weight not in counts
            if not second:
                remaining = set(range(8))-{row["x"],row["z"]}
                assert weight < min(row["A"],12)-max(remaining)
            else:
                assert len(first)+len(second)+len(right)+len(fixed_edges)==12
        verified.append({"scalars":[row[k] for k in ("x","Y","A","z")], "forcing_trace":trace,
                         "repeat_multiplicities":row["repeat_multiplicities"], "duplicate_witnesses":witnesses,
                         "obstruction":ob})
    return verified


def verify_controls(original, certificate, positive, adverse):
    graph, labels = original["graph"], certificate["labels"]
    assert set(labels) == set(graph["vertices"]) and sorted(labels.values()) == list(range(13))
    differences = [abs(labels[u]-labels[v]) for u,v in graph["edges"]]
    assert sorted(differences) == list(range(1,13))
    assert all((labels[u] < 8) != (labels[v] < 8) for u,v in graph["edges"])
    assert positive["graph_digest"] == original["graph_digest"] and positive["checker"]["valid"]
    assert positive["checker"]["edge_differences"] == differences
    ledger = {"graph_digest":original["graph_digest"],"labels":sorted(labels.items())}
    digest = sha256(json.dumps(ledger,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert digest == positive["ledger_id"] == certificate["ledger_id"]
    wrong = adverse["bad_digest"]
    assert wrong["claimed"] == "0"*64 and not wrong["checker"]["valid"]
    assert wrong["checker"]["errors"] == ["original graph digest mismatch"]
    assert adverse["false_maximum_host"] == {"claimed_vertex":"b:0:1","claimed_label":12,
        "actual_label":labels["b:0:1"],"valid":False,"error":"The physical host does not carry the declared maximum"}
    assert labels["b:0:1"] == 9 and max(labels.values()) == 12
    swap = adverse["terminal_swap"]
    u,v = swap["vertices"]
    assert (u,v) == ("l:0:0:0","l:0:1:0")
    swapped = labels | {u:labels[v],v:labels[u]}
    assert swapped == swap["labels"] and sorted(swapped.values()) == list(range(13))
    damaged = [abs(swapped[u]-swapped[v]) for u,v in graph["edges"]]
    assert not swap["checker"]["valid"] and swap["checker"]["edge_differences"] == damaged
    repeated = sorted(w for w,n in Counter(damaged).items() if n>1)
    missing = sorted(set(range(1,13))-set(damaged))
    assert repeated == [5,7] and missing == [4,8]
    return {"repeat_weights":repeated,"missing_weights":missing}


def check(original, certificate, reduction, rows, positive, adverse, history):
    adjacency,lows = inspect(original)
    pairs = check_reduction(adjacency,lows,reduction,rows)
    verified = verify_cases(rows,adjacency,pairs)
    controls = verify_controls(original,certificate,positive,adverse)
    assert history == {"D083_original":"INCOMPLETE","D083_versioned":"PASS",
                       "D093_original":"INCOMPLETE","D093_versioned":"PASS",
                       "D099":"PASS","D100_original":"INCOMPLETE","D100_recovery":"PASS"}
    return {"status":"PASS","verified_cases":verified,"swap_inventory":controls,"historical_statuses":history}
