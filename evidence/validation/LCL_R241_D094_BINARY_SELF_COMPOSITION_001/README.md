# D094 binary self-composition evidence

`LCL-R241-D094-BINARY-SELF-COMPOSITION-001` · November 23, 2026, Pacific/Honolulu · parent `1a232fdc6440029eaee278cf26aed23d2c0519a7`.

[Frozen contract](CONTRACT.md) · [Symbolic proof](../../../research/R241_D094_BINARY_SELF_COMPOSITION.md) · [Named original](original.json) · [Certificate and independent audit](result.json) · [Syntax preflight](preflight_receipt.json) · [Official receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT.** The exact ordered 16-section original in the proof supplies A(a+b+c+d+e+f+g+h+80,a+b+e+f+40;3,3) for eight independent exact integer quotas a,b,c,d,e,f,g,h≥2. This is one named binary specialization of the retained R241.1 finite-list rule, using D094 as both independent local suppliers. The boundary corroborates the symbolic proof and preserves every original name and incidence.

| All-two boundary | Value |
| --- | --- |
| Original | `[[2,2],[2],[3,2],[3],[3],[3,2],[2],[2,2],[2,2],[2],[3,2],[3],[3],[3,2],[2],[2,2]]` |
| Order, edge count, cut | 96, 95, 48 |
| Actual spine labels | (3,95,10,90,18,82,23,75,27,71,34,66,42,58,47,51) |
| Actual interblock connector | s:7–s:8 with endpoints 75 and 27, weight 48 |
| Physical ports | s:0=3, s:15=51, offsets (3,3) |
| Label bands | [0,23], [24,47], [48,71], [72,95] |
| Difference bands | [1,47], {48}, [49,95] |
| Unused resources | No labels or differences |
| Original graph digest | `15eaaa6fdfa17413a4d4cc51997c6c027d521f408c8edbfb33e9c54600c41c57` |
| Distinct ledger ID | `b5f5e0a09d5457b33731b82dfed3d56a6f3c8c21b4384eab87f58fafd7840a0c` |

The syntax and raw-hash preflight parsed 15 and nine unique top-level functions in the exact producer and auditor, verified the pinned runtime and initially vacant output paths, and left no task imports or bytecode cache. The sole official Python 3.13.17 sequence used 0.109375 process-CPU seconds, one worker, one original and certificate and one join. It checked the single retained D094 certificate on its own original, and independently audited both named embeddings of it. All three genuine adverse probes were rejected by their intended paths: false expected graph digest by the unchanged checker, false declaration s:7–s:9 by the original-specific gate, and omitted connector weight 48 by the joint-inventory gate.

The independent auditor rebuilt the original names and edge multiplicities, recomputed all 95 differences and checked both full inventories. Both separate reviews passed. There were zero solver calls, assignment visits, search states or nodes, retries, restarts or historical replays. D093's original **INCOMPLETE** and separate recovery **PASS** retain distinct provenance.

## Reproduction

For separately authorized reproduction, use a disposable checkout at the recorded parent. Copy exact published `run.py`, `audit.py`, `preflight.py`, `config.json`, `CONTRACT.md`, root and bundle `.gitattributes`, and [proof](../../../research/R241_D094_BINARY_SELF_COMPOSITION.md) into their original paths. Verify the frozen hashes and keep the parent HEAD. Leave `preflight_receipt.json`, `original.json`, `result.json`, and `command_receipt.json` absent. From the checkout root, run the preflight once. Proceed with the official invocation only if the preflight reports PASS and its raw input hashes still match.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D094_BINARY_SELF_COMPOSITION_001/preflight.py 084e3b20e84c54008a6ac210bde50eb0ae720dd252bfe38851ef671b6b50241e
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D094_BINARY_SELF_COMPOSITION_001/run.py
```

Compare the resulting named graph, certificate, audit and frozen source identities. Timing and invocation paths describe the fresh run.
