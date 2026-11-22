# B4-UNPADDED-QR12-001 evidence

The [lower-block proof](../../../research/ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
and [family proof](../../../research/B4_UNPADDED_QR12.md) establish the
conditional insertion and the exact ordered alpha family. This directory
preserves the finite checks separately from the symbolic proof and AI
[reviews](REVIEWS.md).

## Declared run

Run B4-UNPADDED-QR12-001-20261121 uses exactly the 12 listed
(q,r,K) cases in [config.json](config.json), one worker, at most
79 vertices and 2,000,000 bytes per result. It ran the explicit
construction only. The largest target, (1,2,64), has 79 vertices.
The largest completed-case record is 32,313 bytes.

The [summary](campaign/summary.json) and [identity](campaign/identity.json)
bind the configurations, runtime/dependencies, source snapshot and
individual records by raw-byte hashes. Each original is retained
before construction, and each record contains all named incidences,
the prefix certificate and inventories, physical port, crossing and
suffix, each completion step, full certificate and alpha split. The
[standard-library audit](independent_audit.py) independently
reconstructed the original graphs and checked the same 12 saved
certificates. Its [result](audit_result.json) adds zero completed
targets.

One separate [15-vertex seed](campaign/seed.json) checks the original
1212 graph, alpha cut, physical ports, witness distances and both
complete incident predicates, at lower threshold 4 and upper threshold
13. Its provenance points to the exact retained adjacent witness.
The audit checked this same seed. There was no DFS rerun.

## Controls and correction

The [command receipts](commands.json) preserve six successful
commands: 7 focused and 11 ingestion test methods, the construction
campaign, its separate audit, the actual (2,3,1) CLI repeat, and
the retained demo. The test repetitions and CLI repeat add no cases
to the declared campaign. The r=1 control matches the retained Q112
labels, interface and trace. Graph admission and the independent
record cap were exercised, with no large graph expansion.

The first mathematical draft wrote upper threshold 12 for the
1212 base. That threshold also selects the third terminal and
adds difference 9. The corrected threshold 13 selects exactly the
intended pair. The [draft and correction](attempts/base-upper-threshold-draft/README.md)
preserve the review failure before any runs. The proof also records
the minimum-high recipe's duplicate difference 3 when applied to
the supplied second host of label 10. Both failures concern their
stated placements. None of the six executable invocations failed.
[MANIFEST.json](MANIFEST.json) hashes every other raw evidence file.
