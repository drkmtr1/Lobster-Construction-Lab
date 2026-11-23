"""Independently reconstruct original topology, growth maps and inventories."""
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


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return sha256(raw).hexdigest()


def canonical(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha(raw)


def raw_bound(ref):
    raw = (ROOT / ref["path"]).read_bytes()
    need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], ref["path"])
    return raw


def key(edge):
    return tuple(sorted(edge))


def topology(q, t, k):
    spine = [f"s:{i}" for i in range(5 + k)]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    parents = dict(zip(spine[1:], spine[:-1], strict=True))
    for i, width in enumerate((q, 2, t, 2)):
        b = f"b:{i}:0"
        parents[b] = spine[i]
        roles[b] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(width):
            v = f"l:{i}:0:{j}"
            parents[v] = b
            roles[v] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    counts = Counter(map(key, parents.items()))
    return {"vertices": sorted(roles), "edges": sorted(counts.elements()), "spine": spine,
            "roles": roles, "profile": [[q], [2], [t], [2]] + [[]] * (k + 1)}, counts


def check(cert, ref, dims):
    original = json.loads(raw_bound(ref))
    expect, edges = topology(*dims)
    graph = original["graph"]
    need(Counter(graph["vertices"]) == Counter(expect["vertices"])
         and Counter(map(key, graph["edges"])) == edges, "original named multiplicity")
    need(graph["schema_version"] == 1 and all(graph[k] == expect[k] for k in ("spine", "roles", "profile")),
         "original named structure")
    digest = canonical(expect)
    labels = cert["labels"]
    m = len(graph["edges"])
    weights = [abs(labels[v] - labels[u]) for u, v in graph["edges"]]
    need(len(labels) == m + 1 <= 21 and Counter(labels.keys()) == Counter(expect["vertices"])
         and all(type(x) is int for x in labels.values())
         and Counter(labels.values()) == Counter(range(m + 1))
         and Counter(weights) == Counter(range(1, m + 1)), "exact label and difference alphabets")
    lid = canonical({"graph_digest": digest, "labels": sorted(labels.items())})
    need(cert["original"] == {k: ref[k] for k in ("path", "bytes", "sha256")}
         and digest == original["graph_digest"] == cert["graph_digest"] != lid
         and lid == cert["ledger_id"], "original and ledger binding")
    need(cert["checker"] == {"claim": "finite certificate for this exact named target only", "valid": True,
                             "errors": [], "m": m, "n": m + 1, "graph_digest": digest,
                             "edge_differences": weights}, "unchanged checker receipt")
    need(cert["named_edges"] == [{"edge": e, "difference": w}
                                for e, w in zip(graph["edges"], weights, strict=True)], "named edge receipt")
    return graph


def distances(graph, starts):
    neighbors = {v: [] for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].append(v)
        neighbors[v].append(u)
    result = dict.fromkeys(starts, 0)
    pending = deque(starts)
    while pending:
        v = pending.popleft()
        for other in neighbors[v]:
            if other not in result:
                result[other] = result[v] + 1
                pending.append(other)
    return result


def cut_rows(graph, labels, cut):
    rows = []
    for u, v in graph["edges"]:
        low, high = sorted((labels[u], labels[v]))
        if low < cut <= high:
            rows.append({"edge": [u, v], "difference": high - low})
    return rows


def alpha(graph, cert, cut):
    labels = cert["labels"]
    path = ["b:0:0", *graph["spine"]]
    edges = Counter(map(key, graph["edges"]))
    need(all(edges[key(e)] == 1 for e in zip(path, path[1:])), "original witness path")
    levels = distances(graph, path)
    low = sorted(v for v, d in distances(graph, ["s:4"]).items() if d % 2)
    need(sorted(labels[v] for v in low) == list(range(8))
         and all((u in low) != (v in low) for u, v in graph["edges"])
         and [labels[v] for v in ("b:0:0", "s:4", "b:2:0")] == [5, 9, 0]
         and max(levels.values()) == 2 and levels["b:2:0"] == 1, "alpha, ports and zero witness")
    rows = cut_rows(graph, labels, cut)
    chosen = sorted(v for v, x in labels.items() if x >= cut)
    need(len(rows) == sum(sum(v in e for v in chosen) for e in graph["edges"]), "complete selected incidences")
    spectrum = sorted(row["difference"] for row in rows)
    need(spectrum == list(range(cut - 5, len(labels))) and cut > 9, "complete selected tail")
    expected = {"A": [len(labels), 8, 5, 1], "L": "b:0:0", "U": "s:4", "Z": "b:2:0", "cut": cut,
                "crossings": rows, "spectrum": spectrum, "selected": chosen, "low": low,
                "witness": path, "distances": levels}
    need(cert["alpha"] == expected, "normalized receipt")


