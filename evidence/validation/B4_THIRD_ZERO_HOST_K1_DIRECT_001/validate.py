"""Verify the supplied core and exactly four direct K=1 constructions."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest
from lcl.records import atomic_json, environment, save_source_snapshot, source_inventory, utc_now
from lcl.verify import verify_certificate, verify_graph, verify_partial


CORE = {"s:0": 7, "s:1": 0, "s:2": 12, "s:3": 1, "s:4": 10, "s:5": 4,
        "b:0:0": 3, "l:0:0:0": 2, "b:1:0": 8, "l:1:0:0": 5,
        "b:3:0": 11, "l:3:0:0": 9, "l:3:0:1": 6}
FIXED = {"s:0": 8, "s:1": 1, "s:2": 13, "s:3": 2, "s:4": 11, "s:5": 5,
         "b:0:0": 4, "l:0:0:0": 3, "b:1:0": 9, "l:1:0:0": 6, "b:2:0": 0,
         "b:3:0": 12, "l:3:0:0": 10, "l:3:0:1": 7}
RESTORED = [["s:2", "b:2:0"], ["b:2:0", "l:2:0:0"], ["b:2:0", "l:2:0:1"]]
CORE_WEIGHTS = [7, 12, 11, 9, 6, 4, 1, 8, 3, 10, 2, 5]
EXPECTED = {
    "run_id": "B4-THIRD-ZERO-HOST-K1-DIRECT-001-20261121",
    "starting_commit": "4aa22d42c1b7c609bfa8d0b691ba16c951383fe6",
    "workers": 1,
    "max_vertices": 18,
    "max_result_bytes": 2000000,
    "new_solver_queries": 0,
    "enumeration": False,
    "auxiliary_core": {
        "profile": [
            [
                1
            ],
            [
                1
            ],
            [],
            [
                2
            ],
            [],
            []
        ],
        "graph_digest": "aa0e6e159d15dd8aa9003403e47f99bcf7607511fb0ea0accf76b505cf3ebe36"
    },
    "completed_seed_graph_digest": "fce6e5676ab825e344c5f217ace9855e4f1e5dc4c88f8a71e9563093daae1a9c",
    "completed_cases": [
        [
            1,
            1
        ],
        [
            2,
            1
        ],
        [
            3,
            1
        ],
        [
            4,
            1
        ]
    ],
    "parameter_order": [
        "t",
        "K"
    ],
    "batch_comparison": [
        4,
        1
    ],
    "terminal_swap_arithmetic_check": False,
    "historical_incomplete_receipt": {
        "raw": "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/raw_result.json",
        "raw_sha256": "9901eecb61366cf2329ebd5639e1a8c2cd738a08d5dc48da41126a6cef201b49",
        "bound": "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json",
        "bound_sha256": "b71cf1dc26700648507e8c2d9769b44e1d4536df6b788438930c2d5585679ff6"
    }
}
HISTORY_STATUS = {"status": "INCOMPLETE", "reason": "max_nodes", "nodes": 100_000,
                  "exhausted": False, "count": None, "count_lower_bound": 0, "witness": None}
PROOF = "research/B4_THIRD_ZERO_HOST_K1_DIRECT.md"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_multiset(edges):
    return Counter(tuple(sorted(e)) for e in edges)


def retain_original(output, filename, profile):
    original = build_graph(profile)
    checked = verify_graph(original)
    require(checked["valid"] and checked["n"] <= EXPECTED["max_vertices"]
            and checked["graph_digest"] == graph_digest(original)
            and original["profile"] == profile, "declared checked original")
    path = output / "originals" / filename
    atomic_json(path, original, max_bytes=EXPECTED["max_result_bytes"])
    return {"path": path.relative_to(output).as_posix(), "sha256_raw": sha(path),
            "graph_digest": checked["graph_digest"], "vertices": checked["n"], "edges": checked["m"]}


def named_ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]


def check_core(graph, original):
    digest = EXPECTED["auxiliary_core"]["graph_digest"]
    require(original["graph_digest"] == digest and (original["vertices"], original["edges"]) == (13, 12),
            "rooted core identity")
    report = verify_certificate(graph, CORE, digest)
    ledger = named_ledger(graph, CORE)
    require(report["valid"] and CORE["s:2"] == 12
            and [row["difference"] for row in ledger] == CORE_WEIGHTS == report["edge_differences"],
            "rooted core certificate and original ledger")
    return {"kind": "auxiliary_rooted_core", "original": original, "labels": CORE,
            "root": {"vertex": "s:2", "label": 12}, "edge_ledger": ledger, "certificate": report}


def third_leaves(t):
    require(type(t) is int and t >= 1, "t must be a positive exact integer")
    return {f"l:2:0:{j}": 14 + j for j in range(t)}


def check_lift(core, seed_graph, seed_labels):
    require(graph_digest(seed_graph) == EXPECTED["completed_seed_graph_digest"]
            and set(seed_graph["vertices"]) - CORE.keys() == {"b:2:0", "l:2:0:0", "l:2:0:1"}
            and set(CORE) < set(seed_graph["vertices"])
            and edge_multiset(seed_graph["edges"]) == edge_multiset(core["edges"] + RESTORED),
            "exact restored original graph")
    translated = {v: x + 1 for v, x in CORE.items()}
    restored = {"b:2:0": 0, "l:2:0:0": 14, "l:2:0:1": 15}
    require(seed_labels == {**translated, **restored}
            and sorted(abs(seed_labels[u] - seed_labels[v]) for u, v in RESTORED) == [13, 14, 15]
            and all(seed_labels[v] - 1 == CORE[v] for v in core["vertices"]),
            "pointwise lift and reverse translation")
    return {"core_to_seed_translation": 1, "restored_labels": restored, "restored_edges": RESTORED,
            "restored_differences": [13, 14, 15], "reverse_translation": -1, "verified": True}


def check_case(t, graph, original):
    m = t + 13
    terminal_labels = third_leaves(t)
    require(original["vertices"] == m + 1 and original["edges"] == m
            and set(graph["vertices"]) == FIXED.keys() | terminal_labels.keys()
            and graph["spine"] == [f"s:{i}" for i in range(6)],
            "exact complete target and fixed named subgraph")
    for i, count in enumerate((1, 1, t, 2)):
        for j in range(count):
            leaf = f"l:{i}:0:{j}"
            require(edge_multiset(e for e in graph["edges"] if leaf in e)
                    == edge_multiset([(f"b:{i}:0", leaf)]), "exact named terminal attachment")
    prefix = {v: x for v, x in FIXED.items() if v != "s:5"} | terminal_labels
    partial = verify_partial(graph, prefix)
    incident = [e for e in graph["edges"] if "s:5" in e]
    require(set(graph["vertices"]) - prefix.keys() == {"s:5"}
            and edge_multiset(incident) == edge_multiset([("s:4", "s:5")])
            and sorted(prefix.values()) == [x for x in range(m + 1) if x != 5]
            and partial["valid"] and partial["graph_digest"] == original["graph_digest"]
            and partial["frontier"] == ["s:4"] and prefix["s:4"] == 11
            and partial["used_differences"] == [d for d in range(1, m + 1) if d != 6]
            and partial["unused_labels"] == [5] and partial["unused_differences"] == [6],
            "exact physical singleton complements")
    full = dict(prefix)
    full["s:5"] = 5
    report = verify_certificate(graph, full, original["graph_digest"])
    ledger = named_ledger(graph, full)
    fixed_weights = sorted(row["difference"] for row in ledger if not terminal_labels.keys() & set(row["edge"]))
    require(report["valid"] and all(full[v] == x for v, x in FIXED.items())
            and sorted(FIXED.values()) == list(range(14)) and fixed_weights == list(range(1, 14))
            and sorted(terminal_labels.values()) == list(range(14, m + 1))
            and [row["difference"] for row in ledger] == report["edge_differences"]
            and abs(full["s:4"] - full["s:5"]) == 6, "ordinary graceful original and fixed ledger")
    return {"parameters": {"t": t, "K": 1}, "original": original, "third_terminal_labels": terminal_labels,
            "prefix_labels": prefix, "partial_certificate": partial,
            "singleton": {"R": [5], "D": [6], "port_vertex": "s:4", "port_label": 11,
                          "final_edge": ["s:4", "s:5"], "assigned_label": 5},
            "full_labels": full, "edge_ledger": ledger, "certificate": report,
            "claim": "ordinary gracefulness on this exact named target"}


def compare_batch(seed, full):
    names = ["l:2:0:2", "l:2:0:3"]
    successive = dict(seed)
    for name in names:
        require(name not in successive and successive["b:2:0"] == 0, "same host and fresh chronological name")
        successive[name] = len(successive)
    batch = seed | {name: len(seed) + i for i, name in enumerate(names)}
    require(successive == batch == full, "same t=4 pointwise batch agreement")
    return {"ordered_names": names, "successive": {v: successive[v] for v in names},
            "batch": {v: batch[v] for v in names}, "agrees_pointwise_on_full_target": True,
            "additional_targets": 0}


def verify_history(config):
    previous = config["historical_incomplete_receipt"]
    raw_path, bound_path = ROOT / previous["raw"], ROOT / previous["bound"]
    require(sha(raw_path) == previous["raw_sha256"] and sha(bound_path) == previous["bound_sha256"],
            "historical immutable raw bytes")
    raw, bound = read(raw_path), read(bound_path)
    require(all(raw[key] == value for key, value in HISTORY_STATUS.items())
            and bound["result"] == raw and bound["classification"] == "INCOMPLETE"
            and bound["certificate"] is None, "preserved incomplete disposition")


def main():
    config_path = HERE / "config.json"
    config = read(config_path)
    require(config == EXPECTED and config["new_solver_queries"] == 0 and config["enumeration"] is False,
            "exact search-free plan")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    diff = subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", "lcl"], cwd=ROOT, text=True)
    require(head == config["starting_commit"] and not diff, "accepted parent and unchanged core")
    verify_history(config)
    output = HERE / "validation"
    output.mkdir()
    inventory = source_inventory(ROOT)
    save_source_snapshot(ROOT, HERE / "source", inventory)
    ident = {"run_id": config["run_id"], "configuration_sha256_raw": sha(config_path),
             "runner_sha256_raw": sha(Path(__file__)), "proof": PROOF, "proof_sha256_raw": sha(ROOT / PROOF),
             "runtime": {**environment(), "version": sys.version, "executable": sys.executable, "utf8_mode": sys.flags.utf8_mode},
             "source": inventory, "historical_incomplete_receipt": config["historical_incomplete_receipt"],
             "limits": {k: config[k] for k in ("workers", "max_vertices", "max_result_bytes")},
             "new_solver_queries": 0}
    cap = config["max_result_bytes"]
    atomic_json(output / "identity.json", ident, max_bytes=cap)
    core_id = retain_original(output, "core.json", config["auxiliary_core"]["profile"])
    originals = {t: retain_original(output, f"t{t}-k1.json", [[1], [1], [t], [2], [], []])
                 for t, k in config["completed_cases"]}
    core_graph = read(output / core_id["path"])
    core_record = check_core(core_graph, core_id)
    core_path = output / "core_certificate.json"
    atomic_json(core_path, core_record, max_bytes=cap)
    entries = []
    seed = None
    for t, k in config["completed_cases"]:
        require(k == 1, "only the K=1 target list")
        original = originals[t]
        graph = read(output / original["path"])
        case = check_case(t, graph, original)
        if t == 2:
            seed = case["full_labels"]
            case["core_lift"] = {"core_certificate_sha256_raw": sha(core_path), **check_lift(core_graph, graph, seed)}
        if t == 4:
            case["same_target_batch_comparison"] = compare_batch(seed, case["full_labels"])
        path = output / f"t{t}-k1-certificate.json"
        atomic_json(path, case, max_bytes=cap)
        entries.append({"parameters": case["parameters"], "certificate": path.name,
                        "sha256_raw": sha(path), "original": original})
    summary = {"status": "PASS", "run_id": config["run_id"], "completed_utc": utc_now(),
               "identity_sha256_raw": sha(output / "identity.json"), "auxiliary_cores": 1,
               "core_certificate_sha256_raw": sha(core_path), "completed_cases": 4, "cases": entries,
               "t2_seed_included_in_completed_cases": True, "new_solver_queries": 0,
               "additional_targets_from_batch_comparison": 0, "additional_terminal_swap_checks": 0}
    atomic_json(output / "summary.json", summary, max_bytes=cap)
    print(json.dumps({"status": "PASS", "auxiliary_cores": 1, "completed_K1_cases": 4,
                      "max_vertices": max(o["vertices"] for o in originals.values()),
                      "new_solver_queries": 0}))


if __name__ == "__main__":
    main()
