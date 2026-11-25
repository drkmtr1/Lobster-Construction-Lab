# D138 — Canonical placement rigidity and role-independent moment obstruction

## Exact scope and inherited structure

Use the exact [D137](ORDINARY_SPINE_MIXED_MULTIPLICITY_CUT_STATE_BRIDGE.md) single-section class. The named ordinary graceful prefix has even edge count n, an extreme physical frontier v and a cut with crossing spectrum [d,n] in its zero-frontier orientation. Its state parameter is an exact integer p≥1, with c=n/2−p and d=n/2+1. The output D134 state has exact p'≥1 and the corresponding extreme frontier and crossing spectrum [m/2+1,m]. The section consists of w, its h≥3 named centers with independently prescribed positive exact integer quotas r_i, and the actual indexed leaves. Write Q=sum_i r_i, H=h+Q+1=2K, m=n+H and assume n≥h+Q. The parity of n and H gives n≥H. Integers are exact throughout. In particular booleans are excluded.

An admissible old placement translates the labels below c by A≥0 and the labels at or above c by A+s with s≥0, and preserves the sides at the designated output cut. Put B=H−A−s≥0. In zero-frontier input coordinates the inherited frontier has label A. D137's complement conjugation for an actual maximum-frontier input swaps the exterior widths and preserves the two-translation class and both cut memberships. We work in the oriented coordinates of D137. Every old noncrossing edge retains its weight and every old crossing edge gains s, so the fresh labels and weights are, respectively,
```
[0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [m−B+1,m],
[d,d+s−1] ⊔ [n+s+1,m].
```
All intervals are exact integer intervals, empty when reversed. Since the old minimum crossing weight d+s still crosses after placement, d+s≥m/2+1=d+K. Hence s≥K and A+B≤K≤n/2. The connector cannot join A to a new frontier of label zero, since that would give weight A<d, including weight zero if A=0. Thus w=m, B≥1, and the connector weight is m−A=n+s+B in the upper residual band.

The required cut before output reorientation is C=m/2+p'+1=A+c+k with 0≤k≤s because both old sides keep their membership. The fresh upper-side label count is U=(m−C+1)−(n−c+1)=K−p−p'−1, of which B are upper exterior and s−k are in the gap. In particular B≤U≤c−p'−1. We use the accepted D137 equation h=p+p'+1, so U=K−h.

Here is the actual incidence argument behind the D137 placements used below. A gap-to-lower-exterior difference is at most A+c+s−1≤n+s−p−1. A gap-to-upper-exterior difference is at most m−(A+c)=n+s+B−c≤n+s−p'−1. A gap-to-gap difference is at most s−1. These bounds preclude an internal fresh incidence touching the gap from supplying an upper residual difference. Bounds involving an empty interval are vacuous. After the connector uses one upper residual weight, the other A+B−1 must come from distinct internal incidences on A+B exterior vertices. The induced exterior subgraph of the actual section tree is a forest. It has at least A+B−1 edges, so it is connected, including if the only vertex is w.

An upper-exterior center is impossible because its actual attachment to w would have weight at most B−1<d. Any exterior terminal must have its actual host in the exterior forest to have a path to w, since its only neighbor is its center. Thus an exterior terminal can only have a lower-exterior host. A lower-exterior terminal would then have weight at most A−1<d, which is also impossible. Every lower-exterior vertex is therefore a center, and every upper-exterior vertex other than w is a terminal hosted by a lower-exterior center. A gap center has all its terminals in the gap. If the center were in the upper gap, all these terminals would also have to be in the upper gap. Indeed, gap-to-gap weights are at most s−1≤H−1<m/2+1, so they cannot cross the required cut. The upper gap length is s−k=U−B<d, so no edge among its labels can give a fresh weight. Each center has a positive quota. Therefore every gap center and its terminals lie in the lower gap. These restrictions are on actual named incidences.

## Rigidity of the upper exterior

Suppose B>1. Label m−1 is then at an actual upper-exterior terminal, since w carries m. Exterior connectivity requires a lower-exterior host. If A=0 this already gives a contradiction. Otherwise the host has label j in [0,A−1]. Its actual terminal-edge weight is m−1−j, in [m−A,m−1].

