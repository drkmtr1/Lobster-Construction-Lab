# D088 fixed-port symbolic exclusion — evidence and reproduction

`LCL-R241-3B2-PORT44-SYMBOLIC-001` · November 23, 2026, Pacific/Honolulu · parent `5e34dd43d46ef239ef837c6042dd650b78c98b22`.

[Symbolic obstruction](../../../research/R241_3B2_PORT44_SYMBOLIC.md) · [b=2 named boundary original](original.json) · [Boundary arithmetic and controls](result.json) · [Official receipt](command_receipt.json) · [Reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**EXCLUDED** A(b+10,b+5;4,4) on exact `[[3,b],[2]]` for every integer b≥2. The four-level argument closes all ten numerical representations using the original incidences. The signed-degree route uses the shared maximum-edge deduction and independently closes its two residual arithmetic cases. The boundary original digest is `870a840435d074dcc62c3c26357a01f2f032859632df87cad843a42c5989a43a`. Its 12 named vertices and 11 original edges are topology evidence. The executable receipt generates no labeling certificate on that original.

The single official Python 3.13.17 sequence reconstructed the boundary original, checked exactly ten extremal representations, returned the signed-degree residual arithmetic, and rechecked D087 b=5 and D086 b=4 on their own retained graphs through the unchanged verifier. D082's exclusion was hash-bound with no replay. The three adverse checks were run against the D087 b=5 certificate. The unchanged checker rejected the false graph digest and the swap of l:0:0:0 with l:0:1:0, which duplicates weights 6 and 8 and omits 5 and 9. The task-local port gate rejected the false (3,3) declaration. One worker used 0.203125 process-CPU seconds. There were zero solver calls, full assignment visits or search states, joins, retries, restarts and replays.

The Python verifier and its independent audit completed with exit 0 and PASS. The outer PowerShell display step then returned 1 on reading the case-sensitive arithmetic fields. A read-only parse verified the saved JSON and its recorded SHA-256 without rerunning the verifier. [Display incident](DISPLAY_NOTE.md)

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact published `run.py`, `audit.py`, `config.json` and bundle `.gitattributes` into their original paths. Copy the proof and the repository-root `.gitattributes` from the D088 checkpoint. Keep HEAD at the recorded parent, verify its identity, the three input SHA-256 pins in the official receipt, and the configured archived source and runtime bytes. Leave `original.json`, `result.json` and `command_receipt.json` absent. Run once with the same project-local executable from the root:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_3B2_PORT44_SYMBOLIC_001/run.py
```

Use `ConvertFrom-Json -AsHashtable` when displaying the saved result in PowerShell so fields such as A and a remain distinct. The standalone official command writes its own original, result and receipt.
