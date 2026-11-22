"""Check the B3 singleton on the 12 declared original targets."""

import unittest
from unittest.mock import patch

from lcl.constructors import three_section_k1
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


CASES = ((1, 1, 1), (1, 1, 4), (2, 1, 1), (2, 2, 3), (3, 1, 5), (5, 3, 2),
         (1, 2, 1), (1, 2, 3), (1, 4, 7), (2, 5, 1), (3, 5, 6), (8, 13, 9))
METHOD = "three_section_k1"


def spec_for(q, r, t):
    return {"method": METHOD, "parameters": {"q": q, "r": r, "t": t},
            "profile": [[q], [r], [t], [], []]}


class B3K1Tests(unittest.TestCase):
    def test_original_targets_and_singleton_inventories(self):
        for q, r, t in CASES:
            with self.subTest(q=q, r=r, t=t):
                original = build_graph(spec_for(q, r, t)["profile"])
                digest = graph_digest(original)
                result = three_section_k1(q, r, t)
                self.assertEqual(result["graph"], original)
                self.assertEqual(result["graph_digest"], digest)
                trace = result["trace"][0]
                prefix, labels = trace["prefix_labels"], result["labels"]
                P, m = q + t + 4, q + r + t + 7
                self.assertEqual(set(original["vertices"]) - set(prefix), {"s:4"})
                self.assertEqual([frozenset(e) for e in original["edges"] if "s:4" in e],
                                 [frozenset(("s:3", "s:4"))])
                self.assertEqual(prefix["s:0"], 1)
                self.assertEqual(prefix["s:3"], P + 1)
                self.assertEqual([prefix[f"l:0:0:{j}"] for j in range(q)], list(range(2, q + 2)))
                self.assertEqual([prefix[f"l:1:0:{j}"] for j in range(r)], list(range(P + 4, m + 1)))
                self.assertEqual([prefix[f"l:2:0:{j}"] for j in range(t)], list(range(q + 4, P)))
                partial = verify_partial(original, prefix)
                self.assertTrue(partial["valid"], partial["errors"])
                self.assertEqual(trace["active_vertex"], "s:3")
                self.assertEqual(trace["active_label"], P + 1)
                self.assertEqual(partial["frontier"], ["s:3"])
                self.assertEqual(partial["unused_labels"], trace["unused_labels"])
                self.assertEqual(partial["unused_differences"], trace["unused_differences"])
                self.assertEqual(trace["unused_labels"], [q + 2])
                self.assertEqual(trace["unused_differences"], [t + 3])
                self.assertFalse(interval_boundary(original, prefix, "s:3")["valid"])
                self.assertEqual(labels["s:4"], q + 2)
                self.assertEqual(abs(labels["s:4"] - labels["s:3"]), t + 3)
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertTrue(all((labels[u] < P) != (labels[v] < P)
                                    for u, v in original["edges"]))
                self.assertTrue(verify_certificate(original, labels, digest)["valid"])

    def test_direct_domain_rejects_before_building(self):
        with patch("lcl.constructors.build_graph") as builder:
            for value in (True, False, 0, -1, 1.0, "1", None):
                for i in range(3):
                    args = [1, 1, 1]
                    args[i] = value
                    with self.subTest(args=args), self.assertRaises(ValueError):
                        three_section_k1(*args)
            builder.assert_not_called()

    def test_cli_target_binding_at_exact_vertex_limit(self):
        spec = spec_for(*CASES[-1])
        original, result = construction_input(spec, max_vertices=38)
        digest = graph_digest(original)
        self.assertTrue(verify_certificate(original, result["labels"], digest)["valid"])
        bad = dict(result["labels"])
        bad["s:4"] = bad["s:3"]
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(dict(spec, profile=[[13], [8], [9], [], []]))
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=37)

    def test_cli_preflight_rejects_before_expansion_and_dispatch(self):
        base = spec_for(*CASES[0])["parameters"]
        invalid = [dict(base, **{key: v}) for key in base for v in (0, -1, True, 1.0)]
        invalid.extend((dict(base, K=1), dict(base, q=10**12), dict(base, t=38),
                        {"q": 1, "r": 1}, {"q": 1, "t": 1}, {"r": 1, "t": 1}))
        with patch("lcl.ingest.build_graph") as builder:
            for params in invalid:
                with self.subTest(params=params), patch("lcl.ingest.constructors." + METHOD) as ctor:
                    with self.assertRaises(ValueError):
                        construction_input({"method": METHOD, "parameters": params,
                                            "profile": [[]]}, max_vertices=38)
                    ctor.assert_not_called()
            builder.assert_not_called()
