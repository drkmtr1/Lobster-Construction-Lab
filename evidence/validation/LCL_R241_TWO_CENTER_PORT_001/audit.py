"""Audit the originals and saved enumeration receipts without project imports."""

from time import process_time

START = process_time()

from collections import Counter
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROFILES = {"small": [[1, 1], [1]], "neighbor": [[1, 1], [2]]}
CASES = [
    ("small_strict", "small", {"s:0": 1, "s:1": 5}, 36),
    ("small_orientation", "small", {}, 576),
    ("neighbor_strict", "neighbor", {"s:0": 1, "s:1": 5}, 144),
]
EXPECTED = {"small_strict": 0, "small_orientation": 4, "neighbor_strict": 4}


def read(path):
    return json.loads((HERE / path).read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical_hash(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode()).hexdigest()


def check_original(original, profile):
    # Independently generate each named child's parent and its depth from s:0.
    graph = original["graph"]
    assert graph["schema_version"] == 1 and graph["profile"] == profile
    spine = ["s:0", "s:1"]
    assert graph["spine"] == spine
    parents = {"s:1": "s:0"}
    roles = {}
    for i, counts in enumerate(profile):
        source = spine[i]
        roles[source] = {"kind": "spine", "section": i}
        for j, size in enumerate(counts):
            b = f"b:{i}:{j}"
            roles[b] = {"kind": "branch", "section": i, "branch": j}
            parents[b] = source
            for k in range(size):
                leaf = f"l:{i}:{j}:{k}"
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
                parents[leaf] = b
    assert Counter(graph["vertices"]) == Counter(roles.keys()) and graph["roles"] == roles
    expected_edges = Counter(tuple(sorted(e)) for e in parents.items())
    assert Counter(tuple(sorted(e)) for e in graph["edges"]) == expected_edges
    assert len(graph["edges"]) == len(roles)-1 and all(v == 1 for v in expected_edges.values())
    assert graph["edges"] == [[p, child] for child, p in parents.items()]
    assert graph["vertices"] == list(roles)
    digest = canonical_hash({"vertices": sorted(roles), "edges": sorted(expected_edges.elements()),
                             "roles": roles, "spine": spine, "profile": profile})
    assert digest == original["graph_digest"]
    classes = [[], []]
    for name in roles:
        cursor = name
        depth = 0
        while cursor != "s:0":
            cursor = parents[cursor]
            depth += 1
        classes[depth % 2].append(name)
        assert depth - int(roles[name]["section"] == 1) <= 2
    assert original["classes"] == classes
    assert len(classes[0]) == 4 and "s:1" in classes[1]
    return digest, classes, graph["edges"]


def permutation_rank(row, alphabet):
    assert len(row) == len(alphabet) and all(type(x) is int for x in row)
    unused = list(alphabet)
    rank = 0
    for value in row:
        index = unused.index(value)
        rank = rank*len(unused) + index
        unused.pop(index)
    return rank


def weight(edge, labels):
    u, v = edge
    return abs(labels[u]-labels[v])


def positive_weights(edges, labels):
    weights = [weight(edge, labels) for edge in edges]
    assert sorted(weights) == list(range(1, len(edges)+1))
    return weights


def check_rows(case, original, control_labels, producer_cpu):
    name, graph_id, pins, limit = case
    digest, classes, edges = original
    p = len(classes[0])
    raw = read(f"{name}.json")
    assert raw["graph_id"] == graph_id and raw["graph_digest"] == digest and raw["pins"] == pins
    assert raw["status"] == "COMPLETE" and raw["visited"] == len(raw["rows"]) == limit
    names = [[v for v in cls if v not in pins] for cls in classes]
    values = [sorted(set(band) - set(pins.values())) for band in (range(p), range(p, len(edges)+1))]
    assert raw["free_names"] == names and raw["free_labels"] == values
    location = {v: (cls, index) for cls, free in enumerate(names) for index, v in enumerate(free)}
    high_count = factorial(len(values[1]))
    assert factorial(len(values[0])) * high_count == limit
    ranks = set()
    ports = Counter()
    witnessed = False
    for lo, hi, repeat in raw["rows"]:
        assert producer_cpu + process_time()-START < 29, "audit CPU reserve"
        rank = permutation_rank(lo, values[0])*high_count + permutation_rank(hi, values[1])
        assert rank not in ranks
        ranks.add(rank)
        if repeat is None:
            labels = pins | dict(zip(names[0], lo, strict=True)) | dict(zip(names[1], hi, strict=True))
            positive_weights(edges, labels)
            ports[(labels["s:0"], labels["s:1"]-p)] += 1
            witnessed |= labels == control_labels
        else:
            i, j, d = repeat
            assert all(type(index) is int for index in repeat)
            assert 0 <= i < j < len(edges)
            endpoints = set(edges[i] + edges[j])
            labels = {v: pins[v] for v in endpoints & pins.keys()}
            for v in endpoints - pins.keys():
                cls, index = location[v]
                labels[v] = (lo, hi)[cls][index]
            assert weight(edges[i], labels) == weight(edges[j], labels) == d
    assert ranks == set(range(limit))
    assert raw["positive"] == sum(ports.values())
    assert witnessed == (name != "small_strict")
    port_rows = [[x, y, count] for (x, y), count in sorted(ports.items())]
    assert raw["port_histogram"] == port_rows
    return {"visits": limit, "positive": sum(ports.values()), "port_histogram": port_rows,
            "negative_receipts": limit-sum(ports.values())}


def check_control(record, labels, original):
    digest, classes, edges = original
    p = len(classes[0])
    assert record["labels"] == labels and all(type(a) is int for a in labels.values())
    assert set(labels) == {v for cls in classes for v in cls}
    assert sorted(labels[v] for v in classes[0]) == list(range(p))
    assert sorted(labels[v] for v in classes[1]) == list(range(p, len(labels)))
    assert all((labels[u] < p) != (labels[v] < p) for u, v in edges)
    weights = positive_weights(edges, labels)
    assert record["edge_rows"] == [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)]
    assert record["graph_digest"] == digest
    assert record["ledger_id"] == canonical_hash({"graph_digest": digest, "labels": sorted(labels.items())})
    assert record["witness"] == record["physical_ports"] == ["s:0", "s:1"]
    assert record["low_size"] == p and record["offsets"] == [labels["s:0"], labels["s:1"]-p]
    production = record["checker"]
    assert production["valid"] and production["errors"] == [] and production["graph_digest"] == digest
    assert (production["n"], production["m"]) == (len(labels), len(edges))
    assert production["edge_differences"] == weights


