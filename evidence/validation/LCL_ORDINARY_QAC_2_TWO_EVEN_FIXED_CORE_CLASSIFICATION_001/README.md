# D122 verification evidence

**ACCEPT** the [fixed-core classification](../../../research/ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION.md) for ordered `[[q,a,c],[2]]` at even q≥6 and c≥2 and odd a≥3. The specified D118 labeled core has a completion exactly when a≥5 or c≤q−4. The negative result concerns all completions of those fixed labels and numerical roles. Both positive branches meet D112's physical growth premises.

| Frozen original | Verified outcome |
| --- | --- |
| [`[[6,3,2],[2]]`](original_I.json) | Construction I yields a full certificate at the cutoff. A's midpoint 8 goes to H and B's midpoint 7 goes to L. |
| [`[[6,3,4],[2]]`](original_adverse.json) | The [fixed-core obstruction](obstruction.json) records forced H labels 3 and 4 and parity capacities 4 and 5 against a same-class demand of 6. No candidate completion or certificate was generated. |
| [`[[6,5,6],[2]]`](original_II.json) | Construction II yields a full certificate beyond I's progression bound. B has three forced half-edges, one loop and three complete pairs. |

[Both certificates and the independent audit](result.json) report every named incidence, full inventories, exact slots and local projections. The retained D119 certificate was rechecked once on its own original, with zero formula evaluations outside the D122 domain.

| Declared control on I | Verified outcome |
| --- | --- |
| Wrong expected digest | The unchanged checker rejects the identity mismatch. |
| Move A midpoint 8 from H to L | Weight 6 and both local inventories persist. L/H quotas change from (0,5) to (1,4), so the local predicate rejects. |
| Move B midpoint 7 from L to C | Weight 5 and both local inventories persist. L/C quotas change from (2,2) to (1,3), so the local predicate rejects. |
| Replace A pair {6,10} by {5,11} | Both local predicates pass. The global check finds repeated labels 5,11 and weights 3,9 and missing labels 6,10 and weights 4,8. |

**PASS** one [preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json) and one [supervised verification](command_receipt.json). The [combined time](verification_supervision.json) was 0.703125 process-CPU seconds and 2.1070232 supervised wall seconds. All three standard-error records are empty. Exactly three originals, two certificates, one obstruction, four positive batches, one retained recheck and four probes were produced or executed as specified. No additional profiles, solvers, assignments, search, joins, role transport, growth, replays, retries or successor experiments occurred.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs. Preserve committed raw line endings, for example with clone-local `core.autocrlf=false`.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION_001/supervise.ps1'
$frozen = '36b7a4a573fcaff3f7aebc0a49738fcebd355391d43539368509fd5378472def'
& $runner -Phase prepare -FrozenConfig $frozen
# Continue only after passing preparation.
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only after passing the parse-only preflight.
& $runner -Phase verify -FrozenConfig $frozen
```
