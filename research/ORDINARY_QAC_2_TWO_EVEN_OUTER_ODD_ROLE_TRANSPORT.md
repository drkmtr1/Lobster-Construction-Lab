# D127 — Transport of the two-even suppliers to the outer odd positions

Let p=(q,a,c) be the ordered physical left quotas on `[[q,a,c],[2]]`. Require exact integers, a unique odd quota at physical index 0 or 2 with value at least three, and two even quotas each at least two with at least one at least six. Then the original admits an ordinary graceful labeling at `(s:0,s:1,b:1:0)=(0,m,1)`, where m=q+a+c+7. Both spine vertices, four centers, and q+a+c+2 indexed terminals give m+1 vertices. The spine, four center attachments and all terminal incidences give m edges.

## Deterministic quota roles and canonical supplier

Put i_A at the unique odd index. Among the even indices with quota at least six, take the smallest as i_Q. That set is nonempty. Its least member is unique, even when the two even values agree or both qualify. The remaining index i_C is even, distinct from i_Q and i_A. Define Q=p[i_Q], A=p[i_A], C=p[i_C]. Thus Q≥6 and C≥2 are even and A≥3 is odd. These are quota roles. The actual centers are the named vertices at these indices. Each selected supplier assigns its own numerical labels to those vertices, with numerical order inherited from that supplier.

The symbolic source has canonical quota order (Q,A,C). Use the first applicable row.

| Canonical condition | Supplier |
| --- | --- |
| A≥5 | [D122](ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION.md) Construction II |
| A=3, C≥6, Q=C | [D123](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) |
| A=3, C≥6, Q≠C | [D124](ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE.md) |
| (Q,A,C)=(6,3,4) | [D126](ORDINARY_634_2_MODIFIED_SHARED_MIDDLE_CORE.md) |
| Remaining A=3 | D122 Construction I |

In the last row C is 2 or 4. For C=2, Q≥6 gives C≤Q−4. For C=4 the Q=6 case is already D126, so even Q≥8 and again C≤Q−4. Thus every row meets its cited source hypotheses. The table covers the entire accepted ordered even–odd–even domain at these minima. In the A=3 overlap with C≥6 and C≤Q−4, D124 has priority and D122 Construction I remains an alternative. D122's original labeled core is obstructed for A=3, C≥Q−2, including the exact D126 profile. That statement remains scoped to its fixed labels. [D125](ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH.md) records the earlier union and dispatch before D126 and remains intact.

## Forward and inverse named correspondence

Let sigma=(i_Q,i_A,i_C), from canonical role index to physical index. If the odd index is 0, i_Q is 1 or 2 and i_C is the other even index. If it is 2, i_Q is 0 or 1 and i_C is the other even index. In both placements the three images are distinct and exhaust {0,1,2}. For each physical index h there is exactly one j with sigma(j)=h. Define tau(h)=j. Then tau(sigma(j))=j and sigma(tau(h))=h.

On the symbolic canonical names, define Phi by
```text
b:0:j   -> b:0:sigma(j)
l:0:j:k -> l:0:sigma(j):k
```
Both spine vertices and every right-section vertex are fixed. The inverse sends physical left index h to tau(h), keeping terminal index k. The canonical quota at j is p[sigma(j)], so the range of k for every such mapped leaf is precisely the actual physical range. Each actual left center or leaf has one preimage by tau and the unchanged k. Every fixed vertex has itself as its sole preimage.

| Canonical incidence | Unique physical image |
| --- | --- |
| `s:0--s:1` | Same witness edge |
| `s:0--b:0:j` | `s:0--b:0:sigma(j)`, once at each physical left center |
| `b:0:j--l:0:j:k` | `b:0:sigma(j)--l:0:sigma(j):k`, once at each actual left terminal |
| `s:1--b:1:0` | Same right attachment |
| `b:1:0--l:1:0:k` for k=0,1 | Both original right terminal edges fixed |

The inverse just given recovers each edge in the table, and the classes exhaust the incidence lists. Thus incidence multiplicity and adjacency are preserved. The target keeps its actual profile, names and graph. The ordered source is a symbolic role correspondence.

## Transport of core and R226 allocations

Let g be the labeling supplied by the selected canonical theorem. Give every physical vertex v the value f(v)=g(Phi_inverse(v)). Its labeled core on the physical original is the image of exactly the selected source core. Every one of its original edges has the same endpoint labels as its preimage, so the retained numerical labels, weights, their multiplicities and the unused inventories are identical.

For a source batch with hosts u,v, put its slots at Phi(u),Phi(v) using Phi on each named terminal slot. Keep its two reserved palettes unchanged. For every label x in that label palette and canonical host u,
```text
|x - f(Phi(u))| = |x - g(u)|.
```
A row is therefore eligible in the physical batch exactly when the source row is eligible against the same difference palette. Host tags are carried to the corresponding physical hosts and numeric difference vertices are fixed. Each half-edge, loop and ordinary edge keeps its label identity, its incidence and its multiplicity. Connected components and balance are identical. Choosing a source assignment gives the corresponding physical assignment, and the inverse gives the converse. This preserves every integral quota slice and the integral projection of each numerical host.

In D122 the canonical degree-A host carries 2 and is numerically lower in both batches. In the D123 modified core and its D124 and D126 uses, the hosts at canonical indices 0,1,2 carry 2,m−6,m−4. Thus in the X/M batch the lower host is the Q-role center and in the M/Z batch it is the A-role center. Order the host tags by those actual numerical labels when invoking R226. The unchanged allocations give the source batch quota at each image host regardless of its physical index.

Each batch has two distinct unchanged labeled core hosts and actual named pendant vacancies. Phi sends disjoint named slot sets to disjoint sets and maps the source shared host to the same shared physical host in both batches. It preserves the aggregate quotas by p[sigma(j)]. Each source host is one edge from the fixed spine, so its image is too. Core injectivity and distinct core weights, integer palettes, local balance, exact integral quotas, and both disjoint global residual partitions all persist. These verify every input of [R226 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) for the physical batches. This reuses the selected supplier's allocations and numeric resources.

Independently of the assembly corollary, the vertex bijection makes the label multiset [0,m] once. On every actual edge vw, the absolute weight agrees with the weight of its unique source preimage, so the complete physical edge multiset is [1,m] once. The entrance, exit and right center retain labels 0,m,1. The same path witnesses the lobster since distances to it are preserved. The exit remains the path's terminal endpoint of degree two with predecessor `s:0` and exactly the neighbors `s:0,b:1:0`. The latter is off the spine and the exit label is the current maximum. These are the exact [D112](ORDINARY_EXTREME_SPINE_GROWTH.md) premises.

Direct symbolic emission selects indices in constant work, uses the selected supplier's finite palette scans for Q+A+C, and puts each indexed label in its mapped physical name with constant work per output. It needs O(q+a+c) indexed operations and terminates. D126 is one finite dispatch branch. No reordered numerical graph or numerical transport is required for the proof.

## Scope of the result

Together with D122–D126 in the middle-odd order, D127 provides the two-even seed at every odd position when the odd quota is at least three, both even quotas are at least two and one is at least six. D122's scoped obstruction, D125's historical union, all-odd coverage and the existing physical interface retain their original statements. The five retained checks are canonical source checks. The forward and inverse proof supplies the outer positions.
