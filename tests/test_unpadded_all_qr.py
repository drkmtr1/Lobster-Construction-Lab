"""Targeted original-graph and preflight checks for B2-UNPADDED-ALL-QR-001."""

import unittest
from unittest.mock import patch

from lcl.constructors import two_section_balanced, two_section_nonadjacent
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


CASES = ((1, 1, 2), (1, 2, 2), (2, 1, 2), (1, 3, 2),
         (3, 1, 2), (2, 5, 3), (5, 2, 3), (4, 4, 3),
         (1, 1, 3), (1, 2, 6), (7, 3, 7), (3, 7, 8))


class UnpaddedAllQrTests(unittest.TestCase):
    def test_parameterized_prefix_and_full_original_certificate(self):
        for q, r, K in CASES:
            with self.subTest(q=q, r=r, K=K):
                original = build_graph([[q], [r]] + [[] for _ in range(K + 1)])
                original_digest = graph_digest(original)
                result = two_section_nonadjacent(q, r, K)
                self.assertEqual(result["graph_digest"], original_digest)
                prefix = result["trace"][0]["prefix_labels"]
                partial = verify_partial(original, prefix)
                self.assertTrue(partial["valid"], partial["errors"])
                self.assertEqual(set(prefix), set(original["vertices"]) -
                                 {f"s:{i}" for i in range(3, K + 3)})
                self.assertEqual(partial["unused_labels"], list(range(r + 2, K + r + 2)))
                self.assertEqual(partial["unused_differences"], list(range(1, K + 1)))
                self.assertEqual(partial["used_differences"], list(range(K + 1, q + r + K + 5)))
                self.assertEqual(partial["frontier"], ["s:2"])
                self.assertEqual(prefix["s:2"], K + r + 3)
                self.assertFalse(interval_boundary(original, prefix, "s:2")["valid"])
                self.assertTrue(all(result["labels"][v] == x for v, x in prefix.items()))
                certificate = verify_certificate(original, result["labels"], original_digest)
                self.assertTrue(certificate["valid"], certificate["errors"])
                self.assertTrue(result["claim_scope"]["independent_input_supply"])
                self.assertFalse(result["claim_scope"]["mathematical_novelty_claim"])

    def test_retained_p5_and_balanced_comparison(self):
        for K in (2, 3, 6):
            prefix = two_section_nonadjacent(1, 2, K)["trace"][0]["prefix_labels"]
            self.assertEqual(prefix, {"s:0": K + 6, "s:1": 1, "s:2": K + 5,
                                      "b:0:0": 0, "l:0:0:0": K + 7,
                                      "b:1:0": K + 4, "l:1:0:0": 2,
                                      "l:1:0:1": 3})
        for t in (1, 2, 4):
            new = two_section_nonadjacent(t, t, 2)["trace"][0]
            old = two_section_balanced(t, 2)["trace"][0]
            self.assertEqual(new["unused_labels"], old["unused_labels"])
            self.assertEqual(new["active_label"], old["active_label"] + 1)

    def test_domain_rejections(self):
        cases = ((0, 1, 2), (1, 0, 2), (1, 1, 1), (-1, 1, 2), (1, -1, 2),
                 (True, 1, 2), (1, True, 2), (1, 1, True),
                 (1.0, 1, 2), (1, 1.0, 2), (1, 1, 2.0))
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                two_section_nonadjacent(*args)

    def test_caller_declared_cli_target_and_limits(self):
        q, r, K = 2, 3, 2
        spec = {"method": "two_section_nonadjacent", "parameters": {"q": q, "r": r, "K": K},
                "profile": [[q], [r]] + [[] for _ in range(K + 1)]}
        original, result = construction_input(spec, max_vertices=q + r + K + 5)
        self.assertTrue(verify_certificate(original, result["labels"], graph_digest(original))["valid"])
        false_labels = dict(result["labels"])
        false_labels["s:2"] = false_labels["s:1"]
        self.assertFalse(verify_certificate(original, false_labels, graph_digest(original))["valid"])
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=q + r + K + 4)
        wrong = dict(spec, profile=[[r], [q]] + [[] for _ in range(K + 1)])
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(wrong)
        with self.assertRaises(ValueError):
            construction_input(dict(spec, parameters={"q": q, "r": r, "K": 1}))

    def test_huge_and_boolean_cli_parameters_do_not_dispatch(self):
        for params in ({"q": 10**12, "r": 1, "K": 2},
                       {"q": 1, "r": 10**12, "K": 2},
                       {"q": 1, "r": 1, "K": 10**12},
                       {"q": 1, "r": 1, "K": True},
                       {"q": 1, "r": 1, "K": 2, "extra": 0}):
            with self.subTest(params=params), patch("lcl.ingest.constructors.two_section_nonadjacent") as ctor:
                with self.assertRaises(ValueError):
                    construction_input({"method": "two_section_nonadjacent", "parameters": params,
                                        "profile": [[]]})
                ctor.assert_not_called()
        combined = {"method": "two_section_nonadjacent",
                    "parameters": {"q": 20, "r": 20, "K": 2}, "profile": [[]]}
        with patch("lcl.ingest.constructors.two_section_nonadjacent") as ctor:
            with patch("lcl.ingest.build_graph") as builder:
                with self.assertRaises(ValueError):
                    construction_input(combined, max_vertices=32)
                builder.assert_not_called()
                ctor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
