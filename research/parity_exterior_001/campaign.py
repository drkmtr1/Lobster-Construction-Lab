"""Future official gate and one-worker matched execution. Never run in preparation."""
import argparse
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time
import types


def bindings():
    path = Path(__file__).absolute().with_name("bindings.py")
    api = types.ModuleType("d154_bindings")
    api.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), vars(api))
    return api


def relative(name):
    path = PurePosixPath(name)
    if (path.is_absolute() or name != path.as_posix() or "\\" in name or ":" in name
            or not path.parts or ".." in path.parts):
        raise ValueError("unsafe manifest path")
    return path


def gate(api, args):
    manifest_path = api.ordinary(api.EVIDENCE/"MANIFEST.json")
    raw_manifest = manifest_path.read_bytes()
    if api.sha(raw_manifest) != args.manifest_sha:
        raise ValueError("approved manifest SHA mismatch")
    manifest = api.read(manifest_path)
    if manifest["status"] != "FROZEN_PREPARATION_ONLY" or manifest["task"] != api.TASK:
        raise ValueError("wrong task or freeze status")
    members = {}
    for row in manifest["files"]:
        name = row["path"]
        path = api.ordinary(api.ROOT/relative(name))
        if (name.casefold() in members or path.stat().st_size != row["bytes"]
                or api.sha(path.read_bytes()) != row["sha256"]):
            raise ValueError(f"frozen member identity: {name}")
        members[name.casefold()] = row
    config = api.read(api.KIT/"config.json")
    runtime = api.exact_runtime(config, base_process=args.worker)
    preflight = api.read(api.EVIDENCE/"PREFLIGHT.json")
    preparation = api.read(api.EVIDENCE/"PREPARATION_SUPERVISION.json")
    paths = {p.relative_to(api.ROOT).as_posix() for p in
             (*api.KIT.iterdir(), *(api.EVIDENCE/"input").iterdir())}
    paths.update(config["retained_sha256"])
    needed = paths | {(api.EVIDENCE/name).relative_to(api.ROOT).as_posix() for name in
                      ("PREFLIGHT.json", "PREPARATION_SUPERVISION.json", "REVIEWS.md")}
    if not {n.casefold() for n in needed} <= members.keys():
        raise ValueError("missing reviewed preparation record")
    if (preflight["status"] != "PASS_PARSE_ONLY" or preflight["count"] != 256
            or preflight["runtime"] != runtime or preflight["python_version"] != config["python_version"]
            or preflight["flags"] != {"isolated": True, "no_site": True, "no_bytecode": True}
            or preflight["definitions"] != api.read(api.KIT/"DEFINITIONS.json")
            or any(not preflight[k] for k in ("no_task_imports", "no_task_bytecode",
                                              "approval_vacant", "official_outputs_vacant"))
            or len(preflight["files"]) != len(paths) or {r["path"] for r in preflight["files"]} != paths
            or any(members.get(r["path"].casefold()) != r for r in preflight["files"])):
        raise ValueError("parse-only receipt binding")
    for name, digest in config["retained_sha256"].items():
        if members[name.casefold()]["sha256"] != digest:
            raise ValueError("retained source identity")
    if (preparation["status"] != "PASS" or [r["phase"] for r in preparation["phases"]] != ["corpus", "preflight"]
            or any(r["exit_code"] != 0 or r["timeout"] for r in preparation["phases"])
            or not 0 <= preparation["cpu_seconds"] <= config["preparation"]["cpu_seconds"]
            or not 0 <= preparation["wall_seconds"] <= config["preparation"]["wall_seconds"]
            or config["task"] != api.TASK or config["limits"]["workers"] != 1):
        raise ValueError("measured preparation or task binding")
    approval = api.ordinary(Path(args.approval).absolute())
    if approval != api.ordinary(api.ROOT/config["approval"]) or approval.stat().st_size > 4096:
        raise ValueError("unapproved authority path")
    raw_approval = approval.read_bytes()
    if api.read(approval) != {"task":api.TASK, "manifest_sha256":args.manifest_sha,
                              "status":"AUTHORIZED_FOR_OFFICIAL_RUN"}:
        raise ValueError("later Owner approval record required")
    frozen = len(raw_manifest)+len(raw_approval)+sum(row["bytes"] for row in members.values())
    if frozen + config["reserve"]["final_records_bytes"] + 4096 > config["limits"]["evidence_bytes"]:
        raise ValueError("campaign evidence unavailable")
    return config, api.ordinary(api.ROOT/config["output"]), frozen, preparation, api.sha(raw_approval)


