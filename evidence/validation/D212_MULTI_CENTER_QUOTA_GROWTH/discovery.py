"""Dormant D212-only specialization of the LCL reference named DFS.

There is deliberately no script entry point. Import and function entry are
reserved for a separately authorized future attempt.
"""

from time import process_time_ns

from lcl.budget import Budget, BudgetExceeded, Limits
from lcl.model import validate_graph
from lcl.search import prepare_domains


def _in_span(option, other_cut):
    a, cut, _ = option
    return a < other_cut < cut if a < cut else cut < other_cut <= a


def _compatible(first, second):
    _, cut, threshold = first
    _, other_cut, other_threshold = second
    if cut == other_cut or threshold == other_threshold:
        return False
    return (
        _in_span(first, other_cut) == (other_threshold < threshold)
        and _in_span(second, cut) == (threshold < other_threshold)
    )


def discover(original, case_limits, live_frames_max):
    """Search the exact supplied original after future admission, with no I/O."""
    cpu_start = process_time_ns()
    budget = Budget(Limits(
        max_nodes=case_limits["label_nodes"],
        time_limit=case_limits["wall_seconds"],
        max_vertices=18,
        max_states=live_frames_max,
    ))
    validation = validate_graph(original)
    if not validation["valid"] or original.get("profile") != case_limits["profile"]:
        raise ValueError("Original does not match the admitted case")
    vertices = tuple(original["vertices"])
    if len(vertices) > budget.limits.max_vertices:
        raise ValueError("Original exceeds admitted vertex limit")
    edges = tuple(map(tuple, original["edges"]))
    n = len(edges)
    spine = tuple(original["spine"])
    hosts = tuple(v for v in vertices if original["roles"][v]["kind"] == "branch")
    roles = original["roles"]
    arms = tuple(sorted(
        (v for v in hosts if roles[v]["section"] == 1),
        key=lambda v: roles[v]["branch"],
    ))
    cpu_limit = case_limits["cpu_seconds"] * 1_000_000_000
    join_nodes = 0
    peak_frames = 0
    complete_graceful_reached = 0
    labels = {}
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    domains, _ = prepare_domains(original)
    domains = {v: sorted(values) for v, values in domains.items()}

    def check():
        budget.check()
        if process_time_ns() - cpu_start >= cpu_limit:
            raise BudgetExceeded("case_cpu_seconds")

    def frames(count):
        nonlocal peak_frames
        if count > live_frames_max:
            raise BudgetExceeded("live_frames_max")
        peak_frames = max(peak_frames, count)

    def legal(v, x, used_labels, used_weights):
        if used_labels & (1 << x):
            return None
        if v == spine[0] and spine[-1] in labels and x >= labels[spine[-1]]:
            return None
        if v == spine[-1] and spine[0] in labels and x <= labels[spine[0]]:
            return None
        if v in arms:
            index = arms.index(v)
            if any(w in labels and labels[w] >= x for w in arms[:index]):
                return None
            if any(w in labels and labels[w] <= x for w in arms[index + 1:]):
                return None
        added = 0
        for w in adjacency[v]:
            if w in labels:
                difference = abs(labels[w] - x)
                bit = 1 << difference
                if (used_weights | added) & bit:
                    return None
                added |= bit
        return added

    def possible_host_options():
        """Partial-edge necessary condition, exact for completed labels."""
        max_non = [0] * (n + 1)
        min_cross = [n] * (n + 1)
        for u, v in edges:
            if u not in labels or v not in labels:
                continue
            low, high = sorted((labels[u], labels[v]))
            weight = high - low
            for cut in range(1, n + 1):
                if low < cut <= high:
                    min_cross[cut] = min(min_cross[cut], weight)
                else:
                    max_non[cut] = max(max_non[cut], weight)
        options = {}
        for host in hosts:
            if host not in labels:
                continue
            a = labels[host]
            choices = []
            for cut in range(1, n + 1):
                threshold = cut - a if a < cut else a - cut + 1
                if max_non[cut] < threshold <= min_cross[cut]:
                    choices.append((a, cut, threshold))
            options[host] = sorted(choices, key=lambda option: (option[2], option[1]))
        return options

    def join(options, remaining, chosen):
        nonlocal join_nodes
        check()
        frames(len(labels) + len(chosen) + 2)
        if not remaining:
            return dict(chosen)
        smallest = None
        for host in remaining:
            choices = [
                option for option in options[host]
                if all(_compatible(option, prior) for prior in chosen.values())
            ]
            if not choices:
                return None
            if smallest is None or len(choices) < len(smallest[1]):
                smallest = (host, choices)
        host, choices = smallest
        rest = tuple(v for v in remaining if v != host)
        for option in choices:
            check()
            if join_nodes >= case_limits["join_nodes"]:
                raise BudgetExceeded("join_nodes")
            join_nodes += 1
            chosen[host] = option
            answer = join(options, rest, chosen)
            del chosen[host]
            if answer is not None:
                return answer
        return None

    def visit(used_labels, used_weights):
        nonlocal complete_graceful_reached
        check()
        frames(len(labels) + 1)
        if len(labels) == len(vertices):
            complete_graceful_reached += 1
        options = possible_host_options()
        if any(not choices for choices in options.values()):
            return None
        if len({row[1] for choices in options.values() for row in choices}) < len(options):
            return None
        if len(labels) == len(vertices):
            selected = join(options, hosts, {})
            if selected is None:
                return None
            return {
                "labels": dict(labels),
                "selected": {v: {"cut": c, "threshold": d}
                             for v, (_, c, d) in selected.items()},
            }

        smallest = None
        for v in vertices:
            if v in labels:
                continue
            choices = []
            for x in domains[v]:
                added = legal(v, x, used_labels, used_weights)
                if added is not None:
                    choices.append((x, added))
            if not choices:
                return None
            key = (len(choices), -len(adjacency[v]))
            if smallest is None or key < smallest[0]:
                smallest = (key, v, choices)
        _, vertex, choices = smallest
        for x, added in choices:
            check()
            budget.tick()
            labels[vertex] = x
            answer = visit(used_labels | (1 << x), used_weights | added)
            del labels[vertex]
            if answer is not None:
                return answer
        return None

    witness = None
    reason = None
    try:
        witness = visit(0, 0)
        check()
        status = "CANDIDATE" if witness is not None else "EXHAUSTED_NO_CERTIFICATE"
    except (BudgetExceeded, KeyboardInterrupt) as exc:
        status = "INCOMPLETE"
        reason = str(exc) if isinstance(exc, BudgetExceeded) else "interrupted"
    return {
        "status": status,
        "reason": reason,
        "label_nodes": budget.nodes,
        "join_nodes": join_nodes,
        "peak_frames": peak_frames,
        "complete_graceful_reached": complete_graceful_reached,
        "process_cpu_ns": process_time_ns() - cpu_start,
        "wall_seconds": budget.elapsed(),
        "candidate": witness,
    }
