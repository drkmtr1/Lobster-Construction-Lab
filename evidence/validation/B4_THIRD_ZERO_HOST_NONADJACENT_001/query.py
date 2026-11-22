"""Freeze and execute exactly the declared named 1122 DFS query."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.budget import Limits
from lcl.model import build_graph, graph_digest
from lcl.records import atomic_json, checked_record, environment, save_source_snapshot, source_inventory, utc_now
from lcl.search import prepare_domains, solve
from lcl.verify import verify_certificate, verify_graph


PROFILE = [[1], [1], [2], [2], []]
GRAPH_DIGEST = "a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc"
BASE = "533f87793bb0dec19936bf888639e91f0e2cdf31"
LOW = ("s:1", "s:3", "b:0:0", "b:2:0", "l:1:0:0", "l:3:0:0", "l:3:0:1")
HIGH = ("s:0", "s:2", "s:4", "b:1:0", "b:3:0", "l:0:0:0", "l:2:0:0", "l:2:0:1")
PINS = {"b:2:0": 0, "s:4": 8}
DOMAINS = {v: list(range(7)) for v in LOW} | {v: list(range(7, 15)) for v in HIGH}
LIMITS = {"max_nodes": 100_000, "time_limit": 5, "max_vertices": 15, "max_states": 20_000}
OUTPUT_LIMIT = 2_000_000
CONTROL = {"s:0": 13, "s:1": 0, "s:2": 7, "s:3": 6, "s:4": 8, "b:0:0": 3, "l:0:0:0": 11,
           "b:1:0": 14, "l:1:0:0": 2, "b:2:0": 1, "l:2:0:0": 10, "l:2:0:1": 12,
           "b:3:0": 9, "l:3:0:0": 4, "l:3:0:1": 5}
RESULT_KEYS = {"method", "restrictions", "limits", "status", "exhausted", "count",
               "count_lower_bound", "witness", "nodes", "elapsed_seconds"}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, item):
    atomic_json(HERE / name, item, max_bytes=OUTPUT_LIMIT)


def prepare():
    config = read(HERE / "config.json")
    expected = {
        "run_id": "B4-THIRD-ZERO-HOST-NONADJACENT-001-20261121", "starting_commit": BASE,
        "profile": PROFILE, "original_graph_digest": GRAPH_DIGEST, "engine": "dfs",
        "count": False, "workers": 1, "new_queries": 1, "max_result_bytes": OUTPUT_LIMIT,
        "limits": LIMITS, "dfs_uses_max_states": False, "alpha_low_class_size": 7, "low_vertices": list(LOW),
        "high_vertices": list(HIGH), "pins": PINS, "domains": DOMAINS,
        "historical_control": {"path": "evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1122-nonadjacent.json",
                               "sha256_raw": "ea65c74546009bda6bf4728d03017f0975d2b42d84b890fc5aae7ad358189677"},
        "conditional_direct_checks": {"cases": [[2, 2], [3, 3], [4, 4], [3, 5]], "parameter_order": ["t", "K"],
                                      "workers": 1, "max_vertices": 21, "max_result_bytes": OUTPUT_LIMIT,
                                      "search": False},
    }
    require(config == expected and config["count"] is False and sys.flags.optimize == 0,
            "configuration, exact first-witness flag, or interpreter differs")
    for field in ("workers", "new_queries", "max_result_bytes", "alpha_low_class_size"):
        require(type(config[field]) is int, f"invalid integer type for {field}")
    original = build_graph(PROFILE)
    expected_edges = [(f"s:{i}", f"s:{i + 1}") for i in range(4)]
    expected_edges += [(f"s:{i}", f"b:{i}:0") for i in range(4)]
    expected_edges += [(f"b:{i}:0", f"l:{i}:0:{j}")
                       for i, count in enumerate((1, 1, 2, 2)) for j in range(count)]
    require(original["spine"] == [f"s:{i}" for i in range(5)]
            and Counter(tuple(sorted(e)) for e in original["edges"])
            == Counter(tuple(sorted(e)) for e in expected_edges), "exact original incidences")
    graph_check = verify_graph(original)
    require(graph_check["valid"] and graph_check["n"] == 15 and graph_check["m"] == 14
            and graph_digest(original) == graph_check["graph_digest"] == GRAPH_DIGEST, "original graph identity")
    require(Counter(LOW + HIGH) == Counter(original["vertices"])
            and all((u in LOW) != (v in LOW) for u, v in original["edges"]), "physical alpha cut")
    allowed, restrictions = prepare_domains(original, config["pins"], config["domains"])
    require(restrictions["pins"] == PINS and restrictions["domains"] == DOMAINS
            and restrictions["hidden_symmetry_reduction"] is False
            and all(allowed[v] == ({PINS[v]} if v in PINS else set(DOMAINS[v])) for v in original["vertices"]),
            "effective restrictions")
    limits = Limits.from_mapping(config["limits"])
    require(limits.to_dict() == LIMITS, "effective limits")
    return config, original, restrictions, limits


def preflight():
    for name in ("preflight.json", "original_graph.json", "control.json", "source",
                 "query_start.json", "raw_result.json", "query_record.json"):
        require(not (HERE / name).exists(), "evidence already exists; preserve the declared query identity")
    config, original, restrictions, limits = prepare()
    reported = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(reported == BASE, "accepted starting checkout")
    changes = subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", "lcl"], cwd=ROOT, text=True)
    require(not changes, "unchanged LCL source required")
    metadata = config["historical_control"]
    path = ROOT / metadata["path"]
    require(sha(path) == metadata["sha256_raw"], "retained historical bytes")
    old = read(path)
    require(old["original_graph"] == original and old["original_graph_digest"] == GRAPH_DIGEST
            and old["solver_result"]["witness"] == CONTROL, "historical witness and original")
    verified = verify_certificate(original, CONTROL, GRAPH_DIGEST)
    require(verified["valid"] and all(CONTROL[v] in DOMAINS[v] for v in original["vertices"]),
            "retained control certificate and alpha domains")
    mismatch = {v: {"required": pin, "actual": CONTROL[v]} for v, pin in PINS.items() if CONTROL[v] != pin}
    require(mismatch == {"b:2:0": {"required": 0, "actual": 1}}, "expected pin failure")

    source = source_inventory(ROOT)
    # Exercise receipt serialization and the original-bound schema without a search.
    probe = {"method": "dfs", "status": "INCOMPLETE", "exhausted": False, "count": None,
             "count_lower_bound": 0, "witness": None, "nodes": 0, "elapsed_seconds": 0.0,
             "reason": "interrupted", "restrictions": restrictions, "limits": limits.to_dict()}
    receipt = checked_record(original, probe, config=config, source=source,
                             expected_pins=PINS, expected_domains=DOMAINS)
    require(RESULT_KEYS <= probe.keys() and receipt["classification"] == "INCOMPLETE"
            and receipt["certificate"] is None and receipt["consistency_errors"] == []
            and receipt["original_graph_digest"] == GRAPH_DIGEST
            and receipt["expected_restrictions"] == {"pins": PINS, "domains": DOMAINS}
            and len(json.dumps(receipt, allow_nan=False).encode()) < OUTPUT_LIMIT,
            "preflight record shape and serialization")
    save_source_snapshot(ROOT, HERE / "source", source)
    save("original_graph.json", original)
    save("control.json", {"kind": "retained_1122_control", "historical_source": metadata,
                          "labels": CONTROL, "certificate": verified, "alpha_low_class_size": 7,
                          "original_graph_digest": GRAPH_DIGEST, "new_pin_mismatches": mismatch,
                          "historical_dfs_rerun": False, "new_search_queries": 0})
    plan = {"run_id": config["run_id"], "prepared_utc": utc_now(), "starting_commit": BASE,
            "config_sha256_raw": sha(HERE / "config.json"), "runner_sha256_raw": sha(Path(__file__)),
            "original_file_sha256_raw": sha(HERE / "original_graph.json"),
            "control_sha256_raw": sha(HERE / "control.json"), "original_graph_digest": GRAPH_DIGEST,
            "source": source, "runtime": {**environment(), "executable": sys.executable,
                                           "version": sys.version, "utf8_mode": sys.flags.utf8_mode},
            "restrictions": restrictions, "limits": limits.to_dict(),
            "max_result_bytes": OUTPUT_LIMIT, "count_requested": False,
            "query_calls_at_preflight": 0, "required_dfs_result_keys": sorted(RESULT_KEYS),
            "schema_probe": "PASS: in-memory synthetic receipt only, zero DFS calls",
            "conditional_targets": config["conditional_direct_checks"], "dfs_uses_max_states": False,
            "query_outputs": ["query_start.json", "raw_result.json", "query_record.json"]}
    save("preflight.json", plan)
    print(json.dumps({"status": "READY", "queries_executed": 0, "pins": PINS, "low": LOW,
                      "high": HIGH, "limits": LIMITS, "control_matches_new_pins": False}))


def execute():
    config, original, restrictions, limits = prepare()
    plan = read(HERE / "preflight.json")
    original_path = HERE / "original_graph.json"
    require(original == read(original_path) and plan["run_id"] == config["run_id"]
            and plan["runner_sha256_raw"] == sha(Path(__file__))
            and plan["config_sha256_raw"] == sha(HERE / "config.json")
            and plan["original_file_sha256_raw"] == sha(original_path)
            and plan["control_sha256_raw"] == sha(HERE / "control.json")
            and plan["source"] == source_inventory(ROOT)
            and all(sha(HERE / "source" / name) == expected
                    for name, expected in plan["source"]["files"].items())
            and plan["restrictions"] == restrictions and plan["limits"] == limits.to_dict()
            and plan["required_dfs_result_keys"] == sorted(RESULT_KEYS)
            and plan["query_outputs"] == ["query_start.json", "raw_result.json", "query_record.json"]
            and plan["query_calls_at_preflight"] == 0
            and plan["schema_probe"].startswith("PASS:")
            and plan["conditional_targets"] == config["conditional_direct_checks"]
            and plan["dfs_uses_max_states"] is False, "saved preflight and source identity")
    for name in plan["query_outputs"]:
        require(not (HERE / name).exists(), "single authorized query already started; do not rerun")
    marker = {"run_id": config["run_id"], "preflight_sha256_raw": sha(HERE / "preflight.json"),
              "scheduled_query_number": 1, "started_utc": utc_now(), "count_requested": False}
    encoded = (json.dumps(marker, indent=2) + "\n").encode()
    with (HERE / "query_start.json").open("xb") as f:
        f.write(encoded)

    # The only search invocation in the task.
    result = solve(read(original_path), pins=config["pins"], domains=config["domains"],
                   limits=limits, count=False)
    save("raw_result.json", result)
    invariants = (RESULT_KEYS <= result.keys() and result["method"] == "dfs"
                  and result["restrictions"] == restrictions and result["limits"] == LIMITS
                  and type(result["nodes"]) is int and 0 <= result["nodes"] <= LIMITS["max_nodes"]
                  and result["elapsed_seconds"] >= 0)
    require(invariants, "raw result fields or declared limits")
    status = result["status"]
    if status == "SAT":
        require(result["exhausted"] is False and result["count"] is None
                and result["count_lower_bound"] == 1 and isinstance(result["witness"], dict),
                "first-witness status")
    elif status == "EXHAUSTED_NO_SOLUTION":
        require(result["exhausted"] is True and result["count"] == result["count_lower_bound"] == 0
                and result["witness"] is None and "reason" not in result, "exhaustion status")
    elif status == "INCOMPLETE":
        require(result["exhausted"] is False and result["count"] is None
                and result["reason"] in ("max_nodes", "time_limit", "interrupted"), "interruption status")
    else:
        raise ValueError("unexpected terminal status")
    record = checked_record(original, result, config=config, source=plan["source"],
                            extra={"run_id": config["run_id"], "new_queries": 1, "search_mode": "first_witness",
                                   "preflight_sha256_raw": sha(HERE / "preflight.json"),
                                   "query_start_sha256_raw": sha(HERE / "query_start.json"),
                                   "raw_result_sha256_raw": sha(HERE / "raw_result.json")},
                            expected_pins=config["pins"], expected_domains=config["domains"])
    save("query_record.json", record)
    require(record["classification"] == status, "original-target evidence quarantined")
    print(json.dumps({"status": status, "nodes": result["nodes"],
                      "elapsed_seconds": result["elapsed_seconds"], "exhausted": result["exhausted"],
                      "exact_count": result["count"], "witness": result["witness"]}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--preflight"]:
        preflight()
    elif sys.argv[1:] == ["--execute"]:
        execute()
    else:
        raise SystemExit("use --preflight or --execute")
