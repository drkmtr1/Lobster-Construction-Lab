"""Independently reconstruct the original and audit D083 proof arithmetic."""

from time import process_time

START = process_time()

from collections import Counter
from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


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


def audit_controls(config):
    folder = ROOT / config["positive_archive"]
    manifest = {itm["path"]: itm["sha256"] for itm in read(folder/"MANIFEST.json")["files"]}
    for name in ("f2_original.json", "repeat_l5_original.json", "certificates.json"):
        assert raw_hash(folder/name) == manifest[name]
    archived = read(folder/"certificates.json")["controls"]
    controls = read("controls.json")
    positive = controls["positive"]
    f2 = topology(read(folder/"f2_original.json"), [[1,2],[2]])
    expected = {"s:0":1, "s:1":5, "b:0:0":9, "l:0:0:0":0, "b:0:1":8,
                "l:0:1:0":2, "l:0:1:1":3, "b:1:0":4, "l:1:0:0":6, "l:1:0:1":7}
    check_certificate(f2, positive, expected)
    assert positive["offsets"] == [1,0] and positive["source"] == "f2_original.json"
    assert all((expected[u] < 5) != (expected[v] < 5) for u, v in f2["edges"])
    assert all(positive[k] == archived["f2"][k] for k in ("labels","graph_digest","ledger_id","checker","edge_rows"))

    neg_folder = ROOT / config["negative_archive"]
    previous_members = {row["path"]:row["sha256"] for row in read(neg_folder/"MANIFEST.json")["files"]}
    for name in ("strict_original.json", "enumeration.json", "audit_result.json", "config.json"):
        assert raw_hash(neg_folder/name) == previous_members[name]
    old = topology(read(neg_folder/"strict_original.json"), [[2,2],[2]])
    previous_cfg = read(neg_folder/"config.json")
    previous_audit = read(neg_folder/"audit_result.json")
    pins = {"s:0":1, "s:1":6}
    assert previous_cfg["pins"] == pins and previous_cfg["profile"] == [[2,2],[2]] and previous_cfg["cut"] == 6
    assert controls["negative"] == {"graph_digest": old["digest"], "pins": pins,
          "positive": 0, "historical_visits": 2880, "new_visits": 0,
          "source": "enumeration.json", "auditor": "audit_result.json",
          "sha256": previous_members["enumeration.json"]}
    assert previous_audit["status"] == "PASS" and previous_audit["visits_certified"] == 2880
    assert previous_audit["positive_certificates"] == 0 and previous_audit["duplicate_edge_receipts"] == 2880
    for name in ("strict_original.json", "enumeration.json", "config.json"):
        assert previous_audit["raw_receipts"][name] == previous_members[name]

    adverse = controls["adverse"]
    assert set(adverse) == {"digest", "offset", "difference"}
    wrong = adverse["digest"]
    assert wrong["graph_id"] == "f2" and wrong["expected"] == "0"*64 != f2["digest"]
    assert wrong["checker"] == positive["checker"] | {"valid": False, "errors": ["original graph digest mismatch"]}
    profile = [[1,2],[2],[1],[2],[1,3],[3],[2],[3]] + [[] for _ in range(5)]
    target = topology(read(folder/"repeat_l5_original.json"), profile)
    retained = archived["repeat_l5"]
    assert retained["graph_digest"] == target["digest"]
    first = retained["macros"][0]
    old = first["F"]
    new = first["H"]
    u, v, leaf = "s:1", "s:2", "l:2:0:0"
    assert old["ports"][-1] == u and new["ports"][0] == v
    assert old["labels"][u]-old["P"] == new["labels"][v] == 0 and new["labels"][leaf] == 1
    crossing = [[x,y] for x,y in target["edges"] if
                (x in old["labels"] and y in new["labels"]) or (y in old["labels"] and x in new["labels"])]
    assert not old["labels"].keys() & new["labels"].keys() and crossing == [[u,v]]
    assert adverse["offset"] == {"valid": False, "reason": "R241 physical offset mismatch",
                                "graph_digest": target["digest"], "connector": [u,v],
                                "swap": [v,leaf], "new_entrance_label": 1, "old_exit_offset": 0}
    saved = retained["suffix"]
    labels = saved["assigned"]
    m = len(target["edges"])
    used_d = sorted(d for _,_,d in weights(target, labels))
    used_r = sorted(labels.values())
    R = sorted(set(range(m+1)) - set(used_r))
    D = sorted(set(range(1,m+1)) - set(used_d))
    assert (R,D) == (list(range(18,23)), list(range(1,6)))
    assert used_r == list(range(18))+list(range(23,m+1)) and used_d == list(range(6,m+1))
    assert saved["port"] == ["s:7",24] and labels["s:7"] == 24
    pending = [e for e in target["edges"] if not set(e) <= labels.keys()]
    path = target["spine"][7:]
    assert saved["path"] == path and pending == [list(e) for e in zip(path,path[1:])]
    assert saved["pending_edges"] == pending and saved["crossing"] == [["s:7","s:8"]]
    assert adverse["difference"] == {"valid": False, "reason": "wrong suffix difference inventory",
                                     "graph_digest": target["digest"], "port": saved["port"],
                                     "declared_d": [2,3,4,5], "actual_d": D}
    return [f2["digest"], old["digest"], target["digest"]]


