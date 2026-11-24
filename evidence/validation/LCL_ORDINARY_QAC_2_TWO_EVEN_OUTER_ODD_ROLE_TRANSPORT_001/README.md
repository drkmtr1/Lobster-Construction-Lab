# D127 verification evidence

**ACCEPT** the symbolic transport to both physical outer odd positions of exact ordered `[[q,a,c],[2]]` when the odd quota is at least three, both even quotas are at least two and one even quota is at least six. The least qualifying even index, unique odd index and remaining even index form the canonical-to-physical correspondence. The proof preserves the original labels and weights, all named incidences, R226 quotas and D112 premises. [Proof and dispatch](../../../research/ORDINARY_QAC_2_TWO_EVEN_OUTER_ODD_ROLE_TRANSPORT.md)

| Retained canonical original | Verified choice | Edge count |
| --- | --- | ---: |
| D122 positive I, `[[6,3,2],[2]]` | D122 I | 18 |
| D122 positive II, `[[6,5,6],[2]]` | D122 II | 24 |
| D123, `[[6,3,6],[2]]` | D123 | 22 |
| D124, `[[6,3,8],[2]]` | D124 | 24 |
| D126, `[[6,3,4],[2]]` | D126 | 20 |

All five [records](result.json) verify the identity map (0,1,2), canonical graph and separate certificate ledger hashes, original named incidences, complete label and difference bijections, and physical D112 premises. D126's accepted certificate is bound to the external D122 adverse original through both archives. D122's fixed-core obstruction was inspected once and keeps its historical scope. The nonidentity orders are proved symbolically.

| Declared control | Verification outcome |
| --- | --- |
| Wrong expected graph digest on D126 | Unchanged checker rejects the graph identity mismatch. |
| Role map (0,0,2) | Rejects nonbijection before quota binding. |
| Role map (2,1,0) for canonical (6,3,4) | Accepts the permutation check. Quota and slot gates reject absent `l:0:2:4`, `l:0:2:5` and omitted actual `l:0:0:4`, `l:0:0:5`. |
| Forward indices (1,2,0) and inverse (2,0,1) | Both direction compositions return the starting center and abstract terminal index. Using the inverse as forward fails at all three canonical indices. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [official verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.59375 process-CPU seconds and 1.500144 supervised wall seconds. Both standard-error records are empty. No numerical transport, new graph, certificate, batch allocation or numerical growth occurred. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QAC_2_TWO_EVEN_OUTER_ODD_ROLE_TRANSPORT_001/supervise.ps1'
$frozen = '68aa68f7de3c7d489ae717b3b3ce9946cd347dd5ec0d22bf40b67af9bce56f73'
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only after preflight passes.
& $runner -Phase verify -FrozenConfig $frozen
```
