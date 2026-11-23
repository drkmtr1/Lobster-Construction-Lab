# D087 symbolic supplier — evidence and reproduction

`LCL-R241-2B2-SYMBOLIC-PORT34-001` · November 23, 2026, Pacific/Honolulu · verified parent `98749555fb483ef258fa9cf040f092f2520d6636`.

[Symbolic proof](../../../research/R241_2B2_SYMBOLIC_PORT34.md) · [b=5 named original](original.json) · [Regression certificate and audit](result.json) · [Execution receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

The proof independently supplies A(b+9,b+4;3,4) on exact `[[2,b],[2]]` for every integer b≥2. Its quantified conclusions follow from the named label and edge partitions in the proof. The finite checks examine only b=2,3,4 as retained controls and b=5 as the one new regression.

The b=5 original digest is `ccb523e1bd406c19fe080e111589c6d5a340b8277590ef0f427a943a199dd520`, with 14 named vertices and 13 original edges. The formula's ledger ID is `9a81b7d472fec9ae756b2a8019d3f149199d44405cd3e76477930980fa5bd3c3`. The physical spine labels are 3 and 13 at cut nine. The single official Python 3.13.17 process saved the original before instantiating the labels, checked that one new certificate through the unchanged original-target verifier, and ran the separate standard-library arithmetic audit. It rechecked the three archived certificates on their own graph digests and confirmed per-center palettes and physical offsets. The audit records four differently assigned terminal indices at b=2, two at b=3, and zero at b=4. The archived D082 (1,0) exclusion is bound by raw hashes, with no replay.

The checker rejected the false original digest and the swap of l:0:0:0 with l:0:1:0 at b=5. The swap preserves the label alphabet and repeats actual differences 6 and 8, each twice, leaving 5 and 9 missing. The task-local gate rejected the false physical-offset declaration. The single worker used 0.203125 process-CPU seconds, sampled before the final receipt write. There were zero solver calls, complete-assignment visits, search states or nodes, joins, retries, restarts and historical replays.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact published `run.py`, `audit.py`, `config.json` and bundle `.gitattributes` bytes to their original paths. Also copy the proof and repository-root `.gitattributes` as recorded at the D087 checkpoint. Keep HEAD at the recorded parent, verify its identity and the three local input hashes in the receipt, and retain the configured source and runtime bindings. The official invocation's shell checked HEAD, tracking SHA, input hashes and vacant outputs. Leave `original.json`, `result.json` and `command_receipt.json` absent in the disposable bundle. Use the same pinned project-local Python executable from the repository root:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_2B2_SYMBOLIC_PORT34_001/run.py
```

The single invocation writes its own original, result and receipt. Its timing is specific to that invocation.
