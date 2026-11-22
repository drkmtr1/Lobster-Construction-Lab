"""Freeze two controls and issue at most one original-bound production DFS."""

import json
from pathlib import Path
import platform
import subprocess
import sys

import audit

HERE, ROOT, OUT = audit.HERE, audit.ROOT, audit.DATA
PARENT = "f67418a57906f4f37b3d20d12a800373db571e0a"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "lcl/search.py", "lcl/budget.py",
           "pyproject.toml", "requirements.txt")
CAP = 2_000_000
PROFILE = [[2], [2], [], [2], [], []]
PINS = {"s:2": 14}
LIMITS = {"max_vertices": 15, "max_nodes": 100000, "time_limit": 6, "max_states": 20000}

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.search import solve
from lcl.verify import verify_certificate


def write(path, raw):
    audit.require(len(raw) <= CAP, "result byte cap")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def save(name, value):
    write(OUT / name, (json.dumps(value, sort_keys=True, indent=2) + "\n").encode())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def cut_table(rows, labels, host):
    b = labels[host]
    table = []
    for c in range(len(rows) + 2):
        old = sorted(row["difference"] for row in rows
                     if (labels[row["edge"][0]] < c) != (labels[row["edge"][1]] < c))
        d0 = b-c+1 if b >= c else c-b
        required = list(range(d0, len(rows) + 1))
        table.append({"c": c, "crossing": old, "required": required, "matches": old == required,
                      "host_side": "at_or_above" if b >= c else "below"})
    return table


def check_certificate(original, labels, profile, max_order):
    graph = original["graph"]
    checked = verify_certificate(graph, labels, original["graph_digest"])
    audit.require(checked["valid"] is True, f"rejected certificate: {checked['errors']}")
    rows = audit.ledger(original, labels, profile, max_order)
    return {"labels": labels, "checker": checked, "ledger": rows}


def freeze(name, profile, order):
    graph = build_graph(profile)
    audit.require(len(graph["vertices"]) == order, "unexpected order")
    original = {"graph": graph, "graph_digest": graph_digest(graph)}
    audit.original_edges(original, profile)
    save(name, original)
    return original


def main():
    config = audit.load(HERE / "config.json")
    audit.require(config["parent"] == PARENT == git("rev-parse", "HEAD").decode().strip()
                  and config["profile"] == PROFILE and config["pins"] == PINS and config["domains"] == {}
                  and config["count"] is False and config["workers"] == 1 and config["limits"] == LIMITS
                  and config["max_bytes"] == CAP and config["max_lift_order"] == 18
                  and config["searches_max"] == 1 and config["automatic_retries"] == config["historical_replays"] == 0
                  and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "frozen pilot scope")
    # A fresh output directory is required even after any failed or interrupted attempt.
    OUT.mkdir()
    snapshots = {}
    for path in SOURCES:
        original = (ROOT / path).read_bytes()
        audit.require(original.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{path}").replace(b"\r\n", b"\n"), path)
        write(OUT / "source" / path, original)
        snapshots[path] = audit.sha(OUT / "source" / path)
    retained = {}
    controls = []
    for spec in config["controls"]:
        for name in ("original", "certificate"):
            path = spec[name]
            audit.require((ROOT / path).read_bytes() == git("show", f"{PARENT}:{path}"), path)
            retained[path] = audit.sha(ROOT / path)
        old = audit.load(ROOT / spec["original"])
        cert = audit.load(ROOT / spec["certificate"])
        labels = cert["labels"]
        result = check_certificate(old, labels, spec["profile"], 15)
        audit.require(labels["s:2"] == 13 and result["checker"] == cert["verification"]
                      and result["ledger"] == cert["edge_ledger"]
                      and cert["original"]["graph_digest"] == old["graph_digest"]
                      and cert["original"]["sha256_raw"] == retained[spec["original"]], "retained certificate")
        cuts = cut_table(result["ledger"], labels, spec["host"])
        audit.require(cuts == audit.independent_cuts(result["ledger"], labels, spec["host"]), "cut disagreement")
        controls.append({**result, "id": spec["id"], "host": spec["host"], "graph_digest": old["graph_digest"],
                         "cuts": cuts})
    audit.require([item["id"] for item in controls] == ["q2", "r2"], "control accounting")
    save("controls.json", controls)
    save("identity.json", {"parent": PARENT, "id": config["id"], "source_sha256": snapshots,
         "retained_sha256": retained, "config_sha256": audit.sha(HERE / "config.json"),
         "runner_sha256": audit.sha(HERE / "run.py"), "auditor_sha256": audit.sha(HERE / "audit.py"),
         "commands_sha256": audit.sha(HERE / "commands.json"),
         "runtime": {"python": sys.version, "implementation": sys.implementation.name,
                     "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
                     "optional_dependencies": []}})
    audit.require(not any(row["matches"] for record in controls for row in record["cuts"]),
                  "retained formula supplies a cut; do not query")
    original = freeze("core_original.json", PROFILE, 15)
    save("query_started.json", {"graph_digest": original["graph_digest"], "pins": PINS, "domains": {},
                               "count": False, "method": "dfs"})
    raw = solve(original["graph"], pins=PINS, domains={}, limits=LIMITS, count=False)
    save("raw_query.json", raw)
    result = {"status": raw["status"], "query_count": 1}
    try:
        if raw["status"] == "SAT":
            labels = raw["witness"]
            core = check_certificate(original, labels, PROFILE, 15)
            audit.require(labels["s:2"] == 14 and (labels["s:1"] == 0 or labels["s:3"] == 0), "root or zero neighbor")
            core["cuts"] = {host: cut_table(core["ledger"], labels, host) for host in ("b:0:0", "b:1:0")}
            profile = [[2], [2], [2], [2], [], []]
            target = freeze("lift_original.json", profile, 18)
            lifted = {v: x + 1 for v, x in labels.items()}
            lifted.update({"b:2:0": 0, "l:2:0:0": 16, "l:2:0:1": 17})
            result.update(core=core, lift=check_certificate(target, lifted, profile, 18))
        elif raw["status"] not in {"INCOMPLETE", "EXHAUSTED_NO_SOLUTION"}:
            raise ValueError("invalid query result")
    except (TypeError, ValueError, KeyError) as error:
        save("result.json", {"status": "REVISE", "query_count": 1, "error": str(error)})
        raise
    save("result.json", result)
    print(json.dumps({"status": raw["status"], "nodes": raw["nodes"],
                      "elapsed_seconds": raw["elapsed_seconds"], "reason": raw.get("reason")}, sort_keys=True))


if __name__ == "__main__":
    main()
