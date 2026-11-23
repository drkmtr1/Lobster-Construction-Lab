"""Check archived positives and record each admissible cut on D066."""
from time import process_time

START = process_time()
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.verify import verify_certificate

W = ("b:0:0", "s:0", "s:1", "s:2", "s:3", "s:4")
LIMITS = {"workers": 1, "cuts": 7, "retained_positives": 2, "new_originals": 0,
          "adverse_max": 4, "cpu_seconds": 30, "record_bytes": 2_000_000,
          "total_bytes": 6_000_000, "queries": 0, "enumeration_nodes": 0,
          "replays": 0, "retries": 0}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(data):
    return sha256(data).hexdigest()


def canonical(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False).encode("utf-8"))


def save(name, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    require(len(raw) <= LIMITS["record_bytes"] and total + len(raw) <= LIMITS["total_bytes"],
            "evidence byte cap")
    with (HERE / name).open("xb") as out:
        out.write(raw)


def frozen_inputs(cfg):
    require(cfg["limits"] == LIMITS and cfg["cuts"] == list(range(10, 17)), "fixed scope")
    require(sys.version_info[:2] in {(3, 12), (3, 13)}, "Python 3.12/3.13")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    require(head == cfg["parent"], "recorded parent")
    require(cfg["runtime"] == {"python": sys.version, "platform": sys.platform,
                               "exe_sha256": digest(Path(sys.executable).read_bytes())},
            "frozen runtime")
    for ref in cfg["sources"].values():
        raw = (ROOT / ref["path"]).read_bytes()
        require((len(raw), digest(raw)) == (ref["bytes"], ref["sha256"]), ref["path"])
        if "git_sha256" in ref:
            git_raw = subprocess.check_output(["git", "show", f"{head}:{ref['path']}"], cwd=ROOT)
            require(digest(git_raw) == ref["git_sha256"]
                    and (raw == git_raw or raw.replace(b"\r\n", b"\n") == git_raw), ref["path"])


def saved(cfg, ref):
    return json.loads((ROOT / cfg["sources"][ref]["path"]).read_bytes())


def certify(original, cert):
    graph, labels = original["graph"], cert["labels"]
    identity = original["graph_digest"]
    checker = verify_certificate(graph, labels, identity)
    ledger = canonical({"graph_digest": identity, "labels": sorted(labels.items())})
    rows = [{"edge": edge, "difference": abs(labels[edge[0]] - labels[edge[1]])}
            for edge in graph["edges"]]
    require(checker["valid"] and checker == cert["checker"]
            and identity == checker["graph_digest"] == cert["graph_digest"]
            and ledger == cert["ledger_id"] != identity and rows == cert["named_edges"],
            "original, ledger and archived certificate binding")
    return {"graph_digest": identity, "ledger_id": ledger, "checker": checker,
            "named_edges": rows, "labels": labels}


def prefix_state(graph, labels):
    require(graph["profile"] == [[2], [2], [2], [2], []]
            and graph["spine"] == list(W[1:])
            and [labels[v] for v in W[1:]] == [10, 2, 16, 7, 9], "exact D066 spine")
    triples = ((6, 12, 13), (14, 1, 4), (0, 15, 11), (8, 3, 5))
    for i, row in enumerate(triples):
        require(tuple(labels[name] for name in (f"b:{i}:0", f"l:{i}:0:0", f"l:{i}:0:1"))
                == row, "exact D066 branch names and labels")
    require(sorted(labels.values()) == list(range(17))
            and all((labels[u] < 8) != (labels[v] < 8) for u, v in graph["edges"]),
            "alpha cut and full label alphabet")
    edges = {frozenset(e) for e in graph["edges"]}
    require(len(edges) == len(graph["edges"]) == 16
            and all(frozenset(e) in edges for e in zip(W, W[1:])), "original witness")
    distances = dict.fromkeys(W, 0)
    for d in (1, 2):
        fresh = [v for v in labels if v not in distances
                 and any(frozenset((u, v)) in edges for u in distances)]
        distances.update(dict.fromkeys(fresh, d))
    require(distances.keys() == labels.keys() and distances["b:2:0"] == 1, "witness distances")
    return {"alpha_low": sorted(v for v in labels if labels[v] < 8),
            "alpha_high": sorted(v for v in labels if labels[v] >= 8), "witness": W,
            "host": ["b:0:0", labels["b:0:0"]], "zero": ["b:2:0", labels["b:2:0"]],
            "exit": ["s:4", labels["s:4"]], "distances": distances}


def cut_receipt(graph, labels, c):
    host = labels["b:0:0"]
    require(type(c) is int and labels["s:4"] < c <= 16, "exact admissible cut")
    selected = {v for v, value in labels.items() if value >= c}
    crossed = []
    for u, v in graph["edges"]:
        ends = (u in selected, v in selected)
        require(not all(ends), "two shifted endpoints on one edge")
        if any(ends):
            crossed.append({"edge": sorted((u, v)), "difference": abs(labels[u] - labels[v])})
    crossed.sort(key=lambda row: row["edge"])
    weights = sorted(row["difference"] for row in crossed)
    required = list(range(c - host, 17))
    actual_counts, required_counts = Counter(weights), Counter(required)
    n, target = len(crossed), len(required)
    deficit = target - n
    # Coefficients of twice the sums in increasing powers of h.
    old_sum = sum(range(1, 17))
    actual_poly = [2 * old_sum, 2 * (n + c - host) - 1, 1]
    required_poly = [2 * old_sum, 2 * 17 - 1, 1]
    difference_poly = [x - y for x, y in zip(required_poly, actual_poly, strict=True)]
    require(target == 23 - c and difference_poly == [0, 2 * deficit, 0], "sum coefficient identity")
    return {"c": c, "selected": sorted(selected), "crossings": crossed, "actual": weights,
            "required": required, "selected_count": n, "required_count": target, "deficit": deficit,
            "missing": sorted((required_counts - actual_counts).elements()),
            "excess": sorted((actual_counts - required_counts).elements()),
            "twice_actual_sum": actual_poly, "twice_required_sum": required_poly,
            "twice_sum_deficit": difference_poly}


def main():
    cfg = json.loads((HERE / "config.json").read_bytes())
    frozen_inputs(cfg)
    p = saved(cfg, "d066_original")
    t = saved(cfg, "d068_original")
    p_cert = saved(cfg, "d066_certificate")["prefix"]
    t_cert = saved(cfg, "d068_certificate")
    require(t_cert["original"] == {k: cfg["sources"]["d068_original"][k]
                                   for k in ("bytes", "path", "sha256")}
            and t["graph"]["profile"] == [[2], [2], [3], [2], [], [], []], "D068 positive binding")
    positives = {"D066_P": certify(p, p_cert), "D068_T_3_2": certify(t, t_cert)}
    state = prefix_state(p["graph"], p_cert["labels"])
    wrong = "0" * 64
    rejection = verify_certificate(p["graph"], p_cert["labels"], wrong)
    require(not rejection["valid"] and rejection["errors"] == ["original graph digest mismatch"],
            "unchanged checker accepted the wrong original")
    save("controls.json", {"verified": positives, "prefix_state": state,
                           "wrong_digest": {"expected": wrong, "checker": rejection}})
    ruled_out = []
    for c in cfg["cuts"]:
        require(process_time() - START < LIMITS["cpu_seconds"], "producer CPU cap")
        row = cut_receipt(p["graph"], p_cert["labels"], c)
        save(f"cut-{c}.json", row)
        require(row["deficit"] > 0 and row["actual"] != row["required"], f"proposed falsifier at c={c}")
        ruled_out.append(c)
    elapsed = process_time() - START
    require(elapsed < LIMITS["cpu_seconds"], "producer CPU cap")
    save("result.json", {"status": "EXHAUSTED_RESTRICTED_NEGATIVE", "cuts": ruled_out,
                         "retained_positives": 2, "adverse_rejections": 1, "new_originals": 0,
                         "queries": 0, "enumeration_nodes": 0, "replays": 0, "retries": 0,
                         "process_cpu_seconds": elapsed})
    print("Producer PASS: seven cut receipts and one checker rejection")


if __name__ == "__main__":
    main()
