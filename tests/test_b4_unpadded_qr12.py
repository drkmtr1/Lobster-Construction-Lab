"""Focused tests for exact QR12 supply, reuse, and bounded admission."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from lcl.constructors import four_section_q112, four_section_qr12
from lcl.ingest import MAX_GRAPH_VERTICES, _parameter_size, construction_input
from lcl.model import build_graph, graph_digest
from lcl.records import save_single
from lcl.verify import verify_certificate


METHOD = "four_section_qr12"


def spec_for(q, r, K):
    return {"method": METHOD, "parameters": {"q": q, "r": r, "K": K},
            "profile": [[q], [r], [1], [2]] + [[] for _ in range(K + 1)]}


def normalized_prefix(result, r, K):
    prefix = result["trace"][0]["prefix_labels"]
    return {v: x - K if x >= r + 6 + K else x for v, x in prefix.items()}


def insert_lower_batch(labels, names):
    size = len(names)
    shifted = {v: x + size if x >= 4 else x for v, x in labels.items()}
    shifted.update({name: 4 + size - index for index, name in enumerate(names, 1)})
    return shifted


class QR12Tests(unittest.TestCase):
    def test_minimum_campaign_case_and_empty_bands(self):
        spec = spec_for(1, 2, 1)
        original = build_graph(spec["profile"])
        declared, result = construction_input(spec, max_vertices=79)
        self.assertEqual(declared, original)
        self.assertEqual(result["method"], METHOD)
        self.assertEqual(result["claim_scope"]["construction_case"], "1212_block_insertions")
        self.assertEqual(result["claim_scope"]["parameters"], {"q": 1, "r": 2, "K": 1})
        prefix, step = result["trace"]
        exact = {"s:0": 15, "s:1": 0, "s:2": 12, "s:3": 7, "s:4": 9,
                 "b:0:0": 1, "l:0:0:0": 14, "b:1:0": 11, "l:1:0:0": 4, "l:1:0:1": 5,
                 "b:2:0": 3, "l:2:0:0": 13, "b:3:0": 10, "l:3:0:0": 2, "l:3:0:1": 6}
        self.assertEqual(prefix["prefix_labels"], exact)
        self.assertEqual((prefix["active_vertex"], prefix["active_label"]), ("s:4", 9))
        self.assertEqual((prefix["unused_labels"], prefix["unused_differences"]), ([8], [1]))
        self.assertEqual((step["parent"], step["vertex"], step["label"], step["difference"]),
                         ("s:4", "s:5", 8, 1))
        self.assertEqual(result["claim_scope"]["alpha_low_class_size"], 9)
        self.assertTrue(verify_certificate(original, result["labels"], graph_digest(original))["valid"])

    def test_named_second_insertion_batches_and_both_growth_legs(self):
        base = normalized_prefix(four_section_qr12(1, 2, 1), 2, 1)
        for q, r, K in ((1, 3, 1), (2, 4, 5)):
            with self.subTest(q=q, r=r, K=K):
                names = [f"l:1:0:{j}" for j in range(2, r)]
                batch = insert_lower_batch(base, names)
                iterative = base
                for name in names:
                    iterative = insert_lower_batch(iterative, [name])
                self.assertEqual(iterative, batch)
                self.assertEqual([batch[v] for v in names], list(range(r + 1, 3, -1)))
                for v in ("s:0", "l:0:0:0"):
                    batch[v] += q - 1
                batch.update({f"l:0:0:{j}": r + 10 + j for j in range(1, q)})
                result = four_section_qr12(q, r, K)
                normalized = normalized_prefix(result, r, K)
                self.assertEqual(normalized, batch)

                graph = build_graph([[q], [r], [1], [2], []])
                self.assertEqual(normalized["b:1:0"], r + 8)
                for name in names:
                    self.assertEqual([e for e in graph["edges"] if name in e], [["b:1:0", name]])
                lower = {name for name, label in normalized.items() if label < 4}
                upper = {name for name, label in normalized.items() if label >= q + r + 10}
                self.assertEqual(upper, {"s:0", "l:0:0:0"})
                for selected, interval in ((lower, range(r + 5, q + r + 12)),
                                           (upper, range(q + r + 9, q + r + 12))):
                    weights = [abs(normalized[u] - normalized[v]) for u, v in graph["edges"]
                               if u in selected or v in selected]
                    self.assertEqual(sorted(weights), list(interval))

    def test_retained_r1_exact_labels_trace_and_interface(self):
        q, K = 2, 1
        reference = four_section_q112(q, K)
        original, wrapped = construction_input(spec_for(q, 1, K))
        self.assertEqual(wrapped["labels"], reference["labels"])
        self.assertEqual(wrapped["trace"], reference["trace"])
        self.assertEqual(wrapped["graph"], reference["graph"])
        self.assertEqual(wrapped["method"], METHOD)
        scope = wrapped["claim_scope"]
        self.assertEqual(scope["parameters"], {"q": q, "r": 1, "K": K})
        self.assertEqual(scope["construction_case"], "retained_q112")
        self.assertEqual(scope["case_source"], "research/B4_FOURTH_2_SUPPLY.md")
        for key in ("suffix_interface", "alpha_low_class_size"):
            self.assertEqual(scope[key], reference["claim_scope"][key])
        self.assertTrue(verify_certificate(original, wrapped["labels"], graph_digest(original))["valid"])

    def test_parameters_and_profile_invalid_before_expansion(self):
        spec = spec_for(2, 3, 1)
        wrong_profiles = (
            [[3], [2], [1], [2], [], []],  # Reorder q and r.
            [[2], [3], [2], [1], [], []],  # Reorder the last two branches.
            [[2, 0], [3], [1], [2], []],   # Padding replaces a spine vertex.
            [[2], [3], [1], [], [2], []],  # Keep order but move the last branch.
        )
        with patch("lcl.constructors.build_graph") as ctor_builder, patch("lcl.ingest.build_graph") as parser_builder:
            for name in ("q", "r", "K"):
                for invalid in (False, True, 0, -1, 2.0, "2", None):
                    params = dict(spec["parameters"], **{name: invalid})
                    with self.subTest(name=name, value=invalid):
                        with self.assertRaises(ValueError):
                            four_section_qr12(**params)
                        with self.assertRaises(ValueError):
                            construction_input(dict(spec, parameters=params))
                missing = dict(spec["parameters"])
                del missing[name]
                with self.assertRaises(ValueError):
                    construction_input(dict(spec, parameters=missing))
            with self.assertRaises(ValueError):
                construction_input(dict(spec, parameters={**spec["parameters"], "t": 1}))
            for profile in wrong_profiles:
                with self.subTest(profile=profile):
                    self.assertEqual(len(profile) + sum(1 + k for block in profile for k in block), 18)
                    with self.assertRaisesRegex(ValueError, "requires ordered branches"):
                        construction_input(dict(spec, profile=profile))
            with self.assertRaises(ValueError):
                construction_input(dict(spec, profile=spec["profile"] + [[]]))
            ctor_builder.assert_not_called()
            parser_builder.assert_not_called()

    def test_joint_preflight_and_79_vertex_target(self):
        spec = spec_for(1, 2, 64)
        original, result = construction_input(spec, max_vertices=79)
        self.assertEqual(len(original["vertices"]), 79)
        self.assertTrue(verify_certificate(original, result["labels"], graph_digest(original))["valid"])
        with patch("lcl.ingest.build_graph") as build:
            with self.assertRaisesRegex(ValueError, "78-vertex"):
                construction_input(spec, max_vertices=78)
            too_large = spec_for(1, 2, 9986)
            with self.assertRaisesRegex(ValueError, "10000-vertex"):
                construction_input(too_large)
            build.assert_not_called()
        preflight_pass = RuntimeError("passed preflight before expanding")
        with patch("lcl.ingest._graph_value", side_effect=preflight_pass) as expand:
            with self.assertRaisesRegex(RuntimeError, "passed preflight"):
                construction_input(spec_for(1, 2, 9985))
            expand.assert_called_once()
        for field in ("q", "r", "K"):
            params = dict(q=1, r=2, K=1)
            params[field] += 9988 - sum(params.values())
            self.assertEqual(_parameter_size(METHOD, params, MAX_GRAPH_VERTICES), 10_000)
            params[field] += 1
            with self.assertRaisesRegex(ValueError, "10000-vertex"):
                _parameter_size(METHOD, params, MAX_GRAPH_VERTICES)

    def test_checker_rejects_false_labels_and_changed_named_incidence(self):
        original, result = construction_input(spec_for(1, 2, 1))
        digest = graph_digest(original)
        bad = dict(result["labels"], **{"s:5": result["labels"]["s:4"]})
        self.assertFalse(verify_certificate(original, bad, digest)["valid"])
        altered = deepcopy(original)
        edge = altered["edges"].index(["b:3:0", "l:3:0:1"])
        altered["edges"][edge] = ["b:1:0", "l:3:0:1"]
        self.assertFalse(verify_certificate(altered, result["labels"], digest)["valid"])

    def test_record_cap_is_separate_from_graph_admission(self):
        spec = spec_for(1, 2, 1)
        original, result = construction_input(spec, max_vertices=79)
        oversized = {**result, "oversized_test_value": "x" * 2_000_000}
        project = Path(__file__).resolve().parents[1]
        with TemporaryDirectory() as root:
            output = Path(root) / "rejected"
            with self.assertRaisesRegex(ValueError, "Record exceeds configured output limit"):
                save_single(project, output, original, oversized, spec)
            self.assertFalse((output / "record.json").exists())


if __name__ == "__main__":
    unittest.main()
