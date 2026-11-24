# D130 verification evidence

**ACCEPT** the exact D123 modified-core completion classification on `[[2,a,c],[2]]` at pins (0,a+c+9,1) for independent exact odd a≥3 and even c≥4. The core admits a completion exactly when a≤c−1. In that sector the residual allocation to hosts is forced by one reflection followed by the step-two translation cycle. The complement is assigned to Z. The obstruction at a≥c+1 applies to every completion of these fixed labels and roles. [Proof](../../../research/ORDINARY_2AC_2_MODIFIED_CORE_CLASSIFICATION.md)

The [positive original](original.json) is `[[2,5,6],[2]]` with canonical digest `d5639f8f1a3f6a88477088ce7acab577b48d8deb50a92e95adf48aac7abd6f0a`. Its [certificate and audit](result.json) have ledger `f20c7d32b8d0a5957828c9326a0e37f8ac507ee893702c6ae816ecc58f2d7dc5`. All 21 labels and 20 original differences occur once. The signed sum is 156 and the excess-degree weighted sum is 192. The actual residual cycle uses 13→5→7→9→11→13, with fixed points at the other six labels. Batch A's X projection is {1,3}, with selected quotas (1,3) in X/M order. Batch B's M projection is {1}, with quotas (1,6) in M/Z order. D112's physical premises hold.

The [adverse original](original_adverse.json) is `[[2,5,4],[2]]` with canonical digest `fcf956468884f52c4ce87e8ea293b7f4485f332d116b51bbcf2632c1d285cbb7`. The [independent bound](obstruction.json) recomputes the exact fixed core, physical slots and reference weights. The sole X vacancy requires label 12, above the residual maximum 11. The output includes no adverse certificate.

D129 passed one retained checker recheck through its manifest, original, archived certificate and proof binding.

| Declared control | Verified outcome |
| --- | --- |
| Wrong expected digest | The unchanged checker rejects the original identity mismatch. |
| Swap X index 1 and Z index 5 | Weight 10 repeats at X index 1 and Z index 2. Weight 3 repeats at M index 3 and Z index 5. Weights 4 and 11 are missing. |
| Move pair {7,9} from M to X | Weights 7 and 5 exchange. Both reserved inventories persist and quotas change from (1,3) to (3,1), so the quota gate rejects. |
| Replace A label 13 and weight 11 with label 12 and weight 10 | Both local allocations pass. Global compatibility rejects repeated label 12 and weight 10 and missing label 13 and weight 11. |

**PASS** one [preparation](preparation_receipt.json) covering both originals, one [parse-only preflight](preflight_receipt.json) and one [supervised verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.5625 process-CPU seconds and 1.7674478 supervised wall seconds. All three standard-error records are empty. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after each phase passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_2AC_2_MODIFIED_CORE_CLASSIFICATION_001/supervise.ps1'
$frozen = 'eabc5a45e0ae4e2417a1de2897079d560ef12e29a8199f952e6484582f17dd45'
& $runner -Phase prepare -FrozenConfig $frozen
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
