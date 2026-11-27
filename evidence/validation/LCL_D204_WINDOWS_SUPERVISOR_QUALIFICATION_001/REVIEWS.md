# Independent supervisor qualification reviews

Disposition **WINDOWS_SUPERVISOR_QUALIFICATION_BLOCKED**. Reviewed source freeze SHA-256 `02556d7c959ca387e42d957e31791e9e17809925cf437974ea1f35e8f0ef8d3f`. The read-only reviews were sequential. No native qualification probe or scientific work ran.

## Pre-launch implementation review

**BLOCK.** The independent reviewer inspected the AMD64 ctypes layouts, Windows Job and process creation attributes, inherited pipe restrictions, handle lifetimes, configured native protections, suspend-time membership checks, timers, IPC, writes, and reconciliation. The frozen code contains the intended control mechanisms but has three launch blockers.

- Emergency waits budget 24 seconds for the companion and up to 10 further seconds in cleanup. Cleanup failure can reach an unbounded implicit `Popen.wait()` in the installed Python. The outer deadlines are not a single bounded stop.
- The internal Job-owner command can accept an unused probe using only an existing run directory. It lacks a matrix-controlled one-shot admission.
- The raw candidate is synced before acknowledgement. The candidate receipt is held in memory until terminal output, so an interruption after acknowledgement can lose it.

The admission controller requires a passing review marker for this source digest. The retained rejection prevents both supervisor modes from reaching native launch. The intended one-shot behavior in the frozen implementation description is subject to the review's specific bypass finding. [Frozen review findings](PRELAUNCH_REVIEW.json) · [Microsoft process attributes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute) · [Microsoft Job termination action](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_end_of_job_time_information)

## Post-stop implementation review

**Confirmed block.** A separate reviewer checked the actual frozen supervisor and installed, hash-bound CPython subprocess source. The review reproduced the budget and implicit infinite-wait path, confirmed that exclusive per-probe directories do not enforce a live matrix permit, and confirmed that the durable receipt can lag acknowledgement. Both entry modes require the exact passing review value before loading the Win32 bindings. The recorded BLOCK therefore denies these modes without relying on any untested host behavior. Nested Job admission, native and sampled enforcement, and terminal cleanup were left unobserved.

## Post-stop evidence-custody review

**Pass for blocked evidence.** The independent custody reviewer recomputed all 63 frozen project bindings and all 2,628 installed runtime dependencies, including the three exact interpreter, launcher and DLL bindings. The reviewer recalculated 35 historical artifact bindings, 15 historical authority bindings and 27 scientific-source bindings. Local commit and parent refs, protected blobs, baseline tag and peel, and the byte-identical 6,675-byte prior approval passed. Live LCL and upstream continuity follow the separately recorded writer intake. The custody review did not independently query the live remotes.

The reviewer verified both run paths remain vacant, the eleven planned probes are NOT_STARTED with unavailable measurements recorded as null, task-bytecode absence, zero activity counters, all preserved limits and domain bindings, and the same sole next action in the state and handoff. The custody verifier measured 2.140625 seconds of its own process CPU in 10.898357 observed wall seconds. Those figures supplement the timed parse-only preflight. Complete aggregate preparation CPU remains unavailable. [Initial custody](INTAKE.json) · [Preflight](PRECHECK.json) · [Blocked outcome](RESULT.json)
