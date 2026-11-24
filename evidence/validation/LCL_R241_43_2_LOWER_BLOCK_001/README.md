# D099 lower-block challenge evidence

`LCL-R241-43-2-LOWER-BLOCK-001` · November 23, 2026, Pacific/Honolulu · parent `b49c028a26fc7c46970930e3eaa0097c401ef5d3`.

[Frozen contract](CONTRACT.md) · [Proof](../../../research/R241_43_2_LOWER_BLOCK.md) · [Original target](original.json) · [Ledgers and all nine diagnostics](result.json) · [Preflight](preflight_receipt.json) · [Execution receipt](command_receipt.json) · [Independent reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**REJECT** the exact one-leaf placement at `b:0:1` on ordered `[[4,3],[2]]`. The domain is the nine allowed thresholds on the two explicitly supplied `[[4,2],[2]]` ledgers. The unchanged original-target checker rejects every placement. Each placement gives the complete label alphabet at cut 9, with its original spine and numerical offsets intact. Each repeats one difference and omits one. The source theorem remains valid under its complete premise.

| Record | Identity |
| --- | --- |
| Retained source graph | `c602b9934b690cf8bc23e1533840815d1f0ebdc3156f51c361b66c014d9480a0` |
| Ledger I at (3,4) | `66750924e7057c3b304ac56021039b3fcded589741ab5b25d2930e8f25ddd658` |
| Ledger II at (4,0) | `dcd8c6c195e50963296d08981ba4a257a1e8231180ebd4b7b55ac83c6641cc07` |
| Target graph at all thresholds | `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6` |
| Only new incidence | `b:0:1--l:0:1:2` |

Each saved row records selected vertex names, all selected old incidence triples, and actual, required, extra and absent weights with multiplicity. It also gives the fresh-leaf value and weight, every target label, all 13 target incidence triples, the complete difference inventory, explicit repeated and missing weights, physical interface and checker receipt. The independent audit reconstructs both physical originals, verifies the one-edge topology delta, checks reflection via `13-d` and independently computes the placements by inserting the fresh name in label order.

The retained D098 certificate and its reflection both passed the unchanged checker on the same retained original. The three separate adverse controls rejected a false expected digest through the checker, false numerical offsets through the physical interface and a malformed wrong-host edge through the original-incidence gate. The malformed claim produced no additional graph record.

One parse-only preflight passed with 26 source pins and four task inputs. The sole official invocation used 0.15625 process-CPU seconds with one worker, two supplied ledgers, nine thresholds, one new target identity, one retained positive recheck, three adverse controls and zero accepted target certificates. Solvers, joins, assignment visits or states, retries, restarts and replays were zero. Seventy-four retained manifest entries matched at intake. Historical D083 and D093 initial **INCOMPLETE** and separate **PASS** dispositions, D088, deferred D076, both baseline identities and both upstream pins were preserved.

## Reproduction

Use a disposable worktree at the recorded parent with pinned project-local Python. Copy the frozen task sources, configuration, contract, proof and applicable Git attributes into their recorded paths. Start with the preflight receipt, target original, results and command receipt paths vacant. Run the preflight once and proceed only after PASS.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/preflight.py fadeda4ab239e7b367e9a104c19044177df56e2dcfef610039484ff7cb0ebafa
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/run.py
```

Regenerated names, labels, all nine spectra, checker and audit results and adverses should agree. Timing and invocation paths describe the individual run.
