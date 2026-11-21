"""Check the exceptional B3 constructor against named original targets."""

import unittest
from unittest.mock import patch

from lcl.constructors import three_section_q1_r2
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


CASES = ((3, 2), (3, 3), (3, 4), (3, 5), (4, 2), (4, 6),
         (5, 3), (5, 7), (8, 4), (8, 8), (13, 11), (21, 14))
METHOD = "three_section_q1_r2"


def spec_for(t, K):
    return {"method": METHOD, "parameters": {"t": t, "K": K},
            "profile": [[1], [2], [t]] + [[] for _ in range(K + 1)]}


class B3Q1R2Tests(unittest.TestCase):
    def test_seed_and_completion_on_declared_original_targets(self):
        for t, K in CASES:
            with self.subTest(t=t, K=K):
                original = build_graph(spec_for(t, K)["profile"])
                digest = graph_digest(original)
                result = three_section_q1_r2(t, K)
                self.assertEqual(result["graph"], original)
                self.assertEqual(result["graph_digest"], digest)
                trace = result["trace"][0]
                seed, prefix = trace["seed_labels"], trace["prefix_labels"]
                a, M = t + 4, t + 9
                self.assertEqual([seed[f"l:2:0:{j}"] for j in range(t)],
                                 [2] + list(range(5, a)))
                self.assertEqual(seed["b:2:0"], a)
                self.assertEqual(seed["s:3"], a + 1)
                self.assertEqual(sorted(seed.values()), list(range(M + 1)))
                tail = [f"s:{i}" for i in range(3, K + 4)]
                remaining = set(tail[1:])
                self.assertEqual(set(original["vertices"]) - set(seed), remaining)
                self.assertEqual(set(seed), set(prefix))
                edges = [(u, v) for u, v in original["edges"] if u in seed and v in seed]
                self.assertTrue(all((seed[u] < a) != (seed[v] < a) for u, v in edges))
                self.assertEqual(sorted(abs(seed[u] - seed[v]) for u, v in edges),
                                 list(range(1, M + 1)))
                self.assertEqual(prefix, {v: x + K if x >= a else x for v, x in seed.items()})
                self.assertEqual({frozenset(e) for e in original["edges"] if remaining.intersection(e)},
                                 {frozenset(e) for e in zip(tail, tail[1:])})
                partial = verify_partial(original, prefix)
                self.assertTrue(partial["valid"], partial["errors"])
                self.assertEqual(partial["unused_labels"], list(range(a, a + K)))
                self.assertEqual(partial["unused_differences"], list(range(1, K + 1)))
                self.assertEqual(partial["frontier"], ["s:3"])
                self.assertEqual(prefix["s:3"], a + K + 1)
                self.assertFalse(interval_boundary(original, prefix, "s:3")["valid"])
                labels = result["labels"]
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertTrue(verify_certificate(original, labels, digest)["valid"])

    def test_direct_domain_rejects_before_building(self):
        with patch("lcl.constructors.build_graph") as builder:
            invalid_values = (True, False, 0, -1, 1.0, "1", None)
            cases = [(t, 2) for t in (*invalid_values, 1, 2)]
            cases.extend((3, K) for K in (*invalid_values, 1))
            for args in cases:
                with self.subTest(args=args), self.assertRaises(ValueError):
                    three_section_q1_r2(*args)
            builder.assert_not_called()

    def test_cli_target_binding_and_exact_vertex_limit(self):
        spec = spec_for(*CASES[-1])
        original, result = construction_input(spec, max_vertices=45)
        digest = graph_digest(original)
        self.assertTrue(verify_certificate(original, result["labels"], digest)["valid"])
        bad = dict(result["labels"])
        bad["s:4"] = bad["s:3"]
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        swapped = [[2], [1], [21]] + [[] for _ in range(15)]
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(dict(spec, profile=swapped))
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=44)

    def test_cli_preflight_rejects_before_expansion_and_dispatch(self):
        base = spec_for(*CASES[0])["parameters"]
        invalid = [dict(base, **{key: value}) for key in base for value in (0, True, 1.0)]
        invalid.extend((dict(base, t=1), dict(base, t=2), dict(base, K=1),
                        dict(base, q=2), dict(base, r=1), dict(base, q=1, r=2),
                        dict(base, t=10**12), dict(base, K=45), {"t": 3}, {"K": 2}))
        with patch("lcl.ingest.build_graph") as builder:
            for params in invalid:
                with self.subTest(params=params), patch("lcl.ingest.constructors." + METHOD) as ctor:
                    with self.assertRaises(ValueError):
                        construction_input({"method": METHOD, "parameters": params,
                                            "profile": [[]]}, max_vertices=45)
                    ctor.assert_not_called()
            builder.assert_not_called()
