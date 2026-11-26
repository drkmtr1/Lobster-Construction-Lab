"""Independent audit by named edges and raw coordinate subtraction; no launcher."""

from itertools import permutations, product


def incidence(record):
    if record["phase"] != "S0":
        raise ValueError("strict-phase records only")
    graph = record["graph"]
    v, u, w = graph["spine"][-3:]
    compulsory = {u, w}
    parent = {u: v, w: u}
    sides = {v: 0, u: 1, w: 0}
    terminals = {}
    cut_off = len(graph["spine"]) - 2
    for name, role in graph["roles"].items():
        section = role["section"]
        if section < cut_off or role["kind"] == "spine":
            continue
        if role["kind"] == "branch":
            compulsory.add(name)
            parent[name] = graph["spine"][section]
            sides[name] = int(section != cut_off)
        else:
            host = f"b:{section}:{role['branch']}"
            terminals.setdefault(host, []).append((role["leaf"], name))
            parent[name] = host
            sides[name] = int(section == cut_off)
    actual_edges = {frozenset(edge) for edge in graph["edges"]}
    if any(frozenset((name, host)) not in actual_edges for name, host in parent.items()):
        raise ValueError("named incidence absent")
    terminals = {host: [name for _, name in sorted(names)] for host, names in terminals.items()}
    return v, u, w, compulsory, parent, sides, terminals


def independent_exteriors(record, charge):
    """Count-first slot permutations, separate from the primary traversal."""
    v, u, w, compulsory, parent, sides, terminals = incidence(record)
    right = sorted(host for host in terminals if sides[host] == 1)
    left = sorted(set(terminals) - set(right))
    R = sum(len(terminals[host]) for host in right)
    K = record["fresh_edges"] // 2
    for counts in product(*(range(len(terminals[host]) + 1) for host in right)):
        for first in left:
            charge("audit_exterior_attempts")
            if not 1 <= sum(counts) <= R // 2 - 2:
                continue
            keep = dict(zip(right, counts))
            keep[first] = 1
            selected = {name for host, names in terminals.items() for name in names[:keep.get(host, 0)]}
            members = compulsory | selected
            low = sorted(name for name in members - {w} if sides[name] == 0)
            high = sorted(name for name in members - {u} if sides[name] == 1)
            A, B = len(low) + 1, len(high) + 1
            s = 2 * K - A - B
            if s < K or not A <= K <= A + s:
                continue
            for lo in permutations(range(1, A)):
                charge("audit_exterior_attempts")
                for hi in permutations(range(A + 2, A + B + 1)):
                    charge("audit_exterior_attempts")
                    reduced = dict(zip(low + high, lo + hi))
                    reduced.update({v: A, u: A + 1, w: 0})
                    weights = [abs(reduced[name] - reduced[parent[name]]) for name in members]
                    if sorted(weights) != list(range(1, A + B + 1)):
                        continue
                    remaining = {host: len(names) - keep.get(host, 0) for host, names in terminals.items()}
                    yield A, B, s, reduced, remaining


def raw_has_support(n, c, K, A, s, reduced, remaining, charge, live):
    """Independent exhaustive recursion over actual label placements without memoization."""
    image_pool = set(range(c + 2, c + 2 + s))
    host_values = {host: reduced[host] + (n + s if reduced[host] > A else 0)
                   for host in remaining}
    cut = c + K
    used = set()
    remaining = remaining.copy()

    def choose(source):
        charge("audit_states")
        live(source + 1)
        if source == s:
            return used == image_pool and not any(remaining.values())
        vertex_label = A + c + source
        for host, value in host_values.items():
            charge("audit_transitions")
            difference = abs(vertex_label - value)
            crosses = (vertex_label < cut) != (value < cut)
            if (not remaining[host] or difference not in image_pool or difference in used
                    or crosses != (difference >= c + 2 + K)):
                continue
            used.add(difference)
            remaining[host] -= 1
            answer = choose(source + 1)
            remaining[host] += 1
            used.remove(difference)
            if answer:
                return True
        return False

    return choose(0)


def negative(record, prefix, charge, live):
    if record["prefix_digest"] != prefix["digest"]:
        raise ValueError("unexpected strict prefix identity")
    checked = 0
    K = record["fresh_edges"] // 2
    for A, B, s, reduced, residual in independent_exteriors(record, charge):
        checked += 1
        if raw_has_support(prefix["edges"], prefix["minimum_cut"], K, A, s, reduced, residual, charge, live):
            raise ValueError("independent audit contradicted a candidate negative")
    return {"status": "NEGATIVE", "basis": "independent raw exhaustion", "qualified_exteriors": checked}


def permutation_cycles(arrows):
    successor = {row[2]: row[3] for row in arrows}
    visited = set()
    cycles = []
    for start in sorted(successor):
        if start in visited:
            continue
        orbit = []
        here = start
        while here not in visited:
            orbit.append(here)
            visited.add(here)
            here = successor[here]
        if here != start:
            raise ValueError("not a permutation cycle")
        cycles.append(orbit)
    return cycles


