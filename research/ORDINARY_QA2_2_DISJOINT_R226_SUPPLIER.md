# D118 — Three left centers from disjoint two-host resource batches

For independently chosen odd exact integers q≥5 and a≥3, ordered `[[q,a,2],[2]]` admits a direct ordinary graceful labeling with `s:0=0`, `s:1=m=q+a+9` and `b:1:0=1`. The construction uses two reserved [R226 revision-2 batches](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-researcher) on one independently specified named core.

## Original and independent core

Start with the named spine `s:0--s:1`. The left centers H=`b:0:0`, L=`b:0:1`, C=`b:0:2` attach to `s:0` and carry q, a and two leaves. The right center `b:1:0` attaches to `s:1` and carries two leaves. In each group, the names are `l:i:j:k` for indices from zero through its quota minus one, each adjacent just to its designated center. Adding centers and then terminals by their single attachment makes a tree with m+1 vertices and m edges. The specified spine witnesses distances one and two for centers and terminals, respectively. Since q+a is even and at least eight, m is odd and at least 17.

The core contains the spine, the four centers, the index-zero leaves at H and L and both right leaves. It is a connected tree with ten vertices and nine edges. Supply the core labels directly as follows.

| Vertices in order | Labels in order |
| --- | --- |
| `s:0,s:1` | 0, m |
| H, L, C, `b:1:0` | m−4, 2, m−6, 1 |
| `l:0:0:0,l:0:1:0` | m−5, m−3 |
| `l:1:0:0,l:1:0:1` | m−1, m−2 |

The nine differences are m on the spine, m−4, 2, m−6 and m−1 on the respective H, L, C and right attachments, 1 and m−5 on the reserved H and L terminal edges, and m−2 and m−3 on the two right terminal edges. This gives the disjoint occupied label inventory `[0,2] ⊔ [m−6,m]` and the weight inventory `{1,2} ⊔ [m−6,m]`, each value occurring once in its inventory. Thus R=D=[3,m−7], of size m−9=q+a. The vacant named leaf slots at H, L and C number q−1, a−1 and two, respectively.

For every ordinary graceful labeling, `sum_v (degree(v)−1) f(v)` is even. Modulo two, each absolute edge difference equals the sum of its endpoint labels. The sum of all differences equals the sum of all vertex labels by the two bijections. On this original the excess degrees at H, L and C are q, a and two. The exit has excess degree one, the right center two, and the entrance contributes zero under the pins. Therefore the required parity is `q f(H)+a f(L)+2 f(C)+m+2≡0 (mod 2)`. The assigned H and m are odd, q is odd, and all other terms are even. This verifies the necessary condition. The full weight inventory is proved below.

## Reserved Batch B on L and C

Reserve labels `R_B={5,7,m−9,m−7}` and differences `D_B={3,5,m−11,m−9}`. In each set the displayed values are strictly increasing for m≥17, and all lie within the corresponding global interval. The absolute difference options are

| Label | At L | At C |
| --- | ---: | ---: |
| 5 | 3 | m−11 |
| 7 | 5 | m−13 |
| m−9 | m−11 | 3 |
| m−7 | m−9 | 1 |

The C option m−13 is even, so differs from 3 and 5, and is strictly smaller than m−11 and m−9. The option 1 is below D_B. Using eligibility in D_B, the graph has a reflected parallel pair on difference vertices 3 and m−11, with labels 5 and m−9 whose options exchange. Label 7 gives a forced L half-edge at 5, and m−7 gives a forced L half-edge at m−9. Each difference vertex is covered in precisely one component, and the counts of label resources and difference vertices within the components are two and two, one and one, and one and one. Every label has an eligible option. R226 with first host L gives A0=2, c=1, eta=0 and projection {2,4}. Choose L quota two, assigning its forced labels to `l:0:1:1,l:0:1:2` in the order 7,m−7. Assign the pair to C at `l:0:2:0,l:0:2:1` in the order 5,m−9. Their absolute weights in these orders are 5,m−9 and m−11,3, giving D_B exactly.

## Reserved Batch A on L and H

Set `R_A=R minus R_B` and `D_A=D minus D_B`. All residual labels are strictly between 2 and m−4. Put `d_L(x)=x−2`, `d_H(x)=m−4−x` and `rho_A(x)=m−2−x`. The increasing label interval R maps bijectively in reverse order to D under d_H. The four removed labels in the order 5,7,m−9,m−7 have d_H images m−9,m−11,5,3, precisely D_B. Thus d_H restricts to a bijection onto D_A.

