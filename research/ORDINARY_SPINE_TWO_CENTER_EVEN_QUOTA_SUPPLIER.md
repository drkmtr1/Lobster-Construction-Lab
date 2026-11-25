# D149 — Two-center terminal-enabled symbolic separation

Task `LCL-ORDINARY-SPINE-TWO-CENTER-EVEN-QUOTA-SUPPLIER-001`. All counts and labels are exact integers, excluding booleans. Intervals are inclusive, with reversed intervals empty. The symbol ⊔ denotes disjoint union. The parameters p and q are half-quotas. The D134 state parameter is fixed at 1.

## 1. Theorem and input

Supply an independently constructed named ordinary graceful [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) prefix with n edges, actual spine frontier v at an extreme, and the p=1 cut-spectrum state. In its zero-frontier orientation G, the cut c and minimum crossing weight d satisfy n=2c+2 and d=c+2. The crossing weights are exactly [d,n]. Vertices at the cut are on its upper side.

Prescribe the two consecutive original sections (3) at u and (2p,2q,0,0,0,0) at w for independent p,q≥1. Call the actual first-section center a, and call the first and second actual centers at w P and Q, respectively. The zero entries give four actual direct leaves at w. The first section has five new vertices, including u and the three terminals of a. The second has 2p+2q+7, including w, both centers and all four direct leaves. Every added vertex has one new edge to its actual parent. Thus H=2K=2p+2q+12 and K=p+q+6. Require n≥2K. Put m=n+2K.

**Positive claim.** For every admitted p,q, the named original has an explicit terminal-enabled completion in the [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) embedding, with the exact D134 p=1 return and the original extreme polarity. Sections 3–5 give the independently supplied reduced exterior, gap, and intermediate reservations. Section 6 proves finite closure and immutable final labels.

**Negative claim.** For any admissible D143 two-section original whose first section has one positive center of odd terminal quota and no direct leaves and whose second section has only even positive-center quotas, a terminal-free exterior is impossible. The second section's actual direct-leaf count and selection are unrestricted in this claim. Thus the positive claim gives an infinite matched separation on the same named originals and within D143. This is a conclusion about the declared embedding and return interface.

## 2. Terminal-free obstruction

In any successful D143 placement, all centers are exterior, both new spine vertices are exterior, and every reduced edge crosses the cut between A and A+1. The edge vu crosses from v on the low side to u on the high side. It follows from uw and the branch attachments that w and the sole first center are on the low side, and all second centers and selected direct leaves at w are high. In a terminal-free exterior there are no other low vertices besides v, w and the first center, since u has no direct leaves. Consequently A=2, w=0, and the first center has reduced label 1. The old v is ineligible to host gap leaves.

Write ℓ_j for the number of gap leaves at low host j and r_b at high host A+b. The gap formulas of D143 are i↦i+(A−2−j) and i↦s+b−i, respectively. If the allocation is a permutation of [0,s−1], the sum of all image coordinates minus source coordinates is zero. Writing U for the sum of the source coordinates assigned to high hosts gives the [D144](ORDINARY_SPINE_TWO_SECTION_GAP_ALLOCATION.md) identity

    ∑_j (A−2−j) ℓ_j + ∑_b (s+b) r_b = 2U.

The only low hosts are w with shift zero and the first center with shift −1. With no exterior terminals, every terminal at a center remains in the gap. Thus the contribution of the first center is odd and each high center's contribution is even. The high spine u has no direct quota. An exterior direct leaf at w has no further child and contributes zero. A direct leaf kept in the gap contributes only at w, with shift zero. The left side is odd, contradicting the identity for every s and every selection of those direct leaves. The argument therefore excludes every terminal-free exterior on the claimed domain, in either actual polarity by the D143 oriented reduction.

## 3. Named exterior and common initial coordinates

Choose A=3. Set B=4 for q≥2 and B=5 for q=1. Set s=2K−A−B and k=K−A, the source cut. For q≥2, s=2p+2q+5 and s−K=p+q−1≥2. For q=1, s=2p+6 and s−K=p−1≥0. Hence the inherited s≥K condition holds, even at p=q=1. The reduced exterior including v has these labels and actual differences.

