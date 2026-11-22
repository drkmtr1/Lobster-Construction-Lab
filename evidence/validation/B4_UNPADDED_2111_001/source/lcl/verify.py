"""Independent checks of original graph identity and graceful certificates.

This module deliberately imports no graph builder, constructor, search routine,
or allocation routine from the project. A caller must provide the ORIGINAL
target graph. A graph embedded only in an untrusted solver result is not an
independent specification of that target.
"""

from __future__ import annotations

from collections import deque
import hashlib
import json
import re
from typing import Any


def _profile_expected(profile: Any, actual_size: int) -> tuple[dict[str, Any] | None, list[str]]:
    """Reconstruct canonical named incidence independently of model.py."""
    errors: list[str] = []
    if not isinstance(profile, list) or not profile:
        return None, ["profile must be a nonempty list of lists"]
    for i, section in enumerate(profile):
        if not isinstance(section, list):
            errors.append(f"profile section {i} must be a list")
            continue
        for j, count in enumerate(section):
            if type(count) is not int or count < 0:
                errors.append(f"profile[{i}][{j}] must be a nonnegative integer; bool is not accepted")
    if errors:
        return None, errors
    described_size = len(profile) + sum(1 + q for section in profile for q in section)
    if described_size != actual_size:
        return None, ["profile vertex count differs from the supplied graph"]
    # Build actual named edges, rather than compare only orders or degrees.
    spine = [f"s:{i}" for i in range(len(profile))]
    vertices = list(spine)
    edges: list[list[str]] = [[spine[i - 1], spine[i]] for i in range(1, len(spine))]
    roles: dict[str, dict[str, Any]] = {
        v: {"kind": "spine", "section": i} for i, v in enumerate(spine)
    }
    for i, section in enumerate(profile):
        for j, count in enumerate(section):
            center = f"b:{i}:{j}"
            vertices.append(center)
            roles[center] = {"kind": "branch", "section": i, "branch": j}
            edges.append([spine[i], center])
            for k in range(count):
                leaf = f"l:{i}:{j}:{k}"
                vertices.append(leaf)
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
                edges.append([center, leaf])
    return {"vertices": vertices, "edges": edges, "spine": spine, "roles": roles}, []