def main():
    if not __debug__:
        raise RuntimeError("Audit requires assertions")
    config = read("config.json")
    assert config["profiles"] == PROFILES and [tuple(case) for case in config["cases"]] == CASES
    assert config["limits"] == {"workers": 1, "assignments": 800, "combined_process_cpu_seconds": 30,
                                "bytes_per_record": 2_000_000, "bytes_total": 6_000_000,
                                "solver_calls": 0, "retries": 0, "history_replays": 0}
    identity = read("identity.json")
    assert identity["parent"] == config["parent"]
    for path, digest in identity["sources"].items():
        assert raw_hash(ROOT / path) == digest
    packet = config["authorization"]
    assert identity["sources"][packet["path"]] == packet["sha256"]
    assert identity["runtime"] == {"python": sys.version,
                                   "path": Path(sys.executable).relative_to(ROOT).as_posix(),
                                   "sha256": raw_hash(Path(sys.executable))}
    originals = {key: check_original(read(f"{key}_original.json"), profile)
                 for key, profile in PROFILES.items()}
    assert len({value[0] for value in originals.values()}) == 2

    bundle = read("certificates.json")
    controls = bundle["positive_controls"]
    assert set(controls) == set(originals)
    for key, original in originals.items():
        check_control(controls[key], config["controls"][key], original)
    assert controls["small"]["offsets"] == [1, 0] and controls["neighbor"]["offsets"] == [1, 1]
    adverse = bundle["adverse"]
    assert adverse["expected_digest"] == "0"*64 != originals["small"][0]
    assert adverse["checker"] == controls["small"]["checker"] | {
        "valid": False, "errors": ["original graph digest mismatch"]}
    assert adverse["offset"] == {"valid": False, "reason": "R241 requires y_B=x_A at the actual ports",
                                "y_B": 0, "x_A": 1, "U_B": ["small", "s:1"], "L_A": ["neighbor", "s:0"]}

    result = read("result.json")
    pcpu = result["producer_process_cpu_seconds"]
    summary = {case[0]: check_rows(case, originals[case[1]], controls[case[1]]["labels"], pcpu)
               for case in CASES}
    total = sum(row["visits"] for row in summary.values())
    counts = {key: {k: row[k] for k in ("visits", "positive")} for key, row in summary.items()}
    assert total == 756 <= config["limits"]["assignments"]
    assert result == {"status": "COMPLETE", "assignments": total, "counts": counts, "originals": 2,
                      "positive_controls": 2, "adverse_controls": 2, "solver_calls": 0, "replays": 0,
                      "producer_process_cpu_seconds": pcpu}
    observed = {key: row["positive"] for key, row in summary.items()}
    elapsed = process_time()-START
    assert pcpu + elapsed < config["limits"]["combined_process_cpu_seconds"]
    record = {"status": "PASS", "producer_and_audit_cpu_seconds": pcpu + elapsed,
              "audit_cpu_seconds": elapsed, "audited_cases": summary,
              "expected_counts": EXPECTED, "observed_matches_expected": observed == EXPECTED,
              "rank_and_falsifier_checks": total, "new_enumerated_assignments": 0,
              "raw_receipts": {p.name: raw_hash(p) for p in sorted(HERE.glob("*.json"))}}
    raw = (json.dumps(record, sort_keys=True, indent=2) + "\n").encode()
    assert len(raw) <= 2_000_000 and sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(raw) <= 6_000_000
    with (HERE / "audit_result.json").open("xb") as stream:
        stream.write(raw)


if __name__ == "__main__":
    main()
