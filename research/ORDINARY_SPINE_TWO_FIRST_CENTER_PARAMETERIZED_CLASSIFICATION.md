# D155 — Exact two-first-center D143 classification

Task `LCL-ORDINARY-SPINE-TWO-FIRST-CENTER-PARAMETERIZED-CLASSIFICATION-001`. All structural parameters and quotas are exact integers, excluding booleans. Intervals are inclusive and empty if reversed. In this proof T and E denote the terminal-free and unrestricted-exterior arms when named as arms. T in a quota formula is a half-quota.

## 1. Statement and retained interface

Supply an independently constructed named ordinary graceful D134 p=1 prefix, with actual extreme frontier v, oriented labels G(v)=0, n=2c+2, and actual crossing spectrum [d,n] at c, where d=c+2. Append the ordered physical sections (2r,2t) and (2p,2q+1,0) at u,w with r,t,p,q≥1. The two sections have H₁=2r+2t+3 and H₂=2p+2q+5 fresh vertices, each giving one actual parent edge, so K=r+t+p+q+4 and m=n+2K. Require n≥2K. Keep the exact D143 two-translation old placement, designated-cut membership and returning D134 state.

**Both arms are feasible exactly when max(r,t,p)≥2.** The affirmative construction uses a terminal-free exterior for the entire stated parameter domain. For r=t=p=1 the proof exhausts every D143 exterior, including selections with actual terminals, for every q≥1. It is a restriction on this placement and return. Ordinary graceful labelings under other embeddings remain outside the claim.