The connector vw has weight m−A. The A distinct attachments from w to lower-exterior centers have weights [m−A+1,m]. If j=A−1, the terminal edge repeats the connector weight. If j≤A−2, center j+1 exists in the lower exterior and its attachment has weight m−(j+1)=m−1−j. In both cases the repeated weight is on two distinct actual named incidences. This proves B=1.

## Rigidity of the lower gap

Let t=h−A≥0 be the number of gap centers. From B=1 and U=1+s−k=K−h derive
```
s=H−A−1=Q+t=2K−A−1,
k=1+s−K+h=K+t.
```
Since U≥1, K≥h+1. The same relation 2K=h+Q+1 gives Q≥h+1 and K≤Q. Write e=n/2−K≥0, so d=K+e+1.

Suppose t>0 and take a gap center with label A+c+u, where 0≤u<k. Its attachment to w crosses the designated cut, and its weight cannot be in the upper residual band by the gap endpoint bound. Thus its actual weight belongs to [d+K,d+s−1]. Direct subtraction gives
```
m−(A+c+u)=d+s+p−u,
p+1 ≤ u ≤ K+p−A−1.
```
The second line takes both ends of the permitted weight band. In particular if that band is empty there can be no such center.

The center has a terminal at some lower-gap coordinate i in [0,k−1]. The terminal edge must have |i−u|≥d. If i≤u this requires u≥d=K+e+1. If i≥u it requires u≤k−1−d=t−e−2. Combining these with the attachment bounds gives an eligible set contained in
```
[p+1,t−e−2] ∪ [K+e+1,K+p−A−1].
```
The two intervals are disjoint because t≤h<K and e≥0. Their exact combined size, counting reversed intervals as empty, is
```
J=max(0,p'−A−e−1)+max(0,p−A−e−1).
```
Indeed the first interval size before taking the positive part is t−e−p−2=p'−A−e−1, and the second gives p−A−e−1. Additional requirements on u could only reduce eligibility.

If both terms are positive, J=p+p'−2A−2e−2 and t−J=A+2e+3>0. If only the first is positive, t−J=p+e+2>0. If only the second is positive, t−J=p'+e+2>0. If neither is positive, J=0<t. At e=0 these margins are A+3, p+2, p'+2 and t, all strictly positive. Thus t distinct physical centers cannot receive distinct eligible gap labels. It follows that t=0, A=h, s=Q and k=K, in addition to B=1 and w=m. The h center labels exhaust [0,h−1] and every terminal uses a label in the gap.

## Independent total-weight identity after B=1

Derive this identity with B=1 and without excluding t>0. Write z_i for the oriented label of physical center i and G for the index set of the t gap centers. Let V sum z_i−x over actual terminal incidences with terminal label x<z_i. For any actual terminal edge, |x−z_i| contributes x−z_i plus 2(z_i−x) exactly in this reversed case.

The connector and lower-exterior attachments exhaust [m−A,m]=[n+s+1,m]. All other fresh edges are the Q actual terminal edges and the t gap attachments, which exhaust [d,d+s−1]. Every terminal label occurs in the gap, and exactly the gap center labels must be removed from its label sum. The total terminal weight is therefore
```
s(A+c) + s(s−1)/2 − sum_(i in G) z_i − sum_i r_i z_i + 2V.
```
The gap attachments add tm−sum_(i in G) z_i because w=m. Equating their combined weight to s d+s(s−1)/2 and using c−d=−p−1 gives
```
sum_i r_i z_i + 2 sum_(i in G) z_i − 2V = s(A−p−1)+tm.
```
Under the rigidity conclusion G is empty, s=Q, A=h and every terminal label exceeds its host label, so V=0. This recovers sum_i r_i z_i=p'Q by h=p+p'+1.

## Exact role and permutation criterion

