"""Validate fixed ledgers and four predeclared formula targets without search."""

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
PARENT = "2d9eb76ea59155a0cfb68b7441dd778467bf475c"
PROOF = "research/B4_JOINT_22_CUT_COMPAT.md"
LIMITS = {"workers": 1, "max_threshold_evaluations": 64, "max_new_named_graphs": 4,
          "max_cpu_seconds": 30, "max_record_bytes": 2_000_000, "max_total_bytes": 10_000_000,
          "solver_queries": 0, "labeling_enumeration_nodes": 0}
CASES = [{"q": 3, "t": None, "order": 16}, {"q": 4, "t": None, "order": 17},
         {"q": 3, "t": 1, "order": 18}, {"q": 4, "t": 2, "order": 20}]
SOURCES = ("lcl/__init__.py", "lcl/model.py", "lcl/verify.py", "pyproject.toml", "requirements.txt")

sys.path.insert(0, str(ROOT))
from lcl.model import build_graph, graph_digest
from lcl.verify import verify_certificate


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def load(path):
    return json.loads(path.read_bytes())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


class RunRecords:
    def __init__(self, started):
        self.bytes = 0
        self.started = started

    def write(self, name, data):
        require(process_time() - self.started <= LIMITS["max_cpu_seconds"], "validation CPU cap")
        require(len(data) <= LIMITS["max_record_bytes"] and self.bytes + len(data) <= LIMITS["max_total_bytes"],
                "run output byte caps")
        path = OUT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
        self.bytes += len(data)

    def save(self, name, data):
        self.write(name, (json.dumps(data, sort_keys=True, indent=2) + "\n").encode())


def core_formula(q):
    require(type(q) is int and q >= 2, "q must be an exact integer at least two")
    spine = dict(zip((f"s:{i}" for i in range(6)), (q+11, 1, q+12, 0, 7, 5)))
    return {**spine, "b:0:0": 2, "l:0:0:0": q+10, "l:0:0:1": q+9,
            **{f"l:0:0:{j}": j+9 for j in range(2, q)},
            "b:1:0": 9, "l:1:0:0": 4, "l:1:0:1": 8,
            "b:3:0": 6, "l:3:0:0": 3, "l:3:0:1": 10}


def batch(labels, first_index, count, cut):
    return {**{v: x + count if x >= cut else x for v, x in labels.items()},
            **{f"l:0:0:{first_index+i}": cut+i for i in range(count)}}


def ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]


def complete(original, labels):
    graph = original["graph"]
    result = verify_certificate(graph, labels, original["graph_digest"])
    return {"labels": labels, "ledger": ledger(graph, labels), "checker": result,
            "graph_digest": original["graph_digest"], "witness": graph["spine"]}


def prefix_lift(core, t, graph):
    require(type(t) is int and t >= 1, "t must be an exact positive integer")
    prefix = {v: x+1 for v, x in core.items() if v != "s:5"}
    prefix.update({"b:2:0": 0, **{f"l:2:0:{j}": max(core.values())+2+j for j in range(t)}})
    missing = set(graph["vertices"]) - prefix.keys()
    pending = [edge for edge in graph["edges"] if any(v in missing for v in edge)]
    m = len(graph["edges"])
    used_weights = sorted(abs(prefix[u] - prefix[v]) for u, v in graph["edges"] if u in prefix and v in prefix)
    used_labels = sorted(prefix.values())
    r = sorted(set(range(m + 1)).difference(used_labels))
    d = sorted(set(range(1, m + 1)).difference(used_weights))
    require(missing == {"s:5"} and pending == [["s:4", "s:5"]] and prefix["s:4"] == 8
            and r == [6] and d == [2] and abs(prefix["s:4"] - r[0]) == d[0], "physical singleton")
    interface = {"prefix": prefix, "used_labels": used_labels, "used_differences": used_weights,
                 "R": r, "D": d, "port": ["s:4", 8], "pending": pending}
    return {**prefix, "s:5": r[0]}, interface


