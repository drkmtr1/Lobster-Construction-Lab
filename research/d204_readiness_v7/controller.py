"""One live controller, one worker and one absolute deadline per D204 phase."""
from contextlib import ExitStack
import os
from pathlib import Path
import queue
import secrets
import threading
import time
import ready_native as n
import ready_protocol as p

HERE = Path(__file__).parent
SYNTH = dict(cpu_max=100_000_000, user_max=60_000_000, cpu_early=30_000_000,
             wall=30000, early=9500, cleanup=5000, tick=250, gap=2000)
OBSERVED_CPU_INCREMENT = 156250  # 100 ns units. All V5 terminal counters lay on this grid.
ERROR_NOT_ENOUGH_QUOTA = 1816
STATUS_QUOTA_EXCEEDED = 0xC0000044
JOB_OBJECT_MSG_END_OF_JOB_TIME = 1
JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT = 3
ROOT = HERE.parents[1]
TASK = "LCL-D204-CONSOLE-DETACHED-EXECUTION-READINESS-002"
TARGETS = ["5554c99f3db5b777a5e139369479c470b9e220753da2193aecbaa3c9ac6d3515",
           "1e9d8d99227973991cb6fb850cfbcd44cfac2c3470396886c59a9264bd3de3cb"]

class UnsafeCleanup(RuntimeError):
    def __init__(self, reason, deadline=None):
        super().__init__(reason)
        self.deadline = deadline

def bounded_io(operation, deadline):
    """Keep disk calls off the timing/control thread, including after worker exit."""
    output, failures, lease = [], [], {}
    def work():
        try:
            lease["thread"] = n.thread_lease()
            output.append(operation())
        except Exception as error:
            failures.append(error)
    thread = threading.Thread(target=work, daemon=True)
    thread.start()
    try:
        while thread.is_alive():
            delay = p.remaining(n.Tick(), deadline, 50)
            if not delay:
                break
            thread.join(delay / 1000)
        if thread.is_alive() or n.Tick() > deadline:
            if thread.is_alive() and "thread" in lease:
                try:
                    n.cancel_thread(lease["thread"].handle)
                except OSError:
                    pass
            raise UnsafeCleanup("BOUNDED_EVIDENCE_DEADLINE", deadline)
        if failures:
            raise failures[0]
        p.need(len(output) == 1, "BOUNDED_EVIDENCE_RESULT")
        return output[0]
    finally:
        if not thread.is_alive() and "thread" in lease:
            lease["thread"].close()

def limits_for(limits):
    cpu, elapsed = limits["cpu_seconds"] * n.TICKS, limits["wall_seconds"] * 1000
    return dict(cpu_max=cpu, user_max=cpu, cpu_early=cpu-60*n.TICKS, wall=elapsed,
                early=elapsed-60000, cleanup=10000, tick=250, gap=2000)

def ticks(sample):
    p.need(type(sample) is dict and all(p.exact_int(sample.get(k), 0, (1 << 63)-1)
                                     for k in ("user", "kernel")), "MISSING_CPU_MEASUREMENT")
    return sample["user"] + sample["kernel"]

def live_read(process):
    value = n.sample(process)
    value.pop("end")  # GetProcessTimes does not define process exit time while active.
    return value

def terminal_read(process, before):
    p.need(n.wait(process, 0), "PROCESS_NOT_EXITED")
    value = n.sample(process)
    p.need(value["born"] == before["born"] and value["end"] >= value["born"] > 0
           and all(value[k] >= before[k] for k in ("user", "kernel")), "TERMINAL_CPU_IDENTITY")
    return value

def ordinary_job_reconciled(initial, job_started, finished, final):
    if any(item is None for item in (initial, job_started, finished, final)):
        return False
    return (final["active"] == 0 and final["lifetime"] == 1
            and all(final[k] >= job_started[k] and
                    (finished[k] == final[k] or
                     finished[k] - final[k] == initial[k] - job_started[k] >= 0)
                    for k in ("user", "kernel")))

def native_user_limit_observed(exit_code, signaled, final, user_limit, events):
    return (exit_code in (ERROR_NOT_ENOUGH_QUOTA, STATUS_QUOTA_EXCEEDED)
            and final is not None and final["active"] == 0 and final["lifetime"] == 1
            and final["terminated"] == 1 and final["user"] >= user_limit
            and (signaled or any(e["message"] == JOB_OBJECT_MSG_END_OF_JOB_TIME for e in events)))