Let σ be a bijection from the physical center indices to [0,h−1]. The numerical role σ(i) is the label of the actual center i. Every physical quota r_i and every actual incidence is unchanged. In the forced placement, ordered gap coordinate a in [0,Q−1] has label x_a=h+c+a. If its physical host is i, its difference is
```
x_a−σ(i)=d+a+p'−σ(i).
```
Thus the normalized terminal difference map π(a)=a+p'−σ(i) must be a permutation of [0,Q−1], since terminals exhaust [d,d+Q−1]. The actual crossing terminal incidences are exactly those with source a≥K. Old crossing edges, connector and attachments exhaust [d+Q,m]. Therefore the return threshold d+K holds exactly when π maps the upper interval [K,Q−1] onto itself, and by bijectivity this is equivalent to preserving both bands separately.

Conversely, suppose such σ and such a two-band permutation exist with displacement p'−σ(i) occurring exactly r_i times for every actual i. Each displacement identifies exactly one physical host. Scan a in increasing order and assign at that actual center the next indexed terminal label x_a. This fills all named vacancies with their exact quota. Apply the forced old embedding and label w=m and center i by σ(i). D137's old, connector and attachment weights remain exact because their labels have those same palettes. The stated π supplies each actual terminal weight once, with the crossing band it requires. The label partition and both weight inventories, same old side memberships, actual connector, polarity flip and returned p' state then follow by the D137 identities. For maximum-frontier input apply the simultaneous complement conjugation. The witnessing spine extends by w and all new vertices attach at their declared physical parents. This gives equivalence within the full declared placement class.

Summing π(a)−a shows that some bijection σ must satisfy sum_i (p'−σ(i))r_i=0. This is a role-independent necessary condition in the sense that allowing any role assignment can help only if some such assignment attains zero. Zero moment alone does not settle the two-band permutation problem. D137's constructive packing and uniform capacity tests remain sufficient for the role-ordered vector b_j=r_(σ^(-1)(j)).

For a symbolic positive corollary, independently supply an admitted D137 role-ordered vector b_j by its positive packet counts and its middle quota chosen sufficiently large that b_(p')>b_(p'−1). Choose the supplied state size for this declared vector. In the new physical quota specification exchange just these two numerical quota values. The fixed physical-index moment changes from zero to b_(p')−b_(p'−1)>0 because the two fixed offsets are zero and one. Assign the two numerical roles oppositely, with all other roles unchanged. Each role sees exactly its original quota and therefore inherits the same permutation, displacement counts, spectra and capacity. This is a symbolic assignment of labels and terminal resources under the declared physical names and slots. There is no graph reorder and no new allocation rule.

## Infinite obstruction against every role assignment

Fix any p,p'≥1 and h=p+p'+1. Let M=max(p,p') and let S be the sum of the offsets −p,...,p'. The arithmetic progression gives S=h(p'−p)/2, an integer. Start with the same positive exact integer quota b at every center. At two distinct physical centers put extra quotas X and Y, positive exact integers with
```
Y>b|S|,       X>MY+b|S|.
```
For any bijection σ the two increments carry distinct offsets α,β in [−p,p']. Its moment is bS+Xα+Yβ. If α≠0, then |Xα|≥X>MY+b|S|≥|Yβ+bS|, which excludes cancellation. If α=0 then β≠0, so |Yβ|≥Y>b|S|. This excludes cancellation in the other case. No role assignment can attain zero and by the rigidity theorem no declared embedding can succeed for these quotas.

Fix any admissible Y beyond its lower bound. There are infinitely many X beyond its bound in the parity class making H=h+hb+X+Y+1 even. Quotas stay positive and one can also require Q≥h+1 by increasing X. For each declared target choose a D134 independently supplied incoming state at p with n≥h+Q, using the unbounded allowed parameter of its initializer and the actual empty sections it requires from the outset. This neither pads a target fixed in advance nor claims one finite prefix admits unlimited sizes. Both parities of the compatible section multiplicity are covered as in D137. No numerical instance or permutation search is needed.

D138 exhausts alternate exterior and gap placements within this exact single-section class. It retains D131–D137 as scoped positive mechanisms and does not impose its obstruction on other state contracts, embeddings or ordinary gracefulness.
