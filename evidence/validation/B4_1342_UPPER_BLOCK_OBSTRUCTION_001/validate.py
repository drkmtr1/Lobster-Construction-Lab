"""Bounded check of the eight prescribed upper-block thresholds."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
PARENT = "c83ae3b11a6bc03189dc44653881137fc014c72a"
PROOF = "research/B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
H, U, Z = "b:0:0", "s:4", "b:2:0"
FRESH = "l:0:0:1"
W = [H, "s:0", "s:1", "s:2", "s:3", U]
THRESHOLDS = list(range(11, 19))
EXPECTED_COUNTS = [13, 10, 8, 7, 6, 5, 4, 1]

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def put(path, raw, cap):
    require(len(raw) <= cap, f"byte cap exceeded for {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def save(relative, value, cap):
    raw = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    put(OUT / relative, raw, cap)
    return {"path": relative, "sha256_raw": sha(raw)}


def git(*args):
    return subprocess.check_output(("git", *args), cwd=ROOT)


def edge_counts(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def ledger(edges, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]


def witness(graph):
    adjacent = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacent[u].append(v)
        adjacent[v].append(u)
    require(all(v in adjacent[u] for u, v in zip(W, W[1:])), "not the physical witness")
    distance = dict.fromkeys(W, 0)
    queue = deque(W)
    while queue:
        u = queue.popleft()
        for v in adjacent[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                queue.append(v)
    require(len(distance) == len(adjacent) and max(distance.values()) == 2 and distance[Z] == 1,
            "incorrect witness distances")
    return {"path": W, "distances": distance}


def retain(name, graph, order, profile, config):
    require(graph["profile"] == profile and len(graph["vertices"]) == order <= config["max_vertices"]
            and len(graph["edges"]) == order - 1, "wrong retained original profile or order")
    digest = graph_digest(graph)
    ref = save(f"originals/{name}.json", {"graph": graph, "graph_digest": digest}, config["max_result_bytes"])
    return {**ref, "graph_digest": digest}


def source_ref(relative):
    return {"path": relative, "sha256_raw": sha((ROOT / relative).read_bytes())}


def control(graph, labels, ref, branch, source, original_source, expected, order):
    p = branch["p"]
    c = verify_certificate(graph, labels, ref["graph_digest"])
    require(c == expected and c["valid"] and c["n"] == order and c["m"] == order - 1,
            "retained certificate does not agree with unchanged verifier")
    require(labels[H] == branch["host_label"] and labels[U] == branch["exit_label"] and labels[Z] == 0,
            "physical anchors changed")
    lows = sorted(v for v, label in labels.items() if label < p)
    highs = sorted(v for v, label in labels.items() if label >= p)
    require(len(lows) == p and all((labels[u] < p) != (labels[v] < p) for u, v in graph["edges"]),
            "incorrect alpha cut")
    return {"original": ref, "source_certificate": source, "source_original": original_source,
            "labels": labels, "state": {"n": order, "p": p, "x": labels[H], "y": labels[U] - p,
                                       "L": H, "H": H, "U": U, "Z": Z},
            "anchors": {v: labels[v] for v in (H, U, Z)},
            "alpha": {"low": lows, "high": highs}, "witness": witness(graph),
            "edge_ledger": ledger(graph["edges"], labels), "verification": c}


def incidence(graph, labels, c, p):
    selected = {v: value for v, value in labels.items() if value >= c}
    edges = [edge for edge in graph["edges"] if any(v in selected for v in edge)]
    require(all(sum(v in selected for v in edge) == 1 for edge in edges)
            and all(value >= p for value in selected.values()), "non-high or multiply selected edge")
    selected_ledger = ledger(edges, labels)
    actual = sorted(row["difference"] for row in selected_ledger)
    required = list(range(c - labels[H], len(graph["edges"]) + 1))
    return {"c": c, "selected_vertices": selected, "selected_edges": selected_ledger,
            "selected_multiset": actual, "actual_count": len(actual), "required_multiset": required,
            "required_count": len(required), "matches": actual == required}


def threshold_check(graph, labels, c):
    if type(c) is not int or not 11 <= c <= 18:
        raise ValueError("c must be an exact integer from 11 through 18")
    return incidence(graph, labels, c, p=9)


def guards(config, graph, labels):
    results = []
    with patch(__name__ + ".incidence", side_effect=AssertionError("invalid threshold evaluated incidence")) as select:
        for c in config["invalid_thresholds"]:
            try:
                threshold_check(graph, labels, c)
            except ValueError as error:
                results.append({"c": c, "type": type(c).__name__, "error": str(error),
                                "incidence_calls": select.call_count})
            else:
                raise ValueError("invalid threshold accepted")
        require(select.call_count == 0 and len(results) == 5, "guard scope")
    return results


def one_leaf(expanded, ref, old_labels, row):
    c = row["c"]
    selected = row["selected_vertices"]
    labels = {v: old_labels[v] + (1 if v in selected else 0) for v in old_labels}
    labels[FRESH] = c
    require(labels[H] == 1 and labels[U] == 10 and labels[Z] == 0
            and sorted(labels.values()) == list(range(20))
            and all((labels[u] < 9) != (labels[v] < 9) for u, v in expanded["edges"]),
            "invalid label alphabet, anchors or numerical alpha cut")
    rows = ledger(expanded["edges"], labels)
    spectrum = Counter(item["difference"] for item in rows)
    missing = [{"difference": d, "multiplicity": 0} for d in range(1, 20) if spectrum[d] == 0]
    repeated = [{"difference": d, "multiplicity": count} for d, count in sorted(spectrum.items()) if count > 1]
    result = verify_certificate(expanded, labels, ref["graph_digest"])
    require(result == {"valid": False, "errors": ["edge differences repeat", "edge differences are not exactly 1..m"],
                       "n": 20, "m": 19, "graph_digest": ref["graph_digest"],
                       "edge_differences": [item["difference"] for item in rows],
                       "claim": "finite certificate for this exact named target only"}
            and missing and repeated, "one-leaf verifier acceptance or unexpected rejection")
    total = sum(d * count for d, count in spectrum.items())
    require(total == 171 + row["actual_count"] + (c - 1)
            and total - 190 == row["actual_count"] + c - 20, "one-leaf sum arithmetic")
    return {"c": c, "h": 1, "original": ref, "labels": labels, "edge_ledger": rows,
            "difference_multiset": sorted(item["difference"] for item in rows), "missing": missing, "repeated": repeated,
            "anchors": {v: labels[v] for v in (H, U, Z)}, "complete_label_alphabet": list(range(20)),
            "actual_difference_sum": total, "required_difference_sum": 190, "signed_defect": total - 190,
            "verification": result}


def main():
    path = HERE / "config.json"
    config = read(path)
    cap = config["max_result_bytes"]
    require(git("rev-parse", "HEAD").decode().strip() == PARENT == config["parent"], "unexpected accepted parent")
    require(config["workers"] == 1 and config["max_vertices"] == 20 and cap == 2_000_000
            and config["solver_queries"] == config["labeling_enumeration"] == config["historical_replay"] == 0
            and config["batch"] == 1 and config["thresholds"] == THRESHOLDS
            and config["expanded_profile"] == [[2], [3], [4], [2], []]
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "wrong run limits or runtime")
    OUT.mkdir()
    snapshots = {}
    for rel in SOURCES:
        raw = (ROOT / rel).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{rel}").replace(b"\r\n", b"\n"),
                f"source differs from parent: {rel}")
        put(OUT / "source" / rel, raw, cap)
        snapshots[rel] = sha(raw)

    neg, pos = config["negative"], config["positive"]
    retained = [entry[key] for entry in (neg, pos) for key in ("certificate", "original")] + [pos["bound_query"]]
    identity = {"run_id": config["run_id"], "parent": PARENT,
                "config_sha256_raw": sha(path.read_bytes()), "runner_sha256_raw": sha(Path(__file__).read_bytes()),
                "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
                "proof": {"path": PROOF, "sha256_raw": sha((ROOT / PROOF).read_bytes())},
                "retained_sha256_raw": {name: source_ref(name)["sha256_raw"] for name in retained},
                "source_sha256_raw": snapshots, "runtime": {"python": sys.version, "implementation": sys.implementation.name,
                     "platform": platform.platform(), "python_executable": ".venv/Scripts/python.exe",
                     "utf8_mode": sys.flags.utf8_mode, "optional_dependencies": []}}
    ident = save("identity.json", identity, cap)

    neg_source = read(ROOT / neg["certificate"])
    orig = read(ROOT / neg["original"])
    graph = orig["graph"]
    neg_ref = retain("1342", graph, 19, neg["profile"], config)
    pos_source = read(ROOT / pos["certificate"])
    pos_graph = read(ROOT / pos["original"])
    pos_ref = retain("1122", pos_graph, 15, pos["profile"], config)
    expanded = build_graph(config["expanded_profile"])
    expanded_ref = retain("2342", expanded, 20, config["expanded_profile"], config)
    require(Counter(expanded["vertices"]) == Counter(graph["vertices"]) + Counter([FRESH])
            and edge_counts(expanded["edges"]) == edge_counts(graph["edges"]) + edge_counts([[H, FRESH]])
            and all(expanded["roles"][v] == role for v, role in graph["roles"].items()),
            "expanded graph differs from the original graph plus just the prescribed leaf")

    require(neg_ref["graph_digest"] == orig["graph_digest"] == neg_source["original"]["graph_digest"]
            and source_ref(neg["original"])["sha256_raw"] == neg_source["original"]["sha256_raw"],
            "retained 1342 original binding")
    negative = control(graph, neg_source["labels"], neg_ref, neg, source_ref(neg["certificate"]),
                       source_ref(neg["original"]), neg_source["verification"], 19)
    require(negative["edge_ledger"] == neg_source["edge_ledger"]
            and negative["alpha"] == {key: neg_source["alpha"][key] for key in ("low", "high")}
            and negative["witness"] == {"path": neg_source["witness"], "distances": neg_source["witness_distances"]}
            and (negative["state"]["p"], negative["state"]["x"], negative["state"]["y"]) == (9, 1, 1),
            "retained normalized 1342 certificate differs")
    negative_receipt = save("negative_1342.json", negative, cap)

    query = read(ROOT / pos["bound_query"])
    given = pos_source["normalized"]
    pos_labels = given["labels"]
    require(pos_source["source"] == {**source_ref(pos["bound_query"]), "graph_digest": pos_ref["graph_digest"]}
            and pos_ref["graph_digest"] == query["original_graph_digest"] and query["original_graph"] == pos_graph
            and query["classification"] == "SAT" and query["result"]["witness"] == pos_labels
            and query["certificate"] == pos_source["certificate"], "1122 historical graph or certificate binding")
    positive = control(pos_graph, pos_labels, pos_ref, pos, source_ref(pos["certificate"]),
                       source_ref(pos["original"]), pos_source["certificate"], 15)
    positive["source_query_record"] = source_ref(pos["bound_query"])
    c = pos["threshold"]
    require(c == 9 and pos_labels[U] < c <= 14, "positive threshold")
    predicate = incidence(pos_graph, pos_labels, c, p=7)
    require(predicate["matches"] and predicate["selected_multiset"] == list(range(5, 15))
            and predicate["selected_edges"] == given["selected_incident_edges"]
            and sorted(predicate["selected_vertices"]) == given["selected_vertices"]
            and positive["witness"] == {"path": given["witness"], "distances": given["witness_distances"]},
            "retained positive incidence predicate differs")
    positive["predicate"] = predicate
    positive_receipt = save("positive_1122.json", positive, cap)

    labels = negative["labels"]
    require(THRESHOLDS == list(range(labels[U] + 1, negative["state"]["n"])), "incomplete strict threshold domain")
    rows = [threshold_check(graph, labels, c) for c in config["thresholds"]]
    require([row["actual_count"] for row in rows] == EXPECTED_COUNTS and all(
        not row["matches"] and row["required_count"] == 20 - row["c"] for row in rows), "unexpected threshold results")
    symbolic_rows = [{"c": row["c"], "actual_selected_edges": row["actual_count"],
                      "necessary_selected_edges": row["required_count"],
                      "coefficient_of_h": row["actual_count"] + row["c"] - 20} for row in rows]
    require(all(row["coefficient_of_h"] != 0 for row in symbolic_rows), "edge sum permits threshold")
    threshold_receipt = save("thresholds.json", rows, cap)
    symbolic_receipt = save("all_batch_sum.json", {
        "old_difference_sum": sum(negative["verification"]["edge_differences"]),
        "inserted_linear_coefficient": "c-1",
        "common_quadratic_term": "h*(h-1)/2", "required_linear_coefficient": 19,
        "necessary_count": "20-c", "difference": "h*(s_c+c-20)", "domain": "exact integer h>=1",
        "thresholds": symbolic_rows}, cap)
    invalid_receipt = save("invalid_thresholds.json", guards(config, graph, labels), cap)
    attempts = [one_leaf(expanded, expanded_ref, labels, row) for row in rows]
    attempt_receipt = save("one_leaf_attempts.json", attempts, cap)
    summary = {"status": "PASS", "run_id": config["run_id"], "identity": ident, "distinct_graph_records": 3,
               "retained_controls": [negative_receipt, positive_receipt], "attempted_original": expanded_ref,
               "threshold_evaluations": len(rows), "thresholds": threshold_receipt, "all_batch_sum": symbolic_receipt,
               "invalid_probes": 5, "invalid_thresholds": invalid_receipt, "attempted_labelings": len(attempts),
               "rejected_labelings": sum(not attempt["verification"]["valid"] for attempt in attempts),
               "attempts": attempt_receipt, "new_graceful_targets": 0,
               "solver_queries": 0, "labeling_enumeration": 0, "historical_replay": 0}
    save("summary.json", summary, cap)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
