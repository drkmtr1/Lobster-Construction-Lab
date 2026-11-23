# D092 fixed (5,3) return capacity test

`LCL-R241-43-PORT53-RETURN-001` · November 23, 2026, Pacific/Honolulu · parent `71861712d5e9eee6a0e0d39d157c299cff720c33`.

[Proof](../../../research/R241_43_PORT53_RETURN.md) · [Named original](original.json) · [Arithmetic audit and controls](result.json) · [Command receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** the structural proof. **REJECT — EXCLUDED** A(11,6;5,3) on exact named `[[4],[3]]` with s:0 low, cut six, s:0=5 and s:1=9. The original has eleven vertices, ten actual edges and witness s:0–s:1. Its canonical graph digest is `458b5d21b3927d5a24ccf901372cb88a1ebbcb0d9d8e57906496d41dd60d9db6`.

The signed degree sum 55=29+4A−3z forces (A,z)=(8,2) after four numerical first-center cases. The right terminal with label 6 repeats the actual spine's weight four. The only pair giving weight ten is split between nonadjacent terminals. D078's (1,1) supplier for the same tree and D090's (3,5) family retain their accepted scopes. D091's proof and original are frozen and bound here without replay. Its distinct parity contradiction and documented algebra correction are preserved.

One Python 3.13.17 worker used 0.03125 process-CPU seconds. The sole official sequence checked one new original, one physical state, four numerical cases, one retained D090 positive and three adverse rejections. The unchanged verifier rejected the false digest and retained cross-center swap of l:0:0:1 and l:0:1:1, which duplicates weights 15 and 17 and omits 14 and 18. The task-local interface gate rejected declared (3,4) on the same retained original with actual offsets (3,5). The independent audit checked the original multiplicities, each case and both actual-incidence contradictions. New certificates, complete-assignment visits, search states or nodes, solver calls, joins, restarts, retries and replays were all zero.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the published `run.py`, `audit.py`, `config.json`, root and bundle `.gitattributes` and [proof](../../../research/R241_43_PORT53_RETURN.md) into their original paths. Keep the parent HEAD. Verify the receipt's three task input hashes, the configured raw source hashes and the project-local Python executable hash. Leave `original.json`, `result.json` and `command_receipt.json` absent. Run once from the checkout root:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_PORT53_RETURN_001/run.py
```

The command writes the named original, runs the standard-library audit and writes the result and receipt. Compare scientific results and source bindings. Runtime timing and invocation paths reflect the fresh environment.
