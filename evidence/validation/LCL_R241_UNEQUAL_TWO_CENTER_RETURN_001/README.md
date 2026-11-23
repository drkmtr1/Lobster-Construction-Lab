# D081 exact originals and validation

[Proof](../../../research/R241_UNEQUAL_TWO_CENTER_RETURN.md) · [Task packet](../../../tasks/LCL_Codex_D081_Unequal_TwoCenter_R241_Return_2026-11-22.md) · [Pre-execution intake](INTAKE.md) · [Separate reviews](REVIEWS.md)

| Named original | Physical offsets | Successful / visited |
| --- | --- | ---: |
| `[[1,2],[1]]` | (1,0) | 0 / 144 |
| `[[1,2],[1]]` | (2,0) | 2 / 144 |
| `[[1,2],[2]]` | (1,0) | 4 / 576 |

The two products on the first graph share its graph digest and are disjoint because s:0 has a different pin. All 864 visits preserve the indexed leaves and distinct named centers. A row saves its rank, two free-label permutations and either a positive marker or two distinct original edge indices and their repeated weight. All six positive rows have complete checker certificates. Two coincide with the explicit alternate and neighboring control ledgers. The independent audit reconstructs the graph topology and class domains, checks the exact Cartesian factorial ranks and original-edge falsifiers for every negative, and checks every affirmative spectrum. It adds no enumeration visits.

The eight fixed certificates cover the alternate state, F(0), retained D079 F(1), F(2), F(4), normalized R(2,1), normalized R(3,2), and their repeated original with L=5. Seven original identities were produced, and the exact F(1) graph and ledger were reused by archive hashes. F(0) retains both named direct-leaf attachments. The repeated original has 43 vertices and prefix low size 18. At s:7 the shifted port is 24, with R=[18,22], D=[1,5] and path labels (24,19,22,18,20,21). Internal states have no separate manufactured graph record. The symbolic R/M interleaving adds no finite case. [Certificates and adverse checks](certificates.json) · [Audit](audit_result.json)

The unchanged verifier rejects the false expected digest. A low-label swap at the actual R(2,1) incoming port rejects the false R241 offset on disjoint original blocks. The suffix check rejects D=[2,3,4,5] on the retained repeated original. All three probes are in memory and preserve the source graphs. Validation used 0.546875 combined process-CPU seconds, one worker, zero solver calls, retries or replay. [Command receipt](command_receipts.json)

## Reproduction

Use a disposable checkout at parent `0841a681219a4445741265998ddbeb1ffc57e38d`. Keep HEAD there. Copy the exact published raw bytes of the new proof and task packet plus this bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `run.py`, `audit.py` and `driver.py` to their published paths. Keep the sources and archives from the parent and match the project-local runtime and identities in [identity.json](identity.json). Leave all generated outputs absent. From the repository root run the driver command in [commands.json](commands.json) once. The guard checks the raw config and unoccupied outputs before starting the producer and auditor in order. An interrupted or discrepant run preserves its available output for review.

[Raw manifest](MANIFEST.json) binds every bundle file except itself, plus the external proof and task packet.
