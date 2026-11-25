# D157 — Alternating ordinary cut-spectrum interface

Task `LCL-ORDINARY-SPINE-ALTERNATING-EXCEPTIONAL-SPECTRUM-001`. All structural parameters and labels are exact integers, excluding booleans. Intervals include their endpoints and reversed intervals are empty. The symbol ⊔ denotes disjoint union.

## 1. Interface and exact inventory rule

Supply an ordinary graceful named prefix with n=2c+2 edges, its actual witnessing spine ending at an extreme vertex v, and the prescribed cut spectrum. Orient its label G(v) to zero by complementation when necessary. Write d=c+2. For ε∈{0,−1} let S_ε mean that the **actual** differences of the edges crossing cut c are [d+ε,n], with noncrossing differences [1,d+ε−1]. A vertex whose label equals the cut belongs to its upper side. S₀ is the D134 p=1 state. S₋₁ has one additional crossing weight, d−1, in the current normalized alphabet. State includes the actual graph, spine, frontier, full labeling, cut and exact inventories.

Append two declared actual spine sections at u,w with 2K fresh vertices and edges and n≥2K. Write m=n+2K. Take A,B,s nonnegative with A+B+s=2K. In oriented coordinates old label x maps to A+x below c, and A+s+x at or above c. Require output cut C=c+K and w=0. This old map is increasing and injective with used and unused palettes
```
old labels   [A,A+c−1] ⊔ [A+c+s,A+n+s]
fresh labels [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m].
```
The nonempty old bands nearest the cut have endpoints A+c−1 and A+c+s. Thus old membership holds exactly when A≤K≤A+s, or equivalently A≤K and B≤K. These conditions put the two fresh exterior bands on their respective sides. The input has a nonempty lower side because it has actual crossing edges. It also has a nonempty upper side. The size and spectrum hypotheses give d+ε≤n. Subtracting actual endpoints, a noncrossing old edge keeps its difference, and a crossing old edge gains s. Both weight palettes are exact:
```
old weights   [1,d+ε−1] ⊔ [d+ε+s,n+s]
fresh weights [d+ε,d+ε+s−1] ⊔ [n+s+1,m].
```
For output S_ε′ let δ=ε′−ε and λ=K+δ. The first required crossing weight at C is d+K+ε′. The smallest actual old crossing weight after shifting is d+ε+s, so s≥λ is necessary and sufficient for all shifted old crossings to meet the output threshold. Since K≥1 and δ≥−1, λ≥0 and all old noncrossing weights lie below the output threshold.

Use the following sufficient construction under these conditions. Supply a connected reduced exterior tree containing v and the fresh exterior vertices, with exactly the original edges retained there. Its labels are [0,A+B], with v=A and w=0 and every edge crossing between [0,A] and [A+1,A+B]. Its actual reduced edge differences must be [1,A+B]. All actual positive centers and both new spine vertices are exterior, and the s remaining vertices are actual leaves of exterior hosts. Add n+s to the upper reduced labels. The actual connector at v agrees with its old placed label A. Expanded exterior incidences all cross the actual cut and take n+s+[1,A+B], which is entirely above the crossing threshold. This construction is sufficient within the declared exterior and gap arrangement. It makes no necessity claim for that arrangement on arbitrary relaxed placements.

A gap leaf at coordinate i∈[0,s−1] has label A+c+i and is physically lower exactly for i<k=K−A. Its weight is d+ε+π(i), where subtraction from its actual host gives
```
lower reduced host j:                   π(i)=i+A−2−ε−j
upper host at reduced label A+b:        π(i)=s+b−ε−i.
```
For the lower formula the leaf label exceeds its lower host. For the upper formula the expanded host exceeds the leaf label and n−c=d. Each actual gap leaf must receive a distinct coordinate on [0,s−1], respecting its own physical host and index. The images must permute [0,s−1] and satisfy π(i)≥λ exactly for opposite physical sides. The first condition fills the exact low fresh weight palette. The second gives noncrossing gap weights [d+ε,d+K+ε′−1] and crossing gap weights [d+K+ε′,d+ε+s−1], with the stated empty-interval conventions. All old weights and expanded exterior weights then join these to give the full spectra [1,d+K+ε′−1] and [d+K+ε′,m]. Both full alphabets are bijections. The enlarged actual named graph is a tree by attaching every fresh vertex at its original parent. Its continued spine witnesses the lobster property. With m=2(c+K)+2, w=0 and cut C, this gives exactly S_ε′.

## 2. Graph colors and crossing balance

