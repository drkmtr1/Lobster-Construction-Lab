# D122 — Exact two-even fixed-core classification

For exact even integers q≥6 and c≥2 and exact odd integers a≥3, consider the exact ordered original `[[q,a,c],[2]]`, with physical H,L,C at `b:0:0,b:0:1,b:0:2`. The prescribed ten-vertex D118 core has an ordinary graceful completion **if and only if a≥5 or c≤q−4**. Both positive branches use two disjoint reserved R226 batches. The obstruction quantifies over every completion of these fixed labels on this original.

## Original, core and necessary degree parity

The spine is `s:0--s:1`. Attach H,L,C to `s:0` and `b:1:0` to `s:1`. Each center `b:i:j` has the actual incidences to `l:i:j:k` for integer k from zero through its quota minus one, with respective quotas q,a,c,2. The additions by single attachments make a tree, with centers at distance one and terminals at distance two from the spine. There are m=q+a+c+7 edges and m+1 vertices. By the bounds and parity, m is even and at least 18.

Take the two spine vertices, four centers, first terminals at H and L, and both right terminals. Their actual edges form the ten-vertex tree with nine edges. The labels at `s:0,s:1,H,L,C,b:1:0` are 0,m,m−4,2,m−6,1. At `l:0:0:0,l:0:1:0,l:1:0:0,l:1:0:1` they are m−5,m−3,m−1,m−2. The nine weights are m on the spine, m−4,2,m−6,m−1 on the attachments, 1 and m−5 at the two left leaves, and m−2 and m−3 at the two right leaves. The disjoint label bands are [0,2] and [m−6,m], and the disjoint weight bands are {1,2} and [m−6,m], each with multiplicity one. Thus R=D=[3,m−7], with vacant quotas q−1,a−1,c.

Modulo two, each actual edge weight equals the sum of its endpoint labels. The total of the graceful edge spectrum equals the sum of the graceful label alphabet. Hence the excess-degree weighted sum must be even. At these pins that sum is `q f(H)+a f(L)+c f(C)+m+2`, whose terms are all even in this core. This necessary check alone gives no completion. Set t=(m−2)/2, rho_A(x)=2t−x, and rho_B(x)=2t−2−x.

## Necessity for all completions

All residual labels lie strictly between L's numerical label and both higher host labels. The three weights for label x are d_H(x)=m−4−x, d_L(x)=x−2 and d_C(x)=m−6−x. The function d_H reverses R bijectively onto D. For any assignment filling exactly the named quotas with all chosen weights in D, apply d_H inverse to each chosen weight. The resulting P maps R to R. From the three weight formulas,

| Actual assignment | P(x) |
| --- | --- |
| H | x |
| L | 2t−x |
| C | x+2 |

The residual spectrum is D once precisely when P is a bijection, because d_H inverse itself is bijective. Each branch preserves parity, so each parity class of a bijection P is permuted separately. For either class p, subtract the input sum from the output sum to obtain

`0 = 2 N_C,p + sum(2t−2x over L labels x in class p)`.

Thus `N_C,p = sum(x−t over L labels x in class p)`. This identity assumes only successful completion and uses no reservation or cycle restriction.

Images 3 and 4 cannot arise from C, since the required preimages would be 1 and 2. They cannot arise from L, whose preimages would be m−5 and m−6, both above m−7. Therefore the image 3 must come from label 3 at H, and the image 4 from label 4 at H.

For a=3 there are exactly two residual L labels. If one is even and one odd, summing the two class identities gives c=x_even+x_odd−2t, an odd integer, contrary to the domain. If both lie in the same class, the other class has no L terms and hence zero C assignments. All c C labels and the two L labels must then fit in one class after removing 3 and 4. The remaining range [5,m−7] starts and ends odd, with (m−10)/2 odds and (m−12)/2 evens. Hence

`c+2 ≤ (m−10)/2 = (q+a+c−3)/2`.

At a=3 this is c≤q−4. Because c and q are even, the excluded sector is exactly a=3 and c≥q−2. This rules out every assignment completing these fixed labels. It gives no exclusion for a different labeled core, numerical role assignment, pin configuration or unrestricted gracefulness.

## Positive Batch B with two lower vacancies

When a=3 and c≤q−4 use Construction I. In general its stated bound c≤q+a−7 ensures b=t−c−1=(q+a−c+3)/2≥5. Set e=t+c+1 so b+e=2t and e≤m−7. Take R_B as the progression b,b+2,…,e with c+2 labels and D_B=d_L(R_B), also of size c+2. Both palettes lie in R,D. The reflection rho_A preserves this progression, which has parity opposite to t.

Every L option lies in D_B. The C option equals d_L(rho_B(x)). Because rho_B(x)=rho_A(x+2) and R_B is rho_A-invariant, C is eligible exactly when x+2 belongs to R_B. Thus e has the sole forced L row. The remaining c+1 labels in the progression through e−2 are rho_B-invariant. The midpoint t−1 is one of them since t−1−b=c is even, and the rest form c/2 complete pairs. Each pair x,y=rho_B(x) gives the two distinct difference vertices d_L(x),d_L(y) and the exchanged host tags. The midpoint uses a single vertex d_L(t−1) with two eligible host choices. The forced half-edge uses d_L(e). The d_L bijection makes these components disjoint and exhaustive. Each is balanced, with no unavailable label.

