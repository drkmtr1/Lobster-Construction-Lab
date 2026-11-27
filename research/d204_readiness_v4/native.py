"""Checked x64 Win32 process, Job, capability and file bindings for D204."""
import ctypes as ct
from ctypes import wintypes as wt
from contextlib import contextmanager
import os
import subprocess

HANDLE, DWORD, BOOL = wt.HANDLE, wt.DWORD, wt.BOOL
SIZE, PTR, U64, I64 = ct.c_size_t, ct.c_void_p, ct.c_uint64, ct.c_int64
OUT = ct.byref
TICKS = 10_000_000
ERROR_BROKEN_PIPE = 109
ERROR_INSUFFICIENT_BUFFER = 122
WAIT_SIGNALED, WAIT_TIMEOUT = 0, 258
FLAGS = 0x0004 | 0x0008 | 0x2000  # Job user time, one active process, kill on close.
BASIC_ACCOUNTING, END_OF_JOB, EXTENDED_LIMIT = 1, 6, 9
TERMINATED_BY_SUPERVISOR = 0xE2040001
INVALID_HANDLE = PTR(-1).value

class Security(ct.Structure):
    _fields_ = [("length", DWORD), ("descriptor", PTR), ("inherit", BOOL)]

class Startup(ct.Structure):
    _fields_ = [
        ("length", DWORD), ("reserved", wt.LPWSTR), ("desktop", wt.LPWSTR),
        ("title", wt.LPWSTR), ("x", DWORD), ("y", DWORD), ("x_size", DWORD),
        ("y_size", DWORD), ("x_chars", DWORD), ("y_chars", DWORD), ("fill", DWORD),
        ("flags", DWORD), ("show", wt.WORD), ("reserved_bytes", wt.WORD),
        ("reserved_buffer", PTR), ("stdin", HANDLE), ("stdout", HANDLE), ("stderr", HANDLE),
    ]

class StartupEx(ct.Structure):
    _fields_ = [("startup", Startup), ("attributes", PTR)]

class ProcessInfo(ct.Structure):
    _fields_ = [("process", HANDLE), ("thread", HANDLE), ("pid", DWORD), ("tid", DWORD)]

class BasicLimit(ct.Structure):
    _fields_ = [
        ("process_user", I64), ("job_user", I64), ("flags", DWORD),
        ("min_working", SIZE), ("max_working", SIZE), ("active_limit", DWORD),
        ("affinity", SIZE), ("priority", DWORD), ("scheduling", DWORD),
    ]

class IOCounts(ct.Structure):
    _fields_ = [(name, U64) for name in (
        "read_operations", "write_operations", "other_operations",
        "read_bytes", "write_bytes", "other_bytes",
    )]

class ExtendedLimit(ct.Structure):
    _fields_ = [
        ("basic", BasicLimit), ("io", IOCounts), ("process_memory", SIZE),
        ("job_memory", SIZE), ("peak_process", SIZE), ("peak_job", SIZE),
    ]

class JobAccounting(ct.Structure):
    _fields_ = [
        ("user", I64), ("kernel", I64), ("period_user", I64), ("period_kernel", I64),
        ("faults", DWORD), ("lifetime", DWORD), ("active", DWORD), ("terminated", DWORD),
    ]

kernel = ct.WinDLL("kernel32.dll", use_last_error=True)

def api(name, output, *args):
    function = getattr(kernel, name)
    function.restype = output
    function.argtypes = args
    return function

