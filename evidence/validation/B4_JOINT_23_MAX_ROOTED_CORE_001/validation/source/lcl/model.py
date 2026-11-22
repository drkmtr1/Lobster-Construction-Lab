"""Named lobster profiles, exact graph identity, and elementary validation.

Profiles preserve branch order and trailing empty sections.  Graph digests bind
physical vertices and incidences; they are not isomorphism-class identifiers.
"""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path
from typing import Any


def _integer(value: Any, name: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum} (booleans are not integers here)")
    return value


def normalize_profile(profile: Any) -> list[list[int]]:
    """Validate and copy the supplied representation without quotienting it."""
    if not isinstance(profile, list) or not profile:
        raise ValueError("profile must be a nonempty list of section lists")
    result = []
    for i, section in enumerate(profile):
        if not isinstance(section, list):
            raise ValueError(f"profile section {i} must be a list")
        result.append([_integer(q, f"profile[{i}][{j}]") for j, q in enumerate(section)])
    return result


def build_graph(profile: list[list[int]]) -> dict:
    """Expand the exact named original graph, with one vertex per specified role."""
    profile = normalize_profile(profile)
    spine = [f"s:{i}" for i in range(len(profile))]
    vertices: list[str] = []
    edges = [[spine[i], spine[i + 1]] for i in range(len(spine) - 1)]
    roles: dict[str, dict] = {}
    # Section order keeps a narrow live-parent frontier for the reference DP.
    for i, section in enumerate(profile):
        vertices.append(spine[i])
        roles[spine[i]] = {"kind": "spine", "section": i}
        for j, q in enumerate(section):
            branch = f"b:{i}:{j}"
            vertices.append(branch)
            roles[branch] = {"kind": "branch", "section": i, "branch": j}
            edges.append([spine[i], branch])
            for k in range(q):
                leaf = f"l:{i}:{j}:{k}"
                vertices.append(leaf)
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
                edges.append([branch, leaf])
    return {"schema_version": 1, "profile": profile, "vertices": vertices,
            "edges": edges, "spine": spine, "roles": roles}


def graph_digest(graph: dict) -> str:
    """Digest original graph data, independent of vertex and edge listing order."""
    payload = {"vertices": sorted(graph["vertices"]),
               "edges": sorted([sorted([u, v]) for u, v in graph["edges"]])}
    for key in ("profile", "spine", "roles"):
        if key in graph:
            payload[key] = graph[key]
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _path_order(remaining: set[str], adjacency: dict[str, set[str]]) -> list[str]:
    if len(remaining) == 1:
        return [next(iter(remaining))]
    ends = sorted(v for v in remaining if len(adjacency[v] & remaining) <= 1)
    if not ends:
        return []
    order, previous, current = [], None, ends[0]
    while current is not None:
        order.append(current)
        following = sorted((adjacency[current] & remaining) - ({previous} if previous else set()))
        if len(following) > 1:
            return []
        previous, current = current, following[0] if following else None
    return order if len(order) == len(remaining) else []


