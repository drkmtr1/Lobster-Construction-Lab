"""D174 independent count-first exterior audit, raw allocator and named positive check."""
from itertools import permutations, product


def original_context(row, prefix, retained):
    graph = row["graph"]
    parents, roles, digest = retained.original(graph)
    before = prefix["graph"]["profile"]
    T1,T2 = map(sum,row["suffix"])
    if (digest != row["digest"] or graph["profile"] != before+row["suffix"]
            or (T1,T2)!=(row["F"],row["R"]) or len(graph["edges"]) != prefix["n"]+2*row["K"]
            or 2*row["K"]!=T1+T2+10):
        raise ValueError("independent original binding")
    u,w = graph["spine"][-2:]
    v = graph["spine"][-3]
    left = tuple(name for name,role in roles.items() if parents.get(name)==u and role["kind"]=="branch")
    at_w = tuple(name for name,role in roles.items() if parents.get(name)==w and role["kind"]=="branch")
    groups = {center:tuple(sorted(name for name,parent in parents.items() if parent==center))
              for center in left+at_w}
    right = tuple(name for name in at_w if groups[name])
    direct, = tuple(name for name in at_w if not groups[name])
    del groups[direct]
    neutrals = tuple(name for name in left if len(groups[name])==4)
    if v!=prefix["frontier"] or len(left)!=5 or len(right)!=2 or direct!=f"b:{roles[w]['section']}:2":
        raise ValueError("independent physical case")
    fresh = {name:parent for name,parent in parents.items() if name not in prefix["actual_labels"]}
    return v,u,w,left,right,direct,neutrals,groups,fresh


def raw_moment(A, B, K, reduced, left, right, groups, h):
    s = 2*K-A-B
    low = sum(sum(leaf not in reduced for leaf in groups[host])*(A-1-reduced[host]) for host in left)
    high = sum(sum(leaf not in reduced for leaf in groups[host])*(s+reduced[host]-A+1) for host in right)
    return low+high+(1-h)*(A-1)


def count_first(row, context, arm, meter, counts):
    v,u,w,left,right,direct,neutrals,groups,fresh = context
    if arm not in ("H0","H1"):
        raise ValueError("unknown independent direct-leaf placement arm")
    second_choices = [range(len(groups[name])+1) for name in right]
    K = row["K"]
    for neutral in neutrals:
        meter.tick("exterior_nodes")
        first_choices = [range(1 if name==neutral else len(groups[name])+1) for name in left]
        for take in product(*second_choices,*first_choices,(int(arm=="H1"),)):
            meter.tick("exterior_nodes")
            lower_counts,upper_counts,h = take[:2],take[2:7],take[7]
            e2,e1 = sum(lower_counts),sum(upper_counts)
            if not e1 or not e2:
                continue
            A,B = 6+e2,3+e1+h
            if (A+B>K or B<4 or
                    2*A>6+row["R"] or 2*B>4+row["F"]):
                continue
            low_term = tuple(leaf for center,count in zip(right,lower_counts,strict=True)
                             for leaf in groups[center][:count])
            up_term = tuple(leaf for center,count in zip(left,upper_counts,strict=True)
                            for leaf in groups[center][:count])
            for pinned in right:
                meter.tick("exterior_nodes")
                residual = len(groups[pinned])-lower_counts[right.index(pinned)]
                if residual < (2 if B==4 else 1):
                    continue
                low_names = tuple(name for name in left if name!=neutral)+low_term
                high_names = tuple(name for name in right if name!=pinned)+up_term+((direct,) if h else ())
                # Count-first enumeration, with lower and upper orders in reverse label order.
                for high in permutations(high_names):
                    meter.tick("exterior_nodes")
                    upper = dict(zip(high,range(A+B,A+2,-1),strict=True))
                    if any([upper[name] for name in names if name in upper]!=
                           sorted(upper[name] for name in names if name in upper) for names in groups.values()):
                        continue
                    for low in permutations(low_names):
                        meter.tick("exterior_nodes")
                        lower = dict(zip(low,range(A-2,0,-1),strict=True))
                        if any([lower[name] for name in names if name in lower]!=
                               sorted(lower[name] for name in names if name in lower) for names in groups.values()):
                            continue
                        reduced = {v:A,u:A+1,w:0,neutral:A-1,pinned:A+2,**lower,**upper}
                        supplied = [(reduced[name],reduced[parent]) for name,parent in fresh.items() if name in reduced]
                        if (any((x>A)==(y>A) for x,y in supplied) or
                                sorted(abs(x-y) for x,y in supplied)!=list(range(1,A+B+1))):
                            continue
                        if raw_moment(A,B,K,reduced,left,right,groups,h)%2:
                            continue
                        counts["qualified_exteriors"] += 1
                        key = f"{A},{B},{e1},{e2},{h},{neutral},{pinned}"
                        strata = counts["qualified_strata"]
                        strata[key] = strata.get(key,0)+1
                        yield A,B,reduced


