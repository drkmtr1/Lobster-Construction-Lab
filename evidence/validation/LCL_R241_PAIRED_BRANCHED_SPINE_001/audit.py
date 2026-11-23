"""Independent original-topology and closed-form arithmetic audit. Standard library only."""

from time import process_time

START = process_time()

from collections import deque
from hashlib import sha256
from itertools import chain
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

GRID = [
    ("T1", (1,), 2),
    ("T2", (2, 3), 2),
    ("T3", (1, 3, 2), 2),
    ("T4", (2, 3, 2, 2), 2),
    ("T5", (2, 3, 2, 2), 3),
    ("T6", (2, 3, 1, 4, 2), 2),
    ("T7", (2, 4, 1, 3, 5, 2), 3),
    ("T8", (7, 1, 2, 4, 3, 1, 5), 5),
    ("T9", (0, 2, 3, 0, 1, 4, 0, 5), 4),
]


def read(path):
    return json.loads((HERE / path).read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical_hash(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def bind_topology(record, quotas, L):
    graph = record["graph"]
    n = len(quotas)
    spine = [f"s:{i}" for i in range(n+L)]
    batch_sizes = [([a] if i < n else []) for i, a in enumerate((*quotas, *([0]*L)))]
    roles = {}
    ordered_edges = list(zip(spine, spine[1:]))
    for i, root in enumerate(spine):
        roles[root] = {"kind": "spine", "section": i}
        if i >= n:
            continue
        hub = f"b:{i}:0"
        roles[hub] = {"kind": "branch", "section": i, "branch": 0}
        ordered_edges.append((root, hub))
        leaves = [f"l:{i}:0:{j}" for j in range(quotas[i])]
        ordered_edges.extend(zip([hub]*len(leaves), leaves))
        for j, leaf in enumerate(leaves):
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    assert graph["schema_version"] == 1 and graph["profile"] == batch_sizes
    assert graph["spine"] == spine and graph["vertices"] == list(roles)
    assert graph["roles"] == roles and graph["edges"] == [list(edge) for edge in ordered_edges]
    N = sum(quotas) + 2*n
    assert len(roles) == N+L and len(ordered_edges) == N+L-1
    assert len(set(roles)) == len(roles)
    assert len({frozenset(pair) for pair in ordered_edges}) == len(ordered_edges)
    parent = dict((v, u) for u, v in ordered_edges)
    assert len(parent) == len(roles)-1 and spine[0] not in parent
    for name in roles:
        while name != spine[0]:
            name = parent[name]
    digest = canonical_hash({"vertices": sorted(roles), "edges": sorted(sorted(e) for e in ordered_edges),
                             "profile": batch_sizes, "spine": spine, "roles": roles})
    assert digest == record["graph_digest"]
    return roles, spine, ordered_edges, N, digest


def ledger_id(digest, labels):
    return canonical_hash({"graph_digest": digest, "labels": sorted(labels.items())})


def rows_for(edges, labels):
    return [[u, v, abs(labels[u]-labels[v])] for u, v in edges
            if u in labels and v in labels]


def distance_to_path(path, rows):
    adjacent = {}
    for u, v, _ in rows:
        adjacent.setdefault(u, []).append(v)
        adjacent.setdefault(v, []).append(u)
    distance = dict.fromkeys(path, 0)
    queue = deque(path)
    while queue:
        u = queue.popleft()
        for v in adjacent[u]:
            if v not in distance:
                distance[v] = distance[u]+1
                queue.append(v)
    assert all(b in adjacent[a] for a, b in zip(path, path[1:]))
    return distance


def module_alphabet(quotas, start, stop, roles):
    # Read off local ranks by role, without using producer functions.
    labels = {}
    for name, role in roles.items():
        i = role["section"]
        if not start <= i < stop:
            continue
        kind = role["kind"]
        if stop-start == 1:
            if kind == "branch":
                labels[name] = 0
            elif kind == "spine":
                labels[name] = 2
            else:
                j = role["leaf"]
                labels[name] = 1 if j == 0 else j+2
        elif i == start:
            labels[name] = {"spine": 1, "branch": quotas[start]+2,
                            "leaf": 2+role.get("leaf", 0)}[kind]
        else:
            labels[name] = {"spine": quotas[start]+3, "branch": 0,
                            "leaf": quotas[start]+4+role.get("leaf", 0)}[kind]
    return labels


def audit_state(record, expected, P, walk, edges):
    assert record["labels"] == expected
    assert all(type(a) is int for a in record["labels"].values())
    assert sorted(record["labels"].values()) == list(range(len(expected)))
    rows = rows_for(edges, expected)
    assert record["edge_rows"] == rows
    d = sorted(w for _, _, w in rows)
    assert d == list(range(1, len(expected)))
    assert all((expected[u] < P) != (expected[v] < P) for u, v, _ in rows)
    assert record["N"] == len(expected) and record["P"] == P
    assert record["low"] == sorted(v for v in expected if expected[v] < P)
    assert record["high"] == sorted(v for v in expected if expected[v] >= P)
    assert len(record["low"]) == P
    assert [record["entrance"], record["exit"]] == [walk[0], walk[-1]]
    assert [record["entrance_label"], record["exit_label"]] == [expected[walk[0]], P+1]
    assert [record["x"], record["y"]] == [expected[walk[0]], 1]
    assert len(set(walk)) == len(walk) and record["witness"] == walk
    distance = distance_to_path(walk, rows)
    assert distance.keys() == expected.keys() and max(distance.values()) <= 2
    assert record["distance"] == distance


def audit_trace(record, quotas, roles, spine, edges):
    n = len(quotas)
    stops = list(range(1 if n % 2 else 2, n+1, 2))
    starts = [0, *stops[:-1]]
    trace = record["trace"]
    assert len(trace) == len(stops)
    blocks = []
    total_low = 0
    for step, (row, start, stop) in enumerate(zip(trace, starts, stops, strict=True)):
        local = module_alphabet(quotas, start, stop, roles)
        p = 1 if stop-start == 1 else quotas[start]+2
        walk = (["b:0:0", "s:0"] if stop-start == 1 else spine[start:stop])
        audit_state(row["module"], local, p, walk, edges)
        blocks.append((local, p, walk))
        previous_low = total_low
        total_low += p

        # Closed form for all labels at this step: preceding low sizes
        # offset this block, while later orders offset only its highs.
        final = {}
        front = 0
        for i, (labels, low_size, _) in enumerate(blocks):
            back = sum(len(later) for later, _, _ in blocks[i+1:])
            for v, local_rank in labels.items():
                final[v] = local_rank + front + (0 if local_rank < low_size else back)
            front += low_size
        witness = list(chain.from_iterable(block_walk for _, _, block_walk in blocks))
        assert set(final) == {v for v, meta in roles.items() if meta["section"] < stop}
        audit_state(row["aggregate"], final, total_low, witness, edges)
        if step == 0:
            assert row["connector"] is None
        else:
            u, v = spine[start-1:start+1]
            old = trace[step-1]["aggregate"]["labels"]
            crosses = [(a, b) for a, b in edges
                       if (a in old and b in local) or (b in old and a in local)]
            assert crosses == [(u, v)]
            assert row["connector"] == {
                "edge": [u, v], "matched_offset": 1, "weight": len(local),
                "previous_exit_before": previous_low+1, "incoming_before": 1,
                "previous_exit_after": previous_low+1+len(local), "incoming_after": previous_low+1,
                "previous_low_size": previous_low, "module_order": len(local)}
            assert final[u]-final[v] == len(local)
    expected_P = ((1 + sum(a+2 for a in quotas[1::2])) if n % 2
                  else sum(a+2 for a in quotas[::2]))
    assert total_low == expected_P
    return final, total_low


def audit_certificate(case, original, record, quotas, L):
    roles, spine, edges, N, digest = bind_topology(original, quotas, L)
    normalized, P = audit_trace(record, quotas, roles, spine, edges)
    assert len(normalized) == N
    shifted = {v: (x if x < P else x+L) for v, x in normalized.items()}
    assert shifted == record["shifted"]
    m = N+L-1
    used_r = sorted(shifted.values())
    used_d = sorted(w for _, _, w in rows_for(edges, shifted))
    assert used_r == list(range(P)) + list(range(P+L, m+1))
    assert used_d == list(range(L+1, m+1))
    R = sorted(set(range(m+1)) - set(used_r))
    D = sorted(set(range(1, m+1)) - set(used_d))
    assert R == list(range(P, P+L)) and D == list(range(1, L+1))
    path = spine[len(quotas)-1:]
    pending = [(u, v) for u, v in edges if {u, v} - shifted.keys()]
    assert pending == list(zip(path, path[1:]))
    assert set(roles) - shifted.keys() == set(path[1:])
    suffix = record["suffix"]
    assert suffix["path"] == path and suffix["pending_edges"] == [list(edge) for edge in pending]
    assert suffix["crossing"] == [[u, v] for u, v in pending if (u in shifted) != (v in shifted)] == [path[:2]]
    assert suffix["port"] == [path[0], P+L+1]
    partial = suffix["partial"]
    assert partial["valid"] and not partial["complete"] and partial["errors"] == []
    assert partial["graph_digest"] == digest and (partial["n"], partial["m"]) == (m+1, m)
    assert partial["frontier"] == [path[0]]
    assert (partial["used_labels"], partial["used_differences"]) == (used_r, used_d)
    assert (partial["unused_labels"], partial["unused_differences"]) == (R, D)

    # Independent fixed-grid arithmetic. L=5 reflects C2 to (0,2,3).
    expected_sequences = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3),
                          5: (6, 1, 4, 0, 2, 3)}
    sequence = [P+a for a in expected_sequences[L]]
    assert record["sequence"] == sequence and shifted[path[0]] == sequence[0]
    assert sorted(sequence[1:]) == R
    assert sorted(abs(b-a) for a, b in zip(sequence, sequence[1:])) == D
    expected = shifted | dict(zip(path[1:], sequence[1:], strict=True))
    assert record["labels"] == expected and all(type(x) is int for x in record["labels"].values())
    assert sorted(expected.values()) == list(range(m+1))
    rows = rows_for(edges, expected)
    assert record["edge_rows"] == rows and sorted(w for _, _, w in rows) == list(range(1, m+1))
    assert record["graph_digest"] == digest and record["ledger_id"] == ledger_id(digest, expected)
    verified = record["checker"]
    assert verified["valid"] and verified["errors"] == []
    assert verified["graph_digest"] == digest and (verified["n"], verified["m"]) == (m+1, m)
    assert verified["edge_differences"] == [w for _, _, w in rows]
    return {"case": case, "n": m+1, "m": m, "P": P, "port": suffix["port"], "R": R, "D": D,
            "graph_digest": digest, "ledger_id": record["ledger_id"], "joins": len(record["trace"])-1}


