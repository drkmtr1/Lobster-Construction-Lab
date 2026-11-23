# B4-K2-D062-TWO-GAP-ORDER-PRESERVING-001

## Original and ranked prefix

Use the [retained D063 target](../evidence/validation/B4_K2_D062_TWO_EDGE_TRANSPORT_001/target_original.json)
`T=[[2],[2],[2],[2],[],[],[]]`, digest
`c5fd852e27ca85602e9a5a2cb39e3b14434b2783272c57523c2c1b7a317859f4`.
The original spine has seven vertices s:0 through s:6. Each of the
four branch centers is one edge from the spine and each terminal is
two edges away. The only unassigned vertices are s:5 and s:6. Their
pending edges are exactly s:4--s:5 and s:5--s:6.

At q=r=t=2, the [D062 construction](B4_JOINT_NESTED_CUT_TWO_HOST.md#exact-k1-zero-host-lift)
translates the D061 alternate C(2,2) ledger by one, restores the
original third center at zero, and supplies labels 16 and 17 at
its two terminals. The [D063 proof](B4_K2_D062_TWO_EDGE_TRANSPORT.md#exact-source-and-original-target)
displays the exact K=1 map F. Both named archived originals were
rechecked with that seed and its supplied lift. The old s:5 label
11 alone is withheld. In increasing rank order, the 17 retained
prefix names are

```text
b:2:0 s:1 b:0:0 b:1:0 s:3 l:3:0:0 l:1:0:0 l:1:0:1 l:3:0:1
l:0:0:1 s:4 l:0:0:0 b:3:0 s:0 s:2 l:2:0:0 l:2:0:1
```

Their old labels are [0,10] and [12,17]. Each integer pair
0 ≤ a < b ≤ 18 leaves 17 available labels. Matching these
in ascending order to the ranked names is the unique increasing
bijection between the two ordered sets. The holes are the exact
resource set R={a,b}. The second edge always has weight b-a.
Write p=f(s:4). The first edge has weight |p-a| in A and |p-b|
in B. For each pair the audit subtracts the weights of the 16
original assigned edges from [1,18] to compute the actual D
and retains any repeated weight and its multiplicity. A repeated
assigned difference rules out both completions. If there are
no repetitions, D has size two, and either order completes
exactly when its two edge differences equal D as a multiset.

There are 19·18/2=171 pairs and exactly two orders per pair.
The labels on the two physical suffix names determine both
the pair and the order, making all 342 full maps distinct.
The validator and arithmetic audit each check the same grid.
They make no rank changes or symmetry identifications.

## Top differences on the actual incidences

The positions at the extremes of the ranked prefix are
b:2:0 (minimum) and l:2:0:1 (maximum). The leaf l:2:0:1
has sole neighbor b:2:0. All three neighbors of b:2:0 are
in the prefix, namely s:2 and the two third terminals.
These facts yield the following necessary conditions.

1. If 0 is omitted and 18 is retained, the label 18 sits at
   l:2:0:1, whose only neighbor has the retained minimum.
   The suffix vertex carrying zero cannot meet 18. Weight
   18 is absent.
2. If 18 is omitted and 0 is retained, zero is at b:2:0.
   Its neighbors all receive retained labels, so weight
   18 is absent.
3. If both 0 and 18 are omitted, all assigned labels are
   1..17, making each assigned weight at most 16. The
   physical port s:4 has rank 10 with zero-based indexing,
   so its label is 11. In either suffix order the first edge
   has weight 11 or 7, and the last edge has weight 18.
   Weight 17 is absent.
4. If 17 is omitted and both 0 and 18 are retained, a
   weight-17 edge must join 0 to 17 or 1 to 18. The first
   cannot occur because b:2:0 has no suffix neighbor. The
   second cannot occur because the sole neighbor of the
   18-labeled leaf is b:2:0 with label zero.

Thus 51 pairs are excluded by the two top weights alone.
The remaining 120 pairs are the two-element subsets of
[1,16]. This deduction was evaluated after the full numerical
checks and did not prune the prescribed grid.

## Exhausted restricted negative

The independent arithmetic audit confirmed all 171 pairs, 342
different full maps, and all 18 actual edge weights for each map.
At 161 pairs an assigned edge difference repeats. The remaining
ten prefixes have the following exact resources. The last two
columns list weights in physical path order.

| R | f(s:4) | D | A suffix weights | B suffix weights |
|---|---:|---|---|---|
| {0, 12} | 11 | {1, 18} | (11, 12) | (1, 12) |
| {1, 12} | 11 | {1, 15} | (10, 11) | (1, 11) |
| {5, 6} | 12 | {1, 3} | (7, 1) | (6, 1) |
| {8, 12} | 11 | {1, 6} | (3, 4) | (1, 4) |
| {9, 12} | 11 | {1, 5} | (2, 3) | (1, 3) |
| {10, 11} | 12 | {1, 5} | (2, 1) | (1, 1) |
| {11, 14} | 10 | {1, 11} | (1, 3) | (4, 3) |
| {11, 16} | 10 | {1, 16} | (1, 5) | (6, 5) |
| {11, 17} | 10 | {1, 17} | (1, 6) | (7, 6) |
| {11, 18} | 10 | {1, 18} | (1, 7) | (8, 7) |

Each row fails the two-edge inventory test in both orders. In
the eight rows with nonadjacent holes the final weight b-a is
absent from D. The two adjacent-hole rows R={5,6} and R={10,11}
have final weight 1 and fail at the first edge. These two pairs
are absent from the D063 grid, whose holes always include
12 when c≤11 or 11 with the other label at least 12 when c≥12.
The expanded test therefore reaches new valid prefixes while
still yielding no valid completion.

**ACCEPT** the exact rank-preserving model, its 171-pair accounting,
the actual inventories and the 18/17 deduction. **REJECT** both
suffix orders for every prefix in this model. This is an
**EXHAUSTED RESTRICTED NEGATIVE** on the fixed named original
and D062 prefix ranks. Other rank orders, other suppliers, and
ordinary gracefulness of T remain open here.

[Evidence and audit](../evidence/validation/B4_K2_D062_TWO_GAP_ORDER_PRESERVING_001/README.md)
