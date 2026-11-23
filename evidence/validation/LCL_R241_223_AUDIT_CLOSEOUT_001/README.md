# D083 audit-only closeout

`LCL-R241-223-AUDIT-CLOSEOUT-001` · verified parent `4f3e5aee98ab43ce1ba5d7bef071ed7922e034c1` · November 22, 2026, Pacific/Honolulu.

**PASS.** The [versioned audit](audit.py) completed the proof arithmetic for the exact 12-vertex, 11-edge original `[[2,2],[3]]`. It reconstructed the six-low, six-high orientation, derived `40+2(A+B)-3z=66`, recovered the three necessary center-label cases, and corroborated that weight 11 forces the remaining case to repeat the original spine's weight 5. This supplies executable verification of the [accepted D083 proof](../../../research/R241_223_STRICT_RETURN.md) for physical pins `s:0=1` and `s:1=6`. The unavailable input still blocks the specific J(a) route.

The [audit result](audit_result.json) records 39 verified input bindings, including the D083 bundle and proof, bound runtime, retained D081 positive certificate, retained D082 negative evidence, and the three archived digest, offset and suffix inventory rejections. The [execution receipt](command_receipt.json) records one CPU-only process, no new graph identities, no named assignment visits or states, and zero solver calls, producer reruns, historical replays, retries or restarts. The original's ordered incidences were reconstructed in memory from its retained profile. The ten unordered numerical center-label pairs are arithmetic checks within the existing proof. The audit used 0.125 process-CPU seconds, sampled before writing its final receipt. The original failed execution still has no combined CPU measurement.

## Source comparison and custody

The [frozen auditor](../LCL_R241_223_STRICT_RETURN_001/audit.py) reused `old` for the D082 topology and the retained D081 component. The revised auditor uses `d082_topology` for both archived digest references. The topology reconstruction, checker-receipt validation and `audit_obstruction()` arithmetic are unchanged. The other changes route input to the frozen sibling bundle, verify its raw manifest and failed receipt, and write bounded output and invocation accounting exclusively to this new directory. The [original execution receipt](../LCL_R241_223_STRICT_RETURN_001/command_receipts.json) remains **INCOMPLETE**. The original producer outputs, proof, reviews and manifest remain frozen.

[Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction

For a separately authorized reproduction, use a disposable checkout of the recorded parent and copy this versioned `audit.py` and its `.gitattributes` into the same bundle path from the published closeout. The versioned script uses raw source and runtime bindings. Keep both output paths in the new bundle absent, and retain the full frozen D083 and earlier evidence at their original paths. Verify the documented project-local Python 3.13.17 executable against the frozen identity. From the repository root the single invocation is:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_223_AUDIT_CLOSEOUT_001/audit.py
```

The command writes only `audit_result.json` and `command_receipt.json` in the versioned bundle. A reproduced receipt has its own timing and invocation identity.
