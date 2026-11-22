"""Verify the declared B4 originals, retaining evidence before any audit."""
import hashlib
import json
from pathlib import Path
import platform
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.constructors import four_section_111t
from lcl.model import build_graph, graph_digest
from lcl.states import interval_boundary
from lcl.verify import verify_certificate, verify_partial


PAIRS = [[2, 1], [3, 1], [8, 1], [17, 1], [2, 2], [2, 3], [2, 4],
         [3, 5], [4, 6], [5, 7], [8, 8], [31, 32]]
LIMITS = {"workers": 1, "max_vertices": 75, "max_output_bytes": 2_000_000}
BASE = "294f415df2a53f13161b56d5888ed4b0c118f7a0"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, payload):
    data = (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode()
    require(len(data) <= LIMITS["max_output_bytes"], "result exceeds 2 MB")
    with (HERE / name).open("xb") as stream:
        stream.write(data)


def check_left_components():
    graph = build_graph([[1], [1], [1]])
    names = ("s:0", "s:1", "s:2", "b:0:0", "l:0:0:0",
             "b:1:0", "l:1:0:0", "b:2:0", "l:2:0:0")
    witness = ["b:0:0", "s:0", "s:1", "s:2"]
    results = []
    for branch, entries, offsets in [("K>=2", (7, 1, 4, 2, 6, 8, 0, 3, 5), [2, 0]),
                                     ("K=1", (8, 2, 5, 0, 7, 6, 1, 3, 4), [0, 1])]:
        labels = dict(zip(names, entries))
        checked = verify_certificate(graph, labels, graph_digest(graph))
        require(checked["valid"] and all((labels[u] < 4) != (labels[v] < 4) for u, v in graph["edges"]),
                f"{branch} left component certificate or alpha cut")
        require([labels[witness[0]], labels[witness[-1]] - 4] == offsets,
                f"{branch} left component port offsets")
        results.append({"branch": branch, "labels": labels, "certificate": checked,
                        "alpha_low_class_size": 4, "port_offsets": offsets})
    return {"status": "PASS", "completed_target_count": 0, "left_component_certificate_count": len(results),
            "original_component": graph, "port_path": witness, "cases": results}


def check_target(t, K):
    n = t + K + 12
    require(n <= LIMITS["max_vertices"], "target exceeds declared vertex cap")
    profile = [[1], [1], [1], [t]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    digest = graph_digest(original)
    result = four_section_111t(t, K)
    require(result["graph"] == original and result["graph_digest"] == digest, "substituted target")
    require(len(original["vertices"]) == n and len(original["edges"]) == n - 1, "target counts")
    labels, trace = result["labels"], result["trace"][0]
    prefix = trace["prefix_labels"]
    a = t + 5
    R, D = ([4], [t + 3]) if K == 1 else (list(range(a, a + K)), list(range(1, K + 1)))
    port = K + t + 6
    interface = {"active_vertex": "s:4", "active_label": port, "unused_labels": R, "unused_differences": D}
    require(result["claim_scope"]["suffix_interface"] == interface
            and all(trace[key] == value for key, value in interface.items()) and prefix["s:4"] == port,
            "returned interface")
    partial = verify_partial(original, prefix)
    require(partial["valid"] and partial["graph_digest"] == digest and partial["frontier"] == ["s:4"]
            and partial["unused_labels"] == R and partial["unused_differences"] == D,
            "partial certificate or resource inventories")
    adjacent = interval_boundary(original, prefix, "s:4")
    require(not adjacent["valid"], "an adjacent interface was incorrectly reported")
    tail = original["spine"][4:]
    pending = set(tail[1:])
    path = list(zip(tail, tail[1:]))
    actual = [tuple(e) for e in original["edges"] if pending.intersection(e)]
    crossing = [e for e in actual if len(pending.intersection(e)) == 1]
    require(set(original["vertices"]) - set(prefix) == pending and actual == path
            and crossing == [("s:4", "s:5")], "original path and crossing edge")
    require(all(labels[v] == value for v, value in prefix.items()), "completed path changed a prefix label")
    weights = [abs(labels[u] - labels[v]) for u, v in actual]
    require(sorted(labels[v] for v in pending) == R and sorted(weights) == D, "suffix consumption")
    cert = verify_certificate(original, labels, digest)
    require(cert["valid"], "unchanged original-target checker rejected certificate")
    p = result["claim_scope"].get("alpha_low_class_size")
    if K == 1:
        require(p == t + 6 and all((labels[u] < p) != (labels[v] < p) for u, v in original["edges"]),
                "singleton alpha cut")
    else:
        require(p is None, "unexpected completed-alpha claim")
    return {"parameters": {"t": t, "K": K}, "original_graph": original, "original_graph_digest": digest,
            "prefix_labels": prefix, "prefix_interface": interface, "partial_certificate": partial,
            "adjacent_boundary_check": adjacent, "unfinished_edges": actual, "crossing_edge": crossing[0],
            "full_labels": labels, "tail_differences": weights, "alpha_low_class_size": p,
            "independent_certificate": cert}


def main():
    for name in ("regression_result.json", "components_result.json", "source"):
        if (HERE / name).exists():
            raise FileExistsError("Existing evidence is immutable")
    config_path = HERE / "config.json"
    config = json.loads(config_path.read_bytes())
    require(config["cases"] == PAIRS and config["parameter_order"] == ["t", "K"]
            and config["limits"] == LIMITS and config["starting_commit"] == BASE, "unapproved configuration")
    paths = sorted((ROOT / "lcl").glob("*.py")) + sorted(ROOT.glob("requirements*.txt"))
    paths.extend([ROOT / "pyproject.toml", ROOT / "tests/test_b4_unpadded_111t.py"])
    source_hashes = {}
    for src in paths:
        relative = src.relative_to(ROOT)
        dest = HERE / "source" / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        source_hashes[relative.as_posix()] = digest_file(dest)
    identity = {"run_id": config["run_id"], "starting_commit": BASE, "limits": LIMITS,
                "config_sha256_raw": digest_file(config_path), "regression_script_sha256_raw": digest_file(Path(__file__)),
                "source_sha256_raw": source_hashes,
                "environment": {"python": sys.version, "executable": sys.executable,
                                "implementation": platform.python_implementation(), "platform": platform.platform(),
                                "optimization_level": sys.flags.optimize, "utf8_mode": sys.flags.utf8_mode}}
    started = time.perf_counter()
    save("components_result.json", {**identity, **check_left_components()})
    cases = [check_target(t, K) for t, K in config["cases"]]
    save("regression_result.json", {**identity, "status": "PASS", "classification": "COMPLETE",
                                   "case_count": len(cases), "cases": cases,
                                   "elapsed_seconds": time.perf_counter() - started,
                                   "components_sha256_raw": digest_file(HERE / "components_result.json"),
                                   "audit_script_sha256_raw": digest_file(HERE / "independent_audit.py")})
    print(json.dumps({"status": "PASS", "completed_targets": len(cases), "left_component_certificates": 2}))


if __name__ == "__main__":
    main()
