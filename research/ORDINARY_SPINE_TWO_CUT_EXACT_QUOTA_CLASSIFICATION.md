# D140 — Exact two-band quota classification for D139's placement

## Exact scope and theorem

Use [D139's](ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE.md) strengthened D134 p=1 input. The supplied named ordinary graceful prefix has even edge count n, ordered witnessing spine, and actual extreme frontier. Its zero-frontier orientation has cut c=n/2−1 and exact crossing spectrum [d,n] with d=n/2+1. Its actual degree-one off-spine terminal u has oriented label c−1 and unique edge u–z to its actual host z at label n−1 of weight d. Retain both names and the incidence.

Append one actual spine vertex w and the three named physical centers with oriented labels 0,1,2 and independently prescribed positive exact quotas r0,r1,r2. Write Q=r0+r1+r2, H=Q+4, K=H/2, m=n+H. Require Q even and n≥H. Fix an exact integer t>0 with Q−t>0. All structural parameters and labels are exact integers, excluding booleans. Use D139's exterior widths 3 and 1, cuts c−1 and c, gap sizes t and Q−t, and w at label m. The exact allocation problem is a bijection
```
I=[−1,Q−1] minus {t−1}  →  J=[0,Q] minus {Q−t}
```
with displacements in {−1,0,+1}, preserving each band split at K and fixing K. Every source i represents its actual terminal label x_i=3+c+i and goes to physical host j=1+i−π(i). All intervals are reversed-empty when their upper endpoint is below their lower endpoint.

In this scope the exact feasible quotas at fixed t are
```
(r0,r1,r2)=(2t+z,2b,z),  with t,b,z≥1 and b+z≥3.
```
If selecting t from the prescribed quotas, feasibility is equivalent to r0−r2 positive even, r1 positive even and r2+r1/2≥3, with the inherited size and named-state hypotheses. Then t=(r0−r2)/2 is forced. The theorem supplies each feasible case by an indexed rule and returns the strengthened input.

## Hole positions and actual forced chains

The original edge u–z stays across the designated cut and has moved weight d+Q−t. The output crossing threshold is d+K, so Q−t≥K is necessary. Fixing K requires K in J, excluding equality. Therefore
```
Q−t ≥ K+1.
```
The same conclusion follows for the abstract two-band problem before using any weight condition. Even Q and the positive quotas give Q≥4 and K≤Q. There are K+1 raw sources below K, with at most one removed, and there are K raw destinations below K, with at most one removed. Equal counts require the source hole below K and the destination hole at or above K. Fixing K again excludes equality for the latter. In particular Q=2K−4 gives t≤K−5, so t−1 is strictly below K and K is in I and J when the strict hole inequality holds.

The lower source −1 can only map to 0, since J has no negative coordinates and the maximum step is one. Inductively for each i from zero through t−2, any admissible destination at most i is already occupied or absent. Indeed all targets from 0 through i have been used by earlier sources −1 through i−1, and any negative destination is absent. The only remaining allowed image is i+1. This gives the first full chain from source [−1,t−2] to destination [0,t−1], with t shifts of +1. At t=1 it consists of −1→0 alone. The destination t−1 exists below K and the next source t−1 is the hole.

The upper destination Q has only source Q−1 within distance one, because larger sources are absent. Proceed backward. For source i from Q−2 down to Q−t, destination i+1 can be reached only from i,i+1,i+2. Any of the latter two that exists has already been assigned to its strictly larger image. Thus surjectivity forces i→i+1. This gives precisely the second forced chain from [Q−t,Q−1] to [Q−t+1,Q], with t shifts of +1. At t=1 the descending induction has no additional step. Both chains lie wholly in their required bands and their source and destination ranges are disjoint. The final imposition of K→K uses neither chain.

Remove the two chains and K on both sides of the bijection. Below K both residual sets are [t,K−1], of length L=K−t. Above K both residual sets are [K+1,Q−t−1], of length U=Q−t−K−1. The latter is empty at equality Q−t=K+1. There is no transfer between the two intervals because the original map preserves bands and K is used. These are the exact independent flexible intervals.

## Complete structure of the flexible allocations

Let a be the least coordinate in a nonempty consecutive interval that is permuted within itself with step size at most one. Its image is a or a+1, with only a available for a singleton. In the first case delete its fixed point. In the second case surjectivity at a forces a+1→a, since the only candidates are a and a+1 and source a already went to a+1. Delete this adjacent pair. In both cases the remaining coordinates form a consecutive interval and the remaining map is a bijection on it. The empty interval needs no step. Induction proves all permutations in this class consist exactly of fixed points and disjoint adjacent transpositions. Conversely every such choice has the required displacement and spectrum.

A transposition contributes one +1 and one −1 displacement, a fixed point contributes a zero, and both forced chains contribute 2t positive displacements. Physical labels 0,1,2 receive +1,0,−1 respectively. Hence the total number of transpositions is z=r2,
```
r0−r2=2t,
z≤floor(L/2)+floor(U/2).
```
The capacity on an interval of length a is exactly floor(a/2): every pair consumes two coordinates, and taking successive pairs from its beginning attains the bound. Every integer between zero and capacity can be attained by stopping at that many pairs. K supplies one of the zero displacements, in addition to the fixed points on the two intervals.

Since Q is even and r0+r2=2t+2z, r1 is positive even, say r1=2b with b≥1. Then
```
Q=2t+2z+2b,  K=t+z+b+2,
L=z+b+2,      U=z+b−3.
```
The strict upper-hole inequality is equivalent to U≥0 or z+b≥3. Put v=z+b. For v=2a, the floor capacities are a+1 and a−2, where v≥3 entails a≥2. For v=2a+1, the capacities are a+1 and a−1, where a≥1. In either case
```
floor((v+2)/2)+floor((v−3)/2)=v−1=z+b−1.
```
This includes U=0 and gives at least z because b≥1. Thus capacity is automatic once the exact parity, positive moment and hole conditions hold. This proves necessity and the availability needed for sufficiency. Conversely if the variable-t tests hold, the chosen t>0 and positive b=r1/2,z=r2 produce exactly these formulas, Q even and Q−t>0. Neither formulation supplies the inherited size or named input.

## Indexed construction and exact named return

Set `ell=min(z,floor(L/2))` and `u_count=z−ell`. If ell=z, the upper count is zero. Otherwise ell is the lower capacity and the proved total inequality gives `u_count≤floor(U/2)`. Take ell adjacent transpositions beginning at t, and u_count adjacent transpositions beginning at K+1, pairing consecutive coordinates. Fix all other flexible points and K. For an empty upper interval its capacity and its chosen count are zero. Apply both forced chains unchanged. The disjoint source and destination partitions above and these interval permutations give the required bijection preserving both bands. The displacement counts are
```
+1: 2t+z
 0: L+U−2z+1 = 2b
−1: z.
```
The added one in the zero count is exactly K. Scan the Q source coordinates in increasing order. For each one, emit the next zero-based terminal index at its actual host j. Below K, the first chain consists only of host-0 terminals. The lower flexible interval has L−2ell fixed points exactly, all and only its host-1 terminals. Therefore the actual center-1 terminal at coordinate K has zero-based index L−2ell. It is within its quota since it accounts for one of the 2b zero displacements.

The indexed rule fills D139's actual fresh label inventory. Its old three-band placement is increasing and its old weight groups are
```
[1,d−1], {d+Q−t}, [d+Q+1,n+Q].
```
D139's shift proof applies here because the only old incidence at the singleton c−1 is the named weight-d edge. The old frontier has oriented placement label 3, so the actual connector to w has weight m−3=n+Q+1. The three attachments have weights [m−2,m]=[n+Q+2,m]. The terminal coordinate x_i=3+c+i exceeds every center label, and its actual weight x_i−j=d+π(i). This gives each member of d+J once. These are the exact disjoint old, connector, attachment and terminal weight resources, filling [1,m]. Likewise the old image and the fresh center labels [0,2], spine label m and gap labels {x_i:i in I} fill [0,m] exactly. Each actual vertex and incidence has its prescribed physical role. Appending w and its centers and leaves by their unique named parent edges preserves acyclicity and extends the witnessing spine. All previous incidences persist.

Use C=3+c+K=m/2+2 before reorientation. The old low group stays below C, including the singleton at 3+c+t−1, and the high band starts at 3+c+Q≥C. For each terminal, crossing is equivalent to source i≥K. The upper terminal weight set is [d+K,d+Q] with d+Q−t excluded, and the lower terminal weight set is [d,d+K−1]. The old exceptional crossing fills its missing weight and the other old crossings, connector and attachments fill the rest of [d+K,m]. The full noncrossing set is [1,d+K−1]. The new frontier w is at m in the placement. Under the D139 complement to the next zero-frontier orientation, its cut is c'=m+1−C=m/2−1 and threshold d'=d+K=m/2+1. Terminal K belongs to center 1 and has placement label C. Its new oriented label is m−C=c'−1, its named host label m−1, and its actual incidence weight is d'. This newly appended actual terminal has degree one.

For actual zero input use the placement directly and the actual cut C. For actual maximum input apply the same D139 simultaneous conjugation. The old actual cuts in increasing order are n+1−c and n+2−c, and the actual shifts are 1,1+Q−t,1+Q across those bands. Absolute weights are unchanged by the complement, the actual cut is m+1−C, and membership of all old vertices relative to the designated cut persists. Actual polarity flips in both cases. The named center-1 boundary leaf just identified is the same physical vertex under its returned orientation.

## Exact coverage comparisons

At z=1 and b≥2, the lower capacity is at least one, so ell=1 and u_count=0. The only chosen transposition is t with t+1 and the other coordinates outside the two forced chains are fixed. This is D139's map pointwise. Its leaf index here is L−2=b+1, in agreement with D139. At z=b=1, K=Q−t is missing from J, so the stronger return cannot be supplied by any map in the declared class. D139's ordinary final step on those quotas remains valid in its own scope.

At b=1 and z≥2 the admitted sum condition holds, including empty upper flexibility at z=2. For z≥3 the quotas (2t+z,2,z) are pairwise distinct. D138's p=p'=1 roles use offsets +1,0,−1 and require equality of the quotas at opposite offsets. Such triples therefore escape every D138 numerical role. At z=2, the two equal quotas leave that reasoning inapplicable.

At t=0 the two holes merely delete the extra endpoints −1 and Q, and I=J=[0,Q−1]. The first gap vanishes and the old embedding is the retained one-cut placement. The present classification concerns the genuine two-gap case t>0 and Q−t>0. Failure of its criterion excludes the declared allocation and placement with the stronger return, while the wider ordinary labeling problem remains open.

## Independent supply, composition and operation bound

The input is exactly the output of [D139's independent symbolic preparation](ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE.md#independent-symbolic-initialization-and-finite-lists). Its D134 initializer at p=1 supplies an arbitrarily large ordinary state with the required named input data except for the boundary leaf. Its actual D137 preparatory section with physical quotas (1,6,1), split 6 and symbolic 0↔1 exchange creates the degree-one center-1 terminal at actual zero-based index 4. That terminal has oriented label c−1, host label n−1 and unique weight d at the prepared boundary. No part of this supplier changes. All initializing sections belong to the declared original target. An admitted sufficiently large initializer can meet the size requirements for a predeclared finite continuation by starting at least at the maximum of 12 and all continuation H values. No numerical initializer or bridge is needed here.

Induct on any finite admitted list. Choose t,b,z independently at each step with the exact quota relation and exact size requirement. The stronger state returns at every step via the newly appended degree-one terminal at index L−2ell proved above. This includes every admitted b=1 branch with z≥2 and every admitted empty list. At each completed section the actual next connector is the sole incidence to a later unplaced section, and the named terminals retain their unique incident edges.

All hypotheses of [D139's immutable final-alphabet composition](ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE.md#immutable-final-alphabet-accounting) persist. To verify the correction directly, at boundary i write C_i for the actual designated cut, A_i for the sum of subsequent actual lower shifts, S_i for the sum of their Q values, and τ_i for the next step's t or zero without a next step. An actual lower shift is 3 for zero-frontier input and 1 for maximum-frontier input, and the default high shift adds that step's Q. Actual memberships persist. The distinguished leaf at boundary i has actual label C_i−1 in the zero case or C_i in the maximum case. Its first subsequent shift alone differs from the default by +τ_i or −τ_i respectively. After that shift every distinguished leaf is a new vertex, so there can be no further exception for that vertex or its edge. Hence the immutable final image of x is x+A_i+S_i I(x≥C_i), with exactly that one signed correction at the distinguished label if a next step exists. The two default label intervals [A_i,A_i+C_i−1] and [A_i+C_i+S_i,A_i+n_i+S_i] replace the one default leaf image by its corrected image inside their gap. The unused labels are their exact corrected complement in [0,n_final]. This image law is the composition of the actual increasing maps. Mapping a fresh vertex when first placed and leaving previous labels fixed is therefore pointwise consistent.

The precise used final weights at boundary i are [1,d_i−1], the singleton {d_i+S_i−τ_i}, and [d_i+1+S_i,n_i+S_i]. Every noncrossing weight is unchanged, every other crossing gains S_i, and the single existing exceptional incidence gains S_i−τ_i. The unused weights are [d_i,d_i+S_i] minus that singleton, together with [n_i+S_i+1,n_final]. Later fresh edges obtain the same exact rule on their first boundary. The final label and difference inventories are exhausted at the last boundary because the composite is identity there. Old and newly consumed resources are disjoint by the actual image and difference formulas. These arguments include the next actual connector and the uniquely indexed new boundary leaf at each step.

There are exactly Q emitted terminal coordinates, three emitted centers and one emitted spine vertex per bridge. The chain bounds, capacities and chosen counts take a constant number of indexed exact integer operations per step. At each source a bounded number of endpoint, parity and index operations recognizes its chain, transposition partner or fixed point, computes the physical host and updates one terminal index. Every source is visited once, excluding the hole. Thus one step takes Θ(Q+4) indexed arithmetic/output operations for fresh vertices. A forward boundary plan and backward suffix sums take O(number of sections) additional indexed operations, and a single scan emits the supplied start and all fresh named vertices and edges in O(n_final+1) indexed operations, including the retained symbolic path and preparatory supply if used. Each finite scan and the finite list terminate. These are indexed exact-integer operation counts, with no bit-complexity claim for the integer arithmetic. No numerical instance, role transport, allocation enumeration or historical replay is needed. D131–D139 and their precise scopes are retained.
