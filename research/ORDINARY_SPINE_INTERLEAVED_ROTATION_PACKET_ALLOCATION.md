# D136 — Interleaved rotation-packet allocation

## Theorem and state

Fix an exact integer p≥1 and h=2p+1. Supply the [D134 return state](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) on the actual named prefix with n edges, physical frontier v carrying either zero or n, declared polarity, oriented cut c and complete actual crossing spectrum [d,n]. Retain both graceful inventories, the ordered witnessing spine and all original incidences. In the oriented coordinates G the frontier label is zero. Require n−2c=h−1 and d−c=p+1, with 1≤c≤n and d≤n as in D134. All intervals are integer intervals, with reversed intervals empty.

Let r_j be independently prescribed exact positive integer quotas for actual centers j=0,...,2p. Set Q=sum_j r_j, N=Q−r_p and k=(h+Q+1)/2. Require even Q≥h+1 and n≥h+Q. The split k is integral and 1≤k≤Q. Require the quota moment sum_j (p−j)r_j=0. This moment is necessary for any permutation with these displacements by summing π(i)−i, and each invariant band separately has zero sum for the same reason.

The rule below supplies a permutation of [0,Q−1] preserving [0,k−1] and [k,Q−1], with displacement p−j exactly r_j times, whenever its deterministic block packing fits. Independently of the block widths, the following condition guarantees it fits:
```
Q ≥ N + A(p)
A(p) = (2p−1)(2p(p−1)+1).
```
It supplies the exact ordinary graceful extension and the same D134 state at fixed h. D134 and [D135](ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION.md) remain separate sufficient suppliers.

## Rotation packets

For each ordered pair 1≤a,b≤p take the permutation of [0,a+b−1] with π(i)=i+a for 0≤i<b and π(i)=i−b for b≤i<a+b. The respective images are [a,a+b−1] and [0,a−1], disjoint and exhaustive. The packet gives b actual tokens of +a at physical host p−a and a of −b at host p+b. Every coordinate is moved and there are no middle-host tokens.

The permutation is addition by a modulo a+b. Write g=gcd(a,b)=gcd(a,a+b). Returning to any start after s positive iterates requires a+b to divide sa. Dividing by g leaves coprime a/g and (a+b)/g, so the least positive such s is (a+b)/g. Every iterate stays in the starting residue class modulo g. The orbit length equals the number of positions in that residue class, so exactly g cycles result. Distinct classes have disjoint occupied positions, even when their interval spans overlap.

At a=b=p, the p transpositions have occupied positions {i,i+p} for i=0,...,p−1. Each interval span has p+1 positions. For p≥2, any two with starting positions i<j satisfy j≤i+p−1, so their interval spans overlap. Their occupied positions remain disjoint because the two ends occupy distinct residue classes between transpositions and different halves within each pair. A duplicate of the same residue-class cycle would reuse its two actual coordinates. The complete packet width is 2p. Reserving each entire span separately takes p(p+1), so the exact saving is p(p−1). This interleaving is supplied by the particular rotation formula.

## Weighted mass matching and actual token custody

Let P_a=r_(p−a) and M_b=r_(p+b). The moment gives sum_a aP_a=sum_b bM_b. Match the virtual masses aP_a and bM_b with two increasing cursors. At the least active pair (a,b) take z equal to the minimum of their remaining masses. The values are exact integers and z>0. Subtract z from both and advance each exhausted cursor. The sums still agree after the subtraction. When one side has no mass, the other has no mass, so the last match exhausts both remaining inventories. At least one active type disappears at each match and at least two disappear at the last. There were 2p types, giving between one and 2p−1 nonempty matches. A type that has disappeared never returns, so a pair is matched at most once.

For a matched triple (a,b,z), plan u=floor(z/(ab)) complete packets and e=z−abu. The exact integer inequalities 0≤e<ab follow from the definition of floor. These packets consume ub actual positive tokens of magnitude a and ua actual negative ones of magnitude b. Repeated packets have signed mass abu on either side.

