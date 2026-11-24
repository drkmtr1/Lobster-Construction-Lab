# D129 — Unified modified-core quota supplier

For independent even integers q,c≥4 and odd a≥3, the exact ordered original `[[q,a,c],[2]]` has an ordinary graceful labeling at pins `(s:0,s:1,b:1:0)=(0,m,1)`, where m=q+a+c+7. The rule supplies the D123 core and two disjoint pairs of reserved palettes directly. There is no alpha or signed-edge condition.

## Named core and resources

The original has its edge s:0--s:1, three left attachments from s:0 to X=b:0:0, M=b:0:1 and Z=b:0:2, and one right attachment from s:1 to b:1:0. Each center is incident to its own indexed terminal leaves, with index ranges 0 through q−1, a−1, c−1 and 1 respectively. These incidences are distinct and exhaust the original. Adding the centers and leaves successively as pendants to the spine proves the original is a tree with m edges and m+1 vertices. Centers have distance one from the spine, and terminals have distance two.

The core has the six spine and center vertices and four terminals. The following table gives the edge order induced by the original and every core difference.

| Actual incidence | Endpoint labels | Absolute difference |
| --- | --- | --- |
| s:0--s:1 | 0, m | m |
| s:0--X | 0, 2 | 2 |
| X--l:0:0:0 | 2, m−3 | m−5 |
| s:0--M | 0, m−6 | m−6 |
| M--l:0:1:0 | m−6, m−5 | 1 |
| s:0--Z | 0, m−4 | m−4 |
| s:1--b:1:0 | m, 1 | m−1 |
| b:1:0--l:1:0:0 | 1, m−1 | m−2 |
| b:1:0--l:1:0:1 | 1, m−2 | m−3 |

This ten-vertex subgraph is a connected tree by the same pendant construction. Since m is even and m≥18, its occupied label bands `[0,2] ⊔ [m−6,m]` are disjoint and injective. Its nine positive differences are exactly `{1,2} ⊔ [m−6,m]`. Thus both residual inventories R and D are `[3,m−7]`. The vacant physical quotas at X,M,Z are q−1,a−1,c.

For any graceful labeling f, an edge difference is congruent modulo two to the sum of its endpoint labels. Summing gives the degree-weighted label sum modulo two. The full vertex and edge inventories have the same total, since the extra vertex value is zero. Therefore the sum of `(degree(v)−1)f(v)` must be even. On this original with the three pins it is `qf(X)+af(M)+cf(Z)+m+2`. The pins contribute m at the exit, two at the right center and zero at the entrance. The core satisfies the identity because m and each left-center label are even. Gracefulness will follow from the integer inventories below.

## Independent split

Set `t=(m−2)/2`, `h=(q+a−3)/2`, `b=t−h=c/2+4`, and `e=t+h=q+a+c/2+1`. All are integers, h≥2, b≥6 and b+e=m−2. Thus `I=[b,e]` includes t−2,t,t+2, and its size is 2h+1=q+a−2. For q=4,a=3, h=2 and t−2=b, t+2=e. The complement `J=[3,b−1] ⊔ [e+1,m−7]` has interval lengths c/2+1 and c/2−1, with total c. In particular e≤m−8 and I lies in R. These inequalities use the independent lower bounds only.

The decreasing map `w(x)=m−4−x` sends the endpoints of R to m−7 and 3, so it bijects R onto D. Since b+e=m−2, it sends I onto `[b−2,e−2]`. Reserve the palettes below before assigning any labels. The identity `w(t+2)=t−4` gives a member of w(I).

| Batch | Hosts in increasing numerical-label order | Labels | Differences | Size |
| --- | --- | --- | --- | --- |
| A | X, M | I minus {t} | w(I) minus {t−4} | q+a−3 |
| B | M, Z | J plus {t} | w(J) plus {t−4} | c+1 |

The split partitions R by transferring one label from I to J and partitions D by transferring one weight from w(I) to w(J). All reserved values are distinct in each alphabet and all weights are positive. In either batch no residual label equals a host.

## Batch A

Every x in I lies above X and below M. Its raw options are `d_X(x)=x−2` and `d_M(x)=m−6−x`. On the reference palettes I and w(I), X is always eligible, while M is eligible exactly for x in `[b,e−2]`. Indeed d_M(b)=e−4, d_M(e−2)=b−2, and the two later M options are b−3 and b−4. Thus the two last labels are isolated forced X half-edges. For the eligible interval the reflection `rho(x)=m−4−x=2t−2−x` exchanges the two options, preserves that interval, and fixes only t−1, with the two tagged options both t−3. Each other reflected pair has two distinct difference vertices and two parallel edges, one per label, with reversed tags. Different pairs and the midpoint and forced rows occupy disjoint difference sets because d_X is injective on I and each component's weight set is its d_X image.

The pair {t−2,t} has weights t−4 and t−2. The deleted label t and the deleted vertex t−4 belong only to this component. Its remaining label t−2 is forced to M at t−2. Every other component persists. The intact smaller representatives are precisely `[b,t−3]`: the reference representatives run through t−2 and the last is the deleted pair's representative. This interval has h−2=(q+a−7)/2=P entries, including zero at h=2. Each isolated half-edge has one label and one weight. Each pair has two ordinary edges and two weight vertices. The loop has one label and one vertex despite its two host tags. These account for every eligible row and every reserved vertex with balance.

The R226 integral X projection is `{2+2j+epsilon : 0≤j≤P, j integer, epsilon in {0,1}}`. A pair must assign both labels to a single host: splitting repeats one weight and misses the other. Either complete assignment gives both weights. The loop can take either host and retains its weight. The two forced X labels contribute two and the forced M label contributes zero. To achieve q−1 choose j=(q−4)/2 and epsilon=1. The bounds follow from j≥0 and P−j=(a−3)/2≥0.

