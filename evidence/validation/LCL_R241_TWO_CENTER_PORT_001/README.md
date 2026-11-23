# D079 two-center R241 port evidence

[Proof](../../../research/R241_TWO_CENTER_PORT_FALSIFIER.md) · [Task packet](../../../tasks/LCL_Codex_D079_TwoCenter_R241_Port_Falsifier_2026-11-22.md) · [Intake](INTAKE.md) · [Separate reviews](REVIEWS.md)

| Original | Named domain | Graceful / visited | Physical offsets, with multiplicities |
| --- | --- | ---: | --- |
| `[[1,1],[1]]` | s:0=1, s:1=5 | 0 / 36 | None |
| `[[1,1],[1]]` | Alpha orientation only | 4 / 576 | (1,0) twice, (2,3) twice |
| `[[1,1],[2]]` | s:0=1, s:1=5 | 4 / 144 | (1,1) four times |

All domains use the physical low/high orientation s:0 low and s:1 high. The 36 pinned rows also occur in the 576-row product, so the accounting is 756 visits and 720 distinct assignments across the two named graphs. A row contains ordered low and high permutations for the saved free names, and either null for success or two zero-based original edge indices with their repeated weight. The independent audit reconstructs the original graph and checks the factorial rank of every saved row, two named edge differences per negative, and full spectra for the eight positive rows. It generates zero further candidate assignments. The two explicit positive controls each passed the unchanged checker. The wrong expected digest and the separate mismatched R241 port premise both rejected.

The exact finite counts corroborate the analytic strict-port falsifier. They show alternate offsets for one original and a strict witness for its neighbor. R241 needs the predecessor's physical high exit offset to equal the next module's physical low entrance offset. These finite controls do not prove closure. [Audit](audit_result.json) · [Certificates and adverse checks](certificates.json)

## Reproduction

Use a disposable checkout of parent `abd43466e1333e8c3f792a7e2109fa6cbaed418c`, leaving HEAD there. Copy the raw Git bytes of the new proof, committed task packet, and this bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `run.py`, `audit.py` and `driver.py` into their published paths. Keep all generated files absent and match the runtime and source information in [identity.json](identity.json). From the repository root run only the driver command in [commands.json](commands.json). It binds the exact config, rejects occupied outputs and runs the producer and auditor sequentially. Preserve archived results and any interrupted outputs.

The single run used 0.078125 combined process-CPU seconds with one worker, zero solver calls, retries or historical replays. All bundle files except the manifest itself are byte-bound. The manifest also binds the external proof and task packet. [Command receipt](command_receipts.json) · [Raw-byte manifest](MANIFEST.json)
