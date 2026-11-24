# D094 binary composition of D090 and D093

`LCL-R241-D090-D093-JOINT-001` · November 23, 2026, Pacific/Honolulu · parent `cbc5656eae1df54d9ea9d7a38280b7aa486a1183`.

[Symbolic proof](../../../research/R241_D090_D093_JOINT.md) · [Named original](original.json) · [Certificate and independent audit](result.json) · [Syntax preflight](preflight_receipt.json) · [Official receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [Manifest](MANIFEST.json)

**ACCEPT** A(a+b+c+d+40,a+b+20;3,3) on the exact ordered original `[[2,a],[2],[3,b],[3],[3],[3,d],[2],[2,c]]` for independent exact integers a,b,c,d≥2. The proof verifies one binary placement, D090 as old B and D093 as new A. Their given physical equality y_B=x_A=5 is realized at one actual connector s:3–s:4, of weight c+d+20. The quantified proof establishes the state, and the sole all-two boundary certificate corroborates it.

| Boundary item | Value |
| --- | --- |
| Profile | `[[2,2],[2],[3,2],[3],[3],[3,2],[2],[2,2]]` |
| Order, edge count, cut | 48, 47, 24 |
| Original spine labels | (3,47,10,42,18,34,23,27) |
| Cross-component edge | s:3–s:4, difference 24 |
| Joint label bands | [0,12], [13,23], [24,36], [37,47] |
| Joint difference bands | [1,23], {24}, [25,47] |
| Unused resources | No labels or differences |
| Original graph digest | `3a92a6a7457223a75c058faedc27e13839b1c5b8a9e9bb7aa5de49f64b2f4cb5` |
| Distinct labeling ledger ID | `edc758c791cd8f4b11996912aa19f912651552db4f1d11898aa1c7a499feb9a8` |

One syntax and raw-hash preflight parsed the complete producer and auditor with standard-library `ast.parse`. It confirmed 17 and 10 unique top-level function definitions, respectively, and checked the pinned runtime and vacant official output paths. It imported neither task module and created no bytecode cache.

The sole official Python 3.13.17 sequence used 0.203125 process-CPU seconds with one worker. It emitted one new original and certificate, verified the sole cross-component incidence and rechecked D090 and recovered D093 on their distinct retained originals. The unchanged checker rejected a false expected graph digest. The task-local interface gate rejected the nonedge s:3–s:5, and the inventory gate rejected the omission of weight 24. The independent auditor rebuilt the original and verified all label and edge inventories and the exact omissions in the adverse checks. The run made zero solver calls, complete-assignment visits, search states or nodes, retries, restarts or replays.

D091 and D092 retain their own exact exclusions. D093's original **INCOMPLETE** bundle was bound byte for byte, and the recovered **PASS** certificate is a distinct record. The proof and both archives retain their original dispositions.

## Reproduction

For separately authorized reproduction use a disposable checkout at the recorded parent. Copy exact published `run.py`, `audit.py`, `preflight.py`, `config.json`, root and bundle `.gitattributes`, and [proof](../../../research/R241_D090_D093_JOINT.md) into their original paths. Keep HEAD at the recorded parent and verify the source, configuration and project-local executable hashes. Leave `preflight_receipt.json`, `original.json`, `result.json`, and `command_receipt.json` absent. From the checkout root, run the preflight once, then proceed with the official invocation only when the preflight reports PASS and its raw hash bindings still match.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D090_D093_JOINT_001/preflight.py 7005fc04e1b8cac9a14a3b1871833e4b0cad0e1d6c55933dbd36b096270a2be7
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D090_D093_JOINT_001/run.py
```

The official command builds the named original directly, runs the independent audit, and writes its result and receipt. Compare the verified graph, label, spectrum and source identities. Timings and invocation paths reflect the fresh environment.