def validate_graph(graph: Any) -> dict:
    """Check a finite simple tree and its lobster representation/witness.

    Without a supplied spine, two simultaneous leaf-pruning rounds must leave
    a path.  A last nonempty one- or two-vertex core handles small trees.
    """
    errors: list[str] = []
    if not isinstance(graph, dict):
        return {"valid": False, "errors": ["graph must be an object"], "n": 0, "m": 0}
    if "schema_version" in graph and (type(graph["schema_version"]) is not int
                                      or graph["schema_version"] != 1):
        errors.append("schema_version must be the integer 1 when supplied")
    vertices, edges = graph.get("vertices"), graph.get("edges")
    if not isinstance(vertices, list) or not vertices:
        return {"valid": False, "errors": ["vertices must be a nonempty list"], "n": 0,
                "m": len(edges) if isinstance(edges, list) else 0}
    if any(not isinstance(v, str) or not v for v in vertices):
        return {"valid": False, "errors": ["vertex IDs must be nonempty strings"],
                "n": len(vertices), "m": len(edges) if isinstance(edges, list) else 0}
    if len(set(vertices)) != len(vertices):
        errors.append("duplicate vertex IDs")
    if not isinstance(edges, list):
        return {"valid": False, "errors": errors + ["edges must be a list"], "n": len(vertices), "m": 0}
    n, m = len(vertices), len(edges)
    vertex_set = set(vertices)
    adjacency = {v: set() for v in vertices}
    edge_set: set[tuple[str, str]] = set()
    for i, edge in enumerate(edges):
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            errors.append(f"edge {i} must contain exactly two endpoints")
            continue
        u, v = edge
        if not isinstance(u, str) or not isinstance(v, str) or u not in vertex_set or v not in vertex_set:
            errors.append(f"edge {i} has an unknown/non-string endpoint")
            continue
        if u == v:
            errors.append(f"edge {i} is a self-loop")
            continue
        key = tuple(sorted((u, v)))
        if key in edge_set:
            errors.append(f"edge {i} duplicates an undirected edge")
        edge_set.add(key)
        adjacency[u].add(v)
        adjacency[v].add(u)
    if m != n - 1:
        errors.append("a tree must have n-1 edges")
    seen, pending = {vertices[0]}, [vertices[0]]
    while pending:
        u = pending.pop()
        for v in adjacency[u] - seen:
            seen.add(v)
            pending.append(v)
    if seen != vertex_set:
        errors.append("graph is disconnected")
    if errors:
        return {"valid": False, "errors": errors, "n": n, "m": m}

    spine = graph.get("spine")
    if "spine" in graph:
        if (not isinstance(spine, list) or not spine
                or any(not isinstance(v, str) or v not in vertex_set for v in spine)
                or len(set(spine)) != len(spine)):
            errors.append("spine must be a nonempty simple list of existing vertex IDs")
        elif any(v not in adjacency[u] for u, v in zip(spine, spine[1:])):
            errors.append("successive supplied spine vertices are not adjacent")
    else:
        remaining = set(vertices)
        for _ in range(2):
            if len(remaining) <= 2:
                break
            leaves = {v for v in remaining if len(adjacency[v] & remaining) <= 1}
            newer = remaining - leaves
            if not newer:
                break
            remaining = newer
        if any(len(adjacency[v] & remaining) > 2 for v in remaining):
            errors.append("two leaf-pruning rounds do not leave a path: graph is not a lobster")
            spine = None
        else:
            spine = _path_order(remaining, adjacency)
            if not spine:
                errors.append("could not construct a supporting spine")
    if not errors and spine:
        distance = {v: 0 for v in spine}
        queue = deque(spine)
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v not in distance:
                    distance[v] = distance[u] + 1
                    queue.append(v)
        if max(distance.values()) > 2:
            errors.append("some vertex lies more than two edges from the supplied/inferred spine")

    if "profile" in graph:
        try:
            profile = normalize_profile(graph["profile"])
            described_size = len(profile) + sum(1 + q for section in profile for q in section)
            if described_size != n:
                raise ValueError("profile vertex count differs from the supplied graph")
            expected = build_graph(profile)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if set(expected["vertices"]) != vertex_set:
                errors.append("vertices do not match the exact profile roles")
            if {tuple(sorted(e)) for e in expected["edges"]} != edge_set:
                errors.append("edges do not match the exact profile incidences")
            if graph.get("spine") != expected["spine"]:
                errors.append("spine does not match the exact profile")
            roles = graph.get("roles")
            if (not isinstance(roles, dict) or set(roles) != set(expected["roles"])
                    or any(not isinstance(roles[v], dict)
                           or set(roles[v]) != set(role)
                           or any(type(roles[v][key]) is not type(value)
                                  or roles[v][key] != value for key, value in role.items())
                           for v, role in expected["roles"].items())):
                errors.append("roles do not match the exact profile")
    elif "roles" in graph:
        if (not isinstance(graph["roles"], dict) or set(graph["roles"]) != vertex_set
                or any(not isinstance(role, dict) for role in graph["roles"].values())):
            errors.append("explicit roles must assign a role object to every actual vertex")
    return {"valid": not errors, "errors": errors, "n": n, "m": m,
            "supporting_spine": spine if not errors else None}


def load_graph(path: str | Path) -> dict:
    """Load a profile-only input, an explicit graph, or a certificate's graph."""
    with Path(path).open(encoding="utf-8-sig") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("input JSON must be an object")
    if "graph" in value and isinstance(value["graph"], dict):
        value = value["graph"]
    if "profile" in value and "vertices" not in value and "edges" not in value:
        value = build_graph(value["profile"])
    result = validate_graph(value)
    if not result["valid"]:
        raise ValueError("invalid graph: " + "; ".join(result["errors"]))
    return value


def branched_prefix_profile(q: int, r: int, z0: int, z1: int, K: int) -> list[list[int]]:
    """B2-P1: two branched sections, then a next vertex and K path edges."""
    _integer(q, "q", 1)
    _integer(r, "r", 1)
    _integer(z0, "z0")
    _integer(z1, "z1")
    _integer(K, "K", 1)
    return [[q] + [0] * z0, [r] + [0] * z1] + [[] for _ in range(K + 1)]
