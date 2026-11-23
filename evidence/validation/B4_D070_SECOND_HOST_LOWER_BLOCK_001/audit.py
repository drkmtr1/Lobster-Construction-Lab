"""Independently reconstruct the retained named graphs and lower-cut spectra."""
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


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def read(path):
    return json.loads(path.read_bytes())


def key(edge):
    return tuple(sorted(edge))


def topology(q, t):
    spine = [f"s:{i}" for i in range(5)]
    parent = dict(zip(spine[1:], spine[:-1], strict=True))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, count in enumerate((q, 2, t, 2)):
        b = f"b:{i}:0"
        parent[b] = spine[i]
        roles[b] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(count):
            v = f"l:{i}:0:{j}"
            parent[v] = b
            roles[v] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    edges = Counter(map(key, parent.items()))
    norm = {"vertices": sorted(roles), "edges": sorted(edges.elements()), "spine": spine,
            "roles": roles, "profile": [[q], [2], [t], [2], []]}
    return norm, edges


def bfs(adjacency, sources):
    distance = dict.fromkeys(sources, 0)
    todo = deque(sources)
    while todo:
        u = todo.popleft()
        for v in adjacency[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                todo.append(v)
    return distance


def check_prefix(cfg, archived, control, labels, q, t, name):
    ref = cfg["sources"][name + "_original"]
    original = read(ROOT / ref["path"])
    graph = original["graph"]
    norm, edges = topology(q, t)
    require(graph["schema_version"] == 1 and all(graph[k] == norm[k] for k in ("profile", "roles", "spine"))
            and Counter(graph["vertices"]) == Counter(norm["vertices"])
            and Counter(map(key, graph["edges"])) == edges, "exact named original multiplicities")
    digest = canonical(norm)
    lid = canonical({"graph_digest": digest, "labels": sorted(labels.items())})
    identity = {k: ref[k] for k in ("path", "bytes", "sha256")}
    require(digest == original["graph_digest"] == control["graph_digest"] == archived["graph_digest"]
            and lid != digest and lid == archived["ledger_id"] == control["ledger_id"]
            and identity == archived["original"] == control["original"], "original and distinct ledger binding")
    require(labels == control["labels"] == archived["labels"], "specified supplied labels")
    m = len(graph["edges"])
    rows = [{"edge": e, "difference": max(labels[v] for v in e) - min(labels[v] for v in e)}
            for e in graph["edges"]]
    weights = [row["difference"] for row in rows]
    require(Counter(labels.keys()) == Counter(norm["vertices"]) and all(type(x) is int for x in labels.values())
            and Counter(labels.values()) == Counter(range(m + 1))
            and Counter(weights) == Counter(range(1, m + 1)), "complete spectra")
    checker = {"valid": True, "errors": [], "graph_digest": digest, "n": m + 1, "m": m,
               "edge_differences": weights, "claim": "finite certificate for this exact named target only"}
    require(checker == control["checker"] == archived["checker"] and rows == archived["named_edges"]
            == control["named_edges"], "unchanged checker receipt")
    adjacency = {v: [] for v in norm["vertices"]}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    low = sorted(v for v, distance in bfs(adjacency, ["s:4"]).items() if distance % 2)
    high = set(labels) - set(low)
    path = ["b:0:0", *norm["spine"]]
    distance = bfs(adjacency, path)
    anchors = {key: [v, labels[v]] for key, v in (("L", "b:0:0"), ("B", "b:1:0"),
                                                  ("U", "s:4"), ("Z", "b:2:0"))}
    require(all(edges[key(pair)] == 1 for pair in zip(path, path[1:]))
            and distance.keys() == labels.keys() and max(distance.values()) == 2
            and distance["b:1:0"] == distance["b:2:0"] == 1
            and sorted(labels[v] for v in low) == list(range(8))
            and sorted(labels[v] for v in high) == list(range(8, m + 1))
            and all((u in high) != (v in high) for u, v in edges), "physical alpha and witness")
    require(control["alpha_low"] == low == archived["alpha"]["low"]
            and distance == control["distances"] == archived["alpha"]["distances"]
            and control["witness"] == archived["alpha"]["witness"] == path
            and control["anchors"] == anchors
            and [anchors[x][1] for x in ("L", "B", "U", "Z")] == [5, q + 11, 9, 0], "physical labels")
    shifted = {v: labels[v] + (2 if v in high else 0) for v in labels}
    used = {abs(shifted[u] - shifted[v]) for u, v in edges}
    r = sorted(set(range(m + 3)).difference(shifted.values()))
    d = sorted(set(range(1, m + 3)).difference(used))
    require(control["normalized_resources"] == {"R": [], "D": []} and r == [8, 9] and d == [1, 2]
            and control["numerical_shift_K2"] == {"R": r, "D": d, "physical_exit": ["s:4", shifted["s:4"]]}
            and shifted["s:4"] == 11, "exact numeric resource complements")
    require([control[k] for k in ("q", "t", "h", "k", "m")] == [q, t, q - 2, t - 2, m], "parameters")
    return graph, low


def cut_audit(graph, labels, low, control, c, name):
    chosen = [v for v in low if labels[v] < c]
    groups = {v: [] for v in low}
    for u, v in graph["edges"]:
        groups[u if labels[u] < 8 else v].append((u, v))
    selected = {e for v in chosen for e in groups[v]}
    rows = [{"edge": e, "difference": abs(labels[e[0]] - labels[e[1]])}
            for e in graph["edges"] if tuple(e) in selected]
    require(len(selected) == len(rows) == sum(len(groups[v]) for v in chosen), "low incidence multiplicities")
    actual = sorted(row["difference"] for row in rows)
    m, b = len(graph["edges"]), labels["b:1:0"]
    required = list(range(b + 1 - c, m + 1))
    old = 2 * sum(labels[v] - labels[u] for u in low for edge in groups[u] for v in edge if v != u)
    # Expand (m+j)(m+j+1) and j*((B-c+1)+(B-c+j)).
    actual_poly = [old, 2 * len(selected) + (b - c + 1) + (b - c), 1]
    required_poly = [m * (m + 1), m + (m + 1), 1]
    gap = [a - r for a, r in zip(actual_poly, required_poly, strict=True)]
    surplus = len(rows) - len(required)
    require(surplus == control["h"] + (3 if c == 6 else 5) and gap == [0, 2 * surplus, 0]
            and len(required) == c + 3 + control["k"], "quantified sum coefficient")
    expected = {"B": b, "c": c, "selected": chosen, "crossings": rows, "actual": actual, "required": required,
                "actual_count": len(actual), "required_count": len(required), "count_surplus": surplus,
                "missing": sorted((Counter(required) - Counter(actual)).elements()),
                "excess_weights": sorted((Counter(actual) - Counter(required)).elements()),
                "twice_actual_sum": actual_poly, "twice_required_sum": required_poly, "twice_sum_surplus": gap,
                "graph_digest": control["graph_digest"], "ledger_id": control["ledger_id"]}
    require(read(HERE / f"{name}-c{c}.json") == expected, "complete named cut receipt")
    return expected


def main():
    cfg = read(HERE / "config.json")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    require(head == cfg["parent"] and cfg["runtime"] ==
            {"python": sys.version, "platform": sys.platform, "exe_sha256": sha(Path(sys.executable).read_bytes())},
            "source and runtime guard")
    for ref in cfg["sources"].values():
        raw = (ROOT / ref["path"]).read_bytes()
        require(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], "raw identity")
        if "git_sha256" in ref:
            blob = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            require(raw == blob and sha(blob) == ref["git_sha256"], "inherited byte identity")
    require(cfg["cases"] == {"seed": [2, 2], "p33": [3, 3]} and cfg["cuts"] == [6, 7, 8], "exact case scope")
    archive = read(ROOT / cfg["sources"]["d070_certificates"]["path"])
    retained = read(HERE / "controls.json")
    require(set(retained["retained"]) == {"seed", "p33"}
            and archive["seed"] == read(ROOT / cfg["sources"]["d070_seed"]["path"]), "retained bindings")
    original = {f"s:{i}": x for i, x in enumerate((10, 2, 15, 6, 9))}
    for i, (b, l, r) in enumerate(((5, 11, 12), (13, 1, 3), (0, 16, 14), (8, 7, 4))):
        original.update({f"b:{i}:0": b, f"l:{i}:0:0": l, f"l:{i}:0:1": r})
    grown = {v: x + 1 if x >= 10 else x for v, x in original.items()}
    grown |= {"l:0:0:2": 10, "l:2:0:2": 18}
    producer = read(HERE / "result.json")
    names = [f"{n}-c{c}" for n in ("seed", "p33") for c in (6, 7, 8)]
    require({k: v for k, v in producer.items() if k != "process_cpu_seconds"} ==
            {"status": "PASS", "cuts": names, "retained_originals": 2, "new_originals": 0,
             "adverse_rejections": 1, "queries": 0, "enumeration_nodes": 0,
             "replays": 0, "retries": 0}, "producer accounting")
    reports = {}
    for name, labels, q, t in (("seed", original, 2, 2), ("p33", grown, 3, 3)):
        control = retained["retained"][name]
        graph, low = check_prefix(cfg, archive[name], control, labels, q, t, name)
        for c in range(6, 9):
            require(producer["process_cpu_seconds"] + process_time() - START < 30, "combined CPU cap")
            reports[f"{name}-c{c}"] = cut_audit(graph, labels, low, control, c, name)
    wrong = retained["wrong_digest"]
    checked = retained["retained"]["seed"]["checker"]
    require(wrong["expected"] == "0" * 64 != checked["graph_digest"] and wrong["checker"] ==
            (checked | {"valid": False, "errors": ["original graph digest mismatch"]}), "digest adverse receipt")
    cpu = producer["process_cpu_seconds"] + process_time() - START
    require(cpu < 30 and set(reports) == set(names) and len(reports) <= 6
            and {x.name for x in HERE.glob("*-c[678].json")} == {n + ".json" for n in names}, "bounded check count")
    record = {"status": "PASS", "cut_checks": 6, "combined_cut_checks": 12, "retained_originals": 2,
              "new_originals": 0, "queries": 0, "adverse_rejections": 1,
              "combined_process_cpu_seconds": cpu, "cuts": reports}
    raw = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    require(len(raw) <= 2_000_000 and total + len(raw) <= 8_000_000, "audit byte caps")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print("PASS: six independently reconstructed cuts and signed sum coefficients")


if __name__ == "__main__":
    main()