def reconcile_terminal_cpu(initial, started, process, job, observations):
    if any(v is None for v in (initial, started, process, job, observations)):
        return {"mode": "unresolved", "guard_ticks": 0}
    keys = ("user", "kernel")
    delta = {key: process[key] - job[key] for key in keys}
    result = {"mode": "unresolved", "guard_ticks": 0, "process_minus_job": delta}
    terminal = {row["stage"]: row for row in observations["snapshots"]}
    before = terminal.get("before-process-handle-close", {}).get("accounting")
    after = terminal.get("after-job-active-zero", {})
    if (before is None or job["active"] != 0 or job["lifetime"] != 1
            or before["lifetime"] != 1 or after.get("accounting") != job
            or after.get("pids") != [] or observations["observed_unexpected_identities"]
            or any(before[k] != job[k] or job[k] < started[k] or process[k] < initial[k] for k in keys)):
        return result
    if ordinary_job_reconciled(initial, started, process, job):
        result["mode"] = "exact-or-suspended-offset"
        return result
    if (all(v[k] % OBSERVED_CPU_INCREMENT == 0 for v in (initial, started, process, job) for k in keys)
            and sum(abs(delta[k] - (initial[k]-started[k])) for k in keys) == OBSERVED_CPU_INCREMENT
            and all(initial[k] >= started[k] for k in keys)):
        result.update(mode="host-one-increment", guard_ticks=OBSERVED_CPU_INCREMENT)
    return result

def hello_check(raw, context, exe, bundle):
    row = p.decode(raw)
    p.need(type(row) is dict and row.get("context") == context, "WORKER_CONTEXT")
    p.need(Path(row["executable"]) == exe and Path(row["dll"]) == exe.with_name("python313.dll"),
           "BASE_IMAGE_OR_DLL")
    p.need(row["version"] == [3, 13, 17] and all(row[key] is True for key in (
        "isolated", "no_site", "no_bytecode")), "WORKER_ISOLATION")
    console = row["console"]
    p.need(console["process_count"] == 0 and console["window"] is False,
           "WORKER_CONSOLE_ATTACHED")
    expect = [exe.parent / rel for rel in ("python313.zip", "DLLs", "Lib", "")]
    p.need([Path(path) for path in row["search"]] == expect, "WORKER_SEARCH_PATH")
    p.need(type(row["modules"]) is dict and len(row["modules"]) <= 256, "WORKER_MODULES")
    for path in map(Path, row["modules"].values()):
        p.need(path.is_relative_to(exe.parent) and path.relative_to(exe.parent).as_posix()
               in bundle["dependencies"], "WORKER_MODULE_ORIGIN")
    return row

def arrival(read, kind, failure):
    row = read()
    p.need(row is not None and row[0] == kind, failure)
    return row[1]

