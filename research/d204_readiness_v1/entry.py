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
from types import ModuleType

HERE = Path(os.path.abspath(__file__)).parent
ROOT = HERE.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_D204_COMPREHENSIVE_EXECUTION_READINESS_001"
FREEZE = EVIDENCE / "V1_FREEZE.json"
TASK = "LCL-D204-COMPREHENSIVE-EXECUTION-READINESS-001"
SCIENCE_RUN = "d204-science-v1"
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
    need(bundle["task"] == TASK and bundle["version"] == 1 and bundle["authorized_science"] is False,
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

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True,
                          timeout=20, encoding="utf-8").stdout.strip()

def authorize(n, stack, p, mode, review_sha, freeze_sha, bundle):
    if mode == "qualify":
        review, _ = read_bound_doc(n, stack, EVIDENCE / "V1_REVIEW.json", review_sha, p.decode)
        need(review.get("task") == TASK and review.get("freeze") == freeze_sha
             and review.get("disposition") == "PASS_FOR_SYNTHETIC_QUALIFICATION",
             "PRELAUNCH_REVIEW_REQUIRED")
        return ROOT / "runs/d204-readiness-v1", None
    q = EVIDENCE / "V1_FINAL_QUALIFICATION.json"
    path = ROOT / "runs/d204-science-v1-approval.json"
    approval, exact = read_bound_doc(n, stack, path, review_sha, p.decode, 65536)
    need(approval.get("intent") == "AUTHORIZE_ONE_D204_SCIENTIFIC_RUN"
         and approval.get("run") == SCIENCE_RUN and approval.get("freeze") == freeze_sha
         and approval.get("limits") == bundle["limits"]
         and approval.get("task") == TASK and type(approval.get("owner_authorization")) is str
         and bool(approval["owner_authorization"].strip())
         and re.fullmatch("[0-9a-f]{40}", approval.get("approved_repository_head", "")),
         "EXACT_FRESH_OWNER_AUTHORIZATION_REQUIRED")
    qualified, _ = read_bound_doc(n, stack, q, approval["qualification_sha256"], p.decode)
    need(qualified.get("freeze") == freeze_sha and qualified.get("ready") is True
         and qualified.get("disposition") == "D204_EXECUTION_READY_AWAITING_OWNER_AUTHORIZATION",
         "FINAL_QUALIFICATION_REQUIRED")
    head = approval["approved_repository_head"]
    need(git("rev-parse", "HEAD", "origin/main").splitlines() == [head, head]
         and git("remote", "get-url", "origin") == CANONICAL_REMOTE and not git("status", "--porcelain"),
         "FRESH_SCIENTIFIC_GIT_CUSTODY")
    need(git("ls-remote", "--exit-code", "origin", "refs/heads/main") == head + "\trefs/heads/main",
         "LIVE_SCIENTIFIC_GIT_CUSTODY")
    return ROOT / "evidence/runs/d204-science-v1", exact

