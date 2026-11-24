# D093 versioned executable verification recovery

`LCL-R241-D090-REVERSE-BANDSWAP-RECOVERY-001` · November 23, 2026, Pacific/Honolulu · parent `597cf7501eea7d07b5019fe38545a9db2a4bcc94`.

[Accepted proof](../../../research/R241_D090_REVERSE_BANDSWAP.md) · [Original INCOMPLETE attempt](../LCL_R241_D090_REVERSE_BANDSWAP_001/README.md) · [Minimal source diff](audit.patch) · [Syntax receipt](preflight_receipt.json) · [Named target](original.json) · [Certificate and audit](result.json) · [Official receipt](command_receipt.json) · [Reviews](REVIEWS.md) · [Manifest](MANIFEST.json)

**Recovery PASS.** The existing D093 theorem independently supplies A(a+b+20,11;5,3) on exact named `[[3],[3,b],[2],[2,a]]` for all exact integers a,b≥2. This executable recovery checks the sole case a=b=2. The original D093 executable outcome remains **INCOMPLETE**, with its sources and records preserved byte for byte.

## Minimal repair and binding

The failed auditor has 404 lines. The recovery auditor preserves raw bytes 0 through 12,645 inclusive through the closing return-dictionary brace on line 233, then appends LF. The removed 10,259-byte suffix starts with the second definition of `match_prior_manifest` on that same line and ends at line 404. Its bytes are identical to the first block starting at line 62 through the closing brace of the first `check` function, with its final LF restored. This comparison verifies every duplicated function and confirms that the removal omits no unique assertion or logic. The source diff shows the repaired boundary and every deleted line.

| Identity | SHA-256 |
| --- | --- |
| Frozen failed audit.py | `f8caa832dfabe516c9eaa01794200221269dc1bfcce677cdd71aee3b642c046d` |
| Recovery audit.py | `26e7596c09fbe48d818efa347f62ca330d4ed3d9d2d6114850e61229eedcba86` |
| Byte-identical producer in both bundles | `f4fdfa3d6cc5cf28c2d26c6d92ffb5df4c104f9a165493627a221658d6cd71b1` |

The new configuration binds 33 retained sources and artifacts, including every member and the manifest of the failed bundle. It names the new task and parent, sets the preflight source pins, and preserves the boundary, retained controls and every original official cap.

## Boundary verification

The 24-vertex, 23-edge target is `[[3],[3,2],[2],[2,2]]`. The unchanged checker passed the full named ledger. The independent audit rebuilt both originals and verified section reversal with the branch and terminal indices preserved, every edge and multiplicity, all label bands and the exact `24−d` calculation for every corresponding edge. The spine labels are (5,21,10,14) at cut 11 with offsets (5,3). Its middle edge s:1–s:2 has weight 11. The complete spectrum is 1 through 23, both unused inventories are empty, and the target graph digest and ledger ID differ from the retained D090 identifiers.

| Boundary identity | Value |
| --- | --- |
| Target graph digest | `5cd81d04a84488e898e598d4a58e577d821358f3fc4ab987ec4aa5f41f66f9a3` |
| Target ledger ID | `7608435b0caddd7831294906d525ecf14867fb3734387a3297e11f7a064c7fe9` |
| Difference bands | former D087 [1,10], original connector {11}, former D089 [12,23] |

The checker rechecked D090 on its own original, rejected a false target digest and rejected the 2↔8 swap at l:0:0:0 and l:2:0:0. The swap leaves the label alphabet intact, repeats weight 9 three times and omits 3 and 15. The original-bound physical gate rejected declared offsets (5,4). D091 and D092 remain scoped negative evidence with their hashes bound and zero replays.

One syntax preflight parsed the exact source bytes with standard-library `ast.parse`, confirmed 14 producer and nine auditor top-level function definitions, verified the runtime and raw source hashes and left the official outputs vacant. It imported neither task module and created no bytecode cache. One official Python 3.13.17 worker used 0.078125 process-CPU seconds, and produced one original and one certificate, one retained positive recheck and three adverse rejections. Solver calls, complete-assignment visits, search states and nodes, new joins, retries, restarts and historical replays were zero.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact recovery `run.py`, `audit.py`, `preflight.py`, `config.json`, and bundle `.gitattributes` to the published paths. Verify all frozen raw hash bindings. Leave `preflight_receipt.json`, `original.json`, `result.json` and `command_receipt.json` absent. From the checkout root, using the pinned project-local executable, run the preflight once and proceed with the official invocation only after its receipt shows PASS and its raw input hashes still match.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D090_REVERSE_BANDSWAP_RECOVERY_001/preflight.py be086acce92080b0e60ae1df272e43e03a5d982b56621593d7bcdfc75bc8bc5b
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D090_REVERSE_BANDSWAP_RECOVERY_001/run.py
```

Source and verification identities are deterministic. Invocation paths and timings reflect the fresh environment.
