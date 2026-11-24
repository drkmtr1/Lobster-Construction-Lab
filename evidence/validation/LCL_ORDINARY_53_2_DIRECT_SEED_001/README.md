# D111 verification evidence

**ACCEPT** one finite ordinary graceful seed on the [frozen ordered D108 original](../LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json) at physical `s:0=0`, `s:1=14` and `b:1:0=1`. The [proof](../../../research/ORDINARY_53_2_DIRECT_SEED.md) derives the certificate from a fixed core, two reflected pairs, one forced singleton and one midpoint. The [result](result.json) contains the named ledger, independent topology and incidence calculations, every label and weight, and both empty inventories.

The ordinary checker and the physical-pin predicate both passed. The signed sequence in original edge order was `14,12,8,7,6,4,3,2,−1,−5,−11,13,9,10`. These observed signs place the witness outside the single-reversal interfaces excluded by D108–D110. The unchanged checker rechecked D106 on its own original.

| Control on the frozen D111 original | Outcome |
| --- | --- |
| Wrong expected digest | The unchanged checker rejects the digest mismatch alone. |
| Swap 4 and 7 across left centers | The vertex bijection and pins persist. The checker rejects the spectrum. The independent audit shows two weight-2 edges, `s:0--b:0:1` and `b:0:1--l:0:1:1`, and no weight 8. |
| Swap 4 and 5 at the first center | The unchanged checker and pin predicate pass. This is one declared probe and only the constructed seed is archived as a certificate. |
| Complement every label about 14 | The unchanged checker passes. The pins are (14,0,13) in entrance, exit, right-center order, and the pin predicate rejects them. |

[Preflight](preflight_receipt.json) parsed the three pinned Python sources, checked all 194 repository bindings and five task source bindings, verified the pinned runtime and vacant outputs, and imported no task modules or wrote bytecode. The single [official invocation](command_receipt.json) used 0.21875 process-CPU seconds and 0.22997919999761507 in-process wall seconds. The [external supervisor](supervisor_receipt.json) recorded 0.5243008 wall seconds and exit 0 with empty [standard error](official_stderr.txt). One worker, one direct attempt, four residual groups, one new certificate, one retained recheck and four probes were recorded. No new graph, solver, assignment enumeration, search, new profile, join, retries, restarts, replays or successor experiments were recorded.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Independent reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use project-local Python and PowerShell 7 at the project root in a disposable checkout where all official outputs are vacant.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_53_2_DIRECT_SEED_001/preflight.py' '006cd4d2118f19030c9ca406b4be54fc1dfd8b3e9b608ba73d1bab5c476ab777'
# Continue only if the preflight passes.
& 'evidence/validation/LCL_ORDINARY_53_2_DIRECT_SEED_001/supervise.ps1'
```