Aggregate these actual consumptions at each type. The positive residue count P'_a=P_a−sum_b u_ab b and the negative residue count M'_b=M_b−sum_a u_ab a are integers by construction. Mass conservation at each type gives
```
a P'_a = a P_a − sum_b ab u_ab = sum_b e_ab
b M'_b = b M_b − sum_a ab u_ab = sum_a e_ab.
```
Only actual matched pairs appear in these sums. The right sides are nonnegative, proving both counts nonnegative, and the sums for a given type are divisible by that type's magnitude. Thus the planned packet groups cannot overdraw any actual token count. Both residual moments equal sum_over_matches e. These divisibilities apply to the aggregates. A single virtual match remainder may lack either divisibility. In the control z=ab−1 the floor is zero and a rounded-up packet would draw ab>z from that match. A nonempty control match has ab≥2. At ab=1 the proposed mass is zero, hence it cannot be a nonempty match. The exact aggregate identities still give integral residual counts.

Let R=sum_a P'_a+sum_b M'_b. By summing the divided aggregate identities,
```
R = sum_over_matches e(1/a+1/b).
```
This is a rational identity with an integer left side. Each term is strictly less than ab(1/a+1/b)=a+b and there is at least one match. Consequently R<sum_over_matches(a+b)≤2p(2p−1), with the strict bound R<2p(2p−1) also valid when R=0.

If R=0 there are no residual blocks and W_res=0. Otherwise send exactly the residual nonzero tokens through D135's bounded walk and stack. They have magnitudes at most p and total signed sum zero. Counts of zero for any type are skipped. At any current point the unused signed sum is the negative of that point. A negative point requires an available positive token, and a positive point requires a negative one. At zero, a nonempty remaining multiset has both signs. The chosen smallest available magnitude of the required sign keeps the walk in [1−p,p]. The stack extracts a closed suffix whenever a point repeats, records every traversed token once and ends at the single initial zero. Hence the D135 construction partitions these R tokens into cycles with at least two vertices, using at most 2p coordinates per cycle span. Filling holes in each residual block with fixed points gives R≤W_res≤pR. This also covers p=1, when the only packet matches equal masses of unit size, and there is no residual.

The complete rotation packets use exactly N−R coordinates because each consumes only nonzero tokens. Therefore
```
W_new = N−R+W_res
W_new ≤ N+(p−1)R ≤ N+(p−1)2p(2p−1).
```
The weak final bound includes p=1. The additive term estimates the cost of residual blocks and excludes any claim of optimality.

## Two-band packing and exact controls

Order the rotation packets by matching order, keeping repeated packets of a type consecutive. Follow with the residual blocks in extraction order. Every block has positive width at most 2p. Let T be the width of the longest initial sequence fitting within k. Place that sequence consecutively starting at zero, and all remaining blocks consecutively starting at k if W_new−T≤Q−k. Fill unused coordinates outside the blocks with fixed points. The two placements have disjoint ranges, and within each block each occupied coordinate and image occurs once. Thus each band is permuted exactly. The allocation has the prescribed nonzero multiplicities from the actual packet and residual tokens. Its fixed point count is (W_new−N)+(Q−W_new)=r_p, and every gap label is used.

If every block fits below k, the upper demand is zero, including if k=Q. Otherwise the next width w_next gives the exact integer slack 0≤k−T<w_next≤2p, so k−T≤2p−1. Then
```
W_new−T ≤ N+(p−1)2p(2p−1)−k+2p−1
        = N+A(p)−k ≤ Q−k.
```
Weak inequalities allow equality in the last capacity bound. This establishes coefficient one on N, independently of the actual deterministic width test. Failure of the test or of the conservative bound leaves other allocations open.

For the split control, place a whole packet at an offset that puts a strict interior boundary s between its coordinates, where 1≤s<a+b. At unshifted positions let i=min(s,b)−1 and j=max(s,b). Then i<s≤j<a+b. If s≤b then i=s−1 and π(i)=s−1+a≥s, while j=b and π(j)=0<s. If s>b then i=b−1 and π(i)=a+b−1≥s, while j=s and π(j)=s−b<s. Both arcs still have their prescribed displacements after translating the packet. Thus the globally valid packet fails both bands at any interior split, even in a larger permutation whose other blocks are disjoint. An upper source gives a lower image, so the upper crossing weights cannot be the required upper band.

