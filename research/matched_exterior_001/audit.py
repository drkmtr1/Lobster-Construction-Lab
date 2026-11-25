"""Independent original, positive reconstruction, and negative audit.

This module never imports the candidate generator or the folded transfer.
"""

from hashlib import sha256
from itertools import combinations, permutations
import json


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def original(graph):
    profile = graph["profile"]
    s = tuple("s:" + str(i) for i in range(len(profile)))
    parents = {s[i]: s[i-1] for i in range(1, len(s))}
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(s)}
    for i, section in enumerate(profile):
        for j, quota in enumerate(section):
            branch = "b:" + str(i) + ":" + str(j)
            parents[branch] = s[i]
            roles[branch] = {"section": i, "branch": j, "kind": "branch"}
            for l in range(quota):
                leaf = "l:" + branch[2:] + ":" + str(l)
                parents[leaf] = branch
                roles[leaf] = {"section": i, "branch": j, "leaf": l, "kind": "leaf"}
    edges = sorted(sorted((child, parent)) for child, parent in parents.items())
    payload = {"vertices": sorted(roles), "edges": edges, "profile": profile,
               "spine": list(s), "roles": roles}
    if (len(graph["vertices"]) != len(roles) or sorted(graph["vertices"]) != payload["vertices"]
            or sorted(sorted(edge) for edge in graph["edges"]) != edges or list(s) != graph["spine"]
            or roles != graph["roles"]):
        raise ValueError("independent named identity mismatch")
    return parents, roles, sha256(canonical(payload)).hexdigest()


def shape(target, prefix):
    graph = target["graph"]
    parents, roles, digest = original(graph)
    if digest != target["digest"] or graph["profile"] != prefix["graph"]["profile"] + target["suffix"]:
        raise ValueError("frozen target/profile/digest changed")
    v = prefix["frontier"]
    u, w = graph["spine"][-2:]
    new = set(roles) - set(prefix["actual_labels"])
    if len(new) != target["fresh"] or parents[u] != v or parents[w] != u or target["fresh"] % 2:
        raise ValueError("independent original interface")
    compulsory = {v,u,w}
    sides = {v:0,u:1,w:0}
    for name in new - {u,w}:
        role = roles[name]
        in_first = role["section"] == roles[u]["section"]
        side = int(not in_first)
        if role["kind"] == "leaf":
            side = 1-side
        elif graph["profile"][role["section"]][role["branch"]] > 0:
            compulsory.add(name)
        sides[name] = side
    return parents, roles, compulsory, tuple(sorted(new - compulsory)), sides, v, u, w


def positive(target, prefix, arm, witness, unchanged_checker):
    graph = target["graph"]
    parents, roles, compulsory, optional, sides, v, u, w = shape(target, prefix)
    labels = witness["labels"]
    checked = unchanged_checker(graph, labels, expected_graph_digest=target["digest"])
    if not checked["valid"]:
        raise ValueError("original-target checker refused certificate")
    n, c, d = prefix["n"], prefix["c"], prefix["d"]
    K = target["fresh"]//2
    m = n+2*K
    final = {name:m-label for name,label in labels.items()}
    reduced = witness["reduced"]
    all_exterior = set(reduced)
    gap = set(optional) - all_exterior
    if not compulsory <= all_exterior <= compulsory.union(optional):
        raise ValueError("exterior subset")
    if arm == "T" and any(roles[name]["kind"] == "leaf" for name in all_exterior):
        raise ValueError("Arm T used an exterior terminal")
    A, B, s = (witness[name] for name in ("A","B","s"))
    if s != len(gap) or A+B+s != 2*K or min(A,B) < 2 or s < K:
        raise ValueError("exterior widths")
    if [reduced[name] for name in (v,u,w)] != [A,A+1,0]:
        raise ValueError("physical exterior pins")
    for side, expected in ((0, range(A+1)), (1, range(A+1,A+B+1))):
        if sorted(reduced[name] for name in reduced if sides[name] == side) != list(expected):
            raise ValueError("exact exterior side alphabet")
    weights = [abs(reduced[name]-reduced[parents[name]]) for name in reduced if name != v]
    if sorted(weights) != list(range(1,A+B+1)):
        raise ValueError("exact exterior spectrum")
    for name, value in reduced.items():
        if final[name] != (value if value <= A else n+s+value):
            raise ValueError("incorrect expanded exterior")
    for name, value in prefix["oriented_labels"].items():
        if final[name] != value+A+(s if value >= c else 0):
            raise ValueError("incorrect old embedding")
    gap_rows = []
    by_host = {}
    for leaf in gap:
        host = parents[leaf]
        if host == v or host not in reduced:
            raise ValueError("gap host absent")
        image = abs(final[leaf]-final[host])-d
        index = final[leaf] - (A+c)
        crossing = (final[leaf]<c+K) != (final[host]<c+K)
        if crossing != (image >= K):
            raise ValueError("gap crossing disagreement")
        gap_rows.append([leaf,host,index,image])
        ordinal = roles[leaf].get("leaf", roles[leaf]["branch"])
        by_host.setdefault(host, []).append((ordinal,index))
    for position in (2,3):
        if sorted(item[position] for item in gap_rows) != list(range(s)):
            raise ValueError("gap inventory")
    if sorted(gap_rows, key=lambda item:item[2]) != witness["gap"]:
        raise ValueError("labelled gap witness discrepancy")
    if any([second for _,second in sorted(rows)] != sorted(second for _,second in rows)
           for rows in by_host.values()):
        raise ValueError("physical branch/terminal ordering")
    actual_cut = m+1-(c+K)
    crossings = sorted(abs(labels[a]-labels[b]) for a,b in graph["edges"]
                       if (labels[a]<actual_cut) != (labels[b]<actual_cut))
    if labels[w] != m or crossings != list(range(d+K,m+1)):
        raise ValueError("exact physical D134 return")
    first = {name for name in roles if roles[name]["section"] <= roles[u]["section"]}
    boundary_edges = [(a,b) for a,b in graph["edges"] if a in first and b in first]
    pending = [sorted((a,b)) for a,b in graph["edges"] if (a in first) != (b in first)]
    if pending != [sorted((u,w))]:
        raise ValueError("actual unfinished spine connector")
    used_labels = sorted(labels[name] for name in first)
    used_weights = sorted(abs(labels[a]-labels[b]) for a,b in boundary_edges)
    crossing_weights = sorted(abs(labels[a]-labels[b]) for a,b in boundary_edges
                              if (labels[a]<actual_cut) != (labels[b]<actual_cut))
    return {"audit":"independent-positive", "original_check":"PASS", "cut":actual_cut,
            "crossing_weights":crossings, "first_boundary":{
                "used_labels":used_labels,"remaining_labels":sorted(set(range(m+1))-set(used_labels)),
                "used_weights":used_weights,"remaining_weights":sorted(set(range(1,m+1))-set(used_weights)),
                "crossing_weights":crossing_weights,"frontier":u,"frontier_label":labels[u],
                "unfinished_edge":pending[0],"unfinished_weight":abs(labels[u]-labels[w])}}


