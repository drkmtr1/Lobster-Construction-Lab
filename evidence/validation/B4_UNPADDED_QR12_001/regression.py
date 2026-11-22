"""Capture twelve declared QR12 certificates and the standalone 1212 seed."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.ingest import construction_input
from lcl.model import build_graph, graph_digest
from lcl.records import atomic_json, environment, save_source_snapshot, source_inventory, utc_now
from lcl.verify import verify_certificate, verify_partial


CASES = [[1,2,1],[2,2,1],[1,3,1],[2,3,1],[1,2,2],[1,3,3],[3,2,4],[2,4,5],[5,3,8],[3,5,15],[5,8,16],[1,2,64]]
LIMITS = {"workers": 1, "max_cases": 12, "max_vertices": 79, "max_result_bytes": 2_000_000}
HISTORICAL = "evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1212-adjacent.json"
BASE = {"s:0": 14, "s:1": 0, "s:2": 11, "s:3": 7, "s:4": 8,
        "b:0:0": 1, "l:0:0:0": 13, "b:1:0": 10, "l:1:0:0": 4, "l:1:0:1": 5,
        "b:2:0": 3, "l:2:0:0": 12, "b:3:0": 9, "l:3:0:0": 2, "l:3:0:1": 6}
W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def undirected(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def alpha(graph, labels, p):
    low = {v for v in graph["vertices"] if labels[v] < p}
    high = set(graph["vertices"]) - low
    require(sorted(labels[v] for v in low) == list(range(p))
            and sorted(labels[v] for v in high) == list(range(p, len(graph["vertices"])))
            and all((u in low) != (v in low) for u, v in graph["edges"]), "alpha cut")
    return {"low_class_size": p, "cutoff": p - 1, "low_vertices": sorted(low),
            "high_vertices": sorted(high)}


def check_seed(profile):
    original = build_graph(profile)
    digest = graph_digest(original)
    historical_path = ROOT / HISTORICAL
    historical = json.loads(historical_path.read_bytes())
    require(historical["original_graph"] == original and historical["original_graph_digest"] == digest
            and historical["solver_result"]["witness"] == BASE, "historical constants or original differ")
    certificate = verify_certificate(original, BASE, digest)
    require(certificate["valid"] and certificate["n"] == 15 and certificate["m"] == 14,
            "standalone seed certificate")
    require(undirected(zip(W, W[1:])) <= undirected(original["edges"]), "actual witness path")
    reached = set(W)
    distances = {v: 0 for v in W}
    for distance in (1, 2):
        following = {v for edge in original["edges"] if reached.intersection(edge) for v in edge} - reached
        distances.update({v: distance for v in following})
        reached.update(following)
    require(reached == set(original["vertices"]) and distances["b:1:0"] == 1, "witness distances")
    predicates = []
    for side, threshold, host, selected, weights in (
        ("below", 4, "b:1:0", {"s:1", "b:0:0", "l:3:0:0", "b:2:0"}, list(range(7, 15))),
        ("at_or_above", 13, "b:0:0", {"s:0", "l:0:0:0"}, [12, 13, 14]),
    ):
        selector = {v for v, x in BASE.items() if (x < threshold) == (side == "below")}
        incidences = [{"edge": [u, v], "difference": abs(BASE[u] - BASE[v])}
                      for u, v in original["edges"] if selector.intersection((u, v))]
        require(selector == selected and sorted(i["difference"] for i in incidences) == weights,
                "complete seed incident predicate")
        predicates.append({"side": side, "threshold": threshold, "host": host,
                           "host_label": BASE[host], "selected_vertices": sorted(selector),
                           "incidences": incidences, "difference_multiset": weights})
    return {"kind": "separate_normalized_base", "completed_target_count": 0, "status": "PASS",
            "historical_source": {"path": HISTORICAL, "sha256_raw": sha(historical_path)},
            "original_graph": original, "original_graph_digest": digest, "labels": BASE,
            "independent_certificate": certificate, "alpha": alpha(original, BASE, 8),
            "witness": W, "witness_distances": distances, "ports": {"b:0:0": 1, "s:4": 8},
            "port_offsets": [1, 0], "predicates": predicates}


def expected_prefix(q, r, K):
    horizontal = {v: x + (r - 2 if x >= 4 else 0) for v, x in BASE.items()}
    horizontal.update({f"l:1:0:{j}": r + 3 - j for j in range(2, r)})
    for v in ("s:0", "l:0:0:0"):
        horizontal[v] += q - 1
    horizontal.update({f"l:0:0:{j}": r + 10 + j for j in range(1, q)})
    return {v: x + (K if x >= r + 6 else 0) for v, x in horizontal.items()}


def check_completed(q, r, K, limits):
    a = r + 6
    m = K + q + r + 11
    require(m + 1 <= limits["max_vertices"], "target exceeds declared size")
    profile = [[q], [r], [1], [2]] + [[] for _ in range(K + 1)]
    original = build_graph(profile)
    digest = graph_digest(original)
    params = {"q": q, "r": r, "K": K}
    spec = {"method": "four_section_qr12", "parameters": params, "profile": profile}
    declared, result = construction_input(spec, max_vertices=limits["max_vertices"])
    require(declared == original == result["graph"] and len(original["vertices"]) == m + 1
            and len(original["edges"]) == m and result["graph_digest"] == digest,
            "constructor did not return the retained original")
    require(result["method"] == spec["method"] and result["claim_scope"]["parameters"] == params
            and result["claim_scope"]["construction_case"] == "1212_block_insertions", "constructor scope")
    trace, *steps = result["trace"]
    prefix, full = trace["prefix_labels"], result["labels"]
    require(prefix == expected_prefix(q, r, K) and all(type(x) is int for x in prefix.values())
            and sorted(prefix.values()) == list(range(a)) + list(range(a + K, m + 1))
            and all(full[v] == x for v, x in prefix.items()), "prefix formula, inventory or preservation")

    path = [f"s:{index}" for index in range(4, K + 5)]
    path_edges = list(zip(path, path[1:]))
    pending = set(path[1:])
    actual = [e for e in original["edges"] if pending.intersection(e)]
    crossing = [e for e in actual if len(pending.intersection(e)) == 1]
    require(set(original["vertices"]) - prefix.keys() == pending
            and undirected(actual) == undirected(path_edges)
            and undirected(crossing) == undirected([("s:4", "s:5")]), "original suffix topology")
    for branch, count in enumerate((q, r, 1, 2)):
        for leaf in range(count):
            name = f"l:{branch}:0:{leaf}"
            require(undirected(e for e in original["edges"] if name in e)
                    == undirected([(f"b:{branch}:0", name)]), "original branch attachment")

    R, D = list(range(a, a + K)), list(range(1, K + 1))
    partial = verify_partial(original, prefix)
    interface = {"unused_labels": R, "unused_differences": D, "active_vertex": "s:4", "active_label": a + K}
    require(partial["valid"] and partial["graph_digest"] == digest and partial["frontier"] == ["s:4"]
            and partial["used_differences"] == list(range(K + 1, m + 1))
            and partial["unused_labels"] == R and partial["unused_differences"] == D
            and prefix["s:4"] == a + K
            and trace == {"operation": "supplied_interval_interface", "stage": 4, **interface,
                          "prefix_labels": prefix, "prefix_difference_interval": [K + 1, m]},
            "prefix certificate or interface mismatch")

    completion = []
    for j, (u, v) in enumerate(path_edges, 1):
        label = a + (j - 1) // 2 if j % 2 else a + K - j // 2
        require(full[v] == label and abs(full[u] - full[v]) == K - j + 1, "suffix arithmetic")
        completion.append({"operation": "next_spine", "parent": u, "vertex": v,
                           "label": label, "difference": K - j + 1})
    require(steps == completion, "completion trace")
    certificate = verify_certificate(original, full, digest)
    require(certificate["valid"], "full original-target certificate")
    p = a + (K + 1) // 2
    require(result["claim_scope"]["alpha_low_class_size"] == p, "alpha metadata")
    return {"status": "PASS", "parameters": params, "original_graph": original,
            "original_graph_digest": digest, "prefix_labels": prefix, "partial_certificate": partial,
            "interface": interface, "crossing_edge": ["s:4", "s:5"], "original_suffix": path,
            "suffix_edges": path_edges, "completion_trace": steps, "full_labels": full,
            "alpha": alpha(original, full, p), "independent_certificate": certificate}


def main():
    config_path = HERE / "config.json"
    config = json.loads(config_path.read_bytes())
    require(config["cases"] == CASES and config["limits"] == LIMITS and config["search"] == "none"
            and config["seed_profile"] == [[1], [2], [1], [2], []]
            and config["parameter_order"] == ["q", "r", "K"]
            and config["starting_commit"] == "308b1cc34170c293eca01f1c34fff4c1adf7e902"
            and config["method"] == "four_section_qr12" and sys.flags.optimize == 0,
            "declared run config, limits or interpreter flags")
    for directory in ("campaign", "source"):
        require(not (HERE / directory).exists(), "choose a new run identity; existing evidence is immutable")
    campaign = HERE / "campaign"
    campaign.mkdir()
    source = source_inventory(ROOT)
    save_source_snapshot(ROOT, HERE / "source", source)
    test_source = "tests/test_b4_unpadded_qr12.py"
    test_bytes = (ROOT / test_source).read_bytes()
    test_snapshot = HERE / "source" / test_source
    test_snapshot.parent.mkdir(exist_ok=False)
    with test_snapshot.open("xb") as out:
        out.write(test_bytes)
    identity = {"run_id": config["run_id"], "starting_commit": config["starting_commit"],
                "config_sha256_raw": sha(config_path), "runner_sha256_raw": sha(Path(__file__)),
                "audit_sha256_raw": sha(HERE / "independent_audit.py"),
                "source": source, "focused_test": {"path": test_source, "sha256_raw": sha(test_snapshot)},
                "runtime": {**environment(), "executable": sys.executable, "version": sys.version,
                            "utf8_mode": sys.flags.utf8_mode}, "limits": LIMITS}
    cap = LIMITS["max_result_bytes"]
    atomic_json(campaign / "identity.json", identity, max_bytes=cap)
    seed_path = campaign / "seed.json"
    atomic_json(seed_path, check_seed(config["seed_profile"]), max_bytes=cap)
    entries = []
    for index, params in enumerate(config["cases"], 1):
        path = campaign / f"case-{index:02}.json"
        record = check_completed(*params, LIMITS)
        atomic_json(path, record, max_bytes=cap)
        entries.append({"record": path.name, "sha256_raw": sha(path), "parameters": record["parameters"],
                        "vertices": record["independent_certificate"]["n"], "bytes": path.stat().st_size})
    summary = {"run_id": config["run_id"], "status": "PASS", "completed_utc": utc_now(),
               "identity_sha256_raw": sha(campaign / "identity.json"),
               "seed_sha256_raw": sha(seed_path), "seed_certificate_count": 1,
               "completed_target_count": len(entries), "cases": entries}
    atomic_json(campaign / "summary.json", summary, max_bytes=cap)
    print(json.dumps({"status": "PASS", "completed_targets": len(entries), "auxiliary_seeds": 1,
                      "max_vertices": max(row["vertices"] for row in entries),
                      "max_case_bytes": max(row["bytes"] for row in entries)}))


if __name__ == "__main__":
    main()