Close = api("CloseHandle", BOOL, HANDLE)
CreateJob = api("CreateJobObjectW", HANDLE, PTR, wt.LPCWSTR)
SetJob = api("SetInformationJobObject", BOOL, HANDLE, ct.c_int, PTR, DWORD)
QueryJob = api("QueryInformationJobObject", BOOL, HANDLE, ct.c_int, PTR, DWORD, PTR)
InJob = api("IsProcessInJob", BOOL, HANDLE, HANDLE, PTR)
GetHandleInfo = api("GetHandleInformation", BOOL, HANDLE, PTR)
TerminateJob = api("TerminateJobObject", BOOL, HANDLE, wt.UINT)
TerminateProcess = api("TerminateProcess", BOOL, HANDLE, wt.UINT)
InitAttrs = api("InitializeProcThreadAttributeList", BOOL, PTR, DWORD, DWORD, PTR)
SetAttr = api("UpdateProcThreadAttribute", BOOL, PTR, DWORD, SIZE, PTR, SIZE, PTR, PTR)
FreeAttrs = api("DeleteProcThreadAttributeList", None, PTR)
CreatePipe = api("CreatePipe", BOOL, PTR, PTR, PTR, DWORD)
HandleInfo = api("SetHandleInformation", BOOL, HANDLE, DWORD, DWORD)
CreateProcess = api(
    "CreateProcessW", BOOL, wt.LPCWSTR, wt.LPWSTR, PTR, PTR, BOOL, DWORD,
    PTR, wt.LPCWSTR, PTR, PTR,
)
ResumeThread = api("ResumeThread", DWORD, HANDLE)
Wait = api("WaitForSingleObject", DWORD, HANDLE, DWORD)
Times = api("GetProcessTimes", BOOL, HANDLE, PTR, PTR, PTR, PTR)
ExitCode = api("GetExitCodeProcess", BOOL, HANDLE, PTR)
Image = api("QueryFullProcessImageNameW", BOOL, HANDLE, DWORD, wt.LPWSTR, PTR)
OpenProcess = api("OpenProcess", HANDLE, DWORD, BOOL, DWORD)
CurrentProcess = api("GetCurrentProcess", HANDLE)
Tick = api("GetTickCount64", U64)
ReadFile = api("ReadFile", BOOL, HANDLE, PTR, DWORD, PTR, PTR)
WriteFile = api("WriteFile", BOOL, HANDLE, PTR, DWORD, PTR, PTR)
OpenFile = api("CreateFileW", HANDLE, wt.LPCWSTR, DWORD, DWORD, PTR, DWORD, DWORD, HANDLE)

def check(result):
    if not result:
        raise ct.WinError(ct.get_last_error())
    return result

class Owned:
    def __init__(self, handle):
        self.handle = check(handle)

    def close(self):
        if self.handle is not None:
            check(Close(self.handle))
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, *exception):
        self.close()

def pin(path):
    handle = OpenFile(str(path), 0x80000000, 1, None, 3, 0x00200000, None)
    if handle == INVALID_HANDLE:
        raise ct.WinError(ct.get_last_error())
    return Owned(handle)

def in_job(process, job=None):
    result = BOOL()
    check(InJob(process, job, OUT(result)))
    return bool(result.value)

def wait(handle, milliseconds):
    result = Wait(handle, milliseconds)
    if result == WAIT_SIGNALED:
        return True
    if result == WAIT_TIMEOUT:
        return False
    raise ct.WinError(ct.get_last_error())

def sample(process):
    born, end, kernel_time, user_time = (wt.FILETIME() for _ in range(4))
    check(Times(process, OUT(born), OUT(end), OUT(kernel_time), OUT(user_time)))
    def ticks(value):
        return (value.dwHighDateTime << 32) | value.dwLowDateTime
    return dict(born=ticks(born), end=ticks(end), user=ticks(user_time), kernel=ticks(kernel_time))

def exit_code(process):
    result = DWORD()
    check(ExitCode(process, OUT(result)))
    return result.value

def image(process):
    text = ct.create_unicode_buffer(32768)
    size = DWORD(len(text))
    check(Image(process, 0, text, OUT(size)))
    return text.value

def job_info(job, kind, structure):
    result = structure()
    check(QueryJob(job, kind, OUT(result), ct.sizeof(result), None))
    return result

def accounting(job):
    value = job_info(job, BASIC_ACCOUNTING, JobAccounting)
    return {name: getattr(value, name) for name, _ in JobAccounting._fields_}

def limits(job):
    basic = job_info(job, EXTENDED_LIMIT, ExtendedLimit).basic
    action = job_info(job, END_OF_JOB, DWORD)
    flags = DWORD()
    check(GetHandleInfo(job, OUT(flags)))
    return dict(native_user_ticks=basic.job_user, flags=basic.flags,
                active_limit=basic.active_limit, end_action=action.value,
                job_handle_inheritable=bool(flags.value & 1))

def configure(job, native_user_ticks):
    info = ExtendedLimit()
    info.basic.job_user = native_user_ticks
    info.basic.flags = FLAGS
    info.basic.active_limit = 1
    check(SetJob(job, EXTENDED_LIMIT, OUT(info), ct.sizeof(info)))
    action = DWORD(0)
    check(SetJob(job, END_OF_JOB, OUT(action), ct.sizeof(action)))


def read(handle, length):
    buffer, num = ct.create_string_buffer(length), DWORD()
    if not ReadFile(handle, buffer, length, OUT(num), None):
        if ct.get_last_error() == ERROR_BROKEN_PIPE:
            return b""
        raise ct.WinError(ct.get_last_error())
    return buffer.raw[:num.value]

