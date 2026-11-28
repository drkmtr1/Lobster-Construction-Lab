"""D231 operational observer v1. Uses qualified V9 native primitives at creation."""
from contextlib import ExitStack
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import msvcrt
import os
from pathlib import Path
import re
import subprocess
import sys
from time import monotonic, process_time, sleep

VERSION = "D231-operations-v1"
OPS = Path(__file__).resolve().parent
ROOT = OPS.parent.parent
CONFIG = json.loads((OPS / "identities.json").read_bytes())


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_new(path, record):
    data = (json.dumps(record, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def validate_receipt(path, expected):
    raw = path.read_bytes()
    if len(raw) > 65536 or not re.fullmatch("[a-f0-9]{64}", expected) or sha256(raw).hexdigest() != expected:
        raise ValueError("receipt bytes or digest")
    data = json.loads(raw)
    if data.get("operational_version") != VERSION:
        raise ValueError("receipt version")
    if data.get("decision") == "AUTHORIZE_D231_EXECUTION":
        address = ROOT / "runs" / CONFIG["run_id"]
        if (path != address.with_name(address.name + "-admission.json")
                or data.get("run_id") != CONFIG["run_id"]
                or data.get("verified_checkpoint") != CONFIG["science"]["preparation"]
                or data.get("source_manifest_sha256") != CONFIG["science"]["manifest_sha256"]
                or data.get("registration_sha256") != CONFIG["science"]["registration_sha256"]
                or data.get("authority_checkpoint") != CONFIG["science"]["authority_checkpoint"]
                or not re.fullmatch("[0-9a-f]{40}", data.get("execution_checkout", ""))
                or not re.fullmatch("[0-9a-f]{64}", data.get("qualification_manifest_sha256", ""))
                or not all(isinstance(data.get(k), str) and data[k].strip()
                           for k in ("director_review", "owner_authorization"))
                or data.get("inner_wall_seconds") != 1198
                or any((ROOT / CONFIG["science"][k]).exists() for k in ("output", "archive"))):
            raise ValueError("scientific receipt fields or destination")
        args = ["-B", "-m", "research.d231_unequal_pair_kernel.driver",
                "--admission", str(path.relative_to(ROOT)), "--admission-sha256", expected]
    elif data.get("decision") == "D231_INERT_QUALIFICATION":
        family = ROOT / "runs/D231_OPERATIONAL_QUALIFICATION_001"
        if (not path.is_relative_to(family) or not re.fullmatch(r"admission\.json", path.name)
                or data.get("test_case") not in ("normal", "inner", "outer")):
            raise ValueError("inert receipt path or case")
        budget, duration = {"normal": (6, .35), "inner": (1.6, 10), "outer": (10, 12)}[data["test_case"]]
        if data.get("inner_wall_seconds") != budget:
            raise ValueError("inert case bounds")
        address = path.parent / "inert"
        args = ["-I", "-S", "-B", "-c",
                "import sys,time; print('D231 inert stdout',flush=True); "
                "print('D231 inert stderr',file=sys.stderr,flush=True); time.sleep(float(sys.argv[1]))",
                str(duration)]
    else:
        raise ValueError("receipt decision")
    return data, address, args


def supervise(receipt, receipt_hash):
    started, cpu_started = monotonic(), process_time()
    data, prefix, child_args = validate_receipt(receipt, receipt_hash)
    runtime = data["runtime"]
    exe = (ROOT / ".venv/Scripts/python.exe").resolve()
    base = Path(runtime["base_executable"]).resolve()
    if (digest(exe) != runtime["launcher_sha256"] or Path(sys.executable).resolve() != base
            or digest(base) != runtime["base_sha256"] or digest(Path(__file__)) != data["observer_sha256"]):
        raise ValueError("observer or interpreter bytes")
    native_path = ROOT / CONFIG["referents"]["native"]
    if digest(native_path) != data["native_sha256"]:
        raise ValueError("retained native bytes")
    spec = importlib.util.spec_from_file_location("retained_d231_v9", native_path)
    n = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(n)
    n.verify_layout()
    args = [str(exe), *child_args]
    paths = {suffix: prefix.with_name(prefix.name + "-" + suffix)
             for suffix in ("stdout.txt", "stderr.txt", "suspended.json", "released.json", "worker.json", "foreground.json")}
    if any(path.exists() for path in paths.values()):
        raise FileExistsError("observation destination occupied")

    report = {"run_id": data["run_id"], "admission_sha256": receipt_hash, "arguments": args,
              "native_sha256": data["native_sha256"], "start_utc": utc(), "scientific": data["decision"] == "AUTHORIZE_D231_EXECUTION",
              "resume_attempted": False, "stop_reason": None, "worker": None}
    proc = worker = None
    drained = False
    hard = started + data["inner_wall_seconds"]
    native_seconds = 899 if report["scientific"] else 4
    with ExitStack() as stack:
        job = stack.enter_context(n.Owned(n.CreateJob(None, None))).handle
        limits = n.ExtendedLimit()
        limits.basic.flags, limits.basic.active_limit = n.FLAGS, 2
        limits.basic.job_user = native_seconds * n.TICKS
        n.check(n.SetJob(job, n.EXTENDED_LIMIT, n.OUT(limits), n.ct.sizeof(limits)))
        action = n.DWORD(0)
        n.check(n.SetJob(job, n.END_OF_JOB, n.OUT(action), n.ct.sizeof(action)))
        settings = n.limits(job)
        report["job_limits"] = settings
        if (settings["flags"] != n.FLAGS or settings["active_limit"] != 2
                or settings["native_user_ticks"] != native_seconds * n.TICKS
                or settings["end_action"] != 0 or settings["job_handle_inheritable"]
                or n.accounting(job)["lifetime"]):
            raise RuntimeError("Job configuration mismatch")
        try:
            streams = [stack.enter_context(open(os.devnull, "rb")),
                       stack.enter_context(paths["stdout.txt"].open("xb")),
                       stack.enter_context(paths["stderr.txt"].open("xb"))]
            handles = [msvcrt.get_osfhandle(stream.fileno()) for stream in streams]
            for handle in handles:
                os.set_handle_inheritable(handle, True)
            info = n.ProcessInfo()
            command = n.ct.create_unicode_buffer(subprocess.list2cmdline(args))
            with n.attributes(job, handles) as attrs:
                startup = n.StartupEx()
                startup.startup.length, startup.startup.flags = n.ct.sizeof(startup), 0x100
                startup.startup.stdin, startup.startup.stdout, startup.startup.stderr = handles
                startup.attributes = attrs
                n.check(n.CreateProcess(str(exe), command, None, None, True, n.WORKER_CREATION_FLAGS,
                                        None, str(ROOT), n.OUT(startup), n.OUT(info)))
            proc = stack.enter_context(n.Owned(info.process)).handle
            thread = stack.enter_context(n.Owned(info.thread)).handle
            suspended = n.accounting(job)
            image = n.image(proc)
            if (Path(image).resolve() != exe or not n.in_job(proc, job)
                    or suspended["active"] != 1 or suspended["lifetime"] != 1
                    or monotonic() >= hard):
                raise RuntimeError("suspended launcher identity or lifetime")
            # The complete suspension record is durable before any release.
            admitted, _, _ = validate_receipt(receipt, receipt_hash)
            if admitted != data:
                raise ValueError("receipt changed before release")
            report["suspended"] = {"pid": info.pid, "image": image, "in_job": True,
                                   "times": n.sample(proc), "job": suspended}
            write_new(paths["suspended.json"], report["suspended"])
            report["resume_attempted"] = True
            # Do not replay if interrupted after this durable indication.
            write_new(paths["released.json"], {"resume_attempt_committed": True, "pid": info.pid, "utc": utc()})
            report["resume_previous_count"] = n.ResumeThread(thread)
            if report["resume_previous_count"] != 1:
                raise RuntimeError("resume count")
            while True:
                signaled = n.wait(proc, 10)
                stats = n.accounting(job)
                if stats["lifetime"] > 2:
                    raise RuntimeError("unexpected process count")
                if worker is None and stats["active"] == 2:
                    members = n.job_pids(job)["pids"]
                    for pid in members:
                        if pid == info.pid:
                            continue
                        handle = n.OpenProcess(0x00101400, False, pid)
                        if not handle:
                            continue  # transient exit, final lifetime still checked
                        worker = stack.enter_context(n.Owned(handle)).handle
                        if not n.in_job(worker, job) or Path(n.image(worker)).resolve() != base:
                            raise RuntimeError("worker outside admitted image or Job")
                        report["worker"] = {"pid": pid, "image": n.image(worker), "times": n.sample(worker)}
                        write_new(paths["worker.json"], report["worker"])
                if monotonic() >= hard:
                    report["stop_reason"] = "INNER_WALL"
                elif (stats["user"] + stats["kernel"]) / n.TICKS + process_time() - cpu_started >= native_seconds:
                    report["stop_reason"] = "SAMPLED_CPU"
                elif signaled and stats["active"] == 0:
                    drained = True
                    break
                if report["stop_reason"]:
                    break
        except (Exception, KeyboardInterrupt) as error:
            report["stop_reason"] = type(error).__name__ + ": " + str(error)
        finally:
            if not drained:
                report["termination_errors"] = n.stop_worker(job, proc)
                end = min(hard + .65, monotonic() + .65)
                while n.accounting(job)["active"] and monotonic() < end:
                    sleep(.01)
            report["job_final"] = n.accounting(job)
            report["launcher_signaled"] = bool(proc and n.wait(proc, 0))
            if report["launcher_signaled"]:
                report["launcher_exit_code"] = n.exit_code(proc)
                report["launcher_times"] = n.sample(proc)
            if worker:
                report["worker_signaled"] = n.wait(worker, 0)
                if report["worker_signaled"]:
                    report["worker_times"] = n.sample(worker)
    report["foreground_seconds"] = monotonic() - started
    report["observer_python_cpu_seconds"] = process_time() - cpu_started
    report["end_utc"] = utc()
    write_new(paths["foreground.json"], report)
    return int(not (drained and not report["stop_reason"] and report.get("launcher_exit_code") == 0
                    and report["job_final"]["lifetime"] == 2))


if __name__ == "__main__":
    if len(sys.argv) != 3 or Path.cwd().resolve() != ROOT:
        raise SystemExit("expected LCL root, receipt path and digest")
    sys.exit(supervise(Path(sys.argv[1]).resolve(), sys.argv[2]))
