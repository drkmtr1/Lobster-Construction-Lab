"""One live controller, one worker and one absolute deadline per D205 phase."""
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
CRASH_OWNER_FALLBACK_MS = 18000
CRASH_SLEEP_MS = 45000
CRASH_WAIT_MS = 4000
CRASH_FIXTURE_FAILURE_EXITS = (1, 64, 65, 66, 67)
U64_MAX = (1 << 64) - 1
CPU_MAX = (1 << 63) - 1
ROOT = HERE.parents[1]
TASK = "LCL-D205-INDEPENDENT-PATH-ORDER-EXECUTION-QUALIFICATION-001"
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
            relay(p.decode(raw), info, save, read, notices, records, exe, bundle, row)
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
        value = p.result_record(raw, phase, bundle["limits"][phase],
                                bundle["candidate_domain"] if scientific else None)
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
            p.need(not scientific or mode == "science", "OFFICIAL_WORKLOAD_REQUIRED")
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
                        early_tick=started+config["early"],
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
        classification = records.get("crash_classification", {})
        if classification.get("cleanup_verified") is not True:
            raise UnsafeCleanup("CRASH_CLEANUP_UNVERIFIED", deadline)
        worker_terminal = crash["exits"]["worker"].get("times")
        owner_terminal = crash["exits"]["owner"].get("times")
        controller_terminal = live_read(n.CurrentProcess())
        controller_valid = valid_live_sample(controller_terminal, local_cpu)
        cpu = ticks(controller_terminal) - ticks(local_cpu) if controller_valid else -1
        records["crash_controller_accounting"] = dict(start=local_cpu, end=controller_terminal)
        reconciled = (classification["controlled_interruption"]
                      and owner_terminal == finished and controller_valid
                      and crash["exits"]["owner"]["code"] == exit_code and failure is None)
        combined = ticks(finished) + ticks(worker_terminal) if reconciled else None
        accounting = dict(mode="isolated-crash-process-times" if reconciled else "unresolved",
                          guard_ticks=0, ordinary_job_reconciliation=False,
                          terminal_job_unavailable_by_design=True)
        end = n.Tick()
        maximum_gap = max(maximum_gap, end - last_tick)
        if failure is None:
            failure = ("KILL_ON_CLOSE_OBSERVED" if reconciled else
                       classification["reason"] or "CRASH_PHASE_ACCOUNTING")
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
                stop_sample=stop_sample, maximum_gap=maximum_gap, last_observation_tick=last_tick,
                reconciled=reconciled, measured=meter)


def valid_live_sample(value, before=None):
    return (type(value) is dict and p.exact_int(value.get("born"), 1, U64_MAX)
            and all(p.exact_int(value.get(key), 0, CPU_MAX) for key in ("user", "kernel"))
            and (before is None or valid_live_sample(before) and value["born"] == before["born"]
                 and all(value[key] >= before[key] for key in ("user", "kernel"))))


def validate_crash_job(inner, ready=None):
    limit = dict(native_user_ticks=SYNTH["user_max"], flags=n.FLAGS, active_limit=1,
                 end_action=0, job_handle_inheritable=False)
    p.need(inner["ownership"] == {"unnamed_job": True, "owner_retains_sole_job_handle": True}
           and inner["effective"] == limit, "CRASH_JOB_OWNERSHIP_OR_LIMITS")
    creation = inner["at_creation"]
    inherited = creation["inherited"]
    p.need(inner["member"] is True and creation["job_at_creation"] is True
           and creation["flags"] == n.WORKER_CREATION_FLAGS
           and type(inherited) is list and len(inherited) == len(set(inherited)) == 4
           and all(p.exact_int(handle, 1, U64_MAX) for handle in inherited)
           and p.exact_int(creation["job_handle"], 1, U64_MAX)
           and creation["job_handle"] not in inherited, "CRASH_ASSIGNMENT_OR_INHERITANCE")
    expected_pids = {"pids": [inner["context"]["pid"]], "reported_assigned": 1}
    p.need(inner["job_pids"] == expected_pids, "CRASH_JOB_PID_COUNTS")
    accounts = [(inner["job_empty"], 0), (inner["job_suspended"], 1)]
    if ready is not None:
        p.need(ready["member"] is True and ready["initial_suspend_count"] == 1
               and ready["effective"] == limit and ready["job_pids"] == expected_pids,
               "CRASH_ACTIVE_JOB")
        accounts.append((ready["accounting"], 1))
    previous = dict(user=0, kernel=0)
    for account, members in accounts:
        p.need(all(p.exact_int(account[key], previous[key], CPU_MAX) for key in ("user", "kernel"))
               and all(p.exact_int(account[key], members, members) for key in ("active", "lifetime"))
               and p.exact_int(account["terminated"], 0, 0), "CRASH_JOB_ACCOUNTING")
        previous = account
    p.need(all(inner["job_empty"][key] == 0 for key in ("user", "kernel")), "CRASH_JOB_NOT_EMPTY")


