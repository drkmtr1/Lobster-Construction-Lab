"""Bound D204 child entry. Real consumers load only after a private scientific grant."""
import ctypes as ct
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import time
from types import ModuleType

TASK = "LCL-D204-CONSOLE-DETACHED-EXECUTION-READINESS-002"
ROOT = Path(os.path.abspath(__file__)).parents[2]
DIR = Path(__file__).parent
FREEZE = ROOT / "evidence/validation/LCL_D204_CONSOLE_DETACHED_EXECUTION_READINESS_002/V7_FREEZE.json"
PREP = "evidence/validation/LCL_ORDINARY_SPINE_CONSECUTIVE_POSITIVE_COORDINATED_GAP_RETURN_001_PREP/"
ENGINE = "research/coordinated_gap_return_001/"
PACKAGE = "_d204_frozen_consumer"
PREFIX_DIGEST = "fd4289cb555097994341bf023415e231841e01e95c1098c7890643252241f061"
TARGETS = ("5554c99f3db5b777a5e139369479c470b9e220753da2193aecbaa3c9ac6d3515",
           "1e9d8d99227973991cb6fb850cfbcd44cfac2c3470396886c59a9264bd3de3cb")

def encoded(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")

def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def freeze(sha):
    data = bounded(FREEZE, 2_000_000)
    if len(data) > 2_000_000 or identity(data)["sha256"] != sha:
        raise RuntimeError("wrong freeze")
    result = json.loads(data)
    if result.get("task") != TASK:
        raise RuntimeError("wrong task")
    return result

def capture(bundle, name):
    item = bundle["project"][name]
    raw = bounded(ROOT / name, item["identity"]["bytes"] * (2 if item["canonical"] else 1))
    if item["canonical"]:
        raw = raw.replace(b"\r\n", b"\n")
    if identity(raw) != item["identity"]:
        raise RuntimeError("unexpected source bytes: " + name)
    return raw

def bounded(path, cap):
    with path.open("rb") as file:
        data = file.read(cap + 1)
    if len(data) > cap:
        raise RuntimeError("oversized bound file")
    return data

def exact_load(name, source, location, package=False):
    if name in sys.modules:
        raise RuntimeError("unexpected preloaded module: " + name)
    module = ModuleType(name)
    module.__file__ = str(location)
    module.__package__ = name if package else name.rpartition(".")[0]
    if package:
        module.__path__ = []
    sys.modules[name] = module
    exec(compile(source, str(location), "exec", dont_inherit=True), vars(module))
    parent, _, child = name.rpartition(".")
    if parent:
        setattr(sys.modules[parent], child, module)
    return module

def scientific_adapter(bundle, phase):
    """This function is never called by a qualification grant."""
    config = json.loads(capture(bundle, PREP + "CONFIG.json"))
    prefix = json.loads(capture(bundle, PREP + "PREFIXES.json"))["records"]["independent_32"]
    originals = json.loads(capture(bundle, PREP + "ORIGINALS.json"))["records"]
    incoming = originals["main_41"]["prefixes"][0]
    if (prefix["prefix_digest"] != PREFIX_DIGEST or incoming["digest"] != PREFIX_DIGEST
            or (originals["main_41"]["original"]["digest"],
                originals["main_48_if_admitted"]["original"]["digest"]) != TARGETS):
        raise RuntimeError("wrong original identities")
    limits = config["future_allocation_caps"][phase]
    exact_load(PACKAGE, b"", ROOT / ENGINE, package=True)
    def engine(name):
        path = ENGINE + name + ".py"
        return exact_load(PACKAGE + "." + name, capture(bundle, path), ROOT / path)
    engine("budget")
    if phase == "primary":
        runner = engine("primary").primary_search
        result = runner(prefix, limits)
    else:
        runner = engine("audit").audit_search
        result = runner(prefix, incoming["graph"], limits)
    def verify(candidate):
        path = "lcl/__init__.py"
        exact_load("lcl", capture(bundle, path), ROOT / path, package=True)
        path = "lcl/verify.py"
        exact_load("lcl.verify", capture(bundle, path), ROOT / path)
        return engine("verify_positive").verify_future_positive(candidate, originals, prefix)
    return result, verify

def fixture(limits, phase, mode, context):
    keys = ("geometry_entries", "placement_attempts", "allocation_states", "pair_trials", "fixed_edge_checks")
    counts = {key: 0 for key in keys}
    counts.update(process_cpu_seconds=0.0, wall_seconds=0.0, peak_live_records=1)
    result = dict(status="EXHAUSTED", counters=counts,
                  compatible_rank_counts=dict(rank_preserving=0, rank_changing=0))
    if mode == "exhaust":
        counts["geometry_entries"] = limits["geometry_entries"]
    elif mode == "incomplete":
        result.update(status="INCOMPLETE", limit="fixture")
    else:
        result.update(status="CANDIDATE", cut=18, rank_class="rank_preserving",
                      labels={"inert": 7})
        result["compatible_rank_counts"]["rank_preserving"] = 1
        counts["geometry_entries"] = 1
        if phase == "primary":
            result["admissible_old_cuts"] = [18]
    def verify(_):
        if mode == "verify-failure":
            raise ValueError("inert synthetic verification failure")
        return dict(status="INDEPENDENTLY_VERIFIED_POSITIVE",
                    checker_results=[{"valid": True}, {"valid": True}], synthetic=True,
                    same_pid=context["pid"])
    return result, verify

def hello(context):
    exe = Path(sys.executable)
    root = exe.parent
    expected = [root / path for path in ("python313.zip", "DLLs", "Lib", "")]
    if ([Path(p) for p in sys.path] != expected or sys.version_info[:3] != (3, 13, 17)
            or sys.platform != "win32" or ct.sizeof(ct.c_void_p) != 8
            or not sys.flags.isolated or not sys.flags.no_site or not sys.dont_write_bytecode):
        raise RuntimeError("wrong worker runtime")
    query = ct.WinDLL("kernel32.dll", use_last_error=True).GetModuleFileNameW
    query.argtypes = (ct.c_void_p, ct.c_wchar_p, ct.c_ulong)
    query.restype = ct.c_ulong
    dll = ct.create_unicode_buffer(32768)
    if not 0 < query(sys.dllhandle, dll, len(dll)) < len(dll):
        raise RuntimeError("cannot identify Python DLL")
    modules = {name: str(Path(path).absolute()) for name, mod in sys.modules.items()
               if name != "__main__" and (path := getattr(mod, "__file__", None))}
    kernel = ct.WinDLL("kernel32.dll", use_last_error=True)
    console_list = kernel.GetConsoleProcessList
    console_list.argtypes = (ct.POINTER(ct.c_ulong), ct.c_ulong)
    console_list.restype = ct.c_ulong
    console_pids = (ct.c_ulong * 16)()
    ct.set_last_error(0)
    console_count = console_list(console_pids, len(console_pids))
    console_error = ct.get_last_error()
    console_window = kernel.GetConsoleWindow
    console_window.argtypes = ()
    console_window.restype = ct.c_void_p
    return dict(context=context, executable=str(exe), dll=dll.value, search=sys.path,
                console=dict(process_count=console_count, window=bool(console_window()),
                             list_error=console_error),
                version=list(sys.version_info[:3]), no_site=bool(sys.flags.no_site),
                isolated=bool(sys.flags.isolated), no_bytecode=sys.dont_write_bytecode,
                modules=modules)

def ipc_frame(kind, raw):
    if len(raw) >= 1 << 20:
        raise RuntimeError("oversized worker frame")
    stream = sys.stdout.buffer
    stream.write(struct.pack(">I", 1 + len(raw)) + kind + raw)
    stream.flush()

def wait_for_grant(handle, maximum=20000):
    wait = ct.WinDLL("kernel32.dll", use_last_error=True).WaitForSingleObject
    wait.argtypes = (ct.c_void_p, ct.c_ulong)
    wait.restype = ct.c_ulong
    # Parent is also responsible for stop; an abandoned bootstrap cannot wait forever.
    if wait(handle, maximum) != 0:
        raise RuntimeError("private grant denied")

def authorize_grant(profile, phase, mode, run_name, base, context, sha, bundle):
    if not re.fullmatch(r"[a-z0-9-]{1,80}", base):
        raise RuntimeError("wrong phase name")
    official = profile == "official"
    if run_name != ("d204-science-v7" if official else "d204-readiness-v7"):
        raise RuntimeError("wrong run name")
    folder = ROOT / ("evidence/runs" if official else "runs") / run_name
    admission = json.loads(bounded(folder / "admission.json", 65536))
    permit = json.loads(bounded(folder / (base + "-start.json"), 65536))
    if (admission["task"] != TASK or admission["mode"] != ("official" if official else "qualify")
            or admission["run"] != run_name or admission["freeze"] != sha
            or permit["run"] != run_name or permit["freeze"] != sha
            or permit["profile"] != profile or permit["mode"] != mode
            or permit["context"] != context or permit["controller"]["pid"] != os.getppid()
            or permit["assigned"] is not (mode != "crash-owner")):
        raise RuntimeError("no matching durable live controller permit")
    if official:
        approval_raw = bounded(folder / "approval.json", 65536)
        approval = json.loads(approval_raw)
        qualification = bounded(DIR.parents[1] / "evidence/validation" /
                                 "LCL_D204_CONSOLE_DETACHED_EXECUTION_READINESS_002" /
                                 "V7_FINAL_QUALIFICATION.json", 1 << 20)
        if (identity(approval_raw)["sha256"] != admission["source_review_or_approval"]
                or approval.get("intent") != "AUTHORIZE_ONE_D204_SCIENTIFIC_RUN"
                or approval.get("run") != run_name or approval.get("freeze") != sha
                or approval.get("limits") != bundle["limits"]
                or identity(qualification)["sha256"] != approval.get("qualification_sha256")
                or json.loads(qualification).get("ready") is not True):
            raise RuntimeError("no matching fresh scientific approval")
    path = DIR / "native.py"
    n = exact_load("ready_native", capture(bundle, path.relative_to(ROOT).as_posix()), path)
    proc = n.CurrentProcess()
    parent_info = permit["controller"]
    with n.Owned(n.OpenProcess(0x00101000, False, parent_info["pid"])) as held:
        if (n.sample(held.handle)["born"] != parent_info["born"]
                or n.sample(proc)["born"] != permit["process"]["born"]
                or Path(n.image(held.handle)) != Path(sys.executable)
                or n.wait(held.handle, 0) or n.Tick() > permit["deadline_tick"]
                or (permit["assigned"] and not n.in_job(proc))):
            raise RuntimeError("unverified live phase creator, worker or Job")
    return n, permit, folder

def child_refusal(native, continuation, deadline):
    exe = sys.executable
    # No marker is allowed to execute, even on an unexpected successful creation.
    try:
        import _winapi
        ph, th, pid, _ = _winapi.CreateProcess(
            exe, subprocess.list2cmdline([exe, "-I", "-S", "-B", "-c", "raise SystemExit(79)"]),
            None, None, False, native.CREATE_SUSPENDED | native.DETACHED_PROCESS,
            None, str(Path(exe).parent), subprocess.STARTUPINFO())
    except OSError as error:
        ipc_frame(b"T", encoded(dict(created=False, winerror=error.winerror)))
        return
    try:
        before = native.sample(ph)
        ipc_frame(b"T", encoded(dict(created=True, pid=pid, born=before["born"])))
        wait_for_grant(continuation, max(0, min(3000, deadline-native.Tick())))
        if not native.wait(ph, 0):
            raise RuntimeError("unexpected suspended child not observed exited")
    finally:
        if not native.wait(ph, 0):
            native.stop_worker(None, ph)
            native.wait(ph, max(0, min(500, deadline-native.Tick())))
        _winapi.CloseHandle(th)
        _winapi.CloseHandle(ph)

def main():
    if len(sys.argv) != 11:
        raise SystemExit(64)
    task, sha, profile, phase, mode, token, run_name, base, grant, ack = sys.argv[1:]
    if (task != TASK or phase not in ("primary", "audit") or len(token) != 32
            or profile not in ("synthetic", "official") or
            (profile == "official" and (mode != "science" or run_name != "d204-science-v7"))):
        raise SystemExit(65)
    if profile == "synthetic" and mode not in {
            "positive", "exhaust", "incomplete", "verify-failure", "native", "sampled",
            "sleep", "gap", "child-refusal", "oversize", "truncated", "byte-cap", "crash-owner", "crash-sleeper",
    }:
        raise SystemExit(65)
    context = dict(task=task, pid=os.getpid(), phase=phase, nonce=token)
    ipc_frame(b"H", encoded(hello(context)))
    wait_for_grant(int(grant), 60000 if profile == "official" else 20000)
    bundle = freeze(sha)
    native, permit, folder = authorize_grant(profile, phase, mode, run_name, base, context, sha, bundle)
    if profile == "synthetic" and mode in ("native", "sampled", "sleep", "gap", "crash-sleeper"):
        ipc_frame(b"A", encoded(context))
    if profile == "synthetic" and mode in ("native", "sampled"):
        end = time.monotonic() + 8
        while time.monotonic() < end:
            sum(i * i for i in range(50000))
        raise SystemExit(66)
    if profile == "synthetic" and mode in ("sleep", "gap", "crash-sleeper"):
        time.sleep(45 if mode == "crash-sleeper" else 12)
        raise SystemExit(66)
    if profile == "synthetic" and mode == "child-refusal":
        child_refusal(native, int(ack), permit["deadline_tick"])
        return
    if profile == "synthetic" and mode in ("oversize", "truncated"):
        raw = struct.pack(">I", (1 << 20) + 1) if mode == "oversize" else struct.pack(">I", 40) + b"Cxxx"
        sys.stdout.buffer.write(raw)
        sys.stdout.buffer.flush()
        return
    if profile == "synthetic" and mode == "crash-owner":
        for unit in ("protocol", "controller"):
            path = DIR / (unit + ".py")
            exact_load("ready_" + unit, capture(bundle, path.relative_to(ROOT).as_posix()), path)
        sys.modules["ready_controller"].crash_owner(
            bundle, sha, Path(sys.executable), ipc_frame, permit, base, int(ack))
        raise SystemExit(67)
    if profile == "official":
        result, verify = scientific_adapter(bundle, phase)
    else:
        result, verify = fixture(bundle["limits"][phase], phase, mode, context)
        if mode == "byte-cap":
            result["inert_padding"] = ">" * 160000
    raw = encoded(result)
    ipc_frame(b"C" if result["status"] == "CANDIDATE" else b"R", raw)
    if result["status"] == "CANDIDATE":
        wait_for_grant(int(ack), 60000 if profile == "official" else 20000)
        receipt = json.loads(bounded(folder / (base + "-candidate.json"), 65536))
        if receipt["context"] != context or receipt["candidate"] != identity(raw):
            raise RuntimeError("verification acknowledgement has no durable matching receipt")
        payload = dict(context=context, candidate=identity(raw))
        try:
            payload["result"] = verify(result)
        except Exception as error:
            payload["error"] = f"{type(error).__name__}: {error}"[:512]
        ipc_frame(b"V", encoded(payload))

if __name__ == "__main__":
    main()