Give v the lower graph color on the original appended tree. Then u is upper and w lower. For section i write C_i for the number of positive centers, D_i for its direct leaves, and T_i for its actual terminal leaves. At u the actual centers and direct leaves are lower and its terminals upper. At w the colors reverse. The fresh graph counts are therefore
```
N_low  = 1 + C_1 + D_1 + T_2
N_high = 1 + C_2 + D_2 + T_1.
```
The connected crossing exterior's label sides equal those graph colors by the root v. Each gap leaf has the graph color opposite its actual parent's color.

Let x count lower gap sources at upper hosts and y upper gap sources at lower hosts. These are exactly the crossing gap incidences, and the image rule gives x+y=s−K−δ. Write L and U for the number of gap leaves at lower and upper hosts. The two source counts are k and s−k. Hence
```
L = k−x+y = B+δ+2y,        U = s−k−y+x = A+δ+2x,
N_low  = A+U = 2(A+x)+δ,   N_high = B+L = 2(B+y)+δ.
```
Here x∈[0,k] and y∈[0,s−k]. These are necessary aggregate physical counts under the declared role arrangement, with the remaining individual quotas and image feasibility still to prove. In particular fixed ε forces both graph classes even, as in strict D153. A phase change has δ=±1 and admits odd counts at this aggregate level. The cyclic theorem below checks both changes on the named profiles. Each S₋₁ boundary differs from the strict spectrum at that boundary by exactly the extra crossing weight d−1 in its then-current alphabet. The subsequent S₀ boundary has exactly the strict spectrum. No extra band accumulates, and no already placed actual edge changes its crossing status.

## 3. Domain and common reduced exterior