def prefilter(graph):
    high = {v for v, d in distances(graph, ["s:4"]).items() if d % 2 == 0} - {"s:4"}
    degree = Counter(v for edge in graph["edges"] for v in edge)
    excess = {v: degree[v] - 1 for v in high}
    # Polynomial support in (selected cardinality, excess) using a product,
    # independent of the producer's named-combination enumeration.
    support = {(0, 0)}
    for x in excess.values():
        support |= {(k + 1, a + x) for k, a in support}
    actual = read(HERE / "prefilter.json")
    need(excess == actual["degree_excess"], "eligible named vertices and degrees")
    rows = []
    for c in range(10, 17):
        possible = sorted(a for k, a in support if k == 17 - c)
        for a in range(1, 8):
            admitted = a in possible
            rows.append({"a": a, "c": c, "k": 17 - c, "possible_excess": possible, "admitted": admitted,
                         "reason": "degree excess can equal a" if admitted else "degree excess cannot equal a"})
    need(actual["pairs"] == rows and len(rows) == 49 and sum(x["admitted"] for x in rows) == 34,
         "complete necessary prefilter")
    return rows


def closed_formula(seed, q, t):
    h = q - 2
    prefix = {v: a if a < 10 else a + h for v, a in seed.items()}
    for j in range(2, q):
        prefix[f"l:0:0:{j}"] = 8 + j
    for j in range(2, t):
        prefix[f"l:2:0:{j}"] = 15 + h + j
    return prefix


def suffix(graph, cert, normalized):
    shifted = {v: a if a < 8 else a + 2 for v, a in normalized.items()}
    edges = graph["edges"]
    pending = [e for e in edges if any(v not in shifted for v in e)]
    used = sorted(shifted.values())
    differences = sorted(abs(shifted[u] - shifted[v]) for u, v in edges if u in shifted and v in shifted)
    r = sorted(set(range(21)) - set(used))
    d = sorted(set(range(1, 21)) - set(differences))
    path = graph["spine"][4:]
    need(r == [8, 9] and d == [1, 2] and shifted["s:4"] == 11
         and pending == [path[:2], path[1:]]
         and set(graph["vertices"]) - shifted.keys() == set(path[1:]), "physical suffix and complements")
    labels = shifted | dict(zip(path[1:], (9, 8), strict=True))
    weights = [abs(labels[u] - labels[v]) for u, v in pending]
    need(labels == cert["labels"] and weights == [2, 1] and cert["shifted_prefix"] == shifted
         and cert["pending"] == pending and cert["path"] == path and cert["R"] == r and cert["D"] == d
         and cert["port"] == ["s:4", 11] and cert["suffix_weights"] == weights, "exact saved completion")
    part = cert["partial_checker"]
    expected = {"valid": True, "complete": False, "errors": [], "n": 21, "m": 20, "frontier": ["s:4"],
                "graph_digest": cert["graph_digest"], "used_labels": used, "used_differences": differences,
                "unused_labels": r, "unused_differences": d}
    need(all(part[k] == v for k, v in expected.items()), "partial checker receipt")