def corpus(api):
    root = api.EVIDENCE/"input"
    index = api.read(root/"corpus_index.json")["targets"]
    for start in range(0, 256, 16):
        shard = index[start]["shard"]
        items = api.read(root/shard)
        if len(items) != 16:
            raise ValueError("frozen shard size")
        for row, entry in zip(items, index[start:start+16]):
            if (api.sha(api.encoded(row)) != entry["record_sha256"]
                    or {k:v for k,v in row.items() if k != "graph"} !=
                       {k:v for k,v in entry.items() if k != "record_sha256"}):
                raise ValueError("frozen original binding")
            yield row


def disposition(api, row, prefix, arm, meter, primary, audit, engine, retained_audit, check, common=None):
    meter.tick("dispositions")
    start = dict(meter.counts)
    if common is not None:
        result = common
        basis = "T-positive-by-inclusion"
    else:
        result = primary.search(row, prefix, arm, meter, engine)
        basis = "dedicated-arm"
    if result["claim"] == "YES":
        reviewed = audit.positive(row, prefix, arm, result["witness"], check, retained_audit)
    else:
        reviewed = audit.negative(row, prefix, arm, meter, retained_audit)
    meter.time_check()
    return {"id":row["target_id"], "graph_digest":row["digest"], "param":row["param"], "arm":arm,
            "basis":basis, "result":result, "audit":reviewed,
            "meter_delta":{k:v-start[k] for k,v in meter.counts.items()}}


def worker(api, args, config, output, frozen, approval_hash):
    if ({p.name for p in output.iterdir()} != {"CLAIM.json"} or
            api.read(output/"CLAIM.json") != {"manifest_sha256": args.manifest_sha,
                                             "approval_sha256": approval_hash, "status": "CLAIMED_ONCE"}):
        raise ValueError("worker claim drift or occupied output")
    with (output/"WORKER").open("xb") as f:
        f.write(b"D154 one worker\n")
    retained_campaign = api.load_exact("d154_retained_meter", api.LEGACY/"campaign.py")
    meter = retained_campaign.Meter(config, output, frozen+sum(p.stat().st_size for p in output.iterdir()))
    active, arm, reason = None, None, None
    positives, negatives, pairs, separating = 0, 0, 0, 0
    controls = []
    try:
        engine = api.load_exact("d154_retained_folded", api.LEGACY/"engine.py")
        retained_audit = api.load_exact("d154_retained_raw", api.LEGACY/"audit.py")
        checker = api.load_exact("d154_original_checker", api.ROOT/"lcl/verify.py").verify_certificate
        primary = api.load_exact("d154_primary", api.KIT/"generator.py")
        audit = api.load_exact("d154_independent", api.KIT/"independent.py")
        prefix = api.read(api.EVIDENCE/"input/prefix.json")
        retained_audit.verify_prefix(prefix, checker)
        for fixture in config["allocator_controls"]:
            values = fixture["A"], fixture["B"], fixture["s"], tuple(fixture["quotas"]), meter
            folded = engine.folded_support(*values)
            raw = retained_audit.raw_support(*values)
            if (folded is not None) != fixture["expected"] or raw != fixture["expected"]:
                raise ValueError(f"exact allocation discrimination control: {fixture['name']}")
            controls.append({"case":fixture["name"], "folded":folded, "raw":raw, "expected":fixture["expected"]})
        meter.write("ALLOCATOR_CONTROLS.json", controls)
        for row in corpus(api):
            active = row["target_id"]
            meter.tick("targets")
            arm = "T"
            t = disposition(api, row, prefix, arm, meter, primary, audit, engine, retained_audit, checker)
            meter.write(active+"-T.json", t)
            arm = "E"
            common = t["result"] if t["result"]["claim"] == "YES" else None
            e = disposition(api, row, prefix, arm, meter, primary, audit, engine, retained_audit, checker, common)
            meter.write(active+"-E.json", e)
            pairs += 1
            if e["result"]["claim"] == "YES":
                positives += 1
                separating += int(t["result"]["claim"] == "NO")
            else:
                negatives += 1
            active, arm = None, None
        if pairs != 256:
            raise ValueError("official corpus did not yield every authorized original")
        meter.time_check()
    except Exception as error:
        reason = f"{type(error).__name__}: {error}"[:300]
    universal = "FALSIFIED" if negatives else "VERIFIED_FINITE" if positives == 256 else "UNDECIDED"
    summary = {"status":"COMPLETE" if reason is None else "INCOMPLETE", "reason":reason,
               "active_target":active, "active_arm":arm, "entered":meter.counts, "paired_audits":pairs,
               "E_yes":positives, "E_exhaustive_no":negatives, "T_no_E_yes":separating,
               "universal_E_hypothesis":universal, "cpu_seconds":time.process_time(),
               "bytes_before_summary":meter.bytes}
    meter.write("SUMMARY.json", summary, emergency=True)
    return int(reason is not None)