| Actual edge | Reduced endpoint labels in edge order | Reduced difference |
|---|---|---:|
| vu | 3,4 | 1 |
| ua | 4,2 | 2 |
| a to its last indexed terminal | 2,5 | 3 |
| uw | 4,0 | 4 |
| wQ | 0,6 | 6 |
| Q to its last indexed terminal | 6,1 | 5 |
| wP | 0,7 | 7 |
| w to its last indexed direct leaf, only q=1 | 0,8 | 8 |

Each endpoint label is assigned to exactly one named vertex. This is a bijection onto [0,A+B]. The displayed edges are the actual ones in the reduced tree, cross after reduced label 3, and use [1,A+B] once. In particular the two exterior terminals retain their original hosts and the reduced difference 5 uses the terminal of Q. The two terminal edges realize the paired exchange in [D147](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md), here checked directly. No exterior choice depends on a completed labeling.

The remaining quotas in physical order (w,a,P,Q) are (4,2,2p,2q−1) for q≥2 and (3,2,2p,1) for q=1. All other exterior vertices have zero gap quota. The actual image rules are

    w: i→i+1      a: i→i−1      P: i→s+4−i      Q: i→s+3−i.

An image must lie in [0,s−1] and be ≥K exactly when its source lies across the cut from the host. At sources 0,2 use w and at sources 1,3 use a. The two transpositions permute [0,3]. Both hosts and all four sources are low since k≥5, and every image is below K. This exhausts a's gap quota. For subsequent coordinates put x=i−4 and express the images as y=π(i)−4. The w rule remains x→x+1. The Q rule is x→R(x)=s−5−x and the P rule is x→R(x)+1. The remaining alphabet in both copies is [0,s−5].

### Case q≥2

Put M=p+q, N=2M, and R(x)=N−x. The remaining alphabet is [0,N], the source is low exactly for x≤M−2, and a crossing image is exactly y≥M+2. Both P and Q are high. In particular Q's map is crossing-exact on every point on which it is used, since R(x)≥M+2 exactly for x≤M−2.

Use the following disjoint cycles.

- At x=0, 1, R(0), use w, P, Q, giving 0→1→R(0)→0.
- For x in [2,p], transpose x and R(x−1) through P. The forward image is R(x)+1=R(x−1); the reverse image is x.
- At R(p+1), R(p), p+1, use w, P, Q, respectively. Their images are R(p), p+1, R(p+1), closing the cycle.
- Use Q on the remaining interval [p+2,N−p−2].

The first three items consume the two intervals [0,p+1] and [N−p−1,N]. The low positions increase from 0 to p+1 and the paired positions R(0),R(1),…,R(p+1) decrease from N to N−p−1 without repeats. The intervals are disjoint since N−p−1=p+2q−1≥p+3. Their complement is invariant under R, so no image leaves its assigned cycle or the complement. The complement has length 2q−3. P is used once in each mixed cycle and twice per pair, for 2+2(p−1)=2p. Q is used once in each mixed cycle and at every complementary position, for 2q−1. The two new uses of w plus its two reserved uses give four.

For the actual crossing predicates, P on [1,p] uses low sources and gives images ≥N+1−p=p+2q+1≥M+2. P on [N−p,N−1] uses high sources and gives images in [2,p+1] below M+2. These are all P uses. Q is crossing-exact by the earlier equivalence, including the mixed source p+1. At q=2 that source is high at equality x=M−1, and its image R(p+1) is below the threshold. At q≥3 it is low and that same Q image crosses. The w source 0 is low with image 1 noncrossing. Its other source R(p+1) is high and its image R(p)=p+2q is ≥M+2 because q≥2. Its edge therefore crosses at exactly the required threshold. All images belong to [0,N] by the permutation proof. At p=1 the P pair interval is empty, with the two mixed uses of P supplying its full quota. At q=2 the complementary interval is a singleton and is fixed by Q. These verifications include their simultaneous boundary.

### Case q=1

Now the alphabet is [0,N] with N=2p+1 and R(x)=N−x. The low source condition is x≤p−1 and a crossing image requires y≥p+3. Use 0→1→R(0)→0 at w,P,Q, use the P transpositions x↔R(x−1) for x∈[2,p], and fix p+1 through P. Indeed R(p+1)+1=p+1. The mixed cycle and pairs exhaust [0,p] and [p+2,2p+1]. The remaining point is precisely the fixed point. This is a permutation, with 1+2(p−1)+1=2p uses of P, one of Q, and one additional use of w, for three including the two reserved uses.