def audit_obstruction(original, pins, cut):
    roles, edges = original["roles"], original["edges"]
    adjacent = {v: [] for v in roles}
    for u, v in edges:
        adjacent[u].append(v)
        adjacent[v].append(u)
    side = {"s:0":0}
    pending = ["s:0"]
    while pending:
        u = pending.pop()
        for v in adjacent[u]:
            if v not in side:
                side[v] = 1-side[u]
                pending.append(v)
            assert side[v] != side[u]
    assert set(side) == set(roles)
    low = {v for v, value in side.items() if value == 0}
    high = set(side)-low
    assert low == {"s:0","b:1:0","l:0:0:0","l:0:0:1","l:0:1:0","l:0:1:1"}
    assert len(low) == len(high) == cut
    degree = {v:len(neighbors) for v,neighbors in adjacent.items()}
    signed_correction = {v:(1 if v in high else -1)*(d-1) for v,d in degree.items() if d > 1}
    assert signed_correction == {"s:0":-2,"s:1":1,"b:0:0":2,"b:0:1":2,"b:1:0":-3}
    n, m = len(roles), len(edges)
    labels_low, labels_high = list(range(cut)), list(range(cut,n))
    high_sum, low_sum = sum(labels_high), sum(labels_low)
    constant = high_sum-low_sum+sum(signed_correction[v]*p for v,p in pins.items())
    target = sum(range(1,m+1))
    assert (high_sum, low_sum, constant, target) == (51,15,40,66)
    lows = sorted(set(labels_low)-{pins["s:0"]})
    highs = sorted(set(labels_high)-{pins["s:1"]})
    left_centers = ["b:0:0","b:0:1"]
    right_center = "b:1:0"
    candidates = []
    # Only ten numerical center pairs are tested. No named complete assignment is built.
    numerical_pairs = list(combinations(highs,2))
    for x, y in numerical_pairs:
        numerator = constant+signed_correction[left_centers[0]]*x+signed_correction[left_centers[1]]*y-target
        z, remainder = divmod(numerator, -signed_correction[right_center])
        if remainder == 0 and z in lows:
            candidates.append({"center_pair":[x,y], "z":z})
    assert candidates == [{"center_pair":[7,9],"z":2}, {"center_pair":[8,11],"z":4},
                          {"center_pair":[9,10],"z":4}]
    r_terminals = sorted(v for v,r in roles.items() if r["section"] == 1 and r["kind"] == "leaf")
    assert all(adjacent[v] == [right_center] for v in r_terminals)
    max_weight = n-1
    assert max_weight == 11 and max_weight != pins["s:1"]
    assert high == set(r_terminals + left_centers + ["s:1"])
    assert all(case["z"] > 0 for case in candidates)
    surviving, = [case for case in candidates if max_weight in case["center_pair"]]
    for center in left_centers:
        assert pins["s:0"] == 1 and "s:0" in adjacent[center]
        terminals = [v for v in adjacent[center] if roles[v]["kind"] == "leaf"]
        assert len(terminals) == 2 and all(adjacent[v] == [center] for v in terminals)
    right_labels = sorted(set(highs)-set(surviving["center_pair"]))
    assert right_labels == [7,9,10] and len(r_terminals) == len(right_labels)
    spine_weight = pins["s:1"]-pins["s:0"]
    right_weights = [value-surviving["z"] for value in right_labels]
    assert spine_weight == 5 and right_weights == [3,5,6]
    assert ["s:0","s:1"] in edges
    repeated_candidates = [[right_center,v] for v in r_terminals]
    assert all(e in edges and e != ["s:0","s:1"] for e in repeated_candidates)
    return {"graph_digest":original["digest"],"low_names":sorted(low),"high_names":sorted(high),
            "degree_by_name":degree,"correction_coefficients":signed_correction,"high_alphabet_sum":high_sum,
            "low_alphabet_sum":low_sum,"fixed_constant":constant,"required_sum":target,
            "numerical_pairs_checked":len(numerical_pairs),"necessary_cases":candidates,
            "surviving_after_max_weight":surviving,"right_terminal_labels":right_labels,
            "right_terminal_weights":right_weights,"right_terminal_edge_names":repeated_candidates,
            "spine_edge":["s:0","s:1"],"repeated_weight":spine_weight,"named_assignment_visits":0}


