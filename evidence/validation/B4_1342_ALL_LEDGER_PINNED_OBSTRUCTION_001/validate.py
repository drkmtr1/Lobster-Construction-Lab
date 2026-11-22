"""Recheck the two retained originals and record the structural proof data."""

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
PARENT = "41f4e42fb73ab87a93abe1f7c348e8442fdd47b7"
PROOF = "research/B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md"
SOURCES = ("lcl/__init__.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
H, Z, U = "b:0:0", "b:2:0", "s:4"
PINS = {H: 1, Z: 0, U: 10}
THRESHOLDS = list(range(11, 19))
WITNESS = [H, "s:0", "s:1", "s:2", "s:3", U]

sys.path.insert(0, str(ROOT))
from lcl.verify import verify_certificate


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def write(relative, raw, cap):
    require(len(raw) <= cap, f"byte cap on {relative}")
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as target:
        target.write(raw)
    return {"path": relative, "sha256_raw": sha(raw)}


def save(relative, value, cap):
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    return write(relative, raw, cap)


def git(*args):
    return subprocess.check_output(("git", *args), cwd=ROOT)


def source(relative):
    return {"path": relative, "sha256_raw": sha((ROOT / relative).read_bytes())}


def named_graph_data(graph):
    neighbors = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].append(v)
        neighbors[v].append(u)
    return neighbors


def parity(neighbors):
    high = {U: True}
    queue = deque([U])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if v not in high:
                high[v] = not high[u]
                queue.append(v)
            require(high[v] != high[u], "edge fails alpha bipartition")
    require(set(high) == set(neighbors), "disconnected graph")
    return sorted(v for v in high if high[v]), sorted(v for v in high if not high[v])


def witness(neighbors):
    require(all(v in neighbors[u] for u, v in zip(WITNESS, WITNESS[1:])), "physical witness")
    distances = dict.fromkeys(WITNESS, 0)
    queue = deque(WITNESS)
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)
    require(set(distances) == set(neighbors) and max(distances.values()) <= 2 and distances[Z] == 1, "witness distances")
    return {"path": WITNESS, "distances": distances}


def retained(name, graph, labels, original, expected, p, pins, order, config):
    n, m = len(graph["vertices"]), len(graph["edges"])
    require(n == order <= config["max_vertices"] and m == n - 1
            and graph["profile"] == [[int(part)] for part in name] + [[]], "original scope")
    verification = verify_certificate(graph, labels, original["graph_digest"])
    require(verification["valid"] and verification == expected, "retained certificate changed")
    neighbors = named_graph_data(graph)
    high, low = parity(neighbors)
    require(sorted(labels[v] for v in high) == list(range(p, n))
            and sorted(labels[v] for v in low) == list(range(p))
            and {v: labels[v] for v in pins} == pins, "retained labels or pins")
    return {"original": original, "state": {"n": n, "p": p, "x": labels[H], "y": labels[U] - p, "L": H, "U": U},
            "pins": pins, "labels": labels, "bipartition": {"high": high, "low": low}, "witness": witness(neighbors),
            "edge_ledger": [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]],
            "verification": verification}


def degree_inputs(graph, neg):
    neighbors = named_graph_data(graph)
    high = neg["bipartition"]["high"]
    require(all((u in high) != (v in high) for u, v in graph["edges"]), "not exactly one high per original edge")
    degrees = {v: len(neighbors[v]) for v in high}
    eligible = {v: d for v, d in degrees.items() if v != U}
    required = sorted(eligible.values())
    require(sum(degrees.values()) == 18 and required == [1, 1, 1, 1, 1, 2, 3, 3, 4], "high degree census")
    degree_two = [v for v, d in eligible.items() if d == 2]
    ones = sorted(v for v, d in eligible.items() if d == 1)
    high_degree = sorted(v for v, d in eligible.items() if d > 2)
    zero_neighbors = sorted(neighbors[Z])
    zero_terminals = sorted(v for v in zero_neighbors if v in ones)
    require(degree_two == ["s:0"] and high_degree == ["b:1:0", "b:3:0", "s:2"]
            and set(zero_neighbors) == {"s:2", *zero_terminals}
            and zero_terminals == [f"l:2:0:{j}" for j in range(4)], "descending induction neighborhood")
    return {"high_degree": degrees, "high_incidence": {v: sorted(neighbors[v]) for v in high},
            "eligible_degree": eligible, "sorted_eligible_degrees": required, "degree_one_vertices": ones,
            "degree_two_vertex": degree_two[0], "degree_above_two_vertices": high_degree,
            "zero_neighbors": zero_neighbors, "zero_terminal_neighbors": zero_terminals, "unselected_exit": U}