By the [D143 reduction](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md#3-exact-exterior-and-gap-reduction), the oriented exterior has widths A,B, the gap has s=2K−A−B≥K, v=A, u=A+1 and w=0. All centers are exterior. The reduced tree on v and the exterior vertices has actual spectrum [1,A+B], with every edge crossing between A and A+1. Its high differences expand by n+s. A gap source i∈[0,s−1] is physically lower for i<k=K−A, and its actual leaf label is A+c+i. The gap difference is d+π(i). At lower host j the map is i+A−2−j, and at upper host index b (reduced label A+b) it is s+b−i. The image must lie in [0,s−1] and be at least K exactly on crossing incidences. Thus D143 requires a permutation of the gap coordinates with exact quotas on the original hosts. No old vertex or physical incidence is reindexed.

## 2. Positive supply of the reduced exterior and coordinate rules

Use A=B=3, s=2K−6, k=K−3 and J=s+2=2k+2. Here K≥8, so s≥K. Set the reduced labels of v,u,w,a,b,P,Q to 3,4,0,1,2,5,6, respectively. The edges vu,ub,ua,uw,wP,wQ have differences 1,2,3,4,5,6 respectively and all cross the reduced cut. The two second centers P,Q are the original even and odd centers, respectively. In Regime I take a,b in their original order. In Regime II choose a to have half-quota at least two, taking the first such center in original order, and b the other actual center. Write R,T for their half-quotas in numerical role order. This assigns labels to two distinguished original centers and retains each original branch index, parent and leaf list. All terminals and the sole actual direct leaf stay in the gap. The required host quotas (w,a,b,P,Q) are (1,2R,2T,2p,2q+1) and sum to s.

Sources are Lⱼ=j for j∈[0,k−1] and Hⱼ=J−j for j∈[3,k+2]. The H sources are precisely [k,2k−1], in reverse order. Image cells of degree coordinate below K are Lⱼ for j∈[0,k+2], and image cells at least K are Hⱼ for j∈[3,k−1]. These two alphabets partition [0,s−1] on their respective source and image roles. The following table substitutes the actual hosts' reduced labels into D143. A use is legal only if its destination cell exists.

| Host | Source Lⱼ | Source Hⱼ |
|---|---|---|
| w | Lⱼ₊₁ | Hⱼ₋₁ |
| a | Lⱼ | Hⱼ |
| b | Lⱼ₋₁ | Hⱼ₊₁ |
| P | Hⱼ | Lⱼ |
| Q | Hⱼ₋₁ | Lⱼ₊₁ |

The H entry on an upper source at a lower host expresses a crossing leaf. The H entry on a lower source at an upper host also expresses a crossing leaf. The L entries express noncrossings. These facts follow from the actual cut and host side. The two uses of H in the source and destination alphabets have distinct bounds.

### Regime I: p≥2

Place L₀ at w, L₁ at b and L₂ at a. Their images are L₁,L₀,L₂. Place Hₖ,Hₖ₊₁,Hₖ₊₂ at P, supplying Lₖ,Lₖ₊₁,Lₖ₊₂. The remaining sources and images have both rows in the common columns [3,k−1].

Put h=T+q≥2 and take a packet of h+1 consecutive columns beginning at ℓ=3. There are k−3=R+p+h−2 common columns, so the packet fits and leaves R+p−3. Choose a deterministic word c₁,…,cₕ with c₁=Q, then T−1 letters b and q letters Q. In order, use a at L_ℓ and cⱼ at L_(ℓ+j) for j=1,…,h. Use c_(j+2) at H_(ℓ+j) for j=0,…,h−2, b at H_(ℓ+h−1), and P at H_(ℓ+h).

Column ℓ receives its L image from a and its H image from the incoming c₁=Q. At the interior column ℓ+j, 1≤j≤h−1, the source one column to the right in row L and the source one column to the left in row H both use c_(j+1). If that letter is b the two images occupy L,H respectively. If it is Q they occupy H,L respectively. The last column receives H from the preceding H source at b and L from its own H source at P. All images are within the packet's two actual rows and each cell is supplied once. Exactly one a and one P are used. The L letters contain T−1 b and q+1 Q, and the H letters before the two final assignments contain T−1 b and q Q. Counting the final b and P gives packet quotas a=1, b=2T−1, P=1, Q=2q+1.

Take the first R−1 unused common columns with both sources at a, then the remaining p−2 with both at P. The former fix their rows and the latter exchange them, each providing a bijection of its own two cells. Empty sets for R=1 or p=2 are permitted. With the reserved sources the totals are w=1, a=2R, b=2T, P=2p and Q=2q+1. All uses have legal destination cells by the reservations and partitions above. The table then gives every crossing predicate.

### Regime II: p=1 and max(r,t)≥2

Choose R≥2 as specified above. Place L₀,L₁,L₂ at a and Hₖ₊₁,Hₖ₊₂ at P. They supply L₀,L₁,L₂,Lₖ₊₁,Lₖ₊₂. Place Hₖ at w, supplying Hₖ₋₁. Its actual coordinates are J−k=k+2=K−1 to J−(k−1)=k+3=K, a crossing at the lower host w.

Put h=T+q≥2 and end the packet at ℓ+h=k−1, with ℓ=k−1−h=R+1≥3. There are R−2 common columns before it. Choose c₁=Q followed by T letters b and q−1 letters Q. Use the same L row and the same H row through H_(ℓ+h−2) as in Regime I. Use Q at H_(ℓ+h−1) and H_(ℓ+h). The first column and the interior columns ℓ+j for 1≤j≤h−1 are filled by the same two-arrow argument. The last packet column gets L from the preceding H source at Q and H from reserved Hₖ at w. The last H source at Q supplies Lₖ, the one remaining right boundary cell. These two right-boundary uses occupy existing image cells, since k−1 belongs to the common interval and Lₖ belongs to the longer noncrossing row.

Put both sources at a on the R−2 earlier columns. The L word contains T b and q Q. The initial H word contains T b and q−1 Q, and the two final H uses add two Q. The packet contributes one a, so together with the three left reservations and the earlier columns a receives 4+2(R−2)=2R. The other quotas are w=1, b=2T, P=2 and Q=2q+1. This includes q=1, R=2 and T=1 together or separately. Both physical first-center orders are covered by the role choice. The displayed images occupy the complete two image alphabets without collision, and the host table certifies the actual crossing status of each use.

## 3. Expansion, independent intermediate supply and finite composition

For each host, assign the increasing physical source coordinates of its uses to its increasing terminal indices. Give w its one original zero-entry leaf. The quota bijections preserve every original vertex and edge on its own parent. The construction specifies the exterior and all source assignments by parameters before any labeling of a full target is consulted.

In the oriented coordinates the old sets are
```
L_old = [3,c+2] ⊔ [c+s+3,n+s+3]
D_old = [1,d−1] ⊔ [d+s,n+s].
```
Keep the lower exterior at 0,1,2, and expand the upper exterior to n+s+[4,6]. The actual old frontier is placed at 3. Its connector and all other exterior edges consume [n+s+1,n+s+6], all crossing the output cut C=c+K. Gap labels are d+1+[0,s−1]. Gap differences are d+[0,s−1]. The two unused old palettes are thus filled once each, proving both bijections. Old crossing differences gain s. The gap permutation supplies noncrossings [d,d+K−1] and crossings [d+K,d+s−1]. Together with the exterior and old edges, the actual noncrossing spectrum is [1,d+K−1] and the crossing spectrum is [d+K,m]. The old side membership holds because the two old intervals are separated by the gap and k∈[0,s]. The expanded original remains a tree with the declared spine extension. At w=0 the output has n'=m, c'=c+K and d'=d+K, hence the exact D134 p=1 state.

Let S_a and S_b be the actual source coordinates given to a and b by the proved reservations, packet and remainder. These explicit lists are obtained by scanning the stated source intervals and reading the deterministic word. Put I=S_a⊔S_b and D=S_a⊔(S_b−1). The first-section source and image sets are I and D, since these first centers have full-coordinate maps i and i−1. They are independently determined by the roles, parameters and packet. At the first boundary in the oriented final alphabet the exact inventories are
```
used labels       L_old ⊔ {1,2,n+s+4} ⊔ (d+1+I)
remaining labels  {0,n+s+5,n+s+6} ⊔ (d+1+([0,s−1] minus I))
used differences  D_old ⊔ [n+s+1,n+s+3] ⊔ (d+D)
remaining weights [n+s+4,n+s+6] ⊔ (d+([0,s−1] minus D)).
```
The used crossing spectrum is [d+s,n+s]⊔[n+s+1,n+s+3]⊔(d+(D∩[K,s−1])). The used noncrossing spectrum is [1,d−1]⊔(d+(D∩[0,K−1])). The actual port is u at n+s+4. Its only unfinished incidence is uw, whose other endpoint is w at zero and whose difference is n+s+4. The second section consumes the remaining high weights via uw,wP,wQ and the remaining gap images via the same specified permutation. Since H₁ is odd, this intermediate boundary has odd edge count and is supplied in the declared target alphabet, with neither an intermediate D134 return nor a rank hypothesis.

For an actual minimum-frontier input the oriented labels already give its actual completion. For an actual maximum-frontier input read G=n−g and complement all oriented output labels about m. The actual old and returned cuts are n+1−c and m+1−C, with membership preserved after the side exchange. The returned actual frontier is m. The intermediate used and remaining label sets are complemented about m and the port is 2. Both difference inventories and all actual crossing statuses are unchanged. The actual lower shift is 3 for either polarity, and the actual upper shift is 3+s.

The symbolic D134 initializer in the p=1 case with a retained independent maximum-frontier seed gives arbitrarily large admissible initial size, using its actual declared path and first branched section. Complementing it supplies the other polarity. For a finite declared sequence of admitted blocks, each step requires its size bound nᵢ₋₁≥2Kᵢ. Taking a sufficiently large initial supplied state meets every bound if a particular starting state is not prescribed. Each admitted return preserves the full named D134 interface, increases the size by 2Kᵢ, and keeps the same actual extreme polarity. This proves closure by induction, including arbitrary finite repetitions of one admitted block.

For immutable labels at a completed boundary i, let Cᵢ be its actual cut and Sᵢ the sum of future gaps. If there are M future blocks, map any label x already present to x+3M+Sᵢ·1(x≥Cᵢ). Successive side tests are the same on each named old vertex. This formula therefore composes exactly with the next block's increasing embedding. At the intermediate boundary within block i use the actual return cut of that block and the same future formula on the displayed partial label inventory. Add Sᵢ precisely to its crossing weights and keep all other used weights. The remaining palettes are the exact final alphabet complements. This gives once-emitted labels and the actual connector difference at all boundaries. Forming words and gap data and emitting named vertices uses finitely many interval passes and host counters, linear in the supplied original and emitted sizes in indexed integer operations. No placement search is required.

## 4. Exceptional r=t=p=1: all possible widths and the terminal-free cases

Here K=q+7. The [D154 width identities](ORDINARY_SPINE_PARITY_COMPATIBLE_EXTERIOR_QUALIFICATION.md) give A=3+τ₂, B=3+e+τ₁≤4, where τ₁ and τ₂ count first- and second-section exterior terminals and e marks the exterior direct leaf. By [D147 terminal balance](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md#2-terminal-balance-and-paired-exchange), τ₁ and τ₂ are positive together. The sum counts each exterior terminal at its actual physical host. Thus either both terminal counts vanish, or e=0, τ₁=1, B=4 and A≥4. This split covers every D143 selection. In both cases u has no direct gap leaf. Any other upper host index is at least two and can take source i only if i≥b+1, by the image range.

If the exterior is terminal-free and e=1, A=3, B=4, and w has no gap leaf. The first three sources i=0,1,2 are lower because k≥B. None admits an upper host. Of the first centers the neutral shift must take zero, then one (shift −1 would repeat zero). Its two leaves are exhausted. At two the shift −1 would repeat one. This is impossible regardless of the direct leaf's exterior label.

If the exterior is terminal-free and e=0, A=B=3, s=2k with k=K−3≥5. The D154 parity rule puts the odd center Q at index 3 and the even P at index 2. At physical upper source k, only P works, with image K−1. Q would give K despite being noncrossing. At k+1 Q would repeat K−1, so P works with K−2. The largest lower-host map there or earlier is i+1≤K−1, too small for its crossing. P's two leaves are now exhausted. At k+2=K−1, Q repeats K−2 and both first-center translations fall below K. The direct gap leaf at w is forced there with image K, using its one leaf. The first three lower sources now again have only the neutral and −1 translations, with the same underflow and collisions as in the e=1 case. All forced sources and images exist for q≥1.

## 5. Exceptional r=t=p=1: complete reduced classification with terminals

Take e=0, τ₁=1, B=4 and A=3+τ₂≥4. The D153 exact count gives y=r+t−1−e−τ₁=0, so every physically upper source uses an actual upper host. The total lower-host gap quota is B=4. D154 gives A≤p+q+2=q+3, and D143 also requires A+B≤K. Here both are the same width bound. The highest upper index 4 belongs to a second center by D147, since only u and the second centers are exterior neighbors of w. The other center has index ℓ₀=2 or 3, and the remaining upper slot is the sole exterior terminal of a first center.

By the pin on weight two, the first-center labels are A−1 and h₀∈[1,A−2]. Let j* be the label of the first center hosting the unique upper terminal. Write n₄ for the number of lower exterior terminals at upper index 4. The lower terminal slots are [1,A−2] minus {h₀}. Use deficits from A+4. The fixed incidences vu,uw and the two first-center attachments have deficits A+3,3,A+2,h₀+3. The two second-center attachments have deficits 0 and 4−ℓ₀. A lower slot j at upper index b contributes j+4−b. The first exterior terminal at upper index b contributes 4−b+j*. The complete reduced spectrum is equivalent to one use of each deficit in [0,A+3].

**Case ℓ₀=2.** The upper terminal has index 3. Its deficit j*+1 is at least two. The lower slots at index 2 have deficit at least three. Thus deficit one forces j=1 at index 4. The D147 balance gives j*=A−3+2n₄≤A−1. Therefore n₄=1 and j*=A−1. The first exterior terminal uses deficit A. Unless h₀=A−2, that lower slot would belong to index 2 and repeat A, as index 4 has only the slot at one. Consequently h₀=A−2, and the lower terminals j∈[2,A−3] all belong to index 2. Their deficits fill [4,A−1], while the slot one and the fixed and upper-terminal edges account for 0,1,2,3,A,A+1,A+2,A+3. This is exact at A=4 when [2,A−3] is empty. There is one selected terminal at index 4 and A−4 at index 2. The latter must fit the chosen physical quota (2 for the even center, 2q+1 for the odd center).

**Case ℓ₀=3.** The upper terminal has index 2, so balance gives j*=2(A−3)+n₄≤A−1, forcing A≤5. At A=4 there is one lower terminal. If at index 3, j*=2 fixes h₀=2, and j=1 gives deficit two. If at index 4, j*=3, and h₀=2 would put j=1 at index 4 with deficit one, repeating the attachment of index 3. Thus h₀=1 and the lower j=2 gives deficit two. At A=5, n₄=0 and j*=4. At index 3 a lower j=2 would give deficit three, repeating uw, so h₀=2 and the lower j=1,3 give deficits two and four. The three possibilities are exactly

| A | h₀ | j* | Lower terminals by upper index |
|---:|---:|---:|---|
| 4 | 2 | 2 | index 3 hosts 1 |
| 4 | 1 | 3 | index 4 hosts 2 |
| 5 | 2 | 4 | index 3 hosts 1,3 |

For the first two rows the lower terminal gives two, the upper terminal and nonpinned first-center attachment give four and five in one order or the other, and the fixed edges give 0,1,3,6,7. In the last row the lower terminals give two and four, the upper terminal and nonpinned attachment give six and five, and the fixed edges give 0,1,3,7,8. Hence all listed rows have exact reduced spectra. A=5 requires q≥2 by the width bound. In both ℓ₀ cases the described numerical configurations yield reduced exteriors on actual names whenever the width and selected counts fit. Give each prescribed numerical role to the chosen actual center and use any distinct original terminal indices at its own parent in the stated counts. Both choices of even-center position are considered subject to those quotas. The first quotas are both two, so the single exterior terminal at j* always fits. There is no other eligible exterior vertex or attachment. The classification is a reduced-spectrum assertion, independent of the remaining gap compatibility.

## 6. Exceptional gap impossibility for the classified exteriors

For ℓ₀=2, the lower hosts w, the neutral first center at A−2, and the minus-one center at A−1 have quotas 1,2,1. On physically upper sources put z=s+2−i, taking each integer in [3,K−2] once. The upper maps are z (index 2) and z+2 (index 4). Those images must be less than K.

If index 4 is the even center, it has one residual leaf. Image K−1 can only arise on the physically upper sources: the lower-host images of a physically lower source are at most k−1+A−2=K−3, and a lower source at an upper host must cross. Image K−1 thus uses index 4 at z=K−3. The displaced image K−3 cannot then be made by a physically upper source. It requires w at source k−1, since the first-center translations there or earlier reach at most k−1<K−3. The only w leaf is exhausted and the first three lower sources suffer the same zero/−1 contradiction as in Section 4.

If index 2 is the even center, its residual quota is 6−A≤2. At z=K−2 the plus-two alternative violates the noncrossing threshold, forcing index 2. Descending by twos within [3,K−2], the plus-two alternative would repeat the preceding forced image. Thus all these positions force index 2. For q≥2 at least three exist. At q=1, K=8, the two forced uses at z=6,4 require A=4. Then z=5,3 must use index 4, with images 7,5. The four upper images are exactly [4,7]. Here k=4 and s=8, so the remaining sources [0,3] use the four lower-host gap leaves. Their total displacement is 2+2·0−1=1. A permutation of [0,3] has displacement sum zero. Hence this last case also fails.

For ℓ₀=3, the first four sources 0 through 3 exist and are physically lower because k≥B=4. Neither eligible upper center can use them. They exhaust the four lower-host leaves; all upper-host images have value at least 4 because i≤s−1 and b≥3. Consequently the four lower-host images must be [0,3]. In the three rows of the table their displacement sums are respectively 2+2·(−1)+0=0, 2+2·1−1=3, and 3+2·1−1=4. The last two rows are impossible. In the first row upper index 4 retains its entire positive quota. The baseline index 3 map s+3−i permutes [4,s−1] on the remaining sources [4,s−1]. More precisely it maps [4,k−1] onto [K,s−1] (both empty if k=4), and [k,s−1] onto [4,K−1]. Each index 4 choice increases the sum of images by one. The required sum on either side is the baseline sum, so index 4 cannot be used at all. This contradicts its required quota.

An independent check of the terminal-enabled obstruction uses the [D144 summed displacement identity](ORDINARY_SPINE_TWO_SECTION_GAP_ALLOCATION.md). For the sole odd second center with upper index b_O, the lower-host contribution modulo two is j*, using the even counts before removing the one terminal and the even total of four lower leaves. The upper-host contribution modulo two is s+b_O−(s+1)(A−3)−j*: start from the two original second quotas and subtract s+b for each selected terminal, whose b−1 values sum to j* by D147. Their sum is b_O−1 modulo two, since s≡A (mod 2). Thus b_O must be 3 for any successful terminal-enabled gap. This already rules out ℓ₀=2 and pins the even center at 4 for ℓ₀=3. All three reduced rows then leave at least one gap leaf at that even center. The baseline sum on [4,s−1] rules out every such use. This separate argument reaches the same impossibility with no allocation enumeration.

Together Sections 4–6 exclude both arms for every member of the exceptional line. Sections 2–3 supply both arms everywhere else. The two-row interval analysis and the exhaustive exterior argument use the exact original quota patterns rather than extrapolating a finite table.

## 7. Frozen structural controls and scope

The D154 retained prefix has n=54 with actual maximum frontier s:25. The smallest Regime I retained target is 0005 with (r,t,p,q)=(1,1,2,1). The two smallest Regime II controls in their respective first-center orders are 0017 and 0065, with (1,2,1,1) and (2,1,1,1). All have K=9, s=12. The proof covers their actual profiles and the physical role assignment on each. It supplies the same direct-leaf source/image pair as each saved witness (0→1 or 8→9), without requiring equality of every saved label. Controls 0001–0004 use (1,1,1,q) with 1≤q≤4 and remain archived as independent computational exhaustions. The new proof excludes those targets and the entire exceptional line for every supplied prefix and size in scope. No D154 outcome was generated or altered by the proof.

The D154 finite coverage, source identities and archive remain independent evidence. This classification establishes neither unrestricted ordinary nongracefulness nor exhaustiveness under other embeddings or return contracts. It makes no claim of literature novelty. The selected symbolic question is settled; no additional hybrid run is needed for this profile family.
