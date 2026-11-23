"""Check the three lower cuts on each of two immutable D070 prefixes."""
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

CASES = {"seed": (2, 2), "p33": (3, 3)}
CUTS = (6, 7, 8)
PORTS = {"L": "b:0:0", "U": "s:4", "B": "b:1:0", "Z": "b:2:0"}
W = ["b:0:0", *(f"s:{i}" for i in range(5))]
LIMITS = {"retained_originals": 2, "new_originals": 0, "workers": 1,
          "cut_checks_per_script": 6, "cut_checks_combined": 12,
          "cpu_seconds": 30, "record_bytes": 2_000_000, "total_bytes": 8_000_000,
          "queries": 0, "enumeration_nodes": 0, "replays": 0, "retries": 0}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def config():
    cfg = read(HERE / "config.json")
    need(cfg["limits"] == LIMITS and cfg["cuts"] == list(CUTS)
         and cfg["cases"] == {k: list(v) for k, v in CASES.items()}, "exact task scope")
    head = git("rev-parse", "HEAD").decode().strip()
    need(head == cfg["parent"] and sys.version_info[:2] in {(3, 12), (3, 13)}
         and cfg["runtime"] == {"python": sys.version, "platform": sys.platform,
                               "exe_sha256": sha(Path(sys.executable).read_bytes())}, "parent and frozen runtime")
    for ref in cfg["sources"].values():
        path = ref["path"]
        raw = (ROOT / path).read_bytes()
        need(len(raw) == ref["bytes"] and sha(raw) == ref["sha256"], f"source raw bytes: {path}")
        if "git_sha256" in ref:
            blob = git("show", f"{head}:{path}")
            need(sha(blob) == ref["git_sha256"] and raw == blob, f"parent bytes: {path}")
    return cfg


def write(name, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    total = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file())
    need(len(raw) <= LIMITS["record_bytes"] and total + len(raw) <= LIMITS["total_bytes"], "byte caps")
    with (HERE / name).open("xb") as file:
        file.write(raw)


def edges_of(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]


def certify(original, cert, ref, q, t):
    graph, digest = original["graph"], original["graph_digest"]
    labels = cert["labels"]
    h, k = q - 2, t - 2
    m = 16 + h + k
    need(graph["profile"] == [[q], [2], [t], [2], []] and graph["spine"] == W[1:]
         and len(graph["edges"]) == m, "declared retained original")
    checker = verify_certificate(graph, labels, digest)
    ledger_payload = {"graph_digest": digest, "labels": sorted(labels.items())}
    ledger = sha(json.dumps(ledger_payload, sort_keys=True, separators=(",", ":")).encode())
    identity = {key: ref[key] for key in ("path", "bytes", "sha256")}
    rows = edges_of(graph, labels)
    need(checker["valid"] and checker == cert["checker"] and cert["graph_digest"] == digest
         and ledger == cert["ledger_id"] != digest and identity == cert["original"]
         and rows == cert["named_edges"], "valid archived original and distinct ledger")
    low = sorted(v for v in labels if labels[v] < 8)
    need(cert["alpha"]["A"] == [m + 1, 8, 5, 1] and cert["alpha"]["witness"] == W
         and cert["alpha"]["low"] == low and all((u in low) != (v in low) for u, v in graph["edges"]),
         "retained alpha orientation and witness")
    anchors = {key: [v, labels[v]] for key, v in PORTS.items()}
    need([anchors[key][1] for key in PORTS] == [5, 9, 13 + h, 0], "physical anchors")
    edges = {frozenset(e) for e in graph["edges"]}
    need(len(edges) == m and all(frozenset(pair) in edges for pair in zip(W, W[1:])), "actual witness edges")
    distances = dict.fromkeys(W, 0)
    for d in (1, 2):
        layer = [v for v in labels if v not in distances
                 and any(frozenset((v, u)) in edges for u in distances)]
        distances.update(dict.fromkeys(layer, d))
    need(distances.keys() == labels.keys() and distances[PORTS["B"]] == distances[PORTS["Z"]] == 1
         and distances == cert["alpha"]["distances"], "actual witness distances")
    weights = {row["difference"] for row in rows}
    r = sorted(set(range(m + 3)) - {x + 2 * (x >= 8) for x in labels.values()})
    d = sorted(set(range(1, m + 3)) - {w + 2 for w in weights})
    need(r == [8, 9] and d == [1, 2], "D070 numerical K=2 inventory")
    return {"q": q, "t": t, "h": h, "k": k, "m": m, "original": identity, "graph_digest": digest,
            "ledger_id": ledger, "checker": checker, "labels": labels, "named_edges": rows, "alpha_low": low,
            "anchors": anchors, "witness": W, "distances": distances,
            "normalized_resources": {"R": [], "D": []},
            "numerical_shift_K2": {"R": r, "D": d, "physical_exit": ["s:4", 11]}}