def expanded(row,prefix,context,A,B,reduced,arm):
    v,u,w,left,right,direct,_,groups,fresh = context
    K,n = row["K"],prefix["n"]
    s,m = 2*K-A-B,n+2*K
    c,C,d = prefix["c"],prefix["c"]+K,prefix["d"]
    mandatory = {v,u,w,*left,*right}
    vertices = set(reduced)
    if (any(type(x) is not int for x in (A,B)) or A<7 or B<4 or s<K or K<A or K>A+s or n<2*K
            or not mandatory<=vertices or not vertices<={v,*fresh}
            or (reduced[v],reduced[u],reduced[w])!=(A,A+1,0)
            or any(type(label) is not int for label in reduced.values())
            or sorted(reduced.values())!=list(range(A+B+1))):
        raise ValueError("independent reduced identity")
    picked = {name for names in groups.values() for name in names if name in vertices}
    if arm not in ("H0","H1") or (direct in vertices)!=(arm=="H1"):
        raise ValueError("independent direct-leaf placement identity")
    e1 = sum(fresh[name] in left for name in picked)
    e2 = len(picked)-e1
    if not e1 or not e2 or (A,B)!=(6+e2,3+e1+int(direct in vertices)):
        raise ValueError("independent terminal or width identity")
    if raw_moment(A,B,K,reduced,left,right,groups,int(direct in vertices))%2:
        raise ValueError("independent raw moment gate")
    edges = [(name,fresh[name]) for name in vertices-{v}]
    reduced_weights = sorted(abs(reduced[x]-reduced[y]) for x,y in edges)
    if (reduced_weights!=list(range(1,A+B+1))
            or any((reduced[x]<=A)==(reduced[y]<=A) for x,y in edges)):
        raise ValueError("independent exterior differences")
    ext = {name:value+(n+s if value>A else 0) for name,value in reduced.items()}
    gap = {host:tuple(sorted(name for name,parent in fresh.items() if parent==host and name not in vertices))
           for host in (*left,*right,w)}
    if (len(gap)!=8 or len(gap[w])!=int(arm=="H0") or sum(map(len,gap.values()))!=s
            or any(name in vertices for names in gap.values() for name in names)):
        raise ValueError("independent gap physical quotas")
    return s,m,C,d,ext,gap,edges,reduced_weights


def raw_support(row, prefix, context, A, B, reduced, arm, meter):
    s, _, C, d, ext, groups, _, _ = expanded(row, prefix, context, A, B, reduced, arm)
    capacity = {host: len(leaves) for host, leaves in groups.items()}
    images = set(range(s))
    sources = set(range(s))
    options = {}
    for source in sorted(sources):
        label = A+prefix["c"]+source
        moves = []
        for host, count in capacity.items():
            meter.tick("transitions")
            image = abs(ext[host]-label)-(d-1)
            cross = (ext[host]<C) != (label<C)
            if count and image in images and (image>=row["K"]) == cross:
                moves.append((host,image))
        options[source] = tuple(moves)
    stack = meter.frames

    def visit():
        stack.append({"remaining_sources": sorted(sources), "remaining_images": sorted(images),
                      "capacities": dict(capacity), "choice": None})
        meter.memory(len(stack))
        meter.tick("transfer_states")
        if not sources:
            stack.pop()
            return not images and not any(capacity.values())
        best = None
        reachable = set()
        possible = dict.fromkeys(capacity, 0)
        for source in sorted(sources):
            here = []
            for host, image in options[source]:
                meter.tick("transitions")
                if capacity[host] and image in images:
                    here.append((host,image))
                    reachable.add(image)
            if not here:
                stack.pop()
                return False
            for host in {h for h, _ in here}:
                possible[host] += 1
            if best is None or len(here)<len(best[1]):
                best = source, here
        if reachable != images or any(possible[h]<count for h,count in capacity.items()):
            stack.pop()
            return False
        source, moves = best
        sources.remove(source)
        for host, image in moves:
            stack[-1]["choice"] = [source,host,image]
            meter.tick("transitions")
            capacity[host] -= 1
            images.remove(image)
            if visit():
                stack.pop()
                return True
            images.add(image)
            capacity[host] += 1
        sources.add(source)
        stack.pop()
        return False

    return visit()


