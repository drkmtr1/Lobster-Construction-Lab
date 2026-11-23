"""Independent audit of the seven certificates and stored diagnostic visits."""

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
PROFILE_B = [[1, 1], [1]]
R21 = [[1, 2], [2], [1], [2]]
R32 = [[1, 3], [3], [2], [3]]
PROFILES = {"unequal": [[1, 2], [1]], "f0": [[1, 0], [0]], "f2": [[1, 2], [2]],
            "f4": [[1, 4], [4]], "r21": R21, "r32": R32, "repeat_l5": R21+R32+[[] for _ in range(5)]}
DECLARED = [["unequal_strict","unequal",1,144,0], ["unequal_alternate","unequal",2,144,2],
            ["neighbor_strict","f2",1,576,4]]


def read(path):
    return json.loads((HERE / path).read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical_hash(obj):
    return sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode()).hexdigest()


def topology(record, profile):
    graph = record["graph"]
    spine = [f"s:{i}" for i in range(len(profile))]
    parents = dict(zip(spine[1:], spine[:-1], strict=True))
    roles = {}
    for i, quotas in enumerate(profile):
        roles[spine[i]] = {"kind": "spine", "section": i}
        for j, quota in enumerate(quotas):
            b = f"b:{i}:{j}"
            parents[b] = spine[i]
            roles[b] = {"kind": "branch", "section": i, "branch": j}
            for k in range(quota):
                leaf = f"l:{i}:{j}:{k}"
                parents[leaf] = b
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": k}
    edges = [[p, child] for child, p in parents.items()]
    assert Counter(tuple(sorted(edge)) for edge in graph["edges"]) == Counter(
        tuple(sorted(edge)) for edge in edges)
    assert graph["edges"] == edges and graph["vertices"] == list(roles)
    assert graph["roles"] == roles and graph["schema_version"] == 1
    assert graph["spine"] == spine and graph["profile"] == profile
    assert len(edges)+1 == len(roles)
    # Every name has the correct path to its physical section.
    for v, role in roles.items():
        u = v
        distance = 0
        while u not in spine:
            u = parents[u]
            distance += 1
        assert u == spine[role["section"]]
        assert distance == {"spine": 0, "branch": 1, "leaf": 2}[role["kind"]]
    digest = canonical_hash({"vertices": sorted(roles), "edges": sorted(sorted(e) for e in edges),
                             "roles": roles, "spine": spine, "profile": profile})
    assert record["graph_digest"] == digest
    return {"digest": digest, "spine": spine, "edges": edges, "roles": roles}


def weights(original, labels):
    return [[u, v, abs(labels[u]-labels[v])] for u, v in original["edges"]
            if u in labels and v in labels]


def normalized(original, record, labels, p, witness):
    n = len(labels)
    assert record["labels"] == labels and all(type(v) is int for v in record["labels"].values())
    assert sorted(labels.values()) == list(range(n))
    rows = weights(original, labels)
    assert record["edge_rows"] == rows and sorted(w for _, _, w in rows) == list(range(1, n))
    assert all((labels[u] < p) != (labels[v] < p) for u, v, _ in rows)
    assert record["low"] == sorted(u for u, x in labels.items() if x < p)
    assert record["high"] == sorted(u for u, x in labels.items() if x >= p)
    assert record["N"] == n and record["P"] == len(record["low"]) == p
    indices = [original["spine"].index(v) for v in witness]
    assert indices == list(range(indices[0], indices[-1]+1))
    assert set(labels) == {v for v, role in original["roles"].items() if role["section"] in indices}
    assert record["witness"] == witness and record["ports"] == [witness[0], witness[-1]]
    x, y = labels[witness[0]], labels[witness[-1]]-p
    assert 0 <= x < p and 0 <= y < n-p
    assert record["offsets"] == [x, y] and record["port_labels"] == [x, p+y]


