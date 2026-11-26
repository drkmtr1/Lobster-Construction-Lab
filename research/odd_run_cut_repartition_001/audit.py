"""Unexecuted independent raw-coordinate audit for D197."""

import hashlib
import json

from .budget import Budget


def _reconstruct(graph):
    """Independently reconstruct physical names, roles and incidences."""
    profile = graph["profile"]
    spine = [f"s:{i}" for i in range(len(profile))]
    vertices = set(spine)
    edges = {tuple(sorted(pair)) for pair in zip(spine, spine[1:])}
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, row in enumerate(profile):
        for j, quota in enumerate(row):
            branch = f"b:{i}:{j}"
            vertices.add(branch)
            edges.add(tuple(sorted((spine[i], branch))))
            roles[branch] = {"kind": "branch", "section": i, "branch": j}
            for k in range(quota):
                terminal = f"l:{i}:{j}:{k}"
                vertices.add(terminal)
                edges.add(tuple(sorted((branch, terminal))))
                roles[terminal] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
    if graph["spine"] != spine or graph["roles"] != roles:
        raise ValueError("Frozen spine or indexed roles differ")
    if len(vertices) != len(graph["vertices"]) or vertices != set(graph["vertices"]):
        raise ValueError("Frozen vertex names differ")
    if len(edges) != len(graph["edges"]) or edges != {tuple(sorted(e)) for e in graph["edges"]}:
        raise ValueError("Frozen named incidences differ")
    payload = dict(vertices=sorted(vertices), edges=sorted(edges), profile=profile, spine=spine, roles=roles)
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                                      ensure_ascii=False).encode()).hexdigest()
    return vertices, sorted(edges), digest


def _inputs(budget):
    record = budget.original
    vertices, edges, target_digest = _reconstruct(record["original"])
    old_vertices, old_edges, old_digest = _reconstruct(record["prefix_graph"])
    if target_digest != record["original_digest"] or old_digest != record["prefix_digest"]:
        raise ValueError("Exact graph digest mismatch")
    if old_digest != budget.prefix["prefix_digest"] or len(old_edges) != 15 or len(edges) != 30:
        raise ValueError("Prefix identity or graph order mismatch")
    if old_edges != [e for e in edges if set(e) <= old_vertices]:
        raise ValueError("Actual original prefix embedding mismatch")
    old = budget.prefix["minimum_labels"]
    if set(old) != old_vertices or sorted(old.values()) != list(range(16)):
        raise ValueError("Independent prefix label alphabet differs")
    v = budget.prefix["frontier"]
    w = record["receiving_spine"]
    i = record["original"]["roles"][w]["section"]
    if old[v] != 0 or record["original"]["profile"][i] != [2, 7, 0, 1]:
        raise ValueError("Registered role premise differs")
    return vertices, edges, old_vertices, old_edges, old, v, w, i


def _indexed_children(slots, picked=()):
    if len(picked) == 4:
        yield picked
        return
    for label in slots:
        yield from _indexed_children(tuple(other for other in slots if other != label),
                                     (*picked, label))


def _difference_support(labels, differences, hosts, quotas, cut, budget):
    """Independent difference-ordered exact cover using raw endpoint arithmetic."""
    ordered_weights = sorted(differences, reverse=True)
    choices = []
    for weight in ordered_weights:
        row = []
        for j, host in enumerate(hosts):
            for proposed in (host - weight, host + weight):
                budget.charge("audit", "transitions")
                if proposed in labels and ((proposed < cut) != (host < cut)) == (weight >= 16):
                    row.append((proposed, j))
        choices.append(row)
    selected = []

    def cover(index, vacant, remaining):
        budget.charge("audit", "states")
        budget.observe_live("audit", index + 1)
        if index == len(ordered_weights):
            return not vacant and not any(remaining)
        for candidate, parent in choices[index]:
            budget.charge("audit", "transitions")
            if candidate not in vacant or not remaining[parent]:
                continue
            quotas_left = list(remaining)
            quotas_left[parent] -= 1
            selected.append((candidate, parent))
            if cover(index + 1, vacant - {candidate}, tuple(quotas_left)):
                return True
            selected.pop()
        return False

    return tuple(selected) if cover(0, frozenset(labels), tuple(quotas)) else None


def search_independently(budget: Budget):
    """Prospective raw audit. Exhaustion alone is not a published disposition."""
    _, _, _, old_edges, incoming, v, w, i = _inputs(budget)
    actual_children = tuple(f"b:{i}:{j}" for j in range(4))
    for frontier, cut in ((30, 17), (0, 14)):
        for r in range(15, 0, -1):
            for upper_width in range(15, -1, -1):
                for lower_width in range(15 - upper_width, -1, -1):
                    budget.charge("audit", "geometries")
                    width = 15 - lower_width - upper_width
                    old = {
                        name: value + lower_width + (width if value >= r else 0)
                        for name, value in incoming.items()
                    }
                    fresh = sorted(set(range(31)) - set(old.values()), reverse=True)
                    if frontier not in fresh:
                        continue
                    old_weights = [abs(old[u] - old[v0]) for u, v0 in old_edges]
                    if len(set(old_weights)) != 15:
                        continue
                    if any(((old[u] < cut) != (old[v0] < cut)) != (d >= 16)
                           for (u, v0), d in zip(old_edges, old_weights, strict=True)):
                        continue
                    slots = tuple(value for value in fresh if value != frontier)
                    for child_labels in _indexed_children(slots):
                        budget.charge("audit", "raw_placements")
                        rooted = (old[v], *child_labels)
                        attached = [abs(frontier - value) for value in rooted]
                        used = set(old_weights + attached)
                        if len(used) != 20 or 0 in used:
                            continue
                        if any(((frontier < cut) != (value < cut)) != (d >= 16)
                               for value, d in zip(rooted, attached, strict=True)):
                            continue
                        labels = set(slots) - set(child_labels)
                        differences = set(range(1, 31)) - used
                        hosts = tuple(child_labels[j] for j in (0, 1, 3))
                        support = _difference_support(labels, differences, hosts, (2, 7, 1), cut, budget)
                        if support is None:
                            continue
                        full = dict(old)
                        full[w] = frontier
                        full.update(zip(actual_children, child_labels, strict=True))
                        for parent, original_index in enumerate((0, 1, 3)):
                            assigned = sorted(label for label, j in support if j == parent)
                            for t, label in enumerate(assigned):
                                full[f"l:{i}:{original_index}:{t}"] = label
                        return {
                            "status": "CANDIDATE", "labels": full, "r": r,
                            "h": sum(value < cut for value in old.values()),
                            "A": lower_width, "B": upper_width, "s": width,
                            "frontier_label": frontier, "output_cut": cut,
                            "original_digest": budget.original["original_digest"],
                            "prefix_digest": budget.original["prefix_digest"],
                        }
    return {"status": "EXHAUSTED", "engine": "audit"}