def transport(pipe, notices, records, stop, ledger, info, exe, bundle, phase, mode, base,
              scientific, local_cap, relay, lease):
    try:
        lease["thread"] = n.thread_lease()
        save = lambda name, data: ledger.save(base + "-" + name, data, local_cap=local_cap)
        save("start.json", p.encode(info))
        notices.put("RESUME")
        def read():
            if stop.is_set():
                raise p.Rejected("TRANSPORT_STOPPED")
            return p.frame(lambda count: n.read(pipe, count))
        raw = arrival(read, b"H", "IPC_EXPECTED_HELLO")
        context = info["context"]
        row = hello_check(raw, context, exe, bundle)
        save("runtime.json", raw)
        records["runtime"] = p.binding(raw)
        notices.put("GRANT")
        if mode in ("native", "sampled", "sleep", "gap") and not scientific:
            marker = p.decode(arrival(read, b"A", "IPC_EXPECTED_FIXTURE_START"))
            p.need(marker == context, "FIXTURE_START_CONTEXT")
            records["fixture_started"] = True
            p.need(read() is None, "IPC_UNEXPECTED_FRAME")
            return
        if mode == "crash-owner" and not scientific:
            raw = arrival(read, b"J", "IPC_EXPECTED_CRASH_ID")
            records["crash_receipt"] = relay(p.decode(raw), info, save, read, notices)
            p.need(read() is None, "IPC_UNEXPECTED_FRAME")
            return
        if mode == "child-refusal" and not scientific:
            raw = arrival(read, b"T", "IPC_EXPECTED_CHILD_RECEIPT")
            records["child"] = p.decode(raw)
            if records["child"].get("created") is True:
                row = records["child"]
                with n.Owned(n.OpenProcess(0x00101001, False, row["pid"])) as child:
                    child_before = live_read(child.handle)
                    p.need(child_before["born"] == row["born"], "UNEXPECTED_CHILD_IDENTITY")
                    until = min(info["deadline_tick"], n.Tick() + 1000)
                    if not n.wait(child.handle, 0):
                        n.check(n.TerminateProcess(child.handle, n.TERMINATED_BY_SUPERVISOR))
                    if not n.wait(child.handle, p.remaining(n.Tick(), until, 1000)):
                        raise UnsafeCleanup("UNEXPECTED_CHILD_EXIT_UNVERIFIED", info["deadline_tick"])
                    records["unexpected_child_verified_exit"] = terminal_read(child.handle, child_before)
                    save("child-cleanup.json", p.encode(records["unexpected_child_verified_exit"]))
                    notices.put("ACK")
            save("child.json", raw)
            p.need(read() is None, "IPC_UNEXPECTED_FRAME")
            return
        result = read()
        p.need(result is not None and result[0] in (b"C", b"R"), "IPC_EXPECTED_RESULT")
        kind, raw = result
        value = p.result_record(raw, phase, bundle["limits"][phase])
        p.need((kind == b"C") == (value["status"] == "CANDIDATE"), "IPC_RESULT_TAG")
        records["result"] = {k: v for k, v in value.items() if k not in ("labels", "inert_padding")}
        if kind == b"C":
            identity = p.persist_candidate(ledger, base, raw, value, context, local_cap)
            records["candidate"] = identity
            if stop.is_set():
                raise p.Rejected("STOP_BEFORE_ACK")
            notices.put("ACK")
            raw = arrival(read, b"V", "IPC_EXPECTED_VERIFICATION")
            save("verification.json", raw)
            verified = p.verified_record(raw, context, identity, scientific, TARGETS,
                                         value["rank_class"], value)
            records["verified"] = verified
        else:
            save("result.json", raw)
        p.need(read() is None, "IPC_UNEXPECTED_FRAME")
    except Exception as error:
        records["transport_error"] = str(error)[:350]
        notices.put("TRANSPORT_ERROR")

def configure_job(stack, config):
    job = stack.enter_context(n.Owned(n.CreateJob(None, None)))
    n.configure(job.handle, config["user_max"])
    limits = n.limits(job.handle)
    p.need(limits == dict(native_user_ticks=config["user_max"], flags=n.FLAGS,
                          active_limit=1, end_action=0, job_handle_inheritable=False), "JOB_LIMITS")
    before = n.accounting(job.handle)
    p.need(all(before[k] == 0 for k in ("lifetime", "active", "user", "kernel")), "JOB_NOT_EMPTY")
    return job, limits, before

class JobObservations:
    """Bounded diagnostics. Notifications never replace strict Job reconciliation."""
    def __init__(self, stack, job):
        self.job = job
        self.port = n.attach_job_port(stack, job)
        self.events, self.points, self.identities = [], [], []

    def observe(self, label, expected=None):
        while len(self.events) < 64:
            event = n.job_event(self.port.handle, self.job)
            if event is None:
                break
            event["stage"] = label
            self.events.append(event)
        p.need(len(self.events) < 64, "JOB_NOTIFICATION_CAP")
        ids = n.job_pids(self.job)
        stats = n.accounting(self.job)
        self.points.append(dict(stage=label, tick=n.Tick(), accounting=stats, **ids))
        unexpected = [pid for pid in ids["pids"] if pid != expected]
        for pid in unexpected:
            handle = n.OpenProcess(0x00101000, False, pid)
            if not handle:
                self.identities.append(dict(pid=pid, identity=None))
                continue
            with n.Owned(handle) as owned:
                if n.in_job(owned.handle, self.job):
                    self.identities.append(dict(pid=pid, creation=n.sample(owned.handle)["born"],
                                                image_name=Path(n.image(owned.handle)).name))
                else:
                    self.identities.append(dict(pid=pid, identity=None))
        return unexpected

    def record(self):
        return dict(events=self.events, snapshots=self.points,
                    observed_unexpected_identities=self.identities, delivery_exhaustive=False)

