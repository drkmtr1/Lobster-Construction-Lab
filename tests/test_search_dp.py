"""Independent finite controls for exact search, DP merging, and budgets."""

import copy
from itertools import product
import unittest
from unittest.mock import patch

from lcl.budget import Limits
from lcl.dp import count_labelings
from lcl.oracle import permutation_oracle
from lcl.search import prepare_domains, solve
from lcl.verify import verify_certificate, verify_partial


def path_graph(n):
    vertices = [f"p{i}" for i in range(n)]
    return {"vertices": vertices, "edges": [[vertices[i], vertices[i + 1]] for i in range(n - 1)]}


def prufer_tree(sequence, n):
    """Test-only named tree fixtures, unrelated to solver assignment logic."""
    degree = [1] * n
    for v in sequence:
        degree[v] += 1
    edges = []
    for v in sequence:
        leaf = next(i for i in range(n) if degree[i] == 1)
        edges.append([f"v{leaf}", f"v{v}"])
        degree[leaf] -= 1
        degree[v] -= 1
    last = [i for i, d in enumerate(degree) if d == 1]
    edges.append([f"v{last[0]}", f"v{last[1]}"])
    return {"vertices": [f"v{i}" for i in range(n)], "edges": edges}


class ExactEngineTests(unittest.TestCase):
    def assert_agreement(self, graph, expected=None, pins=None, domains=None):
        oracle = permutation_oracle(graph, pins=pins, domains=domains)
        self.assertTrue(oracle["exhausted"], oracle)
        if expected is not None:
            self.assertEqual(oracle["count"], expected)
        for name, result in (
            ("dfs", solve(graph, pins=pins, domains=domains, count=True)),
            ("dp", count_labelings(graph, pins=pins, domains=domains)),
        ):
            self.assertTrue(result["exhausted"], (name, result))
            self.assertEqual(result["count"], oracle["count"], (name, graph, result, oracle))
            self.assertFalse(result["restrictions"]["hidden_symmetry_reduction"])
            if result["witness"] is not None:
                self.assertTrue(verify_certificate(graph, result["witness"])["valid"], result)
            else:
                self.assertEqual(result["status"], "EXHAUSTED_NO_SOLUTION")
        return oracle

    def test_retained_named_counts(self):
        for n, expected in ((1, 1), (2, 2), (4, 4), (6, 24)):
            self.assert_agreement(path_graph(n), expected)
        spider = {"vertices": ["h", "a", "b", "c", "d", "e"],
                  "edges": [["h", "a"], ["a", "b"], ["h", "c"], ["c", "d"], ["h", "e"]]}
        self.assert_agreement(spider, 16)

    def test_all_125_named_trees_on_five_vertices(self):
        # All five-vertex trees are lobsters. This exercises every labeled
        # topology at this order, including non-path and high-degree states.
        for sequence in product(range(5), repeat=3):
            with self.subTest(prufer=sequence):
                self.assert_agreement(prufer_tree(sequence, 5))

    def test_vertex_order_does_not_change_named_count(self):
        original = path_graph(6)
        for order in ([5, 4, 3, 2, 1, 0], [0, 2, 4, 1, 3, 5], [2, 5, 0, 4, 1, 3]):
            graph = copy.deepcopy(original)
            graph["vertices"] = [original["vertices"][i] for i in order]
            graph["edges"] = [list(reversed(edge)) for edge in reversed(graph["edges"])]
            self.assert_agreement(graph, 24)

    def test_explicit_restrictions_do_not_become_unrestricted_failure(self):
        graph = path_graph(4)
        self.assert_agreement(graph, 0, pins={"p1": 0, "p2": 3})
        self.assert_agreement(graph, 1, pins={"p0": 1})
        self.assert_agreement(graph, 2, domains={"p0": [1, 2]})
        self.assert_agreement(graph, 0, domains={"p0": []})
        self.assert_agreement(graph, 0, pins={"p0": 0}, domains={"p0": [1]})
        for result in (solve(graph, pins={"p1": 0, "p2": 3}, count=True),
                       count_labelings(graph, pins={"p1": 0, "p2": 3})):
            self.assertEqual(result["restrictions"]["scope"], "restricted")
            self.assertEqual(result["restrictions"]["pins"], {"p1": 0, "p2": 3})
        self.assert_agreement(graph, 4)

    def test_non_alpha_assignment_is_not_pruned(self):
        graph = {"vertices": ["h", "a", "b", "c", "x", "y", "z"],
                 "edges": [["h", "a"], ["h", "b"], ["h", "c"], ["a", "x"], ["b", "y"], ["c", "z"]]}
        labels = {"h": 0, "a": 2, "b": 4, "c": 6, "x": 5, "y": 3, "z": 1}
        # Bipartition values {0,1,3,5} and {2,4,6} overlap in order, so this
        # particular graceful assignment has no alpha separation threshold.
        self.assert_agreement(graph, 1, pins=labels)

    def test_each_dp_state_component_carries_future_information(self):
        graph = path_graph(6)
        pairs = (
            ("differences", (0, 2, 5), (2, 0, 5)),
            ("labels", (1, 0, 2), (1, 3, 2)),
            ("frontier", (0, 4, 1), (1, 4, 0)),
        )
        for omitted, zero, one in pairs:
            reports = []
            for prefix, expected in ((zero, 0), (one, 1)):
                pins = dict(zip(graph["vertices"][:3], prefix))
                report = verify_partial(graph, pins)
                self.assertTrue(report["valid"])
                reports.append({"labels": tuple(report["used_labels"]),
                                "differences": tuple(report["used_differences"]),
                                "frontier": prefix[-1]})
                self.assert_agreement(graph, expected, pins=pins)
            # Removing this component would merge histories with different
            # exact continuation counts, despite the other components agreeing.
            for key in reports[0]:
                if key != omitted:
                    self.assertEqual(reports[0][key], reports[1][key])
            self.assertNotEqual(reports[0][omitted], reports[1][omitted])

    def test_first_witness_is_sat_without_an_exact_count(self):
        graph = path_graph(4)
        result = solve(graph)
        self.assertEqual(result["status"], "SAT")
        self.assertFalse(result["exhausted"])
        self.assertIsNone(result["count"])
        self.assertEqual(result["count_lower_bound"], 1)
        self.assertTrue(verify_certificate(graph, result["witness"])["valid"])

    def test_limits_do_not_turn_into_exhaustive_negative_results(self):
        graph = path_graph(4)
        engines = (lambda **kw: solve(graph, count=True, **kw),
                   lambda **kw: count_labelings(graph, **kw))
        for engine in engines:
            for limits, reason in (({"max_nodes": 1}, "max_nodes"),
                                   ({"max_vertices": 3}, "max_vertices")):
                result = engine(limits=limits)
                self.assertEqual(result["status"], "INCOMPLETE", result)
                self.assertFalse(result["exhausted"])
                self.assertIsNone(result["count"])
                self.assertEqual(result["reason"], reason)
            # Deterministic cooperative-clock boundary, avoiding flaky sleeps.
            with patch("lcl.budget.monotonic", side_effect=[0.0, 2.0, 2.0]):
                timed = engine(limits={"time_limit": 1.0})
            self.assertEqual(timed["status"], "INCOMPLETE")
            self.assertEqual(timed["reason"], "time_limit")
            self.assertIsNone(timed["count"])

    def test_interrupted_counts_preserve_only_verified_lower_bounds(self):
        graph = path_graph(4)
        first = solve(graph)
        dfs = solve(graph, count=True, limits={"max_nodes": first["nodes"]})
        complete_dp = count_labelings(graph)
        dp = count_labelings(graph, limits={"max_nodes": complete_dp["nodes"] - 1})
        for result in (dfs, dp):
            self.assertEqual(result["status"], "INCOMPLETE", result)
            self.assertFalse(result["exhausted"])
            self.assertIsNone(result["count"])
            self.assertGreater(result["count_lower_bound"], 0)
            self.assertLessEqual(result["count_lower_bound"], 4)
            self.assertTrue(verify_certificate(graph, result["witness"])["valid"])

    def test_state_cap_reports_actual_partial_layer_peak(self):
        result = count_labelings(path_graph(4), limits={"max_states": 5})
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["reason"], "max_states")
        self.assertEqual(result["peak_states"], 5)
        self.assertEqual(result["completed_vertices"], 1)
        self.assertIsNone(result["count"])

    def test_limits_validate_direct_and_mapping_construction(self):
        invalid = ({"max_nodes": 0}, {"max_nodes": True}, {"max_states": -1},
                   {"max_vertices": 101}, {"time_limit": 0}, {"time_limit": True},
                   {"time_limit": float("nan")}, {"time_limit": float("inf")})
        for values in invalid:
            with self.assertRaises(ValueError):
                Limits(**values)
            with self.assertRaises(ValueError):
                Limits.from_mapping(values)
        with self.assertRaises(ValueError):
            Limits.from_mapping({"unrecognized": 1})

    def test_malformed_restrictions_rejected_at_input_boundary(self):
        graph = path_graph(4)
        for kwargs in ({"pins": {"p0": True}}, {"pins": {"unknown": 0}},
                       {"pins": 3}, {"pins": [("p0", 0)]}, {"domains": 3},
                       {"domains": {"p0": [False]}}, {"domains": {"p0": [4]}},
                       {"domains": {"p0": 2}}):
            with self.assertRaises(ValueError):
                prepare_domains(graph, **kwargs)

    def test_actual_graph_semantics_required_before_search(self):
        nonlobster = {"vertices": ["h"] + [f"a{i}:{j}" for i in range(3) for j in range(1, 4)],
                      "edges": [["h", f"a{i}:1"] for i in range(3)]
                      + [[f"a{i}:{j}", f"a{i}:{j + 1}"] for i in range(3) for j in (1, 2)]}
        malformed = [nonlobster]
        for version in (True, 2):
            graph = path_graph(2)
            graph["schema_version"] = version
            malformed.append(graph)
        graph = path_graph(2)
        graph["roles"] = {"p0": 0, "p1": {}}
        malformed.append(graph)
        graph = path_graph(7)
        graph["spine"] = ["p3"]
        malformed.append(graph)
        for graph in malformed:
            self.assertEqual(solve(graph, count=True)["status"], "INVALID_INPUT")
            self.assertEqual(count_labelings(graph)["status"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
