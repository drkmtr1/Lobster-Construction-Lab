"""D081 exact named products, direct formulas, and original-bound checking."""

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
    paths = config["sources"] + list(config["intake_inputs"]) + local
    sources = {p: raw_hash(ROOT / p) for p in sorted(paths)}
    need(all(sources[p] == value for p, value in config["intake_inputs"].items()), "intake bytes")
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
    need(process_time()-START < 25, "producer CPU reserve")
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


def first_pair_labels(b, i):
    need(type(b) is int and b >= 0, "nonnegative exact b")
    labels = {f"s:{i}": 1, f"s:{i+1}": b+3, f"b:{i}:0": 2*b+5, f"l:{i}:0:0": 0,
              f"b:{i}:1": 2*b+4, f"b:{i+1}:0": b+2}
    labels.update({f"l:{i}:1:{j}": 2+j for j in range(b)})
    labels.update({f"l:{i+1}:0:{j}": b+4+j for j in range(b)})
    return labels


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


def macro(graph, b, a, start):
    spine = graph["spine"]
    B = normal(graph, first_pair_labels(b, start), b+3, spine[start:start+2])
    A = normal(graph, bridge_labels(a, start+2), a+2, spine[start+2:start+4])
    R, receipt = join(graph, B, A)
    need(R["offsets"] == [1, 1], "macro closure")
    return {"F": B, "H": A, "R": R, "join": receipt}


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


def build_target(original, quotas, L):
    graph = original["graph"]
    macros = [macro(graph, b, a, 4*i) for i, (b, a) in enumerate(quotas)]
    aggregate = macros[0]["R"]
    assemblies = [{"normalized": aggregate, "join": None}]
    for block in macros[1:]:
        aggregate, receipt = join(graph, aggregate, block["R"])
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


def exact_pinned_rows(case, original, total, limits):
    key, graph_id, x, expected, expected_hits = case
    graph = original["graph"]
    p = 5
    pins = {"s:0": x, "s:1": p}
    free = [["b:1:0", "l:0:0:0", "l:0:1:0", "l:0:1:1"],
            ["b:0:0", "b:0:1"]+[f"l:1:0:{j}" for j in range(graph["profile"][1][0])]]
    bands = [[value for value in range(p) if value != x], list(range(p+1, len(graph["vertices"])))]
    need(factorial(len(bands[0])) * factorial(len(bands[1])) == expected, "declared product size")
    rows, positive = [], []
    status = "INCOMPLETE"
    try:
        for lo, hi in product(permutations(bands[0]), permutations(bands[1])):
            rank = len(rows)
            need(total + rank < limits["assignment_cap"] and total + rank < limits["scheduled_visits"],
                 "diagnostic visit cap")
            need(process_time()-START < 25, "diagnostic CPU reserve")
            labels = pins | dict(zip(free[0], lo, strict=True)) | dict(zip(free[1], hi, strict=True))
            repeated = None
            seen = {}
            for edge_index, (_, _, w) in enumerate(edge_rows(graph, labels)):
                if w in seen:
                    repeated = [seen[w], edge_index, w]
                    break
                seen[w] = edge_index
            rows.append([rank, lo, hi, repeated])
            if repeated is None:
                positive.append({"rank": rank, "certificate": certificate(original, labels)})
        need(len(rows) == expected, "diagnostic incomplete")
        status = "COMPLETE"
    finally:
        write(f"{key}_enumeration.json", {"graph_id": graph_id, "graph_digest": original["graph_digest"],
             "pins": pins, "free_names": free, "free_labels": bands, "status": status,
             "visits": len(rows), "positive": positive, "rows": rows})
    need(len(positive) == expected_hits, f"preserved discrepant results in {key}")
    return len(rows), len(positive)


