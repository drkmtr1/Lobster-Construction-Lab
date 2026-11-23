# R241 paired branched-spine evidence

[Proof](../../../research/R241_PAIRED_BRANCHED_SPINE.md) · [Authorization](../../../tasks/LCL_Codex_R241_Arbitrary_Branched_Spine_2026-11-22.md) · [Roadmap](../../../docs/strategy/LCL_Branched_Spine_Research_Roadmap_2026-11-22.md) · [Strategy handoff](../../../handoffs/CODEX-20261122-r241-paired-branched-spine-intake.md) · [Separate reviews](REVIEWS.md)

One official run supplied the nine declared complete maps T1–T9. Seven originals were written here. T4 and T5 use the byte-bound original files already retained by D060 and D076, respectively. The run did not replay either archive. T4 matches the packet's explicit example, and T5 gives a different label-ledger ID on D076's original named graph. Each certificate includes the entire module/aggregate trace on its original, then the physical exit, both exact used and unused inventories, the actual pending path and the complete checked labeling. The largest graph has 42 vertices.

The three in-memory adverse checks were all rejected. They changed the T4 spine connector, supplied a wrong incoming low-port value at the actual T4 join, and removed difference 1 from the T4 residual inventory. The offset probe checks applicability of the stated R241 placement. The independent auditor builds its own topology and uses a blockwise closed form to check the transient maps. The finite checks corroborate the quantified proof over the declared quota domains.

[Case results and arithmetic audit](audit_result.json) · [Adverse checks](adverse.json) · [Raw command receipt](command_receipts.json) · [Source and runtime identity](identity.json) · [Byte manifest](MANIFEST.json)

## Reproduction

Use a disposable checkout at strategy commit `18ba80ea8b271164a6ba7d7a6c92329c53e3dd6a`. Keep HEAD at that commit. It contains the two immutable attachments, the strategy handoff and the inherited sources and originals. Copy the exact published bytes of the external proof plus this bundle's `.gitattributes`, `config.json`, `commands.json`, `run.py`, `audit.py` and `driver.py` into their published paths. Use the recorded project-local Python runtime. Keep all generated outputs absent. Run the driver command from [commands.json](commands.json) once from the repository root. It checks the frozen config and fresh output paths, starts the producer and arithmetic auditor in sequence and retains the official receipt. On an interrupted or failed run preserve its partial files. The archived bundle is a frozen result.

The official run used 0.234375 combined process-CPU seconds with one worker, zero queries, zero enumeration nodes, zero replays and zero retries. The [manifest](MANIFEST.json) binds every bundle file except itself, plus the external proof. The [strategy handoff](../../../handoffs/CODEX-20261122-r241-paired-branched-spine-intake.md) records the separate original attachment hashes.
