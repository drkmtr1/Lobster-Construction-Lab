# D109 verification evidence

The [proof](../../../research/ORDINARY_53_2_FREE_REVERSAL.md) excludes ordinary graceful supply on the exact [frozen D108 original](../LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json) at physical labels `s:0=0`, `s:1=14`, `b:1:0=1` with exactly one signed difference −1 at any left terminal. The result is scoped to magnitude one, one reversal and the three pins. The graph digest is `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8`.

The [result](result.json) independently reconstructs the full original incidence multiset, traversal classes, physical spine and degree identity. It records three cases and all four surviving scalar rows. Each row forces a repeated difference between a right-terminal edge and a distinct left attachment, with either right-terminal index allowed. D107 and D108 remain accepted at their own scopes.

The unchanged checker accepted the retained D106 positive. All four declared controls on D106 gave the intended results. The wrong digest and cross-center swap failed ordinary verification. The within-center swap was graceful and passed the relaxed signed gate. The complement was graceful but failed both the pin test and the separately evaluated signed test. Its actual pins are (14,0,13) in the order entrance, exit and right center. Its negative differences are −14 through −2, the negatives of the 13 positive edges of the retained witness.

The [parse-only preflight](preflight_receipt.json) checked 165 frozen repository inputs, unique definitions and the project-local runtime with no task-module imports or bytecode. The [official invocation](command_receipt.json) used one worker, 0.125 process-CPU seconds, 0.12857380002969876 in-process wall seconds and 0.5707804 supervised wall seconds. It created zero originals and zero certificates. All solver, search, assignment enumeration, additional profile, join, replay, retry and restart counts were zero.

See the [contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). Historical original and recovery records remain preserved.

## Reproduction under separate authorization

Use project-local Python at the project root in a disposable checkout with vacant outputs and a 60-second external supervisor.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_53_2_FREE_REVERSAL_001/preflight.py 896e42c95ff32699955400583a7a5c038c57d37faaa229ece96d7d5350e95114
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_53_2_FREE_REVERSAL_001/run.py
```