def case_row(c, census):
    k = 19 - c
    row = {"c": c, "selected_vertex_count": k, "required_edge_count": k + 1,
           "required_spectrum": list(range(c - 1, 19))}
    if c <= 12:
        least = sum(census["sorted_eligible_degrees"][:k])
        require(least > k + 1, "degree lower bound is insufficient")
        return {**row, "reason": "degree lower bound", "least_degree_sum": least}
    return {**row, "reason": "degree pattern contradicts descending differences",
            "required_degree_two": census["degree_two_vertex"], "required_number_degree_one": k - 1,
            "excluded_degree_above_two": census["degree_above_two_vertices"],
            "descending_differences": list(range(18, c - 1, -1)),
            "forced_terminal_neighbors": census["zero_terminal_neighbors"]}


def threshold(c, census):
    if type(c) is not int or not 11 <= c <= 18:
        raise ValueError("c must be an exact integer from 11 through 18")
    return case_row(c, census)


def guard_probes(values, census):
    receipts = []
    with patch(__name__ + ".case_row", side_effect=AssertionError("invalid threshold reached evaluation")) as evaluate:
        for c in values:
            try:
                threshold(c, census)
            except ValueError as error:
                receipts.append({"input": c, "type": type(c).__name__, "error": str(error),
                                 "evaluation_calls": evaluate.call_count})
            else:
                raise ValueError("invalid threshold accepted")
        require(len(receipts) == 5 and evaluate.call_count == 0, "wrong domain probe scope")
    return receipts