Labels 3 and 4 both remain in R_A. Their lower options 1 and 2 are occupied, and their higher options m−7 and m−8 are in D_A. Reflection preserves [5,m−7], and the removals are exactly the two distinct complete pairs `{5,m−7}` and `{7,m−9}`. Each remaining label in that interval has its partner, and equality of partners would require twice an integer to be m−2, which is odd. The eligible options on each pair exchange by `d_L=d_H∘rho_A`. The corresponding sets of difference vertices are disjoint images under d_H, giving full coverage of D_A together with the two forced half-edges. Each component is balanced, and every label has an eligible option. After removing four Batch B labels and the two forced Batch A labels, exactly q+a−6 labels remain in pairs. Accordingly `c_A=(q+a−6)/2`.

With first host L, R226 gives A0=0, c=c_A, eta=0 and projection `{2j : 0≤j≤c_A, j integer}`. Set `j_A=(a−3)/2`. It is nonnegative, and `c_A−j_A=(q−3)/2≥1`. List the available pairs by increasing smaller label. Select the last j_A pairs for L, taking the empty selection when j_A=0. Each chosen pair is closer to the reflection center than each nonchosen pair. The resulting L palette S_A,L is reflection invariant and has 2j_A=a−3 labels. The H complement S_A,H within R_A has `q+a−4−(a−3)=q−1` labels including 3 and 4. Its higher-host images together with the chosen lower-host images exhaust D_A once because `d_L(S_A,L)=d_H(S_A,L)` as multisets and d_H is bijective on R_A. Attach the sorted palettes at L indices 3 through a−1 and H indices 1 through q−1. At a=3 the L index range and L palette are both empty. Its eligible rows still enter the R226 projection before the zero quota is imposed.

## Global reconstruction

The core and the reserved resources form disjoint label and difference partitions of [0,m] and [1,m], respectively. All batch labels are distinct integers avoiding the two corresponding host labels, with equally many reserved positive difference vertices as leaves per batch. Each batch has its two distinct named hosts in the supplied core and its own distinct vacant terminal positions. The two host sets intersect only at the unchanged L. Their pendant slots are disjoint and total q+a=m−9. The shared L receives a−3+2 additional leaves. The aggregate left quotas including the core are `(1+q−1,1+a−3+2,0+2)=(q,a,2)` in H,L,C order. Every positive-quota host is one edge from the core spine. These checks meet [R226.1 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-researcher), which consumes supplied disjoint reserved palettes and allows a repeated physical host. In this construction the core and both palettes are supplied by the formulas above.

In index order the terminal lists are H `(m−5, increasing S_A,H)`, L `(m−3,7,m−7,increasing S_A,L)`, C `(5,m−9)`, and right `(m−1,m−2)`. The core spine and center labels stay fixed. Independently of the batch corollary, the displayed label lists fill their disjoint palettes once. The direct Batch A image identity, the four actual Batch B weights, and the nine core weights give the full spectrum with multiplicity one. Thus both final unused inventories are empty and the original named graph is ordinary graceful.

Orient edges from the traversal class containing the entrance. All terminal edges toward L are negative because their labels exceed two. Every H or C terminal label is below its host, right terminal labels exceed the right center's label one, and all spine and center-attachment differences are positive in this orientation. Thus exactly the a terminal edges toward L are negative. These signs describe the result. The exit is the final spine vertex with exactly the two neighbors `s:0` and `b:1:0`, labeled 0 and 1. The latter is off-spine and the exit label is m. This verifies the [D112](ORDINARY_EXTREME_SPINE_GROWTH.md) premises.

Accept only exact integer types with q≥5, a≥3, and both odd. To implement the allocation, scan the available representatives of rho_A in integer order, retaining the innermost j_A, or none when j_A=0. Mark both endpoints of each chosen pair, then scan R_A in integer order and append labels to the corresponding indexed list. Emit all actual named slots and edges in their finite index ranges. This uses O(q+a) indexed output operations and terminates without search. The theorem concerns the fixed third quota two and right quota two. [D117](ORDINARY_QAR_ALL_PARITY_SUPPLIER.md) supplies its separate two-left-center domain.
