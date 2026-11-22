"""Finite B2 interface diagnostics; resumable only at immutable case boundaries."""
from pathlib import Path
from time import monotonic
import hashlib

from .budget import Limits
from .engines import z3_solve
from .model import branched_prefix_profile, build_graph
from .records import (atomic_json, checked_record, digest, environment, read_json,
                      run_lock, save_source_snapshot, source_inventory, unique_output, utc_now)
from .search import solve
from .states import b2_restrictions, extract_b2_candidate


def validate_config(config):
    expected = {"schema_version", "objective", "engine", "limits", "invocation", "cases"}
    if not isinstance(config, dict) or set(config) != expected:
        raise ValueError("Pilot config must contain exactly: " + ", ".join(sorted(expected)))
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ValueError("Unsupported pilot config schema")
    if config["objective"] != "B2-P1-interval-diagnostic" or config["engine"] not in ("dfs", "z3"):
        raise ValueError("Unsupported objective or engine")
    Limits.from_mapping(config["limits"])
    invocation = config["invocation"]
    if set(invocation) != {"max_cases", "wall_seconds", "max_record_bytes"}:
        raise ValueError("Specify max_cases, wall_seconds, max_record_bytes")
    for key, upper in (("max_cases", 100), ("max_record_bytes", 2_000_000)):
        if type(invocation[key]) is not int or not 1 <= invocation[key] <= upper:
            raise ValueError(f"Invalid {key}: maximum {upper}")
    wall = invocation["wall_seconds"]
    if isinstance(wall, bool) or not isinstance(wall, (float, int)) or not 0 < wall <= 3600:
        raise ValueError("wall_seconds must be positive and <=3600")
    cases = config["cases"]
    if not isinstance(cases, list) or not 1 <= len(cases) <= 5000:
        raise ValueError("Declare between 1 and 5000 cases explicitly")
    identities = []
    for case in cases:
        if not isinstance(case, dict) or set(case) - {"q", "r", "z0", "z1", "K", "interval_start", "side", "root_label"}:
            raise ValueError("Unknown case parameter")
        for key in ("q", "r", "z0", "z1", "K"):
            minimum = 0 if key in ("z0", "z1") else 1
            if type(case.get(key)) is not int or case[key] < minimum:
                raise ValueError(f"Invalid case {key}")
        # Preflight sizes before creating a potentially enormous profile/graph.
        n = case["q"] + case["r"] + case["z0"] + case["z1"] + case["K"] + 5
        if n > 100:
            raise ValueError("Starter pilot target exceeds 100 vertex ingestion cap")
        graph = build_graph(branched_prefix_profile(**{k: case[k] for k in ("q", "r", "z0", "z1", "K")}))
        b2_restrictions(graph, case["K"], case.get("interval_start", 1),
                        case.get("side", "above"), case.get("root_label"))
        identities.append(digest(case))
    if len(set(identities)) != len(identities):
        raise ValueError("Duplicate exact case declarations")
    return identities


def _attempts(directory, case_id):
    return sorted((Path(directory) / "cases").glob(case_id + ".attempt-*.json"))


def _validate_saved_attempt(record, graph, case, case_id, inventory, config):
    """Detect accidental edits and recheck positive evidence before resumption."""
    payload = dict(record)
    expected_hash = payload.pop("record_sha256", None)
    if expected_hash != digest(payload):
        raise ValueError("Saved attempt checksum mismatch; preserve and review the original record")
    if (record["extra"]["case_id"] != case_id or record["config"]["case"] != case
            or record["source"] != inventory
            or record["config"]["pilot_config_sha256"] != digest(config)):
        raise ValueError("Saved attempt does not match the retained case/source/configuration")
    if record["original_graph"] != graph:
        raise ValueError("Saved attempt changed the original graph")
    pins, domains = b2_restrictions(graph, case["K"], case.get("interval_start", 1),
                                   case.get("side", "above"), case.get("root_label"))
    checked = checked_record(graph, record["result"], config=record["config"], source=inventory,
                             expected_pins=pins, expected_domains=domains)
    if (record["expected_restrictions"] != checked["expected_restrictions"]
            or record["original_graph_digest"] != checked["original_graph_digest"]
            or record["certificate"] != checked["certificate"]
            or record["classification"] != checked["classification"]):
        raise ValueError("Saved attempt does not survive independent target/restriction rechecking")
    if record["extra"].get("candidate") is not None:
        candidate = extract_b2_candidate(graph, record["result"]["witness"])
        if candidate != record["extra"]["candidate"]:
            raise ValueError("Saved exploratory prefix does not match its original full witness")


