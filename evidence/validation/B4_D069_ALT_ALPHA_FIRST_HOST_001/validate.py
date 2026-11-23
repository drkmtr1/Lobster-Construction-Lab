"""Validate the explicit analytic supplier and the three declared originals."""
from time import process_time

START = process_time()
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

A, C = 5, 10
H, Z, U = "b:0:0", "b:2:0", "s:4"
W = [H, *(f"s:{i}" for i in range(5))]
CASES = {"p32": (3, 2, 0), "p33": (3, 3, 0), "t332": (3, 3, 2)}
SEED = {f"s:{i}": value for i, value in enumerate((10, 2, 15, 6, 9))}
for i, (b, first, second) in enumerate(((5, 11, 12), (13, 1, 3), (0, 16, 14), (8, 7, 4))):
    SEED.update({f"b:{i}:0": b, f"l:{i}:0:0": first, f"l:{i}:0:1": second})


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return sha256(raw).hexdigest()


def identity(path):
    raw = (ROOT / path).read_bytes()
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def save(name, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000, "byte budget")
    with (HERE / name).open("xb") as out:
        out.write(raw)


def load_config():
    cfg = read(HERE / "config.json")
    need(cfg["cases"] == {key: list(args) for key, args in CASES.items()}
         and cfg["limits"] == {"workers": 1, "cpu_seconds": 30, "node_cap_if_needed": 250_000,
                              "record_bytes": 2_000_000, "total_bytes": 10_000_000,
                              "max_order": 21, "new_originals": 3, "adverse_max": 2}
         and cfg["search"] == "skipped: analytic supply", "fixed scope")
    need(git("rev-parse", "HEAD").decode().strip() == cfg["parent"], "parent")
    need(sys.version_info[:2] in {(3, 12), (3, 13)} and cfg["runtime"] ==
         {"python": sys.version, "platform": sys.platform, "executable_sha256": sha(Path(sys.executable).read_bytes())},
         "frozen runtime")
    for ref in cfg["sources"].values():
        path = ref["path"]
        need(all(ref[k] == v for k, v in identity(path).items()), f"raw source: {path}")
        if "git_sha256" in ref:
            need(sha(git("show", f"{cfg['parent']}:{path}")) == ref["git_sha256"], f"Git source: {path}")
    return cfg


def key(edge):
    return tuple(sorted(edge))


def edge_rows(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]


def certify(original, labels, source):
    g, digest = original["graph"], original["graph_digest"]
    check = verify_certificate(g, labels, digest)
    need(check["valid"] and check["graph_digest"] == digest
         and check["n"] <= 21, "unchanged original-target checker")
    ledger = json.dumps({"graph_digest": digest, "labels": sorted(labels.items())},
                        sort_keys=True, separators=(",", ":")).encode()
    return {"original": source, "graph_digest": digest, "ledger_id": sha(ledger),
            "labels": labels, "named_edges": edge_rows(g, labels), "checker": check}


def check_archived(record, archive):
    need(all(record[k] == v for k, v in archive.items() if k in record), "retained certificate mismatch")


def selected(graph, labels, cut):
    need(type(cut) is int and labels[U] < cut <= max(labels.values()), "cut must exceed physical exit")
    rows = [row for row in edge_rows(graph, labels) if any(labels[v] >= cut for v in row["edge"])]
    need(all(sum(labels[v] >= cut for v in row["edge"]) == 1 for row in rows), "crossing count")
    return rows


def alpha_state(graph, labels, cut):
    n = len(labels)
    rows = selected(graph, labels, cut)
    need(sorted(x["difference"] for x in rows) == list(range(cut - A, n))
         and sorted(labels.values()) == list(range(n))
         and sorted(x["difference"] for x in edge_rows(graph, labels)) == list(range(1, n))
         and all((labels[u] < 8) != (labels[v] < 8) for u, v in graph["edges"]), "full normalized state")
    need([labels[v] for v in (H, U, Z)] == [A, 9, 0], "physical ports and distinct zero host")
    edges = set(map(key, graph["edges"]))
    need(len(edges) == n - 1 and all(key(e) in edges for e in zip(W, W[1:])), "named witness")
    distances = dict.fromkeys(W, 0)
    for d in (1, 2):
        layer = [v for v in labels if v not in distances and any(key((v, u)) in edges for u in distances)]
        distances.update(dict.fromkeys(layer, d))
    need(distances.keys() == labels.keys() and distances[Z] == 1, "physical distances")
    return {"cut": cut, "selected": sorted(v for v in labels if labels[v] >= cut),
            "crossings": rows, "spectrum": sorted(x["difference"] for x in rows),
            "low": sorted(v for v in labels if labels[v] < 8),
            "L": H, "U": U, "Z": Z, "witness": W, "distances": distances, "A": [n, 8, A, 1]}


def prefilter(graph):
    degree = Counter(v for e in graph["edges"] for v in e)
    highs = sorted(v for v, x in SEED.items() if x >= 8 and v != U)
    excess = {v: degree[v] - 1 for v in highs}
    need(sorted(excess.values()) == [0, 0, 0, 0, 1, 2, 2, 2], "physical degree excess")
    rows = []
    for c in range(10, 17):
        candidates = {sum(excess[v] for v in subset) for subset in combinations(highs, 17 - c)}
        for a in range(1, 8):
            rows.append({"a": a, "c": c, "k": 17 - c, "possible_excess": sorted(candidates),
                         "admitted": a in candidates,
                         "reason": "degree excess can equal a" if a in candidates else "degree excess cannot equal a"})
    need(len(rows) == 49 and sum(row["admitted"] for row in rows) == 34, "prefilter counts")
    return {"degree_excess": excess, "pairs": rows}


