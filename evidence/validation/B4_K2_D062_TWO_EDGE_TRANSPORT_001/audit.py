"""Independent standard-library audit of the one frozen original and 38 receipts."""
from collections import Counter
from hashlib import sha256
from itertools import pairwise
import json
from pathlib import Path
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TARGET_PROFILE = [[2], [2], [2], [2], [], [], []]
K1_PROFILE = TARGET_PROFILE[:-1]
CORE_PROFILE = [[2], [2], [], [2], [], []]
CORE = {
    "s:0": 13, "s:1": 0, "s:2": 14, "s:3": 3, "s:4": 9, "s:5": 10,
    "b:0:0": 1, "l:0:0:0": 11, "l:0:0:1": 8,
    "b:1:0": 2, "l:1:0:0": 5, "l:1:0:1": 6,
    "b:3:0": 12, "l:3:0:0": 4, "l:3:0:1": 7,
}
F = {
    "s:0": 14, "s:1": 1, "s:2": 15, "s:3": 4, "s:4": 10, "s:5": 11,
    "b:0:0": 2, "l:0:0:0": 12, "l:0:0:1": 9,
    "b:1:0": 3, "l:1:0:0": 6, "l:1:0:1": 7,
    "b:2:0": 0, "l:2:0:0": 16, "l:2:0:1": 17,
    "b:3:0": 13, "l:3:0:0": 5, "l:3:0:1": 8,
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(file):
    return json.loads(file.read_bytes())


def normalize(edge):
    return tuple(sorted(edge))


def audit_original(record, profile):
    saved = record["graph"]
    spine = [f"s:{i}" for i in range(len(profile))]
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    expected = Counter(map(normalize, pairwise(spine)))
    for i, branch in enumerate(profile):
        if branch == [2]:
            center = f"b:{i}:0"
            roles[center] = {"kind": "branch", "section": i, "branch": 0}
            expected[normalize((spine[i], center))] += 1
            for j in range(2):
                terminal = f"l:{i}:0:{j}"
                roles[terminal] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
                expected[normalize((center, terminal))] += 1
    edges = [tuple(edge) for edge in saved["edges"]]
    need(saved["schema_version"] == 1 and saved["profile"] == profile
         and saved["spine"] == spine and saved["roles"] == roles
         and Counter(saved["vertices"]) == Counter(roles.keys()), "named physical field mismatch")
    need(Counter(map(normalize, edges)) == expected and len(edges) + 1 == len(roles), "edge multiplicities")
    payload = {"vertices": sorted(roles), "edges": sorted(expected.elements()),
               "roles": roles, "spine": spine, "profile": profile}
    identity = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    need(identity == record["graph_digest"], "original graph identity")
    return set(roles), edges


def differences(edges, labels):
    return [max(labels[u], labels[v]) - min(labels[u], labels[v]) for u, v in edges]


def named_rows(edges, ds):
    return [{"edge": list(edge), "difference": d} for edge, d in zip(edges, ds, strict=True)]


def check_inventory(rec, xs, lo, hi):
    expected = range(lo, hi + 1)
    counts = Counter(xs)
    need(rec == {"values": sorted(xs), "unused": [v for v in expected if counts[v] == 0],
                 "repeated": [[v, counts[v]] for v in sorted(counts) if counts[v] > 1],
                 "out_of_range": [v for v in sorted(counts) if v < lo or v > hi]}, "full multiset inventory")


def check_good_source(original, names, edges, labels, report):
    m = len(edges)
    need(set(labels) == names and all(type(x) is int for x in labels.values())
         and sorted(labels.values()) == list(range(m+1)), "source label inventory")
    ds = differences(edges, labels)
    need(sorted(ds) == list(range(1, m+1))
         and report["edge_differences"] == ds, "source difference inventory")
    need(report["valid"] is True and report["errors"] == []
         and report["graph_digest"] == original["graph_digest"]
         and (report["n"], report["m"]) == (m+1, m), "source certificate receipt")


def check_source_custody(config, freeze):
    expected = {name: sha(HERE / name) for name in ("audit.py", "commands.json", "config.json", "validate.py")}
    for ref in config["archives"].values():
        expected[ref["path"]] = sha(ROOT / ref["path"])
        need(expected[ref["path"]] == ref["sha256"], "retained source hash")
    for path, value in config["production"].items():
        expected[path] = sha(ROOT / path)
        need(expected[path] == value, "production source hash")
    need(expected == freeze["input_sha256"] and freeze["parent"] == config["parent"]
         and freeze["new_originals"] == 1 and freeze["target_sha256"] == sha(HERE / "target_original.json"),
         "frozen original, code and configuration bytes")
    nested_path = ROOT / config["archives"]["nested_manifest"]["path"]
    manifest = read(nested_path)
    entries = {entry["path"]: entry for entry in manifest["files"]}
    for key in ("nested_original", "nested_certificate", "nested_audit", "nested_sources"):
        ref = config["archives"][key]
        file = ROOT / ref["path"]
        entry = entries[file.relative_to(nested_path.parent).as_posix()]
        need(entry["sha256"] == ref["sha256"] and entry["bytes"] == file.stat().st_size, "prior D062 manifest entry")
    proof = config["archives"]["nested_proof"]
    need(manifest["external_proof"] == dict(**proof, bytes=(ROOT / proof["path"]).stat().st_size), "D062 proof bytes")


def check_controls(config, record, edges, prefix_edges, pending, report, counted):
    sources = {key: ROOT / ref["path"] for key, ref in config["archives"].items()}
    core_original = read(sources["core_original"])
    core_names, core_edges = audit_original(core_original, CORE_PROFILE)
    source_cert = read(sources["core_certificate"])
    kept = report["seed"]
    counted(source_cert["labels"] == CORE == kept["labels"]
            and source_cert["graph_digest"] == kept["digest"] == core_original["graph_digest"]
            and source_cert["checker"] == kept["checker"], "archived D061 named ledger")
    check_good_source(core_original, core_names, core_edges, CORE, kept["checker"])
    for pos, (c, low) in enumerate(((7, 6), (13, 11))):
        cross = [(u, v) for u, v in core_edges if min(CORE[u], CORE[v]) < c <= max(CORE[u], CORE[v])]
        d = sorted(differences(cross, CORE))
        counted(d == list(range(low, 15)) and kept["cuts"][pos] == {"c": c, "weights": d}, "archived D062 seed cut")
    catalog = read(sources["catalog"])
    source_index = next(row for row in catalog["ledgers"] if row["key"] == "alternative-22")
    counted(source_index["labels"] == CORE and source_index["graph_digest"] == kept["digest"],
            "catalog exact alternative, distinct from Case B")
    k1_original = read(sources["k1_original"])
    k1_names, k1_edges = audit_original(k1_original, K1_PROFILE)
    k1 = report["k1"]
    counted(k1["labels"] == F and all(F[v] == CORE[v]+1 for v in CORE)
            and [F[x] for x in ("b:2:0", "l:2:0:0", "l:2:0:1")] == [0, 16, 17],
            "independent D062 formula at h=k=0")
    counted(k1["digest"] == k1_original["graph_digest"]
            and Counter(map(normalize, k1_edges)) == Counter(map(normalize, (e for e in edges if "s:6" not in e)))
            and (F["s:4"], F["s:5"]) == (10, 11), "old-to-target physical identity")
    check_good_source(k1_original, k1_names, k1_edges, F, k1["checker"])
    counted(k1["named_edges"] == named_rows(k1_edges, differences(k1_edges, F)), "K=1 named edge ledger")
    frozen = report["frozen_prefix"]
    labels = {v: x for v, x in F.items() if v != "s:5"}
    diff = differences(prefix_edges, labels)
    R = sorted(set(range(19)) - set(labels.values()))
    D = sorted(set(range(1, 19)) - set(diff))
    counted(frozen["labels"] == labels and frozen["port"] == ["s:4", 10]
            and frozen["assigned_edges"] == named_rows(prefix_edges, diff)
            and frozen["pending"] == [list(edge) for edge in pending], "frozen-prefix physical record")
    counted(R == [11, 18] and D == [1, 18] and frozen["checker"]["valid"]
            and frozen["checker"]["unused_labels"] == R and frozen["checker"]["unused_differences"] == D,
            "frozen-prefix complements")
    suffixes = []
    for nearby, end in (R, R[::-1]):
        suffixes.append(differences(pending, {"s:4": labels["s:4"], "s:5": nearby, "s:6": end}))
    counted(frozen["suffix_weights"] == dict(zip(("A","B"), suffixes)) and frozen["valid_orders"] == []
            and all(sorted(ds) != D for ds in suffixes), "frozen-prefix rejection, both orders")
    wrong = report["wrong_digest"]
    counted(wrong["input_labels"] == {} and wrong["wrong_expected"] != wrong["matching_expected"]
            and wrong["matching_expected"] == record["graph_digest"] and wrong["wrong"]["valid"] is False
            and wrong["wrong"]["graph_digest"] == record["graph_digest"]
            and wrong["wrong"]["errors"] == wrong["matching"]["errors"] + ["original graph digest mismatch"],
            "adverse original digest")
    counted(read(sources["nested_audit"])["status"] == "PASS"
            and read(sources["D059"])["second_cut_matches_q2"] == read(sources["D059"])["second_cut_matches_q3"] == []
            and read(sources["D060"])["second_host_matches"] == [], "archived scoped controls")
    counted(all(read(sources[key])["status"] == "INCOMPLETE"
                for key in ("joint_incomplete", "third_zero_incomplete")), "historical INCOMPLETE controls")


def audit_cases(rows, names, edges, prefix_edges, pending, digest):
    prefix_names = names - {"s:5", "s:6"}
    pass_cases = []
    table = []
    for c, row in zip(range(19), rows, strict=True):
        need(type(row["threshold"]) is int and row["threshold"] == c and set(row["orders"]) == {"A", "B"},
             "threshold and order grid")
        available = [label for label in range(19) if label != c]
        mapped_s5 = available[F["s:5"]]
        head = {v: available[F[v]] for v in prefix_names}
        ds = differences(prefix_edges, head)
        R = sorted(set(range(19)) - set(head.values()))
        D = sorted(set(range(1, 19)) - set(ds))
        prefix = row["prefix"]
        need(len(head) == len(set(head.values())) == 17 and R == sorted((c, mapped_s5)), "prefix label injection")
        need(prefix["labels"] == head and prefix["R"] == R and prefix["D"] == D
             and prefix["port"] == ["s:4", head["s:4"]] and prefix["pending"] == [list(e) for e in pending],
             "saved actual prefix and boundary")
        check_inventory(prefix["label_inventory"], list(head.values()), 0, 18)
        check_inventory(prefix["difference_inventory"], ds, 1, 18)
        need(prefix["named_edge_differences"] == named_rows(prefix_edges, ds), "actual assigned edge weights")
        valid_prefix = len(ds) == len(set(ds)) and all(1 <= d <= 18 for d in ds)
        need(prefix["valid"] is valid_prefix, "prefix validity")
        # A shift from w to w+1 collides exactly when w+1 stays put.
        old_cross = [(u, v) for u, v in prefix_edges if min(F[u], F[v]) < c <= max(F[u], F[v])]
        cross_weights = sorted(differences(old_cross, F))
        first = min(cross_weights, default=18)
        need(valid_prefix == (cross_weights == list(range(first, 18))), "assigned-edge tail criterion")
        if valid_prefix:
            need(D == [1, first], "two exact differences from a valid prefix")
        tail_report = {}
        for order, seq in (("A", (mapped_s5, c)), ("B", (c, mapped_s5))):
            saved = row["orders"][order]
            labels = dict(head, **{"s:5": seq[0], "s:6": seq[1]})
            complete = differences(edges, labels)
            tail = differences(pending, labels)
            valid = sorted(complete) == list(range(1, 19))
            uses_both = sorted(tail) == D
            need(saved["labels"] == labels and set(labels) == names
                 and all(type(x) is int for x in labels.values()) and sorted(labels.values()) == list(range(19)),
                 "full candidate label bijection")
            check_inventory(saved["label_inventory"], list(labels.values()), 0, 18)
            check_inventory(saved["difference_inventory"], complete, 1, 18)
            need(saved["named_edge_differences"] == named_rows(edges, complete)
                 and saved["suffix_edges"] == named_rows(pending, tail)
                 and saved["uses_both_missing_differences"] == uses_both and valid == (valid_prefix and uses_both),
                 "actual difference spectrum and two-edge consumer")
            ck = saved["checker"]
            need(ck["graph_digest"] == digest and (ck["n"], ck["m"]) == (19, 18)
                 and ck["edge_differences"] == complete and ck["valid"] is valid, "frozen original checker")
            missing = [w for w in range(1, 19) if w not in complete]
            counts = Counter(complete)
            repeated = [[w, counts[w]] for w in sorted(counts) if counts[w] > 1]
            need(valid or bool(missing and repeated), "explicit rejection arithmetic")
            if valid:
                pass_cases.append([c, order])
            tail_report[order] = {"weights": tail, "missing": missing, "repeated": repeated, "accepted": valid}
        # A retains the old F edge to s:5 and attaches one new terminal there.
        all_old = [edge for edge in edges if "s:6" not in edge]
        crossings = sorted(differences([e for e in all_old if min(F[v] for v in e) < c <= max(F[v] for v in e)], F))
        d0 = abs(mapped_s5-c)
        need(tail_report["A"]["accepted"] == (crossings == list(range(d0, 18))), "D059 full one-cut tail at s:5")
        table.append({"threshold": c, "port": head["s:4"], "R": R, "D": D, "valid_prefix": valid_prefix,
                      "prefix_crossings": cross_weights,
                      "prefix_repeated": prefix["difference_inventory"]["repeated"],
                      "order_A_required_start": d0, "order_A_old_crossings": crossings, "orders": tail_report})
    return table, pass_cases


def main():
    started = process_time()
    need(sys.version_info[:2] in {(3, 12), (3, 13)}, "Python 3.12 or 3.13")
    need(not (HERE / "audit_result.json").exists(), "occupied audit output")
    config = read(HERE / "config.json")
    freeze = read(HERE / "freeze.json")
    result = read(HERE / "result.json")
    lim = config["limits"]
    need(config["parameters"] == [2,2,2,2] and config["target_profile"] == TARGET_PROFILE
         and config["thresholds"] == list(range(19)) and (lim["thresholds"],lim["candidates"]) == (19,38),
         "frozen task")
    check_source_custody(config, freeze)
    orig = read(HERE / "target_original.json")
    names, edges = audit_original(orig, TARGET_PROFILE)
    need((len(names), len(edges)) == (19,18), "target order and size")
    suffix_names = {"s:5", "s:6"}
    pending = [edge for edge in edges if suffix_names.intersection(edge)]
    assigned = [edge for edge in edges if not suffix_names.intersection(edge)]
    need(Counter(map(normalize, pending)) == Counter(map(normalize, [("s:4","s:5"),("s:5","s:6")]))
         and len(assigned) == 16, "physical suffix and sole crossing")
    check_names = []

    def counted(ok, name):
        check_names.append(name)
        need(result["control_assertions"] + len(check_names) <= lim["control_assertions"], "combined control cap")
        need(ok, name)

    control = read(HERE / "controls.json")
    counted(result["control_assertions"] == len(control["assertions"]), "validator control list")
    check_controls(config, orig, edges, assigned, pending, control, counted)
    log = HERE / "candidates.jsonl"
    need(sha(log) == result["candidates_sha256"] and (result["thresholds"],result["full_candidates"]) == (19,38)
         and result["model_complete"] is True and (result["new_originals"],result["solver_queries"]) == (1,0),
         "complete saved scope")
    rows = [json.loads(line) for line in log.read_bytes().splitlines()]
    table, accepted = audit_cases(rows, names, edges, assigned, pending, orig["graph_digest"])
    scientific_status = "VERIFIED_WITNESS" if accepted else "EXHAUSTED_RESTRICTED_NEGATIVE"
    need(accepted == result["witnesses"] and scientific_status == result["status"], "scientific disposition")
    elapsed = process_time() - started
    total_cpu = elapsed + freeze["cpu_seconds"] + result["cpu_seconds"]
    need(total_cpu <= lim["max_cpu_seconds"], "combined process CPU cap")
    report = {"status": "PASS", "scientific_status": scientific_status, "witnesses": accepted,
              "target_digest": orig["graph_digest"], "thresholds": len(table), "audited_saved_candidates": 2*len(table),
              "new_originals": 0, "new_candidate_assignments": 0, "solver_queries": 0,
              "arithmetic_control_assertions": check_names, "combined_control_assertions": len(check_names)+result["control_assertions"],
              "table": table, "cpu_seconds": elapsed, "combined_cpu_seconds": total_cpu,
              "runtime": {"python": sys.version, "platform": sys.platform, "implementation": sys.implementation.name},
              "raw_bindings": {p: sha(HERE / p) for p in
                               ("target_original.json", "controls.json", "candidates.jsonl", "result.json", "audit.py")}}
    data = json.dumps(report, indent=2, sort_keys=True).encode() + b"\n"
    sizes = [p.stat().st_size for p in HERE.iterdir() if p.is_file()] + [len(data)]
    need(max(sizes) <= lim["max_record_bytes"] and sum(sizes) <= lim["max_total_bytes"], "run byte caps")
    with (HERE / "audit_result.json").open("xb") as output:
        output.write(data)
    print(f"PASS: same 19 thresholds and 38 saved candidates. {scientific_status}.")


if __name__ == "__main__":
    main()
