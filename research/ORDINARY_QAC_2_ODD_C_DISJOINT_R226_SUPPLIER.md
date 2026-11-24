# D120 — Odd third quota by dual-reflection interval reservation

For independently chosen odd exact integers q≥5, a≥3 and c≥3, exact ordered `[[q,a,c],[2]]` admits a direct ordinary graceful labeling with `(s:0,s:1,b:1:0)=(0,m,1)`, where m=q+a+c+7. The construction has no alpha or signed-edge constraint.

## Named original and independent core

Take the spine `s:0--s:1`, the three centers H=`b:0:0`, L=`b:0:1`, C=`b:0:2` attached to `s:0`, and the center `b:1:0` attached to `s:1`. At each center `b:i:j` add one incidence to each named terminal `l:i:j:k` for k from zero through its quota minus one, at physical quotas q,a,c,2 in that order. A path with centers and terminals attached by single incidences is connected and acyclic. There are m edges and m+1 vertices. Centers and terminals have distances one and two from the stated spine. The three odd quotas sum to an odd integer at least eleven, so m is even and at least 18.

The independently specified core is the spine, the four centers, the index-zero leaves at H and L, and the two right leaves, retaining all their original incidences.

| Vertices in order | Labels |
| --- | --- |
| `s:0,s:1` | 0,m |
| H,L,C,`b:1:0` | m−4,2,m−6,1 |
| `l:0:0:0,l:0:1:0` | m−5,m−3 |
| `l:1:0:0,l:1:0:1` | m−1,m−2 |

This is the D118 ten-vertex tree form. Its nine edges have weights m on the spine, m−4,2,m−6,m−1 on the four attachments, 1,m−5 on the two left terminal edges, and m−2,m−3 on the two right terminal edges. These give disjoint occupied label bands [0,2] and [m−6,m] and disjoint weight bands {1,2} and [m−6,m], with distinct labels and positive distinct weights. Therefore R=D=[3,m−7], each of size m−9=q+a+c−2. The named vacant quotas at H,L,C are q−1,a−1,c.

Ordinary gracefulness implies that the sum of all vertex labels equals the sum of all edge weights. Modulo two each absolute difference equals the sum of its endpoint labels. Their difference is the sum of excess degrees times labels, even by those two identities. The only terms that can contribute here are q f(H), a f(L), c f(C), m for the exit, and 2 for the right center. The entrance label is zero. Each term in `q f(H)+a f(L)+c f(C)+m+2` is even in this core. This is the necessary parity check. The graceful bijections follow from the palettes below.

## Batch B and its available midpoint

Put s=(q+a)/2≥4 and k=(c−1)/2≥1, both integers. Then m=2s+2k+8, b=s+2, e=b+c+1=s+2k+4, and b+e=m−2. We have b≥6 and m−8−e=s−4≥0. Reserve R_B=[b,e], D_B=[b−2,e−2]. Both intervals are contained in the global residual intervals and each has e−b+1=c+2 distinct integers.

All labels in R lie strictly between L=2 and C=m−6. The L/C options are d_L(x)=x−2 and d_C(x)=m−6−x. Their reflection is rho_B(x)=m−4−x. The map d_L bijects R_B onto D_B. At e−1 and e the L options are e−3 and e−2. Using b+e=m−2, their C options are b−3 and b−4, both below b−2. These labels are forced to L by eligibility within D_B.

The remaining interval [b,e−2] has c labels and its endpoints sum to m−4, so rho_B preserves it. Its unique fixed label is t_B=(m−4)/2=b+k. Every other label in the interval belongs to one of k complete reflected pairs. A pair x,y=rho_B(x) gives the distinct weight vertices x−2 and y−2, with both labels eligible at both hosts and the host options exchanged. The eligible midpoint has both host options at the single weight t_B−2. It counts as one loop, consuming one label and one difference. Injectivity of d_L on R_B implies that the two forced half-edges, k parallel pairs, and one midpoint loop have disjoint difference vertices and together exhaust D_B. They have equal label and vertex counts component by component, and every label has an eligible row.

With L first, R226 has A0=2, pair count k, eta=1 and integral projection `{2+2j+epsilon : 0≤j≤k, epsilon∈{0,1}, j integer}`. Choose j=epsilon=0. Set S_B,L={e−1,e} and S_B,C=[b,e−2], assigning the ordered endpoints to L indices 1 and 2 and the increasing interval to C indices 0 through c−1. The quotas are exactly (2,c). Independently, the C weights in reverse order form [b−2,e−4], while the forced L edges supply e−3,e−2. This gives D_B once.

