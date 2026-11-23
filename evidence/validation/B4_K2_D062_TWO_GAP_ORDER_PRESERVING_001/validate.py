"""Deterministic two-gap continuation on a retained original."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if Path.cwd() != ROOT:
    raise SystemExit("Run from the repository root.")
sys.path.insert(0, str(ROOT))

from lcl.verify import verify_certificate, verify_graph

PARENT = "b0303b9be3ba70de0936e9b942f8044c70a49938"
TARGET_DIGEST = "c5fd852e27ca85602e9a5a2cb39e3b14434b2783272c57523c2c1b7a317859f4"
PROFILE = [[2], [2], [2], [2], [], [], []]
ALPHABET = list(range(19))
DIFFERENCES = list(range(1, 19))
PENDING = [["s:4", "s:5"], ["s:5", "s:6"]]
OUTPUTS = ("freeze.json", "controls.json", "cases.jsonl", "result.json", "audit_result.json")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def save(name, data, cap):
    payload = json.dumps(data, indent=2, sort_keys=True).encode() + b"\n"
    require(len(payload) <= cap, f"record too large: {name}")
    with (HERE / name).open("xb") as out:
        out.write(payload)


def source(config, key):
    return read(ROOT / config["sources"][key]["path"])


def bindings(config):
    archive = {ref["path"]: ref["sha256"] for ref in config["sources"].values()}
    actual = {path: digest(ROOT / path) for path in archive}
    require(actual == archive, "archived input byte mismatch")
    production = {path: digest(ROOT / path) for path in config["production_sha256"]}
    require(production == config["production_sha256"], "production input byte mismatch")
    task = {name: digest(HERE / name) for name in ("validate.py", "audit.py", "commands.json", "config.json")}
    return {"archive": actual, "production": production, "task": task}


def original(config):
    retained = source(config, "target")
    graph = retained["graph"]
    receipt = verify_graph(graph)
    require(receipt["valid"] and retained["graph_digest"] == receipt["graph_digest"] == TARGET_DIGEST
            and (receipt["n"], receipt["m"]) == (19, 18) and graph["profile"] == PROFILE, "exact original")
    return graph, receipt


def positive_controls(config):
    core = source(config, "core_original")
    cert = source(config, "core_certificate")
    checked = verify_certificate(core["graph"], cert["labels"], core["graph_digest"])
    require(checked == cert["checker"] and checked["valid"], "archived D061 core certificate")
    labels = {name: value+1 for name, value in cert["labels"].items()}
    labels.update({"b:2:0": 0, "l:2:0:0": 16, "l:2:0:1": 17})
    k1 = source(config, "k1_original")
    checked_k1 = verify_certificate(k1["graph"], labels, k1["graph_digest"])
    old = source(config, "d063_controls")["k1"]
    require(checked_k1["valid"] and (checked_k1["n"], checked_k1["m"]) == (18,17)
            and old["labels"] == labels and old["checker"] == checked_k1 and labels["s:5"] == 11, "D062 lift certificate")
    status = source(config, "d063_validation")
    require(status["status"] == "EXHAUSTED_RESTRICTED_NEGATIVE" and status["full_candidates"] == 38
            and status["candidates_sha256"] == config["sources"]["d063_log"]["sha256"], "archived D063 outcome")
    return labels, {"D061": checked, "D062_K1": {"labels": labels, "checker": checked_k1}, "D063": status}


def edge_values(edges, labels):
    return [abs(labels[u]-labels[v]) for u,v in edges]


def inventory(weights):
    multiplicity = Counter(weights)
    return {"missing": [d for d in DIFFERENCES if not multiplicity[d]],
            "repeated": [[d,n] for d,n in sorted(multiplicity.items()) if n>1]}


def check(config, limits, frozen, started):
    graph, graph_receipt = original(config)
    require(frozen["inputs"] == bindings(config) and frozen["target"] == config["sources"]["target"]
            and frozen["graph"] == graph_receipt, "frozen input identity")
    labels, control = positive_controls(config)
    scan = [v for v in sorted(labels, key=labels.__getitem__) if v != "s:5"]
    require(len(scan) == 17 and [labels[v] for v in scan] == list(range(11))+list(range(12,18)),
            "D062 prefix rank")
    assigned = [e for e in graph["edges"] if set(e)<=set(scan)]
    pending = [e for e in graph["edges"] if e not in assigned]
    require(pending == PENDING and len(assigned)==16
            and set(graph["vertices"])-set(scan)=={"s:5","s:6"}, "actual pending path")
    empty_ok = verify_certificate(graph, {}, TARGET_DIGEST)
    wrong = verify_certificate(graph, {}, "0"*64)
    require(not wrong["valid"] and wrong["errors"] == empty_ok["errors"] + ["original graph digest mismatch"],
            "wrong-original digest control")
    control.update({"wrong_digest": {"input_labels": {}, "reference": empty_ok, "expected": "0"*64, "observed": wrong},
                    "prefix_rank": scan, "assigned_edges": assigned, "pending_edges": pending,
                    "original_edge_order": graph["edges"]})
    save("controls.json", control, limits["max_record_bytes"])
    witnesses = []
    valid_prefixes = 0
    cases = 0
    pairs = 0
    size = 0
    unique = set()
    with (HERE / "cases.jsonl").open("xb") as log:
        for a,b in combinations(ALPHABET,2):
            pairs += 1
            require(pairs<=limits["pairs"], "pair cap")
            prefix = dict(zip(scan, (v for v in ALPHABET if v not in (a,b)), strict=True))
            R = sorted(set(ALPHABET)-set(prefix.values()))
            weights = edge_values(assigned,prefix)
            missing = inventory(weights)
            valid_prefix = not missing["repeated"]
            require(R==[a,b] and len(weights)==16 and min(weights)>=1 and max(weights)<=18, "prefix inventories")
            valid_prefixes += valid_prefix
            outputs = {}
            for order,s5,s6 in (("A",a,b),("B",b,a)):
                cases += 1
                require(cases<=limits["cases"], "case cap")
                f = {**prefix,"s:5":s5,"s:6":s6}
                unique.add(tuple(f[v] for v in graph["vertices"]))
                ds = edge_values(graph["edges"],f)
                tail = edge_values(pending,f)
                full = inventory(ds)
                ck = verify_certificate(graph,f,TARGET_DIGEST)
                good = sorted(ds)==DIFFERENCES
                require(sorted(f.values())==ALPHABET and ck["graph_digest"]==TARGET_DIGEST
                        and ds==ck["edge_differences"] and ck["valid"] is good
                        and good==(valid_prefix and sorted(tail)==missing["missing"]), "candidate checker disagreement")
                if good:
                    witnesses.append([a,b,order])
                outputs[order] = {"suffix_labels":[s5,s6],"suffix_weights":tail,"inventory":full,"checker":ck}
            row = {"R":R,"D":missing["missing"],"prefix_repeated":missing["repeated"],"valid_prefix":valid_prefix,
                   "prefix":prefix,"prefix_weights":weights,"port":["s:4",prefix["s:4"]],"orders":outputs}
            entry = json.dumps(row,sort_keys=True,separators=(",",":")).encode()+b"\n"
            size += len(entry)
            require(size<=limits["max_record_bytes"], "raw case log byte cap")
            log.write(entry)
            log.flush()
            require(frozen["cpu_seconds"]+process_time()-started<=limits["max_cpu_seconds"], "CPU cap")
        os.fsync(log.fileno())
    require((pairs,cases)==(171,342), "complete grid")
    result = {"status":"VERIFIED_WITNESS" if witnesses else "EXHAUSTED_RESTRICTED_NEGATIVE",
              "grid_complete":True,"pairs":pairs,"full_cases":cases,"distinct_full_maps":len(unique),
              "valid_prefixes":valid_prefixes,"witnesses":witnesses,"solver_queries":0,"new_graph_identities":0,
              "cpu_seconds":process_time()-started,"cases_sha256":digest(HERE/"cases.jsonl")}
    save("result.json",result,limits["max_record_bytes"])
    print(f"Checked {pairs} pairs and {cases} full cases. Witnesses: {witnesses}.")


def main():
    started = process_time()
    require(sys.version_info[:2] in {(3,12),(3,13)}, "project Python 3.12 or 3.13")
    config = read(HERE/"config.json")
    limits = config["limits"]
    model = config["model"]
    require(model == {"label_range":[0,18],"prefix_rank":"increasing D062 F labels with s:5 withheld",
                      "suffix":["s:5","s:6"],"orders":{"A":["a","b"],"B":["b","a"]},"apply_prefilter":False}
            and model["apply_prefilter"] is False, "exact order-preserving model")
    require(config["parent"] == PARENT and config["target_digest"] == TARGET_DIGEST and config["profile"] == PROFILE
            and config["parameters"] == [2]*4
            and all(type(x) is int for x in [*limits.values(),*config["parameters"],
                                             *model["label_range"],
                                             *(x for section in config["profile"] for x in section)]), "frozen domain")
    require(limits==dict(workers=1,pairs=171,cases=342,max_order=19,new_graph_identities=0,solver_queries=0,
                         max_cpu_seconds=30,max_record_bytes=2000000,max_evidence_bytes=10000000,retries=0),"frozen limits")
    require(len(sys.argv)==2 and sys.argv[1] in ("freeze","check"), "select freeze or check")
    if sys.argv[1]=="freeze":
        require(not any((HERE/p).exists() for p in OUTPUTS), "occupied output path")
        require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()==PARENT,"starting checkpoint")
        source_hashes = bindings(config)
        _, graph_receipt = original(config)
        save("freeze.json",{"parent":PARENT,"target":config["sources"]["target"],"graph":graph_receipt,
                            "inputs":source_hashes,"new_graph_identities":0,"cpu_seconds":process_time()-started,
                            "runtime":{"version":sys.version,"implementation":sys.implementation.name,
                                       "platform":sys.platform,"utf8_mode":sys.flags.utf8_mode}},limits["max_record_bytes"])
        print("Bound the existing 19-vertex original. No new graph identity.")
    else:
        require(not any((HERE/p).exists() for p in OUTPUTS[1:]), "occupied candidate output path")
        check(config,limits,read(HERE/"freeze.json"),started)


if __name__ == "__main__":
    main()