def main():
    cfg = read(HERE / "config.json")
    source = cfg["sources"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    need(head == cfg["parent"] and cfg["runtime"] ==
         {"python": sys.version, "platform": sys.platform, "executable_sha256": sha(Path(sys.executable).read_bytes())},
         "runtime and Git parent")
    for ref in source.values():
        raw_bound(ref)
        if "git_sha256" in ref:
            blob = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            need(sha(blob) == ref["git_sha256"], "retained Git blob")
    controls = read(HERE / "controls.json")
    certs = read(HERE / "certificates.json")
    seed = read(HERE / "seed.json")
    need(seed == certs["seed"], "preserved seed")
    original = source["d066_original"]
    graph = check(seed, original, (2, 2, 0))
    alpha(graph, seed, 10)
    filter_rows = prefilter(graph)
    initial = seed["labels"]
    expected_rows = ([10, 2, 15, 6, 9], [5, 11, 12], [13, 1, 3], [0, 16, 14], [8, 7, 4])
    need([initial[v] for v in graph["spine"]] == expected_rows[0]
         and all([initial[v] for v in (f"b:{i}:0", f"l:{i}:0:0", f"l:{i}:0:1")] == row
                 for i, row in enumerate(expected_rows[1:])), "documented explicit seed")
    for name, dims in (("d066", (2, 2, 0)), ("d068", (2, 3, 2))):
        original_ref = source[name + "_original"]
        archive = json.loads(raw_bound(source[name + "_certificate"]))
        if name == "d066":
            archive = archive["prefix"]
        check(controls[name], original_ref, dims)
        need(all(controls[name][key] == archive[key] for key in
                 ("labels", "graph_digest", "ledger_id", "checker", "named_edges")), "archived control")
    old = controls["d066"]
    old_rows = cut_rows(graph, old["labels"], 10)
    need(seed["ledger_id"] != old["ledger_id"] and old_rows == controls["d066_c10"]
         and sorted(e["difference"] for e in old_rows) != list(range(4, 17)), "D066 predicate negative")
    bad = controls["wrong_digest"]
    need(bad["expected"] == "0" * 64 != seed["graph_digest"] and bad["checker"] ==
         (seed["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]}), "wrong-digest probe")
    need(controls["invalid_cut"] == {"c": 9, "exit": 9, "rejected": True,
                                     "error": "cut must exceed physical exit"}, "invalid physical cut probe")
    target = {}
    for name, dims in (("p32", (3, 2, 0)), ("p33", (3, 3, 0)), ("t332", (3, 3, 2))):
        cert = certs[name]
        ref = cert["original"]
        need(ref["path"] == (HERE / (name + "_original.json")).relative_to(ROOT).as_posix(), "declared original")
        target[name] = check(cert, ref, dims)
        if dims[2] == 0:
            alpha(target[name], cert, 11)
            need(cert["labels"] == closed_formula(initial, *dims[:2]), "pointwise normalized formula")
    expected_both = closed_formula(initial, 3, 3)
    expected_routes = {"first_intermediate": closed_formula(initial, 3, 2),
                       "zero_intermediate": closed_formula(initial, 2, 3),
                       "first_then_zero": expected_both, "zero_then_first": expected_both}
    need(certs["routes"] == expected_routes, "both independently derived growth routes")
    suffix(target["t332"], certs["t332"], expected_both)
    result = read(HERE / "result.json")
    need({k: v for k, v in result.items() if k != "process_cpu_seconds"} ==
         {"status": "ANALYTIC_SEED_VERIFIED", "a": 5, "c": 10, "new_originals": ["p32", "p33", "t332"],
          "retained_controls": 2, "seed_on_retained_original": 1, "adverse_rejections": 2,
          "search_invocations": 0, "assignment_nodes": 0, "prefilter_pairs": 49, "prefilter_admitted": 34}
         and {p.name for p in HERE.glob("*_original.json")} ==
         {"p32_original.json", "p33_original.json", "t332_original.json"}, "bounded accounting")
    cpu = result["process_cpu_seconds"] + process_time() - START
    need(cpu < 30, "combined process-CPU cap")
    report = {"status": "PASS", "combined_process_cpu_seconds": cpu, "new_originals": 3,
              "retained_controls": 2, "seed_ledger_id": seed["ledger_id"], "seed_graph_digest": seed["graph_digest"],
              "admitted": sum(x["admitted"] for x in filter_rows), "rejected_by_count": 15,
              "same_named_routes": True, "adverse_rejections": 2, "additional_graph_cases": 0,
              "assignment_nodes": 0, "search_invocations": 0}
    raw = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000, "audit byte budget")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print("PASS: original-bound independent audit, exact spectra, prefilter, and named routes")


if __name__ == "__main__":
    main()
