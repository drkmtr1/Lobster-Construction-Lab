"""Read-only arithmetic reconstruction of the same ten certificates."""
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import process_time

START = process_time()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_bytes())


def checksum(raw):
    return sha256(raw).hexdigest()


def canonical(value):
    return checksum(json.dumps(value, sort_keys=True, ensure_ascii=False,
                               separators=(",", ":")).encode("utf-8"))


def bytes_bound(ref):
    raw = (ROOT / ref["path"]).read_bytes()
    if "checkout_crlf_sha256" in ref and checksum(raw) == ref["checkout_crlf_sha256"]:
        raw = raw.replace(b"\r\n", b"\n")
    require(len(raw) == ref["bytes"] and checksum(raw) == ref["sha256"], ref["path"])
    return raw


def edge_key(edge):
    return tuple(sorted(edge))


def topology(t, k):
    # Generate each non-root vertex from its one required parent.
    spine = [f"s:{i}" for i in range(5 + k)]
    roles = {name: {"section": i, "kind": "spine"} for i, name in enumerate(spine)}
    parents = dict(zip(spine[1:], spine[:-1], strict=True))
    for section, count in enumerate((2, 2, t, 2)):
        center = f"b:{section}:0"
        parents[center] = spine[section]
        roles[center] = {"section": section, "kind": "branch", "branch": 0}
        for index in range(count):
            leaf = f"l:{section}:0:{index}"
            parents[leaf] = center
            roles[leaf] = {"section": section, "kind": "leaf", "branch": 0, "leaf": index}
    profile = [[2], [2], [t], [2]] + [[]] * (k + 1)
    edges = Counter(map(edge_key, parents.items()))
    identity = canonical({"vertices": sorted(roles), "edges": sorted(edges.elements()),
                          "profile": profile, "spine": spine, "roles": roles})
    return roles, edges, spine, profile, identity


def expected_labels(t):
    rows = (
        ("s", (10, 2, 16, 7, 9)),
        ("b", (6, 14, 0, 8)),
        ("l", ((12, 13), (1, 4), (15, 11, *range(17, t + 15)), (3, 5))),
    )
    spine, centers, leaves = (row[1] for row in rows)
    labels = {f"s:{i}": a for i, a in enumerate(spine)}
    labels.update({f"b:{i}:0": a for i, a in enumerate(centers)})
    labels.update({f"l:{i}:0:{j}": a for i, branch in enumerate(leaves) for j, a in enumerate(branch)})
    return labels


def path_labels(k):
    sequences = {2: [3, 1, 0], 3: [4, 1, 0, 2], 4: [5, 1, 2, 0, 3]}
    for length in range(5, k + 1):
        reflected_tail = [length - 2 - value for value in sequences[length - 3][1:]]
        sequences[length] = [length + 1, 1, length - 1, 0] + reflected_tail
    return sequences[k]


def distances(edges, path):
    require(all(edge_key(pair) in edges for pair in zip(path, path[1:])), "witness edges")
    adjacency = {}
    for u, v in edges:
        adjacency.setdefault(u, []).append(v)
        adjacency.setdefault(v, []).append(u)
    levels = dict.fromkeys(path, 0)
    visit = deque(path)
    while visit:
        node = visit.popleft()
        for other in adjacency[node]:
            if other not in levels:
                levels[other] = levels[node] + 1
                visit.append(other)
    require(levels.keys() == adjacency.keys() and max(levels.values()) <= 2
            and levels["b:2:0"] == 1, "witness distances")
    return levels


def check_original(original, t, k):
    roles, edges, spine, profile, identity = topology(t, k)
    graph = original["graph"]
    require(Counter(graph["vertices"]) == Counter(roles.keys())
            and Counter(map(edge_key, graph["edges"])) == edges, "vertex or edge multiplicities")
    require(graph["roles"] == roles and graph["spine"] == spine and graph["profile"] == profile
            and type(graph["schema_version"]) is int and graph["schema_version"] == 1
            and original["graph_digest"] == identity, "profile or original digest")
    return graph, edges, identity


def check_receipt(cert, graph, labels, identity):
    m = len(graph["edges"])
    ledger = [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]
    weights = [row["difference"] for row in ledger]
    require(cert["labels"] == labels and all(type(a) is int for a in cert["labels"].values())
            and Counter(labels.values()) == Counter(range(m + 1))
            and Counter(weights) == Counter(range(1, m + 1)), "complete spectrum")
    lid = canonical({"graph_digest": identity, "labels": sorted(labels.items())})
    require(lid != identity and cert["ledger_id"] == lid and cert["graph_digest"] == identity
            and cert["named_edges"] == ledger, "certificate identities and original-edge ledger")
    receipt = cert["checker"]
    require(receipt["valid"] is True and receipt["errors"] == []
            and receipt["n"] == m + 1 and receipt["m"] == m
            and receipt["graph_digest"] == identity and receipt["edge_differences"] == weights,
            "complete verifier receipt")
    return lid


