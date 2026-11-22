"""Check both B4 111t contracts and exact constructor admission."""

import unittest
from unittest.mock import patch

from lcl.constructors import four_section_111t
from lcl.ingest import MAX_GRAPH_VERTICES, _parameter_size, construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


METHOD = "four_section_111t"
CASES = ((2, 1), (3, 1), (8, 1), (17, 1), (2, 2), (2, 3), (2, 4),
         (3, 5), (4, 6), (5, 7), (8, 8), (31, 32))


def spec_for(t, K):
    return {"method": METHOD, "parameters": {"t": t, "K": K},
            "profile": [[1], [1], [1], [t]] + [[] for _ in range(K + 1)]}


class B4111tTests(unittest.TestCase):
    def test_original_targets_both_prefixes_and_completion(self):
        for t, K in CASES:
            with self.subTest(t=t, K=K):
                original = build_graph(spec_for(t, K)["profile"])
                result = four_section_111t(t, K)
                self.assertEqual(result["graph"], original)
                trace = result["trace"][0]
                prefix, labels = trace["prefix_labels"], result["labels"]
                spine = original["spine"]
                missing = set(spine[5:])
                self.assertEqual(set(original["vertices"]) - set(prefix), missing)
                path = list(zip(spine[4:], spine[5:]))
                incident = [tuple(e) for e in original["edges"] if missing.intersection(e)]
                self.assertEqual(incident, path)
                leavestart = 6 if K == 1 else 5
                self.assertEqual([prefix[f"l:3:0:{j}"] for j in range(t)], list(range(leavestart, leavestart + t)))
                self.assertEqual(trace["active_vertex"], "s:4")
                port = t + K + 6
                resources = ([4], [t + 3]) if K == 1 else (list(range(t + 5, t + 5 + K)), list(range(1, K + 1)))
                partial = verify_partial(original, prefix)
                self.assertTrue(partial["valid"], partial["errors"])
                self.assertEqual(partial["frontier"], ["s:4"])
                self.assertEqual(trace["active_label"], port)
                self.assertEqual(prefix["s:4"], port)
                for name, expected in zip(("unused_labels", "unused_differences"), resources):
                    self.assertEqual(trace[name], expected)
                    self.assertEqual(partial[name], expected)
                self.assertFalse(interval_boundary(original, prefix, "s:4")["valid"])
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertEqual(sorted(labels[v] for v in missing), resources[0])
                self.assertEqual(sorted(abs(labels[u] - labels[v]) for u, v in path), resources[1])
                if K == 1:
                    p = result["claim_scope"]["alpha_low_class_size"]
                    self.assertEqual(p, t + 6)
                    self.assertTrue(all((labels[u] < p) != (labels[v] < p) for u, v in original["edges"]))
                else:
                    self.assertNotIn("alpha_low_class_size", result["claim_scope"])
                self.assertEqual(result["graph_digest"], graph_digest(original))
                self.assertTrue(verify_certificate(original, labels, graph_digest(original))["valid"])

    def test_direct_rejects_invalid_types_and_domains_before_expansion(self):
        with patch("lcl.constructors.build_graph") as builder:
            for invalid in (True, False, 0, -1, 2.0, "2", None):
                for t, K in ((invalid, 1), (2, invalid)):
                    with self.subTest(t=t, K=K), self.assertRaises(ValueError):
                        four_section_111t(t, K)
            with self.assertRaises(ValueError):
                four_section_111t(1, 1)
            builder.assert_not_called()

    def test_ingest_exact_budget_original_binding_and_false_certificate(self):
        spec = spec_for(*CASES[-1])
        retained = build_graph(spec["profile"])
        original, result = construction_input(spec, max_vertices=75)
        self.assertEqual(original, retained)
        digest = graph_digest(retained)
        self.assertTrue(verify_certificate(retained, result["labels"], digest)["valid"])
        bad = dict(result["labels"], **{"s:5": result["labels"]["s:4"]})
        self.assertFalse(verify_certificate(retained, bad, digest)["valid"])
        with self.assertRaisesRegex(ValueError, "74-vertex"):
            construction_input(spec, max_vertices=74)
        self.assertEqual(MAX_GRAPH_VERTICES, 10_000)
        self.assertEqual(_parameter_size(METHOD, {"t": 9987, "K": 1}, MAX_GRAPH_VERTICES), MAX_GRAPH_VERTICES)
        with self.assertRaisesRegex(ValueError, "10000-vertex"):
            _parameter_size(METHOD, {"t": 9988, "K": 1}, MAX_GRAPH_VERTICES)

    def test_ingest_preflight_rejects_invalid_and_same_size_profiles(self):
        spec = spec_for(2, 1)
        alternatives = ([[2], [1], [1], [1], [], []],
                        [[1, 0], [1], [1], [2], []],
                        [[1, 2], [1], [1], [], [], []],
                        [[1], [], [1], [2], [1], []])
        with patch("lcl.ingest.build_graph") as builder, patch("lcl.ingest.constructors." + METHOD) as ctor:
            for params in ({"t": 1, "K": 1}, {"t": True, "K": 1}, {"t": 2, "K": True},
                           {"t": 2, "K": 0}, {"t": 2, "K": -1}, {"t": 2.0, "K": 1},
                           {"t": 2, "K": 1, "padding": 0}, {"t": 2}, {"t": 10**12, "K": 1}):
                with self.subTest(params=params), self.assertRaises(ValueError):
                    construction_input(dict(spec, parameters=params))
            for profile in alternatives:
                with self.subTest(profile=profile):
                    self.assertEqual(len(profile) + sum(size + 1 for section in profile for size in section), 15)
                    with self.assertRaisesRegex(ValueError, "requires three unit branches"):
                        construction_input(dict(spec, profile=profile))
            ctor.assert_not_called()
            builder.assert_not_called()
