"""Check both adjacent-exit rank templates on the retained original."""
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

PARENT = "af9077e17bb720fb9da268d4dcb72f801ea41ccf"
TARGET_DIGEST = "c5fd852e27ca85602e9a5a2cb39e3b14434b2783272c57523c2c1b7a317859f4"
PROFILE = [[2], [2], [2], [2], [], [], []]
ALPHABET = list(range(19))
DIFFERENCES = list(range(1, 19))
PENDING = [["s:4", "s:5"], ["s:5", "s:6"]]
OUTPUTS = ("freeze.json", "controls.json", "cases-L.jsonl", "cases-R.jsonl", "result.json", "audit_result.json")


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
    task = {name: digest(HERE / name) for name in ("validate.py", "audit.py", "commands.json", "config.json", "pre-run.md")}
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


def check_templates(config, limits, frozen, started):
    graph, graph_receipt = original(config)
    require(frozen["inputs"] == bindings(config) and frozen["target"] == config["sources"]["target"]
            and frozen["graph"] == graph_receipt, "frozen input identity")
    labels, control = positive_controls(config)
    scan = [v for v in sorted(labels, key=labels.__getitem__) if v != "s:5"]
    previous = source(config, "d064_validation")
    require(scan == config["model"]["base_prefix_rank"] == source(config, "d064_controls")["prefix_rank"]
            and [labels[v] for v in scan] == list(range(11))+list(range(12,18)), "exact D062/D064 ranks")
    require(previous["status"] == "EXHAUSTED_RESTRICTED_NEGATIVE" and previous["full_cases"] == 342
            and previous["cases_sha256"] == config["sources"]["d064_log"]["sha256"], "retained D064 receipt")
    prefix_names = set(scan)
    assigned = [e for e in graph["edges"] if prefix_names.issuperset(e)]
    pending = [e for e in graph["edges"] if e not in assigned]
    require(pending == PENDING and len(assigned) == 16
            and set(graph["vertices"]) - prefix_names == {"s:5","s:6"}, "actual pending path")
    empty_ok = verify_certificate(graph, {}, TARGET_DIGEST)
    wrong = verify_certificate(graph, {}, "0"*64)
    require(not wrong["valid"] and wrong["errors"] == empty_ok["errors"] + ["original graph digest mismatch"],
            "wrong-original digest control")
    k1 = source(config, "k1_original")
    invalid_labels = dict(labels, **{"s:5":labels["s:4"]})
    invalid = verify_certificate(k1["graph"], invalid_labels, k1["graph_digest"])
    require(not invalid["valid"] and "vertex labels repeat" in invalid["errors"]
            and invalid["edge_differences"][4] == 0, "invalid label and edge control")
    templates = {}
    for template, (i,j) in config["model"]["templates"].items():
        ranks = scan.copy()
        ranks[i],ranks[j] = ranks[j],ranks[i]
        templates[template] = ranks
    control.update({"D064":previous,
                    "wrong_digest":{"input_labels":{},"reference":empty_ok,"expected":"0"*64,"observed":wrong},
                    "invalid_label":{"labels":invalid_labels,"checker":invalid},
                    "prefix_rank":scan,"templates":templates,"assigned_edges":assigned,"pending_edges":pending,
                    "original_edge_order":graph["edges"]})
    save("controls.json", control, limits["max_record_bytes"])

    summary = {}
    unique = set()
    for template in ("L","R"):
        ranks = templates[template]
        pairs = cases = valid_prefixes = size = 0
        witnesses = []
        logname = f"cases-{template}.jsonl"
        with (HERE/logname).open("xb") as log:
            for a,b in combinations(ALPHABET,2):
                pairs += 1
                require(pairs <= limits["pairs_per_template"], "pair cap")
                prefix = dict(zip(ranks,(v for v in ALPHABET if v not in (a,b)),strict=True))
                R = sorted(set(ALPHABET)-set(prefix.values()))
                weights = edge_values(assigned,prefix)
                missing = inventory(weights)
                valid_prefix = not missing["repeated"]
                require(R == [a,b] and len(weights) == 16 and min(weights)>=1 and max(weights)<=18
                        and (not valid_prefix or len(missing["missing"]) == 2), "prefix inventories")
                valid_prefixes += valid_prefix
                orders = {}
                for order,s5,s6 in (("A",a,b),("B",b,a)):
                    cases += 1
                    require(cases <= 2*limits["pairs_per_template"], "per-template case cap")
                    f = dict(prefix, **{"s:5":s5,"s:6":s6})
                    key = tuple(f[v] for v in graph["vertices"])
                    require(key not in unique and len(unique) < limits["cases"], "distinct full case or case cap")
                    unique.add(key)
                    ds = edge_values(graph["edges"],f)
                    tail = edge_values(pending,f)
                    ck = verify_certificate(graph,f,TARGET_DIGEST)
                    good = sorted(ds) == DIFFERENCES
                    require(sorted(f.values()) == ALPHABET and ck["graph_digest"] == TARGET_DIGEST
                            and ds == ck["edge_differences"] and ck["valid"] is good
                            and good == (valid_prefix and sorted(tail) == missing["missing"]), "candidate verifier")
                    if good:
                        witnesses.append([a,b,order])
                    orders[order] = {"suffix_labels":[s5,s6],"suffix_weights":tail,
                                     "inventory":inventory(ds),"checker":ck}
                row = {"template":template,"R":R,"D":missing["missing"],"prefix_repeated":missing["repeated"],
                       "valid_prefix":valid_prefix,"prefix":prefix,"prefix_weights":weights,
                       "port":["s:4",prefix["s:4"]],"orders":orders}
                raw = json.dumps(row,sort_keys=True,separators=(",",":")).encode()+b"\n"
                size += len(raw)
                require(size <= limits["max_record_bytes"], "raw case log byte cap")
                log.write(raw)
                log.flush()
                require(frozen["cpu_seconds"]+process_time()-started <= limits["max_cpu_seconds"], "CPU cap")
            os.fsync(log.fileno())
        require((pairs,cases) == (171,342), "complete template")
        summary[template] = {"pairs":pairs,"cases":cases,"valid_prefixes":valid_prefixes,
                             "witnesses":witnesses,"log_sha256":digest(HERE/logname)}
    require(len(unique) == 684, "complete distinct grid")
    result = {"status":"VERIFIED_WITNESS" if any(v["witnesses"] for v in summary.values())
              else "EXHAUSTED_RESTRICTED_NEGATIVE","grid_complete":True,"templates":summary,
              "distinct_full_maps":len(unique),"full_cases":684,"new_graph_identities":0,"solver_queries":0,
              "cpu_seconds":process_time()-started}
    save("result.json",result,limits["max_record_bytes"])
    print(f"Checked 342 pairs across L and R, all {len(unique)} distinct cases. {result['status']}.")


