"""Supply and verify the nine authorized original targets. No search."""

from time import process_time

START = process_time()
CPU_RESERVE = 5

from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONFIG_PATH = HERE / "config.json"


def need(predicate, reason):
    if not predicate:
        raise ValueError(reason)


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def write(name, data):
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
    need(len(raw) <= 2_000_000 and total + len(raw) <= 10_000_000, "evidence byte cap")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)


def edge_rows(graph, labels):
    return [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]
            if u in labels and v in labels]


def ledger_id(digest, labels):
    payload = {"graph_digest": digest, "labels": sorted(labels.items())}
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def state(graph, labels, p, entrance, exit_name, witness):
    rows = edge_rows(graph, labels)
    n = len(labels)
    need(sorted(labels.values()) == list(range(n)), "normalized label alphabet")
    need(sorted(d for _, _, d in rows) == list(range(1, n)), "normalized difference alphabet")
    need(all((labels[u] < p) != (labels[v] < p) for u, v, _ in rows), "alpha edge cut")
    need(witness[0] == entrance and witness[-1] == exit_name and
         len(set(witness)) == len(witness), "actual witness endpoints")
    adjacent = {v: set() for v in labels}
    for u, v, _ in rows:
        adjacent[u].add(v)
        adjacent[v].add(u)
    need(all(v in adjacent[u] for u, v in zip(witness, witness[1:])), "witness edges")
    queue = deque(witness)
    distance = dict.fromkeys(witness, 0)
    while queue:
        u = queue.popleft()
        for v in adjacent[u] - distance.keys():
            distance[v] = distance[u] + 1
            queue.append(v)
    need(len(distance) == n and max(distance.values()) <= 2, "witness distances")
    x, y = labels[entrance], labels[exit_name]-p
    need(0 <= x < p and 0 <= y < n-p, "physical port classes")
    return {"N": n, "P": p, "x": x, "y": y, "entrance": entrance, "exit": exit_name,
            "entrance_label": labels[entrance], "exit_label": labels[exit_name],
            "labels": labels, "low": sorted(v for v in labels if labels[v] < p),
            "high": sorted(v for v in labels if labels[v] >= p), "edge_rows": rows,
            "witness": witness, "distance": distance}


def starter(graph, a):
    labels = {"b:0:0": 0, "s:0": 2}
    labels.update({f"l:0:0:{j}": 1 if j == 0 else j+2 for j in range(a)})
    return state(graph, labels, 1, "b:0:0", "s:0", ["b:0:0", "s:0"])


def pair(graph, i, a, b):
    entrance, exit_name = f"s:{i}", f"s:{i+1}"
    p = a+2
    labels = {entrance: 1, exit_name: p+1, f"b:{i}:0": p, f"b:{i+1}:0": 0}
    labels.update({f"l:{i}:0:{j}": j+2 for j in range(a)})
    labels.update({f"l:{i+1}:0:{j}": p+2+j for j in range(b)})
    return state(graph, labels, p, entrance, exit_name, [entrance, exit_name])


def require_matching_ports(previous, module):
    outgoing = previous["labels"][previous["exit"]] - previous["P"]
    incoming = module["labels"][module["entrance"]]
    need(outgoing == incoming, "R241 offset mismatch")
    return outgoing


def join(graph, previous, module, i):
    offset = require_matching_ports(previous, module)
    left, right = previous["labels"], module["labels"]
    need(not (left.keys() & right.keys()), "disjoint R241 vertices")
    connector = [f"s:{i-1}", f"s:{i}"]
    need([previous["exit"], module["entrance"]] == connector, "original R241 ports")
    crossing = [[u, v] for u, v in graph["edges"]
                if (u in left and v in right) or (v in left and u in right)]
    need(crossing == [connector], "exact original connector")
    p, size = previous["P"], module["N"]
    labels = {v: a + (size if a >= p else 0) for v, a in left.items()}
    labels.update({v: a+p for v, a in right.items()})
    combined = state(graph, labels, p+module["P"], previous["entrance"], module["exit"],
                     previous["witness"] + module["witness"])
    u, v = connector
    detail = {"edge": connector, "matched_offset": offset, "weight": labels[u]-labels[v],
              "previous_exit_before": left[u], "incoming_before": right[v],
              "previous_exit_after": labels[u], "incoming_after": labels[v],
              "previous_low_size": p, "module_order": size}
    need(detail["weight"] == size, "R241 connector weight")
    return combined, detail


