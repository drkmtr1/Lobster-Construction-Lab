"""One exclusive first-witness run with original-bound certificate checks."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import seed_search as search

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "validation"
PARENT = "bb7927bcf85d6d32b9bde5b1904c6b43ec6b6a8e"
PROOF = "research/B4_1342_RELAXED_HOST_SEED.md"
H, Z, U = search.H, search.Z, search.U
CAP = 2_000_000
WITNESS = [H, "s:0", "s:1", "s:2", "s:3", U]
LIMITS = {"workers": 1, "max_vertices": 22, "max_assignment_nodes": 200_000,
          "max_search_seconds": 20, "max_result_bytes": CAP, "max_pairs": 23}

sys.path.insert(0, str(ROOT))
from lcl.verify import verify_certificate


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def file_ref(path, base):
    return {"path": path.relative_to(base).as_posix(), "sha256_raw": sha(path.read_bytes())}


def read(path):
    return json.loads(path.read_bytes())


def put(path, raw):
    require(len(raw) <= CAP, f"byte cap exceeded: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(raw)


def save(path, data):
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    put(path, raw)
    return file_ref(path, OUT)


def git(*args):
    return subprocess.check_output(("git", *args), cwd=ROOT)


def edge_ledger(graph, labels):
    return [{"edge": [u, v], "difference": abs(labels[u] - labels[v])} for u, v in graph["edges"]]


def checked(graph, labels, digest):
    check = verify_certificate(graph, labels, digest)
    require(check["valid"], f"original verifier rejected: {check['errors']}")
    return check


def seed_record(graph, labels, digest, a, c, p, exit_label):
    require(labels[H] == a and labels[Z] == 0 and labels[U] == exit_label, "physical anchors")
    low = sorted(v for v, g in labels.items() if g < p)
    high = sorted(v for v, g in labels.items() if g >= p)
    n = len(graph["vertices"])
    require(len(low) == p and p + 1 == exit_label < c <= n - 1
            and all((u in low) != (v in low) for u, v in graph["edges"]), "alpha split or threshold")
    require(all([u, v] in graph["edges"] or [v, u] in graph["edges"] for u, v in zip(WITNESS, WITNESS[1:])),
            "named witness")
    distances = {v: {"spine": 0, "branch": 1, "leaf": 2}[role["kind"]]
                 - int(v == H or role["kind"] == "leaf" and role["section"] == 0)
                 for v, role in graph["roles"].items()}
    require(distances[H] == 0 and distances[Z] == 1 and max(distances.values()) <= 2, "host witness distance")
    ledger = edge_ledger(graph, labels)
    selected = sorted(v for v in high if labels[v] >= c)
    inside, outside = [], []
    for row in ledger:
        (inside if any(v in selected for v in row["edge"]) else outside).append(row)
    selected_weights = sorted(row["difference"] for row in inside)
    outside_weights = sorted(row["difference"] for row in outside)
    require(selected_weights == list(range(c - a, n)) and outside_weights == list(range(1, c - a)),
            "full selected or unselected incidence spectrum")
    return {"a": a, "c": c, "labels": labels, "edge_ledger": ledger, "graph_digest": digest,
            "state": {"n": n, "p": p, "L": H, "H": H, "U": U, "Z": Z, "x": a, "y": 1},
            "low": low, "high": high, "witness": WITNESS, "witness_distances": distances,
            "selected_vertices": selected, "selected_edges": inside, "unselected_edges": outside,
            "selected_weights": selected_weights, "unselected_weights": outside_weights,
            "verification": checked(graph, labels, digest)}


def controls(cfg, graph, digest):
    positive = cfg["positive_control"]
    pgraph = read(ROOT / positive["original"])
    pprior = read(ROOT / positive["certificate"])
    query = read(ROOT / positive["query"])
    require(query["original_graph"] == pgraph and query["classification"] == "SAT"
            and query["result"]["witness"] == pprior["normalized"]["labels"]
            and pprior["source"] == {**file_ref(ROOT / positive["query"], ROOT), "graph_digest": query["original_graph_digest"]},
            "positive source binding")
    result = seed_record(pgraph, pprior["normalized"]["labels"], query["original_graph_digest"], 4, 9, 7, 8)
    require(result["verification"] == query["certificate"] == pprior["certificate"]
            and result["selected_edges"] == pprior["normalized"]["selected_incident_edges"], "positive incidence control")
    negative = read(ROOT / cfg["target"]["certificate"])
    labels = negative["labels"]
    verification = checked(graph, labels, digest)
    require(verification == negative["verification"] and list(labels[v] for v in (H, Z, U)) == [1, 0, 10]
            and negative["original"]["graph_digest"] == digest, "adverse retained certificate binding")
    try:
        search.candidate(labels[H], 11)
    except ValueError:
        outside = True
    else:
        raise ValueError("retained host one entered the new domain")
    return {"1122": result, "1342": {"labels": labels, "verification": verification,
                "source_certificate": file_ref(ROOT / cfg["target"]["certificate"], ROOT),
                "host_one_excluded_without_search": outside}}


def guards():
    invalid = [(True, 18), (2.0, 18), ("2", 18), (1, 18), (9, 18),
               (2, True), (2, 18.0), (2, "18"), (2, 10), (2, 19)]
    receipts = []
    for a, c in invalid:
        try:
            search.candidate(a, c)
        except ValueError as error:
            receipts.append({"a": a, "c": c, "types": [type(a).__name__, type(c).__name__], "error": str(error)})
        else:
            raise ValueError("invalid search parameters accepted")
    return receipts


def snapshot(cfg, config_path):
    sources = ("lcl/__init__.py", "lcl/verify.py", "lcl/model.py", "pyproject.toml", "requirements.txt")
    hashes = {}
    for rel in sources:
        raw = (ROOT / rel).read_bytes()
        require(raw.replace(b"\r\n", b"\n") == git("show", f"{PARENT}:{rel}").replace(b"\r\n", b"\n"),
                f"production source differs from parent: {rel}")
        put(OUT / "source" / rel, raw)
        hashes[rel] = sha(raw)
    inputs = [cfg["target"]["original"], cfg["target"]["certificate"], *cfg["positive_control"].values()]
    return save(OUT / "identity.json", {"parent": PARENT, "run_id": cfg["run_id"], "limits": LIMITS,
            "configuration": file_ref(config_path, HERE), "presearch_review": file_ref(HERE / "presearch_review.json", HERE),
            "presearch_proof": file_ref(ROOT / PROOF, ROOT),
            "sources_sha256_raw": hashes, "retained": [file_ref(ROOT / name, ROOT) for name in inputs],
            "task_files": [file_ref(HERE / name, HERE) for name in ("run.py", "seed_search.py")],
            "runtime": {"python": sys.version, "implementation": sys.implementation.name, "platform": platform.platform(),
                        "python_executable": ".venv/Scripts/python.exe", "utf8_mode": sys.flags.utf8_mode,
                        "optional_dependencies": []}})


def run_pairs(eligible, neighbors, side, graph, digest, budget):
    receipts = []
    outcome = "EXHAUSTED_RESTRICTED_NEGATIVE"
    settled = True
    for entry in eligible:
        a, c, subsets = (entry[k] for k in ("a", "c", "subsets"))
        if not settled:
            receipts.append({"a": a, "c": c, "status": f"NOT_RUN_AFTER_{outcome}", "nodes": 0})
            continue
        start_nodes, start_time = budget.nodes, budget.elapsed()
        started = {"a": a, "c": c, "starting_nodes": start_nodes, "starting_elapsed_seconds": start_time,
                   "remaining_node_cap": budget.max_nodes - start_nodes,
                   "remaining_time_seconds": max(0.0, budget.max_seconds - start_time), "eligible_subsets": len(subsets)}
        folder = OUT / "pairs" / f"c{c}-a{a}"
        save(folder / "started.json", started)
        events = []

        def subset_event(status, selected):
            event = {"status": status, "selected": selected, "total_nodes": budget.nodes,
                     "elapsed_seconds": budget.elapsed()}
            save(folder / f"subset-{len(events):03d}.json", event)
            events.append(event)

        status, reason, seed_ref = "EXHAUSTED", None, None
        try:
            labels = search.find_witness(neighbors, side, a, c, subsets, budget, subset_event)
            if labels is not None:
                save(folder / "candidate.json", labels)
                seed = seed_record(graph, labels, digest, a, c, 9, 10)
                require(seed["selected_vertices"] in subsets, "first witness outside admitted named subsets")
                seed_ref = save(OUT / "seed.json", seed)
                status, outcome, settled = "SAT", "SAT", False
        except search.LimitReached as exc:
            status, outcome, settled, reason = "INCOMPLETE", "INCOMPLETE", False, str(exc)
        except KeyboardInterrupt:
            status, outcome, settled, reason = "INCOMPLETE", "INCOMPLETE", False, "interrupted"
        except ValueError as exc:
            status, outcome, settled, reason = "REVISE", "REVISE", False, str(exc)
        row = {**started, "status": status, "reason": reason, "nodes": budget.nodes - start_nodes,
               "cumulative_nodes": budget.nodes, "ending_elapsed_seconds": budget.elapsed(),
               "subset_events": len(events), "seed": seed_ref}
        save(folder / "result.json", row)
        receipts.append(row)
    return outcome, receipts


def main():
    path = HERE / "config.json"
    cfg = read(path)
    target = cfg["target"]
    require(git("rev-parse", "HEAD").decode().strip() == PARENT == cfg["parent"], "unexpected accepted parent")
    require(cfg["limits"] == LIMITS and cfg["mode"] == {"first_verified_witness": True, "exact_count": False, "historical_replay": False}
            and target["pins"] == {Z: 0, U: 10} and target["host"] == H and target["a"] == [2, 8]
            and target["c"] == [11, 18] and target["low"] == [0, 8] and target["high"] == [9, 18]
            and cfg["pair_order"] == "descending c then ascending a"
            and cfg["subset_order"] == "lexicographic named subsets"
            and sys.version_info[:2] in ((3, 12), (3, 13)) and sys.flags.utf8_mode == 1, "wrong scope, mode or runtime")
    OUT.mkdir()
    original = read(ROOT / target["original"])
    graph, digest = original["graph"], original["graph_digest"]
    require(graph["profile"] == target["profile"] == [[1], [3], [4], [2], []] and len(graph["vertices"]) == 19,
            "wrong original named target")
    ident = snapshot(cfg, path)
    control_ref = save(OUT / "controls.json", controls(cfg, graph, digest))
    guard_ref = save(OUT / "guards.json", guards())
    neighbors, side = search.topology(graph)
    pairs = search.prefilter(neighbors, side)
    eligible = [row for row in pairs if row["subsets"]]
    require((len(pairs), len(eligible)) == (56, LIMITS["max_pairs"]), "unexpected prefilter")
    review = read(HERE / "presearch_review.json")
    require(review["disposition"] == "ACCEPT" and review["proof_sha256_raw"] == sha((ROOT / PROOF).read_bytes())
            and review["original_sha256_raw"] == sha((ROOT / target["original"]).read_bytes()), "reviewed presearch scope")
    counts = {}
    for entry in eligible:
        counts.setdefault(str(entry["c"]), {})[str(entry["a"])] = len(entry["subsets"])
    require(counts == review["independent_subset_counts_by_c_a"], "prefilter disagrees with independent review")
    prefilter_ref = save(OUT / "prefilter.json", {"initial_pairs": 56, "excluded_pairs": 33, "eligible_pairs": 23, "pairs": pairs})
    save(OUT / "search_started.json", {"run_id": cfg["run_id"], "prefilter": prefilter_ref, "limits": LIMITS,
                                      "original_digest": digest})
    budget = search.Budget(LIMITS["max_assignment_nodes"], LIMITS["max_search_seconds"])
    outcome, statuses = run_pairs(eligible, neighbors, side, graph, digest, budget)
    summary = {"run_id": cfg["run_id"], "status": outcome, "limits": LIMITS, "identity": ident,
               "original": file_ref(ROOT / target["original"], ROOT), "original_digest": digest,
               "controls": control_ref, "guards": guard_ref, "prefilter": prefilter_ref, "pair_statuses": statuses,
               "search_runs": 1, "assignment_nodes": budget.nodes, "elapsed_seconds": budget.elapsed(),
               "exact_solution_count": None, "historical_replays": 0}
    save(OUT / "search_summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "pair_statuses"} | {
        "pair_states": [[row["c"], row["a"], row["status"], row["nodes"]] for row in statuses
                        if not row["status"].startswith("NOT_RUN")]}, sort_keys=True))
    if outcome == "REVISE":
        sys.exit(2)


if __name__ == "__main__":
    main()