## Batch A and its removed midpoint

Set R_A and D_A to the respective complements of R_B and D_B. On R, the H option d_H(x)=m−4−x reverses the interval onto D. For rho_A(x)=m−2−x, the identity b+e=m−2 makes R_B invariant, and d_H(R_B)=[m−4−e,m−4−b]=[b−2,e−2]=D_B. Thus d_H restricts to a bijection from R_A onto D_A.

Reflection rho_A preserves [5,m−7]. Its arithmetic midpoint is t_A=(m−2)/2=b+k+1, in R_B and therefore absent from the Batch A palette. The remaining intervals are [5,b−1] and [e+1,m−7], exchanged by rho_A. The first lies strictly below t_A and gives exactly the smaller representatives. Both rows at each pair label are eligible because d_L=d_H∘rho_A and the restricted image is D_A. Labels 3 and 4 remain and are forced to H because their L options 1 and 2 are already core weights, while their H options m−7 and m−8 belong to D_A. The d_H bijection makes component weight sets disjoint and exhaustive. Each forced half-edge and pair is balanced, and every label has an eligible row. This includes lower-host rows in the quota-free pair graph when the chosen lower quota is zero.

There are b−5=(q+a−6)/2 available pairs, no eligible midpoint, and no forced contribution to L. The integral lower projection is every even integer from zero to twice that pair count. Select j_A=(a−3)/2 pairs, leaving (q−3)/2≥1 unselected. Take the innermost available pairs, represented by [b−j_A,b−1] for j_A>0 and by the empty set at j_A=0. Include both endpoints of each selected pair in S_A,L and put the rest of R_A, including 3 and 4, in S_A,H. The counts are a−3 at L and q−1 at H. The selected set is reflection invariant, so d_L(S_A,L)=d_H(S_A,L) as multisets. Combining with d_H(S_A,H) gives the direct difference bijection onto D_A. Fill L indices 3 through a−1 and H indices 1 through q−1 from their increasing palettes.

The two arithmetic midpoints differ by one. In Batch A the midpoint t_A is absent because it is reserved in B. In Batch B the eligible midpoint t_B belongs to C with the choice epsilon=0. Since k≥1, t_A=b+k+1≤e−2 and its rho_B partner t_B−1=b+k−1≥b both lie in the C interval. They are distinct, so t_A is a member of a nontrivial B pair. The two arithmetic midpoint values therefore give zero loops in A and one in B.

## Global reconstruction and physical premises

The two local instances use finite distinct integer label sets avoiding their host labels and equal-size sets of positive distinct differences. They satisfy the eligibility, balance and integral quota checks above. Their two actual host sets are both in the unchanged core and intersect exactly at L. The batches use distinct named slots, including separate L index ranges, and exhaust the unfinished original incidences. The aggregate counts in H,L,C order are (1+q−1,1+(a−3)+2,0+c)=(q,a,c). Both residual inventories split into their reserved palettes and every host with a positive quota is one edge from the witnessing spine. These hypotheses permit the reserved-palette assembly of [R226.1 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout).

The complete indexed terminal lists are H `(m−5, increasing S_A,H)`, L `(m−3,e−1,e,increasing S_A,L)`, C `(b,b+1,...,e−2)`, and right `(m−1,m−2)`. Retain all core labels. Independently of R226, these lists and the core use every label in [0,m] once by the disjoint partition. The two direct batch calculations and the nine core weights supply every difference in [1,m] once on the original named graph. This exhausts both inventories. Under orientation from the class containing `s:0`, left terminal edges point toward their centers. Exactly the a edges toward L are negative because all its terminal labels exceed 2. All H and C terminals are below their center, right terminals are above their center, and the spine and attachments are positive.

The terminal spine endpoint `s:1` has exactly the neighbors `s:0` and off-spine `b:1:0`, with labels 0 and 1, and carries the maximum label m. Together with gracefulness and the preserved spine, this checks [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s hypotheses. The construction terminates using O(q+a+c) indexed operations by checking exact integer types, minimum bounds and odd parities and scanning the finite index and label intervals. Mark selected pairs by indexed membership if needed. The scans emit increasing palettes directly without assignment search. Booleans and nonintegers are excluded.

[D119](ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER.md) uses parity progressions for even c≥2, while the odd domain here uses the centered interval. Together the two constructions cover every exact integer c≥2 for the stated odd q and a bounds and right quota two. D119 is an even-parity comparison in the finite audit. D120's quantified result follows from this interval proof.
