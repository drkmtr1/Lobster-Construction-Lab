# D156 — Exact odd-first-center D143 classification

Task `LCL-ORDINARY-SPINE-ODD-FIRST-CENTER-PARAMETERIZED-CLASSIFICATION-001`. The proof uses exact integer parameters, excluding booleans. Intervals are inclusive and empty when reversed. The terminal-free arm is T and the arm permitting any exterior is E. A quota half-parameter T below refers to a numerical first-center role.

## 1. Statement and necessary restrictions

Supply an independently constructed ordinary graceful named D134 p=1 prefix with n edges, actual extreme frontier v at the end of its witnessing spine, and the exact designated cut spectrum. In oriented labels G(v)=0, write n=2c+2, d=c+2 and crossing spectrum [d,n] at c. Append the ordered actual sections (2r+1,2t+1) and (2p,2q+1,0) at u,w, with r,t≥0 and p,q≥1. The two fresh vertex counts, including their actual spine vertices, are H₁=2r+2t+5 and H₂=2p+2q+5. Each new vertex contributes one actual parent edge. Write H₁+H₂=2K, K=r+t+p+q+5, m=n+2K and require n≥2K.

**Both D143 arms are feasible exactly when r+t≥1.** The supplier uses the terminal-free exterior throughout this domain. The obstruction at r=t=0 includes every exterior allowed by D143, even if terminals are permitted. The statement concerns the exact two-translation placement and D134 return.

