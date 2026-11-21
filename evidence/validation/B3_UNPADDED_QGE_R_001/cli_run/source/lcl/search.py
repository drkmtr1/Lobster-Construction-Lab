"""Bounded exact DFS over named labelings; no implicit root or alpha restriction."""
from .budget import Limits, Budget, BudgetExceeded
from .model import validate_graph
from collections.abc import Mapping

def prepare_domains(graph, pins=None, domains=None):
    vertices = graph["vertices"]
    m = len(graph["edges"])
    alphabet = set(range(m + 1))
    if pins is not None and not isinstance(pins, Mapping):
        raise ValueError("pins must be a mapping from physical vertex IDs to integer labels")
    if domains is not None and not isinstance(domains, Mapping):
        raise ValueError("domains must be a mapping from physical vertex IDs to label collections")
    pins = {} if pins is None else dict(pins)
    domains = {} if domains is None else dict(domains)
    if (set(pins) | set(domains)) - set(vertices):
        raise ValueError("Restriction refers to an unknown physical vertex")
    normalized = {}
    for v, values in domains.items():
        if not isinstance(values, (list, tuple, set, frozenset)):
            raise ValueError("Each domain must be an explicit collection of integers")
        if any(type(x) is not int or x not in alphabet for x in values):
            raise ValueError("Domain label is not an integer in 0..m")
        normalized[v] = sorted(set(values))
    for v, label in pins.items():
        if type(label) is not int or label not in alphabet:
            raise ValueError("Pinned label is not an integer in 0..m")
    allowed = {v: set(normalized.get(v, alphabet)) for v in vertices}
    for v, label in pins.items():
        allowed[v] &= {label}
    restrictions = {
        "scope": "restricted" if pins or normalized else "unrestricted",
        "pins": pins,
        "domains": normalized,
        "hidden_symmetry_reduction": False,
        "count_convention": "bijections on named physical vertices; no symmetry quotient",
    }
    return allowed, restrictions

def solve(graph, pins=None, domains=None, limits=None, count=False):
    lim = limits if isinstance(limits, Limits) else Limits.from_mapping(limits)
    validation = validate_graph(graph)
    if not validation["valid"]:
        return {"status": "INVALID_INPUT", "errors": validation["errors"], "method": "dfs"}
    allowed, restrictions = prepare_domains(graph, pins, domains)
    vertices = list(graph["vertices"])
    m = len(graph["edges"])
    budget = Budget(lim)
    result = {
        "method": "dfs", "restrictions": restrictions, "limits": lim.to_dict(),
        "status": "INCOMPLETE", "exhausted": False, "count": None,
        "count_lower_bound": 0, "witness": None, "nodes": 0,
    }
    if len(vertices) > lim.max_vertices:
        result.update(reason="max_vertices", elapsed_seconds=budget.elapsed())
        return result
    adjacency = {v: set() for v in vertices}
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    position = {v: i for i, v in enumerate(vertices)}
    labels = {}
    found = 0
    witness = None

    def legal(v, label, used_labels, used_diffs):
        if used_labels & (1 << label):
            return None
        new_diffs = 0
        for u in adjacency[v]:
            if u in labels:
                d = abs(label - labels[u])
                bit = 1 << d
                if d == 0 or d > m or (used_diffs | new_diffs) & bit:
                    return None
                new_diffs |= bit
        return new_diffs

    def visit(used_labels, used_diffs):
        nonlocal found, witness
        budget.check()
        if len(labels) == len(vertices):
            found += 1
            if witness is None:
                witness = dict(labels)
            return not count
        # MRV changes only visit order, never the set of label assignments.
        best_v, best_choices, best_key = None, None, None
        for v in vertices:
            if v in labels:
                continue
            choices = []
            for x in sorted(allowed[v]):
                dmask = legal(v, x, used_labels, used_diffs)
                if dmask is not None:
                    choices.append((x, dmask))
            key = (len(choices), -len(adjacency[v]), position[v])
            if best_key is None or key < best_key:
                best_v, best_choices, best_key = v, choices, key
            if not choices:
                return False
        for x, dmask in best_choices:
            budget.tick()
            labels[best_v] = x
            stop = visit(used_labels | (1 << x), used_diffs | dmask)
            del labels[best_v]
            if stop:
                return True
        return False

    try:
        stopped_at_witness = visit(0, 0)
        result["exhausted"] = not stopped_at_witness
        result["status"] = "SAT" if found else "EXHAUSTED_NO_SOLUTION"
        if result["exhausted"]:
            result["count"] = found
    except BudgetExceeded as exc:
        result["reason"] = str(exc)
    except KeyboardInterrupt:
        result["reason"] = "interrupted"
    result.update(witness=witness, count_lower_bound=found,
                  nodes=budget.nodes, elapsed_seconds=budget.elapsed())
    if result["status"] == "EXHAUSTED_NO_SOLUTION":
        result["negative_evidence"] = "implementation exhaustion on declared scope; no formal negative certificate"
    return result

