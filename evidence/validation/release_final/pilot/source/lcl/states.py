"""Boundary descriptions and explicitly solver-derived exploratory candidates."""
from .verify import verify_partial, verify_certificate, verify_graph


def _b2_shape(graph, K=None):
    checked = verify_graph(graph)
    if not checked["valid"]:
        raise ValueError("Invalid original graph: " + "; ".join(checked["errors"]))
    profile = graph.get("profile")
    if not isinstance(profile, list) or len(profile) < 4:
        raise ValueError("B2 requires its canonical profile and K>=1 pure-path suffix")
    for section in profile[:2]:
        if not section or section[0] < 1 or any(q != 0 for q in section[1:]):
            raise ValueError("B2 requires one leading positive branch and then direct leaves per section")
    if any(section for section in profile[2:]):
        raise ValueError("B2 requires an actual pure-path suffix from s:2")
    inferred = len(profile) - 3
    if K is not None and inferred != K:
        raise ValueError("K does not match the original B2 profile")
    return inferred

def interval_boundary(graph, labels, active):
    checked = verify_partial(graph, labels)
    if not checked["valid"]:
        return {"valid": False, "errors": checked["errors"]}
    if active not in labels:
        return {"valid": False, "errors": ["Active physical vertex must be assigned"]}
    remaining = sorted(checked["unused_labels"])
    differences = sorted(checked["unused_differences"])
    k = len(remaining)
    if not remaining:
        ok = not differences
        lo = hi = None
    else:
        lo, hi = remaining[0], remaining[-1]
        ok = (remaining == list(range(lo, hi + 1))
              and differences == list(range(1, k + 1))
              and labels[active] in (lo - 1, hi + 1))
    # Every edge from assigned to unassigned must go through this physical port.
    assigned = set(labels)
    crossing = [(u, v) for u, v in graph["edges"] if (u in assigned) != (v in assigned)]
    exact_port = all((u if u in assigned else v) == active for u, v in crossing)
    return {"valid": ok and exact_port, "active_vertex": active,
            "active_label": labels[active], "unused_labels": remaining,
            "unused_differences": differences, "interval": [lo, hi],
            "remaining_edges": k, "all_unfinished_incidence_at_port": exact_port,
            "supplier_status": "not_established_by_boundary_check",
            "errors": [] if ok and exact_port else ["Not the declared interval/physical-port interface"]}

def b2_restrictions(graph, K, interval_start=1, side="above", root_label=None):
    """Finite search constraints, NOT a formula supplying an independent state.

    This imposes an interval label set on the path suffix, not merely a root
    pin. A graceful full solution is restricted afterward for exploratory data.
    """
    if type(K) is not int or K < 1:
        raise ValueError("K must be a positive integer")
    _b2_shape(graph, K)
    if type(interval_start) is not int:
        raise ValueError("interval_start must be an integer")
    m = len(graph["edges"])
    end = interval_start + K - 1
    if interval_start < 0 or end > m:
        raise ValueError("Return interval must lie within 0..m")
    if side not in ("above", "below"):
        raise ValueError("side must be above or below")
    boundary = end + 1 if side == "above" else interval_start - 1
    if boundary not in range(m + 1):
        raise ValueError("Boundary label lies outside 0..m")
    if "s:2" not in graph["vertices"]:
        raise ValueError("Two-section prefix requires s:2")
    suffix = [v for v in graph["vertices"] if v.startswith("s:") and int(v.split(":")[1]) > 2]
    if len(suffix) != K:
        raise ValueError("This pilot requires exactly K pure-path suffix vertices")
    labels = set(range(interval_start, end + 1))
    other = set(range(m + 1)) - labels
    domains = {v: sorted(labels if v in suffix else other) for v in graph["vertices"]}
    pins = {"s:2": boundary}
    if root_label is not None:
        if type(root_label) is not int or root_label not in range(m + 1):
            raise ValueError("root_label must be an integer in 0..m")
        pins["s:0"] = root_label
    return pins, domains

def extract_b2_candidate(graph, full_labels):
    _b2_shape(graph)
    checked = verify_certificate(graph, full_labels)
    if not checked["valid"]:
        raise ValueError("Cannot extract from an invalid full labeling: " + "; ".join(checked["errors"]))
    prefix = {v: x for v, x in full_labels.items()
              if not (v.startswith("s:") and int(v.split(":")[1]) > 2)}
    boundary = interval_boundary(graph, prefix, "s:2")
    return {"classification": "solver_derived_exploratory_prefix",
            "independent_supplier": False, "proof_status": "finite_witness_only",
            "labels": prefix, "boundary": boundary}

