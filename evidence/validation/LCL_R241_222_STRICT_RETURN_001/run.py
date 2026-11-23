"""D082 exact pinned named enumeration and read-only D081 controls."""

from time import process_time

START = process_time()

from hashlib import sha256
from itertools import permutations, product
import json
from math import factorial
from pathlib import Path
import subprocess
import sys

from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate, verify_partial

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads((HERE / path).read_bytes())


def raw_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def write(name, value):
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    existing = sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())
    need(len(data) <= 2_000_000 and existing + len(data) <= 8_000_000, "evidence byte cap")
    with (HERE / name).open("xb") as stream:
        stream.write(data)


def identity(config):
    folder = HERE.relative_to(ROOT).as_posix()
    paths = list(config["intake_sources"]) + config["new_sources"] + [
        f"{folder}/{name}" for name in ("INTAKE.md", "config.json", "commands.json", "run.py", "audit.py", "driver.py")]
    source_hashes = {p: raw_hash(ROOT / p) for p in sorted(paths)}
    need(all(source_hashes[p] == value for p, value in config["intake_sources"].items()), "intake source bytes")
    spec = config["specification"]
    need(source_hashes[spec["path"]] == spec["sha256"], "task specification bytes")
    return {"parent": config["parent"], "source_hashes": source_hashes, "runtime": {
        "path": Path(sys.executable).relative_to(ROOT).as_posix(), "version": sys.version,
        "sha256": raw_hash(Path(sys.executable))}}


def certificate(original, labels):
    need(process_time()-START < 25, "producer CPU reserve")
    digest = original["graph_digest"]
    graph = original["graph"]
    report = verify_certificate(graph, labels, digest)
    need(report["valid"] and report["graph_digest"] == digest, str(report["errors"]))
    payload = {"graph_digest": digest, "labels": sorted(labels.items())}
    ledger = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"graph_digest": digest, "ledger_id": ledger, "labels": labels, "checker": report,
            "edge_rows": [[u, v, abs(labels[u]-labels[v])] for u, v in graph["edges"]]}


def verify_original_ports(graph, B, A, next_labels):
    u, v = B["ports"][-1], A["ports"][0]
    old = B["labels"]
    need(u in graph["spine"] and v in graph["spine"]
         and graph["spine"].index(v) == graph["spine"].index(u)+1, "ports on original spine")
    need(not old.keys() & next_labels.keys(), "disjoint original port blocks")
    edges = [[s, t] for s, t in graph["edges"]
             if (s in old and t in next_labels) or (t in old and s in next_labels)]
    need(edges == [[u, v]], "exact physical connector")
    need(old[u]-B["P"] == next_labels[v], "R241 physical offset mismatch")


def verify_suffix_inventory(original, saved, declared):
    graph = original["graph"]
    assigned = saved["assigned"]
    path = saved["path"]
    length = len(path)-1
    p = saved["partial_checker"]["unused_labels"][0]
    pending = [e for e in graph["edges"] if any(v not in assigned for v in e)]
    need(pending == [list(edge) for edge in zip(path, path[1:])], "exact original suffix edge path")
    need(set(graph["vertices"]) - assigned.keys() == set(path[1:]), "exact pending original names")
    checked = verify_partial(graph, assigned)
    need(checked == saved["partial_checker"] and checked["valid"] and
         checked["graph_digest"] == original["graph_digest"], "actual original partial")
    need(checked["frontier"] == [path[0]] and assigned[path[0]] == p+length+1, "actual exit label")
    need(checked["unused_labels"] == list(range(p, p+length)), "exact suffix label inventory")
    need(checked["unused_differences"] == declared == list(range(1,length+1)), "wrong suffix difference inventory")


def reject(operation, reason, *args):
    try:
        operation(*args)
    except ValueError as exc:
        need(str(exc) == reason, "wrong adverse failure")
        return {"valid": False, "reason": str(exc)}
    raise ValueError("adverse input accepted")


