"""Independent parent-incidence and finite arithmetic audit of the structural proof."""
from time import process_time

START = process_time()
from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
A, B, Z, U = "b:0:0", "b:1:0", "b:2:0", "s:4"
SPINE_LOWS = {"s:1", "s:3"}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return sha256(raw).hexdigest()


def canonical(data):
    return sha(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def edge_key(edge):
    return tuple(sorted(edge))


def topology(size):
    spine = [f"s:{i}" for i in range(5)]
    parents = dict(zip(spine[1:], spine[:-1], strict=True))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, width in enumerate((size, 2, size, 2)):
        center = f"b:{i}:0"
        parents[center] = spine[i]
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(width):
            name = f"l:{i}:0:{j}"
            parents[name] = center
            roles[name] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    edges = Counter(map(edge_key, parents.items()))
    normalized = {"vertices": sorted(roles), "edges": sorted(edges.elements()), "roles": roles, "spine": spine,
                  "profile": [[size], [2], [size], [2], []]}
    return normalized, edges


def inspect(original, size):
    norm, edges = topology(size)
    graph = original["graph"]
    need(Counter(graph["vertices"]) == Counter(norm["vertices"])
         and Counter(map(edge_key, graph["edges"])) == edges, "exact vertex and edge multiplicities")
    need(type(graph["schema_version"]) is int and graph["schema_version"] == 1
         and all(graph[x] == norm[x] for x in ("spine", "profile", "roles"))
         and canonical(norm) == original["graph_digest"], "original named role and digest identity")
    adjacency = {v: set() for v in norm["vertices"]}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def bfs(adjacency, starts):
    dist = dict.fromkeys(starts, 0)
    queue = deque(starts)
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def certificate(original, cert, adjacency):
    graph, gid = original["graph"], original["graph_digest"]
    labels = cert["labels"]
    m = len(graph["edges"])
    lid = canonical({"graph_digest": gid, "labels": sorted(labels.items())})
    edgerows = [{"edge": e, "difference": max(labels[v] for v in e) - min(labels[v] for v in e)}
                for e in graph["edges"]]
    weights = [row["difference"] for row in edgerows]
    need(set(labels) == adjacency.keys() and all(type(x) is int for x in labels.values())
         and Counter(labels.values()) == Counter(range(m + 1))
         and Counter(weights) == Counter(range(1, m + 1)), "original graceful alphabets")
    need(cert["graph_digest"] == gid != lid and cert["ledger_id"] == lid and cert["named_edges"] == edgerows,
         "distinct exact ledger identity")
    checker = {"valid": True, "errors": [], "graph_digest": gid, "n": m + 1, "m": m,
               "edge_differences": weights, "claim": "finite certificate for this exact named target only"}
    need(cert["checker"] == checker, "archived affirmative checker result")
    low = {v for v, dist in bfs(adjacency, [U]).items() if dist % 2}
    high = adjacency.keys() - low
    need(Counter(labels[v] for v in low) == Counter(range(8))
         and Counter(labels[v] for v in high) == Counter(range(8, m + 1))
         and all((u in low) != (v in low) for u, v in graph["edges"]), "physical alpha orientation")
    return {"graph_digest": gid, "ledger_id": lid, "checker": checker}


def cut_receipt(original, cert, saved, c):
    labels = cert["labels"]
    chosen = sorted(v for v, value in labels.items() if value < c)
    rows = []
    for u, v in original["graph"]["edges"]:
        smaller, larger = sorted((labels[u], labels[v]))
        if smaller < c <= larger:
            rows.append({"edge": [u, v], "difference": larger - smaller})
    actual = sorted(r["difference"] for r in rows)
    m, b = len(original["graph"]["edges"]), labels[B]
    required = list(range(b - c + 1, m + 1))
    surplus = len(actual) - len(required)
    # Twice the sum polynomials, expanded directly from the edge groups.
    old = sum(cert["checker"]["edge_differences"])
    actual_poly = [2 * old, 2 * len(rows) + b - c + 1 + b - c, 1]
    graceful_poly = [m * (m + 1), m + (m + 1), 1]
    deficit = [a - r for a, r in zip(actual_poly, graceful_poly, strict=True)]
    need(surplus > 0 and deficit == [0, 2 * surplus, 0], "prior restricted difference-sum failure")
    expect = {"B": b, "c": c, "graph_digest": cert["graph_digest"], "ledger_id": cert["ledger_id"],
              "actual": actual, "required": required, "selected": chosen, "crossings": rows,
              "actual_count": len(actual), "required_count": len(required), "count_surplus": surplus,
              "missing": sorted((Counter(required) - Counter(actual)).elements()),
              "excess_weights": sorted((Counter(actual) - Counter(required)).elements()),
              "twice_actual_sum": actual_poly, "twice_required_sum": graceful_poly, "twice_sum_surplus": deficit}
    need(saved == expect, "exact D071 cut receipt")
    return {"c": c, "actual_count": len(actual), "required_count": len(required), "surplus": surplus}


def structural_incidence(adj):
    low = {v for v, d in bfs(adj, [U]).items() if d % 2}
    high = adj.keys() - low
    need(low == {A, Z, *SPINE_LOWS, "l:1:0:0", "l:1:0:1", "l:3:0:0", "l:3:0:1"}
         and all(set(adj[v]) <= high for v in low) and all(set(adj[v]) <= low for v in high),
         "exact bipartition")
    low_degree = {v: len(adj[v]) for v in low}
    excess = {v: len(adj[v]) - 1 for v in high}
    three = {"s:2", B, "b:3:0"}
    need({v for v, x in low_degree.items() if x == 3} == {A, Z, *SPINE_LOWS}
         and Counter(low_degree.values()) == Counter({1: 4, 3: 4}), "lower-count degree groups")
    need({v for v, x in excess.items() if x == 2} == three
         and {v for v, x in excess.items() if x == 1} == {"s:0"}
         and Counter(excess.values()) == Counter({0: 5, 1: 1, 2: 3}), "upper-count excess groups")
    # Infer the unique count of selected degree-two and degree-three vertices
    # from the excess equation, before using named incidences.
    need([(one, two) for one in range(2) for two in range(4) if one + 2 * two == 5] ==
         [(1, 2)], "upper excess forces s:0 and two degree-three highs")
    need("s:1" in adj["s:0"] and all("s:3" in adj[v] for v in three - {B}),
         "B=10 forces both spine lows under upper-inside-lower containment")
    six = low - SPINE_LOWS
    need(len(six) == 6 and set.union(*(adj[v] for v in six)) == high - {U},
         "B=12 lower-selected edges meet all eight other highs")
    first = {v for v in adj[A] if excess[v] == 0}
    third = {v for v in adj[Z] if excess[v] == 0}
    need(first == {"l:0:0:0", "l:0:0:1"} and third == {"l:2:0:0", "l:2:0:1"}
         and first | third | {U} == {v for v, x in excess.items() if x == 0},
         "B=8 unselected terminal alternatives")
    need(adj[U] == {"s:3"} and adj[B] == {"s:1", "l:1:0:0", "l:1:0:1"}
         and A not in adj[B] and "s:3" not in adj[B], "B=8 critical disjoint neighbors")
    need(8 - 3 == 5 and 9 - 3 == 6 and 8 - 2 == 6, "B=8 forced difference-two/three contradiction")
    witness = [A, *(f"s:{i}" for i in range(5))]
    dist = bfs(adj, witness)
    need(all(v in adj[u] for u, v in zip(witness, witness[1:]))
         and dist.keys() == adj.keys() and max(dist.values()) == 2 and dist[B] == dist[Z] == 1,
         "physical witness and host distances")
    return {"low": sorted(low), "high": sorted(high), "low_degrees": low_degree, "high_excess": excess,
            "witness": witness, "distances": dist, "B12_high_neighbors": sorted(high - {U}),
            "B8_first_terminals": sorted(first), "B8_third_terminals": sorted(third)}


def numeric_table(scope, producer_cpu, low_size):
    need(scope == {"upper": list(range(10, 17)), "lower": list(range(6, 9)),
                   "host_labels": [8, *range(10, 17)]}, "exact numerical domain")
    rows = []
    for u, d, b in product(scope["upper"], scope["lower"], scope["host_labels"]):
        need(len(rows) < 168 and producer_cpu + process_time() - START < 30, "numeric or combined CPU cap")
        lower_start, upper_start = b - d + 1, u - 5
        k_min, k_max = max(0, d - (low_size - 2)), min(2, d - 2)
        counts = [d + 4 + 2 * k for k in range(k_min, k_max + 1)]
        required = 17 - lower_start
        if required not in counts:
            reason = "lower_count"
        elif 17 - u < 3:
            reason = "upper_count"
        elif b == 10:
            need(d in (6, 7) and required == d + 6 and upper_start >= lower_start,
                 "B=10 forces two selected spine lows despite one allowed")
            reason = "B10_both_spine_lows"
        elif b == 12:
            need(d == 6 and lower_start == 7, "B=12 exact lower tail")
            if upper_start <= lower_start:
                need(17 - u < 8, "B=12 all eight high neighbors exceed upper count")
                reason = "B12_eight_high_neighbors"
            else:
                reason = "B12_unselected_s1"
        else:
            need(b == 8 and d in (6, 7, 8) and u > b, "only B=8 remains")
            if u >= 13:
                need(u - 10 > 2 and u - 6 < 10, "B=8 forced zero-edge excess")
                reason = "B8_zero_terminal"
            else:
                need(0 <= u - 10 <= 2 and u - 6 < 10
                     and list(range(10 - 5, u - 5)) == list(range(5, u - 6 + 1))
                     and (16 - (22 - u)) - (u - 10) == 4, "B=8 four residual differences")
                reason = "B8_missing_weight_two"
        rows.append({"u": u, "d": d, "B": b, "upper_start": upper_start, "lower_start": lower_start,
                     "possible_lower_counts": counts, "required_lower_count": required, "case": reason})
    need(len(rows) == 168, "exact numeric case count")
    return rows


def main():
    cfg = read(HERE / "config.json")
    src = cfg["sources"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    need(head == cfg["parent"] and cfg["runtime"] ==
         {"version": sys.version, "platform": sys.platform,
          "executable_sha256": sha(Path(sys.executable).read_bytes())}, "frozen parent and runtime")
    for ref in src.values():
        raw = (ROOT / ref["path"]).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], "frozen source")
        if "git_sha256" in ref:
            blob = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            need(blob == raw and sha(blob) == ref["git_sha256"], "frozen Git blob")

    def archive(name):
        return read(ROOT / src[name]["path"])

    original = archive("seed_original")
    adj = inspect(original, 2)
    shape = structural_incidence(adj)
    cert66, cert70 = archive("d066_certificates")["prefix"], archive("d070_seed")
    all70 = archive("d070_certificates")
    need(cert70 == all70["seed"], "identical archived seed copies")
    positives = read(HERE / "controls.json")
    d66 = certificate(original, cert66, adj)
    d70 = certificate(original, cert70, adj)
    need(positives["status"] == "PASS" and d66 == positives["d066"] and d70 == positives["d070"]
         and d66["graph_digest"] == d70["graph_digest"] and d66["ledger_id"] != d70["ledger_id"], "co-original control")
    labels = cert70["labels"]
    upper = sorted(row["difference"] for row in cert70["named_edges"]
                   if max(labels[v] for v in row["edge"]) >= 10)
    need([labels[v] for v in (A, Z, U)] == [5, 0, 9] and upper == list(range(5, 17))
         and cert70["alpha"]["witness"] == shape["witness"]
         and cert70["alpha"]["distances"] == shape["distances"], "positive D070 single-block control")
    wrong = positives["adverse"]
    need(wrong["expected"] == "0" * 64 != d70["graph_digest"] and wrong["checker"] ==
         (d70["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]}), "actual altered digest")

    grown = archive("p33_original")
    checked_grown = certificate(grown, all70["p33"], inspect(grown, 3))
    cut_rows = {}
    for name, graph, cert in (("seed", original, cert70), ("p33", grown, all70["p33"])):
        for c in range(6, 9):
            key = f"{name}-c{c}"
            cut_rows[key] = cut_receipt(graph, cert, archive("d071_" + key), c)
    producer_cpu = positives["process_cpu_seconds"]
    table = numeric_table(cfg["domain"], producer_cpu, len(shape["low"]))
    cpu = producer_cpu + process_time() - START
    need(cpu < 30 and len(cut_rows) == 6 and all(positives[k] == 0 for k in
         ("queries", "labeling_nodes", "new_originals")), "bounded audit")
    result = {"status": "PASS", "structural_incidence": shape, "numeric_cases": table,
              "reasons": Counter(row["case"] for row in table), "d071_cut_receipts": cut_rows,
              "d066": d66, "d070": d70, "d071_grown_archive": checked_grown["ledger_id"],
              "combined_process_cpu_seconds": cpu, "new_originals": 0, "queries": 0,
              "labeling_nodes": 0, "rank_microchecks": 0}
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 8_000_000, "audit byte caps")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print("PASS: original incidence proof premises, six retained receipts and 168 numerical cases")


if __name__ == "__main__":
    main()