def main():
    started = process_time()
    require(sys.version_info[:2] in {(3,12),(3,13)}, "project Python 3.12 or 3.13")
    config = read(HERE/"config.json")
    limits = config["limits"]
    model = config["model"]
    require(model["label_range"] == [0,18] and model["templates"] == {"L":[9,10],"R":[10,11]}
            and model["suffix"] == ["s:5","s:6"] and model["orders"] == {"A":["a","b"],"B":["b","a"]}
            and model["apply_prefilter"] is False, "exact two adjacent exchanges and no pruning")
    ints = [*limits.values(),*config["parameters"],*model["label_range"],
            *(x for swap in model["templates"].values() for x in swap),
            *(x for sec in config["profile"] for x in sec)]
    require(config["parent"] == PARENT and config["target_digest"] == TARGET_DIGEST and config["profile"] == PROFILE
            and config["parameters"] == [2]*4 and all(type(x) is int for x in ints), "frozen domain")
    require(limits == dict(workers=1,templates=2,pairs_per_template=171,cases=684,max_order=19,new_graph_identities=0,
                           solver_queries=0,max_cpu_seconds=30,max_record_bytes=2000000,max_evidence_bytes=10000000,
                           retries=0),"frozen limits")
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
        print("Bound the existing 19-vertex original and both adjacent-rank templates.")
    else:
        require(not any((HERE/p).exists() for p in OUTPUTS[1:]), "occupied candidate output path")
        check_templates(config,limits,read(HERE/"freeze.json"),started)


if __name__ == "__main__":
    main()
