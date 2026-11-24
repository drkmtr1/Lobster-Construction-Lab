# D101 maximum-label host evidence

`LCL-R241-42-2-MAXIMUM-HOST-001` · November 23, 2026, Pacific/Honolulu · parent `5bba13b56ec3802a39c8e9d03036a00b61dd2e90`.

[Proof](../../../research/R241_42_2_MAXIMUM_HOST.md) · [Frozen contract](CONTRACT.md) · [Case data, audit and controls](result.json) · [Preflight](preflight_receipt.json) · [Official receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** the structural obstruction and **REJECT** the cut-8 state with physical `b:0:1=12` and both spine ports free on the frozen D098 ordered `[[4,2],[2]]`. The original source digest is `c602b9934b690cf8bc23e1533840815d1f0ebdc3156f51c361b66c014d9480a0`. The conditional D099 target is bound to digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. The source premise failed, so no extension or target certificate was produced.

Signed degrees force an even exit label, 8 or 10, and the maximum edge weights restrict the entrance to 0, 1 or 2. The remaining eleven scalar cases use the actual named spine, attachments and terminal incidences. The independent auditor reconstructs the D098 original, checks all forcing steps against possible original incidences, and verifies each repeated or missing weight. It retains both eligible leaf names instead of assigning an index to a forced label. All already forced repeat multiplicities are saved. In the (x,Y,A,z)=(2,8,9,4) row, for example, weights 4 and 7 occur twice and 6 occurs three times.

The unchanged checker accepted the retained D098 ledger and rejected the bad original digest and corrupt label swap. The maximum-host check rejected the claim that b:0:1 carried 12 in that positive control. Its actual label is 9. The swap preserved the label alphabet and repeated differences 5 and 7 while omitting 4 and 8. The auditor and implementation reviewer inspected the assertions for singleton-repeat assumptions before the run.

One parse-only preflight passed with 52 source pins. 108 retained manifest entries matched at intake. The single official one-worker invocation passed in 0.078125 process-CPU seconds, with eleven scalar cases, one retained positive recheck and three genuine adverse probes. There were zero new original identities, source or target certificates, extensions, solvers, complete assignments, search states or nodes, joins, port sweeps, retries, restarts or historical replays. The distinct D083, D093 and D100 original INCOMPLETE records and versioned PASS records were retained, along with the D099 result, deferred D076, baseline and upstream pins.

## Reproduction

Use a disposable LCL checkout at the recorded parent and the pinned project-local Python. Copy the frozen contract, proof, source and config files to their recorded paths. Leave generated outputs vacant. Run the preflight once and continue only if it passes.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_42_2_MAXIMUM_HOST_001/preflight.py a5b905777ca8411c5efadca38a74510cccadaf11f9175bed4fecbc0d839aabfb
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_42_2_MAXIMUM_HOST_001/run.py
```

Compare the graph digest, exact scalar cases, checked witnesses, control receipts and dispositions. Timing and invocation paths describe the individual run.
