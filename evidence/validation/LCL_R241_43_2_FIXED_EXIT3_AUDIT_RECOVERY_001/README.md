# D100 versioned audit recovery

`LCL-R241-43-2-FIXED-EXIT3-AUDIT-RECOVERY-001` · November 23, 2026, Pacific/Honolulu · parent `cc4b25328b359dc05f47097b9ff743bea3e13cce`.

[Frozen recovery contract](CONTRACT.md) · [Accepted proof](../../../research/R241_43_2_FIXED_EXIT3.md) · [Original INCOMPLETE execution](../LCL_R241_43_2_FIXED_EXIT3_001/command_receipt.json) · [Exact auditor diff](audit.patch) · [Preflight](preflight_receipt.json) · [Recovery receipt](command_receipt.json) · [Case data, audit and actual controls](result.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**PASS** for this separate recovery. **ACCEPT** the existing structural obstruction and **REJECT** A(14,9;x,3) for integer x in [0,8] on the exact frozen ordered original `[[4,3],[2]]`, at cut 9 and physical s:1=12. The original D100 execution remains **INCOMPLETE** byte for byte. Its missing result and controls were never written. This bundle records fresh recovery outputs.

The recovered auditor reconstructs the target topology, bipartition, degree vector and signed equation, verifies the forced representations of differences 13 through 10, and checks all eight scalar contradictions. It uses the cited repeated weight as a membership test with multiplicity at least two. It separately checks that two distinct original incidences realize the asserted weight, and records every repeat among the six fixed incidence weights. The forced-palette contradiction in the (4,7) row is recorded separately using weights {2,4,5}. For a right-terminal witness, the forced label belongs to the palette and both eligible indexed leaves have only the physical right center as a neighbor. The evidence leaves the terminal index unassigned.

For A=13, B=10, x=6, z=5, the fixed weights in spine, three attachment and increasing right-terminal-label order are 6,7,4,7,4,6. The full multiplicities of the repeated weights are {4:2,6:2,7:2}. The two actual attachments s:0–b:0:0 and s:1–b:1:0 each have weight 7.

The task-local producer and preflight were copied byte for byte. Within the auditor, the diff replaces the singleton repeat check, strengthens the named witness verification, records repeat counts and checks the archived D100 INCOMPLETE disposition. All other assertions were inspected before invocation for dependencies on uniqueness or dictionary order. The unchanged checker rechecked the retained D098 positive. The expected-digest and physical-offset adverse probes were rejected. The terminal swap preserved the vertex alphabet and failed the difference inventory by repeating 5 and 7 and omitting 4 and 8.

One parse-only preflight checked 45 source pins and four recovery inputs. The sole recovery invocation used 0.15625 process-CPU seconds with one worker, eight scalar cases, one retained positive recheck and three adverse controls. It created zero graph identities or target certificates and executed zero joins, exit-offset tests or port sweeps, solvers, assignment visits, search states or nodes, retries, restarts or historical replays. The manifest binds the original D100 failure and old bundle, frozen D099 target and its separate result, unchanged proof and checker, and the D083 and D093 original and versioned dispositions. Both protected upstream main pins and baseline identities were preserved.

## Reproduction

Use a disposable checkout at the recorded parent with pinned project-local Python. Copy the recovery sources, contract, exact diff and configuration to their recorded paths. Leave the recovery output paths vacant. Execute the recovery preflight once and proceed only if it passes.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_FIXED_EXIT3_AUDIT_RECOVERY_001/preflight.py f29245341b0a8a489293618f86e2bf12bfed7f905152b716689a249d080d09d0
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_FIXED_EXIT3_AUDIT_RECOVERY_001/run.py
```

Compare the eight case records, control outcomes, frozen hashes and audit disposition. Timing and invocation paths describe the individual run.
