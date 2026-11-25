# D139 — Two-cut boundary-leaf bridge

## General two-cut resource identities

Supply an ordinary graceful named prefix with n edges and labels [0,n]. For exact integers 1≤a<b≤n choose nonnegative exact A,s1,s2,B with A+s1+s2+B=H and m=n+H. Embed by E(x)=x+A+s1 I(x≥a)+s2 I(x≥b). The image of each input band [0,a−1], [a,b−1], [b,n] is a translated interval in [0,m]. These image bands are disjoint and ordered. Their exact label complement is
```
[0,A−1] ⊔ [A+a,A+a+s1−1] ⊔ [A+b+s1,A+b+s1+s2−1] ⊔ [m−B+1,m].
```
A reversed interval is empty. All integers in this proof are exact and booleans are excluded.

For an actual old edge, call its smaller and larger labels x<y. The difference E(y)−E(x) equals y−x plus s1 when x<a≤y and plus s2 when x<b≤y, independently. Thus the four original crossing-bit sets W00, W10, W01, W11 transform to W00, W10+s1, W01+s2, W11+s1+s2. Original graceful weights are distinct, so each translated class is internally injective. Their pairwise disjointness is necessary and sufficient for old-weight injectivity. Every transformed difference lies in [1,m] because the two image labels lie in [0,m] and are distinct. The fresh difference inventory in the injective case is exactly the complement of these four sets in [1,m]. The original edge identity and crossing bits are required for this test.

Let c be the designated incoming cut and one of a,b, and let C be the designated output cut in placement coordinates, before any final complement. A cut prescribed after complement at c' corresponds to C=m+1−c'. A prescribed actual high-frontier input is likewise read in the designated orientation. Write I_c(v) for the original at-or-above predicate at each old vertex v and I_C(v) for its image predicate. For compatibility of the old incidences require
```
I_C(v)=I_c(v) for every old vertex v,
w' ≥ d_out for every old edge crossing c,
w' < d_out for every other old edge,
```
where w' is the transformed absolute weight. Equivalently, under membership preservation, the old shifted crossing and noncrossing sets are exactly the intersections of the old occupied spectrum with [d_out,m] and [1,d_out−1]. Given old-weight injectivity, these conditions are necessary and sufficient for the old vertices and incidences to meet the cut and spectral requirements on their occupied resources. Fresh incidences must still fill the remaining labels and the corresponding two residual weight subsets. Because E increases, membership can also be checked by E(c−1)<C≤E(c). Complementing coordinates exchanges sides with the indicated integer cut and preserves absolute differences.

If s1=0 the surviving shift joins W00 and W10 as the b-noncrossing class and joins W01 and W11 as the b-crossing class. If s2=0 the surviving shift uses W00 and W01 against W10 and W11 at a. These are precisely the [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) one-cut collision and inventory formulas for the surviving shift cut. The designated state cut remains a separate compatibility test when it differs from that shift cut. If both gaps vanish every old weight is unchanged. These tests establish resource calculus for an old prefix, without supplying a fresh section by themselves.

## Strengthened input and exact old inventory

Fix p=p'=1 and h=3. Supply an ordinary graceful named D134 prefix whose actual frontier v is at zero in its oriented coordinates G, with even n, c=n/2−1, d=n/2+1, designated crossing spectrum [d,n], its witnessing spine and the full inventories. Require an actual terminal leaf u with G(u)=c−1 and unique incident edge of weight d. Its unique host z must have G(z)=(c−1)+d=n−1. The other numerical possibility (c−1)−d=−3 is outside [0,n]. The invariant makes this a real named leaf and host incidence, not a conclusion from the untagged spectrum.

Append a fresh actual spine vertex w adjacent to v, its three named physical centers j=0,1,2, and their indexed terminals of quotas (2t+1,2b,1) with independently chosen exact t,b≥1. Put Q=2t+2b+2, H=Q+4=2K, K=t+b+3 and m=n+H. Require n≥H. In particular n≥10, so 1≤c−1<c≤n and zero is below both cuts. In this specialization b denotes the quota parameter, with the two cuts explicitly c−1 and c.

