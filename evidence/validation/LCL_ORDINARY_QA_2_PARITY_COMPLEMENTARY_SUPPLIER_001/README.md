# D116 verification evidence

**ACCEPT** the [symbolic ordinary supplier](../../../research/ORDINARY_QA_2_PARITY_COMPLEMENTARY_SUPPLIER.md) for ordered `[[q,a],[2]]` at independently chosen exact integers q≥5 and a≥3 with at least one even. The named lower host has even quota and takes whole reflected pairs. An available midpoint stays higher, and both exact inventories and integral quotas follow. The proof also handles the even–even midpoint-only mutation symbolically.

The [independent boundary audit](result.json) reconstructs the actual [D114 original](../LCL_ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER_001/original.json) and verifies pointwise formula agreement with its [retained certificate](../LCL_ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER_001/result.json) at (6,3). The original's 16 named labels, 15 weights, R226 components, physical roles and D112 premises agree. The unchanged checker rechecked D114 once and separately rechecked D111 on its own original. The formula runs only for D114.

| Declared probe on D114 | Outcome |
| --- | --- |
| Wrong graph digest | The unchanged checker rejects the digest mismatch. |
| Swap labels 6 and 5 across the two hosts | The label bijection, pins and quotas (4,3) persist. Weight 3 occurs on `b:0:0--l:0:0:1` and `b:0:1--l:0:1:2`. Weight 7 occurs on `b:0:0--l:0:0:4` and `b:0:1--l:0:1:1`. Weights 4 and 8 are missing. The ordinary checker rejects. |
| Move pair {5,10} to the lower host | Both residual inventories remain exact. Quotas become (6,1) in lower/higher order, so the allocation gate rejects. The mutation remains allocation-only. |
| Complement about 15 | The ordinary checker accepts. The physical-pin gate rejects (15,0,14) in entrance, exit and right-center order. |

The [parse-only preflight](preflight_receipt.json) checked 282 repository pins, five task source hashes, intended unique definitions, runtime and vacant outputs with no task imports or bytecode. The single [official invocation](command_receipt.json) used 0.234375 process-CPU seconds and 0.26279190002242103 in-process wall seconds. The [external supervisor](supervisor_receipt.json) recorded 0.5431175 seconds and exit zero, with empty [standard error](official_stderr.txt). There was one worker, one formula boundary, two retained rechecks and four controls. New profiles, graphs, certificates, solvers, assignment visits, search, joins, replays, retries, restarts and successor experiments all numbered zero.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Independent reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned Python runtime and PowerShell 7 from a disposable checkout with vacant official outputs.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_QA_2_PARITY_COMPLEMENTARY_SUPPLIER_001/preflight.py' '377db1fcbf8071b4d83785afa975854b6dee13a530a52663fc32d48358dd6709'
# Continue only if the preflight passes.
& 'evidence/validation/LCL_ORDINARY_QA_2_PARITY_COMPLEMENTARY_SUPPLIER_001/supervise.ps1'
```
