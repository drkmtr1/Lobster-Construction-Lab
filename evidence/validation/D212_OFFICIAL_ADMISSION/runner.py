"""One-shot D212 intake and execution; no scientific imports in preflight."""

import ast
import hashlib
import json
import math
import os
import re
import runpy
import sys
from pathlib import Path
from time import monotonic_ns, process_time_ns

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FROZEN = ROOT / "evidence/validation/D212_MULTI_CENTER_QUOTA_GROWTH"
RUN_ID = "d212-multi-center-quota-growth-001"
PREP = ROOT / "runs" / (RUN_ID + "-intake")
OUTPUT = ROOT / "evidence/runs" / RUN_ID
BASE = "bc3801da2c9ef0770e37a577baa064dc2283a020"
ACCEPTED = "7f71885ecdd13ff17eb6725eef5a61d755d8bd2f"
CASES = ("B2", "B3", "B4")
NANO = 10**9
START = (process_time_ns(), monotonic_ns())


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def elapsed():
    return [process_time_ns() - START[0], monotonic_ns() - START[1]]


def read(path):
    require(path.stat().st_size <= 65_536, f"Input too large: {path.name}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime():
    require(sys.implementation.name == "cpython" and sys.version_info[:2] in
            ((3, 12), (3, 13)), "Unexpected interpreter version")
    require(sys.flags.isolated and sys.flags.no_site and
            sys.flags.dont_write_bytecode, "Interpreter isolation failed")
    cache = PREP / "bytecode-vacant"
    require(sys.pycache_prefix is not None and Path(sys.pycache_prefix).resolve() == cache
            and not cache.exists(), "Isolated bytecode prefix is not vacant")
    executable = Path(sys.executable).resolve()
    require(executable == Path(sys._base_executable).resolve(), "Base interpreter required")
    dll = executable.with_name(f"python{sys.version_info.major}{sys.version_info.minor}.dll")
    return {"executable": str(executable), "sha256": sha(executable),
            "dll": str(dll), "dll_sha256": sha(dll), "version": sys.version,
            "excluded_bytecode_prefix": str(cache)}


def parse_unique(path, expected=None):
    tree = ast.parse(path.read_bytes(), filename=str(path))
    top_level = set()

    def visit(node, scope):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                require(child.name not in scope, f"Duplicate definition in {path.name}")
                scope.add(child.name)
                visit(child, set())
            else:
                visit(child, scope)

    visit(tree, top_level)
    require(expected is None or expected in top_level, f"Missing entry in {path.name}")
    return sorted(top_level)


def original_rows(config):
    # Read the separately frozen literal names, edges rule and counts.
    source = (FROZEN / "ORIGINALS.md").read_text(encoding="utf-8-sig")
    spine = ["s:0", "s:1", "s:2", "s:3"]
    rows = {}
    for line in source.splitlines():
        columns = [part.strip().strip("`") for part in line.strip("|").split("|")]
        if not columns or columns[0] not in CASES:
            continue
        case, raw_profile, raw_centers, raw_terminals, order, size = columns
        require(case not in rows, "Repeated original")
        profile = json.loads(raw_profile)
        require(profile == config["cases"][case]["profile"] and
                all(type(q) is int and q == 1 for section in profile for q in section),
                "Original profile mismatch")
        attachments = list(zip(raw_centers.split(","), raw_terminals.split(","), strict=True))
        roles = {v: {"kind": "spine", "section": i} for i, v in enumerate(spine)}
        edges = [list(pair) for pair in zip(spine, spine[1:])]
        vertices = []
        for i, parent in enumerate(spine):
            vertices.append(parent)
            for j in range(len(profile[i])):
                center, leaf = attachments.pop(0)
                require((center, leaf) == (f"b:{i}:{j}", f"l:{i}:{j}:0"),
                        "Named arm mismatch")
                vertices.extend((center, leaf))
                edges.extend(([parent, center], [center, leaf]))
                roles[center] = {"kind": "branch", "section": i, "branch": j}
                roles[leaf] = {"kind": "leaf", "section": i, "branch": j, "leaf": 0}
        require(not attachments and len(vertices) == int(order)
                and len(edges) == int(size), "Original size mismatch")
        graph = {"schema_version": 1, "profile": profile, "vertices": vertices,
                 "edges": edges, "spine": spine, "roles": roles}
        canonical = {**graph, "vertices": sorted(vertices),
                     "edges": sorted(sorted(edge) for edge in edges)}
        del canonical["schema_version"]
        content = json.dumps(canonical, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False).encode()
        rows[case] = {"graph": graph, "digest": hashlib.sha256(content).hexdigest()}
    require(tuple(rows) == CASES, "Missing or substituted original")
    return rows


def preflight():
    require(not OUTPUT.exists(), "Official output already exists")
    require(not (PREP / "PREFLIGHT.json").exists(), "Preflight already exists")
    config = read(FROZEN / "LIMITS.json")
    require(tuple(config["case_order"]) == CASES and config["execution_authorized"] is False,
            "Unexpected frozen preparation configuration")
    paths = [path for path in sorted((ROOT / "lcl").glob("*.py"))]
    paths += [HERE / "runner.py", HERE / "supervise.ps1", FROZEN / "BINDINGS.md"]
    registered = {}
    for line in (FROZEN / "BINDINGS.md").read_text(encoding="utf-8-sig").splitlines():
        if re.match(r"^[a-f0-9]{40} ", line):
            blob, rel = line.split(" ", 1)
            registered[rel] = blob
            paths.append(ROOT / rel)
    require(len(registered) == 11, "Frozen binding inventory changed")
    files = sorted(set(paths))
    required = {"discovery.py": "discover", "audit_growth.py": "audit_growth",
                "runner.py": "official"}
    definitions = {
        path.relative_to(ROOT).as_posix(): parse_unique(path, required.get(path.name))
        for path in files if path.suffix == ".py"
    }
    for directory in (HERE, FROZEN):
        require(not any(path.suffix in (".pyc", ".pyo") for path in directory.rglob("*")),
                "Unexpected task bytecode")
    originals = original_rows(config)
    result = {
        "status": "PASS", "run": RUN_ID, "prep_checkpoint": BASE,
        "acceptance_checkpoint": ACCEPTED, "runtime": runtime(),
        "registered_blobs": registered, "definitions": definitions,
        "source_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in files},
        "originals": originals, "task_module_imports": 0, "scientific_calls": 0,
    }
    result["measured_before_write_ns"] = elapsed()
    content = json.dumps(result, indent=2, sort_keys=True, allow_nan=False).encode() + b"\n"
    require(len(content) <= 65_536, "Preflight evidence limit")
    cpu, wall = elapsed()
    require(cpu < 3 * NANO and wall < 8 * NANO, "Preflight time limit")
    with (PREP / "PREFLIGHT.json").open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def signature(original, candidate, checked):
    labels = candidate["labels"]
    rows = sorted(checked["growth_rows"].items(), key=lambda pair: pair[1]["threshold"])
    insertion = []
    for host, row in rows:
        cut = row["cut"]
        earlier = [event["cut"] for event in insertion]
        direction = "first" if not earlier else ("left" if cut < min(earlier) else "right")
        insertion.append({
            "host": host, "cut": cut, "threshold": row["threshold"],
            "host_label": row["host_label"], "orientation": row["orientation"],
            "direction": direction, "host_to_cut_interval": sorted([row["host_label"], cut]),
            "lower": sorted((x, v) for v, x in labels.items() if x < cut),
            "upper": sorted((x, v) for v, x in labels.items() if x >= cut),
            "threshold_edges": [edge for edge in row["crossing_edges_and_weights"]
                                if edge[2] == row["threshold"]],
        })
    return {
        "edges_in_original_order": original["edges"],
        "threshold_order": insertion,
        "infinite_quota_domain": {host: {"existing": 1, "growth": "any independent integer >= 0"}
                                   for host, _ in rows},
        "profile": original["profile"],
    }


def official(expected_approval_hash):
    approval_path = PREP / "ADMISSION.json"
    require(sha(approval_path) == expected_approval_hash, "Owner admission hash mismatch")
    approval = read(approval_path)
    require(approval["intent"] == "AUTHORIZE_ONE_OFFICIAL_D212_DIAGNOSTIC" and
            approval["run"] == RUN_ID and approval["prep_checkpoint"] == BASE and
            approval["acceptance_checkpoint"] == ACCEPTED and approval["owner_authorization"],
            "Wrong admission identity")
    require((PREP / "INVOCATION.lock").is_file(), "External measured entry required")
    with (PREP / "PYTHON_ENTRY.lock").open("xb"):
        pass
    for name, key in (("PREFLIGHT.json", "preflight_sha256"),
                      ("PREFLIGHT_OBSERVER.json", "preflight_observer_sha256")):
        require(sha(PREP / name) == approval[key], f"Changed intake record: {name}")
    pre = read(PREP / "PREFLIGHT.json")
    require(pre["status"] == "PASS" and pre["prep_checkpoint"] == BASE
            and pre["acceptance_checkpoint"] == ACCEPTED and pre["run"] == RUN_ID
            and pre["runtime"] == runtime(), "Unapproved preflight or runtime")
    for rel, digest in pre["source_sha256"].items():
        require(sha(ROOT / rel) == digest, f"Local binding changed: {rel}")
    require(not any(p.suffix in (".pyc", ".pyo")
                    for directory in (HERE, FROZEN) for p in directory.rglob("*")),
            "Unexpected task bytecode")
    config = read(FROZEN / "LIMITS.json")
    total = config["total"]
    prep_charge = approval["intake_charge_ns"]
    reserve = NANO

    def measured():
        return [lead + used for lead, used in zip(prep_charge, elapsed(), strict=True)]

    def check():
        cpu, wall = measured()
        require(cpu < total["cpu_seconds"] * NANO - reserve and
                wall < total["wall_seconds"] * NANO - reserve, "Shared execution ceiling")

    check()
    sys.path.insert(0, str(ROOT))
    from lcl.model import build_graph, graph_digest
    from lcl.records import atomic_json, run_lock

    for case in CASES:
        retained = pre["originals"][case]
        rebuilt = build_graph(config["cases"][case]["profile"])
        require(rebuilt == retained["graph"] and graph_digest(rebuilt) == retained["digest"],
                f"Retained original mismatch: {case}")

    OUTPUT.mkdir(exist_ok=False)
    receipts = {}
    sums = [0, 0]
    statuses = {}
    started = []
    error = None

    def save(name, record, terminal=False):
        if not terminal:
            check()
        paths = [p for p in OUTPUT.iterdir() if p.name != "RUNNING.lock"]
        size = len(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False,
                              allow_nan=False).encode("utf-8")) + 1
        # Reserve both final records and one additional copy of this write.
        other_records = 1 if terminal else 2
        require(approval["intake_record_count"] + len(paths) + 1 + other_records
                <= config["record_count_max"]
                and size <= config["record_bytes_max"], "Evidence record limit")
        intake_bytes = approval["intake_evidence_bytes"]
        require(intake_bytes + sum(p.stat().st_size for p in paths) + 2 * size
                + other_records * config["record_bytes_max"] + 256
                <= config["evidence_bytes_max"], "Aggregate evidence ceiling")
        path = OUTPUT / name
        atomic_json(path, record, max_bytes=config["record_bytes_max"])
        receipts[name] = {"sha256": sha(path), "bytes": path.stat().st_size}

    with run_lock(OUTPUT):
        try:
            save("START.json", {
                "run": RUN_ID, "approval_sha256": expected_approval_hash,
                "head": approval["repository_head"], "originals": {
                    case: pre["originals"][case]["digest"] for case in CASES},
                "case_order": list(CASES), "limits": config, "workers": 1,
                "runtime": pre["runtime"], "measured_ns": measured(),
            })
            discover = runpy.run_path(str(FROZEN / "discovery.py"))["discover"]
            audit = runpy.run_path(str(FROZEN / "audit_growth.py"))["audit_growth"]
            for case in CASES:
                check()
                limits = config["cases"][case]
                cpu, wall = measured()
                for spent, key in ((cpu, "cpu_seconds"), (wall, "wall_seconds")):
                    require(spent + limits[key] * NANO + reserve < total[key] * NANO,
                            "Insufficient shared headroom for the next admitted case")
                original_row = pre["originals"][case]
                original = original_row["graph"]
                started.append(case)
                result = discover(original, limits, config["live_frames_max"])
                status = result["status"]
                statuses[case] = status
                require(status in ("CANDIDATE", "INCOMPLETE", "EXHAUSTED_NO_CERTIFICATE"),
                        "Unrecognized scientific disposition")
                for index, key in enumerate(("label_nodes", "join_nodes")):
                    count = result[key]
                    require(type(count) is int and 0 <= count <= limits[key],
                            "Missing or exceeded node count")
                    sums[index] += count
                    require(sums[index] <= total[key], "Shared node ceiling")
                require(type(result["peak_frames"]) is int
                        and 0 <= result["peak_frames"] <= config["live_frames_max"]
                        and type(result["process_cpu_ns"]) is int and result["process_cpu_ns"] >= 0
                        and type(result["wall_seconds"]) in (float, int)
                        and math.isfinite(result["wall_seconds"]) and result["wall_seconds"] >= 0,
                        "Missing case measurement")
                runner_reason = None
                if status != "INCOMPLETE" and (
                        result["process_cpu_ns"] >= limits["cpu_seconds"] * NANO
                        or result["wall_seconds"] >= limits["wall_seconds"]):
                    status = "INCOMPLETE"
                    runner_reason = "Per-case cap reached in returned measurement"
                candidate = result.pop("candidate")
                if candidate is not None:
                    save(f"{case}.raw.json", {"case": case, "original_digest": original_row["digest"],
                                               "candidate": candidate, "search": result})
                checked = None
                structure = None
                if status == "CANDIDATE":
                    require(candidate is not None, "Missing candidate")
                    check()
                    checked = audit(original, candidate, original_row["digest"])
                    status = "AUDITED_POSITIVE" if checked["valid"] else "VERIFICATION_FAILED"
                    if checked["valid"]:
                        structure = signature(original, candidate, checked)
                statuses[case] = status
                save(f"{case}.result.json", {
                    "case": case, "status": status, "search": result, "audit": checked,
                    "runner_reason": runner_reason,
                    "structural_signature": structure, "shared_measured_ns": measured(),
                })
                require(status != "VERIFICATION_FAILED", "Candidate audit failed")
                require(result["reason"] != "interrupted", "Interrupted case")
        except (Exception, KeyboardInterrupt) as exc:
            error = f"{type(exc).__name__}: {str(exc)[:2048]}"
        finally:
            save("TERMINAL.json", {
                "run": RUN_ID, "approval_sha256": expected_approval_hash,
                "session": "STOPPED" if error else "COMPLETE",
                "cases_started": started, "case_status": statuses, "error": error,
                "label_nodes": sums[0], "join_nodes": sums[1],
                "measured_before_terminal_write_ns": measured(),
                "solver_calls": 0, "records_before_terminal": dict(receipts),
            }, terminal=True)
    return 1 if error else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["preflight"]:
        preflight()
    elif len(sys.argv) == 3 and sys.argv[1] == "official":
        raise SystemExit(official(sys.argv[2]))
    else:
        raise SystemExit("No authorized D212 entry selected")
