# D091 fixed (5,3) return obstruction

`LCL-R241-42-PORT53-RETURN-001` · November 23, 2026, Pacific/Honolulu · parent `40a77f222bcce61cf4b4a970b6eb59c6ac2b4261`.

[Proof](../../../research/R241_42_PORT53_RETURN.md) · [Named original](original.json) · [Arithmetic audit and controls](result.json) · [Execution receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** the extremal and corrected signed-degree proofs. **REJECT — EXCLUDED** A(10,6;5,3) on the exact named `[[4],[2]]` original with low s:0, cut six, s:0=5 and s:1=9. The original has ten vertices, nine edges and physical spine s:0–s:1. Its canonical graph digest is `066f8e8939b9638ce060a5cdd73a4ee44f811d95c70ab216809fea291a0a9497`. The extremal weights 9, 8 and 7 use all three edges incident to the forced zero center. No original incidence can realize weight six.

The separate degree sum at the same forced z=0 requires 2A=13 and excludes every integer label A. This corrects the packet's proposed inference A=6 from that equality. The label 6 is forced by the separate extremal palette, whose actual weight multiset sums to 43, repeats 4 and omits 6. D078's (1,1) construction on the same original and D090's composed four-section family remain valid.

One Python 3.13.17 worker used 0.171875 process-CPU seconds. The sole official sequence created one original, checked one port pair and ten numerical representations, and issued no new certificate. The D090 certificate passed the unchanged verifier on its own original. The checker rejected the wrong digest and the cross-center terminal swap, which repeats 16 and 18 twice each and omits 15 and 19. The separate physical-port gate rejected the declared offsets (3,4) against the retained physical offsets (3,5). The D087–D089 inputs were hash-bound without replay. All assignment visits, solver calls, search states and nodes, joins, retries and restarts were zero.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact published `run.py`, `audit.py`, `config.json`, bundle and repository root `.gitattributes` and [proof](../../../research/R241_42_PORT53_RETURN.md) into their original paths. Keep HEAD at the recorded parent, verify the three input hashes in the receipt, and check the configured retained sources and project-local runtime hash. Leave `original.json`, `result.json` and `command_receipt.json` absent. Run once from the checkout root:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_42_PORT53_RETURN_001/run.py
```

The command freezes the named original, runs the standard-library audit and creates the three output files. Compare the scientific results and source identities to the archive. Runtime timing and invocation paths reflect the fresh environment.