def check_certificate(original, record, labels):
    assert record["labels"] == labels and all(type(v) is int for v in record["labels"].values())
    assert set(labels) == set(original["roles"]) and sorted(labels.values()) == list(range(len(labels)))
    rows = weights(original, labels)
    assert record["edge_rows"] == rows
    assert sorted(w for _, _, w in rows) == list(range(1, len(labels)))
    digest = original["digest"]
    assert record["graph_digest"] == digest
    assert record["ledger_id"] == canonical_hash({"graph_digest": digest, "labels": sorted(labels.items())})
    checker = record["checker"]
    assert checker["valid"] and checker["errors"] == [] and checker["graph_digest"] == digest
    assert (checker["n"], checker["m"]) == (len(labels), len(rows))
    assert checker["edge_differences"] == [w for _, _, w in rows]


def bridge(a, i):
    roots = [f"s:{i}", f"s:{i+1}"]
    centers = [f"b:{i}:0", f"b:{i+1}:0"]
    labels = dict(zip(roots + centers, (0, a+3, 2*a+4, a+1), strict=True))
    assignments = (range(1, a+1), [a+2, *range(a+4, 2*a+4)])
    for section, leaf_alphabet in enumerate(assignments, i):
        for j, value in enumerate(leaf_alphabet):
            labels[f"l:{section}:0:{j}"] = value
    return labels


def first_pair(b, i, roles):
    fixed = {f"s:{i}": 1, f"s:{i+1}": b+3, f"b:{i}:0": 2*b+5, f"b:{i}:1": 2*b+4,
             f"b:{i+1}:0": b+2, f"l:{i}:0:0": 0}
    result = {}
    for name, role in roles.items():
        section = role["section"]
        if section not in (i, i+1):
            continue
        if name in fixed:
            result[name] = fixed[name]
        elif section == i:
            assert role["kind"] == "leaf" and role["branch"] == 1
            result[name] = 2+role["leaf"]
        else:
            assert role["kind"] == "leaf" and role["branch"] == 0
            result[name] = b+4+role["leaf"]
    return result


def closed_form(blocks):
    out = {}
    front = 0
    for i, (local, low_size, _) in enumerate(blocks):
        back = sum(len(labels) for labels, _, _ in blocks[i+1:])
        for v, a in local.items():
            assert v not in out
            out[v] = a + front + back*int(a >= low_size)
        front += low_size
    return out


def audit_join(original, receipt, B, A, combined):
    old, p, old_spine = B
    new, q, new_spine = A
    n = len(new)
    u, v = old_spine[-1], new_spine[0]
    crossings = [[x, y] for x, y in original["edges"]
                 if (x in old and y in new) or (y in old and x in new)]
    assert not old.keys() & new.keys() and crossings == [[u, v]]
    y, x = old[u]-p, new[v]
    assert y == x
    assert combined[u] == old[u]+n and combined[v] == x+p
    assert combined[u]-combined[v] == n
    assert receipt == {"connector": [u, v], "old_block_order": len(old), "new_block_order": n,
                       "old_low_size": p, "new_low_size": q, "old_exit_offset": y,
                       "new_entrance_offset": x, "old_exit_before": old[u], "new_entrance_before": x,
                       "old_exit_after": combined[u], "new_entrance_after": combined[v],
                       "connector_weight": n}
    old_rows = weights(original, {v: combined[v] for v in old})
    new_rows = weights(original, {v: combined[v] for v in new})
    assert sorted(w for _, _, w in old_rows) == list(range(n+1, n+len(old)))
    assert sorted(w for _, _, w in new_rows) == list(range(1, n))


