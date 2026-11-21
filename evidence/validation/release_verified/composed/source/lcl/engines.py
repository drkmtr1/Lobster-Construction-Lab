"""Optional exact SMT and diagnostic adapters. Core imports need no packages."""
from importlib.metadata import version, PackageNotFoundError
from time import monotonic

from .budget import Limits
from .model import validate_graph
from .search import prepare_domains


def dependency_versions():
    found = {}
    for name in ("networkx", "sympy", "mpmath", "z3-solver"):
        try:
            found[name] = version(name)
        except PackageNotFoundError:
            found[name] = None
    return found


def z3_solve(graph, pins=None, domains=None, limits=None):
    """Exact integer encoding; a bounded UNKNOWN is never UNSAT.

    max_nodes is used as Z3's rlimit (resource units), NOT counted DFS nodes.
    Internal 512 MiB max_memory is a solver limit, not process containment.
    """
    lim = Limits.from_mapping(limits.to_dict() if isinstance(limits, Limits) else limits)
    validation = validate_graph(graph)
    if not validation["valid"]:
        return {"status": "INVALID_INPUT", "errors": validation["errors"], "method": "z3"}
    allowed, restrictions = prepare_domains(graph, pins, domains)
    base = {"method": "z3", "restrictions": restrictions, "limits": lim.to_dict(),
            "solver_memory_limit_mib": 512, "resource_unit_limit": lim.max_nodes,
            "count": None, "count_lower_bound": 0, "witness": None,
            "exhausted": False}
    try:
        import z3
    except ImportError:
        return dict(base, status="UNAVAILABLE", reason="Install requirements-smt.txt in the project venv")
    started = monotonic()
    if len(graph["vertices"]) > lim.max_vertices:
        return dict(base, status="INCOMPLETE", reason="max_vertices", elapsed_seconds=0.0)
    solver = z3.Solver()
    solver.set(timeout=max(1, int(lim.time_limit * 1000)),
               rlimit=lim.max_nodes, max_memory=512)
    m = len(graph["edges"])
    variables = {v: z3.Int(f"label_{i}") for i, v in enumerate(graph["vertices"])}
    solver.add(z3.Distinct(list(variables.values())))
    for v, x in variables.items():
        solver.add(z3.Or([x == a for a in sorted(allowed[v])]))
    differences = []
    for u, v in graph["edges"]:
        delta = variables[u] - variables[v]
        d = z3.If(delta >= 0, delta, -delta)
        differences.append(d)
        solver.add(d >= 1, d <= m)
    if differences:
        solver.add(z3.Distinct(differences))
    try:
        status = solver.check()
        if status == z3.sat:
            model = solver.model()
            base.update(status="SAT", count_lower_bound=1,
                        witness={v: model.eval(x).as_long() for v, x in variables.items()})
        elif status == z3.unsat:
            base.update(status="EXHAUSTED_NO_SOLUTION", exhausted=True, count=0,
                        negative_evidence="Z3 UNSAT on the explicit encoding; no independently checked proof object")
        else:
            base.update(status="INCOMPLETE", reason=solver.reason_unknown())
    except KeyboardInterrupt:
        base.update(status="INCOMPLETE", reason="interrupted")
    base.update(elapsed_seconds=monotonic()-started, solver_version=z3.get_version_string())
    return base


def networkx_diagnostics(graph, other=None):
    """Optional topology cross-check; isomorphism does not replace physical IDs."""
    validation = validate_graph(graph)
    if not validation["valid"]:
        return {"status": "INVALID_INPUT", "errors": validation["errors"]}
    try:
        import networkx as nx
    except ImportError:
        return {"status": "UNAVAILABLE", "reason": "Install requirements-graph.txt"}
    g = nx.Graph()
    g.add_nodes_from(graph["vertices"])
    g.add_edges_from(graph["edges"])
    result = {"status": "OK", "networkx_version": nx.__version__,
              "is_tree": nx.is_tree(g), "degrees": dict(g.degree()),
              "physical_ids_preserved": True}
    if other is not None:
        checked = validate_graph(other)
        if not checked["valid"]:
            return {"status": "INVALID_INPUT", "errors": checked["errors"]}
        h = nx.Graph()
        h.add_nodes_from(other["vertices"])
        h.add_edges_from(other["edges"])
        result["isomorphic_ignoring_roles"] = nx.is_isomorphic(g, h)
        result["warning"] = "Isomorphism is diagnostic only; never merge physical-port experiment identities"
    return result


def symbolic_h010_check():
    """Exact symbolic check of the retained leaf-interval reversal identity.

    Does not prove inequalities, collision freedom, domain coverage or novelty.
    No untrusted expression strings are parsed.
    """
    try:
        import sympy as sp
    except ImportError:
        return {"status": "UNAVAILABLE", "reason": "Install requirements-symbolic.txt"}
    t, q, j, c, x, y = sp.symbols("t q j c x y", integer=True)
    b = 2*t + q - 1
    residual = sp.expand((b - (t+j)) - (t+q-1-j))
    reflection_residual = sp.expand(((c-x)-(c-y))**2 - (x-y)**2)
    return {"status": "OK", "sympy_version": sp.__version__,
            "leaf_reversal_residual": str(residual),
            "reflection_squared_difference_residual": str(reflection_residual),
            "identities_hold": residual == 0 and reflection_residual == 0,
            "scope": "polynomial identities only; interval inequalities and resource disjointness still require proof"}
