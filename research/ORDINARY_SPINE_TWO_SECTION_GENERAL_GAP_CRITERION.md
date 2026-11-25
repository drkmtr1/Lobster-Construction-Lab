# D146 — Exact folded gap quotas at general D143 exterior widths

Task `LCL-ORDINARY-SPINE-TWO-SECTION-GENERAL-GAP-CRITERION-001`. All coordinates, parameters, labels and quotas are exact integers, excluding booleans. Intervals are inclusive, with reversed intervals empty. Write ⊔ for disjoint union.

## 1. Domain and result

Supply the independently constructed named ordinary [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) p=1 state of [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) on the old prefix, including its ordered physical spine, extreme frontier v, both full inventories and actual cut membership. In oriented coordinates v has label zero, n=2c+2, and crossing weights are exactly [d,n] with d=c+2. Append the two actual consecutive sections at u,w. Fix A≥2, B≥2, g≥0, K=A+B+g, s=A+B+2g, k=K−A=B+g, and m=n+2K, with n≥2K. Then s−K=g and A+B+s=2K.

The named reduced exterior labeling of D143 Section 3 is an independent input. It gracefully labels the actual exterior tree including v onto [0,A+B], fixes v=A and w=0, places u above A, and makes every exterior incidence cross the cut between A and A+1. Each of the A+B fresh exterior vertices has an individual physical host role and a prescribed quota q_h of named gap leaves. The given quotas sum to s. The old frontier is ineligible and physically ineligible fresh roles have zero quota. The actual gap leaves, with their original host and branch or terminal indices, are part of the target. No independent exterior supply for arbitrary targets is assumed.

The fresh gap sources have coordinates i∈[0,s−1] and full label A+c+i. A lower host j∈[0,A−1] has translation a_j=A−2−j and image i+a_j. An upper host of reduced label A+b, b∈[1,B], has image s+b−i. The actual leaf edge has weight d plus its image. The source is physically lower iff i<k. The image must lie in [0,s−1] and be at least K exactly when the source and its actual host are on opposite sides of the return cut. D143 requires a bijection of this alphabet.

The theorem decides existence within this supplied embedding exactly by a formal coefficient. The local destination state needs at most 4W bits, with W=max(1,A−2,B−1). Each actual physical host retains its own quota variable. Constructive predecessor extraction, intermediate inventories and exact return are part of the result. The interior stabilizes at fixed widths and fixed allowed roles, giving a rational generating series. All controls and verifications below are symbolic.

## 2. Exact crossing windows and local transitions

Set T=s+1, f=floor(s/2), P=floor(T/2), and define φ_s(t)=min(t,T−t) on all integers. Equivalently it is T/2−|t−T/2|. It is 1-Lipschitz and invariant under t↦T−t. Thus every lower-host assignment changes the folded column by at most |a_j|≤max(1,A−2). At upper host b write δ=b−1, so the image is T−i+δ and its folded displacement is at most δ≤B−1. Therefore every legal edge has folded distance at most W. This argument also applies to raw images before range filtering.

In folded column p, L_p=p exists for 0≤p≤f, and R_p=T−p exists for 2≤p≤P. For s=2h the two ranges of actual positions are [0,h] and [h+1,2h−1], with both slots in column h. For s=2h+1 they are [0,h] and [h+1,2h], with only R in column h+1. They partition the alphabet and give φ_s(i)=p at either position. Each position has a distinct source copy and destination copy. These are numerical fold rows. The physical cut predicates remain i<k and z≥K on the original coordinates. In particular k=B+g and the fold has f=g+floor((A+B)/2), so the source cut need not coincide with a fold boundary. The crossing destinations are precisely R_p with 2≤p≤g+1 because K>f and T−K=g+1.

The exact legal source intervals for each host are as follows. The letter z denotes a raw image coordinate.

| Host | Physical source side | Exact interval for i |
|---|---|---|
| Lower j, translation a=a_j | Lower | [max(0,−a), k−1] |
| Lower j, translation a=a_j | Upper | [K−a, min(s−1,s−1−a)] |
| Upper A+b | Lower | [b+1, min(k−1,g+b)] |
| Upper A+b | Upper | [max(k,g+b+1), s−1] |

