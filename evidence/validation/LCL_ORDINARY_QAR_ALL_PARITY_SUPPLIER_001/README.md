# D117 verification evidence

**ACCEPT** the [symbolic ordinary graceful supplier](../../../research/ORDINARY_QAR_ALL_PARITY_SUPPLIER.md) for exact ordered `[[q,a],[r]]`, independent exact integers q≥5, a≥3 and r≥2, and physical pins `s:0=0`, `s:1=q+a+r+4`, `b:1:0=1`. The seed uses R226 to meet the integral left quotas across all four parities. The named D112 growth and a separate direct inventory argument give the final right quota and full spectra. No alpha or signed-edge restriction is imposed.

The [saved audit](result.json) reconstructs [D111](../LCL_ORDINARY_53_2_DIRECT_SEED_001/result.json) and [D114](../LCL_ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER_001/result.json) against their own frozen originals. The unchanged checker rechecked each retained certificate once. The indexed formula agreed pointwise at (5,3,2) and (6,3,2). Both leftover inventories were empty. D111's lower quota uses the midpoint alone, while D114's uses two complete pairs. Both satisfy D112's physical premises. The already accepted D105-to-D106 transition is bound through the archived D112 evidence without replay.

| Declared probe | Verified outcome |
| --- | --- |
| D111 wrong original digest | The unchanged checker rejects the digest mismatch. |
| D111 swap labels 4 and 5 within the higher center | The weights 8 and 7 exchange on the two named incidences. Ordinary gracefulness and D112 compatibility persist, but the indexed formula differs at exactly those terminal names. |
| D114 cross-center swap of labels 6 and 5 | The label bijection, pins and physical quotas persist. Weight 3 repeats on `b:0:0--l:0:0:1` and `b:0:1--l:0:1:2`. Weight 7 repeats on `b:0:0--l:0:0:4` and `b:0:1--l:0:1:1`. Weights 4 and 8 are missing. The unchanged checker rejects. |
| D114 complement about 15 | The ordinary checker accepts. The pins are (15,0,14) in entrance, exit and right-center order. The physical pins and growth-label predicates reject. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [official invocation](command_receipt.json). Preflight verified 299 repository pins, five task source hashes, the configuration, runtime, unique intended definitions and vacant outputs with zero task imports. The audit used 0.1875 process-CPU seconds, 0.2222685000160709 seconds in the child, and 0.4139276 [supervised wall seconds](supervisor_receipt.json). Standard error was [empty](official_stderr.txt). There were one worker, two retained evaluations and rechecks, and four declared controls. There were zero new numerical profiles, graph identities, finite certificates, solver calls, complete-assignment visits, search nodes or states, joins, retries, restarts, historical replays or successor experiments.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Independent reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned Python runtime and PowerShell 7 in a disposable checkout with vacant official outputs.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_QAR_ALL_PARITY_SUPPLIER_001/preflight.py' '1a57c3ae1e99a29c103f90557b788f6eb041256d4b91a999bfc49faa63008f91'
# Continue only after a passing preflight.
& 'evidence/validation/LCL_ORDINARY_QAR_ALL_PARITY_SUPPLIER_001/supervise.ps1'
```
