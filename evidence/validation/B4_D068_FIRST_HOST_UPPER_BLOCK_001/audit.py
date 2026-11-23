"""Reconstruct the two archived originals and audit the seven cut receipts."""
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


def need(condition, description):
    if not condition:
        raise ValueError(description)


def read(path):
    return json.loads(path.read_bytes())


def sha(data):
    return sha256(data).hexdigest()


def serialized(data):
    return json.dumps(data, separators=(",", ":"), sort_keys=True,
                      ensure_ascii=False).encode("utf-8")


def edge_key(edge):
    return tuple(sorted(edge))


def topology(t, k):
    spine = [f"s:{i}" for i in range(5 + k)]
    parent = dict(zip(spine[1:], spine[:-1], strict=True))
    roles = {s: {"kind": "spine", "section": i} for i, s in enumerate(spine)}
    for i, n in enumerate((2, 2, t, 2)):
        center = f"b:{i}:0"
        parent[center] = spine[i]
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(n):
            leaf = f"l:{i}:0:{j}"
            parent[leaf] = center
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    counts = Counter(map(edge_key, parent.items()))
    profile = [[2], [2], [t], [2]] + [[]] * (k + 1)
    norm = {"vertices": sorted(roles), "edges": sorted(counts.elements()),
            "profile": profile, "roles": roles, "spine": spine}
    return norm, counts


def inspect_original(original, cert, captured, t, k):
    norm, counts = topology(t, k)
    graph = original["graph"]
    need(Counter(graph["vertices"]) == Counter(norm["vertices"])
         and Counter(map(edge_key, graph["edges"])) == counts, "named edge or vertex multiplicity")
    need(type(graph["schema_version"]) is int and graph["schema_version"] == 1
         and all(graph[key] == norm[key] for key in ("profile", "roles", "spine")), "original roles")
    identity = sha(serialized(norm))
    labels = cert["labels"]
    weights = [abs(labels[v] - labels[u]) for u, v in graph["edges"]]
    m = len(graph["edges"])
    need(Counter(labels.keys()) == Counter(norm["vertices"])
         and all(type(a) is int for a in labels.values())
         and Counter(labels.values()) == Counter(range(m + 1))
         and Counter(weights) == Counter(range(1, m + 1)), "exact graceful alphabets")
    ledger = sha(serialized({"graph_digest": identity, "labels": sorted(labels.items())}))
    receipt = cert["checker"]
    named = [{"edge": e, "difference": w} for e, w in zip(graph["edges"], weights, strict=True)]
    need(identity != ledger and original["graph_digest"] == identity == cert["graph_digest"]
         and cert["ledger_id"] == ledger and named == cert["named_edges"], "original and ledger identities")
    need(receipt == {"valid": True, "errors": [], "n": m + 1, "m": m, "graph_digest": identity,
                     "edge_differences": weights, "claim": "finite certificate for this exact named target only"}
         and all(captured[key] == cert[key] for key in
                 ("graph_digest", "ledger_id", "labels", "named_edges", "checker")), "checker receipt")
    return counts, labels, identity


def adjacency(edges):
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    return graph


def distances(graph, starts):
    levels = dict.fromkeys(starts, 0)
    pending = deque(starts)
    while pending:
        node = pending.popleft()
        for neighbor in graph[node]:
            if neighbor not in levels:
                levels[neighbor] = levels[node] + 1
                pending.append(neighbor)
    return levels


def state(edges, labels):
    graph = adjacency(edges)
    witness = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
    need(all(edge_key(e) in edges for e in zip(witness, witness[1:])), "physical witness path")
    from_exit = distances(graph, ["s:4"])
    low = sorted(v for v, d in from_exit.items() if d % 2)
    high = sorted(v for v, d in from_exit.items() if not d % 2)
    need(sorted(labels[v] for v in low) == list(range(8))
         and sorted(labels[v] for v in high) == list(range(8, 17))
         and all((u in low) != (v in low) for u, v in edges), "all actual alpha crossings")
    levels = distances(graph, witness)
    need(levels.keys() == labels.keys() and max(levels.values()) == 2
         and levels["b:2:0"] == 1
         and [labels[v] for v in ("b:0:0", "b:2:0", "s:4")] == [6, 0, 9], "physical anchors")
    return {"alpha_low": low, "alpha_high": high, "witness": witness, "distances": levels,
            "host": ["b:0:0", 6], "zero": ["b:2:0", 0], "exit": ["s:4", 9]}