For a lower source and lower host, i+a≤k−1+A−2=K−3 and i+a≥0 is exactly the indicated lower bound. For an upper source and lower host, i+a∈[K,s−1] is required. Its lower bound K−a is at least k+2, so the entire interval is physically upper. At upper host b the minimum raw image over the alphabet is b+1 and the upper bound s−1 is equivalent to i≥b+1. For a lower source this edge crosses and z≥K requires i≤g+b. For an upper source it is noncrossing and z<K requires i≥g+b+1, implying i≥b+1. This proves each interval in both directions. A host marked physically ineligible contributes no options.

For an existing source slot in column p, read its actual i and test the appropriate physical-side interval above for the chosen host. Its exact destination slot then follows from this table.

| Source | Host | Raw z | Slot if z≤f | Slot if z>f |
|---|---|---|---|---|
| L_p | Lower j | p+a_j | L_(p+a_j) | R_(T−p−a_j) |
| R_p | Lower j | T−p+a_j | L_(T−p+a_j) | R_(p−a_j) |
| L_p | Upper A+b | T−p+δ | L_(T−p+δ) | R_(p−δ) |
| R_p | Upper A+b | p+δ | L_(p+δ) | R_(T−p−δ) |

The source and target slots must exist. The interval test and the correct branch of the second table ensure exactly that target existence because every admitted z is in the alphabet. The tables include both fold rows changing destination row when they pass through the fold. They also include all missing columns through the slot domains and all short or overlapping boundary conditions through simultaneous intersections. No row has priority over another. If g=0, the two crossing-source intervals are empty and there are no crossing destinations. If a cut and fold are distinct or one of the boundary intervals overlaps another folded window, the original-coordinate predicate selects the same arcs as the physical incidence requirement. This establishes every local transition without a separate case convention for short gaps.

## 3. Bounded transfer and proof of state sufficiency

Let S_p,D_p be the existing source and destination slots of folded column p, empty outside [0,P]. Process all source columns p=0,…,P and then the W empty-source stages p=P+1,…,P+W. Before stage p represent the occupied destinations in [p−W,p+W−1] by two slots per column, at most 4W bits. Absent slots have bit zero. The state invariant is that all sources below column p have been assigned to distinct destinations, all existing destinations below p−W are occupied and retired, and no destination above p+W−1 is yet occupied. In particular column p+W starts free because every previous source column is at most p−1. Start at p=0 with the empty mask.

At each stage apply the following exact rule.

1. Select one permitted labelled arc for each source in S_p, using the empty selection when it is empty. Their destinations lie in [p−W,p+W], must be pairwise distinct and must avoid all occupied mask slots.
2. Form the union of the occupied mask with these destinations, requiring every existing destination of column p−W to be occupied. Drop that column and reindex the remaining occupancy on [p−W+1,p+W] for the next stage.
3. Weight each selection by the product of the variables X_h for its actual host labels. When multiple selections give the same masks, retain each contribution. There is a variable for every actual fresh exterior host, including zero-quota roles.

A retired destination in column p−W cannot be reached from any later source column at least p+1, since its distance would exceed W. Hence the occupancy requirement at retirement is necessary. The mask contains every previously used destination reachable by the current source, and the next mask holds every surviving occupancy reachable by a later source. Earlier sources have already consumed their unique choice. Therefore these checks impose all and only the geometric dependencies of later steps. Host usage by earlier choices is accounted for separately by their formal exponents. These facts prove the invariant by induction and prove that histories sharing an occupancy mask have identical geometric continuations.

After stage P the retired range ends at P−W. The W flush stages retire columns P−W+1 through P, interpreting negative columns as nonexistent when W is large relative to the gap. Each existing destination is checked once, including the largest column P on the last flush. The final mask at stage P+W+1 spans only columns above P and is empty. This gives the claimed W-stage flush even if some stages are vacuous.

Every legal host-labelled bijection gives a unique sequence of labelled selections and must pass every retirement check, because a missed destination could not be supplied later. Conversely any accepted sequence assigns every source exactly once, uses only legal host incidences, and supplies every destination exactly once by the occupancy and flush tests. The constructions are inverse on the label-coordinate allocation to physical hosts. This proves the representation without dropping any possible boundary or packet-free assignment.

## 4. Exact quota criterion, extraction and complexity