def grow_first(labels, cut, name):
    need(labels[H] == A and name not in labels and cut > labels[U], "first attachment state")
    return {v: x + (x >= cut) for v, x in labels.items()} | {name: cut}


def grow_third(labels, name):
    need(labels[Z] == 0 and name not in labels, "third attachment state")
    return labels | {name: len(labels)}


def preserve(graph, previous, edges):
    old = previous["graph"]
    need(Counter(graph["vertices"]) == Counter(old["vertices"]) + Counter(v for _, v in edges)
         and Counter(map(key, graph["edges"])) == Counter(map(key, old["edges"])) + Counter(map(key, edges)),
         "exact named extension")


def main():
    cfg = load_config()
    source = cfg["sources"]
    archived = lambda name: read(ROOT / source[name]["path"])
    p2 = archived("d066_original")
    p2_ref = identity(source["d066_original"]["path"])
    retained = archived("d066_certificate")["prefix"]
    old = certify(p2, retained["labels"], p2_ref)
    check_archived(old, retained)
    q = archived("d068_certificate")
    t_ref = identity(source["d068_original"]["path"])
    need(q["original"] == t_ref, "D068 retained original binding")
    control = certify(archived("d068_original"), q["labels"], t_ref)
    check_archived(control, q)
    old_cut = selected(p2["graph"], retained["labels"], C)
    need(sorted(row["difference"] for row in old_cut) == archived("d069_cut10")["actual"]
         and sorted(row["difference"] for row in old_cut) != list(range(C - 6, 17)), "D066 predicate negative")
    filters = prefilter(p2["graph"])
    save("prefilter.json", filters)
    seed = certify(p2, SEED, p2_ref)
    seed["alpha"] = alpha_state(p2["graph"], SEED, C)
    need(seed["graph_digest"] == "35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4"
         and len({seed["graph_digest"], seed["ledger_id"], old["ledger_id"]}) == 3, "co-original ledger identity")
    wrong = verify_certificate(p2["graph"], SEED, "0" * 64)
    need(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "wrong-digest adverse")
    try:
        selected(p2["graph"], SEED, 9)
    except ValueError as exc:
        invalid_cut = {"c": 9, "exit": 9, "rejected": True, "error": str(exc)}
    else:
        raise ValueError("invalid cut accepted")
    save("controls.json", {"d066": old, "d068": control, "d066_c10": old_cut,
                           "wrong_digest": {"expected": "0" * 64, "checker": wrong}, "invalid_cut": invalid_cut})
    save("seed.json", seed)

    originals, refs = {}, {}
    for name, (q, t, k) in CASES.items():
        graph = build_graph([[q], [2], [t], [2]] + [[]] * (k + 1))
        need(len(graph["vertices"]) <= 21, "order cap")
        record = {"graph": graph, "graph_digest": graph_digest(graph)}
        filename = name + "_original.json"
        save(filename, record)
        refs[name] = identity((HERE / filename).relative_to(ROOT).as_posix())
        originals[name] = read(HERE / filename)
    first, third = "l:0:0:2", "l:2:0:2"
    p32, p33, t332 = (originals[name] for name in CASES)
    preserve(p32["graph"], p2, [(H, first)])
    preserve(p33["graph"], p32, [(Z, third)])
    first_step = grow_first(SEED, C, first)
    zero_step = grow_third(SEED, third)
    first_then_zero = grow_third(first_step, third)
    zero_then_first = grow_first(zero_step, C, first)
    need(first_then_zero == zero_then_first and first_then_zero[first] == 10
         and first_then_zero[third] == 18, "named pointwise composition")
    first_cert = certify(p32, first_step, refs["p32"]) | {"alpha": alpha_state(p32["graph"], first_step, 11)}
    both_cert = certify(p33, first_then_zero, refs["p33"]) | {"alpha": alpha_state(p33["graph"], first_then_zero, 11)}
    path = [U, "s:5", "s:6"]
    graph = t332["graph"]
    preserve(graph, p33, list(zip(path, path[1:])))
    pre = {v: x + 2 * (x >= 8) for v, x in first_then_zero.items()}
    pending = [e for e in graph["edges"] if not all(v in pre for v in e)]
    need(pending == [path[:2], path[1:]], "actual pending suffix")
    report = verify_partial(graph, pre)
    need(report["valid"] and report["graph_digest"] == t332["graph_digest"] and report["frontier"] == [U]
         and report["unused_labels"] == [8, 9] and report["unused_differences"] == [1, 2]
         and pre[U] == 11, "original nonadjacent port and inventories")
    labels = pre | {"s:5": 9, "s:6": 8}
    complete = certify(t332, labels, refs["t332"])
    complete.update({"shifted_prefix": pre, "partial_checker": report, "R": [8, 9], "D": [1, 2],
                     "port": [U, 11], "path": path, "pending": pending, "suffix_weights": [2, 1]})
    save("certificates.json", {"seed": seed, "p32": first_cert, "p33": both_cert, "t332": complete,
                               "routes": {"first_intermediate": first_step, "zero_intermediate": zero_step,
                                          "first_then_zero": first_then_zero, "zero_then_first": zero_then_first}})
    cpu = process_time() - START
    need(cpu < 30, "producer CPU cap")
    save("result.json", {"status": "ANALYTIC_SEED_VERIFIED", "a": A, "c": C,
                         "new_originals": list(CASES), "retained_controls": 2, "seed_on_retained_original": 1,
                         "adverse_rejections": 2, "search_invocations": 0, "assignment_nodes": 0,
                         "prefilter_pairs": 49, "prefilter_admitted": 34, "process_cpu_seconds": cpu})
    print("PASS: explicit seed, geometric scope, both routes, and original K=2 completion")


if __name__ == "__main__":
    main()
