# B4-22T2-ZERO-HOST-ALL-TK-001 evidence

[Proof](../../../research/B4_22T2_ZERO_HOST_ALL_TK.md) · [Authorized scope](INTAKE.md) · [Independent reviews](REVIEWS.md)

The frozen originals and certificates cover four new prefixes at t=3,4,5,8 and four new full originals at (t,K)=(3,2),(4,3),(5,5),(8,8). P₂ and T(2,2) recheck the D066 and D067 archives. The graph digest identifies the exact original. A separate ledger SHA-256 binds its labels to that digest. The batch comparisons reuse P₅. The independent audit reads the same ten certificates without importing the producer, the production graph builder, or the verifier.

## Reproduce in a disposable checkout

Check out the recorded parent `ee8b19fd268dcd84ff5c2f655bb4d6ffe4f58143` in a disposable working tree. Copy the exact Git blob bytes of the new proof and this bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `validate.py`, and `audit.py` from this task's containing commit to their given paths. Leave HEAD at the parent. Use the documented project-local Python 3.12 or 3.13 environment. The configuration pins retained raw archive and source bytes to Git parent blobs. The B2 proof also permits the recorded CRLF checkout bytes matching its LF Git blob. No other normalization is used.

With original, checker and audit outputs absent, run the three invocations in [commands.json](commands.json) in order from the repository root. The first freezes graph identities and source hashes before the second constructs certificates. The third independently reconstructs the same named graphs. Stop and preserve all output if a phase fails. Each phase writes fresh output and never overwrites an existing receipt. [Command receipts](command_receipts.json) record the official sequence.

The run uses one worker and no queries, DFS, labeling enumeration, replays or retries. It checks 10 complete positive certificates and separately tests six rejection paths. The 30-second process-CPU budget is shared by freeze, validation and audit. A distinct malformed-edge check only mutates P₃ in memory and records the attempted change, so it adds no frozen original or positive case. `MANIFEST.json` records raw bytes for each bundle file other than itself and for the external proof.
