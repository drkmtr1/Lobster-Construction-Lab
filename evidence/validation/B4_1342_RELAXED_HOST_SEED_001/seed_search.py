"""Exact bounded DFS for the task's named graceful alpha predicate."""

from itertools import combinations
import time

H, Z, U = "b:0:0", "b:2:0", "s:4"


def topology(graph):
    neighbors = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].append(v)
        neighbors[v].append(u)
    side = {U: 1}
    queue = [U]
    for u in queue:
        for v in neighbors[u]:
            if v not in side:
                side[v] = 1 - side[u]
                queue.append(v)
            if side[u] == side[v]:
                raise ValueError("edge does not cross the physical bipartition")
    if len(side) != len(neighbors) or sum(side.values()) != 10 or len(side) != 19:
        raise ValueError("incorrect search topology")
    return neighbors, side


def candidate(a, c):
    if type(a) is not int or not 2 <= a <= 8:
        raise ValueError("a must be an exact integer in 2..8")
    if type(c) is not int or not 11 <= c <= 18:
        raise ValueError("c must be an exact integer in 11..18")


def prefilter(neighbors, side):
    eligible = sorted(v for v in side if side[v] and v != U)
    zero = set(neighbors[Z])
    pairs = []
    for c in range(18, 10, -1):
        k = 19 - c
        size_sets = list(combinations(eligible, k))
        fixed_sets = [vertices for vertices in size_sets if "s:2" in vertices]
        for a in range(2, 9):
            candidate(a, c)
            excess_sets = [vertices for vertices in fixed_sets if sum(len(neighbors[v]) - 1 for v in vertices) == a]
            slots = sorted(set(range(9, c - a)) - {10})
            passed = [list(vertices) for vertices in excess_sets if len(zero - set(vertices)) <= len(slots)]
            if not excess_sets:
                reason = "no size-k subset containing s:2 has the required excess degree"
            elif not passed:
                reason = "all size-and-excess subsets lack slots for unselected Z neighbors"
            else:
                reason = None
            pairs.append({"a": a, "c": c, "k": k, "subsets_of_size_k": len(size_sets),
                          "subsets_with_s2": len(fixed_sets), "subsets_with_required_excess": len(excess_sets),
                          "slots_for_unselected_zero_neighbors": slots, "subsets": passed, "exclusion": reason})
    return pairs


class LimitReached(Exception):
    pass


class Budget:
    def __init__(self, nodes, seconds):
        self.max_nodes = nodes
        self.max_seconds = seconds
        self.start = time.monotonic()
        self.nodes = 0

    def elapsed(self):
        return time.monotonic() - self.start

    def poll(self):
        if self.elapsed() >= self.max_seconds:
            raise LimitReached("global_time_cap")

    def visit(self):
        self.poll()
        if self.nodes >= self.max_nodes:
            raise LimitReached("global_node_cap")
        self.nodes += 1


def find_witness(neighbors, side, a, c, subsets, budget, record_subset):
    """Try each surviving named subset and return the first complete assignment."""
    candidate(a, c)
    split = c - a

    def edge_weight(v, value, u, other):
        high_label, low_label = (value, other) if side[v] else (other, value)
        d = high_label - low_label
        if 1 <= d <= 18 and (high_label >= c) == (d >= split):
            return d
        return None

    def search(domains, labels, used_labels, used_weights):
        budget.poll()
        if len(labels) == len(neighbors):
            # Every original edge was closed once, when its second end was
            # assigned. Thus injectivity already implies both full alphabets.
            return dict(labels)

        best = None
        for v, values in domains.items():
            if v in labels:
                continue
            assigned = [u for u in neighbors[v] if u in labels]
            choices = []
            for value in values:
                if value in used_labels:
                    continue
                new_weights = []
                for u in assigned:
                    d = edge_weight(v, value, u, labels[u])
                    if d is None or d in used_weights or d in new_weights:
                        break
                    new_weights.append(d)
                else:
                    choices.append((value, new_weights))
            if not choices:
                return None
            rank = (len(choices), -len(assigned), -len(neighbors[v]), v)
            if best is None or rank < best[0]:
                best = (rank, v, choices)

        _, vertex, choices = best
        for value, new_weights in choices:
            budget.visit()
            labels[vertex] = value
            used_labels.add(value)
            used_weights.update(new_weights)
            found = search(domains, labels, used_labels, used_weights)
            if found is not None:
                return found
            used_weights.difference_update(new_weights)
            used_labels.remove(value)
            del labels[vertex]
        return None

    for vertices in subsets:
        budget.poll()
        record_subset("STARTED", vertices)
        selected = set(vertices)
        domains = {}
        for v in sorted(side):
            if side[v]:
                domains[v] = range(c, 19) if v in selected else range(9, c)
            else:
                domains[v] = range(9)
        labels = {Z: 0, U: 10, H: a}
        if any(label not in domains[v] for v, label in labels.items()) or len(set(labels.values())) != len(labels):
            raise ValueError("declared pins conflict with eligible subset")
        pinned_edges = [(u, v) for u in labels for v in neighbors[u] if v in labels and u < v]
        initial_weights = [edge_weight(u, labels[u], v, labels[v]) for u, v in pinned_edges]
        if None in initial_weights or len(set(initial_weights)) != len(initial_weights):
            record_subset("EXHAUSTED", vertices)
            continue
        found = search(domains, labels, set(labels.values()), set(initial_weights))
        if found is not None:
            record_subset("CANDIDATE", vertices)
            return found
        record_subset("EXHAUSTED", vertices)
    return None
