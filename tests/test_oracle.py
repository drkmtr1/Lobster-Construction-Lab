"""Finite named-count controls and honest interruption semantics."""

import unittest

from lcl.oracle import permutation_oracle
from lcl.verify import verify_certificate


def path_graph(n):
    vertices = [f"p{i}" for i in range(n)]
    return {"vertices": vertices, "edges": [[vertices[i], vertices[i + 1]] for i in range(n - 1)]}


class PermutationOracleTests(unittest.TestCase):
    def test_small_named_counts(self):
        for n, expected in ((1, 1), (2, 2), (4, 4), (6, 24)):
            result = permutation_oracle(path_graph(n))
            self.assertEqual(result["status"], "SAT", result)
            self.assertTrue(result["exhausted"])
            self.assertEqual(result["count"], expected)
            self.assertTrue(verify_certificate(path_graph(n), result["witness"])["valid"])

    def test_corrected_six_vertex_spider_count(self):
        graph = {"vertices": ["x", "y", "u1", "u2", "v1", "v2"],
                 "edges": [["x", "y"], ["x", "u1"], ["u1", "u2"], ["x", "v1"], ["v1", "v2"]]}
        result = permutation_oracle(graph)
        self.assertEqual(result["count"], 16)
        self.assertTrue(result["exhausted"])

    def test_fixed_core_failure_not_unrestricted_failure(self):
        graph = path_graph(4)
        unrestricted = permutation_oracle(graph)
        restricted = permutation_oracle(graph, pins={"p1": 0, "p2": 3})
        self.assertEqual(unrestricted["count"], 4)
        self.assertEqual(restricted["count"], 0)
        self.assertEqual(restricted["status"], "EXHAUSTED_NO_SOLUTION")
        self.assertEqual(restricted["scope"], "restricted")
        self.assertEqual(restricted["restrictions"]["pins"], {"p1": 0, "p2": 3})

    def test_domain_restrictions(self):
        graph = path_graph(4)
        result = permutation_oracle(graph, domains={"p0": [0]})
        self.assertTrue(result["exhausted"])
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["scope"], "restricted")
        empty = permutation_oracle(graph, domains={"p0": []})
        self.assertTrue(empty["exhausted"])
        self.assertEqual(empty["count"], 0)
        conflict = permutation_oracle(graph, pins={"p0": 0}, domains={"p0": [1]})
        self.assertEqual(conflict["count"], 0)

    def test_limits_never_mean_no_solution(self):
        for kwargs in ({"max_vertices": 3}, {"max_permutations": 0}, {"max_permutations": 1}, {"time_limit": 0}):
            result = permutation_oracle(path_graph(4), **kwargs)
            self.assertEqual(result["status"], "INCOMPLETE", result)
            self.assertFalse(result["exhausted"])
            self.assertNotIn("count", result)
            self.assertIn("count_lower_bound", result)

    def test_cap_equal_to_exhaustive_size_is_exact(self):
        result = permutation_oracle(path_graph(4), max_permutations=24)
        self.assertTrue(result["exhausted"])
        self.assertEqual(result["count"], 4)

    def test_interruption_retains_witness_without_promoting_count(self):
        graph = path_graph(4)
        result = permutation_oracle(graph, max_permutations=6)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertFalse(result["exhausted"])
        self.assertNotIn("count", result)
        self.assertEqual(result["count_lower_bound"], 1)
        self.assertTrue(verify_certificate(graph, result["witness"])["valid"])

    def test_invalid_restrictions_and_limits(self):
        graph = path_graph(4)
        for kwargs in ({"pins": {"p0": True}}, {"pins": {"unknown": 0}},
                       {"pins": {"p0": 0, "p1": 0}}, {"domains": {"p0": [False]}},
                       {"max_vertices": False}, {"time_limit": float("nan")}):
            self.assertEqual(permutation_oracle(graph, **kwargs)["status"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
