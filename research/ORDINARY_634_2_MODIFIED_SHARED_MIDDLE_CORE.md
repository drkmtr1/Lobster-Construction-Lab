# D126 — Modified shared-middle completion of the frozen (6,3,4) seed

The exact retained ordered original `[[6,3,4],[2]]` admits an ordinary graceful labeling at physical pins `(s:0,s:1,b:1:0)=(0,20,1)` using the D123 modified core. Its canonical digest is `be51de0924c9de0f9a81929ecb98c9f29502e7f78ccadd0bfb6384f32c99e393`. The same original is the adverse instance for [D122](ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION.md), whose fixed-core obstruction retains its scope. D122 labels the left centers (16,2,14), while this seed uses (2,14,16). The frozen original has identical names, incidences and spine in both records.

## Core and residual inventories

Let X, M and Z be the physical left centers at indices 0, 1 and 2. The original consists of two spine vertices, four centers and 15 terminals. The spine, four attachments and 15 pendant incidences give 20 edges on 21 vertices. Each center attaches to its own spine vertex and each terminal to its indexed center alone. The witnessing spine stays `s:0--s:1`, at distances one and two from the centers and terminals respectively.

Supply the [D123](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) core at m=20. Its spine labels are (0,20), its X/M/Z/right center labels are (2,14,16,1), and the original X index 0, M index 0 and two right indices carry (17,15,19,18), respectively. These ten vertices form a tree since they retain the four center attachments, the spine and one pendant attachment per reserved terminal. Their nine actual weights follow from the following incidence order.

| Core incidence | Weight |
| --- | ---: |
| `s:0--s:1` | 20 |
| `s:0--b:0:0` | 2 |
| `b:0:0--l:0:0:0` | 15 |
| `s:0--b:0:1` | 14 |
| `b:0:1--l:0:1:0` | 1 |
| `s:0--b:0:2` | 16 |
| `s:1--b:1:0` | 19 |
| `b:1:0--l:1:0:0` | 18 |
| `b:1:0--l:1:0:1` | 17 |

The labels are the disjoint bands [0,2] and [14,20], and the weights are the disjoint bands {1,2} and [14,20]. Hence the unused label and difference sets are both [3,13]. The actual vacant quotas are (5,2,4). Modulo two, each edge difference equals the sum of its endpoint labels. A graceful labeling has equal total label and difference sums, so the excess-degree weighted sum must be even. The entrance label is zero, terminals have excess degree zero, the exit contributes 20, and the right center contributes 2. The three left-center terms yield the actual total 6·2+3·14+4·16+20+2=140. The resource partitions below establish sufficiency for this construction.

## Joint reservations

The arithmetic used in [D123](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) and [D124](ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE.md) gives t=(20−2)/2=9 and endpoints b=t−6/2=6 and e=t+6/2=12. Thus I=[6,12], and J=[3,5] ⊔ {13}. The map w(x)=16−x reverses [3,13] onto itself, with w(I)=[4,10] and w(J)={3,11,12,13}. Since 5=w(11) belongs to w(I), send label 9 and difference 5 to B. This supplies the exact partitions directly from the parameters.

| Batch | Actual hosts | Reserved labels | Reserved differences |
| --- | --- | --- | --- |
| A | X, M | {6,7,8,10,11,12} | {4,6,7,8,9,10} |
| B | M, Z | {3,4,5,9,13} | {3,5,11,12,13} |

### Batch A

All A labels are between X=2 and M=14, so the options are x−2 and 14−x. In the reference interval I and w(I), 11 and 12 are forced to X because their M weights 3 and 2 are below 4. Reflection x↦16−x interchanges the host options on [6,10]. It gives pairs {6,10} and {7,9} and the midpoint loop at 8. In the second pair, 7 has weights 5 at X and 7 at M, while 9 has weights 7 at X and 5 at M. Removing label 9 and difference 5 leaves 7 forced to M at 7. Other components retain every option. The complete eligible rows against the actual reservation are these.

