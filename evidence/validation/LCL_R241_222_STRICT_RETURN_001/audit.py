"""Independent topology, factorial-rank, and actual-edge receipt audit."""

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


def lex_rank(order, alphabet):
    assert len(order) == len(alphabet) and all(type(x) is int for x in order)
    items = alphabet.copy()
    value = 0
    for label in order:
        index = items.index(label)
        value = value*len(items) + index
        items.pop(index)
    return value


def verify_falsifier(edges, labels, repeat):
    i, j, w = repeat
    assert all(type(v) is int for v in repeat) and 0 <= i < j < len(edges)
    assert all(abs(labels[u]-labels[v]) == w for u, v in (edges[i],edges[j]))


def audit_controls(config):
    folder = ROOT / config["archive"]
    manifest = {itm["path"]: itm["sha256"] for itm in read(folder/"MANIFEST.json")["files"]}
    for name in ("f2_original.json", "unequal_original.json", "repeat_l5_original.json",
                 "certificates.json", "unequal_strict_enumeration.json", "audit_result.json"):
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

    unequal = topology(read(folder/"unequal_original.json"), [[1,2],[1]])
    negative = read(folder/"unequal_strict_enumeration.json")
    previous_audit = read(folder/"audit_result.json")
    pins = {"s:0":1,"s:1":5}
    assert controls["negative"] == {"graph_digest": unequal["digest"], "pins": pins,
          "positive": 0, "historical_visits": 144, "new_visits": 0,
          "source": "unequal_strict_enumeration.json", "auditor": "audit_result.json"}
    assert negative["pins"] == pins and negative["graph_digest"] == unequal["digest"]
    assert negative["status"] == "COMPLETE" and negative["visits"] == len(negative["rows"]) == 144
    assert negative["positive"] == [] and previous_audit["status"] == "PASS"
    assert previous_audit["counts"]["unequal_strict"] == [0,144]
    assert previous_audit["raw_receipts"]["unequal_strict_enumeration.json"] == manifest["unequal_strict_enumeration.json"]
    rank, lo, hi, repeat = negative["rows"][0]
    lo_names, hi_names = negative["free_names"]
    assert rank == 0 and lo == [0,2,3,4] and hi == [6,7,8]
    retained_row = pins | dict(zip(lo_names, lo, strict=True)) | dict(zip(hi_names, hi, strict=True))
    verify_falsifier(unequal["edges"], retained_row, repeat)

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
    return [f2["digest"], unequal["digest"], target["digest"]]


def audit_enumeration(original, cpu):
    raw = read("enumeration.json")
    pins = {"s:0":1, "s:1":6}
    assert raw["graph_digest"] == original["digest"] and raw["pins"] == pins and raw["cut"] == 6
    low = {"s:0","b:1:0","l:0:0:0","l:0:0:1","l:0:1:0","l:0:1:1"}
    high = set(original["roles"])-low
    edges = original["edges"]
    assert all((u in low) != (v in low) for u,v in edges)
    lo_names, hi_names = raw["free_names"]
    assert Counter(lo_names) == Counter(low-{"s:0"}) and Counter(hi_names) == Counter(high-{"s:1"})
    free_lo, free_hi = [0,2,3,4,5], [7,8,9,10]
    assert raw["free_labels"] == [free_lo,free_hi]
    high_count = factorial(len(free_hi))
    size = factorial(len(free_lo))*high_count
    assert raw["status"] == "COMPLETE" and raw["visits"] == len(raw["rows"]) == size == 2880
    location = {v:(side,j) for side,names in enumerate((lo_names,hi_names)) for j,v in enumerate(names)}
    positives = {row["rank"]:row["certificate"] for row in raw["positive"]}
    assert len(positives) == len(raw["positive"])
    valid_ranks, covered = set(), set()
    for rank, lo, hi, repeat in raw["rows"]:
        assert cpu+process_time()-START < 29, "audit CPU reserve"
        expected = lex_rank(lo, free_lo)*high_count + lex_rank(hi, free_hi)
        assert type(rank) is int and rank == expected and rank not in covered
        covered.add(rank)
        if repeat is None:
            labels = pins | dict(zip(lo_names,lo,strict=True)) | dict(zip(hi_names,hi,strict=True))
            check_certificate(original, positives[rank], labels)
            valid_ranks.add(rank)
        else:
            i,j,_ = repeat
            assert type(i) is type(j) is int and 0 <= i < j < len(edges)
            endpoints = set(edges[i]+edges[j])
            labels = {v:pins[v] for v in endpoints & pins.keys()}
            for v in endpoints-pins.keys():
                side,index = location[v]
                labels[v] = (lo,hi)[side][index]
            verify_falsifier(edges, labels, repeat)
    assert covered == set(range(size)) and set(positives) == valid_ranks
    return size, len(valid_ranks)


def main():
    if not __debug__:
        raise RuntimeError("Audit requires enabled assertions")
    config = read("config.json")
    assert config["profile"] == [[2,2],[2]] and config["pins"] == {"s:0":1,"s:1":6} and config["cut"] == 6
    assert config["limits"] == {"workers":1,"visits":2880,"new_original_cap":8,"planned_new_originals":1,
                               "adverse":3,"combined_cpu_seconds":30,"bytes_per_record":2_000_000,
                               "bytes_total":8_000_000,"solver_calls":0,"retries":0,"replays":0}
    identity = read("identity.json")
    assert identity["parent"] == config["parent"]
    assert identity["runtime"] == {"version":sys.version, "path":Path(sys.executable).relative_to(ROOT).as_posix(),
                                  "sha256":raw_hash(Path(sys.executable))}
    for path, digest in identity["source_hashes"].items():
        assert raw_hash(ROOT/path) == digest
    assert all(identity["source_hashes"][p] == h for p,h in config["intake_sources"].items())
    spec = config["specification"]
    assert identity["source_hashes"][spec["path"]] == spec["sha256"]
    assert [p.name for p in HERE.glob("*_original.json")] == ["strict_original.json"]
    original = topology(read("strict_original.json"), [[2,2],[2]])
    assert len(original["roles"]) == 11 and len(original["edges"]) == 10
    retained = audit_controls(config)
    assert len(set(retained+[original["digest"]])) == 4
    result = read("result.json")
    cpu = result["process_cpu_seconds"]
    size, num = audit_enumeration(original, cpu)
    assert result == {"status":"COMPLETE","new_originals":1,"visits":size,"positive":num,
                      "adverse_rejections":3,"retained_replay_visits":0,"solver_calls":0,"process_cpu_seconds":cpu}
    total = cpu+process_time()-START
    assert total < 30
    output = {"status":"PASS","producer_and_audit_cpu_seconds":total,
              "visits_certified":size,"duplicate_edge_receipts":size-num,"positive_certificates":num,
              "new_audit_visits":0,"retained_replay_visits":0,"adverse_rejections":3,
              "raw_receipts":{p.name:raw_hash(p) for p in sorted(HERE.glob("*.json"))}}
    data = (json.dumps(output,indent=2,sort_keys=True)+"\n").encode()
    assert len(data) <= 2_000_000
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())+len(data) <= 8_000_000
    with (HERE/"audit_result.json").open("xb") as stream:
        stream.write(data)


if __name__ == "__main__":
    main()
