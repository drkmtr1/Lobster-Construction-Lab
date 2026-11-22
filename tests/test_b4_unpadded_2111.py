"""Check the exact B4 2111 profile and adjacency at the original s:4."""

import unittest
from unittest.mock import patch

from lcl.constructors import four_section_2111
from lcl.ingest import MAX_GRAPH_VERTICES, _parameter_size, construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate


CASES = (1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 64)
METHOD = "four_section_2111"


def spec_for(K):
    return {"method": METHOD, "parameters": {"K": K},
            "profile": [[2], [1], [1], [1]] + [[] for _ in range(K + 1)]}


class B42111Tests(unittest.TestCase):
    def test_original_targets_prefix_and_alpha_completion(self):
        for K in CASES:
            with self.subTest(K=K):
                original = build_graph(spec_for(K)["profile"])
                digest = graph_digest(original)
                result = four_section_2111(K)
                self.assertEqual(result["graph"], original)
                self.assertEqual(result["graph_digest"], digest)
                trace = result["trace"][0]
                prefix, labels = trace["prefix_labels"], result["labels"]
                spine = [f"s:{i}" for i in range(K + 5)]
                self.assertEqual([prefix[v] for v in spine[:5]], [K + 12, 2, K + 9, 5, K + 6])
                self.assertEqual([(prefix[f"b:{i}:0"], prefix[f"l:{i}:0:0"]) for i in range(4)],
                                 [(0, K + 11), (K + 10, 1), (3, K + 8), (K + 7, 4)])
                self.assertEqual(prefix["l:0:0:1"], K + 13)
                for leaf in ("l:0:0:0", "l:0:0:1"):
                    self.assertEqual([edge for edge in original["edges"] if leaf in edge],
                                     [["b:0:0", leaf]])
                suffix = set(spine[5:])
                self.assertEqual(set(original["vertices"]) - set(prefix), suffix)
                path = list(zip(spine[4:], spine[5:]))
                self.assertEqual({frozenset(e) for e in original["edges"] if suffix.intersection(e)},
                                 {frozenset(e) for e in path})
                self.assertEqual([e for e in original["edges"] if len(suffix.intersection(e)) == 1],
                                 [["s:4", "s:5"]])
                boundary = interval_boundary(original, prefix, "s:4")
                self.assertTrue(boundary["valid"], boundary["errors"])
                self.assertEqual(trace["active_vertex"], "s:4")
                self.assertEqual(trace["active_label"], K + 6)
                self.assertEqual(trace["unused_labels"], boundary["unused_labels"])
                self.assertEqual(trace["unused_differences"], boundary["unused_differences"])
                self.assertEqual(trace["unused_labels"], list(range(6, K + 6)))
                self.assertEqual(trace["unused_differences"], list(range(1, K + 1)))
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertEqual([abs(labels[u] - labels[v]) for u, v in path], list(range(K, 0, -1)))
                self.assertEqual(len(result["trace"]), K + 1)
                p = 6 + len(spine[5::2])
                self.assertEqual(result["claim_scope"]["alpha_low_class_size"], p)
                self.assertEqual(sorted(labels[v] for v in spine[5::2]), list(range(6, p)))
                self.assertEqual(sorted(labels[v] for v in spine[6::2]), list(range(p, K + 6)))
                self.assertTrue(all((labels[u] < p) != (labels[v] < p) for u, v in original["edges"]))
                self.assertTrue(verify_certificate(original, labels, digest)["valid"])
                if K == 1:
                    self.assertEqual((labels["s:4"], labels["s:5"], p), (7, 6, 7))

    def test_direct_domain_rejects_before_building(self):
        with patch("lcl.constructors.build_graph") as builder:
            for K in (True, False, 0, -1, 1.0, "1", None):
                with self.subTest(K=K), self.assertRaises(ValueError):
                    four_section_2111(K)
            builder.assert_not_called()

    def test_cli_target_binding_at_exact_vertex_limit(self):
        spec = spec_for(CASES[-1])
        original, result = construction_input(spec, max_vertices=78)
        digest = graph_digest(original)
        self.assertTrue(verify_certificate(original, result["labels"], digest)["valid"])
        bad = dict(result["labels"])
        bad["s:5"] = bad["s:4"]
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        with self.assertRaisesRegex(ValueError, "77-vertex"):
            construction_input(spec, max_vertices=77)
        self.assertEqual(MAX_GRAPH_VERTICES, 10_000)
        self.assertEqual(_parameter_size(METHOD, {"K": 9986}, MAX_GRAPH_VERTICES), 10_000)
        with self.assertRaisesRegex(ValueError, "10000-vertex"):
            _parameter_size(METHOD, {"K": 9987}, MAX_GRAPH_VERTICES)

    def test_cli_preflight_rejects_parameter_and_same_size_profile_changes(self):
        spec = spec_for(1)
        alternatives = ([[1], [2], [1], [1], [], []],
                        [[1], [1], [2], [1], [], []],
                        [[1], [1], [1], [2], [], []],
                        [[1, 0], [1], [2], [1], []],
                        [[1, 1], [1], [2], [], [], []],
                        [[1], [], [1], [2], [1], []])
        with patch("lcl.ingest.build_graph") as builder:
            with patch("lcl.ingest.constructors." + METHOD) as ctor:
                for params in ({"K": True}, {"K": 0}, {"K": -1}, {"K": 1.0},
                               {}, {"K": 1, "q": 1}, {"K": 10**12}, {"K": 78}):
                    with self.subTest(params=params), self.assertRaises(ValueError):
                        construction_input(dict(spec, parameters=params), max_vertices=78)
                for profile in alternatives:
                    with self.subTest(profile=profile):
                        self.assertEqual(len(profile) + sum(1 + q for s in profile for q in s), 15)
                        with self.assertRaisesRegex(ValueError, "requires ordered branches"):
                            construction_input(dict(spec, profile=profile), max_vertices=78)
                ctor.assert_not_called()
            builder.assert_not_called()