def audit_adverse(t4, original):
    tests = read("adverse.json")
    assert set(tests) == {"connector", "port", "differences"}
    bad = tests["connector"]
    graph = original["graph"]
    removed, substituted = bad["removed"], bad["substituted"]
    assert removed == ["s:1", "s:2"] and substituted == ["s:0", "s:2"]
    assert removed in graph["edges"] and substituted not in graph["edges"]
    edges = [substituted if e == removed else e for e in graph["edges"]]
    digest = canonical_hash({"vertices": sorted(graph["vertices"]), "edges": sorted(sorted(e) for e in edges),
                             "profile": graph["profile"], "spine": graph["spine"], "roles": graph["roles"]})
    assert bad["expected_graph_digest"] == t4["graph_digest"] != digest
    receipt = bad["checker"]
    assert receipt["graph_digest"] == digest and not receipt["valid"]
    assert {"actual named edges do not match the original profile",
            "original graph digest mismatch"} <= set(receipt["errors"])
    assert tests["port"] == {"exit": "s:1", "incoming": "s:2", "swapped_with": "b:3:0",
                             "y_B": 1, "x_A": 0, "reason": "R241 offset mismatch", "rejected": True}
    assert t4["trace"][0]["aggregate"]["y"] == 1 and t4["trace"][1]["module"]["labels"]["b:3:0"] == 0
    assert tests["differences"] == {"declared": [2], "actual": t4["suffix"]["partial"]["unused_differences"],
                                    "reason": "exact suffix difference inventory", "rejected": True}