def supervise(api, args, config, output, preparation, approval_hash, started):
    if os.path.lexists(output):
        raise ValueError("official output must be vacant")
    output.mkdir()
    api.write_new(output/"CLAIM.json", {"manifest_sha256":args.manifest_sha, "approval_sha256":approval_hash,
                                        "status":"CLAIMED_ONCE"}, 4096)
    command = [sys._base_executable, "-I", "-S", "-B", str(Path(__file__).absolute()),
               "--manifest-sha", args.manifest_sha, "--approval", str(Path(args.approval).absolute()), "--worker"]
    wall_limit = config["limits"]["wall_seconds"]-config["reserve"]["preparation_and_startup_wall_seconds"]
    process, reason = None, None
    try:
        process = subprocess.Popen(command, cwd=api.ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        process.wait(timeout=max(0, wall_limit-(time.monotonic()-started)))
    except (subprocess.TimeoutExpired, KeyboardInterrupt, OSError) as error:
        reason = type(error).__name__
    if reason and process is not None and process.poll() is None:
        try:
            process.kill()
            process.wait(timeout=5)
        except (subprocess.TimeoutExpired, OSError):
            reason += ": worker exit unconfirmed"
    try:
        summary = api.read(output/"SUMMARY.json")
    except (OSError, ValueError):
        summary = {}
        reason = reason or "worker summary unavailable"
    worker_cpu = summary.get("cpu_seconds")
    supervisor_cpu = time.process_time()
    wall = time.monotonic()-started
    cpu = (preparation["cpu_seconds"]+supervisor_cpu+worker_cpu
           if type(worker_cpu) in (int, float) and worker_cpu >= 0 else None)
    combined_wall = preparation["wall_seconds"]+wall
    status = ("COMPLETE" if reason is None and process is not None and process.returncode == 0
              and summary.get("status") == "COMPLETE" and cpu is not None and cpu+1 <= config["limits"]["cpu_seconds"]
              and combined_wall+1 <= config["limits"]["wall_seconds"] and wall <= wall_limit else "INCOMPLETE")
    api.write_new(output/"SUPERVISION.json",
                  {"status":status, "reason":reason or (None if status == "COMPLETE" else "worker or combined cap"),
                   "worker_exit":process.returncode if process is not None else None, "worker_cpu":worker_cpu,
                   "supervisor_cpu":supervisor_cpu, "combined_cpu":cpu, "combined_observed_wall":combined_wall}, 8192)
    return int(status != "COMPLETE")


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha", required=True)
    parser.add_argument("--approval", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    api = bindings()
    config, output, frozen, preparation, approval_hash = gate(api, args)
    if args.worker:
        code = worker(api, args, config, output, frozen, approval_hash)
    else:
        code = supervise(api, args, config, output, preparation, approval_hash, started)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
