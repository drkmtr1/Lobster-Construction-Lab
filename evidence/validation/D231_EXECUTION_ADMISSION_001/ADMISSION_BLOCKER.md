# D231 — Scientific execution blocked at fresh admission

**BLOCKED_AT_ADMISSION_NO_EXECUTION.** The single Owner-authorized invocation remained unstarted. Fresh admission failed on pre-existing bytecode for the frozen driver's shared import dependencies. No source, cache or environment was changed to clear the gate.

## Authorization and checks

- Approved preparation checkpoint `ba91a5873470256d889a171132817959054c98cc`, immediately after D230 acceptance `0f0bbbe9c19bbdbf8274096806f0f3e7ae662d4f`.
- Separate D231 Director acceptance and intended execution checkout `a6c4843c49c7c0327f3866f7c662f43267ee8934`, the direct child of the approved preparation and synchronized to LCL main before fresh admission. Only STATE, FINDINGS and DECISIONS changed.
- Sole authorized scientific run `d231-unequal-pair-return-kernel-001`. Source-manifest SHA-256 `ca2f6a00371c834e8c4c41c2a5aaf89270bd9dff042c6e0aefd10e8a6492ad41`. Registration SHA-256 `298114c1d88e2da7ef7fc35fc72e97e7aabfddac059912d1f5af726ccb0a06f0`.
- Exact committed-blob identity across preparation and acceptance plus fresh raw-byte identity matched for all 26 manifest bindings. The frozen parse-only preflight and protected checker source matched. Checker SHA-256 `230b852035a49eb2973a42730f31a5b94c733a92886dcc9158b50c3e94649909`.
- Live LCL and both pinned upstream main refs matched. Baseline tag object `fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d` and peel `36ea1603602491bf3c1c5b81ed4c23aaa2210e70` matched locally and remotely. MDL pin `858a8c1fcfda87ba40bb1adee498a6131504a803` and Bounded Search pin `e48b94eec4091b4fe189e325cab2eda464409943` both matched. One clean LCL worktree was observed at admission.
- A quoting error in a read-only Git blob lookup was corrected by separate direct lookups against the two exact commits. The actual source checks passed. The independent filesystem cache check then produced the admission blocker.

## Exact blocker

The driver imports `lcl.records` before creating its registered run directory. That import closure includes the seven bound modules below. The cache directory contains 16 entries, of which these seven concern the task. The D231 and retained D229 numerical package directories themselves have no bytecode. The bound shared cache objects were read as bytes for identification only. The independent evidence reviewer checked that the seven inspected cache headers have timestamp-based flags zero and source timestamps and sizes matching the present sources.

The approved interpreter flag `-B` inhibits bytecode writes. CPython's source loader can still read an existing valid cache. This distinction was checked against the local CPython standard library's `importlib/_bootstrap_external.py`: `get_code` tries reading cached data before the write guard on `sys.dont_write_bytecode`. The Director-approved no-task-bytecode admission condition therefore fails for the actual frozen import closure.

| Existing cache | Bytes | Last write UTC | SHA-256 |
|---|---:|---|---|
| `lcl/__pycache__/__init__.cpython-313.pyc` | 254 | 2026-11-21T06:25:49.9904096Z | `13ed31177a86852324cc6cbee78bd71383f0d49fe83798702ff80e4170d4342d` |
| `lcl/__pycache__/budget.cpython-313.pyc` | 4013 | 2026-11-21T06:25:50.1086002Z | `9783b521b3dc11f27a96c93c586cc652324a039145ab4a8e6d690f51af91a8b1` |
| `lcl/__pycache__/engines.cpython-313.pyc` | 7774 | 2026-11-21T06:25:50.1376233Z | `b9fb6220dccd1c2a96ae921bc864a75a23abf77f2c0a14bdddf216172bba737a` |
| `lcl/__pycache__/model.cpython-313.pyc` | 16628 | 2026-11-21T06:25:50.0920805Z | `8e24f96596e0646845acccc3fdedc756ab98751345ac7952a3bca6e14464ced3` |
| `lcl/__pycache__/records.cpython-313.pyc` | 12380 | 2026-11-21T06:25:50.1961473Z | `3d4b3a4256cd00e16b7f5af43bf602ded17acccdaf3238256261f5270fe994aa` |
| `lcl/__pycache__/search.cpython-313.pyc` | 7016 | 2026-11-21T06:25:50.1356199Z | `752e10deb6fbd490f6554ad5a9cd47d21c439f187d0f56111b58f1328169dc90` |
| `lcl/__pycache__/verify.cpython-313.pyc` | 20204 | 2026-11-21T06:25:50.2196685Z | `261e53265b9d37fb94e07e151c8581d13cfeec2021a266a498d365cdf127fc84` |

This finding concerns runtime admission. The frozen checker **source** still matches its binding. No cached project module was loaded during the admission attempt, and the protected checker function was never invoked.

## Scientific and evidence disposition

Admission stopped before the fresh runtime probe, final process check, receipt creation or any launcher or worker invocation. No actual receipt, receipt hash, executed command, scientific exit code, foreground measurement, CPU measurement, primary or audit charge, or scientific record exists. The read-only review of the proposed foreground wrapper passed before launch. The local ignored review copy is `runs/d231-unequal-pair-return-kernel-001-foreground.py`, SHA-256 `de53812bdf445761198b03ed9336ca7b497337eb6706b2649a3b16d697342b7e`. It was never run. There is no supervision observation from a scientific process.

Both `runs/d231-unequal-pair-return-kernel-001` and `evidence/runs/d231-unequal-pair-return-kernel-001` remained vacant. There was no completed or interrupted scientific evidence to archive or hash. The registered scientific archive stays absent. This validation note preserves the blocker independently of the registered scientific output.

| Scope | Result |
|---|---:|
| Scientific invocations | 0 |
| Covered residual aggregates | 0 |
| Architecture-excluded aggregates | 0 |
| Unresolved residual aggregates | 29 |
| Attempted numerical placements | 0 |
| Unvisited numerical placements | 322 |
| Independent positive certificates or exhaustion reports to audit | 0 |

The accepted 136 symbolic normalized positives and the independent insertion theorem for maximum at least 19 retain their exact scopes. The unrestricted four-quota positive-odd returning S2 theorem has no scientific instantiation from this admission attempt. The former D230 comparison remains symbolically superseded, never prepared and never executed. [Preparation](../D231_INDEPENDENT_COORDINATE_INSERTION_SUPPLIER/PREPARATION.md) · [Separate blocker reviews](SEPARATE_REVIEWS.md)
