# B4-UNPADDED-QR21-001 validation

The [conditional insertion and symbolic (q,r,t,1) proof](../../../research/ALPHA_UPPER_BLOCK_LEAF_INSERTION.md)
is separate from this bounded campaign on the
[exact QR21 route](../../../research/B4_UNPADDED_QR21.md).

## Completed targets and same-certificate audit

The configuration fixes the 12 tuples in (q,r,K) order, one worker,
79 target vertices, and 2,000,000 bytes per result. The last tuple
(2,1,64) reaches 79 vertices. Each original is independently retained
before construction. All 12 certificates passed the unchanged checker.
The records preserve exact named topology and labels, both unused
inventories, physical s:4, crossing edge, suffix, completion trace,
and completed alpha partition.

The arithmetic audit uses only the standard library. It reconstructs
the exact named graph with vertex and undirected-edge multiplicities,
and independently checks the ordered labels, root, both inventory
complements, original suffix and trace, and alpha cut. All same 12
saved certificates passed. The audit adds zero completed targets.

## Separately certified components and seed

- `upper_component_result.json` certifies the 10-vertex B_2 with
  low size 4, ports 0 and 5, and threshold 8. Its complete upper
  incident edge list yields differences 7..9.
- `left_component_result.json` certifies the 12-vertex
  expanded left with low size 6, ports 0 and 7, and minimum-high
  second center 6. The third center remains label one.
- `seed_result.json` certifies the 17-vertex normalized prefix
  for q=2,r=3,t=2, with low size 8 and ports 0 and 8.

Each auxiliary record includes the original graph, exact labels,
certificate and physical witness. None is a completed target.
The retained nine-vertex base appears in the proof and its
old experiment was not rerun.

## Commands and custody

The six successful UTF-8 commands in `commands.json` cover
16 passing test methods across two targeted modules, regression,
separate audit, the actual (2,3,1) CLI repeat, and the retained demo.
The tests include one retained 1121 dispatch control on the overlapping
(1,1,1) graph. Its certificate is checked without pointwise comparison
or a replay of the historical campaign. Test and CLI repetitions do
not add distinct completed QR21 targets.

Adverse tests include altered leaf incidence, a false certificate,
malformed and oversized parameters, wrong same-size profiles and the
79/78 campaign boundary. The independent preflight checks for q,r,K
vary each coordinate at the 10,000/10,001 boundary without building
those large graphs. The 2,000,000-byte record cap applies separately.
No solver, enumeration or arbitrary-t route was run.

Result records preserve runtime and raw source/configuration identity.
`source/` preserves implementation, dependencies and the focused
test. CLI and demo retain their own inputs and snapshots. The
raw-byte manifest is protected by `.gitattributes`. The separate
read-only reviewer dispositions are in `REVIEWS.md`.
