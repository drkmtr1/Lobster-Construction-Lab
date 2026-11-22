"""Independent named-topology, cut-spectrum, and resource arithmetic."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "2d9eb76ea59155a0cfb68b7441dd778467bf475c"
PROOF = "research/B4_JOINT_22_CUT_COMPAT.md"


def check(condition, detail):
    if not condition:
        raise ValueError(detail)


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def reconstruct(original, q, t):
    graph = original["graph"]
    spine = [f"s:{i}" for i in range(6)]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    counts = (q, 2, t, 2)
    profile = [[size] if size is not None else [] for size in counts] + [[], []]
    for i, size in enumerate(counts):
        if size is None:
            continue
        b = f"b:{i}:0"
        roles[b] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((b, spine[i]))
        for j in range(size):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((b, leaf))
    canonical = [tuple(sorted(e)) for e in edges]
    check(Counter(graph["vertices"]) == Counter(roles.keys())
          and Counter(tuple(sorted(e)) for e in graph["edges"]) == Counter(canonical),
          "named vertices and physical incidence multiplicities")
    check(graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
          and graph["schema_version"] == 1 and len(edges) + 1 == len(roles), "named profile and roles")
    body = {"vertices": sorted(roles), "edges": sorted(canonical), "roles": roles, "profile": profile, "spine": spine}
    raw = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    check(sha256(raw).hexdigest() == original["graph_digest"], "original digest")
    return graph["edges"]


def check_ledger(original, edges, cert, errors):
    labels = cert["labels"]
    m = len(edges)
    check(set(labels) == set(original["graph"]["vertices"]) and all(type(x) is int for x in labels.values())
          and sorted(labels.values()) == list(range(m + 1)), "complete label bijection")
    weights = [abs(labels[u] - labels[v]) for u, v in edges]
    rows = [{"edge": edge, "difference": w} for edge, w in zip(edges, weights)]
    expected_digest = original["graph_digest"]
    result = cert["checker"]
    check(rows == cert["ledger"] and cert["witness"] == original["graph"]["spine"]
          and cert["graph_digest"] == result["graph_digest"] == expected_digest
          and result["edge_differences"] == weights and result["errors"] == errors
          and result["valid"] is (not errors) and result["n"] == m + 1 and result["m"] == m, "unchanged checker receipt")
    if not errors:
        check(sorted(weights) == list(range(1, m + 1)), "complete actual-edge differences")
    return rows


def cut_table(labels, rows, hosts, counts, limit):
    """Accumulate each named edge over exactly the integer cuts it crosses."""
    m = len(rows)
    contributions = [[] for _ in range(m + 2)]
    for row in rows:
        u, v = row["edge"]
        low, high = sorted((labels[u], labels[v]))
        for c in range(low + 1, high + 1):
            contributions[c].append(row)
    result = {}
    for host in hosts:
        table = []
        b = labels[host]
        for c, edges in enumerate(contributions):
            counts["thresholds"] += 1
            check(counts["thresholds"] <= limit, "threshold cap")
            d0 = max(c-b, b-c+1)
            crossing = sorted(row["difference"] for row in edges)
            required = list(range(d0, m + 1))
            table.append({"c": c, "host_label": b, "host_side": "below" if b < c else "at_or_above",
                          "first_new_weight": d0, "crossing_edges": edges, "crossing_spectrum": crossing,
                          "required_spectrum": required, "matches": crossing == required,
                          "missing": sorted(set(required) - set(crossing)), "excess": sorted(set(crossing) - set(required))})
        result[host] = table
    return result


def check_identity(config, ident):
    check(config["parent"] == ident["parent"] == PARENT and ident["id"] == config["id"]
          and ident["runtime"] == {"version": sys.version, "platform": platform.platform(), "utf8_mode": 1,
                                   "implementation": sys.implementation.name, "optional_dependencies": []}, "runtime identity")
    inputs = {(HERE / name).relative_to(ROOT).as_posix() for name in ("config.json", "validate.py", "audit.py", "commands.json")}
    check(ident["inputs_sha256"] == {name: digest(ROOT / name) for name in (inputs | {PROOF})}, "source input hashes")
    check(set(ident["retained_sha256"]) == {config["original"], *config["controls"].values()}
          and set(ident["source_sha256"]) == {"lcl/__init__.py", "lcl/model.py", "lcl/verify.py",
                                               "pyproject.toml", "requirements.txt"}, "retained and source inventories")
    for name, expected in ident["retained_sha256"].items():
        path = ROOT / name
        base = subprocess.check_output(["git", "show", f"{PARENT}:{name}"], cwd=ROOT)
        check(path.read_bytes() == base and digest(path) == expected, name)
    for name, expected in ident["source_sha256"].items():
        snapshot = DATA / "source" / name
        base = subprocess.check_output(["git", "show", f"{PARENT}:{name}"], cwd=ROOT)
        check(digest(snapshot) == digest(ROOT / name) == expected
              and snapshot.read_bytes().replace(b"\r\n", b"\n") == base.replace(b"\r\n", b"\n"), name)


def audit_cases(config, base):
    cores = {}
    evidence = {}
    checked_cases = [(case["q"], case["t"], case["order"]) for case in config["cases"]]
    check(checked_cases == [(3,None,16),(4,None,17),(3,1,18),(4,2,20)], "exact four graph cases")
    for q, t, n in checked_cases:
        name = f"q{q}" if t is None else f"q{q}-t{t}"
        record = read(DATA / (name + "-original.json"))
        edges = reconstruct(record, q, t)
        cert = read(DATA / (name + ".json"))
        rows = check_ledger(record, edges, cert, [])
        labels = cert["labels"]
        check(n == len(labels), "case order")
        if t is None:
            shifted = {"s:0", "s:2", "l:0:0:0", "l:0:0:1"}
            check(all(labels[v] == b + ((q-2) if v in shifted else 0) for v, b in base.items())
                  and {v: labels[v] for v in labels.keys() - base.keys()} ==
                      {f"l:0:0:{j}": 9+j for j in range(2, q)}
                  and labels["s:2"] == q+12 and labels["s:3"] == 0, "named first-growth formula")
            cores[q] = (labels, rows)
        else:
            older = cores[q][0]
            check(all(labels[v] == b+1 for v, b in older.items())
                  and {v: labels[v] for v in labels.keys() - older.keys()} ==
                    {"b:2:0": 0, **{f"l:2:0:{j}": q+14+j for j in range(t)}}, "exact restored third branch")
            pending = [row["edge"] for row in rows if "s:5" in row["edge"]]
            f = {v: x for v, x in labels.items() if v != "s:5"}
            ds = sorted(row["difference"] for row in rows if "s:5" not in row["edge"])
            r = sorted(set(range(n)).difference(f.values()))
            d = sorted(set(range(1, n)).difference(ds))
            check(r == [6] and d == [2] and labels["s:5"] == 6 and f["s:4"] == 8
                  and pending == [["s:4", "s:5"]] and cert["interface"] ==
                     {"prefix": f, "used_labels": sorted(f.values()), "used_differences": ds,
                      "R": r, "D": d, "port": ["s:4", 8], "pending": pending}, "physical final edge resources")
        evidence[name] = {"order": n, "graph_digest": record["graph_digest"]}
    batch = read(DATA / "batch.json")
    check(batch == {"case_q3_one": cores[3][0], "case_q4_one_batch": cores[4][0],
                    "case_q4_two_batches": cores[4][0], "updated_cuts": [11, 12, 13]}, "batch receipts")
    return cores, evidence


def main():
    started = process_time()
    config = read(HERE / "config.json")
    limits = config["limits"]
    check(limits == {"workers": 1, "max_threshold_evaluations": 64, "max_new_named_graphs": 4,
                     "max_cpu_seconds": 30, "max_record_bytes": 2_000_000, "max_total_bytes": 10_000_000,
                     "solver_queries": 0, "labeling_enumeration_nodes": 0}, "frozen scope")
    summary = read(DATA / "summary.json")
    prior_cpu = summary["cpu_seconds"]
    check(summary == {"status": "PASS", "new_graphs": 4, "retained_graphs": 1, "control_certificates": 2,
                      "threshold_evaluations": 0, "solver_queries": 0, "labeling_enumeration_nodes": 0,
                      "cpu_seconds": prior_cpu} and 0 <= prior_cpu <= limits["max_cpu_seconds"], "run scope")
    check_identity(config, read(DATA / "identity.json"))

    original = read(ROOT / config["original"])
    edges = reconstruct(original, 2, None)
    controls = read(DATA / "controls.json")
    check(set(config["controls"]) == set(controls) == {"A", "B"}, "shared physical original for two ledgers")
    for case in ("A", "B"):
        control = controls[case]
        saved = read(ROOT / config["controls"][case])
        errors = ["edge differences repeat", "edge differences are not exactly 1..m"] if case == "A" else []
        rows = check_ledger(original, edges, control, errors)
        check(all(control[key] == saved[key] for key in ("labels", "ledger", "checker", "graph_digest"))
              and control["labels"]["s:2"] == 14, "retained certificate binding")
        if case == "A":
            weights = Counter(row["difference"] for row in rows)
            check(weights[2] == 2 and set(range(1, 15)) - weights.keys() == {6}
                  and control["labels"]["s:1"] == 0, "retained negative")
    base = controls["B"]["labels"]
    check(base["s:3"] == 0, "actual zero")
    adverse = read(DATA / "adverse.json")
    check(adverse["expected_digest"] == "0"*64 != original["graph_digest"] and
          adverse["checker"] == {**controls["B"]["checker"], "valid": False,
                                 "errors": ["original graph digest mismatch"]}, "adverse digest")
    cores, evidence = audit_cases(config, base)
    counter = {"thresholds": 0}
    cut_limit = limits["max_threshold_evaluations"]
    old = cut_table(base, controls["B"]["ledger"], ["b:0:0", "b:1:0"], counter, cut_limit)
    new = cut_table(cores[3][0], cores[3][1], ["b:1:0"], counter, cut_limit)
    check(counter["thresholds"] == 49 and [row["c"] for row in old["b:0:0"] if row["matches"]] == [11, 12, 13]
          and not any(row["matches"] for row in old["b:1:0"] + new["b:1:0"]), "exact threshold dispositions")
    cut11 = old["b:0:0"][11]
    check(cut11["crossing_spectrum"] == list(range(9, 15)) and cut11["host_side"] == "below", "complete first growth premise")
    artifacts = {p.relative_to(DATA).as_posix(): digest(p) for p in sorted(DATA.rglob("*")) if p.is_file()}
    sizes = [(DATA / name).stat().st_size for name in artifacts]
    cpu = prior_cpu + process_time() - started
    check(cpu <= limits["max_cpu_seconds"], "combined process-CPU cap")
    report = {"status": "PASS", "threshold_evaluations": counter["thresholds"], "core_q2_cuts": old, "core_q3_cuts": new,
              "new_graphs": evidence, "retained_graphs": 1, "control_certificates": 2, "adverse_tests": 1,
              "first_cut_matches": [11, 12, 13], "second_cut_matches_q2": [], "second_cut_matches_q3": [],
              "cpu_seconds_total": cpu, "solver_queries": 0, "labeling_enumeration_nodes": 0, "audited_sha256": artifacts}
    raw = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    check(max([len(raw), *sizes]) <= limits["max_record_bytes"]
          and len(raw) + sum(sizes) <= limits["max_total_bytes"], "per-result and total output byte caps")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print(f"PASS: 49 host/threshold rows, four new originals, second-host failures on q2 and q3 ({cpu:.6f} total CPU seconds)")


if __name__ == "__main__":
    main()
