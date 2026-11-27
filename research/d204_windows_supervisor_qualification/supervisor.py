"""Bracketed native Windows qualification of one fixed, synthetic-only task."""
import hashlib
import importlib.util
import json
import os
from contextlib import ExitStack
from pathlib import Path
import stat
import struct
import subprocess
import sys
import threading
import time

TASK = "LCL-D204-WINDOWS-SUPERVISOR-QUALIFICATION-001"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_D204_WINDOWS_SUPERVISOR_QUALIFICATION_001"
RUN = ROOT / "runs/d204-windows-supervisor-qualification-001"
RECOVERY = ROOT / "evidence/validation/LCL_D204_EXECUTION_ENVIRONMENT_RECOVERY_PREP_001"
APPROVED_PROPOSAL = "5c1a382abe594d093443e7e2b4b390cab9785f57b73158c1b34a2e978eb09293"

class Rejected(RuntimeError):
    pass

def require(condition, description):
    if not condition:
        raise Rejected(description)

def digest(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("ascii")

def regular(path):
    for item in (path, *path.parents):
        attributes = item.lstat().st_file_attributes
        require(not attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT, "reparse path: " + str(item.name))
    require(path.is_file(), "missing regular file: " + str(path.name))

def check_file(path, expected, canonical=False):
    regular(path)
    require(path.stat().st_size <= expected["bytes"] * (2 if canonical else 1),
            "oversized binding: " + path.name)
    data = path.read_bytes()
    if canonical:
        data = data.replace(b"\r\n", b"\n")
    require(digest(data) == expected, "binding mismatch: " + path.name)
    return data

def frozen_gate(freeze_sha):
    require(sys.platform == "win32" and sys.version_info[:3] == (3, 13, 17)
            and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
            "run with the frozen isolated CPython flags")
    freeze = EVIDENCE / "FREEZE.json"
    regular(freeze)
    require(freeze.stat().st_size <= 2000000, "oversized freeze")
    data = freeze.read_bytes()
    require(digest(data)["sha256"] == freeze_sha, "freeze hash does not match reviewed gate")
    bundle = json.loads(data)
    require(bundle["task"] == TASK and bundle["scientific_dispatch"] is False,
            "incorrect qualification identity")
    for relative, binding in bundle["project"].items():
        check_file(ROOT / relative, binding["identity"], binding["canonical"])
    matrix = json.loads((HERE / "MATRIX.json").read_bytes())
    review = EVIDENCE / "PRELAUNCH_REVIEW.json"
    regular(review)
    require(review.stat().st_size <= 16384, "oversized review")
    expected = json.loads(review.read_bytes())
    require(expected["task"] == TASK and expected["freeze_sha256"] == freeze_sha
            and expected["disposition"] == "PASS_FOR_SYNTHETIC_QUALIFICATION",
            "missing matching independent native-launch review")
    proposal = (RECOVERY / "PROPOSAL.json").read_bytes().replace(b"\r\n", b"\n")
    require(digest(proposal)["sha256"] == APPROVED_PROPOSAL, "recovery proposal mismatch")
    require(matrix["task"] == TASK and matrix["scientific_dispatch"] is False
            and matrix["future"]["phase_and_shared_limits"] == json.loads(proposal)["accepted_scientific_limits"],
            "matrix identity or preserved ceilings mismatch")
    policy = json.loads(proposal)["proposed_windows_policy"]
    freeze_policy = matrix["future"]
    require((freeze_policy["tick_ms"], freeze_policy["gap_ms"], freeze_policy["cpu_reserve_seconds"],
             freeze_policy["wall_reserve_seconds"], freeze_policy["cleanup_ms"],
             freeze_policy["terminal_reserve"]) ==
            (policy["sample_target_milliseconds"], policy["max_admissible_observation_gap_milliseconds"],
             policy["cpu_reserve_seconds"], policy["elapsed_reserve_seconds"],
             policy["cleanup_observation_grace_seconds"] * 1000,
             policy["terminal_evidence_reservation_bytes"]), "future policy controls mismatch")
    exe = Path(sys._base_executable)
    require(exe == Path(sys.base_prefix) / "python.exe", "unexpected base interpreter path")
    path = HERE / "win32.py"
    binding = bundle["project"][path.relative_to(ROOT).as_posix()]["identity"]
    native_source = check_file(path, binding)
    spec = importlib.util.spec_from_file_location("qualified_win32", path)
    native = importlib.util.module_from_spec(spec)
    exec(compile(native_source, str(path), "exec", dont_inherit=True), vars(native))
    return native, bundle, matrix, exe

def pin_project(stack, native, bundle):
    for relative, binding in bundle["project"].items():
        path = ROOT / relative
        regular(path)
        stack.enter_context(native.pin(path))
        check_file(path, binding["identity"], binding["canonical"])

def runtime_files(home):
    result = {"python.exe", "python313.dll", "python3.dll", "vcruntime140.dll", "vcruntime140_1.dll"}
    if (home / "python313.zip").is_file():
        result.add("python313.zip")
    require(not any(home.glob("*._pth")), "CPython path override present")
    for name in ("Lib", "DLLs"):
        for path in (home / name).rglob("*"):
            relative = path.relative_to(home)
            if "site-packages" not in relative.parts and path.is_file():
                result.add(relative.as_posix())
    known_excluded = {"pythonw.exe", "NEWS.txt", "LICENSE.txt", "LICENSE"}
    unexpected = [path.name for path in home.iterdir() if path.is_file()
                  and path.name not in result and path.name not in known_excluded]
    require(not unexpected, "unexpected installation-root file: " + ", ".join(unexpected[:6]))
    return result


def pin_runtime(stack, native, bundle, exe):
    approved = bundle["dependencies"]
    require(set(approved) == runtime_files(exe.parent), "runtime file inventory changed")
    for name, binding in approved.items():
        path = exe.parent / name
        regular(path)
        stack.enter_context(native.pin(path))
        check_file(path, binding)

class Ledger:
    """One writer per probe, charged before each exclusive write."""
    def __init__(self, folder, cap, reserve):
        self.folder = folder
        self.cap = cap
        self.reserve = reserve
        self.charged = 0

    def save(self, name, data, terminal=False):
        require(name in {"start.json", "runtime.json", "raw-candidate.bin", "terminal.json", "observer.json"},
                "unknown receipt file")
        available = self.cap - self.charged - (0 if terminal else self.reserve)
        if len(data) > available or (terminal and len(data) > self.reserve):
            raise Rejected("EVIDENCE_LIMIT")
        self.charged += len(data)
        with (self.folder / name).open("xb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())

class Watchdog:
    """Owns sampling and termination without touching evidence storage."""
    def __init__(self, native, process, job, start, identity, matrix, probe):
        self.native, self.process, self.job = native, process, job
        self.start, self.last, self.identity = start, start, identity
        self.first = None
        self.maximum_gap, self.samples = 0, 0
        self.latest = identity
        self.previous = identity
        self.stop_reason, self.failure = None, None
        self.stop_requested_at = None
        self.fault_delay_ms = probe.get("fault_delay_ms", 0)
        self.gap = matrix["gap_ms"]
        self.target = matrix["tick_ms"]
        self.cpu_early = probe.get("cpu_early_ticks", matrix["cpu_early_ticks"])
        self.wall_early = probe.get("wall_early_ms", matrix["wall_early_ms"])
        self.event = threading.Event()
        self.mutex = threading.Lock()
        self.thread = threading.Thread(target=self.observe, name="native-watchdog", daemon=True)

    def stop(self, cause):
        with self.mutex:
            if self.stop_reason is not None:
                return
            self.stop_reason = cause
            self.stop_requested_at = self.native.Tick()
            try:
                self.native.check(self.native.TerminateJob(
                    self.job, self.native.TERMINATED_BY_SUPERVISOR))
            except Exception as error:
                self.failure = str(error)[:512]

    def observe(self):
        try:
            while not self.event.is_set():
                current = self.native.sample(self.process)
                now = self.native.Tick()
                prior_tick = self.last
                self.samples += 1
                self.maximum_gap = max(self.maximum_gap, now - self.last)
                old = self.latest
                self.previous = old
                self.last, self.latest = now, current
                if self.first is None:
                    self.first = {"tick": now, **current}
                if (now < prior_tick or current["born"] != self.identity["born"]
                        or any(current[k] < old[k] for k in ("user", "kernel"))):
                    self.stop("ACCOUNTING_FAILURE")
                elif self.maximum_gap > self.gap:
                    self.stop("OBSERVATION_GAP")
                elif current["user"] + current["kernel"] >= self.cpu_early:
                    self.stop("SAMPLED_COMBINED_CPU")
                elif now - self.start >= self.wall_early:
                    self.stop("SAMPLED_ELAPSED")
                if self.native.wait(self.process, 0):
                    return
                pause = self.fault_delay_ms if self.samples == 1 and self.fault_delay_ms else self.target
                self.event.wait(pause / 1000)
        except Exception as error:
            self.failure = str(error)[:512]
            self.stop("WATCHDOG_FAILURE")

    def receipt(self):
        return dict(samples=self.samples, first=self.first, previous=self.previous, last=self.latest,
                    start=self.start, last_tick=self.last, maximum_gap_ms=self.maximum_gap,
                    stop_reason=self.stop_reason, stop_requested_at=self.stop_requested_at, failure=self.failure)

def read_exact(native, handle, count, allow_eof=False):
    data = bytearray()
    while len(data) < count:
        item = native.read(handle, count - len(data))
        if not item:
            if not data and allow_eof:
                return None
            raise Rejected("IPC_INCOMPLETE")
        data.extend(item)
    return bytes(data)

def read_frame(native, handle, limit):
    header = read_exact(native, handle, 4, allow_eof=True)
    if header is None:
        return None
    size = struct.unpack(">I", header)[0]
    if not 1 <= size <= limit:
        raise Rejected("IPC_FRAME_LIMIT")
    message = read_exact(native, handle, size)
    return message[:1], message[1:]

def runtime_report(raw, exe, pid, bundle):
    report = json.loads(raw)
    require(report["pid"] == pid and Path(report["executable"]) == exe
            and Path(report["dll"]) == exe.with_name("python313.dll"),
            "runtime executable, DLL or process mismatch")
    paths = [exe.parent / part for part in ("python313.zip", "DLLs", "Lib", "")]
    require([Path(value) for value in report["sys_path"]] == paths
            and report["isolated"] and report["no_site"] and report["bytecode_disabled"],
            "dependency resolution or runtime flag mismatch")
    for location in report["modules"].values():
        path = Path(location)
        require(path.is_relative_to(exe.parent), "module loaded outside approved runtime")
        relative = path.relative_to(exe.parent).as_posix()
        require(relative in bundle["dependencies"], "unbound imported module: " + relative)
    return report

def ipc(native, sender, receiver, ledger, watcher, exe, pid, bundle, matrix, records):
    hello = read_frame(native, sender, matrix["frame_limit"])
    require(hello is not None and hello[0] == b"H", "missing runtime frame")
    records["runtime"] = runtime_report(hello[1], exe, pid, bundle)
    ledger.save("runtime.json", encoded(records["runtime"]))
    require(not watcher.stop_reason, watcher.stop_reason)
    native.write(receiver, b"G")
    result = read_frame(native, sender, matrix["frame_limit"])
    if result is None:
        return
    tag, payload = result
    if tag == b"C":
        records["pending_candidate"] = digest(payload)
        ledger.save("raw-candidate.bin", payload)
        records["candidate"] = digest(payload)
        require(not watcher.stop_reason, watcher.stop_reason)
        native.write(receiver, b"A")
        records["ack_after_fsync"] = True
        result = read_frame(native, sender, matrix["frame_limit"])
        require(result is not None and result[0] == b"V", "missing same-worker verification frame")
        records["verification"] = json.loads(result[1])
        require(records["verification"] == {"pid": pid, "value": 2470}, "synthetic verification mismatch")
    else:
        require(tag == b"R", "unexpected frame")
        records["result"] = json.loads(payload)
    require(read_frame(native, sender, matrix["frame_limit"]) is None, "unexpected extra frame")

def classify(probe, stats, exit_status, job_signaled, message_error, records):
    if stats["failure"]:
        return "CONTROL_FAILURE"
    if stats["stop_reason"]:
        return stats["stop_reason"]
    if message_error:
        return message_error
    if job_signaled and exit_status == 1816:
        return "NATIVE_USER_LIMIT"
    if exit_status != 0:
        return "WORKER_FAILURE"
    if probe["id"] == "child_refusal":
        result = records.get("result", {})
        if result.get("child_created") is False and result.get("winerror") in (5, 1816):
            return "CHILD_REFUSED"
        return "CONTAINMENT_FAILURE"
    if records.get("ack_after_fsync") and records.get("verification"):
        return "DURABLE_CANDIDATE_AND_VERIFIED"
    if records.get("result") == {"value": 42}:
        return "NATURAL"
    return "UNEXPECTED_WORKER_RESULT"


def wait_for_exit(native, process, start, wall_ms):
    while not native.wait(process, 30):
        require(native.Tick() - start < wall_ms, "worker exit not verified by wall stop")

def owner(native, bundle, matrix, exe, probe):
    folder = RUN / probe["id"]
    folder.mkdir(exist_ok=False)
    ledger = Ledger(folder, probe.get("probe_evidence", matrix["normal_probe_evidence"]),
                    matrix["terminal_reserve"])
    native_ticks = probe.get("native_ticks", matrix["native_ticks"])
    records = {}
    conclusion = {}
    owner_start = native.sample(native.CurrentProcess())
    try:
        with ExitStack() as stack:
            pin_project(stack, native, bundle)
            layouts = native.verify_layout()
            job = stack.enter_context(native.Owned(native.CreateJob(None, None)))
            native.configure(job.handle, native_ticks)
            limits = native.limits(job.handle)
            require(limits == dict(native_user_ticks=native_ticks, flags=native.FLAGS,
                                   active_limit=1, end_action=0, job_handle_inheritable=False),
                    "configured Job limits mismatch")
            empty = native.accounting(job.handle)
            require(empty["lifetime"] == empty["active"] == empty["user"] == empty["kernel"] == 0,
                    "Job was not empty at creation")
            outer_job = native.in_job(native.CurrentProcess())
            outer_limits = None
            if outer_job:
                enclosing = native.job_info(None, native.EXTENDED_LIMIT, native.ExtendedLimit).basic
                outer_limits = dict(flags=enclosing.flags, active_limit=enclosing.active_limit,
                                    job_user=enclosing.job_user, process_user=enclosing.process_user)
            start = native.Tick()
            process, thread, pid, sender, receiver = native.launch_suspended(
                stack, job.handle, exe, HERE / "probe_worker.py", probe["id"])
            watcher = None
            try:
                member = native.in_job(process.handle, job.handle)
                require(member, "at-creation Job membership missing")
                born = native.sample(process.handle)
                actual_image = native.image(process.handle)
                require(Path(actual_image) == exe and not native.wait(process.handle, 0),
                        "suspended worker image or state mismatch")
                baseline = native.accounting(job.handle)
                require(baseline["active"] == baseline["lifetime"] == 1,
                        "unexpected suspended Job membership count")
                require(native.limits(job.handle) == limits, "suspended effective Job limits mismatch")
                start_record = dict(task=TASK, probe=probe["id"], pid=pid, image=actual_image,
                                    creation=born["born"], before_resumption=True,
                                    supervisor_in_job=outer_job, enclosing_limits=outer_limits,
                                    suspended_assigned=True,
                                    limits=limits, job_before_creation=empty,
                                    job_after_creation=baseline, worker_before_resumption=born,
                                    phase_start_tick=start, layouts=layouts)
                watcher = Watchdog(native, process.handle, job.handle, start, born, matrix, probe)
                watcher.thread.start()
                ledger.save("start.json", encoded(start_record))
                require(not watcher.stop_reason, watcher.stop_reason)
                require(native.ResumeThread(thread.handle) == 1, "unexpected initial suspension count")
                message_error = None
                try:
                    ipc(native, sender.handle, receiver.handle, ledger, watcher, exe, pid,
                        bundle, matrix, records)
                except (Rejected, OSError, ValueError, KeyError, TypeError) as error:
                    message_error = str(error)[:512]
                    watcher.stop(message_error)
                wait_for_exit(native, process.handle, start, matrix["wall_max_ms"] - 2500)
                watcher.thread.join(matrix["cleanup_ms"] / 1000)
                require(not watcher.thread.is_alive(), "watchdog did not finish")
                readings = watcher.receipt()
                terminal_process = native.sample(process.handle)
                exit_status = native.exit_code(process.handle)
                signaled_job = native.wait(job.handle, 0)
                proc_exit_observed = native.Tick()
                # Release all worker references before asserting the final Job member count.
                thread.close()
                process.close()
                final_job = native.accounting(job.handle)
                while final_job["active"] and native.Tick() - proc_exit_observed < matrix["cleanup_ms"]:
                    time.sleep(0.025)
                    final_job = native.accounting(job.handle)
                end = native.Tick()
                status = classify(probe, readings, exit_status, signaled_job, message_error, records)
                seen_cpu = max(terminal_process["user"] + terminal_process["kernel"],
                               final_job["user"] + final_job["kernel"])
                lifetime_ok = final_job["lifetime"] == 1 or (
                    status == "CHILD_REFUSED" and final_job["lifetime"] == 2)
                matches = terminal_process["born"] == born["born"] and terminal_process["end"] > 0
                advances = all(terminal_process[key] >= readings["last"][key]
                               and final_job[key] >= baseline[key] >= 0 for key in ("user", "kernel"))
                reconciles = all(terminal_process[key] == final_job[key] for key in ("user", "kernel"))
                if status == "CHILD_REFUSED" and final_job["lifetime"] == 2:
                    reconciles = all(final_job[key] >= terminal_process[key] for key in ("user", "kernel"))
                cleanup = final_job["active"] == 0 and end - proc_exit_observed <= matrix["cleanup_ms"]
                measurements = (matches and advances and reconciles and cleanup and lifetime_ok
                                and readings["samples"] >= 1 and 0 <= end - start <= matrix["wall_max_ms"]
                                and seen_cpu <= matrix["cpu_max_ticks"])
                if status == "NATIVE_USER_LIMIT":
                    measurements = measurements and terminal_process["user"] >= native_ticks
                if status == "EVIDENCE_LIMIT":
                    measurements = measurements and (
                        "pending_candidate" in records and "candidate" not in records
                        and not (folder / "raw-candidate.bin").exists())
                if status not in ("OBSERVATION_GAP", "CONTROL_FAILURE"):
                    measurements = measurements and readings["maximum_gap_ms"] <= matrix["gap_ms"]
                conclusion.update(status=status if measurements else "TERMINAL_RECONCILIATION_FAILURE",
                                  observed_status=status, launch=start_record, worker_terminal=terminal_process,
                                  job_terminal=final_job, job_signaled=signaled_job, worker_exit=exit_status,
                                  cleanup_verified=cleanup, watchdog=readings, worker_cpu_ticks=seen_cpu,
                                  worker_elapsed_ms=end - start, measurement_predicates_pass=measurements,
                                  bounded_ipc=records)
            finally:
                if process.handle is not None:
                    if not native.wait(process.handle, 0):
                        if native.in_job(process.handle, job.handle):
                            native.check(native.TerminateJob(job.handle, native.TERMINATED_BY_SUPERVISOR))
                        else:
                            native.check(native.TerminateProcess(process.handle, native.TERMINATED_BY_SUPERVISOR))
                    require(native.wait(process.handle, matrix["cleanup_ms"]),
                            "unverified emergency process termination")
                if watcher is not None and watcher.thread.is_alive():
                    watcher.event.set()
                    watcher.thread.join(matrix["cleanup_ms"] / 1000)
                    require(not watcher.thread.is_alive(), "unverified watchdog shutdown")
    except (Rejected, OSError, ValueError, KeyError, RuntimeError, KeyboardInterrupt) as error:
        conclusion["status"] = "CONTROL_FAILURE"
        conclusion["failure"] = f"{type(error).__name__}: {error}"[:1024]
    conclusion.update(task=TASK, probe=probe["id"], expected=probe["expected"],
                      owner_cpu_at_entry=owner_start,
                      owner_cpu_before_receipt=native.sample(native.CurrentProcess()),
                      owner_evidence_charged_before_receipt=ledger.charged)
    ledger.save("terminal.json", encoded(conclusion), terminal=True)
    return conclusion["status"] == probe["expected"]

def process_ticks(reading):
    return reading["user"] + reading["kernel"]

def worker_observer(native, start, exe):
    # Match the durable PID and creation FILETIME before using the retained handle.
    process = native.Owned(native.OpenProcess(0x00101001, False, start["pid"]))
    try:
        require(native.sample(process.handle)["born"] == start["creation"]
                and Path(native.image(process.handle)) == exe, "observer worker identity mismatch")
    except BaseException:
        process.close()
        raise
    return process

def read_record(path):
    require(path.stat().st_size <= 65536, "oversized receipt")
    return json.loads(path.read_bytes())

def interrupt_owner(native, helper, folder, exe, deadline):
    runtime = folder / "runtime.json"
    while not runtime.is_file() or runtime.stat().st_size == 0:
        require(helper.poll() is None, "owner ended before interruption observation")
        require(native.Tick() < deadline, "interruption start receipt deadline exceeded")
        time.sleep(0.025)
    start = read_record(folder / "start.json")
    with worker_observer(native, start, exe) as worker:
        require(not native.wait(worker.handle, 0), "interruption worker is not active")
        interrupt = native.Tick()
        # The helper alone owns the Job handle. This observer holds only worker and helper process handles.
        helper.kill()
        helper.wait(timeout=5)
        require(native.wait(worker.handle, 5000), "kill-on-close did not terminate the worker")
        stop = native.Tick()
        final = native.sample(worker.handle)
        require(final["end"] > 0 and final["born"] == start["creation"],
                "missing terminal accounting for interrupted worker")
        require(not (folder / "terminal.json").exists(), "owner unexpectedly wrote a normal terminal record")
        return dict(status="OWNER_INTERRUPTED_KILL_ON_CLOSE", cleanup_verified=True,
                    worker_terminal=final, worker_exit=native.exit_code(worker.handle),
                    worker_cpu_ticks=process_ticks(final), worker_elapsed_ms=stop - start["phase_start_tick"],
                    interruption_tick=interrupt, verified_worker_exit_tick=stop,
                    post_interruption_job_totals_unavailable=True)

def emergency_cleanup(native, helper, folder, exe):
    # No second engine or retry. This is cleanup for the stopped probe only.
    path = folder / "start.json"
    worker = None
    result = {}
    try:
        if path.is_file():
            start = read_record(path)
            worker = worker_observer(native, start, exe)
            result["identity"] = start["pid"]
    except Exception as error:
        result["worker_handle_observation"] = str(error)[:512]
    try:
        if helper.poll() is None:
            helper.kill()
        helper.wait(timeout=5)
        result["owner_exit_verified"] = True
        if worker is not None:
            if not native.wait(worker.handle, 4000):
                native.check(native.TerminateProcess(worker.handle, native.TERMINATED_BY_SUPERVISOR))
            result["worker_exit_verified"] = native.wait(worker.handle, 1000)
            if result["worker_exit_verified"]:
                result["worker_terminal"] = native.sample(worker.handle)
    except Exception as error:
        result["cleanup_error"] = str(error)[:512]
    finally:
        if worker is not None:
            worker.close()
    return result

def observe_probe(native, exe, freeze_sha, probe, matrix):
    folder = RUN / probe["id"]
    started = native.Tick()
    cpu_start = native.sample(native.CurrentProcess())
    helper_command = [str(exe), "-I", "-S", "-B", str(HERE / "supervisor.py"),
                      TASK, freeze_sha, "owner", probe["id"]]
    with subprocess.Popen(helper_command, executable=str(exe), cwd=ROOT,
                          stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL, close_fds=True,
                          creationflags=0x08000000) as helper:
        # Popen retains its own process handle on the fixed CPython runtime.
        # The companion accounting handle stays open even if the helper exits immediately.
        try:
            with native.Owned(native.OpenProcess(0x00101000, False, helper.pid)) as retained:
                require(Path(native.image(retained.handle)) == exe, "unexpected companion image")
                if probe["id"] == "interruption":
                    outcome = interrupt_owner(native, helper, folder, exe, started + 15000)
                else:
                    while helper.poll() is None:
                        require(native.Tick() - started <= 24000, "companion deadline exceeded")
                        time.sleep(0.025)
                    outcome = read_record(folder / "terminal.json")
                helper_reading = native.sample(retained.handle)
                observed = native.Tick() - started
                observer_reading = native.sample(native.CurrentProcess())
                observer_cpu = process_ticks(observer_reading) - process_ticks(cpu_start)
                measured = (process_ticks(helper_reading) + observer_cpu
                            + outcome.get("worker_cpu_ticks", 0))
                allowed = (outcome["status"] == probe["expected"]
                           and (helper.returncode == 0 if probe["id"] != "interruption"
                                else helper.returncode is not None and helper.returncode != 0)
                           and bool(outcome.get("cleanup_verified"))
                           and helper_reading["end"] > 0 and observer_cpu >= 0
                           and measured <= matrix["cpu_max_ticks"]
                           and observed <= matrix["wall_max_ms"])
                record = dict(passed=allowed, expected=probe["expected"],
                              actual=outcome["status"], helper_pid=helper.pid,
                              helper_terminal=helper_reading, helper_exit=helper.returncode,
                              observer_cpu_ticks=observer_cpu, observed_probe_cpu_ticks=measured,
                              observed_probe_elapsed_ms=observed)
                if probe["id"] == "interruption":
                    record["interruption"] = outcome
        except (Exception, KeyboardInterrupt) as error:
            cleanup = emergency_cleanup(native, helper, folder, exe)
            record = dict(passed=False, expected=probe["expected"], actual="OBSERVER_FAILURE",
                          error=f"{type(error).__name__}: {error}"[:1024],
                          observed_probe_elapsed_ms=native.Tick() - started, cleanup=cleanup,
                          unavailable_measurements_are_not_zero=True)
    if not folder.exists():
        folder.mkdir(exist_ok=False)
    observer_ledger = Ledger(folder, 65536, 65536)
    observer_ledger.save("observer.json", encoded(record), terminal=True)
    return record

def scientific_transition(phase, engine, accounting_proved, raw_durable, independent_verification,
                          traversal_proved, admitted_primary=None):
    """Inactive phase contract. Neither this function nor the CLI can dispatch science."""
    if phase not in ("primary", "audit"):
        raise Rejected("unknown phase")
    if phase == "audit" and admitted_primary != "ALLOW_INDEPENDENT_AUDIT_ONLY":
        return "STOP_AUDIT_WITHOUT_VALID_PRIMARY_EXHAUSTION"
    if phase == "primary" and admitted_primary is not None:
        return "STOP_PRIMARY_REENTRY"
    if engine == "CANDIDATE":
        if not raw_durable:
            return "STOP_CANDIDATE_CUSTODY_FAILURE"
        if not independent_verification:
            return "STOP_VERIFICATION_FAILURE"
        if not accounting_proved:
            return "STOP_RESOURCE_OR_CUSTODY_FAILURE"
        return "STOP_VERIFIED_POSITIVE" if phase == "primary" else "STOP_ENGINE_DISCREPANCY"
    if engine == "EXHAUSTED" and accounting_proved is True and traversal_proved is True:
        return "ALLOW_INDEPENDENT_AUDIT_ONLY" if phase == "primary" else "STOP_REGISTERED_NEGATIVE"
    return "STOP_INCOMPLETE_OR_FAILED"

def qualification(native, bundle, matrix, exe, freeze_sha):
    clock = native.Tick()
    runner_start = native.sample(native.CurrentProcess())
    limit = matrix["normal_probe_evidence"] + 65536
    require(len(matrix["probes"]) <= 12 and len(matrix["probes"]) * limit < 5000000,
            "matrix exceeds reserved qualification evidence")
    with ExitStack() as stack:
        pin_project(stack, native, bundle)
        pin_runtime(stack, native, bundle, exe)
        RUN.mkdir(exist_ok=False)
        receipts = []
        for probe in matrix["probes"]:
            result = observe_probe(native, exe, freeze_sha, probe, matrix)
            receipts.append(dict(probe=probe["id"], **result))
            # Use complete worker and companion readings plus the periodic full runner reading.
            external_ticks = sum(process_ticks(item["helper_terminal"]) for item in receipts
                                 if "helper_terminal" in item)
            external_ticks += sum(item["observed_probe_cpu_ticks"] - process_ticks(item["helper_terminal"])
                                  - item["observer_cpu_ticks"] for item in receipts
                                  if "observed_probe_cpu_ticks" in item)
            runner_cpu = process_ticks(native.sample(native.CurrentProcess())) - process_ticks(runner_start)
            if not result["passed"] or native.Tick() - clock > 300000 or external_ticks + runner_cpu > 1200000000:
                break
        # Recheck the held scientific source and runtime paths before publication.
        with ExitStack() as terminal_pins:
            pin_project(terminal_pins, native, bundle)
            pin_runtime(terminal_pins, native, bundle, exe)
        complete = len(receipts) == len(matrix["probes"]) and all(item["passed"] for item in receipts)
        summary = dict(task=TASK, complete=complete, freeze=freeze_sha, probes=receipts,
                       elapsed_ms=native.Tick() - clock,
                       runner_cpu_ticks=process_ticks(native.sample(native.CurrentProcess())) - process_ticks(runner_start),
                       known_companion_and_worker_cpu_ticks=external_ticks,
                       scientific_worker_launches=0, scientific_consumer_imports=0,
                       original_checker_invocations=0, task_bytecode_files=0,
                       absent_helper_or_worker_measurements_are_not_zero=True)
        Ledger(RUN, 65536, 65536).save("terminal.json", encoded(summary), terminal=True)
    return complete

def main():
    if len(sys.argv) not in (4, 5) or sys.argv[1] != TASK:
        raise SystemExit("qualification identity required")
    freeze_sha, mode = sys.argv[2:4]
    if mode not in ("qualify", "owner") or len(sys.argv) != (4 if mode == "qualify" else 5):
        raise SystemExit("only fixed synthetic qualification is authorized")
    native, bundle, matrix, exe = frozen_gate(freeze_sha)
    if mode == "qualify":
        complete = qualification(native, bundle, matrix, exe, freeze_sha)
    else:
        probes = {probe["id"]: probe for probe in matrix["probes"]}
        require(sys.argv[4] in probes and RUN.is_dir(), "unknown synthetic workload or unopened qualification")
        complete = owner(native, bundle, matrix, exe, probes[sys.argv[4]])
    raise SystemExit(0 if complete else 1)

if __name__ == "__main__":
    main()
