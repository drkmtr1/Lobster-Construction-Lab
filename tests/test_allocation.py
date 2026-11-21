"""Finite independent controls for R226's structural extraction and scope."""

from itertools import permutations
import unittest

from lcl.allocation import complete_two_host
from lcl.verify import verify_certificate


def double_star(q_u, q_v):
    vertices, edges = ["u", "v"], [["u", "v"]]
    for host, quota in (("u", q_u), ("v", q_v)):
        for i in range(quota):
            leaf = f"{host}:{i}"
            vertices.append(leaf)
            edges.append([host, leaf])
    return {"vertices": vertices, "edges": edges, "spine": ["u", "v"]}


def brute_extension_exists(graph, core_labels):
    """Direct enumeration for <=4 unassigned named vertices; no solver imports."""
    m = len(graph["edges"])
    remaining_vertices = [v for v in graph["vertices"] if v not in core_labels]
    remaining_labels = sorted(set(range(m + 1)) - set(core_labels.values()))
    for labels in permutations(remaining_labels):
        candidate = {**core_labels, **dict(zip(remaining_vertices, labels))}
        if sorted(abs(candidate[u] - candidate[v]) for u, v in graph["edges"]) == list(range(1, m + 1)):
            return True
    return False


class AllocationTests(unittest.TestCase):
    def test_parallel_pair_parity_obstruction_is_restricted(self):
        graph = double_star(1, 1)
        result = complete_two_host(graph, {"u": 0, "v": 3}, ("u", "v"))
        self.assertEqual(result["status"], "RESTRICTED_INFEASIBLE")
        self.assertEqual((result["details"]["A0"], result["details"]["c"], result["details"]["eta"]), (0, 1, 0))
        self.assertEqual(result["details"]["fractional_quota_interval"], [0, 2])
        self.assertFalse(result["restrictions"]["ordinary_nongracefulness_claim"])
        ordinary_witness = {"u": 0, "v": 2, "u:0": 3, "v:0": 1}
        self.assertTrue(verify_certificate(graph, ordinary_witness)["valid"])

    def test_half_edge_forces_the_actual_host(self):
        passing = complete_two_host(double_star(1, 0), {"u": 0, "v": 1}, ("u", "v"))
        self.assertEqual(passing["status"], "SAT")
        self.assertEqual(passing["labels"]["u:0"], 2)
        failing = complete_two_host(double_star(0, 1), {"u": 0, "v": 1}, ("u", "v"))
        self.assertEqual(failing["status"], "RESTRICTED_INFEASIBLE")

    def test_midpoint_can_supply_either_host_and_zero_quotas_are_retained(self):
        for quotas in ((1, 0), (0, 1)):
            graph = double_star(*quotas)
            result = complete_two_host(graph, {"u": 0, "v": 2}, ("u", "v"))
            self.assertEqual(result["status"], "SAT")
            self.assertEqual(result["details"]["eta"], 1)
            self.assertTrue(verify_certificate(graph, result["labels"])["valid"])

    def test_n224_documented_adverse_control(self):
        graph = {"vertices": ["U", "A", "B", "V", "X", "Y"],
                 "edges": [["U", "A"], ["A", "B"], ["B", "V"], ["A", "X"], ["B", "Y"]]}
        result = complete_two_host(graph, {"U": 3, "A": 1, "B": 5, "V": 0}, ("A", "B"))
        self.assertEqual(result["status"], "RESTRICTED_INFEASIBLE")
        self.assertEqual(result["details"]["unused_labels"], [2, 4])
        self.assertEqual(result["details"]["unused_differences"], [1, 3])
        self.assertEqual(result["details"]["c"], 1)
        ordinary = {"A": 0, "B": 5, "U": 1, "V": 2, "X": 4, "Y": 3}
        self.assertTrue(verify_certificate(graph, ordinary)["valid"])

    def test_empty_completion_preserves_valid_complete_core(self):
        graph = double_star(0, 0)
        core = {"u": 1, "v": 0}
        result = complete_two_host(graph, core, ("u", "v"))
        self.assertEqual(result["status"], "SAT")
        self.assertEqual(result["labels"], core)
        self.assertEqual((result["details"]["A0"], result["details"]["c"], result["details"]["eta"]), (0, 0, 0))

    def test_all_two_host_core_labelings_for_nine_tiny_targets(self):
        cases = 0
        for q_u in range(3):
            for q_v in range(3):
                graph = double_star(q_u, q_v)
                m = len(graph["edges"])
                for a, b in permutations(range(m + 1), 2):
                    with self.subTest(quotas=(q_u, q_v), core=(a, b)):
                        core = {"u": a, "v": b}
                        expected = brute_extension_exists(graph, core)
                        result = complete_two_host(graph, core, ("v", "u"))
                        self.assertEqual(result["status"] == "SAT", expected)
                        self.assertNotEqual(result["status"], "INVALID_INPUT")
                        if expected:
                            report = verify_certificate(graph, result["labels"], result["restrictions"]["graph_digest"])
                            self.assertTrue(report["valid"], report["errors"])
                            self.assertEqual({v: result["labels"][v] for v in core}, core)
                        cases += 1
        self.assertEqual(cases, 120)

    def test_nonadjacent_hosts_supported(self):
        graph = {"vertices": ["u", "w", "v", "x", "y"],
                 "edges": [["u", "w"], ["w", "v"], ["u", "x"], ["v", "y"]]}
        for values in permutations(range(5), 3):
            core = dict(zip(("u", "w", "v"), values))
            if abs(core["u"] - core["w"]) == abs(core["w"] - core["v"]):
                continue
            result = complete_two_host(graph, core, ("u", "v"))
            self.assertEqual(result["status"] == "SAT", brute_extension_exists(graph, core))
            if result["status"] == "SAT":
                self.assertTrue(verify_certificate(graph, result["labels"])["valid"])

    def test_invalid_core_or_unassigned_shape_rejected(self):
        graph = double_star(1, 1)
        invalid = [({}, ("u", "v")), ({"u": True, "v": 1}, ("u", "v")),
                   ({"u": 0, "v": 0}, ("u", "v")), ({"u": -1, "v": 2}, ("u", "v")),
                   ({"u": 0, "v": 4}, ("u", "v")), ({"u": 0, "missing": 1}, ("u", "missing")),
                   ({"u": 0, "v": 3}, ("u", "u")), ({"u": 0, "v": 3}, ("u", "u:0")),
                   ({"u:0": 0, "v:0": 3}, ("u:0", "v:0"))]
        for core, hosts in invalid:
            self.assertEqual(complete_two_host(graph, core, hosts)["status"], "INVALID_INPUT")
        unsupported = {"vertices": ["u", "v", "x", "y"],
                       "edges": [["u", "v"], ["v", "x"], ["x", "y"]]}
        self.assertEqual(complete_two_host(unsupported, {"u": 0, "v": 1}, ("u", "v"))["status"], "INVALID_INPUT")
        duplicate_core_diff = {"u": 0, "v": 1, "v:0": 2}
        self.assertEqual(complete_two_host(graph, duplicate_core_diff, ("u", "v"))["status"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
