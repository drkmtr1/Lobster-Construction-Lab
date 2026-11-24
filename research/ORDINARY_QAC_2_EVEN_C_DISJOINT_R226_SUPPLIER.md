# D119 — Variable even third quota by disjoint parity progressions

For independent exact integers q≥5 and a≥3 odd and c≥2 even, exact ordered `[[q,a,c],[2]]` has a direct ordinary graceful labeling with `s:0=0`, `s:1=m=q+a+c+7`, and `b:1:0=1`. The construction supplies two disjoint reserved palettes to the adopted R226.1 revision-2 criterion. Its proof also checks both bijections directly.

## Named topology and core

Start with the spine `s:0--s:1`. Attach H=`b:0:0`, L=`b:0:1`, and C=`b:0:2` to `s:0`, and `b:1:0` to `s:1`. For each center `b:i:j`, add exactly one incidence to each named terminal `l:i:j:t` with t from zero through the physical quota minus one. The quotas in this order are q,a,c,2. Each new vertex attaches by one edge, proving connectedness and acyclicity. The counts are m+1 vertices and m edges, with distance one for centers and two for terminals from the stated spine. Since q+a+c is even and at least ten, m is odd and at least 17.

The independently specified core consists of the two spine vertices, four centers, and `l:0:0:0,l:0:1:0,l:1:0:0,l:1:0:1`. Give them labels as follows.

| Vertices in order | Labels |
| --- | --- |
| `s:0,s:1` | 0,m |
| H,L,C,`b:1:0` | m−4,2,m−6,1 |
| `l:0:0:0,l:0:1:0` | m−5,m−3 |
| `l:1:0:0,l:1:0:1` | m−1,m−2 |

These ten vertices form a tree by their actual named attachments. The core's nine edges are the spine (weight m), the H,L,C,right attachments (m−4,2,m−6,m−1), the two reserved left terminal edges (1,m−5), and the two right terminal edges (m−2,m−3). Hence core labels are the disjoint union [0,2] and [m−6,m], and core weights are the disjoint union {1,2} and [m−6,m], each with multiplicity one. The residual inventories are R=D=[3,m−7], each of size m−9=q+a+c−2. The unfilled quotas at H,L,C are q−1,a−1,c.

Modulo two, each absolute difference equals the sum of its endpoint labels. In a graceful labeling the sums of all labels and all weights coincide, so the excess-degree sum is even. The left-center excess degrees are q,a,c, the right-center excess degree is two, the exit excess degree is one and the entrance has label zero. Therefore the necessary identity is `q f(H)+a f(L)+c f(C)+m+2≡0 (mod 2)`. The terms q f(H) and m are odd and the remaining terms are even. Sufficiency follows from the resource proof below.

## Batch B on L and C

Write k=c/2. Reserve O={5+2i:0≤i≤k}, E={m−7−2i:0≤i≤k} and R_B=O ⊔ E. Reserve D_B={3+2i:0≤i≤k} ⊔ {m−9−2i:0≤i≤k}. O is odd from 5 to c+5; E is even from q+a=m−c−7 to m−7. In particular m−7−(c+5)=q+a−5≥3. The differences are odd from 3 to c+3 and even from q+a−2 to m−9, all in D. Each progression has k+1 distinct terms. Parity makes the two parts disjoint even when their numerical spans overlap. This proof uses no ordering of the spans or restriction to one side of a midpoint. Both palettes have c+2 elements.

All residual labels are strictly between L=2 and C=m−6. Their options are d_L(x)=x−2 and d_C(x)=m−6−x, exchanged by rho_B(x)=m−4−x. For 0≤i≤k−1, set x_i=5+2i and y_i=m−9−2i. They sum to m−4, with crossed options 3+2i and m−11−2i. These options are distinct by parity, and the indexed odd and even sequences are each injective. The pairs cover every label in O except c+5 and every label in E except m−7, and their difference vertices exhaust D_B except c+3 and m−9. At c+5 the lower option is c+3 and the C option q+a−4 is even and below q+a−2, the minimum even reserved weight. At m−7 the lower option is m−9 and the C option is 1, outside D_B. Thus eligibility **within D_B** gives k parallel-pair components and the two isolated forced L half-edges. Each component's label count equals its difference-vertex count, all vertices are covered, every label has an eligible row, and the odd reflection sum precludes a midpoint.

With L first, R226 gives A0=2, pair count k, eta=0, and lower projection {2+2j:0≤j≤k, j integer}. Choose j=0. Assign c+5 and m−7 at L indices 1 and 2 in that order. Assign the c paired labels at C in increasing order, indices 0 through c−1. The L weights are c+3 and m−9. Each C pair supplies exactly 3+2i and m−11−2i once, verifying the complete reserved spectrum directly.

