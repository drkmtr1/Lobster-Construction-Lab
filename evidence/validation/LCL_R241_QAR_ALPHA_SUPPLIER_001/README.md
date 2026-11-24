# D097 three-quota alpha supplier evidence

`LCL-R241-QAR-ALPHA-SUPPLIER-001` · November 23, 2026, Pacific/Honolulu · parent `7da574dbcef308f9d0f9340a7735844bdc00182f`.

[Frozen contract](CONTRACT.md) · [Symbolic proof](../../../research/R241_QAR_ALPHA_SUPPLIER.md) · [Named original](original.json) · [Certificate and independent audit](result.json) · [Syntax preflight](preflight_receipt.json) · [Execution receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** A(q+a+r+5,q+a+2;q+1,q+2) on ordered `[[q,a],[r]]` for exact integers q,a≥2 and r≥q. The eight edge groups exhaust the spectrum, with the eighth group empty on the capacity boundary. Below r=q the prescribed exit offset exceeds the available high alphabet.

| Sole new original | q=4, a=2, r=4 |
| --- | --- |
| Ordered profile | `[[4,2],[4]]` |
| Vertices, edges and cut | 15, 14, 8 |
| Spine labels and offsets | (5,14), (5,6) |
| Center labels `b:0:0`, `b:0:1`, `b:1:0` | 9, 8, 0 |
| Terminal labels in their indexed groups | (1,2,3,4), (6,7), (10,11,12,13) |
| Exact edge-order weights | 9, 4, 8, 7, 6, 5, 3, 2, 1, 14, 10, 11, 12, 13 |
| Unused labels and differences | Both empty |
| Graph digest | `bc6a36015e6068ddcb30f384464072f32829b490de4c05921dc33b557570e8de` |
| Labeling ledger ID | `3b4867acd7d69f71e525b27c25a8d10b6eea5a00129cb26547455f2cba29513f` |

The D089 q=3,a=2,r=3 and D096 q=2,a=2,r=3 certificates agree pointwise with the indexed formula and pass the unchanged checker on their respective originals. Independent audit reconstructs all incidences and bands for all three records without importing production modules. D096 exercises the fresh-right band [11] on an existing original. The wrong expected digest and corrupted certificate are rejected by the unchanged checker, and the false offset is rejected by the physical interface gate. The swapped terminal labels repeat 3 and 7 and omit 2 and 8.

One parse-only preflight checked four task inputs, 34 source pins, the project-local Python runtime and unique source definitions. One official verification sequence used 0.09375 process-CPU seconds with one worker, one new original and certificate, two retained rechecks and three adverse probes. Joins, solver calls, assignment visits, search states and nodes, retries, restarts and replays were zero. At intake 81 retained raw manifest records matched. D083 and D093 each retain their original **INCOMPLETE** and separate **PASS** records. The D088 fixed-port exclusion, baseline object and peeled commit, and both upstream main pins remain preserved.

## Reproduction

Use a disposable worktree at the recorded parent with the pinned project-local Python. Copy the frozen source, configuration, contract, proof and applicable Git attributes to the recorded paths. Leave the generated preflight receipt, original, result and command receipt paths vacant. Run the preflight once and proceed only after PASS.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_QAR_ALPHA_SUPPLIER_001/preflight.py 803f5d72348e76c3797c226d69b65b4fdd8c7f4a5775caf731c526a058e2b2c0
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_QAR_ALPHA_SUPPLIER_001/run.py
```

The regenerated graph identity, certificate, control arithmetic and audit should match the frozen evidence. Timing and invocation paths describe the individual run.