def launch_worker(stack, launch, job, exe, sha, profile, phase, mode, run_name, base):
    token = secrets.token_hex(16)
    n.configure_startup(stack, job.handle if job else None, exe, exe.parent, HERE / "worker.py",
                        [TASK, sha, profile, phase, mode, token, run_name, base], launch)
    proc = launch["process"].handle
    p.need(Path(n.image(proc)) == exe and not n.wait(proc, 0), "SUSPENDED_PROCESS_IMAGE")
    if job:
        p.need(n.in_job(proc, job.handle), "AT_CREATION_MEMBERSHIP")
    return dict(task=TASK, phase=phase, nonce=token, pid=launch["pid"])

def cleanup(launch, job, watcher, stop, deadline, grace, ordinary_end, lease):
    stop.set()
    until = min(deadline, n.Tick() + grace)
    proc = launch.get("process")
    proc = proc.handle if proc is not None else None
    errors = []
    if proc and not n.wait(proc, 0):
        errors = n.stop_worker(job.handle if job else None, proc)
    while proc and not n.wait(proc, 0):
        delay = p.remaining(n.Tick(), until, 20)
        if not delay:
            raise UnsafeCleanup("UNCONFIRMED_WORKER_EXIT")
        n.wait(proc, delay)
    if watcher and watcher.is_alive():
        if not ordinary_end and "thread" in lease:
            try:
                n.cancel_thread(lease["thread"].handle)
            except OSError as error:
                errors.append(("CancelSynchronousIo", error.winerror))
        delay = p.remaining(n.Tick(), until, grace)
        watcher.join(delay / 1000)
        if watcher.is_alive():
            # The still-live transport owns its open pipe until controller exit.
            launch["source"].handle = None
            raise UnsafeCleanup("TRANSPORT_EXIT_NOT_CONFIRMED")
    if n.Tick() > until:
        raise UnsafeCleanup("CLEANUP_DEADLINE_EXCEEDED")
    return errors, until

