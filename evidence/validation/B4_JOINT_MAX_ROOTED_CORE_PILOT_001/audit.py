"""Standard-library arithmetic on the exact named graphs and saved query."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_edges(record, profile):
    graph = record["graph"]
    spine = [f"s:{i}" for i in range(6)]
    roles = {f"s:{i}": {"kind": "spine", "section": i} for i in range(6)}
    edges = [(f"s:{i}", f"s:{i+1}") for i in range(5)]
    for i, section in enumerate(profile):
        if not section:
            continue
        center = f"b:{i}:0"
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((center, spine[i]))
        for j in range(section[0]):
            leaf = f"l:{i}:0:{j}"
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
            edges.append((center, leaf))
    canonical = [tuple(sorted(edge)) for edge in edges]
    require(Counter(tuple(sorted(edge)) for edge in graph["edges"]) == Counter(canonical)
            and Counter(graph["vertices"]) == Counter(roles.keys()), "original incidences and multiplicities")
    require(graph["schema_version"] == 1 and graph["roles"] == roles
            and graph["spine"] == spine and graph["profile"] == profile, "physical names and roles")
    payload = {"vertices": sorted(roles), "edges": sorted(canonical),
               "roles": roles, "profile": profile, "spine": spine}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    require(hashlib.sha256(raw).hexdigest() == record["graph_digest"], "canonical graph digest")
    return graph["edges"]


def ledger(record, labels, profile, max_order):
    edges = original_edges(record, profile)
    m = len(edges)
    require(m + 1 <= max_order and set(labels) == set(record["graph"]["vertices"])
            and all(type(x) is int for x in labels.values())
            and sorted(labels.values()) == list(range(m + 1)), "exact labels and order")
    rows = [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]
    require(sorted(row["difference"] for row in rows) == list(range(1, m + 1)), "original difference bijection")
    return rows


def independent_cuts(rows, labels, host):
    """Accumulate each edge into every cut it straddles, preserving multiplicity."""
    m = len(rows)
    bands = [[] for _ in range(m + 2)]
    for row in rows:
        low, high = sorted(labels[v] for v in row["edge"])
        for c in range(low + 1, high + 1):
            bands[c].append(row["difference"])
    a = labels[host]
    return [{"c": c, "host_side": "at_or_above" if a >= c else "below",
             "crossing": sorted(band),
             "required": list(range(max(c - a, a - c + 1), m + 1)),
             "matches": sorted(band) == list(range(max(c - a, a - c + 1), m + 1))}
            for c, band in enumerate(bands)]


def checked_certificate(original, labels, profile, record, cap):
    rows = ledger(original, labels, profile, cap)
    require(record["labels"] == labels and record["ledger"] == rows, "saved named label and edge ledger")
    checked = record["checker"]
    require(checked["valid"] is True and checked["errors"] == []
            and checked["n"] == len(labels) and checked["m"] == len(rows)
            and checked["edge_differences"] == [row["difference"] for row in rows]
            and checked["graph_digest"] == original["graph_digest"], "original-bound checker output")
    return rows


def main():
    config = load(HERE / "config.json")
    run = load(DATA / "result.json")
    identity = load(DATA / "identity.json")
    raw = load(DATA / "raw_query.json")
    require(identity["parent"] == config["parent"]
            and identity["config_sha256"] == sha(HERE / "config.json")
            and identity["runner_sha256"] == sha(HERE / "run.py")
            and identity["auditor_sha256"] == sha(HERE / "audit.py")
            and identity["commands_sha256"] == sha(HERE / "commands.json"), "execution identity")
    for path, digest in identity["source_sha256"].items():
        snapshot = DATA / "source" / path
        parent_blob = subprocess.check_output(["git", "show", f'{config["parent"]}:{path}'], cwd=ROOT)
        require(sha(snapshot) == sha(ROOT / path) == digest
                and parent_blob.replace(b"\r\n", b"\n") == snapshot.read_bytes().replace(b"\r\n", b"\n"), path)
    for path, digest in identity["retained_sha256"].items():
        parent_blob = subprocess.check_output(["git", "show", f'{config["parent"]}:{path}'], cwd=ROOT)
        require(sha(ROOT / path) == digest and parent_blob == (ROOT / path).read_bytes(), path)

    controls = load(DATA / "controls.json")
    for spec, saved in zip(config["controls"], controls, strict=True):
        original = load(ROOT / spec["original"])
        cert = load(ROOT / spec["certificate"])
        rows = checked_certificate(original, cert["labels"], spec["profile"], saved, 15)
        cuts = independent_cuts(rows, saved["labels"], spec["host"])
        require(len(saved["labels"]) == 14 and saved["labels"]["s:2"] == 13 and
                saved["id"] == spec["id"] and saved["graph_digest"] == original["graph_digest"]
                and saved["host"] == spec["host"] and saved["cuts"] == cuts
                and not any(row["matches"] for row in cuts), "retained cross-host transfer")
        require(cert["original"]["sha256_raw"] == sha(ROOT / spec["original"])
                and cert["original"]["graph_digest"] == original["graph_digest"]
                and cert["edge_ledger"] == rows and cert["verification"] == saved["checker"], "retained binding")

    original = load(DATA / "core_original.json")
    edges = original_edges(original, [[2],[2],[],[2],[],[]])
    root_neighbors = sorted(v if u == "s:2" else u for u, v in edges if "s:2" in (u, v))
    query = load(DATA / "query_started.json")
    require(query == {"graph_digest": original["graph_digest"], "pins": {"s:2": 14}, "domains": {},
                      "count": False, "method": "dfs"} and root_neighbors == ["s:1", "s:3"]
            and len(edges) == 14 and raw["method"] == "dfs" and raw["limits"] == config["limits"]
            and raw["restrictions"] == {"pins": {"s:2": 14}, "domains": {}, "scope": "restricted",
                 "hidden_symmetry_reduction": False,
                 "count_convention": "bijections on named physical vertices; no symmetry quotient"}
            and 0 <= raw["nodes"] <= 100000 and raw["elapsed_seconds"] >= 0, "single rooted query scope")
    require(run["status"] == raw["status"] and run["query_count"] == 1, "query disposition")
    new_completed = 0
    if raw["status"] == "SAT":
        require(raw["exhausted"] is False and raw["count"] is None and raw["count_lower_bound"] == 1, "first witness")
        labels = raw["witness"]
        rows = checked_certificate(original, labels, config["profile"], run["core"], 15)
        require(labels["s:2"] == 14 and any(labels[v] == 0 for v in root_neighbors)
                and run["core"]["cuts"] == {host: independent_cuts(rows, labels, host)
                                              for host in ("b:0:0", "b:1:0")}, "root and joint cut checks")
        target = load(DATA / "lift_original.json")
        lifted = run["lift"]
        target_rows = checked_certificate(target, lifted["labels"], [[2],[2],[2],[2],[],[]], lifted, 18)
        mapped = {v: x for v, x in lifted["labels"].items() if v in labels}
        new_weights = {tuple(sorted(row["edge"])): row["difference"] for row in target_rows if "b:2:0" in row["edge"]}
        require(len(lifted["labels"]) == 18 and all(mapped[v] - labels[v] == 1 for v in labels)
                and lifted["labels"]["b:2:0"] == 0 and lifted["labels"]["l:2:0:0"] == 16
                and lifted["labels"]["l:2:0:1"] == 17
                and new_weights == {("b:2:0", "s:2"): 15, ("b:2:0", "l:2:0:0"): 16,
                                    ("b:2:0", "l:2:0:1"): 17}, "named lift and exact new difference band")
        new_completed = 1
    elif raw["status"] == "EXHAUSTED_NO_SOLUTION":
        require(raw["exhausted"] is True and raw["count"] == 0
                and raw["count_lower_bound"] == 0 and raw["witness"] is None, "normal exhaustion")
    else:
        require(raw["status"] == "INCOMPLETE" and raw["reason"] in {"max_nodes", "time_limit", "interrupted"}
                and raw["exhausted"] is False and raw["count"] is None
                and raw["count_lower_bound"] == 0 and raw["witness"] is None, "incomplete run scope")
    require((DATA / "lift_original.json").exists() == bool(new_completed), "conditional graph count")
    report = {"status": "PASS", "query_status": raw["status"], "nodes": raw["nodes"], "retained_graphs": 2,
              "joint_core_records": 1, "completed_t2_records": new_completed, "solver_calls_in_audit": 0,
              "audited_files": {p.relative_to(DATA).as_posix(): sha(p) for p in sorted(DATA.rglob("*")) if p.is_file()}}
    payload = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    require(len(payload) <= config["max_bytes"], "audit byte limit")
    with (HERE / "audit_result.json").open("xb") as handle:
        handle.write(payload)
    print(f'PASS: {raw["status"]}; two retained controls, one joint original, {new_completed} completed lift')


if __name__ == "__main__":
    main()
