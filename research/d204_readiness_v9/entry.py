"""Fixed qualification entry and separately Owner-gated D204 science entry."""
from contextlib import ExitStack
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import threading
import time
from types import ModuleType

HERE = Path(os.path.abspath(__file__)).parent
ROOT = HERE.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_D204_INTERRUPTION_EVIDENCE_QUALIFICATION_003"
FREEZE = EVIDENCE / "V9_FREEZE.json"
TASK = "LCL-D204-INTERRUPTION-EVIDENCE-QUALIFICATION-003"
SCIENCE_RUN = "d204-science-v9"
CANONICAL_REMOTE = "https://github.com/drkmtr1/Lobster-Construction-Lab.git"

def need(condition, label):
    if not condition:
        raise RuntimeError(label)

def binding(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def regular(path):
    for parent in (path, *path.parents):
        attr = parent.lstat().st_file_attributes
        need(not attr & stat.FILE_ATTRIBUTE_REPARSE_POINT, "REPARSE_PATH")

def raw(path, maximum):
    regular(path)
    need(path.is_file() and path.stat().st_size <= maximum, "BASE_FILE_SIZE")
    with path.open("rb") as file:
        result = file.read(maximum + 1)
    need(len(result) <= maximum, "BASE_FILE_BOUND")
    return result

def boot(sha):
    need(sys.platform == "win32" and sys.version_info[:3] == (3, 13, 17)
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "ISOLATED_BOUND_CPYTHON_REQUIRED")
    data = raw(FREEZE, 2_000_000)
    need(binding(data)["sha256"] == sha, "FREEZE_HASH")
    bundle = json.loads(data)
    need(bundle["task"] == TASK and bundle["version"] == 9 and bundle["authorized_science"] is False,
         "FREEZE_IDENTITY")
    source = {}
    for unit in ("entry", "protocol", "native", "controller"):
        path = HERE / (unit + ".py")
        info = bundle["project"][path.relative_to(ROOT).as_posix()]["identity"]
        payload = raw(path, info["bytes"])
        need(binding(payload) == info, "ACTIVE_SOURCE_HASH")
        source[unit] = payload
    for unit in ("protocol", "native", "controller"):
        name = "ready_" + unit
        need(name not in sys.modules, "UNEXPECTED_BOOT_MODULE")
        module = ModuleType(name)
        module.__file__ = str(HERE / (unit + ".py"))
        sys.modules[name] = module
        exec(compile(source[unit], module.__file__, "exec", dont_inherit=True), vars(module))
    p, n, c = (sys.modules["ready_" + unit] for unit in ("protocol", "native", "controller"))
    n.verify_layout()
    return p, n, c, bundle, data, source

def lock_inputs(n, stack, bundle, exe, data, sources):
    need(n.locked_bytes(stack, FREEZE, len(data)) == data, "LOCKED_FREEZE_CHANGED")
    root = Path(sys.base_prefix)
    need(exe == root / "python.exe", "BASE_EXECUTABLE")
    need(Path(n.image(n.CurrentProcess())) == exe, "DIRECT_BASE_REQUIRED")
    project = {}
    for name, item in bundle["project"].items():
        path = ROOT / name
        regular(path)
        bound = item["identity"]
        view = n.locked_bytes(stack, path, bound["bytes"] * (2 if item["canonical"] else 1))
        if item["canonical"]:
            view = view.replace(b"\r\n", b"\n")
        need(binding(view) == bound, "LOCKED_SOURCE_HASH: " + name)
        project[name] = view
    for unit, payload in sources.items():
        need(payload == project[(HERE / (unit + ".py")).relative_to(ROOT).as_posix()],
             "BOOT_SOURCE_CHANGED")
    for path in (root, root / "Lib", root / "DLLs", HERE):
        regular(path)
        n.locked_file(stack, path, directory=True)
    need(not any(root.glob("*._pth"))
         and (root / "python313.zip").exists() == ("python313.zip" in bundle["dependencies"]),
         "UNEXPECTED_STARTUP_PATH_ENTRY")
    for name, bound in bundle["dependencies"].items():
        path = root / name
        regular(path)
        payload = n.locked_bytes(stack, path, bound["bytes"])
        need(binding(payload) == bound, "LOCKED_RUNTIME_IDENTITY: " + name)
    return project

def read_bound_doc(n, stack, path, sha, decoder, maximum=1 << 20):
    regular(path)
    value = n.locked_bytes(stack, path, maximum)
    need(binding(value)["sha256"] == sha, "APPROVAL_OR_REVIEW_HASH")
    return decoder(value), value

def local_git(*args):
    exe = Path(os.environ["ProgramFiles"]) / "Git/cmd/git.exe"
    regular(exe)
    system = os.environ["SystemRoot"]
    child = subprocess.Popen([str(exe), "-c", "core.fsmonitor=false", *args],
                             cwd=ROOT, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, close_fds=True,
                             env=dict(SystemRoot=system, WINDIR=system, PATH=str(exe.parent),
                                      GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="NUL",
                                      GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0"))
    output = []
    deadline = time.monotonic() + 20
    reader = threading.Thread(target=lambda: output.append(child.stdout.read(1_048_577)), daemon=True)
    reader.start()
    try:
        child.wait(timeout=max(0, deadline - time.monotonic() - 3))
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait(timeout=max(0, deadline - time.monotonic()))
        raise RuntimeError("LOCAL_GIT_DEADLINE")
    reader.join(max(0, deadline - time.monotonic()))
    need(not reader.is_alive() and child.returncode == 0 and len(output) == 1
         and len(output[0]) <= 1_048_576, "LOCAL_GIT_CAPTURE")
    child.stdout.close()
    return output[0]

def qualification_gate(p, marker, freeze_sha, matrix, terminal_raw, seal_raw, outer_raw, phases):
    """Check the archived native qualification to which an official marker refers."""
    need(marker.get("task") == TASK and marker.get("freeze") == freeze_sha
         and marker.get("ready") is True and marker.get("all_required_checks_passed") is True
         and marker.get("disposition") == "D204_EXECUTION_READY_AWAITING_OWNER_AUTHORIZATION",
         "FINAL_QUALIFICATION_REQUIRED")
    for name, payload in (("terminal", terminal_raw), ("seal", seal_raw), ("outer", outer_raw)):
        need(marker.get(name) == binding(payload), "QUALIFICATION_RECEIPT_BINDING")
    terminal, seal, outer = (p.decode(raw) for raw in (terminal_raw, seal_raw, outer_raw))
    need(terminal.get("task") == seal.get("task") == TASK
         and terminal.get("freeze") == seal.get("freeze") == freeze_sha
         and terminal.get("mode") == "qualify" and seal.get("terminal") == binding(terminal_raw)
         and outer.get("controller_signaled") is True and outer.get("outer_timeout") is False
         and type(outer.get("exit_code")) is int and outer["exit_code"] == 0
         and p.finite(outer.get("controller_cpu_total"), 160)
         and p.finite(outer.get("controller_cpu_user"), 160)
         and p.finite(outer.get("controller_cpu_kernel"), 160)
         and abs(outer["controller_cpu_total"] - outer["controller_cpu_user"]
                 - outer["controller_cpu_kernel"]) <= 0.000001
         and p.exact_int(outer.get("actual_outer_elapsed_ms"), 1, 795000),
         "QUALIFICATION_NATIVE_TERMINAL")
    result = terminal["result"]
    cases = matrix["cases"]
    observations = result["cases"]
    need(result["qualification_pass"] is True and result["entered"] == 16
         and len(cases) == len(observations) == 14
         and p.exact_int(result.get("aggregate_controller_worker_cpu_ticks"), 0,
                         matrix["maximum_aggregate_cpu_ticks"])
         and p.exact_int(result.get("elapsed_ms"), 0, matrix["maximum_sequence_ms"]),
         "QUALIFICATION_MATRIX_COMPLETENESS")
    all_names = set()
    for expected, observed in zip(cases, observations):
        plan = expected["phases"]
        need(observed["case"] == expected["id"] and observed["expected"] == expected["expect"]
             and observed["pass_"] is True and len(plan) == len(observed["phases"]),
             "QUALIFICATION_CASE_COMPLETENESS")
        for index, ((phase, mode), summary) in enumerate(zip(plan, observed["phases"])):
            name = expected["id"] + "-" + phase + "-phase.json"
            all_names.add(name)
            policy = matrix["test_policy"] | expected.get("policy", {})
            disposition = expected["expect"] if index+1 == len(plan) else "ADMIT_AUDIT"
            payload = phases[name]
            envelope = p.decode(payload)
            controls = envelope["controls"]
            need(terminal["prior_artifacts"].get(name) == binding(payload)
                 and summary["phase"] == controls["phase"] == phase
                 and summary["disposition"] == envelope["provisional_disposition"] == disposition
                 and summary["measured"] is True and controls["measured"] is True
                 and p.exact_int(summary["actual_cpu_ticks"], 0, policy["cpu_max"])
                 and p.exact_int(summary["actual_elapsed_ms"], 0, policy["wall"]),
                 "QUALIFICATION_PHASE_RECONCILIATION")
            if mode == "crash-owner":
                crash = controls["app"]
                raw_name = expected["id"] + "-" + phase + "-crash-exit.json"
                need(raw_name in phases and crash["crash_classification"] ==
                     {"cleanup_verified": True, "controlled_interruption": True, "reason": None}
                     and terminal["prior_artifacts"].get(raw_name) == crash["crash_raw_binding"]
                     == binding(phases[raw_name])
                     and p.decode(phases[raw_name]) == crash["crash_receipt"]
                     and controls["job"] is None
                     and controls["accounting_reconciliation"]["mode"] == "isolated-crash-process-times",
                     "QUALIFICATION_CRASH_RECONCILIATION")
                all_names.add(raw_name)
    need(set(phases) == all_names and len(all_names) == 17, "QUALIFICATION_ARCHIVE_PHASE_SET")


def verify_qualification(n, stack, p, marker, freeze_sha):
    folder = EVIDENCE / "V9_RUN"
    archive_files = {}
    for key, path in (("terminal", folder / "terminal.json"), ("seal", folder / "seal.json"),
                      ("outer", EVIDENCE / "V9_LAUNCH.json")):
        expected = marker.get(key, {}).get("sha256")
        _, archive_files[key] = read_bound_doc(n, stack, path, expected, p.decode)
    matrix_raw = n.locked_bytes(stack, HERE / "matrix.json", 65536)
    matrix = p.decode(matrix_raw)
    archived = p.decode(archive_files["terminal"])["prior_artifacts"]
    names = [case["id"] + "-" + phase + "-phase.json"
             for case in matrix["cases"] for phase, _ in case["phases"]]
    names.append("crash-primary-crash-exit.json")
    phases = {name: read_bound_doc(n, stack, folder / name, archived[name]["sha256"], p.decode)[1]
              for name in names}
    qualification_gate(p, marker, freeze_sha, matrix, archive_files["terminal"], archive_files["seal"],
                       archive_files["outer"], phases)


def authorize(n, stack, p, mode, review_sha, freeze_sha, bundle):
    if mode == "qualify":
        review, _ = read_bound_doc(n, stack, EVIDENCE / "V9_REVIEW.json", review_sha, p.decode)
        need(review.get("task") == TASK and review.get("freeze") == freeze_sha
             and review.get("disposition") == "PASS_FOR_SYNTHETIC_QUALIFICATION",
             "PRELAUNCH_REVIEW_REQUIRED")
        return ROOT / "runs/d204-readiness-v9", None, None
    q = EVIDENCE / "V9_FINAL_QUALIFICATION.json"
    path = ROOT / "runs/d204-science-v9-approval.json"
    approval, exact = read_bound_doc(n, stack, path, review_sha, p.decode, 65536)
    need(approval.get("intent") == "AUTHORIZE_ONE_D204_SCIENTIFIC_RUN"
         and approval.get("run") == SCIENCE_RUN and approval.get("freeze") == freeze_sha
         and approval.get("limits") == bundle["limits"]
         and approval.get("task") == TASK and type(approval.get("owner_authorization")) is str
         and bool(approval["owner_authorization"].strip())
         and re.fullmatch("[0-9a-f]{40}", approval.get("approved_repository_head", "")),
         "EXACT_FRESH_OWNER_AUTHORIZATION_REQUIRED")
    qualified, qualification = read_bound_doc(n, stack, q, approval["qualification_sha256"], p.decode)
    need(qualified.get("freeze") == freeze_sha and qualified.get("ready") is True
         and qualified.get("disposition") == "D204_EXECUTION_READY_AWAITING_OWNER_AUTHORIZATION"
         and qualified.get("all_required_checks_passed") is True,
         "FINAL_QUALIFICATION_REQUIRED")
    verify_qualification(n, stack, p, qualified, freeze_sha)
    head = approval["approved_repository_head"]
    need(local_git("rev-parse", "HEAD", "origin/main").decode().splitlines() == [head, head]
         and local_git("remote", "get-url", "origin").decode().strip() == CANONICAL_REMOTE
         and not local_git("status", "--porcelain", "--ignore-submodules=all"),
         "FRESH_SCIENTIFIC_GIT_CUSTODY")
    need(local_git("show", head + ":" + q.relative_to(ROOT).as_posix()) == qualification
         and local_git("show", head + ":" + FREEZE.relative_to(ROOT).as_posix()) ==
         n.locked_bytes(stack, FREEZE, 2_000_000), "APPROVED_GIT_BLOBS")
    expected = {"lcl_main":head, "mdl_head":"858a8c1fcfda87ba40bb1adee498a6131504a803",
                "bounded_search_head":"e48b94eec4091b4fe189e325cab2eda464409943",
                "tag":"fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d",
                "peel":"36ea1603602491bf3c1c5b81ed4c23aaa2210e70"}
    need(local_git("rev-parse", "lcl-v0.1.0-baseline", "lcl-v0.1.0-baseline^{}").decode().splitlines()
         == [expected["tag"], expected["peel"]] and approval.get("verified_live_refs") == expected,
         "FRESH_REMOTE_AND_TAG_RECEIPT")
    receipt, live_bytes = read_bound_doc(n, stack, ROOT / "runs/d204-science-v9-live-refs.json",
                                approval["live_ref_receipt_sha256"], p.decode, 65536)
    need(receipt.get("task") == TASK and receipt.get("run") == SCIENCE_RUN
         and receipt.get("refs") == expected and type(receipt.get("checked_unix")) is int
         and 0 <= time.time() - receipt["checked_unix"] <= 900,
         "CHECKED_LIVE_REFS_REQUIRED")
    return ROOT / "evidence/runs/d204-science-v9", exact, live_bytes


def sequence(c, p, exe, sha, bundle, ledger, run, label, plan, config_for, scientific=False,
             local_cap=None, enter=None, complete=None):
    phases, previous = [], None
    for phase, mode in plan:
        if phase == "audit" and previous != "ADMIT_AUDIT":
            break
        if enter is not None:
            enter()
        base = phase if scientific else label + "-" + phase
        config = config_for(phase)
        began = c.n.Tick()
        cpu_begin = c.live_read(c.n.CurrentProcess())
        deadline = began+config["wall"]
        c.bounded_io(lambda: ledger.save(base + "-entry.json", p.encode(
            dict(phase=phase, workload=mode))), min(deadline, began+config["early"]))
        meter = c.run_phase(exe, sha, bundle, ledger, run.name, base, phase, mode, config,
                            scientific=scientific, local_cap=local_cap, relay=c.observe_crash,
                            started=began, local_cpu=cpu_begin)
        value = meter["app"].get("result", {})
        status = value.get("status")
        if meter["failure"]:
            result = meter["failure"] if not scientific else "STOP_RESOURCE_OR_CUSTODY_FAILURE"
        elif mode == "child-refusal" and not scientific:
            result = "CHILD_REFUSED"
        else:
            result = p.decide(phase, status, meter["app"].get("verified"), meter["measured"], previous)
        if phase == "audit" and status == "CANDIDATE" and result != "STOP_ENGINE_DISCREPANCY":
            meter["audit_disagreement_with_verification_or_custody_failure"] = True
        # This record is provisional. Force the full retained phase evidence before admitting audit.
        def commit_phase():
            ledger.save(base + "-phase.json", p.encode(dict(provisional_disposition=result, controls=meter)))
            ledger.verify()
        c.bounded_io(commit_phase, deadline)
        complete_cpu = None if meter["worker_cpu"] is None else meter["worker_cpu"]
        if complete_cpu is not None and not scientific:
            complete_cpu += c.ticks(c.live_read(c.n.CurrentProcess())) - meter["controller_start_cpu"]
        now = c.n.Tick()
        accepted = (meter["measured"] and complete_cpu is not None and
                    0 <= complete_cpu <= config["cpu_max"] -
                    meter.get("accounting_reconciliation", {}).get("guard_ticks", 0) and
                    0 <= now-meter["start_tick"] <= config["wall"])
        if not scientific and mode in ("native", "sampled", "sleep", "gap"):
            accepted = accepted and meter["app"].get("fixture_started") is True
            if mode == "gap":
                accepted = accepted and meter["injected_gap"] is True
        if not scientific and mode == "crash-owner":
            controller_end = c.live_read(c.n.CurrentProcess())
            if c.valid_live_sample(controller_end, meter["app"]["crash_controller_accounting"]["end"]):
                if meter["worker_cpu"] is not None:
                    complete_cpu = (meter["worker_cpu"] + c.ticks(controller_end)
                                    - meter["controller_start_cpu"])
                now = c.n.Tick()
                accepted = (accepted and complete_cpu is not None
                            and 0 <= complete_cpu <= config["cpu_max"]
                            and 0 <= now-meter["last_observation_tick"] <= config["gap"]
                            and 0 <= now-meter["start_tick"] <= config["wall"])
            else:
                complete_cpu = None
                accepted = False
        if not accepted:
            result = "STOP_RESOURCE_OR_CUSTODY_FAILURE"
        phases.append(dict(phase=phase, disposition=result, measured=accepted,
                           actual_elapsed_ms=now-meter["start_tick"], actual_cpu_ticks=complete_cpu,
                           disagreement=bool(meter.get("audit_disagreement_with_verification_or_custody_failure"))))
        if complete is not None:
            complete(meter["worker_cpu"])
        if not accepted or result != "ADMIT_AUDIT":
            break
        previous = result
    return phases

def matrix(c, p, exe, sha, bundle, project, ledger, run):
    data = p.decode(project[(HERE / "matrix.json").relative_to(ROOT).as_posix()])
    p.need(data["task"] == TASK and data["scientific_dispatch"] is False
           and data["test_policy"] == c.SYNTH and data["maximum_workers"] == 16
           and sum(len(case["phases"]) for case in data["cases"]) <= 16, "MATRIX_SCOPE")
    out, entered, worker_sum = [], 0, 0
    start = c.n.Tick()
    cpu_start = c.ticks(c.live_read(c.n.CurrentProcess()))
    aggregate_available = True
    def measured_aggregate():
        return c.ticks(c.live_read(c.n.CurrentProcess())) - cpu_start + worker_sum
    def enter():
        nonlocal entered
        entered += 1
        p.need(entered <= 16 and measured_aggregate() < data["maximum_aggregate_cpu_ticks"]
               and c.n.Tick() - start < data["maximum_sequence_ms"], "MATRIX_BUDGET")
    def charge(worker_cpu):
        nonlocal worker_sum, aggregate_available
        if worker_cpu is None:
            aggregate_available = False
        else:
            worker_sum += worker_cpu
    for case in data["cases"]:
        config = c.SYNTH | case.get("policy", {})
        local = None if "limit_increment" not in case else (
            ledger.charged + ledger.reserve + case["limit_increment"])
        phases = sequence(c, p, exe, sha, bundle, ledger, run, case["id"], case["phases"],
                          lambda _: config, local_cap=local, enter=enter, complete=charge)
        disposition = phases[-1]["disposition"]
        ok = (disposition == case["expect"] and len(phases) == len(case["phases"])
              and all(r["measured"] for r in phases)
              and measured_aggregate() <= data["maximum_aggregate_cpu_ticks"]
              and c.n.Tick()-start <= data["maximum_sequence_ms"])
        out.append(dict(case=case["id"], expected=case["expect"], phases=phases, pass_=ok))
        if not ok:
            break
    return dict(qualification_pass=aggregate_available and len(out) == len(data["cases"])
                and all(row["pass_"] for row in out), cases=out, entered=entered,
                aggregate_controller_worker_cpu_ticks=measured_aggregate() if aggregate_available else None,
                elapsed_ms=c.n.Tick()-start)

def official(c, p, exe, sha, bundle, ledger, run):
    phases = sequence(c, p, exe, sha, bundle, ledger, run, "official",
                      (("primary", "science"), ("audit", "science")),
                      lambda phase: c.limits_for(bundle["limits"][phase]), scientific=True)
    disposition = phases[-1]["disposition"]
    if any(phase["disagreement"] for phase in phases):
        disposition = "STOP_AUDIT_DISCREPANCY_WITH_VERIFICATION_OR_CUSTODY_FAILURE"
    return {"registered_outcome": disposition, "phases": phases}

def main():
    need(len(sys.argv) == 5 and sys.argv[1] == TASK and sys.argv[2] in ("qualify", "official"),
         "FIXED_TASK_AND_ENTRY_REQUIRED")
    mode, sha, review_sha = sys.argv[2:]
    need(all(re.fullmatch("[0-9a-f]{64}", value) for value in (sha, review_sha)), "HASH_FORMAT")
    p, n, c, bundle, data, sources = boot(sha)
    exe = Path(sys._base_executable)
    with ExitStack() as stack:
        def admission():
            with ExitStack() as bindings:
                run, approval, live_receipt = authorize(n, bindings, p, mode, review_sha, sha, bundle)
                project = lock_inputs(n, bindings, bundle, exe, data, sources)
                regular(run.parent)
                p.reserve(run)
                cap = 8_000_000 if mode == "qualify" else bundle["limits"]["new_evidence_bytes"]
                # The 4 KiB independent emergency sub-reservation comes out of the same cap.
                ledger = p.Ledger(run, cap-4096, p.TERMINAL_RESERVE-4096)
                ledger.save("admission.json", p.encode(dict(
                    task=TASK, freeze=sha, mode=mode, run=run.name, source_review_or_approval=review_sha)))
                if approval is not None:
                    ledger.save_all([("approval.json", approval), ("live-refs.json", live_receipt)])
                return bindings.pop_all(), run, project, ledger
        locked, run, project, ledger = c.bounded_io(admission, n.Tick()+180000)
        stack.enter_context(locked)
        try:
            result = (matrix(c, p, exe, sha, bundle, project, ledger, run) if mode == "qualify"
                      else official(c, p, exe, sha, bundle, ledger, run))
            def reconfirm():
                with ExitStack() as checks:
                    lock_inputs(n, checks, bundle, exe, data, sources)
                ledger.verify()
            c.bounded_io(reconfirm, n.Tick()+90000)
        except c.UnsafeCleanup as error:
            emergency = p.encode(dict(task=TASK, freeze=sha, outcome="UNVERIFIED_CLEANUP_STOP",
                                      reason=str(error)[:300], native_receipt_complete=False))
            def preserve_stop():
                if len(emergency) <= 4096:
                    with (run / "emergency.json").open("xb") as file:
                        if file.write(emergency) == len(emergency):
                            file.flush()
                            os.fsync(file.fileno())
            stop_deadline = min(error.deadline, n.Tick()+1000) if error.deadline else n.Tick()+1000
            if n.Tick() < stop_deadline:
                try:
                    c.bounded_io(preserve_stop, stop_deadline)
                except Exception:
                    pass
            raise SystemExit(3) from error
        except Exception as error:
            result = dict(execution_failure=f"{type(error).__name__}: {error}"[:512])
        terminal = p.encode(dict(
            task=TASK, mode=mode, freeze=sha, prior_artifacts=ledger.records.copy(),
            charged_before_terminal=ledger.charged, result=result, provisional=True))
        publication_deadline = n.Tick()+15000
        c.bounded_io(lambda: ledger.save("terminal.json", terminal, terminal=True), publication_deadline)
        try:
            def publish():
                ledger.verify()
                ledger.save("seal.json", p.encode(dict(
                    task=TASK, freeze=sha, terminal=p.binding(terminal),
                    meaning="Evidence reconciliation only. Acceptance also requires launcher exit and independent review."
                )), terminal=True)
                ledger.verify()
            c.bounded_io(publish, publication_deadline)
        except Exception:
            raise SystemExit(4)
    if mode == "qualify" and result.get("qualification_pass") is not True:
        raise SystemExit(2)
    if "execution_failure" in result:
        raise SystemExit(2)
    if mode == "official" and result.get("registered_outcome") not in (
            "STOP_VERIFIED_POSITIVE", "STOP_REGISTERED_NEGATIVE"):
        raise SystemExit(5)

if __name__ == "__main__":
    main()
