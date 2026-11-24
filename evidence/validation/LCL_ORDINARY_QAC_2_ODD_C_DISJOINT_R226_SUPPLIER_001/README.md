# D120 verification evidence

**ACCEPT** the [symbolic supplier](../../../research/ORDINARY_QAC_2_ODD_C_DISJOINT_R226_SUPPLIER.md) for exact ordered `[[q,a,c],[2]]` with independent odd integers q≥5, a≥3 and c≥3 at pins `(s:0,s:1,b:1:0)=(0,q+a+c+7,1)`. On the unchanged D118 core, the centered Batch B reservation removes the arithmetic midpoint from A and makes one different midpoint eligible in B. The local quota projections and global partitions yield the full named graph labeling. D119 and D120 give every c≥2 at the stated odd q and a bounds. D112's physical premises pass.

The sole [frozen original](original.json), `[[5,3,3],[2]]`, has 19 named vertices and 18 original edges. The [certificate and independent audit](result.json) verify both inventories. A's arithmetic midpoint 8 is paired with 6 in B. B's own midpoint 7 supplies weight 5 at either host and is assigned to C. The unchanged checker rechecked D119 on its retained even-parity original once. The odd supplier had zero retained formula evaluations.

| Control | Verified outcome |
| --- | --- |
| Wrong original digest | Rejected for the original-identity mismatch. |
| Cross-batch swap of 5 and 6 | The alphabet, quotas and pins persist. Weight 8 repeats on `b:0:0--l:0:0:3` and `b:0:1--l:0:1:2`. Weight 7 repeats on `b:0:1--l:0:1:1` and `b:0:2--l:0:2:0`. Weights 6 and 9 are missing. |
| Move B midpoint 7 from C to L | Weight 5 and both local inventories persist. L/C quotas change from (2,3) to (3,2) and the local quota check rejects. |
| Replace A's pair {5,11} by {6,10} | Both local predicates accept. The global predicate rejects repeated labels 6,10 and weights 4,8, and missing labels 5,11 and weights 3,9. |

**PASS** one [original preparation](preparation_receipt.json), [parse-only preflight](preflight_receipt.json), and [official invocation](command_receipt.json). Combined use was 0.3125 process-CPU seconds and 1.2824638 [supervised wall seconds](verification_supervision.json). All three standard-error records are empty. Counts were one worker, one new original and certificate, two positive reservations, one retained recheck and four controls. There were zero additional profiles, assignment enumerations, solvers, searches, joins, replays, retries, restarts and successor experiments.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs. Preserve the committed raw line endings, for example with clone-local `core.autocrlf=false`.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QAC_2_ODD_C_DISJOINT_R226_SUPPLIER_001/supervise.ps1'
$frozen = 'fbabde6973d99273739035d14c2970fb02b44e07296a7d4cfbea00a178e7e1d4'
& $runner -Phase prepare -FrozenConfig $frozen
# Continue only after passing preparation.
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only after passing the parse-only preflight.
& $runner -Phase verify -FrozenConfig $frozen
```
