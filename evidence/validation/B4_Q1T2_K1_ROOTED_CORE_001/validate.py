"""Search-free validation on the declared named core and completed originals."""

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

PARENT = "e9842f1caf0ea0005bf9840ae9bfe1f4b2974242"
RUN = "B4-Q1T2-K1-ROOTED-CORE-001-20261121"
LIMIT = 2_000_000
OUTPUT = HERE / "validation"
PROOF = "research/B4_Q1T2_K1_ROOTED_CORE.md"
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")
RETAINED = (
    "research/B4_THIRD_ZERO_HOST_K1_DIRECT.md",
    "research/B4_UNPADDED_Q1T2.md",
    "research/ALPHA_UPPER_BLOCK_GENERAL_HOST.md",
    "research/ALPHA_LOWER_BLOCK_LEAF_INSERTION.md",
    "research/B4_THIRD_ZERO_HOST_K1.md",
    "references/upstream/mdl/N241_relational_ports.md",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_DIRECT_001/validation/core_certificate.json",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/raw_result.json",
    "evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, record):
    raw = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(raw) <= LIMIT, f"record over byte limit: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def domain(name, value):
    if type(value) is not int or value < 2:
        raise ValueError(f"{name} must be an exact integer >= 2")


def core_labels(q):
    domain("q", q)
    labels = {
        "s:0": q + 10, "s:1": 1, "s:2": q + 11,
        "s:3": 0, "s:4": 5, "s:5": 4,
        "b:0:0": 2, "l:0:0:0": 10,
        "b:1:0": 8, "l:1:0:0": 6,
        "b:3:0": 3, "l:3:0:0": 9, "l:3:0:1": 7,
    }
    labels.update({f"l:0:0:{j}": 10 + j for j in range(1, q)})
    return labels


def supply_prefix(q, t):
    domain("q", q)
    domain("t", t)
    prefix = {vertex: label + 1 for vertex, label in core_labels(q).items() if vertex != "s:5"}
    prefix["b:2:0"] = 0
    prefix.update({f"l:2:0:{j}": q + 13 + j for j in range(t)})
    return prefix


def hold_original(name, profile, order):
    require(order <= 20, "original order exceeds campaign limit")
    graph = build_graph(profile)
    require(len(graph["vertices"]) == order and len(graph["edges"]) == order - 1,
            "original order or size mismatch")
    digest = graph_digest(graph)
    path = OUTPUT / "originals" / f"{name}.json"
    original_hash = save(path, {"graph": graph, "graph_digest": digest})
    return graph, {"path": f"originals/{path.name}", "sha256_raw": original_hash,
                   "graph_digest": digest}


def ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])}
            for u, v in graph["edges"] if u in labels and v in labels]


def check_core(q, original):
    graph, ref = original
    labels = core_labels(q)
    check = verify_certificate(graph, labels, ref["graph_digest"])
    require(check["valid"] and labels["s:2"] == q + 11, "core verification or root pin")
    return {"q": q, "original": ref, "physical_root": {"vertex": "s:2", "label": q + 11},
            "labels": labels, "edge_ledger": ledger(graph, labels), "verification": check}


def check_target(q, t, original, core):
    graph, ref = original
    prefix = supply_prefix(q, t)
    edges = [edge for edge in graph["edges"] if any(v not in prefix for v in edge)]
    require(set(graph["vertices"]) - prefix.keys() == {"s:5"} and edges == [["s:4", "s:5"]],
            "wrong physical remainder")
    partial = verify_partial(graph, prefix)
    port = {"vertex": "s:4", "label": prefix["s:4"]}
    require(partial["valid"] and partial["graph_digest"] == ref["graph_digest"]
            and not partial["complete"] and partial["frontier"] == ["s:4"]
            and partial["unused_labels"] == [5] and partial["unused_differences"] == [1]
            and port["label"] == 6, "wrong singleton interface")
    used = partial["unused_labels"][0]
    weight = abs(port["label"] - used)
    require(weight == partial["unused_differences"][0], "final edge consumes wrong difference")
    labels = {**prefix, "s:5": used}
    require(all(labels[v] == x + 1 for v, x in core["labels"].items()), "core translation mismatch")
    check = verify_certificate(graph, labels, ref["graph_digest"])
    require(check["valid"], "full verification failed")
    return {
        "parameters": {"q": q, "t": t, "K": 1}, "original": ref, "core_certificate": f"core-q{q}.json",
        "prefix": prefix, "prefix_edge_ledger": ledger(graph, prefix), "partial_verification": partial,
        "port": port, "remaining_vertices": ["s:5"], "crossing_edge": edges[0],
        "unused_labels": [used], "unused_differences": [weight],
        "completion": {"vertex": "s:5", "label": used, "edge": edges[0], "difference": weight},
        "labels": labels, "edge_ledger": ledger(graph, labels), "verification": check,
    }


