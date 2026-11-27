# D211 coordinated four-host ordinary supplier

The exact named original `[[p],[q,a],[b],[t]]` is ordinary graceful for independently selected even integers q≥6, a≥4, b≥2 and independently selected integers p,t≥1. [D209](ORDINARY_SPINE_TWO_SIDED_ORDINARY_SUPPLIER.md#2-unequal-flanks-and-the-large-equal-boundary) gives all p≠t and [D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) gives p=t=1. The construction below supplies every p=t=s≥2 by coordinating terminal labels at four actual centers.

## 1. Original partial tree and its inventory

The four original spine vertices L,x,y,R have labels 0,m,4,m−2. The five centers in original order have labels J=m−1, 3, 2, H=m−4, 5 and prescribed quotas s,q,a,b,s, respectively. Fix the first actual terminal at each flank at labels k and m−5, respectively. Every other named terminal remains unassigned until the allocation is finished. The spine has three edges, centers contribute five attachment edges, and terminal edges number q+a+b+2s, so m=q+a+b+2s+8=2h for an integer h. The partial tree has eleven vertices and ten edges, all on the original.

Use D210's formulas with numerical parameters q₀,a₀,b₀ of sum m−10. Here q₀≥6, a₀≥4 and b₀≥2 are even. These parameters determine only k and the palettes on the actual partial tree. They prescribe no incidences or additional names. Set k=8 for a₀=4. For a₀≥6 put j=(a₀−6)/2, k=10+j and K=m−8−j. In both branches 6≤k≤m−6 and m≥24. The fixed labels are distinct. The actual edges have these differences.

| Edges in original order | Absolute differences |
|---|---|
| Three spine edges | m, m−4, m−6 |
| Five center attachments | m−1, m−3, m−2, m−8, m−7 |
| Two fixed flank terminal edges | m−1−k, m−10 |

The weights other than m−1−k use [m−10,m] with m−9 and m−5 omitted. The additional weight m−1−k is m−9 for a₀=4 or m−11−j for a₀≥6. In the second branch it lies in [1,m−11], as m=q₀+b₀+16+2j. Therefore the ten weights are distinct. The unused labels and weights are exactly

```text
X = {1,m−3} ⊔ ([6,m−6] minus {k})
D = [1,m−11] ⊔ {m−5}                              if a₀=4
D = ([1,m−11] minus {m−1−k}) ⊔ {m−5,m−9}           if a₀≥6.
```

Every interval here is integral and a reversed interval is empty. The cardinality of either residual inventory is m−10=q+a+b+2(s−1), equal to the actual pending terminal count. The base allocation writes S₂,S₃,S_H for the label pools at hosts 2,3,H. The respective groups and the region I for the first reflection transfer are

| Branch | S₂ | S₃ | S_H | I |
|---|---|---|---|---|
| a₀=4 | {1,6,7,m−3} | [9,m−8] | {m−7,m−6} | [9,m−10] |
| a₀≥6 | {1,m−3,m−7} ⊔ [K,m−9] ⊔ [7,k−1] | {6} ⊔ [k+1,K−1] | {m−6,m−8} | [k+1,K−4] |

These are D210's proved palette identities for the displayed fixed skeleton. In particular their label union is X, their three absolute-difference images partition D, and their sizes are a₀,q₀+b₀−2,2. This application uses only the arithmetic identities, since the fixed differences and unused palettes above are identical to those in D210. With ρ(z)=m−1−z, the region I is the exact invariant intersection S₃∩ρ(S₃). Every z∈I satisfies H−ρ(z)=z−3, so a ρ-invariant set T⊆I of size b₀−2 moves from host 3 to host H with its difference set unchanged. The counts after this move are a₀,q₀,b₀ at hosts 2,3,H. All elements of I are in disjoint ρ-pairs because m is even. The construction specifies the joint reservation before that move. [D210 base images and reflection](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md#2-base-allocation-at-the-three-actual-centers)

## 2. Joint reflection on an invariant palette

Let a finite label set E in a terminal allocation be invariant under an integer reflection τ(z)=c−z. For each z∈E let d(z) be its old numerical host, and suppose each τ(d(z)) is the label of an actual eligible host for the intended final allocation. Assign z to the host with label τ(d(τ(z))). The new differences at labels z∈E are

```text
|z−τ(d(τ(z)))| = |τ(z)−d(τ(z))|.
```

The right side runs through exactly the previous differences on E with their multiplicities, as τ permutes E. The label inventory is unchanged. Only the union E needs to be invariant. A pair can have its two labels provisionally held by the same host or by different hosts. This is an operation on label pools with prescribed physical hosts. It gives a way to verify selected moves and does not itself supply eligible pools or guarantee capacities.

Take σ(z)=m+1−z. It exchanges 2 with J and H with 5. Hence an entire σ-pair from host 2 can go to J, and an entire σ-pair from H can go to 5, preserving the two weights in each case. For a pair with z at host 2 and w=σ(z) at H, σ sends z to host 5 and w to J in the pool interpretation. When z≥5 and w≤H,J the old and new differences are related by the actual endpoint formulas

```text
z−5 = H−w
J−w = z−2.
```

The pairs used below have z=7 or 9 and w=m−6 or m−8, so both inequalities give positive differences. Finally z*=h+2 is the midpoint of 5 and J, with z*−5=J−z*=h−3. Once a move allocates it to either of those hosts it can go to the other with no change in the difference inventory. This equality uses the host midpoint, not a fixed point of σ.

## 3. Equal flanks of size two

Put (q₀,a₀,b₀)=(q+2,a,b). These parameters have sum m−10. The interval I has endpoint sum m−1. Its length is q+b−2 if a₀=4, and q+b−4 if a₀≥6. Both lengths are even and at least four; therefore the central pair {h−1,h} lies in I. After withholding this pair there are at least b−2 eligible labels. In the two branches the excess over b−2 is q−2 and q−4, respectively. Choose the first (b−2)/2 other ρ-pairs in increasing order of their smaller labels and take their union T. This includes the empty choice at b=2. The two withheld labels remain at host 3 after the initial transfer.

Move h−1 from host 3 to host 2 and h from host 3 to H. Their old weights are h−4,h−3 and their new weights are h−3,h−4. The evaluation uses h≥12, so h lies below H. Now host 2 still has 7, as a singleton in the a₀=4 formula or in [7,k−1] in the other branch. Host H still has its base label m−6. This σ-pair is disjoint from the just moved labels: the two withheld labels were originally in S₃, disjoint from the two donors' base pools. Apply the split-pair identity and put 7 at host 5 and m−6 at host J. Host 3 loses exactly two labels from its intermediate q+2. Hosts 2 and H each gain one and lose one, retaining counts a and b. Each flank gains one extra label, to go at its actual index 1.

## 4. Every equal flank size at least three

Write s−1=2r+ε with r≥1 and ε∈{0,1}. Put q₀=q, a₀=a+2r and b₀=b+2r+2ε. All are even, a₀≥6, and q₀+a₀+b₀+10=q+a+b+4r+2ε+10=m. Thus only the a₀≥6 base formula is used. Its I has even length q+b+2r+2ε−6, with endpoint sum m−1. Set

```text
d = |I|/2 = r+ε+(q+b−6)/2 ≥ r+ε+1,
I = [h−d,h+d−1].
```

### Reserve the right donor before allocating any flanks

Use U and its union V=U∪ρ(U) as follows.

| Parameters | U | V |
|---|---|---|
| ε=0, r=1 | ∅ | ∅ |
| ε=0, r≥2 | [h+2−r,h+r−1] | [h−r,h+r−1] |
| ε=1, r=1 | {h−1,h+2} | {h−3,h−1,h,h+2} |
| ε=1, r≥2 | [h+1−r,h+r] | [h−r−1,h+r] |

The interval endpoints of U in the general rows sum to m+1; the exceptional pair sums to m+1 too. Thus U is σ-invariant. In the second row ρ(U)=[h−r,h+r−3], which is adjacent to U at r=2 and overlaps it for larger r. In the fourth row ρ(U)=[h−r−1,h+r−2], and these two intervals join. In the exceptional third row ρ(U)={h,h−3}. This proves the displayed unions and their ρ-invariance. The general unions have lengths 2r or 2r+2 and fit in I by its radius d. For ε=1, r=1, d≥3, so the centered six-label interval [h−3,h+2] lies in I and contains V. In all cases |V|≤2r+2ε≤b₀−2, and |V| is even. Since |I|−(b₀−2)=q−4≥2, choose T by adding the first (b₀−2−|V|)/2 pairs of I outside V, in increasing order of smaller label. Invariance makes every orbit outside V a complete pair, so this choice always fits. At b=2 the required number is zero when |V| reaches 2r+2ε; the empty V case still has enough pairs. Perform the D210 transfer T from 3 to H. In particular U is now at host H and remains σ-invariant.

### Allocate both flanks from the reserved pools

1. Move the split σ-pairs {7,m−6} and {9,m−8} by Section 2. Labels 7 and 9 are both in [7,k−1] because k≥10. Their mates are the two distinct base labels at H. They are disjoint from T, which is drawn from S₃ and ends at K−4≤m−12. Therefore the two moves use disjoint labels and do not consume U.
2. At host 2 the additional σ-pair {8,m−7} is present. The σ-images of [10,k−1] are exactly [K,m−9], since m+2−k=K. These two intervals are disjoint, as K−k=q₀+b₀−2>0. The range [10,k−1] has j entries, including the empty case j=0, so the complete displayed menu contains j+1=(a−4)/2+r pairs. They avoid 7 and 9, have no labels in either used split pair, and lie in the unchanged parts of the host-2 base. Choose the first r−1 in increasing order of the smaller label, and put both labels of each at J. The menu has at least r pairs since a≥4.
3. Move U at H to host 5 by the invariant-set identity. Here |U|=2r−2+2ε in all four rows. When ε=1, U contains z*=h+2, including the exceptional pair. Assign that one label to J instead by the equal-difference midpoint identity. All labels of U came from S₃ through T; they are disjoint from the split pairs and from the complete pairs at 2.

The split moves consume two labels from each of 2 and H and supply two to each flank. Thus 2 loses 2+2(r−1)=2r and H loses 2+|U|=2r+2ε. The central counts become a,q,b at hosts 2,3,H, respectively, while J gains 2+2(r−1)+ε=2r+ε=s−1 and 5 gains 2+|U|−ε=2r+ε. No label is moved twice in these final allocations except the equivalent description of the midpoint in step 3, which can be assigned directly to its final host. The moves preserve the entire difference inventory with multiplicity because each acts on a disjoint selected label set and either permutes that set's differences or preserves the single difference.

## 5. Named certificate, source comparison and strategic reassessment

For both s≥2 cases keep the two fixed first flank terminals. Sort each flank's extra labels and assign them to actual indices 1 through s−1. Sort each central pool and give those labels to increasing indices at its prescribed parent. Every unassigned original terminal is assigned exactly once and every label in X is used once. The remaining differences partition D with multiplicity one by the proven moves. Combining the two inventories with the fixed skeleton gives vertex labels [0,m] and actual differences [1,m]. Selecting finite pairs by their smaller endpoints and emitting the ordered lists terminates for every finite input. No intermediate graph or separate graceful central labeling is involved. This certificate has no separating alpha cut, since L at zero and x at m fix the direction across the bipartition, yet the label-2 center is in the class of L and has its original terminal of label 1 in the other class. Label 1 never moves in the construction.

[D105](ORDINARY_43_2_EXTREME_SPINE.md) gives a 13-edge ordinary graceful central supplier with opposite extremes for its separate exact quotas. [D117](ORDINARY_QAR_ALL_PARITY_SUPPLIER.md) gives the same usable port pattern for its parameter domain using a two-host residual reflection and growth at the actual right center. D209 consumes an independently graceful central tree and appends unequal flanks; its all-even unit exclusions apply to particular two-step or translation interfaces. D210 independently sets up the whole-original unit skeleton and transfers between 3 and H. D211 keeps the independent partial-tree arithmetic while sharing a σ-pair between donors at 2 and H and receivers at 5 and J. Its central spine edge xy has weight m−4>m−(2s+4), the central edge count, so the restriction to the actual central component is not a translation or reflection of a graceful labeling of that component.

[R226](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) supplies exact two-host reflected pair and midpoint feasibility for a supplied local palette instance. It applies to the initial ρ-transfer. In a split σ-pair the individual labels each change their weights, and the change at one donor/recipient pair is compensated by the other pair. For example 7 changes from weight 5 to 2 while m−6 changes from 2 to 5. Treating these as independent fixed-palette moves for host pairs (2,5) and (H,J) would miss that exchange. [R232](../references/upstream/mdl/N232_R232_joint_allocation.md#n232-closeout) distributes forced labels, pairs and singletons across independently supplied, disjoint, locally balanced two-host palettes under its singleton-forest and pair-capacity tests. The split σ-pair instead allows weights to exchange between different host pairs within its jointly invariant palette, with explicit supply of that palette here.

[R248](../references/upstream/mdl/N248_component_palette_reflection.md#n248-full-review) uses the same union-invariance and simultaneous host/label reflection identity for selected components of a supplied complete graceful tree. It relocates actual rooted components and can reflect internal labels. The D211 identity operates on unassigned single-terminal label pools and preserves the eventual original incidences by assigning actual names only at the end. It needs a valid partial skeleton and provisional label/difference partition; it does not need an independently graceful source graph. The transferable identity is general under its hypotheses. The reservations, quota equations and four-host layout are specific to this supplier. No historical novelty is claimed.

**Strategic reassessment.** D209 for unequal flanks, D210 for unit flanks and the two equal-flank cases here close all positive flank pairs for every all-even central triple in the stated domain. Repeating a benchmark or preparing a numerical search in that slice would not discharge an open existence obligation. For the wider D117 domain all unequal flanks are already covered. For central triples outside the all-even slice, the equal-flank coverage remains the D209 union and D210's additional unit cases; the complement of those established domains remains open here. Parity constraints in a fixed transfer menu do not rule out other jointly supplied pools or another construction. Broader supplier work would need a new allocation or interface that supplies those unresolved parity regimes or a distinct original family. This reassessment selects no successor. D207's monotone-return question remains unresolved and deferred.

[Frozen originals](../evidence/validation/D211_COORDINATED_FOUR_HOST_SUPPLIER/ORIGINALS.md) · [Prescribed hand arithmetic](../evidence/validation/D211_COORDINATED_FOUR_HOST_SUPPLIER/FIXED_ARITHMETIC.md)

## 6. Separate mathematical review

An independent read-only reviewer inspected the actual proof, original definitions, six hand records and retained primary source passages. The review passed both size-two branches, all four r/ε regimes, the radius and pair counts at b=2 and j=0, the exceptional six-label containment, and every actual quota and disjointness condition. It separately checked the invariant-palette identity, the distinction between the host midpoint and the reflection fixed point, the comparison with R226/R232/R248, and the exact combined scope. The reviewer hand-recomputed 170 actual edge differences and 176 vertex assignments, confirmed both inventories and the deterministic choices in each original, and matched the Director's indexed certificate for control 3. No executable or formal verification was performed.
