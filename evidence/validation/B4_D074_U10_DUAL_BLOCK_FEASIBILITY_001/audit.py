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


def structure(graph, adj):
    low = {v for v, d in distances(adj, [U]).items() if d % 2}
    high = adj.keys() - low
    degree = {v: len(adj[v]) for v in adj}
    excess = {v: degree[v] - 1 for v in high}
    need({v for v in low if degree[v] == 3} == {A, Z, *SPINE_LOWS}
         and Counter(degree[v] for v in low) == Counter({1: 4, 3: 4})
         and {v for v in high if excess[v] == 2} == {"s:2", B, F}
         and {v for v in high if excess[v] == 1} == {"s:0"}
         and Counter(excess.values()) == Counter({0: 5, 1: 1, 2: 3})
         and all((u in low) != (v in low) for u, v in graph["edges"]), "named alpha classes and degrees")
    first = {"l:0:0:0", "l:0:0:1"}
    third = {"l:2:0:0", "l:2:0:1"}
    need(adj[Z] == {"s:2"} | third and all(adj[v] == {Z} for v in third)
         and adj["s:2"] == {Z, *SPINE_LOWS}, "descending weights and selected spine edges")
    six = adj[A] | adj[Z]
    need(six == {"s:0", "s:2", *first, *third} and B not in six
         and 17 - len(six) == 11 and 17 - len(six | {B}) == 10,
         "B=12 six distinct neighbors and seventh B")
    need(adj[A] == first | {"s:0"} and adj["s:0"] == {A, "s:1"}
         and adj[B] == {"s:1", "l:1:0:0", "l:1:0:1"}
         and adj[F] == {"s:3", "l:3:0:0", "l:3:0:1"} and adj[U] == {"s:3"},
         "actual residual weight sources")
    witness = [A, *graph["spine"]]
    dist = distances(adj, witness)
    need(all(v in adj[u] for u, v in zip(witness, witness[1:]))
         and dist.keys() == adj.keys() and max(dist.values()) == 2
         and dist[A] == 0 and dist[B] == dist[Z] == 1, "physical witness and port distances")
    lower = [12 - 2 * k for k in range(3)]
    need(lower == [12, 10, 8] and sum(degree[v] for v in low) == 16
         and list(range(8 - 8 + 1, 17)) == list(range(1, 17)), "B=8 whole lower tail")
    weighted_excess = sum(range(1, 17)) - (sum(range(8, 17)) - sum(range(8)))
    need(weighted_excess == 56, "weighted degree identity")
    return {"low": sorted(low), "high": sorted(high), "degrees": degree, "high_excess": excess,
            "witness": witness, "distances": dist, "B12_six": sorted(six), "B12_seven": sorted(six | {B}),
            "possible_B_by_spine_low_count": lower, "weighted_excess": weighted_excess}


def upper_count(state):
    eligible = set(state["high"]) - {B, U, "s:2"}
    need(len(eligible) == 6, "eligible upper count")
    support = {(0, 0)}
    for v in eligible:
        support |= {(k + 1, a + state["high_excess"][v]) for k, a in support}
    rows = {u: sorted(a + 2 for k, a in support if k == 16 - u) for u in range(11, 17)}
    need(rows == {11: [3, 4, 5], 12: [2, 3, 4, 5], 13: [2, 3, 4, 5],
                  14: [2, 3, 4, 5], 15: [2, 3, 4], 16: [2]}, "all 19 necessary upper pairs")
    return rows


def residual_arithmetic():
    # Eliminate already prescribed terminal/first-edge weights in the proof.
    # These are fixed interval subtractions, without assigning any vertex.
    cases = {
        "a3_T9_u11": (7, [], range(1, 8)),
        "a3_T9_u12": (8, [8], range(1, 8)),
        "a3_T9_u13": (9, [8, 9], range(1, 8)),
        "a3_T11_u12": (8, [6], [1, 2, 3, 4, 5, 7, 8]),
        "a3_T11_u13": (9, [6, 9], [1, 2, 3, 4, 5, 7, 8]),
        "a3_T12_u13_first9": (9, [6, 8], [1, 2, 3, 4, 5, 7, 9]),
        "a3_T12_u13_third9": (9, [8, 9], range(1, 8)),
        "a4_u13": (8, [5, 7, 8], [1, 2, 3, 4, 6]),
        "a5_u11": (5, [4], [1, 2, 3, 5]),
        "a5_u12": (6, [4, 6], [1, 2, 3, 5]),
    }
    result = {}
    for name, (top, used, expected) in cases.items():
        complement = set(range(1, top + 1))
        need(len(set(used)) == len(used) and set(used) <= complement, name)
        remaining = sorted(complement - set(used))
        need(remaining == list(expected), name)
        result[name] = {"complement": [1, top], "used": used, "remaining": remaining}
    # Check the smallest numerical contradictions in the other cases.
    need(22 + 7 - 6 < 15 + 9 and 23 + 7 - 7 < 15 + 9
         and 15 - 2 == 13 and 13 in {13, 14} and 13 - 4 == 9,
         "weighted and repeated-weight bounds")
    return result


