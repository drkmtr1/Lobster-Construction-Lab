"""Verify the direct 2322 prefix and the two declared suffix certificates."""

from time import process_time

START = process_time()

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
BASE = "3edcdbc3ee793aa3a9a6d12fcda6a5b0e5916670"
PROOF = "research/B4_D075_DIRECT_2322_ALPHA_S4_10.md"
CONSUMER = "research/B2_NONADJACENT_CONSUMER.md"
PROFILE = [[2], [3], [2], [2]]
LOW = ["s:1", "s:3", "b:0:0", "b:2:0", "l:1:0:0", "l:1:0:1",
       "l:1:0:2", "l:3:0:0", "l:3:0:1"]
WITNESS = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
CONTROL_PATHS = {
    "D066": "evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/certificates.json",
    "D070": "evidence/validation/B4_D069_ALT_ALPHA_FIRST_HOST_001/seed.json",
}
CONTROL_ORIGINAL = "evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json"
SEED_GROUPS = ((15, 3, 16, 8, 10), (4, 11, 14), (17, 0, 1, 2), (7, 12, 13), (9, 5, 6))
OUTPUTS = ("prefix_original.json", "k2_original.json", "k5_original.json",
           "controls.json", "certificates.json", "run_result.json",
           "audit_result.json", "command_receipts.json")
MAX_RECORD = 2_000_000
MAX_TOTAL = 10_000_000


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def write(name, data):
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    existing = sum(p.stat().st_size for p in BUNDLE.iterdir() if p.is_file())
    need(len(raw) <= MAX_RECORD and existing + len(raw) <= MAX_TOTAL, "byte cap")
    with (BUNDLE / name).open("xb") as stream:
        stream.write(raw)


def sources():
    tracked = ["lcl/model.py", "lcl/verify.py", PROOF, CONSUMER,
               "research/B4_2222_NONADJACENT_ALL_K.md", CONTROL_ORIGINAL, *CONTROL_PATHS.values()]
    local = ["INTAKE.md", "run.py", "audit.py", "driver.py", "commands.json"]
    return sorted(tracked + [(BUNDLE / p).relative_to(ROOT).as_posix() for p in local])


def frozen_config():
    return {
        "parent": BASE, "attachment_sha256":
            "0dbd5f2a934424135ae9fb32495a409afed5ee62632be8f618785f0e68e80fb0",
        "runtime": {"version": sys.version, "sha256": digest(Path(sys.executable)),
                    "relative_executable": Path(sys.executable).relative_to(ROOT).as_posix()},
        "sources": {p: digest(ROOT / p) for p in sources()},
        "prefix_profile": PROFILE + [[]], "low_names": LOW, "pin": {"s:4": 10},
        "optional_host_tests": {"b:2:0": 0, "b:1:0": 9},
        "method": "explicit ledger from signed weight sum and extreme weight bands on P",
        "limits": {"workers": 1, "feasibility_invocations": 0, "assignment_nodes": 0,
                   "combined_process_cpu_seconds": 30,
                   "bytes_per_record": MAX_RECORD, "bytes_total": MAX_TOTAL,
                   "maximum_order": 23, "new_graphs": 3, "new_maps": 3},
        "targets_on_success": [2, 5], "automatic_retries": 0, "historical_replays": 0,
    }


def save_original(name, profile):
    graph = build_graph(profile)
    # Independent parent check before accepting the project model's digest.
    parents = {}
    for vertex in graph["vertices"]:
        parts = vertex.split(":")
        section = int(parts[1])
        if parts[0] == "s" and section:
            parents[vertex] = f"s:{section-1}"
        elif parts[0] == "b":
            parents[vertex] = f"s:{section}"
        elif parts[0] == "l":
            parents[vertex] = f"b:{section}:0"
    expected_vertices = {f"s:{i}" for i in range(len(profile))}
    for i, (count,) in enumerate(profile[:4]):
        expected_vertices.add(f"b:{i}:0")
        expected_vertices.update(f"l:{i}:0:{j}" for j in range(count))
    need(Counter(graph["vertices"]) == Counter(expected_vertices), "original names")
    need(Counter(tuple(sorted(edge)) for edge in graph["edges"])
         == Counter(tuple(sorted(edge)) for edge in parents.items()), "original incidences")
    need(len(graph["vertices"]) == len(profile) + 4 + sum(x[0] for x in profile[:4])
         <= 23, "original order")
    record = {"graph": graph, "graph_digest": graph_digest(graph)}
    write(name, record)
    return load(BUNDLE / name)


def labeled_edges(graph, labels):
    return [[u, v, abs(labels[u] - labels[v])] for u, v in graph["edges"]
            if u in labels and v in labels]


def ledger_id(original, labels):
    payload = {"graph_digest": original["graph_digest"], "labels": sorted(labels.items())}
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def certificate(original, labels):
    checked = verify_certificate(original["graph"], labels, original["graph_digest"])
    need(checked["valid"], checked["errors"])
    return {"graph_digest": original["graph_digest"], "ledger_id": ledger_id(original, labels),
            "labels": labels, "edges": labeled_edges(original["graph"], labels), "checker": checked}


