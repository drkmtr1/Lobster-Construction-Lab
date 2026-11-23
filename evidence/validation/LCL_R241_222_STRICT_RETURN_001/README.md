# D082 exact original, strict pins and verification

[Proof](../../../research/R241_222_STRICT_RETURN.md) · [Task specification](../../../tasks/LCL_Codex_D082_222_Strict_Return_2026-11-22.md) · [Verified intake](INTAKE.md) · [Separate reviews](REVIEWS.md)

On original `[[2,2],[2]]` with s:0=1, s:1=6 and normalized cut 6, the complete exact product has zero successful rows out of 2,880. There is one new original and no J(a) original. The signed-degree proof excludes the same pinned state without using the enumeration. No other port was searched.

Each saved row is `[rank, free_low_permutation, free_high_permutation, falsifier]`. Free names and alphabets are saved in the diagnostic. A falsifier consists of two distinct zero-based indices into the retained original edge order and their common weight. The independent audit reconstructs the original named graph and confirms that the two permutation ranks cover the full Cartesian product once each. It checks both original edges of all 2,880 saved falsifiers and generates zero fresh visits. The empty positive list is the exhausted result. The graph digest is an original-identity binding, distinct from the label-ledger binding used for checked certificates. [Original](strict_original.json) · [Ranked rows](enumeration.json) · [Audit](audit_result.json)

The unchanged checker accepted the retained D081 strict positive on `[[1,2],[2]]`. Its digest and ledger match the retained certificate. The negative prescribed-state control `[[1,2],[1]]` binds to D081's exact 0/144 receipt and audit with zero replay visits. The wrong digest rejected at the unchanged checker. The other two probes use the archived D081 repeated original: a low-label swap corrupts the incoming port at its actual s:1–s:2 connector, and a false D=[2,3,4,5] reaches the physical suffix gate after checking the original partial state. All three rejected. [Controls and adverse receipts](controls.json)

## Reproduction

Use a disposable checkout at `ec058da9fe0c834978cc5de927cd96f5b0ca2e68`, with HEAD left at that parent. Copy the exact raw bytes of the new proof, task specification, and bundle `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `run.py`, `audit.py` and `driver.py` to their published paths. Preserve the parent archive files and use the project-local runtime and source identities in [identity.json](identity.json). Leave all generated files absent. From the repository root, run the driver command in [commands.json](commands.json) exactly once. It checks the raw config and unoccupied outputs before starting the producer and independent auditor sequentially. Preserve partial output on interruption or a cap.

The official run used one worker and 0.296875 combined process-CPU seconds. Zero solver calls, retries, replay or audit-added visits. [Command receipt](command_receipts.json) · [Raw manifest](MANIFEST.json)
