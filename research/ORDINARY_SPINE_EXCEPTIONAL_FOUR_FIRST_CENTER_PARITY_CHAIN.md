# D165 — Four-first-center exceptional parity-chain classification

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-FOUR-FIRST-CENTER-PARITY-CHAIN-001`. All parameters are exact integers. Intervals are inclusive and reversed intervals are empty. An admitted block uses the declared D157 (S₋₁) membership-preserving old placement, a connected crossing exterior containing both new spine vertices and every positive center, and a gap of actual leaves attached to their own exterior parents. Use an independently supplied named prefix and actual witnessing spine, with (n=2c+2), (d=c+2) and extreme frontier (v). Orient its label to zero. At input cut (c) the crossing weights are ([d-1,n]) and the noncrossing weights are ([1,d-2]). Cut equality belongs to the upper side.

## 1. Statement and scope

The original has first terminal quotas (1,1,2,4) in any physical order, two positive second quotas and exactly one actual direct leaf at the second spine vertex (w). Let (p,q) be the full respective quotas of the second centers (P,Q) at reduced labels 10 and 8. Put (R=p+q) and assume (R) odd. The two actual sections add (2K=R+17) edges and vertices. Require (n ≥ 2K), write (m=n+2K), and require an exact (S₋₁) return.

The fixed exterior specified below admits a completion, with selectable first-center numerical roles, precisely as follows.

| Quota at (P) | Necessary and sufficient condition |
|---|---|
| Even (p ≥ 2) | (q ≥ 3) and (R ≥ 7) |
| Odd (p ≥ 3) | (q ≥ 4) |
| (p=1) | (q ≥ 8) |

If the two second numerical roles are also selectable, the criterion is (R ≥ 7) and ({p,q} ≠ {1,6}). The same criterion holds for the full terminal-enabled class E+ within the declared arrangement. Its positive side is symbolic. Its negative side uses a symbolic count and terminal-balance obstruction for (R<7), and an accepted finite exhaustive D164 negative with symbolic transport for the ({1,6}) corner. This determines E+ only on the selected topology. T feasibility, ordinary nongracefulness, and the full D164 finite separation hypothesis are outside this result.

## 2. Physical exterior and row coordinates

At the first section there are (1+4+8=13) fresh vertices. The second supplies (1+2+1+R=4+R). The two fresh edge counts equal the fresh vertex counts because each new vertex attaches once to a parent. From (v) in the lower graph color, the fresh lower color contains (w), the four first centers and (R) second terminals. The fresh upper color contains (u), the two second centers, the direct leaf and the eight first terminals. Thus (N_low=5+R) and (N_high=12).

Choose actual first-center roles (b,a,c₁,Z) at labels (2,3,4,5), with the four-leaf center at (Z). Here (c₁) names an actual center, and (c) denotes the cut. Use (v=6,u=7,w=0,Q=8,P=10). Choose one actual terminal at (a) for 9 and one at (P) for 1. Each physical quota at these two parents is positive. The actual direct leaf remains in the gap. The row of fresh first exterior incidences (vu, uZ, uc₁, ua, ub, a9) has respective differences (1,2,3,4,5,6). The remaining incidences (uw,wQ,P1,wP) have respective differences (7,8,9,10). All these edges cross at the reduced boundary between 6 and 7. Their original named graph is connected because the centers and selected terminals retain their actual parents and (v,u,w) retain the two spine edges. The reduced labels partition ([0,10]).

Write
```
A=6, B=4, k=K−6=(R+5)/2, s=2K−10=2k+2, J=s+3=2k+5.
```
The smallest odd total of two positive quotas is 3, so (k ≥ 4), (K ≥ 10), and (s ≥ K). The old oriented shifts below and at or above (c) are (6) and (6+s). The actual output cut in orientation is (C=c+K). The source label at coordinate (i) is (6+c+i). A lower reduced host (j) gives image (i+5-j), by subtracting its label from the gap label and then subtracting (d-1) from the weight. An upper reduced host (6+b_0) gains (n+s) in its expanded label. Subtracting the gap label, then (d-1), gives image (s+b_0+1-i), since (n-c=d). Hence (Q,P) reflect with intercepts (J,J+2). The source is physically lower exactly when (i<k). Valid gap images use ([0,s-1]) once each and are at least (K) exactly for crossing incidences.

Use (L_j=j) and (H_j=J-j). The source rows (L_{[0,k-1]}) and (H_{[4,k+5]}) are respectively ([0,k-1]) and ([k,s-1]) in actual coordinates. The destination rows (L_{[0,k+5]}) and (H_{[4,k-1]}) are respectively ([0,K-1]) and ([K,s-1]). Each row pair partitions the exact alphabet independently. The physical lower-host shifts are (δ=3,2,1,0,5) for (b,a,c₁,Z,w) respectively. They send (L_j) to (L_{j+δ}) and (H_j) to (H_{j-δ}), with the destination required to lie in that row. (Q) sends (L_j) to (H_j) and (H_j) to (L_j). (P) sends (L_j) to (H_{j-2}) and (H_j) to (L_{j+2}). These are the legal crossing types, since an upper source crosses exactly at a lower host and a lower source crosses exactly at an upper host. In particular the larger (H) source index corresponds to the smaller actual coordinate.

## 3. Necessary reservations, moments and endpoints

Let (x,y) count respectively lower sources at upper hosts and upper sources at lower hosts. As in D157, (x+y=s-K). There are (k) lower sources, so the two aggregate host capacities are (B+2y) at lower hosts and (A+2x) at upper hosts. In fact the lower host capacity is (k-x+y=B+2y), and the upper capacity is its complement in (s). Lower-color fresh vertices consist of the (A) fresh lower exterior vertices and the upper parents' gap leaves. The symmetric formula holds for the upper color. Thus (N_low=2(A+x)), (N_high=2(B+y)), giving (x=k-6) and (y=2) in this exterior. In particular (k ≥ 6).

Upper-parent images are at least 4, since the smallest reflection intercept is (s+3) and the largest source coordinate is (s-1). Nonnegative lower shifts then force images 0 through 3 to use their equal sources at the sole neutral host (Z). Inductively, a positive shift into the next image would use an already assigned smaller source. These four assignments exhaust (Z). The only lower-host assignments left are three first-section terminals and the direct leaf. Exactly two are in each source row by (y=2).

The permutation moment (Σᵢ(π(i)−i)=0) holds in actual gap coordinates. Each upper-host term is odd modulo two, since both reflection intercepts are odd. Their combined quota (R-1) is even. If (a) has original quota two, the four remaining lower shifts are (1,2,3,5), with odd sum. This is impossible. Hence (a) has original quota one, all used by its exterior terminal. There are two possibilities.

| Original quota two at | Four nonneutral shifts | Their total (D) |
|---|---|---|
| (c₁) | (1,1,3,5) | 10 |
| (b) | (1,3,3,5) | 12 |

Let (X) be the two remaining lower-host source indices in row (L), and (Y) those in row (H). Their images have respective indices (X'={x_i+δ_i}) and (Y'={y_i-η_i}), with each shift from its actual host. Every remaining (L) source uses (Q) or (P) into (H). On ([4,k-1]) the source indices omit (X), the destination indices omit (Y'), and a (P) step subtracts two. Thus (2N_{PL}=ΣY'-ΣX). Every remaining (H) source uses (Q) or (P) into (L). On ([4,k+5]) the source indices omit (Y), the destination indices omit (X'), and a (P) step adds two. Thus (2N_{PH}=ΣY-ΣX'). Adding gives
```
p−1 = N_PL+N_PH = ΣY−ΣX−D/2.
```
Both cross-row matchings preserve index parity. In the first interval the omitted parity counts agree on the two sides, so (ΣY' ≡ ΣX) modulo two. As both shifts (η_i) are odd, (ΣY ≡ ΣY'). Therefore (D=10) forces even (p), while (D=12) forces odd (p).

Each (H) lower-host image has index at most (k-1), so (y_i ≤ k-1+η_i). The two shifts sum to at most eight, and (ΣX ≥ 4+5=9). The even difference (ΣY-ΣX) is therefore at most (2k-4), the largest even value below or equal to (2k-3). From the moment, even (p ≤ 2k-8) and odd (p ≤ 2k-9). Since (R=2k-5), these imply respectively (q ≥ 3) and (q ≥ 4).

## 4. Exact repair of two deleted row cells

Consider one (L) reservation at (x_0) with positive odd shift (δ), and one (H) reservation at (y_0) of opposite index parity with positive odd shift (η). Require (x_0,y_0-η ∈ [4,k-1]), (y_0,x_0+δ ∈ [4,k+5]), (y_0-η ≥ x_0), and (y_0 ≥ x_0+δ). These odd-shift and membership conditions make each deletion pair lie on one parity path. They are needed in the elementary chain statement and hold in all applications below.

On the (L)-to-(H) path of (x_0)'s parity the source index (x_0) is missing and the destination index (y_0-η) is missing. Apply (P) to (x_0+2,x_0+4,…,y_0-η). Their shifted images exactly fill (x_0,x_0+2,…,y_0-η-2). Use (Q) at every other available index of that parity. In reverse row direction the omitted source is (y_0) and omitted destination (x_0+δ). Apply (P) to (x_0+δ,x_0+δ+2,…,y_0-2). Their images are (x_0+δ+2,…,y_0). All other available indices of this parity use (Q). Endpoint equality gives the empty run. Each run, together with the identity assignments on its complement, is a bijection onto the exact remaining destinations. The count of (P) leaves is (y_0-x_0-(δ+η)/2).

If the two (L) reservations have opposite parity, the two repairs act on different parity paths in each direction. They combine without collisions. Lower-host reservations preserve their row, and the repairs switch rows exactly as required by the physical incidence. Individual host quotas follow by designating the lower reservations and counting the two repair runs. All cross-row choices other than those counted at (P) go to (Q).

## 5. Symbolic constructions for the fixed exterior

Always reserve (L_0,L_1,L_2,L_3) at (Z). Use the table's physical quota-two placement according to (p)'s parity. Fill the unassigned roles in the order b, a, c₁, taking the available actual quota-one centers in increasing original branch index. In particular a always has quota one. The construction uses exactly its exterior terminal.

**Even (p=2).** The hypotheses give (q ≥ 5) odd and (k ≥ 6). Pair (L_4) at (b) with (H_9) at (w), and (L_5) at (c₁) with (H_6) at (c₁). Their (H) images are (H_4,H_5), and (L) images (L_7,L_6). All belong to the required intervals even at (k=6). The first pair has one (P) use at (H_7); the second has none. All other cross-row choices use (Q). The direct leaf has (i=J-9=2k-4) and image (J-4=2k+1) and at k=6 they are 8 and 13. This is an actual upper-source crossing, with the two first-center incidences at (L_4,L_5) noncrossing and the (H_6) incidence crossing.

**Even (p ≥ 4) and odd (p ≥ 3).** In both cases take (x_1=4,x_2=5). Use (c₁) at both (L) reservations for even (p). For odd (p) use (c₁,b) respectively. Use (w) at (H_{4+Δ₁}) and (b) at (H_{5+Δ₂}), where (Δ₁,Δ₂) are odd and
```
5≤Δ₁≤largest odd ≤ k,         3≤Δ₂≤largest odd ≤ k−3.
```
For (k ≥ 6) their sum ranges over every even value from 8 to (2k-4). Indeed write each variable as its minimum plus twice a bounded nonnegative integer, and distribute the required sum's excess over 8 to those integers, first up to the first one's bound and then to the second. The upper bounds sum to (2k-4) for each parity of (k). Use (Δ₁+Δ₂=p+4) for even (p). Here (q ≥ 3) is exactly the upper-sum bound, and (p ≥ 4) gives the lower bound in this subcase. For odd p use p+5. The inequalities q ≥ 4 and p ≥ 3 likewise give the bounds. In either case (R ≥ 7).

The two (H) sources have indices (4+Δ₁) odd and (5+Δ₂) even, both in ([4,k+5]). Their (H) images have indices (Δ₁-1,Δ₂+2) in ([4,k-1]), with respectively even and odd parity and no index smaller than the corresponding (L) deletion. The two (L) images have indices 5 and 6 for even (p), or 5 and 8 for odd (p). They are in ([4,k+5]) and no larger than the associated (H) deletions. Thus both repairs apply and use (Δ₁+Δ₂-D/2=p-1) leaves at (P). Every other remaining cross-row choice uses (Q).

**(p=1).** The moment requires (D=12). For (k=6) the two (L) reservations must omit (X={4,5}) of opposite parity. The only cross-row host is (Q), so necessarily (Y'=X) and (X'=Y). Both shift types reverse index parity. For each (x₀ ∈ X), its (L) translation reaches (y_0=x_0+δ) of opposite parity. The (H) translation at that unique parity in (Y) must return to (x_0), as (X) has only one member of that return parity. Hence the paired shifts must be equal. The multiset (1,3,3,5) cannot split into two equal pairs.

For (k ≥ 7), use (L_4,L_6) at (b), with images (L_7,L_9), and (H_7,H_9) at (c₁,w), with images (H_6,H_4). Now (X={4,6}=Y') and (Y={7,9}=X'). All indices lie in their required intervals. Identity in row indices using (Q) therefore gives the exact cross-row bijections on the complements, without any (P) gap assignment. The (H_9) direct leaf crosses. The actual center (P) and its one exterior terminal remain present. Since (k=(q+6)/2), the threshold is exactly (q ≥ 8).

In every construction (Z) gets four, (a) zero, (b,c₁) respectively one and two in the even case or two and one in the odd case, and (w) one. The remaining (s-8=R-1) sources give (p-1) leaves at (P) and (q) at (Q). There are (k-6) crossing (L) sources (all but the six at lower hosts) and two crossing (H) sources (the two lower-host reservations). Every other arrow has the noncrossing row type. All destinations are filled once in the appropriate crossing partition. This proves the ordered criterion. With selectable second roles, if the odd quota is at least three, choose it at (Q) and the even quota at (P). If the odd quota is one and (R ≥ 7), the even quota is at least six. The value six fails both placements. For every even quota at least eight choose the unit quota at P.

## 6. Full E+ scope and archived controls

For an arbitrary E+ witness within the declared D157 arrangement, let (e_1,e_2) count exterior terminals by original section and (h) indicate the exterior direct leaf. Then (A=5+e_2), (B=3+e_1+h). The D147 reduced terminal balance used by D164 requires (e_1=0) exactly when (e_2=0). To see the needed implication, (u) is at (A+1) by the forced weight one. Replacing an ordinary lower attachment to (u) by a lower terminal at a true upper center increases the reference difference by the positive amount (b_0-1). Replacing an ordinary upper attachment to (w) by an upper terminal at a true first center reduces the difference by its positive reduced label. Both reduced edge sums must be equal. Thus E+ requires both terminal counts positive. Since (N_low=2(A+x) ≥ 12) in E+, it follows that (R ≥ 7). This argument allows all admitted widths.

For prefix transport within the declared arrangement, a full witness on any admitted prefix first normalizes by complementing to the minimum orientation if needed. The prescribed old shifts leave exactly the two exterior intervals and the middle gap. The old membership condition is (A ≤ K ≤ A+s). The smallest old crossing weight after shifting is (d-1+s) and requires (s ≥ K). Every exterior edge crosses, so its difference is (n+s) plus the reduced difference obtained by undoing the upper expansion. The (A+B) distinct such weights exhaust ([n+s+1,m]). The middle labels and residual weights are therefore exactly ([A+c,A+c+s-1]) and ([d-1,d+s-2]). Subtract their initial values to obtain a full normalized gap permutation. Its legal arrows, physical cut (k), threshold (K), and individual quotas depend on the normalized exterior and suffix. They are independent of (n,c,d).

Conversely retain the normalized exterior, actual selected leaves and gap coordinates, and lift them on any independently supplied admitted prefix. Apply the prescribed old shifts, expand upper exterior labels by (n+s), and add (A+c) to gap coordinates. The same actual parent differences follow from the normalized formulas and the full bands fill both alphabets. The crossing and noncrossing returns are exact by D157. Complementation to maximum polarity transports the cut and absolute weights exactly as in Section 7. This normalization and lifting applies to E+ and preserves the selected actual terminal set and the direct leaf's exterior or gap status. It makes no reduction claim outside the declared arrangement.

A bijection between two relative copies fixes the roles of (v,u,w), matches centers within each section to centers of the same full quota, and matches actual terminals at their own matched parent by original terminal index order. Match the two equal first quota-one centers by physical index order among that quota; match the unique direct leaves separately. This transports physical incidences and the normalized witness in either direction. The labeling on a given original still uses its fixed named indices; the arrangement imposes no increasing label order among the physical branch positions. Thus all physical orders of the same two quota multisets have equivalent reduced feasibility on admitted prefixes.

The checked D164 positive `target-0060` has ordered profiles ((1,1,2,4),(2,5,0)). Its saved E+ exterior has (a=b:28:1), (Z=b:28:3), (P=b:29:0), (Q=b:29:1), exterior terminals (l:28:1:0) and (l:29:0:0), and the direct leaf at source 8 and image 13. The (p=2) construction independently supplies those quotas and that direct-leaf feature, preserving the actual named incidences. Exact reproduction of every archived coordinate is unnecessary for the theorem.

Under the Director's completed-evidence acceptance recorded in the [D165 custody receipt](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN_001/CUSTODY.json), the `target-0057` E+ negative is on ordered ((1,1,2,4),(1,6,0)), with its independent exhaustion and agreed qualified physical strata covering 66 representatives. The other seven saved negatives retain their distinct original bindings. Both role choices fail on the fixed exterior by the ordered theorem. For the full E+ class, if there were an E+ completion in any physical order on another admitted prefix, normalize and transport it by actual parent names to the matching original roles of target-0057, then lift onto its independently supplied (n=74) prefix, admitted since (2K=24). The declared class and E+ membership are preserved, contradicting the accepted full-class exhaustion on that original. The reviewed D164 enumeration is complete for compatible E+ witnesses after its sound necessary prunes and sibling-name transport. This proves the full-class corner by accepted finite exhaustion plus symbolic transport, without a new negative search or an assertion that the fixed exterior exhausts all possible E+ exteriors. The full E+ classification follows from this corner, the (R<7) count, and symbolic supply elsewhere. [D164 records](../evidence/runs/d164-exceptional-four-first-001/MANIFEST.json) · [D163 normalization](ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION.md#7-prefix-independence-in-the-exact-arrangement-and-the-p2-controls)

## 7. Exact named reconstruction and composition

Select the first indexed terminal at (a) and (P) for the two exterior roles. At each parent assign its constructed source coordinates in increasing order to the remaining actual terminal indices in increasing order. The sole direct leaf at (w) gets its designated source. Use no new incidence. The old, gap and reduced exterior label partitions give
```
L_old   = [6,c+5] ⊔ [c+s+6,n+s+6]
L_fresh = [0,5] ⊔ [c+6,c+s+5] ⊔ [n+s+7,m]
D_old   = [1,d−2] ⊔ [d−1+s,n+s]
D_fresh = [d−1,d+s−2] ⊔ [n+s+1,m].
```
The old difference palette follows by preserving cut membership, hence adding (s) only to old crossing weights. The exact gap permutation fills the low fresh band. Each expanded exterior edge crosses and gains (n+s), filling the high band. The gap crossing weights are ([d+K-1,d+s-2]) and its noncrossing weights are ([d-1,d+K-2]). Together the full crossing and noncrossing palettes are ([d+K-1,m]) and ([1,d+K-2]). Full vertex and weight bijections follow from the disjoint bands. The actual extreme output frontier is (w=0) in orientation. Since (m=2C+2), this returns exactly (S₋₁) at (C). The continued witnessing spine retains the actual suffix section incidences.

Let (I=S_b ⊔  S_a ⊔  S_{c₁} ⊔  S_Z) be the actual gap-source sets at first-section parents and (J_1=(S_b+3) ⊔ (S_a+2) ⊔ (S_{c₁}+1) ⊔  S_Z) their image sets. Disjointness follows respectively from the reserved source partition and the proved bijection on images. Let (I',J_2) be their complements in ([0,s-1]). Removing already included (v), the oriented exterior partitions are
```
E₁ = {2,3,4,5,n+s+7,n+s+9}
E₂ = {0,1,n+s+8,n+s+10}.
```
The previously scored first exterior incidences use (n+s+[1,6]), the remaining incidences (n+s+[7,10]). Therefore at the first-section boundary the exact inventories are
```
used labels       L_old ⊔ E₁ ⊔ (6+c+I)
remaining labels  E₂ ⊔ (6+c+I′)
used weights      D_old ⊔ (n+s+[1,6]) ⊔ (d−1+J₁)
remaining weights   (n+s+[7,10]) ⊔ (d−1+J₂).
```
The label-side partitions are intersections of those oriented label sets with ([0,C-1]) and ([C,m]). In particular gap labels below the cut correspond to (I ∩ [0,k-1]) and (I' ∩ [0,k-1]) respectively. In the used weights, the old crossing band and the used exterior band are crossing and ([1,d-2]) is noncrossing. The remaining exterior band is crossing. In each respective gap weight set the crossing part is (d-1+(J_i ∩ [K,s-1])) and the noncrossing part (d-1+(J_i ∩ [0,K-1])). The literal unfinished interface edge is (uw), with endpoints (n+s+7) and 0 in orientation, and weight (n+s+7). It belongs to the remaining crossing inventory.

For actual minimum polarity retain these labels and cut. For actual maximum polarity orient the input by (G=n-g). The actual input cut is (n+1-c). Complement the output about (m), with actual cut (m+1-C). For an actual old label (g) below the actual input cut, (G ≥ c), so the output is (m-(n-g+6+s)=g+4). For an old actual upper label the output is (g+4+s). Thus the respective actual lower shifts are six for minimum and four for maximum; the upper shift adds (s). Both preserve actual cut membership. Complement both partial label inventories, reversing their sides, and keep the weight inventories and crossing flags. In maximum polarity the first frontier is (u=3), the returned frontier is (w=m), and the connector has the same weight.

For any finite sequence of admitted blocks, each input prefix must satisfy its own phase, size, actual port and inventory requirements. This includes preceding D134 or D157 suppliers within their separate exact scopes and other compatible (S₋₁) blocks. The independent symbolic rule supplies the complete new state from the actual topology and prior state. Each old vertex retains its actual cut side under each successive placement. If (C_i) is the actual cut at block (i), let (Λ_i,Σ_i) be the sums of subsequent actual lower shifts and gap widths. An existing label (g) then has final image (g+Λ_i+Σ_i · 𝟙[g ≥ C_i]), by induction along the sequence. Each existing crossing weight gains Σ_i, and each noncrossing weight is unchanged. Apply the same placement to the labels and eventual weight of (uw), and to the block's intermediate label and weight sets in its own alphabet. Final complements give the remaining inventories including later blocks. All interval choices and quota assignments terminate in finitely many operations per finite block, and the finite suffix sums give immutable final labels for the admitted sequence. There is no assertion of an arbitrary topology decomposition.

## 8. Strategic reassessment

On this fixed exterior the residual allocation admits an exact description after choosing the four named lower-host assignments. For each same-parity index path and for each cross-row direction, let (S_j,D_j) be the indicators of surviving source and destination cells after the reservations, and (B_j) the indicator that its source uses (P). For L→H, flow conservation is (D_j=S_j-B_j+B_{j+2}), starting with (B_{j_{min}}=0) and ending with (B_{j_{max}+2}=0). Necessity is the list of exactly two incoming arrow types at a destination. For sufficiency the recurrence must give (0 ≤ B_j ≤ S_j) at every index and respect both boundaries. Assign the indicated moves and each destination then has exactly its required incoming count. For H→L reverse the path order to obtain the same recurrence. The combined (P) count must be (p−1). This handles multiple deletions in one parity path, including the no-(P) two-cycle. It is an exact symbolic description conditional on legal reservations, with a unique residual assignment for those reservations. There is no arbitrary image-mask choice on the two remaining physical upper hosts. The needed inputs are the exact row alphabets, the particular shifts zero and two on the cross-row arrows, and the bounded exceptional lower-host assignments. No claim on arbitrary widths or on the capped target follows.

The evidence suggests testing a wider first-profile boundary through actual quotas and analogous exact repairs. The proved supplier concerns ((1,1,2,4)), whereas target-0429 has first profile ((1,3,4,4)). A single proposed unstarted direction is the latter profile's symbolic width-(6,4) supply, contrasting the saved positive target-0428 with the uncompleted target-0429 under the same first profile. The D164 finite separation hypothesis remains undecided.