def run_pilot(project, config, *, resume=None, retry_incomplete=False, output=None):
    project = Path(project)
    case_ids = validate_config(config)
    inventory = source_inventory(project)
    env = environment()
    signature = digest({"source": inventory["sha256"], "config": config, "environment": env})
    if resume is not None and output is not None:
        raise ValueError("Choose resume or a new output, not both")
    directory = Path(resume) if resume is not None else Path(output or unique_output(project, "b2"))
    if resume is None:
        directory.mkdir(parents=True, exist_ok=False)
    elif not directory.is_dir():
        raise ValueError("Resume directory does not exist")
    started = monotonic()
    processed = 0
    reason = "all_declared_cases_recorded"
    with run_lock(directory):
        if resume is None:
            save_source_snapshot(project, directory / "source", inventory)
            manifest = {"schema_version": 1, "created_utc": utc_now(), "signature": signature,
                        "source": inventory, "environment": env, "config": config,
                        "case_ids": case_ids, "resume_granularity": "case boundary; no DFS/SMT search-state resume"}
            atomic_json(directory / "manifest.json", manifest)
        else:
            manifest = read_json(directory / "manifest.json")
            own_signature = digest({"source": manifest["source"]["sha256"],
                                    "config": manifest["config"], "environment": manifest["environment"]})
            if (manifest["signature"] != signature or own_signature != signature
                    or manifest["source"] != inventory or manifest["environment"] != env
                    or manifest["config"] != config or manifest["case_ids"] != case_ids):
                raise ValueError("Source, configuration or environment changed; preserve this run and create a new one")
            for relative, expected in inventory["files"].items():
                preserved = directory / "source" / relative
                if not preserved.is_file() or hashlib.sha256(preserved.read_bytes()).hexdigest() != expected:
                    raise ValueError("Preserved source snapshot changed; stop and review this run's provenance")
        (directory / "cases").mkdir(exist_ok=True)
        for case_id, case in zip(case_ids, config["cases"]):
            graph = build_graph(branched_prefix_profile(**{k: case[k] for k in ("q", "r", "z0", "z1", "K")}))
            previous = _attempts(directory, case_id)
            if previous:
                last = read_json(previous[-1])
                _validate_saved_attempt(last, graph, case, case_id, inventory, config)
                if last["classification"] == "QUARANTINED":
                    reason = "QUARANTINED_REVIEW_REQUIRED"
                    break
                if not (retry_incomplete and last["classification"] == "INCOMPLETE"):
                    continue
            remaining = config["invocation"]["wall_seconds"] - (monotonic() - started)
            if processed >= config["invocation"]["max_cases"]:
                reason = "invocation_max_cases"
                break
            if remaining <= 0:
                reason = "invocation_wall_seconds"
                break
            pins, domains = b2_restrictions(graph, case["K"], case.get("interval_start", 1),
                                           case.get("side", "above"), case.get("root_label"))
            effective_limits = Limits.from_mapping(config["limits"]).to_dict()
            effective_limits["time_limit"] = min(effective_limits["time_limit"], remaining)
            engine = solve if config["engine"] == "dfs" else z3_solve
            result = engine(graph, pins=pins, domains=domains, limits=effective_limits)
            record = checked_record(graph, result, config={"case": case, "effective_limits": effective_limits,
                                    "pilot_config_sha256": digest(config)}, source=inventory,
                                    extra={"case_id": case_id, "attempt": len(previous)+1,
                                           "purpose": "finite restricted interface diagnostic; not independent supply"},
                                    expected_pins=pins, expected_domains=domains)
            if record["classification"] != "QUARANTINED" and record["certificate"] and record["certificate"]["valid"]:
                record["extra"]["candidate"] = extract_b2_candidate(graph, result["witness"])
            record["record_sha256"] = digest(record)
            attempt_path = directory / "cases" / f"{case_id}.attempt-{len(previous)+1:04d}.json"
            atomic_json(attempt_path, record, max_bytes=config["invocation"]["max_record_bytes"])
            processed += 1
            checkpoint = _checkpoint(directory, case_ids, processed, started, "case_saved")
            atomic_json(directory / "checkpoint.json", checkpoint, replace=True)
            if record["classification"] in ("QUARANTINED", "INVALID_INPUT", "UNAVAILABLE"):
                reason = record["classification"]
                break
            if result.get("reason") == "interrupted":
                reason = "interrupted"
                break
        checkpoint = _checkpoint(directory, case_ids, processed, started, reason)
        atomic_json(directory / "checkpoint.json", checkpoint, replace=True)
    return dict(checkpoint, directory=str(directory.resolve()))


def _checkpoint(directory, case_ids, processed, started, reason):
    latest, counts = {}, {}
    for case_id in case_ids:
        files = _attempts(directory, case_id)
        if files:
            result = read_json(files[-1])
            status = result["classification"]
            latest[case_id] = {"status": status, "attempts": len(files), "path": str(files[-1].relative_to(directory))}
            counts[status] = counts.get(status, 0) + 1
    return {"updated_utc": utc_now(), "declared_cases": len(case_ids), "recorded_cases": len(latest),
            "unattempted_cases": len(case_ids)-len(latest), "counts": counts, "latest": latest,
            "processed_this_invocation": processed, "elapsed_seconds": monotonic()-started,
            "stop_reason": reason, "research_conclusion": "finite diagnostic only",
            "next_action": "Inspect original targets, restrictions, certificates and baselines before selecting another bounded task"}
