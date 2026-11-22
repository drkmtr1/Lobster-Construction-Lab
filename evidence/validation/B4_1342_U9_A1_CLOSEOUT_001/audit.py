"""Check the two retained originals and nine degree cases without LCL imports."""

from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = "86d3d1cf7ab140b23a9aace81c654b43b26b65af"
PROOF = "research/B4_1342_U9_A1_ANALYTIC_CLOSEOUT.md"
H, Z, U = "b:0:0", "b:2:0", "s:4"
LIMITS = {
    "workers": 1,
    "max_order": 19,
    "max_result_bytes": 2000000,
    "threshold_cases": 9,
    "solver_queries": 0,
    "labeling_enumeration": 0,
    "historical_replay": 0,
    "new_graph_profiles": 0
}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def reconstruct(original, counts, expected_digest):
    spine = [f"s:{i}" for i in range(5)]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, size in enumerate(counts):
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], center))
        for j in range(size):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
    graph_identity = {"profile": [[n] for n in counts] + [[]], "spine": spine, "roles": roles,
                      "vertices": sorted(roles), "edges": sorted(tuple(sorted(e)) for e in edges)}
    check(Counter(original["vertices"]) == Counter(roles.keys()) and
          Counter(tuple(sorted(e)) for e in original["edges"]) == Counter(graph_identity["edges"]),
          "original name and edge multiplicities")
    check(original["schema_version"] == 1 and all(original[key] == graph_identity[key]
          for key in ("profile", "spine", "roles")), "original physical roles")
    raw = json.dumps(graph_identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    check(sha(raw) == expected_digest and len(roles) <= LIMITS["max_order"], "original digest or order cap")
    adj = {v: [] for v in roles}
    for left, right in edges:
        adj[left].append(right)
        adj[right].append(left)
    colors = {U: True}
    queue = deque([U])
    while queue:
        vertex = queue.popleft()
        for neighbor in adj[vertex]:
            if neighbor not in colors:
                colors[neighbor] = not colors[vertex]
                queue.append(neighbor)
            check(colors[vertex] != colors[neighbor], "edge must cross alpha orientation")
    check(len(colors) == len(roles) == len(edges) + 1, "connected original tree")
    return adj, sorted(v for v, high in colors.items() if high)


def thresholds(adj, high):
    degrees = {v: len(adj[v]) for v in high}
    check(len(high) == 10 and sum(degrees.values()) == 18 and degrees[U] == 1, "high census")
    eligible = sorted(degrees[v] for v in high if v != U)
    check(eligible == [1, 1, 1, 1, 1, 2, 3, 3, 4], "eligible degrees")
    twos = [v for v in degrees if degrees[v] == 2]
    zeros_neighbors = sorted(adj[Z])
    terminals = [f"l:2:0:{i}" for i in range(4)]
    check(twos == ["s:0"] and degrees["s:2"] == 3 and zeros_neighbors == [*terminals, "s:2"]
          and all(adj[v] == [Z] for v in terminals), "descending induction premises")
    rows = []
    for c in range(10, 19):
        k = len(range(c, 19))
        required = len(range(c - 1, 19))
        low_sum = sum(eligible[:k])
        check(c > 9 and required == k + 1, "port and required cardinality")
        row = {"c": c, "selected_vertices": k, "required_edges": required,
               "minimum_edges": low_sum, "required_differences": [c-1, 18]}
        if c <= 12:
            check(low_sum == {10: 17, 11: 13, 12: 10}[c] and low_sum > required, "lower bound contradiction")
            row["reason"] = "minimum exceeds required"
        else:
            check(k - 1 <= eligible.count(1), "number of hypothetical degree-one vertices")
            row["reason"] = "excess one forces s:0 and excludes s:2; descending weights force only third terminals"
            row["hypothetical_degree_two_vertex"] = twos[0]
            row["hypothetical_degree_one_count"] = k - 1
            row["descending_weights"] = list(range(18, c-1, -1))
        rows.append(row)
    check(len(rows) == LIMITS["threshold_cases"], "threshold count")
    return {"degrees": degrees, "eligible_degrees_sorted": eligible,
            "zero_neighbors": zeros_neighbors, "thresholds": rows}


def positive_control(graph, bound, certificate):
    expected = bound["original_graph_digest"]
    check(bound["original_graph"] == graph and bound["classification"] == "SAT"
          and bound["certificate"] == certificate["certificate"], "1122 original and certificate binding")
    adj, high = reconstruct(graph, [1, 1, 2, 2], expected)
    labels = certificate["normalized"]["labels"]
    check(bound["result"]["witness"] == labels and set(labels) == set(adj)
          and all(type(x) is int for x in labels.values()) and sorted(labels.values()) == list(range(15))
          and {v: labels[v] for v in (U, H, Z)} == {U: 8, H: 4, Z: 0}
          and sorted(labels[v] for v in high) == list(range(7, 15)), "1122 retained alpha labels")
    ledger = [{"edge": [l, r], "difference": abs(labels[l] - labels[r])} for l, r in graph["edges"]]
    used = [row["difference"] for row in ledger]
    check(sorted(used) == list(range(1, 15)) and used == certificate["certificate"]["edge_differences"]
          and certificate["certificate"]["graph_digest"] == expected, "1122 differences")
    selected = sorted(v for v in labels if labels[v] >= 9)
    selected_rows = [row for row in ledger if any(v in selected for v in row["edge"])]
    weights = sorted(row["difference"] for row in selected_rows)
    check(weights == list(range(5, 15)) and
          selected_rows == certificate["normalized"]["selected_incident_edges"], "1122 full selected spectrum")
    return {"graph_digest": expected, "labels": labels, "edge_ledger": ledger,
            "inventories": {"used_labels": sorted(labels.values()), "used_differences": sorted(used),
                            "unused_labels": [], "unused_differences": []},
            "predicate": {"c": 9, "selected": selected, "selected_differences": weights,
                          "unselected_differences": sorted(set(used) - set(weights))}}


def main():
    config = read(HERE / "config.json")
    check(config["parent"] == PARENT == git("rev-parse", "HEAD").decode().strip()
          and config["limits"] == LIMITS and sys.version_info[:2] in ((3, 12), (3, 13))
          and sys.flags.utf8_mode == 1, "parent, limits and Python")
    refs = {}
    for path in config["retained"].values():
        raw = (ROOT / path).read_bytes()
        check(raw == git("show", f"{PARENT}:{path}"), f"retained raw bytes: {path}")
        refs[path] = sha(raw)
    inputs = {key: read(ROOT / path) for key, path in config["retained"].items()}
    original = inputs["original_1342"]
    adj, high = reconstruct(original["graph"], [1, 3, 4, 2], original["graph_digest"])
    data = thresholds(adj, high)
    positive = positive_control(inputs["original_1122"], inputs["bound_1122"], inputs["certificate_1122"])
    retained = inputs["certificate_1122"]["source"]
    bound_path = config["retained"]["bound_1122"]
    check(retained == {"path": bound_path, "sha256_raw": refs[bound_path],
                       "graph_digest": positive["graph_digest"]}, "1122 retained source receipt")
    task_files = (HERE / "config.json", HERE / "audit.py", HERE / "commands.json", ROOT / PROOF)
    result = {"status": "PASS", "id": config["id"], "parent": PARENT, "limits": LIMITS,
              "runtime": {"version": sys.version, "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode},
              "retained_sha256_raw": refs,
              "input_sha256_raw": {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in task_files},
              "original_1342": {"graph_digest": original["graph_digest"], "high": high,
                                "low": sorted(set(adj) - set(high)), "high_incidence": {v: sorted(adj[v]) for v in high},
                                **data},
              "positive_1122": positive}
    raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    check(len(raw) <= LIMITS["max_result_bytes"], "result byte cap")
    with (HERE / "audit_result.json").open("xb") as output:
        output.write(raw)
    print("PASS: two retained originals, nine thresholds, 1122 selected differences 5..14")


if __name__ == "__main__":
    main()