| Label | X row | M row |
| ---: | ---: | ---: |
| 6 | 4 | 8 |
| 7 | — | 7 |
| 8 | 6 | 6 |
| 10 | 8 | 4 |
| 11 | 9 | — |
| 12 | 10 | — |

The two edges of the parallel pair lie on difference vertices 4,8, with reversed host tags. The equal options for label 8 make one loop using one vertex and one label. Each other component is a single half-edge. Every reserved difference is covered, there are no empty rows, and the number of label resources equals the number of difference vertices in each component. The pair gives either zero or two X assignments and the loop gives either zero or one. The two forced X half-edges and one forced M half-edge yield integral X totals {2,3,4,5}. Select five at X using both labels of the pair and the midpoint. X labels (6,8,10,11,12) yield weights (4,6,8,9,10) and M label 7 yields 7. This gives the local quotas (5,1) and all of the reserved spectrum.

### Batch B

Both hosts exceed every reserved label. M gives 14−x=w(x+2) and Z gives 16−x=w(x). Against the actual B difference palette the eligible rows are these.

| Label | M row | Z row |
| ---: | ---: | ---: |
| 3 | 11 | 13 |
| 4 | — | 12 |
| 5 | — | 11 |
| 9 | 5 | — |
| 13 | — | 3 |

Label 9 supplies isolated difference 5 at M. The Z option would be 7. The only Z preimage of 5 is 11 and the only M preimage is 9, so no J label shares this component. For a J label the M option is eligible exactly when its coordinate plus two belongs to J. The lower interval gives chains {3,5} and {4}, and the upper interval {13} supplies a single odd chain. Thus there are three nonempty chains, along with the isolated M half-edge.

The {3,5} component has difference vertices 13 and 11, with one ordinary edge from label 3 and one Z half-edge from label 5. Weight 13 must be consumed by label 3 at Z, leaving the forced Z assignment of 5 at 11. This is also the rooted tree extraction of [R226 revision 2, Section 5](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-researcher). The singleton components of 4 and 13 each contain one Z half-edge and one difference vertex. Each component balances, every label has an eligible row, and all reserved vertices are covered. The unique extraction sends every J label to Z, leaving integral M projection {1}. Pick M label 9 and Z labels (3,4,5,13). Their actual weights are 5 at M and (13,12,11,3) at Z. This gives quotas (1,4) and the full B spectrum once.

## Assembly and original certificate

Set the terminal lists in increasing physical index order as follows.

| Host | Indexed terminal labels |
| --- | --- |
| X | (17,6,8,10,11,12) |
| M | (15,7,9) |
| Z | (3,4,5,13) |
| Right center | (19,18) |

The core stays fixed. A fills X indices 1 through 5 and M index 1. B fills M index 2 and Z indices 0 through 3. Each batch uses two distinct core hosts, both adjacent to the retained spine, and the host sets intersect exactly at unchanged M. The slots are disjoint and give every actual unfilled pendant incidence exactly once. Their totals with the reserved core leaves are (6,3,4,2). Each local palette consists of distinct integer labels avoiding its hosts and the equally sized difference set is positive and distinct. The two palettes partition each unused global inventory. The balanced, integral local allocations give all hypotheses of the [R226 reserved-palette corollary, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-researcher).

Independently, the core and both terminal allocations exhaust [0,20] once. The direct actual differences in original order are
```text
20,2,15,4,6,8,9,10,14,1,7,5,16,13,12,11,3,19,18,17
```
The batch weight calculations and nine core weights exhaust [1,20] once, preserving every original name, incidence and the witnessing spine. Oriented from the traversal class containing `s:0`, precisely the six X terminal edges and the reserved M terminal edge are negative, with absolute weights 15,4,6,8,9,10 and 1. Their sum is 53, so the signed sum is 210−2·53=104. Equivalently, the weighted degree sums of the head and tail classes are 227 and 123.

The terminal spine endpoint `s:1` is the maximum 20 with exact neighbors `s:0` at zero and off-spine `b:1:0` at one. It retains its predecessor and satisfies [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s physical premises. This completes the sole uncovered triple within [D125](ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH.md)'s stated ordered even–odd–even minima. The construction is the single retained seed. Its independent executable checks are archived separately.