On the common set of 2^(4W) relative masks let T_p(M,N) be the sum of the monomial weights of all valid stage p selections between masks M,N. Invalid masks have no transitions. With e_0 the empty-mask column vector put

    Z_(A,B,g)(X) = e_0^T T_0 T_1 … T_(P+W) e_0.

The permitted physical role set is part of these matrices. Alternatively form the matrices with every role allowed and set X_h=0 at ineligible roles, which deletes every term with a use of those roles. At any intermediate stage the coefficient of a monomial counts exactly partial histories of that host-count vector at that mask. This holds initially, and each selection adds its host counts by multiplication. Nonnegative coefficients thus give the exact criterion

    [prod_h X_h^(q_h)] Z_(A,B,g)(X) > 0.

Counts are global per named host. The coefficient counts allocations of label coordinates to hosts, before bijections of the resulting labels to leaves at one host. To extract one, keep the prefix polynomials at each stage or their relevant coefficient arrays. Starting at the final empty mask with residual q, choose a predecessor mask and a particular labelled selection such that its count vector can be subtracted and the corresponding predecessor coefficient is positive. Such a predecessor exists by the sum with nonnegative coefficients. Using a fixed order of masks and labels makes this deterministic. Backtrack through all stages to the initial empty mask and zero residual. Every extracted edge then gives its actual host and both coordinates. At each host assign source labels to its declared leaf list, sorted by physical branch index for direct leaves or terminal index for a center, in increasing source-coordinate order. Each original named leaf appears exactly once at its already prescribed host.

Let H=A+B and Q=prod_h(q_h+1). Truncating exponents above q_h for any host is exact for the requested monomial, since all later increments are nonnegative. At each stage at most two sources occur, each with at most H physical host choices. The empty-source case has one trial. Thus at most (H+1)^2 local selections need to be checked per mask. Forming a mask transition and updating a vector of H counters can conservatively be charged O(W+H) indexed operations. A direct counter propagation and predecessor extraction therefore use at most

    O((P+W+1) · 2^(4W) · (H+1)^2 · Q · (W+H))

indexed arithmetic operations, with finite storage by keeping all predecessor layers or predecessor records. This is polynomial in s for fixed A,B, since q_h≤s and H is then fixed. In variable widths the bound has both the 2^(4W) factor and the product of growing quota dimensions. It gives no width-independent polynomial bound. Coefficients are bounded by H^s since each actual source has at most H host choices and the targets then follow. This bounds their binary length by O(1+s log H), but the displayed operation count treats arithmetic and indexing as units. Bit costs depend on operand and address lengths and the arithmetic representation. Even at fixed widths the bound in s is not a bound polynomial in the binary length of a succinct encoding of the quotas. No propagation or extraction was executed in this task.

## 5. Stable interior and rational series at fixed widths

Fix A,B and the allowed numerical host roles, with H=A+B and W as above. We give a common stability cutoff g≥2W. The values f=g+floor(H/2), P=g+ceil(H/2), k=g+B and K=g+H differ from g by fixed constants. The working window at stage p consists of columns [p−W,p+W]. In the full interval [2,g+1] both slots exist, L sources are lower, R sources are upper, L destinations are noncrossing and R destinations are crossing. Indeed L positions have coordinate at most g+1<k, and R positions there have coordinate at least T−(g+1)=K. These tests hold independently of whether a fold row meets the physical cut elsewhere.

For g≥2W the following consecutive stage products are well defined, using masks with slots relative to p.

- **Left stages p=0,…,W+1.** All working window columns are at most 2W+1≤g+1. Every existing slot has the above side predicates, also in the L-only columns 0 and 1. Translations stay on the same row with offsets a_j and −a_j for L and R respectively. Reflections switch rows with offsets −δ and +δ. A nominal L target below 0 or nominal R target below column 2 is outside the alphabet. In this range no nominal slot crosses the seam at the right end of a row, since its column is at most g+1. Accordingly the local tests and missing slots depend only on the left index p, and give a fixed row product α starting at e_0^T.
- **Interior stages W+2≤p≤g+1−W.** The working window lies wholly in [2,g+1]. It has both slots in every column and exactly the relative offset rules just stated. The retirement check uses both slots at offset −W. Therefore the matrix M is constant and the number of such stages is g−2W, including zero at equality.
- **Right stages g+2−W≤p≤P+W.** Every working window column is at least g+2−2W≥2, so no missing slot at the left end enters. Write p=g+t; the range of t is [2−W,ceil(H/2)+W]. Every existing source coordinate is g plus a constant determined by t and row, since T=2g+H+1. Its candidate image is likewise g plus a constant. The source cut, image threshold and fold seam are g plus fixed offsets. Moreover each raw image has folded column at least p−W≥2 by the distance bound even before filtering, which implies the raw image is in [2,T−2] and therefore in the alphabet. The remaining presence and retirement tests are fixed in relative coordinates. This part, including the flush stages, gives a fixed column product β ending at e_0.

