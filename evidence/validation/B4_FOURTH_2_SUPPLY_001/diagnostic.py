"""Run the four declared above-side queries with the unchanged named exact DFS."""
import hashlib
import json
from pathlib import Path
import platform
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lcl.budget import Limits
from lcl.model import build_graph, graph_digest
from lcl.search import solve
from lcl.verify import verify_certificate, verify_graph


EXPECTED = {"1212": ([[1], [2], [1], [2], []], 8),
            "1122": ([[1], [1], [2], [2], []], 7)}
CAPS = {"max_nodes": 100_000, "time_limit": 5.0, "max_vertices": 16, "max_states": 20_000}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, record):
    payload = (json.dumps(record, indent=2) + "\n").encode()
    require(len(payload) <= 2_000_000, "diagnostic result byte limit")
    with path.open("xb") as out:
        out.write(payload)


def prepare(config):
    require(config["engine"] == "dfs" and config["count"] is False
            and config["workers"] == 1 and config["query_count"] == 4
            and config["max_output_bytes"] == 2_000_000 and config["limits"] == CAPS, "diagnostic budget")
    targets = {}
    for spec in config["targets"]:
        ident = spec["id"]
        require(ident in EXPECTED and ident not in targets, "duplicate or undeclared original")
        profile, p = EXPECTED[ident]
        original = build_graph(profile)
        report = verify_graph(original)
        require(spec["profile"] == profile and report["valid"] and report["n"] == 15 and report["m"] == 14
                and report["graph_digest"] == spec["digest"] == graph_digest(original), "original identity")
        low, high = set(spec["low"]), set(spec["high"])
        require(len(low) == len(spec["low"]) == p and len(high) == len(spec["high"]) == 15 - p
                and low.isdisjoint(high) and low | high == set(original["vertices"])
                and "s:4" in high and all((u in low) != (v in low) for u, v in original["edges"]),
                "named above-side alpha bipartition")
        domains = {v: list(range(p)) for v in low} | {v: list(range(p, 15)) for v in high}
        targets[ident] = (original, domains)
    require(set(targets) == set(EXPECTED), "missing original")
    queries = config["queries"]
    expected_order = [(ident, offset) for ident in EXPECTED for offset in (0, 1)]
    require([(q["target"], q["exit_offset"]) for q in queries] == expected_order, "query order and count")
    for query in queries:
        ident, offset = query["target"], query["exit_offset"]
        interface = "adjacent" if offset == 0 else "nonadjacent"
        require(query["id"] == f"{ident}-{interface}" and query["above_side"] is True
                and query["pins"] == {"s:4": EXPECTED[ident][1] + offset}
                and query["domains"] == targets[ident][1], "undeclared query restrictions")
    return targets


def main():
    config_path = HERE / "diagnostic_config.json"
    config = json.loads(config_path.read_bytes())
    originals = prepare(config)
    regression_path, audit_path = HERE / "regression_result.json", HERE / "independent_audit_result.json"
    regression = json.loads(regression_path.read_bytes())
    audit = json.loads(audit_path.read_bytes())
    require(regression["status"] == audit["status"] == "PASS" and regression["case_count"] == 12
            and audit["same_certificate_count"] == 12 and audit["regression_sha256_raw"] == sha(regression_path)
            and config["starting_commit"] == regression["starting_commit"], "complete the planned direct validation first")
    for name, digest in regression["source_sha256_raw"].items():
        require(sha(ROOT / name) == sha(HERE / "source" / name) == digest, "source changed: " + name)
    out = HERE / "diagnostic_results"
    out.mkdir()
    identity = {"run_id": config["run_id"], "starting_commit": config["starting_commit"],
                "source_sha256_raw": regression["source_sha256_raw"],
                "config_sha256_raw": sha(config_path), "runner_sha256_raw": sha(Path(__file__)),
                "regression_sha256_raw": sha(regression_path), "audit_sha256_raw": sha(audit_path),
                "environment": {"python": sys.version, "executable": sys.executable,
                                "platform": platform.platform(), "utf8_mode": sys.flags.utf8_mode},
                "workers": 1, "count": False}
    summary = []
    for query in config["queries"]:
        original, domains = originals[query["target"]]
        pins = query["pins"]
        digest = graph_digest(original)
        result = solve(original, pins=pins, domains=domains, limits=Limits.from_mapping(CAPS), count=False)
        info = result["restrictions"]
        require(info["scope"] == "restricted" and info["pins"] == pins and info["domains"] == domains
                and info["hidden_symmetry_reduction"] is False and result["limits"] == CAPS
                and result["nodes"] <= CAPS["max_nodes"], "solver scope")
        status, labels = result["status"], result["witness"]
        require(status in ("SAT", "EXHAUSTED_NO_SOLUTION", "INCOMPLETE"), "unexpected solver result")
        certificate = None
        if status == "SAT":
            certificate = verify_certificate(original, labels, digest)
            require(certificate["valid"] and all(labels[v] in domain for v, domain in domains.items())
                    and all(labels[v] == x for v, x in pins.items()) and not result["exhausted"],
                    "witness or restriction check")
        elif status == "EXHAUSTED_NO_SOLUTION":
            require(result["exhausted"] and result["count"] == 0 and labels is None, "inconsistent exhaustion")
        else:
            require(not result["exhausted"] and result["reason"], "incomplete result must have reason")
        path = out / (query["id"] + ".json")
        save(path, {**identity, "query": query, "original_graph": original, "original_graph_digest": digest,
                    "solver_result": result, "independent_certificate": certificate})
        summary.append({"query": query["id"], "status": status, "nodes": result["nodes"],
                        "elapsed_seconds": result["elapsed_seconds"], "reason": result.get("reason"),
                        "exhausted": result["exhausted"], "verified_witness": certificate is not None,
                        "record": path.name, "record_sha256_raw": sha(path)})
    save(out / "summary.json", {**identity, "query_count": len(summary), "queries": summary,
                                "additional_completed_construction_targets": 0})
    print(json.dumps({"query_count": len(summary), "queries": summary}))


if __name__ == "__main__":
    main()
