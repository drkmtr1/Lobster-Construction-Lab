"""Check the supplied exact rooted ledger and two named lifts without search."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
PARENT = "98ae0ee75b5afedfd6019a2f79c5da7c9d40c99c"
PROOF = "research/B4_JOINT_23_MAX_ROOTED_CORE.md"
LIMITS = {"workers": 1, "authorized_dfs_queries": 1, "dfs_nodes": 100000,
          "dfs_cooperative_seconds": 6, "max_cpu_seconds": 30, "max_order": 20, "max_new_graphs": 3,
          "max_record_bytes": 2_000_000, "max_total_bytes": 10_000_000, "automatic_retries": 0}
CASES = [{"id": "core", "t": None, "order": 16}, {"id": "lift-t1", "t": 1, "order": 18},
         {"id": "lift-t2", "t": 2, "order": 19}]
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def read(path):
    return json.loads(path.read_bytes())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


class Records:
    def __init__(self, started):
        self.started = started
        self.bytes = 0

    def write(self, name, raw):
        require(process_time() - self.started <= LIMITS["max_cpu_seconds"], "CPU budget")
        require(len(raw) <= LIMITS["max_record_bytes"] and self.bytes + len(raw) <= LIMITS["max_total_bytes"],
                "record byte caps")
        path = OUT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as out:
            out.write(raw)
        self.bytes += len(raw)

    def save(self, name, data):
        self.write(name, (json.dumps(data, sort_keys=True, indent=2) + "\n").encode())


def verify(original, labels):
    graph = original["graph"]
    verdict = verify_certificate(graph, labels, original["graph_digest"])
    require(verdict["valid"] is True, "original certificate rejected")
    return {"graph_digest": original["graph_digest"], "labels": labels, "checker": verdict,
            "witness": graph["spine"], "ledger": [
                {"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]}


def lifted_prefix(seed, t, graph):
    require(type(t) is int and t >= 1, "exact positive t")
    prefix = {v: x+1 for v, x in seed.items() if v != "s:5"}
    prefix.update({"b:2:0": 0, **{f"l:2:0:{j}": 17+j for j in range(t)}})
    missing = set(graph["vertices"]) - prefix.keys()
    pending = [edge for edge in graph["edges"] if any(v in missing for v in edge)]
    used_labels = sorted(prefix.values())
    used_diffs = sorted(abs(prefix[u] - prefix[v]) for u, v in graph["edges"] if u in prefix and v in prefix)
    m = len(graph["edges"])
    R = sorted(set(range(m+1)).difference(used_labels))
    D = sorted(set(range(1, m+1)).difference(used_diffs))
    require(missing == {"s:5"} and pending == [["s:4", "s:5"]] and prefix["s:4"] == 8
            and R == [seed["s:5"]+1] == [4] and D == [abs(prefix["s:4"]-R[0])] == [4], "singleton interface")
    interface = {"prefix": prefix, "pending": pending, "used_labels": used_labels, "used_differences": used_diffs,
                 "R": R, "D": D, "port": ["s:4", 8]}
    return {**prefix, "s:5": R[0]}, interface


def main():
    started = process_time()
    config = read(HERE / "config.json")
    require(config["parent"] == PARENT == git("rev-parse", "HEAD").decode().strip()
            and config["limits"] == LIMITS and config["cases"] == CASES
            and config["execution"] == {"method": "direct structural ledger", "dfs_queries": 0,
                "labeling_enumeration_nodes": 0, "only_root_pin": {"s:2": 15}}
            and [c["id"] for c in config["controls"]] == ["C22", "C32"]
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "frozen scope and runtime")
    OUT.mkdir()
    records = Records(started)
    retained = {}
    for name in [*(c[k] for c in config["controls"] for k in ("original", "certificate")),
                 *config["retained_negative"].values()]:
        raw = (ROOT / name).read_bytes()
        require(raw == git("show", f"{PARENT}:{name}"), f"retained source {name}")
        retained[name] = sha(raw)
    snapshots = {}
    for name in SOURCES:
        raw = (ROOT / name).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{name}").replace(b"\r\n", b"\n"), name)
        records.write("source/" + name, raw)
        snapshots[name] = sha(raw)
    inputs = [HERE / name for name in ("config.json", "validate.py", "audit.py", "commands.json")] + [ROOT / PROOF]
    records.save("identity.json", {"id": config["id"], "parent": PARENT, "retained_sha256": retained,
                 "source_sha256": snapshots, "inputs_sha256": {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in inputs},
                 "runtime": {"version": sys.version, "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
                             "implementation": sys.implementation.name, "optional_dependencies": []}})
    controls = {}
    for spec in config["controls"]:
        original = read(ROOT / spec["original"])
        prior = read(ROOT / spec["certificate"])
        labels = prior["labels"]
        receipt = verify(original, labels)
        q, r = spec["q"], spec["r"]
        require(original["graph"]["profile"] == [[q], [r], [], [2], [], []]
                and labels["s:2"] == q+r+10
                and all(receipt[k] == prior[k] for k in ("graph_digest", "labels", "ledger", "checker")), "positive control")
        controls[spec["id"]] = receipt
    negative_spec = config["retained_negative"]
    previous_audit = read(ROOT / negative_spec["audit"])
    old_manifest = read(ROOT / negative_spec["manifest"])
    require(old_manifest["files"]["audit_result.json"]["sha256"] == retained[negative_spec["audit"]]
            and previous_audit["status"] == "PASS" and previous_audit["second_cut_matches_q2"] == []
            and previous_audit["second_cut_matches_q3"] == [], "D059 negative-control binding")
    records.save("controls.json", {"positive": controls, "D059_negative": {
        "source": negative_spec["audit"], "sha256": retained[negative_spec["audit"]],
        "second_cut_matches_q2": [], "second_cut_matches_q3": [], "repeated_threshold_evaluations": 0}})

    seed = config["seed"]
    for case in CASES:
        name, t = case["id"], case["t"]
        profile = [[2], [3], [] if t is None else [t], [2], [], []]
        graph = build_graph(profile)
        require(len(graph["vertices"]) == case["order"] <= LIMITS["max_order"], "test order")
        original = {"graph": graph, "graph_digest": graph_digest(graph)}
        records.save(name + "-original.json", original)
        if t is None:
            require(seed["s:2"] == 15 and seed["s:3"] == 0, "physical maximum and chosen zero neighbor")
            receipt = verify(original, seed)
            adverse = verify_certificate(graph, seed, "0"*64)
            require(adverse["valid"] is False and adverse["errors"] == ["original graph digest mismatch"], "wrong-digest check")
            records.save("adverse.json", {"expected_digest": "0"*64, "checker": adverse})
        else:
            labels, info = lifted_prefix(seed, t, graph)
            receipt = {**verify(original, labels), "interface": info}
        records.save(name + ".json", receipt)
    cpu = process_time() - started
    records.save("summary.json", {"status": "PASS", "new_originals": 3, "positive_controls": 2,
                 "retained_negative_controls": 1, "adverse_tests": 1, "dfs_queries": 0,
                 "labeling_enumeration_nodes": 0, "cpu_seconds": cpu})
    print(f"PASS: direct C(2,3), two exact lifts, two retained positive controls and one wrong digest ({cpu:.6f} CPU seconds)")


if __name__ == "__main__":
    main()
