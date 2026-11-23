"""Reconstruct named incidences and check structural arithmetic without label search."""
from time import process_time

START = process_time()
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
A, B, Z, U, F = "b:0:0", "b:1:0", "b:2:0", "s:4", "b:3:0"
SPINE_LOWS = {"s:1", "s:3"}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def canonical(data):
    return sha(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def edge_key(edge):
    return tuple(sorted(edge))


def topology(original):
    spine = [f"s:{i}" for i in range(5)]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    parents = dict(zip(spine[1:], spine[:-1], strict=True))
    for i in range(4):
        center = f"b:{i}:0"
        parents[center] = spine[i]
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(2):
            leaf = f"l:{i}:0:{j}"
            parents[leaf] = center
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    edges = Counter(map(edge_key, parents.items()))
    profile = [[2], [2], [2], [2], []]
    graph = original["graph"]
    need(Counter(graph["vertices"]) == Counter(roles.keys())
         and Counter(map(edge_key, graph["edges"])) == edges and len(edges) == 16,
         "named vertex and edge multiplicities")
    need(type(graph["schema_version"]) is int and graph["schema_version"] == 1
         and graph["spine"] == spine and graph["roles"] == roles and graph["profile"] == profile,
         "named original role metadata")
    norm = {"vertices": sorted(roles), "edges": sorted(edges.elements()),
            "spine": spine, "roles": roles, "profile": profile}
    need(canonical(norm) == original["graph_digest"], "canonical named graph digest")
    adjacent = {v: set() for v in roles}
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    return adjacent


def distances(adjacent, starts):
    distance = dict.fromkeys(starts, 0)
    queue = deque(starts)
    while queue:
        v = queue.popleft()
        for u in adjacent[v]:
            if u not in distance:
                distance[u] = distance[v] + 1
                queue.append(u)
    return distance


def premises(graph, adj):
    low = {v for v, dist in distances(adj, [U]).items() if dist % 2}
    high = adj.keys() - low
    need(low == {A, Z, *SPINE_LOWS, "l:1:0:0", "l:1:0:1", "l:3:0:0", "l:3:0:1"}
         and all((u in low) != (v in low) for u, v in graph["edges"]), "original alpha orientation")
    degrees = {v: len(adj[v]) for v in adj}
    need({v for v in low if degrees[v] == 3} == {A, Z, *SPINE_LOWS}
         and Counter(degrees[v] for v in low) == Counter({1: 4, 3: 4})
         and {v for v in high if degrees[v] == 3} == {"s:2", B, F}
         and {v for v in high if degrees[v] == 2} == {"s:0"}
         and Counter(degrees[v] for v in high) == Counter({1: 5, 2: 1, 3: 3}), "named degree groups")
    w = [A, *graph["spine"]]
    levels = distances(adj, w)
    need(all(v in adj[u] for u, v in zip(w, w[1:])) and levels.keys() == adj.keys()
         and max(levels.values()) == 2 and levels[A] == 0 and levels[B] == levels[Z] == 1, "physical witness")

    # In the lower count, k is the number of selected spine lows.
    candidate_b = {12 - 2 * k for k in range(3)}
    need(candidate_b - {8} == {10, 12}, "exit label excludes B=8")
    u9 = [e for e in graph["edges"] if any(v in high - {U} for v in e)]
    excess9 = len(u9) - len(high - {U})
    need(excess9 == 7 and len(u9) == 15 and adj[U] == {"s:3"}
         and 12 - 2 * len(SPINE_LOWS) == 8, "u=9 forces a=7,d=8 and a label collision")
    minimum_high, maximum_low = range(8, 17).start, range(8).stop - 1
    need(minimum_high - maximum_low == 1, "unique boundary pair for weight one")

    # Check the named premise for the descending proof and both containments.
    third = {"l:2:0:0", "l:2:0:1"}
    need(adj[Z] == {"s:2"} | third and all(adj[v] == {Z} for v in third)
         and adj["s:2"] == {Z, *SPINE_LOWS}, "forced s:2 and its two named spine neighbors")
    six = adj[A] | adj[Z]
    need(six == {"s:0", "s:2", "l:0:0:0", "l:0:0:1", *third}
         and len(six) == 6 and B not in six and 17 - len(six) == 11, "B=12 six required high neighbors")
    seven = six | {B}
    forced_cut = 17 - len(seven)
    a = sum(degrees[v] - 1 for v in seven)
    nonspine = low - SPINE_LOWS
    fourth = {"l:3:0:0", "l:3:0:1"}
    conflict = [e for e in graph["edges"] if F in e and any(v in fourth for v in e)]
    need(forced_cut == 10 and a == 5 and len(nonspine) == 6 == a + 1
         and high - seven == {F, U} and fourth <= nonspine and len(conflict) == 2
         and all(adj[v] == {F} for v in fourth), "B=12 fourth-terminal contradiction")
    # For B=10, upper start minus lower start equals
    # (u-10)+(d-(a+1)). Equality sets both nonnegative terms to zero.
    containment = {"B10_start_gap_terms": ["u-10", "d-(a+1)"],
                   "B10_equal_starts_when": ["u=10", "d=a+1"],
                   "equal_starts_imply": "equal edge sets by injective weights",
                   "B10_selected_s2_spine_edges": [e for e in graph["edges"]
                                                 if "s:2" in e and any(v in SPINE_LOWS for v in e)],
                   "B12_six_high_neighbors": sorted(six), "B12_seven_high_neighbors": sorted(seven),
                   "B12_reverse_inclusion_forced": {"u": forced_cut, "a": a, "d": 6,
                                                    "b:3:0": 9, "excluded_edges": conflict}}
    need(len(containment["B10_selected_s2_spine_edges"]) == 2, "exact conflicting spine edges")
    return {"low": sorted(low), "high": sorted(high), "degrees": degrees, "witness": w,
            "witness_distance": levels, "lower_B_after_exit_collision": sorted(candidate_b - {8}),
            "u9_conditional": {"selected_edges": u9, "excess": excess9, "forced_a": 7, "forced_d": 8,
                               "required_B": 8, "first_weight_pair": [minimum_high, maximum_low]},
            "zero_neighbors": sorted(adj[Z]), "containment": containment}


def check_archived(original, cert, state):
    labels = cert["labels"]
    weights = []
    for u, v in original["graph"]["edges"]:
        weights.append(abs(labels[u] - labels[v]))
    gid = original["graph_digest"]
    lid = canonical({"graph_digest": gid, "labels": sorted(labels.items())})
    need(set(labels) == set(state["low"] + state["high"]) and all(type(x) is int for x in labels.values())
         and Counter(labels[v] for v in state["low"]) == Counter(range(8))
         and Counter(labels[v] for v in state["high"]) == Counter(range(8, 17))
         and Counter(weights) == Counter(range(1, 17)), "complete retained alpha alphabets")
    checker = {"valid": True, "errors": [], "graph_digest": gid, "n": 17, "m": 16,
               "edge_differences": weights, "claim": "finite certificate for this exact named target only"}
    rows = [{"edge": e, "difference": w} for e, w in zip(original["graph"]["edges"], weights, strict=True)]
    need(cert["graph_digest"] == gid != lid and cert["ledger_id"] == lid and cert["named_edges"] == rows
         and cert["checker"] == checker and labels[U] == 9, "archived original and separate ledger identity")
    return {"checker": checker, "graph_digest": gid, "ledger_id": lid}


def main():
    cfg = read(HERE / "config.json")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    need(head == cfg["parent"] and cfg["runtime"] ==
         {"python": sys.version, "platform": sys.platform,
          "executable_sha256": sha(Path(sys.executable).read_bytes())}, "frozen parent/runtime")
    need(cfg["domain"] == {"a": [1, 7], "u": [9, 16], "d": "a+1..8", "B": [9, 16], "exit": 8, "zero": 0}
         and cfg["limits"]["numeric_tuples"] == 0, "exact proof-only task domain")
    for ref in cfg["sources"].values():
        raw = (ROOT / ref["path"]).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], "raw source identity")
        if "git_sha256" in ref:
            blob = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            need(blob == raw and sha(blob) == ref["git_sha256"], "parent Git source")

    def archive(name):
        return read(ROOT / cfg["sources"][name]["path"])

    original = archive("original")
    state = premises(original["graph"], topology(original))
    controls = read(HERE / "controls.json")
    d66 = check_archived(original, archive("d066_certs")["prefix"], state)
    seed = archive("d070_seed")
    d70 = check_archived(original, seed, state)
    need(controls["status"] == "PASS" and controls["retained"] == {"D066": d66, "D070": d70}
         and d66["ledger_id"] != d70["ledger_id"], "retained control receipts")
    adverse = controls["wrong_digest"]
    need(adverse["expected"] == "0" * 64 != d70["graph_digest"]
         and adverse["checker"] == d70["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]},
         "genuine wrong digest rejection")
    upper = [r for r in seed["named_edges"] if any(seed["labels"][v] >= 10 for v in r["edge"])]
    lower = {d: [r for r in seed["named_edges"] if any(seed["labels"][v] < d for v in r["edge"])]
             for d in (6, 7, 8)}
    required = {d: list(range(seed["labels"][B] - d + 1, 17)) for d in lower}
    need(sorted(r["difference"] for r in upper) == list(range(5, 17))
         and [len(lower[d]) for d in (6, 7, 8)] == [12, 15, 16]
         and all(sorted(r["difference"] for r in lower[d]) != required[d] for d in lower),
         "archived U=9 reference cuts")
    old = archive("d073_audit")
    need(old["status"] == "PASS" and old["graph_digest"] == original["graph_digest"]
         and old["retained_ledgers"] == [d66["ledger_id"], d70["ledger_id"]], "preserved D073 scope")
    cpu = cfg["setup_process_cpu_seconds"] + controls["process_cpu_seconds"] + process_time() - START
    need(cpu < 30 and all(controls[k] == 0 for k in ("solver_calls", "assignment_nodes", "new_originals")),
         "combined process CPU and execution limits")
    report = {"status": "PASS", "domain": cfg["domain"], "structural_premises": state,
              "d070_archived_U9": {"upper_at_10": upper, "lower": lower, "required_lower": required},
              "retained_ledgers": [d66["ledger_id"], d70["ledger_id"]],
              "graph_digest": original["graph_digest"], "numeric_tuples": 0, "solver_calls": 0,
              "assignment_nodes": 0, "new_originals": 0, "combined_process_cpu_seconds": cpu}
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 8_000_000, "audit evidence byte caps")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print("PASS: independent named incidences, count and containment boundaries, and archive controls")


if __name__ == "__main__":
    main()