def run_phase(exe, sha, bundle, ledger, run_name, base, phase, mode, config,
              scientific=False, local_cap=None, relay=None, started=None, local_cpu=None):
    if started is None:
        started = n.Tick()
    deadline = started + config["wall"]
    if local_cpu is None:
        local_cpu = live_read(n.CurrentProcess())
    stop = threading.Event()
    notices = queue.SimpleQueue()
    launch, records, lease = {}, {}, {}
    job = watcher = initial = job_observation = job_started = None
    failure = stop_sample = None
    reasons, maximum_gap, last_tick = [], 0, started
    previous = first = None
    injected = False
    admitted = {"resume": False, "grant": False, "ack": False}
    native_error = []
    with ExitStack() as stack:
        try:
            enclosing_limits = None
            if n.in_job(n.CurrentProcess()):
                outer = n.job_info(None, n.EXTENDED_LIMIT, n.ExtendedLimit).basic
                enclosing_limits = dict(flags=outer.flags, active_limit=outer.active_limit,
                                        user_time=outer.job_user, process_time=outer.process_user)
            if mode != "crash-owner":
                job, effective, empty = configure_job(stack, config)
                job_observation = JobObservations(stack, job.handle)
                job_observation.observe("before-create")
            else:
                effective = empty = None
            p.need(n.Tick() < started + config["early"], "PRE_LAUNCH_DEADLINE")
            profile = "official" if scientific else "synthetic"
            context = launch_worker(stack, launch, job, exe, sha, profile, phase, mode, run_name, base)
            proc = launch["process"].handle
            initial = live_read(proc)
            job_started = n.accounting(job.handle) if job else None
            if job:
                p.need(job_started["active"] == job_started["lifetime"] == 1
                       and n.limits(job.handle) == effective, "SUSPENDED_JOB_ACCOUNTING")
                p.need(not job_observation.observe("suspended", launch["pid"]), "UNEXPECTED_JOB_MEMBER")
            info = dict(context=context, start_tick=started, deadline_tick=deadline,
                        process=initial, effective=effective, enclosing=enclosing_limits,
                        job_empty=empty, job_suspended=job_started, assigned=job is not None,
                        run=run_name, freeze=sha, profile=profile, mode=mode,
                        controller=dict(pid=os.getpid(), born=local_cpu["born"]))
            watcher = threading.Thread(target=transport, daemon=True, args=(
                launch["source"].handle, notices, records, stop, ledger, info, exe, bundle, phase,
                mode, base, scientific, local_cap, relay, lease))
            watcher.start()
            sample_at = started
            while True:
                now = n.Tick()
                if now < last_tick:
                    failure = "ELAPSED_REGRESSION"
                    break
                if now >= sample_at or n.wait(proc, 0):
                    sample = live_read(proc)
                    now = n.Tick()
                    maximum_gap = max(maximum_gap, now - last_tick)
                    p.need(sample["born"] == initial["born"] and (previous is None or all(
                        sample[k] >= previous[k] for k in ("user", "kernel"))), "PROCESS_ACCOUNTING")
                    previous = sample
                    if first is None:
                        first = dict(tick=now, **sample)
                    last_tick, sample_at = now, now + config["tick"]
                    observed = ticks(sample)
                    if not scientific:
                        observed += ticks(live_read(n.CurrentProcess())) - ticks(local_cpu)
                    if maximum_gap > config["gap"]:
                        failure = "OBSERVATION_GAP"
                    elif observed >= config["cpu_early"]:
                        failure = "SAMPLED_COMBINED_CPU"
                    elif now - started >= config["early"]:
                        failure = "SAMPLED_ELAPSED"
                    if failure:
                        stop_sample = dict(tick=now, combined=observed, process=sample)
                        break
                if n.wait(proc, 0) and not watcher.is_alive() and n.Tick() <= sample_at:
                    break
                # Serialize resume/grant/ack with stop decisions in this thread.
                while not notices.empty():
                    ready = notices.get()
                    if ready == "TRANSPORT_ERROR":
                        failure = records["transport_error"]
                        break
                    if n.Tick() >= started + config["early"] or n.Tick() - last_tick > config["gap"]:
                        failure = "PRE_CONTROL_DEADLINE"
                        break
                    if job_observation and job_observation.observe(ready.lower(), launch["pid"]):
                        failure = "UNEXPECTED_LIVE_JOB_MEMBER"
                        break
                    if ready == "RESUME":
                        p.need(not admitted["resume"], "DUPLICATE_RESUME")
                        p.need(n.ResumeThread(launch["thread"].handle) == 1, "INITIAL_SUSPENSION")
                        admitted["resume"] = True
                    elif ready == "GRANT":
                        p.need(admitted["resume"] and not admitted["grant"], "GRANT_ORDER")
                        n.check(n.SetEvent(launch["gates"][0].handle))
                        admitted["grant"] = True
                    elif ready == "ACK":
                        p.need(admitted["grant"] and not admitted["ack"], "ACK_ORDER")
                        n.check(n.SetEvent(launch["gates"][1].handle))
                        admitted["ack"] = True
                if failure:
                    break
                if mode == "gap" and records.get("fixture_started") and not injected:
                    injected = True
                    time.sleep(2.25)
                else:
                    time.sleep(0.015)
        except Exception as error:
            failure = str(error)[:350]
        finally:
            try:
                native_error, cleanup_until = cleanup(
                    launch, job, watcher, stop, deadline, config["cleanup"], not failure, lease)
            except UnsafeCleanup as error:
                error.deadline = deadline
                raise
            finally:
                if "thread" in lease:
                    lease["thread"].close()
        proc = launch.get("process")
        finished = exit_code = signaled_job = final = None
        if proc is not None:
            if initial is not None:
                finished = terminal_read(proc.handle, previous or initial)
            exit_code = n.exit_code(proc.handle)
            if job:
                signaled_job = n.wait(job.handle, 0)
                if job_observation.observe("before-process-handle-close", launch["pid"]):
                    failure = "UNEXPECTED_LIVE_JOB_MEMBER"
                    native_error.extend(n.stop_worker(job.handle, proc.handle))
            launch["thread"].close()
            proc.close()
        if job:
            final = n.accounting(job.handle)
            while final["active"] and n.Tick() < cleanup_until:
                delay = p.remaining(n.Tick(), cleanup_until, 20)
                time.sleep(delay / 1000)
                final = n.accounting(job.handle)
            if final["active"] or n.Tick() > cleanup_until:
                raise UnsafeCleanup("JOB_NOT_EMPTY", deadline)
            if job_observation.observe("after-job-active-zero", launch["pid"]):
                raise UnsafeCleanup("JOB_MEMBER_AFTER_CLEANUP", deadline)
    end = n.Tick()
    cpu = ticks(live_read(n.CurrentProcess())) - ticks(local_cpu)
    combined = None if finished is None else max(ticks(finished), ticks(final) if final else 0)
    observations = job_observation.record() if job_observation else None
    accounting = reconcile_terminal_cpu(initial, job_started, finished, final, observations)
    reconciled = accounting["mode"] != "unresolved"
    if mode == "child-refusal" and finished is not None and final is not None:
        child = records.get("child", {})
        if admitted["grant"] and (
                "created" not in child or
                child["created"] and "unexpected_child_verified_exit" not in records):
            raise UnsafeCleanup("CHILD_REFUSAL_CLEANUP_UNVERIFIED", deadline)
        # A denied association can count as brief lifetime membership. No child code is resumed.
        limit_message = any(e["message"] == JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT
                            for e in observations["events"])
        reconciled = (child.get("created") is False and child.get("winerror") in (5, ERROR_NOT_ENOUGH_QUOTA)
                      and final["lifetime"] in (1, 2)
                      and (final["lifetime"] == 2 or final["terminated"] > job_started["terminated"]
                           or limit_message)
                      and all(final[k] >= finished[k] for k in ("user", "kernel")))
    if mode == "crash-owner":
        crash = records.get("crash_receipt")
        if crash is None:
            raise UnsafeCleanup("INTERRUPTED_OWNER_WITHOUT_VERIFIED_CHILD_EXIT")
        p.need(finished == crash["owner_terminal"], "INTERRUPTED_OWNER_MEASUREMENT")
        combined = ticks(finished) + ticks(crash["worker_terminal"])
        reconciled = crash["owner_exit"] == n.TERMINATED_BY_SUPERVISOR
        if reconciled and failure is None:
            failure = "KILL_ON_CLOSE_OBSERVED"
    if native_error and failure is None:
        failure = "NATIVE_TERMINATION_ERROR"
    if (failure is None and mode == "native" and records.get("fixture_started")
            and native_user_limit_observed(exit_code, signaled_job, final, config["user_max"],
                                           observations["events"])):
        failure = "NATIVE_USER_LIMIT"
    if failure is None and (exit_code != 0 or records.get("transport_error")):
        failure = records.get("transport_error") or "WORKER_EXIT_FAILURE"
    meter_cpu = None if combined is None else combined + (0 if scientific else cpu)
    meter = (meter_cpu is not None and 0 <= meter_cpu <= config["cpu_max"]-accounting["guard_ticks"] and cpu >= 0
             and 0 <= end - started <= config["wall"] and reconciled and not native_error
             and (maximum_gap <= config["gap"] or mode == "gap" and failure == "OBSERVATION_GAP"))
    return dict(process=finished, job=final, native_error=native_error, exit_code=exit_code,
                job_end_signaled=signaled_job,
                failure=failure, phase=phase, app=records, admitted=admitted,
                worker_cpu=combined, controller_cpu=cpu, observed_cpu=meter_cpu,
                elapsed=end-started, start_tick=started, deadline=deadline, first=first, last=previous,
                controller_start_cpu=ticks(local_cpu), injected_gap=injected if watcher else False,
                job_observations=observations, accounting_reconciliation=accounting,
                stop_sample=stop_sample, maximum_gap=maximum_gap, reconciled=reconciled, measured=meter)


