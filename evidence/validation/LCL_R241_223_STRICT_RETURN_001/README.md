# D083 original and obstruction evidence

The [structural proof](../../../research/R241_223_STRICT_RETURN.md) excludes the prescribed state `A(12,6;1,0)` on exact original `[[2,2],[3]]`. The original has graph digest `fce38d9f3d5130467a183191f999d24ec93312d1ae4846f2a34fffd8c420974e`. No candidate labeling or joined original was produced. The exact assignment domain has 14,400 elements. The analytic proof resolves it without visiting or recording any assignment. The proposed R241 composition lacks its input state.

The [producer result](result.json) is **COMPLETE**. One new original was saved. The unchanged checker accepted the retained D081 F(2) certificate. The D082 negative is bound to its archived proof, original and enumerated receipt with zero replay. The [controls](controls.json) record rejection by the respective original-graph digest, physical join and suffix inventory checks. Source and runtime bindings are in [identity.json](identity.json) and [config.json](config.json).

The [official execution](command_receipts.json) is **INCOMPLETE**. The producer used 0.109375 process-CPU seconds. Its wall time was about 0.3004 seconds. The independent arithmetic audit exited after about 0.1736 wall seconds at `audit_controls` with `KeyError: 'digest'`. The saved source first bound `old` to the archived D082 topology and later rebound it to the retained D081 F block, which has no digest field. Original reconstruction and control assertions reached the return statement. The proof-arithmetic stage `audit_obstruction` and the final audit result were never reached. No aggregate CPU measurement was recorded. The proof describes intended audit duties. The command receipt records how far execution reached.

The [separate reviews](REVIEWS.md) accept the analytic argument and the saved producer evidence within its scope. The implementation review calls for an additive, separately authorized audit repair that preserves the frozen source and failed receipt. Its minimal proposal is to name the D082 topology binding separately and use that binding in the return. No patch to the frozen audit, audit retry, new enumeration, solver, alternate-port sweep, historical replay or successor was executed.

## Reproduce the recorded attempt

Use a disposable checkout at the recorded parent `c51820f16cc790189e18ecbaa726161225c56fdf`. Copy the exact published bytes of the [task](../../../tasks/LCL_Codex_D083_223_Strict_Return_2026-11-22.md), [proof](../../../research/R241_223_STRICT_RETURN.md), and this bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `run.py`, `audit.py` and `driver.py` into their original paths without advancing HEAD. Copy the D083 root `.gitattributes` as well for raw-byte custody. Keep the producer and audit output paths unoccupied, including `strict_original.json`, `identity.json`, `controls.json`, `result.json`, `audit_result.json` and `command_receipts.json`. Use the documented project-local Python 3.13.17 with the bound runtime and source bytes. From the repository root, the single recorded invocation is:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_223_STRICT_RETURN_001/driver.py
```

The driver runs the producer and then the audit in the recorded order. With the frozen source, the expected outcome is the saved audit error. Reproduction belongs in the disposable checkout under separate authorization. Preserve the published evidence bytes.

The [manifest](MANIFEST.json) binds every other file in this bundle and the external task and proof to their raw bytes. The raw original-file hash is distinct from the graph digest. There is no labeling ledger ID for the rejected D083 state.
