"""Reconstruct the named original and audit arithmetic premises without a solver."""
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
A, B, Z, U, F = "b:0:0", "b:1:0", "b:2:0", "s:4", "b:3:0"
SPINE_LOWS = {"s:1", "s:3"}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return sha256(raw).hexdigest()


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def edge_key(edge):
    return tuple(sorted(edge))


def topology(original):
    spine = [f"s:{i}" for i in range(5)]
    parents = dict(zip(spine[1:], spine[:-1], strict=True))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i in range(4):
        center = f"b:{i}:0"
        parents[center] = spine[i]
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(2):
            v = f"l:{i}:0:{j}"
            parents[v] = center
            roles[v] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    counts = Counter(map(edge_key, parents.items()))
    norm = {"vertices": sorted(roles), "edges": sorted(counts.elements()), "roles": roles,
            "spine": spine, "profile": [[2], [2], [2], [2], []]}
    graph = original["graph"]
    need(Counter(graph["vertices"]) == Counter(roles.keys())
         and Counter(map(edge_key, graph["edges"])) == counts and len(counts) == 16,
         "original named incidences and multiplicities")
    need(type(graph["schema_version"]) is int and graph["schema_version"] == 1
         and all(graph[k] == norm[k] for k in ("roles", "spine", "profile"))
         and canonical(norm) == original["graph_digest"], "canonical named original identity")
    adj = {v: set() for v in roles}
    for u, v in counts:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def levels(adj, starts):
    found = dict.fromkeys(starts, 0)
    queue = deque(starts)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in found:
                found[v] = found[u] + 1
                queue.append(v)
    return found


def check_structure(adj):
    low = {v for v, d in levels(adj, [U]).items() if d % 2}
    high = adj.keys() - low
    need({v for v in low if len(adj[v]) == 3} == {A, Z, *SPINE_LOWS}
         and Counter(len(adj[v]) for v in low) == Counter({1: 4, 3: 4}), "low degree structure")
    excess = {v: len(adj[v]) - 1 for v in high}
    need(Counter(excess.values()) == Counter({0: 5, 1: 1, 2: 3})
         and {v for v, e in excess.items() if e == 1} == {"s:0"}
         and {v for v, e in excess.items() if e == 2} == {"s:2", B, F}, "high degree structure")
    first, third = ({f"l:{i}:0:{j}" for j in range(2)} for i in (0, 2))
    need(adj[A] == first | {"s:0"} and adj[Z] == third | {"s:2"}
         and len(adj[A] | adj[Z]) == 6 and all(adj[v] == {Z} for v in third), "descending weight and six-high premises")
    need(adj["s:2"] == SPINE_LOWS | {Z} and adj["s:0"] == {A, "s:1"}
         and adj[B] == {"s:1", "l:1:0:0", "l:1:0:1"}
         and adj[F] == {"s:3", "l:3:0:0", "l:3:0:1"} and adj[U] == {"s:3"},
         "residual named neighbors")
    need(all(adj[v] <= high for v in low) and all(adj[v] <= low for v in high), "unique alpha endpoint")
    witness = [A, *(f"s:{i}" for i in range(5))]
    distance = levels(adj, witness)
    need(all(v in adj[u] for u, v in zip(witness, witness[1:])) and distance.keys() == adj.keys()
         and max(distance.values()) == 2 and distance[A] == 0 and distance[B] == distance[Z] == 1,
         "original witness and exact host distances")
    need(sum(range(1, 17)) - (sum(range(8, 17)) - sum(range(8))) == 56, "excess weighted-degree equation")
    return {"low": sorted(low), "high": sorted(high), "low_degrees": {v: len(adj[v]) for v in low},
            "high_excess": excess, "witness": witness, "distances": distance}