def crash_owner(bundle, sha, exe, send, permit, base, continuation):
    """Private grant-only inert crash fixture. The external observer owns no Job handle."""
    config = dict(SYNTH)
    started = n.Tick()
    deadline = min(permit["deadline_tick"], started + 18000)
    launch = {}
    with ExitStack() as stack:
        job, effective, empty = configure_job(stack, config)
        try:
            context = launch_worker(stack, launch, job, exe, sha, "synthetic", "primary",
                                    "crash-sleeper", permit["run"], base + "-inner")
            proc = launch["process"].handle
            before = live_read(proc)
            job_started = n.accounting(job.handle)
            p.need(job_started["active"] == job_started["lifetime"] == 1, "CRASH_CHILD_ADMISSION")
            inner = dict(context=context, process=before, effective=effective, job_empty=empty,
                         job_suspended=job_started, start_tick=started, deadline_tick=deadline,
                         assigned=True, run=permit["run"], freeze=sha, profile="synthetic",
                         mode="crash-sleeper",
                         controller=dict(pid=os.getpid(), born=live_read(n.CurrentProcess())["born"]))
            send(b"J", p.encode(inner))
            p.need(n.wait(continuation, p.remaining(n.Tick(), deadline, 5000)), "CRASH_OBSERVER_GRANT")
            p.need(n.ResumeThread(launch["thread"].handle) == 1, "CRASH_CHILD_RESUME")
            raw = arrival(lambda: p.frame(lambda k: n.read(launch["source"].handle, k)),
                          b"H", "CRASH_CHILD_HELLO")
            runtime = hello_check(raw, context, exe, bundle)
            n.check(n.SetEvent(launch["gates"][0].handle))
            activation = p.decode(arrival(lambda: p.frame(lambda k: n.read(launch["source"].handle, k)),
                                          b"A", "CRASH_CHILD_ACTIVATION"))
            p.need(activation == context, "CRASH_CHILD_ACTIVATION_CONTEXT")
            send(b"K", p.encode({"runtime": runtime, "worker_activation": activation}))
            while not n.wait(proc, 0) and n.Tick() < deadline:
                time.sleep(0.02)
        finally:
            cleanup(launch, job, None, threading.Event(), deadline, 4000, False, {})