## Strict improvement over the D135 block rule

Fix p≥2. Choose positive balanced counts on all smaller magnitudes 1,...,p−1 on each sign, such as equal counts at opposite signs, and let S be their nonzero count. Add t copies of +p and t of −p for independently varying exact t≥1, so N=S+2t. Choose one fixed positive middle quota M≥A(p) with M+S even and S+2+M≥h+1. Such M exists, and every t in the family gives even Q=N+M meeting the size and uniform capacity conditions on Q.

Consider D135's smallest-available-sign walk restricted to the smaller inventory. It is independently balanced, so before the smaller inventory is exhausted the walk's current point and the remaining smaller signed sum guarantee it has a token of the required sign. At zero both signs remain whenever there are tokens. Inductively the full D135 walk takes exactly those smaller tokens first because every one of the required sign is smaller in absolute value than p. After the S steps the point is zero, so the distinct-position stack has returned to its singleton zero. Subsequent steps alternate +p and −p and yield t separate transpositions, each spanning p+1 coordinates. Smaller cycles occupy at least S coordinates under D135's disjoint-span rule. Thus
```
W_old ≥ S+(p+1)t
W_old−Q ≥ (p−1)t−M.
```
For every t with (p−1)t>M, D135's chosen blocks exceed the total capacity before either band is considered. Reordering those blocks cannot help. The new uniform bound continues to admit every such t. This conclusion compares the two deterministic allocation mechanisms. For p≥3 start with symmetric smaller types and add two +1 tokens and one −2 token to them. Both magnitudes are smaller than p, all counts remain positive, their added moment is zero and the quotas are nonsymmetric. The preceding argument applies without any equality of opposite smaller counts.

For each declared quota vector choose a D134 initializer with its symbolic parameter c_0 sufficiently large in the admitted parity class. Its first returned size is 4c_0+4p+2 and grows unboundedly with c_0. In particular that size can be chosen to meet n≥h+Q for the declared vector. This uses D134's accepted initializer from a supplied maximum-port prefix, with the actual empty sections it prescribes. It asserts no simultaneous unbounded admission for a single finite prefix. No numerical initializer, quota vector or allocation is needed for the comparison.

## Exact ordinary transition and reusable return

Use m=n+h+Q+1 and the D134 oriented embedding F(old)=h+G(old)+Q indicator(G(old)≥c). Give the new last spine vertex w label m, center j its oriented label j, and terminal coordinate i label x_i=h+c+i. The complete label partition consists of the center block [0,h−1], low old band [h,h+c−1], gap [h+c,h+c+Q−1], high old band [h+c+Q,h+n+Q] and {m}. Attach label x_i to the actual center j=p+i−π(i) in [0,2p]. The host counter in increasing i specifies the next physical terminal index there, so the exact r_j leaves at every host are present once. Their differences are x_i−j=d+π(i), positive since every gap label exceeds all center labels.

Old noncrossing edges have unchanged weights [1,d−1]. Old crossing edges gain Q, giving [d+Q,n+Q]. The terminal permutation uses [d,d+Q−1] exactly. The actual connector from the old frontier v to w gives m−h=n+Q+1. Attachments to the h named centers have weights m−j, producing [n+Q+2,m]. These actual incidence groups give the complete graceful difference inventory, with no repeated weight. The new named spine vertex, centers and indexed terminals are attached in pendant order, giving a tree with h+Q+1 fresh edges and vertices. The spine extends by the actual connector and all center and terminal distances are at most two. Every old named incidence persists.

At oriented output cut c_out=h+c+k, the old cut sides are preserved because 0≤k≤Q. All centers are below c_out and w is above it. Terminal i crosses exactly when i≥k, so the two band permutations give [d,d+k−1] for noncrossing terminals and [d+k,d+Q−1] for crossing terminals. The connector, attachments and old crossing edges extend this latter interval to [d+k,m]. The crossing terminal interval is empty if k=Q.

