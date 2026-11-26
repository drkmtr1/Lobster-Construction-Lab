# D169 — Exceptional exterior supply by second-center role exchange

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-SECOND-ROLE-EXCHANGE-001`. All structural parameters and labels are exact integers, with booleans excluded. Intervals are inclusive, reversed intervals are empty, and ⊔ denotes disjoint union. Claims concern the declared D157 connected crossing-exterior, leaf-only gap arrangement and its exact exceptional return.

## 1. Original topology and exact domain

Independently supply a named ordinary graceful [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) S₋₁ prefix with its actual witnessing spine and extreme frontier v. Orient its labeling G so G(v)=0. Write n=2c+2 and d=c+2, with the upper side starting at c. The crossing weights are [d−1,n] and the complementary weights are [1,d−2]. Append the actual consecutive spine sections u,w. The [D163](ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION.md) family has first terminal quotas (4,2r+1,2t+1) in any physical order. The second section has positive terminal quotas 2p,4 in either order and the sole actual direct leaf at its declared index. Here r,t≥0 and p≥1. Use `K=r+t+p+9`, `m=n+2K` and `n≥2K`.

For the selected open corner r=t=0 the first section adds 10 vertices, namely u, three centers and six terminals. The second adds 2p+8, namely w, two centers, the direct leaf and 2p+4 terminals. Each new vertex introduces one edge at its actual parent. Therefore K=p+9, and there are 2p+18 fresh vertices and edges. In the original bipartition oriented from v in the lower class, w, the three first centers and the second terminals are lower. The first terminals, u, the second centers and the direct leaf are upper. The fresh class counts are `N_low=2p+8` and `N_high=10`.

## 2. Independently supplied reduced exterior

Set A=5, B=4 and use the reduced coordinates below. Give role Z to the quota-four first center, a to the earlier indexed actual quota-one center and b to the other one. Give Q to the actual second center with quota 2p and P to the actual second center with quota four. For p≥3 these second quotas differ. The choice depends only on the input named roles and preserves both physical second orders and the original direct-leaf index. Select the first terminal in the actual terminal list of a for reduced label 8 and the first terminal at P for label 1.

| Actual role | v | u | w | b | a | Z | Q | P | First terminal at a | First terminal at P |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Reduced label | 5 | 6 | 0 | 2 | 3 | 4 | 7 | 9 | 8 | 1 |

The labels fill [0,9]. The actual edge list with its differences is

| Edge | vu | uZ | ua | ub | a to its selected terminal | uw | wQ | P to its selected terminal | wP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Reduced difference | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |

Every edge crosses between [0,5] and [6,9]. The actual spine and center attachments connect all the parents, and the selected exterior terminals attach to their own parents. Thus this is a connected named exterior with the exact reduced spectrum. The sole direct leaf at w stays in the gap. The remaining gap quotas at (b,a,Z,Q,P,w) are (1,0,4,2p,3,1). In particular the center a and its exterior terminal remain present.

## 3. Folded alphabets and exact construction

Put `k=K−5=p+4≥7`, `s=2K−9=2k+1`, and `J=s+3=2k+4`. The size premises give `s≥K` and `5≤K≤5+s`. Place an old oriented label by adding 5 below c, and 5+s at or above c. Expand each upper reduced exterior label by n+s. A gap leaf at source i has label 5+c+i. At a lower reduced host j₀ its label exceeds the host, so the difference is `5+c+i−j₀=d−1+(i+4−j₀)`. At an upper reduced host 5+b₀ its label is below the expanded host, so the difference is `n+s+5+b₀−(5+c+i)=d−1+(s+b₀+1−i)`. Thus these formulas give the normalized image π(i) of the actual edge.

The cut is C=c+K, so the gap source is physically lower exactly for i<k. A gap image is required to cross exactly for π(i)≥K. Write L_j=j and H_j=J−j. Folding the two separate alphabets by their respective thresholds gives the following intervals.

| Alphabet | L columns | H columns |
| --- | --- | --- |
| Sources | [0,k−1] | [4,k+4] |
| Images | [0,k+4] | [4,k−1] |

Indeed the H source indices go from J−(s−1)=4 to J−k=k+4 and H image indices end at J−K=k−1. L images are precisely [0,K−1]. The two rows in each alphabet partition [0,s−1]. The maps just derived give

| Actual parent | L_j maps to | H_j maps to |
| --- | --- | --- |
| b | L_(j+2) | H_(j−2) |
| a, zero residual capacity | L_(j+1) | H_(j−1) |
| Z | L_j | H_j |
| w | L_(j+4) | H_(j−4) |
| Q | H_j | L_j |
| P | H_(j−2) | L_(j+2) |

Each lower host keeps the row. It crosses on an H source and is noncrossing on an L source. Each upper host exchanges rows, crossing on L and remaining noncrossing on H. Therefore every displayed arrow with existing cells and actual host capacity obeys the crossing predicate.

Reserve L_0 through L_3 at Z with identical images, L_4 at b with image L_6, and H_10 at w with image H_6. The reserved L source and image sets have distinct cells and the H reservation cannot collide with either L set. At k=7 the largest L source index and H destination index are both 6, and the H source row reaches column 11. Thus all reservations exist already at the first admitted size.

The residual L sources have columns [4,k−1]∖{4} and H images have columns [4,k−1]∖{6}. Assign L_6 at P to H_4 and use Q at every other residual L source. Their images are H_4 and H_[5,k−1] with H_6 removed, exactly the residual destination set. The residual H sources have columns [4,k+4]∖{10} and L images have columns [4,k+4]∖{6}. Assign H_6 and H_8 at P to L_8 and L_10. Use Q on [4,k+4]∖{6,8,10}, giving its identical L indices. These images fill the residual L set exactly and do not use the reserved L_6. At k=7 the L path uses column 6 and the entire H path from column 6 to column 10 has legal endpoints. Larger k retains these paths and appends identity assignments at Q. These two repairs are the displacement-two residue paths of [D168](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md), with the assignments here explicitly proved by the image-set partitions.

Exactly one L source and two H sources use P, so its gap quota is three. The residual L source count is k−5 and one is at P, giving k−6 at Q. The residual H source count is k and two are at P, giving k−2 at Q. Their sum at Q is 2k−8=2p. The reservations exhaust Z, b and the direct leaf of w. No assignment uses the exhausted center a.

The lower-to-upper crossing count is x=k−5=p−1 and the upper-to-lower count is y=1, with `x+y=k−4=p=s−K`. The actual direct leaf at w uses coordinate `i=J−10=2k−6` and image `π(i)=J−6=2k−2`. Since k≥7, i≥k and π(i)≥k+5=K. At k=7 this image equals the first crossing image K. As a further check the counts give the D157 identities `2(A+x)=2p+8` and `2(B+y)=10`.

For p=2, k=6 and H_6 is absent from the crossing image row [4,5]. This identifies the failure of the displayed role-exchanged word at that endpoint. The full p=2 negative has the distinct basis in §5.

## 4. Exact actual lifting, intermediate inventories and return

Give the two selected exterior terminals their already specified reduced labels, expanded at the upper one. Assign each parent's remaining terminal indices in their original order to that parent's increasing source coordinates. The unique w assignment gives the actual direct leaf its coordinate without changing its direct-leaf role. This constructs the named labeling and exact original edges independently of any completed whole-target labeling.

The old band placement and its complementary vertex palettes are

```text
L_old    = [5,c+4] ⊔ [c+s+5,n+s+5]
L_fresh  = [0,4] ⊔ [c+5,c+s+4] ⊔ [n+s+6,m]
D_old    = [1,d−2] ⊔ [d−1+s,n+s]
D_fresh  = [d−1,d+s−2] ⊔ [n+s+1,m].
```

For the labels, the old intervals are the shifted exact input cut sides and the fresh intervals are their exact complement in [0,m]. The exterior accounts for the two outside fresh bands, with v=5 already in the old set. The source bijection fills the middle band. For weights, the shift leaves each old noncrossing difference unchanged and adds s at each old crossing edge. Therefore the old weights have exactly the displayed bands. Each exterior edge crosses and gains n+s, so the exterior uses [n+s+1,m]. The remaining fresh weights are exactly [d−1,d+s−2], all used by the gap image bijection. This proves the actual vertex-label and edge-difference bijections.

The old lower and upper label bands remain on the respective sides of C because `5≤K≤5+s`. Exterior labels remain on their reduced sides. The crossing gap weights are [d+K−1,d+s−2] and the other gap weights are [d−1,d+K−2], by the exact image thresholds. The old crossing band begins at d−1+s≥d+K−1. Consequently the full crossing and noncrossing spectra are [d+K−1,m] and [1,d+K−2]. The extended witnessing spine ends at w=0, with m=2C+2, so the actual output is S₋₁.

In the first section the only gap sources are the four Z leaves and the b leaf. Thus `I=[0,4]` and `J₁={0,1,2,3,6}`, with complements `I′=[5,s−1]` and `J₂={4,5}⊔[7,s−1]`. The fresh first exterior labels are `E₁={2,3,4,n+s+6,n+s+8}`. The remaining exterior labels are `E₂={0,1,n+s+7,n+s+9}`. The first and remaining exterior differences are n+s+[1,5] and n+s+[6,9] by the actual edges in §2. In particular the connector uw remains in the second set. The partial inventories are

```text
Used labels           L_old ⊔ E₁ ⊔ (5+c+I)
Remaining labels      E₂ ⊔ (5+c+I′)
Used differences      D_old ⊔ (n+s+[1,5]) ⊔ (d−1+J₁)
Remaining differences (n+s+[6,9]) ⊔ (d−1+J₂).
```

All first gap labels lie below C and all first gap images are below K. The low portion of E₁ is {2,3,4} and that of E₂ is {0,1}, with the other labels in each exterior set upper. Split I′ into [5,k−1] below C and [k,s−1] at or above it. Thus lower and upper used and remaining label sets are exactly the corresponding listed parts, with the two old intervals already on their own sides. First used crossing differences comprise [d−1+s,n+s] and n+s+[1,5]. The used noncrossing differences are [1,d−2] and d−1+J₁. The remaining crossing differences are n+s+[6,9] and d−1+[K,s−1]. The remaining noncrossing ones are `d−1+({4,5}⊔[7,K−1])`. The direct leaf is in the remaining upper labels and crossing weights. The actual partial frontier u has label n+s+6. The literal unfinished edge uw has supplied endpoints n+s+6 and 0, so its reserved crossing difference is n+s+6.

For maximum input polarity orient G=n−g and complement the output about m. The actual input and output cuts are n+1−c and m+1−C, using equality on the upper side. At an old actual lower label x the orientation lies in the old upper band, so the complemented new label is `m−(n−x+5+s)=x+4`. An old actual upper label similarly moves to x+4+s. Minimum polarity has respective shifts 5 and 5+s. Complement every partial label set for maximum polarity, interchanging its sides, and retain all absolute weights and crossing classes. The unfinished connector endpoints are then u=3 and w=m since m=n+s+9, and its weight remains n+s+6.

For an admitted finite sequence require each block's actual named port, exact phase, cut and input resource premises, including the relevant size bound. Inductively each supplier's exact return admits the next block if those premises hold. Through successive membership-preserving translations, a label x at a completed boundary with actual cut C_i finishes at `x+Λ_i+Σ_i·1(x≥C_i)`, where Λ_i sums subsequent actual lower shifts and Σ_i sums their subsequent gap widths. Each crossing weight increases by Σ_i and each noncrossing one stays fixed. Apply the same transformations to the placed first-section resources and known endpoints in the current block's output alphabet. The unfinished uw retains its crossing reserve after adding Σ_i. Exact final complements give both remaining palettes, including the actual unfinished edge until its declared stage. This realizes immutable emitted labels. The finite indexed leaf assignments and finite block sequence terminate. No arbitrary topology decomposition is inferred.

## 5. Controls and exact full D163 classification

[D162](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION.md) supplies the positive p=1 case for all r,t, including r=t=0. [D163](ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION.md) proves feasibility on its original ordered fixed E+ exterior with Q quota four and P quota 2p exactly when p=1 or r+t≥1. Its obstruction when r=t=0 and p≥2 forces all four available Q incidences at upper sources. It then lacks sufficient lower P placements for the required x=p−1. Here Q has 2p gap leaves, and P has three, so the fixed-quota exhaustion inference has different premises. The role exchange preserves the reduced coordinates and edges of the template, with the actual different second parent now carrying each numeric role. It also preserves all original named incidences, including the actual terminal chosen at the new P. Its successful range needs no replay or enumeration.

At p=2,r=t=0 retain the accepted D161 finite E+ exhaustion for target-004, target-015 and target-070, respectively with first profiles (1,1,4), (1,4,1), (4,1,1), each with second profile (4,4,0). Their original digests and E+ records are

| Frozen target | Original graph digest | E+ record SHA-256 |
| --- | --- | --- |
| target-004 | `49143ae3c58e2c784b153f5008d056d78ded9695a1ae71f19b2d3c0d10838563` | `a58dc3015ed943b89a426fbc62eee9bda776ef048b6020f9c103581ee987cfe9` |
| target-015 | `fac9636b9a211deb5ab31886c6f41290839d6b62a5b47ee77997d55f31ab1dd6` | `b96a2d5a009913159d0d21e19e63af330e9f027732da738079915b0c04bacb73` |
| target-070 | `374df7928a928813c2fb07057cb93b032cc45c6432a472e07e983673d4d38ebb` | `68470da9a0c724192c4cbc82f9026e5441f3e0c698eab3d4dcb06c307e026ba7` |

The archived E+ and T records have independent exhaustion audits and are bound to their actual original and pair records. D163 transports the E+ exclusion within the declared arrangement by extracting a normalized putative witness, identifying corresponding names and actual parent lists of equal quota and lifting it to the retained admitted prefix. The argument preserves the direct-leaf role, either order of equal second quotas, the exceptional phase and actual polarity by complementation. A putative E+ witness at any admitted prefix would give a witness on the applicable frozen original, contradicting its accepted E+ exhaustion. The full T negatives have the separate symbolic proof in D163. [D163 transport and controls](ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION.md#7-prefix-independence-in-the-exact-arrangement-and-the-p2-controls) · [D161 reconciliation](../evidence/runs/d161-exceptional-quota-four-001/RECONCILIATION.json)

Combining the p=1 result, D163's r+t≥1 suppliers, the accepted transported corner exclusion and the present symbolic p≥3 supplier yields the exact classification in the declared arrangement:

| Class | Feasible exactly when |
| --- | --- |
| E+ | p≠2 or r+t≥1 |
| T | max(r,t)≥2 |
| Either arm | p≠2 or r+t≥1 |
| E+ feasible and T infeasible | r,t∈{0,1} and (p,r,t)≠(2,0,0) |

Indeed T feasibility implies r+t≥2, hence E+ feasibility, and T infeasibility is exactly the small odd-quota range r,t∈{0,1}. Both restricted arms fail precisely at the transported corner. This excludes only the declared placement and phase class. The full result combines symbolic supply and T obstruction with a finite-exhaustion basis for the one E+ exclusion.

## 6. Strategic reassessment

The two choices of second role here lead to different actual capacity vectors on one reduced template. D163's ordered obstruction therefore gives a reason to test a menu of compatible physical role placements before changing the exterior geometry. Independent exterior supply and role-menu coverage remain central because each menu needs its own independently verified reduced crossing and named-incidence construction. D168 gives an exact consumer once a compatible lower inventory and one two-host exterior are supplied. Extending the consumer to more hosts would still leave the supply question. The literature-informed pinned two-host shell lift addresses a different prerequisite, an independent D157 initializer with exact cut and port. It remains in its declared strategic scope, unstarted with its source checks open. This investigation closes the D163 corner symbolically, with no hybrid execution required. [D168](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md) · [Literature alignment](../docs/LOBSTER_RESEARCH_ALIGNMENT.md)

The sole proposed next investigation is a matched role-menu diagnostic across the frozen D164 four-first-center population. On the accepted completed E+ positives, ask whether every named original has a compatible instance of the single D165–D166 width-(6,4) terminal-exchange template when all admissible actual center and selected terminal roles are available. The two outcomes distinguish sufficiency on the frozen witnessed domain from a witnessed original requiring a different reduced exterior. For each missed original require accepted compatible E+ evidence and independently checked exclusion of the complete specified menu on that same original and admitted prefix. Use target-0060 and target-0428 E+ as positive controls and the scoped target-0057 E+ exhaustion as an adverse control. Preserve original names, directed roles, selected terminals, both partial inventories and exact return. Record structural differences between a witnessed exterior and the tested menu, especially actual widths, selected roles and failed quotas or residue constraints. Incomplete historical arms give no negative control, and the comparison does not resume D164 or settle its unresolved separation hypothesis. This is a proposed falsifiable hybrid question for separate Owner authorization. No inputs, runs or methods for it were prepared here. [D165 geometry and controls](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN.md) · [D166 geometry and controls](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT.md)
