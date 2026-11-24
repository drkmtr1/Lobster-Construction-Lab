# D100 fixed-exit-three proof and stopped audit

`LCL-R241-43-2-FIXED-EXIT3-001` · November 23, 2026, Pacific/Honolulu · parent `7a434bfe299d404cc5cf84cb53df0533c2560ab2`.

[Proof](../../../research/R241_43_2_FIXED_EXIT3.md) · [Frozen contract](CONTRACT.md) · [Retained D099 original](../../../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json) · [Preflight receipt](preflight_receipt.json) · [Official failure receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**Mathematics.** The separate mathematical review accepts the structural obstruction to A(14,9;x,3) on exact ordered `[[4,3],[2]]` for every integer x in [0,8]. The frozen original has digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. The proof provides the exhaustive eight scalar cases and their original-incidence contradictions. It concerns cut 9 and the physical exit label 12.

**Official execution is INCOMPLETE.** The syntax and raw-input preflight passed, including 32 source pins, four exact task inputs, unique function definitions, a pinned project-local Python and vacant outputs. The sole official run reached eight scalar rows and recorded one D098 positive recheck and three adverse controls before the audit assertion stopped it. These counts come from the frozen failure receipt. The individual control receipts, final arithmetic audit and `result.json` were never written. The auditor's final control and historical-status assertions were beyond the stopping point. This closeout does not reconstruct raw outputs from an aborted invocation.

In the case A=13, B=10, x=6, z=5, the spine, three attachments and two right terminal edges give weights 6,7,4,7,4,6. The frozen auditor at [line 139](audit.py#L139) wrongly required the repeated-weight list to equal [7]. The actual repeated weights are 4,6,7. Weight 7 still occurs on two distinct original attachments, which is sufficient for the mathematical contradiction. The failure receipt records the assertion and exit code 1. The sources and receipt remain frozen.

The one-worker invocation used 0.125 process-CPU seconds. New graph identities, accepted certificates, joins, solver calls, assignment visits or states, port sweeps, retries, restarts and replays were zero. No recovery was attempted. Eighty-six archived manifest entries were matched at intake. The historical D083 and D093 original incomplete dispositions and separate successful recoveries, D099, deferred D076, both baseline identities and both upstream pins were preserved.
