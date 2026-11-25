"""Named exterior generator and D146 relative frontier support."""

from dataclasses import dataclass
from itertools import product


@dataclass
class Case:
    graph: dict
    v: str
    u: str
    w: str
    k_total: int
    parents: dict
    sides: dict
    compulsory: tuple
    optional: tuple
    terminals: set


def case_data(row, prefix):
    graph = row["graph"]
    v = prefix["frontier"]
    u, w = graph["spine"][-2:]
    fresh = {name for name in graph["vertices"] if name not in prefix["oriented_labels"]}
    if len(fresh) != row["fresh"]:
        raise ValueError("frozen fresh vertex count")
    adjacency = {name: [] for name in fresh | {v}}
    for a, b in graph["edges"]:
        if a in adjacency and b in adjacency:
            adjacency[a].append(b)
            adjacency[b].append(a)
    parents = {v: None}
    sides = {v: 0}
    visit = [v]
    for parent in visit:
        for name in adjacency[parent]:
            if name not in parents:
                parents[name] = parent
                sides[name] = 1 - sides[parent]
                visit.append(name)
    if len(parents) != len(adjacency) or parents[u] != v or parents[w] != u:
        raise ValueError("named spine interface")
    compulsory = tuple(name for name in visit if name in (v, u, w) or len(adjacency[name]) > 1)
    optional = tuple(sorted(fresh.difference(compulsory)))
    terminals = {name for name in optional if graph["roles"][name]["kind"] == "leaf"}
    return Case(graph, v, u, w, row["fresh"]//2, parents, sides, compulsory, optional, terminals)


def symbolic_exclusion(suffix, arm):
    first, second = suffix
    if 0 in first:
        return None
    centers = sum(q > 0 for q in second)
    leaves = second.count(0)
    if centers == 1 and leaves == 0:
        return "D147-first-upper-source"
    if arm == "T" and ((centers == 1 and leaves <= 3) or (centers == 2 and leaves <= 2)):
        return "terminal-free-forced-three"
    return None


def exterior_candidates(case, arm, meter, prunes):
    optional = tuple(name for name in case.optional if arm == "E" or name not in case.terminals)

    def reject(reason):
        prunes[reason] = prunes.get(reason, 0) + 1

    def label(exterior):
        A = sum(case.sides[name] == 0 for name in exterior) - 1
        B = sum(case.sides[name] == 1 for name in exterior)
        if A < 2 or B < 2 or A+B > case.k_total:
            reject("cut-width")
            return
        labels = {case.v: A, case.u: A+1, case.w: 0}
        used = {1, A+1}
        children = {name: [] for name in exterior}
        for name in exterior:
            if name != case.v:
                children[case.parents[name]].append(name)
        # Parent before child, with independently indexed roles.
        names = sorted(exterior.difference(labels), key=lambda name: (name in case.terminals, name))
        free = [set(range(1, A)), set(range(A+2, A+B+1))]

        def place(index):
            meter.tick("exterior_nodes")
            if index == len(names):
                yield A, B, dict(labels)
                return
            name = names[index]
            parent = case.parents[name]
            side = case.sides[name]
            for value in sorted(free[side]):
                if value == A+B and parent != case.w:
                    meter.tick("exterior_nodes")
                    reject("maximum-physical-neighbor")
                    continue
                weight = abs(value - labels[parent])
                if weight in used:
                    meter.tick("exterior_nodes")
                    reject("repeated-exterior-weight")
                    continue
                labels[name] = value
                free[side].remove(value)
                used.add(weight)
                yield from place(index+1)
                del labels[name]
                free[side].add(value)
                used.remove(weight)

        yield from place(0)

    exterior = set(case.compulsory)

    def choose(index):
        meter.tick("exterior_nodes")
        if len(exterior) - 1 > case.k_total:
            reject("exterior-too-large")
        elif index == len(optional):
            yield from label(exterior)
        else:
            yield from choose(index+1)
            name = optional[index]
            exterior.add(name)
            yield from choose(index+1)
            exterior.remove(name)

    yield from choose(0)


def role_values(A, B):
    return tuple(range(A)) + tuple(range(A+1, A+B+1))


def folded_support(A, B, s, quotas, meter):
    """Return one list (source, host-index, image) or None after exhaustion."""
    K = (A+B+s)//2
    k = K-A
    W = max(1, A-2, B-1)
    T = s+1
    P = T//2
    roles = role_values(A, B)

    def positions(col):
        row = []
        if 0 <= col <= s//2:
            row.append((col, 0))
        if 2 <= col <= P:
            row.append((T-col, 1))
        return row

    def options(source, origin):
        for index, host in enumerate(roles):
            if not quotas[index]:
                continue
            below = host < A
            target = source+A-2-host if below else s+host-A-source
            crosses = (source < k) != below
            if not 0 <= target < s or (target >= K) != crosses:
                continue
            right = int(target > s//2)
            column = T-target if right else target
            offset = column - origin
            if not 0 <= offset <= 2*W:
                raise ValueError("illegal D146 folded offset")
            yield index, target, 1 << (2*offset+right)

    if len(quotas) != len(roles) or any(type(q) is not int or q < 0 for q in quotas) or sum(quotas) != s:
        raise ValueError("bad exact gap quotas")
    start = (0, (0,)*len(roles))
    layers = [{start: None}]
    live = 1
    meter.tick("transfer_states")
    for p in range(P+W+1):
        origin = p-W
        sources = tuple(source for source, _ in positions(p))
        choices = tuple(tuple(options(source, origin)) for source in sources)
        retiring = sum(1 << row for _, row in positions(origin))
        next_layer = {}
        for state in layers[-1]:
            for arcs in product(*choices):
                meter.tick("transitions")
                mask, counts = state
                new_counts = list(counts)
                for index, _, bit in arcs:
                    new_counts[index] += 1
                    if mask & bit or new_counts[index] > quotas[index]:
                        break
                    mask |= bit
                else:
                    if mask & retiring != retiring:
                        continue
                    successor = (mask >> 2, tuple(new_counts))
                    if successor not in next_layer:
                        meter.tick("transfer_states")
                        live += 1
                        meter.memory(live)
                        next_layer[successor] = (state, tuple((i, h, j) for i, (h, j, _) in zip(sources, arcs)))
        if not next_layer:
            return None
        layers.append(next_layer)
    final = (0, tuple(quotas))
    if final not in layers[-1]:
        return None
    selected = []
    for layer in reversed(layers[1:]):
        final, arcs = layer[final]
        selected.extend(arcs)
    return sorted(selected)


def assignment(case, prefix, A, B, reduced, meter):
    hosts = {value: name for name, value in reduced.items() if name != case.v}
    roles = role_values(A, B)
    q_names = {name: [] for name in hosts.values()}
    for leaf in case.optional:
        if leaf not in reduced:
            q_names[case.parents[leaf]].append(leaf)
    def ordinal(name):
        role = case.graph["roles"][name]
        return role.get("leaf", role["branch"])
    for names in q_names.values():
        names.sort(key=ordinal)
    n, c = prefix["n"], prefix["c"]
    m = n+2*case.k_total
    s = m-n-A-B
    quotas = tuple(len(q_names[hosts[h]]) for h in roles)
    choices = folded_support(A, B, s, quotas, meter)
    if choices is None:
        return None
    oriented = {v: A+x+s*(x>=c) for v, x in prefix["oriented_labels"].items()}
    for name, label in reduced.items():
        if name != case.v:
            oriented[name] = label if label < A else n+s+label
    rows = []
    used = [0]*len(roles)
    for i, index, j in choices:
        host = hosts[roles[index]]
        leaf = q_names[host][used[index]]
        used[index] += 1
        oriented[leaf] = A+c+i
        rows.append([leaf, host, i, j])
    return {"A": A, "B": B, "s": s, "reduced": reduced, "gap": rows,
            "labels": {v: m-x for v, x in oriented.items()}}


def search(row, prefix, arm, meter):
    reason = symbolic_exclusion(row["suffix"], arm)
    if reason:
        return {"claim": "NO", "prunes": {reason: 1}, "exteriors": 0}
    case = case_data(row, prefix)
    prunes = {}
    count = 0
    for A, B, reduced in exterior_candidates(case, arm, meter, prunes):
        count += 1
        witness = assignment(case, prefix, A, B, reduced, meter)
        if witness is not None:
            return {"claim": "YES", "prunes": prunes, "exteriors": count, "witness": witness}
    return {"claim": "NO", "prunes": prunes, "exteriors": count}
