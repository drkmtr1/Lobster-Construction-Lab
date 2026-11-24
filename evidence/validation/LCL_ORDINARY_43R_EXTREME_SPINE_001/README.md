# D107 verification evidence

The [symbolic proof](../../../research/ORDINARY_43R_EXTREME_SPINE.md) establishes the indexed ordinary graceful supplier on ordered `[[4,3],[r]]` for every exact integer r≥2. It uses D105 as the base and the exact D106 transition as its induction step. The spine has physical labels (0,r+11). The sole negative signed edge remains −1 at `l:0:0:3 → b:0:0`, and signed degree sum is (r+11)(r+12)/2−2.

The [independent audit](result.json) rechecks only the frozen r=2 D105 and r=3 D106 originals and certificates. It binds their raw original hashes, exact named graph digests and retained ledger IDs. It verifies both archived labelings pointwise against the formula, all original difference groups and signed incidences, and the archived one-step topology and weight delta. The proof supplies the general result.

The [preflight](preflight_receipt.json) checked 136 frozen repository input hashes, unique intended definitions and the project-local runtime. It imported no task modules and left no bytecode. The single [official invocation](command_receipt.json) used one worker, 0.203125 process-CPU seconds, 0.20265649998327717 in-process wall seconds and 0.6296432 outer supervised wall seconds. Both retained positives passed the unchanged checker. Three probes on the D106 original rejected the wrong digest, rejected the cross-center swap because it repeats weights 6 and 7 and omits 5 and 8, and rejected the within-center swap at the exact signed-interface gate after it passed ordinary gracefulness. The within-center swap moves the −1 to `l:0:0:0 → b:0:0`.

No extra profiles, graph identities, certificates, solver calls, complete-assignment visits, search states or nodes, joins, retries, restarts or historical replays occurred. See the [contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json).

## Reproduction under separate authorization

Use the pinned project-local Python at the project root in a disposable checkout with vacant outputs. Supervise the official invocation with a 60-second outer deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_43R_EXTREME_SPINE_001/preflight.py 1cb00e967d66adac6cd00ca36719c2080836e64debdb640cb52aba68a043bba6
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_43R_EXTREME_SPINE_001/run.py
```