Consequently Z_(A,B,g)=α M^(g−2W) β when g≥2W. With widths and allowed roles fixed, the series in a formal parameter z is

    sum_(g≥0) Z_(A,B,g) z^g
      = sum_(0≤g<2W) Z_(A,B,g) z^g
        + z^(2W) α (I−zM)^(-1) β.

The inverse is the formal geometric series and is rational over the rational function field in the host variables because its denominator determinant has constant term one. The finite initial polynomials use the unaltered exact tables. The cutoff is sufficient and need not be minimal. No short-gap polynomial or matrix entry was evaluated.

## 6. Symbolic controls and exact earlier scopes

**Pointwise D145 recovery.** At A=2,B=3 write k=g+3. Then s=2k−1, T=2k, f=k−1, P=k and W=2. The existing L and R positions coincide with D145, all L sources are lower and all R sources upper, and the crossing destinations are R_p for 2≤p≤k−2. The lower translations 0 and −1 give L_p→L_p and L_p→L_(p−1) when those targets exist. On R they give respectively R_p for 2≤p≤k−2 and R_(p+1) for 2≤p≤k−3. For each upper δ a lower L source p has image R_(p−δ) precisely for 2+δ≤p≤min(k−1,k−2+δ). From R_p the upper raw image p+δ is valid when p+δ≤k+1, with destination L_(p+δ) for p+δ≤k−1 and R_(2k−p−δ) otherwise. These are the D145 rules arc by arc, including both short-gap endpoints and all host tags. Substituting W=2 also gives its eight-bit mask and two flushes. Thus its criterion, original D143 control and D144 four-parameter recovery are inherited pointwise.

**Separation from both D144 recipes.** On that same reduced exterior take integer r≥0, g=r+1, k=r+4 and quotas (3,0,1+2r,2,1) in the D145 physical host order. Use u on the paired slots L_p↔R_p for p∈[2,k−3], b_2 on L_(k−1)↔R_(k−2), u on R_k fixed and b_3 on R_(k−1) fixed. The remaining L_0,L_1,L_(k−2) are fixed at w. These are exactly the legal arcs of the previous control after substitution, with the stated quotas and crossing images. D144 rule 2 needs width r+2>g. Rule 1 exhausts the b_2 quota on the boundary, requires one odd b_3 mixed packet, and gives M_2=−2 because there are no a leaves. The exact coefficient is positive by the explicit allocation, with no recurrence evaluation.

**Retained obstructions.** The raw physical windows also apply at B=1. The first upper source i=k exists since s−k=A+g≥2. It has no lower-host option because K−a_j≥k+2. An upper host would require i≥g+b+1, which is impossible at k=g+1 and b=1. Thus the D144 B=1 obstruction is preserved outside the main positive domain. At A=2, for any B≥2 the first two sources are lower since k≥2. No upper host accepts either since i≥b+1≥2. The lower translation −1 underflows at zero and would repeat destination zero at source one after source zero has been assigned to w. Hence both require w. In particular the D145 parity-passing adverse vector has q_w=1 and every accepted term here still has degree at least two in X_w.

**Inclusion of the arbitrary-width D144 packet domain.** The D144 certified boundary rules and packets supply distinct labelled destinations with the required source sides, crossing statuses and exact host quotas on the supplied named exterior. Each such assignment therefore satisfies the exact raw windows in Section 2, and its successive local selections define a path by Section 3. This proves inclusion even when its paired corridor is empty. No necessity is inferred for the D144 recipe, as the preceding separation shows. The even and odd partitions, missing-slot checks and physical-side intervals above apply for every g, including g=0, noncoincident cut and fold, and the negative retirement columns allowed at short gaps.

