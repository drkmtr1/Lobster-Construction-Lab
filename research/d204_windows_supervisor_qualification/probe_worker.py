"""Fixed inert workloads. The only subprocess request is the child-refusal fixture."""
import sys

WORKLOADS = frozenset({
    "natural", "native_cpu", "combined_cpu", "elapsed", "observer_gap",
    "child_refusal", "interruption", "candidate", "oversized", "incomplete", "byte_cap",
})

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in WORKLOADS:
        raise SystemExit(64)
    if (sys.platform != "win32" or sys.version_info[:3] != (3, 13, 17)
            or not sys.flags.isolated or not sys.flags.no_site or not sys.dont_write_bytecode):
        raise SystemExit(65)
    # Win32 CPython searches its own ZIP, DLLs, Lib and installation root in isolated mode.
    exe = sys.executable.replace("/", "\\")
    home = exe.rsplit("\\", 1)[0]
    approved = [home + "\\" + relative for relative in ("python313.zip", "DLLs", "Lib")]
    approved.append(home)
    if [part.casefold() for part in sys.path] != [part.casefold() for part in approved]:
        raise SystemExit(66)
    import ctypes
    import json
    import os
    import struct
    import subprocess
    import time
    from pathlib import Path
    mode = sys.argv[1]
    stream = sys.stdout.buffer
    def frame(tag, payload):
        stream.write(struct.pack(">I", 1 + len(payload)) + tag + payload)
        stream.flush()
    def report(tag, payload):
        frame(tag, json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    name = ctypes.WinDLL("kernel32.dll", use_last_error=True).GetModuleFileNameW
    name.argtypes = (ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_ulong)
    name.restype = ctypes.c_ulong
    buffer = ctypes.create_unicode_buffer(32768)
    if not 0 < name(sys.dllhandle, buffer, len(buffer)) < len(buffer):
        raise SystemExit(67)
    del name
    modules = {module_name: str(Path(location).resolve()) for module_name, module in sys.modules.items()
               if module_name != "__main__" and (location := getattr(module, "__file__", None))}
    # A childless Worker discloses its own fixed environment; the supervisor checks every path.
    report(b"H", dict(pid=os.getpid(), executable=exe, dll=buffer.value, sys_path=sys.path,
                      isolated=sys.flags.isolated, no_site=sys.flags.no_site,
                      bytecode_disabled=sys.dont_write_bytecode, modules=modules))
    if sys.stdin.buffer.read(1) != b"G":
        raise SystemExit(68)
    if mode in ("native_cpu", "combined_cpu"):
        limit = time.monotonic() + 8
        value = 1
        while time.monotonic() < limit:
            for _ in range(1000):
                value = (31 * value + 17) & 0xFFFFFFFF
        raise SystemExit(69)
    if mode in ("elapsed", "observer_gap", "interruption"):
        time.sleep(12)
        raise SystemExit(70)
    if mode == "child_refusal":
        try:
            child = subprocess.Popen([exe, "-I", "-S", "-B", "-c", "raise SystemExit(79)"],
                                     executable=exe, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                     cwd=home, close_fds=True, creationflags=0x08000000)
        except OSError as error:
            report(b"R", dict(child_created=False, winerror=error.winerror))
        else:
            pid = child.pid
            try:
                code = child.wait(timeout=1)
            except subprocess.TimeoutExpired:
                child.kill()
                code = child.wait(timeout=1)
            report(b"R", dict(child_created=True, child_pid=pid, child_exit=code))
            raise SystemExit(71)
        return
    if mode == "oversized":
        stream.write(struct.pack(">I", 16385))
        stream.flush()
        time.sleep(12)
        return
    if mode == "incomplete":
        stream.write(struct.pack(">I", 30) + b"Ctwo bytes")
        stream.flush()
        return
    if mode == "byte_cap":
        frame(b"C", b"B" * 10000)
        time.sleep(12)
        return
    if mode == "candidate":
        frame(b"C", b"inert synthetic payload, not a certificate\n")
        if sys.stdin.buffer.read(1) != b"A":
            raise SystemExit(72)
        report(b"V", dict(pid=os.getpid(), value=sum(value * value for value in range(20))))
        return
    report(b"R", dict(value=42))

if __name__ == "__main__":
    main()
