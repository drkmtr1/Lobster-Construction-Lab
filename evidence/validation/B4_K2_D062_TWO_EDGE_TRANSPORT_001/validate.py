"""Check only the 38 prescribed transports on one frozen original."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if Path.cwd() != ROOT:
    raise SystemExit("Run from the repository root.")
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial, verify_graph

PARENT = "2e558bc9f13c2437e381272360452e9ff2de3646"
PROFILE = [[2], [2], [2], [2], [], [], []]
SUFFIX = [["s:4", "s:5"], ["s:5", "s:6"]]
UNASSIGNED = {"s:5", "s:6"}
CORE_DIGEST = "0de66c6b0db0331b1798bbb1b5e6f563ee10b8cd614635445ce73efbd7f57a03"
K1_DIGEST = "1e9734225ebec5d92882fa276792b21af7abd8142652472fc9daf772b5431495"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE / name).read_bytes())


def raw(obj):
    return json.dumps(obj, sort_keys=True, indent=2).encode() + b"\n"


def save(name, obj, limits):
    data = raw(obj)
    require(len(data) <= limits["max_record_bytes"], f"result byte cap: {name}")
    with (HERE / name).open("xb") as stream:
        stream.write(data)


def inputs(config):
    found = {name: sha(HERE / name) for name in ("audit.py", "commands.json", "config.json", "validate.py")}
    for ref in config["archives"].values():
        found[ref["path"]] = sha(ROOT / ref["path"])
        require(found[ref["path"]] == ref["sha256"], f"archive bytes: {ref['path']}")
    for name, expected in config["production"].items():
        found[name] = sha(ROOT / name)
        require(found[name] == expected, f"production input bytes: {name}")
    return found


def archive(config, key):
    return json.loads((ROOT / config["archives"][key]["path"]).read_bytes())


def freeze(config, limits, started):
    require(subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == PARENT, "parent checkout")
    require(not any((HERE / name).exists() for name in
                    ("target_original.json", "freeze.json", "controls.json", "candidates.jsonl", "result.json",
                     "audit_result.json")), "occupied output path")
    source_hashes = inputs(config)
    target = build_graph(PROFILE)
    require(verify_graph(target)["valid"] and len(target["vertices"]) == 19 and len(target["edges"]) == 18,
            "single target topology and cap")
    save("target_original.json", {"graph": target, "graph_digest": graph_digest(target)}, limits)
    save("freeze.json", {"parent": PARENT, "target_sha256": sha(HERE / "target_original.json"),
                        "input_sha256": source_hashes, "runtime": {
                            "python": sys.version, "implementation": sys.implementation.name,
                            "platform": platform.system(), "utf8_mode": sys.flags.utf8_mode},
                        "new_originals": 1, "cpu_seconds": process_time() - started}, limits)


def ledger(edges, labels):
    return [{"edge": edge, "difference": abs(labels[edge[0]] - labels[edge[1]])} for edge in edges]


def inventory(values, alphabet):
    counts = Counter(values)
    return {"values": sorted(values), "unused": sorted(set(alphabet) - counts.keys()),
            "repeated": [[v, n] for v, n in sorted(counts.items()) if n > 1],
            "out_of_range": sorted(counts.keys() - set(alphabet))}


def controls(config, target, digest, assigned_edges, pending_edges, counted):
    old = archive(config, "core_original")
    seed = archive(config, "core_certificate")
    core, f0 = old["graph"], seed["labels"]
    seed_receipt = verify_certificate(core, f0, old["graph_digest"])
    counted(seed_receipt == seed["checker"] and seed_receipt["valid"], "archived D061 certificate")
    counted(old["graph_digest"] == CORE_DIGEST == seed["graph_digest"] == graph_digest(core), "D061 original identity")
    counted([f0[x] for x in ("b:0:0", "b:1:0", "s:2", "s:4", "s:5")] == [1, 2, 14, 9, 10],
            "D061 physical ports and maximum")
    s7 = sorted(row["difference"] for row in ledger(core["edges"], f0)
                if (f0[row["edge"][0]] < 7) != (f0[row["edge"][1]] < 7))
    s13 = sorted(row["difference"] for row in ledger(core["edges"], f0)
                 if (f0[row["edge"][0]] < 13) != (f0[row["edge"][1]] < 13))
    counted(s7 == list(range(6, 15)) and s13 == list(range(11, 15)), "D062 seed cuts")
    k1 = archive(config, "k1_original")
    f = {v: d + 1 for v, d in f0.items()}
    f.update({"b:2:0": 0, "l:2:0:0": 16, "l:2:0:1": 17})
    f_receipt = verify_certificate(k1["graph"], f, k1["graph_digest"])
    counted(k1["graph_digest"] == K1_DIGEST == graph_digest(k1["graph"]), "reused K=1 original identity")
    counted(f_receipt["valid"] and (f_receipt["n"], f_receipt["m"]) == (18, 17), "D062 K=1 checker")
    counted([f[v] for v in ("s:2", "s:4", "s:5", "b:2:0")] == [15, 10, 11, 0], "D062 physical labels")
    counted([e for e in target["edges"] if "s:6" not in e] == k1["graph"]["edges"],
            "target retains exact named K=1 edges")
    frozen_labels = {v: d for v, d in f.items() if v not in UNASSIGNED}
    frozen = verify_partial(target, frozen_labels)
    counted(frozen["valid"] and frozen["frontier"] == ["s:4"] and frozen["graph_digest"] == digest,
            "frozen partial original")
    counted(frozen["unused_labels"] == [11, 18] and frozen["unused_differences"] == [1, 18],
            "frozen-prefix target complements")
    weights_a = [abs(10-11), abs(11-18)]
    weights_b = [abs(10-18), abs(18-11)]
    counted(sorted(weights_a) != [1,18] and sorted(weights_b) != [1,18], "frozen-prefix rejection in both orders")

    # Empty labels isolate the digest control from the 38 full candidate checks.
    matched = verify_certificate(target, {}, digest)
    wrong = verify_certificate(target, {}, "0"*64)
    counted(not wrong["valid"] and wrong["graph_digest"] == digest
            and wrong["errors"] == matched["errors"] + ["original graph digest mismatch"], "wrong expected digest")
    return f, {"seed": {"digest": CORE_DIGEST, "labels": f0, "checker": seed_receipt,
                         "cuts": [{"c": 7, "weights": s7}, {"c": 13, "weights": s13}]},
               "k1": {"digest": K1_DIGEST, "labels": f, "checker": f_receipt,
                      "named_edges": ledger(k1["graph"]["edges"], f)},
               "frozen_prefix": {"labels": frozen_labels, "checker": frozen, "port": ["s:4", 10],
                                 "assigned_edges": ledger(assigned_edges, frozen_labels), "pending": pending_edges,
                                 "suffix_weights": {"A": weights_a, "B": weights_b}, "valid_orders": []},
               "wrong_digest": {"input_labels": {}, "matching_expected": digest, "wrong_expected": "0"*64,
                                "matching": matched, "wrong": wrong}}


def check_candidates(config, limits, started):
    require(not any((HERE / name).exists() for name in ("controls.json", "candidates.jsonl", "result.json",
                                                       "audit_result.json")), "occupied checking output")
    original = read("target_original.json")
    frozen = read("freeze.json")
    require(frozen["parent"] == PARENT and frozen["input_sha256"] == inputs(config)
            and frozen["target_sha256"] == sha(HERE / "target_original.json"), "frozen bindings")
    target, digest = original["graph"], original["graph_digest"]
    require(target["profile"] == PROFILE and graph_digest(target) == digest and len(target["vertices"]) == 19
            and len(target["edges"]) == 18, "frozen exact target")
    assigned = [edge for edge in target["edges"] if UNASSIGNED.isdisjoint(edge)]
    pending = [edge for edge in target["edges"] if not UNASSIGNED.isdisjoint(edge)]
    require(pending == SUFFIX and len(assigned) == 16, "physical suffix incidence")
    control_names = []

    def counted(condition, message):
        control_names.append(message)
        require(len(control_names) <= limits["control_assertions"], "control cap")
        require(condition, message)

    f, control = controls(config, target, digest, assigned, pending, counted)
    control["assertions"] = control_names
    save("controls.json", control, limits)
    thresholds = 0
    candidates = 0
    accepted = []
    size = 0
    label_alphabet, diff_alphabet = range(19), range(1, 19)
    with (HERE / "candidates.jsonl").open("xb") as stream:
        for c in config["thresholds"]:
            thresholds += 1
            require(thresholds <= limits["thresholds"], "threshold cap")
            g = {v: d + int(d >= c) for v, d in f.items()}
            head = {v: d for v, d in g.items() if v not in UNASSIGNED}
            named_prefix = ledger(assigned, head)
            labs = inventory(list(head.values()), label_alphabet)
            diffs = inventory([row["difference"] for row in named_prefix], diff_alphabet)
            require(set(head) == set(target["vertices"]) - UNASSIGNED
                    and labs["unused"] == sorted([c, g["s:5"]])
                    and not labs["repeated"] and not labs["out_of_range"], "two unused labels")
            valid_prefix = not diffs["repeated"] and not diffs["out_of_range"]
            verdicts = {}
            for order, (s5, s6) in (("A", (g["s:5"], c)), ("B", (c, g["s:5"]))):
                candidates += 1
                require(candidates <= limits["candidates"], "candidate cap")
                labels = {**head, "s:5": s5, "s:6": s6}
                suffix = ledger(pending, labels)
                d = sorted(row["difference"] for row in suffix)
                uses_both = len(diffs["unused"]) == 2 and d == diffs["unused"]
                label_inventory = inventory(list(labels.values()), label_alphabet)
                named_edges = ledger(target["edges"], labels)
                difference_inventory = inventory([row["difference"] for row in named_edges], diff_alphabet)
                receipt = verify_certificate(target, labels, digest)
                require(label_inventory["values"] == list(label_alphabet) and receipt["graph_digest"] == digest
                        and receipt["edge_differences"] == [row["difference"] for row in named_edges]
                        and receipt["valid"] is (valid_prefix and uses_both), "original checker disagreement")
                if receipt["valid"]:
                    accepted.append([c, order])
                verdicts[order] = {"labels": labels, "label_inventory": label_inventory,
                                   "named_edge_differences": named_edges, "difference_inventory": difference_inventory,
                                   "suffix_edges": suffix, "uses_both_missing_differences": uses_both,
                                   "checker": receipt}
            row = {"threshold": c, "prefix": {"labels": head, "valid": valid_prefix, "port": ["s:4", head["s:4"]],
                                              "pending": pending, "named_edge_differences": named_prefix,
                                              "label_inventory": labs, "difference_inventory": diffs,
                                              "R": labs["unused"], "D": diffs["unused"]}, "orders": verdicts}
            data = json.dumps(row, sort_keys=True, separators=(",", ":")).encode() + b"\n"
            size += len(data)
            require(len(data) <= limits["max_record_bytes"] and size <= limits["max_record_bytes"], "candidate byte cap")
            stream.write(data)
            stream.flush()
            require(frozen["cpu_seconds"] + process_time() - started <= limits["max_cpu_seconds"], "process CPU cap")
        os.fsync(stream.fileno())
    require((thresholds, candidates) == (19, 38), "complete prescribed scope")
    save("result.json", {"status": "VERIFIED_WITNESS" if accepted else "EXHAUSTED_RESTRICTED_NEGATIVE",
                         "model_complete": True, "witnesses": accepted, "thresholds": thresholds,
                         "full_candidates": candidates, "control_assertions": len(control_names),
                         "new_originals": 1, "solver_queries": 0, "cpu_seconds": process_time() - started,
                         "candidates_sha256": sha(HERE / "candidates.jsonl")}, limits)
    print(f"Checked {thresholds} thresholds and {candidates} candidates. Verified witnesses: {accepted}.")


def main():
    started = process_time()
    require(sys.version_info[:2] in {(3, 12), (3, 13)}, "project Python required")
    config = read("config.json")
    limits = config["limits"]
    integers = [*config["parameters"], *config["thresholds"], *limits.values()]
    integers.extend(x for section in config["target_profile"] for x in section)
    require(all(type(x) is int for x in integers), "exact integer configuration")
    require(config["parent"] == PARENT and config["target_profile"] == PROFILE and config["parameters"] == [2]*4
            and config["thresholds"] == list(range(19)) and config["orders"] ==
            {"A": ["G_c(s:5)","c"], "B": ["c","G_c(s:5)"]}, "exact frozen task domain")
    require(limits == dict(workers=1, new_originals=1, max_order=19, thresholds=19, candidates=38,
                           control_assertions=100, max_cpu_seconds=30, max_record_bytes=2000000,
                           max_total_bytes=8000000, solver_queries=0, retries=0), "exact frozen limits")
    require(len(sys.argv) == 2 and sys.argv[1] in {"freeze", "check"}, "use freeze or check")
    if sys.argv[1] == "freeze":
        freeze(config, limits, started)
        print("Frozen one exact named target, 19 vertices and 18 edges.")
    else:
        check_candidates(config, limits, started)


if __name__ == "__main__":
    main()