def verify_crash_exits(receipt, info, exe):
    identities = {"owner": info, "worker": receipt["inner"]}
    holds, exits = receipt["held"], receipt["exits"]
    for label, expected in identities.items():
        identity = holds[label]
        p.need(identity["pid"] == expected["context"]["pid"]
               and identity["image"] == str(exe)
               and valid_live_sample(identity["times"], expected["process"]),
               "CRASH_RETAINED_IDENTITY")
        p.need(p.exact_int(exits[label]["signaled_tick"], 0, U64_MAX),
               "CRASH_INDEPENDENT_SIGNAL_REQUIRED")
        terminal = exits[label].get("times")
        p.need(terminal is None or terminal.get("born") == identity["times"]["born"],
               "CRASH_TERMINAL_IDENTITY")
    return identities


def classify_crash(receipt, info, exe, bundle):
    """Interpret an inert interruption transcript. Process exit and qualification are separate."""
    cleanup_verified = False
    try:
        inner = receipt["inner"]
        identities = verify_crash_exits(receipt, info, exe)
        exits, held = receipt["exits"], receipt["held"]
        cleanup_verified = True
        p.need(info["profile"] == "synthetic" and info["mode"] == "crash-owner"
               and info["assigned"] is False and info["context"]["phase"] == "primary"
               and inner["profile"] == "synthetic" and inner["mode"] == "crash-sleeper"
               and inner["assigned"] is True and inner["run"] == info["run"]
               and inner["freeze"] == info["freeze"] and inner["controller"] ==
               {"pid": info["context"]["pid"], "born": info["process"]["born"]}
               and inner["context"]["pid"] != info["context"]["pid"],
               "CRASH_FIXTURE_BINDING")
        for role in identities.values():
            context = role["context"]
            p.need(context["task"] == TASK and context["phase"] == "primary"
                   and p.exact_int(context["pid"], 1, (1 << 32)-1)
                   and type(context["nonce"]) is str and len(context["nonce"]) == 32
                   and all(char in "0123456789abcdef" for char in context["nonce"]),
                   "CRASH_CONTEXT")
        p.need(inner["context"]["nonce"] != info["context"]["nonce"], "CRASH_NONCE_REUSE")
        ready = receipt["ready"]
        hello_check(p.encode(receipt["owner_runtime"]), info["context"], exe, bundle)
        hello_check(p.encode(ready["runtime"]), inner["context"], exe, bundle)
        p.need(ready["worker_activation"] == inner["context"], "CRASH_ACTIVATION")
        validate_crash_job(inner, ready)
        p.need(receipt["observer_job_handle"] is False and receipt["terminal_job_accounting"] is None,
               "CRASH_OBSERVER_JOB_HANDLE")
        p.need(receipt["errors"] == [] and receipt["direct_worker_termination"] is False,
               "CRASH_ALTERNATE_TERMINATION_OR_OBSERVATION_FAILURE")
        request = receipt["request"]
        p.need(request["owner_unsignaled"] is True and request["worker_unsignaled"] is True
               and request["target_pid"] == held["owner"]["pid"]
               and request["target_born"] == held["owner"]["times"]["born"]
               and request["intended_status"] == n.TERMINATED_BY_SUPERVISOR
               and request["api_succeeded"] is True and request["winerror"] is None,
               "CRASH_OWNER_TERMINATION_REQUEST")
        before_request = request["prior_samples"]
        for label in identities:
            terminal = exits[label]["times"]
            p.need(valid_live_sample(before_request[label], held[label]["times"])
                   and valid_live_sample(terminal, before_request[label])
                   and p.exact_int(terminal["end"], terminal["born"], U64_MAX)
                   and p.exact_int(exits[label]["code"], 0, (1 << 32)-1),
                   "CRASH_TERMINAL_ACCOUNTING")
        p.need(exits["owner"]["code"] == n.TERMINATED_BY_SUPERVISOR
               and exits["worker"]["code"] not in (*CRASH_FIXTURE_FAILURE_EXITS,
                   ERROR_NOT_ENOUGH_QUOTA, STATUS_QUOTA_EXCEEDED, n.TERMINATED_BY_SUPERVISOR, 259),
               "CRASH_NATURAL_OR_FAILURE_EXIT")
        owner_end, worker_end = (exits[key]["times"]["end"] for key in ("owner", "worker"))
        worker_born = held["worker"]["times"]["born"]
        p.need(held["owner"]["times"]["born"] <= worker_born <= min(owner_end, worker_end),
               "CRASH_FILETIME_CORROBORATION")
        latest_signal = max(item["signaled_tick"] for item in exits.values())
        earliest_signal = min(item["signaled_tick"] for item in exits.values())
        p.need(all(p.exact_int(tick, 0, U64_MAX) for tick in (
                   info["start_tick"], info["early_tick"], info["deadline_tick"], inner["start_tick"],
                   inner["deadline_tick"], ready["resume_tick"], ready["ready_tick"], receipt["ready_received_tick"],
                   request["checked_tick"], request["issued_tick"], request["returned_tick"],
                   receipt["cleanup_deadline_tick"], receipt["observations_complete_tick"]))
               and info["start_tick"] <= inner["start_tick"] <= ready["resume_tick"] <= ready["ready_tick"]
               <= receipt["ready_received_tick"] <= request["checked_tick"] <= request["issued_tick"]
               <= request["returned_tick"] <= earliest_signal <= latest_signal
               <= receipt["observations_complete_tick"] <= receipt["cleanup_deadline_tick"]
               and inner["deadline_tick"] == min(info["deadline_tick"],
                                                 inner["start_tick"] + CRASH_OWNER_FALLBACK_MS)
               and request["issued_tick"] < info["early_tick"] <= info["deadline_tick"]
               and receipt["cleanup_deadline_tick"] == min(info["deadline_tick"], inner["deadline_tick"] - 1,
                                                         request["issued_tick"] + CRASH_WAIT_MS)
               and receipt["cleanup_deadline_tick"] < ready["resume_tick"] + CRASH_SLEEP_MS,
               "CRASH_CHRONOLOGY_OR_DEADLINE")
        return dict(cleanup_verified=True, controlled_interruption=True, reason=None)
    except (KeyError, TypeError, ValueError, p.Rejected) as error:
        return dict(cleanup_verified=cleanup_verified, controlled_interruption=False,
                    reason=str(error) if isinstance(error, p.Rejected) else "CRASH_EVIDENCE_SCHEMA")