Choose A=3, B=1, s1=t, s2=Q−t. The three translations are 3 below c−1, 3+t on the singleton c−1, and 3+Q from c onward. The singleton is exactly the vertex u. By its physical degree-one property the only old edge involving that singleton is the actual u–z crossing of weight d. It increases by Q−t. Every other older crossing at c spans both cuts and increases by Q. Every old noncrossing incidence has both endpoints in the same outer band, because it cannot touch u. These edges keep their weights. Hence the exact old spectrum is
```
[1,d−1] ⊔ {d+Q−t} ⊔ [d+Q+1,n+Q].
```
The singleton lies strictly above d−1 and strictly below d+Q+1. This proves injectivity and uses the unique named incidence; a higher-degree singleton would require tracking each of its edges and the claimed change of only one weight would lack justification.

## Fresh inventories and displacement map

The lower exterior [0,2] supplies the three physical center labels j. The upper exterior is {m}, used by w. The two gaps of the old image are [c+2,c+t+1] and [c+t+3,c+Q+2]. They give terminal labels x_i=3+c+i in increasing coordinate order for
```
I=[−1,Q−1] minus {t−1}.
```
The missing coordinate t−1 is the old u label. Both gaps are disjoint, inside [0,m], and each terminal label exceeds every center label. The inherited physical frontier v has placed label 3. Thus the actual connector vw has weight m−3=n+Q+1, and the three w–center attachments have the distinct weights [m−2,m]=[n+Q+2,m]. The remaining terminal weight band is d+J, where
```
J=[0,Q] minus {Q−t}.
```
It is the exact low complement of the old spectrum; the exceptional crossing weight occupies its deleted coordinate.

Define π on I as follows:
```
source                             image or rule
[−1,t−2]                           i+1 in [0,t−1]
{t,t+1}                            exchange t and t+1
[t+2,Q−t−1]                        identity
[Q−t,Q−1]                          i+1 in [Q−t+1,Q].
```
This is the proposed map, with the identity row making the otherwise case explicit. The source intervals are disjoint and cover I, since the first stops before the missing t−1, the upper shift begins at Q−t=t+2b+2≥t+4 and the two middle rows are adjacent. The images are disjoint and cover J in the listed interval order, with the last beginning strictly above the missing Q−t. The first and last rows each have t coordinates, the exchange has two and the identity row has Q−2t−2=2b coordinates. The first lower interval is the singleton {−1} at t=1. At b=1 the identity interval is [t+2,t+3], and the last row begins at t+4. These endpoint statements use only parameter identities.

The positive displacement +1 occurs on the first and last rows and at t, for 2t+1 total. Zero occurs on the identity row, for 2b total, and −1 occurs at t+1, once. Assign terminal coordinate i to physical center j=1+i−π(i) in [0,2]. This produces exactly the given physical quotas. Scan I in increasing order and assign at each host its next prescribed terminal index. Its actual edge weight is x_i−j=3+c+i−j=d+π(i). Hence every remaining terminal weight is consumed exactly once. The named attachment, connector and terminal edges, together with the retained old incidences, give the full bijections onto [0,m] and [1,m]. Attaching w, the centers and terminals by their specified parents preserves the tree, and the ordered old spine extended by w witnesses all vertices at distance at most two. No renamed center, terminal or incidence is used.

## Escape from every D138 numerical role assignment

At p=p'=1 a D138 role assignment uses the three offsets +1,0,−1 once each among the physical hosts. Its moment can vanish only if the two quotas given opposite offsets agree. The present quotas are pairwise distinct: 2t+1 is odd and at least three, 2b is positive even and 1 is smaller than either. Thus all numerical roles in the exact [D138](ORDINARY_SPINE_CANONICAL_PLACEMENT_RIGIDITY.md) class are excluded on these inputs, which also satisfy that class's size and parity hypotheses. The present bridge instead obeys
```
sum_(i in I) (π(i)−i)
= sum(J)−sum(I)
= [Q(Q+1)/2−(Q−t)] − [−1+Q(Q−1)/2−(t−1)]
= 2t.
```
Here π is a bijection between unequal coordinate sets, and the nonzero moment agrees with the computed displacement counts. The increments t and Q−t are strictly positive. Each of the three old bands contains an old label, including the singleton c−1. Thus E(x)−x takes three distinct values on the supplied old alphabet. No single-cut two-translation embedding agrees on it with this placement, including after conjugation. The D138 theorem applies within its own class.

## Output cut and exact returned leaf domain

Take C=3+c+K=m/2+2. Every old low vertex, including u at 3+c+t−1 with t−1<K, stays below C. Every old high vertex has label at least 3+c+Q≥C. Thus exact designated-cut membership persists. The new centers and the inherited frontier are below C, w is above it, and terminal i crosses exactly if i≥K.

