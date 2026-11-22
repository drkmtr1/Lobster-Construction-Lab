"""Record the bounded U=9 named-subset calculation and retained controls."""

from collections import deque
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
PARENT = "3ac2ccc91d28063e89ebd21bf3ec5bf525f72992"
PROOF = "research/B4_1342_U9_STRUCTURAL_OBSTRUCTION.md"
U, H, Z, F = "s:4", "b:0:0", "b:2:0", "b:3:0"
WITNESS = [H, "s:0", "s:1", "s:2", "s:3", U]

sys.path.insert(0, str(ROOT))
from lcl.verify import verify_certificate


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_bytes())


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def write(path, raw, cap):
    require(len(raw) <= cap, f"byte limit: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def graph_facts(graph):
    adj = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adj[u].append(v)
        adj[v].append(u)
    distance = {U: 0}
    queue = deque([U])
    while queue:
        v = queue.popleft()
        for u in adj[v]:
            if u not in distance:
                distance[u] = distance[v] + 1
                queue.append(u)
            require(distance[u] % 2 != distance[v] % 2, "alpha incidence")
    require(distance.keys() == adj.keys(), "connected original")
    high = sorted(v for v, d in distance.items() if d % 2 == 0)
    low = sorted(adj.keys() - set(high))
    require(all(v in adj[u] for u, v in zip(WITNESS, WITNESS[1:])), "physical witness")
    witness_distance = {v: 0 for v in WITNESS}
    queue = deque(WITNESS)
    while queue:
        v = queue.popleft()
        for u in adj[v]:
            if u not in witness_distance:
                witness_distance[u] = witness_distance[v] + 1
                queue.append(u)
    require(max(witness_distance.values()) == 2 and witness_distance[Z] == 1, "witness distance")
    return {"high": high, "low": low, "neighbors": {v: sorted(adj[v]) for v in adj},
            "witness": WITNESS, "witness_distances": witness_distance}


def control(profile, graph, labels, expected, graph_digest, pins, p, cap):
    n = len(graph["vertices"])
    require(n == 9 + sum(section[0] for section in profile if section)
            and n <= cap and graph["profile"] == profile and len(graph["edges"]) == n - 1, "control scope")
    result = verify_certificate(graph, labels, graph_digest)
    require(result == expected and result["valid"], "original-bound checker")
    facts = graph_facts(graph)
    require(sorted(labels[v] for v in facts["low"]) == list(range(p))
            and sorted(labels[v] for v in facts["high"]) == list(range(p, n))
            and {v: labels[v] for v in pins} == pins, "retained alpha or pins")
    return {"pins": pins, "labels": labels, "graph_digest": graph_digest, "facts": facts,
            "checker": result, "edge_ledger": [
                {"edge": edge, "difference": abs(labels[edge[0]] - labels[edge[1]])} for edge in graph["edges"]]}


def alpha_pairs(d):
    return [[lo, lo + d] for lo in range(9) if 9 <= lo + d <= 18]


def proof_facts(facts):
    neighbors = facts["neighbors"]
    require(len(facts["high"]) == 10 and len(facts["low"]) == 9
            and neighbors[U] == ["s:3"] and alpha_pairs(1) == [[8, 9]]
            and alpha_pairs(2) == [[7, 9], [8, 10]]
            and neighbors["s:3"] == sorted([U, "s:2", F]), "forced low and high")
    zero_terminals = sorted(set(neighbors[Z]) - {"s:2"})
    require(zero_terminals == [f"l:2:0:{j}" for j in range(4)]
            and all(neighbors[v] == [Z] for v in zero_terminals), "descending induction")
    return {"alpha_pairs": {str(d): alpha_pairs(d) for d in (1, 2, 18)},
            "forced": {"s:3": 8, F: 10}, "force_fourth_center_from_c": 11,
            "exit_neighbor": "s:3", "s3_neighbors": neighbors["s:3"],
            "zero_neighbors": neighbors[Z], "zero_terminals": zero_terminals,
            "descend": {"start": 18, "stop": "c", "other_zero_neighbor": "s:2",
                        "degree_excess_if_s2_unselected": 0},
            "selected_s2_s3_max_difference": 10}


def subset_table(facts, forcing, cap):
    eligible = [v for v in facts["high"] if v != U]
    degree = {v: len(facts["neighbors"][v]) for v in facts["high"]}
    require(len(eligible) == 9 and 2 ** len(eligible) == cap and sum(degree.values()) == 18, "degree census")
    zero_neighbors = set(forcing["zero_neighbors"])
    rows = {(c, a): {"c": c, "a": a, "k": 19 - c, "d0": c - a, "surviving_sets": []}
            for c in range(10, 19) for a in range(2, 9)}
    visited = 0
    for mask in range(cap):
        selected = [v for i, v in enumerate(eligible) if mask & (1 << i)]
        visited += 1
        c = 19 - len(selected)
        a = sum(degree[v] - 1 for v in selected)
        if (c, a) not in rows:
            continue
        d0 = c - a
        if a == 8 or c == 10 or "s:2" not in selected or F in selected or d0 > 10:
            continue
        if len(zero_neighbors - set(selected)) > len(range(11, d0)):
            continue
        rows[c, a]["surviving_sets"].append(selected)
    require(sum(degree[v] for v in eligible) == 17, "c=10 degree sum")
    survivors = [row for row in rows.values() if row["surviving_sets"]]
    require([(row["c"], row["a"]) for row in survivors] ==
            [(11, 6), (12, 3), (12, 5), (12, 6), (13, 3), (13, 5)]
            and all(len(row["surviving_sets"]) == 1 for row in survivors), "unexpected subset reduction")
    return {"degree": degree, "eligible": eligible, "subsets_visited": visited,
            "c10_selected_degree_sum": 17, "c10_required_a": 8, "pairs": list(rows.values())}


def evaluate(a, c, h):
    return {"a": a, "c": c, "h": h, "d0": c - a}


def checked_scope(a, c, h):
    for name, value, lower, upper in (("a", a, 2, 8), ("c", c, 10, 18), ("h", h, 1, None)):
        if type(value) is not int or value < lower or (upper is not None and value > upper):
            raise ValueError(name)
    return evaluate(a, c, h)


def invalid_inputs():
    valid = (2, 10, 1)
    receipts = []
    with patch(__name__ + ".evaluate", side_effect=AssertionError("invalid evaluation reached")) as hook:
        for index, (name, bad_values) in enumerate((
            ("a", (True, 1, 9, 2.0, "2")), ("c", (True, 9, 19, 10.0, "10")),
            ("h", (True, 0, -1, 1.0, "1")),
        )):
            for value in bad_values:
                trial = list(valid)
                trial[index] = value
                try:
                    checked_scope(*trial)
                except ValueError as error:
                    require(str(error) == name, "incorrect rejection")
                    receipts.append({"parameter": name, "input": trial, "type": type(value).__name__,
                                     "evaluation_calls": hook.call_count})
                else:
                    raise ValueError(f"invalid input accepted: {trial!r}")
        require(hook.call_count == 0, "guards must precede evaluation")
    return receipts


def case_arithmetic(table, facts):
    adj = facts["neighbors"]
    require(adj[F] == ["l:3:0:0", "l:3:0:1", "s:3"] and adj["s:0"] == [H, "s:1"]
            and adj["s:2"] == [Z, "s:1", "s:3"]
            and set(adj["b:1:0"]) == {"s:1", *(f"l:1:0:{j}" for j in range(3))}
            and adj["l:0:0:0"] == [H], "residual physical edges")
    rows = {}
    for row in table["pairs"]:
        if row["surviving_sets"]:
            selected = row["surviving_sets"][0]
            rows[f'{row["c"]},{row["a"]}'] = {
                "unselected_highs": sorted(set(facts["high"]) - set(selected)),
                "band": [1, row["d0"] - 1]}
    for key in ("11,6", "12,5", "12,6", "13,5"):
        rows[key]["fourth_terminal_weights"] = [3, 4]
        rows[key]["fourth_terminal_labels"] = [10 - d for d in (3, 4)]
    rows["11,6"]["repeated_label"] = 6
    rows["12,6"].update(first_terminal_weight=11 - 6, repeated_label=6)
    rows["12,5"].update(first_attachment_weight=11 - 5, forced_s1=11 - 5, repeated_label=6)
    rows["12,3"].update(second_center_forbidden_weights=[11 - 8, 11 - 3],
                         fourth_terminal_labels=[10 - (11 - 8), 10 - (11 - 3)], repeated_label=11 - 4)
    rows["13,3"].update(forced_s2=8 + (13 - 3), gaps=[
        {"s0": v, "remaining_weights": sorted({11, 12, v} - {v - 3}),
         "required_gap": max({11, 12, v} - {v - 3}) - min({11, 12, v} - {v - 3}),
         "physical_gap": 18 - v}
        for v in range(13, 18) if v - 3 in {11, 12, v}])
    rows["13,5"]["orderings"] = [{"s0": v, "first_terminal": 23 - v, "forced_s1": v - 5,
                                  "repeated_label": v - 5} for v in (11, 12)]
    require(rows["12,3"]["repeated_label"] in rows["12,3"]["fourth_terminal_labels"]
            and all(rows[key]["repeated_label"] in rows[key]["fourth_terminal_labels"]
                    for key in ("11,6", "12,5", "12,6"))
            and [row["s0"] for row in rows["13,3"]["gaps"]] == [14, 15]
            and all(row["required_gap"] != row["physical_gap"] for row in rows["13,3"]["gaps"])
            and all(row["repeated_label"] in rows["13,5"]["fourth_terminal_labels"]
                    for row in rows["13,5"]["orderings"]), "residual contradictions")
    return rows


def main():
    config_path = HERE / "config.json"
    config = load(config_path)
    limits = config["limits"]
    require(config["parent"] == PARENT == git("rev-parse", "HEAD").decode().strip(), "parent checkout required")
    require(limits == {"workers": 1, "max_order": 19, "max_bytes": 2_000_000, "max_named_subsets": 512,
                       "solver_queries": 0, "graceful_labeling_enumeration": 0, "historical_search_replay": 0,
                       "new_graphs": 0, "new_enlarged_attempts": 0}
            and config["domain"] == {"a": [2, 8], "c": [10, 18], "h_min": 1}
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode, "limits or runtime")
    cap = limits["max_bytes"]
    OUT.mkdir()
    def save(name, info):
        write(OUT / name, (json.dumps(info, sort_keys=True, indent=2) + "\n").encode(), cap)

    refs = {}
    for path in config["retained"]:
        raw = (ROOT / path).read_bytes()
        require(raw == git("show", f"{PARENT}:{path}"), f"retained bytes: {path}")
        refs[path] = digest(raw)
    snapshots = {}
    for path in config["sources"]:
        raw = (ROOT / path).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{path}").replace(b"\r\n", b"\n"), f"source: {path}")
        write(OUT / "source" / path, raw, cap)
        snapshots[path] = digest(raw)
    save("identity.json", {"parent": PARENT, "id": config["id"], "retained_sha256": refs,
         "sources_sha256": snapshots, "inputs_sha256": {path.relative_to(ROOT).as_posix(): digest(path.read_bytes())
             for path in (config_path, HERE / "commands.json", HERE / "validate.py", HERE / "audit.py", ROOT / PROOF)},
         "runtime": {"version": sys.version, "platform": platform.platform(), "implementation": sys.implementation.name,
                     "utf8_mode": sys.flags.utf8_mode, "python": ".venv/Scripts/python.exe", "optional_dependencies": []}})

    original, counterpart, prior, pos_graph, query, seed = [load(ROOT / p) for p in config["retained"]]
    require(original == counterpart and prior["original"]["graph_digest"] == original["graph_digest"]
            and prior["original"]["sha256_raw"] == refs[config["retained"][1]], "1342 source binding")
    neg = control([[1], [3], [4], [2], []], original["graph"], prior["labels"], prior["verification"],
                  original["graph_digest"], {U: 10, H: 1, Z: 0}, 9, limits["max_order"])
    require(neg["edge_ledger"] == prior["edge_ledger"], "1342 edge ledger")
    require(query["original_graph"] == pos_graph and query["classification"] == "SAT"
            and query["result"]["witness"] == seed["normalized"]["labels"]
            and query["certificate"] == seed["certificate"]
            and seed["source"] == {"path": config["retained"][4], "sha256_raw": refs[config["retained"][4]],
                                   "graph_digest": query["original_graph_digest"]}, "1122 retained bindings")
    pos = control([[1], [1], [2], [2], []], pos_graph, seed["normalized"]["labels"], seed["certificate"],
                  query["original_graph_digest"], {U: 8, H: 4, Z: 0}, 7, limits["max_order"])
    selected = sorted(v for v in pos["labels"] if pos["labels"][v] >= 9)
    ledger = [row for row in pos["edge_ledger"] if any(v in selected for v in row["edge"])]
    require(ledger == seed["normalized"]["selected_incident_edges"]
            and sorted(row["difference"] for row in ledger) == list(range(5, 15)), "1122 band")
    pos["predicate"] = {"c": 9, "selected": selected, "ledger": ledger, "spectrum": list(range(5, 15))}
    save("controls.json", {"1342_previous_u10": neg, "1122_positive": pos})

    forcing = proof_facts(neg["facts"])
    table = subset_table(neg["facts"], forcing, limits["max_named_subsets"])
    cases = case_arithmetic(table, neg["facts"])
    save("structural.json", {"forcing": forcing, "subset_table": table, "contradictions": cases,
                            "batch_necessity": {"m": 18, "d0": "c-a", "h_min": 1,
                                "fixed_below_d0": [1, "d0-1"], "forced_by_new": ["d0", "min(m,d0+h-1)"],
                                "forced_by_shift": ["d0+h", "m"], "predecessor": "w-h",
                                "necessary_spectrum": ["d0", "m"]}})
    probes = invalid_inputs()
    save("invalid_inputs.json", probes)
    summary = {"status": "PASS", "id": config["id"], "limits": limits, "retained_graph_records": 2,
               "pairs": len(table["pairs"]), "pairs_excluded_by_reduction": 57, "residual_cases": len(cases),
               "subsets_visited": table["subsets_visited"], "input_rejections": len(probes)}
    save("summary.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
