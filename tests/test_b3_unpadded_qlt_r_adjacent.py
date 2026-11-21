"""Checks for the declared adjacent three-section cases and admission bounds."""

import unittest
from unittest.mock import patch

from lcl.constructors import three_section_qltr_adjacent
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate


CASES = ((1, 2, 1, 1), (1, 2, 2, 1), (1, 2, 1, 2), (1, 3, 2, 3),
         (2, 3, 1, 1), (2, 3, 3, 2), (2, 5, 2, 4), (3, 4, 4, 1),
         (3, 7, 2, 5), (5, 6, 6, 6), (5, 9, 3, 7), (8, 13, 9, 11))
METHOD = "three_section_qltr_adjacent"


def spec_for(q, r, t, K):
    return {"method": METHOD, "parameters": {"q": q, "r": r, "t": t, "K": K},
            "profile": [[q], [r], [t]] + [[] for _ in range(K + 1)]}


class B3AdjacentTests(unittest.TestCase):
    def test_named_prefix_and_stages_on_original_targets(self):
        for q, r, t, K in CASES:
            with self.subTest(q=q, r=r, t=t, K=K):
                original = build_graph(spec_for(q, r, t, K)["profile"])
                digest = graph_digest(original)
                result = three_section_qltr_adjacent(q, r, t, K)
                self.assertEqual(result["graph_digest"], digest)
                self.assertEqual(result["graph"], original)
                prefix = result["trace"][0]["prefix_labels"]
                a = q + t + 3
                port = a + K
                m = q + r + t + K + 6
                expected = {"s:0": t, "s:1": port + t + 2, "s:2": a - 1,
                            "s:3": port, "b:0:0": port + 2, "b:1:0": 0,
                            "b:2:0": port + 1}
                leaf_groups = ([x for x in range(1, q + 2) if x != t],
                               [x for x in range(port + 3, m + 1) if x != port + t + 2],
                               list(range(q + 2, a - 1)))
                for i, group in enumerate(leaf_groups):
                    expected.update({f"l:{i}:0:{j}": x for j, x in enumerate(group)})
                self.assertEqual(prefix, expected)
                boundary = interval_boundary(original, prefix, "s:3")
                self.assertTrue(boundary["valid"], boundary["errors"])
                self.assertEqual(boundary["unused_labels"], list(range(a, port)))
                self.assertEqual(boundary["unused_differences"], list(range(1, K + 1)))
                tail = [f"s:{i}" for i in range(3, K + 4)]
                self.assertEqual(set(original["vertices"]) - set(prefix), set(tail[1:]))
                self.assertEqual({frozenset(e) for e in original["edges"]
                                  if set(tail[1:]).intersection(e)},
                                 {frozenset(e) for e in zip(tail, tail[1:])})
                labels = result["labels"]
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertEqual([abs(labels[u] - labels[v]) for u, v in zip(tail, tail[1:])],
                                 list(range(K, 0, -1)))
                if K == 1:
                    self.assertEqual((labels["s:3"], labels["s:4"]), (a + 1, a))
                self.assertTrue(verify_certificate(original, labels, digest)["valid"])

    def test_direct_domain_rejects_invalid_parameters_before_building(self):
        with patch("lcl.constructors.build_graph") as builder:
            for invalid in (True, False, 0, -1, 1.0, "1", None):
                for index in range(4):
                    args = list(CASES[0])
                    args[index] = invalid
                    with self.subTest(args=args), self.assertRaises(ValueError):
                        three_section_qltr_adjacent(*args)
            for args in ((1, 1, 1, 1), (2, 1, 1, 1), (1, 2, 3, 1)):
                with self.subTest(args=args), self.assertRaises(ValueError):
                    three_section_qltr_adjacent(*args)
            builder.assert_not_called()

    def test_cli_target_binding_at_singleton_and_exact_limit(self):
        spec = spec_for(*CASES[1])
        original, result = construction_input(spec, max_vertices=13)
        digest = graph_digest(original)
        self.assertTrue(verify_certificate(original, result["labels"], digest)["valid"])
        bad = dict(result["labels"], **{"s:4": result["labels"]["s:3"]})
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(dict(spec, profile=[[2], [1], [2], [], []]))
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=12)

    def test_cli_preflight_rejects_before_expansion_and_dispatch(self):
        base = spec_for(*CASES[0])["parameters"]
        invalid = [dict(base, **{key: value}) for key in base
                   for value in (0, -1, True, 1.0)]
        invalid.extend((dict(base, q=2), dict(base, t=3), dict(base, r=10**12),
                        dict(base, K=40), dict(base, extra=0), {"q": 1, "r": 2, "t": 1}))
        with patch("lcl.ingest.build_graph") as builder:
            for params in invalid:
                with self.subTest(params=params), patch("lcl.ingest.constructors." + METHOD) as ctor:
                    with self.assertRaises(ValueError):
                        construction_input({"method": METHOD, "parameters": params,
                                            "profile": [[]]}, max_vertices=48)
                    ctor.assert_not_called()
            builder.assert_not_called()
