"""Audit the saved named input, retained control, and first-witness SAT receipt.

This standard-library audit invokes no search and does not replay DFS.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROFILE = [[1], [1], [2], [2], []]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(name):
    return json.loads((HERE / name).read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def edge_multiset(edges):
    return Counter(tuple(sorted(e)) for e in edges)


def reconstruct():
    spine = [f"s:{i}" for i in range(5)]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    edges = list(zip(spine, spine[1:]))
    low = {"s:1", "s:3"}
    for i, terminals in enumerate((1, 1, 2, 2)):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        if i % 2 == 0:
            low.add(center)
        for j in range(terminals):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
            if i % 2 == 1:
                low.add(leaf)
    identity = {"profile": PROFILE, "spine": spine, "roles": roles,
                "vertices": sorted(roles), "edges": sorted(sorted(e) for e in edges)}
    return identity, low


def check_original(graph, expected):
    return (graph["profile"] == expected["profile"] and graph["spine"] == expected["spine"]
            and graph["roles"] == expected["roles"] and Counter(graph["vertices"]) == Counter(expected["vertices"])
            and edge_multiset(graph["edges"]) == edge_multiset(expected["edges"]))


def main():
    independent, low = reconstruct()
    high = set(independent["vertices"]) - low
    require(len(low) == 7 and len(high) == 8 and len(independent["edges"]) == 14
            and all((u in low) != (v in low) for u, v in independent["edges"]), "named graph and alpha cut")
    digest = canonical(independent)
    original = read("original_graph.json")
    config = read("config.json")
    plan = read("preflight.json")
    marker = read("query_start.json")
    raw = read("raw_result.json")
    record = read("query_record.json")
    control = read("control.json")
    require(check_original(original, independent) and check_original(record["original_graph"], independent)
            and config["profile"] == PROFILE and digest == config["original_graph_digest"]
            == record["original_graph_digest"] == plan["original_graph_digest"], "retained original graph identity")
    pins = {"b:2:0": 0, "s:4": 8}
    domains = {v: list(range(7)) for v in low} | {v: list(range(7, 15)) for v in high}
    declared = {"pins": pins, "domains": domains}
    limits = {"max_nodes": 100_000, "time_limit": 5, "max_vertices": 15, "max_states": 20_000}
    require(set(config["low_vertices"]) == low and set(config["high_vertices"]) == high
            and config["alpha_low_class_size"] == 7 and config["engine"] == "dfs"
            and config["pins"] == pins and config["domains"] == domains
            and raw["restrictions"]["scope"] == "restricted"
            and raw["restrictions"]["pins"] == pins and raw["restrictions"]["domains"] == domains
            and raw["restrictions"]["hidden_symmetry_reduction"] is False
            and raw["restrictions"] == plan["restrictions"] and record["expected_restrictions"] == declared,
            "exact two pins, full domains and no symmetry reduction")
    require(raw["limits"] == config["limits"] == plan["limits"] == limits and config["count"] is False
            and config["workers"] == config["new_queries"] == record["extra"]["new_queries"]
            == marker["scheduled_query_number"] == 1
            and config["max_result_bytes"] == plan["max_result_bytes"] == 2_000_000
            and marker["count_requested"] is plan["count_requested"] is False
            and config["dfs_uses_max_states"] is plan["dfs_uses_max_states"] is False
            and plan["schema_probe"].startswith("PASS:")
            and 0 < raw["nodes"] <= limits["max_nodes"] and 0 <= raw["elapsed_seconds"] < limits["time_limit"],
            "declared search mode, time, node and output limits")

    source = plan["source"]
    require(source == record["source"] and source["sha256"] == canonical(source["files"])
            and all(sha(HERE / "source" / name) == digest for name, digest in source["files"].items())
            and all(plan["runtime"][key] == value for key, value in record["environment"].items()),
            "raw source snapshot and runtime identities")
    require(record["config"] == config and record["config_sha256"] == canonical(config)
            and plan["config_sha256_raw"] == sha(HERE / "config.json")
            and plan["runner_sha256_raw"] == sha(HERE / "query.py")
            and plan["original_file_sha256_raw"] == sha(HERE / "original_graph.json")
            and plan["control_sha256_raw"] == sha(HERE / "control.json")
            and marker["preflight_sha256_raw"] == record["extra"]["preflight_sha256_raw"] == sha(HERE / "preflight.json")
            and record["extra"]["query_start_sha256_raw"] == sha(HERE / "query_start.json")
            and record["extra"]["raw_result_sha256_raw"] == sha(HERE / "raw_result.json")
            and config["run_id"] == plan["run_id"] == marker["run_id"] == record["extra"]["run_id"]
            and len(record["consistency_errors"]) == 0 and plan["query_calls_at_preflight"] == 0,
            "frozen config, original and result custody")
    required = set(plan["required_dfs_result_keys"])
    require(required <= raw.keys() and record["result"] == raw and raw["method"] == "dfs"
            and raw["status"] == record["classification"] == "SAT"
            and raw["exhausted"] is False and raw["count"] is None
            and raw["count_lower_bound"] == 1 and "reason" not in raw, "first-witness SAT receipt")
    witness = raw["witness"]
    require(isinstance(witness, dict) and set(witness) == set(independent["vertices"])
            and all(type(x) is int for x in witness.values())
            and sorted(witness.values()) == list(range(15))
            and all(witness[v] in domains[v] for v in witness)
            and all(witness[v] == x for v, x in pins.items()), "new seed labels, pins and domains")
    weights = [abs(witness[u] - witness[v]) for u, v in original["edges"]]
    require(sorted(weights) == list(range(1, 15))
            and record["certificate"]["graph_digest"] == digest
            and record["certificate"]["valid"] and record["certificate"]["edge_differences"] == weights,
            "new seed independent arithmetic and original-target checker")

    historical = ROOT / config["historical_control"]["path"]
    before = json.loads(historical.read_bytes())
    require(sha(historical) == config["historical_control"]["sha256_raw"]
            and control["historical_source"] == config["historical_control"]
            and check_original(before["original_graph"], independent), "historical control custody")
    values = control["labels"]
    differences = [abs(values[u] - values[v]) for u, v in original["edges"]]
    require(values == before["solver_result"]["witness"]
            and set(values) == set(independent["vertices"])
            and all(type(x) is int for x in values.values())
            and sorted(values.values()) == list(range(15)) and sorted(differences) == list(range(1, 15))
            and differences == control["certificate"]["edge_differences"]
            and control["certificate"]["valid"] and control["certificate"]["graph_digest"] == digest
            and all(values[v] in domains[v] for v in values) and values["s:4"] == 8
            and values["b:2:0"] == 1 and control["historical_dfs_rerun"] is False
            and control["new_pin_mismatches"] == {"b:2:0": {"actual": 1, "required": 0}},
            "historical graph, alpha labeling, and adverse new-pin check")
    inputs = ("config.json", "original_graph.json", "control.json", "preflight.json",
              "query_start.json", "raw_result.json", "query_record.json")
    require(all((HERE / name).stat().st_size <= config["max_result_bytes"] for name in inputs), "result byte cap")
    audit = {"status": "PASS", "run_id": config["run_id"] + "-arithmetic-custody-audit",
             "original_graph_digest": digest, "input_sha256_raw": {name: sha(HERE / name) for name in inputs},
             "audit_source_sha256_raw": sha(Path(__file__)), "environment": {"python": sys.version,
                    "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode},
             "retained_control_certificates_audited": 1, "saved_query_records_audited": 1,
             "new_seed_certificates_audited": 1, "additional_seed_certificates": 0,
             "completed_targets": 0, "additional_queries": 0,
             "scope": "Arithmetic audit of the same retained control, named query and verified seed; no search replay"}
    data = (json.dumps(audit, indent=2) + "\n").encode()
    require(len(data) <= config["max_result_bytes"], "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(data)
    print("PASS: 1 retained control and the same 1 verified seed, 0 added seeds, targets or queries")


if __name__ == "__main__":
    main()
