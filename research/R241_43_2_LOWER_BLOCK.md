# D099 obstruction to the prescribed lower-block placement

[Evidence](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/README.md) · [D098 supplied ledger](R241_NAMED_CENTER_ROLE_TRANSPORT.md) · [Retained lower-block theorem](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)

**REJECT** the one-leaf placement from either of the two prescribed supplied ledgers on source profile [[4,2],[2]], at physical b:0:1 and all allowed thresholds, on exact target [[4,3],[2]].

## Named originals and reflected source

Both names s:0, s:1 and their spine edge stay. The left attachments at s:0 reach b:0:0 and b:0:1. The right attachment at s:1 reaches b:1:0. The source terminal counts at those centers are 4, 2 and 2, with consecutive indices from zero and exactly one incident edge per terminal. The target has counts 4, 3 and 2. The only new vertex is l:0:1:2, adjacent only to b:0:1. All old names, roles and edges remain. The source has 13 vertices and 12 edges. The target has 14 vertices and 13 edges. The spine is a witness for both trees, since centers are distance one and leaves distance two through their designated centers. The host b:0:1 is a high center one edge from s:0.

Ledger I is the original-bound D098 labeling at cut 8, with physical labels (3,12), offsets (3,4) and host label 9. Ledger II reflects each old low label u to 7−u and each old high label v to 20−v. Reflection bijects each class to itself. On an actual edge of original difference d=v−u, the new difference is (20−v)−(7−u)=13−d. The values 1 through 12 are permuted. The physical spine labels become (4,8), yielding offsets (4,0), and the host label becomes 11. The graph and original witness are fixed. In each ledger the source satisfies all supplied-state and host requirements. The possible low thresholds are exactly x<c≤8 with c≥1. The incidence condition is checked separately.

## Derive the complete incidence spectra

Each original edge has exactly one low endpoint. Therefore each edge occurs in precisely one low vertex's incidence group. These groups come from direct subtraction on the original edges. In each row below the endpoint order is the order used for the listed weights, in both ledgers.

| Named low vertex | Its actual high neighbors in order | Label I | Weights I | Label II | Weights II |
| --- | --- | ---: | --- | ---: | --- |
| b:1:0 | s:1, l:1:0:0, l:1:0:1 | 0 | 12,10,11 | 7 | 1,3,2 |
| l:0:1:0 | b:0:1 | 1 | 8 | 6 | 5 |
| l:0:1:1 | b:0:1 | 2 | 7 | 5 | 6 |
| s:0 | s:1, b:0:0, b:0:1 | 3 | 9,5,6 | 4 | 4,8,7 |
| l:0:0:0 | b:0:0 | 4 | 4 | 3 | 9 |
| l:0:0:1 | b:0:0 | 5 | 3 | 2 | 10 |
| l:0:0:2 | b:0:0 | 6 | 2 | 1 | 11 |
| l:0:0:3 | b:0:0 | 7 | 1 | 0 | 12 |

Select the rows whose ledger label is less than c. This gives exactly the named S_c and every original incidence in E_c with its multiplicity. In I the groups below c=4 give [5,12]. Increasing c by one incorporates the next single weight immediately below the band. In II the groups below c=5 give {4}∪[7,12]. Admitting the vertices labeled 5, 6 and 7 then adds {6}, {5} and {1,2,3}, respectively. For the retained hypothesis the required band is [B−c+1,12]. The table records all differences between actual and required spectra as well as the results of the prescribed placement. Each entry listed in a set or interval has multiplicity one in the premise.

| Ledger | c | Actual premise weights | Required | Extra | Absent | New weight | Repeated weight | Missing weight |
| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| I | 4 | [5,12] | [6,12] | {5} | ∅ | 6 | 6 | 5 |
| I | 5 | [4,12] | [5,12] | {4} | ∅ | 5 | 5 | 4 |
| I | 6 | [3,12] | [4,12] | {3} | ∅ | 4 | 4 | 3 |
| I | 7 | [2,12] | [3,12] | {2} | ∅ | 3 | 3 | 2 |
| I | 8 | [1,12] | [2,12] | {1} | ∅ | 2 | 2 | 1 |
| II | 5 | {4}∪[7,12] | [7,12] | {4} | ∅ | 7 | 5 | 4 |
| II | 6 | {4}∪[6,12] | [6,12] | {4} | ∅ | 6 | 5 | 4 |
| II | 7 | [4,12] | [5,12] | {4} | ∅ | 5 | 5 | 4 |
| II | 8 | [1,12] | [4,12] | {1,2,3} | ∅ | 4 | 4 | 1 |

## Actual placements and resource obstruction

The formula G_c leaves old labels below c in place, assigns c to l:0:1:2 and increments all old labels at least c. The four disjoint bands [0,c−1], {c}, [c+1,8] and [9,13] exhaust the new alphabet, including the empty third band at c=8. The cut is 9, with every old edge retaining its orientation. The new leaf is low and its physical host increases from B to B+1, giving weight B+1−c. The physical entrance remains x and the exit label increases by one, to 13 in I and 9 in II. The offsets and the actual spine witness persist in each placement. These data describe the placements even though their spectra fail gracefulness.

For an old edge, its high endpoint always moves and its low endpoint moves exactly when outside S_c. Thus its weight increases by one on E_c and is unchanged elsewhere. In I let t=9−c. The old weights [1,t−1] remain, [t,12] shift to [t+1,13], and the new weight is t+1. Exactly t is missing and t+1 appears twice. In II at c=5,6,7 let w=12−c, so w is 7, 6 or 5. The selected old weights are {4}∪[w,12]. The original [1,w−1] except 4 stay, and the shifted weights are {5}∪[w+1,13]. Adding w fills its place but leaves 4 missing. For w=7 or 6, an unchanged edge supplies the second 5. For w=5, the new edge supplies it. At c=8 all old differences shift to [2,13], and adding 4 repeats 4 and leaves 1 missing. These multiset calculations use the actual placement in every row and prove failure of the full spectrum.

The recorded rows preserve every old and new vertex label, the selected named incidences, all 13 target-edge differences, and the exact inventories and original-target checker outcomes. The result concerns these two supplied ledgers and their nine placements at the same physical host on the stated ordered original. Other labelings and other construction mechanisms for this target remain open here. The retained theorem's implication remains applicable wherever its full premise holds.
