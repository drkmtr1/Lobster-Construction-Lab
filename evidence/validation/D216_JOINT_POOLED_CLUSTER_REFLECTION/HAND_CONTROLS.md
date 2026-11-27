# D216 exact named hand controls

The spine in every original is `s:0--s:1--s:2--s:3`. A branch entry in section i at index j names `b:i:j` and each terminal at index e names `l:i:j:e`. The ordered terminal tuples below bind exactly those indices. The exterior shell in these controls is the normalized unit-flank shell. At A=3 its spine is (4,3,7,0), its exterior branch vertices have labels (2,6) and their terminals (5,1). Its actual spine weights are (1,4,7), its two branch-attachment weights are (2,6), and its terminal weights are (3,5). The cut is 4. It is the unique normalized shell established in the manuscript.

## 1. Prescribed 20-edge positive and two adverse selections

Original `[[1],[1,1,2],[1,1,1],[1]]`. Donor `s:1`, receiver `s:2`. The independently supplied pool has 13 edges and root 0. The following table specifies the temporary graph and the restored original. In the pool, every central branch attaches to the donor, including those indexed in section 2. In the original, section 2 branches attach to the receiver without changing their internal incidences.

| Actual branch | Pooled center | Pooled terminal tuple | Internal differences | Final center | Final terminal tuple | Final attachment difference |
|---|---:|---|---|---:|---|---:|
| `b:1:0` | 4 | (7) | (3) | 7 | (10) | 4 |
| `b:1:1` | 10 | (11) | (1) | 13 | (14) | 10 |
| `b:1:2` | 13 | (1,2) | (12,11) | 16 | (4,5) | 13 |
| `b:2:0` | 5 | (12) | (7) | 15 | (8) | 5 |
| `b:2:1` | 8 | (6) | (2) | 11 | (9) | 9 |
| `b:2:2` | 9 | (3) | (6) | 12 | (6) | 8 |

The pooled nonroot labels are exactly [1,13]. Its six root weights are 4,10,13,5,8,9. The terminal weights (3,1,12,11,7,2,6) complete [1,13]. This checks the pooled supply before amalgamation.

With ρ(x)=17−x, take E={`b:2:0`}. Its full label palette P(E)={5,12} is a reflected pair. The changed-weight set M consists of `b:2:1` and `b:2:2`; their center coordinates {8,9} are also a reflected pair. In the final table the terminal differences remain the displayed internal differences by direct subtraction. For the two unreflected receiving branches the weights 8 and 9 exchange. For the reflected receiving branch the attachment weight stays 5.

The actual final spine labels are (17,3,20,0), with differences (14,17,20). The left and right exterior branch labels are (2,19) and their indexed terminals (18,1). The branch-attachment weights are (15,19) and the terminal weights (16,18). The exterior thus uses exactly [14,20]. Its non-donor labels occupy [0,2] and [17,20]; the remaining labels [3,16] occur once on the donor and the six pooled branches. The named endpoints give exactly the 20 weights [1,20] and retain the actual connector `s:1--s:2` with weight 17.

**Adverse vertex palette.** Keep the very same pool, shell and required receiver set, and take E=R. Then M is empty and the weight condition holds. But P(E)={3,5,6,8,9,12} goes to {5,8,9,11,12,14}. Coordinate 11 hits an unreflected donor label. Coordinate 14 leaves [1,13] and its actual label 17 duplicates `s:0`. The vertex condition fails.

**Adverse attachment palette.** Take E=∅. The vertex condition holds. Now M=R and {5,8,9} goes to {12,8,9}, losing weight 5 and repeating weight 12 already on the internal edge from `b:1:2` to `l:1:2:0`. The attachment condition fails. This is the same fixed source as the positive and the preceding adverse selection.

## 2. Symbolic supplier for the selected 26-edge mixed-quota original

Original `[[1],[2,2,2],[2,2,3],[1]]`. Donor `s:1`, receiver `s:2`, N=19, k=7 and A=3. The manuscript derives the two weight bands and independent pool by hand. All central branch attachments in the pool have parent `s:1` with label 0. The original has the stipulated two physical parents.

| Actual branch | Pooled center | Pooled terminal tuple | Internal differences | Final center | Final terminal tuple | Final attachment difference |
|---|---:|---|---|---:|---|---:|
| `b:1:0` | 19 | (8,3) | (11,16) | 22 | (11,6) | 19 |
| `b:1:1` | 18 | (1,4) | (17,14) | 21 | (4,7) | 18 |
| `b:1:2` | 15 | (5,2) | (10,13) | 18 | (8,5) | 15 |
| `b:2:0` | 6 | (14,9) | (8,3) | 20 | (12,17) | 6 |
| `b:2:1` | 7 | (16,11) | (9,4) | 19 | (10,15) | 7 |
| `b:2:2` | 12 | (17,13,10) | (5,1,2) | 14 | (9,13,16) | 12 |

The pool's 19 nonroot labels split between {1,2,3,4,5,8,15,18,19} and {6,7,9,10,11,12,13,14,16,17}, with multiplicity one. The root differences are the six center labels. Their union with the thirteen displayed internal weights is the disjoint union of [1,9]∪{12} on the future receiver group and {10,11,13,14,15,16,17,18,19} on the donor group. This is the full weight set [1,19].

For ρ(x)=23−x, select E=R, all three actual section 2 branches. Their entire palette is the five pairs {6,17}, {7,16}, {9,14}, {10,13}, {11,12}. This includes the unique quota-three branch. Since M=∅ the changed-weight condition holds. Actual transfer uses each listed final center and terminal at its exact name. Subtraction at the reflected hosts confirms terminal weights (8,3), (9,4), (5,1,2) in branch order. The receiver label 26 minus its three center labels gives (6,7,12).

The original spine labels are (23,3,26,0), with weights (20,23,26). The exterior branch labels are (2,25) and their terminals (24,1), with attachment weights (21,25) and terminal weights (22,24). These are exactly [20,26]. The center and terminal rows of the original use [4,22] exactly once, and the shell uses its complement [0,3]∪[23,26]. The actual internal and attachment weights exhaust [1,19], so the literal original edge spectrum is exactly [1,26]. The actual connector `s:1--s:2` remains and has weight 23.

This exact witness resolves the selected compatibility question by hand. The controls use no official diagnostic, solver, executable numerical discovery, or protected checker.

[Primary mathematical manuscript](../../../research/JOINT_POOLED_CLUSTER_REFLECTION.md)
