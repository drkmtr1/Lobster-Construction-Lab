"""Independent count-first exterior audit and raw expanded-endpoint allocator."""
from itertools import permutations, product


def original_context(row, prefix, retained):
    graph = row["graph"]
    parents, roles, digest = retained.original(graph)
    before = prefix["graph"]["profile"]
    T1,T2 = map(sum,row["suffix"])
    if (digest != row["digest"] or graph["profile"] != before+row["suffix"]
            or (T1,T2)!=(row["T1"],row["T2"]) or len(graph["edges"]) != prefix["n"]+2*row["K"]
            or 2*row["K"]!=T1+T2+8):
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
    neutral, = tuple(name for name in left if len(groups[name])==4)
    if v!=prefix["frontier"] or len(left)!=3 or len(right)!=2:
        raise ValueError("independent physical case")
    fresh = {name:parent for name,parent in parents.items() if name not in prefix["actual_labels"]}
    return v,u,w,left,right,direct,neutral,groups,fresh


def count_first(row, context, arm, meter, counts):
    v,u,w,left,right,direct,neutral,groups,fresh = context
    first_choices = [range(1 if name==neutral else len(groups[name])+1) for name in left]
    second_choices = [range(len(groups[name])+1) for name in right]
    K = row["K"]
    for take in product(*second_choices,*first_choices,range(2)):
        meter.tick("exterior_nodes")
        lower_counts,upper_counts,h = take[:2],take[2:5],take[5]
        e2,e1 = sum(lower_counts),sum(upper_counts)
        if (arm=="T")!=(e1+e2==0):
            continue
        A,B = 4+e2,3+e1+h
        if (A+B>K or B<4 or bool(e1)!=bool(e2) or
                2*A>4+row["T2"] or 2*B>4+row["T1"]):
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
                    counts["qualified_exteriors"] += 1
                    yield A,B,reduced


def expanded(row,prefix,context,A,B,reduced,arm):
    v,u,w,left,right,direct,neutral,groups,fresh = context
    K,n = row["K"],prefix["n"]
    s,m = 2*K-A-B,n+2*K
    c,C,d = prefix["c"],prefix["c"]+K,prefix["d"]
    mandatory = {v,u,w,*left,*right}
    vertices = set(reduced)
    if (any(type(x) is not int for x in (A,B)) or A<4 or B<3 or s<K
            or not mandatory<=vertices or not vertices<={v,*fresh}
            or (reduced[v],reduced[u],reduced[w])!=(A,A+1,0)
            or any(type(label) is not int for label in reduced.values())
            or sorted(reduced.values())!=list(range(A+B+1))):
        raise ValueError("independent reduced identity")
    picked = {name for names in groups.values() for name in names if name in vertices}
    if (arm=="T")!= (not picked):
        raise ValueError("independent disjoint arm identity")
    e1 = sum(fresh[name] in left for name in picked)
    e2 = len(picked)-e1
    if (A,B)!=(4+e2,3+e1+int(direct in vertices)):
        raise ValueError("independent physical width identity")
    edges = [(name,fresh[name]) for name in vertices-{v}]
    reduced_weights = sorted(abs(reduced[x]-reduced[y]) for x,y in edges)
    if (reduced_weights!=list(range(1,A+B+1))
            or any((reduced[x]<=A)==(reduced[y]<=A) for x,y in edges)):
        raise ValueError("independent exterior differences")
    ext = {name:value+(n+s if value>A else 0) for name,value in reduced.items()}
    gap = {host:tuple(sorted(name for name,parent in fresh.items() if parent==host and name not in vertices))
           for host in (*left,*right,w)}
    if (sum(map(len,gap.values()))!=s or any(name in vertices for names in gap.values() for name in names)):
        raise ValueError("independent gap physical quotas")
    return s,m,C,d,ext,gap,edges,reduced_weights


def raw_allocation(row,prefix,context,A,B,reduced,arm,meter):
    s,_,C,d,ext,gap,_,_ = expanded(row,prefix,context,A,B,reduced,arm)
    remaining = {host:len(names) for host,names in gap.items()}
    legal = {}
    for i in range(s):
        label = A+prefix["c"]+i
        moves = []
        for host,quota in remaining.items():
            meter.tick("transitions")
            image = abs(ext[host]-label)-(d-1)
            crossing = (label<C)!=(ext[host]<C)
            if quota and 0<=image<s and (image>=row["K"])==crossing:
                moves.append((host,image))
        legal[i] = tuple(moves)
    pending,unused = set(range(s)),set(range(s))

    def descend():
        meter.memory(s-len(pending)+1)
        meter.tick("transfer_states")
        if not pending:
            return not unused and not any(remaining.values())
        selected,best = None,None
        reachable = set()
        capacity = dict.fromkeys(remaining,0)
        for i in sorted(pending):
            options = []
            seen_hosts = set()
            for host,image in legal[i]:
                meter.tick("transitions")
                if remaining[host] and image in unused:
                    options.append((host,image))
                    seen_hosts.add(host)
                    reachable.add(image)
            if not options:
                return False
            for host in seen_hosts:
                capacity[host] += 1
            if best is None or len(options)<len(best):
                selected,best = i,options
        if reachable!=unused or any(capacity[h]<q for h,q in remaining.items()):
            return False
        pending.remove(selected)
        for host,image in best:
            meter.tick("transitions")
            remaining[host] -= 1
            unused.remove(image)
            if descend():
                return True
            unused.add(image)
            remaining[host] += 1
        pending.add(selected)
        return False

    return descend()


def negative(row,prefix,arm,meter,retained):
    context = original_context(row,prefix,retained)
    counts = {"qualified_exteriors":0}
    for A,B,reduced in count_first(row,context,arm,meter,counts):
        if raw_allocation(row,prefix,context,A,B,reduced,arm,meter):
            raise ValueError("independent audit refuted claimed negative")
    return {"status":"PASS_INDEPENDENT_EXHAUSTION","counts":counts,
            "basis":"ALLOCATION_EXHAUSTED" if counts["qualified_exteriors"] else "NECESSARY_GAP_EXCLUSIONS"}


def positive(row,prefix,arm,solution,meter,retained,checker):
    context = original_context(row,prefix,retained)
    v,u,w,left,right,_,_,_,fresh = context
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
    return {"status":"PASS_INDEPENDENT_RECONSTRUCTION","certificate":cert,"actual_labels":actual,
            "original":graph,"graph_digest":row["digest"],"reduced":reduced,"reduced_weights":reduced_weights,
            "expanded_exterior_actual":{name:m-label for name,label in ext.items()},
            "exterior_edges":exterior_edges,"gap":detail,"gap_quotas":{host:len(names) for host,names in gap.items()},
            "crossing_counts":{"lower_source_upper_host":sum(x["crossing"] and x["source"]<row["K"]-A for x in detail),
                               "upper_source_lower_host":sum(x["crossing"] and x["source"]>=row["K"]-A for x in detail)},
            "resources":resources,"connector":{"ends":[u,w],"labels":[actual[u],actual[w]],"weight":inter[0][2],
                                               "crossing":inter[0][3]},
            "cut":cut,"polarity":"maximum","crossing":crossing,"noncrossing":noncrossing}