def write(handle, data):
    num = DWORD()
    check(WriteFile(handle, data, len(data), OUT(num), None))
    if num.value != len(data):
        raise RuntimeError("short native write")

def verify_layout():
    sizes = (ct.sizeof(HANDLE), ct.sizeof(Security), ct.sizeof(Startup),
             ct.sizeof(StartupEx), ct.sizeof(ProcessInfo), ct.sizeof(BasicLimit),
             ct.sizeof(ExtendedLimit), ct.sizeof(JobAccounting))
    if sizes != (8, 24, 104, 112, 24, 64, 144, 48):
        raise RuntimeError(f"unexpected Win32 layouts {sizes}")
    offsets = (Startup.stdin.offset, StartupEx.attributes.offset,
               BasicLimit.active_limit.offset, ExtendedLimit.io.offset)
    if offsets != (80, 104, 40, 64):
        raise RuntimeError(f"unexpected Win32 field offsets {offsets}")
    return dict(sizes=sizes, offsets=offsets)


CreateEvent = api("CreateEventW", HANDLE, PTR, BOOL, BOOL, wt.LPCWSTR)
SetEvent = api("SetEvent", BOOL, HANDLE)
Duplicate = api("DuplicateHandle", BOOL, HANDLE, HANDLE, HANDLE, PTR, DWORD, BOOL, DWORD)
OpenThread = api("OpenThread", HANDLE, DWORD, BOOL, DWORD)
CurrentThread = api("GetCurrentThread", HANDLE)
CancelSync = api("CancelSynchronousIo", BOOL, HANDLE)
FileName = api("GetFinalPathNameByHandleW", DWORD, HANDLE, wt.LPWSTR, DWORD, DWORD)
FileInfo = api("GetFileInformationByHandleEx", BOOL, HANDLE, ct.c_int, PTR, DWORD)
TICKS_MS = TICKS // 1000

def duplicate(stack, handle, access, inherit):
    current = CurrentProcess()
    result = HANDLE()
    check(Duplicate(current, handle, current, OUT(result), access, inherit, 0))
    return stack.enter_context(Owned(result.value))

def events(stack):
    parent = tuple(stack.enter_context(Owned(CreateEvent(None, False, False, None)))
                   for _ in range(2))
    leased = tuple(duplicate(stack, event.handle, 0x00100000, True) for event in parent)
    return parent, leased

@contextmanager
def attributes(job, handles):
    count = 2 if job else 1
    size = SIZE()
    ct.set_last_error(0)
    if InitAttrs(None, count, 0, OUT(size)) or ct.get_last_error() != ERROR_INSUFFICIENT_BUFFER:
        raise RuntimeError("unexpected process attribute sizing result")
    if not 0 < size.value <= 65536:
        raise RuntimeError("invalid process attribute allocation size")
    buffer = ct.create_string_buffer(size.value)
    check(InitAttrs(buffer, count, 0, OUT(size)))
    try:
        jobs = (HANDLE * 1)(job)
        listed = (HANDLE * len(handles))(*handles)
        if job:
            check(SetAttr(buffer, 0, 0x0002000D, jobs, ct.sizeof(jobs), None, None))
        check(SetAttr(buffer, 0, 0x00020002, listed, ct.sizeof(listed), None, None))
        yield ct.cast(buffer, PTR)
    finally:
        FreeAttrs(buffer)

def pipe(stack):
    source, sink = HANDLE(), HANDLE()
    sa = Security(ct.sizeof(Security), None, True)
    check(CreatePipe(OUT(source), OUT(sink), OUT(sa), 4096))
    return tuple(stack.enter_context(Owned(h.value)) for h in (source, sink))

def configure_startup(stack, job, exe, cwd, script, args, launch):
    parent_events, child_events = events(stack)
    source, sink = pipe(stack)
    no_input, drop = pipe(stack)
    drop.close()
    check(HandleInfo(source.handle, 1, 0))
    launch.update(source=source, gates=parent_events)
    info = ProcessInfo()
    child = [event.handle for event in child_events]
    command = ct.create_unicode_buffer(subprocess.list2cmdline([
        str(exe), "-I", "-S", "-B", str(script), *args, *(str(h) for h in child),
    ]))
    with attributes(job, [no_input.handle, sink.handle, *child]) as attrs:
        startup = StartupEx()
        startup.startup.length = ct.sizeof(startup)
        startup.startup.flags = 0x100
        startup.startup.stdin = no_input.handle
        startup.startup.stdout = startup.startup.stderr = sink.handle
        startup.attributes = attrs
        system_root = os.environ["SystemRoot"]
        env = ct.create_unicode_buffer(f"SystemRoot={system_root}\0WINDIR={system_root}\0\0")
        result = CreateProcess(str(exe), command, None, None, True, 0x08080404,
                               env, str(cwd), OUT(startup), OUT(info))
        error = ct.get_last_error()
        for name in ("process", "thread"):
            handle = getattr(info, name)
            if handle:
                launch[name] = stack.enter_context(Owned(handle))
        launch["pid"] = info.pid
        if not result:
            raise ct.WinError(error)
    for handle in (no_input, sink, *child_events):
        handle.close()