def check_certificate(original, cert, state):
    labels = cert["labels"]
    rows = [{"edge": e, "difference": abs(labels[e[0]] - labels[e[1]])} for e in original["graph"]["edges"]]
    weights = [r["difference"] for r in rows]
    gid = original["graph_digest"]
    lid = canonical({"graph_digest": gid, "labels": sorted(labels.items())})
    need(set(labels) == set(state["low"] + state["high"]) and all(type(x) is int for x in labels.values())
         and Counter(labels[v] for v in state["low"]) == Counter(range(8))
         and Counter(labels[v] for v in state["high"]) == Counter(range(8, 17))
         and Counter(weights) == Counter(range(1, 17)), "complete named certificate alphabets")
    report = {"valid": True, "errors": [], "n": 17, "m": 16, "graph_digest": gid,
              "edge_differences": weights, "claim": "finite certificate for this exact named target only"}
    need(gid == cert["graph_digest"] != lid and cert["ledger_id"] == lid and rows == cert["named_edges"]
         and cert["checker"] == report, "archive certificate identity")
    return {"graph_digest": gid, "ledger_id": lid, "checker": report}


def check_d070(cert, original, cfg):
    labels = cert["labels"]
    ref = cfg["sources"]["original"]
    need(cert["original"] == {k: ref[k] for k in ("path", "bytes", "sha256")}
         and [labels[v] for v in (A, Z, U, B)] == [5, 0, 9, 13], "D070 measured physical pins")
    rows = cert["named_edges"]
    upper = sorted(row["difference"] for row in rows if max(labels[v] for v in row["edge"]) >= 10)
    need(upper == list(range(5, 17)), "D070 full upper tail")
    lower = {}
    for d in (6, 7, 8):
        selected = [r for r in rows if min(labels[v] for v in r["edge"]) < d]
        actual = sorted(r["difference"] for r in selected)
        required = list(range(14 - d, 17))
        archived = cfg["sources"][f"d071_seed_c{d}"]
        old = read(ROOT / archived["path"])
        need(old["actual"] == actual and old["required"] == required and old["crossings"] == selected
             and old["ledger_id"] == cert["ledger_id"] and old["graph_digest"] == original["graph_digest"]
             and actual != required, "retained D070 lower predicate fails")
        lower[d] = {"actual": actual, "required": required, "named_crossings": selected}
    return {"upper_at_10": upper, "lower": lower}


def support(state):
    # Pairs (selected count, excess), with the actual B membership separated.
    free = {(0, 0)}
    for v, excess in state["high_excess"].items():
        if v not in (B, U):
            free |= {(count + 1, total + excess) for count, total in free}
    plus_b = {(count + 1, total + state["high_excess"][B]) for count, total in free}
    return free, plus_b


def residual_arithmetic():
    # Only remove already named weights from the indicated complement.
    a2 = {}
    for x, t, leaf in ((10, 11, 12), (10, 12, 11), (12, 11, 10), (12, 10, 11)):
        remainder = sorted(set(range(1, 11)) - {x - 2, leaf - 2})
        a2[f"{x},{t},{leaf}"] = remainder
    need(a2 == {"10,11,12": [1, 2, 3, 4, 5, 6, 7, 9],
                "10,12,11": [1, 2, 3, 4, 5, 6, 7, 10],
                "12,11,10": [1, 2, 3, 4, 5, 6, 7, 9],
                "12,10,11": [1, 2, 3, 4, 5, 6, 7, 8]}, "a=2 local weight arithmetic")
    a3 = {}
    for t, u in ((10, 11), (10, 12), (10, 13), (11, 12), (11, 13), (12, 13)):
        remaining = set(range(1, u - 3)) - {x - 3 for x in range(10, u) if x != t}
        expect = (set(range(1, 8)) if t == 10 else set(range(1, 7)) | {t - 3})
        need(remaining == expect, "a=3 corrected residual weights")
        a3[f"{t},{u}"] = sorted(remaining)
    a4 = {u: sorted(set(range(1, u - 4)) - {x - 4 for x in range(11, u)}) for u in (11, 12, 13)}
    need(all(rest == list(range(1, 7)) for rest in a4.values())
         and set(range(1, 9)) - {6, 7, 8} == set(range(1, 6)), "a=4 residual weights")
    return {"a2_u13_after_first_edges": a2, "a3_residual": a3, "a4_X10_residual": a4}


