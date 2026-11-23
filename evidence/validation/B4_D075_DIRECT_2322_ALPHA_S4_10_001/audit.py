"""Reconstruct and audit the declared named originals without project imports."""

from time import process_time

START = process_time()

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(name):
    return json.loads((HERE / name).read_bytes())


def canonical_hash(value):
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def audit_graph(record, counts, spine_size):
    original = record["graph"]
    spine = [f"s:{i}" for i in range(spine_size)]
    parents = {spine[i]: spine[i-1] for i in range(1, spine_size)}
    roles = {name: {"kind": "spine", "section": i} for i, name in enumerate(spine)}
    for i, count in enumerate(counts):
        center = f"b:{i}:0"
        parents[center] = spine[i]
        roles[center] = {"kind": "branch", "section": i, "branch": 0}
        for j in range(count):
            terminal = f"l:{i}:0:{j}"
            parents[terminal] = center
            roles[terminal] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    profile = [[c] for c in counts] + [[] for _ in range(spine_size - len(counts))]
    edges = Counter(tuple(sorted(pair)) for pair in parents.items())
    assert Counter(original["vertices"]) == Counter(roles.keys())
    assert Counter(tuple(sorted(pair)) for pair in original["edges"]) == edges
    assert original["roles"] == roles and original["spine"] == spine
    assert original["profile"] == profile and original["schema_version"] == 1
    digest = canonical_hash({"vertices": sorted(roles), "edges": sorted(edges.elements()),
                             "roles": roles, "spine": spine, "profile": profile})
    assert digest == record["graph_digest"]
    return original, parents, digest


def audit_map(cert, original, parents, digest):
    labels = cert["labels"]
    assert set(labels) == set(original["vertices"])
    assert all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(len(parents)+1))
    diffs = {(v, u): abs(labels[v]-labels[u]) for v, u in parents.items()}
    assert sorted(diffs.values()) == list(range(1, len(parents)+1))
    assert cert["edges"] == [[u, v, abs(labels[u]-labels[v])] for u, v in original["edges"]]
    assert cert["graph_digest"] == digest
    assert cert["ledger_id"] == canonical_hash({"graph_digest": digest, "labels": sorted(labels.items())})
    checker = cert["checker"]
    assert checker["valid"] and checker["errors"] == [] and checker["graph_digest"] == digest
    assert checker["edge_differences"] == [w for _, _, w in cert["edges"]]
    assert checker["n"] == len(labels) and checker["m"] == len(parents)


def audit_controls():
    check = read("controls.json")
    original_path = "evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json"
    original_raw = (ROOT / original_path).read_bytes()
    original = json.loads(original_raw)
    controls = {
        "D066": "evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/certificates.json",
        "D070": "evidence/validation/B4_D069_ALT_ALPHA_FIRST_HOST_001/seed.json",
    }
    assert set(check) == controls.keys()
    for name, path in controls.items():
        retained = json.loads((ROOT / path).read_bytes())
        if name == "D066":
            retained = retained["prefix"]
        else:
            assert retained["original"] == {"path": original_path, "bytes": len(original_raw),
                                             "sha256": sha256(original_raw).hexdigest()}
        graph, parents, digest = audit_graph(original, (2, 2, 2, 2), 5)
        assert retained["graph_digest"] == digest and check[name]["labels"] == retained["labels"]
        assert all(check[name][key] == retained[key] for key in ("ledger_id", "checker"))
        audit_map(check[name], graph, parents, digest)
        assert retained["labels"]["s:4"] == 9
        assert all((retained["labels"][v] < 8) != (retained["labels"][u] < 8)
                   for v, u in parents.items())
    assert check["D066"]["graph_digest"] == check["D070"]["graph_digest"]
    assert check["D066"]["ledger_id"] != check["D070"]["ledger_id"]