def controls(config):
    folder = ROOT / config["archive"]
    manifest = read(folder / "MANIFEST.json")
    names = ("f2_original.json", "unequal_original.json", "repeat_l5_original.json",
             "certificates.json", "unequal_strict_enumeration.json", "audit_result.json")
    members = {row["path"]: row["sha256"] for row in manifest["files"]}
    for name in names:
        need(raw_hash(folder / name) == members[name], "D081 manifest binding")
    archived = read(folder / "certificates.json")["controls"]
    f2 = read(folder / "f2_original.json")
    good = certificate(f2, archived["f2"]["labels"])
    need(all(good[k] == archived["f2"][k] for k in good), "D081 positive exact certificate")
    labels = good["labels"]
    need(f2["graph"]["profile"] == [[1,2],[2]] and [labels["s:0"],labels["s:1"]] == [1,5]
         and all((labels[u] < 5) != (labels[v] < 5) for u, v in f2["graph"]["edges"]), "D081 positive port")

    earlier = read(folder / "unequal_original.json")
    negative = read(folder / "unequal_strict_enumeration.json")
    audit = read(folder / "audit_result.json")
    need(earlier["graph"]["profile"] == [[1,2],[1]] and negative["pins"] == {"s:0":1,"s:1":5}
         and negative["graph_digest"] == earlier["graph_digest"], "D081 negative original and pins")
    need(negative["status"] == "COMPLETE" and len(negative["rows"]) == negative["visits"] == 144
         and negative["positive"] == [] and audit["status"] == "PASS"
         and audit["counts"]["unequal_strict"] == [0,144], "D081 retained exact negative")
    need(audit["raw_receipts"]["unequal_strict_enumeration.json"] == members["unequal_strict_enumeration.json"],
         "D081 audited negative identity")

    wrong = verify_certificate(f2["graph"], labels, "0"*64)
    need(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "wrong expected digest")
    repeated = read(folder / "repeat_l5_original.json")
    saved = archived["repeat_l5"]
    need(saved["graph_digest"] == repeated["graph_digest"], "retained repeated original")
    block = saved["macros"][0]
    B, A = block["F"], block["H"]
    v, leaf = A["ports"][0], "l:2:0:0"
    incoming = A["labels"]
    need((incoming[v], incoming[leaf]) == (0,1), "retained incoming state")
    corrupted = incoming | {v: incoming[leaf], leaf: incoming[v]}
    mismatch = reject(verify_original_ports, "R241 physical offset mismatch", repeated["graph"], B, A, corrupted)
    suffix = saved["suffix"]
    incorrect = [2,3,4,5]
    bad_d = reject(verify_suffix_inventory, "wrong suffix difference inventory", repeated, suffix, incorrect)
    record = {"positive": good | {"offsets": [1,0], "source": names[0]},
              "negative": {"graph_digest": earlier["graph_digest"], "pins": negative["pins"],
                           "positive": 0, "historical_visits": 144, "new_visits": 0,
                           "source": names[4], "auditor": names[5]},
              "adverse": {"digest": {"graph_id": "f2", "expected": "0"*64, "checker": wrong},
                          "offset": mismatch | {"graph_digest": repeated["graph_digest"],
                              "connector": [B["ports"][-1], v], "swap": [v,leaf],
                              "new_entrance_label": corrupted[v], "old_exit_offset": B["offsets"][-1]},
                          "difference": bad_d | {"graph_digest": repeated["graph_digest"],
                              "port": suffix["port"], "declared_d": incorrect,
                              "actual_d": suffix["partial_checker"]["unused_differences"]}}}
    write("controls.json", record)


def enumerate_pinned(original, config):
    graph = original["graph"]
    cut = config["cut"]
    pins = config["pins"]
    # Read class parity directly from named role depth along the physical spine.
    level = {"spine": 0, "branch": 1, "leaf": 2}
    side = {v: (role["section"]+level[role["kind"]]) % 2 for v, role in graph["roles"].items()}
    need(side["s:0"] == 0 and side["s:1"] == 1, "physical orientation")
    need(sum(s == 0 for s in side.values()) == cut and all(side[u] != side[v] for u, v in graph["edges"]),
         "exact alpha cut")
    names = [[v for v in graph["vertices"] if side[v] == k and v not in pins] for k in (0,1)]
    bands = [sorted(set(band)-set(pins.values())) for band in (range(cut), range(cut,len(side)))]
    budget = config["limits"]["visits"]
    need(factorial(len(bands[0]))*factorial(len(bands[1])) == budget, "exact named product")
    rows, positives = [], []
    status = "INCOMPLETE"
    try:
        for low, high in product(permutations(bands[0]), permutations(bands[1])):
            rank = len(rows)
            need(rank < budget and process_time()-START < 25, "diagnostic cap")
            labels = pins | dict(zip(names[0], low, strict=True)) | dict(zip(names[1], high, strict=True))
            seen = {}
            repeat = None
            for i, (u, v) in enumerate(graph["edges"]):
                w = abs(labels[u]-labels[v])
                if w in seen:
                    repeat = [seen[w], i, w]
                    break
                seen[w] = i
            rows.append([rank, low, high, repeat])
            if repeat is None:
                positives.append({"rank": rank, "certificate": certificate(original, labels)})
        need(len(rows) == budget, "incomplete product")
        status = "COMPLETE"
    finally:
        write("enumeration.json", {"graph_digest": original["graph_digest"], "pins": pins, "cut": cut,
               "free_names": names, "free_labels": bands, "visits": len(rows), "status": status,
               "positive": positives, "rows": rows})
    return len(rows), len(positives)


def main():
    config = read("config.json")
    need(Path.cwd() == ROOT and sys.version_info[:2] in ((3,12),(3,13)), "project Python")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    need(head == config["parent"], "expected accepted parent")
    write("identity.json", identity(config))
    graph = build_graph(config["profile"])
    write("strict_original.json", {"graph": graph, "graph_digest": graph_digest(graph)})
    original = read("strict_original.json")
    controls(config)
    visits, positive = enumerate_pinned(original, config)
    write("result.json", {"status": "COMPLETE", "new_originals": 1, "visits": visits, "positive": positive,
                          "adverse_rejections": 3, "retained_replay_visits": 0,
                          "solver_calls": 0, "process_cpu_seconds": process_time()-START})


if __name__ == "__main__":
    main()