def rejected_inputs():
    cases = [(True, "bool"), (2.0, "float"), ("2", "str"), (1, "int"), (-2, "int")]
    records = []
    for parameter in ("q", "t"):
        for value, kind in cases:
            args = {"q": 2, "t": 2, parameter: value}
            try:
                supply_prefix(**args)
            except ValueError as error:
                require(str(error) == f"{parameter} must be an exact integer >= 2",
                        "unexpected rejection")
                records.append({"parameter": parameter, "value": value, "type": kind, "error": str(error)})
            else:
                raise ValueError("invalid case admitted")
    return records


def main():
    config_bytes = (HERE / "config.json").read_bytes()
    config = json.loads(config_bytes)
    expected = {
        "run_id": RUN, "parent": PARENT, "workers": 1, "max_vertices": 20, "max_result_bytes": LIMIT,
        "solver_queries": 0, "enumeration": 0, "auxiliary_core_q": [2, 3, 4], "K": 1,
        "completed_q_t": [[2, 2], [2, 3], [3, 2], [4, 3]], "completed_orders": [17, 18, 18, 20],
    }
    require(config == expected, "campaign configuration changed")
    require(git("rev-parse", "HEAD").decode().strip() == PARENT, "unexpected parent")
    require(not git("diff", "HEAD", "--name-only", "--", "lcl", "references"), "protected source changed")
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in {(3, 12), (3, 13)},
            "use the documented project Python")
    OUTPUT.mkdir(exist_ok=False)
    source_hashes = {}
    for rel in SOURCES:
        raw = (ROOT / rel).read_bytes()
        path = OUTPUT / "source" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
        source_hashes[rel] = sha(raw)
    identity_hash = save(OUTPUT / "identity.json", {
        "run_id": RUN, "parent": PARENT, "config_sha256_raw": sha(config_bytes),
        "runner_sha256_raw": sha(Path(__file__).read_bytes()), "audit_sha256_raw": sha((HERE / "audit.py").read_bytes()),
        "proof": {"path": PROOF, "sha256_raw": sha((ROOT / PROOF).read_bytes())},
        "source_sha256_raw": source_hashes,
        "retained_sha256_raw": {rel: sha((ROOT / rel).read_bytes()) for rel in RETAINED},
        "runtime": {"implementation": sys.implementation.name, "python": sys.version,
                    "executable": Path(sys.executable).relative_to(ROOT).as_posix(),
                    "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
                    "third_party_imports": []},
    })
    cores = {q: hold_original(f"core-q{q}", [[q], [1], [], [2], [], []], q + 12)
             for q in config["auxiliary_core_q"]}
    targets = [hold_original(f"target-q{q}-t{t}", [[q], [1], [t], [2], [], []], order)
               for (q, t), order in zip(config["completed_q_t"], config["completed_orders"], strict=True)]
    rejections = rejected_inputs()
    save(OUTPUT / "domain_rejections.json", rejections)
    core_certificates = {}
    for q, original in cores.items():
        record = check_core(q, original)
        save(OUTPUT / f"core-q{q}.json", record)
        core_certificates[q] = record
    completed = []
    for (q, t), original in zip(config["completed_q_t"], targets, strict=True):
        record = check_target(q, t, original, core_certificates[q])
        path = OUTPUT / f"target-q{q}-t{t}.json"
        digest = save(path, record)
        completed.append({"parameters": [q, t], "n": record["verification"]["n"],
                          "certificate": path.name, "sha256_raw": digest, "bytes": path.stat().st_size})
    summary = {"run_id": RUN, "identity_sha256_raw": identity_hash, "status": "PASS",
               "completed_targets": completed, "auxiliary_cores": sorted(cores),
               "domain_rejections": len(rejections), "solver_queries": 0, "enumeration": 0}
    save(OUTPUT / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
