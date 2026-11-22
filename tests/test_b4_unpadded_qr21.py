"""Bounded exact QR21 construction and admission checks."""
from copy import deepcopy
import unittest
from unittest.mock import patch

from lcl.constructors import four_section_qr21
from lcl.ingest import MAX_GRAPH_VERTICES, _parameter_size, construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate

CASES = ((1, 1, 1), (1, 2, 1), (2, 1, 1), (2, 3, 1), (1, 1, 2), (1, 3, 3),
         (3, 1, 4), (2, 2, 5), (3, 4, 8), (8, 5, 15), (5, 8, 16), (2, 1, 64))
METHOD = "four_section_qr21"


def spec_for(q, r, K):
    return {"method": METHOD, "parameters": {"q": q, "r": r, "K": K},
            "profile": [[q], [r], [2], [1]] + [[] for _ in range(K + 1)]}


class QR21Tests(unittest.TestCase):
    def test_declared_targets_exact_boundary_and_prefix_preservation(self):
        for q, r, K in CASES:
            with self.subTest(q=q, r=r, K=K):
                original = build_graph(spec_for(q, r, K)["profile"])
                m = q + r + K + 11
                a = r + 5
                result = four_section_qr21(q, r, K)
                self.assertEqual(result["graph"], original)
                labels, trace = result["labels"], result["trace"][0]
                prefix = trace["prefix_labels"]
                self.assertEqual(prefix["s:0"], m - (q - 1))
                self.assertEqual([prefix[f"l:0:0:{j}"] for j in range(q)],
                                 [K + r + 11] + [K + r + 12 + j for j in range(1, q)])
                self.assertEqual([prefix[f"l:1:0:{j}"] for j in range(r)], list(range(3, r + 3)))
                self.assertEqual([prefix["l:2:0:0"], prefix["l:2:0:1"]], [K + r + 9, K + r + 10])
                for leaf in ("l:2:0:0", "l:2:0:1"):
                    self.assertEqual([e for e in original["edges"] if leaf in e], [["b:2:0", leaf]])
                remaining = set(original["spine"][5:])
                path = list(zip(original["spine"][4:], original["spine"][5:]))
                self.assertEqual(set(original["vertices"]) - set(prefix), remaining)
                self.assertEqual([tuple(e) for e in original["edges"] if remaining.intersection(e)], path)
                self.assertEqual([e for e in path if len(remaining.intersection(e)) == 1], [("s:4", "s:5")])
                state = interval_boundary(original, prefix, "s:4")
                self.assertTrue(state["valid"], state["errors"])
                self.assertEqual(state["active_label"], a + K)
                self.assertEqual(state["unused_labels"], list(range(a, a + K)))
                self.assertEqual(state["unused_differences"], list(range(1, K + 1)))
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertEqual([abs(labels[u] - labels[v]) for u, v in path], list(range(K, 0, -1)))
                self.assertEqual(len(result["trace"]), K + 1)
                p = a + (K + 1) // 2
                self.assertEqual(result["claim_scope"]["alpha_low_class_size"], p)
                self.assertTrue(all((labels[u] < p) != (labels[v] < p) for u, v in original["edges"]))
                self.assertTrue(verify_certificate(original, labels, graph_digest(original))["valid"])

    def test_direct_parameters_rejected_before_expansion(self):
        with patch("lcl.constructors.build_graph") as builder:
            for index in range(3):
                for invalid in (True, False, 0, -1, 1.0, "1", None):
                    args = [1, 1, 1]
                    args[index] = invalid
                    with self.subTest(args=args), self.assertRaises(ValueError):
                        four_section_qr21(*args)
            builder.assert_not_called()

    def test_ingest_rejects_wrong_keys_values_and_profiles_before_dispatch(self):
        spec = spec_for(2, 3, 1)
        alternatives = ([[3], [2], [2], [1], [], []], [[2], [3], [1], [2], [], []],
                        [[2, 0], [3], [2], [1], []], [[2], [3], [2], [], [1], []])
        with patch("lcl.ingest.build_graph") as builder, patch("lcl.ingest.constructors." + METHOD) as ctor:
            for name in ("q", "r", "K"):
                missing = {key: v for key, v in spec["parameters"].items() if key != name}
                with self.subTest(missing=name), self.assertRaises(ValueError):
                    construction_input(dict(spec, parameters=missing))
                for invalid in (True, False, 0, -2, 1.0, "1", 10**12):
                    with self.subTest(name=name, value=invalid), self.assertRaises(ValueError):
                        construction_input(dict(spec, parameters=dict(spec["parameters"], **{name: invalid})))
            with self.assertRaises(ValueError):
                construction_input(dict(spec, parameters=dict(spec["parameters"], t=2)))
            for profile in alternatives:
                with self.subTest(profile=profile):
                    self.assertEqual(len(profile) + sum(1 + q for section in profile for q in section), 18)
                    with self.assertRaisesRegex(ValueError, "requires ordered branches"):
                        construction_input(dict(spec, profile=profile))
            with self.assertRaises(ValueError):
                construction_input(dict(spec, profile=spec["profile"] + [[]]))
            ctor.assert_not_called()
            builder.assert_not_called()

    def test_joint_size_boundary_and_original_certificate(self):
        spec = spec_for(*CASES[-1])
        original = build_graph(spec["profile"])
        declared, result = construction_input(spec, max_vertices=79)
        self.assertEqual(declared, original)
        digest = graph_digest(original)
        self.assertEqual(result["graph_digest"], digest)
        self.assertTrue(verify_certificate(original, result["labels"], digest)["valid"])
        bad = dict(result["labels"], **{"s:5": result["labels"]["s:4"]})
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        altered = deepcopy(original)
        edge = altered["edges"].index(["b:2:0", "l:2:0:1"])
        altered["edges"][edge] = ["b:1:0", "l:2:0:1"]
        self.assertFalse(verify_certificate(altered, result["labels"], digest)["valid"])
        with self.assertRaisesRegex(ValueError, "78-vertex"):
            construction_input(spec, max_vertices=78)
        self.assertEqual(MAX_GRAPH_VERTICES, 10_000)
        for name in ("q", "r", "K"):
            params = dict(q=1, r=1, K=1)
            params[name] = 9986
            with self.subTest(large=name):
                self.assertEqual(_parameter_size(METHOD, params, MAX_GRAPH_VERTICES), 10_000)
                params[name] = 9987
                with self.assertRaisesRegex(ValueError, "10000-vertex"):
                    _parameter_size(METHOD, params, MAX_GRAPH_VERTICES)

    def test_retained_1121_route_on_overlapping_k1_target(self):
        spec = spec_for(1, 1, 1)
        original = build_graph(spec["profile"])
        retained = dict(spec, method="four_section_1121", parameters={"K": 1})
        declared, result = construction_input(retained, max_vertices=79)
        self.assertEqual(declared, original)
        self.assertEqual(result["method"], "four_section_1121")
        self.assertTrue(verify_certificate(original, result["labels"], graph_digest(original))["valid"])
