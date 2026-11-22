"""Exact bounded frontier DP retaining BOTH resource inventories and live labels.

This evaluates the retained N240 count identity in vertex order. Histories merge
only when used-label mask, used-difference mask, and all live-frontier labels
agree. No claim of constant-size global compression is made.
"""
from .budget import Limits, Budget, BudgetExceeded
from .model import validate_graph
from .search import prepare_domains

def count_labelings(graph, limits=None, pins=None, domains=None):
    lim = limits if isinstance(limits, Limits) else Limits.from_mapping(limits)
    validation = validate_graph(graph)
    if not validation["valid"]:
        return {"status": "INVALID_INPUT", "errors": validation["errors"], "method": "frontier_dp"}
    allowed, restrictions = prepare_domains(graph, pins, domains)
    vs = list(graph["vertices"])
    n = len(vs)
    m = len(graph["edges"])
    budget = Budget(lim)
    out = {"method": "frontier_dp", "status": "INCOMPLETE", "exhausted": False,
           "count": None, "count_lower_bound": 0, "witness": None,
           "restrictions": restrictions, "limits": lim.to_dict(),
           "peak_states": 1, "completed_vertices": 0}
    if n > lim.max_vertices:
        out.update(reason="max_vertices", nodes=0, elapsed_seconds=budget.elapsed())
        return out
    index = {v: i for i, v in enumerate(vs)}
    adj = {v: set() for v in vs}
    for u, v in graph["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    # Value: (number of named histories, one representative full prefix).
    states = {(0, 0, ()): (1, ())}
    old_frontier = []
    finished_count = 0
    finished_witness = None
    try:
        for i, v in enumerate(vs):
            frontier = [u for u in vs[:i+1] if any(index[w] > i for w in adj[u])]
            next_states = {}
            for (used, diffs, values), (multiplicity, history) in states.items():
                live = dict(zip(old_frontier, values))
                for x in sorted(allowed[v]):
                    budget.tick()
                    if used & (1 << x):
                        continue
                    additions = 0
                    valid = True
                    for u in adj[v]:
                        if index[u] < i:
                            d = abs(x - live[u])
                            bit = 1 << d
                            if d == 0 or d > m or (diffs | additions) & bit:
                                valid = False
                                break
                            additions |= bit
                    if not valid:
                        continue
                    updated = dict(live)
                    updated[v] = x
                    key = (used | (1 << x), diffs | additions,
                           tuple(updated[u] for u in frontier))
                    h = history + (x,)
                    if key in next_states:
                        prior, representative = next_states[key]
                        next_states[key] = (prior + multiplicity, representative)
                    else:
                        if len(next_states) >= lim.max_states:
                            raise BudgetExceeded("max_states")
                        next_states[key] = (multiplicity, h)
                        out["peak_states"] = max(out["peak_states"], len(next_states))
                    if i == n - 1:
                        finished_count += multiplicity
                        if finished_witness is None:
                            finished_witness = dict(zip(vs, h))
            states = next_states
            old_frontier = frontier
            out["completed_vertices"] = i + 1
            out["peak_states"] = max(out["peak_states"], len(states))
            if not states:
                out.update(status="EXHAUSTED_NO_SOLUTION", exhausted=True, count=0)
                break
        else:
            total = sum(value[0] for value in states.values())
            out.update(status="SAT" if total else "EXHAUSTED_NO_SOLUTION",
                       exhausted=True, count=total)
            finished_count = total
            if states and finished_witness is None:
                finished_witness = dict(zip(vs, next(iter(states.values()))[1]))
    except BudgetExceeded as exc:
        out["reason"] = str(exc)
    except KeyboardInterrupt:
        out["reason"] = "interrupted"
    out.update(witness=finished_witness, count_lower_bound=finished_count,
               nodes=budget.nodes, elapsed_seconds=budget.elapsed())
    if out["status"] == "EXHAUSTED_NO_SOLUTION":
        out["negative_evidence"] = "implementation exhaustion on declared scope; no formal negative certificate"
    return out