Use the ordered actual profiles (2r+1,2t) and (2p,4,0) with r≥2, t≥1, p≥t. The first adds 2r+2t+4 vertices and the second 2p+8. Thus K=r+t+p+6≥10 and n≥2K is the size condition. Their fresh graph classes have sizes 2p+7 and 2r+2t+5. Both are odd. The [D153 theorem](ORDINARY_SPINE_TWO_SECTION_TOPOLOGICAL_PARITY.md#3-the-selected-two-first-center-family) gives the strict D143 negative control on precisely these named profiles. The relaxed transition changes the gap crossing count premise, while keeping the original incidences.

Choose A=3,B=4,s=2K−7,k=K−3, so s=2k−1. Both membership inequalities hold and s≥K+1, reaching all the required thresholds. Give v,u,w reduced labels 3,4,0 and numerical first roles a,b labels 1,2. The original second centers P,Q of quotas 2p,4 have reduced labels 5,6. The original direct leaf of w has label 7. All actual terminals remain in the gap, and there is no direct gap leaf. The actual edges vu,ub,ua,uw,wP,wQ and the edge from w to its direct leaf have reduced weights 1,2,3,4,5,6,7, all crossing. Taking first roles by their numerical assignment on each leg changes no physical branch index or parent.

## 4. Outbound S₀ to S₋₁

Here ε=0, δ=−1, and λ=K−1. Give the actual odd first center role a (quota 2r+1) and the even first center role b (quota 2t). Put J=s+2=2k+1 and identify Lⱼ=j, Hⱼ=J−j. The L sources are columns [0,k−1] and the H sources columns [3,k+1], giving the actual upper interval [k,s−1] in reverse. Destinations L use [0,k+1], the values below λ, and H use [3,k−1], the values [λ,s−1] in reverse. Both source and destination row alphabets are bijective representations of [0,s−1] in their respective roles. The host formulas of Section 1 give these arrows whenever the destination cell exists:

| Host | Lⱼ image | Hⱼ image |
|---|---|---|
| a | Lⱼ | Hⱼ |
| b | Lⱼ₋₁ | Hⱼ₊₁ |
| P | Hⱼ | Lⱼ |
| Q | Hⱼ₋₁ | Lⱼ₊₁ |

For every row arrow its H destination occurs exactly when a lower source uses an upper host or an upper source uses a lower host. L destinations are precisely noncrossing. Domain legality is checked by the following partition.

Reserve L₀,L₁,L₂ at a (same L images), and Hₖ,Hₖ₊₁ at P (images Lₖ,Lₖ₊₁). The remaining source and image cells are both rows of [3,k−1]. There are k−3=r+t+p common columns. Put h=t+2, take h+1 columns starting at ℓ=3, and choose c₁=Q followed by t letters b and one Q. This fits because the leftover count r+p−3 is nonnegative. Use the assignments
```
L_ℓ                       a
L_(ℓ+j), 1≤j≤h            c_j
H_(ℓ+j), 0≤j≤h−2          c_(j+2)
H_(ℓ+h−1), H_(ℓ+h)        Q, a respectively.
```
At the first column the neutral L source gives its L image and c₁=Q gives H from the next L source. For an interior column ℓ+j with 1≤j≤h−1, the L source from its right and H source from its left use the same letter c_(j+1). If it is b they supply L and H respectively. If it is Q they supply H and L respectively. The final column gets L from the preceding H source at Q and H from its own neutral H source. Thus the arrows occupy exactly the packet cells with no collision. Its lower word supplies t uses of b and two of Q. The early H word supplies t uses of b and one of Q. The last two H sources add one Q and one a, and the first L source gives one a. Its complete quotas are a=2, b=2t and Q=4.

Allocate both sources of the first r−2 remaining columns to a, and both sources of the last p−1 to P. These respectively fix and swap the rows in their own column. They consume exactly the remaining cells. Including reservations the quotas are a=3+2+2(r−2)=2r+1, b=2t, Q=4 and P=2+2(p−1)=2p. The crossings are x=2+(p−1)=p+1 from the Q lower word and P pairs, and y=t+1+(r−2)=r+t−1 from the upper b word, the last a and a pairs. All prescribed image cells exist in the reserved or common intervals, and the argument includes empty remainders at r=2 or p=1. Section 1 gives the exact S₋₁ output.

## 5. Return S₋₁ to S₀

Here ε=−1, δ=1, and λ=K+1. Give the actual even first center role a (quota 2t) and odd first center role b (quota 2r+1). Keep P,Q and the actual direct leaf in their common exterior roles. Put J=s+3=2k+2 and again use Lⱼ=j,Hⱼ=J−j. L sources use columns [0,k−1]; H sources use [4,k+2], representing [k,s−1] in reverse. L destinations use [0,k+3], exactly the values below λ. H destinations use [4,k−2], representing [λ,s−1] in reverse. These give both full alphabets. Direct substitution in Section 1 yields the arrows

| Host | Lⱼ image | Hⱼ image |
|---|---|---|
| a | Lⱼ₊₁ | Hⱼ₋₁ |
| b | Lⱼ | Hⱼ |
| P | Hⱼ | Lⱼ |
| Q | Hⱼ₋₁ | Lⱼ₊₁ |

As before H images occur exactly for opposite-side source and host, when the listed image cell exists.

Give L₀,L₁,L₂,L₃,Lₖ₋₁ to b, fixing those five L images. Give Hₖ₋₁,Hₖ,Hₖ₊₁,Hₖ₊₂ to Q, supplying Lₖ through Lₖ₊₃ and using all Q leaves. The reserved sets are disjoint since k≥7. Both rows in the common columns [4,k−2] remain. Their number is k−5=r+t+p−2. Starting at column 4, use the first 2t columns in consecutive two-column packets. In a packet on j,j+1 the four arrows are
```
L_j --a--> L_(j+1) --P--> H_(j+1) --a--> H_j --P--> L_j.
```
They stay in those two actual columns and exhaust all four cells. Each packet uses two a and two P. Next place both cells of p−t columns at P, exchanging their rows. Place both cells of the last r−2 columns at b, fixing their rows. The capacity identity 2t+(p−t)+(r−2)=r+t+p−2 proves exact coverage and the domains make every count nonnegative. Totals are a=2t, b=5+2(r−2)=2r+1, P=2t+2(p−t)=2p and Q=4. Counts by actual crossing type are x=t+(p−t)=p and y=t+(r−2)=r+t−2. The assignments include r=2,t=1,p=t together, when the common interval has exactly one packet and no pair remainder. Every arrow stays within its reserved or common cells, and Section 1 yields exactly S₀.

## 6. Named reconstruction, exact partial inventories and polarity

In each leg choose the declared roles at the two actual first indices. For each physical host, list its assigned integer source coordinates in increasing order and label its actual terminal indices in increasing order at that parent. The exact quota counts make these assignments bijections at every host. The only direct leaf is still exactly the original zero entry at w and is given the expanded exterior label n+s+7. Thus the construction supplies independently the original indices and incidences without solving or changing a completed target.

The old inventories are those of Section 1 for A=3,B=4. Together the complete gap permutation and expanded exterior supply their exact complements, with the corresponding full spectra proved there. In particular the outbound noncrossing spectrum is [1,d+K−2], and its crossing spectrum is [d+K−1,m]. The return noncrossing spectrum is [1,d+K−1] and its crossing spectrum [d+K,m].

At the first-section boundary let S_a and S_b be the actual integer source-coordinate sets prescribed at the two first roles. They are read directly from each leg's reservations, word or four-cycles, and pair remainder, before any labels of the second section are written. Put I=S_a⊔S_b and
```
outbound J_1 = S_a ⊔ (S_b−1)
return   J_1 = (S_a+1) ⊔ S_b.
```
These are the first gap sources and images by the relevant lower-host formulas. Their unions are disjoint by the gap bijection. The first exterior labels are {1,2,n+s+4}, and its actual edges vu,ub,ua give n+s+[1,3]. With L_old and D_old from Section 1 the exact partial resources are
```
used labels       L_old ⊔ {1,2,n+s+4} ⊔ (A+c+I)
remaining labels  {0,n+s+5,n+s+6,n+s+7} ⊔ (A+c+([0,s−1] minus I))
used differences  D_old ⊔ (n+s+[1,3]) ⊔ (d+ε+J_1)
remaining weights (n+s+[4,7]) ⊔ (d+ε+([0,s−1] minus J_1)).
```
The used crossing spectrum is [d+ε+s,n+s]⊔(n+s+[1,3])⊔(d+ε+(J_1∩[λ,s−1])). Its used noncrossing counterpart is [1,d+ε−1]⊔(d+ε+(J_1∩[0,λ−1])). The remaining gap carries the same two statuses by the complementary J_1 image sets. Its remaining exterior weights all cross. The physical frontier is u at n+s+4 and the actual unfinished connector for this block is uw with w at zero and weight n+s+4. The second section consumes that weight, n+s+[5,7] on its exterior attachments and the exact complementary gap images. These are independently supplied partial sets in the target alphabet without an imposed ordinary half-spectrum on the partial boundary.

For an actual maximum-frontier input, write its actual label x as n−G. Its actual cut is n+1−c, and complement the output about m so the new actual cut is m+1−C. If x is below the actual input cut then G≥c and the final actual old label is m−(A+s+G)=x+B. If x is at or above the actual cut then G<c and its new label is x+B+s, using A+B+s=2K. The cuts exchange sides in both prefix and output, so membership is preserved and all absolute differences and crossing statuses are unchanged. The minimum-frontier actual lower shift is A=3 and the maximum-frontier actual lower shift B=4. The respective upper shift adds s. The actual frontier w is zero or m according to the input polarity, and the actual u is n+s+4 or 3, respectively. In the maximum case complement both first-boundary label sets about m, retaining both weight inventories and the actual weight of uw.

## 7. Independent supply, cycle closure and immutable labels

Use the [D134 p=1 symbolic initializer](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md#independent-symbolic-initialization-for-every-fixed-odd-h) under its exact independent seed, named path, branching and parity premises to supply S₀ of arbitrarily large admissible sizes. Its sections are actual declared parts of every admitted initialized original. The outbound leg supplies S₋₁ independently on its own actual sections. Applied to this state, the return leg supplies S₀ on the next distinct actual sections. The input to either leg retains the complete graph and exact inventories, so the proof requires no projected or deleted section. Both legs are valid for independently prescribed triples in the stated domain, subject to the size bound at the actual preceding boundary. A finite alternating list beginning at S₀ closes after every pair, and an odd-length prefix supplies S₋₁. Repetition of the same admitted block profile is permitted with distinct actual names each time, since the size increases. For any fixed finite declared list, an independently supplied sufficiently large initial state can meet all bounds when the starting size is selectable.

Let C_i be the actual cut at completed boundary i, with actual label alphabet [0,n_i]. Set L_i to the sum of the actual lower shifts of subsequent blocks and S_i to the sum of their gap widths. Phase and polarity are known from the declared sequence. At boundary i the final image is
```
Ψ_i(x)=x+L_i+S_i·1(x≥C_i).
```
All later placements preserve membership, so these terms are exactly the accumulated shifts on each original named vertex. The maps compose with each next block's old embedding. At a completed boundary the final used labels are Ψ_i([0,n_i]), the union of the two translated cut intervals. The final used differences are [1,d_i+ε_i−1]⊔[d_i+ε_i+S_i,n_i+S_i], writing d_i=c_i+2 in that boundary's oriented state. Remaining palettes are exact complements in the final alphabets. At the partial first-section boundary of block i, apply Ψ_i to its supplied used labels and add S_i only to its displayed used crossing weights. The unfinished connector, whose two endpoint labels are independently supplied for block i, is transformed by Ψ_i and its difference increases by S_i since it crosses C_i. Computing the complementary reserves after this transformation yields both exact final-alphabet resources at the partial boundary. Thus the initializer and each subsequent original vertex can be emitted once with its final label. A finite backward pass forms the shift sums, and finite scans of the explicit words, columns and named indices emit every vertex and incidence. The arithmetic operation count is linear in the declared finite graph size.

This proves a repeatable two-block phase cycle in the declared domain. The strict D143 and D153 scopes are preserved, as are the ordinary deficit transition D131 and the alpha module compositions of R241 under their own assumptions. No unrestricted lobster theorem, necessity reduction for arbitrary relaxed placements, or general phase-compatible profile classification is claimed.