def positive(record, prefix, witness):
    # This future audit must call the unchanged checker on the frozen original.
    from lcl.verify import verify_certificate

    if record["prefix_digest"] != prefix["digest"]:
        raise ValueError("unexpected strict prefix identity")
    graph = record["graph"]
    labels = witness["labels"]
    result = verify_certificate(graph, labels, expected_graph_digest=record["digest"])
    if not result["valid"]:
        raise ValueError("original-target checker rejected the proposed certificate")
    v, u, w, compulsory, parent, sides, terminals = incidence(record)
    terminal_owner = {name: host for host, names in terminals.items() for name in names}
    reduced = witness["reduced"]
    A, B, s = (witness[key] for key in ("A", "B", "s"))
    n, c = prefix["edges"], prefix["minimum_cut"]
    d = c + 2
    K = record["fresh_edges"] // 2
    m = n + 2 * K
    minimum = {name: m - value for name, value in labels.items()}
    if not ((compulsory | {v}) <= set(reduced) <= (compulsory | {v} | set(terminal_owner))):
        raise ValueError("unexpected reduced vertices")
    if (A + B + s != 2 * K or s < K or not A <= K <= A + s
            or [reduced[name] for name in (v, u, w)] != [A, A + 1, 0]):
        raise ValueError("unexpected exterior geometry")
    for side, alphabet in ((0, range(A + 1)), (1, range(A + 1, A + B + 1))):
        if sorted(value for name, value in reduced.items() if sides[name] == side) != list(alphabet):
            raise ValueError("reduced side alphabet")
    exterior_diffs = sorted(abs(reduced[name] - reduced[parent[name]]) for name in reduced if name != v)
    if exterior_diffs != list(range(1, A + B + 1)):
        raise ValueError("reduced differences")
    selections = set(reduced) & set(terminal_owner)
    e1 = sum(sides[name] == 1 for name in selections)
    e2 = len(selections) - e1
    R = sum(record["suffix"][1])
    if not (e1 == 1 and 1 <= e2 <= R // 2 - 2 and A == 4 + e2
            and B == len(record["suffix"][1]) + 2):
        raise ValueError("selected counts")
    for name, actual in prefix["actual_labels"].items():
        oriented = n - actual
        if minimum[name] != A + oriented + (s if oriented >= c else 0):
            raise ValueError("old label transport")
    for name, value in reduced.items():
        if minimum[name] != value + (n + s if value > A else 0):
            raise ValueError("reduced placement")
    arrows = []
    x = y = 0
    shifts = {}
    for leaf in set(terminal_owner) - selections:
        host = terminal_owner[leaf]
        source = minimum[leaf] - (A + c)
        image = abs(minimum[leaf] - minimum[host]) - d
        crosses = (minimum[leaf] < c + K) != (minimum[host] < c + K)
        if crosses != (image >= K):
            raise ValueError("incorrect physical crossing")
        if sides[host] == 0:
            shifts[host] = A - 2 - reduced[host]
            if image - source != shifts[host]:
                raise ValueError("wrong actual lower translation")
        x += int(crosses and sides[host] == 1)
        y += int(crosses and sides[host] == 0)
        arrows.append([leaf, host, source, image])
    arrows.sort(key=lambda row: row[2])
    if (arrows != witness["gap"] or [row[2] for row in arrows] != list(range(s))
            or sorted(row[3] for row in arrows) != list(range(s)) or (x, y) != (R // 2 - 2 - e2, 0)):
        raise ValueError("raw gap witness")
    cut = m + 1 - (c + K)
    first_section = graph["roles"][u]["section"]
    used_vertices = {name for name, role in graph["roles"].items() if role["section"] <= first_section}
    partitions = {key: [] for key in ("used_crossing", "used_noncrossing",
                                      "remaining_crossing", "remaining_noncrossing")}
    pending = []
    for a, b in graph["edges"]:
        aa, bb = labels[a], labels[b]
        used = a in used_vertices and b in used_vertices
        crossing = (aa < cut) != (bb < cut)
        key = ("used_" if used else "remaining_") + ("crossing" if crossing else "noncrossing")
        partitions[key].append(abs(aa - bb))
        if (a in used_vertices) != (b in used_vertices):
            pending.append(frozenset((a, b)))
    crossing = sorted(partitions["used_crossing"] + partitions["remaining_crossing"])
    noncrossing = sorted(partitions["used_noncrossing"] + partitions["remaining_noncrossing"])
    if (labels[w] != m or pending != [frozenset((u, w))]
            or crossing != list(range(d + K, m + 1)) or noncrossing != list(range(1, d + K))):
        raise ValueError("actual strict return")
    label_partitions = {key: [] for key in ("used_lower", "used_upper", "remaining_lower", "remaining_upper")}
    for name, label in labels.items():
        key = ("used_" if name in used_vertices else "remaining_") + ("lower" if label < cut else "upper")
        label_partitions[key].append(label)
    return {"status": "POSITIVE", "checker": "PASS", "cut": cut,
            "crossing": crossing, "noncrossing": noncrossing, "cross_counts": [x, y],
            "selected": sorted((name, terminal_owner[name]) for name in selections),
            "lower_shifts": shifts, "cycles": permutation_cycles(arrows),
            "used_labels": sorted(labels[name] for name in used_vertices),
            "remaining_labels": sorted(labels[name] for name in set(labels) - used_vertices),
            "label_partitions": {key: sorted(values) for key, values in label_partitions.items()},
            "difference_partitions": {key: sorted(values) for key, values in partitions.items()},
            "connector": {"names": [u, w], "labels": [labels[u], labels[w]], "weight": abs(labels[u] - labels[w])}}