def audit_success(result, original, parents, digest, config):
    bundle = read("certificates.json")
    seed = bundle["seed"]
    audit_map(seed, original, parents, digest)
    labels = seed["labels"]
    # Re-derive the constructive ledger from the chosen large/small bands.
    assert [labels[f"l:1:0:{j}"] for j in range(3)] == [0, 1, 2]
    assert labels["b:1:0"] == 17 and labels["s:1"] == 3 and labels["s:3"] == 8
    assert labels["b:3:0"] == 9 and [labels[f"l:3:0:{j}"] for j in range(2)] == [5, 6]
    assert labels["s:0"] + 2*labels["s:2"] == 47
    assert labels["s:2"] == 16 and labels["s:0"] == 15
    assert labels["b:0:0"] == 4 and labels["b:2:0"] == 7
    assert [labels[f"l:0:0:{j}"] for j in range(2)] == [11, 14]
    assert [labels[f"l:2:0:{j}"] for j in range(2)] == [12, 13]
    # Derive the unique parity classes from the parent topology and high exit.
    depth = {"s:0": 0}
    while len(depth) != len(labels):
        for v, parent in parents.items():
            if parent in depth:
                depth[v] = depth[parent]+1
    low = {v for v in depth if (depth[v]-depth["s:4"]) % 2}
    high = set(depth) - low
    assert sorted(labels[v] for v in low) == list(range(9))
    assert sorted(labels[v] for v in high) == list(range(9, 18))
    assert seed["alpha"] == {"low": sorted(low), "high": sorted(high), "low_size": 9}
    assert sorted(config["low_names"]) == sorted(low)
    assert labels["s:4"] == 10 and seed["physical_exit"] == {"name": "s:4", "label": 10}
    assert seed["entrance"] == {"name": "b:0:0", "label": 4}
    assert seed["optional_hosts"] == {
        v: {"actual": labels[v], "matches": labels[v] == proposed}
        for v, proposed in {"b:2:0": 0, "b:1:0": 9}.items()}
    witness = ["b:0:0"] + original["spine"]
    assert seed["witness_path"] == witness
    actual = Counter(tuple(sorted((u, v))) for u, v in parents.items())
    assert all(actual[tuple(sorted(edge))] == 1 for edge in zip(witness,witness[1:]))
    for v in labels:
        steps = 0
        while v not in witness:
            v = parents[v]
            steps += 1
        assert steps <= 2

    assert set(bundle["targets"]) == {"2", "5"}
    assert result["new_originals"] == result["new_positive_maps"] == 3
    for k, path_labels in ((2, [12, 10, 9]), (5, [15, 10, 13, 9, 11, 12])):
        graph, new_parents, target_digest = audit_graph(read(f"k{k}_original.json"), (2, 3, 2, 2), k+5)
        cert = bundle["targets"][str(k)]
        audit_map(cert, graph, new_parents, target_digest)
        assert {v: u for v, u in new_parents.items() if v in labels} == parents
        expected = {v: x+k*(v in high) for v, x in labels.items()}
        assert cert["assigned"] == expected
        used_d = sorted(abs(expected[v]-expected[u]) for v, u in parents.items())
        used_r = sorted(expected.values())
        partial = cert["suffix"]["partial"]
        m = len(new_parents)
        assert partial["used_labels"] == used_r and partial["used_differences"] == used_d
        assert used_r == list(range(9)) + list(range(k+9,k+18))
        assert used_d == list(range(k+1,k+18))
        assert partial["unused_labels"] == sorted(set(range(m+1)) - set(used_r)) == list(range(9, k+9))
        assert partial["unused_differences"] == sorted(set(range(1,m+1)) - set(used_d)) == list(range(1,k+1))
        path = graph["spine"][4:]
        assert set(new_parents) - set(parents) == set(path[1:])
        pending = Counter(tuple(sorted((v, u))) for v, u in new_parents.items() if v not in expected)
        assert pending == Counter(tuple(sorted(pair)) for pair in zip(path, path[1:]))
        assert Counter(tuple(sorted(e)) for e in cert["suffix"]["pending_edges"]) == pending
        assert cert["suffix"]["path"] == path and cert["suffix"]["crossing"] == [["s:4", "s:5"]]
        assert partial["valid"] and partial["frontier"] == ["s:4"] and partial["graph_digest"] == target_digest
        assert not partial["complete"] and partial["m"] == m and partial["n"] == m+1
        assert cert["path_labels"] == path_labels == [cert["labels"][v] for v in path]
        assert cert["labels"] == expected | dict(zip(path[1:], path_labels[1:]))
        assert cert["seed_ledger_id"] == seed["ledger_id"]
        assert cert["consumer_sha256"] == config["sources"]["research/B2_NONADJACENT_CONSUMER.md"]

    bad_digest = bundle["adverse"]["wrong_expected_digest"]
    assert bad_digest["expected"] == "0"*64 != digest
    assert bad_digest["report"] == seed["checker"] | {
        "valid": False, "errors": ["original graph digest mismatch"]}
    bad_suffix = bundle["adverse"]["wrong_suffix_inventory"]
    assert bad_suffix == {"valid": False, "declared_d": [1, 3],
                          "error": "residual difference inventory mismatch",
                          "graph_digest": bundle["targets"]["2"]["graph_digest"]}
    assert bad_suffix["declared_d"] != bundle["targets"]["2"]["suffix"]["partial"]["unused_differences"]
    assert result["negative_controls"] == 2