def audit_macros(original, record, quota_list, L):
    macro_parts = []
    spine = original["spine"]
    assert len(record["macros"]) == len(record["assemblies"]) == len(quota_list)
    for index, (row, (b, a)) in enumerate(zip(record["macros"], quota_list, strict=True)):
        i = 4*index
        B = (first_pair(b, i, original["roles"]), b+3, spine[i:i+2])
        H = (bridge(a, i+2), a+2, spine[i+2:i+4])
        normalized(original, row["F"], *B)
        normalized(original, row["H"], *H)
        assert row["F"]["offsets"] == [1, 0] and row["H"]["offsets"] == [0, 1]
        R = (closed_form([B, H]), a+b+5, spine[i:i+4])
        normalized(original, row["R"], *R)
        assert row["R"]["offsets"] == [1, 1]
        audit_join(original, row["join"], B, H, R[0])
        macro_parts.append(R)

    for index, row in enumerate(record["assemblies"]):
        parts = macro_parts[:index+1]
        prefix = closed_form(parts)
        p = sum(q for _, q, _ in parts)
        witness = spine[:4*(index+1)]
        normalized(original, row["normalized"], prefix, p, witness)
        assert row["normalized"]["offsets"] == [1, 1]
        if index == 0:
            assert row["join"] is None
        else:
            prev_record = record["assemblies"][index-1]["normalized"]
            prev = (prev_record["labels"], prev_record["P"], prev_record["witness"])
            audit_join(original, row["join"], prev, parts[-1], prefix)
    assert len(prefix) == sum(2*a+2*b+11 for b, a in quota_list)
    assert p == sum(a+b+5 for b, a in quota_list)

    suffix = record["suffix"]
    if L == 0:
        assert suffix is None
        return prefix
    shifted = {v: a if a < p else a+L for v, a in prefix.items()}
    assert suffix["assigned"] == shifted
    m = len(original["edges"])
    used_r = sorted(shifted.values())
    used_d = sorted(w for _, _, w in weights(original, shifted))
    assert used_r == list(range(p)) + list(range(p+L, m+1))
    assert used_d == list(range(L+1, m+1))
    R = sorted(set(range(m+1)) - set(used_r))
    D = sorted(set(range(1, m+1)) - set(used_d))
    assert (R, D) == (list(range(p, p+L)), list(range(1, L+1)))
    path = spine[len(witness)-1:]
    pending = [e for e in original["edges"] if not set(e) <= shifted.keys()]
    assert set(original["roles"]) - shifted.keys() == set(path[1:])
    assert pending == [list(e) for e in zip(path, path[1:])]
    crossing = [e for e in pending if (e[0] in shifted) != (e[1] in shifted)]
    assert suffix["path"] == path and suffix["pending_edges"] == pending
    assert suffix["crossing"] == crossing == [path[:2]]
    assert suffix["port"] == [path[0], p+L+1]
    checked = suffix["partial_checker"]
    assert checked["valid"] and not checked["complete"] and checked["errors"] == []
    assert checked["graph_digest"] == original["digest"] and checked["frontier"] == [path[0]]
    assert (checked["n"], checked["m"]) == (m+1, m)
    assert (checked["used_labels"], checked["used_differences"]) == (used_r, used_d)
    assert (checked["unused_labels"], checked["unused_differences"]) == (R, D)
    # The only finite suffix case reflects C2=(3,1,0) in 3 to get (0,2,3).
    assert L == 5
    base = [6, 1, 4, 0, 2, 3]
    sequence = [p+x for x in base]
    assert suffix["sequence"] == sequence and sequence[0] == shifted[path[0]]
    assert sorted(sequence[1:]) == R
    assert sorted(abs(u-v) for u, v in zip(sequence, sequence[1:])) == D
    return shifted | dict(zip(path[1:], sequence[1:], strict=True))


def lex_rank(order, alphabet):
    assert len(order) == len(alphabet) and all(type(x) is int for x in order)
    available = alphabet.copy()
    rank = 0
    for value in order:
        index = available.index(value)
        rank = rank*len(available) + index
        del available[index]
    return rank