def main():
    if not __debug__:
        raise RuntimeError("Audit requires assertions")
    config = read("config.json")
    assert [(i, tuple(a), L) for i, a, L in config["grid"]] == GRID
    assert config["limits"] == {"workers": 1, "full_targets": 9, "adverse": 3, "process_cpu_seconds": 30,
                                "bytes_per_file": 2_000_000, "bytes_total": 10_000_000, "search_calls": 0,
                                "assignment_nodes": 0, "replays": 0, "retries": 0}
    identity = read("identity.json")
    assert identity["strategy_parent"] == config["strategy_parent"]
    for path, digest in identity["raw_sources"].items():
        assert raw_hash(ROOT / path) == digest
    for name in ("task", "roadmap"):
        entry = config["documents"][name]
        assert entry["sha256"] == identity["raw_sources"][entry["path"]]
    assert identity["runtime"] == {"sha256": raw_hash(Path(sys.executable)), "version": sys.version,
                                    "path": Path(sys.executable).relative_to(ROOT).as_posix()}

    result = read("result.json")
    summary = []
    for case, quotas, L in GRID:
        assert result["process_cpu_seconds"] + process_time()-START < 29, "audit CPU reserve"
        record = read(f"{case}_certificate.json")
        reference = record["original"]
        path = ROOT / reference["path"]
        retained = config["retained"]
        if case == "T5":
            assert reference["path"] == retained["original"] and not (HERE/"T5_original.json").exists()
            old = read(ROOT / retained["certificates"])["targets"]["2"]
            assert old["graph_digest"] == record["graph_digest"]
            assert ledger_id(record["graph_digest"], old["labels"]) == old["ledger_id"]
            assert old["ledger_id"] != record["ledger_id"]
            assert record["retained_co_original"] == {"ledger_id": old["ledger_id"], "source": retained["certificates"]}
            members = {row["path"]: row["sha256"] for row in read(ROOT / retained["manifest"])["files"]}
            for source in (path, ROOT / retained["certificates"]):
                assert raw_hash(source) == members[source.name]
        elif case == "T4":
            assert reference["path"] == retained["t4_original"] and not (HERE/"T4_original.json").exists()
            members = read(ROOT / retained["t4_manifest"])["files"]
            assert raw_hash(path) == members["validation/lift-t2-original.json"]["sha256"]
        else:
            assert path == HERE / f"{case}_original.json"
        assert raw_hash(path) == reference["sha256"]
        original = read(path)
        summary.append(audit_certificate(case, original, record, quotas, L))
        if case == "T4":
            spine_labels = [1, 15, 5, 11, 9, 8]
            exemplar = dict(zip(original["graph"]["spine"], spine_labels, strict=True))
            for i, group in enumerate(((14, 2, 3), (0, 16, 17, 18), (10, 6, 7), (4, 12, 13))):
                exemplar[f"b:{i}:0"] = group[0]
                exemplar.update({f"l:{i}:0:{j}": x for j, x in enumerate(group[1:])})
            assert record["labels"] == exemplar
            audit_adverse(record, original)

    assert len({row["graph_digest"] for row in summary}) == 9
    assert len(list(HERE.glob("T*_original.json"))) == 7
    assert len(list(HERE.glob("T*_certificate.json"))) == 9
    assert result == {"status": "PASS", "complete_certificates": 9, "new_originals": 7,
                      "retained_originals": 2, "adverse": 3, "search_calls": 0,
                      "assignment_nodes": 0, "historical_replays": 0,
                      "process_cpu_seconds": result["process_cpu_seconds"]}
    files = list(HERE.glob("*.json"))
    elapsed = process_time()-START
    total_cpu = elapsed + result["process_cpu_seconds"]
    assert total_cpu < config["limits"]["process_cpu_seconds"]
    out = {"status": "PASS", "cases": summary, "full_certificates": 9, "new_audit_originals": 0,
           "adverse_receipts": 3, "audit_process_cpu_seconds": elapsed,
           "producer_and_audit_cpu_seconds": total_cpu,
           "raw_receipts": {f.name: raw_hash(f) for f in sorted(files)}}
    raw = (json.dumps(out, indent=2, sort_keys=True) + "\n").encode()
    assert len(raw) <= 2_000_000 and sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) + len(raw) <= 10_000_000
    with (HERE / "audit_result.json").open("xb") as stream:
        stream.write(raw)


if __name__ == "__main__":
    main()
