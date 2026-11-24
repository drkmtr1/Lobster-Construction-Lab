# D107 — Symbolic ordinary right-terminal growth on ordered [[4,3],[r]]

For every exact integer r≥2, the named original `[[4,3],[r]]` has an ordinary graceful labeling with physical spine labels `s:0=0`, `s:1=r+11` and sole signed reversal −1 at `l:0:0:3 → b:0:0` when edges are directed from the bipartition class of `s:0`.

## Original and indexed formula

There are two spine vertices, three centers, seven left terminals and r right terminals. The spine is `s:0--s:1`, both left centers attach to `s:0`, and the right center attaches to `s:1`. The two left terminal groups have indices [0,3] and [0,2]. The right terminal indices are [0,r−1]. Every indexed terminal is adjacent only to its own center. Thus there are r+12 vertices and r+11 edges, each incident to its designated vertices with multiplicity one. Adding a center or terminal uses exactly one edge to the existing tree and creates no cycle. The original spine is a witness, with centers one edge away and terminals two edges away.

| Vertex or indexed group | Label |
| --- | --- |
| s:0, s:1 | 0, r+11 |
| b:0:0, b:0:1, b:1:0 | 10, 9, 1 |
| l:0:0:0 through l:0:0:3 | 2,3,8,11 |
| l:0:1:0 through l:0:1:2 | 4,5,6 |
| l:1:0:0 | 7 |
| l:1:0:k with 1≤k≤r−1 | 11+k |

The fixed labels excluding the exit are the twelve distinct values in [0,11]. The right terminals with positive indices add precisely [12,r+10] at unit spacing. The exit adds r+11. The interval for the positive indices is a singleton at r=2, and the index zero is always assigned by its separate fixed entry. The listed groups cover every vertex precisely once. Setting fixed labels, visiting k=1 through r−1 once and setting the exit terminates after r+12 label assignments, which is O(r). The algorithm checks that r has exact integer type and r≥2 before emitting labels.

Orient every actual edge from the class containing `s:0`, which consists of `s:0`, the right center and all left terminals. The opposite class consists of `s:1`, the two left centers and all right terminals. The edge partition follows from the names.

| Original edges | Signed differences | Absolute inventory |
| --- | --- | --- |
| Left attachments, both left terminal groups and the first right terminal | (10,9), (8,7,2,−1), (5,4,3), (6) | [1,10] |
| Right terminal edges with 1≤k≤r−1 | (11+k)−1=10+k | [11,r+9] |
| Right attachment | (r+11)−1=r+10 | {r+10} |
| Actual spine edge | r+11−0=r+11 | {r+11} |

The parentheses group the two attachments, first left terminal group, second left terminal group and first right terminal, in that order. The only negative edge is the fourth terminal of the first left center, running from 11 to 10. The first edge group has ten actual incidences. The remaining groups consist of r−1, one and one actual incidences, so the partition accounts for all r+11 edges. The intervals are disjoint and consecutive, and [11,r+9] is a singleton at r=2. Both inventories are bijective.

## Induction from D105 using the D106 transition

At r=2 the complete indexed formula is the accepted [D105 certificate](../evidence/validation/LCL_ORDINARY_43_2_EXTREME_SPINE_001/result.json) pointwise, including right terminal labels 7 and 12 and exit 13. At r=3 the formula gives right terminal labels 7,12,13 and exit 14, with all other labels as in the archived [D106 certificate](../evidence/validation/LCL_ORDINARY_43_3_EXTREME_SPINE_001/result.json). The audit checks these agreements at every named vertex and on both actual originals.

Assume the formula, graceful inventories and signed edge condition at an exact integer r≥2. Write m=r+11. The next original increases only the count of right terminals from r to r+1, adding the next index `l:1:0:r` at the unchanged center `b:1:0`. All old names, roles, indices, incidences and the spine remain. The new terminal is one edge from its center and two from the spine. The new label prescribed by the formula is 11+r=m. The new exit label is m+1. Every other old label is unchanged, so the retained [0,m−1] accepts m at the fresh terminal and m+1 at the exit to give [0,m+1] exactly once.

In both originals the only neighbors of `s:1` are the physical `s:0` with label 0 and its center `b:1:0` with label 1. The old spine and right attachment realize m and m−1. Since the old difference inventory is a bijection, the unchanged incidences exhaust [1,m−2]. The fresh terminal edge gives m−1 and the raised exit gives m on the right attachment and m+1 on the spine. These differences occur on three distinct actual incidences and give the remaining interval exactly once.

Traversal parity on the old vertices is unchanged. The fresh right terminal is odd, while the right center is even. The three fresh or changed signed differences are m−1, m and m+1 on the fresh terminal, attachment and spine, all positive because m≥13. Every other signed difference remains the same. In particular −1 on `l:0:0:3 → b:0:0` is unchanged and stays the unique negative edge. This establishes the induction hypothesis at r+1. The base and the one induction step prove the exact scoped iteration.

## Signed sum and scope

The absolute inventory sums to m(m+1)/2. The only reversal has magnitude one, so the signed sum is m(m+1)/2−2. Counting instead by vertex degree gives even weighted sum r+40: the right center of degree r+1 carries 1, the entrance carries 0, and the left terminals sum to 39. The odd weighted sum is 2(r+11)+5·10+4·9+7+∑(11+k) for 1≤k≤r−1. The indexed sum is (r−1)(r+22)/2, so odd minus even is (r+11)(r+12)/2−2, in agreement with the signed edge sum.

This is one ordinary graceful family with left quotas fixed at 4 and 3. The spine labels are physical vertex labels. The even class contains 0 and 11 and the odd class contains 7 and r+11, so neither separation order works for these certificates. [D104](R241_43_2_LEFT_TERMINAL_ZERO.md) excludes alpha labeling at r=2. [D098](R241_NAMED_CENTER_ROLE_TRANSPORT.md) gives a separate alpha construction at r=3, and [D097](R241_QAR_ALPHA_SUPPLIER.md) does so for r≥4. The official verification rechecks only the two retained originals and certificates. The quantified conclusion is proved by the induction above. [Audit evidence](../evidence/validation/LCL_ORDINARY_43R_EXTREME_SPINE_001/README.md).
