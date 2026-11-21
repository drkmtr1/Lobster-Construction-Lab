"""Physical boundary semantics and noncircular classification of B2 data."""

import copy
import unittest

from lcl.model import build_graph
from lcl.states import b2_restrictions, extract_b2_candidate, interval_boundary
from lcl.verify import verify_certificate


def b2_fixture():
    graph = build_graph([[1], [1], [], []])
    labels = {"s:0": 1, "b:0:0": 4, "l:0:0:0": 6,
              "s:1": 7, "b:1:0": 0, "l:1:0:0": 5,
              "s:2": 3, "s:3": 2}
    return graph, labels


class BoundaryStateTests(unittest.TestCase):
    def test_translated_and_reflected_interval_boundaries(self):
        graph, labels = b2_fixture()
        self.assertTrue(verify_certificate(graph, labels)["valid"])
        for full, start, side in ((labels, 2, "above"),
                                  ({v: 7 - x for v, x in labels.items()}, 5, "below")):
            prefix = {v: x for v, x in full.items() if v != "s:3"}
            result = interval_boundary(graph, prefix, "s:2")
            self.assertTrue(result["valid"], result)
            self.assertEqual(result["unused_labels"], [start])
            self.assertEqual(result["unused_differences"], [1])
            self.assertEqual(result["interval"], [start, start])
            self.assertEqual(result["supplier_status"], "not_established_by_boundary_check")
            pins, domains = b2_restrictions(graph, 1, interval_start=start, side=side)
            self.assertEqual(pins, {"s:2": full["s:2"]})
            self.assertEqual(domains["s:3"], [start])
            self.assertTrue(all(full[v] in allowed for v, allowed in domains.items()))

    def test_correct_numeric_endpoint_at_wrong_physical_vertex_rejected(self):
        graph, labels = b2_fixture()
        prefix = {v: x for v, x in labels.items() if v != "s:3"}
        # Both s:0=1 and s:2=3 lie just outside the remaining interval [2,2].
        # Only the actual port s:2 is incident to the unfinished edge.
        result = interval_boundary(graph, prefix, "s:0")
        self.assertFalse(result["valid"])
        self.assertFalse(result["all_unfinished_incidence_at_port"])

    def test_multiple_open_ports_are_not_a_single_port_interface(self):
        graph = {"vertices": ["p0", "p1", "p2", "p3"],
                 "edges": [["p0", "p1"], ["p1", "p2"], ["p2", "p3"]]}
        result = interval_boundary(graph, {"p1": 0, "p2": 3}, "p1")
        self.assertEqual(result["unused_labels"], [1, 2])
        self.assertEqual(result["unused_differences"], [1, 2])
        self.assertFalse(result["valid"])
        self.assertFalse(result["all_unfinished_incidence_at_port"])

    def test_remaining_difference_inventory_is_required(self):
        graph = {"vertices": ["p0", "p1", "p2", "p3"],
                 "edges": [["p0", "p1"], ["p1", "p2"], ["p2", "p3"]]}
        result = interval_boundary(graph, {"p0": 0, "p1": 1}, "p1")
        self.assertEqual(result["unused_labels"], [2, 3])
        self.assertEqual(result["unused_differences"], [2, 3])
        self.assertTrue(result["all_unfinished_incidence_at_port"])
        self.assertFalse(result["valid"])

    def test_completed_and_unassigned_boundary_cases(self):
        graph, labels = b2_fixture()
        result = interval_boundary(graph, labels, "s:2")
        self.assertTrue(result["valid"])
        self.assertEqual(result["remaining_edges"], 0)
        self.assertEqual(result["interval"], [None, None])
        self.assertFalse(interval_boundary(graph, {}, "s:2")["valid"])
        self.assertFalse(interval_boundary(graph, {"s:2": True}, "s:2")["valid"])

    def test_exact_b2_topology_is_required(self):
        invalid_profiles = ([[1], [1], [], [0]], [[1], [1], [0], []],
                            [[1, 1], [1], [], []], [[0, 1], [1], [], []],
                            [[], [1], [], []])
        for profile in invalid_profiles:
            with self.assertRaises(ValueError):
                b2_restrictions(build_graph(profile), 1)
        graph, _ = b2_fixture()
        rewired = copy.deepcopy(graph)
        rewired["edges"][2] = ["s:0", "s:3"]
        with self.assertRaises(ValueError):
            b2_restrictions(rewired, 1)
        explicit = {key: graph[key] for key in ("vertices", "edges")}
        with self.assertRaises(ValueError):
            b2_restrictions(explicit, 1)

    def test_restriction_boundaries_and_explicit_root_pin(self):
        graph, _ = b2_fixture()
        for kwargs in ({"K": 0}, {"K": True}, {"K": 2},
                       {"K": 1, "interval_start": -1}, {"K": 1, "interval_start": True},
                       {"K": 1, "interval_start": 0, "side": "below"},
                       {"K": 1, "interval_start": 7, "side": "above"},
                       {"K": 1, "side": "sideways"}, {"K": 1, "root_label": True},
                       {"K": 1, "root_label": -1}, {"K": 1, "root_label": 8}):
            with self.assertRaises(ValueError):
                b2_restrictions(graph, **kwargs)
        pins, _ = b2_restrictions(graph, 1, interval_start=2, root_label=1)
        self.assertEqual(pins, {"s:2": 3, "s:0": 1})

    def test_extracted_candidate_remains_solver_derived(self):
        graph, labels = b2_fixture()
        result = extract_b2_candidate(graph, labels)
        self.assertEqual(result["classification"], "solver_derived_exploratory_prefix")
        self.assertFalse(result["independent_supplier"])
        self.assertEqual(result["proof_status"], "finite_witness_only")
        self.assertNotIn("s:3", result["labels"])
        self.assertTrue(result["boundary"]["valid"])

    def test_invalid_full_witness_is_checked_before_suffix_deletion(self):
        graph, labels = b2_fixture()
        for replacement in (labels["s:0"], True, 20):
            broken = dict(labels)
            broken["s:3"] = replacement
            with self.assertRaises(ValueError):
                extract_b2_candidate(graph, broken)
        missing = {v: x for v, x in labels.items() if v != "s:3"}
        with self.assertRaises(ValueError):
            extract_b2_candidate(graph, missing)


if __name__ == "__main__":
    unittest.main()