For P the low sources are exactly [1,p−1] and their images 2p+2−x are ≥p+3. All remaining P sources are high and have images ≤p+2 by the same formula. All these images belong to the alphabet by the permutation proof. The Q source N is high and goes to 0, so its edge is noncrossing. The w source 0 remains low and goes to 1, below p+3. At p=1 the pair set and the crossing-image interval are empty. The P source 1 in the mixed cycle is now high with noncrossing image, and the P fixed point is also high with a noncrossing image. Thus the construction covers the s=K boundary as well.

### Named leaf order

Give each assigned source the full oriented leaf label A+c+i on the corresponding actual host. For the gap use increasing coordinate order within each host's remaining indexed terminal or direct-leaf list. Only the stated exterior terminal indices are reserved. For q=1 the last direct leaf is already exterior. All quotas were proved by distinct source counts, so this assigns every original leaf exactly once at its originally declared parent. In the standard order P is always index 0 and Q index 1, even when p or q is 1 or when the quotas agree. There is no reordering of branch entries.

## 4. Full inventories and exact return

For an old label G(x), use F(x)=A+G(x)+s·1_{G(x)≥c}. Its occupied label bands and differences are

    L_old = [A,A+c−1] ⊔ [A+c+s,A+n+s]
    D_old = [1,d−1] ⊔ [d+s,n+s].

Old same-side differences stay fixed and each actual old crossing gains s. The expanded exterior keeps the low reduced labels and adds n+s to the high ones. Its fresh label set is E=[0,A−1]⊔[A+n+s+1,m], and its actual edges including vu use exactly [n+s+1,m]. The gap fills exactly [A+c,A+c+s−1], and each actual gap difference is d+π(i) by subtraction from its named host. The proved permutation gives [d,d+s−1]. The three sets complete the label alphabet [0,m] and the weight alphabet [1,m], with no repeats.

At C=c+K the first upper gap coordinate is k. The old sides are preserved because k≥0 and s−k=K−B≥0. Each expanded exterior edge crosses. Gap and old crossings use [d+K,d+s−1] and [d+s,n+s] respectively, giving [d+K,m] with the exterior crossings. The actual noncrossing weight spectrum is [1,d+K−1], including the gap demands [d,d+K−1]. In oriented coordinates w has 0, m=2C+2, and d+K=C+2. These are the exact D134 p=1 return data.

For an actual minimum-frontier input, use F as the actual label. For an actual maximum-frontier input, start with G=n−g and emit m−F, where g denotes the given actual old labeling. The actual cuts are then n+1−c and m+1−C, with sides interchanged twice and old membership preserved. The old actual low and high shifts are B and B+s in the maximum case, and A and A+s in the minimum case. This retains actual frontier polarity, edge weights, crossing statuses, names, and original incidences in both cases.

## 5. Independently supplied first-section reservations

The first section uses the three expanded exterior labels E_1={2,n+s+4,n+s+5}, from a, u, and a's exterior terminal. The actual edges vu, ua and that terminal edge have high differences D_1=[n+s+1,n+s+3]. The only first-section gap leaves are at a and use I_1={1,3} with images J_1={0,2}. These are known from the given prefix and prescribed parameters before any second-section labeling. In the declared final alphabet the exact inventories are

    used labels        L_old ⊔ E_1 ⊔ (A+c+I_1)
    remaining labels   (E minus E_1) ⊔ (A+c+([0,s−1] minus I_1))
    used differences   D_old ⊔ D_1 ⊔ (d+J_1)
    remaining weights  [n+s+4,m] ⊔ (d+([0,s−1] minus J_1)).

The first-boundary crossing weights are [d+s,n+s] ⊔ D_1. The first-boundary noncrossings are [1,d−1] ⊔ (d+J_1). The actual frontier u carries n+s+4 and only its edge uw is unfinished. As w has 0, this connector consumes n+s+4 in the next section. The rest of that section uses the complementary resources by the proved exterior spectrum and gap permutation. The maximum-oriented version complements all partial labels about m and the cut about m+1. Its frontier u carries B−1 and the weight inventories and actual crossing edges stay the same. The intermediate edge count n+5 is odd, so no normalized D134 p=1 state is required there.

