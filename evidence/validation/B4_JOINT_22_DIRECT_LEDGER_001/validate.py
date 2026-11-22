"""Verify the two predeclared ledgers and one fixed-size lift without search."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
PARENT = "e3138ed2804883396fb548f824316155fc859974"
PROOF = "research/B4_JOINT_22_DIRECT_LEDGER.md"
CORE = [[2], [2], [], [2], [], []]
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
CAP = 2_000_000
LIMITS = {"workers": 1, "solver_queries": 0, "labeling_enumeration_nodes": 0,
          "candidates_max": 4, "per_case_max": 2, "max_order": 18, "max_bytes": CAP,
          "cpu_seconds": 30, "max_graph_records": 4, "automatic_retries": 0}

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def require(condition, context):
    if not condition:
        raise ValueError(context)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def write(path, raw):
    require(len(raw) <= CAP, f"result byte cap: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def save(name, value):
    write(OUT / name, (json.dumps(value, sort_keys=True, indent=2) + "\n").encode())


def original_record(profile, n):
    graph = build_graph(profile)
    require(len(graph["vertices"]) == n <= LIMITS["max_order"], "original order cap")
    return {"graph": graph, "graph_digest": graph_digest(graph)}


def ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]


def inventories(rows, labels, m):
    weights = [item["difference"] for item in rows]
    repeats = {str(w): count for w, count in Counter(weights).items() if count > 1}
    return {"used_labels": sorted(labels.values()), "unused_labels": sorted(set(range(m + 1)) - set(labels.values())),
            "used_differences": sorted(weights), "unused_differences": sorted(set(range(1, m + 1)) - set(weights)),
            "repeated_differences": repeats}


def exact_t(t):
    if type(t) is not int or t < 1:
        raise ValueError("t must be an exact positive integer")
    return t


def main():
    started = process_time()
    config = read(HERE / "config.json")
    require(config["parent"] == PARENT == git("rev-parse", "HEAD").decode().strip()
            and config["limits"] == LIMITS and config["lift_t"] == 2
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "scope or runtime")
    candidates = config["candidates"]
    require(len(candidates) == 2 and [c["case"] for c in candidates] == ["A", "B"]
            and [c["zero"] for c in candidates] == ["s:1", "s:3"]
            and [s["id"] for s in config["controls"]] == ["q2", "r2"], "exact record scope")
    OUT.mkdir()
    refs = {}
    for path in [config["pilot_original"], config["historical_incomplete"],
                 *(s[k] for s in config["controls"] for k in ("original", "certificate"))]:
        raw = (ROOT / path).read_bytes()
        require(raw == git("show", f"{PARENT}:{path}"), f"retained raw bytes: {path}")
        refs[path] = sha(raw)
    snapshots = {}
    for path in SOURCES:
        raw = (ROOT / path).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{path}").replace(b"\r\n", b"\n"), path)
        write(OUT / "source" / path, raw)
        snapshots[path] = sha(raw)
    files = [HERE / name for name in ("config.json", "validate.py", "audit.py", "commands.json")] + [ROOT / PROOF]
    save("identity.json", {"id": config["id"], "parent": PARENT, "retained_sha256": refs, "source_sha256": snapshots,
         "inputs_sha256": {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in files},
         "runtime": {"python": sys.version, "implementation": sys.implementation.name,
                     "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode, "optional_dependencies": []}})

    controls = []
    for spec in config["controls"]:
        original = read(ROOT / spec["original"])
        cert = read(ROOT / spec["certificate"])
        graph, labels = original["graph"], cert["labels"]
        checked = verify_certificate(graph, labels, original["graph_digest"])
        rows = ledger(graph, labels)
        require(graph["profile"] == spec["profile"] and len(graph["vertices"]) == 14
                and labels["s:2"] == 13 and checked["valid"] and checked == cert["verification"]
                and rows == cert["edge_ledger"] and cert["original"]["graph_digest"] == original["graph_digest"]
                and cert["original"]["sha256_raw"] == refs[spec["original"]], "retained core binding")
        controls.append({"id": spec["id"], "graph_digest": original["graph_digest"],
                         "labels": labels, "ledger": rows, "checker": checked})
    save("controls.json", controls)

    original = original_record(CORE, 15)
    require(original == read(ROOT / config["pilot_original"]), "same physical core as the pilot")
    save("core_original.json", original)
    graph = original["graph"]
    digest = original["graph_digest"]
    for candidate in candidates:
        labels = candidate["labels"]
        require(labels["s:2"] == 14 and labels[candidate["zero"]] == 0, "physical root or zero")
        rows = ledger(graph, labels)
        checked = verify_certificate(graph, labels, digest)
        data = inventories(rows, labels, 14)
        require(data["used_labels"] == list(range(15)), "candidate complete assignment")
        seen = set()
        first_repeat = None
        for row in rows:
            difference = row["difference"]
            if difference in seen:
                first_repeat = row
                break
            seen.add(difference)
        case = candidate["case"]
        save(f"candidate_{case}.json", {**candidate, "graph_digest": digest, "physical_s2": labels["s:2"],
             "ledger": rows, "inventories": data, "first_repeated_edge": first_repeat, "checker": checked})
        if case == "A":
            require(not checked["valid"] and data["unused_differences"] == [6]
                    and data["repeated_differences"] == {"2": 2}, "Case A falsifier")
        else:
            require(checked["valid"] and first_repeat is None and data["used_differences"] == list(range(1, 15)),
                    "Case B seed")
    core = candidates[1]["labels"]
    adverse_digest = "0" * 64
    adverse = verify_certificate(graph, core, adverse_digest)
    require(adverse["valid"] is False and adverse["errors"] == ["original graph digest mismatch"], "adverse binding")
    save("adverse.json", {"expected_digest": adverse_digest, "actual_digest": digest, "checker": adverse})

    guards = []
    for value in (True, 0, 2.0, "2"):
        try:
            exact_t(value)
        except ValueError:
            guards.append({"input": value, "type": type(value).__name__, "rejected": True})
        else:
            raise ValueError("invalid t accepted")
    t = exact_t(config["lift_t"])
    target = original_record([[2], [2], [t], [2], [], []], 18)
    save("lift_original.json", target)
    lifted = {v: label + 1 for v, label in core.items() if v != "s:5"}
    lifted["b:2:0"] = 0
    for j in range(t):
        lifted[f"l:2:0:{j}"] = 16 + j
    target_graph = target["graph"]
    missing = set(target_graph["vertices"]) - lifted.keys()
    pending = [edge for edge in target_graph["edges"] if any(v in missing for v in edge)]
    require(missing == {"s:5"} and pending == [["s:4", "s:5"]], "physical singleton boundary")
    prefix_rows = [{"edge": edge, "difference": abs(lifted[edge[0]] - lifted[edge[1]])}
                   for edge in target_graph["edges"] if edge not in pending]
    prefix_inventory = inventories(prefix_rows, lifted, t + 15)
    require(prefix_inventory["unused_labels"] == [6] and prefix_inventory["unused_differences"] == [2]
            and lifted["s:4"] == 8 and abs(lifted["s:4"] - 6) == 2, "both singleton resources")
    final = {**lifted, "s:5": 6}
    checked = verify_certificate(target_graph, final, target["graph_digest"])
    require(checked["valid"], "exact completed original")
    save("lift.json", {"t": t, "graph_digest": target["graph_digest"], "prefix": lifted,
                       "prefix_inventories": prefix_inventory, "port": {"vertex": "s:4", "label": 8},
                       "pending_edges": pending, "labels": final, "ledger": ledger(target_graph, final),
                       "checker": checked, "invalid_t_inputs": guards})
    cpu = process_time() - started
    require(cpu <= LIMITS["cpu_seconds"], "validation CPU budget")
    save("summary.json", {"status": "PASS", "validation_cpu_seconds": cpu, "graph_records": 4,
         "retained_controls": 2, "candidates": 2, "accepted_candidates": 1, "failed_candidates": 1,
         "solver_queries": 0, "labeling_enumeration_nodes": 0, "completed_t2": 1})
    print(f"PASS: two candidates, one verified rooted core, one exact t=2 lift ({cpu:.6f} CPU seconds)")


if __name__ == "__main__":
    main()
