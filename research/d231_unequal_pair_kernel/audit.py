"""Independent D231 actual-endpoint audit and host-subset exhaustion."""

from collections import Counter
from itertools import combinations

from lcl.records import digest
from research.d229_homogeneous_pair_kernel.audit import verify_named, verify_rows
from research.d229_homogeneous_pair_kernel.coverage import emit_labels
from research.d229_homogeneous_pair_kernel.model import CoreKey
from research.d229_homogeneous_pair_kernel.retained import known_core


def specification(quotas):
    """Use actual transported intervals at h=6,F=11, with no model imports."""
    n = sum(quotas)
    size = 11 + 2 * n
    carried_inputs = {i + n for i in range(11) if i not in (2, 10)}
    carried_weights = {w + n - 4 for w in range(11) if w not in (1, 10)}
    # Remove the *actual* returns before assigning residual block tags.
    vacancies_in = set(range(size)) - carried_inputs - {2, size - 1}
    vacancies_out = set(range(size)) - carried_weights - {1, size - 1}
    upper_sum = size - 4
    inputs = {
        (("L", i) if i < 11 + n - 1 else ("U", upper_sum - i)): i
        for i in sorted(vacancies_in)
    }
    weights = {
        (("L", w) if w < 11 + n - 5 else ("U", upper_sum - w)): w
        for w in sorted(vacancies_out)
    }
    demands = {}
    for k, quota in enumerate(quotas, 1):
        demands["L", k] = quota - int(k in (3, 4))
        demands["H", k] = quota
    demands["L", 7] = demands["L", 8] = 1
    return size, inputs, weights, demands


def difference(host, i, size):
    """Endpoint subtraction in the named target at h=10."""
    kind, k = host
    center = k if kind == "L" else size + 22 - k
    return abs(13 + i - center) - 10


def validate(quotas, rows, poll):
    size, inputs, weights, demands = specification(quotas)
    if type(rows) is not tuple or len(rows) != sum(demands.values()):
        raise ValueError("wrong residual row count")
    hosts = Counter()
    seen_i, seen_w = set(), set()
    full_rows = []
    for host, source, target in rows:
        poll()
        for tag, coordinate in (host, source, target):
            if type(tag) is not str or type(coordinate) is not int:
                raise ValueError("wrong coordinate or host type")
        if host not in demands or source not in inputs or target not in weights:
            raise ValueError("undeclared host or coordinate")
        if source in seen_i or target in seen_w:
            raise ValueError("repeated tagged resource")
        i, w = inputs[source], weights[target]
        if difference(host, i, size) != w:
            raise ValueError("actual endpoint does not give the claimed weight")
        hosts[host] += 1
        seen_i.add(source)
        seen_w.add(target)
        full_rows.append((host, i, w))
    if hosts != Counter(demands) or seen_i != inputs.keys() or seen_w != weights.keys():
        raise ValueError("uncovered resource or incorrect host quota")
    return full_rows


def original_profile(quotas):
    a, b, c, d = quotas
    return ((a,), (a, 1), (b, c, d, b, c, d) + (1,) * 9, (1,))


def decode_roles(roles, profile):
    result = {}
    for i, (section, quotas) in enumerate(zip(roles, profile, strict=True)):
        for a, (text, _) in enumerate(zip(section, quotas, strict=True)):
            result[f"b:{i}:{a}"] = text[0], int(text[1:])
    return result


def reverse_name(vertex):
    fields = vertex.split(":")
    fields[1] = str(3 - int(fields[1]))
    return ":".join(fields)


def reconstruct(quotas, rows, roles, poll):
    complete = validate(quotas, rows, poll)
    source_key = CoreKey(6, 0, (1, 1, 1), 2)
    source = known_core(source_key)
    verify_rows(source_key, source, poll)
    n = sum(quotas)
    size = 11 + 2 * n
    for (kind, k), (_, i), (_, w) in source:
        poll()
        if (kind, k, i, w) not in (("L", 3, 10, 10), ("L", 4, 2, 1)):
            complete.append(((kind, k + 4), i + n, w + n - 4))
    complete.extend(((("L", 4), 2, 1), (("L", 3), size - 1, size - 1)))
    if sorted(i for _, i, _ in complete) != list(range(size)):
        raise ValueError("lifted inputs do not exhaust the alphabet")
    if sorted(w for _, _, w in complete) != list(range(size)):
        raise ValueError("lifted weights do not exhaust the alphabet")
    for host, i, w in complete:
        poll()
        if difference(host, i, size) != w:
            raise ValueError("carried row or return fails endpoint audit")
    profile = original_profile(quotas)
    assignments = decode_roles(roles, profile)
    quotas_by_role = {
        assignments[f"b:{i}:{a}"]: quota for i, section in enumerate(profile)
        for a, quota in enumerate(section)
    }
    if Counter(host for host, _, _ in complete) != Counter(quotas_by_role):
        raise ValueError("physical quota and role mismatch")
    labels = emit_labels(10, complete, assignments)
    original, fold = verify_named(profile, labels, poll)
    reverse = {reverse_name(vertex): value for vertex, value in labels.items()}
    reverse_original, reverse_fold = verify_named(profile[::-1], reverse, poll)
    return {
        "profile": profile,
        "labels": labels,
        "edge_count": size + 22,
        "original_sha256": digest({"edges": original, "labels": labels}),
        "fold_sha256": digest({"edges": fold, "labels": labels}),
        "reverse_original_sha256": digest({"edges": reverse_original, "labels": reverse}),
        "reverse_fold_sha256": digest({"edges": reverse_fold, "labels": reverse}),
    }


def exhaust(quotas, budget):
    """Independently enumerate exact row subsets host by host."""
    size, inputs, weights, demands = specification(quotas)
    by_weight = {actual: tagged for tagged, actual in weights.items()}
    choices = {}
    for host, quota in demands.items():
        if quota == 0:
            continue
        valid = []
        for tagged, actual in inputs.items():
            budget.row_attempt("audit")
            weight = by_weight.get(difference(host, actual, size))
            if weight is not None:
                valid.append((host, tagged, weight))
        choices[host] = tuple(valid)
    order = tuple(sorted(choices, key=lambda host: (len(choices[host]), host)))
    selected = []

    def visit(level, used_i, used_w):
        budget.charge()
        if level == len(order):
            if len(used_i) == len(inputs) and len(used_w) == len(weights):
                return tuple(selected)
            return None
        host = order[level]
        available = tuple(
            row for row in choices[host] if row[1] not in used_i and row[2] not in used_w
        )
        for group in combinations(available, demands[host]):
            budget.charge()
            new_i = {row[1] for row in group}
            new_w = {row[2] for row in group}
            if len(new_i) != len(group) or len(new_w) != len(group):
                continue
            selected.extend(group)
            result = visit(level + 1, used_i | new_i, used_w | new_w)
            if result is not None:
                return result
            del selected[-len(group):]
        return None

    return visit(0, set(), set())
