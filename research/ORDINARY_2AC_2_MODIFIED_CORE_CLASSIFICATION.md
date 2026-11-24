# D130 — Exact quota-two modified-core classification

For independent exact odd integers a≥3 and exact even integers c≥4, consider the original ordered `[[2,a,c],[2]]` at pins (0,a+c+9,1). The specified D123 labeled core admits a graceful completion if and only if a≤c−1. Every positive completion has the same allocation of residual label values to X, M and Z. Within a host its residual labels can be assigned to its vacant indices in any order.

## Core, necessary sum and fixed-core obstruction

Let m=a+c+9 and t=(m−2)/2. Thus m=2t+2 is even and at least 16. The original has the spine s:0--s:1, three attachments at s:0 to X=b:0:0, M=b:0:1 and Z=b:0:2, and the attachment at s:1 to b:1:0. The centers have respectively 2,a,c,2 indexed pendant terminals. The named spine and these disjoint incidences form a connected tree with m edges and m+1 vertices. The centers are distance one from the spine, and the terminals distance two.

The D123 core consists of the spine and four centers, the index-zero terminals at X and M and both right terminals. Its nine incidences are listed in original order.

| Incidence | Labels | Weight |
| --- | --- | --- |
| s:0--s:1 | 0,m | m |
| s:0--X | 0,2 | 2 |
| X--l:0:0:0 | 2,m−3 | m−5 |
| s:0--M | 0,m−6 | m−6 |
| M--l:0:1:0 | m−6,m−5 | 1 |
| s:0--Z | 0,m−4 | m−4 |
| s:1--b:1:0 | m,1 | m−1 |
| b:1:0--l:1:0:0 | 1,m−1 | m−2 |
| b:1:0--l:1:0:1 | 1,m−2 | m−3 |

The core is a connected tree with ten vertices because it retains the spine and only pendants are needed to recover its centers and leaves. Its labels `[0,2] ⊔ [m−6,m]` and weights `{1,2} ⊔ [m−6,m]` are injective in their respective alphabets. The residual inventories are therefore R=D=[3,m−7] and the vacancies are (1,a−1,c). The ordinary excess-degree parity sum at the pins is `2f(X)+af(M)+cf(Z)+m+2`, which is even. This follows by summing the congruence between an absolute edge difference and the sum of its endpoints' labels and using equality of the full vertex and difference sums.

Every x in R lies strictly above X and below M and Z. Define `w(x)=m−4−x`, a bijection R→D. The actual residual weights are `x−2`, `m−6−x` and w(x), respectively. Subtracting w(x) gives, in X/M/Z order, `2(x−t), −2, 0`. Every completion uses each residual label once. Its weight sum equals the sum of D, which also equals the sum of w(x) over R. Thus the sum of x−t over X assignments equals the number of M assignments, namely a−1. This necessary identity is valid for the general modified core whenever these host formula ranges hold and M has a−1 residual vacancies.

The sole X vacancy forces `U=t+a−1`. The inequality U≤m−7 is equivalent to `a−1≤t−5`, or `2a+8≤a+c+7`, hence a≤c−1. Since a is odd and c is even, the complement in the exact parameter domain is a≥c+1. There the required X label falls outside R, so every completion of this labeled core is impossible. This deduction is independent of any choice of reservations or named permutation. It concerns the specified core. D122's obstruction concerns its own different labeled core.

## Positive resources and coordinates

Assume a≤c−1 and set `L=t−(a−1)=(c−a+9)/2`. Then L≥5, U≤m−7 and L+U=2t. Let S be the step-two progression from L to U, inclusive, and let J=R minus S. The progression has a distinct values, all in R and of the same parity as t because a−1 is even. The residual alphabet has m−9=a+c values, so J has c.

Supply A on X/M with labels S minus {L} and weights `w(S minus {L+2})`. Supply B on M/Z with labels J plus {L} and weights `w(J plus {L+2})`. The label and weight partitions are disjoint by the disjointness of S,J, the transfer of one element in each coordinate alphabet, and the bijection w. Each batch has equal numbers of labels and weights, respectively a−1 and c+1.

In coordinates z=w⁻¹(d) the host options for residual labels are X: `2t−x`, M: `x+2`, Z: x. These formulas apply whenever the resulting coordinate belongs to the batch's reserved coordinate set. The same formulas also characterize global eligibility with coordinate set R.

## Batch A

The A coordinate set is S minus {L+2}. Label U has the X coordinate L, and its M coordinate U+2 is out of the reserved set. Label U−2 has the M coordinate U, and its X coordinate L+2 is removed. The resulting forced half-edges have distinct isolated vertices. Among the remaining A labels, precisely the step-two progression from L+2 through U−4 occurs, with an inverted range interpreted as empty. This progression is the set of **all intact pair labels**, so counting each pair once requires taking its smaller member. The pairs are the orbits of `r(x)=2t−2−x`: it exchanges the progression's two endpoints whenever it is nonempty and its midpoint t−1 has opposite parity to S. The smaller representatives run by two from L+2 up to t−2 when nonempty.

