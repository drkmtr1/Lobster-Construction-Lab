# D086 fixed physical port — evidence and reproduction

`LCL-R241-242-PORT-34-001` · November 23, 2026, Pacific/Honolulu · parent `b3dc05a811e21ccb1fabba8889462f826fb760a0`.

[Proof and exact named ledger](../../../research/R241_242_PORT_34.md) · [Original graph](original.json) · [Result and independent audit](result.json) · [Execution receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**WITNESSED** A(13,8;3,4) on the exact named `[[2,4],[2]]` original. Graph digest `7b10b6b54067ddd72ab79eb80eaaa8be69a0e40dd5d7fd0c31f8c41cb68ef2bf` binds all 13 vertices and 12 incidences. Ledger ID `6946174e3601f4be7f4993515d316a4c92b5cdf86549b2afe8c6013e56bf64fe` binds the verified labeling to that graph. The physical spine s:0–s:1 has labels 3 and 12. The [candidate](candidate.json) is the exact user-supplied map. Its independent audit checked the signed-degree equation, four forced (A,B) arithmetic cases, all original differences, both residual inventories and the complete comparison with D085.

One CPU-only process on project-local Python 3.13.17 froze the sole original before verifying the single new certificate. The unchanged checker rechecked D084 and D085 at (3,4) on their own original identities. D082's historical (1,0) exclusion was bound without replay. The unchanged checker rejected a false graph digest and a swap of l:0:0:0 with l:0:1:0, whose actual differences repeat 5 and 7. The separate physical-port gate rejected declaration (3,3). The combined process-CPU measurement was 0.171875 seconds, sampled before writing the final receipt. No complete assignments were enumerated. There were zero solver calls, search nodes, assignment-search states, R241 joins, retries, restarts and historical replays.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact published `run.py`, `audit.py`, `candidate.json`, `config.json` and bundle `.gitattributes` into their original paths. Copy the proof and repository-root `.gitattributes` from the published D086 checkpoint. Keep HEAD at the parent, verify its identity, validate the configuration and runtime SHA-256 pins, and check the four local input hashes in the executed receipt. The official shell gated HEAD, tracking, local input hashes and vacant output paths. Leave `original.json`, `result.json` and `command_receipt.json` absent in the disposable bundle. With the same pinned project-local Python executable, run once from the project root:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_242_PORT_34_001/run.py
```

The invocation saves its own original, result, and receipt. Its timing is specific to that invocation.
