# D124 verification evidence

**ACCEPT** the direct ordinary graceful supplier for ordered `[[q,3,c],[2]]` at independently chosen exact even q,c≥6 with q≠c and pins (0,q+c+10,1). The D123 core remains fixed. The interval of width q+1 supplies X and one physical M vacancy through reflection and deletion. The complementary c labels supply Z through forced translation chains, with the other M vacancy supplied by an isolated half-edge. The two local allocations partition all original labels, edge differences and terminal slots. [Proof](../../../research/ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE.md)

| Verified original | Outcome |
| --- | --- |
| [New `[[6,3,8],[2]]`](original.json) | All 25 vertex labels and 24 edge differences occur once, with signed sum 166 and excess-degree weighted sum 252. The A projection is {2,3,4,5}, choosing (5,1) in X/M order. The B projection is {1}, choosing (1,8) in M/Z order. |
| [Retained D123 `[[6,3,6],[2]]`](../../../evidence/validation/LCL_ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE_001/original.json) | One formula comparison agrees at all named labels, core vertices, palettes, ordered allocations and slots. The unchanged original-target checker also rechecked the retained certificate once. The historical procedure was not replayed. |

The new graph digest is `386aa9158bf0ea3763067cb2fe2b87abe27837cc033b759328e0cbaf90cc37a4`. The [certificate and audit](result.json) have ledger `bb5651a7e20245659f831eef965eeed8fb247239855a843b6ac82d19f2a5399b`. The quantified proof covers both unequal orders and specializes symbolically to D123 on the diagonal. The seeds meet D112's physical premises. D122 retains its original fixed-core obstruction.

| Declared control on the new original | Verified result |
| --- | --- |
| Wrong expected graph digest | The unchanged checker rejects the identity mismatch. |
| Swap X index 1 and Z index 4 | Weight 5 repeats on X index 1 and Z index 5. Weight 12 repeats on X index 5 and Z index 4. Weights 6 and 13 are missing. The vertex bijection, quotas and pins persist. |
| Assign B label 3 to M instead of Z | The label inventory and row eligibility pass. M's option repeats 15 with Z label 5, omits 17 and changes M/Z quotas from (1,8) to (2,7). The allocation fails. |
| Replace A label 8 and weight 6 with label 7 and weight 5 | The changed A pair is {7,13}. Both local allocations pass. The global check finds repeated label 7 and weight 5 and missing label 8 and weight 6. |

**PASS** one [preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json) and one [official verification](command_receipt.json). There were two new positive batch reservations and two retained comparison batch objects. The [combined receipt](verification_supervision.json) records 0.203125 process-CPU seconds and 0.7740493 supervised wall seconds. All three standard-error records are empty. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after each phase passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE_001/supervise.ps1'
$frozen = 'e974caf52f88988d3f2e6daec40484a27d8d0fd3fd22cf24d0b5528cc93d450e'
& $runner -Phase prepare -FrozenConfig $frozen
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
