# Dependency and platform research

**Checked:** 2026-11-21 UTC / 2026-11-20 Pacific/Honolulu.  
**Decision:** keep the core standard-library-only. Make NetworkX, SymPy and Z3 optional, with real imports only in the code paths that use them. CP-SAT is a researched alternative, not an initial requirement. Sources are listed in [SOURCES.md](SOURCES.md).

## 1. Python and Windows

The release supports 64-bit CPython 3.12 and 3.13; `pyproject.toml` declares `>=3.12,<3.14`, and the setup script enforces those two interpreter versions. The build host used for this work reports CPython 3.12.14 on Linux. Both release interpreter versions fit the selected optional package metadata. Existing Windows Python 3.13.5 does not need to be replaced with 3.12 solely for this project. Actual tests performed by this build are recorded separately in the verification report; metadata compatibility must not be reported as an executed Windows test.

Use a normal 64-bit CPython installation. The official [Python 3.13 Windows guide](https://docs.python.org/3.13/using/windows.html) describes the full installer for development. The [3.13.5 release page](https://www.python.org/downloads/release/python-3135/) includes a Windows installer (64-bit). That page is a reference for the known version, not a recommendation to downgrade or a statement that it is the latest release. [D05, D06]

When the Windows launcher is available, create an isolated environment from the intended interpreter:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import struct; print(8 * struct.calcsize('P'))"
```

The last command should report `64`. Substitute `-3.12` only if that is the installed interpreter you intend to use. Directly invoking the environment's Python avoids activation-policy requirements. Use the package's startup instructions for core commands and its explicit optional requirements when you choose to install adapters.

## 2. Selected package observations

| Package | Selected observed version | Primary compatibility evidence | Project role |
|---|---|---|---|
| NetworkX | `3.7` | PyPI requires `!=3.14.1, >=3.12`; universal `py3-none-any` wheel; official guide lists 3.12/3.13/3.14 | Optional structural checks and graph comparison; no default scientific-stack extra |
| SymPy | `1.14.0` | Stable PyPI page requires `>=3.9`; universal `py3-none-any` wheel | Optional exact symbolic identities and assumption-aware arithmetic |
| z3-solver | `5.4.1.0` | Current PyPI release has `py3-none-win_amd64` wheel | Optional finite integer constraint solver, imported as `z3` |
| OR-Tools | `9.15.6755` | PyPI requires `>=3.9`; explicit `cp312-cp312-win_amd64` and `cp313-cp313-win_amd64` wheels | Deferred CP-SAT comparison if justified |

These are directly inspected release and wheel facts, not promises about future versions. Z3's current page did not expose a `Requires-Python` field in the retrieved text; its wheel tag is the evidence used here. No Python lower bound is invented for it. [D01–D04]

NetworkX 3.7 does not support Python 3.11. The release's 3.12/3.13 target avoids that mismatch. Supporting another interpreter would be an explicit future portability change, with dependency and setup validation; do not silently select an untested fallback. Core operations continue to work without NetworkX.

The NetworkX installation guide states that the base package is pure Python with no hard dependencies; drawing, spectral and other extras use additional scientific libraries. This project does not need `networkx[default]` for its initial graph routines. Avoid bringing in NumPy/SciPy/Matplotlib merely because the optional extra exists. [D01]

Use the stable SymPy release selected above. The discovery search surfaced later release candidates, but a prerelease is unnecessary for exact integer identities and does not increase the mathematical strength of an argument. [D02, E06, E07]

## 3. What dependency pins do and do not establish

Top-level version pins make the intended adapter versions reviewable. They do not lock every transitive dependency, guarantee the same native runtime on all platforms, or certify algorithmic correctness. A package installation should record the actual Python/platform, resolved versions, and a small adapter check when that adapter is used. If offline reproduction is required later, generate a platform-specific wheel set and hashes in an authorized online environment; no such wheel archive is claimed in this build.

No network installation was needed for the mathematical research. Any optional modules already present in the build host must be distinguished from the selected future-install versions. An adapter tested with one present version does not establish runtime testing of another selected version.

The independent certificate checker must not depend on NetworkX, SymPy, Z3 or OR-Tools. A missing optional package should produce a clear unavailable-dependency result or instruction, not a fabricated mathematical answer and not an import failure for unrelated core commands.

## 4. Why the dependency list stays small

The core algorithms use integer arithmetic, sets/bit masks, dictionaries, recursion or explicit stacks, JSON, hashing, and deterministic iteration. These facilities suffice for the retained formulas, R226 extraction, bounded exact DFS, resource-aware frontier DP, and independent verification.

NetworkX adds convenient structural inspection. SymPy adds exact manipulation of candidate parameter formulas. Z3 adds an independently implemented finite constraint engine. Each has a concrete mathematical job. CP-SAT could add a different engine, but the initial project already has three independent routes to a finite witness or check; adding it now would broaden maintenance before resolving a demonstrated bottleneck. [E02–E04, E06, E09]

SageMath, GPU frameworks, neural training libraries, general-purpose agent platforms and a proof assistant are not first-run dependencies. They can be added when a precise research duty needs them. More installed mathematics software does not establish independent state supply, compatibility or an infinite proof.

## 5. Adapter acceptance and upgrades

An agent proposing a dependency update should identify the needed API or bug fix, check the official release/platform metadata, run the affected bounded examples, and preserve an independently verified witness. If solver output semantics change, update the status mapping explicitly. Unknown, timeout, unsupported domain and invalid model must remain distinguishable from exhaustive infeasibility.

Test a Windows interpreter directly before describing that platform as tested. Retain the standard-library path so the project remains useful even when an optional wheel cannot be installed. Record any exact-version mismatch in the verification report instead of silently describing a nearby version as the selected one.