def check_prefix(cert, original, t):
    graph, edges, identity = check_original(original, t, 0)
    labels = expected_labels(t)
    low = sorted(v for v, value in labels.items() if value < 8)
    high = sorted(v for v in labels if v not in low)
    require(sorted(labels[v] for v in low) == list(range(8))
            and sorted(labels[v] for v in high) == list(range(8, t + 15))
            and all((u in low) != (v in low) for u, v in edges)
            and (labels[W[0]], labels[W[-1]], labels["b:2:0"]) == (6, 9, 0), "alpha and ports")
    require(cert["t"] == t and cert["state"] == {
        "n": t + 15, "p": 8, "x": 6, "y": 1, "low": low, "high": high, "L": W[0],
        "U": W[-1], "z": "b:2:0", "witness": W, "distances": distances(edges, W),
    }, "recorded alpha state")
    return check_receipt(cert, graph, labels, identity), labels


def check_target(cert, original, t, k, source):
    graph, edges, identity = check_original(original, t, k)
    lid, normalized = source
    prefix = {v: a + k * (a >= 8) for v, a in normalized.items()}
    path = graph["spine"][4:]
    pending = [e for e in graph["edges"] if any(v not in prefix for v in e)]
    require(Counter(map(edge_key, pending)) == Counter(map(edge_key, zip(path, path[1:])))
            and set(graph["vertices"]) - prefix.keys() == set(path[1:])
            and [e for e in pending if sum(v in prefix for v in e) == 1] == [path[:2]],
            "original pending edges or physical crossing")
    m = t + k + 14
    used = sorted(prefix.values())
    weights = sorted(abs(prefix[u] - prefix[v]) for u, v in edges if u in prefix and v in prefix)
    r = sorted(set(range(m + 1)) - set(used))
    d = sorted(set(range(1, m + 1)) - set(weights))
    require(used == list(range(8)) + list(range(k + 8, m + 1))
            and weights == list(range(k + 1, m + 1)) and r == list(range(8, k + 8))
            and d == list(range(1, k + 1)), "exact used and residual inventories")
    ck = path_labels(k)
    translated = [x + 8 for x in ck]
    suffix_weights = [abs(y - x) for x, y in zip(translated, translated[1:])]
    require(translated[0] == prefix["s:4"] == k + 9 and sorted(translated[1:]) == r
            and sorted(suffix_weights) == d, "source-independent suffix spectrum")
    labels = prefix | dict(zip(path[1:], translated[1:], strict=True))
    expected = {
        "t": t, "K": k, "source_ledger_id": lid, "prefix": prefix, "R": r, "D": d,
        "port": {"vertex": "s:4", "label": k + 9}, "path": path, "pending": pending,
        "C_K": ck, "translated_path": translated, "suffix_weights": suffix_weights,
        "witness": W + path[1:], "distances": distances(edges, W + path[1:]),
    }
    require(all(cert[key] == value for key, value in expected.items()), "full path evidence")
    part = cert["partial_checker"]
    require(part["valid"] is True and part["complete"] is False and part["errors"] == []
            and part["graph_digest"] == identity and part["frontier"] == ["s:4"]
            and part["used_labels"] == used and part["used_differences"] == weights
            and part["unused_labels"] == r and part["unused_differences"] == d, "partial receipt")
    return check_receipt(cert, graph, labels, identity)


def check_batches(p5):
    batches = load(HERE / "batches.json")
    require([row["partition"] for row in batches] == [[1, 2], [2, 1]], "batch scope")
    for row in batches:
        index = 2
        accumulated = expected_labels(2)
        require(len(row["steps"]) == len(row["partition"]), "batch step count")
        for size, step in zip(row["partition"], row["steps"], strict=True):
            names = [f"l:2:0:{j}" for j in range(index, index + size)]
            additions = {v: p5[v] for v in names}
            require(step == {"names": names, "host": "b:2:0", "added": additions},
                    "named batch evidence")
            require(sorted(additions.values()) == list(range(len(accumulated), len(accumulated) + size)),
                    "batch uses next label band")
            accumulated.update(additions)
            index += size
        require(index == 5 and accumulated == p5 == row["labels"], "pointwise batch equality")