def observe_crash(row, info, save, read, notices):
    child_pid = row["context"]["pid"]
    owner_pid = info["context"]["pid"]
    p.need(child_pid != owner_pid and row["job_suspended"]["active"] == 1
           and row["effective"]["flags"] == n.FLAGS, "CRASH_PROBE_JOB_BINDING")
    with n.Owned(n.OpenProcess(0x00101001, False, owner_pid)) as owner, \
         n.Owned(n.OpenProcess(0x00101000, False, child_pid)) as child:
        child_before, owner_before = row["process"], info["process"]
        p.need(live_read(owner.handle)["born"] == owner_before["born"]
               and live_read(child.handle)["born"] == child_before["born"]
               and not n.wait(child.handle, 0), "CRASH_PROBE_IDENTITY")
        try:
            save("inner-start.json", p.encode(row))
            notices.put("ACK")
            runtime = p.decode(arrival(read, b"K", "CRASH_WORKER_READINESS"))
            p.need(runtime["runtime"]["context"] == row["context"]
                   and runtime["worker_activation"] == row["context"] and not n.wait(child.handle, 0),
                   "CRASH_CHILD_NO_LONGER_ACTIVE")
            save("crash-ready.json", p.encode(runtime))
            p.need(not n.wait(child.handle, 0), "CRASH_CHILD_NATURAL_EXIT")
        finally:
            until = min(info["deadline_tick"], n.Tick() + 4000)
            if not n.wait(owner.handle, 0):
                n.check(n.TerminateProcess(owner.handle, n.TERMINATED_BY_SUPERVISOR))
            for entry in (owner, child):
                while not n.wait(entry.handle, 0):
                    delay = p.remaining(n.Tick(), until, 20)
                    if not delay:
                        raise UnsafeCleanup("CRASH_PROBE_EXIT_NOT_VERIFIED")
                    n.wait(entry.handle, delay)
            receipt = dict(owner_terminal=terminal_read(owner.handle, owner_before),
                           worker_terminal=terminal_read(child.handle, child_before),
                           owner_exit=n.exit_code(owner.handle), worker_exit=n.exit_code(child.handle),
                           terminal_job_unavailable_by_closed_sole_handle=True)
            save("crash-exit.json", p.encode(receipt))
        p.need(receipt["worker_exit"] not in (0, 1, 64, 65, 66, 67), "CRASH_NATURAL_EXIT_NOT_PROOF")
        return receipt
