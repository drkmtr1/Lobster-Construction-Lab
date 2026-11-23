"""Freeze and validate the declared original-bound D068 certificates."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import process_time

START = process_time()
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_graph, verify_partial

P_CASES = (3, 4, 5, 8)
T_CASES = ((3, 2), (4, 3), (5, 5), (8, 8))
W = ["b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4"]
Z = "b:2:0"
SEED = {
    **{f"s:{i}": value for i, value in enumerate((10, 2, 16, 7, 9))},
    "b:0:0": 6, "l:0:0:0": 12, "l:0:0:1": 13,
    "b:1:0": 14, "l:1:0:0": 1, "l:1:0:1": 4,
    Z: 0, "l:2:0:0": 15, "l:2:0:1": 11,
    "b:3:0": 8, "l:3:0:0": 3, "l:3:0:1": 5,
}
LIMITS = {
    "workers": 1, "new_prefixes": 4, "new_targets": 4, "complete_checks": 10,
    "max_order": 31, "cpu_seconds": 30, "record_bytes": 2_000_000,
    "total_bytes": 12_000_000, "queries": 0, "nodes": 0, "retries": 0,
}


def read(path):
    return json.loads(path.read_bytes())


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(raw):
    return sha256(raw).hexdigest()


def identity(path):
    raw = (ROOT / path).read_bytes()
    return {"path": path, "bytes": len(raw), "sha256": digest(raw)}


def put(name, record):
    raw = (json.dumps(record, sort_keys=True, indent=2) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    require(len(raw) <= LIMITS["record_bytes"] and total + len(raw) <= LIMITS["total_bytes"],
            "evidence byte cap")
    with (HERE / name).open("xb") as output:
        output.write(raw)


def check_config(cfg):
    require(cfg["limits"] == LIMITS and cfg["prefixes"] == list(P_CASES)
            and cfg["targets"] == [list(x) for x in T_CASES], "fixed scope mismatch")
    require(git("rev-parse", "HEAD").decode().strip() == cfg["parent"], "parent mismatch")
    require(sys.version_info[:2] in {(3, 12), (3, 13)}, "Python 3.12/3.13 required")
    for name, ref in cfg["retained"].items():
        path = ref["path"]
        actual = identity(path)
        committed = git("show", f'{cfg["parent"]}:{path}')
        raw = (ROOT / path).read_bytes()
        if "checkout_crlf_sha256" in ref:
            actual["bytes"], actual["sha256"] = len(committed), digest(committed)
            require(raw == committed or (raw.replace(b"\r\n", b"\n") == committed
                    and digest(raw) == ref["checkout_crlf_sha256"]), "consumer checkout bytes")
        require(all(ref[field] == value for field, value in actual.items())
                and digest(committed) == ref["sha256"],
                f"retained source bytes changed: {name}")


def archive(cfg, kind):
    return read(ROOT / cfg["retained"][kind]["path"])


def profile(t, k=0):
    return [[2], [2], [t], [2]] + [[] for _ in range(k + 1)]


def freeze(cfg, started):
    records = {}
    cases = [(t, 0) for t in P_CASES] + list(T_CASES)
    require(not any(HERE.glob("*_original.json")) and not (HERE / "freeze.json").exists(),
            "frozen outputs already exist")
    for t, k in cases:
        require(process_time() - started < LIMITS["cpu_seconds"], "freeze CPU cap")
        name = case_name(t, k)
        graph = build_graph(profile(t, k))
        report = verify_graph(graph)
        require(report["valid"] and report["n"] == t + k + 15 <= LIMITS["max_order"],
                f"original identity: {name}")
        path = name + "_original.json"
        put(path, {"graph": graph, "graph_digest": graph_digest(graph)})
        records[name] = identity((HERE / path).relative_to(ROOT).as_posix())
    task_paths = ["config.json", "commands.json", "validate.py", "audit.py", "INTAKE.md"]
    task_sources = {path: identity((HERE / path).relative_to(ROOT).as_posix()) for path in task_paths}
    task_sources["proof"] = identity(cfg["proof"])
    require(process_time() - started < LIMITS["cpu_seconds"], "freeze CPU cap")
    put("freeze.json", {"records": records, "sources": task_sources,
                        "runtime": {"python": sys.version, "platform": sys.platform,
                                    "executable_sha256": digest(Path(sys.executable).read_bytes())},
                        "cpu_seconds": process_time() - started})


def case_name(t, k):
    return f"p{t}" if k == 0 else f"t{t}_k{k}"


def frozen(record):
    require(identity(record["path"]) == record, f"frozen original changed: {record['path']}")
    return read(ROOT / record["path"])


def edge_key(edge):
    return tuple(sorted(edge))


def named_edges(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])}
            for u, v in graph["edges"]]


def ledger_id(original, labels):
    payload = {"graph_digest": original["graph_digest"], "labels": sorted(labels.items())}
    return digest(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())


def attach(old, names):
    require(old.get(Z) == 0 and len(set(names)) == len(names) and not (old.keys() & set(names)),
            "zero-host batch inputs")
    return old | {name: len(old) + i for i, name in enumerate(names)}


def extras(t):
    return [f"l:2:0:{j}" for j in range(2, t)]


def growth_incidence(graph, base_graph, added):
    old_names = set(base_graph["vertices"])
    require(set(graph["vertices"]) == old_names | set(added), "unexpected vertices in growth")
    unchanged = [edge_key(e) for e in graph["edges"] if all(v in old_names for v in e)]
    fresh = [edge_key(e) for e in graph["edges"] if any(v not in old_names for v in e)]
    require(sorted(unchanged) == sorted(map(edge_key, base_graph["edges"])),
            "old named incidences changed")
    require(sorted(fresh) == sorted(edge_key((Z, leaf)) for leaf in added),
            "fresh incidences must attach only to b:2:0")


def witness(graph, path):
    edges = set(map(edge_key, graph["edges"]))
    require(all(edge_key(e) in edges for e in zip(path, path[1:])), "witness path")
    distances = dict.fromkeys(path, 0)
    for step in (1, 2):
        frontier = [v for v in graph["vertices"] if v not in distances
                    and any(edge_key((v, u)) in edges for u in distances)]
        distances.update(dict.fromkeys(frontier, step))
    require(distances.keys() == set(graph["vertices"]) and distances[Z] == 1, "witness distances")
    return distances


def certificate(original, labels):
    result = verify_certificate(original["graph"], labels, original["graph_digest"])
    require(result["valid"], result["errors"])
    return {
        "graph_digest": original["graph_digest"], "labels": labels,
        "ledger_id": ledger_id(original, labels), "checker": result,
        "named_edges": named_edges(original["graph"], labels),
    }


def normalized(original, labels, t):
    graph = original["graph"]
    require(type(t) is int and t >= 2 and graph["profile"] == profile(t), "prefix profile")
    low = sorted(v for v in labels if labels[v] < 8)
    high = sorted(set(labels) - set(low))
    require(sorted(labels[v] for v in low) == list(range(8))
            and sorted(labels[v] for v in high) == list(range(8, t + 15)), "alpha alphabets")
    require(all((labels[u] < 8) != (labels[v] < 8) for u, v in graph["edges"]), "alpha crossing")
    require([labels[v] for v in (W[0], W[-1], Z)] == [6, 9, 0], "physical ports and zero host")
    state = {"n": t + 15, "p": 8, "x": 6, "y": 1, "low": low, "high": high,
             "L": W[0], "U": W[-1], "z": Z, "witness": W, "distances": witness(graph, W)}
    return certificate(original, labels) | {"t": t, "state": state}


def numerical_contract(k, r, d, port):
    require(type(k) is int and k >= 2, "nonadjacent contract needs K>=2")
    require(r == list(range(8, k + 8)) and d == list(range(1, k + 1))
            and port == k + 9, "nonadjacent inventories or physical port")


def sequence(k):
    bases = {2: (3, 1, 0), 3: (4, 1, 0, 2), 4: (5, 1, 2, 0, 3)}
    if k in bases:
        return bases[k]
    previous = sequence(k - 3)
    return (k + 1, 1, k - 1, *(k - 2 - x for x in previous))


def full(original, source, t, k):
    graph = original["graph"]
    require(graph["profile"] == profile(t, k), "full profile")
    prefix = {v: value if value < 8 else value + k for v, value in source["labels"].items()}
    path = [f"s:{i}" for i in range(4, k + 5)]
    pending = [e for e in graph["edges"] if set(e) - prefix.keys()]
    require(set(graph["vertices"]) - prefix.keys() == set(path[1:])
            and sorted(map(edge_key, pending)) == sorted(map(edge_key, zip(path, path[1:]))),
            "original suffix incidences")
    part = verify_partial(graph, prefix)
    m = t + k + 14
    require(part["valid"] and part["graph_digest"] == original["graph_digest"]
            and part["frontier"] == ["s:4"]
            and part["used_labels"] == list(range(8)) + list(range(k + 8, m + 1))
            and part["used_differences"] == list(range(k + 1, m + 1)), "shifted prefix")
    r, d = part["unused_labels"], part["unused_differences"]
    numerical_contract(k, r, d, prefix["s:4"])
    ck = sequence(k)
    translated = [8 + x for x in ck]
    require(translated[0] == prefix["s:4"] and sorted(translated[1:]) == r, "suffix labels")
    labels = prefix | dict(zip(path[1:], translated[1:], strict=True))
    suffix_weights = [abs(labels[u] - labels[v]) for u, v in zip(path, path[1:])]
    require(sorted(suffix_weights) == d, "suffix differences")
    return certificate(original, labels) | {
        "t": t, "K": k, "source_ledger_id": source["ledger_id"], "prefix": prefix,
        "R": r, "D": d, "partial_checker": part, "port": {"vertex": "s:4", "label": prefix["s:4"]},
        "path": path, "pending": pending, "C_K": ck, "translated_path": translated,
        "suffix_weights": suffix_weights, "witness": W + path[1:],
        "distances": witness(graph, W + path[1:]),
    }


def rejection(operation, expected):
    try:
        operation()
    except ValueError as exc:
        require(str(exc) == expected, "unexpected rule rejection")
        return {"rejected": True, "error": str(exc)}
    raise ValueError("adverse rule unexpectedly accepted")


def adverse(original, baseline, labels):
    graph = original["graph"]
    wrong_digest = verify_certificate(graph, labels, "0" * 64)
    missing = verify_certificate(graph, {v: a for v, a in labels.items() if v != "l:2:0:2"},
                                 original["graph_digest"])
    require(wrong_digest["errors"] == ["original graph digest mismatch"] and not wrong_digest["valid"],
            "wrong digest unexpectedly accepted")
    require(not missing["valid"] and "complete certificate must label every original vertex exactly once"
            in missing["errors"], "missing terminal unexpectedly accepted")
    malformed = deepcopy(graph)
    malformed["edges"].remove([Z, "l:2:0:2"])
    malformed["edges"].append(["s:2", "l:2:0:2"])
    wrong_host = rejection(lambda: growth_incidence(malformed, baseline["graph"], extras(3)),
                           "fresh incidences must attach only to b:2:0")
    wrong_host["checker"] = verify_graph(malformed)
    wrong_host["remove"] = [Z, "l:2:0:2"]
    wrong_host["add"] = ["s:2", "l:2:0:2"]
    require(not wrong_host["checker"]["valid"], "wrong host accepted by original checker")
    return {"wrong_digest": wrong_digest, "missing_terminal": missing, "wrong_host": wrong_host,
            "wrong_exit": rejection(lambda: numerical_contract(2, [8, 9], [1, 2], 10),
                                    "nonadjacent inventories or physical port"),
            "missing_D": rejection(lambda: numerical_contract(2, [8, 9], [1], 11),
                                   "nonadjacent inventories or physical port"),
            "K1": rejection(lambda: numerical_contract(1, [8], [1], 10),
                            "nonadjacent contract needs K>=2") | {"actual_edge_weight": 2}}


def batches(seed, direct):
    comparisons = []
    for partition in ((1, 2), (2, 1)):
        labels, cursor, steps = seed, 2, []
        for size in partition:
            names = [f"l:2:0:{j}" for j in range(cursor, cursor + size)]
            grown = attach(labels, names)
            steps.append({"names": names, "host": Z, "added": {v: grown[v] for v in names}})
            labels = grown
            cursor += size
        require(labels == direct and cursor == 5, "pointwise batch agreement")
        comparisons.append({"partition": partition, "steps": steps, "labels": labels})
    return comparisons


def validate(cfg, started):
    freeze_record = read(HERE / "freeze.json")
    require(not (HERE / "result.json").exists() and not any(HERE.glob("*_certificate.json")),
            "validation outputs already exist")
    for ref in freeze_record["sources"].values():
        require(identity(ref["path"]) == ref, "frozen task source changed")
    seed = archive(cfg, "p2_original")
    retained = archive(cfg, "d066_certificates")["prefix"]
    require(retained["labels"] == SEED and retained["graph_digest"] == seed["graph_digest"],
            "D066 literal named seed binding")
    p2 = normalized(seed, SEED, 2)
    require(all(p2[key] == retained[key] for key in retained), "D066 archived certificate mismatch")
    put("p2_certificate.json", p2 | {"original": cfg["retained"]["p2_original"]})
    prefixes = {2: p2}
    for t in P_CASES:
        require(process_time() - started + freeze_record["cpu_seconds"] < LIMITS["cpu_seconds"],
                "combined producer CPU cap")
        name = case_name(t, 0)
        ref = freeze_record["records"][name]
        original = frozen(ref)
        growth_incidence(original["graph"], seed["graph"], extras(t))
        labels = attach(SEED, extras(t))
        require(all(labels[f"l:2:0:{j}"] == 15 + j for j in range(2, t)), "named formula")
        prefixes[t] = normalized(original, labels, t)
        put(name + "_certificate.json", prefixes[t] | {"original": ref, "seed_ledger_id": p2["ledger_id"]})
    for t, k in ((2, 2), *T_CASES):
        require(process_time() - started + freeze_record["cpu_seconds"] < LIMITS["cpu_seconds"],
                "combined producer CPU cap")
        name = case_name(t, k)
        ref = cfg["retained"]["t22_original"] if t == 2 else freeze_record["records"][name]
        record = full(frozen(ref), prefixes[t], t, k)
        if t == 2:
            old = archive(cfg, "d067_k2")
            require(all(record[key] == old[key] for key in ("labels", "named_edges", "checker", "prefix",
                         "R", "D", "path", "graph_digest")), "D067 original-bound control mismatch")
        put(name + "_certificate.json", record | {"original": ref})
    p3 = frozen(freeze_record["records"]["p3"])
    put("adverse.json", adverse(p3, seed, prefixes[3]["labels"]))
    put("batches.json", batches(SEED, prefixes[5]["labels"]))
    elapsed = process_time() - started
    require(elapsed + freeze_record["cpu_seconds"] < LIMITS["cpu_seconds"], "combined producer CPU cap")
    put("result.json", {"status": "PASS", "retained": 2, "prefixes": 4, "targets": 4,
                        "complete_checks": 10, "adverse_rejections": 6, "batch_partitions": 2,
                        "queries": 0, "nodes": 0, "retries": 0, "cpu_seconds": elapsed})


if __name__ == "__main__":
    cfg = read(HERE / "config.json")
    check_config(cfg)
    require(sys.argv[1:] in (["freeze"], ["validate"]), "choose one phase")
    (freeze if sys.argv[1] == "freeze" else validate)(cfg, START)
    print(f"{sys.argv[1]} PASS")
