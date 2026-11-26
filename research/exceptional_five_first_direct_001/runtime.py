
"""Bounded I/O, identity and meter for the future one-worker D174 run."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import time
import tracemalloc
import types


ROOT = Path(__file__).absolute().parents[2]
KIT = Path(__file__).absolute().parent
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_FIRST_DIRECT_PLACEMENT_MATCHED_001_PREP"


class Limit(RuntimeError):
    pass


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))+"\n").encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path):
    for part in reversed((path, *path.parents)):
        if os.path.lexists(part) and (part.is_symlink() or getattr(part.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError(f"nonordinary path: {part}")
    return path


def repo_path(value):
    rel = PurePosixPath(value)
    if (rel.is_absolute() or rel.as_posix() != value or not rel.parts
            or any(p == ".." or ":" in p or "\\" in p for p in rel.parts)):
        raise ValueError("invalid repository path")
    return ordinary(ROOT.joinpath(*rel.parts))


def read(path):
    return json.loads(ordinary(path).read_bytes())


def file_binding(path):
    path = ordinary(path)
    data = path.read_bytes()
    if path.suffix == ".md":
        data = data.replace(b"\r\n", b"\n")
    return {"bytes":len(data), "sha256":sha(data)}


def load_source(name, path):
    if name in sys.modules:
        raise ValueError("duplicate module")
    path = ordinary(path)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def check_runtime(config, base_process):
    rt = config["runtime"]
    exe = repo_path(rt["venv"])
    base = ordinary(Path(sys._base_executable).absolute())
    files = {"venv":exe, "cfg":repo_path(rt["cfg"]), "base":base, "dll":ordinary(base.with_name(rt["dll"]))}
    expected = base if base_process else exe
    if (ordinary(Path(sys.executable).absolute()) != expected
            or sys.version.split()[0] != rt["version"]
            or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
                    and sys.flags.optimize == 0)
            or {key:sha(p.read_bytes()) for key,p in files.items()} != rt["sha256"]):
        raise ValueError("pinned runtime, executable or flags mismatch")


def write_new(path, value, allowed):
    data = encoded(value)
    if len(data) > allowed:
        raise Limit(f"{path.name}: record or aggregate byte ceiling")
    temp = path.with_name(path.name+".partial")
    if os.path.lexists(path):
        raise ValueError(f"record already exists: {path.name}")
    with ordinary(temp).open("xb") as file:
        count = file.write(data)
        if count != len(data):
            raise OSError("short evidence write")
        file.flush()
        os.fsync(file.fileno())
    temp.rename(path)
    return len(data)


class Meter:
    def __init__(self, config, output, charged_bytes, deadline):
        self.limits = config["limits"]
        self.reserve = config["reserve"]
        self.output = output
        self.deadline = deadline
        self.bytes = charged_bytes
        self.counts = dict.fromkeys(("targets", "dispositions", "numerical_dispositions",
                                     "exterior_nodes", "transfer_states", "transitions"),0)
        self.by_phase = {}
        self.arm_start_counts = dict(self.counts)
        self.pending_event = None
        self.poll = 0
        self.phase = "startup"
        self.frames = []
        self.candidate = None
        self.peak_candidate_states = 0

    def time_check(self):
        cpu_ceiling = self.limits["cpu_seconds"]-self.reserve["preparation_startup_cpu_seconds"]
        if time.process_time() >= cpu_ceiling:
            raise Limit("worker process CPU ceiling")
        if time.monotonic() >= self.deadline:
            raise Limit("worker monotonic deadline")
        if tracemalloc.get_traced_memory()[1] > self.limits["traced_worker_bytes"]:
            raise Limit("peak traced Python allocation ceiling")

    def tick(self, name):
        self.pending_event = name
        if self.counts[name] >= self.limits[name]:
            raise Limit(f"{name} ceiling")
        self.poll += 1
        if self.poll % 64 == 0:
            self.time_check()
        self.counts[name] += 1
        phase = self.by_phase.setdefault(self.phase, {})
        phase[name] = phase.get(name,0)+1
        self.pending_event = None

    def memory(self, states):
        self.peak_candidate_states = max(states,self.peak_candidate_states)
        if states > self.limits["live_candidate_states"]:
            raise Limit("per-candidate retained state ceiling")

    def write(self, name, value):
        self.phase = "evidence write"
        self.pending_event = name
        self.time_check()
        allowance = self.limits["evidence_bytes"]-self.bytes-self.reserve["final_records_bytes"]
        self.bytes += write_new(self.output/name,value,min(allowance,self.limits["record_bytes"]))
        self.pending_event = None

    def interruption(self):
        return {"phase":self.phase, "candidate":self.candidate, "recursion":self.frames,
                "pending_event":self.pending_event, "counts":self.counts, "counts_by_phase":self.by_phase,
                "arm_start_counts":self.arm_start_counts,
                "peak_candidate_states":self.peak_candidate_states}
