# B3-UNPADDED-K1-001 validation

The regression passed the 12 declared original targets, six with q>=r and six with q<r. It records each independently built, named original target, its digest, the prefix and both singleton inventories, the sole original edge `s:3--s:4`, and the final certificate. It also records the unchanged adjacent predicate's rejection of this singleton boundary.

The separately written arithmetic audit passed on those same 12 saved targets. It reconstructs the named graph and full alpha classes, verifies the prefix spectrum and singleton completion, and compares certificates using the unchanged checker. It does not invoke the constructor. The finite results corroborate the symbolic proof.

The regression and audit used CPython 3.13.17 on Windows 11 with optimization level 0. The limits were one worker, 38 vertices per target, and 2,000,000 bytes per result. The 23-file byte-preserved source snapshot includes runtime modules, dependency declarations, and focused test source. The audit verifies live and snapshot hashes, and the CLI and demo save their own inputs and source snapshots.

`commands.json` records invocations, statuses, and outputs. The nine targeted modules passed 45 test methods, including the newly added tests, earlier B3 and B2 constructors, the nonadjacent consumer, and ingestion. The CLI verified the declared minimum `(1,1,1)` case. The retained H010 demo passed on its own graph. Full discovery was excluded because it includes solver searches. `MANIFEST.json` lists the raw SHA-256 and byte counts of the evidence files except for the manifest itself.