For each intact label x, both options are eligible and distinct, and the reflected partner interchanges those two host tags. Their coordinate set is `{x+2,r(x)+2}`. The progression shifted by two is precisely the remaining coordinate set after removing the forced coordinates L,U. Translation is injective, so all pair components have disjoint vertices. There are (a−3)/2 intact pairs, because removing L,U−2,U from S leaves a−3 entries. Each pair balances with two ordinary edges and two vertices. Each half-edge balances with one label and one vertex. All rows and vertices are accounted for and there is no midpoint loop.

A pair must be allocated wholly to one host, since splitting it repeats one coordinate and misses the other. Either whole allocation covers the same two coordinates. The exact integral X projection is `{1+2j : 0≤j≤(a−3)/2, j integer}`. Choose j=0, sending U to X and every other A label to M. Directly their coordinate sets are `{L}` and the progression from L+4 through U by two, respectively, and partition S minus {L+2}. The exact local quotas are (1,a−2). At a=3 only the two forced half-edges remain.

## Batch B

At L, the Z coordinate L is unavailable and the M coordinate L+2 is reserved. No J label can reach L+2 through Z since L+2 belongs to S. Through M the only preimage is L itself. Thus L gives an isolated forced M half-edge. Every x in J has its Z coordinate x available and its M coordinate available precisely when x+2 is in J. The only additional possible coordinate L+2 would again require x=L.

The connected components on J are its maximal step-two chains. The parity opposite to S is a single full progression of that parity in R. The same parity as S has a lower progression of labels below L and a possible upper progression above U. The lower progression is nonempty because both 3 and 4 are below L, and either parity occurs there. The upper progression is empty if U is the last R label of its parity. Removing the nonempty middle progression S separates the two same-parity portions, and edges never change parity. These describe every ordinary edge and isolated vertex.

A chain of n labels has n distinct difference vertices, n−1 ordinary edges and one forced Z half-edge at the largest coordinate. This includes a singleton. Every chain balances. At its least coordinate only the Z option of that same label can supply the weight. Repeatedly applying the same argument to the next coordinate forces every chain label to Z. Thus the exact M projection is {1}, and assigning L to M and J to Z gives quotas (1,c). The actual chosen weights are `{w(L+2)} ⊔ w(J)` with multiplicity one.

## Named reconstruction and R226 custody

At X emit (m−3,U). At M emit m−5, the increasing step-two progression from L+2 to U−2, then L. At Z emit increasing J. At the right center emit (m−1,m−2). A fills X index 1 and M indices 1..a−2. B fills M index a−1 and Z indices 0..c−1. Each named leaf has precisely its original incidence to the designated host. The slots are disjoint and exhaust all unfinished incidences. The two host pairs intersect only at unchanged M. Including the core, the physical quotas are 2,a,c and two right terminals.

The adopted [R226.1 revision-2 theorem](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout), Sections 3–7 and 10, applies. The independently specified core is a labeled tree with injective labels and distinct actual weights in the global alphabets. The hosts in either batch are distinct unchanged core vertices at distance one from its witnessing spine. The label and weight palettes are finite and disjoint from core resources, avoid the host labels, have positive weights, and form the complete global residual partitions. Each batch supplies equally many fresh named pendant incidences as its palette size and precisely the nonnegative prescribed physical quotas. The host-tagged graphs have no unavailable rows and satisfy each balance and integral quota condition. The direct coordinate allocations give exact bijections to the reserved spectra independently of the corollary. Together with the core inventories these prove both full original bijections onto `[0,m]` and `[1,m]`.

The signed diagnostic in the traversal orientation from s:0 has precisely the two X terminal edges and the index-zero M terminal edge negative. Every residual M or Z terminal label is below its host. The right attachment and right terminals point from the right center, whose label is one, toward higher labels. The D112 exit s:1 has the exact neighbors s:0 and b:1:0, at labels zero and one. The exit's label is m and the right center is off the unchanged spine. No growth was required. Type guards require exact integers, excluding booleans and integer subclasses, and enforce the stated parities and bounds. One finite scan of R in increasing order emits S and J with O(a+c) indexed operations and no assignment search.

## Forced host allocation in every positive completion

For any successful completion define P(x) as the coordinate of the actual weight for label x. Because both absolute weight alphabets are fully consumed, P is a permutation of R. The lone X assignment is at U and sends U to L. Z assignments are fixed points, and an M assignment increases its coordinate by two.

In the permutation cycle through U, the next point is L<U. Every point in that cycle before the return to U must be M. It cannot be Z because a fixed point has a singleton cycle, and there is only one X label. Therefore the return path is exactly `L,L+2,...,U−2,U`. It has a−1 M labels, exhausting the M vacancies. All remaining labels must be Z. This proves uniqueness of the label-to-host allocation over all completions of the fixed core. Named permutations of vacant same-host terminal indices retain the spectra and leave the core unchanged.
