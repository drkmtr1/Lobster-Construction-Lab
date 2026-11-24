# D129 verification evidence

**ACCEPT** the D123 modified-core supplier for exact ordered `[[q,a,c],[2]]` with independent exact even q,c≥4 and odd a≥3 at pins (0,q+a+c+7,1). The central reservation supplies q−1 X slots and a−2 M slots by assigning exactly (q−4)/2 complete reflected pairs to X. The complementary chains supply all c Z slots and the isolated half-edge supplies one M slot. The proof gives both complete original bijections and checks the physical D112 premises. [Proof](../../../research/ORDINARY_QAC_2_UNIFIED_MODIFIED_SHARED_MIDDLE_CORE.md)

The sole [new original](original.json) is `[[6,5,8],[2]]` with canonical graph digest `331d4fa1bffe82689865c1a600c819cb1e4a3dbcbd90ff7614e4bd3317e1e234` and raw SHA-256 `5355ee7c4aa06639f30f286f1730cbf27420f8552f9311ca7ad0fba28405ed4f`. Its [certificate and audit](result.json) have ledger `9e8cd19be4d9c779fb333540f8d9bd67ec4c886bdf40f46c3e65ab9f53570541`. All 27 labels and 26 actual differences occur once. The signed sum is 199 and the excess-degree weighted sum is 316. A's X projection is {2,3,4,5,6,7}, with selected quotas (5,3) in X/M order. B's M projection is {1}, with quotas (1,8) in M/Z order.

D126 and D128 each passed one retained checker recheck and one pointwise comparison of core labels, both palettes, ordered allocations, named slots and complete labels. D126 uses D122's unchanged adverse original. D123 and D124 specializations are proved symbolically.

| Declared control | Verified outcome |
| --- | --- |
| Wrong expected digest | The unchanged checker rejects the graph identity mismatch. |
| Swap X index 1 and Z index 4 | Weight 5 repeats on X index 1 and Z index 5. Weight 14 repeats on X index 5 and Z index 4. Weights 6 and 15 are missing. |
| Move pair {8,14} from X to M | Weights 6 and 12 exchange. Both reserved inventories persist, and the X/M quotas change from (5,3) to (3,5). The quota gate rejects. |
| Replace A label 8 and weight 6 with label 7 and weight 5 | Both local allocations pass. A has the new parallel pair {7,15}, with label 14 forced to X. The global gate rejects repeated label 7 and weight 5 and missing label 8 and weight 6. |

**PASS** one [preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json) and one [supervised verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.75 process-CPU seconds and 2.0434179 supervised wall seconds. All three standard-error records are empty. The scope counters separate two new and four retained comparison batch objects from the four controls. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after each phase passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QAC_2_UNIFIED_MODIFIED_SHARED_MIDDLE_CORE_001/supervise.ps1'
$frozen = 'fedcc9311012e64538bf5929e6d8b45cc0a871fe3e0adb05d5ab534df66a23c1'
& $runner -Phase prepare -FrozenConfig $frozen
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
