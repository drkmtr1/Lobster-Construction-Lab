"""Independent standard-library audit of original graphs, cuts and resources."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "98ae0ee75b5afedfd6019a2f79c5da7c9d40c99c"
PROOF = "research/B4_JOINT_23_MAX_ROOTED_CORE.md"


def check(condition, detail):
    if not condition:
        raise ValueError(detail)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def reconstruct(original, profile, order):
    graph = original["graph"]
    spine = [f"s:{i}" for i in range(6)]
    edges = list(zip(spine, spine[1:]))
    roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
    for i, section in enumerate(profile):
        if not section:
            continue
        b = f"b:{i}:0"
        roles[b] = {"kind": "branch", "section": i, "branch": 0}
        edges.append((spine[i], b))
        for j in range(section[0]):
            leaf = f"l:{i}:0:{j}"
            edges.append((b, leaf))
            roles[leaf] = {"kind": "leaf", "section": i, "branch": 0, "leaf": j}
    canonical = [tuple(sorted(e)) for e in edges]
    check(Counter(graph["vertices"]) == Counter(roles.keys())
          and Counter(tuple(sorted(e)) for e in graph["edges"]) == Counter(canonical), "named edge multiplicities")
    check(len(roles) == order == len(edges)+1 and graph["spine"] == spine and graph["roles"] == roles
          and graph["profile"] == profile and graph["schema_version"] == 1, "physical graph and roles")
    body = {"vertices": sorted(roles), "edges": sorted(canonical), "spine": spine, "roles": roles, "profile": profile}
    payload = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    check(sha256(payload).hexdigest() == original["graph_digest"], "canonical digest")
    return graph["edges"]


def certificate(original, edges, cert):
    labels = cert["labels"]
    m = len(edges)
    check(set(labels) == set(original["graph"]["vertices"]) and all(type(v) is int for v in labels.values())
          and sorted(labels.values()) == list(range(m+1)), "label bijection")
    rows = [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in edges]
    weights = [row["difference"] for row in rows]
    verdict = cert["checker"]
    check(rows == cert["ledger"] and cert["witness"] == original["graph"]["spine"]
          and sorted(weights) == list(range(1,m+1)) and weights == verdict["edge_differences"]
          and verdict["valid"] is True and verdict["errors"] == []
          and verdict["n"] == m+1 and verdict["m"] == m
          and original["graph_digest"] == cert["graph_digest"] == verdict["graph_digest"], "full original-bound certificate")
    return rows


def identity_check(config, ident):
    check(ident["id"] == config["id"] and ident["parent"] == config["parent"] == PARENT
          and ident["runtime"] == {"version": sys.version, "platform": platform.platform(), "utf8_mode": 1,
                                   "implementation": sys.implementation.name, "optional_dependencies": []}, "runtime identity")
    inputs = {(HERE / name).relative_to(ROOT).as_posix() for name in ("config.json", "commands.json", "validate.py", "audit.py")}
    check(ident["inputs_sha256"] == {name: sha(ROOT / name) for name in inputs | {PROOF}}, "raw task input hashes")
    names = {spec[key] for spec in config["controls"] for key in ("original", "certificate")}
    check(set(ident["retained_sha256"]) == names | set(config["retained_negative"].values())
          and set(ident["source_sha256"]) == {"lcl/__init__.py", "lcl/model.py", "lcl/verify.py",
                                             "pyproject.toml", "requirements.txt"}, "retained and runtime source inventories")
    for name, expected in ident["retained_sha256"].items():
        parent = subprocess.check_output(["git", "show", f"{PARENT}:{name}"], cwd=ROOT)
        check(sha(ROOT / name) == expected and (ROOT / name).read_bytes() == parent, name)
    for name, expected in ident["source_sha256"].items():
        parent = subprocess.check_output(["git", "show", f"{PARENT}:{name}"], cwd=ROOT)
        snapshot = DATA / "source" / name
        check(sha(ROOT / name) == sha(snapshot) == expected
              and snapshot.read_bytes().replace(b"\r\n", b"\n") == parent.replace(b"\r\n", b"\n"), name)


def controls_check(config):
    receipts = read(DATA / "controls.json")
    check(set(receipts["positive"]) == {"C22", "C32"}, "two original controls")
    for spec, q in zip(config["controls"], (2,3), strict=True):
        original = read(ROOT / spec["original"])
        saved = read(ROOT / spec["certificate"])
        receipt = receipts["positive"][spec["id"]]
        edges = reconstruct(original, [[q],[2],[],[2],[],[]], q+13)
        certificate(original, edges, receipt)
        check(all(receipt[k] == saved[k] for k in ("labels", "graph_digest", "ledger", "checker"))
              and receipt["labels"]["s:2"] == q+12, spec["id"])
    negative = config["retained_negative"]
    prior = read(ROOT / negative["audit"])
    manifest = read(ROOT / negative["manifest"])
    expected = sha(ROOT / negative["audit"])
    check(manifest["files"]["audit_result.json"]["sha256"] == expected
          and prior["status"] == "PASS" and prior["threshold_evaluations"] == 49
          and prior["second_cut_matches_q2"] == prior["second_cut_matches_q3"] == []
          and receipts["D059_negative"] == {"source": negative["audit"], "sha256": expected,
               "second_cut_matches_q2": [], "second_cut_matches_q3": [], "repeated_threshold_evaluations": 0},
          "D059 fixed-ledger failure preserved without replay")


def case_a(edges):
    initial = {"s:1":0, "s:2":15, "s:3":1, "s:4":14, "s:5":2,
               "b:3:0":3, "l:3:0:0":13, "l:3:0:1":12}
    used = [abs(initial[u]-initial[v]) for u, v in edges if u in initial and v in initial]
    check(sorted(used) == [2,9,10,12,13,14,15] and sorted(set(range(16)).difference(initial.values())) == list(range(4,12)),
          "Case A initial allocation")
    full_partial = {**initial, "b:1:0":11, "s:0":8, "b:0:0":4}
    check(not any({u,v} == {"b:0:0","b:1:0"} for u,v in edges)
          and max(range(4,12))-min(range(4,12)) == 7, "Case A possible pair for 7")
    pending = [e for e in edges if not all(v in full_partial for v in e)]
    remainder = set(range(16)).difference(full_partial.values())
    used = [abs(full_partial[u]-full_partial[v]) for u, v in edges if u in full_partial and v in full_partial]
    check(7 not in used and len(pending) == 5 and remainder == {5,6,7,9,10}
          and all(sum(v in full_partial for v in e) == 1 for e in pending), "Case A terminal boundary")
    return {"restriction": full_partial, "pending_weight": 7, "only_label_pair": [4,11],
            "physical_pair_is_edge": False, "pending_edges": pending, "unused_labels": sorted(remainder),
            "unused_differences": sorted(set(range(1,16))-set(used))}


def cut_tables(labels, rows):
    by_cut = [[] for _ in range(17)]
    for row in rows:
        low, high = sorted(labels[v] for v in row["edge"])
        for c in range(low+1, high+1):
            by_cut[c].append(row)
    result = {}
    for host in ("b:0:0", "b:1:0"):
        b = labels[host]
        table = []
        for c, selected in enumerate(by_cut):
            current = sorted(row["difference"] for row in selected)
            d0 = max(c-b, b-c+1)
            needed = list(range(d0,16))
            table.append({"c": c, "host_label": b, "host_side": "below" if b<c else "at_or_above",
                          "first_new_difference": d0, "crossing_edges": selected, "spectrum": current,
                          "required": needed, "missing": sorted(set(needed)-set(current)),
                          "excess": sorted(set(current)-set(needed)), "matches": current == needed})
        result[host] = table
    check([row["c"] for row in result["b:0:0"] if row["matches"]] == [6,12,13,14]
          and all(not row["matches"] for row in result["b:1:0"]), "exact host cut dispositions")
    return result


def check_lift(seed, t, original, cert):
    edges = reconstruct(original, [[2],[3],[t],[2],[],[]], 17+t)
    rows = certificate(original, edges, cert)
    f = cert["labels"]
    check(all(f[v] == x+1 for v,x in seed.items()) and f["s:2"] == 16
          and {v: f[v] for v in f.keys()-seed.keys()} ==
               {"b:2:0":0, **{f"l:2:0:{j}":17+j for j in range(t)}}, "named lift and root attachment")
    pending = [row for row in rows if "s:5" in row["edge"]]
    prefix = {v:x for v,x in f.items() if v != "s:5"}
    used_ds = sorted(row["difference"] for row in rows if row not in pending)
    used_ls = sorted(prefix.values())
    R = sorted(set(range(17+t))-set(used_ls))
    D = sorted(set(range(1,17+t))-set(used_ds))
    check(R == D == [4] and f["s:5"] == 4 and f["s:4"] == 8
          and pending == [{"edge":["s:4","s:5"],"difference":4}]
          and cert["interface"] == {"prefix":prefix, "pending":[["s:4","s:5"]], "used_labels":used_ls,
                                    "used_differences":used_ds, "R":R, "D":D, "port":["s:4",8]}, "both actual singleton resources")


def main():
    started = process_time()
    config = read(HERE / "config.json")
    limits = config["limits"]
    check(limits == {"workers":1, "authorized_dfs_queries":1, "dfs_nodes":100000, "dfs_cooperative_seconds":6,
                     "max_cpu_seconds":30, "max_order":20, "max_new_graphs":3, "max_record_bytes":2_000_000,
                     "max_total_bytes":10_000_000, "automatic_retries":0}
          and config["execution"] == {"method":"direct structural ledger","dfs_queries":0,
                    "labeling_enumeration_nodes":0,"only_root_pin":{"s:2":15}}, "fixed limits and execution path")
    identity_check(config, read(DATA / "identity.json"))
    controls_check(config)
    original = read(DATA / "core-original.json")
    edges = reconstruct(original, [[2],[3],[],[2],[],[]], 16)
    core = read(DATA / "core.json")
    rows = certificate(original, edges, core)
    seed = core["labels"]
    check(seed == config["seed"] and seed["s:2"] == 15 and seed["s:3"] == 0
          and {v if u == "s:2" else u for u,v in edges if "s:2" in (u,v)} == {"s:1","s:3"}
          and [row["difference"] for row in rows] == [13,14,15,7,4,12,11,10,9,6,5,1,8,2,3], "direct seed and top edges")
    adverse = read(DATA / "adverse.json")
    check(adverse["expected_digest"] == "0"*64 != original["graph_digest"] and
          adverse["checker"] == {**core["checker"],"valid":False,"errors":["original graph digest mismatch"]}, "one wrong digest")
    evidence = {"core": {"order":16,"graph_digest":original["graph_digest"]}}
    for t in (1,2):
        name = f"lift-t{t}"
        target = read(DATA / (name + "-original.json"))
        check_lift(seed, t, target, read(DATA / (name + ".json")))
        evidence[name] = {"order":17+t,"graph_digest":target["graph_digest"]}
    case_a_failure = case_a(edges)
    tables = cut_tables(seed, rows)
    prior = read(DATA / "summary.json")
    cpu_before = prior["cpu_seconds"]
    check(prior == {"status":"PASS","new_originals":3,"positive_controls":2,"retained_negative_controls":1,
                    "adverse_tests":1,"dfs_queries":0,"labeling_enumeration_nodes":0,"cpu_seconds":cpu_before}
          and 0 <= cpu_before <= limits["max_cpu_seconds"], "exact execution counts")
    outputs = {x.relative_to(DATA).as_posix(): sha(x) for x in sorted(DATA.rglob("*")) if x.is_file()}
    sizes = [(DATA / name).stat().st_size for name in outputs]
    cpu = cpu_before + process_time() - started
    check(cpu <= limits["max_cpu_seconds"], "combined process CPU")
    report = {"status":"PASS","new_graphs":evidence,"positive_controls":2,"retained_negative_controls":1,
              "adverse_tests":1,"case_A_failure":case_a_failure,
              "threshold_rows":sum(len(t) for t in tables.values()),"cut_tables":tables,
              "first_host_matches":[6,12,13,14],"second_host_matches":[],
              "dfs_queries":0,"labeling_enumeration_nodes":0,"cpu_seconds_total":cpu,"audited_sha256":outputs}
    raw = (json.dumps(report,sort_keys=True,indent=2)+"\n").encode()
    check(max([len(raw),*sizes]) <= limits["max_record_bytes"]
          and len(raw)+sum(sizes) <= limits["max_total_bytes"], "byte limits")
    with (HERE / "audit_result.json").open("xb") as out:
        out.write(raw)
    print(f"PASS: three new graphs, both named interfaces, 34 cut rows, zero searches ({cpu:.6f} total CPU seconds)")


if __name__ == "__main__":
    main()