def prefix(graph, quotas):
    n = len(quotas)
    first_length = 1 if n % 2 else 2
    first = starter(graph, quotas[0]) if n % 2 else pair(graph, 0, *quotas[:2])
    aggregate = first
    trace = [{"module": first, "aggregate": aggregate, "connector": None}]
    for i in range(first_length, n, 2):
        module = pair(graph, i, *quotas[i:i+2])
        aggregate, receipt = join(graph, aggregate, module, i)
        trace.append({"module": module, "aggregate": aggregate, "connector": receipt})
    return aggregate, trace


def recurrence(L):
    bases = {2: [3, 1, 0], 3: [4, 1, 0, 2], 4: [5, 1, 2, 0, 3]}
    if L in bases:
        return bases[L]
    return [L+1, 1, L-1] + [L-2-x for x in recurrence(L-3)]


def suffix_contract(original, shifted, p, path, declared_d):
    graph = original["graph"]
    pending = [edge for edge in graph["edges"] if any(v not in shifted for v in edge)]
    need(set(graph["vertices"]) - shifted.keys() == set(path[1:]) and
         Counter(tuple(sorted(e)) for e in pending) ==
         Counter(tuple(sorted(e)) for e in zip(path, path[1:])), "actual original suffix")
    partial = verify_partial(graph, shifted)
    L = len(path)-1
    need(partial["valid"] and partial["graph_digest"] == original["graph_digest"] and
         partial["frontier"] == [path[0]] and shifted[path[0]] == p+L+1, "actual shifted exit")
    need(partial["unused_labels"] == list(range(p, p+L)), "exact suffix label inventory")
    need(partial["unused_differences"] == declared_d == list(range(1, L+1)),
         "exact suffix difference inventory")
    return {"partial": partial, "path": path, "pending_edges": pending,
            "crossing": [path[:2]], "port": [path[0], shifted[path[0]]]}


def complete(original, quotas, L):
    graph = original["graph"]
    n = len(quotas)
    alpha, trace = prefix(graph, quotas)
    p = alpha["P"]
    shifted = {v: a + (L if a >= p else 0) for v, a in alpha["labels"].items()}
    path = graph["spine"][n-1:]
    suffix = suffix_contract(original, shifted, p, path, list(range(1, L+1)))
    sequence = [p+x for x in recurrence(L)]
    need(sequence[0] == shifted[path[0]] and len(sequence) == len(path), "consumer sequence")
    labels = shifted | dict(zip(path[1:], sequence[1:]))
    digest = original["graph_digest"]
    checker = verify_certificate(graph, labels, digest)
    need(checker["valid"] and checker["graph_digest"] == digest, str(checker["errors"]))
    return {"trace": trace, "shifted": shifted, "suffix": suffix, "sequence": sequence,
            "labels": labels, "edge_rows": edge_rows(graph, labels), "graph_digest": digest,
            "ledger_id": ledger_id(digest, labels), "checker": checker}


def adverse_controls(original, t4):
    graph = original["graph"]
    changed, substitute = ["s:1", "s:2"], ["s:0", "s:2"]
    wrong = graph | {"edges": [substitute if edge == changed else edge for edge in graph["edges"]]}
    checker = verify_certificate(wrong, t4["labels"], original["graph_digest"])
    need(not checker["valid"] and {"actual named edges do not match the original profile",
                                 "original graph digest mismatch"} <= set(checker["errors"]),
         "substituted connector not rejected")
    b, a = t4["trace"]
    outgoing, incoming = b["aggregate"], a["module"]
    old = incoming["labels"]
    # Swap two low values only in memory to make the incoming label zero.
    other = next(v for v, x in old.items() if x == 0)
    modified = incoming | {"labels": old | {incoming["entrance"]: 0, other: 1}}
    reasons = {}
    probes = [("port", "R241 offset mismatch", require_matching_ports, (outgoing, modified)),
              ("differences", "exact suffix difference inventory", suffix_contract,
               (original, t4["shifted"], a["aggregate"]["P"], t4["suffix"]["path"], [2]))]
    for key, expected, operation, args in probes:
        try:
            operation(*args)
        except ValueError as exc:
            need(str(exc) == expected, "unexpected adverse outcome")
            reasons[key] = str(exc)
        else:
            raise ValueError("accepted an adverse probe")
    return {"connector": {"removed": changed, "substituted": substitute, "checker": checker,
                          "expected_graph_digest": original["graph_digest"]},
            "port": {"exit": outgoing["exit"], "incoming": incoming["entrance"],
                     "swapped_with": other, "y_B": outgoing["y"], "x_A": 0,
                     "reason": reasons["port"], "rejected": True},
            "differences": {"declared": [2], "actual": [1, 2],
                            "reason": reasons["differences"], "rejected": True}}


