# D085 two physical offset states — evidence and reproduction

`LCL-R241-232-TWO-PORT-001` · November 23, 2026, Pacific/Honolulu · parent `8c8dc2abbca0a2ba3c2615c4b42410c7383b9ee3`.

[Proof](../../../research/R241_232_TWO_PORT.md) · [Exact named original](original.json) · [State results, certificate and audit](result.json) · [Receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

The exact new original `[[2,3],[2]]` has digest `935716942dfcf80c9b0f0c323872d83772ca870eaae173ba053978468a336174`. Its physical spine witness is s:0–s:1. The 12 vertices and 11 edges are preserved by name, quota and index. At cut seven the physical pair (2,0) is excluded by the 12 ordered center contradictions. The pair (3,4) is witnessed by ledger ID `c021941534f6ac250ad77fdf1fca7d6c21cfae619c6498fca22f66dc7f8114fa`, with s:0=3 and s:1=11. The ledger and structural case inputs are fixed in [cases.json](cases.json). There is no unresolved state in the two-point domain.

The one official Python 3.13.17 process froze one new original, checked one explicit ledger through the unchanged verifier and ran the independent standard-library reconstruction and arithmetic audit. It checked 24 ordered numerical center cases with all first terminals unassigned. It rechecked both D084 positive ledgers on their retained original and bound the D082 historical (1,0) negative without replay. The same unchanged checker rejected a false original digest and a terminal swap that duplicates original-edge weights 4 and 6. The task-local physical-port gate rejected a misdeclared offset. One worker used 0.0625 combined process-CPU seconds, sampled before writing the final receipt. No complete assignment enumeration, search, solver, replay, retry or join was performed.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy the exact published bytes of `run.py`, `audit.py`, `cases.json`, `config.json` and the bundle `.gitattributes` into their original paths. Copy the proof and repository-root `.gitattributes` from the published D085 checkpoint. Keep HEAD at the recorded parent. Verify the runtime and [configuration](config.json) pins and the four local input hashes in the [receipt](command_receipt.json). Keep `original.json`, `result.json` and `command_receipt.json` unoccupied. The official shell checked local HEAD, tracking SHA, local input hashes and empty output paths before launch. From the repository root, use the same project-local Python executable:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_232_TWO_PORT_001/run.py
```

The single invocation writes the original first, then runs the checker and separate audit and records its own timing. Use disposable outputs for reproduction.
