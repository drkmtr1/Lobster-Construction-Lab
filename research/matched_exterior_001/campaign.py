"""Future supervised entry point. Preparation never calls this file."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import time


KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_MATCHED_EXTERIOR_TWO_CENTER_001"
MANIFEST = EVIDENCE / "MANIFEST.json"


class Limit(RuntimeError):
    pass


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ordinary(path):
    for entry in reversed([path, *path.parents]):
        if os.path.lexists(entry):
            attributes = getattr(entry.lstat(), "st_file_attributes", 0)
            if entry.is_symlink() or attributes & 0x400:
                raise ValueError(f"unsafe filesystem entry: {entry}")
    return path


def valid_relative(name):
    path = PurePosixPath(name)
    if (path.is_absolute() or name != path.as_posix() or "\\" in name or ":" in name
            or any(part in (".", "..") for part in path.parts) or not path.parts):
        raise ValueError("unsafe frozen relative path")
    return path


def exact_runtime(config, worker):
    runtime = config["runtime"]
    base = ordinary(Path(sys._base_executable).absolute())
    paths = {"base":base, "dll":base.with_name(runtime["dll"]),
             "cfg":ROOT / runtime["cfg"], "venv":ROOT / runtime["venv"]}
    if base.name.casefold() != runtime["base"].casefold():
        raise ValueError("unexpected base interpreter name")
    for key, path in paths.items():
        if digest(ordinary(path)) != runtime[key+"_sha"]:
            raise ValueError(f"runtime file drift: {key}")
    expected = base if worker else ROOT / runtime["venv"]
    if (Path(sys.executable).resolve() != expected.resolve()
            or platform.python_version() != config["python_version"]
            or not sys.dont_write_bytecode or not sys.flags.isolated or not sys.flags.no_site):
        raise ValueError("wrong frozen runtime or flags")


def gate(arguments):
    ordinary(MANIFEST)
    if digest(MANIFEST) != arguments.manifest_sha:
        raise ValueError("manifest SHA mismatch")
    manifest = read(MANIFEST)
    if manifest["status"] != "FROZEN_PREPARATION_ONLY":
        raise ValueError("manifest status")
    members = {}
    for item in manifest["files"]:
        name = item["path"]
        path = ordinary(ROOT / valid_relative(name))
        if name.casefold() in members or path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            raise ValueError(f"frozen identity mismatch: {name}")
        members[name.casefold()] = item
    needed = [KIT / x for x in ("campaign.py", "engine.py", "audit.py", "prepare.py", "preflight.py", "check_originals.py", "config.json", "DEFINITIONS.json", "CONTRACT.md")]
    needed += [ROOT / "lcl" / x for x in ("__init__.py", "model.py", "verify.py")]
    needed += [EVIDENCE / x for x in ("REVIEWS.md", "PREFLIGHT.json", "PREPARATION_SUPERVISION.json", "RAW_ORIGINAL_CHECK.json",
                                     "input/corpus_index.json", "input/prefix.json")]
    if any(path.relative_to(ROOT).as_posix().casefold() not in members for path in needed):
        raise ValueError("incomplete frozen source and input inventory")
    preflight = read(EVIDENCE / "PREFLIGHT.json")
    if (preflight["status"] != "PASS_PARSE_ONLY" or not preflight["no_task_imports"]
            or not preflight["official_outputs_vacant"] or not preflight["approval_vacant"]):
        raise ValueError("parse-only receipt")
    for bound in preflight["files"]:
        if members.get(bound["path"].casefold()) != bound:
            raise ValueError("preflight-to-manifest binding")
    supervision = read(EVIDENCE / "PREPARATION_SUPERVISION.json")
    if supervision["status"] != "PASS" or any(
        phase["exit_code"] != 0 or phase["timeout"] for phase in supervision["phases"]
    ):
        raise ValueError("preparation supervision record")
    config = read(KIT / "config.json")
    exact_runtime(config, arguments.worker)
    expected_runtime = {key:config["runtime"][key+"_sha"] for key in ("base","dll","cfg","venv")}
    bound_sources = {item["path"] for item in preflight["files"]}
    expected_sources = {path.relative_to(ROOT).as_posix() for path in KIT.iterdir() if path.is_file()}
    expected_sources.update(path.relative_to(ROOT).as_posix() for path in (EVIDENCE/"input").iterdir())
    expected_sources.update("lcl/"+name for name in ("__init__.py","model.py","verify.py"))
    expected_sources.add((EVIDENCE/"RAW_ORIGINAL_CHECK.json").relative_to(ROOT).as_posix())
    raw_check = read(EVIDENCE/"RAW_ORIGINAL_CHECK.json")
    checker_hashes = {name:members["lcl/"+name]["sha256"] for name in ("__init__.py","model.py","verify.py")}
    if (raw_check["status"] != "PASS_SOURCE_ONLY_ORIGINALS" or raw_check["originals_checked"] != 320
            or raw_check["source_sha256"] != checker_hashes or not raw_check["preexisting_lcl_caches_bypassed"]):
        raise ValueError("uncached original-source custody")
    if (preflight["runtime"] != expected_runtime or preflight["python_version"] != config["python_version"]
            or preflight["flags"] != {"isolated":True,"no_site":True,"no_bytecode":True}
            or preflight["parsed_definitions"] != read(KIT/"DEFINITIONS.json")
            or bound_sources != expected_sources or len(bound_sources) != len(preflight["files"])):
        raise ValueError("inexact reviewed parse-only contents")
    if (not 0 <= supervision["cpu_seconds"] < 300 or not 0 <= supervision["wall_seconds"] < 300
            or [phase["phase"] for phase in supervision["phases"]] != ["corpus","raw-original-check","preflight"]):
        raise ValueError("preparation exceeded its reserve share")
    approval = ordinary(Path(arguments.approval).absolute())
    expected = ordinary(ROOT / config["approval"])
    if approval != expected:
        raise ValueError("unexpected approval path")
    approval_bytes = approval.read_bytes()
    if len(approval_bytes) > config["limits"]["record_bytes"]:
        raise ValueError("approval record ceiling")
    grant = json.loads(approval_bytes)
    if grant != {"task":config["task"], "manifest_sha256":arguments.manifest_sha,
                 "status":"AUTHORIZED_FOR_OFFICIAL_RUN"}:
        raise ValueError("future execution authorization missing or invalid")
    frozen_bytes = sum(item["bytes"] for item in members.values()) + MANIFEST.stat().st_size + len(approval_bytes)
    if frozen_bytes + config["reserve"]["final_records_bytes"] + 1024 > config["limits"]["evidence_bytes"]:
        raise ValueError("no budget for official evidence")
    output = ordinary(ROOT / config["output"])
    if manifest["task"] != config["task"] or len(members) != len(manifest["files"]):
        raise ValueError("task binding")
    return config, output, frozen_bytes, members, hashlib.sha256(approval_bytes).hexdigest(), supervision


class Meter:
    def __init__(self, config, output, frozen_bytes):
        self.limits = config["limits"]
        self.reserve = config["reserve"]
        self.output = output
        self.bytes = frozen_bytes
        self.counts = dict.fromkeys(("targets","dispositions","exterior_nodes","transfer_states","transitions"),0)
        self.poll = 0

    def time_check(self):
        if time.process_time() > self.limits["cpu_seconds"] - self.reserve["preparation_and_startup_cpu_seconds"]:
            raise Limit("process-CPU cap")

    def tick(self, name):
        if self.counts[name] == self.limits[name]:
            raise Limit(f"{name} cap")
        self.counts[name] += 1
        self.poll += 1
        if self.poll % 64 == 0:
            self.time_check()

    def memory(self, retained):
        if retained > self.reserve["max_live_candidate_states"]:
            raise Limit("retained per-candidate state ceiling")

    def write(self, name, value, emergency=False):
        payload = (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))+"\n").encode()
        available = self.limits["evidence_bytes"] - self.bytes
        if not emergency:
            available -= self.reserve["final_records_bytes"]
        if name in ("SUMMARY.json","SUPERVISION.json"):
            available = min(available, 8192)
        if len(payload) > min(available,self.limits["record_bytes"]):
            raise Limit("evidence cap")
        with (self.output / name).open("xb") as stream:
            stream.write(payload)
        self.bytes += len(payload)


def corpus(members):
    raw_index = read(EVIDENCE / "input/corpus_index.json")
    prefix = read(EVIDENCE / "input/prefix.json")
    rows = raw_index["targets"]
    shard_name = None
    shard = {}
    for entry in rows:
        name = entry["shard"]
        if name != shard_name:
            path = EVIDENCE / "input" / valid_relative(name)
            if path.relative_to(ROOT).as_posix().casefold() not in members:
                raise ValueError("unmanifested input shard")
            shard = {row["target_id"]: row for row in read(path)}
            shard_name = name
        row = shard[entry["target_id"]]
        raw = (json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)+"\n").encode()
        if (hashlib.sha256(raw).hexdigest() != entry["record_sha256"] or
                {k:v for k,v in row.items() if k != "graph"} !=
                {k:v for k,v in entry.items() if k != "record_sha256"}):
            raise ValueError("frozen corpus index mismatch")
        yield row, prefix


def evaluate(engine, audit, verify, row, prefix, arm, meter, common=None):
    meter.tick("dispositions")
    begun = dict(meter.counts)
    if common is None:
        result = engine.search(row, prefix, arm, meter)
        derivation = "dedicated-arm-search"
    else:
        result = common
        derivation = "checked-T-witness-admitted-by-E"
    if result["claim"] == "YES":
        reviewed = audit.positive(row, prefix, arm, result["witness"], verify)
    else:
        reviewed = audit.negative(row, prefix, arm, meter)
    meter.time_check()
    return {"target_id":row["target_id"], "digest":row["digest"], "arm":arm, "result":result,
            "review":reviewed, "derivation":derivation,
            "meter_delta":{k:v-begun[k] for k,v in meter.counts.items()}}


def run_worker(config, output, frozen_bytes, members, approval_digest):
    claim = read(output / "CLAIM.json")
    permit = {"sha":digest(MANIFEST), "approval":approval_digest, "status":"CLAIMED_ONCE"}
    if claim != permit or any(path.name != "CLAIM.json" for path in output.iterdir()):
        raise ValueError("unexpected official output ownership")
    # Exclusive worker claim also prevents direct invocations after a launch interruption.
    with (output / "WORKER").open("xb") as stream:
        stream.write(b"official worker once\n")
    meter = Meter(config, output, frozen_bytes)
    meter.bytes += (output / "CLAIM.json").stat().st_size + (output / "WORKER").stat().st_size
    cache = ordinary(output/".source-only-cache-unused")
    if os.path.lexists(cache) or any(path.is_dir() for path in KIT.iterdir()):
        raise ValueError("unexpected bytecode cache or module-shadow directory")
    for name in ("model","verify"):
        if os.path.lexists(ROOT/"lcl"/name):
            raise ValueError("unexpected original-source package shadow")
    sys.pycache_prefix = str(cache)
    sys.path[:0] = [str(KIT), str(ROOT)]
    import engine
    import audit
    from lcl.verify import verify_certificate
    observed = {}
    prefix = read(EVIDENCE / "input/prefix.json")
    audit.verify_prefix(prefix, verify_certificate)
    active = None
    active_arm = None
    complete_two_center = 0
    separation = 0
    status = "COMPLETE"
    failure = None
    try:
        fixture = config["allocator_control"]
        args = (fixture["A"], fixture["B"], fixture["s"], tuple(fixture["quotas"]), meter)
        folded = engine.folded_support(*args)
        raw = audit.raw_support(*args)
        if (folded is not None) != fixture["expected"] or raw != fixture["expected"]:
            raise ValueError("D145 independent allocator control mismatch")
        meter.write("ALLOCATOR_CONTROL.json", {"expected":fixture["expected"], "folded":folded,
                                               "independent_raw":raw})
        controls = {row["name"]:row for row in config["controls"]}
        for row, prefix in corpus(members):
            active = row["target_id"]
            meter.tick("targets")
            active_arm = "T"
            t = evaluate(engine, audit, verify_certificate, row, prefix, "T", meter)
            meter.write(active+"-T.json", t)
            active_arm = "E"
            e = evaluate(engine, audit, verify_certificate, row, prefix, "E", meter,
                         t["result"] if t["result"]["claim"] == "YES" else None)
            meter.write(active+"-E.json", e)
            pair = (t["result"]["claim"],e["result"]["claim"])
            if row["control"]:
                wanted = controls[row["control"]]
                observed[row["control"]] = pair
                if pair != (wanted["T"],wanted["E"]):
                    raise ValueError("frozen common/adverse/separating control disagreed")
            if row["second_centers"] == 2:
                complete_two_center += 1
                separation += int(pair == ("NO","YES"))
            active = active_arm = None
        if set(observed) != set(controls):
            raise ValueError("some required controls did not execute")
    except Limit as error:
        status, failure = "INCOMPLETE", str(error)
    except (ValueError, KeyError, OSError, MemoryError) as error:
        status, failure = "INCOMPLETE", str(error)[:300]
    meter.write("SUMMARY.json", {"status":status, "reason":failure, "active_target":active, "active_arm":active_arm,
                                  "counts":meter.counts, "controls":observed,
                                  "audited_two_center_pairs":complete_two_center,
                                  "audited_two_center_separations":separation,
                                  "cpu_seconds":time.process_time(),
                                  "evidence_bytes_before_summary":meter.bytes}, emergency=True)
    return int(status != "COMPLETE")


def supervise(arguments, config, output, frozen_bytes, approval_digest, preparation, started):
    if os.path.lexists(output):
        raise ValueError("official output must be vacant")
    wall = config["limits"]["wall_seconds"] - config["reserve"]["preparation_and_startup_wall_seconds"]
    output.mkdir()
    claim = {"sha":arguments.manifest_sha,"approval":approval_digest,"status":"CLAIMED_ONCE"}
    with (output / "CLAIM.json").open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(claim,stream,sort_keys=True,separators=(",",":"))
    command = [sys._base_executable,"-I","-S","-B",str(Path(__file__).absolute()),
               "--manifest-sha", arguments.manifest_sha, "--approval", arguments.approval, "--worker"]
    process = None
    reason = None
    try:
        process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        process.wait(timeout=max(0,wall-(time.monotonic()-started)))
    except subprocess.TimeoutExpired:
        reason = "external wall cap"
    except KeyboardInterrupt:
        reason = "interrupted"
    except OSError as error:
        reason = str(error)[:300]
    if reason and process is not None and process.poll() is None:
        try:
            process.kill()
            process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            reason += "; child exit could not be confirmed"
    try:
        latest = read(output/"SUMMARY.json") if (output/"SUMMARY.json").is_file() else {}
    except (OSError, ValueError):
        latest = {}
        reason = reason or "unreadable worker summary"
    worker_exit = process.returncode if process is not None else None
    cpu = time.process_time()
    observed_wall = time.monotonic()-started
    worker_cpu = latest.get("cpu_seconds")
    cpu_valid = (type(worker_cpu) in (float,int) and 0 <= worker_cpu
                 <= config["limits"]["cpu_seconds"]-config["reserve"]["preparation_and_startup_cpu_seconds"])
    combined_cpu = preparation["cpu_seconds"]+cpu+worker_cpu if cpu_valid else None
    combined_wall = preparation["wall_seconds"]+observed_wall
    # Allow one second for final serialization and process closeout in both phases.
    ok = (not reason and worker_exit == 0 and latest.get("status") == "COMPLETE"
          and combined_cpu is not None and combined_cpu+1 <= config["limits"]["cpu_seconds"]
          and observed_wall <= wall and combined_wall+1 <= config["limits"]["wall_seconds"]
          and cpu+preparation["cpu_seconds"]+1 <= config["reserve"]["preparation_and_startup_cpu_seconds"])
    final_meter = Meter(config,output,frozen_bytes+sum(path.stat().st_size for path in output.iterdir()))
    final_meter.write("SUPERVISION.json", {"status":"COMPLETE" if ok else "INCOMPLETE",
                                           "worker_exit":worker_exit,"wall_seconds":observed_wall,
                                           "supervisor_cpu_seconds":cpu,
                                           "reason":reason or (None if ok else "worker or combined resource check"),
                                           "measured_worker_cpu_seconds":worker_cpu,
                                           "measured_combined_cpu_seconds":combined_cpu,
                                           "observed_combined_wall_seconds":combined_wall,
                                           "evidence_bytes_before_supervision":final_meter.bytes}, emergency=True)
    return int(not ok)


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha", required=True)
    parser.add_argument("--approval", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()
    config, output, frozen_bytes, members, approval_digest, preparation = gate(arguments)
    if arguments.worker:
        code = run_worker(config, output, frozen_bytes, members, approval_digest)
    else:
        code = supervise(arguments, config, output, frozen_bytes, approval_digest, preparation, started)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