def main():
    if not __debug__:
        raise RuntimeError("Audit requires enabled assertions")
    config = read("config.json")
    assert config["profile"] == [[2,2],[3]] and config["pins"] == {"s:0":1,"s:1":6} and config["cut"] == 6
    limits = {"workers":1,"max_visits":14400,"max_recorded_states":14400,"scheduled_visits":0,
              "new_original_cap":8,"planned_new_originals":1,"adverse":3,"combined_cpu_seconds":30,
              "bytes_per_record":2_000_000,"bytes_total":8_000_000,"solver_calls":0,"retries":0,"replays":0}
    assert config["limits"] == limits and not (HERE/"enumeration.json").exists()
    identity = read("identity.json")
    assert identity["parent"] == config["parent"]
    assert identity["runtime"] == {"version":sys.version,"path":Path(sys.executable).relative_to(ROOT).as_posix(),
                                  "sha256":raw_hash(Path(sys.executable))}
    for path,digest in identity["source_hashes"].items():
        assert raw_hash(ROOT/path) == digest
    assert all(identity["source_hashes"][p] == h for p,h in config["intake_sources"].items())
    spec = config["specification"]
    assert identity["source_hashes"][spec["path"]] == spec["sha256"]
    assert [p.name for p in HERE.glob("*_original.json")] == ["strict_original.json"]
    original = topology(read("strict_original.json"), [[2,2],[3]])
    assert len(original["roles"]) == 12 and len(original["edges"]) == 11
    retained = audit_controls(config)
    assert len(set(retained+[original["digest"]])) == 4
    proof_arithmetic = audit_obstruction(original, config["pins"], config["cut"])
    result = read("result.json")
    producer_cpu = result["process_cpu_seconds"]
    assert result == {"status":"COMPLETE","new_originals":1,"assignment_visits":0,
                      "recorded_assignment_states":0,"adverse_rejections":3,"retained_replay_visits":0,
                      "solver_calls":0,"process_cpu_seconds":producer_cpu}
    total = producer_cpu+process_time()-START
    assert total < 30
    output = {"status":"PASS","producer_and_audit_cpu_seconds":total,"proof_arithmetic":proof_arithmetic,
              "assignment_visits":0,"recorded_assignment_states":0,"retained_replay_visits":0,
              "adverse_rejections":3,"raw_receipts":{p.name:raw_hash(p) for p in sorted(HERE.glob("*.json"))}}
    data = (json.dumps(output,indent=2,sort_keys=True)+"\n").encode()
    assert len(data) <= 2_000_000
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(data) <= 8_000_000
    with (HERE/"audit_result.json").open("xb") as stream:
        stream.write(data)


if __name__ == "__main__":
    main()