def archived_controls():
    result = {}
    original = load(ROOT / CONTROL_ORIGINAL)
    for name, path in CONTROL_PATHS.items():
        saved = load(ROOT / path)
        if name == "D066":
            saved = saved["prefix"]
        else:
            expected = saved["original"]
            need(expected["path"] == CONTROL_ORIGINAL and
                 expected["sha256"] == digest(ROOT / CONTROL_ORIGINAL), "D070 original binding")
        record = certificate(original, saved["labels"])
        for key in ("graph_digest", "ledger_id", "checker"):
            need(record[key] == saved[key], f"retained {key}")
        need(saved["labels"]["s:4"] == 9 and
             all((saved["labels"][u] < 8) != (saved["labels"][v] < 8)
                 for u, v in original["graph"]["edges"]), "retained alpha and exit")
        result[name] = record
    need(result["D066"]["graph_digest"] == result["D070"]["graph_digest"] and
         result["D066"]["ledger_id"] != result["D070"]["ledger_id"], "control identities")
    return result


def recurrence(k):
    if k <= 4:
        return {2: [3, 1, 0], 3: [4, 1, 0, 2], 4: [5, 1, 2, 0, 3]}[k]
    return [k+1, 1, k-1] + [k-2-a for a in recurrence(k-3)]


def suffix_contract(original, assigned, k, declared_d):
    graph = original["graph"]
    path = [f"s:{i}" for i in range(4, k+5)]
    pending = [edge for edge in graph["edges"] if any(v not in assigned for v in edge)]
    need(set(graph["vertices"]) - assigned.keys() == set(path[1:]), "pending names")
    need(Counter(tuple(sorted(e)) for e in pending) ==
         Counter(tuple(sorted(e)) for e in zip(path, path[1:])), "actual pending path")
    need(assigned["s:4"] == k+10, "actual s:4 port")
    partial = verify_partial(graph, assigned)
    need(partial["valid"] and partial["graph_digest"] == original["graph_digest"] and
         partial["frontier"] == ["s:4"], "partial and frontier")
    need(partial["unused_labels"] == list(range(9, k+9)), "residual label inventory")
    need(declared_d == partial["unused_differences"] == list(range(1, k+1)),
         "residual difference inventory mismatch")
    return {"partial": partial, "path": path, "pending_edges": pending,
            "crossing": [["s:4", "s:5"]]}


def main():
    need(subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == BASE,
         "wrong reproduction parent")
    need(sys.version_info[:2] in ((3, 12), (3, 13)), "project Python runtime")
    need(not any((BUNDLE / f).exists() for f in OUTPUTS), "existing official output")
    config = frozen_config()
    if sys.argv[1:]:
        need(sys.argv[1:] == ["--freeze"], "expected --freeze")
        need(not (BUNDLE / "config.json").exists(), "configuration already frozen")
        config["freeze_process_cpu_seconds"] = process_time() - START
        write("config.json", config)
        return
    recorded = load(BUNDLE / "config.json")
    need(config == {k: v for k, v in recorded.items() if k != "freeze_process_cpu_seconds"},
         "frozen identities differ")
    original = save_original("prefix_original.json", PROFILE + [[]])
    write("controls.json", archived_controls())
    labels = {f"s:{i}": a for i, a in enumerate(SEED_GROUPS[0])}
    for i, (center, *terminals) in enumerate(SEED_GROUPS[1:]):
        labels[f"b:{i}:0"] = center
        labels.update({f"l:{i}:0:{j}": a for j, a in enumerate(terminals)})
    seed = certificate(original, labels)
    need(seed["labels"]["s:4"] == 10 and
         sorted(seed["labels"][v] for v in LOW) == list(range(9)), "prefix alpha/exit")
    seed.update({"alpha": {"low": sorted(LOW), "high": sorted(set(labels) - set(LOW)),
                           "low_size": 9},
                 "entrance": {"name": "b:0:0", "label": labels["b:0:0"]},
                 "witness_path": WITNESS, "physical_exit": {"name": "s:4", "label": 10},
                 "optional_hosts": {v: {"actual": labels[v], "matches": labels[v] == a}
                                    for v, a in config["optional_host_tests"].items()}})
    adverse = verify_certificate(original["graph"], labels, "0" * 64)
    need(not adverse["valid"] and adverse["errors"] == ["original graph digest mismatch"],
         "wrong digest must fail")
    targets = {}
    for k in config["targets_on_success"]:
        target = save_original(f"k{k}_original.json", PROFILE + [[] for _ in range(k+1)])
        assigned = {v: a + k if a >= 9 else a for v, a in labels.items()}
        suffix = suffix_contract(target, assigned, k, list(range(1, k+1)))
        if k == 2:
            try:
                suffix_contract(target, assigned, 2, [1, 3])
            except ValueError as exc:
                need(str(exc) == "residual difference inventory mismatch", "wrong rejection")
                adverse_suffix = {"valid": False, "declared_d": [1, 3], "error": str(exc),
                                  "graph_digest": target["graph_digest"]}
            else:
                raise ValueError("bad inventory was accepted")
        path_labels = [9+a for a in recurrence(k)]
        need(path_labels[0] == assigned["s:4"], "suffix starts at physical port")
        finished = assigned | dict(zip(suffix["path"][1:], path_labels[1:]))
        targets[str(k)] = certificate(target, finished) | {
            "assigned": assigned, "suffix": suffix, "path_labels": path_labels,
            "seed_ledger_id": seed["ledger_id"], "consumer_sha256": config["sources"][CONSUMER],
        }
    write("certificates.json", {"seed": seed, "targets": targets, "adverse": {
        "wrong_expected_digest": {"expected": "0" * 64, "report": adverse},
        "wrong_suffix_inventory": adverse_suffix}})
    write("run_result.json", {"status": "SUPPLIED", "new_originals": 3,
                              "new_positive_maps": 3, "historical_controls": 2,
                              "negative_controls": 2, "feasibility_invocations": 0,
                              "assignment_nodes": 0, "process_cpu_seconds": process_time() - START})


if __name__ == "__main__":
    main()