def cut(data, c):
    labels = data["labels"]
    m, h, k = (data[x] for x in ("m", "h", "k"))
    b = data["anchors"]["B"][1]
    selected = sorted(v for v, value in labels.items() if value < c)
    crossings = []
    for row in data["named_edges"]:
        u, v = row["edge"]
        membership = (u in selected, v in selected)
        need(not all(membership), "selected endpoints must be on opposite sides")
        if any(membership):
            crossings.append(row)
    actual = sorted(row["difference"] for row in crossings)
    required = list(range(b - c + 1, m + 1))
    excess = len(actual) - len(required)
    need(len(actual) == {6: 12, 7: 15, 8: 16}[c] + h + k and len(required) == c + k + 3
         and excess == h + (3 if c == 6 else 5), "proposed counts falsified")
    # Coefficients of twice the sums in increasing powers of the batch j.
    actual_poly = [m * (m + 1), 2 * (len(actual) + b - c) + 1, 1]
    required_poly = [m * (m + 1), 2 * m + 1, 1]
    gap = [x - y for x, y in zip(actual_poly, required_poly, strict=True)]
    need(gap == [0, 2 * excess, 0], "proposed sum defect falsified")
    return {"c": c, "B": b, "selected": selected, "crossings": crossings,
            "actual": actual, "required": required, "count_surplus": excess,
            "actual_count": len(actual), "required_count": len(required),
            "missing": sorted((Counter(required) - Counter(actual)).elements()),
            "excess_weights": sorted((Counter(actual) - Counter(required)).elements()),
            "twice_actual_sum": actual_poly, "twice_required_sum": required_poly,
            "twice_sum_surplus": gap, "graph_digest": data["graph_digest"], "ledger_id": data["ledger_id"]}


def main():
    cfg = config()
    ref = cfg["sources"]
    archive = read(ROOT / ref["d070_certificates"]["path"])
    need(archive["seed"] == read(ROOT / ref["d070_seed"]["path"]), "independent seed archive binding")
    controls = {}
    for name, (q, t) in CASES.items():
        original = read(ROOT / ref[name + "_original"]["path"])
        controls[name] = certify(original, archive[name], ref[name + "_original"], q, t)
    original = read(ROOT / ref["seed_original"]["path"])
    wrong = verify_certificate(original["graph"], controls["seed"]["labels"], "0" * 64)
    need(not wrong["valid"] and wrong["errors"] == ["original graph digest mismatch"], "actual adverse digest")
    write("controls.json", {"retained": controls, "wrong_digest": {"expected": "0" * 64, "checker": wrong}})
    checked = []
    for name, record in controls.items():
        for c in CUTS:
            need(process_time() - START < LIMITS["cpu_seconds"], "producer CPU cap")
            key = f"{name}-c{c}"
            write(key + ".json", cut(record, c))
            checked.append(key)
    cpu = process_time() - START
    need(cpu < LIMITS["cpu_seconds"], "producer CPU cap")
    write("result.json", {"status": "PASS", "cuts": checked, "retained_originals": 2, "new_originals": 0,
                          "adverse_rejections": 1, "queries": 0, "enumeration_nodes": 0,
                          "replays": 0, "retries": 0, "process_cpu_seconds": cpu})
    print("PASS: two retained originals, six full cut spectra, one actual digest rejection")


if __name__ == "__main__":
    main()