The exchange is below K because t+1<K. The high-shift row starts at Q−t=K+b−1≥K. The initial row and all its images are below K, and the identity row may split into its fixed lower and upper parts. Hence the lower source band maps bijectively to [0,K−1] and the upper source band maps to [K,Q] minus {Q−t}. Here t−1<K and K≤Q−t<Q make the deletion positions explicit. In particular the exceptional old crossing d+Q−t is on the required upper side, with equality at b=1. The exact crossing spectrum is the disjoint union
```
([d+K,d+Q] minus {d+Q−t})
⊔ {d+Q−t}
⊔ [d+Q+1,n+Q]
⊔ [n+Q+1,m]
= [d+K,m] = [m/2+1,m].
```
The groups come from crossing terminals, u–z, other old crossings and connector/attachments. The noncrossings use [1,d+K−1] by the lower terminal band and the old noncrossings. This satisfies the general old-incidence compatibility test and fills the remaining resources.

In the next zero-frontier coordinates complement the placement labels about m. The new cut and minimum crossing weight are c'=m+1−C=m/2−1 and d'=d+K=m/2+1. They are valid cuts and give the ordinary D134 p'=1 state. With b≥2, K is in the fixed row [t+2,Q−t−1] and π(K)=K. The actual new terminal of coordinate K lies at label C before complement. It is a named degree-one terminal of center 1. Its zero-based terminal index at center 1 is K−(t+2)=b+1, since the fixed row begins at t+2. After orienting, its label is m−C=c'−1, its named host has label m−1 and its unique edge has weight d'. These are the exact stronger input data for the next step. With b=1, K=Q−t starts the high shift and π(K)=K+1. The unique vertex at label C is now a terminal of center zero, and it has oriented label c'−1 but host label m and weight d'+1. No other vertex can provide the leaf at c'−1 because the vertex labels are distinct. This construction therefore returns the ordinary cut state but fails to return the strengthened leaf condition at b=1.

For an actual zero-frontier input use the displayed E and fresh labels directly. The actual polarity becomes maximum. For an actual maximum-frontier input use G=n−g and complement every displayed output about m. The actual cuts are n+1−c and n+2−c for the old input, in increasing order, and the resulting shifts of the old actual labels are 1, 1+Q−t and 1+Q on the three respective bands. Indeed, the low actual group has G≥c, the singleton has G=c−1 and the high remainder has G<c−1. This is still an order-preserving three-translation map with positive gaps Q−t and t. The designated output cut is m+1−C and every old vertex preserves membership relative to its actual designated cut. The actual polarity becomes zero, and in the next zero-frontier orientation the labels and incidence conclusions for the returned leaf are exactly those just proved. Absolute weights and the actual named incidences are invariant under the complements.

## Independent symbolic initialization and finite lists