def publish_crash(receipt, records, save, info, exe, bundle):
    records["crash_receipt"] = receipt
    payload = p.encode(receipt)
    try:
        save("crash-exit.json", payload)
    except Exception:
        verified = False
        try:
            verify_crash_exits(receipt, info, exe)
            verified = True
        except (KeyError, TypeError, ValueError, p.Rejected):
            pass
        records["crash_classification"] = dict(cleanup_verified=verified,
                                               controlled_interruption=False,
                                               reason="CRASH_RAW_EVIDENCE_NOT_DURABLE")
        raise
    records["crash_raw_binding"] = p.binding(payload)
    records["crash_classification"] = classify_crash(receipt, info, exe, bundle)


def crash_owner(bundle, sha, exe, send, permit, base, continuation):
    """Private grant-only inert crash fixture. The external observer owns no Job handle."""
    started = n.Tick()
    deadline = min(permit["deadline_tick"], started + CRASH_OWNER_FALLBACK_MS)
    launch = {}
    with ExitStack() as stack:
        job, effective, empty = configure_job(stack, SYNTH)
        try:
            context = launch_worker(stack, launch, job, exe, sha, "synthetic", "primary",
                                    "crash-sleeper", permit["run"], base + "-inner")
            proc = launch["process"].handle
            before = live_read(proc)
            job_started = n.accounting(job.handle)
            p.need(job_started["active"] == job_started["lifetime"] == 1, "CRASH_CHILD_ADMISSION")
            inner = dict(context=context, process=before, effective=effective, job_empty=empty,
                         job_suspended=job_started, start_tick=started, deadline_tick=deadline,
                         member=n.in_job(proc, job.handle), job_pids=n.job_pids(job.handle),
                         at_creation=launch["at_creation"],
                         ownership=dict(unnamed_job=True, owner_retains_sole_job_handle=True),
                         assigned=True, run=permit["run"], freeze=sha, profile="synthetic",
                         mode="crash-sleeper",
                         controller=dict(pid=os.getpid(), born=live_read(n.CurrentProcess())["born"]))
            send(b"J", p.encode(inner))
            p.need(n.wait(continuation, p.remaining(n.Tick(), deadline, 5000)), "CRASH_OBSERVER_GRANT")
            resume_tick = n.Tick()
            suspend_count = n.ResumeThread(launch["thread"].handle)
            p.need(suspend_count == 1, "CRASH_CHILD_RESUME")
            raw = arrival(lambda: p.frame(lambda k: n.read(launch["source"].handle, k)),
                          b"H", "CRASH_CHILD_HELLO")
            runtime = hello_check(raw, context, exe, bundle)
            n.check(n.SetEvent(launch["gates"][0].handle))
            activation = p.decode(arrival(lambda: p.frame(lambda k: n.read(launch["source"].handle, k)),
                                          b"A", "CRASH_CHILD_ACTIVATION"))
            p.need(activation == context, "CRASH_CHILD_ACTIVATION_CONTEXT")
            ready = dict(runtime=runtime, worker_activation=activation,
                         initial_suspend_count=suspend_count, resume_tick=resume_tick,
                         member=n.in_job(proc, job.handle), effective=n.limits(job.handle),
                         job_pids=n.job_pids(job.handle), accounting=n.accounting(job.handle),
                         ready_tick=n.Tick())
            send(b"K", p.encode(ready))
            while not n.wait(proc, 0) and n.Tick() < deadline:
                time.sleep(0.02)
        finally:
            cleanup(launch, job, None, threading.Event(), deadline, 4000, False, {})