## 6. Independent seeding, repetition and termination

D134 §Independent symbolic initialization supplies named p=1 states of arbitrarily large size from an independently supplied maximum-frontier seed and the real initializer path and branched section. Keep those original sections in the target. D143 §6 supplies the size and complementary-polarity argument. For a finite declared list of these D149 blocks, require each current n≥2K for the next prescribed p,q. A sufficiently large independent initializer can satisfy every bound by taking its initial n≥the largest 2K on the list. Induction using §4 increases the edge count by 2K and the oriented cut and threshold by K at each block and preserves the same extreme polarity. This supplies every admitted list, including mixed q=1 and q≥2, and every finite repeat of one admitted block.

At a completed block boundary j let C_j be its *actual* cut. For the remaining blocks let L_j be the sum of their actual lower shifts (A_i or B_i according to the retained polarity), and S_j the sum of their gap widths s_i. Every label x at boundary j has final label x+L_j+S_j·1_{x≥C_j}. This follows by composition because actual cut-side membership persists. Each actual weight gains S_j precisely when it crosses. At the first section of a block use that block's actual completed cut and the displayed partial crossing inventory. The later embeddings are already fixed by the list and they apply to those partial labels and incidences without requiring the second section to be emitted first. Their affine maps on each side transport the occupied sets in §§4–5 injectively. Both remaining inventories in the final alphabet are the respective exact complements there, also at the partial boundary. This emits each vertex in its immutable final label and retains its physical connector.

Each block's coordinate description can be read in increasing source order from the closed intervals and their endpoints. A source can be assigned to its host and its host's next available index in a constant number of indexed operations. Each finite block terminates. With suffix sums precomputed once, emitting the supplied prefix and the finite list is linear in the number of original vertices plus the number of blocks in indexed integer operations. Integer bit costs are separate from this operation count. No search or transfer evaluation is needed.

## 7. Retained controls and scope

The four frozen D148 controls have v=s:25, u=s:26, w=s:27, a=b:26:0, two ordered centers b:27:0 and b:27:1, and direct leaves b:27:2 through b:27:5. They all have the retained n=54 prefix and meet the size premise. The independent symbolic theorem covers their exact named original profiles by the ordered interpretation, as shown below. The archived roles document which actual center had reduced labels 7 and 6. The entries are read from the existing original-bound records.

| D148 original | Ordered (p,q) | Standard theorem case | Archived index at reduced 7, then 6 |
|---|---|---|---|
| 0132 | (1,1) | q=1 | 0,1 |
| 0134 | (1,2) | q≥2 | 0,1 |
| 0140 | (2,1) | q=1 | 1,0 |
| 0142 | (2,2) | q≥2 | 0,1 |

The theorem applied in physical order to 0140 uses B=5 even though its archived witness uses B=4. A separate role choice on that *same* named original uses P at b:27:1 and Q at b:27:0, with half-quotas (1,2) in the formula's role order. This choice is justified directly: uw and both center attachments keep their original endpoints, each 7-role terminal is an actual indexed child of b:27:1, each 6-role terminal is an actual indexed child of b:27:0, and only that second role's last child is reserved exterior. Each actual child receives the quota-compatible formula at its own host. In general one may choose numerical roles in either physical order by passing the half-quotas of the chosen P,Q in that order and preserving the original indices and parent lists. No isomorphism quotient, swapped terminal incidence, or permutation of the declared profile is needed. The controls establish topology and quota coverage, and explain the archived role reversal. No new pointwise replay of archived labels is asserted.

The terminal-free parity test also excludes all four controls symbolically, independent of their D148 computational T negatives. D145 and D146 provide exact criteria on their declared supplied exteriors. This result supplies an exterior and an explicit coordinate allocation and would yield a positive term in the D146 test by its proved path equivalence. It does not evaluate that test. It extends the one-second-center symbolic separation of D147 to the prescribed two-center even-quota family, and gives symbolic scope beyond the four matched finite observations without altering any execution disposition. General terminal-enabled exterior supply, other quota parities, and ordinary gracefulness outside D143 remain separate questions. Target-0188 and its two-to-one exterior-terminal balance remain a separate unstarted lead.
