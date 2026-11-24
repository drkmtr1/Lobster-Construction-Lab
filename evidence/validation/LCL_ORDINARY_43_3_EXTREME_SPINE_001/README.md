# D106 verification evidence

The [proof](../../../research/ORDINARY_43_3_EXTREME_SPINE.md) transfers the retained [D105 certificate](../LCL_ORDINARY_43_2_EXTREME_SPINE_001/result.json) to the exact target ordered `[[4,3],[3]]`. The [target original](original.json) has graph digest `df89d0f500d8900d44641b6725f4ce3095df900c663006271855330d01d2a86e`. Its single new vertex is `l:1:0:2` and its only new incidence is the edge to `b:1:0`.

The [result](result.json) contains the complete original-bound certificate under `certificate` and the independent transition audit and whole edge ledger under `incidence_audit`. The target ledger ID is `b1be1d8561e4570e4d295c8f61ae3b2c7171146519cf1d1ebe917becb3a7565c`. Both unused inventories are empty. The two changed old incidences and the newly added incidence give absolute weights 14, 13 and 12, while all other weights are retained. The physical spine labels are (0,14). The sole negative signed edge is `l:0:0:3 → b:0:0` with value −1, so the signed degree sum is 103. This certificate does not separate the bipartition label classes. The separate D098 theorem supplies an alpha labeling on the same target topology at q=4, a=r=3. The D104 exclusion is on the two-right-terminal source.

The [parse-only preflight](preflight_receipt.json) checked all 121 repository hashes with zero task imports. The single [official invocation](command_receipt.json) used one worker, 0.09375 process-CPU seconds, 0.1058935999753885 in-process wall seconds and 0.4793879 seconds under the outer deadline. It verified one new original and one accepted certificate. The unchanged checker accepted the retained D105 original-bound certificate. The three target probes rejected the wrong graph digest, rejected the cross-center swap for repeats 6 and 7, and rejected the within-center swap at the exact signed-interface gate. The within-center swap retained ordinary gracefulness and moved the reversal to `l:0:0:0 → b:0:0`. Its record is an adverse control. No solver, enumeration, search, additional profile, join, replay, retry or restart occurred.

See the [contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). Historical original and versioned receipts remain preserved.

## Reproduction under separate authorization

Use the pinned project-local executable from the project root in a disposable checkout with vacant output paths. Supervise the official invocation with a 60-second outer deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_43_3_EXTREME_SPINE_001/preflight.py 080ae88b5fcd500c4ad8b75edcbfbebe1a72b616faf6b2389f57b8d445825fb9
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_43_3_EXTREME_SPINE_001/run.py
```