def bookkeeping(cfg, state, previous_cpu):
    opts = cfg["domain"]
    need(opts == {"a": list(range(1, 8)), "u": list(range(10, 17)), "B": [8, *range(10, 17)],
                  "max_d": 8}, "exact unexpanded domain")
    count_support = support(state)
    rows = []
    for a, u, b in product(opts["a"], opts["u"], opts["B"]):
        for d in range(a + 1, opts["max_d"] + 1):
            need(len(rows) < 1568 and previous_cpu + process_time() - START < 30, "numeric or CPU cap")
            low_start, high_start = b - d + 1, u - a
            low_possible = b in {12 - 2 * k for k in range(max(0, d - 6), min(2, d - 2) + 1)}
            high_possible = (17 - u, a) in count_support[b >= u]
            if not low_possible:
                reason = "lower_count"
            elif not high_possible:
                reason = "upper_count"
            elif a == 5:
                reason = "D072_pinned_obstruction"
            elif a == 1:
                reason = "s2_upper_selection_excess"
            elif b == 10:
                need(high_start >= low_start, "B10 containment direction")
                reason = "B10_forces_both_spine_lows"
            elif b == 12:
                need(d <= 6, "B12 lower complement")
                reason = "B12_named_containment"
            else:
                need(b == 8 and a in (2, 3, 4), "residual case coverage")
                reason = f"B8_a{a}_residual_weights"
            rows.append({"a": a, "u": u, "d": d, "B": b, "admissible_numeric": True,
                         "lower_degree_possible": low_possible, "upper_degree_possible": high_possible,
                         "upper_start": high_start, "lower_start": low_start,
                         "joint_complete_spectra": False, "reason": reason})
    need(len(rows) == 1568, "complete numerical bookkeeping")
    return rows


def main():
    cfg = read(HERE / "config.json")
    source = cfg["sources"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    need(head == cfg["parent"] and cfg["runtime"] ==
         {"python": sys.version, "platform": sys.platform,
          "executable_sha256": sha(Path(sys.executable).read_bytes())}, "frozen runtime and parent")
    for ref in source.values():
        raw = (ROOT / ref["path"]).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], "frozen source hash")
        if "git_sha256" in ref:
            blob = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            need(blob == raw and sha(blob) == ref["git_sha256"], "archive Git blob")

    def archive(name):
        return read(ROOT / source[name]["path"])

    original = archive("original")
    state = check_structure(topology(original))
    actual = read(HERE / "controls.json")
    d66 = check_certificate(original, archive("d066_certs")["prefix"], state)
    seed = archive("d070_seed")
    d70 = check_certificate(original, seed, state)
    need(actual["retained"] == {"D066": d66, "D070": d70}
         and d66["graph_digest"] == d70["graph_digest"] and d66["ledger_id"] != d70["ledger_id"],
         "unchanged checker and distinct co-original ledgers")
    adverse = actual["wrong_digest"]
    need(adverse["expected"] == "0" * 64 != original["graph_digest"]
         and adverse["checker"] == d70["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]},
         "actual wrong digest rejection")
    old = archive("d072_audit")
    need(old["status"] == "PASS" and old["d066"] == d66 and old["d070"] == d70
         and old["reasons"] == {"lower_count": 126, "upper_count": 12, "B10_both_spine_lows": 10,
                                 "B12_eight_high_neighbors": 3, "B12_unselected_s1": 2,
                                 "B8_missing_weight_two": 9, "B8_zero_terminal": 6}, "preserved D072 audit")
    d070_cuts = check_d070(seed, original, cfg)
    local = residual_arithmetic()
    prior_cpu = cfg["setup_process_cpu_seconds"] + actual["process_cpu_seconds"]
    cases = bookkeeping(cfg, state, prior_cpu)
    cpu = prior_cpu + process_time() - START
    need(cpu < 30 and all(actual[k] == 0 for k in ("solver_calls", "assignment_nodes", "new_originals")),
         "bounded completed audit")
    report = {"status": "PASS", "state": state, "d070_cuts": d070_cuts, "local_arithmetic": local,
              "numeric_cases": cases, "numeric_counts": Counter(row["reason"] for row in cases),
              "retained_ledgers": [d66["ledger_id"], d70["ledger_id"]], "graph_digest": d70["graph_digest"],
              "solver_calls": 0, "assignment_nodes": 0, "new_originals": 0,
              "combined_process_cpu_seconds": cpu}
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000, "audit byte caps")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print("PASS: named incidences, retained controls, residual arithmetic, and 1,568 numerical rows")


if __name__ == "__main__":
    main()