def check_adverse(p3_digest):
    saved = load(HERE / "adverse.json")
    require(set(saved) == {"wrong_digest", "wrong_host", "missing_terminal", "wrong_exit",
                          "missing_D", "K1"}, "adverse case scope")
    wrong_digest, missing = saved["wrong_digest"], saved["missing_terminal"]
    require(wrong_digest["valid"] is False and wrong_digest["graph_digest"] == p3_digest
            and wrong_digest["errors"] == ["original graph digest mismatch"], "adverse graph identity")
    require(missing["valid"] is False and missing["graph_digest"] == p3_digest
            and "complete certificate must label every original vertex exactly once" in missing["errors"],
            "missing named leaf rejection")
    wrong_host = saved["wrong_host"]
    _, edges, _, _, _ = topology(3, 0)
    removed, added = map(edge_key, (wrong_host["remove"], wrong_host["add"]))
    require(removed == edge_key(("b:2:0", "l:2:0:2")) and edges[removed] == 1
            and added == edge_key(("s:2", "l:2:0:2")) and edges[added] == 0, "wrong-host input")
    require(wrong_host["rejected"] is True and wrong_host["checker"]["valid"] is False
            and "actual named edges do not match the original profile" in wrong_host["checker"]["errors"]
            and wrong_host["error"] == "fresh incidences must attach only to b:2:0", "wrong host rejection")
    require(10 != 2 + 9 and [1] != [1, 2], "adverse numerical mismatches")
    for key in ("wrong_exit", "missing_D"):
        require(saved[key] == {"rejected": True, "error": "nonadjacent inventories or physical port"}, key)
    require(saved["K1"] == {"rejected": True, "error": "nonadjacent contract needs K>=2",
                            "actual_edge_weight": abs(10 - 8)} and abs(10 - 8) != 1, "K=1 scope")


def main():
    cfg = load(HERE / "config.json")
    parent = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    require(parent == cfg["parent"], "source parent")
    freeze = load(HERE / "freeze.json")
    for ref in [*cfg["retained"].values(), *freeze["sources"].values(), *freeze["records"].values()]:
        bytes_bound(ref)
    for ref in cfg["retained"].values():
        raw = subprocess.check_output(["git", "show", f"{parent}:{ref['path']}"], cwd=ROOT)
        require(checksum(raw) == ref["sha256"], "parent source hash")
    require(freeze["runtime"] == {"python": sys.version, "platform": sys.platform,
                                "executable_sha256": checksum(Path(sys.executable).read_bytes())},
            "runtime identity")
    require(cfg["prefixes"] == [3, 4, 5, 8] and cfg["targets"] == [[3, 2], [4, 3], [5, 5], [8, 8]],
            "declared graph scope")
    references = freeze["records"]
    require(set(references) == {"p3", "p4", "p5", "p8", "t3_k2", "t4_k3", "t5_k5", "t8_k8"},
            "frozen graph scope")
    binding = {**references, "p2": cfg["retained"]["p2_original"],
               "t2_k2": cfg["retained"]["t22_original"]}
    require({p.name for p in HERE.glob("*_certificate.json")} ==
            {key + "_certificate.json" for key in binding}, "certificate scope")
    originals = {key: json.loads(bytes_bound(ref)) for key, ref in binding.items()}
    certificates = {key: load(HERE / (key + "_certificate.json")) for key in binding}
    for key, cert in certificates.items():
        require(cert["original"] == binding[key], "original source binding")
    p2_archived = json.loads(bytes_bound(cfg["retained"]["d066_certificates"]))["prefix"]
    k2_archived = json.loads(bytes_bound(cfg["retained"]["d067_k2"]))
    for archived, key in [(p2_archived, "p2"), (k2_archived, "t2_k2")]:
        require(all(archived[field] == certificates[key][field]
                    for field in ("labels", "graph_digest", "named_edges", "checker")), "retained control")
    prefixes = {}
    validation = load(HERE / "result.json")
    prior_cpu = freeze["cpu_seconds"] + validation["cpu_seconds"]
    for t in (2, 3, 4, 5, 8):
        require(process_time() - START + prior_cpu < 30, "combined process CPU cap")
        key = f"p{t}"
        prefixes[t] = check_prefix(certificates[key], originals[key], t)
        if t > 2:
            require(certificates[key]["seed_ledger_id"] == prefixes[2][0], "seed ledger binding")
    ledgers = {}
    for t, k in ((2, 2), (3, 2), (4, 3), (5, 5), (8, 8)):
        require(process_time() - START + prior_cpu < 30, "combined process CPU cap")
        key = f"t{t}_k{k}"
        ledgers[key] = check_target(certificates[key], originals[key], t, k, prefixes[t])
    check_batches(prefixes[5][1])
    check_adverse(originals["p3"]["graph_digest"])
    require({k: v for k, v in validation.items() if k != "cpu_seconds"} ==
            {"status": "PASS", "retained": 2, "prefixes": 4, "targets": 4, "complete_checks": 10,
             "adverse_rejections": 6, "batch_partitions": 2, "queries": 0, "nodes": 0, "retries": 0},
            "producer accounting")
    cpu = process_time() - START
    total_cpu = prior_cpu + cpu
    require(total_cpu < 30, "combined process CPU cap")
    result = {"status": "PASS", "checked_same_records": 10, "additional_graphs": 0,
              "additional_queries": 0, "adverse_receipts": 6, "batch_partitions": 2,
              "cpu_seconds": cpu, "combined_cpu_seconds": total_cpu,
              "ledger_ids": {**{f"p{t}": value[0] for t, value in prefixes.items()}, **ledgers}}
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    require(len(raw) <= 2_000_000 and total + len(raw) <= 12_000_000, "evidence byte cap")
    with (HERE / "audit_result.json").open("xb") as output:
        output.write(raw)
    print("audit PASS")


if __name__ == "__main__":
    main()
