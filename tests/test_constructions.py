"""Small independent witness checks for the exact retained construction domains."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from lcl.constructors import (caterpillar, h010, l007, l010, two_section_balanced,
                              two_section_padded, two_section_unit)
from lcl.model import (branched_prefix_profile, build_graph, graph_digest,
                       load_graph, normalize_profile, validate_graph)
from lcl.verify import verify_certificate, verify_partial


class ConstructionTests(unittest.TestCase):
    def assert_checked(self, result):
        report = verify_certificate(result["graph"], result["labels"], result["graph_digest"])
        self.assertTrue(report["valid"], report["errors"])
        self.assertFalse(result["claim_scope"]["universal_lobster_claim"])
        self.assertTrue(result["claim_scope"]["independent_input_supply"])

    def test_caterpillar_varied_exact_profiles(self):
        for profile in ([[]], [[], []], [[], [], [], [], []], [[0, 0, 0]],
                        [[0, 0], [], [0], []], [[], [0, 0, 0], [], [0, 0]]):
            with self.subTest(profile=profile):
                result = caterpillar(profile)
                self.assertEqual(result["graph"]["profile"], profile)
                self.assert_checked(result)

    def test_l007_small_parameter_grid(self):
        for q in range(1, 5):
            for r in range(1, 5):
                for z in range(3):
                    with self.subTest(q=q, r=r, z=z):
                        result = l007(q, r, z)
                        self.assert_checked(result)
                        self.assertFalse(result["claim_scope"]["later_suffix_supplied"])
                        self.assertEqual(len(result["graph"]["edges"]), (q + 1) * r + z + 1)

    def test_h010_documented_nine_edge_example(self):
        result = h010([1, 2], 2, [[], []])
        self.assertEqual(result["labels"], {
            "s:0": 0, "s:1": 2, "s:2": 1,
            "b:0:0": 6, "l:0:0:0": 3,
            "b:0:1": 9, "l:0:1:0": 4, "l:0:1:1": 5,
            "b:0:2": 7, "b:0:3": 8})
        self.assert_checked(result)

    def test_l010_documented_fifteen_edge_example(self):
        result = l010([1, 2], 8, [[], []])
        self.assertEqual(result["labels"]["b:0:0"], 6)
        self.assertEqual(result["labels"]["b:0:1"], 15)
        self.assertEqual(result["labels"]["l:0:1:0"], 7)
        self.assertEqual(result["labels"]["l:0:1:1"], 8)
        self.assertEqual(len(result["graph"]["edges"]), 15)
        self.assert_checked(result)

    def test_branched_constructors_consume_varied_caterpillar_suffixes(self):
        cases = [([1], 2, [[], []]), ([1, 2], 2, [[], []]),
                 ([2, 1], 3, [[0], [0]]), ([1, 1], 5, [[0, 0], [], [0]])]
        for qs, z, suffix in cases:
            for constructor, padding in ((h010, z + 10), (l010, z + 80)):
                with self.subTest(constructor=constructor.__name__, qs=qs, suffix=suffix):
                    result = constructor(qs, padding, suffix)
                    self.assert_checked(result)
                    self.assertEqual(result["graph"]["profile"], [qs + [0] * padding] + suffix)
                    prefix = result["trace"][0]
                    self.assertEqual(prefix["unused_labels"], prefix["unused_differences"])

    def test_reflection_preserves_exact_target(self):
        result = h010([1, 2], 2, [[], []])
        graph = result["graph"]
        m = len(graph["edges"])
        reflected = {v: m - label for v, label in result["labels"].items()}
        self.assertTrue(verify_certificate(graph, reflected, result["graph_digest"])["valid"])

    def test_two_section_padded_documented_recipe_boundary_example(self):
        result = two_section_padded(1, 1, 7, 2, 1)
        self.assert_checked(result)
        self.assertEqual(len(result["graph"]["edges"]), 16)
        self.assertEqual(result["labels"]["s:1"], 7)
        self.assertEqual(result["labels"]["s:2"], 5)
        self.assertEqual(result["labels"]["s:3"], 6)
        self.assertEqual(result["labels"]["b:0:0"], 16)
        self.assertEqual(result["labels"]["b:1:0"], 1)
        self.assertEqual(result["trace"][1]["unused_labels"], [6])
        self.assertEqual(result["trace"][1]["unused_differences"], [1])
        self.assertFalse(result["claim_scope"]["mathematical_novelty_claim"])

    def test_two_section_padded_varied_sizes_and_excess_padding(self):
        for q, r, K, extra1, extra0 in ((1, 1, 1, 0, 0), (5, 8, 1, 0, 0),
                                      (2, 3, 4, 0, 0), (4, 2, 3, 2, 5)):
            z1 = K + 1 + extra1
            K1 = r + z1 + K + 2
            z0 = K1 + 1 + extra0
            with self.subTest(q=q, r=r, K=K, z0=z0, z1=z1):
                result = two_section_padded(q, r, z0, z1, K)
                self.assert_checked(result)
                self.assertEqual(result["graph"]["profile"], branched_prefix_profile(q, r, z0, z1, K))
                self.assertEqual(result["trace"][1]["unused_labels"], list(range(K1 - K + 1, K1 + 1)))
                self.assertEqual(result["trace"][1]["unused_differences"], list(range(1, K + 1)))
                for interface in result["trace"][:2]:
                    partial = verify_partial(result["graph"], interface["prefix_labels"])
                    self.assertTrue(partial["valid"], partial["errors"])
                    self.assertEqual(partial["unused_labels"], interface["unused_labels"])
                    self.assertEqual(partial["unused_differences"], interface["unused_differences"])

    def test_two_section_padded_rejects_outside_its_recipe(self):
        for args in ((1, 1, 7, 1, 1), (1, 1, 6, 2, 1), (0, 1, 7, 2, 1),
                     (1, 0, 7, 2, 1), (1, 1, 7, 2, 0), (True, 1, 7, 2, 1),
                     (1, 1, 7, True, 1), (1, 1, 7.0, 2, 1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                two_section_padded(*args)

    def test_two_section_unit_formula_and_supplied_interfaces(self):
        for K in (1, 2, 3, 10, 41):
            with self.subTest(K=K):
                result = two_section_unit(K)
                self.assert_checked(result)
                self.assertEqual(result["graph"]["profile"], [[1], [1]] + [[] for _ in range(K + 1)])
                self.assertEqual(len(result["graph"]["edges"]), K + 6)
                interface = result["trace"][0]
                prefix = interface["prefix_labels"]
                self.assertEqual(prefix, {"s:0": K + 6, "b:0:0": 0, "l:0:0:0": K + 5,
                                          "s:1": 2, "b:1:0": K + 4, "l:1:0:0": 1, "s:2": K + 3})
                partial = verify_partial(result["graph"], prefix)
                self.assertTrue(partial["valid"], partial["errors"])
                self.assertEqual(partial["unused_labels"], list(range(3, K + 3)))
                self.assertEqual(partial["unused_differences"], list(range(1, K + 1)))
                self.assertEqual(interface["unused_labels"], partial["unused_labels"])
                self.assertEqual(interface["unused_differences"], partial["unused_differences"])
                self.assertFalse(result["claim_scope"]["mathematical_novelty_claim"])

    def test_two_section_unit_rejects_invalid_domain(self):
        for K in (0, -1, True, 1.0, "1", None):
            with self.subTest(K=K), self.assertRaises(ValueError):
                two_section_unit(K)

    def test_two_section_balanced_no_padding_and_independent_interface(self):
        for q in (1, 2, 5):
            for K in (1, 2, 7):
                with self.subTest(q=q, K=K):
                    result = two_section_balanced(q, K)
                    self.assert_checked(result)
                    self.assertEqual(result["graph"]["profile"], [[q], [q]] + [[] for _ in range(K + 1)])
                    self.assertEqual(len(result["graph"]["edges"]), K + 2 * q + 4)
                    interface = result["trace"][0]
                    partial = verify_partial(result["graph"], interface["prefix_labels"])
                    self.assertTrue(partial["valid"], partial["errors"])
                    self.assertEqual(partial["unused_labels"], list(range(q + 2, K + q + 2)))
                    self.assertEqual(partial["unused_differences"], list(range(1, K + 1)))
                    self.assertEqual(interface["active_label"], K + q + 2)
                    self.assertFalse(result["claim_scope"]["unequal_branch_sizes_covered"])
                    self.assertFalse(result["claim_scope"]["mathematical_novelty_claim"])

    def test_two_section_balanced_rejects_invalid_domain(self):
        for q, K in ((0, 1), (1, 0), (-1, 2), (2, -1), (True, 1), (1, True),
                     (1.0, 1), (1, 1.0), (None, 1), (1, "1")):
            with self.subTest(q=q, K=K), self.assertRaises(ValueError):
                two_section_balanced(q, K)

    def test_domains_are_explicit(self):
        invalid = [lambda: caterpillar([[1]]), lambda: l007(True, 1),
                   lambda: l007(1, 0), lambda: l007(1, 1, -1),
                   lambda: h010([], 5, [[], []]), lambda: h010([1], True, [[], []]),
                   lambda: h010([True], 5, [[], []]), lambda: h010([1], 5, [[]]),
                   lambda: h010([1], 5, [[1]]), lambda: h010([4], 20, [[], []]),
                   lambda: h010([1, 2], 1, [[], []]), lambda: l010([1, 2], 7, [[], []])]
        for function in invalid:
            with self.subTest(function=function):
                with self.assertRaises(ValueError):
                    function()


class ModelTests(unittest.TestCase):
    def test_profile_identity_and_trailing_sections(self):
        profile = [[0, 2], [], []]
        graph = build_graph(profile)
        self.assertTrue(validate_graph(graph)["valid"])
        self.assertEqual(graph["spine"], ["s:0", "s:1", "s:2"])
        self.assertEqual(graph["roles"]["b:0:0"], {"kind": "branch", "section": 0, "branch": 0})
        self.assertEqual(graph["roles"]["l:0:1:1"],
                         {"kind": "leaf", "section": 0, "branch": 1, "leaf": 1})
        profile[0].append(7)
        self.assertEqual(graph["profile"], [[0, 2], [], []])

    def test_profile_rejects_noninteger_and_nonlist_inputs(self):
        for profile in ([], None, (), [[True]], [[1.0]], [[-1]], [["1"]], [()]
                        , [[0], None]):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                normalize_profile(profile)

    def test_digest_normalizes_listing_order_but_binds_roles(self):
        graph = build_graph([[2, 0], []])
        equivalent = copy.deepcopy(graph)
        equivalent["vertices"].reverse()
        equivalent["edges"] = [list(reversed(edge)) for edge in reversed(equivalent["edges"])]
        equivalent["labels"] = {"s:0": 99}
        self.assertEqual(graph_digest(graph), graph_digest(equivalent))
        changed = copy.deepcopy(graph)
        changed["roles"]["s:0"]["section"] = False
        self.assertNotEqual(graph_digest(graph), graph_digest(changed))
        self.assertFalse(validate_graph(changed)["valid"])

    def test_exact_profile_rejects_incidences_and_roles_that_do_not_match(self):
        graph = build_graph([[1], [], []])
        changed = copy.deepcopy(graph)
        changed["edges"][-1] = ["s:0", "l:0:0:0"]
        self.assertFalse(validate_graph(changed)["valid"])
        changed = copy.deepcopy(graph)
        changed["roles"].pop("s:0")
        self.assertFalse(validate_graph(changed)["valid"])

    def test_inferred_spine_distinguishes_lobster_boundary(self):
        for length, expected in ((2, True), (3, False)):
            vertices, edges = ["c"], []
            for arm in range(3):
                previous = "c"
                for step in range(length):
                    vertex = f"a:{arm}:{step}"
                    vertices.append(vertex)
                    edges.append([previous, vertex])
                    previous = vertex
            self.assertEqual(validate_graph({"vertices": vertices, "edges": edges})["valid"], expected)
        self.assertTrue(validate_graph({"vertices": ["x"], "edges": []})["valid"])
        self.assertTrue(validate_graph({"vertices": ["x", "y"], "edges": [["x", "y"]]})["valid"])

    def test_invalid_simple_graphs_and_spines(self):
        cases = [{"vertices": ["a", "a"], "edges": [["a", "a"]]},
                 {"vertices": ["a", "b"], "edges": [["a", "x"]]},
                 {"vertices": ["a", "b", "c"], "edges": [["a", "b"], ["b", "a"]]},
                 {"vertices": ["a", "b"], "edges": []},
                 {"vertices": ["a", "b"], "edges": [["a", "b"]], "spine": None}]
        cases.extend({"vertices": ["a"], "edges": [], "schema_version": value}
                     for value in (True, 2, 1.0, "1"))
        cases.append({"vertices": ["a"], "edges": [], "roles": {"a": 3}})
        for graph in cases:
            self.assertFalse(validate_graph(graph)["valid"])

    def test_b2_p1_parameterization_preserves_target_edge_count(self):
        for q, r, z0, z1, K in ((1, 2, 0, 1, 1), (3, 1, 2, 4, 5)):
            graph = build_graph(branched_prefix_profile(q, r, z0, z1, K))
            self.assertEqual(len(graph["edges"]), q + r + z0 + z1 + K + 4)
            self.assertEqual(len(graph["spine"]), K + 3)
            self.assertTrue(validate_graph(graph)["valid"])

    def test_json_profile_shortcut_and_certificate_graph(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps({"profile": [[0], []]}), encoding="utf-8")
            graph = load_graph(path)
            path.write_text(json.dumps({"graph": graph, "labels": {}}), encoding="utf-8")
            self.assertEqual(load_graph(path), graph)


if __name__ == "__main__":
    unittest.main()
