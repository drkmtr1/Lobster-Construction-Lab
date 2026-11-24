# D115 verification evidence

**ACCEPT** the [symbolic ordinary supplier](../../../research/ORDINARY_QA_2_ODD_ODD_COMPLEMENTARY_SUPPLIER.md) for ordered `[[q,a],[2]]` at independently chosen exact odd integers q≥5 and a≥3. The explicitly supplied core yields complementary palettes. At the lower host, a centered interval contains a−2 labels and uses the midpoint and (a−3)/2 reflected pairs. The q remaining labels go to the higher host. The displaced lower-host difference multiset equals its higher-host image under reflection.

The [independent boundary audit](result.json) reconstructs the [retained D111 original](../LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json), all 15 named vertex labels, all 14 original weights and all four residual components. At (5,3), the lower interval is [7,7] and the quotas are (1,5) in lower/higher order. The formula agrees at every name with the [retained ledger](../LCL_ORDINARY_53_2_DIRECT_SEED_001/result.json), rechecked once. Both inventories and D112's physical premises hold. The D113 specialization is proved symbolically for a=3.

| Declared probe on D111 data | Outcome |
| --- | --- |
| Wrong original graph digest | The unchanged checker rejects the digest mismatch. |
| Cross-center swap of 4 and 7 | The label bijection and pins persist. Weight 2 repeats on `s:0--b:0:1` and `b:0:1--l:0:1:1`. Weight 8 is missing, and the ordinary checker rejects. |
| Move pair {5,9} to the lower host | The pair still supplies weights {3,7} and the midpoint stays at the lower host. Both full residual inventories persist. Quotas become (3,3) and the allocation gate rejects. The probe stays at the allocation level. |
| Complement about 14 | The unchanged ordinary checker accepts. The pin gate rejects (14,0,13) in entrance, exit and right-center order. |

The [parse-only preflight](preflight_receipt.json) checked 265 repository pins, five task source hashes, intended unique definitions, runtime and vacant outputs with no task imports or bytecode. The one [official invocation](command_receipt.json) used 0.078125 CPU seconds and 0.09078659996157512 internal wall seconds. The [supervisor](supervisor_receipt.json) recorded 0.2123198 seconds and exit zero with empty [standard error](official_stderr.txt). One worker, one retained boundary and recheck, and four probes were recorded. New profiles, originals, certificates, solver calls, assignment enumeration, search, joins, replays, retries, restarts and successor experiments were all zero.

[Contract](CONTRACT.md) · [Configuration](config.json) · [Independent reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned Python runtime and PowerShell 7 from the project root in a disposable checkout with vacant official output paths.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_QA_2_ODD_ODD_COMPLEMENTARY_SUPPLIER_001/preflight.py' 'e71a5c5eec1957e337748bd9a8d0ff9913f704de1bcc604bfc245e67e8db1b8f'
# Continue only if the preflight passes.
& 'evidence/validation/LCL_ORDINARY_QA_2_ODD_ODD_COMPLEMENTARY_SUPPLIER_001/supervise.ps1'
```
