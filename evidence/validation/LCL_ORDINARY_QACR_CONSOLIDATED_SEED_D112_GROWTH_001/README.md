# D125 verification evidence

**ACCEPT** the consolidated ordinary supplier for exact ordered `[[q,a,c],[r]]` at `(s:0,s:1,b:1:0)=(0,q+a+c+r+5,1)` on precisely the D118–D124 positive seed union and every exact integer r≥2. The [proof and dispatch table](../../../research/ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH.md) give both domain inclusions, the priority rule, the indexed D112 application and the independent full inventories. They also derive the persistent all-even pin obstruction.

| Retained positive | Left quotas | Selected supplier | Seed edges |
| --- | --- | --- | ---: |
| D118 | (5,3,2) | D119, with D118 specialization | 17 |
| D119 | (5,3,4) | D119 | 19 |
| D120 | (5,3,3) | D120 | 18 |
| D122 I | (6,3,2) | D122 I | 18 |
| D122 II | (6,5,6) | D122 II | 24 |
| D123 | (6,3,6) | D123 | 22 |
| D124 | (6,3,8) | D124 | 24 |

The [results](result.json) bind the seven distinct originals and certificates to their accepted manifests, report each actual named incidence and ledger identity, and verify the complete inventories, D112 premises and r=2 pointwise identity from frozen labels. The D121 inspection verifies the archived identity order and pointwise agreement on the same D119 original. The read-only D122 adverse inspection verifies its distinct original and scoped obstruction.

| Declared control | Verified outcome |
| --- | --- |
| Wrong expected graph digest | Unchanged checker rejects the D124 mismatch while reproducing its original weights. |
| Cross-bind D123 metadata to D124 | Original-identity binding rejects before any label or growth operation. |
| Dispatch archived D122 adverse triple (6,3,4) | Returns OUTSIDE_ESTABLISHED_COVERAGE. The D122 fixed-core obstruction keeps its distinct scope. |
| Wrong claimed D124 seed edge count | Rejects 25 against 24 actual edges, 24 profile-derived edges and maximum label 24. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [official retained-only verification](command_receipt.json). The [combined receipt](verification_supervision.json) reports 0.671875 process-CPU seconds and 1.6543117 supervised wall seconds. Both standard-error records are empty. The run used seven retained rechecks, seven positive dispatch evaluations, both historical inspections and four controls. New originals, certificates, seed formula evaluations, reservations and numerical growth all count zero. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant output paths. Preserve the frozen raw line endings.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH_001/supervise.ps1'
$frozen = 'be14ad181a255cbf2b285fa3d746c5eb2f5d23805966d9a46664b1da4cd38f35'
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only after the preflight passes.
& $runner -Phase verify -FrozenConfig $frozen
```