def audit_cut(groups, labels, c):
    # Group by the numerically larger endpoint. Alpha and the strict cut
    # imply the smaller endpoint of every selected old edge is unshifted.
    edges = sorted(edge for upper, group in groups.items() if upper >= c for edge in group)
    need(all(min(labels[v] for v in edge) < c for edge in edges), "single shifted endpoint")
    entries = [{"edge": list(e), "difference": max(labels[v] for v in e) - min(labels[v] for v in e)}
               for e in edges]
    actual = sorted(x["difference"] for x in entries)
    required = list(range(c - labels["b:0:0"], max(labels.values()) + 1))
    missed = list((Counter(required) - Counter(actual)).elements())
    excessive = list((Counter(actual) - Counter(required)).elements())
    deficit = len(missed) - len(excessive)
    # Expand (m+h)(m+h+1), and the fresh progression
    # h*((c-a)+(c-a+h-1)), adding the old weights and their increment.
    m, a = max(labels.values()), labels["b:0:0"]
    target_poly = [m * (m + 1), m + (m + 1), 1]
    original_twice = 2 * sum(abs(labels[v] - labels[u]) for group in groups.values() for u, v in group)
    transformed_poly = [original_twice, 2 * len(edges) + (c - a) + (c - a - 1), 1]
    delta = [target_poly[i] - transformed_poly[i] for i in range(3)]
    need(deficit > 0 and delta == [0, 2 * deficit, 0] and len(required) == 23 - c, "all-batch necessity")
    computed = {"c": c, "selected": sorted(v for v in labels if labels[v] >= c), "crossings": entries,
                "actual": actual, "required": required, "selected_count": len(actual),
                "required_count": len(required), "deficit": deficit, "missing": sorted(missed),
                "excess": sorted(excessive), "twice_actual_sum": transformed_poly,
                "twice_required_sum": target_poly, "twice_sum_deficit": delta}
    need(read(HERE / f"cut-{c}.json") == computed, f"c={c} independent receipt mismatch")
    return computed


def main():
    cfg = read(HERE / "config.json")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    need(head == cfg["parent"] and cfg["cuts"] == list(range(10, 17)), "frozen scope")
    need(cfg["runtime"] == {"python": sys.version, "platform": sys.platform,
                            "exe_sha256": sha(Path(sys.executable).read_bytes())}, "frozen runtime")
    for ref in cfg["sources"].values():
        raw = (ROOT / ref["path"]).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], "frozen byte identity")
        if "git_sha256" in ref:
            git_raw = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            need(sha(git_raw) == ref["git_sha256"]
                 and raw.replace(b"\r\n", b"\n") == git_raw.replace(b"\r\n", b"\n"), "parent byte identity")

    def input_file(key):
        return read(ROOT / cfg["sources"][key]["path"])

    controls = read(HERE / "controls.json")
    pc = input_file("d066_certificate")["prefix"]
    tc = input_file("d068_certificate")
    need(tc["original"] == {field: cfg["sources"]["d068_original"][field]
                            for field in ("bytes", "path", "sha256")}, "D068 archive certificate path")
    edges, labels, identity = inspect_original(input_file("d066_original"), pc,
                                               controls["verified"]["D066_P"], 2, 0)
    inspect_original(input_file("d068_original"), tc, controls["verified"]["D068_T_3_2"], 3, 2)
    need(controls["prefix_state"] == state(edges, labels), "supplied alpha state")
    wrong = controls["wrong_digest"]
    expected_bad = pc["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]}
    need(wrong["expected"] == "0" * 64 != identity and wrong["checker"] == expected_bad,
         "actual digest rejection receipt")
    groups = {}
    for edge in edges:
        groups.setdefault(max(labels[v] for v in edge), []).append(edge)
    producer = read(HERE / "result.json")
    need({k: v for k, v in producer.items() if k != "process_cpu_seconds"} ==
         {"status": "EXHAUSTED_RESTRICTED_NEGATIVE", "cuts": list(range(10, 17)), "retained_positives": 2,
          "adverse_rejections": 1, "new_originals": 0, "queries": 0, "enumeration_nodes": 0,
          "replays": 0, "retries": 0}, "producer accounting")
    rows = []
    for c in range(10, 17):
        need(process_time() - START + producer["process_cpu_seconds"] < 30, "combined CPU cap")
        rows.append(audit_cut(groups, labels, c))
    cpu = process_time() - START
    total_cpu = producer["process_cpu_seconds"] + cpu
    need(total_cpu < 30 and {p.name for p in HERE.glob("cut-*.json")} ==
         {f"cut-{c}.json" for c in range(10, 17)}, "complete bounded audit")
    report = {"status": "PASS", "cuts": rows, "retained_positives": 2, "adverse_rejections": 1,
              "new_originals": 0, "queries": 0, "process_cpu_seconds": cpu,
              "combined_process_cpu_seconds": total_cpu}
    data = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(data) <= 2_000_000 and total + len(data) <= 6_000_000, "audit byte cap")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(data)
    print("Audit PASS: two original incidences, seven cut receipts and symbolic sum coefficients")


if __name__ == "__main__":
    main()
