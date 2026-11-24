# D128 verification evidence

**ACCEPT** the direct D123 modified-core supplier for exact ordered `[[4,a,4],[2]]` with exact odd a≥3 at pins (0,a+15,1). Batch A assigns every intact reflected pair to M, with the midpoint and two forced labels supplying three X vacancies. Batch B supplies M's last vacancy and all four Z terminals. The proof covers a=3 symbolically, where A has no intact pair. [Proof](../../../research/ORDINARY_4A4_2_MODIFIED_SHARED_MIDDLE_CORE.md)

The sole [new original](original.json) is `[[4,5,4],[2]]`. Its graph digest is `c9cdc5e37bfaa9c2566532b422d965bc437aa5ca8d3de68c10626ae8efb81406`. The [certificate and audit](result.json) have ledger `544fdae0b943bc3eb0c8126e763ce6bee18d8188262f917ace98b379e836c4be`. All 21 labels and 20 named differences occur once. The signed sum is 128 and the excess-degree weighted sum is 164. The integral X projection is {2,3,4,5}, choosing (3,3) at X/M, and the integral B projection at M is {1}, choosing (1,4). D112's premises pass. The retained D126 certificate passed once using its archived labels and frozen D122 original, bound through both manifests.

| Declared control | Verified outcome |
| --- | --- |
| Wrong expected digest | The unchanged checker rejects the graph identity mismatch. |
| Swap X index 1 and Z index 2 | Weight 3 repeats on X index 1 and Z index 3. Weight 8 repeats on M index 1 and Z index 2. Weights 6 and 11 are missing. |
| Move pair {6,10} from M to X | The two weights exchange and both numeric inventories persist. The X/M quotas change from (3,3) to (5,1), so the quota gate rejects. |
| Replace A label 11 and difference 9 with label 13 and difference 11 | Both local allocations pass. The global check rejects repeated label 13 and weight 11 and missing label 11 and weight 9. |

**PASS** one [preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json) and one [supervised verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.75 process-CPU seconds and 2.1450574 supervised wall seconds. All three standard-error records are empty. No additional profiles, historical formula evaluation, numerical transport or growth occurred. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after each phase passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_4A4_2_MODIFIED_SHARED_MIDDLE_CORE_001/supervise.ps1'
$frozen = '3b5c881cb454e054f09a7f04aa6d9d37d1c18dd63a75944d41fc4eda6899d5fc'
& $runner -Phase prepare -FrozenConfig $frozen
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