Take the first j representatives starting at b and include each reflected partner to form K. Set X's allocation to `K ∪ {t−1,e−1,e}` and M's to the remainder. X receives 2j+3=q−1. M receives the forced t−2 plus 2(P−j) labels, giving a−2. If q=4, K is empty even when a>3. If a=3, all intact pairs go to X. When both equalities hold the intact-pair list is empty and the forced rows and loop suffice. When q>4 and a>3, each host gets a nonempty set of whole pairs. The chosen allocation consumes exactly the two weights of each intact pair, the loop's one weight and each forced row's own weight. Disjointness across the actual components gives the complete reserved spectrum with multiplicity one.

## Batch B

Each residual label lies below both M and Z, so `d_Z(x)=w(x)` and `d_M(x)=w(x+2)`. At t, M gives t−4 in D_B and Z gives t−2=w(t) in w(I) and outside D_B. Neither option for any x in J can use t−4. Its coordinate would have to be x=t+2 for Z or x=t for M, both in I. Consequently t is an isolated forced M half-edge. Each x in J has its Z option, and its M option is eligible exactly if x+2 is in J. These equivalences use the reserved D_B only.

In difference coordinates w(x), each two-option J row links x to x+2. The gap I has at least five integers so no length-two step connects the intervals of J. The complete ordinary graph of J rows is the union of the maximal step-two chains in those intervals. The left interval has both parities because its length is at least three. For c=4 the right interval is a singleton, giving three nonempty chains in total. For c≥6 the right interval has both parities, giving four. Each chain with n entries has n difference vertices, n−1 distinct ordinary edges, and one Z half-edge at its largest coordinate, including n=1. It balances. At the smallest coordinate only the Z option of that label can supply the weight, because the preceding coordinate is absent. Inductively, once each earlier label uses its Z option, the next weight must come from its own label's Z option. Thus each chain has a unique extraction to Z. The isolated t component also balances, giving the sole M quota 1 and Z quota c. Directly the chosen weights are `{t−4} ⊔ w(J)=D_B`.

## Reconstruction and incidence checks

Output X terminals as m−3 followed by increasing A values for X. Output M terminals as m−5, increasing A values for M, then t. Output Z terminals as increasing J, and the right terminals as (m−1,m−2). Batch A occupies X indices 1..q−1 and M indices 1..a−2. Batch B occupies M index a−1 and Z indices 0..c−1. Each named leaf is adjacent only to its own host. These disjoint slots exhaust all unfinished incidences and give exact aggregate quotas q,a,c including the core leaves. The physical hosts of the two batches intersect only at the unchanged M.

The [adopted R226.1 revision-2 theorem](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout), Sections 3–7 and 10, applies. The core is an independently supplied injectively labeled tree with distinct actual differences in the full alphabets, each pair of physical hosts is distinct and in the core, and each positive-quota host has distance one from the retained spine. Each local label and difference palette has the prescribed size and all eligible rows and components meet balance and integral quotas. The named pendant slots are fresh relative to the core and disjoint across batches, their count is m−9, and neither batch changes either host's value or consumes the other's palette. Independently of the corollary, the direct component weight calculations and the two global residual partitions combine with the core bands to give the full bijections onto `[0,m]` and `[1,m]`. Every original incidence is counted once. Both final inventories are empty.

Orient incidences from the traversal class containing s:0 and take head label minus tail label. The left terminals are in this class, so precisely every X terminal and the reserved M terminal at index zero are negative. All other M terminals and every Z terminal lie below their centers. The left attachments and spine point from zero to positive labels. The right attachment and right terminal edges point from label one to labels greater than one. The signed pattern is descriptive. For D112 the exact named spine is s:0--s:1, s:1 is its exit with neighbors s:0 and the off-spine b:1:0, and these labels are respectively m, 0 and 1. No growth is required to establish this result.

Exact input guards require `type(value) is int` for all three quotas and check the respective bounds and parities, excluding bools and integer subclasses. A finite scan marks the selected reflected pairs and emits the palettes in increasing order. The slots and all labels take O(q+a+c) indexed operations, with no comparison sort or search for an allocation in the supplier.

## Pointwise specializations

- [D123](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) has q=c=u≥6 even and a=3. Then h=u/2 and j=P=(u−4)/2, giving every intact pair to X. Its X allocation is I minus {t−2,t}, its sole A value at M is t−2, and B and all physical indices agree.
- [D124](ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE.md) has a=3 and unequal even q,c≥6. Then h=q/2, j=P, and the same palette and indexed identities hold with independent c. This equality holds for either ordering of q and c.
- [D126](ORDINARY_634_2_MODIFIED_SHARED_MIDDLE_CORE.md) has (q,a,c)=(6,3,4). Again every intact pair goes to X, and b=6, e=12, t=9 give its exact core, allocations, slots and three-chain B reservation.
- [D128](ORDINARY_4A4_2_MODIFIED_SHARED_MIDDLE_CORE.md) has q=c=4 and odd a≥3. Then b=6, e=m−8 and j=0, so all intact pairs go to M. The X and M lists, both reserved palettes and every terminal index agree. This includes its symbolic zero-pair boundary.

These comparisons use the same modified core throughout. [D122](ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION.md) concerns a different labeled core and its obstruction retains that scope. [D125](ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH.md) retains its historical union, and [D127](ORDINARY_QAC_2_TWO_EVEN_OUTER_ODD_ROLE_TRANSPORT.md) retains its literal outer-odd domain.
