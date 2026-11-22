"""Conditional consumers of explicitly supplied original-graph states."""

from .model import _integer
from .verify import verify_certificate, verify_partial


def _nonadjacent_path_labels(K: int, ell: int) -> list[int]:
    """Return translated C_K, including its already-assigned port.

    Unroll the three-step recurrence in linear time. ``sign`` and ``shift``
    compose the reflections that enclose the current smaller instance.
    """
    bases = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3)}
    result = [ell + K + 1]
    n, sign, shift = K, 1, 0
    while n >= 5:
        result.extend(ell + shift + sign * value for value in (1, n - 1, 0))
        shift += sign * (n - 2)
        sign = -sign
        n -= 3
    result.extend(ell + shift + sign * value for value in bases[n][1:])
    return result


def complete_nonadjacent_path(graph: dict, prefix_labels: dict[str, int],
                              K: int, ell: int) -> dict[str, int]:
    """Complete an actually supplied K-edge path from physical ``s:2``.

    The caller supplies the original graph and a valid prefix. Exactly
    ``s:3`` through ``s:(K+2)`` must be unassigned, with their actual incident
    edges forming the K-edge path from ``s:2``. Unused labels must be
    ``ell..ell+K-1``, unused differences ``1..K``, and the port label
    ``ell+K+1``. Returns a new full label mapping; the prefix is not changed.

    This is a conditional consumer, not an independent prefix supplier. It
    does not change or generalize the adjacent-port ``interval_boundary``.
    """
    _integer(K, "K", 2)
    if type(ell) is not int:
        raise ValueError("ell must be an integer; bool is not accepted")
    checked = verify_partial(graph, prefix_labels)
    if not checked["valid"]:
        raise ValueError("invalid original graph or prefix: " + "; ".join(checked["errors"]))

    suffix = {f"s:{i}" for i in range(3, K + 3)}
    if set(graph["vertices"]) - set(prefix_labels) != suffix or "s:2" not in prefix_labels:
        raise ValueError("unassigned vertices must be exactly the original named path after s:2")
    expected_edges = {frozenset((f"s:{i}", f"s:{i + 1}")) for i in range(2, K + 2)}
    incident_edges = {frozenset(edge) for edge in graph["edges"] if suffix.intersection(edge)}
    if incident_edges != expected_edges:
        raise ValueError("unassigned incidences must be exactly the original K-edge path from s:2")
    if (checked["unused_labels"] != list(range(ell, ell + K))
            or checked["unused_differences"] != list(range(1, K + 1))
            or prefix_labels["s:2"] != ell + K + 1):
        raise ValueError("prefix does not supply the declared nonadjacent-port inventories")

    values = _nonadjacent_path_labels(K, ell)
    labels = dict(prefix_labels)
    labels.update({f"s:{i + 2}": values[i] for i in range(1, K + 1)})
    certificate = verify_certificate(graph, labels, checked["graph_digest"])
    if not certificate["valid"]:
        raise ArithmeticError("consumer failed original-target verification: " + "; ".join(certificate["errors"]))
    return labels