## 7. Original-target inventories and finite composition

Expand reduced lower exterior labels unchanged and reduced upper labels by addition of n+s. On the old prefix use the D143 embedding, with old labels [A,A+c−1]⊔[A+c+s,A+n+s] and old weights [1,d−1]⊔[d+s,n+s]. Write E for all expanded fresh exterior labels. They are exactly [0,A−1]⊔[A+n+s+1,m], and their actual tree edges including vu use [n+s+1,m], each crossing. Put the extracted labels A+c+i on the declared named leaves as in Section 4. They supply exactly [A+c,A+c+s−1] and weights [d,d+s−1] by the bijection. All labels in [0,m] and all actual differences in [1,m] are therefore used once. A gap edge crosses exactly on image coordinate at least K, so its crossing weights are [d+K,d+s−1]. The old and exterior crossings complete [d+K,m].

Before emitting either section, let I_1 consist of source coordinates whose actual host belongs to the first section at u, and J_1 be their image coordinates from the extracted labelled arcs. Let E_1 be the labels of the first section's exterior vertices, and D_1 the actual weights of its exterior edges, including vu and excluding uw. These finite sets are determined from the supplied named exterior and the gap extraction, before any whole-tree labeling is emitted. The used label inventory at the first boundary is

    [A,A+c−1] ⊔ [A+c+s,A+n+s] ⊔ E_1 ⊔ (A+c+I_1),

and the remaining label inventory is

    (E minus E_1) ⊔ (A+c+([0,s−1] minus I_1)).

The used difference inventory is

    [1,d−1] ⊔ [d+s,n+s] ⊔ D_1 ⊔ (d+J_1),

and the remaining difference inventory is

    ([n+s+1,m] minus D_1) ⊔ (d+([0,s−1] minus J_1)).

Its actual crossing set of weights is [d+s,n+s] ⊔ D_1 ⊔ (d+(J_1∩[K,s−1])); the other used weights are noncrossing. If the supplied reduced label of u is A+b_u, the first frontier label is n+s+A+b_u. The actual unfinished edge uw is the unique connector to the next section and weighs n+s+A+b_u when w at zero is emitted. This is the weight assigned to that actual exterior edge before gap selection. All other first-section incidences are emitted with their declared endpoints, and the second section uses exactly the complementary resources. No intermediate graceful rank or half-spectrum constraint is assumed.

The full return has physical w at the oriented extreme zero, new oriented cut C=c+K and threshold d+K, with m=2C+2 and crossing spectrum [d+K,m]. For actual input frontier at n, orient by x↦n−x and emit by F↦m−F. This gives actual frontier m, actual cuts n+1−c and m+1−C, and the same weight inventories and crossing statuses. The growing map on old actual labels then shifts low labels by B and high labels by B+s. For actual minimum polarity the two shifts are A and A+s. In both cases old membership is preserved. The first-boundary label sets for maximum polarity are obtained by the same output complement, without changing their weight sets.

For any finite admitted list, widths and quotas can vary between blocks. At every step require the inherited size premise and independent named exterior labeling, and the proved positive coefficient for that block. By the exact return, induction supplies the next oriented state and preserves the physical frontier polarity. An independently supplied D134 p=1 initializer can be chosen large enough for a declared finite list as in D143. For immutable labels, at a completed boundary use the actual cut there and sum later actual lower shifts and later gaps separately. Every label at that boundary is shifted by the former sum, plus the latter on the actual upper side. Membership preservation makes this equal to the composed embedding. Each existing difference gains precisely the sum of later gaps when it crosses. At intermediate first-section boundaries the same rule uses the cut of the current block and the explicitly displayed crossing set before the second section. Injectivity of the composite yields the exact used sets and hence both complementary inventories in the final alphabet. This assigns each physical vertex once at its final label. Each transfer, predecessor chain and finite block list terminates. No universal quota positivity, independent exterior construction for all original topologies, or width-independent frontier size is claimed.

The conditional allocation duty for supplied D143 exteriors is settled within this domain. The next structural issue is independently supplying compatible named exteriors from prescribed original topologies. Symbolic construction and obstruction proofs, computational discovery with exact original-target verification, and hybrid discovery followed by theorem proof can be compared by the mathematical leverage they offer on that issue. That reassessment and any computational activity require a separate task authorization.
