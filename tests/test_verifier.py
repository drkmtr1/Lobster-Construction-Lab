"""Adverse finite certificates and original-incidence binding checks."""

import copy
import unittest

from lcl.verify import verify_certificate, verify_graph, verify_partial


def path_graph(n):
    vertices = [f"p{i}" for i in range(n)]
    return {"vertices": vertices, "edges": [[vertices[i], vertices[i + 1]] for i in range(n - 1)]}


def profile_fixture():
    # An explicit independent fixture for [[1], []], not model.build_graph.
    return {
        "schema_version": 1, "profile": [[1], []],
        "vertices": ["s:0", "s:1", "b:0:0", "l:0:0:0"],
        "edges": [["s:0", "s:1"], ["s:0", "b:0:0"], ["b:0:0", "l:0:0:0"]],
        "spine": ["s:0", "s:1"],
        "roles": {"s:0": {"kind": "spine", "section": 0},
                  "s:1": {"kind": "spine", "section": 1},
                  "b:0:0": {"kind": "branch", "section": 0, "branch": 0},
                  "l:0:0:0": {"kind": "leaf", "section": 0, "branch": 0, "leaf": 0}},
    }


class CertificateTests(unittest.TestCase):
    def test_singleton_and_zero_edges(self):
        self.assertTrue(verify_certificate(path_graph(1), {"p0": 0})["valid"])

    def test_valid_path_and_named_topology(self):
        graph = path_graph(4)
        labels = dict(zip(graph["vertices"], [0, 3, 1, 2]))
        report = verify_certificate(graph, labels)
        self.assertTrue(report["valid"], report)
        self.assertEqual(sorted(report["edge_differences"]), [1, 2, 3])
        self.assertTrue(verify_certificate(graph, labels, report["graph_digest"])["valid"])

    def test_invalid_label_types_duplicates_and_missing_labels(self):
        graph = path_graph(4)
        for values in ([False, 3, 1, 2], [0.0, 3, 1, 2], [0, 3, 1, 1], [0, 4, 1, 2]):
            self.assertFalse(verify_certificate(graph, dict(zip(graph["vertices"], values)))["valid"])
        self.assertFalse(verify_certificate(graph, {"p0": 0, "p1": 3})["valid"])
        self.assertFalse(verify_certificate(graph, {"p0": 0, "p1": 3, "p2": 1, "impostor": 2})["valid"])

    def test_all_vertices_unique_does_not_excuse_repeated_differences(self):
        graph = path_graph(4)
        report = verify_certificate(graph, dict(zip(graph["vertices"], [0, 1, 2, 3])))
        self.assertFalse(report["valid"])
        self.assertIn("edge differences repeat", report["errors"])

    def test_profile_role_swap_and_edge_substitution_rejected(self):
        graph = profile_fixture()
        labels = {"s:1": 0, "s:0": 3, "b:0:0": 1, "l:0:0:0": 2}
        self.assertTrue(verify_certificate(graph, labels)["valid"])
        changed_roles = copy.deepcopy(graph)
        changed_roles["roles"]["s:0"], changed_roles["roles"]["b:0:0"] = (
            changed_roles["roles"]["b:0:0"], changed_roles["roles"]["s:0"])
        self.assertFalse(verify_certificate(changed_roles, labels)["valid"])
        changed_edge = copy.deepcopy(graph)
        changed_edge["edges"][-1] = ["s:1", "l:0:0:0"]
        # Same vertex and edge counts are insufficient: exact incidence matters.
        self.assertFalse(verify_certificate(changed_edge, labels)["valid"])
        changed_type = copy.deepcopy(graph)
        changed_type["roles"]["s:1"]["section"] = True
        self.assertFalse(verify_certificate(changed_type, labels)["valid"])

    def test_expected_digest_rejects_another_valid_graph(self):
        original = path_graph(4)
        digest = verify_graph(original)["graph_digest"]
        substitute = {"vertices": original["vertices"], "edges": [["p0", "p1"], ["p0", "p2"], ["p0", "p3"]]}
        labels = {"p0": 0, "p1": 1, "p2": 2, "p3": 3}
        self.assertTrue(verify_certificate(substitute, labels)["valid"])
        self.assertFalse(verify_certificate(substitute, labels, digest)["valid"])

    def test_edge_order_is_not_a_topology_change(self):
        graph = profile_fixture()
        digest = verify_graph(graph)["graph_digest"]
        graph["edges"] = [list(reversed(e)) for e in reversed(graph["edges"])]
        graph["vertices"].reverse()
        self.assertEqual(verify_graph(graph)["graph_digest"], digest)

    def test_malformed_and_non_tree_graphs(self):
        fixtures = [None, {}, {"vertices": ["a", "a"], "edges": [["a", "a"]]},
                    {"vertices": ["a", "b"], "edges": [["a", "b"], ["b", "a"]]},
                    {"vertices": ["a", "b", "c"], "edges": [["a", "b"]]},
                    {"vertices": ["a", "b"], "edges": [["a", "x"]]},
                    {"vertices": ["a", "b", "c"], "edges": [["a", "b"], ["b", "c"], ["c", "a"]]}]
        for graph in fixtures:
            self.assertFalse(verify_graph(graph)["valid"], graph)

    def test_lobster_membership_and_invalid_declared_spine(self):
        # Three arms of length 3 leave a claw after two leaf-deletion rounds.
        vertices = ["h"] + [f"a{i}:{j}" for i in range(3) for j in range(1, 4)]
        edges = []
        for i in range(3):
            edges.extend([["h", f"a{i}:1"], [f"a{i}:1", f"a{i}:2"], [f"a{i}:2", f"a{i}:3"]])
        self.assertFalse(verify_graph({"vertices": vertices, "edges": edges})["valid"])
        graph = path_graph(7)
        self.assertTrue(verify_graph(graph)["valid"])
        graph["spine"] = ["p3"]
        self.assertFalse(verify_graph(graph)["valid"])

    def test_non_alpha_graceful_claw_remains_admissible(self):
        graph = {"vertices": ["h", "a", "b", "c", "x", "y", "z"],
                 "edges": [["h", "a"], ["h", "b"], ["h", "c"], ["a", "x"], ["b", "y"], ["c", "z"]]}
        self.assertTrue(verify_certificate(graph, {"h": 0, "a": 2, "b": 4, "c": 6, "x": 5, "y": 3, "z": 1})["valid"])

    def test_profile_size_mismatch_is_rejected_before_expansion(self):
        graph = {"vertices": ["s:0"], "edges": [], "profile": [[10**12]]}
        self.assertFalse(verify_graph(graph)["valid"])

    def test_partial_resources_and_no_completion_claim(self):
        graph = path_graph(4)
        report = verify_partial(graph, {"p1": 0, "p2": 3})
        self.assertTrue(report["valid"])
        self.assertEqual(report["unused_labels"], [1, 2])
        self.assertEqual(report["unused_differences"], [1, 2])
        self.assertEqual(report["frontier"], ["p1", "p2"])
        self.assertFalse(report["complete"])
        self.assertIn("no completion", report["claim"])
        self.assertFalse(verify_partial(graph, {"p1": 0, "p2": 0})["valid"])


if __name__ == "__main__":
    unittest.main()