def raw_support(A, B, s, quotas, meter):
    """Independent ascending source recursion with full destination bitset."""
    K = (A+B+s)//2
    upper = lambda h: h >= A
    possibilities = []
    for source in range(s):
        arcs = []
        for h in range(A+B):
            if quotas[h] == 0:
                continue
            image = s+(h-A+1)-source if upper(h) else source+A-2-h
            if 0 <= image < s and ((image >= K) == ((source < K-A) == upper(h))):
                arcs.append((h, 1 << image))
        possibilities.append(arcs)
    dead = set()

    def find(i, used, remaining):
        key = (i, used, remaining)
        if key in dead:
            return False
        meter.tick("transfer_states")
        meter.memory(len(dead)+i+1)
        if i == s:
            return not any(remaining) and used == (1<<s)-1
        for host, bit in possibilities[i]:
            meter.tick("transitions")
            if used & bit or not remaining[host]:
                continue
            revised = list(remaining)
            revised[host] -= 1
            if find(i+1, used|bit, tuple(revised)):
                return True
        dead.add(key)
        return False

    return find(0, 0, tuple(quotas))


def negative(target, prefix, arm, meter):
    parents, roles, core, optional, sides, v, u, w = shape(target, prefix)
    left, right = target["suffix"]
    dl = len(left)-1
    dr = right.count(0)
    right_centers = len(right)-dr
    if dl == 0 and right_centers == 1 and dr == 0:
        return {"audit":"D147-first-upper-source", "independent_candidates":0}
    maximum_direct = {1:3, 2:2}[right_centers]
    if arm == "T" and dl == 0 and dr <= maximum_direct:
        return {"audit":"terminal-free-forced-three", "independent_candidates":0}
    permitted = [leaf for leaf in optional if arm == "E" or roles[leaf]["kind"] == "branch"]
    K = target["fresh"]//2
    tested = 0
    for size in range(min(len(permitted), K-len(core)+1)+1):
        for chosen in combinations(permitted, size):
            meter.tick("exterior_nodes")
            exterior = core.union(chosen)
            low = sorted(name for name in exterior if sides[name] == 0 and name not in (v,w))
            high = sorted(name for name in exterior if sides[name] == 1 and name != u)
            A, B = 1+len(low), 1+len(high)
            if A < 2 or B < 2 or A+B > K:
                continue
            s = 2*K-A-B
            for low_values in permutations(range(1,A)):
                meter.tick("exterior_nodes")
                for high_values in permutations(range(A+2,A+B+1)):
                    meter.tick("exterior_nodes")
                    labels = dict(zip(low+high, low_values+high_values))
                    labels.update({v:A, u:A+1, w:0})
                    if sorted(abs(labels[name]-labels[parents[name]]) for name in exterior-{v}) != list(range(1,A+B+1)):
                        continue
                    tested += 1
                    counts = [0]*(A+B)
                    for name in set(optional)-exterior:
                        label = labels[parents[name]]
                        index = label if label < A else label-1
                        counts[index] += 1
                    if raw_support(A,B,s,counts,meter):
                        raise ValueError("independent audit found a candidate for a declared negative")
    return {"audit":"independent-exhaustion", "independent_candidates":tested}

def verify_prefix(prefix, unchanged_checker):
    graph = prefix["graph"]
    _, _, identity = original(graph)
    n = len(graph["edges"])
    frontier = graph["spine"][-1]
    actual = prefix["actual_labels"]
    if (identity != prefix["digest"] or n != prefix["n"] or n < 20
            or prefix["frontier"] != frontier or actual[frontier] != n
            or prefix["polarity"] != "maximum"):
        raise ValueError("frozen prefix identity/interface")
    if not unchanged_checker(graph, actual, expected_graph_digest=identity)["valid"]:
        raise ValueError("frozen prefix checker")
    directed = {name:n-label for name,label in actual.items()}
    c = n//2-1
    d = c+2
    crossing = sorted(abs(directed[x]-directed[y]) for x,y in graph["edges"]
                      if (directed[x]<c) != (directed[y]<c))
    if (n != 2*c+2 or (c,d) != (prefix["c"],prefix["d"])
            or prefix["actual_cut"] != n+1-c or directed != prefix["oriented_labels"]
            or crossing != list(range(d,n+1))):
        raise ValueError("frozen prefix exact cut")