def main():
    config = read("config.json")
    need(Path.cwd() == ROOT and sys.version_info[:2] in ((3, 12), (3, 13)), "project Python")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    need(head == config["parent"], "expected parent")
    write("identity.json", identity(config))
    originals = {}
    for key, profile in config["profiles"].items():
        need(len(originals) < config["limits"]["new_original_cap"], "new original ceiling")
        graph = build_graph(profile)
        name = f"{key}_original.json"
        write(name, {"graph": graph, "graph_digest": graph_digest(graph)})
        originals[key] = read(name)
    retained = config["retained"]
    archive = read(ROOT / retained["original"])
    archived = read(ROOT / retained["certificate"])["positive_controls"]["small"]
    saved = {row["path"]: row["sha256"] for row in read(ROOT / retained["manifest"])["files"]}
    for key in ("original", "certificate"):
        path = ROOT / retained[key]
        need(raw_hash(path) == saved[path.name], "D079 raw binding")
    need(archive["graph"]["profile"] == [[1, 1], [1]], "F(1) original identity")
    f1 = certificate(archive, first_pair_labels(1, 0))
    for field in ("labels", "graph_digest", "ledger_id", "checker", "edge_rows"):
        need(f1[field] == archived[field], "F(1) exact archived ledger")
    originals["f1_retained"] = archive

    counts = {}
    total = 0
    for case in config["enumerations"]:
        visits, hits = exact_pinned_rows(case, originals[case[1]], total, config["limits"])
        counts[case[0]] = [hits, visits]
        total += visits
    retained_case = f1 | {"normalized": normal(archive["graph"], f1["labels"], 4, ["s:0","s:1"])}
    controls = {"f1_retained": retained_case}
    alternate = {"s:0": 2, "s:1": 5, "b:0:0": 7, "l:0:0:0": 3, "b:0:1": 8,
                 "l:0:1:0": 0, "l:0:1:1": 1, "b:1:0": 4, "l:1:0:0": 6}
    graph = originals["unequal"]["graph"]
    controls["unequal"] = certificate(originals["unequal"], alternate) | {
        "normalized": normal(graph, alternate, 5, ["s:0","s:1"])}
    for b in (0, 2, 4):
        key = f"f{b}"
        original = originals[key]
        labels = first_pair_labels(b, 0)
        controls[key] = certificate(original, labels) | {
            "normalized": normal(original["graph"], labels, b+3, ["s:0","s:1"])}
    for key, quotas, L in config["macro_cases"]:
        controls[key] = build_target(originals[key], quotas, L)

    good = controls["f2"]
    wrong = verify_certificate(originals["f2"]["graph"], good["labels"], "0"*64)
    need(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "wrong digest")
    macro_state = controls["r21"]["macros"][0]
    original = originals["r21"]
    old, new = macro_state["F"], macro_state["H"]
    v, leaf = "s:2", "l:2:0:0"
    after = new["labels"] | {v: new["labels"][leaf], leaf: new["labels"][v]}
    bad_offset = try_reject(join, "R241 physical offset mismatch", original["graph"],
                            old, new | {"labels": after})
    bad_offset.update({"y_B": old["offsets"][1], "x_A": after[v], "ports": ["s:1", v],
                       "swapped_low_names": [v, leaf], "graph_digest": original["graph_digest"]})
    repeated_original = originals["repeat_l5"]
    normalized = controls["repeat_l5"]["assemblies"][-1]["normalized"]
    faulty_d = [2, 3, 4, 5]
    bad_suffix = try_reject(suffix_contract, "wrong suffix difference inventory",
                            repeated_original, normalized, 5, faulty_d)
    bad_suffix.update({"declared_d": faulty_d, "actual_d": [1, 2, 3, 4, 5],
                       "graph_digest": repeated_original["graph_digest"]})
    write("certificates.json", {"controls": controls, "adverse": {
        "wrong_digest": {"expected": "0"*64, "graph_id": "f2", "checker": wrong},
        "offset": bad_offset, "suffix": bad_suffix}})
    need(len({o["graph_digest"] for o in originals.values()}) == 8, "distinct originals")
    need(total == config["limits"]["scheduled_visits"], "complete diagnostic schedule")
    write("result.json", {"status": "COMPLETE", "new_originals": 7, "retained_originals": 1,
                          "control_certificates": 8, "diagnostic_positive_certificates": sum(v[0] for v in counts.values()),
                          "adverse": 3, "diagnostic_visits": total, "counts": counts, "solver_calls": 0,
                          "replays": 0, "process_cpu_seconds": process_time()-START})


if __name__ == "__main__":
    main()
