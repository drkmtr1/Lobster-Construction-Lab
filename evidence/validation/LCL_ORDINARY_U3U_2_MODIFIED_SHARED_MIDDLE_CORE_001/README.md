# D123 verification evidence

**ACCEPT** the direct supplier for exact ordered `[[u,3,u],[2]]` at every exact even integer u≥6, with fixed physical pins (0,2u+10,1). The modified ten-vertex core places the weight-one incidence at the physical middle center. Reflection component deletion supplies its index-1 terminal from Batch A. An isolated half-edge supplies its index-2 terminal from Batch B, whose four translation chains force every other label to Z. Both disjoint reservations realize their named quotas and complete the original label and difference bijections. The supplied seeds meet D112's premises. D122's original fixed-core obstruction retains its exact scope. [Proof](../../../research/ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md)

| Frozen boundary | Identity |
| --- | --- |
| [Original `[[6,3,6],[2]]`](original.json) | `ac71eba8f56fefb203192b6d3f2cf2b7157bd0ab9a091260413fcc1884ba28b4` |
| [Certificate, independent audit and controls](result.json) | Ledger `be06550ced186c0b21dc4b864efad036f0a8c6b7a6e21c2d5b96032a4764ecb3` |

Batch A's X projection is `{2,3,4,5}`, selecting 5. Batch B's M projection is `{1}`, with chains on labels (3,5), (4,6), (14) and (15) and the isolated M label 10. The certificate covers every label 0–22 and weight 1–22 exactly once. The archived D122 positive I passed one checker recheck on its own original. The D122 adverse original, disposition and record hashes were inspected read-only.

| Declared control | Verification outcome |
| --- | --- |
| Wrong expected digest | Unchanged original-target checker rejects the mismatch. |
| Swap X index 1 and Z index 3 | Alphabet, pins and quotas persist. Weight 4 repeats at X index 1 and Z index 4. Weight 11 repeats at X index 5 and Z index 3. Weights 5 and 12 are missing. |
| Move A pair {7,11} from X to M | Weights 5 and 9 exchange and both inventories persist. X/M quotas change from (5,1) to (3,3), so the local check rejects. |
| Replace A's label 7 and weight 5 with label 6 and weight 4 | Both local checks accept, while the global check reports repeated label 6 and weight 4 and missing label 7 and weight 5. |

**PASS** one [preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json) and one [official verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.40625 process-CPU seconds and 1.4363846 supervised wall seconds. All three standard-error records are empty. See the [contract](CONTRACT.md), [frozen configuration](config.json), [separate reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json).

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after each phase passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE_001/supervise.ps1'
$frozen = '26799e5feaddbe138cf9d07dc2408abe334bf402382ad408bf929397ac887d85'
& $runner -Phase prepare -FrozenConfig $frozen
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