The integral lower projection is `{1+2j+epsilon:0≤j≤c/2, j integer, epsilon∈{0,1}}`, from A0=1, c/2 pairs and one loop. Choose j=0 and epsilon=1. Put t−1,e at L and the c paired labels at C. Each pair at C uses its two weights once in reversed order, while the L midpoint and half-edge use their two distinct weights once. This directly completes D_B and supplies quotas (2,c).

## Positive Batch B with four lower vacancies

For every a≥5 use Construction II. Put k=c/2≥1, b=t−k−2=(q+a+1)/2≥6 and e=t+k+2. Thus b+e=2t and e≤m−7. Take R_B=[b,e] with t removed, and again D_B=d_L(R_B). The size of each is 2k+4=c+4. They lie in R,D and rho_A preserves R_B because it preserves the interval and its deleted midpoint. No upper bound on c is needed.

Every L option is eligible, and by the same reflection identity the C option is eligible precisely when x+2 is in R_B. The only failures are x=t−2, with x+2 at the hole, and x=e−1,e, with x+2 above e. These three labels are available and distinct since k≥1. All other labels have both rows. The set of two-option labels is rho_B-invariant: whenever x and rho_B(x) belong to R_B, the same property holds for the partner. It contains t−1, since t−1 and t+1 are within R_B. After the three forced labels and one midpoint are removed, c labels form c/2 pairs. As in I, d_L identifies the disjoint components with all of D_B: three isolated half-edges, the loop and the parallel pairs. Their label counts equal their difference-vertex counts.

The integral lower projection is `{3+2j+epsilon:0≤j≤c/2, j integer, epsilon∈{0,1}}`, with A0=3 and one loop. Choose j=0 and epsilon=1. Assign t−2,t−1,e−1,e to L and all paired labels to C. Using d_L at the four singletons and d_C=d_L∘rho_B on the complete C pairs gives every reserved weight once. The quotas are (4,c).

## Complementary Batch A

Write s=2 for I or s=4 for II. In both cases rho_A preserves R_B, so d_H(R_B)=d_L(rho_A(R_B))=D_B. Set R_A and D_A as the complements of the B palettes. The restriction of d_H bijects R_A onto D_A. Labels 3 and 4 remain and are forced to H because their lower options 1 and 2 are core weights. All remaining A labels are in the rho_A-invariant complement within [5,m−7]. The midpoint t is in this complement: I uses the opposite parity and II deletes t. It has one equal-weight loop with both hosts eligible. Every nonfixed label belongs to a complete pair, both options eligible by d_L=d_H∘rho_A. The d_H bijection makes the two half-edges, loop and pairs disjoint and exhaustive, each balanced. At zero lower quota the eligible L rows still belong to the quota-free graph.

There are q+a−2−s labels in R_A. Removing two forced H labels and the midpoint leaves (q+a−s−5)/2 pairs. With L first, A0=0 and eta=1, so the lower projection is `{2j+epsilon:0≤j≤(q+a−s−5)/2, j integer, epsilon∈{0,1}}`. Choose j_A=(a−1−s)/2 and epsilon_A=0. This is nonnegative in the selected branch and the unused pair margin is (q−4)/2≥1. Take the innermost j_A available pairs, ordered by the smaller representative, or none when j_A=0. The selected lower palette is reflection invariant and has a−1−s labels. Assign the remaining q−1 labels, including t,3,4, to H. Directly, the L weights on the selected pairs equal their d_H images as a multiset, and together with the complement at H fill D_A once.

## Named assembly and exact scope

Use H index zero and L index zero from the core. Fill H indices 1 through q−1 with its increasing A palette. Fill L indices 1 through s with its increasing B palette and indices s+1 through a−1 with its increasing A palette. Use the increasing C palette at indices 0 through c−1. The right indices 0 and 1 remain m−1,m−2. The two batches use distinct actual named vacancies, with two distinct core hosts per batch and shared host L alone. Every vacancy is filled once, and the counts including the core are q,a,c. Both batches use distinct integer labels avoiding the hosts and equal-size positive distinct difference palettes. The two local feasible quota slices and global disjoint partitions therefore satisfy [R226 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). All positive-quota hosts are one edge from the witnessing spine.

Independently, the named labels fill [0,m] once by the core and residual label partition. The nine core edges and the two direct batch calculations fill [1,m] once on the actual incidences. All names, indices, roles and edges retain their original identities. In the orientation from the class of `s:0`, exactly the a terminal edges into L are negative, because their labels exceed 2. Left terminals at H and C are below their hosts, right terminals are above their host, and both spine and attachments have positive signed differences. The maximum label is at the terminal spine endpoint `s:1`, whose only neighbors are `s:0` at zero and off-spine `b:1:0` at one. This verifies [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s premises without a growth application.

Reject invalid exact types, minima or parities before classifying. For valid inputs with a=3 and c≥q−2, return the parity-class obstruction without a candidate labeling. Otherwise choose I at a=3 and II at a≥5. Generate palettes by bounded scans and use indexed membership marks for the selected Batch A pairs. Ordered output requires no search or sorting. The scans and exact named output take O(q+a+c) indexed operations and terminate. This proves both directions on the declared ordered fixed-core sector.
