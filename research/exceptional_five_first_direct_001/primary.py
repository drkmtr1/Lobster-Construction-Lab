"""D174 slot-first qualified exterior enumeration and folded-consumer adapter."""
from itertools import product


def physical(row, prefix):
    section = len(prefix["graph"]["spine"])
    v,u,w = prefix["frontier"],f"s:{section}",f"s:{section+1}"
    left = tuple(f"b:{section}:{j}" for j in range(5))
    right = tuple(f"b:{section+1}:{j}" for j in range(2))
    direct = f"b:{section+1}:2"
    parents = {u:v,w:u,direct:w}
    groups = {}
    for ids, quotas, spine in ((left,row["suffix"][0],u),(right,row["suffix"][1][:2],w)):
        for name, count in zip(ids,quotas,strict=True):
            parents[name] = spine
            groups[name] = tuple(f"l:{name[2:]}:{j}" for j in range(count))
            parents.update({leaf:name for leaf in groups[name]})
    neutrals = tuple(name for name in left if len(groups[name]) == 4)
    return v,u,w,left,right,direct,parents,groups,neutrals


def candidates(row, arm, meter, counts, case):
    v,u,w,left,right,direct,parents,groups,neutrals = case
    K,T1,T2 = row["K"],row["F"],row["R"]
    if arm not in ("H0","H1"):
        raise ValueError("unknown direct-leaf placement arm")
    for e1 in range(1,T1+1):
        for e2 in range(1,T2+1):
            for h in (int(arm=="H1"),):
                meter.tick("exterior_nodes")
                A,B = 6+e2,3+e1+h
                if A+B>K:
                    continue
                counts["entered_widths"] += 1
                if B<4 or 2*e2>T2-6 or 2*(e1+h)>T1-2:
                    counts["rejected_widths"] += 1
                    continue
                for neutral,pinned in product(neutrals,right):
                    meter.tick("exterior_nodes")
                    reduced = {v:A,u:A+1,w:0,neutral:A-1,pinned:A+2}
                    low = tuple(range(1,A-1))
                    high = tuple(range(A+3,A+B+1))
                    slots = low+high
                    used_weights = {1,2,A+1,A+2}
                    mandatory_low = set(left)-{neutral}
                    mandatory_high = (set(right)-{pinned})|({direct} if h else set())
                    limits = {host:len(names) for host,names in groups.items()}
                    limits[neutral] = 0
                    limits[pinned] -= 2 if B==4 else 1
                    if limits[pinned] < 0:
                        continue
                    selected = dict.fromkeys(groups,0)

                    def visit(depth):
                        if depth == len(slots):
                            if used_weights != set(range(1,A+B+1)):
                                raise AssertionError("completed reduced spectrum invariant")
                            moment = sum(len(groups[host])*reduced[host] for host in left)
                            moment += sum(len(groups[host])*(reduced[host]-A) for host in right)
                            if (moment-A-B)%2:
                                return
                            counts["qualified_exteriors"] += 1
                            key = f"{A},{B},{e1},{e2},{h},{neutral},{pinned}"
                            strata = counts["qualified_strata"]
                            strata[key] = strata.get(key,0)+1
                            yield A,B,dict(reduced)
                            return
                        label = slots[depth]
                        lower = label<A
                        must = mandatory_low if lower else mandatory_high
                        stop = len(low) if lower else len(slots)
                        groups_on_side = right if lower else left
                        names = [(name,None) for name in sorted(must)]
                        if stop-depth>len(must):
                            names += [(groups[host][selected[host]],host) for host in groups_on_side
                                      if selected[host]<limits[host]]
                        for name,host in names:
                            meter.tick("exterior_nodes")
                            weight = set()
                            # All new incidences with assigned neighbors are exact here.
                            pairs = [(name,parents[name])]
                            pairs.extend((child,name) for child,parent in parents.items() if parent==name)
                            for child,parent in pairs:
                                other = parent if name==child else child
                                if other not in reduced:
                                    continue
                                value = abs(label-reduced[other])
                                if ((label>A)==(reduced[other]>A) or value in used_weights or value in weight):
                                    break
                                weight.add(value)
                            else:
                                reduced[name] = label
                                used_weights.update(weight)
                                if host is None:
                                    must.remove(name)
                                else:
                                    selected[host] += 1
                                yield from visit(depth+1)
                                if host is None:
                                    must.add(name)
                                else:
                                    selected[host] -= 1
                                used_weights.difference_update(weight)
                                del reduced[name]

                    yield from visit(0)



def solve(row, prefix, arm, meter, folded):
    case = physical(row,prefix)
    counts = {"entered_widths":0,"rejected_widths":0,"qualified_exteriors":0,"qualified_strata":{}}
    meter.phase = "primary exterior"
    for A,B,reduced in candidates(row,arm,meter,counts,case):
        meter.candidate = {"A":A,"B":B,"reduced":reduced,"ordinal":counts["qualified_exteriors"]}
        meter.phase = "folded allocation"
        allocation = folded.folded_support(row,case,A,B,reduced,meter)
        if allocation is not None:
            return {"claim":"YES","counts":counts,
                    "solution":{"A":A,"B":B,"reduced":reduced,"assignment":allocation}}
        meter.phase = "primary exterior"
        meter.candidate = None
    return {"claim":"NO","counts":counts}
