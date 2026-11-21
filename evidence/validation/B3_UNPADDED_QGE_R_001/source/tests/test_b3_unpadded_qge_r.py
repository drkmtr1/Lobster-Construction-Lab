"""Fixed original-target checks for B3-UNPADDED-QGE-R-001."""

import unittest
from unittest.mock import patch

from lcl.constructors import three_section_nonadjacent
from lcl.consumers import complete_nonadjacent_path
from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


CASES = ((1, 1, 1, 2), (1, 1, 1, 3), (1, 1, 1, 4), (1, 1, 1, 5),
         (2, 1, 1, 2), (2, 2, 1, 6), (3, 1, 4, 3), (3, 2, 1, 4),
         (3, 3, 5, 7), (5, 2, 3, 8), (5, 5, 2, 12), (8, 3, 7, 14))


def named_edges(q, r, t, K):
    edges = {(f"s:{i}", f"s:{i + 1}") for i in range(K + 3)}
    for i, count in enumerate((q, r, t)):
        edges.add((f"s:{i}", f"b:{i}:0"))
        edges.update((f"b:{i}:0", f"l:{i}:0:{j}") for j in range(count))
    return {tuple(sorted(e)) for e in edges}


class B3UnpaddedTests(unittest.TestCase):
    def test_declared_original_graphs_and_arithmetic(self):
        for q, r, t, K in CASES:
            with self.subTest(q=q, r=r, t=t, K=K):
                original = build_graph([[q], [r], [t]] + [[] for _ in range(K + 1)])
                edges = named_edges(q, r, t, K)
                self.assertEqual(len(edges), q + r + t + K + 6)
                self.assertEqual({tuple(sorted(e)) for e in original["edges"]}, edges)
                self.assertEqual(set(original["vertices"]), {v for e in edges for v in e})
                result = three_section_nonadjacent(q, r, t, K)
                a, x, m = q + t + 3, q - r, q + r + t + K + 6
                prefix = result["trace"][0]["prefix_labels"]
                expected = {"s:0": x, "s:1": K + a + 2, "s:2": q + 2,
                            "s:3": K + a + 1, "b:0:0": m, "b:1:0": q + 1,
                            "b:2:0": K + a}
                expected.update({f"l:0:0:{j}": j if j < x else j + 1 for j in range(q)})
                expected.update({f"l:1:0:{j}": K + a + 3 + j for j in range(r)})
                expected.update({f"l:2:0:{j}": q + 3 + j for j in range(t)})
                self.assertEqual(prefix, expected)
                suffix = {f"s:{i}" for i in range(4, K + 4)}
                self.assertEqual(set(original["vertices"]) - set(prefix), suffix)
                incident = {e for e in edges if suffix.intersection(e)}
                self.assertEqual(incident, {tuple(sorted((f"s:{i}", f"s:{i + 1}")))
                                            for i in range(3, K + 3)})
                part = verify_partial(original, prefix)
                self.assertTrue(part["valid"], part["errors"])
                self.assertEqual(part["frontier"], ["s:3"])
                self.assertEqual(part["unused_labels"], list(range(a, a + K)))
                self.assertEqual(part["unused_differences"], list(range(1, K + 1)))
                self.assertEqual(part["used_differences"], list(range(K + 1, m + 1)))
                self.assertEqual(prefix["s:3"], a + K + 1)
                self.assertFalse(interval_boundary(original, prefix, "s:3")["valid"])
                labels = result["labels"]
                self.assertEqual(result["graph_digest"], graph_digest(original))
                self.assertTrue(all(labels[v] == value for v, value in prefix.items()))
                self.assertEqual(set(labels), set(original["vertices"]))
                self.assertTrue(all(type(v) is int for v in labels.values()))
                self.assertEqual(sorted(labels.values()), list(range(m + 1)))
                self.assertEqual(sorted(abs(labels[u] - labels[v]) for u, v in edges),
                                 list(range(1, m + 1)))
                certificate = verify_certificate(original, labels, graph_digest(original))
                self.assertTrue(certificate["valid"], certificate["errors"])
                with self.assertRaises(ValueError):
                    complete_nonadjacent_path(original, prefix, K, a)

    def test_invalid_domain(self):
        for bad in (True, False, 0, -1, 1.0, "1", None):
            for index in range(4):
                args = [1, 1, 1, 2]
                args[index] = bad
                with self.subTest(args=args), self.assertRaises(ValueError):
                    three_section_nonadjacent(*args)
        for args in ((1, 2, 1, 2), (1, 1, 1, 1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                three_section_nonadjacent(*args)

    def test_cli_target_binding_and_false_certificate(self):
        q, r, t, K = 3, 2, 1, 4
        spec = {"method": "three_section_nonadjacent",
                "parameters": {"q": q, "r": r, "t": t, "K": K},
                "profile": [[q], [r], [t]] + [[] for _ in range(K + 1)]}
        original, result = construction_input(spec, max_vertices=q+r+t+K+7)
        self.assertTrue(verify_certificate(original, result["labels"], graph_digest(original))["valid"])
        bad = dict(result["labels"])
        bad["s:3"] = bad["s:2"]
        self.assertFalse(verify_certificate(original, bad, graph_digest(original))["valid"])
        with self.assertRaises(ValueError):
            construction_input(spec, max_vertices=q+r+t+K+6)
        wrong = dict(spec, profile=[[r], [q], [t]] + [[] for _ in range(K + 1)])
        with self.assertRaisesRegex(ValueError, "different target"):
            construction_input(wrong)

    def test_cli_preflight_before_expansion_or_dispatch(self):
        cases = ({"q": 1, "r": 2, "t": 1, "K": 2},
                 {"q": 1, "r": 1, "t": 1, "K": 1},
                 {"q": True, "r": 1, "t": 1, "K": 2},
                 {"q": 1, "r": 1, "t": 0, "K": 2},
                 {"q": 1, "r": 1, "t": 1, "K": 2.0},
                 {"q": 10**12, "r": 1, "t": 1, "K": 2},
                 {"q": 1, "r": 1, "t": 1, "K": 2, "extra": 0},
                 {"q": 1, "r": 1, "t": 1})
        for params in cases:
            with self.subTest(params=params), patch("lcl.ingest.constructors.three_section_nonadjacent") as ctor:
                with patch("lcl.ingest.build_graph") as builder:
                    with self.assertRaises(ValueError):
                        construction_input({"method": "three_section_nonadjacent", "parameters": params,
                                            "profile": [[]]}, max_vertices=39)
                    ctor.assert_not_called()
                    builder.assert_not_called()
        with patch("lcl.ingest.constructors.three_section_nonadjacent") as ctor:
            with patch("lcl.ingest.build_graph") as builder:
                with self.assertRaises(ValueError):
                    construction_input({"method": "three_section_nonadjacent",
                                        "parameters": {"q": 20, "r": 10, "t": 2, "K": 2},
                                        "profile": [[]]}, max_vertices=39)
                ctor.assert_not_called()
                builder.assert_not_called()


if __name__ == "__main__":
    unittest.main()
