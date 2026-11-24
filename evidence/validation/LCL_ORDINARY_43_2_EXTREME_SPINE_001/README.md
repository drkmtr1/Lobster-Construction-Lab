# D105 verification evidence

The [direct proof](../../../research/ORDINARY_43_2_EXTREME_SPINE.md) gives an ordinary graceful labeling of the exact frozen ordered [D099 original](../LCL_R241_43_2_LOWER_BLOCK_001/original.json), with physical labels `s:0=0` and `s:1=13`. Its canonical graph digest is `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`.

The [result](result.json) contains the complete original-bound certificate under `certificate` and the 13-edge signed and absolute ledger under `incidence_audit`. Certificate ledger ID is `af0e2be70013710c5b5b64c6c554512adfaad5ae0faa8ab63c146e428ed50a93`. The independent audit reconstructs the original incidences and bipartition and confirms both unused inventories are empty. The sole negative signed edge is `l:0:0:3--b:0:0` with value −1 in the direction from the class containing `s:0`. The degree sum is 89. Neither class order gives an alpha separation. The exact D104 exclusion remains accepted on the same graph.

The [parse-only preflight](preflight_receipt.json) checked all 107 frozen repository pins and imported no task modules. The single [official invocation](command_receipt.json) used one worker, 0.125 process-CPU seconds, 0.13624050002545118 in-process wall seconds and 0.4279599 outer supervised wall seconds. It produced one ordinary certificate and zero new graph identities. The unchanged checker also accepted the retained D098 positive. The false original digest, wrong declared spine labels and invalid terminal swap were genuinely rejected on the D105 original. The swap repeats weights 6 and 7 twice and omits 5 and 8. All solver, complete-assignment, search, additional-profile, join, retry, restart and replay counters are zero.

See the [contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). Historical original and versioned execution receipts remain preserved.

## Reproduction under separate authorization

Use the pinned project-local executable from the project root in a disposable checkout with vacant output paths. Supervise the official invocation with a 60-second outer deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_43_2_EXTREME_SPINE_001/preflight.py 9954997746f5328f18d1691631d6ca960aae31134d9a39eaa26200817398bb81
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_43_2_EXTREME_SPINE_001/run.py
```
