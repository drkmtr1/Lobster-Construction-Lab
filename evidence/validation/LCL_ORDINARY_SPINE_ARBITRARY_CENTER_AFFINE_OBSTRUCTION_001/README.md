# D133 retained verification evidence

**ACCEPT** the quantified obstruction for appending a single section with h≥3 positive-quota centers and total terminal quota Q at n≥h+Q under any one integer affine isometry of the supplied ordinary graceful prefix. The connector and exact terminal bands force all terminals to the two extreme center labels. The same proof excludes any old relabeling whose occupied labels form one consecutive interval and whose actual old differences exhaust [1,n]. The h=2 degeneration recovers D132. This is an obstruction within the stated inventory and topology regime. [Proof](../../../research/ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION.md)

The unchanged checker and independent audit rechecked D105 and D130 on their actual archived originals at deficit zero. D105 is bound to its D099-owned original, D130 to its retained positive original, and both rechecks agree with the reviewed D131 and D132 archives. The D104 alpha exclusion retains its binding to the exact D105 original. [Retained bindings and controls](result.json)

| Declared control | Verified outcome |
| --- | --- |
| Incorrect D105 expected digest | The unchanged checker rejects only the identity mismatch. |
| Symbolic equality n=h+Q | The maximum width of either unused interval is at most n. The smallest new weight is n+1, leaving a strict unit gap. |
| Intermediate host in either band | The lower shift is 1+(h−2−j) and the upper loss is 1+(j−1). Each is strictly positive for the intermediate label and contradicts the corresponding exact sum. |
| Symbolic h=2 degeneration | The intermediate interval is empty. The quotas at labels one and zero must be κ and Q−κ respectively, as in D132. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [supervised retained verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.5625 process-CPU seconds and 1.5296155 supervised wall seconds. Both standard-error records are empty. There are zero new originals, certificates, numerical suffixes or transitions. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved. Continue only after preflight passes.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION_001/supervise.ps1'
$frozen = '557da9ddde09e355bf406f923f726791a7824d6b97ac86f76fbe088d1c7bf8c1'
& $runner -Phase preflight -FrozenConfig $frozen
& $runner -Phase verify -FrozenConfig $frozen
```