def audit_enumeration(case, original, control_labels, cpu):
    key, graph_id, x, size, wanted_hits = case
    roles = original["roles"]
    depth_delta = {"spine": 0, "branch": 1, "leaf": 2}
    low = {v for v, role in roles.items() if (role["section"] + depth_delta[role["kind"]]) % 2 == 0}
    high = set(roles) - low
    edges = original["edges"]
    assert len(low) == 5
    pins = {"s:0": x, "s:1": 5}
    record = read(f"{key}_enumeration.json")
    assert record["graph_id"] == graph_id
    assert record["pins"] == pins and record["graph_digest"] == original["digest"]
    assert record["status"] == "COMPLETE" and record["visits"] == len(record["rows"]) == size
    lo_names, hi_names = record["free_names"]
    assert Counter(lo_names) == Counter(low-{"s:0"}) and Counter(hi_names) == Counter(high-{"s:1"})
    lo_band = sorted(set(range(5)) - {x})
    hi_band = list(range(6, len(roles)))
    assert record["free_labels"] == [lo_band, hi_band]
    assert all((u in low) != (v in low) for u, v in edges)
    high_count = factorial(len(hi_band))
    assert factorial(len(lo_band))*high_count == size
    location = {v: (side, j) for side, names in enumerate((lo_names, hi_names))
                for j, v in enumerate(names)}
    accepted = {row["rank"]: row["certificate"] for row in record["positive"]}
    assert len(accepted) == len(record["positive"]) == wanted_hits
    ranks, found = set(), set()
    matches = 0
    for rank, lo, hi, repeat in record["rows"]:
        assert cpu + process_time()-START < 29, "audit CPU reserve"
        assert type(rank) is int and rank == lex_rank(lo, lo_band)*high_count+lex_rank(hi, hi_band)
        assert rank not in ranks
        ranks.add(rank)
        if repeat is None:
            labels = pins | dict(zip(lo_names, lo, strict=True)) | dict(zip(hi_names, hi, strict=True))
            check_certificate(original, accepted[rank], labels)
            found.add(rank)
            matches += int(labels == control_labels)
        else:
            i, j, w = repeat
            assert all(type(x) is int for x in repeat) and 0 <= i < j < len(edges)
            endpoints = set(edges[i]+edges[j])
            labels = {v: pins[v] for v in endpoints & pins.keys()}
            for v in endpoints - pins.keys():
                side, index = location[v]
                labels[v] = (lo, hi)[side][index]
            assert all(abs(labels[u]-labels[v]) == w for u, v in (edges[i], edges[j]))
    assert ranks == set(range(size)) and found == set(accepted)
    assert matches == (0 if key == "unequal_strict" else 1)
    return [len(found), size]