def observe_crash(inner, info, save, read, notices, records, exe, bundle, owner_runtime):
    receipt = dict(inner=inner, owner_runtime=owner_runtime, held={}, exits={}, errors=[],
                   request=None, ready=None, direct_worker_termination=False,
                   observer_job_handle=False, terminal_job_accounting=None)
    deadline = info["deadline_tick"]
    until = min(deadline, n.Tick() + CRASH_WAIT_MS)
    with ExitStack() as stack:
        handles = {}
        try:
            p.need(inner["context"]["pid"] != info["context"]["pid"], "CRASH_DISTINCT_PROCESS")
            for label, role, access in (("owner", info, 0x00101001), ("worker", inner, 0x00101000)):
                pid = role["context"]["pid"]
                handle = stack.enter_context(n.Owned(n.OpenProcess(access, False, pid))).handle
                identity = dict(pid=n.check(n.ProcessId(handle)), image=n.image(handle),
                                times=live_read(handle))
                p.need(identity["pid"] == pid and identity["image"] == str(exe)
                       and valid_live_sample(identity["times"], role["process"]),
                       "CRASH_PROBE_IDENTITY")
                receipt["held"][label] = identity
                handles[label] = handle
            p.need(not any(n.wait(handle, 0) for handle in handles.values()), "CRASH_PRE_GRANT_EXIT")
            validate_crash_job(inner)
            save("inner-start.json", p.encode(inner))
            notices.put("ACK")
            ready = p.decode(arrival(read, b"K", "CRASH_WORKER_READINESS"))
            receipt.update(ready=ready, ready_received_tick=n.Tick())
            save("crash-ready.json", p.encode(ready))
        except Exception as error:
            receipt["errors"].append("readiness: " + str(error)[:250])
        try:
            if set(handles) == {"owner", "worker"}:
                owner, worker = handles["owner"], handles["worker"]
                prior_samples = {label: live_read(handle) for label, handle in handles.items()}
                checked = n.Tick()
                owner_live = not n.wait(owner, 0)
                worker_live = not n.wait(worker, 0)
                issued = n.Tick()
                until = min(deadline, inner["deadline_tick"] - 1, issued + CRASH_WAIT_MS)
                request = dict(prior_samples=prior_samples, checked_tick=checked, issued_tick=issued,
                               owner_unsignaled=owner_live, worker_unsignaled=worker_live,
                               target_pid=receipt["held"]["owner"]["pid"],
                               target_born=prior_samples["owner"]["born"],
                               intended_status=n.TERMINATED_BY_SUPERVISOR,
                               api_succeeded=None, winerror=None)
                receipt["request"] = request
                if owner_live and issued < until:
                    request.update(n.request_termination(owner, n.TERMINATED_BY_SUPERVISOR))
                request["returned_tick"] = n.Tick()
        except Exception as error:
            receipt["errors"].append("termination request: " + str(error)[:250])
        receipt["cleanup_deadline_tick"] = until
        pending = handles.copy()
        while pending and n.Tick() <= until:
            for label, handle in list(pending.items()):
                try:
                    if not n.wait(handle, 0):
                        continue
                    output = dict(signaled_tick=n.Tick())
                    receipt["exits"][label] = output
                    try:
                        output["times"] = n.sample(handle)
                        output["code"] = n.exit_code(handle)
                    finally:
                        del pending[label]
                except Exception as error:
                    receipt["errors"].append(label + " exit observation: " + str(error)[:250])
                    pending.pop(label, None)
            delay = p.remaining(n.Tick(), until, 20)
            if pending and delay:
                time.sleep(delay / 1000)
            elif pending:
                break
        receipt["observations_complete_tick"] = n.Tick()
        publish_crash(receipt, records, save, info, exe, bundle)
