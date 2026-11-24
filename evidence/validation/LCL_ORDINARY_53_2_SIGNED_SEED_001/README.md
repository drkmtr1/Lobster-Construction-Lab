# D108 verification evidence

The [proof](../../../research/ORDINARY_53_2_SIGNED_SEED.md) excludes the prescribed ordinary signed seed on exact ordered `[[5,3],[2]]`. The [target original](original.json) has graph digest `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8` and differs from the D105 original by precisely the named fifth terminal `l:0:0:4` and its edge to `b:0:0`. The obstruction is for physical `s:0=0`, `s:1=14`, `b:1:0=1` and the sole negative signed difference −1 on `l:0:0:3 → b:0:0` from the class of `s:0`. It leaves ordinary gracefulness under other constraints undecided.

The [result](result.json) records two structural cases with three surviving scalar center rows in total. The independent audit derives the signed degree coefficients from actual incidences and checks the label-13 split and inequalities, then verifies the repeated-weight witnesses. The witness right-terminal edge is specified by its required label and actual center. The proof allows either terminal index.

The [parse-only preflight](preflight_receipt.json) passed with 150 repository input pins, no task imports and no bytecode. The [single official invocation](command_receipt.json) used one worker, 0.1875 process-CPU seconds, 0.22529929998563603 in-process wall seconds and 0.6538175 outer supervised wall seconds. It created one original and no certificate. The D106 retained positive passed on its own original. All three probes were genuine checker or signed-interface checks on the D106 original. The wrong digest and cross-center swap failed ordinary verification. The within-center swap remained ordinarily graceful and failed the exact named signed-interface gate. There were zero solvers, assignment enumeration, search states or nodes, other profiles, joins, retries, restarts or historical replays.

See the [contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). The D107 theorem and historical evidence retain their scopes.

## Reproduction under separate authorization

Use project-local Python at the project root in a disposable checkout with vacant output paths. Supervise the official invocation with a 60-second outer deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/preflight.py 5922c299ce7a778f30bf5e84ecabcabbe114a1d4f8888d06810f01f02b5cf98f
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/run.py
```
