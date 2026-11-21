# B3-UNPADDED-Q1-R2-001 validation

The regression verified the explicit `t=1` base-prefix labeling once and saved it in `base_prefix_result.json`. This is the original `[[1],[2],[1],[]]` prefix with 11 vertices and 10 edges. Its certificate uses differences 1 through 10 and contributes zero completed targets.

All 12 declared `(t,K)` pairs passed seed, shifted prefix, and full certificate checks on the original named graphs. The independent arithmetic audit reads those same 12 saved cases and reconstructs the seed, original path and both inventories. It evaluates the retained recurrence independently and checks the saved certificates against the unchanged verifier. The base-prefix certificate is outside the audit's case set.

The regression and audit used CPython 3.13.17 on Windows 11 with optimization level 0. The declared limits are one worker, at most 45 vertices per target, and 2,000,000 bytes per result. The regression saves both original and induced-prefix graphs, parameters, assignments, prefix inventories, tail differences and certificate results. The completed-run receipt also records the base receipt's SHA-256 hash.

`commands.json` records exact validation invocations, exit statuses, and outputs. The eight targeted modules passed 41 test methods, including the new focused tests, the three prior B3 constructors, retained B2 constructors, the nonadjacent consumer and ingestion. The CLI case repeats declared pair `(3,5)`, and the retained demo verifies its own H010 graph. Full test discovery was outside scope because it includes solver searches.

The 23-file raw source snapshot contains runtime modules, dependency declarations and focused test source. The audit matches live sources and the snapshot against the recorded hashes. The CLI and demo saved their own source inventories and configurations. `MANIFEST.json` records the raw bytes of the evidence package except for itself.