def _resource_rows(edges, labels, cut):
    return [
        dict(ends=[u, v], difference=abs(labels[u] - labels[v]),
             crosses=(labels[u] < cut) != (labels[v] < cut))
        for u, v in edges
    ]


def _label_parts(names, labels, cut):
    return dict(names=sorted(names), lower=sorted(labels[v] for v in names if labels[v] < cut),
                upper=sorted(labels[v] for v in names if labels[v] >= cut))


def verify_witness(budget: Budget, witness):
    """Prospective positive certificate audit, including the unchanged checker."""
    vertices, edges, old_vertices, old_edges, incoming, v, w, i = _inputs(budget)
    budget.poll()
    r, h, a, b, s, frontier, cut = (
        witness[key] for key in ("r", "h", "A", "B", "s", "frontier_label", "output_cut")
    )
    if (not all(type(value) is int for value in (r, h, a, b, s, frontier, cut))
            or not 1 <= r <= 15 or min(a, b, s) < 0 or a + b + s != 15
            or (frontier, cut) not in ((0, 14), (30, 17))):
        raise ValueError("Witness is outside the registered domain")
    labels = witness["labels"]
    if (set(labels) != vertices or any(type(x) is not int for x in labels.values())
            or set(labels.values()) != set(range(31)) or labels[w] != frontier):
        raise ValueError("Witness violates the full vertex alphabet or extreme frontier")
    if any(labels[name] != value + a + s * (value >= r) for name, value in incoming.items()):
        raise ValueError("Witness changes the exact old embedding")
    if h != sum(labels[name] < cut for name in old_vertices):
        raise ValueError("Witness gives the wrong induced old cut")
    if (witness["original_digest"] != budget.original["original_digest"]
            or witness["prefix_digest"] != budget.original["prefix_digest"]):
        raise ValueError("Witness claims the wrong input identity")
    full = _resource_rows(edges, labels, cut)
    if (sorted(row["difference"] for row in full if row["crosses"]) != list(range(16, 31))
            or sorted(row["difference"] for row in full if not row["crosses"]) != list(range(1, 16))):
        raise ValueError("Actual difference spectrum disagrees")
    installed = _resource_rows(old_edges, labels, cut)
    pending = [row for row in full if not set(row["ends"]) <= old_vertices]
    connectors = [row for row in pending if set(row["ends"]) & old_vertices]
    if len(connectors) != 1 or set(connectors[0]["ends"]) != {v, w}:
        raise ValueError("Literal connector topology disagrees")
    # Both reference cuts are recorded because r need not be the supplied phase cut.
    changes = {}
    for key, reference in (("embedding_split", r), ("supplied_prefix_cut", budget.prefix["normalized_cut"])):
        old_rows = _resource_rows(old_edges, incoming, reference)
        changes[key] = dict(
            side_vertices=sorted(name for name in old_vertices
                                 if (incoming[name] < reference) != (labels[name] < cut)),
            crossing_edges=[dict(before=before, after=after)
                            for before, after in zip(old_rows, installed, strict=True)
                            if before["crosses"] != after["crosses"]],
        )
    child_placements = {f"b:{i}:{j}": labels[f"b:{i}:{j}"] for j in range(4)}
    terminal_placements = [
        dict(name=f"l:{i}:{j}:{k}", parent=f"b:{i}:{j}", label=labels[f"l:{i}:{j}:{k}"])
        for j, q in enumerate((2, 7, 0, 1)) for k in range(q)
    ]
    budget.poll()
    from lcl.verify import verify_certificate
    checked = verify_certificate(budget.original["original"], labels, budget.original["original_digest"])
    budget.poll()
    if checked.get("valid") is not True or checked.get("graph_digest") != budget.original["original_digest"]:
        raise ValueError("Unchanged original-target checker failed")
    return dict(witness=witness, changes=changes, full_edge_resources=full,
                original_child_placements=child_placements, original_terminal_placements=terminal_placements,
                old_labels=_label_parts(old_vertices, labels, cut),
                remaining_labels=_label_parts(vertices - old_vertices, labels, cut),
                old_edge_resources=installed, remaining_edge_resources=pending,
                residual_terminal_labels=sorted(row["label"] for row in terminal_placements),
                residual_terminal_differences=sorted(abs(row["label"] - labels[row["parent"]])
                                                     for row in terminal_placements),
                literal_connector={**connectors[0], "labels": [labels[x] for x in connectors[0]["ends"]]},
                original_checker=checked)
