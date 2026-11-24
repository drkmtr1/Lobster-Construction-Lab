# D103 verification evidence

The [proof](../../../research/R241_43_2_ZERO_ENTRANCE.md) excludes cut-9 supply on frozen ordered `[[4,3],[2]]` with `s:0=0` and the exit free. The exact [D099 original](../LCL_R241_43_2_LOWER_BLOCK_001/original.json) is reused. Its graph digest is `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. No D103 labeling certificate was produced.

The [result](result.json) gives all 36 distinct ordered high triples containing 13 and their parity/range dispositions. The audit independently derives the signed degree coefficients from the original incidence multiset and confirms exactly seven survivors in that same domain. Each survivor records both residual palettes, the six fixed weights, all fixed repeats and an actual duplicate or provable missing weight. The right-terminal pair is ordered by label. Its weights do not require an ordering of the indexed terminal names.

One [parse-only preflight](preflight_receipt.json) checked all 79 repository-relative pins and the exact source bytes, with zero task-module imports and no bytecode caches. One official [invocation](command_receipt.json) used a single worker, 0.15625 process-CPU seconds, 0.19600669998908415 in-process wall seconds and 0.6293796 outer supervised wall seconds under the 60-second deadline. The unchanged checker accepted the retained D098 positive on its own original. Three adverse probes correctly rejected the wrong digest, the false physical entrance-zero claim and the label-alphabet-preserving terminal swap. The terminal swap repeated differences 5 and 7 and omitted 4 and 8. There were zero new graph identities, certificates, solver calls, complete-assignment visits, search states or nodes, separate exit tests, joins, retries, restarts and historical replays.

See the [frozen contract](CONTRACT.md), [configuration](config.json), [independent reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). The historical D083, D093 and D100 original and versioned executions retain their respective statuses.

## Reproduction under separate authorization

Use the pinned project-local Python from the project root in a disposable checkout with vacant output paths. Supervise the official process with a 60-second outer deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_ZERO_ENTRANCE_001/preflight.py b6cfd1f14f2fd8cb321ca227831c6f60ceb6697acdaa252802784bf1b03d4877
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_ZERO_ENTRANCE_001/run.py
```
