# D163 — Exceptional exterior even-quota packet extension

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-EVEN-SECOND-QUOTA-EXTENSION-001`. All labels, counts and parameters are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty. Use ⊔ for disjoint union. Every statement below concerns the declared [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) membership-preserving connected crossing-exterior arrangement with all positive centers exterior, an actual leaf-only gap at original hosts, and exact S₋₁ input and return.

## 1. Domain and conclusions

Independently supply a named ordinary graceful S₋₁ prefix with actual witnessing spine and extreme v. Orient G(v)=0. Its size is n=2c+2, with d=c+2 and actual crossing and noncrossing spectra [d−1,n] and [1,d−2] at cut c. Attach actual consecutive spine sections at u,w. The first quotas in any physical order are 4,2r+1,2t+1. The positive second quotas are 2p and 4 in either physical order, with a sole actual direct leaf at its declared original index. Here r,t≥0 and p≥1. No numerical role assignment changes an original parent or branch index.

The first addition has 2r+2t+10 vertices and the second 2p+8, so K=r+t+p+9 gives 2K new vertices and edges. Put m=n+2K and require n≥2K. In the original graph bipartition from v lower, the fresh lower side has w, the three first centers, and 2p+4 second terminals. The fresh upper side has u, the two second centers, the direct leaf and 2r+2t+6 first terminals. Thus N_low=2p+8 and N_high=2r+2t+10. Both are even, as required by the fixed phase.

For the specified [D162](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION.md) E+ exterior A=5,B=4 with the declared role choices, allocation is feasible **exactly when p=1 or r+t≥1**. Here feasibility allows choosing which odd first center has numerical role b. The fixed exterior's remaining exclusion for p≥2 and r=t=0 does not rule out alternate exteriors.

Across all admitted terminal-free exteriors T is feasible **exactly when max(r,t)≥2**, independently of p. In the full E+ class p=1 is the accepted D162 case, p=2 is feasible **exactly when r+t≥1**, and for p≥3 the case r=t=0 remains open here. The p=2 full-class negative is an accepted finite exhaustive result transported symbolically to the admitted independent prefixes and polarities, with the named-role justification in Section 7. For p=2 the separating range is r,t∈{0,1}, r+t≥1. The proof offers no unrestricted nongracefulness result.

## 2. Exact exterior and physical arrow maps

In E+ use A=5,B=4,s=2K−9,k=K−5=r+t+p+4 and J=s+3=2k+4. These obey A≤K≤A+s and s≥K since K≥10. Give v,u,w,a,b,Z,Q,P reduced labels 5,6,0,3,2,4,7,9 respectively. Give a,b the chosen actual odd quotas 2r+1,2t+1, Z the actual quota four, Q actual quota four and P actual quota 2p. At p=2 the equal second quotas permit either numerical choice of Q and P, still using distinct physical parents. Reserve one original terminal at a for reduced label 8 and one at P for reduced label 1. The actual direct leaf of w is a gap leaf. The remaining physical quotas at (a,b,Z,Q,P,w) are (2r,2t+1,4,4,2p−1,1). When r=0, the actual center a and its exterior terminal still exist.

The reduced labels occupy [0,9]. The actual edges vu,uZ,ua,ub,a-to-8 use weights 1,2,3,4,5. The actual edges uw,wQ,P-to-1,wP use 6,7,8,9. All cross between [0,5] and [6,9]. The exterior is connected through the original spine and center/terminal incidences. The expanded first and second exterior weight ranges are n+s+[1,5] and n+s+[6,9], respectively.

For general declared widths expand upper reduced exterior labels by n+s. A gap leaf of coordinate i carries A+c+i, is physically lower exactly for i<k, and contributes weight d−1+π(i). Actual endpoint subtraction gives π(i)=i+A−1−j at a lower parent j and π(i)=s+b₀+1−i at an upper parent A+b₀. The images must biject [0,s−1] and be at least K exactly for crossings of the actual cut C=c+K. For this E+ exterior the corresponding maps are i+1,i+2,i,s+3−i,s+5−i,i+4 in the host order given above.

Set Lⱼ=j, Hⱼ=J−j. The source intervals L_[0,k−1] and H_[4,k+4] map to the lower [0,k−1] and the upper [k,s−1] coordinates respectively, the latter in reverse. The destination intervals L_[0,k+4] and H_[4,k−1] map to the noncrossing [0,K−1] and crossing [K,s−1] images. The complete table obtained by substitution is

| Actual host | L source at j | H source at j |
|---|---|---|
| a | L_(j+1) | H_(j−1) |
| b | L_(j+2) | H_(j−2) |
| Z | L_j | H_j |
| Q | H_j | L_j |
| P | H_(j−2) | L_(j+2) |
| w | L_(j+4) | H_(j−4) |

An arrow is usable when its source and destination exist and the actual host has capacity. With those bounds, lower hosts keep the row and upper hosts exchange rows, so the H image condition is exactly the physical crossing test.

## 3. Selectable pairs at a double-displacement boundary

A double entry before common column j has all L positions through j+1 supplied, H positions through j−3 supplied, and H_(j−2),H_(j−1) still to fill. Indices refer only to existing cells. Any outside reservation is retained separately. In its internal range all later image cells are unused. For both sources at b, column j outputs L_(j+2) from L_j and H_(j−2) from H_j. For both at P, it outputs the same two images with the source roles reversed. Each fills one required H cell, adds one L cell, and gives exactly the double entry at j+1. The b pair consumes two b gap leaves and contributes one upper-source crossing y. The P pair consumes two P gap leaves and contributes one lower-source crossing x. This distinguishes the exact physical quotas and crossing types even though the image sets coincide.

An additional P pair in the parameterized construction below increases p by one. Then 2p increases by two at its fixed actual P, its remaining gap quota increases by two, K and k increase by one, s and J by two, and the common-column capacity increases by one. This is a family of constructions in the new alphabets and their exact right boundary positions. The shift of those positions is part of the proof.

## 4. Terminal-enabled allocation for the exact positive range

First take t≥1 in the chosen numerical roles. Assign the cells below, with a paired range meaning both L and H sources of each column.

| Sources | Host |
|---|---|
| L_[0,3] | Z |
| L_[4,r+3], H_[5,r+4] | a |
| L_(r+4), L_(r+5) | b |
| Both rows of [r+6,r+p+4] | P |
| Both rows of [r+p+5,k−1] | b |
| H_(k+1) | b |
| H indices 4, r+5, k+3, k+4 | Q |
| H_k | P |
| H_(k+2) | w |

The two paired intervals are adjacent, of lengths p−1 and t−1, and partition [r+6,k−1]. They may each be empty. The lower source positions before them are exhausted by Z, a, and the two b entries. On H, (4,[5,r+4],r+5) and the paired intervals give [4,k−1]. The remaining H cells occur in order P,b,w,Q,Q. In particular k≥r+6, so all four Q indices are distinct even at p=t=1. The prefix H interval at a is empty when r=0.

Before the pairs the initial b lower sources give L_(r+6),L_(r+7), a lower and upper sources give L_[5,r+4] and H_[4,r+3], and H_4,H_(r+5) at Q supply L_4,L_(r+5). Together with Z these fill L_[0,r+7] and H_[4,r+3], the double entry at r+6. The paired cells fill L_[r+8,k+1] and H_[r+4,k−3], so after all pairs L_[0,k+1] and H_[4,k−3] are occupied once. This remains true at k=r+6 with both paired intervals empty. The final five H sources give, in source order, L_(k+2), H_(k−1), H_(k−2), L_(k+3), L_(k+4). These complete exactly both destination rows without overlap. In particular every source and image used lies in the stated alphabets.

The total a count is 2r and b receives 2+2(t−1)+1=2t+1. Z has four, Q four, P 2(p−1)+1=2p−1, and w one. The lower-source crossings are precisely the p−1 lower P pairs. The upper-source crossings have r uses at a, t−1 paired uses at b, one final use at b and one at w. Thus x=p−1 and y=r+t+1, giving x+y=s−K. The actual direct leaf uses H_(k+2), coordinate k+2, and image K+1. At p=1 the paired P interval vanishes. The two first b lower positions and t−1 b pairs yield exactly the D162 t≥1 assignment.

At p=1 and t=0 use the accepted [D162 t=0 word](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION.md#case-t0). In detail k=r+5, L_[0,3] is at Z, L_[4,r+3] at a and L_(k−1) at b. On H use [5,r+4] at a, {4,k,k+2,k+4} at Q, k+1 at P and k+3 at w. The H images are [4,k−2] from a and k−1 from w, and the five L images from Q and P fill {4,k,k+2,k+3,k+4}. The exact quotas and edge types agree with Section 2, including r=0. Here x=0 and y=r+1, and the actual direct leaf has coordinate k+1 with image K.

For p≥2 and at least one odd quota exceeding one, choose an actual such first center for b, with its own original physical terminals. This makes t≥1 in the numerical role notation. If necessary, exchange r and t as role parameters only, leaving their sum, each actual terminal list and every original incidence fixed. The construction guarantees a feasible role choice at these parameters.

## 5. Fixed E+ exterior obstruction for r=t=0 and p≥2

Now k=p+4≥6 and the quotas at (a,b,Z,Q,P,w) are (0,1,4,4,2p−1,1). Upper-host images are at least four and lower translations are nonnegative. The [D160 low-destination induction](ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY.md#width-independent-first-center-obstruction-under-the-same-arrangement) forces L_0 through L_3 at neutral Z, exhausting Z. A positive lower displacement into L_4 or L_5 at b or w would need one of these consumed sources. a has zero gap capacity. The P upper source would have index 2 or 3, outside the H row. Therefore L_4 and L_5 force H_4 and H_5 at Q.

The rightmost H index k+4 must use Q. b and w would need H images outside their range, P would need L_(k+6) and both a and Z are unavailable. In the last three H columns k+2,k+3,k+4, b is always outside its H range, and P either exceeds the L range or would supply the already consumed L_(k+4) at column k+2. Again a and Z are unavailable. Only Q and the one w leaf can serve these three sources. At least two must use Q, distinct from H_4,H_5 as k≥6. Thus all four Q uses lie on H.

The D157 fixed-phase graph-class identity gives N_low=2(A+x). With A=5 and N_low=2p+8 this forces x=p−1. Each of these lower-to-upper incidences must use P, since Q is exhausted. A lower source L_j is legal at P only if H_(j−2) exists, so j≥6. There are at most k−6=p−2 eligible lower sources, contradicting the required p−1. This proof covers both assignments of the two physical quota-one first centers to a and b because their quotas coincide. Combined with the supplier, it proves the exact stated fixed-exterior condition. Other terminal-enabled exteriors remain outside the obstruction.

## 6. Terminal-free classification for every p≥1

### All-exterior necessity

With no exterior terminal, the lower fresh exterior consists of w and the three first centers, so A=4. If the direct leaf is in the gap then B=3. The unique reduced weight-one crossing and the literal vu pin u at A+1. The first upper gap source i=k exists because s−k=K−B≥A. At a lower host it would require crossing but its image is at most K−1. At an upper host its image is K−B+b₀+1 and must be below K, giving b₀≤1. Its sole possible host u has no direct gap leaf. This is the [D158 obstruction](ORDINARY_SPINE_EXCEPTIONAL_PHASE_PRESERVING_BRIDGE.md#2-first-physically-upper-source).

If the direct leaf is exterior, A=B=4 and all original terminals are in the gap. Both upper parents have even quota, now 2p and four. In the gap permutation moment Σ_i(π(i)−i)=0 their contributions modulo two vanish because π(i)−i=s+b₀+1−2i at each upper parent. The lower shifts at reduced 1,2,3 are 2,1,0. Thus the unit host at reduced 2 has even quota, necessarily the actual quota four. Upper images are at least four. Induction on the first four images forces the neutral host to receive at least four gap leaves. Its quota is odd, so it needs at least five. This proves max(r,t)≥2 for all physical role orders and both direct-leaf placements.

### Supply, rows and common boundary

With max(r,t)≥2 select an eligible odd first neutral quota z≥5 by original index and let a₀≥1 be the other odd quota. Retain D162's reduced v=4,u=5,w=0,a=1,b=2,Z=3,Q=6,P=7,direct leaf=8, with actual quotas a₀,4,z,4,2p on a,b,Z,Q,P. The first weights are [1,4] (vu and three first center edges), and the remaining weights [5,8] (uw and three second attachments). They cross. In Case B only swap the numerical labels at P and the direct leaf, preserving those weight sets and all edges.

Here s=2K−8, k=K−4=r+t+p+5, J=s+3=2k+3. Source rows are L_[0,k−1], H_[4,k+3], destination rows L_[0,k+3], H_[4,k−1]. These are exact alphabets by subtracting each H endpoint from J and using K=k+4. D162's default arrows follow by endpoint subtraction: a,b shift the L row up by two or one and H down by two or one, respectively. Z is neutral. Q exchanges rows preserving j. Default P sends L_j to H_(j−1) and H_j to L_(j+1). Swapped P=8 sends L_j to H_(j−2) and H_j to L_(j+2). Use the row-preservation/exchange crossing rule of Section 2.

Reserve L_[0,3] at Z and H_(k+2),H_(k+3) at Q. Use N_Z=(z−5)/2 neutral pairs, then (b,Q) at column l. It gives L_l,L_(l+1) and leaves H_l pending. At a unit entry at j, L is filled through j, H through j−2 and H_(j−1) is next to fill, apart from the two reserved right L cells. The opening gives this entry at l+1. A default (P,P) column supplies L_(j+1),H_(j−1), preserving this entry at j+1. D162's Packet U on j,j+1, namely (a,b),(Z,b), emits L_(j+2),H_(j−1),L_(j+1),H_j and gives a unit entry at j+2. Its quotas are a=1,b=2,Z=1. Its two H uses cross.

The common columns [4,k−1] have length k−4=N_Z+(a₀+5)/2+p=(a₀+z)/2+p, since a₀+z=2r+2t+2. In each of the following cases we count exactly this capacity.

### Case A, a₀=1

After the opening place Packet U and p consecutive default (P,P) columns, giving N_Z+3+p common columns. These preserve the unit entry to k. Use H_k at b to fill H_(k−1) and H_(k+1) at Q to fill L_(k+1). The prescribed right reservations finish the L row. Total quotas are a=1, b=1+2+1=4, Z=4+2N_Z+1=z, Q=2+1+1=4 and P=2p. The p pairs each contribute one lower P crossing, so x=p. Upper crossings are N_Z from neutral pairs, two from Packet U and one from the b completion, giving y=N_Z+3=r+t+1.

### Case B, a₀=3

Use swapped P=8. After the opening, start at a unit entry j. The first (b,P) column outputs L_(j+1),L_(j+2) and leaves H_(j−1),H_j pending. This gives a double entry at j+1. Use p−1 pairs (P,P) with the double images of Section 3, maintaining it to ℓ=j+p. Place the remaining triple as follows.

| Column | Hosts of (L,H) | Images of (L,H) |
|---|---|---|
| ℓ | (a,a) | L_(ℓ+2), H_(ℓ−2) |
| ℓ+1 | (P,Z) | H_(ℓ−1), H_(ℓ+1) |
| ℓ+2 | (b,a) | L_(ℓ+3), H_ℓ |

These triple images fill the L positions ℓ+2,ℓ+3 and H positions ℓ−2 through ℓ+1, exactly restoring a unit entry at ℓ+3. The full packet uses a=3,b=2,Z=1,P=2+2(p−1)=2p, and has p+3 columns. With the opening and neutral loops this fills N_Z+p+4 common columns. Close at H_k with b and H_(k+1) with Q. b, Z and Q have the same quotas as in Case A. Lower P crosses at ℓ+1 and on each inserted P pair, so x=1+(p−1)=p. The upper crossings are N_Z from Z pairs, three at a,a,Z in the triple and one at b in the completion, hence y=N_Z+4=r+t+1. For p=1 no P pairs are inserted and this is precisely the original four-column D162 packet. The two cross-column boundaries and all individual destinations are specified by the entry sets.

### Case C, a₀≥5 odd

Use default P=7. After the opening place Packet U and p unit (P,P) columns, then the [D160](ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY.md#4-the-conversion-and-the-unified-allocation-word) conversion (a,b),(a,Q) starting at a unit entry j. Its new L images are j+1,j+2,j+3 and its H image j−1. The result is a double entry at j+2. Complete with N_a=(a₀−5)/2 pairs (a,a) through k−1, and both H_k and H_(k+1) at a. The common L images after the conversion are L_[j+4,k+1]. The H images of all a sources from j+2 through k+1 are H_[j,k−1], including N_a=0. The full length is N_Z+p+5+N_a, exactly k−4. Full quotas are a=1+2+2N_a+2=a₀, b=1+2+1=4, Z=z, Q=2+1+1=4 and P=2p. The p unit P pairs give x=p. The crossing H uses give y=N_Z+2+1+N_a+2=r+t+1, with the terms respectively from neutral loops, U, conversion, double loops and closure.

For all cases the initial opening supplies the first L advance and all pending H indices thereafter are at least 4. In A and B the farthest unreserved L image before the closing H sources is L_k. In C it is L_(k+1). The closing H images lie within [4,k−1], and the two reserved Q cells supply L_(k+2),L_(k+3). This, the counts and the entry partitions prove all bounds and bijections. Empty intervals and p=1 are included. In every case x+y=p+r+t+1=s−K. The three words therefore prove the full T sufficiency and classification without any optimization or finite-state completeness assumption.

## 7. Prefix independence in the exact arrangement and the p=2 controls

Fix a named relative two-section topology, including the actual incidence roles, distinct center indices and their terminal lists, v at the old interface and w at the return. With K fixed, a compatible normalized witness consists of A,B,s, the selected actual exterior subset with its reduced labeling, and an exact assignment of its remaining actual host leaves to the gap coordinates. A≥0, B≥0, A+B+s=2K, A≤K≤A+s and s≥K are necessary within the declared class. The side inequalities are equivalent to the occupied old band edges lying on the stated sides of C. The least old crossing weight is d−1+s, so the output crossing threshold d+K−1 requires s≥K.

For necessity, start from any admitted full labeling in this arrangement. Orient to the minimum polarity. The explicit old placement leaves precisely the three fresh bands in Section 8. Exterior fresh vertices occupy the outside bands and connected exterior edges cross. An edge meeting the old prefix uses its actual vu at the placed v=A. Every crossing exterior difference is n+s plus the difference after subtracting n+s from each upper exterior label. Thus these distinct exterior weights are in [n+s+1,m], and their count A+B fills the band. Removing the shifts gives the exact reduced labeling and spectrum. The gap leaves occupy the middle labels and use each residual weight in [d−1,d+s−2]. Subtract A+c from their labels and d−1 from these weights. The resulting source and image variables obey exactly the host maps of Section 2, independent of n,c,d. Their required crossing relation depends only on k=K−A and K. This extracts an identical normalized feasibility question from any admitted prefix.

For sufficiency take any such normalized witness and any independently supplied prefix with the required n≥2K and S₋₁. Its old band shifts, the upper exterior expansion and gap reconstruction in Section 8 yield the full label and weight bijections. The lifted spectra and the actual w return are exact. Both polarities are related by the specified complement of actual labels and cut. These two directions preserve all selected actual terminal roles and the actual direct-leaf status, so they apply separately to T and E+.

A correspondence between two named copies of the same relative original topology maps ports to their actual ports, corresponding physical centers to physical centers of equal quota, and the indices of each center's actual terminal list to the matching indices at that parent. It sends the unique actual direct leaf to the direct leaf. The normalized equations constrain labels and physical adjacencies but impose no numerical label order by branch index. Thus this relabeling of the witness transfers between the named copies without changing either copy's ordered topology. For the p=2 equal second quotas, map the two positive centers by their order among positive centers and map the direct leaf separately if its declared entry is at a different index. Every incidence and eligible parent is thereby preserved. Within a named target, the labels are always assigned to its own fixed original indices.

For p=2 the nine accepted four/four separators recover symbolically: six ordered originals from the odd pair (1,3) and three from (3,3), with three possible physical positions of quota four in the first section. Their positive E+ assignments follow by the general supplier and their T negatives by parity. Their normalized witness need not have the same numerical gap assignments as the archived witness.

The other three four/four small-odd controls have the first quotas (1,1,4) in its three physical orders. The accepted D161 results for target-004, target-015 and target-070 establish E+ NO and T NO in the declared arrangement on the independently supplied n=74 prefix, with both numerical arms independently exhausted. Here K=11, so n=74 is admitted. The accepted D161 symbolic gates for this frozen stratum preserve all compatible witnesses. The neutral host receives the first four leaves and must be the only first center with that capacity. The first upper source and the exact image-four reservation give the D161 upper-host pins. The accepted grouping of terminal indices retains existence on the named original. Thus an E+ witness on any other admitted prefix at these same parameters would normalize and re-lift to an admitted E+ witness on the corresponding D161 original, contradicting its accepted result. This is finite exhaustive evidence plus symbolic transport. It adds no all-exterior symbolic exclusion for larger p and uses no replay. [Frozen control bindings](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION_001/CUSTODY.json) · [D161 execution](../evidence/runs/d161-exceptional-quota-four-001/MANIFEST.json)

Combining the transported E+ negatives for r=t=0 with E+ supply elsewhere gives the exact p=2 full E+ and separation statements in Section 1. The three both-arm negatives also have the separate T parity proof now given here. The other allowed p values retain the scopes stated in Section 1.

## 8. Reconstruction, partial resources and immutable composition

Choose the smallest original terminal index at a and P for the two E+ exterior terminals. For each host, match the remaining actual indices in increasing order to its supplied increasing source coordinates. For T all actual terminals are matched this way, and its direct leaf has its chosen exterior label. In E+ the direct leaf at w has its actual singleton source. These are independent data derived before using any completed labeling. They preserve both physical sections, their literal center and leaf incidences and the witnessing spine.

The full occupied old label and weight inventories, and their exact fresh complements, are
```
L_old    [A,A+c−1] ⊔ [A+c+s,A+n+s]
L_fresh  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
D_old    [1,d−2] ⊔ [d−1+s,n+s]
D_fresh  [d−1,d+s−2] ⊔ [n+s+1,m].
```
The old lower and upper shifts in oriented coordinates are A and A+s. Old noncrossing weights are unchanged, and old crossing weights gain s. The exterior has the high fresh spectrum with all its edges crossing. The exact gap permutation fills the middle labels and the lower fresh weight range. Thus both full inventories are bijective. Gap crossing weights are [d+K−1,d+s−2] and noncrossing weights [d−1,d+K−2]. Together with the exterior and old ranges the total spectra are [d+K−1,m] and [1,d+K−2]. The actual new spine end w=0, cut C=c+K and m=2(c+K)+2 give precisely S₋₁.

Let S_a,S_b,S_Z be the supplied first-center gap source sets and I their disjoint union. Put J₁=(S_a+1)⊔(S_b+2)⊔S_Z in E+ and J₁=(S_a+2)⊔(S_b+1)⊔S_Z in T. These disjoint unions are guaranteed by the exact image partitions. Let I′ and J₂ be the respective complements in [0,s−1]. Excluding the old v already in L_old, the first and remaining exterior label sets are

| Arrangement | E₁, first labels | E₂, remaining labels |
|---|---|---|
| E+ | {2,3,4,n+s+6,n+s+8} | {0,1,n+s+7,n+s+9} |
| T | {1,2,3,n+s+5} | {0,n+s+6,n+s+7,n+s+8} |

T Case B permutes the last two exterior labels at actual w attachments and leaves the two resource sets intact. In both arrangements the first exterior weights are n+s+[1,A] and the remaining exterior weights n+s+[A+1,A+B]. Thus the exact first-section resources are
```
used labels        L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels   E₂ ⊔ (A+c+I′)
used weights       D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights  (n+s+[A+1,A+B]) ⊔ (d−1+J₂).
```
Lower gap labels in both lists have coordinates below k. The used crossing weights are [d−1+s,n+s]⊔(n+s+[1,A])⊔(d−1+(J₁∩[K,s−1])). Their used noncrossing counterparts are [1,d−2]⊔(d−1+(J₁∩[0,K−1])). The remaining crossing weights are (n+s+[A+1,A+B])⊔(d−1+(J₂∩[K,s−1])), with remaining noncrossing weights d−1+(J₂∩[0,K−1]). At the first boundary u has actual oriented label n+s+A+1. The sole unfinished incidence into the next section is the literal uw with w=0 and weight n+s+A+1, a crossing.

For maximum input polarity orient via G=n−g and complement output about m. The actual cuts are n+1−c and m+1−C. An actual old lower label x corresponds to oriented n−x≥c and is sent to m−(n−x+A+s)=x+B. An actual old upper label receives x+B+s. For minimum polarity retain the lower shift A and upper shift A+s. In E+ the actual lower shifts are 5 and 4, respectively. Complement the partial label lists and keep every weight and crossing flag. In maximum polarity w=m and u=B−1. This relates both genuine actual polarity cases.

In any finite declared composition use only individually admitted D143 strict S₀ blocks, D157 phase changes, D158–D162 blocks within their exact premises, and D163 supplied S₋₁ blocks. At every step the independently provided previous output must have the actual port and label state of the next input, including its exact phase, cut, inventories and n_before≥2K_i. The actual cut-side indicator for old labels is invariant. If C_i is the actual cut at completed boundary i, and Λ_i,Σ_i are sums of subsequent actual lower shifts and gaps, an existing label x ends at x+Λ_i+Σ_i·1(x≥C_i). This follows by induction on the finite sequence. Crossing weights gain Σ_i and other weights retain their values. The first-section partial sets lie in their own block's output alphabet and undergo the same suffix placement. Apply the map to the actual known unfinished endpoints of uw, whose crossing weight gains Σ_i. Complements in the final alphabets give the final remaining inventories. All quota ranges, finite blocks and suffix sums terminate, and immutable emission follows from these predetermined values. This uses the given declared physical sections and does not imply arbitrary decomposition.

The selectable pair identity provides a local quota adjustment at a fixed boundary. Independent exterior supply across broader actual center multiplicities and legal quota partitions remains a distinct bottleneck. [Strategic reassessment](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION_001/STRATEGY.md)