def main():
    started = process_time()
    config = load(HERE / "config.json")
    require(config["parent"] == PARENT == git("rev-parse", "HEAD").decode().strip()
            and config["limits"] == LIMITS and config["cases"] == CASES
            and list(config["controls"]) == ["A", "B"] and sys.version_info[:2] in ((3, 12), (3, 13))
            and sys.flags.utf8_mode == 1, "recorded parent, limits and interpreter")
    OUT.mkdir()
    records = RunRecords(started)
    paths = [config["original"], *config["controls"].values()]
    retained = {}
    for path in paths:
        raw = (ROOT / path).read_bytes()
        require(raw == git("show", f"{PARENT}:{path}"), path)
        retained[path] = sha(raw)
    sources = {}
    for path in SOURCES:
        raw = (ROOT / path).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{path}").replace(b"\r\n", b"\n"), path)
        records.write("source/" + path, raw)
        sources[path] = sha(raw)
    inputs = [HERE / name for name in ("config.json", "validate.py", "audit.py", "commands.json")] + [ROOT / PROOF]
    records.save("identity.json", {"id": config["id"], "parent": PARENT, "retained_sha256": retained,
                 "source_sha256": sources, "inputs_sha256": {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in inputs},
                 "runtime": {"version": sys.version, "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode,
                             "implementation": sys.implementation.name, "optional_dependencies": []}})
    original = load(ROOT / config["original"])
    control_records = {}
    for case, path in config["controls"].items():
        prior = load(ROOT / path)
        labels = prior["labels"]
        result = complete(original, labels)
        require(result["graph_digest"] == prior["graph_digest"] and labels["s:2"] == 14
                and result["ledger"] == prior["ledger"] and result["checker"] == prior["checker"]
                and result["checker"]["valid"] is (case == "B"), f"control {case}")
        control_records[case] = result
    records.save("controls.json", control_records)
    base = control_records["B"]["labels"]
    require(base == core_formula(2), "identity batch on retained physical ledger")
    adverse = verify_certificate(original["graph"], base, "0" * 64)
    require(adverse["valid"] is False and adverse["errors"] == ["original graph digest mismatch"], "wrong-digest rejection")
    records.save("adverse.json", {"expected_digest": "0" * 64, "checker": adverse})
    one = batch(base, 2, 1, 11)
    two = batch(base, 2, 2, 11)
    require(one == core_formula(3) and two == batch(one, 3, 1, 12) == core_formula(4), "batch agreement")
    records.save("batch.json", {"case_q3_one": one, "case_q4_one_batch": two, "case_q4_two_batches": batch(one, 3, 1, 12),
                               "updated_cuts": [11, 12, 13]})

    for case in config["cases"]:
        q, t = case["q"], case["t"]
        name = f"q{q}" if t is None else f"q{q}-t{t}"
        profile = [[q], [2], [] if t is None else [t], [2], [], []]
        graph = build_graph(profile)
        require(len(graph["vertices"]) == case["order"], "exact test order")
        target = {"graph": graph, "graph_digest": graph_digest(graph)}
        records.save(name + "-original.json", target)
        core = core_formula(q)
        if t is None:
            result = complete(target, core)
            require(core["s:2"] == q+12 and core["s:3"] == 0, "physical root")
        else:
            labels, interface = prefix_lift(core, t, graph)
            result = {**complete(target, labels), "interface": interface}
        require(result["checker"]["valid"] is True, "unchanged original checker")
        records.save(name + ".json", result)
    cpu = process_time() - started
    records.save("summary.json", {"status": "PASS", "new_graphs": 4, "retained_graphs": 1, "control_certificates": 2,
                "threshold_evaluations": 0, "solver_queries": 0, "labeling_enumeration_nodes": 0, "cpu_seconds": cpu})
    print(f"PASS: two controls, four new named graphs, wrong-digest rejection ({cpu:.6f} CPU seconds)")


if __name__ == "__main__":
    main()
