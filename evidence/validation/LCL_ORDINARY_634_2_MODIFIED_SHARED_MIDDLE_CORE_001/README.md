# D126 verification evidence

**ACCEPT** the D123 modified core on exact retained ordered `[[6,3,4],[2]]` at physical pins (0,20,1). The component audit distinguishes the A loop and parallel pair from B's forced translation chain and singleton components. The upper complement {13} gives one nonempty chain. A fills M index 1 and B fills M index 2. The actual named incidences consume all 21 labels and all 20 weights exactly once. [Proof](../../../research/ORDINARY_634_2_MODIFIED_SHARED_MIDDLE_CORE.md)

The [frozen target](../../../evidence/validation/LCL_ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION_001/original_adverse.json) retains graph digest `be51de0924c9de0f9a81929ecb98c9f29502e7f78ccadd0bfb6384f32c99e393` and raw SHA-256 `9875fa6239d80dac3702b73d502b9621469b6c1c44289f7026fff39c8fcdb18f`. The [new certificate and audit](result.json) have ledger `937010b12e4ad66a0b4ac5b51d9843564536986407a3f9af4983634266d8a3e9`. They record signed sum 104, excess-degree weighted sum 140, A's X projection {2,3,4,5} and B's M projection {1}. The exact D112 growth premises pass, with zero numerical growth applications.

The original D122 obstruction was inspected read-only and remains valid for its fixed labeled core. The accepted D124 certificate was rechecked once on its own original using archived labels. D126 closes the only uncovered triple within D125's stated ordered even–odd–even minima.

| Declared control on the frozen target | Verified outcome |
| --- | --- |
| Wrong expected digest | Unchanged checker rejects the identity mismatch. |
| Swap X index 1 and Z index 2 | Weight 3 repeats on X index 1 and Z index 3. Weight 10 repeats on X index 5 and Z index 2. Weights 4 and 11 are missing, with pins and alphabet preserved. |
| Move B label 3 to M | Row eligibility passes. Weight 11 repeats at (M,3) and (Z,5), weight 13 is missing, and quotas become (2,3) in M/Z order. |
| Replace A label 6 and weight 4 by label 5 and weight 3 | Both local allocations pass, including the changed A pair {5,11}. Global compatibility rejects duplicate label 5 and weight 3 and missing label 6 and weight 4. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [supervised verification](command_receipt.json). The [combined receipt](verification_supervision.json) records 0.34375 process-CPU seconds and 1.068118 supervised wall seconds. Both standard-error records are empty. One explicit construction, two positive reservations, one certificate, one retained positive recheck, one adverse binding inspection and four controls were recorded. [Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs and raw line endings preserved.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_634_2_MODIFIED_SHARED_MIDDLE_CORE_001/supervise.ps1'
$frozen = 'a8682132994a5150d9407d918b2be9bed0f2a3969f25261c49513b57288745c8'
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only after preflight passes.
& $runner -Phase verify -FrozenConfig $frozen
```