def main():
    config_path = HERE / "config.json"
    config = read(config_path)
    cap = config["max_result_bytes"]
    require(git("rev-parse", "HEAD").decode().strip() == PARENT == config["parent"], "unexpected parent")
    require(config["workers"] == 1 and config["max_vertices"] == 19 and cap == 2_000_000
            and all(config[key] == 0 for key in ("solver_queries", "labeling_enumeration", "historical_replay",
                                                "new_graph_records", "new_graceful_targets", "new_attempted_enlarged_graphs"))
            and config["pins"] == PINS and config["thresholds"] == THRESHOLDS
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "wrong limits or runtime")
    OUT.mkdir()
    snapshots = {}
    for source_path in SOURCES:
        raw = (ROOT / source_path).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{source_path}").replace(b"\r\n", b"\n"),
                f"source differs from parent: {source_path}")
        write(f"source/{source_path}", raw, cap)
        snapshots[source_path] = sha(raw)
    n_config, p_config = config["1342"], config["1122"]
    sources = [n_config[key] for key in ("original", "source_original", "certificate")] + [
        p_config[key] for key in ("original", "bound_query", "certificate")]
    identity = {"run_id": config["run_id"], "parent": PARENT, "config_sha256_raw": sha(config_path.read_bytes()),
                "runner_sha256_raw": sha(Path(__file__).read_bytes()), "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
                "proof": source(PROOF), "retained_sha256_raw": {path: source(path)["sha256_raw"] for path in sources},
                "source_sha256_raw": snapshots, "runtime": {"python": sys.version, "implementation": sys.implementation.name,
                     "platform": platform.platform(), "python_executable": ".venv/Scripts/python.exe",
                     "utf8_mode": sys.flags.utf8_mode, "optional_dependencies": []}}
    ident = save("identity.json", identity, cap)

    prior_graph = read(ROOT / n_config["original"])
    source_original = read(ROOT / n_config["source_original"])
    n_cert = read(ROOT / n_config["certificate"])
    require(prior_graph == source_original and prior_graph["graph_digest"] == n_cert["original"]["graph_digest"]
            and source(n_config["source_original"])["sha256_raw"] == n_cert["original"]["sha256_raw"], "1342 bindings")
    n_original = {**source(n_config["original"]), "graph_digest": prior_graph["graph_digest"]}
    ngraph = prior_graph["graph"]
    negative = retained("1342", ngraph, n_cert["labels"], n_original, n_cert["verification"], 9, PINS, 19, config)
    require(negative["edge_ledger"] == n_cert["edge_ledger"]
            and negative["witness"] == {"path": n_cert["witness"], "distances": n_cert["witness_distances"]},
            "1342 witness or incidence ledger differs")
    negative["source_certificate"] = source(n_config["certificate"])
    negative["source_original"] = source(n_config["source_original"])

    pgraph = read(ROOT / p_config["original"])
    query = read(ROOT / p_config["bound_query"])
    p_cert = read(ROOT / p_config["certificate"])
    p_labels = p_cert["normalized"]["labels"]
    digest = query["original_graph_digest"]
    require(query["original_graph"] == pgraph and query["classification"] == "SAT"
            and query["result"]["witness"] == p_labels and query["certificate"] == p_cert["certificate"]
            and p_cert["source"] == {**source(p_config["bound_query"]), "graph_digest": digest}, "1122 bindings")
    positive = retained("1122", pgraph, p_labels, {**source(p_config["original"]), "graph_digest": digest},
                        p_cert["certificate"], 7, {H: 4, Z: 0, U: 8}, 15, config)
    positive["source_query_record"] = source(p_config["bound_query"])
    positive["source_certificate"] = source(p_config["certificate"])
    c = p_config["threshold"]
    selected = sorted(v for v, g in p_labels.items() if g >= c)
    rows = [item for item in positive["edge_ledger"] if any(v in selected for v in item["edge"])]
    weights = sorted(item["difference"] for item in rows)
    require(c == 9 and p_labels[U] < c <= 14 and weights == list(range(c - p_labels[H], 15))
            and rows == p_cert["normalized"]["selected_incident_edges"], "1122 complete incidence spectrum")
    positive["predicate"] = {"c": c, "selected_vertices": selected, "selected_ledger": rows, "selected_spectrum": weights}
    controls = [save("retained_1342.json", negative, cap), save("retained_1122.json", positive, cap)]

    census = degree_inputs(ngraph, negative)
    require(config["thresholds"] == list(range(PINS[U] + 1, len(ngraph["vertices"]))), "strict threshold domain")
    cases = [threshold(c, census) for c in config["thresholds"]]
    structural = save("structural.json", {
        "original": n_original, "pin_scope": PINS, "alpha_labels": {"low": [0, 8], "high": [9, 18]},
        "census": census, "threshold_cases": cases, "descending": {
            "zero_host": Z, "base_difference": 18, "base_pair": [0, 18], "excluded_nonterminal_zero_neighbor": "s:2",
            "higher_endpoint_rule": "larger forced terminals contribute only their own differences to zero",
            "equal_endpoint_rule": "high label j is required for difference j and forces low label zero",
            "contradicts_required_vertex": "s:0"},
        "sum_identity": {"old_sum": sum(negative["verification"]["edge_differences"]),
                         "basis": ["1", "h", "h*(h-1)/2"], "actual_coefficients": [171, "s_c+c-1", 1],
                         "required_coefficients": [171, 19, 1], "difference": "h*(s_c+c-20)", "domain": "integer h>=1"}}, cap)
    probes = save("invalid_thresholds.json", guard_probes(config["invalid_thresholds"], census), cap)
    summary = {"status": "PASS", "run_id": config["run_id"], "identity": ident, "retained_controls": controls,
               "structural": structural, "invalid_thresholds": probes, "distinct_graph_records": 2,
               "threshold_cases": len(cases), "input_rejections": 5, "solver_queries": 0, "labeling_enumeration": 0,
               "historical_replay": 0, "new_graph_records": 0, "new_graceful_targets": 0, "new_attempted_enlarged_graphs": 0}
    save("summary.json", summary, cap)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