def _digest(graph: dict[str, Any], vertices: list[str], edges: list[tuple[str, str]]) -> str:
    """Exact identity convention shared as a specification, not as code."""
    payload: dict[str, Any] = {
        "vertices": sorted(vertices),
        "edges": sorted([sorted(edge) for edge in edges]),
    }
    for key in ("profile", "spine", "roles"):
        if key in graph:
            payload[key] = graph[key]
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _check_graph(graph: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(graph, dict):
        return {"valid": False, "errors": ["graph must be an object"], "n": 0, "m": 0,
                "graph_digest": None, "vertices": [], "edges": [], "adjacency": {}}
    raw_vertices = graph.get("vertices")
    raw_edges = graph.get("edges")
    vertices: list[str] = []
    edges: list[tuple[str, str]] = []
    if not isinstance(raw_vertices, list) or not raw_vertices:
        errors.append("vertices must be a nonempty list")
    elif any(not isinstance(v, str) or not v for v in raw_vertices):
        errors.append("every vertex ID must be a nonempty string")
    elif len(set(raw_vertices)) != len(raw_vertices):
        errors.append("vertex IDs must be unique")
    else:
        vertices = list(raw_vertices)
    vertex_set = set(vertices)
    seen: set[tuple[str, str]] = set()
    if not isinstance(raw_edges, list):
        errors.append("edges must be a list")
    else:
        for index, edge in enumerate(raw_edges):
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                errors.append(f"edge {index} must contain exactly two vertex IDs")
                continue
            u, v = edge
            if not isinstance(u, str) or not isinstance(v, str):
                errors.append(f"edge {index} endpoints must be strings")
                continue
            if u not in vertex_set or v not in vertex_set:
                errors.append(f"edge {index} references an unknown vertex")
                continue
            if u == v:
                errors.append(f"edge {index} is a loop")
                continue
            key = tuple(sorted((u, v)))
            if key in seen:
                errors.append(f"edge {index} duplicates an undirected edge")
                continue
            seen.add(key)
            edges.append((u, v))
    n = len(raw_vertices) if isinstance(raw_vertices, list) else 0
    m = len(raw_edges) if isinstance(raw_edges, list) else 0
    if "schema_version" in graph and (type(graph["schema_version"]) is not int or graph["schema_version"] != 1):
        errors.append("unsupported graph schema_version")
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if vertices:
        if m != len(vertices) - 1:
            errors.append("a tree must have exactly n-1 edges")
        reached = {vertices[0]}
        pending = [vertices[0]]
        while pending:
            u = pending.pop()
            for v in adjacency[u] - reached:
                reached.add(v)
                pending.append(v)
        if reached != vertex_set:
            errors.append("graph is disconnected")
    if "profile" in graph:
        expected, profile_errors = _profile_expected(graph["profile"], len(vertices))
        errors.extend(profile_errors)
        if expected is not None:
            if vertex_set != set(expected["vertices"]):
                errors.append("actual named vertices do not match the original profile")
            expected_edges = {tuple(sorted(e)) for e in expected["edges"]}
            if seen != expected_edges or m != len(expected["edges"]):
                errors.append("actual named edges do not match the original profile")
            if graph.get("spine") != expected["spine"]:
                errors.append("declared physical spine does not match the original profile")
            actual_roles = graph.get("roles")
            role_match = isinstance(actual_roles, dict) and set(actual_roles) == set(expected["roles"])
            if role_match:
                for vertex, expected_role in expected["roles"].items():
                    actual_role = actual_roles[vertex]
                    if not isinstance(actual_role, dict) or set(actual_role) != set(expected_role):
                        role_match = False
                        break
                    if any(type(actual_role[k]) is not type(v) or actual_role[k] != v for k, v in expected_role.items()):
                        role_match = False
                        break
            if not role_match:
                errors.append("declared physical roles do not match the original profile")
    elif "roles" in graph:
        roles = graph["roles"]
        if not isinstance(roles, dict) or set(roles) != vertex_set:
            errors.append("roles must identify exactly the actual vertices")
        elif any(not isinstance(role, dict) for role in roles.values()):
            errors.append("each role must be an object")
    if "spine" in graph:
        spine = graph["spine"]
        spine_valid = (isinstance(spine, list) and bool(spine)
                       and all(isinstance(v, str) and v in vertex_set for v in spine))
        if spine_valid:
            spine_valid = len(set(spine)) == len(spine)
        if not spine_valid:
            errors.append("spine must be a nonempty simple list of actual vertices")
        elif any(spine[i + 1] not in adjacency[spine[i]] for i in range(len(spine) - 1)):
            errors.append("consecutive spine vertices must be adjacent")
        else:
            distance = {v: 0 for v in spine}
            queue = deque(spine)
            while queue:
                u = queue.popleft()
                for v in adjacency[u]:
                    if v not in distance:
                        distance[v] = distance[u] + 1
                        queue.append(v)
            if set(distance) != vertex_set or any(d > 2 for d in distance.values()):
                errors.append("some vertex is more than two edges from the declared spine")
    elif vertices:
        # For a tree, simultaneous leaf deletion twice leaves a path iff it is
        # a lobster. The empty remainder includes singleton/short-path cases.
        remaining = set(vertices)
        for _ in range(2):
            leaves = {v for v in remaining if len(adjacency[v] & remaining) <= 1}
            remaining -= leaves
        if any(len(adjacency[v] & remaining) > 2 for v in remaining):
            errors.append("tree is not a lobster: its twice-pruned core is not a path")
    digest = None
    if vertices and len(edges) == m:
        try:
            digest = _digest(graph, vertices, edges)
        except (TypeError, ValueError):
            errors.append("graph identity fields must be JSON serializable")
    return {"valid": not errors, "errors": errors, "n": n, "m": m,
            "graph_digest": digest, "vertices": vertices, "edges": edges,
            "adjacency": adjacency}


def verify_graph(graph: Any) -> dict[str, Any]:
    """Check a declared original graph independently; return JSON-safe data."""
    report = _check_graph(graph)
    return {key: report[key] for key in ("valid", "errors", "n", "m", "graph_digest")}


def _check_labels(labels: Any, vertices: list[str], m: int, complete: bool) -> tuple[dict[str, int], list[str]]:
    if not isinstance(labels, dict):
        return {}, ["labels must be an object keyed by actual vertex IDs"]
    errors: list[str] = []
    target = set(vertices)
    keys = set(labels)
    if keys - target:
        errors.append("labels contain unknown vertex IDs")
    if complete and keys != target:
        errors.append("complete certificate must label every original vertex exactly once")
    checked: dict[str, int] = {}
    for v, value in labels.items():
        if type(value) is not int:
            errors.append(f"label at {v!r} must be an integer; bool is not accepted")
        elif not 0 <= value <= m:
            errors.append(f"label at {v!r} is outside 0..m")
        elif v in target:
            checked[v] = value
    if len(set(checked.values())) != len(checked):
        errors.append("vertex labels repeat")
    if complete and len(checked) == len(vertices) and set(checked.values()) != set(range(m + 1)):
        errors.append("vertex labels do not exhaust 0..m")
    return checked, errors


def verify_certificate(graph: Any, labels: Any, expected_graph_digest: str | None = None) -> dict[str, Any]:
    """Verify exact topology, label bijection, and every original edge.

    expected_graph_digest binds this invocation to a previously retained target
    identity. This detects substituted graphs; it is not a digital signature.
    """
    inspected = _check_graph(graph)
    errors = list(inspected["errors"])
    assigned, label_errors = _check_labels(labels, inspected["vertices"], inspected["m"], True)
    errors.extend(label_errors)
    differences = [abs(assigned[u] - assigned[v]) for u, v in inspected["edges"]
                   if u in assigned and v in assigned]
    if len(differences) != inspected["m"]:
        errors.append("not every original edge has two valid labeled endpoints")
    if len(differences) != len(set(differences)):
        errors.append("edge differences repeat")
    if sorted(differences) != list(range(1, inspected["m"] + 1)):
        errors.append("edge differences are not exactly 1..m")
    if expected_graph_digest is not None:
        if not isinstance(expected_graph_digest, str) or re.fullmatch(r"[0-9a-fA-F]{64}", expected_graph_digest) is None:
            errors.append("expected_graph_digest must be a SHA256 hexadecimal string")
        elif expected_graph_digest.lower() != inspected["graph_digest"]:
            errors.append("original graph digest mismatch")
    return {"valid": not errors, "errors": errors, "n": inspected["n"], "m": inspected["m"],
            "graph_digest": inspected["graph_digest"], "edge_differences": differences,
            "claim": "finite certificate for this exact named target only"}


def verify_partial(graph: Any, labels: Any) -> dict[str, Any]:
    """Check a partial assignment without assuming any future completion."""
    inspected = _check_graph(graph)
    errors = list(inspected["errors"])
    assigned, label_errors = _check_labels(labels, inspected["vertices"], inspected["m"], False)
    errors.extend(label_errors)
    differences = [abs(assigned[u] - assigned[v]) for u, v in inspected["edges"]
                   if u in assigned and v in assigned]
    if any(not 1 <= d <= inspected["m"] for d in differences):
        errors.append("an assigned original edge has an invalid difference")
    if len(differences) != len(set(differences)):
        errors.append("assigned edge differences repeat")
    assigned_set = set(assigned)
    frontier = sorted(v for v in assigned if inspected["adjacency"][v] - assigned_set)
    return {"valid": not errors, "errors": errors, "n": inspected["n"], "m": inspected["m"],
            "graph_digest": inspected["graph_digest"], "used_labels": sorted(assigned.values()),
            "used_differences": sorted(differences),
            "unused_labels": sorted(set(range(inspected["m"] + 1)) - set(assigned.values())),
            "unused_differences": sorted(set(range(1, inspected["m"] + 1)) - set(differences)),
            "frontier": frontier, "complete": not errors and len(assigned) == inspected["n"],
            "claim": "partial assignment only; no completion or independent-supplier claim"}
