"""Bounded CLI admission before graph expansion or formula dispatch.

The public mathematical constructors keep their stated integer domains.  These
helpers add explicit CLI resource limits before any profile replication or
vertex construction; a rejected input is not a mathematical obstruction.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import constructors
from .model import build_graph, graph_digest, validate_graph
from .records import read_json


MAX_INPUT_BYTES = 2_000_000
MAX_GRAPH_VERTICES = 10_000


def _limit(value: Any) -> int:
    if type(value) is not int or not 1 <= value <= MAX_GRAPH_VERTICES:
        raise ValueError(f"max_vertices must be an integer in 1..{MAX_GRAPH_VERTICES}; booleans are rejected")
    return value


def _integer(value: Any, name: str, minimum: int, limit: int) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}; booleans are rejected")
    if value > limit:
        raise ValueError(f"{name} exceeds the {limit}-vertex CLI design limit")
    return value


def _profile_size(profile: Any, limit: int, name: str = "profile") -> int:
    """Count independently, with no copied profile, replicated list, or graph."""
    if not isinstance(profile, list) or not profile:
        raise ValueError(f"{name} must be a nonempty list of section lists")
    if len(profile) > limit:
        raise ValueError(f"{name} exceeds the {limit}-vertex CLI design limit")
    total = len(profile)
    for i, section in enumerate(profile):
        if not isinstance(section, list):
            raise ValueError(f"{name}[{i}] must be a list")
        if len(section) > limit - total:
            raise ValueError(f"{name} exceeds the {limit}-vertex CLI design limit")
        total += len(section)
        for j, q in enumerate(section):
            q = _integer(q, f"{name}[{i}][{j}]", 0, limit)
            if q > limit - total:
                raise ValueError(f"{name} exceeds the {limit}-vertex CLI design limit")
            total += q
    return total


def _graph_value(value: Any, limit: int) -> dict:
    if not isinstance(value, dict):
        raise ValueError("graph input must be a JSON object")
    if "graph" in value:
        if any(key in value for key in ("profile", "vertices", "edges")):
            raise ValueError("ambiguous graph wrapper also declares a top-level target")
        value = value["graph"]
        if not isinstance(value, dict):
            raise ValueError("graph must be an object")
        if "graph" in value:
            raise ValueError("nested graph wrappers are not supported")
    profile_size = None
    if "profile" in value:
        profile_size = _profile_size(value["profile"], limit)
    if "vertices" not in value and "edges" not in value:
        if profile_size is None:
            raise ValueError("graph input requires a profile or explicit vertices and edges")
        graph = build_graph(value["profile"])
        # A shortcut may carry a schema/spine/role declaration.  Preserve it
        # and validate it; never silently discard conflicting identity data.
        graph.update(value)
    else:
        vertices, edges = value.get("vertices"), value.get("edges")
        if not isinstance(vertices, list) or not vertices:
            raise ValueError("explicit vertices must be a nonempty list")
        if len(vertices) > limit:
            raise ValueError(f"explicit graph exceeds the {limit}-vertex CLI design limit")
        if not isinstance(edges, list):
            raise ValueError("explicit edges must be a list")
        if len(edges) != len(vertices) - 1:
            raise ValueError("an explicit tree must have exactly n-1 edges")
        if profile_size is not None and profile_size != len(vertices):
            raise ValueError("profile vertex count differs from the supplied explicit graph")
        graph = value
    if "roles" in graph and (not isinstance(graph["roles"], dict)
                             or len(graph["roles"]) != len(graph["vertices"])):
        raise ValueError("roles must be an object with one entry per actual vertex")
    report = validate_graph(graph)
    if not report["valid"]:
        raise ValueError("invalid original graph: " + "; ".join(report["errors"]))
    return graph


def graph_input(path: str | Path, max_vertices: int = MAX_GRAPH_VERTICES) -> dict:
    """Read <=2 MB JSON, preflight its size, then build/validate its target."""
    limit = _limit(max_vertices)
    return _graph_value(read_json(path, max_bytes=MAX_INPUT_BYTES), limit)


def _parameter_size(method: str, params: Any, limit: int) -> int:
    if not isinstance(params, dict):
        raise ValueError("constructor parameters must be an object")
    required = {
        "caterpillar": {"profile"},
        "l007": {"q", "r"},
        "l010": {"qs", "z", "suffix_profile"},
        "h010": {"qs", "z", "suffix_profile"},
        "two_section_padded": {"q", "r", "z0", "z1", "K"},
    }[method]
    allowed = required | ({"z"} if method == "l007" else set())
    if not required <= set(params) or not set(params) <= allowed:
        raise ValueError(f"{method} parameter keys must include {sorted(required)} and may only use {sorted(allowed)}")
    if method == "caterpillar":
        count = _profile_size(params["profile"], limit, "parameters.profile")
    elif method == "l007":
        q = _integer(params["q"], "q", 1, limit)
        r = _integer(params["r"], "r", 1, limit)
        z = _integer(params.get("z", 0), "z", 0, limit)
        count = 2 + r * (q + 1) + z
    elif method in ("l010", "h010"):
        qs = params["qs"]
        if not isinstance(qs, list) or not qs:
            raise ValueError("qs must be a nonempty list of positive branch sizes")
        if len(qs) > limit:
            raise ValueError(f"qs exceeds the {limit}-vertex CLI design limit")
        suffix_size = _profile_size(params["suffix_profile"], limit, "suffix_profile")
        z = _integer(params["z"], "z", 0, limit)
        count = 1 + len(qs) + suffix_size + z
        if count > limit:
            raise ValueError(f"constructor target exceeds the {limit}-vertex CLI design limit")
        for i, q in enumerate(qs):
            count += _integer(q, f"qs[{i}]", 1, limit)
            if count > limit:
                raise ValueError(f"constructor target exceeds the {limit}-vertex CLI design limit")
        if method == "l010":
            # Reject an impossible budget before the exponential block
            # recurrence can accumulate oversized intermediate integers.
            K, m = suffix_size - 1, count - 1
            t = K + 2
            for q in qs:
                center = 2 * t + q - 1
                if center > m:
                    raise ValueError("outside L010 domain: declared alphabet is smaller than a required center")
                t = center + 1
    else:
        q = _integer(params["q"], "q", 1, limit)
        r = _integer(params["r"], "r", 1, limit)
        z0 = _integer(params["z0"], "z0", 0, limit)
        z1 = _integer(params["z1"], "z1", 0, limit)
        K = _integer(params["K"], "K", 1, limit)
        count = q + r + z0 + z1 + K + 5
    if count > limit:
        raise ValueError(f"constructor target exceeds the {limit}-vertex CLI design limit")
    return count


def construction_input(spec: Any, max_vertices: int = MAX_GRAPH_VERTICES) -> tuple[dict, dict]:
    """Bound declarations and parameters before invoking an implemented formula.

    Returns (independently declared original graph, constructor result).  The
    result's actual graph and claimed graph digest must agree with that target.
    File callers should first use records.read_json with its <=2 MB default.
    """
    limit = _limit(max_vertices)
    if not isinstance(spec, dict) or set(spec) != {"method", "parameters", "profile"}:
        raise ValueError("Construction JSON requires exactly method, parameters, profile")
    methods = {"caterpillar": constructors.caterpillar, "l007": constructors.l007,
               "l010": constructors.l010, "h010": constructors.h010,
               "two_section_padded": constructors.two_section_padded}
    method = spec["method"]
    if not isinstance(method, str) or method not in methods:
        raise ValueError("Unknown implemented constructor")
    declared_size = _profile_size(spec["profile"], limit)
    parameter_size = _parameter_size(method, spec["parameters"], limit)
    if parameter_size != declared_size:
        raise ValueError("constructor parameters describe a different vertex count from the declared original")
    original = _graph_value({"profile": spec["profile"]}, limit)
    result = methods[method](**spec["parameters"])
    if not isinstance(result, dict) or not isinstance(result.get("graph"), dict):
        raise ValueError("constructor returned no graph object")
    returned_graph = _graph_value(result["graph"], limit)
    actual_digest, expected_digest = graph_digest(returned_graph), graph_digest(original)
    if actual_digest != expected_digest:
        raise ValueError("Constructor returned a different target from the declared original profile")
    if result.get("graph_digest") != actual_digest:
        raise ValueError("Constructor's claimed graph digest does not match its actual target")
    return original, result


def allocation_input(spec: Any, max_vertices: int = MAX_GRAPH_VERTICES) -> dict:
    """Preflight an allocation's original target; R226 checks its core/hosts."""
    limit = _limit(max_vertices)
    if not isinstance(spec, dict):
        raise ValueError("Allocation JSON must be an object")
    if ("profile" in spec) == ("graph" in spec):
        raise ValueError("Allocation JSON requires exactly one of profile or graph")
    if "graph" in spec:
        return _graph_value(spec["graph"], limit)
    target = {key: spec[key] for key in ("profile", "schema_version", "spine", "roles") if key in spec}
    if "vertices" in spec or "edges" in spec:
        raise ValueError("Allocation explicit vertices/edges must be inside graph")
    return _graph_value(target, limit)