def negative(row,prefix,arm,meter,retained):
    context = original_context(row,prefix,retained)
    counts = {"qualified_exteriors":0,"qualified_strata":{}}
    meter.phase = "independent exterior"
    for A,B,reduced in count_first(row,context,arm,meter,counts):
        meter.candidate = {"A":A,"B":B,"reduced":reduced,"ordinal":counts["qualified_exteriors"]}
        meter.phase = "independent raw allocation"
        if raw_support(row,prefix,context,A,B,reduced,arm,meter):
            raise ValueError("independent allocation refuted the claimed negative")
        meter.phase = "independent exterior"
        meter.candidate = None
    return {"status":"PASS_INDEPENDENT_EXHAUSTION","counts":counts}


def positive(row,prefix,arm,solution,meter,retained,checker):
    meter.phase = "independent certificate reconstruction"
    context = original_context(row,prefix,retained)
    v,u,w,left,right,direct,_,groups,fresh = context
    A,B,reduced = (solution[field] for field in ("A","B","reduced"))
    s,m,C,d,ext,gap,exterior_edges,reduced_weights = expanded(row,prefix,context,A,B,reduced,arm)
    assignments = solution["assignment"]
    if len(assignments)!=s:
        raise ValueError("gap witness cardinality")
    oriented = {name:x+A+(s if x>=prefix["c"] else 0) for name,x in prefix["oriented_labels"].items()}
    if ext[v]!=oriented[v]:
        raise ValueError("old frontier assignment")
    oriented.update(ext)
    remaining = {host:list(names) for host,names in gap.items()}
    used = set()
    detail = []
    for i,(host,image) in enumerate(assignments):
        meter.tick("transitions")
        value = A+prefix["c"]+i
        if host not in remaining or not remaining[host]:
            raise ValueError("independent quota overuse")
        name = remaining[host].pop(0)
        weight = abs(ext[host]-value)
        crossing = (value<C)!=(ext[host]<C)
        if (type(image) is not int or not 0<=image<s or image in used or weight!=d-1+image
                or crossing!=(image>=row["K"]) or fresh[name]!=host):
            raise ValueError("independent gap witness image or incidence")
        oriented[name] = value
        used.add(image)
        detail.append({"source":i,"image":image,"leaf":name,"host":host,"label_oriented":value,
                       "weight":weight,"crossing":crossing})
    graph = row["graph"]
    if any(remaining.values()) or set(oriented)!=set(graph["vertices"]):
        raise ValueError("independent quota or full vertex coverage")
    actual = {name:m-value for name,value in oriented.items()}
    cut = m+1-C
    actual_frontier = actual[w]
    cert = checker(graph,actual,expected_graph_digest=row["digest"])
    if (not cert["valid"] or actual_frontier!=m
            or any(actual[name]!=x+B+(s if x>=prefix["actual_cut"] else 0)
                   or (actual[name]<cut)!=(x<prefix["actual_cut"])
                   for name,x in prefix["actual_labels"].items())):
        raise ValueError("unchanged checker or actual old placement")
    classified = [(x,y,abs(actual[x]-actual[y]),(actual[x]<cut)!=(actual[y]<cut))
                  for x,y in graph["edges"]]
    crossing = sorted(weight for _,_,weight,crosses in classified if crosses)
    noncrossing = sorted(weight for _,_,weight,crosses in classified if not crosses)
    threshold = d+row["K"]-1
    if crossing!=list(range(threshold,m+1)) or noncrossing!=list(range(1,threshold)):
        raise ValueError("independent exact phase return")
    section = len(prefix["graph"]["spine"])
    partial = {name:label for name,label in actual.items() if graph["roles"][name]["section"]<=section}
    used_edges = [edge for edge in classified if edge[0] in partial and edge[1] in partial]
    pending = [edge for edge in classified if edge not in used_edges]
    inter = [edge for edge in pending if (edge[0] in partial)!=(edge[1] in partial)]
    if len(inter)!=1 or set(inter[0][:2])!={u,w}:
        raise ValueError("independent unfinished connector")
    resources = {"used_labels":sorted(partial.values()),"remaining_labels":sorted(set(range(m+1))-set(partial.values())),
                 "used_weights":sorted(edge[2] for edge in used_edges),"remaining_weights":sorted(edge[2] for edge in pending),
                 "used_crossing":sorted(edge[2] for edge in used_edges if edge[3]),
                 "remaining_crossing":sorted(edge[2] for edge in pending if edge[3]),
                 "used_noncrossing":sorted(edge[2] for edge in used_edges if not edge[3]),
                 "remaining_noncrossing":sorted(edge[2] for edge in pending if not edge[3])}
    terminal_roles = [{"terminal":name,"parent":fresh[name],"reduced":reduced[name],
                       "parent_reduced":reduced[fresh[name]]}
                      for names in groups.values() for name in names if name in reduced]
    selected_first = sum(terminal["parent"] in left for terminal in terminal_roles)
    neutral, = [name for name in left if reduced[name]==A-1]
    upper_two, = [name for name in right if reduced[name]==A+2]
    if (len(gap[neutral])!=4 or not (row["K"]<=s and 0<=A<=row["K"]<=A+s)
            or any(detail[i]["host"]!=neutral for i in range(4))
            or detail[-1]["host"]!=upper_two or detail[-1]["image"]!=4
            or B==4 and detail[row["K"]-A]["host"]!=upper_two):
        raise ValueError("independent physical endpoint reservations")
    report = {"status":"PASS_INDEPENDENT_RECONSTRUCTION","certificate":cert,"actual_labels":actual,
            "exterior_structure":{"A":A,"B":B,"s":s,"e1":selected_first,"e2":len(terminal_roles)-selected_first,
                                  "h":int(direct in reduced),"neutral":neutral,"upper_index_two":upper_two,
                                  "upper_index_two_gap_quota":len(gap[upper_two]),"terminals":terminal_roles,
                                  "displacements":{host:{"kind":"translation","offset":A-1-reduced[host]}
                                                   if reduced[host]<A else
                                                   {"kind":"reflection","intercept":s+reduced[host]-A+1}
                                                   for host in gap}},
            "original":graph,"graph_digest":row["digest"],"reduced":reduced,"reduced_weights":reduced_weights,
            "expanded_exterior_actual":{name:m-label for name,label in ext.items()},
            "exterior_edges":exterior_edges,"gap":detail,"gap_quotas":{host:len(names) for host,names in gap.items()},
            "crossing_counts":{"lower_source_upper_host":sum(x["crossing"] and x["source"]<row["K"]-A for x in detail),
                               "upper_source_lower_host":sum(x["crossing"] and x["source"]>=row["K"]-A for x in detail)},
            "resources":resources,"connector":{"ends":[u,w],"labels":[actual[u],actual[w]],"weight":inter[0][2],
                                               "crossing":inter[0][3]},
            "cut":cut,"polarity":"maximum","crossing":crossing,"noncrossing":noncrossing}

    report["exterior_structure"]["upper_host_separation"] = abs(reduced[right[0]]-reduced[right[1]])
    report["exterior_structure"]["direct_leaf"] = direct
    report["exterior_structure"]["arm"] = arm
    report["label_side_partitions"] = {
        name: {"lower":[z for z in resources[name+"_labels"] if z<cut],
               "upper":[z for z in resources[name+"_labels"] if z>=cut]}
        for name in ("used","remaining")}
    report["return_phase"] = {"phase":"S_-1","frontier":w,"label":actual_frontier,"cut":cut}
    report["polarity_transport"] = {"oriented_cut":C,"oriented_frontier":0,"oriented_old_shifts":[A,A+s],
                                    "maximum_old_shifts":[B,B+s]}
    return report