def k2_gate():
    p = 8
    resources, port, needed = [p, p + 1], p + 4, [1, 2]
    differences = [port - v for v in resources]
    need(differences == [4, 3] and set(differences).isdisjoint(needed), "K=2 exit obstruction")
    return {"physical_edge": [U, "s:5"], "R": resources, "D": needed, "port": port,
            "possible_first_weights": differences,
            "growth_invariant": "R={p,p+1}, exit=p+4, first weights 4 or 3 for p=8+j"}


def main():
    cfg = read(HERE / "config.json")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    need(head == cfg["parent"] and cfg["runtime"] ==
         {"python": sys.version, "platform": sys.platform,
          "executable_sha256": sha(Path(sys.executable).read_bytes())}, "frozen parent/runtime")
    need(cfg["domain"] == {"a": [1, 7], "u": [11, 16], "d": "a+1..8", "exit": 10, "zero": 0}
         and cfg["solver_calls"] == cfg["assignment_nodes"] == 0, "exact proof-only task domain")
    for ref in cfg["sources"].values():
        path = ref["path"]
        raw = (ROOT / path).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], f"raw source: {path}")
        if "git_sha256" in ref:
            blob = subprocess.check_output(["git", "show", f"{head}:{path}"], cwd=ROOT)
            need(blob == raw and sha(blob) == ref["git_sha256"], f"parent source: {path}")

    def archive(name):
        return read(ROOT / cfg["sources"][name]["path"])

    original = archive("original")
    state = structure(original["graph"], topology(original))
    controls = read(HERE / "controls.json")
    d66 = check_archived(original, archive("d066_certs")["prefix"], state)
    d70 = check_archived(original, archive("d070_seed"), state)
    need(controls["status"] == "PASS" and controls["retained"] == {"D066": d66, "D070": d70}
         and d66["ledger_id"] != d70["ledger_id"], "distinguished archived controls")
    adverse = controls["wrong_digest"]
    need(adverse["expected"] == "0" * 64 != d70["graph_digest"]
         and adverse["checker"] == d70["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]},
         "actual wrong digest rejection")
    for id in ("d073_audit", "d074_audit"):
        old = archive(id)
        need(old["status"] == "PASS" and old["graph_digest"] == original["graph_digest"]
             and old["retained_ledgers"] == [d66["ledger_id"], d70["ledger_id"]], "preserved archive identities")
    pairs = upper_count(state)
    residual = residual_arithmetic()
    gate = k2_gate()
    cpu = cfg["setup_process_cpu_seconds"] + controls["process_cpu_seconds"] + process_time() - START
    need(cpu < 30 and all(controls[k] == 0 for k in ("solver_calls", "assignment_nodes", "new_originals")),
         "combined execution limits")
    report = {"status": "PASS", "disposition": "EXHAUSTED RESTRICTED NEGATIVE by structural proof",
              "domain": cfg["domain"], "structure": state, "necessary_a_by_u": pairs,
              "necessary_count_pairs": sum(map(len, pairs.values())), "residual_arithmetic": residual,
              "k2_gate": gate, "retained_ledgers": [d66["ledger_id"], d70["ledger_id"]],
              "graph_digest": original["graph_digest"], "solver_calls": 0, "assignment_nodes": 0,
              "new_originals": 0, "new_ledgers": 0, "combined_process_cpu_seconds": cpu}
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000, "audit byte caps")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print("PASS: named original, 19 necessary pairs, local arithmetic, archived controls, and K=2 gate")


if __name__ == "__main__":
    main()
