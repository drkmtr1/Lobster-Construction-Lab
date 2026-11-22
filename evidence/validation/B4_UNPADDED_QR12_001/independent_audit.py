"""Independent standard-library arithmetic audit of saved QR12 certificates."""
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE / "campaign"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def edgeset(edges):
    return Counter(tuple(sorted(edge)) for edge in edges)


def reconstruct(profile):
    spine = [f"s:{i}" for i in range(len(profile))]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, section in enumerate(profile):
        for j, count in enumerate(section):
            center = f"b:{i}:{j}"
            edges.append((spine[i], center))
            roles[center] = {"kind": "branch", "section": i, "branch": j}
            for k in range(count):
                leaf = f"l:{i}:{j}:{k}"
                edges.append((center, leaf))
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
    return {"profile": profile, "spine": spine, "roles": roles, "vertices": sorted(roles),
            "edges": sorted(sorted(e) for e in edges)}


def assert_original(actual, theoretical):
    require(actual["profile"] == theoretical["profile"] and actual["spine"] == theoretical["spine"]
            and actual["roles"] == theoretical["roles"]
            and Counter(actual["vertices"]) == Counter(theoretical["vertices"])
            and edgeset(actual["edges"]) == edgeset(theoretical["edges"]), "original named graph")
    return hashlib.sha256(json.dumps(theoretical, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def cut_record(low, high):
    return {"low_class_size": len(low), "cutoff": len(low) - 1,
            "low_vertices": sorted(low), "high_vertices": sorted(high)}


def check_graceful(case, original, low, high):
    digest = assert_original(case["original_graph"], original)
    edges = original["edges"]
    labels = case["labels"] if "labels" in case else case["full_labels"]
    m = len(edges)
    require(len(original["vertices"]) == m + 1 and set(labels) == set(original["vertices"])
            and all(type(x) is int for x in labels.values())
            and sorted(labels.values()) == list(range(m + 1)), "full label bijection")
    require(sorted(abs(labels[u] - labels[v]) for u, v in edges) == list(range(1, m + 1)),
            "full original incidence differences")
    low_set, high_set = set(low), set(high)
    require(sorted(labels[v] for v in low_set) == list(range(len(low)))
            and sorted(labels[v] for v in high_set) == list(range(len(low), m + 1))
            and all((u in low_set) != (v in low_set) for u, v in edges)
            and case["alpha"] == cut_record(low_set, high_set), "completed alpha split")
    certificate = case["independent_certificate"]
    require(case["original_graph_digest"] == digest == certificate["graph_digest"]
            and certificate["valid"] and certificate["n"] == m + 1 and certificate["m"] == m
            and certificate["edge_differences"]
            == [abs(labels[u] - labels[v]) for u, v in case["original_graph"]["edges"]],
            "unchanged checker result identity")
    return digest


def rank_orders(q, r):
    # Physical vertices listed by increasing label in their normalized classes.
    low = ["s:1", "b:0:0", "l:3:0:0", "b:2:0"]
    low += [f"l:1:0:{j}" for j in range(r - 1, 1, -1)]
    low += ["l:1:0:0", "l:1:0:1", "l:3:0:1", "s:3"]
    high = ["s:4", "b:3:0", "b:1:0", "s:2", "l:2:0:0"]
    high += [f"l:0:0:{j}" for j in range(1, q)]
    high += ["l:0:0:0", "s:0"]
    return low, high


def audit_seed(record):
    original = reconstruct([[1], [2], [1], [2], []])
    low, high = rank_orders(1, 2)
    digest = check_graceful(record, original, low, high)
    historical = HERE.parents[2] / record["historical_source"]["path"]
    require(sha(historical) == record["historical_source"]["sha256_raw"]
            and load(historical)["solver_result"]["witness"] == record["labels"],
            "saved historical provenance")
    labels = record["labels"]
    require(labels == {v: i for i, v in enumerate(low + high)}, "exact normalized seed")
    W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
    edges = original["edges"]
    require(record["witness"] == W and len(set(W)) == len(W)
            and edgeset(zip(W, W[1:])) <= edgeset(edges)
            and record["ports"] == {"b:0:0": 1, "s:4": 8} and record["port_offsets"] == [1, 0],
            "actual W and port state")
    distances = {v: 0 for v in W}
    for level in (1, 2):
        layer = {v for e in edges if set(e).intersection(distances) for v in e} - distances.keys()
        distances.update(dict.fromkeys(layer, level))
    require(set(distances) == set(labels) and distances == record["witness_distances"]
            and distances["b:1:0"] == 1 and distances["b:0:0"] == 0,
            "host and witness distances")
    for entry, threshold, selected, expected, host in zip(
        record["predicates"], (4, 13), (set(low[:4]), set(high[-2:])),
        (list(range(7, 15)), list(range(12, 15))), ("b:1:0", "b:0:0"), strict=True,
    ):
        side = "below" if threshold == 4 else "at_or_above"
        incident = [e for e in edges if selected.intersection(e)]
        weights = sorted(abs(labels[u] - labels[v]) for u, v in incident)
        require(entry["threshold"] == threshold and entry["side"] == side and entry["host"] == host
                and entry["host_label"] == labels[host] and set(entry["selected_vertices"]) == selected
                and edgeset(i["edge"] for i in entry["incidences"]) == edgeset(incident)
                and all(abs(labels[i["edge"][0]] - labels[i["edge"][1]]) == i["difference"]
                        for i in entry["incidences"])
                and entry["difference_multiset"] == weights == expected, "complete seed predicate")
    return digest


def audit_case(case):
    q, r, K = (case["parameters"][key] for key in ("q", "r", "K"))
    original = reconstruct([[q], [r], [1], [2]] + [[] for _ in range(K + 1)])
    low, high = rank_orders(q, r)
    prefix = dict(zip(low, range(len(low))))
    prefix.update(dict(zip(high, range(len(low) + K, K + q + r + 12))))
    require(case["prefix_labels"] == prefix, "named prefix and class blocks")
    full = case["full_labels"]
    spine = original["spine"]
    path = spine[4:]
    pending = set(path[1:])
    tail = list(zip(path, path[1:]))
    actual = [e for e in original["edges"] if pending.intersection(e)]
    crossing = [e for e in actual if len(pending.intersection(e)) == 1]
    require(set(original["vertices"]) - prefix.keys() == pending
            and edgeset(actual) == edgeset(tail) == edgeset(case["suffix_edges"])
            and case["original_suffix"] == path
            and edgeset(crossing) == edgeset([("s:4", "s:5")]) == edgeset([case["crossing_edge"]]),
            "exact remaining original path and crossing")
    m = len(original["edges"])
    require(all(full[v] == x for v, x in prefix.items()), "prefix preservation")
    used = sorted(abs(prefix[u] - prefix[v]) for u, v in original["edges"] if not pending.intersection((u, v)))
    R = sorted(set(range(m + 1)) - set(prefix.values()))
    D = sorted(set(range(1, m + 1)) - set(used))
    require(R == list(range(len(low), len(low) + K)) and D == list(range(1, K + 1))
            and used == list(range(K + 1, m + 1)) and prefix["s:4"] == len(low) + K
            and case["interface"] == {"active_vertex": "s:4", "active_label": prefix["s:4"],
                                       "unused_labels": R, "unused_differences": D},
            "used spectrum, unused inventories and physical port")
    # Independently peel the two ends of R and follow the named path.
    steps = []
    for j, (u, v) in enumerate(tail):
        x = R[j // 2] if j % 2 == 0 else R[-1 - j // 2]
        difference = abs(full[u] - full[v])
        require(full[v] == x and difference == K - j, "suffix step or descending weight")
        steps.append({"operation": "next_spine", "parent": u, "vertex": v,
                      "label": x, "difference": difference})
    require(case["completion_trace"] == steps, "completion trace")
    digest = check_graceful(case, original, low + spine[5::2], high + spine[6::2])
    require(case["alpha"]["low_class_size"] == r + 6 + (K + 1) // 2, "alpha class size")
    return digest


def main():
    config = load(HERE / "config.json")
    limits = config["limits"]
    summary = load(RUN / "summary.json")
    identity = load(RUN / "identity.json")
    require(summary["run_id"] == identity["run_id"] == config["run_id"]
            and summary["status"] == "PASS" and summary["completed_target_count"] == len(summary["cases"]) == 12
            and summary["seed_certificate_count"] == 1
            and summary["identity_sha256_raw"] == sha(RUN / "identity.json")
            and summary["seed_sha256_raw"] == sha(RUN / "seed.json")
            and identity["config_sha256_raw"] == sha(HERE / "config.json")
            and identity["runner_sha256_raw"] == sha(HERE / "regression.py")
            and identity["audit_sha256_raw"] == sha(Path(__file__))
            and identity["limits"] == limits, "record identity")
    require(all(sha(HERE / "source" / name) == value
                for name, value in identity["source"]["files"].items()), "source snapshot identity")
    test = identity["focused_test"]
    require(sha(HERE / "source" / test["path"]) == test["sha256_raw"], "focused test identity")
    seed_digest = audit_seed(load(RUN / "seed.json"))
    rows = []
    for declared, row in zip(config["cases"], summary["cases"], strict=True):
        path = RUN / row["record"]
        require(sha(path) == row["sha256_raw"]
                and path.stat().st_size == row["bytes"] <= limits["max_result_bytes"], "case bytes")
        case = load(path)
        require(case["status"] == "PASS"
                and [case["parameters"][key] for key in config["parameter_order"]] == declared
                and case["parameters"] == row["parameters"] and row["vertices"] == sum(declared) + 12
                and row["vertices"] <= limits["max_vertices"], "case identity and cap")
        rows.append({"parameters": case["parameters"], "original_graph_digest": audit_case(case),
                     "case_sha256_raw": row["sha256_raw"], "status": "PASS"})
    result = {"status": "PASS", "run_id": config["run_id"] + "-audit",
              "campaign_sha256_raw": sha(RUN / "summary.json"), "same_certificate_count": len(rows),
              "additional_completed_targets": 0, "same_auxiliary_seed_graph_digest": seed_digest,
              "additional_seed_certificates": 0, "cases": rows}
    data = (json.dumps(result, indent=2) + "\n").encode()
    require(len(data) <= limits["max_result_bytes"], "audit output cap")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(data)
    print(f"PASS: audited {len(rows)} saved targets and the same auxiliary base; zero added targets")


if __name__ == "__main__":
    main()
