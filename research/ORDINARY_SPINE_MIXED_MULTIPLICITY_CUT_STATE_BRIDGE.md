# D137 — Mixed-multiplicity cut-state bridge and rigidity

## Exact state and scope

Use independent exact integers p,p'≥1. The named input is an ordinary graceful prefix with n edges, its ordered witnessing spine, actual last vertex v at one extreme, actual polarity and cut, and complete inventories as in [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md). In input coordinates G take the frontier label to be zero. The cut 1≤c≤n and exact crossing spectrum [d,n] satisfy n−2c=2p and d−c=p+1. Consequently n is even, c=n/2−p, d=n/2+1, and exactly n/2 old edges cross. The requested output has extreme last vertex, an oriented cut 1≤c'≤m with crossing spectrum [d',m], and m−2c'=2p', d'−c'=p'+1.

The appended section consists of one new spine vertex w, h≥3 actual centers at w and their respective positive exact integer terminal counts r_j for j=0,...,h−1. All names and indexed incidences are prescribed. There are Q=sum_j r_j terminals and H=h+Q+1 fresh edges, including vw. Put m=n+H, require H even, and write K=H/2. Assume n≥h+Q=H−1. Since n and H are even, n≥H and K≤n/2. The actual section multiplicity is h. The odd numbers 2p+1 and 2p'+1 parameterize the two states independently of h.

In the order-preserving two-translation class defined below, preserving old cut membership and the prescribed state contracts forces h=p+p'+1. Conversely, a canonical bridge exists under this equation with Q≥h+1 and the stated asymmetric allocation conditions. The equation alone leaves the placement and allocation feasibility problem open.

## Label embedding, cut membership and exact palettes

In oriented input coordinates allow the old placement E(x)=x+A for x<c and E(x)=x+A+s otherwise, with exact integers A≥0, s≥0, B=H−A−s≥0. Its image consists of [A,A+c−1] and [A+c+s,A+n+s]. These bands are in [0,m], are ordered, and are disjoint also when s=0. The fresh labels are
```
[0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [m−B+1,m].
```
Here and below a reversed interval is empty. We refer to the three intervals as the lower exterior, gap and upper exterior. This classification permits any fresh placement within the declared embedding class.

For an actual maximum-frontier input, complement both input and output coordinates before this analysis. In general conjugating by x↦n−x and y↦m−y maps the cut to n+1−c, with lower shift m−n−A−s=B and upper shift B+s. The former low side becomes the high side, including the correct strict below-cut convention at integer endpoints. The corresponding output cut becomes m+1 minus the actual cut. This exchanges old sides at both boundaries and preserves the same side-membership property, spectra and two-translation class. A polarity flip in oriented input coordinates is therefore a flip for either actual input polarity.

Old noncrossing differences remain [1,d−1]. Each old crossing difference gains s because the high endpoint moves s farther. Thus the occupied differences are exactly [1,d−1] ⊔ [d+s,n+s], and the fresh weights must be [d,d+s−1] ⊔ [n+s+1,m]. These bands are in range and no old weight collides. The output threshold is d'=m/2+1=d+K. All old crossing edges still cross, so their minimum d+s must be at least d+K. Thus s≥K and A+B=H−s≤K≤n/2.

## Forced polarity and the fresh upper count

If w had label zero in the output of E, the actual connector from v, which has label A, would have weight A≤K≤d−1. If A>0 this is already consumed by the old noncrossing edges. At A=0 it is zero, outside the graceful alphabet and also a vertex-label collision. In either case it is impossible. Therefore w has label m, so B≥1. The connector weight is m−A=n+s+B, in the upper residual band since A≥0 and B≥1.

In the same output coordinates, before reorientation about w, the return cut is C=m+1−c'=m/2+p'+1. Since old side membership persists, A+c≤C≤A+c+s. The old low and high bands are both nonempty, so both inequalities follow from their occupied endpoints. Write C=A+c+k, 0≤k≤s. The total count of positions at or above C is m−C+1, and exactly n−c+1 are old. Hence the fresh upper count is
```
U=m−C−n+c=K−p−p'−1.
```
All B upper-exterior labels are on that side. The other upper fresh labels are the s−k upper gap labels. Thus B≤U, s−k=U−B and U≤c−p'−1 by K≤n/2. In a putative solution U≥1. All lower-exterior labels are below the cut.

## Exterior connectivity and center-side rigidity

The upper residual difference band has A+B entries. No internal fresh edge touching the gap can attain one of them. Between gap and lower exterior the largest possible difference is attained by the upper gap endpoint and label zero, and is at most A+c+s−1≤n+s−p−1. Between gap and upper exterior, the minimum gap endpoint against label m bounds the difference by m−(A+c)=n+s+B−c≤n+s−p'−1. Within the gap it is at most s−1. All three bounds are below n+s+1. Within the lower exterior the difference is at most A−1, and within the upper exterior it is at most B−1. Both are less than d by A+B≤K≤n/2. An interval with no eligible endpoint makes the corresponding bound vacuous.

The connector has used one upper residual weight. The other A+B−1 distinct upper residual weights must come from internal edges among the A+B exterior vertices. The actual internal section is a tree consisting of w with its attached centers and each center with its own leaves. Its induced exterior subgraph is therefore a forest. With V=A+B≥1 vertices and at least V−1 edges, the forest must have one component, since each component of order u has u−1 edges. This includes the singleton w when V=1.

An upper-exterior center would attach to w with weight at most B−1<d. Thus no center is in that exterior interval. An exterior terminal must have its host in the exterior subgraph, because its only neighbor is its actual center and it must connect there to w. In particular an exterior terminal cannot belong to any gap center. A lower-exterior terminal would have its host in the lower exterior since no upper-exterior center exists. The resulting same-interval weight is at most A−1<d, which excludes it. As w is upper-exterior, every lower-exterior vertex is consequently a center.

Suppose a center lies at or above C within the gap. All its terminals must be in the gap, by exterior connectivity. No gap-to-gap incidence can cross the cut because its weight is at most s−1≤H−1<m/2+1=d', using n≥H. Therefore all terminals of that center must lie in the upper part of the gap. Its length s−k=U−B is at most c−p'−1−B<d. Each internal difference within that part is less than d, so it cannot supply a fresh difference. If the upper gap is empty the center is already excluded, and a length-one part has no two distinct labels there. Positivity of the center's quota now rules out every upper gap center. All actual fresh centers lie below C.

## Compatibility and scoped obstructions

The new crossing count is K since [d',m] has m/2 entries and n/2 old edges still cross. The connector crosses, all h attachments cross, and exactly U−1 terminal vertices are on the upper side. Their actual leaf edges cross because their centers are below C. There is no other new crossing incidence. Hence
```
K = 1+h+(U−1) = h+U
h = p+p'+1.
```
If h=2p'+1 is imposed, then h+U−K=p'−p. This exceeds zero for p'>p and is below zero for p'<p. Either mismatch excludes a mixed-state transition in the declared class before quota allocation. This rigidity uses the exact crossing spectra, extremes, size regime, one actual section, two old translations and cut membership. It gives no obstruction beyond those hypotheses.

## Canonical bridge and the asymmetric quota moment

Assume h=p+p'+1 and Q≥h+1, retaining H even and all other state and size hypotheses. When p+p' is even, h is odd and Q must be even. When p+p' is odd, h is even and Q must be odd. Now use A=h, s=Q, B=1, give w label m and give the center at actual index j label j. The gap labels are x_i=h+c+i for 0≤i<Q. The partition into centers [0,h−1], old low band [h,h+c−1], terminal gap, old high band [h+c+Q,h+n+Q] and {m} covers [0,m] once.

Use a permutation π of [0,Q−1] preserving the two bands split at K, with displacement p'−j exactly r_j times. Because 2K=h+Q+1 and Q≥h+1, K≤Q. Assign x_i to its actual named host j=p'+i−π(i), and scan gap indices in increasing order with the next terminal index counter per host. The displacement is bounded by the allowed host range, so j is always a physical center and each terminal index is emitted once. Here h+c−p'=c+p+1=d, hence x_i−j=d+π(i)>0. Conversely the canonical terminal inventory requires π to be a permutation. The prescribed return cut requires separate preservation of the two bands, as shown below. Summing displacements gives the necessary canonical moment sum_j (p'−j)r_j=0. The positive magnitudes are 1,...,p' and the negative magnitudes 1,...,p.

The two old spectra are [1,d−1] and [d+Q,n+Q]. Terminals use [d,d+Q−1] exactly. The actual connector has weight m−h=n+Q+1 and the attachments have weights m−j, namely [n+Q+2,m]. All actual incidence groups are disjoint and exhaustive. Every new vertex attaches by its specified parent to the tree, so the output remains a tree with the old witnessing spine extended by w. The new centers and terminals are at distances one and two from that spine. No old incidence or physical index changes.

## Asymmetric packet and residual allocation

Let L=p+p'=h−1, N=Q−r_(p') and assume the canonical moment. For positive type a≤p' and negative type b≤p, store virtual mass a times its actual positive token count and b times its actual negative count. These two total masses are equal. In increasing order of magnitude match the two least nonempty types with z equal to the lesser remaining mass. Subtraction exhausts at least one active type each time, and both at the final match because the remaining totals always agree. All matches are positive integers, there is at least one, and there are at most L−1 matches.

