# D132 retained verification evidence

**ACCEPT** the conditional ordinary two-center spine transition from a supplied D131 state with n edges and deficit δ. With independent exact positive quotas q,a, a canonical affine mode is admitted when its effective coordinate κ, equal to δ for reflection and n−δ for translation, matches either physical quota. The return deficit is the other quota. At n≥q+a+2 this is also the exact existence test over all single affine isometries of the supplied labels. The positive construction itself does not require the size bound. Admitted mixed lists close, and the fixed-final-alphabet realization assigns each physical label once. [Proof](../../../research/ORDINARY_SPINE_TWO_CENTER_AFFINE_TRANSITION.md)

The unchanged checker and independent audit rechecked D105 and D130 on their actual archived originals. Both supply the ordinary normalized frontier at deficit zero and meet D112's physical premises. D131's manifest binds both originals, archived certificates and proof. D104's accepted alpha exclusion retains its binding to the D099-owned D105 graph. [Bindings and controls](result.json)

| Declared control | Verified outcome |
| --- | --- |
| Incorrect D105 expected digest | The unchanged checker rejects the identity mismatch. |
| D130 wrong frontier s:0 with deficit 20 | Its numerical deficit is consistent at s:0, but the actual ordered witness ends at s:1. The physical gate rejects. |
| Symbolic deficit zero at n≥q+a+2 | Reflection gives 0, below either quota. Translation gives n, above either quota. The classified affine regime rejects. |
| Symbolic δ=n−q with n>2max(q,a) | The reflection coordinate exceeds both quotas. Translation gives κ=q and returns a. Mode choice is part of the plan. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [supervised retained verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.515625 process-CPU seconds and 1.3586748 supervised wall seconds. Both standard-error records are empty. No new original, certificate, numerical transition or suffix list was generated. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after preflight passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_SPINE_TWO_CENTER_AFFINE_TRANSITION_001/supervise.ps1'
$frozen = '707bc5fcf8340e4c202af55d61707bacfb61c21a63d7fd86e08ceff0e1aaae92'
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
