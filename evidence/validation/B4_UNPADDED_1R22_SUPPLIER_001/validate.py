"""Search-free original-target validation of the declared 1R22 cases."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.consumers import _nonadjacent_path_labels
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

RUN = "B4-UNPADDED-1R22-SUPPLIER-001-20261121"
PARENT = "048e5a1d59a2b7a861cc4810b01f42f8baf024c7"
OUTPUT = HERE / "validation"
LIMIT = 2_000_000
PENDING = "s:4"
WITNESS = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
DIAGNOSTICS = "evidence/validation/B4_FOURTH_2_SUPPLY_001"
PROOF = "research/B4_UNPADDED_1R22_SUPPLIER.md"
SOURCE = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "lcl/consumers.py",
          "requirements.txt", "pyproject.toml")
RETAINED = (
    "research/ALPHA_LOWER_BLOCK_LEAF_INSERTION.md", "research/ALPHA_UPPER_BLOCK_GENERAL_HOST.md",
    "research/B4_UNPADDED_QR12.md", "research/B4_THIRD_ZERO_HOST_NONADJACENT.md",
    "research/B4_UNPADDED_Q1T2.md", "research/B4_Q1T2_K1_ROOTED_CORE.md",
    "research/B2_NONADJACENT_CONSUMER.md", f"{DIAGNOSTICS}/DIAGNOSTICS.md",
    *(f"{DIAGNOSTICS}/diagnostic_results/1122-{side}.json" for side in ("adjacent", "nonadjacent")),
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    raw = (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= LIMIT, f"oversized record {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(raw)
    return sha(raw)


def domain(name, value):
    if type(value) is not int or value < 2:
        raise ValueError(f"{name} must be an exact integer >= 2")


def plan(r, K):
    domain("r", r)
    domain("K", K)
    return r + K + 14


def normalized(r):
    domain("r", r)
    labels = {
        "s:0": r + 12, "s:1": r, "s:2": r + 11, "s:3": r + 5, "s:4": r + 7,
        "b:0:0": r + 4, "l:0:0:0": r + 9,
        "b:1:0": r + 13, "l:1:0:0": 0,
        "b:2:0": r + 1, "l:2:0:0": r + 8, "l:2:0:1": r + 10,
        "b:3:0": r + 6, "l:3:0:0": r + 2, "l:3:0:1": r + 3,
    }
    labels.update({f"l:1:0:{j}": r - j for j in range(1, r)})
    return labels


def hold(name, profile, order):
    require(order <= 23, f"{name} exceeds declared vertex limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == order and len(graph["edges"]) == order - 1, "wrong size")
    digest = graph_digest(graph)
    path = OUTPUT / "originals" / f"{name}.json"
    raw_hash = save(path, {"graph": graph, "graph_digest": digest})
    return graph, {"path": f"originals/{path.name}", "graph_digest": digest, "sha256_raw": raw_hash}


def ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])}
            for u, v in graph["edges"] if u in labels and v in labels]


def witness_distances(graph):
    adjacency = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(all(v in adjacency[u] for u, v in zip(WITNESS[:-1], WITNESS[1:], strict=True)), "wrong witness path")
    distances = dict.fromkeys(WITNESS, 0)
    for level in (1, 2):
        frontier = [v for v, d in distances.items() if d == level - 1]
        for v in frontier:
            for u in adjacency[v]:
                distances.setdefault(u, level)
    require(set(distances) == set(graph["vertices"]) and distances["b:1:0"] == 1, "wrong witness distance")
    return distances


def check_seed(r, original):
    graph, ref = original
    labels = normalized(r)
    check = verify_certificate(graph, labels, ref["graph_digest"])
    p = r + 6
    require(check["valid"] and all((labels[u] < p) != (labels[v] < p) for u, v in graph["edges"]),
            "wrong normalized alpha certificate")
    require(labels["b:0:0"] == r + 4 and labels[PENDING] == p + 1, "wrong normalized ports")
    selected = [v for v in graph["vertices"] if labels[v] < 1]
    incident = [row for row in ledger(graph, labels) if set(row["edge"]) & set(selected)]
    require(selected == ["l:1:0:0"] and labels["b:1:0"] == r + 13
            and incident == [{"edge": ["b:1:0", "l:1:0:0"], "difference": r + 13}], "wrong returned premise")
    return {"r": r, "original": ref, "labels": labels, "edge_ledger": ledger(graph, labels),
            "alpha": {"low_size": p, "low": sorted(v for v in labels if labels[v] < p),
                      "high": sorted(v for v in labels if labels[v] >= p)},
            "state": {"n": r + 14, "p": p, "x": r + 4, "y": 1, "L": "b:0:0", "U": PENDING},
            "witness": WITNESS, "witness_distances": witness_distances(graph),
            "lower_predicate": {"threshold": 1, "host": "b:1:0", "host_label": r + 13,
                                "selected_vertices": selected, "incident": incident},
            "verification": check}


def check_target(r, K, original, seed):
    graph, ref = original
    p = seed["state"]["p"]
    prefix = {v: x + K if x >= p else x for v, x in seed["labels"].items()}
    path = [f"s:{i}" for i in range(4, K + 5)]
    pending = set(path[1:])
    necessary = {frozenset(edge) for edge in zip(path[:-1], path[1:], strict=True)}
    actual = [edge for edge in graph["edges"] if pending.intersection(edge)]
    require(set(graph["vertices"]) - prefix.keys() == pending and len(actual) == K
            and set(map(frozenset, actual)) == necessary, "wrong physical remainder")
    crossing = [edge for edge in actual if bool(set(edge) & prefix.keys())]
    require(crossing == [["s:4", "s:5"]], "wrong original crossing")
    partial = verify_partial(graph, prefix)
    require(partial["valid"] and not partial["complete"] and partial["graph_digest"] == ref["graph_digest"]
            and partial["frontier"] == [PENDING] and prefix[PENDING] == p + K + 1
            and partial["unused_labels"] == list(range(p, p + K))
            and partial["unused_differences"] == list(range(1, K + 1)), "wrong resource contract")
    values = _nonadjacent_path_labels(K, p)
    require(len(values) == K + 1 and values[0] == prefix[PENDING], "wrong sequence binding")
    labels = {**prefix, **dict(zip(path[1:], values[1:], strict=True))}
    check = verify_certificate(graph, labels, ref["graph_digest"])
    require(check["valid"], "completion failed on the retained original")
    return {"parameters": {"r": r, "K": K}, "original": ref, "normalized": f"normalized-r{r}.json",
            "prefix": prefix, "prefix_edge_ledger": ledger(graph, prefix), "partial_verification": partial,
            "port": {"vertex": PENDING, "label": prefix[PENDING]}, "crossing_edge": crossing[0],
            "unused_labels": partial["unused_labels"], "unused_differences": partial["unused_differences"],
            "remaining_vertices": path[1:], "path": path, "path_labels": values,
            "suffix_edge_ledger": ledger({"edges": actual}, labels), "labels": labels,
            "edge_ledger": ledger(graph, labels), "verification": check}


def retained_recheck(side):
    path = f"{DIAGNOSTICS}/diagnostic_results/1122-{side}.json"
    raw = (ROOT / path).read_bytes()
    record = json.loads(raw)
    original = build_graph([[1], [1], [2], [2], []])
    digest = graph_digest(original)
    require(digest == record["original_graph_digest"] == graph_digest(record["original_graph"]), "retained graph")
    labels = record["solver_result"]["witness"]
    check = verify_certificate(original, labels, digest)
    require(check["valid"] and labels["s:4"] == {"adjacent": 7, "nonadjacent": 8}[side]
            and all((labels[u] < 7) != (labels[v] < 7) for u, v in original["edges"]), "retained alpha")
    host = labels["b:1:0"]
    cuts = []
    for c in range(1, 8):
        selected = sorted(v for v in labels if labels[v] < c)
        weights = sorted(row["difference"] for row in ledger(original, labels)
                         if set(selected).intersection(row["edge"]))
        expected = list(range(host - c + 1, 15))
        require(weights != expected, "unexpected lower-block predicate")
        cuts.append({"c": c, "selected": selected, "weights": weights, "required": expected})
    return {"side": side, "source": path, "source_sha256_raw": sha(raw), "host_label": host,
            "exit_label": labels["s:4"], "check": check, "cuts": cuts}


def rejected_inputs():
    records = []
    for key in ("r", "K"):
        for value in (True, 2.0, "2", 1):
            args = {"r": 2, "K": 2, key: value}
            try:
                plan(**args)
            except ValueError as error:
                require(str(error) == f"{key} must be an exact integer >= 2", "unexpected rejection")
                records.append({"parameter": key, "value": value, "type": type(value).__name__, "error": str(error)})
            else:
                raise ValueError("invalid input admitted")
    return records


def main():
    config_path = HERE / "config.json"
    conf = json.loads(config_path.read_bytes())
    require(conf == {"run_id": RUN, "parent": PARENT, "workers": 1, "max_vertices": 23,
                     "max_result_bytes": LIMIT, "solver_queries": 0, "labeling_enumeration": 0,
                     "normalized_r": [2, 3, 4], "completed_r_K": [[2, 2], [2, 3], [3, 4], [4, 5]],
                     "completed_orders": [18, 19, 21, 23], "retained": ["adjacent", "nonadjacent"]},
            "campaign configuration changed")
    require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip() == PARENT,
            "unexpected parent")
    require(not subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", "lcl", "references"], cwd=ROOT),
            "protected source changed")
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in {(3, 12), (3, 13)},
            "use the documented project Python")
    OUTPUT.mkdir(exist_ok=False)
    source_hashes = {}
    for rel in SOURCE:
        raw = (ROOT / rel).read_bytes()
        path = OUTPUT / "source" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as output:
            output.write(raw)
        source_hashes[rel] = sha(raw)
    identity = {"run_id": RUN, "parent": PARENT, "config_sha256_raw": sha(config_path.read_bytes()),
                "runner_sha256_raw": sha(Path(__file__).read_bytes()), "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
                "proof": {"path": PROOF, "sha256_raw": sha((ROOT / PROOF).read_bytes())}, "source_sha256_raw": source_hashes,
                "retained_sha256_raw": {rel: sha((ROOT / rel).read_bytes()) for rel in RETAINED},
                "runtime": {"implementation": sys.implementation.name, "python": sys.version,
                            "executable": Path(sys.executable).relative_to(ROOT).as_posix(),
                            "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
                            "third_party_imports": []}}
    identity_hash = save(OUTPUT / "identity.json", identity)
    seeds = {r: hold(f"normalized-r{r}", [[1], [r], [2], [2], []], r + 14) for r in conf["normalized_r"]}
    targets = {}
    for (r, K), order in zip(conf["completed_r_K"], conf["completed_orders"], strict=True):
        require(plan(r, K) == order, "wrong declared order")
        targets[r, K] = hold(f"target-r{r}-K{K}", [[1], [r], [2], [2]] + [[] for _ in range(K + 1)], order)
    retained = [retained_recheck(side) for side in conf["retained"]]
    rejections = rejected_inputs()
    save(OUTPUT / "retained.json", retained)
    save(OUTPUT / "domain_rejections.json", rejections)
    certificates = {}
    for r, original in seeds.items():
        certificates[r] = check_seed(r, original)
        save(OUTPUT / f"normalized-r{r}.json", certificates[r])
    completed = []
    for (r, K), original in targets.items():
        case = check_target(r, K, original, certificates[r])
        path = OUTPUT / f"target-r{r}-K{K}.json"
        digest = save(path, case)
        completed.append({"r": r, "K": K, "n": case["verification"]["n"],
                          "certificate": path.name, "sha256_raw": digest, "bytes": path.stat().st_size})
    summary = {"run_id": RUN, "identity_sha256_raw": identity_hash, "status": "PASS",
               "completed_targets": completed, "normalized_prefixes": sorted(seeds),
               "retained_rechecks": len(retained), "domain_rejections": len(rejections),
               "solver_queries": 0, "labeling_enumeration": 0}
    save(OUTPUT / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
