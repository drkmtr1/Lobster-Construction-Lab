# B4-UNPADDED-UNIT-001 validation

The regression verified the explicit 13-vertex fixed seed once and recorded it in `seed_result.json`. It uses differences 1 through 12 on the original named prefix graph, with a low class of size 6 and physical ports `b:0:0=0` and `s:4=6`. This certificate contributes zero completed targets.

All 12 declared completed targets passed on independently retained original graphs. The regression records the exact prefix, unused labels and differences, the physical port and crossing edge, the K original suffix assignments, the completed alpha classes, and the final certificate. The separate arithmetic audit reconstructs the graph, the named labels and the two classes, and verifies the same 12 saved targets without invoking the constructor. Its check of the separate seed record is limited to the recorded byte hash.

The regression and audit ran on CPython 3.13.17 for Windows 11 with optimization level 0. The limits were 12 completed targets, one worker, 77 vertices per target and 2,000,000 bytes per result. The 23-file byte-preserved source snapshot includes the runtime modules, dependency declarations and focused test source. The CLI and demo save their own source inventories and configurations.

`commands.json` records validation invocations, statuses and outputs. The ten targeted modules passed 49 test methods. The actual CLI case repeated declared K=1, and the retained demo verified its own H010 graph. Full discovery was outside scope because it includes solver searches. `MANIFEST.json` records the raw byte counts and SHA-256 hashes of the evidence files except the manifest itself.

The full staged whitespace check reported 12 inherited end-of-file blank-line notices from four unchanged source files in three byte-preserved snapshots. The staged whitespace check outside those snapshots passed. All staged evidence bytes matched the working files.
