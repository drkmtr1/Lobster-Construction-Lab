"""One bounded D080 run on the declared originals."""

from time import process_time

START = process_time()

from hashlib import sha256
from itertools import permutations, product
import json
from math import factorial
from pathlib import Path
import subprocess
import sys

from lcl.consumers import _nonadjacent_path_labels
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads((HERE / path).read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def write(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    existing = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
    need(len(raw) <= 2_000_000 and existing + len(raw) <= 8_000_000, "evidence byte cap")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)


def identity(config):
    local = [f"{HERE.relative_to(ROOT).as_posix()}/{f}" for f in
             ("INTAKE.md", "config.json", "commands.json", "run.py", "audit.py", "driver.py")]
    paths = config["sources"] + list(config["retained"].values()) + local
    sources = {p: raw_hash(ROOT / p) for p in sorted(paths)}
    packet = config["authorization"]
    need(sources[packet["path"]] == packet["sha256"], "task byte identity")
    return {"parent": config["parent"], "sources": sources,
            "runtime": {"version": sys.version, "path": Path(sys.executable).relative_to(ROOT).as_posix(),
                        "sha256": raw_hash(Path(sys.executable))}}


def edge_rows(graph, labels):
    return [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]
            if u in labels and v in labels]


def ledger_id(digest, labels):
    raw = {"graph_digest": digest, "labels": sorted(labels.items())}
    return sha256(json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def certificate(original, labels):
    digest = original["graph_digest"]
    checker = verify_certificate(original["graph"], labels, digest)
    need(checker["valid"] and checker["graph_digest"] == digest, str(checker["errors"]))
    return {"graph_digest": digest, "ledger_id": ledger_id(digest, labels), "labels": labels,
            "edge_rows": edge_rows(original["graph"], labels), "checker": checker}


def normal(graph, labels, p, spine):
    rows = edge_rows(graph, labels)
    n = len(labels)
    need(all(type(x) is int for x in labels.values()), "exact labels")
    need(sorted(labels.values()) == list(range(n)), "normalized label alphabet")
    need(sorted(w for _, _, w in rows) == list(range(1, n)), "normalized difference alphabet")
    need(all((labels[u] < p) != (labels[v] < p) for u, v, _ in rows), "alpha cut")
    s, t = spine[0], spine[-1]
    x, y = labels[s], labels[t]-p
    need(0 <= x < p and 0 <= y < n-p, "actual port classes")
    return {"labels": labels, "N": n, "P": p, "low": sorted(v for v in labels if labels[v] < p),
            "high": sorted(v for v in labels if labels[v] >= p), "edge_rows": rows,
            "witness": spine, "ports": [s, t], "port_labels": [labels[s], labels[t]], "offsets": [x, y]}


def bridge_labels(a, i):
    need(type(a) is int and a >= 1, "positive exact a")
    labels = {f"s:{i}": 0, f"s:{i+1}": a+3, f"b:{i}:0": 2*a+4, f"b:{i+1}:0": a+1,
              f"l:{i+1}:0:0": a+2}
    labels.update({f"l:{i}:0:{j}": j+1 for j in range(a)})
    labels.update({f"l:{i+1}:0:{j}": a+3+j for j in range(1, a+1)})
    return labels


def embed(labels, start):
    moved = {}
    for v, value in labels.items():
        fields = v.split(":")
        fields[1] = str(int(fields[1])+start)
        moved[":".join(fields)] = value
    return moved


def join(graph, B, A):
    old, new = B["labels"], A["labels"]
    p, n = B["P"], A["N"]
    u, v = B["ports"][1], A["ports"][0]
    y, x = old[u]-p, new[v]
    need(y == x, "R241 physical offset mismatch")
    need(not (old.keys() & new.keys()), "R241 original blocks must be disjoint")
    crossings = [[s, t] for s, t in graph["edges"]
                 if (s in old and t in new) or (t in old and s in new)]
    need(crossings == [[u, v]], "exact original connector")
    shifted = {s: f + (n if f >= p else 0) for s, f in old.items()}
    shifted.update({s: f+p for s, f in new.items()})
    combined = normal(graph, shifted, p+A["P"], B["witness"] + A["witness"])
    detail = {"connector": [u, v], "old_block_order": B["N"], "new_block_order": n,
              "old_low_size": p, "new_low_size": A["P"], "old_exit_offset": y,
              "new_entrance_offset": x, "old_exit_before": old[u], "new_entrance_before": new[v],
              "old_exit_after": shifted[u], "new_entrance_after": shifted[v],
              "connector_weight": shifted[u]-shifted[v]}
    need(detail["connector_weight"] == n, "connector weight")
    return combined, detail


def macro(graph, a, start, retained_labels):
    spine = graph["spine"]
    B = normal(graph, embed(retained_labels, start), 4, spine[start:start+2])
    A = normal(graph, bridge_labels(a, start+2), a+2, spine[start+2:start+4])
    Q, receipt = join(graph, B, A)
    need(Q["offsets"] == [1, 1], "macro closure")
    return {"B": B, "H": A, "Q": Q, "join": receipt}


def suffix_contract(original, normalized, L, declared_d):
    graph = original["graph"]
    p = normalized["P"]
    path = graph["spine"][len(normalized["witness"])-1:]
    labels = {v: f + (L if f >= p else 0) for v, f in normalized["labels"].items()}
    pending = [edge for edge in graph["edges"] if any(v not in labels for v in edge)]
    need(len(path) == L+1 and set(graph["vertices"]) - labels.keys() == set(path[1:]),
         "exact unfinished vertices")
    need(pending == [list(e) for e in zip(path, path[1:])], "exact unfinished edge path")
    checked = verify_partial(graph, labels)
    port = [path[0], labels[path[0]]]
    need(checked["valid"] and checked["graph_digest"] == original["graph_digest"]
         and checked["frontier"] == [path[0]] and port[1] == p+L+1, "actual suffix port")
    need(checked["unused_labels"] == list(range(p, p+L)), "wrong suffix labels")
    need(checked["unused_differences"] == declared_d == list(range(1, L+1)),
         "wrong suffix difference inventory")
    sequence = _nonadjacent_path_labels(L, p)
    need(sequence[0] == port[1] and len(sequence) == len(path), "numerical recurrence contract")
    final = labels | dict(zip(path[1:], sequence[1:], strict=True))
    return final, {"assigned": labels, "partial_checker": checked, "path": path, "port": port,
                   "pending_edges": pending, "crossing": [path[:2]], "sequence": sequence}


def build_target(original, quotas, L, B):
    graph = original["graph"]
    macros = [macro(graph, a, 4*i, B) for i, a in enumerate(quotas)]
    aggregate = macros[0]["Q"]
    assemblies = [{"normalized": aggregate, "join": None}]
    for block in macros[1:]:
        aggregate, receipt = join(graph, aggregate, block["Q"])
        assemblies.append({"normalized": aggregate, "join": receipt})
    if L:
        labels, suffix = suffix_contract(original, aggregate, L, list(range(1, L+1)))
    else:
        labels, suffix = aggregate["labels"], None
    return certificate(original, labels) | {"macros": macros, "assemblies": assemblies, "suffix": suffix}


def try_reject(operation, expected, *args):
    try:
        operation(*args)
    except ValueError as exc:
        need(str(exc) == expected, "unexpected adverse rejection")
        return {"valid": False, "reason": str(exc)}
    raise ValueError("adverse input was accepted")


def exact_pinned_rows(case, original, total):
    name, expected, _ = case
    graph = original["graph"]
    a, b = (q[0] for q in graph["profile"])
    p = a+2
    pins = {"s:0": 0, "s:1": p+1}
    free = [["b:1:0"]+[f"l:0:0:{j}" for j in range(a)],
            ["b:0:0"]+[f"l:1:0:{j}" for j in range(b)]]
    bands = [list(range(1, p)), [x for x in range(p, len(graph["vertices"])) if x != p+1]]
    need(factorial(len(bands[0])) * factorial(len(bands[1])) == expected, "declared product size")
    rows, positives = [], 0
    status = "INCOMPLETE"
    try:
        for lo, hi in product(permutations(bands[0]), permutations(bands[1])):
            need(total + len(rows) < 160 and process_time()-START < 25, "diagnostic cap")
            labels = pins | dict(zip(free[0], lo, strict=True)) | dict(zip(free[1], hi, strict=True))
            weights = [w for _, _, w in edge_rows(graph, labels)]
            repeated = None
            seen = {}
            for edge_index, w in enumerate(weights):
                if w in seen:
                    repeated = [seen[w], edge_index, w]
                    break
                seen[w] = edge_index
            rows.append([lo, hi, repeated])
            positives += int(repeated is None)
        need(len(rows) == expected, "diagnostic incomplete")
        status = "COMPLETE"
    finally:
        write(f"{name}_enumeration.json", {"graph_digest": original["graph_digest"], "pins": pins,
             "free_names": free, "free_labels": bands, "status": status,
             "visits": len(rows), "positive": positives, "rows": rows})
    return len(rows), positives


def main():
    config = read("config.json")
    need(Path.cwd() == ROOT and sys.version_info[:2] in ((3, 12), (3, 13)), "project Python")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    need(head == config["parent"], "expected strategy parent")
    write("identity.json", identity(config))
    originals = {}
    for key, profile in config["profiles"].items():
        need(len(originals) < 6, "new original ceiling")
        graph = build_graph(profile)
        name = f"{key}_original.json"
        write(name, {"graph": graph, "graph_digest": graph_digest(graph)})
        originals[key] = read(name)
    retained = config["retained"]
    archive = json.loads((ROOT / retained["original"]).read_bytes())
    archived_certificate = json.loads((ROOT / retained["certificate"]).read_bytes())["positive_controls"]["small"]
    manifest = json.loads((ROOT / retained["manifest"]).read_bytes())
    saved = {row["path"]: row["sha256"] for row in manifest["files"]}
    for key in ("original", "certificate"):
        path = ROOT / retained[key]
        need(raw_hash(path) == saved[path.name], "D079 raw binding")
    B = archived_certificate["labels"]
    control = certificate(archive, B)
    for field in ("graph_digest", "ledger_id", "checker", "edge_rows"):
        need(control[field] == archived_certificate[field], "D079 retained ledger binding")
    controls = {"retained_B": control | {"normalized": normal(archive["graph"], B, 4, ["s:0", "s:1"])}}
    equal = {"s:0": 0, "s:1": 3, "b:0:0": 5, "l:0:0:0": 1, "b:1:0": 2, "l:1:0:0": 4}
    for key, labels, p in (("equal", equal, 3), ("h1", bridge_labels(1, 0), 3),
                           ("h2", bridge_labels(2, 0), 4)):
        original = originals[key]
        part = normal(original["graph"], labels, p, ["s:0", "s:1"])
        controls[key] = certificate(original, labels) | {"normalized": part}
    for key, quotas, L in config["macro_cases"]:
        controls[key] = build_target(originals[key], quotas, L, B)
    counts = {}
    total = 0
    for case in config["enumerations"]:
        visits, positive = exact_pinned_rows(case, originals[case[0]], total)
        counts[case[0]] = [positive, visits]
        total += visits

    wrong = verify_certificate(archive["graph"], B, "0"*64)
    need(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "wrong digest")
    original = originals["q1_l2"]
    saved_q = controls["q1_l2"]["assemblies"][-1]["normalized"]
    bad_suffix = try_reject(suffix_contract, "wrong suffix difference inventory", original, saved_q, 2, [2])
    # On the retained Q(1) incidences, corrupt only the incoming premise.
    local = controls["q1"]["macros"][0]
    u, v, leaf = "s:1", "s:2", "l:2:0:0"
    old, new = local["B"], local["H"]
    after = new["labels"] | {v: new["labels"][leaf], leaf: new["labels"][v]}
    mismatch = try_reject(join, "R241 physical offset mismatch", originals["q1"]["graph"],
                          old, new | {"labels": after})
    mismatch.update({"y_B": old["offsets"][1], "x_A": after[v], "ports": [u, v],
                     "swapped_low_names": [v, leaf], "graph_digest": originals["q1"]["graph_digest"]})
    write("certificates.json", {"certificates": controls, "adverse": {
        "wrong_digest": {"expected": "0"*64, "checker": wrong}, "offset": mismatch,
        "suffix": bad_suffix | {"declared_d": [2], "actual_d": [1, 2]}}})
    digests = {g["graph_digest"] for g in originals.values()} | {archive["graph_digest"]}
    need(len(digests) == 7 and total == 160, "distinct original and exact visit accounting")
    write("result.json", {"status": "COMPLETE", "new_originals": 6, "retained_originals": 1,
                          "certificates": 7, "adverse": 3, "diagnostic_visits": total, "counts": counts,
                          "solver_calls": 0, "replays": 0, "process_cpu_seconds": process_time()-START})


if __name__ == "__main__":
    main()