In a match (a,b,z) reserve u=floor(z/(ab)) complete [D136](ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md) packets. A packet rotates [0,a+b−1] by a modulo a+b, with disjoint images [a,a+b−1] and [0,a−1]. It uses b actual +a tokens and a actual −b tokens. Its width a+b≤L contains no fixed points. Write e=z−abu with 0≤e<ab. Subtract actual complete packet tokens at each type. Multiplying each integer residual count by its magnitude gives the sum of match remainders at that type, so the actual residual counts are nonnegative integers. Summing the identities across either sign gives equal residual mass sum e. Individual virtual remainders do not have to divide by either magnitude. The residual token count R is exactly sum_matches e(1/a+1/b), which is strictly less than sum_matches(a+b)≤L(L−1).

If R=0 there are no residual blocks. Otherwise use [D135's](ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION.md) sign-directed walk with the least available absolute magnitude of the required sign. Its unconsumed signed sum is the negative of its current position. This supplies a positive token at negative positions and a negative token at positive positions. At zero with tokens remaining, both signs are present. Starting at zero, adding a positive step at a nonpositive point in [1−p,p'] yields a point in [2−p,p']. Subtracting a negative magnitude at a positive point in that range yields a point in [1−p,p'−1]. Thus every point remains in [1−p,p'], which has L positions. Zero counts at a type are skipped. The distinct-position stack extracts the closed suffix on a repeat and retains its repeated endpoint. Each consumed token is assigned once either to an extracted cycle or to the current stack. The final position is zero and the stack is its singleton, so every token is in one recorded cycle. Each cycle has at least two vertices because the tokens are nonzero. Translating each cycle to its own span and filling its holes with fixed points gives at most R/2 blocks, each of width at most L. In particular
```
R ≤ W_res ≤ LR/2
W_new = N−R+W_res ≤ N+(L−2)R/2 ≤ N+L(L−1)(L−2)/2.
```
This uses L≥2 and holds also at zero residue and at L=2.

Order complete packets by matching order, followed by the recorded residual blocks. Take the longest initial block list of width T≤K and place it from zero. Place its tail from K if W_new−T≤Q−K. Each block then consumes a disjoint interval of its own band and permutes it. Filling all remaining positions with fixed points gives exactly Q−N=r_(p') zero displacements, including the residual block holes. Both bands are permuted, and the actual nonzero multiplicities were conserved.

When every block fits below K, upper demand is zero, including when the upper band is empty. Otherwise the next width is at most L and exceeds K−T. Hence K−T≤L−1. Therefore
```
W_new−T ≤ N+L(L−1)(L−2)/2−K+L−1 ≤ Q−K
```
whenever Q≥N+A(L), where A(L)=L(L−1)(L−2)/2+L−1. The product of the three consecutive integers is even, and all weak inequalities permit equality. This independent sufficient capacity bound can admit without computing the actual width test. Failure of either capacity condition leaves other allocations open. At p'=p, L=2p and A(L)=(2p−1)(2p(p−1)+1) as in D136.

## Independent positive domain

For any p,p'≥1 choose arbitrary positive packet multiplicities for (a,1) for every a from 1 to p' and (1,b) for every b from 2 to p. Each packet contributes equal mass on both signs. Every positive and negative magnitude receives at least one actual token, including negative magnitude one from (1,1). This independently prescribes the nonmiddle quotas at all actual host indices. The proof of the allocation applies to those counts by weighted moment and capacity, irrespective of whether the matching extracts those exact supplying packets. Choose the independent middle quota in the parity class making h+Q+1 even, sufficiently large for Q≥h+1 and Q≥N+A(L). Infinitely many such middle quotas exist and, independently, packet multiplicities may grow. This gives an infinite domain for every distinct pair p,p' and permits either parity of physical h according to the relation. For each declared input choose D134's symbolic initializer at p with parameter large enough for its first returned size 4c_0+4p+2 to be at least h+Q. Its empty sections are actual spine sections of the declared original. This argument uses a supplied maximum-frontier seed and does not require a numerical initialization or a fixed prefix working at every size.

## Return, closure and immutable final alphabet

Take C=h+c+K before reorientation. The old bands keep their cut memberships since 0≤K≤Q. Centers lie below C, and w lies above it because C≤h+c+Q≤m−1. Terminal i crosses exactly when i≥K. The two band permutations are what gives [d,d+K−1] for the noncrossing terminal edges and [d+K,d+Q−1] for the crossing terminal edges. The latter interval is empty when K=Q. Old crossing edges, the connector and the attachments extend that latter band to the full crossing spectrum [d+K,m], while the noncrossing inventory is [1,d+K−1].

If the input frontier is actually zero, use F as the actual output and C as the actual cut. The old lower labels shift by h and upper labels by h+Q. If the input frontier is actually n, use m−F and cut m+1−C. An actual low old label then has G≥c and shifts by 1. An actual high old label has G<c and shifts by Q+1. The two complements exchange both cuts' sides, so actual membership persists. Actual polarity flips. The named last vertex w has exactly v and its h centers as neighbors. In the next zero-frontier coordinates,
```
c'=m+1−C=c+K+p−p'
d'=d+K
m−2c'=2p'
d'−c'=p'+1.
```
Here 2K=h+Q+1, n−2c=2p and h=p+p'+1. In particular c'=n/2+K−p'≥1 because K≥h+1>p', and d'=m/2+1≤m. This verifies both oriented and actual cut bounds. For p'≠p these identities and the connector and terminal formulas give the symbolic positive control without emitting a section.

For any finite declared state list p_0,...,p_t, step i must have actual h_i=p_(i−1)+p_i+1. Equivalently the recurrence for prescribed multiplicities is p_i=h_i−1−p_(i−1). For the positive construction require each state parameter to be positive and each step to pass its quota, parity, size and allocation tests. Induct from the supplied cut state using the exact return above. The empty list changes nothing. The same-state cases make D134, D135 and D136 available under their respective sufficient conditions with h_i=2p_i+1, and admit finite lists mixing these steps with the bridges. Some multiplicity lists fail the state recurrence or other admission conditions.

At each boundary i write n_i,d_i for its normalized edge count and crossing threshold, C_i for the actual cut, A_i for the sum of later actual lower shifts and S_i for the sum of later gaps. Later low shifts are h_j or 1 by the actual polarity at that step, and later highs gain the same low shift plus Q_j. Because membership persists, the composite maps x to x+A_i below C_i and x+A_i+S_i above or at it. It agrees pointwise on old labels with applying the next embedding then its later composite. Thus each physical vertex may receive its final label only once, including the old endpoint of the next actual connector. The used and residual final-alphabet labels and weights are
```
used labels       [A_i,A_i+C_i−1] ⊔ [A_i+C_i+S_i,A_i+n_i+S_i]
remaining labels  [0,A_i−1] ⊔ [A_i+C_i,A_i+C_i+S_i−1] ⊔ [A_i+n_i+S_i+1,n_final]
used differences  [1,d_i−1] ⊔ [d_i+S_i,n_i+S_i]
remaining diffs   [d_i,d_i+S_i−1] ⊔ [n_i+S_i+1,n_final].
```
Each noncrossing difference is unchanged, each crossing difference gains S_i. At a step from n,d with Q,K and later gap sum S, the fresh final weights are [d,d+K−1], [d+K+S,d+Q−1+S] and [n+Q+1+S,m+S]. The previous weights are [1,d−1] and [d+Q+S,n+Q+S]. These five bands are disjoint and fill [1,d+K−1] and [d+K+S,m+S], verifying the return accounting for varying parameters. Fresh label reservations in the actual output coordinates map injectively into their final places and are disjoint from the previous labels because the local partitions are disjoint. The only incidence from the completed prefix to its unassigned suffix is the next original spine connector, when one remains. Both final inventories are empty at completion.

Weighted matching and packet planning use O(L) indexed arithmetic operations with count arrays and monotone cursors. The residual walk uses O(L+R) indexed operations with a coordinate-to-stack-index array and amortized suffix removal, as every token is recorded once. Scanning blocks and expanding the rotations takes O(N) operations apart from residual holes, which require at most O(Q) operations on acceptance. One increasing gap scan and host counters emit in O(Q+h) operations. The sizes, cuts and polarities are planned forward and remaining translations accumulated backward. The total admitted emission and planning cost is linear in the full indexed output because L=h−1, R≤N≤Q and each section adds h+Q+1 vertices. This is an indexed exact integer arithmetic bound, distinct from bit complexity. Every match exhausts a type, the walks consume finite token lists and all output is over finite declared ranges.

[D131](ORDINARY_SPINE_DEFICIT_TRANSITION.md), [D132](ORDINARY_SPINE_TWO_CENTER_AFFINE_TRANSITION.md) and [D133](ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION.md) retain their deficit, affine construction and scoped obstruction results. This bridge changes state multiplicity within the piecewise architecture. Its extreme-frontier and prescribed crossing hypotheses, the size bound, recurrence and canonical weighted allocation restrictions remain.
