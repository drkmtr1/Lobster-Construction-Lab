"""Independently audit the saved B4 certificates with exact integer arithmetic."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import sys


HERE = Path(__file__).resolve().parent


def require(predicate, description):
    if not predicate:
        raise ValueError(description)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_edges(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def audit_case(case):
    K = case["parameters"]["K"]
    graph = case["original_graph"]
    prefix, labels = case["prefix_labels"], case["full_labels"]
    spine = [f"s:{i}" for i in range(K + 5)]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = list(zip(spine, spine[1:]))
    for section, terminal_count in enumerate((1, 2, 1, 1)):
        stem = f"b:{section}:0"
        roles[stem] = {"kind": "branch", "section": section, "branch": 0}
        edges.append((spine[section], stem))
        for leaf_index in range(terminal_count):
            leaf = f"l:{section}:0:{leaf_index}"
            roles[leaf] = {"kind": "leaf", "section": section, "branch": 0, "leaf": leaf_index}
            edges.append((stem, leaf))
    profile = [[1], [2], [1], [1]] + [[] for _ in range(K + 1)]
    require(graph["profile"] == profile and graph["spine"] == spine and graph["roles"] == roles
            and Counter(graph["vertices"]) == Counter(roles.keys())
            and canonical_edges(graph["edges"]) == canonical_edges(edges), "original named target mismatch")
    identity = {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles),
                "edges": sorted(sorted(edge) for edge in edges)}
    original_digest = hashlib.sha256(json.dumps(identity, ensure_ascii=False, sort_keys=True,
                                                 separators=(",", ":")).encode()).hexdigest()
    require(original_digest == case["original_graph_digest"] and case["independent_certificate"]["valid"]
            and case["independent_certificate"]["graph_digest"] == original_digest, "certificate identity")

    low = ["b:0:0", "b:2:0", "s:1", "l:1:0:0", "l:1:0:1", "l:3:0:0", "s:3"]
    high = ["s:4", "b:3:0", "b:1:0", "s:2", "l:2:0:0", "l:0:0:0", "s:0"]
    expected = {vertex: label for label, vertex in enumerate(low)}
    expected.update({vertex: label for label, vertex in enumerate(high, start=K + 7)})
    require(prefix == expected and all(type(value) is int for value in prefix.values()),
            "exact named prefix mismatch")
    pending = spine[5:]
    tail = list(zip(spine[4:], pending))
    actual_tail = [edge for edge in edges if any(v in pending for v in edge)]
    crossing = [edge for edge in actual_tail if sum(v in pending for v in edge) == 1]
    require(set(roles) - set(prefix) == set(pending) and canonical_edges(actual_tail) == canonical_edges(tail)
            and canonical_edges(crossing) == canonical_edges([("s:4", "s:5")])
            and canonical_edges([case["crossing_edge"]]) == canonical_edges(crossing), "physical suffix mismatch")
    m = K + 13
    require(len(edges) == m and len(roles) == m + 1 and set(labels) == set(roles)
            and all(type(value) is int for value in labels.values())
            and sorted(labels.values()) == list(range(m + 1)), "full label bijection")
    require(all(labels[v] == value for v, value in prefix.items()), "prefix preservation")
    diffs = {edge: abs(labels[edge[0]] - labels[edge[1]]) for edge in edges}
    require(sorted(diffs.values()) == list(range(1, m + 1)), "full difference bijection")
    R = sorted(set(range(m + 1)) - set(prefix.values()))
    D = sorted(set(range(1, m + 1)) - {diffs[e] for e in edges if e not in actual_tail})
    require(R == list(range(7, K + 7)) and D == list(range(1, K + 1))
            and case["prefix_trace"] == {"active_vertex": "s:4", "active_label": K + 7,
                                         "unused_labels": R, "unused_differences": D}, "resource contract")
    suffix = [((7 + (j - 1) // 2) if j % 2 else (7 + K - j // 2)) for j in range(1, K + 1)]
    require([labels[v] for v in pending] == suffix and sorted(suffix) == R
            and [diffs[e] for e in tail] == case["tail_differences"] == list(reversed(D)), "path arithmetic")
    low.extend(pending[::2])
    high.extend(pending[1::2])
    p = len(low)
    require(case["alpha_low_class_size"] == p == 7 + (K + 1) // 2
            and Counter(case["alpha_low_vertices"]) == Counter(low)
            and Counter(case["alpha_high_vertices"]) == Counter(high)
            and sorted(labels[v] for v in low) == list(range(p))
            and sorted(labels[v] for v in high) == list(range(p, m + 1))
            and all((u in low) != (v in low) for u, v in edges), "full alpha cut")
    return {"K": K, "original_graph_digest": original_digest, "alpha_low_class_size": p, "status": "PASS"}


def main():
    regression = HERE / "regression_result.json"
    config_path = HERE / "config.json"
    data = json.loads(regression.read_bytes())
    config = json.loads(config_path.read_bytes())
    require(data["run_id"] == config["run_id"] and data["status"] == "PASS"
            and data["config_sha256_raw"] == digest(config_path)
            and data["audit_script_sha256_raw"] == digest(Path(__file__)), "input evidence identity")
    require(all(digest(HERE / "source" / name) == sha
                for name, sha in data["source_sha256_raw"].items()), "source snapshot identity")
    require([case["parameters"]["K"] for case in data["cases"]] == config["cases"]
            and data["case_count"] == len(config["cases"]) == 12, "declared target set")
    results = [audit_case(case) for case in data["cases"]]
    record = {"run_id": config["run_id"] + "-arithmetic-audit", "status": "PASS",
              "regression_sha256_raw": digest(regression), "audit_script_sha256_raw": digest(Path(__file__)),
              "same_certificate_count": len(results), "additional_completed_targets": 0,
              "environment": {"python": sys.version, "platform": platform.platform()}, "cases": results}
    output = (json.dumps(record, indent=2) + "\n").encode()
    require(len(output) <= config["max_output_bytes"], "record byte limit")
    with (HERE / "independent_audit_result.json").open("xb") as stream:
        stream.write(output)
    print(json.dumps({"status": "PASS", "same_certificate_count": len(results), "additional_completed_targets": 0}))


if __name__ == "__main__":
    main()
