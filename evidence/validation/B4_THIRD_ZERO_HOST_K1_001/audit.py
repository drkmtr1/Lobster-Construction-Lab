"""Independent arithmetic and custody audit for the saved K1 control and query."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TARGET = [[1], [1], [2], [2], [], []]
COMPLETE_DIGEST = "fce6e5676ab825e344c5f217ace9855e4f1e5dc4c88f8a71e9563093daae1a9c"
PREFIX_DIGEST = "a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc"


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def raw_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    return hashlib.sha256(data).hexdigest()


def named_edges(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def reconstruct(profile):
    spine = [f"s:{i}" for i in range(len(profile))]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, section in enumerate(profile):
        for j, leaves in enumerate(section):
            center = f"b:{i}:{j}"
            roles[center] = {"kind": "branch", "section": i, "branch": j}
            edges.append((spine[i], center))
            for k in range(leaves):
                leaf = f"l:{i}:{j}:{k}"
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
                edges.append((center, leaf))
    return {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles),
            "edges": sorted(sorted(edge) for edge in edges)}


def matches(original, expected):
    return (all(original[k] == expected[k] for k in ("profile", "spine", "roles"))
            and Counter(original["vertices"]) == Counter(expected["vertices"])
            and named_edges(original["edges"]) == named_edges(expected["edges"]))


def ledger(original, labels, expected):
    m = len(original["edges"])
    need(matches(original, expected) and set(labels) == set(expected["vertices"])
         and all(type(x) is int for x in labels.values())
         and sorted(labels.values()) == list(range(m + 1)), "exact graph and full label alphabet")
    weights = [abs(labels[u] - labels[v]) for u, v in original["edges"]]
    need(sorted(weights) == list(range(1, m + 1)), "original edge-difference bijection")
    return weights


def main():
    config = read(HERE / "config.json")
    preflight = read(HERE / "preflight.json")
    control = read(HERE / "control.json")
    original = read(HERE / "original_graph.json")
    marker = read(HERE / "query_start.json")
    raw = read(HERE / "raw_result.json")
    receipt = read(HERE / "query_record.json")
    expected = reconstruct(TARGET)
    digest = canonical(expected)
    need(digest == COMPLETE_DIGEST == preflight["original_graph_digest"]
         == config["original_graph_digest"] == receipt["original_graph_digest"]
         and config["profile"] == TARGET and (len(expected["vertices"]), len(expected["edges"])) == (16, 15)
         and matches(original, expected) and matches(receipt["original_graph"], expected),
         "exact complete original and distinct digest")
    pins = {"b:2:0": 0}
    wanted = {v: [0] if v in pins else list(range(16)) for v in expected["vertices"]}
    restrictions = {"pins": pins, "domains": {}}
    need(config["pins"] == pins and config["domains"] == {} and preflight["effective_domains"] == wanted
         and receipt["expected_restrictions"] == restrictions and raw["restrictions"] == preflight["restrictions"]
         and all(raw["restrictions"][key] == value for key, value in restrictions.items())
         and raw["restrictions"]["scope"] == "restricted" and raw["restrictions"]["hidden_symmetry_reduction"] is False
         and "no symmetry quotient" in raw["restrictions"]["count_convention"],
         "only the zero-host pin and full effective alphabet elsewhere")

    limits = {"max_nodes": 100_000, "time_limit": 5, "max_vertices": 16, "max_states": 20_000}
    need(raw["limits"] == preflight["limits"] == config["limits"] == limits
         and config["engine"] == raw["method"] == "dfs"
         and marker["count_requested"] is preflight["count_requested"] is config["count"] is False
         and config["dfs_uses_max_states"] is preflight["dfs_uses_max_states"] is False
         and config["workers"] == config["new_queries"] == marker["scheduled_query_number"]
         == receipt["extra"]["new_queries"] == 1
         and config["max_result_bytes"] == preflight["max_result_bytes"] == 2_000_000
         and preflight["conditional_targets"] == config["conditional_growth_checks"]
         and preflight["schema_probe"]["synthetic_only"] is True
         and preflight["schema_probe"]["solver_calls"] == preflight["query_calls_at_preflight"] == 0
         and receipt["extra"]["search_mode"] == "first_witness", "single query and exact caps")
    need(raw == receipt["result"] and raw["status"] == receipt["classification"] == "INCOMPLETE"
         and set(preflight["expected_result_keys"]) <= raw.keys()
         and raw["nodes"] == limits["max_nodes"] and raw["reason"] == "max_nodes"
         and 0 <= raw["elapsed_seconds"] < limits["time_limit"] and raw["exhausted"] is False
         and raw["count"] is None and raw["count_lower_bound"] == 0 and raw["witness"] is None
         and receipt["certificate"] is None and receipt["consistency_errors"] == [],
         "actual incomplete node-limit receipt without a witness or exact count")

    prior = ROOT / config["historical_prefix"]["path"]
    historical = read(prior)
    expected_prefix = reconstruct(TARGET[:-1])
    before = historical["solver_result"]["witness"]
    need(control["historical_prefix"] == config["historical_prefix"]
         and raw_digest(prior) == control["historical_prefix"]["sha256_raw"]
         and canonical(expected_prefix) == historical["original_graph_digest"] == PREFIX_DIGEST != digest,
         "retained 15-vertex prefix identity and provenance")
    ledger(historical["original_graph"], before, expected_prefix)
    need(before["s:4"] == 7 and all((before[u] < 7) != (before[v] < 7)
                                  for u, v in expected_prefix["edges"]), "retained adjacent prefix alpha condition")
    after = {v: x + (x >= 7) for v, x in before.items()}
    after["s:5"] = 7
    weights = ledger(original, control["labels"], expected)
    need(control["kind"] == "newly_derived_complete_control" and control["labels"] == after
         and control["derivation"] == {"retained_label_threshold": 7, "shift_at_or_above": 1,
                                       "new_physical_vertex": "s:5", "new_label": 7}
         and control["certificate"]["valid"] and control["certificate"]["graph_digest"] == digest
         and control["certificate"]["edge_differences"] == weights
         and control["new_pin_mismatches"] == {"b:2:0": {"actual": 2, "required": 0}}
         and after["b:2:0"] == 2 and control["historical_dfs_rerun"] is False
         and control["new_search_queries"] == 0, "one complete derived comparison control")

    source = preflight["source"]
    need(source == receipt["source"] and source["sha256"] == canonical(source["files"])
         and all(raw_digest(HERE / "source" / name) == value for name, value in source["files"].items())
         and all(preflight["runtime"][key] == value for key, value in receipt["environment"].items()),
         "source bytes and runtime identity")
    extra = receipt["extra"]
    need(config == receipt["config"] and receipt["config_sha256"] == canonical(config)
         and preflight["config_sha256_raw"] == raw_digest(HERE / "config.json")
         and preflight["runner_sha256_raw"] == raw_digest(HERE / "query.py")
         and preflight["original_file_sha256_raw"] == raw_digest(HERE / "original_graph.json")
         and preflight["control_sha256_raw"] == raw_digest(HERE / "control.json")
         and extra["preflight_sha256_raw"] == marker["preflight_sha256_raw"] == raw_digest(HERE / "preflight.json")
         and extra["query_start_sha256_raw"] == raw_digest(HERE / "query_start.json")
         and extra["raw_result_sha256_raw"] == raw_digest(HERE / "raw_result.json")
         and config["run_id"] == preflight["run_id"] == marker["run_id"] == extra["run_id"],
         "immutable evidence links")
    need(not (HERE / "growth_checks").exists() and not (HERE / "query_error.json").exists(),
         "no growth activation or reporting error")
    names = ("config.json", "original_graph.json", "preflight.json", "control.json",
             "query_start.json", "raw_result.json", "query_record.json")
    cap = config["max_result_bytes"]
    need(all((HERE / name).stat().st_size <= cap for name in names), "byte limit")
    result = {"status": "PASS", "run_id": config["run_id"] + "-custody-audit",
              "original_graph_digest": digest, "input_sha256_raw": {name: raw_digest(HERE / name) for name in names},
              "audit_source_sha256_raw": raw_digest(Path(__file__)),
              "runtime": {"python": sys.version, "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode},
              "derived_complete_controls_audited": 1, "saved_query_records_audited": 1,
              "distinct_complete_profiles_audited": 1, "new_verified_seeds": 0, "growth_targets": 0,
              "additional_queries": 0, "additional_target_profiles": 0,
              "scope": "Arithmetic and original-identity verification of the same saved control and incomplete receipt"}
    data = (json.dumps(result, indent=2) + "\n").encode()
    need(len(data) <= cap, "audit result byte limit")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(data)
    print("PASS: one derived control and one incomplete receipt; 0 added queries or target profiles")


if __name__ == "__main__":
    main()