def matrix(c, p, exe, sha, bundle, project, ledger, run):
    data = p.decode(project[(HERE / "matrix.json").relative_to(ROOT).as_posix()])
    p.need(data["task"] == TASK and data["scientific_dispatch"] is False
           and data["test_policy"] == c.SYNTH and data["maximum_workers"] == 16
           and sum(len(case["phases"]) for case in data["cases"]) <= 16, "MATRIX_SCOPE")
    out, entered, total = [], 0, 0
    start = c.n.Tick()
    for case in data["cases"]:
        result, prior = None, None
        config = c.SYNTH | case.get("policy", {})
        phases = []
        for phase, fixture in case["phases"]:
            entered += 1
            p.need(entered <= 16 and total < data["maximum_aggregate_cpu_ticks"]
                   and c.n.Tick() - start < data["maximum_sequence_ms"], "MATRIX_BUDGET")
            base = case["id"] + "-" + phase
            local = None if "limit_increment" not in case else (
                ledger.charged + ledger.reserve + case["limit_increment"])
            meter = c.run_phase(exe, sha, bundle, ledger, run.name, base, phase, fixture, config,
                                local_cap=local, relay=c.observe_crash)
            total_sample = meter["observed_cpu"]
            if total_sample is not None:
                total += total_sample
            if meter["failure"]:
                result = meter["failure"]
            elif fixture == "child-refusal":
                result = "CHILD_REFUSED"
            else:
                result = p.decide(phase, meter["app"].get("result", {}).get("status"),
                                  meter["app"].get("verified"), meter["measured"], prior)
            phase_ok = meter["measured"] and (
                total_sample is not None and total_sample <= config["cpu_max"]
                and meter["elapsed"] <= config["wall"])
            ledger.save(base + "-phase.json", p.encode(
                dict(disposition=result, controls=meter, observed=phase_ok)))
            phases.append(dict(phase=phase, disposition=result, measured=phase_ok))
            if not phase_ok or result != "ADMIT_AUDIT":
                break
            prior = result
        ok = (result == case["expect"] and len(phases) == len(case["phases"])
              and all(r["measured"] for r in phases))
        out.append(dict(case=case["id"], expected=case["expect"], phases=phases, pass_=ok))
        if not ok:
            break
    return dict(qualification_pass=len(out) == len(data["cases"]) and all(row["pass_"] for row in out),
                cases=out, entered=entered, sum_phase_process_cpu_ticks=total,
                elapsed_ms=c.n.Tick()-start)

def official(c, p, exe, sha, bundle, ledger, run):
    phases = []
    primary = None
    for phase in ("primary", "audit"):
        prior = primary if phase == "audit" else None
        if phase == "audit" and prior != "ADMIT_AUDIT":
            break
        meter = c.run_phase(exe, sha, bundle, ledger, run.name, phase, phase, "science",
                            c.limits_for(bundle["limits"][phase]), scientific=True)
        status = meter["app"].get("result", {}).get("status")
        decision = p.decide(phase, status, meter["app"].get("verified"),
                            meter["measured"] and meter["failure"] is None, prior)
        ledger.save(phase + "-phase.json", p.encode(dict(disposition=decision, controls=meter)))
        phases.append(dict(phase=phase, disposition=decision))
        if phase == "primary":
            primary = decision
    return {"registered_outcome": phases[-1]["disposition"], "phases": phases}

def main():
    need(len(sys.argv) == 5 and sys.argv[1] == TASK and sys.argv[2] in ("qualify", "official"),
         "FIXED_TASK_AND_ENTRY_REQUIRED")
    mode, sha, review_sha = sys.argv[2:]
    need(all(re.fullmatch("[0-9a-f]{64}", value) for value in (sha, review_sha)), "HASH_FORMAT")
    p, n, c, bundle, data, sources = boot(sha)
    exe = Path(sys._base_executable)
    with ExitStack() as stack:
        run, approval = authorize(n, stack, p, mode, review_sha, sha, bundle)
        project = lock_inputs(n, stack, bundle, exe, data, sources)
        regular(run.parent)
        p.reserve(run)
        cap = 8_000_000 if mode == "qualify" else bundle["limits"]["new_evidence_bytes"]
        ledger = p.Ledger(run, cap)
        ledger.save("admission.json", p.encode(dict(task=TASK, freeze=sha, mode=mode, run=run.name,
                                                  source_review_or_approval=review_sha)))
        if approval is not None:
            ledger.save("approval.json", approval)
        try:
            result = (matrix(c, p, exe, sha, bundle, project, ledger, run) if mode == "qualify"
                      else official(c, p, exe, sha, bundle, ledger, run))
            ledger.verify()
        except c.UnsafeCleanup as error:
            print("UNVERIFIED_CLEANUP_STOP:", str(error)[:300], file=sys.stderr)
            raise SystemExit(3) from error
        except Exception as error:
            result = dict(execution_failure=f"{type(error).__name__}: {error}"[:512])
        ledger.save("terminal.json", p.encode(dict(
            task=TASK, mode=mode, freeze=sha, prior_artifacts=ledger.records.copy(),
            charged_before_terminal=ledger.charged, result=result)), terminal=True)
        try:
            ledger.verify()
        except Exception:
            raise SystemExit(4)
    if mode == "qualify" and result.get("qualification_pass") is not True:
        raise SystemExit(2)
    if "execution_failure" in result:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