## Batch A on L and H

Set R_A=R setminus R_B and D_A=D setminus D_B. The higher option d_H(x)=m−4−x bijects R onto D by reversing the interval. On O it gives the even reserved difference progression, and on E it gives the odd reserved difference progression. Therefore d_H restricts to a bijection onto D_A. The reflection rho_A(x)=m−2−x exchanges O and E index by index, so the removal consists of k+1 complete reflected pairs, even when a progression crosses the midpoint. Reflection preserves [5,m−7]. The lower option satisfies d_L=d_H∘rho_A there, and both options of every remaining pair are eligible. Labels 3 and 4 remain, with unavailable lower options 1 and 2 and eligible higher options m−7 and m−8. The odd sum m−2 excludes a midpoint. Under the bijective d_H, the components have disjoint difference vertices and exhaust D_A. Two half-edges at distinct vertices and the parallel pairs give balance and no unavailable label. Quota-free eligible rows remain in the graph when the prescribed lower quota is zero.

The number of pairs is `(m−9−(c+2)−2)/2=(q+a−6)/2`. With L first, A0=0, eta=0 and the integral projection consists of all even counts from zero through twice that pair count. Choose j_A=(a−3)/2, leaving (q−3)/2≥1 unselected pairs. Use the j_A largest of the available smaller representatives, each satisfying x<rho_A(x). Equivalently choose the innermost available pairs. When j_A=0 choose none. Let S_A,L be the union of the selected pairs and S_A,H its complement in R_A. Their sizes are a−3 and q−1, and S_A,L is reflection invariant. Thus d_L(S_A,L)=d_H(S_A,L) as multisets, and d_L(S_A,L) together with d_H(S_A,H) supplies D_A without repeats. Fill L indices 3 through a−1 and H indices 1 through q−1 from their increasing lists.

## Global compatibility and exact construction

R_A and R_B are disjoint and exhaust R, and D_A and D_B are disjoint and exhaust D. The hosts are distinct within each batch, unchanged core vertices, and the two host sets intersect at L alone. All named slots are distinct actual pendants at their prescribed center. They cover every noncore vertex and unfinished edge. Both batches have finite distinct labels avoiding their host labels, an equal number of positive distinct reserved weights, and exact integral local allocations. All positive-quota hosts are at distance one from the core spine. These are the hypotheses of Section 10 of [R226.1 revision 2](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). Its global assembly is valid with L reused and unchanged. In H,L,C order, the exact physical totals are (1+q−1,1+(a−3)+2,c)=(q,a,c).

In named order the terminal lists are H `(m−5, increasing S_A,H)`, L `(m−3,c+5,m−7,increasing S_A,L)`, C the increasing paired Batch B labels, and right `(m−1,m−2)`. Independently of R226, the core and label palettes fill [0,m] once. The nine core weights, Batch A's direct image calculation and Batch B's explicit pair and endpoint weights fill [1,m] once on the actual original edges. Both unused inventories are empty. Under the orientation from the class containing `s:0`, left terminal edges point toward their centers, while right terminal edges point away from their center. Exactly the a terminal edges toward L are negative since their labels exceed 2. Every H and C terminal label lies below its center, all right-terminal labels exceed 1, and the spine and center attachments are positive in this orientation.

The exit is the terminal endpoint of the unchanged spine, with exact neighborhood {`s:0`,`b:1:0`}, maximum label m, and predecessor label zero. The other neighbor is off the spine and labeled one. The ordinary graceful labeling and this witness satisfy [D112](ORDINARY_EXTREME_SPINE_GROWTH.md). This checks its premises.

Reject all inputs whose type is other than exact integer, including booleans, and reject out-of-domain bounds or parity. Generate the reserved progression memberships and scan the integer residual interval in increasing order to emit sorted palettes. Scan the available smaller representatives in increasing order and select the final j_A, or none at zero. Emit both selected endpoints, the ordered named labels and the named incidences. These finite passes take O(q+a+c) indexed output operations without a comparison sort or search.

## Specialization and scope

At c=2, m=q+a+9 and k=1, giving exactly the D118 reservations `R_B={5,7,m−9,m−7}` and `D_B={3,5,m−11,m−9}`. Its L endpoints are 7,m−7, and its C list is 5,m−9 in increasing order. The complement, reflection, smaller representatives, innermost j_A, core and all named slot orders coincide pointwise with [D118](ORDINARY_QA2_2_DISJOINT_R226_SUPPLIER.md) for every q,a in that theorem. [D117](ORDINARY_QAR_ALL_PARITY_SUPPLIER.md) supplies its separate two-left-center domain. D119 establishes the claimed odd–odd–even three-left-center seed with right quota two. The finite boundary corroborates the symbolic proof.
