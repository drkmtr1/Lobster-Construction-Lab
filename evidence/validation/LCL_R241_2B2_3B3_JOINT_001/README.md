# D090 original four-section R241 composition

`LCL-R241-2B2-3B3-JOINT-001` · November 23, 2026, Pacific/Honolulu · parent `830c36b931b02a03e99e8b3ba4b4f778f178db38`.

[Proof](../../../research/R241_2B2_3B3_JOINT.md) · [Named original](original.json) · [Full certificate, controls and independent audit](result.json) · [Execution receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** independent normalized A(a+b+20,a+b+9;3,5) on the exact named `[[2,a],[2],[3,b],[3]]` original for every integer pair a,b≥2. The two independently supplied blocks have local offsets (3,4) and (4,5). Use D087 as old B and D089 as new A. The joint proof accounts for every named edge and for both inventories. The finite boundary certificate corroborates the symbolic proof.

| Boundary item | Value |
|---|---|
| Exact profile | `[[2,2],[2],[3,2],[3]]` |
| Order, size and alpha cut | 24, 23 and 13 |
| Physical spine labels | (3,23,10,18) |
| Sole cross-block original edge | s:1–s:2, weight 13 |
| Global label bands, in order | [0,5], [6,12], [13,18], [19,23] |
| Global difference bands, in order | [1,12], {13}, [14,23] |
| Unused labels and differences | both empty |
| Original graph digest | `ff3c03a17863bbf33bdd2e7d4cc452310740f967198d97045bcc3158b9683786` |
| Distinct labeling ledger ID | `66f5cb9407d61b85705675c509ed6b3bd3defa84408668f3b6a166f029558b06` |

The sole official producer and independent audit used 0.203125 process-CPU seconds on one worker. They verified one new original and certificate and one original connector. They checked the archived D087 and D089 positives on their own named originals and hash-bound D088's scoped negative. The unchanged checker rejected a wrong graph digest. The task-local interface gate rejected the declared s:1–s:3 edge, and the task-local inventory gate rejected the removal of the connector singleton. The independent audit recovered the actual singleton from the original edges and verified that its deletion omits exactly weight 13. There were zero solver calls, assignment visits, search states or nodes, retries, restarts or historical replays.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact published `run.py`, `audit.py`, `config.json`, bundle and root `.gitattributes` and [proof](../../../research/R241_2B2_3B3_JOINT.md) into their original paths. Keep HEAD at the recorded parent. Check the three input SHA-256 pins in the receipt, as well as the configured source and project-local runtime hashes. Leave `original.json`, `result.json` and `command_receipt.json` absent. Run once from the repository root:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_2B2_3B3_JOINT_001/run.py
```

The run freezes the original before assigning labels, executes the standard-library audit in the same process and creates those three files. Compare the scientific results and source identities to the archive. Timing and invocation path fields reflect the fresh environment.
