"""Original-target checks for the fixed B2-UNPADDED-K1-001 cases."""

import unittest
from unittest.mock import patch

from lcl.constructors import two_section_k1, two_section_nonadjacent
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


CASES = ((1, 1), (1, 2), (2, 1), (1, 8), (8, 1), (2, 3),
         (3, 2), (3, 3), (4, 9), (9, 4), (17, 31), (31, 17))


def expected_edges(q, r):
    edges = [("s:0", "s:1"), ("s:1", "s:2"), ("s:2", "s:3"),
             ("s:0", "b:0:0"), ("s:1", "b:1:0")]
    edges += [("b:0:0", f"l:0:0:{j}") for j in range(q)]
    edges += [("b:1:0", f"l:1:0:{j}") for j in range(r)]
    return {tuple(sorted(edge)) for edge in edges}


class UnpaddedK1Tests(unittest.TestCase):
    def test_original_named_target_and_arithmetic(self):
        for q, r in CASES:
            with self.subTest(q=q, r=r):
                original = build_graph([[q], [r], [], []])
                expected = expected_edges(q, r)
                self.assertEqual({tuple(sorted(e)) for e in original["edges"]}, expected)
                self.assertEqual(set(original["vertices"]), {v for edge in expected for v in edge})
                result = two_section_k1(q, r)
                labels = result["labels"]
                m = q + r + 5
                self.assertEqual(result["graph_digest"], graph_digest(original))
                self.assertEqual(set(labels), set(original["vertices"]))
                named = {"s:0": 3, "s:1": q + 5, "s:2": 1, "s:3": q + 4,
                         "b:0:0": q + 3, "l:0:0:0": 2, "b:1:0": 0}
                named.update({f"l:0:0:{j}": j + 3 for j in range(1, q)})
                named.update({f"l:1:0:{j}": q + 6 + j for j in range(r)})
                self.assertEqual(labels, named)
                self.assertTrue(all(type(v) is int for v in labels.values()))
                self.assertEqual(sorted(labels.values()), list(range(m + 1)))
                differences = sorted(abs(labels[u] - labels[v]) for u, v in expected)
                self.assertEqual(differences, list(range(1, m + 1)))
                self.assertTrue(verify_certificate(original, labels, graph_digest(original))["valid"])
                prefix = result["trace"][0]["prefix_labels"]
                self.assertEqual(set(prefix), set(original["vertices"]) - {"s:3"})
                self.assertTrue(all(labels[v] == value for v, value in prefix.items()))
                partial = verify_partial(original, prefix)
                self.assertTrue(partial["valid"], partial["errors"])
                self.assertEqual(partial["unused_labels"], [q + 4])
                self.assertEqual(partial["unused_differences"], [q + 3])
                self.assertEqual(partial["frontier"], ["s:2"])
                self.assertEqual(prefix["s:2"], 1)
                self.assertEqual(labels["s:3"], q + 4)
                self.assertFalse(interval_boundary(original, prefix, "s:2")["valid"])

    def test_invalid_structural_parameters(self):
        for bad in (True, False, 0, -1, 1.0, "1", None):
            for args in ((bad, 1), (1, bad)):
                with self.subTest(args=args), self.assertRaises(ValueError):
                    two_section_k1(*args)
        with self.assertRaises(ValueError):
            two_section_nonadjacent(1, 1, 1)

    def test_cli_original_target_and_false_certificate(self):
        q, r = 2, 3
        spec = {"method": "two_section_k1", "parameters": {"q": q, "r": r},
                "profile": [[q], [r], [], []]}
        original, result = construction_input(spec, max_vertices=q + r + 6)
        self.assertTrue(verify_certificate(original, result["labels"], graph_digest(original))["valid"])
        bad = dict(result["labels"])
        bad["s:2"] = bad["s:1"]
        self.assertFalse(verify_certificate(original, bad, graph_digest(original))["valid"])
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=q + r + 5)
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(dict(spec, profile=[[r], [q], [], []]))

    def test_cli_preflight_rejects_before_dispatch_or_expansion(self):
        for params in ({"q": 10**12, "r": 1}, {"q": 1, "r": 10**12},
                       {"q": True, "r": 1}, {"q": 1, "r": 0},
                       {"q": 1, "r": 1.0}, {"q": 1, "r": 1, "K": 1},
                       {"q": 1}):
            with self.subTest(params=params), patch("lcl.ingest.constructors.two_section_k1") as ctor:
                with self.assertRaises(ValueError):
                    construction_input({"method": "two_section_k1", "parameters": params,
                                        "profile": [[]]}, max_vertices=54)
                ctor.assert_not_called()
        with patch("lcl.ingest.constructors.two_section_k1") as ctor, patch("lcl.ingest.build_graph") as builder:
            with self.assertRaises(ValueError):
                construction_input({"method": "two_section_k1", "parameters": {"q": 31, "r": 31},
                                    "profile": [[]]}, max_vertices=54)
            ctor.assert_not_called()
            builder.assert_not_called()


if __name__ == "__main__":
    unittest.main()