By [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md#3-exact-exterior-and-gap-reduction), the reduced exterior is a gracefully labeled tree on the fresh exterior vertices and v. Its reduced sides are [0,A] and [A+1,A+B]. Every reduced edge crosses. Its labels satisfy v=A,w=0, and the only exterior incidence of v is vu, forcing u=A+1 by the weight-one pair. All actual centers are exterior. The remaining vertices are named leaves in the gap, of size s=2K−A−B≥K. Source i∈[0,s−1] is physically lower for i<k=K−A. Its actual full label is A+c+i and its difference is d+π(i). At reduced lower host j the image is i+A−2−j. At upper index j (reduced label A+j) the image is s+j−i. The gap must give a bijection of [0,s−1], with image at least K exactly when the actual incidence crosses the cut.

Orient the graph bipartition of the appended tree by giving v the lower color. Along the spine u is upper and w lower. The two first centers and the second centers' terminals are lower. The two second centers, their section's direct leaf and the first centers' terminals are upper. Thus the fresh graph-class counts are N_low=2(p+q+2) and N_high=2(r+t+3). These classes agree with the reduced label sides on the connected exterior. Let τ₁,τ₂ count chosen exterior terminals of the first and second sections, and let e∈{0,1} record exterior use of the sole direct leaf. The mandatory fresh exterior vertices in each color number three, so A=3+τ₂ and B=3+e+τ₁.

For clarity derive the count equations of [D153](ORDINARY_SPINE_TWO_SECTION_TOPOLOGICAL_PARITY.md#2-exact-crossing-counts-and-topological-parity) here. Write x for a physically lower gap source hosted at an upper host and y for a physically upper gap source hosted at a lower host. These types partition the s−K gaps whose images are at least K. The counts of lower and upper hosts' gap leaves are k−x+y and (s−k)−y+x, hence B+2y and A+2x by x+y=s−K. A leaf's graph color is opposite its host's, so N_low=2(A+x), N_high=2(B+y). Therefore
```
x=p+q−1−τ₂,    y=r+t−e−τ₁,
0≤τ₂≤p+q−1,   0≤τ₁≤r+t−e,  e∈{0,1}.
```
The selection must also use the declared actual quota at every parent. The aggregate bounds are exactly the nonnegative x,y restrictions, giving A≤p+q+2, B≤r+t+3 and A+B≤K because the two width bounds sum to K. They do not determine an image bijection.

For terminal-free A=B=3, v,u,w and the two sides force first-center reduced labels 1 and 2. Their translations are 0 and −1. The odd quotas of those two centers give an odd contribution from the −1 role, canceled modulo two by the direct leaf at w with displacement +1. From the sum identity of [D144](ORDINARY_SPINE_TWO_SECTION_GAP_ALLOCATION.md), each upper leaf at index j contributes s+j−2i, so modulo two only the odd second quota contributes. Since s=2K−6 is even, the total is congruent to the index of the odd second center. It must be even, since a permutation preserves the coordinate sum. The only available indices are 2 and 3, because u occupies index 1. Hence the odd center Q is at index 2 and the even center P at index 3.

## 2. Terminal-free positive construction

Assume r+t≥1. Choose a from the actual first centers with a positive half-parameter, breaking ties by original index, and let b be the other first center. Their half-parameters are R≥1,T≥0 and R+T=r+t. Keep their original names, physical indices and actual terminal lists. Give v,u,w,a,b,Q,P reduced labels 3,4,0,1,2,5,6. The real edges vu,ub,ua,uw,wQ,wP have differences 1 through 6 in that order. Every reduced edge crosses. All terminals and the direct leaf retain their prescribed parents in the gap. The quotas at w,a,b,Q,P are 1,2R+1,2T+1,2q+1,2p, which sum to s.

Put k=K−3, s=2k and J=s+2=2k+2. In the positive domain K≥8 and s≥K. Use Lⱼ=j and Hⱼ=J−j. Source cells Lⱼ, j∈[0,k−1], are exactly the lower sources and Hⱼ, j∈[3,k+2], are exactly the upper sources [k,2k−1] in reverse. Destination cells Lⱼ, j∈[0,k+2], are exactly [0,K−1], and Hⱼ, j∈[3,k−1], are exactly [K,s−1] in reverse. Each pair of row alphabets partitions [0,s−1] for its own use.

| Actual host | Image of Lⱼ | Image of Hⱼ |
|---|---|---|
| w | Lⱼ₊₁ | Hⱼ₋₁ |
| a | Lⱼ | Hⱼ |
| b | Lⱼ₋₁ | Hⱼ₊₁ |
| Q | Hⱼ | Lⱼ |
| P | Hⱼ₋₁ | Lⱼ₊₁ |

The table follows by substituting the host labels into the actual D143 formulas. An incidence crosses exactly for a lower source at an upper host or an upper source at a lower host. The table sends those uses to row H and the others to row L, provided the destination cell exists. The following assignments verify that legality without treating the two row alphabets as interchangeable.

Reserve L₀ at w, L₁ at b and L₂ at a, giving L₁,L₀,L₂ respectively. Reserve Hₖ,Hₖ₊₁,Hₖ₊₂ at Q, giving Lₖ,Lₖ₊₁,Lₖ₊₂. The remaining source and destination cells are both rows in [3,k−1].

Put h=T+p≥1 and choose h+1 consecutive common columns starting at ℓ=3. The common column count is k−3=R+T+p+q−1=R+q+h−1. The packet fits because R+q≥2, leaving R+q−2 columns. Use the deterministic word c₁=P followed by T letters b and p−1 letters P. In the following display the interval of early H sources is empty at h=1.

| Source | Host |
|---|---|
| L_ℓ | a |
| L_(ℓ+j), 1≤j≤h | cⱼ |
| H_(ℓ+j), 0≤j≤h−2 | c_(j+2) |
| H_(ℓ+h−1) | P |
| H_(ℓ+h) | a |

The leftmost column gets L from its neutral L source and H from c₁=P one column to the right. In every interior column ℓ+j, 1≤j≤h−1, its incoming L source from the right and H source from the left both use c_(j+1). At b the two images occupy L and H respectively, and at P they occupy H and L respectively. The last column gets L from P at the preceding H source and H from its own neutral H source. All destinations exist in the common columns and each cell is reached once. The argument remains exact for a packet of two columns, since then the final two H sources are distinct and there is no interior column.

The L word has T occurrences of b and p of P. Its suffix c₂ through cₕ supplies T occurrences of b and p−1 of P on the early H sources. Adding the final P on H and one neutral use on each row gives packet quotas a=2, b=2T, P=2p, Q=w=0. Give both sources of the first R−1 unused columns to a (identity on its rows), and both sources of the remaining q−1 columns to Q (swap the two rows). These use exactly the unused common images. The full quotas with the reservations are:
```
w: 1,    a: 1+2+2(R−1)=2R+1,    b: 1+2T,
Q: 3+2(q−1)=2q+1,               P: 2p.
```
The actual lower-to-upper count is p from the packet L word and q−1 from the Q swaps, giving x=p+q−1. The upper-to-lower count is T from its b uses, one from the final H at a and R−1 from the neutral pairs, giving y=R+T. These agree with the necessary counts and the host table checks each incidence. The formulas include T=0,R=1,p=1,q=1 together, h=1, either empty remainder, and both actual first-center orders. The role choice changes only the numerical labels of actual centers.

## 3. Exact supply, intermediate state and composition

Place the actual terminals of each named center in increasing available source coordinate and increasing terminal index at that same parent. Use L₀ at the real direct leaf indexed by the zero entry of the second profile. The construction is determined by the declared input, with no completed target labeling or first-section rank assumption used in supply. Let D_old and L_old be the initial consumed weight and label sets after the D143 placement:
```
L_old = [3,c+2] ⊔ [c+s+3,n+s+3]
D_old = [1,d−1] ⊔ [d+s,n+s].
```
The old side shifts are 3 and 3+s, leaving old noncrossing differences unchanged and increasing actual old crossing differences by s. Expand the reduced upper exterior by n+s and leave 0,1,2 fixed. On the six declared exterior edges, including vu, the differences are n+s+[1,6]. They all cross C=c+K: the lower exterior and placed v=3 lie below C, and the upper exterior is above it by the size hypotheses. The gap consumes labels d+1+[0,s−1] and differences d+[0,s−1] through the proved two-row bijection. The exterior and gap are exactly the two old label and difference complements. The resulting labels and actual edge differences each exhaust their full alphabets once. Its actual crossing spectrum is [d+K,m] (crossing gap [d+K,d+s−1], old [d+s,n+s], exterior [n+s+1,m]). Its noncrossing spectrum is [1,d+K−1] (old [1,d−1], gap [d,d+K−1]). The old sides retain membership since C=A+c+k with 0≤k≤s. The actual w has oriented label zero and the output has n'=m, c'=c+K,d'=d+K, giving the exact p=1 return.

For the oriented first boundary, let S_a and S_b be the actual source-coordinate sets of a and b above. Explicitly, S_a contains L₂,L_ℓ,H_(ℓ+h) and the two cells of each all-a column. S_b contains L₁, each L_(ℓ+j) with cⱼ=b, and each H_(ℓ+j) in the early H interval with c_(j+2)=b. Interpret cells as their integer source coordinates. The first terminals' source and destination sets are I=S_a⊔S_b and D=S_a⊔(S_b−1), respectively, by the two actual center formulas and the gap bijection. The first boundary includes u,a,b and their leaves and excludes w and its descendants:
```
used labels       L_old ⊔ {1,2,n+s+4} ⊔ (d+1+I)
remaining labels  {0,n+s+5,n+s+6} ⊔ (d+1+([0,s−1] minus I))
used differences  D_old ⊔ [n+s+1,n+s+3] ⊔ (d+D)
remaining weights [n+s+4,n+s+6] ⊔ (d+([0,s−1] minus D)).
```
The used crossing differences are [d+s,n+s]⊔[n+s+1,n+s+3]⊔(d+(D∩[K,s−1])), and the used noncrossing differences are [1,d−1]⊔(d+(D∩[0,K−1])). All these sets are available from the explicit packet before the second section is emitted. The actual port u has label n+s+4. Its only incidence to the unfinished section is uw, with w at zero and weight n+s+4. Edges uw,wQ,wP and the second-section gap leaves consume the listed remaining weights. H₁ is odd, so the intermediate edge count n+H₁ is odd and the first boundary is interpreted in the declared target alphabet.

For the other actual input polarity orient G=n−g and complement the entire output about m. The cuts become n+1−c and m+1−C. Reversing both sides together preserves membership and every actual difference and crossing status. The returned physical w is now m and the intermediate u is 2. Its used and unused label sets are complemented about m. Absolute weights and both inventories of weights stay as displayed. This conjugation gives minimum-to-minimum and maximum-to-maximum transitions, and also carries any putative maximum-polarity counterexample to the negative proof into the oriented coordinates. For A=B=3 the actual lower shift is 3 in either polarity and the upper shift is 3+s.

The symbolic D134 p=1 initializer, applied under its independent retained seed and named path/section premises, supplies arbitrarily large input sizes in its admitted parity class. The new transition preserves all of D143's named ordinary input contract, including the crossing spectrum and extreme. Thus an arbitrary finite list of admitted blocks composes by induction when n_before≥2K at each step. Repeated use of one admitted block stays admitted because size increases. If the initial size can be chosen, a sufficiently large independently supplied prefix admits any such finite list. This includes the supplied state alone for the empty list.

For immutable labels after boundary i, write C_i for its actual cut, S_i for the sum of future gap widths, and M_i for the number of future blocks. Map an already present label x to x+3M_i+S_i·1(x≥C_i) in the final alphabet. The side indicator is invariant through later blocks. Composing this map across adjacent boundaries therefore gives exactly the same final label on each original named vertex. For the partial first section of block i, use that block's actual return cut and the same map; future weights increase by S_i precisely on its displayed crossing set. The exact remaining palettes in the final alphabet are the complements of these transformed used sets, and the real unfinished connector has the corresponding transformed endpoint labels and difference. Supply each original or fresh label once using its boundary map. The list is finite, its suffix sums take one backwards pass, and finite scans of the word, gap and named host lists emit every incidence once. The construction takes linear indexed-integer operations in the supplied and emitted sizes.

## 4. Complete obstruction at r=t=0

Here the first profile is (1,1), K=p+q+5≥7. The exact count y=r+t−e−τ₁ forces e=τ₁=0 and B=3 for all exteriors. The arithmetic balance of [D147](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md#2-terminal-balance-and-paired-exchange) equates the sum of actual first-center label contributions of first exterior terminals with the sum of actual second-center upper indices minus one for second exterior terminals. Every term is positive when the corresponding terminal exists. Therefore τ₂=0 and A=3. All positive centers and the two spine vertices are exterior, so this analysis covers arm E as well as T; the only other selectable vertices were the terminal leaves and the one direct leaf. For these widths the parity calculation in Section 1 gives Q at upper index 2 and P at 3, independently of which first physical center receives which lower label. The actual u has no direct gap leaf, and the old v is ineligible.

The three lower hosts w,a,b each require one leaf. With k=K−3≥4, sources 0,1,2 are present on the lower side. No upper host at j≥2 can take one: s+j−i≤s−1 requires i≥j+1. Thus they exhaust the three lower-host assignments. Every upper-host image is at least 3 since i≤s−1 and j≥2. The three first images must therefore fill [0,2]. All remaining sources and destinations are [3,s−1]. On this interval the Q map s+2−i is a reflection with exactly the required sum of images. Each use of P instead adds one to that sum. A permutation would require zero such uses, contrary to the actual quota 2p>0. Additional crossing restrictions only narrow the eligible arrows. This contradiction also holds at the minimal K=7 and under complement conjugation. It rules out the exact D143 class and does not decide ordinary gracefulness under other placements.

## 5. Retained control and scope

The Director-accepted [D155](ORDINARY_SPINE_TWO_FIRST_CENTER_PARAMETERIZED_CLASSIFICATION.md) construction uses the same row alphabets and the same proof mechanism for paired incoming arrows on the actual two-first-center tree. Its first quotas are even, so the odd upper center there has index 3, whereas the odd-first parity in this proof forces index 2. The new packet closes at its right boundary with the displaced H-to-L arrow and the neutral H-to-H arrow. Three upper boundary reservations use the index-2 odd center. These are separate quota and boundary checks. D154's stored named originals have even first quotas and are historical custody only. They are not tests of these new targets, and no original or labeling was generated for verification.

The exact classification resolves the selected family completely. It supplies no general ordinary nongracefulness assertion, broader interface closure, or priority claim. [Strategic reassessment](../evidence/validation/LCL_ORDINARY_SPINE_ODD_FIRST_CENTER_PARAMETERIZED_CLASSIFICATION_001/STRATEGY.md)
