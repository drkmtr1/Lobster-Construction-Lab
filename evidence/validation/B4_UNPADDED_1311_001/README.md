# B4-UNPADDED-1311-001 validation

The [minimum-high extension and symbolic family proof](../../../research/ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md)
are mathematical results. The new executable campaign uses only the
[exact 1311 profile](../../../research/B4_UNPADDED_1311.md).

## Completed original targets and arithmetic audit

The declared configuration fixes 12 lengths, one worker, 79 target
vertices, and 2,000,000 bytes per result. K=64 reaches 79 vertices.
The regression retains each original before construction. It
records all three middle leaf incidences and their exact labels,
root m, both inventories, the actual s:4 port, the original
crossing and suffix, every completion step, the full alpha cut
and unchanged original-target verifier results. All 12 passed.

The separate standard-library audit reconstructs the original
named graph and compares vertex and undirected-edge multiplicities
independent of storage order. It also reconstructs the exact
labels, differences, both inventory complements, physical suffix
and trace, and alpha split. All same-12 certificates passed on
the first attempt. The audit adds zero completed targets.

## Separate component and seed

`left_component_result.json` certifies one 11-vertex expanded
left component for r=3, with low-class size 6, minimum-high
host b:1:0=6, physical port labels 0 and 7, and its distance-two
witness. `seed_result.json` certifies the 15-vertex prefix with
low-class size 8, physical port labels 0 and 8, and the original
concatenated witness. Both are auxiliary. The retained relabeled
nine-vertex source is identified in the proof, with no repeat
of its accepted experiment.

## Commands and custody

`commands.json` records all eight successful commands using
project-local Python with `PYTHONUTF8=1`. The four targeted modules
ran 23 methods. The other four commands were the regression,
arithmetic audit, actual K=1 CLI example, and H010 demo. The CLI
repeats a declared case. Tests check early rejection, wrong
same-size profiles, false certificates, moved leaf incidence,
and the 79/78 boundary. The 10,000/10,001 ceiling was checked by
size preflight. The inherited record cap applies separately.

Before validation, a source-edit guard caught a missing word
in the template match for existing metadata. It stopped before
any constructor or ingestion code was written. The match was
corrected before implementation and no validation had run.

Runtime and hashes are in the result records. The source snapshots
include the implementation, dependencies and focused tests. The
CLI and demo preserve their own inputs and snapshots. Separate AI
dispositions are in `REVIEWS.md`. The manifest hashes raw file bytes,
preserved by `.gitattributes`. No solver search or general q/r
execution was used.