For low input use F as the actual output and cut c_out. The actual old label translations on the low and high sides are h and h+Q. For high input use m−F and cut m+1−c_out. An actual old label below n+1−c has G≥c, hence translates by 1, and a label at or above that actual cut translates by Q+1. Both preserve actual side membership, with a side exchange in each of the two oriented complements in the high-input case. The spectral cut tracks the same actual crossing edges in either orientation. The new last spine vertex w has exactly v and the h fresh centers as neighbors and has opposite actual polarity.

In the next low-frontier coordinates,
```
n_new=m, c_new=m+1−c_out=c+k, d_new=d+k
n_new−2c_new=h−1, d_new−c_new=p+1.
```
The calculation uses 2k=h+Q+1. The new cut is positive and d_new≤n+Q<m, so it remains admissible. This is the exact D134 return interface, including the actual named frontier and polarity. Because all three suppliers return it, finite lists admitted step by step by any of D134, D135 or D136 at the same h close by induction, including the empty list. All allocation-side conditions for a fixed vector depend only on its quotas and h at that interface, so an admitted vector can repeat as the prefix size increases.

## Immutable final alphabet and operation bound

For a declared finite admitted list, at boundary i let C_i be its actual cut, A_i the sum of subsequent actual lower translations and S_i the sum of subsequent inserted gaps. By preservation of actual membership, the final composite adds A_i below C_i and A_i+S_i at or above it. Therefore applying the next local embedding and then its final composite equals the earlier composite pointwise on every previous vertex. Each label can be emitted once at its own first boundary, and the old endpoint of each next connector already carries its final label. The final-alphabet used and remaining labels at boundary i are
```
used      [A_i,A_i+C_i−1] ⊔ [A_i+C_i+S_i,A_i+n_i+S_i]
remaining [0,A_i−1] ⊔ [A_i+C_i,A_i+C_i+S_i−1] ⊔ [A_i+n_i+S_i+1,n_final].
```
The boundary weights become
```
used      [1,d_i−1] ⊔ [d_i+S_i,n_i+S_i]
remaining [d_i,d_i+S_i−1] ⊔ [n_i+S_i+1,n_final].
```
Only actual crossing edges gain S_i. For a step of size change n to m, with its own gap Q, split k and later gap sum S, its final newly consumed weights are [d,d+k−1], [d+k+S,d+Q−1+S] and [n+Q+1+S,m+S]. The previous boundary already occupies [1,d−1] and [d+Q+S,n+Q+S]. The five bands are disjoint and together yield [1,d+k−1] and [d+k+S,m+S]. These calculations verify the separate terminal bands on which D134's immutable realization depends. The fresh label reservation maps into the final alphabet via the injective composite of that boundary in its actual orientation. Every completed section has all its center and terminal incidences, leaving only the actual next spine connector between the supplied vertices and the unassigned suffix. Both residual inventories are empty at the final boundary.

Two cursor arrays give O(p) indexed arithmetic operations for matching, planning packet groups and subtracting aggregate token counts. Each packet can be represented by its magnitudes and repetition count. Expanding all packets takes at most O(N−R) operations for block iteration and coordinate emission. Use the D135 residual sign cursors and an array from position to stack index for O(p+R) operations. Each exhausted magnitude is skipped at most once per sign. Recording and popping extracted suffixes visits O(R) edges in total. Block placement and width scanning take O(N) operations. Filling fixed positions, assigning one displacement per coordinate and emitting names via host counters take O(Q+p) operations. The resulting per-section bound is O(p+N+Q) indexed arithmetic operations, with the prefix inspected once and sizes, cuts and polarities planned forward and final shift sums backward. This gives linear indexed operations in the complete output size, since N≤Q and h≤Q at each appended section. These bounds do not charge exact integer operations by bit length. Every walk step consumes a token, every match exhausts an active type, and all emissions use finite declared ranges.

The adopted [R226](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) and [R232](../references/upstream/mdl/N232_R232_joint_allocation.md) have separate supplied-palette obligations. Here balanced opposite-sign token masses supply new local packets before actual terminal emission. D134 and D135 retain their full independent domains. This theorem still uses a fixed odd center count, a balanced quota moment for these oriented host labels and the supplied cut-state initialization.