def main():
    if not __debug__ or sys.version_info[:2] not in ((3, 12), (3, 13)):
        raise RuntimeError("audit requires assertions and Python 3.12 or 3.13")
    cfg = read("config.json")
    for path, sha in cfg["sources"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == sha
    assert sha256(Path(sys.executable).read_bytes()).hexdigest() == cfg["runtime"]["sha256"]
    assert cfg["runtime"]["version"] == sys.version
    assert cfg["runtime"]["relative_executable"] == Path(sys.executable).relative_to(ROOT).as_posix()
    assert cfg["automatic_retries"] == cfg["historical_replays"] == 0
    assert cfg["limits"]["workers"] == 1
    assert cfg["limits"]["feasibility_invocations"] == cfg["limits"]["assignment_nodes"] == 0
    assert cfg["pin"] == {"s:4": 10}
    assert cfg["optional_host_tests"] == {"b:2:0": 0, "b:1:0": 9}
    assert cfg["limits"]["combined_process_cpu_seconds"] == 30
    assert cfg["limits"]["new_graphs"] == cfg["limits"]["new_maps"] == 3
    assert cfg["targets_on_success"] == [2, 5]
    original, parents, digest = audit_graph(read("prefix_original.json"), (2, 3, 2, 2), 5)
    result = read("run_result.json")
    assert result["historical_controls"] == 2 and result["status"] == "SUPPLIED"
    assert result["feasibility_invocations"] == result["assignment_nodes"] == 0
    assert not any(HERE.glob("query*.json"))
    audit_controls()
    audit_success(result, original, parents, digest, cfg)
    caps = cfg["limits"]
    total = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
    assert all(p.stat().st_size <= caps["bytes_per_record"] for p in HERE.iterdir() if p.is_file())
    audit_seconds = process_time() - START
    combined = result["process_cpu_seconds"] + cfg["freeze_process_cpu_seconds"] + audit_seconds
    assert combined <= caps["combined_process_cpu_seconds"]
    audit = {"status": "PASS", "supply_status": result["status"], "historical_controls": 2,
             "new_originals_rechecked": result["new_originals"], "new_audit_originals": 0,
             "negative_receipts_rechecked": result.get("negative_controls", 0),
             "witness_checked": result["status"] == "SUPPLIED", "search_calls": 0,
             "audit_process_cpu_seconds": audit_seconds, "combined_process_cpu_seconds": combined,
             "audited_raw_sha256": {p.name: sha256(p.read_bytes()).hexdigest()
                                    for p in HERE.glob("*.json")}}
    raw = (json.dumps(audit, sort_keys=True, indent=2) + "\n").encode()
    assert len(raw) <= caps["bytes_per_record"] and total + len(raw) <= caps["bytes_total"]
    with (HERE / "audit_result.json").open("xb") as stream:
        stream.write(raw)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