Use a supplied maximum-frontier seed and the [D134 independent symbolic initializer](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md#independent-symbolic-initialization-for-every-fixed-odd-h) at p=1. This gives the ordinary normalized D134 state, with independently adjustable size. In that initializer the allowed parameter c_0 can be arbitrarily large and the first returned size is 4c_0+6, as follows from its preliminary size 3c_0, first quota total c_0+2 and three centers. Its empty sections and all its other prescribed parts must be actual declared sections of the target.

Follow this input by the actual preparatory section with three physical quotas (1,6,1). With Q=8, H=12 and split K=6, use [D137's canonical placement](ORDINARY_SPINE_MIXED_MULTIPLICITY_CUT_STATE_BRIDGE.md#canonical-bridge-and-the-asymmetric-quota-moment) at p=p'=1. Symbolically prescribe the displacement map exchanging 0 and 1 on [0,7], fixing all other coordinates. Its only nonzero displacements are +1 and −1, one each, so it gives exact physical quotas (1,6,1) and preserves [0,5] and [6,7]. Under the canonical D137 identities the center-1 terminal with source coordinate 6 has placement label 3+c+6 equal to the output cut, and weight d+6 equal to the new crossing threshold. Upon orienting with the new frontier zero it has label c'−1 and its actual host center 1 has label m−1. It is the actual zero-based terminal index 4 at center 1, whose six fixed coordinates run from 2 through 7. This is the required named leaf with its unique edge. The argument holds for an arbitrary supplied state with the stated conditions and n≥12, without constructing any numerical original or initialization.

For any finite declared bridge list, choose the D134 starting size at least the maximum of 12 and all declared increments H_i. Every size then stays sufficient since each actual section increases it. All preparatory pieces are chosen in the declared original before supply. From a strengthened state, induction admits every declared list whose nonfinal steps have t≥1,b≥2, whose optional last step can have b=1 and whose size requirements hold at each boundary. The empty list is allowed. The final b=1 step leaves an ordinary D134 state, with no stronger return claimed from that step. This closes the strengthened state at every admitted intermediate step. The per-step old embedding and the finite symbolic terminal scan terminate, so finite construction terminates.

## Immutable final-alphabet accounting

The following composition applies to the declared bridge list after the preparatory supply, or from any strengthened input. At boundary i denote the actual cut by C_i, spectrum threshold by d_i, size by n_i and, when a later bridge remains, the named distinguished leaf by u_i. Let L_i be the sum of the actual lower shifts of all subsequent embeddings and S_i the sum of their gaps Q_j. Define τ_i as t for the very next step and zero at the final boundary. Each actual old embedding has default shifts equal to its lower shift and that lower shift plus Q on the high side. It also moves its distinguished vertex alone by +t relative to that default when the actual frontier is zero and by −t when the actual frontier is maximum. Those distinguished labels are respectively C_i−1 on the low side and C_i on the high side. Any later returned distinguished leaf is newly appended, so a vertex already present at boundary i can be exceptional only at the first next step.

All actual memberships at the designated cut persist. The composite to the final alphabet on an actual boundary label x is therefore
```
Phi_i(x) = x + L_i + S_i I(x>=C_i)
           + delta_i I(x is the actual label of u_i),
```
where delta_i is the signed correction just described for the first next step, or zero without a next step. With no distinguished leaf needed at the final boundary the correction term is absent. This composite is the actual map of the successive increasing embeddings, and composing the first next embedding with the next-boundary composite agrees pointwise. An old vertex already emitted thus keeps the same final label. To emit a fresh vertex once, use its actual output label mapped by the composite from its first boundary.

Precisely, the used final labels are the intervals [L_i,L_i+C_i−1] and [L_i+C_i+S_i,L_i+n_i+S_i], with the default image of u_i replaced by its corrected image if a next bridge remains. The correction places that label in the central gap because 0<τ_i<Q_next≤S_i, with either signed correction and endpoint as above. The unused labels are the exact complement in [0,n_final]. To obtain them explicitly, take the three exterior/gap intervals complementary to the default bases and remove the corrected label and insert the default image. End intervals are interpreted as empty as needed.

Every existing noncrossing edge remains unchanged. The exceptional old leaf edge is a designated crossing and gains Q−t on the first next step, while every other current crossing gains Q. No present edge becomes the distinguished edge at a later step because its distinguished leaf would be new. Consequently the final used weight inventory, including the final boundary by taking τ_i=S_i=0, is
```
[1,d_i−1] ⊔ {d_i+S_i−τ_i} ⊔ [d_i+1+S_i,n_i+S_i].
```
The unused weights are [d_i,d_i+S_i] minus the displayed singleton, together with [n_i+S_i+1,n_final]. This is generally different from the two-band inventory without the second cut. To account for newly consumed resources at a boundary, apply its same label composite to the local fresh label set. Keep every local fresh noncrossing weight and increase every local fresh crossing weight by S_i, except subtract τ_i from that increase on the fresh returned distinguished edge when a later step exists. The earlier edges satisfy exactly the same incidence-wise composite rule, since their physical endpoints and named memberships persist. The resulting old/new sets are disjoint and exhaustive for the used resources by injectivity of the composite and the formula for the distinct final weights on the entire used subgraph. The only incidence from a completed prefix to the as-yet unemitted part of the declared target is the next actual spine connector when a section remains. Each completed center has all its actual terminals. At completion the composite is identity and both unused inventories are empty.

One forward pass can plan cuts, sizes and polarities, and one backward pass can sum shifts and gaps. The exceptional edge and label are named at each boundary. Scanning the prefix once and each fresh terminal interval once gives linear indexed output operations in the size of the declared tree, counting exact integer arithmetic as indexed operations rather than bit cost. No numerical application is needed for the proof.

D139 supplies the stated family in this strengthened p=1 state and proves the general resource identities. It leaves arbitrary quota vectors, input states without this physical leaf and other two-cut transitions open. D131–D138 retain their precise scopes.
