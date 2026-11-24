# D096 right-center zero-host extension evidence

`LCL-R241-2AR-ZERO-HOST-001` · November 23, 2026, Pacific/Honolulu · parent `4407901f36d7b7d7ca54d15fa846eba33a68402e`.

[Frozen contract](CONTRACT.md) · [Symbolic proof](../../../research/R241_2AR_ZERO_HOST.md) · [Named original](original.json) · [Certificate and independent audit](result.json) · [Syntax receipt](preflight_receipt.json) · [Official receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

The a=2, r=3 original `[[2,2],[3]]` has 12 vertices, 11 edges and cut six. Its physical ports are `s:0=3` and `s:1=10`, returning offsets (3,4). Its sole added terminal `l:1:0:2=11` attaches to `b:1:0=0` and gives difference 11. The preserved labels are [0,10], the preserved differences are [1,10], and both unused inventories are empty.

- Graph digest `fce38d9f3d5130467a183191f999d24ec93312d1ae4846f2a34fffd8c420974e`. The one emitted original record shares its named identity with D083. The distinct ledger ID is `40c1f4122b0a9a82d446d5bc3d128c91914daad4d3c5190ac60af99c8b5e5093`.
- D083's structural exclusion has physical pins (1,6), versus (3,10) here. Its original execution remains **INCOMPLETE** and the separately versioned audit remains **PASS**. The separate D093 **INCOMPLETE** original and **PASS** recovery also retain their original identities.
- The unchanged checker rechecked the D084 (3,4) certificate on its own `[[2,2],[2]]` original. Two per-center terminal orders differ between that control and the indexed D087 formula; the audit compares each relevant palette and uses the D087 named labels in the new certificate.
- The unchanged checker rejected a false digest. The task-local interface rejected an incorrect offset declaration. An independent recomputation found two occurrences each of differences 3 and 5 and missing differences 2 and 6 after the terminal swap. The unchanged checker rejected that ledger.
- One parse-only preflight checked the frozen local runtime, four task inputs, 32 source pins, the exact top-level function lists and vacant outputs. One official producer/audit invocation used 0.171875 process-CPU seconds. It emitted one original record and one certificate, rechecked one retained positive and rejected three adverse probes. Joins, solvers, assignment visits, search nodes, states, retries, restarts and replays were zero. Raw archived manifest checks matched 86 records at intake.
- The public LCL publication uses the pinned provenance. Both upstream remote main refs matched the retained pins. The Bounded Search working checkout was on a separate recovery branch; it was left untouched.

## Reproduction

Use a disposable checkout at the recorded parent, with the pinned project-local Python runtime. Copy the frozen task sources and configuration, proof and applicable Git attributes into their recorded paths. Leave the four generated receipts and result paths vacant, including `preflight_receipt.json`, `original.json`, `result.json`, and `command_receipt.json`. Run one preflight and proceed to the official invocation only after PASS.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_2AR_ZERO_HOST_001/preflight.py 5dd1e1784b9e0a0592c9c081f79502cea3dc67878e20cf721b8b31229025c357
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_2AR_ZERO_HOST_001/run.py
```

Regenerated arithmetic, original and ledger identity should match the frozen evidence. Invocation paths and timing describe the corresponding run.
