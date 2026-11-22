"""Four declared search-free compositions on original named B4 targets."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.consumers import _nonadjacent_path_labels
from lcl.model import build_graph, graph_digest
from lcl.records import atomic_json, environment, source_inventory, utc_now
from lcl.verify import verify_certificate, verify_partial


CASES = [[2, 2], [3, 3], [4, 4], [3, 5]]
PLAN = {"cases": CASES, "parameter_order": ["t", "K"], "workers": 1, "max_vertices": 21,
        "max_result_bytes": 2_000_000, "search": False}
PROOF = "research/B4_THIRD_ZERO_HOST_NONADJACENT.md"
BASE = {"s:0": 9, "s:1": 1, "s:2": 12, "s:3": 5, "s:4": 8, "b:0:0": 4, "l:0:0:0": 10,
        "b:1:0": 11, "l:1:0:0": 2, "b:2:0": 0, "l:2:0:0": 13, "l:2:0:1": 14,
        "b:3:0": 7, "l:3:0:0": 3, "l:3:0:1": 6}
W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(name):
    return json.loads((HERE / name).read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_multiset(edges):
    return Counter(tuple(sorted(e)) for e in edges)


def check_case(t, K):
    profile = [[1], [1], [t], [2]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    digest = graph_digest(original)
    m = K + t + 12
    path = [f"s:{i}" for i in range(4, K + 5)]
    suffix = set(path[1:])
    tail_edges = list(zip(path, path[1:]))
    incident = [e for e in original["edges"] if suffix.intersection(e)]
    crossing = [e for e in incident if len(suffix.intersection(e)) == 1]
    require(len(original["vertices"]) == m + 1 <= PLAN["max_vertices"]
            and len(original["edges"]) == m
            and edge_multiset(incident) == edge_multiset(tail_edges)
            and edge_multiset(crossing) == edge_multiset([("s:4", "s:5")]),
            "exact original tail")
    for i, count in enumerate((1, 1, t, 2)):
        for j in range(count):
            leaf = f"l:{i}:0:{j}"
            require(edge_multiset(e for e in original["edges"] if leaf in e)
                    == edge_multiset([(f"b:{i}:0", leaf)]), "original leaf attachment")

    normalized = {**BASE, **{f"l:2:0:{j}": 13 + j for j in range(2, t)}}
    normalized_edges = [e for e in original["edges"] if not suffix.intersection(e)]
    weights = [abs(normalized[u] - normalized[v]) for u, v in normalized_edges]
    require(set(original["vertices"]) - normalized.keys() == suffix
            and all(normalized[v] == x for v, x in BASE.items())
            and sorted(normalized.values()) == list(range(t + 13))
            and sorted(weights) == list(range(1, t + 13))
            and all((normalized[u] < 7) != (normalized[v] < 7) for u, v in normalized_edges),
            "normalized extension and label preservation")
    prefix = {v: x + K if x >= 7 else x for v, x in normalized.items()}
    R, D = list(range(7, K + 7)), list(range(1, K + 1))
    partial = verify_partial(original, prefix)
    require(partial["valid"] and partial["graph_digest"] == digest
            and partial["frontier"] == ["s:4"] and prefix["s:4"] == K + 8
            and partial["used_differences"] == list(range(K + 1, m + 1))
            and partial["unused_labels"] == R and partial["unused_differences"] == D,
            "nonadjacent B4 inventories and physical port")

    sequence = _nonadjacent_path_labels(K, 7)
    require(len(sequence) == len(path) and sequence[0] == prefix["s:4"]
            and sorted(sequence[1:]) == R, "translated original path labels")
    full = dict(prefix)
    full.update(zip(path[1:], sequence[1:]))
    require(all(full[v] == x for v, x in prefix.items()), "prefix preservation")
    trace = [{"edge": [u, v], "new_label": full[v], "difference": abs(full[u] - full[v])}
             for u, v in tail_edges]
    require(sorted(row["difference"] for row in trace) == D, "tail difference inventory")
    certificate = verify_certificate(original, full, digest)
    require(certificate["valid"], "original-target graceful certificate")

    extended = W + path[1:]
    require(edge_multiset(zip(extended, extended[1:])) <= edge_multiset(original["edges"]),
            "extended original witness")
    distances = dict.fromkeys(extended, 0)
    for level in (1, 2):
        layer = {v for edge in original["edges"] if set(edge).intersection(distances) for v in edge} - distances.keys()
        distances.update(dict.fromkeys(layer, level))
    require(set(distances) == set(full) and distances["b:2:0"] == 1, "witness distances")
    return {"parameters": {"t": t, "K": K}, "original_graph": original,
            "original_graph_digest": digest, "normalized_extension": normalized,
            "normalized_edge_differences": weights, "normalized_ports": {"b:0:0": 4, "s:4": 8},
            "normalized_port_offsets": [4, 1], "shifted_prefix": prefix,
            "suffix_interface": {"unused_labels": R, "unused_differences": D, "port_vertex": "s:4",
                                 "port_label": prefix["s:4"], "crossing_edge": ["s:4", "s:5"]},
            "partial_certificate": partial, "path_vertices": path, "path_labels": sequence,
            "completion_trace": trace, "full_labels": full, "certificate": certificate,
            "witness": W, "extended_witness": extended, "witness_distances": distances,
            "claim": "ordinary gracefulness on this exact named target"}


def main():
    config = read("config.json")
    plan = read("preflight.json")
    query = read("query_record.json")
    audit = read("audit_result.json")
    require(query["classification"] == "SAT" and query["certificate"]["valid"]
            and query["result"]["witness"] == BASE
            and audit["status"] == "PASS" and audit["new_seed_certificates_audited"] == 1
            and audit["input_sha256_raw"]["query_record.json"] == sha(HERE / "query_record.json")
            and plan["source"] == source_inventory(ROOT)
            and plan["conditional_targets"] == config["conditional_direct_checks"] == PLAN,
            "verified seed, frozen sources and declared four cases")
    output = HERE / "direct_checks"
    output.mkdir()
    identity = {"run_id": config["run_id"] + "-direct", "limits": PLAN, "seed_query_sha256_raw": sha(HERE / "query_record.json"),
                "seed_audit_sha256_raw": sha(HERE / "audit_result.json"), "config_sha256_raw": sha(HERE / "config.json"),
                "runner_sha256_raw": sha(Path(__file__)), "proof": PROOF, "proof_sha256_raw": sha(ROOT / PROOF),
                "source": plan["source"], "runtime": {**environment(), "version": sys.version,
                                                       "utf8_mode": sys.flags.utf8_mode}}
    cap = PLAN["max_result_bytes"]
    atomic_json(output / "identity.json", identity, max_bytes=cap)
    entries = []
    for i, (t, K) in enumerate(CASES, 1):
        name = f"case-{i:02}.json"
        path = output / name
        data = check_case(t, K)
        atomic_json(path, data, max_bytes=cap)
        entries.append({"file": name, "sha256_raw": sha(path), "parameters": data["parameters"],
                        "original_graph_digest": data["original_graph_digest"],
                        "vertices": data["certificate"]["n"], "bytes": path.stat().st_size})
    summary = {"run_id": identity["run_id"], "status": "PASS", "completed_utc": utc_now(),
               "identity_sha256_raw": sha(output / "identity.json"), "cases": entries,
               "completed_targets": len(entries), "new_queries": 0}
    atomic_json(output / "summary.json", summary, max_bytes=cap)
    print(json.dumps({"status": "PASS", "completed_targets": len(entries), "new_queries": 0,
                      "max_vertices": max(row["vertices"] for row in entries),
                      "max_case_bytes": max(row["bytes"] for row in entries)}))


if __name__ == "__main__":
    main()
