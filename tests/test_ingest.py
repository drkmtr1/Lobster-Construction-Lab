"""Regression controls for CLI limits before expansion and constructor calls."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lcl.ingest import allocation_input, construction_input, graph_input
from lcl.model import build_graph, graph_digest


class IngestTests(unittest.TestCase):
    def read_graph(self, value, limit=10_000):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            return graph_input(path, max_vertices=limit)

    def test_huge_profile_rejected_before_any_graph_expansion(self):
        for value in ({"profile": [[10**12]]}, {"graph": {"profile": [[10**12]]}},
                      {"profile": [[0] * 101]}, {"profile": [[]] * 101}):
            with self.subTest(value_type=list(value)), patch("lcl.ingest.build_graph") as builder:
                with self.assertRaises(ValueError):
                    self.read_graph(value, limit=100)
                builder.assert_not_called()

    def test_exact_vertex_limit_and_explicit_identity_preserved(self):
        graph = build_graph([[2], []])  # Five named vertices.
        graph["annotation"] = "caller retained metadata"
        admitted = self.read_graph(graph, limit=5)
        self.assertEqual(admitted, graph)
        self.assertEqual(admitted["roles"], graph["roles"])
        self.assertEqual(graph_digest(admitted), graph_digest(graph))
        with self.assertRaises(ValueError):
            self.read_graph(graph, limit=4)
        self.assertEqual(self.read_graph({"graph": graph, "labels": {}}), graph)

    def test_graph_file_size_rejected_before_json_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "too_large.json"
            with path.open("wb") as stream:
                stream.truncate(2_000_001)
            with self.assertRaisesRegex(ValueError, "byte design limit"):
                graph_input(path)

    def test_bad_graph_types_and_conflicting_shortcut_metadata(self):
        for value in ([], {"profile": [[True]]}, {"profile": [[1.0]]},
                      {"profile": [[-1]]}, {"profile": [[]], "schema_version": True},
                      {"profile": [[]], "roles": {"s:0": {"kind": "spine", "section": False}}},
                      {"profile": [[]], "spine": ["missing"]},
                      {"vertices": ["v"], "edges": [], "roles": {"v": 3}},
                      {"graph": {"graph": {"profile": [[]]}}},
                      {"graph": {"profile": [[]]}, "profile": [[]]},
                      {"profile": [[]], "vertices": ["s:0"]}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.read_graph(value)

    def test_invalid_limits_are_rejected(self):
        for limit in (True, 0, -1, 10_001, 100.0):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                self.read_graph({"profile": [[]]}, limit=limit)

    def test_large_constructor_parameters_never_dispatch(self):
        cases = [
            ("l007", {"q": 1, "r": 10**12, "z": 0}),
            ("l007", {"q": 10**12, "r": 1}),
            ("h010", {"qs": [10**12], "z": 2, "suffix_profile": [[], []]}),
            ("l010", {"qs": [1] * 10_001, "z": 2, "suffix_profile": [[], []]}),
            ("caterpillar", {"profile": [[0] * 10_001]}),
            ("two_section_padded", {"q": 1, "r": 1, "z0": 7, "z1": 2, "K": 10**12}),
            ("two_section_unit", {"K": 10**12}),
            ("two_section_balanced", {"q": 10**12, "K": 1}),
        ]
        for method, parameters in cases:
            with self.subTest(method=method), patch(f"lcl.ingest.constructors.{method}") as constructor:
                with self.assertRaises(ValueError):
                    construction_input({"method": method, "parameters": parameters, "profile": [[]]})
                constructor.assert_not_called()

    def test_boolean_and_malformed_constructor_parameters_never_dispatch(self):
        cases = [("l007", {"q": True, "r": 1}), ("l007", {"q": 1, "r": False}),
                 ("l007", {"q": 1, "r": 1, "z": True}),
                 ("h010", {"qs": [True], "z": 2, "suffix_profile": [[], []]}),
                 ("l010", {"qs": [1], "z": 2, "suffix_profile": [[True], []]}),
                 ("caterpillar", {"profile": [[True]]}),
                 ("l007", {"q": 1, "r": 1, "extra": []}), ("l007", [1, 1]),
                 ("two_section_padded", {"q": 1, "r": 1, "z0": 7, "z1": 2, "K": True})]
        cases.append(("two_section_unit", {"K": True}))
        cases.append(("two_section_balanced", {"q": True, "K": 1}))
        for method, params in cases:
            with self.subTest(method=method), patch(f"lcl.ingest.constructors.{method}") as constructor:
                with self.assertRaises(ValueError):
                    construction_input({"method": method, "parameters": params, "profile": [[]]})
                constructor.assert_not_called()

    def test_all_implemented_constructor_dispatches_are_admitted(self):
        cases = [
            {"method": "caterpillar", "parameters": {"profile": [[0], []]}, "profile": [[0], []]},
            {"method": "l007", "parameters": {"q": 1, "r": 2}, "profile": [[1, 1], []]},
            {"method": "h010", "parameters": {"qs": [1, 2], "z": 2, "suffix_profile": [[], []]},
             "profile": [[1, 2, 0, 0], [], []]},
            {"method": "l010", "parameters": {"qs": [1], "z": 2, "suffix_profile": [[], []]},
             "profile": [[1, 0, 0], [], []]},
            {"method": "two_section_padded", "parameters": {"q": 1, "r": 1, "z0": 7, "z1": 2, "K": 1},
             "profile": [[1] + [0] * 7, [1, 0, 0], [], []]},
            {"method": "two_section_unit", "parameters": {"K": 2},
             "profile": [[1], [1], [], [], []]},
            {"method": "two_section_balanced", "parameters": {"q": 2, "K": 2},
             "profile": [[2], [2], [], [], []]},
        ]
        for spec in cases:
            with self.subTest(method=spec["method"]):
                original, result = construction_input(spec)
                self.assertEqual(original["profile"], spec["profile"])
                self.assertEqual(graph_digest(original), result["graph_digest"])

    def test_same_size_different_target_and_false_claimed_digest_rejected(self):
        spec = {"method": "caterpillar", "parameters": {"profile": [[0], []]}, "profile": [[], [0]]}
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(spec)
        spec["profile"] = [[0], []]
        graph = build_graph(spec["profile"])
        with patch("lcl.ingest.constructors.caterpillar", return_value={"graph": graph, "graph_digest": "0" * 64}):
            with self.assertRaisesRegex(ValueError, "claimed graph digest"):
                construction_input(spec)

    def test_invalid_l010_budget_rejected_before_growth_or_dispatch(self):
        spec = {"method": "l010", "parameters": {"qs": [1] * 30, "z": 0, "suffix_profile": [[], []]},
                "profile": [[1] * 30, [], []]}
        with patch("lcl.ingest.constructors.l010") as constructor:
            with self.assertRaisesRegex(ValueError, "L010 domain"):
                construction_input(spec)
            constructor.assert_not_called()

    def test_allocation_original_and_host_input_separation(self):
        graph = build_graph([[1], []])
        spec = {"graph": graph, "core_labels": {"s:0": 0}, "hosts": ["s:0"]}
        self.assertIs(allocation_input(spec), graph)
        self.assertEqual(allocation_input({"profile": [[1], []]}), graph)
        self.assertEqual(allocation_input({"graph": {"profile": [[1], []]}}), graph)
        for value in ({"profile": [[10**12]]}, {"graph": {"profile": [[10**12]]}},
                      {"profile": [[True]]}, {"profile": [[]], "graph": graph}, {}, []):
            with self.subTest(value_type=type(value).__name__), patch("lcl.ingest.build_graph") as builder:
                with self.assertRaises(ValueError):
                    allocation_input(value)
                builder.assert_not_called()


if __name__ == "__main__":
    unittest.main()
