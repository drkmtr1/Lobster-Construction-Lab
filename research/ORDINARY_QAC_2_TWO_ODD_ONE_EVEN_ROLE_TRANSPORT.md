# D121 — Deterministic numerical host-role transport

Exact ordered `[[q,a,c],[2]]` admits a direct ordinary graceful labeling whenever the three left quotas are exact integers, exactly one is even and at least two, both others are odd and at least three, and at least one odd quota is at least five. Its physical pins are `(s:0,s:1,b:1:0)=(0,m,1)` with m=q+a+c+7. This transports the numerical construction of [D119](ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER.md). No alpha or signed-edge restriction is imposed.

## Roles and exact correspondence

Write p=(q,a,c), with physical indices 0,1,2. Validate exact integer types, excluding booleans and nonintegers, and the stated parity and lower bounds. The unique even index i_C exists by the domain. The set of indices of odd quotas at least five is nonempty. Choose its least index i_H, so ties, including equal quota values, have a unique outcome. This index differs from i_C by parity. The remaining index i_L is unique and odd. Consequently Q=p[i_H]≥5 and A=p[i_L]≥3 are odd and E=p[i_C]≥2 is even. These are exactly D119's bounds, with no inequality between Q and A required.

Define sigma by sigma(0)=i_H, sigma(1)=i_L, sigma(2)=i_C. The three values are distinct and exhaust the physical indices, so sigma is a permutation. View the role-ordered `[[Q,A,E],[2]]` symbolically. Its center `b:0:j` has exactly p[sigma(j)] terminal indices. Define Phi on its names by `b:0:j → b:0:sigma(j)` and `l:0:j:k → l:0:sigma(j):k`, fixing both spine vertices and every right-section vertex. The inverse uses sigma inverse on each left center or leaf index j, keeping k. The equal ranges in each role give a bijection on named vertices.

The fixed spine edge maps to itself. Each left attachment `s:0--b:0:j` maps to the actual attachment at physical index sigma(j), giving all three once. Each left terminal incidence `b:0:j--l:0:j:k` maps to the actual edge at that physical center and the same terminal index, with the inverse recovering every original edge. The right attachment and both right terminal incidences are fixed. These disjoint classes exhaust the graphs, so Phi also bijects actual edges with incidence multiplicity preserved. This argument applies to every permitted physical order, including identity and nonidentity maps. It uses no numerical reordered graph. The original names, physical roles, profile and edges stay fixed.

## D119 values at the actual hosts

Let H,L,C denote the actual centers at i_H,i_L,i_C. Use D119's nine-edge ten-vertex core directly at the following actual vertices.

| Vertices in order | Labels |
| --- | --- |
| `s:0,s:1` | 0,m |
| H,L,C,`b:1:0` | m−4,2,m−6,1 |
| H index 0, L index 0 | m−5,m−3 |
| `l:1:0:0,l:1:0:1` | m−1,m−2 |

The core consumes labels [0,2] and [m−6,m] and weights {1,2} and [m−6,m], exactly as in D119. Thus R=D=[3,m−7]. With k=E/2, reserve R_B as the disjoint union of `{5+2i:0≤i≤k}` and `{m−7−2i:0≤i≤k}`. Reserve D_B as the disjoint union of `{3+2i:0≤i≤k}` and `{m−9−2i:0≤i≤k}`. Let R_A=R setminus R_B and D_A=D setminus D_B. All numerical values coincide with D119 at Q,A,E.

For each batch, a local row with label x and canonical host u maps to the row with x and actual host Phi(u), whose label is the same as u's. Hence the proposed weight and its membership in the same reserved difference palette are identical. This is a bijection of eligible rows preserving the difference vertices, multigraph edges with multiplicity, host tags, component balances, and all label and difference equations. The quotas are counted by host tag, so the integral lower projection is also identical. In Batch A the lower counts are `{2j:0≤j≤(Q+A−6)/2, j integer}`, and in B they are `{2+2j:0≤j≤E/2, j integer}`. Use A's unchanged reflection x ↦ m−2−x, choose the innermost (A−3)/2 available pairs by their smaller representatives, and assign their increasing labels to L. Assign the A complement to H. For B take lower count two, placing E+5 and m−7 at the L endpoints and the increasing remainder at C. This transports the same numerical allocation at every original named slot.

| Batch | Actual terminal positions | Counts |
| --- | --- | --- |
| A | L indices 3 through A−1 and H indices 1 through Q−1 | A−3 and Q−1 |
| B | L indices 1 and 2 and C indices 0 through E−1 | 2 and E |

The two host pairs share only L. These slots are disjoint, with L's A range empty when A=3. They cover every unfinished terminal edge once. Including the core, H,L,C have Q,A,E terminals, hence p at the physical indices. Since Phi leaves all label and weight values unchanged, the two reserved palettes split both residual inventories exactly. The transported batches and core therefore satisfy [R226 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout).

## Original graceful labeling

Let g be the canonical numerical supplier and set f(v)=g(Phi_inverse(v)) on the physical original. Since Phi is a bijection, [0,m] occurs once. Each original edge is the unique image of a canonical edge, and its weight equals the canonical weight by the displayed formula. Thus the actual edge multiset is [1,m], with multiplicity one, independently of the R226 assembly corollary. The exit, entrance and right center retain their fixed labels. Phi preserves adjacency and therefore distances to the fixed witnessing spine. In the orientation from the traversal class of `s:0`, the signs also transport edge by edge. Exactly the A incidences from a left terminal into the selected L host are negative. This describes the output. The terminal spine endpoint `s:1` retains degree two and exact neighbors `s:0` and the off-spine `b:1:0`. Their labels are 0 and 1 and its own label is m. Along with the ordinary graceful labeling and the spine this gives [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s physical premises.

The algorithm selects the three indices in constant work, scans the D119 integer palettes and reflection pairs in O(Q+A+E) indexed operations, and writes the labels directly using the physical host and terminal index at emission. This represents the same f without constructing any reordered numerical original. Both palettes and all output index ranges are finite. As Q+A+E=q+a+c, the construction terminates in O(q+a+c) indexed output operations.

## Retained check and remaining parity

The sole retained D119 profile `[[5,3,4],[2]]` has sigma=(0,1,2). Pointwise agreement on this original is a finite check of formula and custody. The symbolic edge correspondence proves the nonidentity orders. [D120](ORDINARY_QAC_2_ODD_C_DISJOINT_R226_SUPPLIER.md) keeps its separately established all-odd ordered domain.

For ordinary gracefulness the sum of all weights equals the sum of all labels. Modulo two each edge weight is the sum of its endpoint labels, so the sum of excess degrees times labels must be even. At these physical pins the sum is `Q f(H)+A f(L)+E f(C)+m+2`, which for the D119 core is congruent to `m(Q+E+1)` modulo two. D121 satisfies the necessary condition. With exactly two even left quotas, m would be even and this necessary test would pass for the same core. With three even left quotas, the center terms would be even for any labels, but m+2 would be odd. Thus the three pins are incompatible in the all-even case by the necessary parity test alone. A supplier in the two-even sector remains an open obligation.
