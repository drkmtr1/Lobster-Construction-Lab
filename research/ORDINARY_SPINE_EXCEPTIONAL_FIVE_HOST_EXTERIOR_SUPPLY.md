# D160 — Five-host exceptional-phase exterior supply

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-FIVE-HOST-EXTERIOR-SUPPLY-001`. All parameters, labels and quotas are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty. Write ⊔ for disjoint union.

## 1. Theorem and physical parity

Supply an independently constructed ordinary graceful named prefix in the [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) state S₋₁. Its witnessing spine ends at an actual extreme v. In the orientation G(v)=0, let n=2c+2, d=c+2, and let the exact crossing and noncrossing weight sets at cut c be [d−1,n] and [1,d−2]. Equality with a cut is on its upper side.

Append the actual consecutive sections of the ordered profiles (q₁,q₂,q₃), (r₁,r₂,0), all five quotas positive. The actual spine vertices are u,w. The first section has u, three centers and T₁=q₁+q₂+q₃ terminals. The second has w, two centers, T₂=r₁+r₂ terminals and one actual direct leaf. There are 2K=T₁+T₂+8 new vertices and edges. Require n≥2K. Set e∈{0,1}, W=4+e, A=B=W, s=2K−2W, k=K−W and m=n+2K. Require s≥K.

Give the first-center numerical roles a,b,Z and the second-center roles Q,P to actual original centers. The input can specify the role assignment, or use the lexicographically first tuple of physical indices meeting a stated quota regime among the two constant-size sets of role bijections (three and two roles). This is a choice of compatible roles on the given original. All physical branch indices, their ordering in the original profiles, and all parent/terminal incidences remain fixed. In role order write the actual quotas as (α+e,β,ζ), (γ+e,η,0). Thus (α,β,ζ,γ,η) are the five physical gap quotas and sum to s. The role order is only used to state hypotheses, and the actual zero entry stays at its declared index.

**Sufficient theorem.** In each width, the named exterior and gap construction below independently return S₋₁ in either actual input polarity. Choose one row of the following table and its five independent nonnegative integer increments n_a,n_b,n_Z,n_Q,n_P.

| Opening column | α | β | ζ | γ | η |
|---|---:|---:|---:|---:|---:|
| (b,Q) | 4+2n_a | 2+2n_b | W+2n_Z | W+2n_Q | 2n_P, n_P≥1 |
| (Z,P) | 4+2n_a | 1+2n_b | W+1+2n_Z | W−1+2n_Q | 1+2n_P |

The first row is the proposed theorem. The second row follows from the same conversion and completion with a different single opening. Both are sufficient families. General current-width quota feasibility or all-exterior feasibility is outside the theorem.

The graph bipartition with v lower has u upper, w lower, all three actual first centers lower, both actual second centers upper, and the actual direct leaf upper. The actual second terminals are lower and first terminals upper. Thus the fresh graph-class counts are N_low=4+T₂ and N_high=4+T₁; these are graph classes, while the gap's physical sides refer to cut C=c+K after placement.

For a membership-preserving fixed-phase D157 connected crossing exterior, the old crossing band gains s and starts at d−1+s. The new target crossing band starts at d−1+K. The exterior uses the high residual band [n+s+1,m], which is entirely crossing. The gap therefore has exactly s−K crossing images. In general widths A,B within this declared arrangement, let L and U be lower- and upper-host gap quotas, x the lower-source uses of upper hosts and y the upper-source uses of lower hosts. There are K−A physically lower gap sources, so K−A=L−y+x, and x+y=s−K. With L+U=s and A+B+s=2K these give L=B+2y and U=A+2x. Connectedness puts the fresh lower/upper exterior classes in the corresponding graph classes, since v is lower and every exterior edge crosses. Each gap leaf is opposite its own host in the graph bipartition, so N_low=A+U=2(A+x) and N_high=B+L=2(B+y). Hence T₁ and T₂ must both be even. Both constructive quota regimes satisfy this necessary parity. The necessity is limited to the declared embedding and fixed-phase return.

## 2. Independent reduced exteriors

In both widths give the roles the reduced labels
```
v=W,  u=W+1,  w=0,  a=W−3,  b=W−2,  Z=W−1,
Q=2W−2,  P=2W−1,  actual direct leaf at w=2W.
```
The spine edges vu,uw have differences 1,W+1. The three actual u-center edges uZ,ub,ua have differences 2,3,4. The actual w-center edges wQ,wP and w-direct-leaf edge have differences 2W−2,2W−1,2W.

For W=4 these are exactly [1,8], and the listed labels use [0,8] bijectively. All original terminals are gap leaves. For W=5, the labels 1 and 7 and the weights 5 and 7 are missing. Give an actual terminal of a reduced label 7, producing 7−2=5, and an actual terminal of Q reduced label 1, producing 8−1=7. This is the [D147 paired exchange](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md#2-terminal-balance-and-paired-exchange): the reference weights 6−1=5 and 7−0=7 are supplied instead at a and Q, with the same two values and actual terminal incidences. The reference pairs are numerical only. Both terminals used are actual indexed vertices of the prescribed original. This covers [0,10] in labels and [1,10] in weights. In each width the resulting graph is connected through vu and uw. Every edge of it crosses the reduced cut between W and W+1. No gap leaf lies on an original path between exterior vertices. The exterior is supplied directly from its roles and terminal indices.

Expand each reduced label above W by n+s while leaving lower labels as given. The actual label W at v agrees with the old placement. On the actual return cut C=c+K these exterior edges all cross. In fact the lower labels are at most W, while even the old upper band begins at c+s+W≥C. They produce exactly n+s+[1,2W]=[n+s+1,m].

## 3. Gap coordinates, legal arrows and endpoints

Use the old placement E(x)=G(x)+W for G(x)<c and E(x)=G(x)+W+s otherwise. Since W≤K≤W+s, it preserves old membership at C. A gap leaf at coordinate i has actual label c+W+i. Its side is lower iff i<k. Its difference at a lower host of reduced label j is d−1+(i+W−1−j). At an upper host of reduced label W+b₀ the actual difference is d−1+(s+b₀+1−i), by subtraction from the expanded upper label. These identities apply to the leaf's original parent edge. In particular the gap images π(i) at a,b,Z,Q,P are respectively i+2, i+1, i, s+W−1−i, s+W−i. Require a permutation of [0,s−1] with π(i)≥K exactly on actual crossing incidences.

Let J=s+W−1=2k+W−1. Use Lⱼ=j and Hⱼ=J−j. For sources, L indices [0,k−1] give the lower coordinates [0,k−1], while H indices [W,k+W−1] give the upper coordinates [k,s−1] in reverse. For destinations, L indices [0,k+W−1] give [0,K−1], and H indices [W,k−1] give [K,s−1] in reverse. Each pair partitions its own alphabet. Substituting the actual images gives:

| Host | L source | H source |
|---|---|---|
| a | Lⱼ₊₂ | Hⱼ₋₂ |
| b | Lⱼ₊₁ | Hⱼ₋₁ |
| Z | Lⱼ | Hⱼ |
| Q | Hⱼ | Lⱼ |
| P | Hⱼ₋₁ | Lⱼ₊₁ |

A cell is usable exactly when it exists in the relevant source or destination row. The table preserves the original crossing test because lower-host arrows keep the row, upper-host arrows exchange rows, and the H destination row is precisely the crossing band.

Since s≥K gives k≥W, L₀ through L_(W−1) exist. Destination Lⱼ there can come only from Z at Lⱼ, a or b at an earlier L source, or a nonexistent H source of index j or j−1. At L₀ the translations underflow. Each earlier forced Z assignment fixes its own source, so induction forces these W sources at Z. At the other end Hⱼ with j≥k+2 cannot use a,b,Z because even j−2≥k, outside the H destination row. Starting with H_(k+W−1), P overflows the L range, and thereafter its Lⱼ₊₁ is already used by the higher-index Q assignment. Downward induction forces Q for H_(k+2) through H_(k+W−1). Thus ζ≥W and γ≥W−2 are necessary on these fixed exteriors, including when the common interval is empty. Their proof requires no common-column length beyond k≥W. The assignments Hₖ and Hₖ₊₁ at a will be a chosen completion of the positive words.

## 4. The conversion and the unified allocation word

Reserve the forced cells. In the common columns [W,k−1], first use n_Z columns (Z,Z) and n_Q columns (Q,Q). Each supplies exactly its local L and H images. Next use one opening (b,Q), followed by n_b columns (b,b) and n_P columns (P,P). The opening at column l supplies L_l locally from H_l at Q and sends L_l at b to L_(l+1). It requires the next H source to supply H_l. Each following unit column t sends one image to L_(t+1) and one to H_(t−1), filling the previous H obligation and creating only the next unit pair of obligations. Exactly the same two opening images are obtained using (Z,P), since L_l at Z gives local L_l and H_l at P gives L_(l+1). In either opening both edges are noncrossing.

Then use the two successive conversion columns (a,b), (a,Q), starting at j. On entry L_j is already supplied, H_(j−1) is outstanding, and no earlier column has sent a destination beyond L_j. The conversions give exactly
```
L_j     at a → L_(j+2)       H_j     at b → H_(j−1)
L_(j+1) at a → L_(j+3)       H_(j+1) at Q → L_(j+1).
```
Thus all H destinations below j are filled, H_j and H_(j+1) are the next H obligations, and all L destinations below j+4 are filled. The remaining n_a common columns, indexed [j+2,k−1], use (a,a). Their L images are exactly L_[j+4,k+1], following the three L images of the conversion. Their H images are H_[j,k−3]. Finally Hₖ and Hₖ₊₁ use a and give H_(k−2),H_(k−1). Equivalently all H sources in [j+2,k+1] use a and supply H_[j,k−1], including when no common a column exists. This proves the partition across the conversion and at its right boundary. The conversion's furthest L image is j+3≤k+1, and the first H image H_(j−1) is legal because the opening precedes j. All H images from the remaining a sources are in the common destination range. The forced Q suffix fills exactly L_[k+2,k+W−1]. Combined with the left reservations and all preceding local images, the L and H destinations are each covered once.

In the first opening regime the reserved and special columns give a=4, b=2, Z=W, Q=W and P=0 before the pair increments. In the second regime the opening alone changes their counts by (0,−1,+1,−1,+1) in order (a,b,Z,Q,P). Each pair contributes two uses at its own host, giving the theorem's quotas exactly. The common column count in both regimes is
```
n_Z+n_Q+1+n_b+n_P+2+n_a = (s−2W)/2 = k−W.
```
All loop lengths are nonnegative with the declared minima. The first regime needs at least four common columns because P has positive even quota. The second needs at least three, since its positive P quota can come entirely from the opening. Hence the opening and both conversion columns always fit. The reservation arguments also cover k=W or shorter-than-required common intervals elsewhere in the size domain, without asserting a positive word there.

Actual lower-source crossings come from the L member of each Q or P pair, so x=n_Q+n_P. Actual upper-source crossings come from the H members of Z,b,a pairs, the first conversion's H source at b, and the two H completions at a. Thus y=n_Z+n_b+n_a+3. All other used arrows take the row appropriate to a noncrossing incidence. In both regimes,
```
x=(γ+η−W)/2,    y=(α+β+ζ−W)/2,    x+y=(s−2W)/2=s−K.
```
These counts also agree with the separate physical source and graph-class identities in Section 1.

## 5. Symbolic controls and a terminal-free obstruction

At the first regime's minimum only one P pair is present. The common L/H pairs in order are (b,Q), (P,P), (a,b), (a,Q); the other four loop counts vanish. For l=W these give L images L_l through L_(l+5) and H images H_l,H_(l+1) directly from the four columns. The final H sources at a give H_(l+2),H_(l+3), since k=l+4. The remaining L destinations follow from the same forced left and right reservations. The actual minima are (4,2,4),(4,2) for e=0 and (5,2,5),(6,2) for e=1, in numerical role order with the original direct leaf understood. At the second opening regime's minimum all five loop lengths vanish, so its (Z,P), (a,b), (a,Q) word and two a completions are exactly the zero-unit-loop, zero-double-loop case of the image interval proof. These are symbolic endpoint checks, with no generated original or numerical allocation evaluation.

Consider any terminal-free exterior in the same connected crossing, fixed-phase arrangement, using the membership-preserving band placement and retaining all centers exterior. The lower exterior contains exactly the three first centers and w besides v, so A=4, independently of their assigned labels. If the actual sole direct leaf at w is in the gap, the upper exterior contains just u and the two second centers, so B=3. The difference-one pin gives u=A+1: the unique reduced crossing pair of weight one is A,A+1, and v=A has only vu in the reduced exterior. At the first upper source i=k=K−A there is an upper gap coordinate since K≥A+B and s−k=K−B>0. A lower host would require a crossing but its image is K−1−j≤K−1. At upper index b₀ the noncrossing condition is K−B+b₀+1≤K−1, or b₀≤B−2=1. Only u is eligible numerically and u has no direct gap leaf. [D158 first-upper-source obstruction](ORDINARY_SPINE_EXCEPTIONAL_PHASE_PRESERVING_BRIDGE.md#2-first-physically-upper-source)

If the direct leaf is exterior then A=B=4. The actual lower gap hosts are the first centers with reduced labels 1,2,3 in some order. They have displacement +2,+1,0 respectively. Eligible upper hosts have b₀≥2 because u still has no gap leaves and holds index 1. Every upper-host image is at least b₀+2≥4. Hence destinations 0,1,2,3 must be supplied with the three lower translations. Induction forces source i at the label-three host for each i in [0,3], since positive translations would need an earlier already consumed source. No original role permutation avoids the quota demand of four at that host. All first quotas at most three therefore exclude every terminal-free exterior of this declared arrangement, including the parity-compatible profiles (2,2,2),(2,2,0). Conjugation preserves the argument in the other frontier polarity. The obstruction is strengthened below to cover terminal-enabled exteriors in the same arrangement.

### Width-independent first-center obstruction under the same arrangement

Here is a separate proof for every terminal-enabled exterior in the declared D157 arrangement on this topology. The widths and selection of actual exterior leaves can be arbitrary under those premises. The crossing exterior contains v, u, w and all centers. Thus A≥4 and B≥3, and s≥K≥A+B ensures that coordinates 0 through 3 exist. As above, the unique crossing difference-one pair and the literal edge vu force u=A+1. Since u has no actual direct leaf, every eligible upper gap host still has index b₀≥2. For every source i≤s−1 its upper-host image is at least b₀+2≥4. The gap images 0 through 3 must therefore come from lower hosts. Every such host has reduced label j≤A−1 and displacement A−1−j≥0. Image zero requires source zero and j=A−1. Inductively, any positive displacement supplying image t≤3 would require an already consumed source i<t. It follows that source t must use the unique host j=A−1 at each t. These incidences must also pass the physical crossing test. If the host does not exist or an arrow is illegal, the allocation already fails. Otherwise this host must supply four gap leaves. It cannot be w, which has reduced label zero, and any selected exterior terminal is itself a leaf and cannot host another gap leaf. It must be an actual first center, with at least four actual remaining terminals after exterior selections.

Consequently if all original first quotas are at most three, every admitted exterior in this arrangement fails, including terminal-enabled exteriors and either polarity. This proof depends only on the unchanged relaxed images, the pin and the listed original topology. It requires no classification of additional width choices. The stronger width-five bound ζ≥5 still applies to the particular D160 paired-terminal exterior, including any permitted role transport. The theorem makes no assertion of ordinary nongracefulness or impossibility under other placement classes.

## 6. Exact named resources and both polarities

Keep the supplied physical names for u,w, the centers and the direct leaf. For e=1 assign the reduced exterior terminals to the smallest original terminal index at a and Q. At each actual parent give the other original terminal indices their increasing assigned source coordinates in that parent's source set. Every terminal has a unique original name and its own physical incidence. This rule uses the exterior formulas, input quotas and the explicit words before either section is emitted. In particular it supplies the partial inventories without first obtaining or searching a complete labeling.

Write L_old=[W,c+W−1]⊔[c+s+W,n+s+W]. The fresh exterior labels comprise [0,W−1] and [n+s+W+1,m], and the gap occupies [c+W,c+s+W−1]. The five old, exterior and gap intervals partition [0,m], with each label used once. The old crossing edges gain s and the old noncrossing edges gain zero in absolute weight, so D_old=[1,d−2]⊔[d−1+s,n+s]. The gap permutation supplies [d−1,d+s−2], and the connected crossing exterior supplies [n+s+1,m]. Hence the actual differences are exactly [1,m]. At C the gap crossing band is [d−1+K,d+s−2], and its noncrossing band is [d−1,d+K−2]. Together with the exterior and old edges, the full crossing spectrum is [d+K−1,m] and the noncrossing spectrum [1,d+K−2]. The extreme w=0, cut c+K and m=2(c+K)+2 give exactly S₋₁.

For the first boundary, let S_a,S_b,S_Z be the independently assigned actual coordinate sets. Put I=S_a⊔S_b⊔S_Z and J₁=(S_a+2)⊔(S_b+1)⊔S_Z. Let I′,J₂ be their complements in [0,s−1]. All unions are disjoint by the source and image partition. Define E₁={W−3,W−2,W−1,n+s+W+1} and E₂={0,n+s+2W−2,n+s+2W−1,n+s+2W}, with additional n+s+W+2 in E₁ and 1 in E₂ exactly when e=1. The first exterior edges are vu and the three u-center edges, plus the actual exterior terminal edge at a when e=1. Their differences are n+s+[1,W]. The second section and connector have exterior differences n+s+[W+1,2W], using the edge at Q of reduced difference 7 when e=1. Thus:
```
used labels       L_old ⊔ E₁ ⊔ (c+W+I)
remaining labels  E₂ ⊔ (c+W+I′)
used weights      D_old ⊔ (n+s+[1,W]) ⊔ (d−1+J₁)
remaining weights (n+s+[W+1,2W]) ⊔ (d−1+J₂).
```
At the known cut C the actual lower labels in either gap portion correspond to source coordinates below k. The old bands and expanded exteriors have their stated sides. Used crossing differences are [d−1+s,n+s]⊔(n+s+[1,W])⊔(d−1+(J₁∩[K,s−1])). Used noncrossing differences are [1,d−2]⊔(d−1+(J₁∩[0,K−1])). Remaining crossing differences are (n+s+[W+1,2W])⊔(d−1+(J₂∩[K,s−1])), and the remaining noncrossing differences are d−1+(J₂∩[0,K−1]). The physical frontier at the first boundary is u at n+s+W+1. Its sole unfinished edge into this second section is uw, with w at zero and weight n+s+W+1, which belongs to the remaining exterior band. There is no substituted incidence.

For maximum input polarity, complement about n to orient and complement the resulting output about m. The actual pre- and post-placement cuts are n+1−c and m+1−C. An actual lower label x corresponds to G=n−x≥c; the new actual label is m−(W+s+n−x)=x+W since 2K=2W+s. An actual upper label becomes x+W+s. The cut inequalities conjugate exactly, so existing actual membership is preserved. Complement all partial labels about m, preserving every weight and crossing status. The physical w has label m, and u has label W−1. In minimum polarity the actual shifts are likewise W and W+s, with the displayed oriented labels. Both cases emit the same actual graph.

## 7. Immutable composition and termination

From an independently supplied S₋₁ start, any finite list of individually admitted D160 blocks composes by induction. Also admit D157 outbound and return transitions, D158 and D159 phase-preserving bridges, and supplied strict [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) blocks, each precisely at its matching phase and other written premises. For a start in S₀ one can use the independently supplied D134 initializer under its own named hypotheses and the D157 outbound to reach S₋₁. Use the declared actual consecutive sections of each block. In each step require its own n_before≥2K_i and placement/phase tests. In the notation of the current interface n rises by 2K_i and the oriented cut by K_i. Each output must provide the next input with the same physical spine port, exact phase, cut and label/weight inventories. All actual memberships are preserved in their successive actual cuts. There is no implied decomposition of an arbitrary original.

At completed boundary i let C_i be the actual cut, Λ_i the sum of subsequent actual lower shifts, and Σ_i the sum of subsequent gap widths, using the parameters of each declared transition. Every label x already supplied at boundary i has final label Ψ_i(x)=x+Λ_i+Σ_i·1(x≥C_i). Indeed the cut-side indicator is invariant at each subsequent step. This transforms any used label set, and adds Σ_i to each used crossing weight while preserving noncrossing weights. At each D160 first boundary the same formula with the cut of the enclosing completed block applies to its partial label and weight sets, using the explicit crossing parts above. Its known unfinished connector crosses that cut, so its weight gains exactly Σ_i when its supplied endpoints are transformed, and u's actual label transforms by Ψ_i. The remaining inventories in the final alphabet are exact complements of the transformed used inventories. This supplies immutable final labels using the independently planned block sizes and shifts. The finite lists of bounded role choices, formula-defined assignments, ordered index traversals and suffix sums terminate. Neither construction nor composition adds or deletes any original vertex or edge.

The two-width supplier and the first-center obstruction leave broader quota classification and exterior supply outside the ruled-out domain open. [Strategic reassessment](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY_001/STRATEGY.md)