def provenance(config):
    paths = (config["sources"] + list(config["retained"].values())
             + [config["documents"][x]["path"] for x in ("roadmap", "task")]
             + [config["documents"][x] for x in ("proof", "preliminary_handoff")])
    paths += [(HERE / f).relative_to(ROOT).as_posix()
              for f in ("config.json", "run.py", "audit.py", "driver.py", "commands.json")]
    hashes = {p: raw_hash(ROOT / p) for p in sorted(paths)}
    for name in ("roadmap", "task"):
        entry = config["documents"][name]
        need(hashes[entry["path"]] == entry["sha256"], "immutable attachment identity")
    return {"raw_sources": hashes,
            "runtime": {"version": sys.version, "path": Path(sys.executable).relative_to(ROOT).as_posix(),
                        "sha256": raw_hash(Path(sys.executable))},
            "strategy_parent": config["strategy_parent"]}


def main():
    config = read(CONFIG_PATH)
    need(Path.cwd() == ROOT and sys.version_info[:2] in ((3, 12), (3, 13)), "root/runtime")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    need(head == config["strategy_parent"], "fixed strategy parent")
    write("identity.json", provenance(config))
    retained = config["retained"]
    original_path = ROOT / retained["original"]
    retained_original = read(original_path)
    t4_path = ROOT / retained["t4_original"]
    t4_original = read(t4_path)
    t4_manifest_row = read(ROOT / retained["t4_manifest"])["files"]["validation/lift-t2-original.json"]
    need(raw_hash(t4_path) == t4_manifest_row["sha256"], "D060 archive byte identity")
    old = read(ROOT / retained["certificates"])["targets"]["2"]
    manifest_rows = {row["path"]: row for row in read(ROOT / retained["manifest"])["files"]}
    for source in (original_path, ROOT / retained["certificates"]):
        need(raw_hash(source) == manifest_rows[source.name]["sha256"], "D076 archive byte identity")
    original_digests = []
    for case, quotas, L in config["grid"]:
        need(process_time() - START < config["limits"]["process_cpu_seconds"] - CPU_RESERVE,
             "producer CPU reserve reached")
        need(type(L) is int and L >= 2 and quotas and
             all(type(a) is int and a >= 0 for a in quotas) and
             (len(quotas) % 2 == 0 or quotas[0] > 0), "stated quota/suffix domain")
        profile = [[a] for a in quotas] + [[] for _ in range(L)]
        if case in ("T4", "T5"):
            original, path = (t4_original, t4_path) if case == "T4" else (retained_original, original_path)
            need(original["graph"]["profile"] == profile and
                 original["graph_digest"] == graph_digest(original["graph"]), "retained original")
            reference = {"path": path.relative_to(ROOT).as_posix(), "sha256": raw_hash(path)}
        else:
            graph = build_graph(profile)
            name = f"{case}_original.json"
            write(name, {"graph": graph, "graph_digest": graph_digest(graph)})
            original = read(HERE / name)
            reference = {"path": (HERE / name).relative_to(ROOT).as_posix(), "sha256": raw_hash(HERE / name)}
        original_digests.append(original["graph_digest"])
        record = complete(original, quotas, L)
        record["original"] = reference
        if case == "T5":
            need(record["graph_digest"] == old["graph_digest"] and
                 record["ledger_id"] != old["ledger_id"], "distinct co-original ledger")
            record["retained_co_original"] = {"ledger_id": old["ledger_id"], "source": retained["certificates"]}
        write(f"{case}_certificate.json", record)
        if case == "T4":
            write("adverse.json", adverse_controls(original, record))
    need(len(set(original_digests)) == len(config["grid"]) == 9, "exact grid accounting")
    write("result.json", {"status": "PASS", "complete_certificates": 9, "new_originals": 7,
                          "retained_originals": 2, "adverse": 3, "search_calls": 0,
                          "assignment_nodes": 0, "historical_replays": 0,
                          "process_cpu_seconds": process_time() - START})


if __name__ == "__main__":
    main()
