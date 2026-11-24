# D131 retained verification evidence

**ACCEPT** the sign-independent ordinary graceful transition on a supplied named prefix with frontier deficit δ. For one appended actual spine section with one positive-quota center, the specified embedding is admissible exactly for integer r≥1 with r≥δ. It returns deficit r−δ. Every admitted finite quota list has a fixed-final-alphabet realization that assigns each physical label once and maintains both complete residual inventories. The mathematical proof establishes the theorem and both corollaries. [Proof](../../../research/ORDINARY_SPINE_DEFICIT_TRANSITION.md)

The unchanged checker and independent audit rechecked two archived seeds. D105's ordinary certificate uses the D099-owned original `[[4,3],[2]]`. The accepted D104 alpha exclusion binds to that same original. D130 uses its own positive original `[[2,5,6],[2]]`. Both exhausted their original normalized inventories and met the D112 physical premises with initial deficit zero. [Retained bindings and control reports](result.json)

| Declared control | Verified outcome |
| --- | --- |
| Incorrect D105 expected digest | The unchanged checker rejects the original identity mismatch. |
| D105 wrong frontier s:0 with deficit 13 | Its scalar deficit agrees at the claimed vertex. The exact ordered witness ends at s:1, so the physical gate rejects. |
| D130 correct frontier with claimed deficit one | Its physical frontier passes. The actual deficit is zero, so the numerical state gate rejects. |
| Symbolic δ=r+1 | The required new frontier value is m+1 and the returned deficit is −1. The proposed placement is inadmissible before emission. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [supervised retained verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.328125 process-CPU seconds and 0.8538056 supervised wall seconds. Both standard-error records are empty. There were zero numerical transition applications, suffix lists, joins, new originals and new certificates. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after preflight passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_SPINE_DEFICIT_TRANSITION_001/supervise.ps1'
$frozen = 'fbe755b54e14375ad2da4c806b9be4df9b4780c46367e579be5dc132b13c3543'
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
