"""Optional-backend controls and safe command-line result boundaries."""

import builtins
from contextlib import redirect_stdout
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lcl import __main__ as cli
from lcl.engines import (dependency_versions, networkx_diagnostics,
                         symbolic_h010_check, z3_solve)
from lcl.oracle import permutation_oracle
from lcl.verify import verify_certificate


def path_graph(n):
    vertices = [f"p{i}" for i in range(n)]
    return {"vertices": vertices, "edges": [[vertices[i], vertices[i + 1]] for i in range(n - 1)]}


def unavailable_import(package):
    original = builtins.__import__

    def replacement(name, *args, **kwargs):
        if name == package or name.startswith(package + "."):
            raise ImportError("deliberately absent optional dependency")
        return original(name, *args, **kwargs)

    return replacement


class OptionalAdapterTests(unittest.TestCase):
    def test_versions_are_explicit_and_core_needs_no_optional_import(self):
        versions = dependency_versions()
        self.assertEqual(set(versions), {"networkx", "sympy", "mpmath", "z3-solver"})
        self.assertTrue(all(v is None or isinstance(v, str) for v in versions.values()))

    def test_missing_packages_report_unavailable(self):
        for package, call in (("z3", lambda: z3_solve(path_graph(4))),
                              ("networkx", lambda: networkx_diagnostics(path_graph(4))),
                              ("sympy", symbolic_h010_check)):
            with patch("builtins.__import__", side_effect=unavailable_import(package)):
                result = call()
            self.assertEqual(result["status"], "UNAVAILABLE", (package, result))

    @unittest.skipUnless(importlib.util.find_spec("z3"), "optional z3-solver is absent")
    def test_smt_positive_witnesses_agree_with_finite_controls(self):
        spider = {"vertices": ["h", "a", "b", "c", "d", "e"],
                  "edges": [["h", "a"], ["a", "b"], ["h", "c"], ["c", "d"], ["h", "e"]]}
        for graph, count in ((path_graph(1), 1), (path_graph(4), 4),
                             (path_graph(6), 24), (spider, 16)):
            self.assertEqual(permutation_oracle(graph)["count"], count)
            result = z3_solve(graph)
            self.assertEqual(result["status"], "SAT", result)
            self.assertFalse(result["exhausted"])
            self.assertIsNone(result["count"])
            self.assertEqual(result["count_lower_bound"], 1)
            self.assertTrue(verify_certificate(graph, result["witness"])["valid"])
            self.assertFalse(result["restrictions"]["hidden_symmetry_reduction"])

    @unittest.skipUnless(importlib.util.find_spec("z3"), "optional z3-solver is absent")
    def test_smt_restricted_unsat_does_not_change_unrestricted_target(self):
        graph = path_graph(4)
        restricted = z3_solve(graph, pins={"p1": 0, "p2": 3})
        self.assertEqual(restricted["status"], "EXHAUSTED_NO_SOLUTION")
        self.assertTrue(restricted["exhausted"])
        self.assertEqual(restricted["count"], 0)
        self.assertEqual(restricted["restrictions"]["scope"], "restricted")
        self.assertIn("no independently checked proof", restricted["negative_evidence"])
        self.assertEqual(z3_solve(graph)["status"], "SAT")
        self.assertEqual(z3_solve(graph, domains={"p0": []})["status"], "EXHAUSTED_NO_SOLUTION")

    @unittest.skipUnless(importlib.util.find_spec("z3"), "optional z3-solver is absent")
    def test_smt_limits_never_become_unsat(self):
        graph = path_graph(4)
        for limits in ({"max_nodes": 1}, {"max_vertices": 3}):
            result = z3_solve(graph, limits=limits)
            self.assertEqual(result["status"], "INCOMPLETE", result)
            self.assertFalse(result["exhausted"])
            self.assertIsNone(result["count"])
            self.assertIsNone(result["witness"])
            self.assertTrue(result["reason"])

    @unittest.skipUnless(importlib.util.find_spec("z3"), "optional z3-solver is absent")
    def test_smt_has_no_alpha_or_root_zero_requirement(self):
        graph = {"vertices": ["h", "a", "b", "c", "x", "y", "z"],
                 "edges": [["h", "a"], ["h", "b"], ["h", "c"], ["a", "x"], ["b", "y"], ["c", "z"]]}
        labels = {"h": 0, "a": 2, "b": 4, "c": 6, "x": 5, "y": 3, "z": 1}
        result = z3_solve(graph, pins=labels)
        self.assertEqual(result["status"], "SAT", result)
        self.assertEqual(result["witness"], labels)
        nonzero = z3_solve(path_graph(4), pins={"p0": 1})
        self.assertEqual(nonzero["status"], "SAT")
        self.assertEqual(nonzero["witness"]["p0"], 1)

    @unittest.skipUnless(importlib.util.find_spec("networkx"), "optional NetworkX is absent")
    def test_networkx_diagnostics_keep_actual_physical_ids(self):
        graph = path_graph(4)
        original = copy.deepcopy(graph)
        renamed = {"vertices": ["a", "b", "c", "d"],
                   "edges": [["a", "b"], ["b", "c"], ["c", "d"]]}
        result = networkx_diagnostics(graph, renamed)
        self.assertEqual(result["status"], "OK")
        self.assertTrue(result["is_tree"])
        self.assertTrue(result["isomorphic_ignoring_roles"])
        self.assertTrue(result["physical_ids_preserved"])
        self.assertEqual(set(result["degrees"]), set(graph["vertices"]))
        self.assertEqual(graph, original)

    @unittest.skipUnless(importlib.util.find_spec("sympy"), "optional SymPy is absent")
    def test_symbolic_identity_check_does_not_claim_domain_proof(self):
        result = symbolic_h010_check()
        self.assertEqual(result["status"], "OK")
        self.assertTrue(result["identities_hold"])
        self.assertEqual(result["leaf_reversal_residual"], "0")
        self.assertEqual(result["reflection_squared_difference_residual"], "0")
        self.assertIn("inequalities", result["scope"])
        self.assertIn("disjointness", result["scope"])

    def test_malformed_graphs_rejected_before_optional_solver_use(self):
        graph = path_graph(2)
        graph["schema_version"] = True
        self.assertEqual(z3_solve(graph)["status"], "INVALID_INPUT")
        self.assertEqual(networkx_diagnostics(graph)["status"], "INVALID_INPUT")


