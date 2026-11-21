"""Check parity seeds, original paths and admission for the declared B3 cases."""

import unittest
from unittest.mock import patch

from lcl.constructors import three_section_qltr_large_t
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


CASES = ((1, 3, 3, 2), (1, 3, 3, 3), (1, 3, 3, 4), (1, 4, 3, 5),
         (1, 7, 8, 6), (2, 3, 4, 2), (2, 6, 7, 7), (3, 4, 5, 3),
         (3, 8, 9, 8), (4, 5, 6, 4), (5, 6, 7, 11), (8, 13, 12, 14))
METHOD = "three_section_qltr_large_t"


def spec_for(q, r, t, K):
    return {"method": METHOD, "parameters": {"q": q, "r": r, "t": t, "K": K},
            "profile": [[q], [r], [t]] + [[] for _ in range(K + 1)]}


class B3LargeThirdBranchTests(unittest.TestCase):
    def test_seed_and_completion_on_declared_original_targets(self):
        for q, r, t, K in CASES:
            with self.subTest(q=q, r=r, t=t, K=K):
                original = build_graph(spec_for(q, r, t, K)["profile"])
                digest = graph_digest(original)
                result = three_section_qltr_large_t(q, r, t, K)
                self.assertEqual(result["graph"], original)
                self.assertEqual(result["graph_digest"], digest)
                trace = result["trace"][0]
                seed, prefix = trace["seed_labels"], trace["prefix_labels"]
                a, M, H = q + t + 3, q + r + t + 6, q % 2
                self.assertEqual(seed["s:1"], a + 2 * H + 4)
                self.assertEqual([seed[f"l:1:0:{j}"] for j in range(r)],
                                 [x for x in range(a + 3, M + 1) if x != seed["s:1"]])
                self.assertEqual(sorted(seed.values()), list(range(M + 1)))
                tail = [f"s:{i}" for i in range(3, K + 4)]
                remaining = set(tail[1:])
                self.assertEqual(set(original["vertices"]) - set(seed), remaining)
                self.assertEqual(set(seed), set(prefix))
                edges = [(u, v) for u, v in original["edges"] if u in seed and v in seed]
                self.assertEqual(sorted(abs(seed[u] - seed[v]) for u, v in edges),
                                 list(range(1, M + 1)))
                self.assertTrue(all((seed[u] < a) != (seed[v] < a) for u, v in edges))
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
            for invalid in (True, False, 0, -1, 1.0, "1", None):
                for index in range(4):
                    args = list(CASES[0])
                    args[index] = invalid
                    with self.subTest(args=args), self.assertRaises(ValueError):
                        three_section_qltr_large_t(*args)
            for args in ((1, 2, 3, 2), (1, 3, 3, 1), (1, 3, 2, 2), (3, 3, 5, 2), (4, 3, 6, 2)):
                with self.subTest(args=args), self.assertRaises(ValueError):
                    three_section_qltr_large_t(*args)
            builder.assert_not_called()

    def test_cli_target_binding_and_exact_vertex_limit(self):
        spec = spec_for(*CASES[-1])
        original, result = construction_input(spec, max_vertices=54)
        digest = graph_digest(original)
        self.assertTrue(verify_certificate(original, result["labels"], digest)["valid"])
        bad = dict(result["labels"])
        bad["s:4"] = bad["s:3"]
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(dict(spec, profile=[[13], [8], [12]] + [[] for _ in range(15)]))
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=53)

    def test_cli_preflight_rejects_before_expansion_and_dispatch(self):
        base = spec_for(*CASES[0])["parameters"]
        invalid = [dict(base, **{key: value}) for key in base for value in (0, True, 1.0)]
        invalid.extend((dict(base, r=2), dict(base, K=1), dict(base, q=3, t=5),
                        dict(base, t=2), dict(base, r=10**12), dict(base, K=48),
                        dict(base, extra=0), {"q": 1, "r": 3, "t": 3}))
        with patch("lcl.ingest.build_graph") as builder:
            for params in invalid:
                with self.subTest(params=params), patch("lcl.ingest.constructors." + METHOD) as ctor:
                    with self.assertRaises(ValueError):
                        construction_input({"method": METHOD, "parameters": params,
                                            "profile": [[]]}, max_vertices=54)
                    ctor.assert_not_called()
            builder.assert_not_called()
