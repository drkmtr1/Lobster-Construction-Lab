"""Small direct-permutation oracle, separately structured from project solvers.

Only graph ingestion is shared with the independent certificate verifier.
Assignment enumeration and edge-difference checks do not call a constructor,
solver, pruning rule, or certificate-success routine.
"""

from __future__ import annotations

import itertools
import math
import time
from typing import Any

from .verify import verify_graph


def permutation_oracle(
    graph: dict[str, Any], pins: dict[str, int] | None = None,
    max_vertices: int = 8, max_permutations: int = 100_000,
    time_limit: float = 5.0, domains: dict[str, list[int]] | None = None,
) -> dict[str, Any]:
    """Count named graceful bijections by direct enumeration, within caps.

    Counts include graph automorphisms and label complementation. Pins/domains
    restrict the declared assignment problem explicitly. An interrupted count
    is only a lower bound; no zero-solution conclusion follows from a limit.
    Time limits are cooperative checks between permutations, not OS isolation.
    """
    started = time.monotonic()
    report = verify_graph(graph)
    errors = list(report["errors"])
    if type(max_vertices) is not int or max_vertices < 1:
        errors.append("max_vertices must be a positive integer")
    if type(max_permutations) is not int or max_permutations < 0:
        errors.append("max_permutations must be a nonnegative integer")
    if isinstance(time_limit, bool) or not isinstance(time_limit, (int, float)) or not math.isfinite(time_limit) or time_limit < 0:
        errors.append("time_limit must be a finite nonnegative number")
    if pins is None:
        pins = {}
    if domains is None:
        domains = {}
    if not isinstance(pins, dict):
        errors.append("pins must be an object")
        pins = {}
    if not isinstance(domains, dict):
        errors.append("domains must be an object")
        domains = {}
    vertices = graph.get("vertices", []) if isinstance(graph, dict) else []
    valid_vertices = set(v for v in vertices if isinstance(v, str)) if isinstance(vertices, list) else set()
    m = report["m"]
    clean_domains: dict[str, list[int]] = {}
    for vertex, value in pins.items():
        if vertex not in valid_vertices:
            errors.append(f"pin references unknown vertex {vertex!r}")
        if type(value) is not int or not 0 <= value <= m:
            errors.append(f"pin at {vertex!r} must be an integer in 0..m")
    pin_values = [value for value in pins.values() if type(value) is int]
    if len(pin_values) != len(set(pin_values)):
        errors.append("pinned labels repeat")
    for vertex, allowed in domains.items():
        if vertex not in valid_vertices:
            errors.append(f"domain references unknown vertex {vertex!r}")
        if not isinstance(allowed, (list, tuple, set, frozenset)):
            errors.append(f"domain at {vertex!r} must be a finite collection")
        elif any(type(x) is not int or not 0 <= x <= m for x in allowed):
            errors.append(f"domain at {vertex!r} must contain only integers in 0..m")
        else:
            clean_domains[vertex] = sorted(set(allowed))
    restrictions = {
        "pins": dict(pins), "domains": clean_domains, "symmetry_reduction": None,
        "alpha_required": False, "count_convention": "named bijections; no symmetry quotient",
    }
    limits = {"max_vertices": max_vertices, "max_permutations": max_permutations,
              "time_limit": time_limit, "enforcement": "cooperative between permutations"}
    base: dict[str, Any] = {
        "method": "direct_permutation_oracle", "graph_digest": report["graph_digest"],
        "scope": "restricted" if pins or domains else "unrestricted",
        "restrictions": restrictions, "limits": limits,
        "proof_status": "finite computation; not a formal negative certificate",
    }
    if errors:
        return {**base, "status": "INVALID_INPUT", "errors": errors, "exhausted": False,
                "witness": None, "attempted_permutations": 0,
                "elapsed_seconds": time.monotonic() - started}
    if len(vertices) > max_vertices:
        return {**base, "status": "INCOMPLETE", "reason": "MAX_VERTICES", "exhausted": False,
                "count_lower_bound": 0, "witness": None, "attempted_permutations": 0,
                "elapsed_seconds": time.monotonic() - started}
    allowed_sets = {v: set(a) for v, a in clean_domains.items()}
    impossible_domains = any(not allowed for allowed in allowed_sets.values())
    impossible_pins = any(v in allowed_sets and value not in allowed_sets[v] for v, value in pins.items())
    if impossible_domains or impossible_pins:
        return {**base, "status": "EXHAUSTED_NO_SOLUTION", "reason": "CONTRADICTORY_DOMAIN_RESTRICTIONS",
                "count": 0, "exhausted": True, "witness": None, "attempted_permutations": 0,
                "elapsed_seconds": time.monotonic() - started}
    free_vertices = [v for v in vertices if v not in pins]
    available = [x for x in range(m + 1) if x not in set(pins.values())]
    total = math.factorial(len(free_vertices))
    permutations = iter(itertools.permutations(available))
    target = set(range(1, m + 1))
    count = 0
    attempted = 0
    witness = None
    reason = "EXHAUSTED"
    deadline = started + time_limit
    while attempted < total:
        if attempted >= max_permutations:
            reason = "MAX_PERMUTATIONS"
            break
        if time.monotonic() >= deadline:
            reason = "TIME_LIMIT"
            break
        values = next(permutations)
        attempted += 1
        labels = dict(pins)
        labels.update(zip(free_vertices, values))
        if any(labels[v] not in allowed for v, allowed in allowed_sets.items()):
            continue
        differences = [abs(labels[u] - labels[v]) for u, v in graph["edges"]]
        # Recheck the entire spectrum directly: no shared solver state/pruning.
        if len(differences) == m and len(set(differences)) == m and set(differences) == target:
            count += 1
            if witness is None:
                witness = labels
    exhausted = attempted == total
    result = {
        **base, "status": ("SAT" if count else "EXHAUSTED_NO_SOLUTION") if exhausted else "INCOMPLETE",
        "exhausted": exhausted, "reason": "EXHAUSTED" if exhausted else reason,
        "witness": witness, "attempted_permutations": attempted, "permutation_domain_size": total,
        "elapsed_seconds": time.monotonic() - started,
    }
    result["count" if exhausted else "count_lower_bound"] = count
    return result
