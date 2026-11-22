"""Audit the same saved direct K=1 certificates with standard-library arithmetic."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
CORE_PROFILE = [[1], [1], [], [2], [], []]
CORE_LABELS = {"s:0": 7, "s:1": 0, "s:2": 12, "s:3": 1, "s:4": 10, "s:5": 4,
               "b:0:0": 3, "l:0:0:0": 2, "b:1:0": 8, "l:1:0:0": 5,
               "b:3:0": 11, "l:3:0:0": 9, "l:3:0:1": 6}


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(obj):
    data = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()


def edges(items):
    return Counter(tuple(sorted(pair)) for pair in items)


def expected_graph(profile):
    spine = [f"s:{i}" for i in range(6)]
    vertices = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    incidences = list(zip(spine, spine[1:]))
    for i, section in enumerate(profile):
        for branch, count in enumerate(section):
            center = f"b:{i}:{branch}"
            vertices[center] = {"kind": "branch", "section": i, "branch": branch}
            incidences.append((spine[i], center))
            for j in range(count):
                leaf = f"l:{i}:{branch}:{j}"
                vertices[leaf] = {"kind": "leaf", "section": i, "branch": branch, "leaf": j}
                incidences.append((center, leaf))
    return {"profile": profile, "spine": spine, "roles": vertices, "vertices": sorted(vertices),
            "edges": sorted(sorted(edge) for edge in incidences)}


def load_original(metadata, profile, limit):
    path = OUT / metadata["path"]
    original = load(path)
    theory = expected_graph(profile)
    graph_id = digest(theory)
    need(sha(path) == metadata["sha256_raw"] and graph_id == metadata["graph_digest"]
         and all(original[k] == theory[k] for k in ("profile", "spine", "roles"))
         and Counter(original["vertices"]) == Counter(theory["vertices"])
         and edges(original["edges"]) == edges(theory["edges"])
         and metadata["vertices"] == len(theory["vertices"]) <= limit
         and metadata["edges"] == len(theory["edges"]) == len(theory["vertices"]) - 1,
         "retained original names, multiplicities and digest")
    return original, graph_id


def check_certificate(record, original, graph_id, labels):
    m = len(original["edges"])
    need(set(labels) == set(original["vertices"]) and all(type(x) is int for x in labels.values())
         and sorted(labels.values()) == list(range(m + 1)), "full label bijection")
    ledger = [{"edge": [u, v], "difference": abs(labels[u] - labels[v])}
              for u, v in original["edges"]]
    weights = [row["difference"] for row in ledger]
    cert = record["certificate"]
    need(record["edge_ledger"] == ledger and sorted(weights) == list(range(1, m + 1))
         and cert["valid"] and cert["errors"] == [] and cert["edge_differences"] == weights
         and cert["graph_digest"] == graph_id and (cert["n"], cert["m"]) == (m + 1, m),
         "ordinary certificate and each original edge weight")


def check_target(t, record, original, graph_id):
    m = t + 13
    fixed = {v: x + 1 for v, x in CORE_LABELS.items()} | {"b:2:0": 0}
    terminals = {f"l:2:0:{j}": x for j, x in enumerate(range(14, m + 1))}
    expected = fixed | terminals
    actual = record["full_labels"]
    need(record["parameters"] == {"t": t, "K": 1} and actual == expected
         and record["third_terminal_labels"] == terminals
         and sorted(fixed.values()) == list(range(14))
         and record["claim"] == "ordinary gracefulness on this exact named target",
         "fixed and terminal labels")
    check_certificate(record, original, graph_id, actual)
    fixed_edges = [pair for pair in original["edges"] if set(pair).isdisjoint(terminals)]
    spine = original["spine"]
    need(sorted(abs(actual[u] - actual[v]) for u, v in fixed_edges) == list(range(1, 14))
         and all(edges(pair for pair in original["edges"] if v in pair) == edges([("b:2:0", v)])
                 for v in terminals), "fixed spectrum and prescribed third incidences")
    need(all(edges([(f"s:{i}", f"b:{i}:0")]) <= edges(original["edges"]) for i in range(4))
         and edges(zip(spine, spine[1:])) <= edges(original["edges"]), "named topology witness")

    prefix = record["prefix_labels"]
    need(prefix == {v: x for v, x in actual.items() if v != "s:5"}
         and set(original["vertices"]) - prefix.keys() == {"s:5"}
         and edges(pair for pair in original["edges"] if "s:5" in pair) == edges([("s:4", "s:5")]),
         "unchanged prefix and sole unfinished original edge")
    used = sorted(abs(prefix[u] - prefix[v]) for u, v in original["edges"] if u in prefix and v in prefix)
    R = sorted(set(range(m + 1)) - set(prefix.values()))
    D = sorted(set(range(1, m + 1)) - set(used))
    partial = record["partial_certificate"]
    need(R == [5] and D == [6] and prefix["s:4"] == 11 and actual["s:5"] == 5
         and abs(prefix["s:4"] - actual["s:5"]) == 6
         and record["singleton"] == {"R": R, "D": D, "port_vertex": "s:4", "port_label": 11,
                                     "final_edge": ["s:4", "s:5"], "assigned_label": 5}
         and partial["valid"] and partial["graph_digest"] == graph_id and partial["frontier"] == ["s:4"]
         and partial["unused_labels"] == R and partial["unused_differences"] == D
         and partial["used_differences"] == used, "both exact resource complements")
    need(edges([("l:0:0:0", "b:0:0"), ("b:0:0", "s:0")]) <= edges(original["edges"])
         and actual["l:0:0:0"] < actual["b:0:0"] < actual["s:0"], "ordinary scope witness")


def main():
    config_file = HERE / "config.json"
    config = load(config_file)
    identity_file = OUT / "identity.json"
    ident = load(identity_file)
    summary_path = OUT / "summary.json"
    summary = load(summary_path)
    cap = config["max_result_bytes"]
    need(config["completed_cases"] == [[1, 1], [2, 1], [3, 1], [4, 1]]
         and config["workers"] == 1 and config["max_vertices"] == 18 and cap == 2_000_000
         and config["enumeration"] is False and config["terminal_swap_arithmetic_check"] is False
         and config["new_solver_queries"] == ident["new_solver_queries"] == summary["new_solver_queries"] == 0
         and summary["run_id"] == ident["run_id"] == config["run_id"] and summary["status"] == "PASS"
         and summary["t2_seed_included_in_completed_cases"] is True
         and summary["auxiliary_cores"] == 1 and summary["completed_cases"] == len(summary["cases"]) == 4
         and summary["identity_sha256_raw"] == sha(identity_file)
         and summary["additional_targets_from_batch_comparison"] == summary["additional_terminal_swap_checks"] == 0
         and ident["configuration_sha256_raw"] == sha(config_file)
         and ident["runner_sha256_raw"] == sha(HERE / "validate.py")
         and ident["proof_sha256_raw"] == sha(ROOT / ident["proof"])
         and ident["source"]["sha256"] == digest(ident["source"]["files"])
         and all(sha(HERE / "source" / name) == value for name, value in ident["source"]["files"].items()),
         "immutable run and exact limits")
    hist = config["historical_incomplete_receipt"]
    raw = load(ROOT / hist["raw"])
    bound = load(ROOT / hist["bound"])
    need(ident["historical_incomplete_receipt"] == hist
         and sha(ROOT / hist["raw"]) == hist["raw_sha256"] and sha(ROOT / hist["bound"]) == hist["bound_sha256"]
         and bound["classification"] == raw["status"] == "INCOMPLETE"
         and raw["reason"] == "max_nodes" and raw["nodes"] == 100_000 and raw["exhausted"] is False
         and raw["count"] is None and raw["count_lower_bound"] == 0 and raw["witness"] is None
         and bound["result"] == raw and bound["certificate"] is None, "historical incomplete query unchanged")

    core_path = OUT / "core_certificate.json"
    core = load(core_path)
    original, core_id = load_original(core["original"], CORE_PROFILE, config["max_vertices"])
    need(sha(core_path) == summary["core_certificate_sha256_raw"]
         and core_id == config["auxiliary_core"]["graph_digest"]
         and core["labels"] == CORE_LABELS and core["root"] == {"vertex": "s:2", "label": 12},
         "fixed rooted core")
    check_certificate(core, original, core_id, core["labels"])
    entries = []
    seed = None
    for (t, _), row in zip(config["completed_cases"], summary["cases"], strict=True):
        path = OUT / row["certificate"]
        case = load(path)
        graph, graph_id = load_original(row["original"], [[1], [1], [t], [2], [], []], config["max_vertices"])
        need(case["original"] == row["original"] and case["parameters"] == row["parameters"]
             and sha(path) == row["sha256_raw"] and path.stat().st_size <= cap, "saved case identity")
        check_target(t, case, graph, graph_id)
        if t == 2:
            seed = case["full_labels"]
            lifted = case["core_lift"]
            attachments = [("s:2", "b:2:0"), ("b:2:0", "l:2:0:0"), ("b:2:0", "l:2:0:1")]
            need(graph_id == config["completed_seed_graph_digest"]
                 and lifted["core_certificate_sha256_raw"] == sha(core_path)
                 and lifted["core_to_seed_translation"] == 1 and lifted["reverse_translation"] == -1
                 and lifted["restored_labels"] == {"b:2:0": 0, "l:2:0:0": 14, "l:2:0:1": 15}
                 and edges(graph["edges"]) - edges(original["edges"]) == edges(attachments)
                 and edges(lifted["restored_edges"]) == edges(attachments)
                 and [abs(seed[u] - seed[v]) for u, v in attachments] == lifted["restored_differences"]
                 == [13, 14, 15] and all(seed[v] - 1 == x for v, x in CORE_LABELS.items())
                 and lifted["verified"] is True, "pointwise reversible core-to-seed lift")
        if t == 4:
            batch = case["same_target_batch_comparison"]
            full = case["full_labels"]
            extra = {"l:2:0:2": 16, "l:2:0:3": 17}
            need(all(full[v] == x for v, x in seed.items()) and full == seed | extra
                 and batch["ordered_names"] == list(extra)
                 and batch["successive"] == batch["batch"] == extra
                 and batch["agrees_pointwise_on_full_target"] is True and batch["additional_targets"] == 0,
                 "same-target batch agreement")
        entries.append({"t": t, "K": 1, "graph_digest": graph_id,
                        "certificate_sha256_raw": row["sha256_raw"], "status": "PASS"})
    audit = {"status": "PASS", "run_id": config["run_id"] + "-arithmetic-audit",
             "audit_source_sha256_raw": sha(Path(__file__)), "summary_sha256_raw": sha(summary_path),
             "core_certificate_sha256_raw": sha(core_path), "same_auxiliary_cores": 1,
             "same_completed_cases": 4, "additional_targets": 0, "additional_queries": 0,
             "runtime": {"python": sys.version, "platform": platform.platform()}, "cases": entries}
    data = (json.dumps(audit, indent=2) + "\n").encode()
    need(len(data) <= cap, "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(data)
    print("PASS: same 1 core and 4 completed targets, 0 new cases or queries")


if __name__ == "__main__":
    main()