CreatePort = api("CreateIoCompletionPort", HANDLE, HANDLE, HANDLE, SIZE, DWORD)
GetQueued = api("GetQueuedCompletionStatus", BOOL, HANDLE, PTR, PTR, PTR, DWORD)

class CompletionAssociation(ct.Structure):
    _fields_ = [("key", PTR), ("port", HANDLE)]

class ProcessIdList(ct.Structure):
    _fields_ = [("assigned", DWORD), ("listed", DWORD), ("ids", SIZE * 16)]

def attach_job_port(stack, job):
    handle = stack.enter_context(Owned(CreatePort(INVALID_HANDLE, None, 0, 1)))
    association = CompletionAssociation(job, handle.handle)
    check(SetJob(job, 7, OUT(association), ct.sizeof(association)))
    return handle

def job_event(port, key):
    number, actual_key, parameter = DWORD(), SIZE(), PTR()
    result = GetQueued(port, OUT(number), OUT(actual_key), OUT(parameter), 0)
    if not result:
        code = ct.get_last_error()
        if code == WAIT_TIMEOUT and parameter.value is None:
            return None
        raise ct.WinError(code)
    if actual_key.value != key:
        raise RuntimeError("unexpected Job completion key")
    return {"message": number.value, "parameter": parameter.value, "tick": Tick()}

def job_pids(job):
    value = job_info(job, 3, ProcessIdList)
    if value.listed > len(value.ids):
        raise RuntimeError("unbounded Job PID list")
    return {"reported_assigned": value.assigned, "pids": list(value.ids[:value.listed])}

class FileTag(ct.Structure):
    _fields_ = [("attributes", DWORD), ("tag", DWORD)]

def locked_file(stack, path, directory=False):
    attrs = 0x00200000 | (0x02000000 if directory else 0)
    handle = OpenFile(str(path), 0x80000000, 1, None, 3, attrs, None)
    if handle == INVALID_HANDLE:
        raise ct.WinError(ct.get_last_error())
    held = stack.enter_context(Owned(handle))
    tag = FileTag()
    check(FileInfo(handle, 9, OUT(tag), ct.sizeof(tag)))
    if tag.attributes & 0x400 or bool(tag.attributes & 0x10) != directory:
        raise RuntimeError("reparse or mismatched file type: " + path.name)
    name = ct.create_unicode_buffer(32768)
    length = FileName(handle, name, len(name), 0)
    if not 0 < length < len(name) or name.value.casefold() != ("\\\\?\\" + str(path)).casefold():
        raise RuntimeError("different opened object: " + path.name)
    return held

def locked_bytes(stack, path, maximum):
    held = locked_file(stack, path)
    data = bytearray()
    while True:
        block = read(held.handle, min(1 << 20, maximum + 1 - len(data)))
        if not block:
            return bytes(data)
        data.extend(block)
        if len(data) > maximum:
            raise RuntimeError("bound file exceeds byte limit: " + path.name)

def stop_worker(job, proc):
    errors = []
    if job and not TerminateJob(job, TERMINATED_BY_SUPERVISOR):
        errors.append(("TerminateJobObject", ct.get_last_error()))
    if proc and not wait(proc, 0) and (not job or errors):
        if not TerminateProcess(proc, TERMINATED_BY_SUPERVISOR):
            errors.append(("TerminateProcess", ct.get_last_error()))
    return errors

def thread_lease():
    value = HANDLE()
    current = CurrentProcess()
    check(Duplicate(current, CurrentThread(), current, OUT(value), 1, False, 0))
    return Owned(value.value)

def cancel_thread(handle):
    if not CancelSync(handle):
        error = ct.get_last_error()
        if error != 1168:  # ERROR_NOT_FOUND: no pending synchronous I/O
            raise ct.WinError(error)
