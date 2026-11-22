"""Search-free checker run on the declared rooted core and four exact targets."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

RUN = "B4-1R22-K1-ROOTED-CORE-001-20261121"
PARENT = "2920269aeb30e99f0bc36a4559c24c95c7ccce84"
OUTPUT = HERE / "validation"
CAP = 2_000_000
CORE_PROFILE = [[1], [], [2], [2], [], []]
PROOF = "research/B4_1R22_K1_ROOTED_CORE.md"
SOURCE = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "requirements.txt", "pyproject.toml")
RETAINED = (
    "research/B4_UNPADDED_1R22_SUPPLIER.md",
    "evidence/validation/B4_UNPADDED_1R22_SUPPLIER_001/REVIEWS.md",
    "research/B4_Q1T2_K1_ROOTED_CORE.md",
    "research/B4_THIRD_ZERO_HOST_K1_DIRECT.md",
    "research/B4_THIRD_ZERO_HOST_NONADJACENT.md",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/raw_result.json",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, record):
    raw = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= CAP, f"result over byte limit: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def plan(r):
    if type(r) is not int or r < 2:
        raise ValueError("r must be an exact integer >= 2")
    return r + 15


def core_labels():
    return {
        "s:0": 13, "s:1": 0, "s:2": 10, "s:3": 4, "s:4": 8, "s:5": 3,
        "b:0:0": 1, "l:0:0:0": 12,
        "b:2:0": 2, "l:2:0:0": 9, "l:2:0:1": 11,
        "b:3:0": 7, "l:3:0:0": 5, "l:3:0:1": 6,
    }


def supply_prefix(r, core):
    plan(r)
    require(core["s:1"] == 0, "wrong physical root")
    prefix = {v: x + r for v, x in core.items() if v != "s:5"}
    prefix["b:1:0"] = r + 14
    prefix["l:1:0:0"] = 0
    prefix.update({f"l:1:0:{j}": r - j for j in range(1, r)})
    return prefix


def hold(name, profile, order):
    require(order <= 20, "original order exceeds campaign limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == order and len(graph["edges"]) == order - 1, "wrong graph size")
    digest = graph_digest(graph)
    path = OUTPUT / "originals" / f"{name}.json"
    raw_hash = save(path, {"graph": graph, "graph_digest": digest})
    return graph, {"path": f"originals/{path.name}", "graph_digest": digest, "sha256_raw": raw_hash}


def ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])}
            for u, v in graph["edges"] if u in labels and v in labels]


def witness(graph):
    path = [f"s:{i}" for i in range(6)]
    edges = {frozenset(edge) for edge in graph["edges"]}
    require(graph["spine"] == path and all(frozenset((u, v)) in edges
            for u, v in zip(path[:-1], path[1:], strict=True)), "wrong spine witness")
    distances = dict.fromkeys(path, 0)
    for v, role in graph["roles"].items():
        section = role["section"]
        if role["kind"] == "branch":
            require(frozenset((v, f"s:{section}")) in edges, "wrong center incidence")
            distances[v] = 1
        elif role["kind"] == "leaf":
            center = f"b:{section}:0"
            require(frozenset((v, center)) in edges and frozenset((center, f"s:{section}")) in edges,
                    "wrong terminal incidence")
            distances[v] = 2
    require(set(distances) == set(graph["vertices"]), "incomplete witness")
    return {"path": path, "distances": distances}


def check_core(original):
    graph, ref = original
    labels = core_labels()
    check = verify_certificate(graph, labels, ref["graph_digest"])
    require(check["valid"] and labels["s:1"] == 0, "core verification or root pin")
    return {"original": ref, "physical_root": {"vertex": "s:1", "label": 0}, "labels": labels,
            "edge_ledger": ledger(graph, labels), "witness": witness(graph), "verification": check}


def check_target(r, original, core, core_hash):
    graph, ref = original
    prefix = supply_prefix(r, core["labels"])
    pending = [edge for edge in graph["edges"] if set(edge).difference(prefix)]
    require(set(graph["vertices"]).difference(prefix) == {"s:5"} and pending == [["s:4", "s:5"]],
            "wrong physical remainder")
    partial = verify_partial(graph, prefix)
    port = {"vertex": "s:4", "label": r + core["labels"]["s:4"]}
    want_label = r + core["labels"]["s:5"]
    want_difference = abs(core["labels"]["s:4"] - core["labels"]["s:5"])
    require(partial["valid"] and partial["graph_digest"] == ref["graph_digest"] and not partial["complete"]
            and partial["frontier"] == ["s:4"] and partial["unused_labels"] == [want_label]
            and partial["unused_differences"] == [want_difference] and prefix["s:4"] == port["label"],
            "wrong singleton interface")
    require(abs(port["label"] - want_label) == want_difference, "wrong resource consumption")
    labels = {**prefix, "s:5": want_label}
    complete = verify_certificate(graph, labels, ref["graph_digest"])
    require(complete["valid"], "full verification failed on the retained original")
    return {"parameters": {"r": r, "K": 1}, "original": ref,
            "core": {"path": "core.json", "sha256_raw": core_hash},
            "prefix": prefix, "prefix_edge_ledger": ledger(graph, prefix), "partial_verification": partial,
            "port": port, "crossing_edge": pending[0], "remaining_vertices": ["s:5"],
            "unused_labels": partial["unused_labels"], "unused_differences": partial["unused_differences"],
            "completion": {"vertex": "s:5", "label": want_label, "edge": pending[0], "difference": want_difference},
            "labels": labels, "edge_ledger": ledger(graph, labels), "witness": witness(graph),
            "verification": complete}


def grow(old, r, h):
    require(old["l:1:0:0"] == 0 and old["b:1:0"] == r + 14, "wrong supplied growth premise")
    shifted = {v: x + (h if v != "l:1:0:0" else 0) for v, x in old.items()}
    fresh = {f"l:1:0:{r+i}": h-i for i in range(h)}
    require(not shifted.keys() & fresh.keys(), "fresh name collision")
    return {**shifted, **fresh}


def growth_check(cases, originals):
    two, three, four = (cases[r]["labels"] for r in (2, 3, 4))
    first = grow(two, 2, 1)
    repeated = grow(first, 3, 1)
    one_batch = grow(two, 2, 2)
    require(first == three and repeated == one_batch == four, "pointwise named growth mismatch")
    for r, s in ((2, 3), (2, 4), (3, 4)):
        before, after = (originals[i][0] for i in (r, s))
        fresh = {f"l:1:0:{i}" for i in range(r, s)}
        old_edges, new_edges = ({frozenset(e) for e in graph["edges"]} for graph in (before, after))
        require(set(before["vertices"]) < set(after["vertices"])
                and set(after["vertices"]) - set(before["vertices"]) == fresh
                and old_edges < new_edges and new_edges - old_edges == {frozenset(("b:1:0", leaf)) for leaf in fresh},
                "wrong original growth incidences")
    return {"base_r": 2, "via_r": 3, "same_target_r": 4, "fresh_names": ["l:1:0:2", "l:1:0:3"],
            "intermediate": first, "one_batch": one_batch, "successive_batches": repeated,
            "direct": four, "pointwise_equal": True, "additional_targets": 0}


def rejections():
    outcomes = []
    for value in (True, 2.0, "2", 1):
        try:
            plan(value)
        except ValueError as error:
            require(str(error) == "r must be an exact integer >= 2", "unexpected rejection")
            outcomes.append({"value": value, "type": type(value).__name__, "error": str(error)})
        else:
            raise ValueError("invalid value admitted")
    return outcomes


def main():
    config_path = HERE / "config.json"
    config_raw = config_path.read_bytes()
    config = json.loads(config_raw)
    require(config == {"run_id": RUN, "parent": PARENT, "core_profile": CORE_PROFILE,
                       "completed_r": [2, 3, 4, 5], "completed_orders": [17, 18, 19, 20], "K": 1,
                       "workers": 1, "max_vertices": 20, "max_result_bytes": CAP, "solver_queries": 0,
                       "computational_enumeration": 0, "historical_search_replay": 0}, "campaign configuration changed")
    require(git("rev-parse", "HEAD").decode().strip() == PARENT, "unexpected parent")
    require(not git("diff", "HEAD", "--name-only", "--", "lcl", "references"), "protected source changed")
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in {(3, 12), (3, 13)},
            "use the documented project Python")
    OUTPUT.mkdir(exist_ok=False)
    source_hashes = {}
    for rel in SOURCE:
        raw = (ROOT / rel).read_bytes()
        path = OUTPUT / "source" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        source_hashes[rel] = sha(raw)
    identity = {"run_id": RUN, "parent": PARENT, "config_sha256_raw": sha(config_raw),
                "runner_sha256_raw": sha(Path(__file__).read_bytes()), "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
                "proof": {"path": PROOF, "sha256_raw": sha((ROOT / PROOF).read_bytes())},
                "source_sha256_raw": source_hashes,
                "retained_sha256_raw": {rel: sha((ROOT / rel).read_bytes()) for rel in RETAINED},
                "runtime": {"implementation": sys.implementation.name, "python": sys.version,
                            "executable": Path(sys.executable).relative_to(ROOT).as_posix(),
                            "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode, "third_party_imports": []}}
    identity_hash = save(OUTPUT / "identity.json", identity)
    held_core = hold("core", CORE_PROFILE, 14)
    targets = {}
    for r, order in zip(config["completed_r"], config["completed_orders"], strict=True):
        require(plan(r) == order, "wrong target order")
        targets[r] = hold(f"target-r{r}", [[1], [r], [2], [2], [], []], order)
    rejected = rejections()
    save(OUTPUT / "domain_rejections.json", rejected)
    core = check_core(held_core)
    core_hash = save(OUTPUT / "core.json", core)
    cases, completed = {}, []
    for r, original in targets.items():
        case = check_target(r, original, core, core_hash)
        path = OUTPUT / f"target-r{r}.json"
        digest = save(path, case)
        cases[r] = case
        completed.append({"r": r, "K": 1, "n": case["verification"]["n"], "certificate": path.name,
                          "sha256_raw": digest, "bytes": path.stat().st_size})
    comparison_hash = save(OUTPUT / "batch_comparison.json", growth_check(cases, targets))
    summary = {"run_id": RUN, "identity_sha256_raw": identity_hash, "status": "PASS",
               "core_sha256_raw": core_hash, "auxiliary_cores": 1, "completed_targets": completed,
               "domain_rejections": len(rejected), "batch_comparison_sha256_raw": comparison_hash,
               "solver_queries": 0, "computational_enumeration": 0, "historical_search_replay": 0}
    save(OUTPUT / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