def main():
    if not __debug__:
        raise RuntimeError("Audit requires enabled assertions")
    config = read("config.json")
    assert config["profiles"] == PROFILES and config["enumerations"] == DECLARED
    assert config["macro_cases"] == [["r21",[[2,1]],0], ["r32",[[3,2]],0],
                                     ["repeat_l5",[[2,1],[3,2]],5]]
    assert config["limits"] == {"workers": 1, "assignment_cap": 900, "scheduled_visits": 864,
        "new_original_cap": 8, "retained_originals": 1, "adverse": 3, "cpu_seconds": 30,
        "bytes_per_record": 2_000_000, "bytes_total": 8_000_000, "solver_calls": 0, "retries": 0, "replays": 0}
    ident = read("identity.json")
    assert ident["parent"] == config["parent"]
    assert ident["runtime"] == {"version": sys.version, "path": Path(sys.executable).relative_to(ROOT).as_posix(),
                                "sha256": raw_hash(Path(sys.executable))}
    for path, digest in ident["sources"].items():
        assert raw_hash(ROOT/path) == digest
    assert all(ident["sources"][p] == value for p, value in config["intake_inputs"].items())
    auth = config["authorization"]
    assert raw_hash(ROOT/auth["path"]) == ident["sources"][auth["path"]] == auth["sha256"]

    originals = {k: topology(read(f"{k}_original.json"), profile) for k, profile in PROFILES.items()}
    archive = config["retained"]
    saved = {row["path"]: row["sha256"] for row in read(ROOT/archive["manifest"])["files"]}
    for key in ("original", "certificate"):
        path = ROOT/archive[key]
        assert raw_hash(path) == saved[path.name]
    originals["f1_retained"] = topology(read(ROOT/archive["original"]), PROFILE_B)
    assert len({o["digest"] for o in originals.values()}) == 8
    assert len(list(HERE.glob("*_original.json"))) == 7
    bundle = read("certificates.json")
    cert = bundle["controls"]
    assert set(cert) == set(originals)
    expected = {"unequal": {"s:0": 2, "s:1": 5, "b:0:0": 7, "l:0:0:0": 3, "b:0:1": 8,
                            "l:0:1:0": 0, "l:0:1:1": 1, "b:1:0": 4, "l:1:0:0": 6}}
    for key, b in (("f0",0), ("f1_retained",1), ("f2",2), ("f4",4)):
        expected[key] = first_pair(b, 0, originals[key]["roles"])
        normalized(originals[key], cert[key]["normalized"], expected[key], b+3, ["s:0","s:1"])
        assert cert[key]["normalized"]["offsets"] == [1,0]
    normalized(originals["unequal"], cert["unequal"]["normalized"], expected["unequal"], 5, ["s:0","s:1"])
    assert cert["unequal"]["normalized"]["offsets"] == [2,0]
    boundary = originals["f0"]
    assert len(boundary["roles"]) == 6
    for center, spine_vertex in (("b:0:1", "s:0"), ("b:1:0", "s:1")):
        assert [e for e in boundary["edges"] if center in e] == [[spine_vertex, center]]
    retained = read(ROOT/archive["certificate"])["positive_controls"]["small"]
    for key in ("ledger_id", "graph_digest", "edge_rows", "labels", "checker"):
        assert cert["f1_retained"][key] == retained[key]
    for k, quotas, L in config["macro_cases"]:
        expected[k] = audit_macros(originals[k], cert[k], quotas, L)
    assert len(expected["repeat_l5"]) == 43
    assert cert["repeat_l5"]["suffix"]["sequence"] == [24,19,22,18,20,21]
    assert cert["r21"]["labels"] == cert["repeat_l5"]["assemblies"][0]["normalized"]["labels"]
    for k, labels in expected.items():
        check_certificate(originals[k], cert[k], labels)

    bad = bundle["adverse"]
    wrong = bad["wrong_digest"]
    assert wrong["graph_id"] == "f2" and wrong["expected"] == "0"*64 != cert["f2"]["graph_digest"]
    assert wrong["checker"] == cert["f2"]["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]}
    assert bad["offset"] == {"valid": False, "reason": "R241 physical offset mismatch",
                             "y_B": 0, "x_A": 1, "ports": ["s:1","s:2"],
                             "swapped_low_names": ["s:2","l:2:0:0"], "graph_digest": originals["r21"]["digest"]}
    r21 = cert["r21"]["macros"][0]
    assert r21["F"]["port_labels"][1]-r21["F"]["P"] == 0
    assert (r21["H"]["labels"]["s:2"], r21["H"]["labels"]["l:2:0:0"]) == (0,1)
    assert bad["suffix"] == {"valid": False, "reason": "wrong suffix difference inventory",
                             "declared_d": [2,3,4,5], "actual_d": [1,2,3,4,5],
                             "graph_digest": originals["repeat_l5"]["digest"]}

    result = read("result.json")
    cpu = result["process_cpu_seconds"]
    counts = {case[0]: audit_enumeration(case, originals[case[1]], expected[case[1]], cpu)
              for case in DECLARED}
    assert result == {"status": "COMPLETE", "new_originals": 7, "retained_originals": 1,
                      "control_certificates": 8, "diagnostic_positive_certificates": 6, "adverse": 3,
                      "diagnostic_visits": 864, "counts": counts, "solver_calls": 0, "replays": 0,
                      "process_cpu_seconds": cpu}
    assert sum(visits for _, visits in counts.values()) == 864 <= config["limits"]["assignment_cap"]
    aggregate = cpu+process_time()-START
    assert aggregate < 30
    output = {"status": "PASS", "producer_and_audit_cpu_seconds": aggregate, "counts": counts,
              "rank_and_receipt_checks": 864, "new_audit_visits": 0, "checked_control_certificates": 8,
              "checked_diagnostic_positive_certificates": 6, "adverse_rejections": 3,
              "raw_receipts": {p.name: raw_hash(p) for p in sorted(HERE.glob("*.json"))}}
    raw = (json.dumps(output,sort_keys=True,indent=2)+"\n").encode()
    assert len(raw) <= 2_000_000
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(raw) <= 8_000_000
    with (HERE/"audit_result.json").open("xb") as stream:
        stream.write(raw)


if __name__ == "__main__":
    main()
