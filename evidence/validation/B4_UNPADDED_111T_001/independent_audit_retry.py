"""Audit the same saved certificates with integer arithmetic and no LCL imports."""
import hashlib
import json
from pathlib import Path
import platform
import sys


HERE = Path(__file__).resolve().parent


def require(predicate, description):
    if not predicate:
        raise ValueError(description)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_path(K):
    bases = {2: [3, 1, 0], 3: [4, 1, 0, 2], 4: [5, 1, 2, 0, 3]}
    if K in bases:
        return bases[K]
    return [K + 1, 1, K - 1] + [K - 2 - value for value in normalized_path(K - 3)]


def audit_target(case):
    t, K = case["parameters"]["t"], case["parameters"]["K"]
    graph = case["original_graph"]
    prefix, full = case["prefix_labels"], case["full_labels"]
    spine = [f"s:{i}" for i in range(K + 5)]
    vertices = spine[:]
    edges = list(zip(spine, spine[1:]))
    for i, count in enumerate((1, 1, 1, t)):
        center = f"b:{i}:0"
        vertices.append(center)
        edges.append((spine[i], center))
        for j in range(count):
            leaf = f"l:{i}:0:{j}"
            vertices.append(leaf)
            edges.append((center, leaf))
    require(graph["profile"] == [[1], [1], [1], [t]] + [[] for _ in range(K + 1)]
            and sorted(graph["vertices"]) == sorted(vertices) and graph["spine"] == spine
            and [tuple(edge) for edge in graph["edges"]] == edges, "named target mismatch")
    m = t + K + 11
    require(len(edges) == m and len(vertices) == m + 1 and set(full) == set(vertices)
            and all(type(value) is int for value in full.values())
            and sorted(full.values()) == list(range(m + 1)), "full vertex-label partition")
    weights = {edge: abs(full[edge[0]] - full[edge[1]]) for edge in edges}
    require(sorted(weights.values()) == list(range(1, m + 1)), "full original-edge partition")
    require(case["independent_certificate"]["valid"]
            and case["independent_certificate"]["graph_digest"] == case["original_graph_digest"],
            "original certificate identity")

    fourth_leaves = [f"l:3:0:{j}" for j in range(t)]
    if K == 1:
        low = ["b:0:0", "l:1:0:0", "s:1", "b:2:0", "s:5", "s:3"] + fourth_leaves
        high = ["b:3:0", "s:4", "l:2:0:0", "s:2", "b:1:0", "l:0:0:0", "s:0"]
        expected_full = {v: value for value, v in enumerate(low + high)}
        expected_prefix = {v: value for v, value in expected_full.items() if v != "s:5"}
        require(case["alpha_low_class_size"] == len(low) == t + 6
                and all((u in low) != (v in low) for u, v in edges), "alpha cut or classes")
        R, D = [4], [t + 3]
    else:
        low = ["l:1:0:0", "s:1", "b:0:0", "b:2:0", "s:3"] + fourth_leaves
        high = ["b:3:0", "s:4", "s:2", "l:2:0:0", "l:0:0:0", "s:0", "b:1:0"]
        a = len(low)
        expected_prefix = {v: value for value, v in enumerate(low)}
        expected_prefix.update({v: value for value, v in enumerate(high, start=a + K)})
        expected_full = dict(expected_prefix)
        pattern = normalized_path(K)
        require(expected_prefix["s:4"] == a + pattern[0], "normalized physical port")
        expected_full.update({v: a + x for v, x in zip(spine[5:], pattern[1:])})
        require(case["alpha_low_class_size"] is None, "unexpected completed-alpha evidence")
        R, D = list(range(a, a + K)), list(range(1, K + 1))
    require(prefix == expected_prefix and full == expected_full, "exact named assignments")
    require(case["prefix_interface"] == {"active_vertex": "s:4", "active_label": full["s:4"],
                                          "unused_labels": R, "unused_differences": D},
            "saved port or inventory differs from calculated interface")
    unfinished = [e for e in edges if e[0] not in prefix or e[1] not in prefix]
    crossing = [e for e in unfinished if (e[0] in prefix) != (e[1] in prefix)]
    require(unfinished == list(zip(spine[4:], spine[5:])) == [tuple(e) for e in case["unfinished_edges"]]
            and crossing == [("s:4", "s:5")] == [tuple(case["crossing_edge"])], "original remaining incidence")
    require(sorted(set(range(m + 1)) - set(prefix.values())) == R
            and sorted(weights[e] for e in unfinished) == D
            and [weights[e] for e in unfinished] == case["tail_differences"],
            "arithmetic resource or completion mismatch")
    return {"parameters": case["parameters"], "original_graph_digest": case["original_graph_digest"],
            "status": "PASS"}


def main():
    regression = HERE / "regression_result.json"
    data = json.loads(regression.read_bytes())
    config_file = HERE / "config.json"
    config = json.loads(config_file.read_bytes())
    require(data["status"] == "PASS" and data["config_sha256_raw"] == sha256(config_file)
            and data["audit_script_sha256_raw"] == sha256(HERE / "independent_audit.py"),
            "evidence input identity")
    require(all(sha256(HERE / "source" / name) == expected
                for name, expected in data["source_sha256_raw"].items()), "source snapshot identity")
    require([[case["parameters"][p] for p in config["parameter_order"]] for case in data["cases"]]
            == config["cases"] and data["case_count"] == len(config["cases"]) == 12, "declared targets")
    result = {"run_id": config["run_id"] + "-same-certificate-audit",
              "regression_sha256_raw": sha256(regression), "script_sha256_raw": sha256(Path(__file__)),
              "replaces_audit_sha256_raw": sha256(HERE / "independent_audit.py"),
              "environment": {"python": sys.version, "platform": platform.platform()},
              "status": "PASS", "same_certificate_count": 12, "additional_completed_targets": 0,
              "cases": [audit_target(case) for case in data["cases"]]}
    encoded = (json.dumps(result, indent=2) + "\n").encode()
    require(len(encoded) <= config["limits"]["max_output_bytes"], "audit output exceeds 2 MB")
    with (HERE / "independent_audit_result.json").open("xb") as stream:
        stream.write(encoded)
    print(json.dumps({"status": "PASS", "same_certificate_count": 12, "additional_completed_targets": 0}))


if __name__ == "__main__":
    main()
