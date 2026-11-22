"""Freeze and execute the single K=1 named-tree query, with one host pin."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.budget import Limits
from lcl.model import build_graph, graph_digest
from lcl.records import (atomic_json, checked_record, environment, save_source_snapshot,
                         source_inventory, utc_now)
from lcl.search import prepare_domains, solve
from lcl.verify import verify_certificate, verify_graph

RUN_ID = "B4-THIRD-ZERO-HOST-K1-001-20261121"
BASE = "70664759ca1c3a6e5a6049aaff179e2a7e2990ec"
PROFILE = [[1], [1], [2], [2], [], []]
DIGEST = "fce6e5676ab825e344c5f217ace9855e4f1e5dc4c88f8a71e9563093daae1a9c"
PINS = {"b:2:0": 0}
LIMITS = {"max_nodes": 100_000, "time_limit": 5, "max_vertices": 16, "max_states": 20_000}
CAP = 2_000_000
EXPECTED_CONFIG = {
    "run_id": RUN_ID, "starting_commit": BASE, "profile": PROFILE, "original_graph_digest": DIGEST,
    "engine": "dfs", "count": False, "workers": 1, "new_queries": 1, "max_result_bytes": CAP,
    "limits": LIMITS, "dfs_uses_max_states": False, "pins": PINS, "domains": {},
    "historical_prefix": {"path": "evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1122-adjacent.json", "sha256_raw": "ccdf06602ee9b3f1b59b89be02adbe2e39188b11e8d0945331350994e45c0488", "graph_digest": "a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc"},
    "conditional_growth_checks": {"cases": [[3, 1], [4, 1]], "parameter_order": ["t", "K"],
                                  "workers": 1, "max_vertices": 18, "max_result_bytes": CAP,
                                  "search": False, "compare_same_t4_batch": True},
}
EXPECTED_CONTROL = {
    "s:0": 15, "s:1": 0, "s:2": 10, "s:3": 6, "s:4": 8, "s:5": 7,
    "b:0:0": 1, "l:0:0:0": 14, "b:1:0": 12, "l:1:0:0": 5,
    "b:2:0": 2, "l:2:0:0": 11, "l:2:0:1": 13, "b:3:0": 9, "l:3:0:0": 3, "l:3:0:1": 4,
}
RESULT_KEYS = {"method", "restrictions", "limits", "status", "exhausted", "count",
               "count_lower_bound", "witness", "nodes", "elapsed_seconds"}
OUTPUTS = ("query_start.json", "raw_result.json", "query_record.json", "query_error.json")


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    atomic_json(HERE / name, value, max_bytes=CAP)


def edges_with_multiplicity(edges):
    return Counter(tuple(sorted(e)) for e in edges)


def prepare():
    config = load(HERE / "config.json")
    require(config == EXPECTED_CONFIG and config["count"] is False
            and config["dfs_uses_max_states"] is False and sys.flags.optimize == 0
            and all(type(config[field]) is int for field in ("workers", "new_queries", "max_result_bytes"))
            and type(config["pins"]["b:2:0"]) is int, "exact declared inputs and limits")
    original = build_graph(PROFILE)
    spine = [f"s:{i}" for i in range(6)]
    expected_edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, terminals in enumerate((1, 1, 2, 2)):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        expected_edges.append((spine[i], center))
        for j in range(terminals):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            expected_edges.append((center, leaf))
    checked = verify_graph(original)
    require(original["spine"] == spine and original["roles"] == roles
            and Counter(original["vertices"]) == Counter(roles.keys())
            and edges_with_multiplicity(original["edges"]) == edges_with_multiplicity(expected_edges)
            and checked["valid"] and (checked["n"], checked["m"]) == (16, 15)
            and graph_digest(original) == checked["graph_digest"] == DIGEST, "complete original graph")
    allowed, restrictions = prepare_domains(original, config["pins"], config["domains"])
    expected = {v: {0} if v == "b:2:0" else set(range(16)) for v in original["vertices"]}
    require(allowed == expected and restrictions["scope"] == "restricted"
            and restrictions["pins"] == PINS and restrictions["domains"] == {}
            and restrictions["hidden_symmetry_reduction"] is False, "effective restrictions")
    limits = Limits.from_mapping(config["limits"])
    require(limits.to_dict() == LIMITS, "effective limits")
    return config, original, restrictions, limits, {v: sorted(values) for v, values in allowed.items()}


def derive_control(config, original):
    provenance = config["historical_prefix"]
    historical = ROOT / provenance["path"]
    require(sha(historical) == provenance["sha256_raw"], "retained prefix evidence bytes")
    saved = load(historical)
    prefix = build_graph(PROFILE[:-1])
    labels = saved["solver_result"]["witness"]
    require(saved["original_graph"] == prefix and saved["original_graph_digest"]
            == graph_digest(prefix) == provenance["graph_digest"] != DIGEST, "retained prefix identity")
    checked = verify_certificate(prefix, labels, provenance["graph_digest"])
    require(checked["valid"] and checked["n"] == 15 and labels["s:4"] == 7
            and all((labels[u] < 7) != (labels[v] < 7) for u, v in prefix["edges"]),
            "valid retained prefix for deriving the comparison")
    complete = {v: x + (x >= 7) for v, x in labels.items()}
    complete["s:5"] = 7
    cert = verify_certificate(original, complete, DIGEST)
    mismatch = {v: {"required": want, "actual": complete[v]} for v, want in PINS.items()
                if complete[v] != want}
    require(complete == EXPECTED_CONTROL and cert["valid"]
            and mismatch == {"b:2:0": {"required": 0, "actual": 2}}, "derived complete control")
    return {"kind": "newly_derived_complete_control", "historical_prefix": provenance,
            "derivation": {"retained_label_threshold": 7, "shift_at_or_above": 1,
                           "new_physical_vertex": "s:5", "new_label": 7},
            "original_graph_digest": DIGEST, "labels": complete, "certificate": cert,
            "new_pin_mismatches": mismatch, "historical_dfs_rerun": False, "new_search_queries": 0}


def probe_schema(config, original, restrictions, source, control):
    common = {"method": "dfs", "restrictions": restrictions, "limits": LIMITS,
              "nodes": 0, "elapsed_seconds": 0.0}
    probes = [
        ({**common, "status": "INCOMPLETE", "exhausted": False, "count": None,
          "count_lower_bound": 0, "witness": None, "reason": "interrupted"}, "INCOMPLETE"),
        ({**common, "status": "EXHAUSTED_NO_SOLUTION", "exhausted": True, "count": 0,
          "count_lower_bound": 0, "witness": None}, "EXHAUSTED_NO_SOLUTION"),
        ({**common, "status": "SAT", "exhausted": False, "count": None,
          "count_lower_bound": 1, "witness": control["labels"]}, "QUARANTINED"),
    ]
    for synthetic, classification in probes:
        receipt = checked_record(original, synthetic, config=config, source=source,
                                 expected_pins=PINS, expected_domains={})
        require(RESULT_KEYS <= synthetic.keys() and receipt["classification"] == classification
                and receipt["original_graph_digest"] == DIGEST
                and receipt["expected_restrictions"] == {"pins": PINS, "domains": {}}
                and len(json.dumps(receipt, allow_nan=False).encode()) < CAP,
                "synthetic receipt classification and schema")
    return {"synthetic_only": True, "solver_calls": 0,
            "checked": ["incomplete", "exhausted_zero", "pin_mismatch_quarantine"]}


def preflight():
    names = ("preflight.json", "original_graph.json", "control.json", "source", *OUTPUTS)
    require(not any((HERE / name).exists() for name in names), "preserve existing evidence")
    config, original, restrictions, limits, effective = prepare()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    diff = subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", "lcl"], cwd=ROOT, text=True)
    require(head == BASE and not diff, "accepted parent and unchanged core")
    control = derive_control(config, original)
    source = source_inventory(ROOT)
    probes = probe_schema(config, original, restrictions, source, control)
    save_source_snapshot(ROOT, HERE / "source", source)
    save("original_graph.json", original)
    save("control.json", control)
    plan = {"run_id": RUN_ID, "starting_commit": BASE, "prepared_utc": utc_now(),
            "config_sha256_raw": sha(HERE / "config.json"), "runner_sha256_raw": sha(Path(__file__)),
            "original_file_sha256_raw": sha(HERE / "original_graph.json"),
            "original_graph_digest": DIGEST, "control_sha256_raw": sha(HERE / "control.json"),
            "source": source, "runtime": {**environment(), "version": sys.version, "executable": sys.executable,
                                           "utf8_mode": sys.flags.utf8_mode},
            "restrictions": restrictions, "effective_domains": effective,
            "limits": limits.to_dict(), "dfs_uses_max_states": False, "max_result_bytes": CAP,
            "count_requested": False, "query_calls_at_preflight": 0, "schema_probe": probes,
            "expected_result_keys": sorted(RESULT_KEYS), "query_outputs": list(OUTPUTS),
            "conditional_targets": config["conditional_growth_checks"]}
    save("preflight.json", plan)
    print(json.dumps({"status": "READY", "queries_executed": 0, "derived_controls": 1,
                      "original_digest": DIGEST, "pins": PINS, "domains": {}, "effective_domains": effective,
                      "schema_probes": probes, "limits": LIMITS}))


def verify_status(result, restrictions):
    require(RESULT_KEYS <= result.keys() and result["method"] == "dfs"
            and result["restrictions"] == restrictions and result["limits"] == LIMITS
            and type(result["nodes"]) is int and 0 <= result["nodes"] <= LIMITS["max_nodes"]
            and result["elapsed_seconds"] >= 0, "raw result schema")
    status = result["status"]
    if status == "SAT":
        require(result["exhausted"] is False and result["count"] is None and result["count_lower_bound"] == 1
                and isinstance(result["witness"], dict) and "reason" not in result, "first witness semantics")
    elif status == "EXHAUSTED_NO_SOLUTION":
        require(result["exhausted"] is True and result["count"] == result["count_lower_bound"] == 0
                and result["witness"] is None and "reason" not in result, "normal exhaustion semantics")
    elif status == "INCOMPLETE":
        require(result["exhausted"] is False and result["count"] is None
                and result["reason"] in ("max_nodes", "time_limit", "interrupted"), "incomplete semantics")
    else:
        raise ValueError("unrecognized terminal status")
    return status


def execute():
    require(not any((HERE / name).exists() for name in OUTPUTS), "the single authorized query has started")
    config, original, restrictions, limits, effective = prepare()
    plan = load(HERE / "preflight.json")
    retained = HERE / "original_graph.json"
    require(load(retained) == original and plan["run_id"] == RUN_ID
            and plan["config_sha256_raw"] == sha(HERE / "config.json")
            and plan["runner_sha256_raw"] == sha(Path(__file__))
            and plan["original_file_sha256_raw"] == sha(retained)
            and plan["control_sha256_raw"] == sha(HERE / "control.json")
            and plan["source"] == source_inventory(ROOT)
            and all(sha(HERE / "source" / name) == value for name, value in plan["source"]["files"].items())
            and plan["restrictions"] == restrictions and plan["effective_domains"] == effective
            and plan["limits"] == limits.to_dict() and plan["dfs_uses_max_states"] is False
            and plan["query_calls_at_preflight"] == 0 and plan["schema_probe"]["synthetic_only"] is True
            and plan["schema_probe"]["solver_calls"] == 0 and plan["expected_result_keys"] == sorted(RESULT_KEYS)
            and plan["query_outputs"] == list(OUTPUTS)
            and plan["conditional_targets"] == config["conditional_growth_checks"], "frozen preflight")
    marker = {"run_id": RUN_ID, "started_utc": utc_now(), "scheduled_query_number": 1,
              "preflight_sha256_raw": sha(HERE / "preflight.json"), "count_requested": False}
    with (HERE / "query_start.json").open("xb") as out:
        out.write((json.dumps(marker, indent=2) + "\n").encode())
    try:
        # Sole solver invocation, using only the declared pin.
        result = solve(load(retained), pins=config["pins"], domains=config["domains"], limits=limits, count=False)
        save("raw_result.json", result)
        status = verify_status(result, restrictions)
        receipt = checked_record(original, result, config=config, source=plan["source"],
                                 expected_pins=PINS, expected_domains={},
                                 extra={"run_id": RUN_ID, "new_queries": 1, "search_mode": "first_witness",
                                        "preflight_sha256_raw": sha(HERE / "preflight.json"),
                                        "query_start_sha256_raw": sha(HERE / "query_start.json"),
                                        "raw_result_sha256_raw": sha(HERE / "raw_result.json")})
        save("query_record.json", receipt)
        require(receipt["classification"] == status, "quarantined original-bound result")
    except (Exception, KeyboardInterrupt):
        save("query_error.json", {"run_id": RUN_ID, "traceback": traceback.format_exc(),
                                  "raw_result_saved": (HERE / "raw_result.json").exists()})
        raise
    print(json.dumps({key: result[key] for key in
                      ("status", "nodes", "elapsed_seconds", "exhausted", "count", "count_lower_bound", "witness")}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--preflight"]:
        preflight()
    elif sys.argv[1:] == ["--execute"]:
        execute()
    else:
        raise SystemExit("use --preflight or --execute")
