
"""Independent arm classification, raw exhaustion and original-target reconstruction."""
from itertools import permutations


def classification(context, A, B, reduced):
    v, u, w, left, right, direct, _, groups, parents = context
    selected = {leaf for children in groups.values() for leaf in children if leaf in reduced}
    if not selected:
        raise ValueError("terminal-free exterior in the E+ partition")
    first = {leaf for leaf in selected if parents[leaf] in left}
    second = selected-first
    if ((A, B) == (6,4) and direct not in reduced
            and (reduced[v], reduced[u], reduced[w]) == (6,7,0)
            and sorted(reduced[h] for h in left) == [2,3,4,5]
            and sorted(reduced[h] for h in right) == [8,10]
            and sorted((reduced[leaf], reduced[parents[leaf]]) for leaf in first) == [(9,3)]
            and sorted((reduced[leaf], reduced[parents[leaf]]) for leaf in second) == [(1,10)]):
        return "M"
    return "A"


def menu_candidates(context, meter):
    v, u, w, left, right, _, neutrals, groups, _ = context
    for neutral in neutrals:
        meter.tick("exterior_nodes")
        for c1 in reversed(left):
            meter.tick("exterior_nodes")
            if c1 == neutral:
                continue
            available = [h for h in left if h not in (c1, neutral)]
            for a, b in permutations(available):
                meter.tick("exterior_nodes")
                D = 3*len(groups[b])+2*(len(groups[a])-1)+len(groups[c1])+5
                if D % 2:
                    continue
                for p in reversed(right):
                    meter.tick("exterior_nodes")
                    q, = [h for h in right if h != p]
                    if len(groups[q]) < 2:
                        continue
                    yield 6, 4, {w:0, groups[p][0]:1, b:2, a:3, c1:4, neutral:5,
                                  v:6, u:7, q:8, groups[a][0]:9, p:10}


def raw_support(row, prefix, context, A, B, reduced, meter, retained):
    s, _, C, d, expanded, groups, _, _ = retained.expanded(row, prefix, context, A, B, reduced, "E+")
    capacity = {host: len(leaves) for host, leaves in groups.items()}
    images = set(range(s))
    sources = set(range(s))
    options = {}
    for source in sorted(sources):
        label = A+prefix["c"]+source
        moves = []
        for host, count in capacity.items():
            meter.tick("transitions")
            image = abs(expanded[host]-label)-(d-1)
            cross = (expanded[host]<C) != (label<C)
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


def negative(row, prefix, arm, meter, retained, graph_audit):
    context = retained.original_context(row, prefix, graph_audit)
    if arm == "M":
        sequence = menu_candidates(context, meter)
    else:
        discarded = {"qualified_exteriors": 0, "qualified_strata": {}}
        sequence = retained.count_first(row, context, "E+", meter, discarded)
    counts = {"qualified_exteriors": 0, "qualified_strata": {}}
    meter.phase = "independent exterior"
    for A, B, reduced in sequence:
        actual_arm = classification(context,A,B,reduced)
        if arm == "A" and actual_arm == "M":
            continue
        if actual_arm != arm:
            raise ValueError("independent arm enumerator mismatch")
        strata = counts["qualified_strata"]
        _, _, _, left, right, direct, _, groups, _ = context
        e1, e2 = (sum(len(set(groups[h]) & reduced.keys()) for h in group) for group in (left,right))
        neutral, = (h for h in left if reduced[h] == A-1)
        pinned, = (h for h in right if reduced[h] == A+2)
        key = f"{A},{B},{e1},{e2},{int(direct in reduced)},{neutral},{pinned}"
        strata[key] = strata.get(key,0)+1
        counts["qualified_exteriors"] += 1
        meter.candidate = {"A": A, "B": B, "reduced": reduced, "ordinal": counts["qualified_exteriors"]}
        meter.phase = "independent raw allocation"
        if raw_support(row,prefix,context,A,B,reduced,meter,retained):
            raise ValueError("independent exhaustion refuted the primary negative")
        meter.phase = "independent exterior"
        meter.candidate = None
    return {"status":"PASS_INDEPENDENT_EXHAUSTION","counts":counts}


def positive(row, prefix, arm, solution, meter, retained, graph_audit, checker):
    context = retained.original_context(row,prefix,graph_audit)
    A, B, reduced = (solution[field] for field in ("A","B","reduced"))
    if classification(context,A,B,reduced) != arm:
        raise ValueError("positive witness does not belong to requested arm")
    meter.phase = "independent certificate reconstruction"
    report = retained.positive(row,prefix,"E+",solution,meter,graph_audit,checker)
    struct = report["exterior_structure"]
    p, q = sorted(reduced[h] for h in context[4])
    struct["upper_host_separation"] = q-p
    struct["arm"] = arm
    _, _, w, left, right, direct, _, _, _ = context
    has_m_slots = ((A,B) == (6,4) and {reduced[h] for h in left} == {2,3,4,5}
                   and {reduced[h] for h in right} == {8,10})
    reasons = []
    if (A,B) != (6,4):
        reasons.append("WIDTH")
    if direct in reduced:
        reasons.append("DIRECT_LEAF_IN_EXTERIOR")
    if not has_m_slots and (A,B) == (6,4):
        reasons.append("NUMERICAL_CENTER_ROLES")
    selected = struct["terminals"]
    terminal_key = sorted((x["parent"] in left,x["reduced"],x["parent_reduced"]) for x in selected)
    if terminal_key != [(False,1,10),(True,9,3)]:
        reasons.append("SELECTED_TERMINAL_ROLES")
    if arm == "A" and not reasons:
        raise ValueError("alternative exterior has no structural distinction")
    struct["outside_menu_reasons"] = reasons
    m = prefix["n"]+2*row["K"]
    cut_oriented = m+1-report["cut"]
    if cut_oriented != prefix["c"]+row["K"] or report["actual_labels"][w] != m:
        raise ValueError("polarity transport endpoints")
    report["label_side_partitions"] = {
        name: {"lower":[z for z in report["resources"][name+"_labels"] if z<report["cut"]],
               "upper":[z for z in report["resources"][name+"_labels"] if z>=report["cut"]]}
        for name in ("used","remaining")}
    report["complement"] = {"oriented_cut":cut_oriented,"oriented_frontier":0,
                            "lower_shift":A,"upper_shift":A+struct["s"],
                            "actual_lower_shift":B,"actual_upper_shift":B+struct["s"]}
    report["return_phase"] = {"phase":"S_-1","frontier":w,"label":m,"cut":report["cut"]}
    return report
