# D113 verification evidence

**ACCEPT** the [symbolic ordinary supplier](../../../research/ORDINARY_Q3_2_ODD_COMPLEMENTARY_SUPPLIER.md) for the ordered originals `[[q,3],[2]]` with exact odd integer q≥5. The nine-vertex core fixes the three physical pins and leaves complementary label and difference intervals. The formula follows from the explicit indexed allocation and the symbolic R226 component and quota proof.

The [independent boundary audit](result.json) reconstructs the actual [D111 original](../LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json), all 15 vertex names and labels, all 14 incidences and differences, and the four residual components. It confirms pointwise agreement with the [retained certificate](../LCL_ORDINARY_53_2_DIRECT_SEED_001/result.json), independently rechecked once. The residual difference vertices are {3,7}, {4,6}, {5} and {8}, with label groups {5,9}, {6,8}, {7} and {4}. The prescribed higher/lower residual quotas are five and one. The ordinary spectrum and label alphabet are complete and D112's physical premises hold.

| Declared probe on D111 data | Outcome |
| --- | --- |
| Wrong expected graph digest | The unchanged ordinary checker rejects the mismatch. |
| Exchange 4 and 7 across centers | Labels and pins stay valid. Weights 8 and 5 become 5 and 2. The checker rejects the duplicate 2 on `s:0--b:0:1` and `b:0:1--l:0:1:1`, and missing 8. |
| Move midpoint 7 to the higher host | The two inventories remain exact. The residual higher/lower counts are (6,0) and the allocation predicate rejects. This probe stays at the allocation level. |
| Complement all labels about 14 | The ordinary checker accepts. The pin predicate rejects actual labels (14,0,13) in entrance, exit and right-center order. |

The [parse-only preflight](preflight_receipt.json) verified 228 repository input pins, five task source hashes, unique intended definitions, the runtime and vacant outputs. No task modules were imported and no bytecode was created. The single [official invocation](command_receipt.json) used 0.203125 process-CPU seconds and 0.20637549995444715 internal wall seconds. The [external supervisor](supervisor_receipt.json) recorded 0.485666 seconds and exit zero, with empty [standard error](official_stderr.txt). The counts are one worker, one boundary evaluation, one retained positive recheck, four probes and one symbolic proof. Additional profiles, graphs, certificates, solver calls, enumeration, search, joins, replays, retries, restarts and successor experiments were all zero.

[Contract](CONTRACT.md) · [Configuration](config.json) · [Independent reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Run from the project root in a disposable checkout with vacant output paths, using the pinned Python runtime and PowerShell 7.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_Q3_2_ODD_COMPLEMENTARY_SUPPLIER_001/preflight.py' '0698bcff67d4ecc6e01faa18baff823e19982ad29f39bae747cbc7586bbfcb09'
# Continue only if the preflight passes.
& 'evidence/validation/LCL_ORDINARY_Q3_2_ODD_COMPLEMENTARY_SUPPLIER_001/supervise.ps1'
```
