"""Original-target certificates, immutable attempt files and source snapshots."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import uuid

from . import __version__
from .engines import dependency_versions
from .model import graph_digest
from .verify import verify_certificate


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path, max_bytes=2_000_000):
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise ValueError(f"Input exceeds {max_bytes} byte design limit: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_json(path, value, *, replace=False, max_bytes=2_000_000):
    path = Path(path)
    data = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                      allow_nan=False).encode("utf-8") + b"\n"
    if len(data) > max_bytes:
        raise ValueError("Record exceeds configured output limit")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not replace:
        raise FileExistsError(f"Preserved evidence already exists: {path}")
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        # Calls are protected by a run lock for shared manifests/checkpoints.
        # Attempt IDs are unique; this is not a distributed filesystem protocol.
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def source_inventory(project):
    project = Path(project)
    paths = list((project / "lcl").glob("*.py"))
    paths += list(project.glob("requirements*.txt"))
    if (project / "pyproject.toml").exists():
        paths.append(project / "pyproject.toml")
    files = {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(paths)}
    return {"files": files, "sha256": digest(files)}


def environment():
    return {"python": platform.python_version(), "implementation": platform.python_implementation(),
            "platform": platform.platform(), "machine": platform.machine(),
            "package_version": __version__, "optional_dependencies": dependency_versions()}


def save_source_snapshot(project, destination, inventory):
    project, destination = Path(project), Path(destination)
    for relative, expected in inventory["files"].items():
        src = project / relative
        data = src.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError("Source changed during snapshot; retry after edits finish")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)


def checked_record(graph, result, *, config, source, extra=None,
                   expected_pins=None, expected_domains=None):
    """Bind a result to the caller-retained original, never the solver's graph."""
    target_digest = graph_digest(graph)
    labels = result.get("witness", result.get("labels"))
    certificate = None
    classification = result.get("status", "UNKNOWN")
    consistency_errors = []
    pins = {} if expected_pins is None else dict(expected_pins)
    domains = {} if expected_domains is None else {v: sorted(set(xs)) for v, xs in expected_domains.items()}
    if labels is not None:
        certificate = verify_certificate(graph, labels, expected_graph_digest=target_digest)
        if not certificate["valid"]:
            classification = "QUARANTINED"
        else:
            for v, x in pins.items():
                if v not in labels or labels[v] != x or type(x) is not int:
                    consistency_errors.append(f"Witness violates caller-retained pin at {v}")
            for v, values in domains.items():
                if v not in labels or labels[v] not in values:
                    consistency_errors.append(f"Witness violates caller-retained domain at {v}")
    elif classification in ("SAT", "CONSTRUCTED"):
        classification = "QUARANTINED"
        certificate = {"valid": False, "errors": ["Positive result has no witness"]}
    status = result.get("status")
    if status in ("EXHAUSTED_NO_SOLUTION", "RESTRICTED_INFEASIBLE") and labels is not None:
        consistency_errors.append("Negative status contradicts a supplied witness")
    if status == "EXHAUSTED_NO_SOLUTION" and (result.get("exhausted") is not True or result.get("count") != 0):
        consistency_errors.append("Exhaustive negative requires exhausted=true and exact count zero")
    if status == "INCOMPLETE" and (result.get("exhausted") is True or result.get("count") is not None):
        consistency_errors.append("Incomplete result cannot claim an exact count or exhaustion")
    count = result.get("count")
    lower = result.get("count_lower_bound")
    if count is not None:
        if type(count) is not int or count < 0 or result.get("exhausted") is not True:
            consistency_errors.append("Exact count must be a nonnegative integer after exhaustion")
        if status == "SAT" and (type(count) is not int or count < 1):
            consistency_errors.append("SAT exact count must be positive")
    if lower is not None and (type(lower) is not int or lower < 0):
        consistency_errors.append("Count lower bound must be a nonnegative integer")
    if labels is not None and type(lower) is int and lower < 1:
        consistency_errors.append("A supplied witness requires a positive count lower bound when reported")
    if status in ("EXHAUSTED_NO_SOLUTION", "RESTRICTED_INFEASIBLE") and lower not in (None, 0):
        consistency_errors.append("Negative status cannot carry a positive count lower bound")
    if type(count) is int and type(lower) is int and lower > count:
        consistency_errors.append("Lower bound exceeds exact count")
    if consistency_errors:
        classification = "QUARANTINED"
    record = {"schema_version": 1, "created_utc": utc_now(),
              "classification": classification, "original_graph": graph,
              "original_graph_digest": target_digest, "result": result,
              "certificate": certificate, "config": config, "config_sha256": digest(config),
              "source": source, "environment": environment(),
              "expected_restrictions": {"pins": pins, "domains": domains},
              "consistency_errors": consistency_errors, "universal_claim": False}
    if extra:
        record["extra"] = extra
    return record


def save_single(project, output, graph, result, config, *, expected_pins=None, expected_domains=None):
    """One invocation directory with its exact code/dependencies and target."""
    project, output = Path(project), Path(output)
    if output.exists():
        raise FileExistsError("Choose a new output directory; existing evidence is preserved")
    output.mkdir(parents=True)
    inventory = source_inventory(project)
    save_source_snapshot(project, output / "source", inventory)
    record = checked_record(graph, result, config=config, source=inventory,
                            expected_pins=expected_pins, expected_domains=expected_domains)
    record["record_sha256"] = digest(record)
    atomic_json(output / "record.json", record)
    atomic_json(output / "config.json", config)
    return record


@contextmanager
def run_lock(directory):
    lock = Path(directory) / "RUNNING.lock"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"pid": os.getpid(), "created_utc": utc_now()}))
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def unique_output(project, prefix="example"):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path(project) / "runs" / f"{prefix}-{stamp}-{uuid.uuid4().hex[:8]}"