class CommandBoundaryTests(unittest.TestCase):
    def invoke(self, args):
        output = io.StringIO()
        with redirect_stdout(output):
            code = cli.main(args)
        return code, json.loads(output.getvalue())

    def test_verify_uses_separately_declared_original(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            original = directory / "original.json"
            certificate = directory / "certificate.json"
            original.write_text(json.dumps(path_graph(4)), encoding="utf-8")
            certificate.write_text(json.dumps({"p0": 0, "p1": 3, "p2": 1, "p3": 2}), encoding="utf-8")
            code, result = self.invoke(["verify", str(original), str(certificate)])
            self.assertEqual(code, 0)
            self.assertTrue(result["valid"])
            # These labels are graceful on the embedded star, not on the
            # separately declared path. Embedded graph substitution is ignored.
            certificate.write_text(json.dumps({
                "graph": {"vertices": ["p0", "p1", "p2", "p3"],
                          "edges": [["p0", "p1"], ["p0", "p2"], ["p0", "p3"]]},
                "labels": {"p0": 0, "p1": 1, "p2": 2, "p3": 3},
            }), encoding="utf-8")
            code, result = self.invoke(["verify", str(original), str(certificate)])
            self.assertEqual(code, 2)
            self.assertFalse(result["valid"])

    def test_malformed_certificate_shapes_give_structured_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            original = directory / "original.json"
            certificate = directory / "certificate.json"
            original.write_text(json.dumps(path_graph(4)), encoding="utf-8")
            for value in ([], None, {"result": []}, {"result": None}):
                certificate.write_text(json.dumps(value), encoding="utf-8")
                code, result = self.invoke(["verify", str(original), str(certificate)])
                self.assertEqual(code, 2)
                self.assertEqual(result["status"], "ERROR")

    def test_huge_profile_rejected_before_expansion(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            target = directory / "target.json"
            limits = directory / "limits.json"
            target.write_text(json.dumps({"profile": [[10**12]]}), encoding="utf-8")
            limits.write_text(json.dumps({"max_vertices": 8}), encoding="utf-8")
            # The guards ensure this regression can never actually allocate
            # the adversarial profile, even if the preflight later regresses.
            with patch("lcl.ingest.build_graph", side_effect=AssertionError("expanded huge profile")):
                code, result = self.invoke(["solve", str(target), "--limits", str(limits),
                                            "--out", str(directory / "out")])
            self.assertEqual(code, 2)
            self.assertEqual(result["status"], "ERROR")
            self.assertFalse((directory / "out").exists())


if __name__ == "__main__":
    unittest.main()
