"""Original-path and adverse checks for the conditional nonadjacent consumer."""

import copy
import unittest

from lcl.consumers import _nonadjacent_path_labels, complete_nonadjacent_path
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


def path_fixture(K):
    # The prefix uses 0, K+1, K+2 and differences K+1, K+2.
    graph = build_graph([[] for _ in range(K + 3)])
    prefix = {"s:0": K + 1, "s:1": 0, "s:2": K + 2}
    return graph, prefix


class NonadjacentPathConsumerTests(unittest.TestCase):
    def test_bases_and_recurrence_inventories(self):
        self.assertEqual(_nonadjacent_path_labels(2, 0), [3, 1, 0])
        self.assertEqual(_nonadjacent_path_labels(3, 0), [4, 1, 0, 2])
        self.assertEqual(_nonadjacent_path_labels(4, 0), [5, 1, 2, 0, 3])
        self.assertEqual(_nonadjacent_path_labels(5, 0), [6, 1, 4, 0, 2, 3])
        for K in range(2, 33):
            for ell in (-7, 0, 9):
                with self.subTest(K=K, ell=ell):
                    values = _nonadjacent_path_labels(K, ell)
                    self.assertEqual(values[0], ell + K + 1)
                    self.assertEqual(sorted(values[1:]), list(range(ell, ell + K)))
                    self.assertEqual(sorted(abs(a - b) for a, b in zip(values, values[1:])),
                                     list(range(1, K + 1)))

    def test_original_path_certificates_and_prefix_preservation(self):
        for K in range(2, 33):
            with self.subTest(K=K):
                graph, prefix = path_fixture(K)
                retained_graph, retained_prefix = copy.deepcopy(graph), dict(prefix)
                labels = complete_nonadjacent_path(graph, prefix, K, 1)
                certificate = verify_certificate(retained_graph, labels, graph_digest(retained_graph))
                self.assertTrue(certificate["valid"], certificate["errors"])
                self.assertEqual(prefix, retained_prefix)
                self.assertEqual(graph, retained_graph)
                self.assertEqual({v: labels[v] for v in prefix}, prefix)
                self.assertFalse(interval_boundary(graph, prefix, "s:2")["valid"])

    def test_original_b2_finite_prefix_is_only_a_supplied_fixture(self):
        graph = build_graph([[1], [2], [], [], []])
        # Reflection of an independently found finite K=2 prefix; no seed claim.
        prefix = {"s:0": 3, "b:0:0": 7, "l:0:0:0": 1, "s:1": 0,
                  "b:1:0": 9, "l:1:0:0": 4, "l:1:0:1": 2, "s:2": 8}
        partial = verify_partial(graph, prefix)
        self.assertTrue(partial["valid"], partial["errors"])
        self.assertEqual(partial["unused_labels"], [5, 6])
        self.assertEqual(partial["unused_differences"], [1, 2])
        self.assertFalse(interval_boundary(graph, prefix, "s:2")["valid"])
        original = copy.deepcopy(graph)
        labels = complete_nonadjacent_path(graph, prefix, 2, 5)
        self.assertEqual((labels["s:3"], labels["s:4"]), (6, 5))
        self.assertTrue(verify_certificate(original, labels, graph_digest(original))["valid"])

    def test_rejects_invalid_types_prefix_port_and_inventories(self):
        graph, prefix = path_fixture(3)
        for K, ell in ((True, 1), (1, 1), (0, 1), (3.0, 1), (3, True), (3, 1.0),
                       (3, -1), (3, 0), (3, 2)):
            with self.subTest(K=K, ell=ell), self.assertRaises(ValueError):
                complete_nonadjacent_path(graph, prefix, K, ell)
        for altered in ({**prefix, "s:2": True}, {**prefix, "s:2": 0},
                        {"s:0": prefix["s:0"], "s:1": 0},
                        {**prefix, "s:3": 1}, {**prefix, "unknown": 1}):
            with self.subTest(prefix=altered), self.assertRaises(ValueError):
                complete_nonadjacent_path(graph, altered, 3, 1)
        # Both are valid partial labelings; each isolates a different guard.
        for altered in ({"s:0": 5, "s:1": 0, "s:2": 4},  # wrong port
                        {"s:0": 0, "s:1": 4, "s:2": 5}):  # wrong differences
            self.assertTrue(verify_partial(graph, altered)["valid"])
            with self.subTest(prefix=altered), self.assertRaises(ValueError):
                complete_nonadjacent_path(graph, altered, 3, 1)

    def test_rejects_branched_or_wrong_physical_remaining_path(self):
        graph, prefix = path_fixture(4)
        # Remove profile metadata so the verifier can accept each different
        # original tree; the consumer itself must reject the actual incidences.
        for old, new in ((["s:5", "s:6"], ["s:4", "s:6"]),
                         (["s:2", "s:3"], ["s:1", "s:3"])):
            changed = {"vertices": list(graph["vertices"]),
                       "edges": [list(edge) for edge in graph["edges"]]}
            changed["edges"][changed["edges"].index(old)] = new
            self.assertTrue(verify_partial(changed, prefix)["valid"])
            with self.subTest(new=new), self.assertRaises(ValueError):
                complete_nonadjacent_path(changed, prefix, 4, 1)


if __name__ == "__main__":
    unittest.main()
