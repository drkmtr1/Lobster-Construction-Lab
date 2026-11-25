# D145 — Exact symbolic physical quotas on the D143 five-vertex exterior

Task `LCL-ORDINARY-SPINE-TWO-SECTION-EXACT-GAP-CRITERION-001`. All parameters and counts are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty.

## 1. Domain and result

Use the accepted [D143 two-section reduction](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) with an independently supplied named D134 p=1 prefix, size n≥2K, oriented cut c=n/2−1, actual frontier v oriented to zero and exact crossing spectrum [d,n] for d=c+2. Fix A=2, B=3, K≥5, k=K−2≥3, g=K−5=k−3 and s=2K−5=2k−1. The full size is m=n+2K=n+s+5. The independently supplied reduced exterior has actual named spine v,u,w and branches a at u and b_2,b_3 at w. Its labels at v,u,w,a,b_2,b_3 are 2,3,0,1,4,5. The actual initial connector, first attachment, second connector and second attachments have reduced differences 1,2,3,4,5 in that order and cross the reduced cut after label 2. The old frontier v has no gap leaves.

Prescribe a nonnegative physical quota vector q=(q_w,q_a,q_u,q_2,q_3) summing to s. These are counts of named direct leaves at w,u and terminals at a,b_2,b_3. The target supplies their actual host, section and branch or terminal indices. A zero terminal quota keeps its exterior branch as a direct leaf. The numerical host labels and actual topology are fixed.

For each source coordinate i∈[0,s−1], the full label is d+i. The image coordinate j gives actual difference d+j. At the five respective hosts the image formulas are i, i−1, 2k−i, 2k+1−i and 2k+2−i. The source is lower for i<k and upper otherwise. It crosses exactly when its actual host lies on the other side. A legal option has j in [0,s−1] and j≥K exactly on crossing edges.

The criterion is positivity of the coefficient of X^q in an explicitly defined bounded-width transfer polynomial. Sections 2–4 prove a necessary and sufficient criterion for all quotas in this fixed embedding, along with constructive extraction. Section 5 proves an eventually constant interior transfer and a rational series in the gap parameter. No numerical evaluation of the criterion is part of this proof.

## 2. Fold and exact local options

Extend φ(t)=k−|t−k| to integer t. It is 1-Lipschitz, by the reverse triangle inequality, and φ(2k−i)=φ(i). The lower hosts apply shifts 0 and −1, so their folded changes have absolute value at most 1. An upper host applies 2k−i+δ with δ in {0,1,2}, so its folded change has absolute value at most δ≤2. This bound uses only the formulas and therefore applies to every legal option.

Each folded column p has at most two positions. Name them L_p=p when 0≤p≤k−1 and R_p=2k−p when 2≤p≤k. These two lists partition [0,s−1] without repetition. In particular R_k denotes the single coordinate k and there is no L_k. The L sources are all lower and the R sources all upper. The crossing destinations are exactly the R positions with p∈[2,k−2]. The two positions R_(k−1),R_k, at coordinates k+1 and k, are upper sources and noncrossing destinations. All L destinations are noncrossing.

Use a distinct source and destination copy of each position. The following table contains every arc of the resulting bipartite graph, with label equal to its physical host. Each row is intersected with existence of its named source and target, in particular p≥2 on every R source. No identification of different host labels is made.

| Host | Source | Condition on column p | Destination |
|---|---|---|---|
| w | L_p | all present | L_p |
| w | R_p | 2≤p≤k−2 | R_p |
| a | L_p | 1≤p≤k−1 | L_(p−1) |
| a | R_p | 2≤p≤k−3 | R_(p+1) |
| upper with shift δ | L_p | 2+δ≤p≤min(k−1,k−2+δ) | R_(p−δ) |
| upper with shift δ | R_p | p+δ≤k−1 | L_(p+δ) |
| upper with shift δ | R_p | k≤p+δ≤k+1 | R_(2k−p−δ) |

Here the upper host for δ=0,1,2 is u,b_2,b_3 respectively. From L to a lower host, the shifts either stay in the low destinations or underflow at p=0 for a. From R to a lower host, the destination must cross and have coordinate at least k+2. The formulas give R_p at w, and R_(p+1) at a when it exists in the crossing set. In particular the shift from i=k to i−1 does not qualify. From L to an upper host the formula gives coordinate 2k+δ−p and requires k+2≤2k+δ−p≤2k−2. This is exactly the displayed interval after enforcing source existence. From R to an upper host the image is p+δ, which is at least 2. The noncrossing requirement is p+δ≤k+1, and k+1≤s−1 for all k≥3. The last two rows are the unique split of that condition into L and R destinations. The converse in each row follows from the same formulas and the actual sidedness of the host and source.

This proves the table uniformly, including overlaps of the two ends. Columns 0 and 1 lack R, column k lacks L, and no columns outside [0,k] exist. When k=3 the crossing interval of R columns is empty, and the first four rows leave only the L options. The upper-host rows from L are then empty, and the permitted upper-host options from R use their noncrossing destinations with the same limits. For k=4 or 5 every window is still its stated intersection, so a missing R or an empty shift range cannot introduce an additional arc. No boundary overwrite or priority rule is used.

## 3. Exact transfer and state sufficiency

Use five commuting indeterminates X_h, one for each physical host h. Let S_p and D_p be the source and destination copies of the existing positions in column p, with both empty outside [0,k]. Process the source columns in order p=0,1,…,k+2. The last two stages have no sources and flush the remaining destinations.

Before stage p keep a mask M of occupied destinations in columns [p−2,p+1]. Encode it by the two slots L,R in each of four consecutive columns. Absent destinations always have bit zero. The intended invariant is that all sources in columns <p have chosen distinct destinations, every destination in columns <p−2 has been occupied, and there is no occupied destination in a column >p+1. The last assertion follows from source distance at most 2. The initial mask for p=0 is empty. It corresponds to the empty assignment, and the columns below −2 have no destinations.

For each stage p and input mask M perform the following symbolic transitions.

1. For each source in S_p select one arc from the table for its column, keeping its actual host label. If S_p is empty, select the empty set. All current target columns are in [p−2,p+2]. Require the selected destinations to be pairwise distinct and outside M. Destinations in column p+2 are free at the start of this stage.
2. Let N be the union of M with these selected destinations. Require every existing destination of column p−2 to be in N. Remove that column and reindex the remaining occupied mask on [p−1,p+2], which is the next stage's window.
3. Give the transition weight the product of X_h over its chosen arcs. Multiple distinct valid choices between the same masks contribute separately.

These rules are sufficient to retain every future constraint. No remaining source after stage p can reach a destination of column p−2, by distance at most 2. Therefore the last-chance test is necessary. Distinctness in step 1 checks all earlier destinations reachable by current sources. The use of an earlier destination below the mask is impossible by the same distance bound. The next mask records all and only occupied destinations that later choices can still affect. No earlier source remains to be matched twice, since each source is processed once and all choices in its stage are explicit. This proves the invariant by induction. It also shows how different histories with the same mask can safely share future transitions. Any dependence on their different host usage is retained by the monomials of the transfer polynomial.

Conversely a legal complete gap allocation selects arcs for exactly the sources in each stage. An occupied destination below the mask cannot be selected later. If a destination of column p−2 were still unoccupied at retirement, no later source could supply it. Thus a complete allocation passes every transition and produces its own uniquely determined path of labelled selections. In the forward direction an accepted path supplies exactly one image for each source by construction. The two flush stages retire the last existing columns k−1 and k. All destinations are then occupied exactly once, so the resulting map is bijective. The arcs certify actual crossing status. The final mask at stage k+3 is empty because every remaining window column lies above k. This proves both directions without any restriction to the boundary assignments or packets of D144.

## 4. Coefficient criterion and constructive extraction

For each stage p define a polynomial T_p(M,N) as the sum of the weights of all transitions from input mask M to output mask N. This is a local rule with at most two sources and at most five labelled arcs per source. There are at most 2^8 possible masks at each stage. The entry for an invalid mask is zero. Put F_0(empty)=1 and F_0(M)=0 elsewhere. Recursively define

    F_(p+1)(N) = sum_M F_p(M) T_p(M,N)
    Z_k(X) = F_(k+3)(empty).

For all p the coefficient of X^r in F_p(M) counts the partial histories using exactly r_h leaves at each host and ending at M. This follows from the transition proof and multiplication by the prescribed monomial. At the final stage the same statement counts label-coordinate allocations to physical hosts realizing r, before any permutations of named leaves at one host. Hence the exact criterion is

    [X_w^q_w X_a^q_a X_u^q_u X_2^q_2 X_3^q_3] Z_k(X) > 0.

Negative or noninteger quotas and quotas of total other than s are outside the prescribed input. All relevant coefficients are nonnegative. For extraction, start at the final stage with the empty mask and residual count q. Select a predecessor mask and one local arc selection whose host-count vector e does not exceed the residual componentwise, and for which the predecessor coefficient with counts reduced by e is positive. Such a choice exists by the recurrence. A deterministic order of masks and arc labels makes the choice canonical. Traverse back to the empty initial mask and residual zero. Each selected arc now fixes a source, an image and an actual physical host. Put the resulting source labels on the named leaves in increasing source-coordinate order within the host, using the prescribed order of the direct branch or terminal indices. This preserves all original incidences and gives the exact quotas.

Equivalently retain an exact quota-counter array, truncating exponents above the prescribed counts. Future increments are nonnegative, so that truncation is exact for X^q. The number of counter vectors per mask is at most the product over h of (q_h+1). There are k+3 stages and boundedly many transitions per mask. Thus exact counter propagation and extraction can use O((k+3) times that product) indexed operations at fixed host count, counting coefficient additions as arithmetic operations. Storing predecessor layers or transition choices gives finite extraction under the same bound. These are symbolic proofs of a recurrence and a finite algorithm. No counter propagation, matching search or numerical quota evaluation was executed.

## 5. Stable interior and rational series

Use relative masks indexed by column offsets −2,−1,0,1 from the current source column, with L and R slots. Then each T_p is a matrix on a common set of 2^8 masks, zeroing impossible masks. Let e_0 be the column vector at the empty mask. For every k≥6 the following three parts are stable.

- At p=0,1,2,3 the source and destination presence is determined by the left end. The window stops at p+2≤5≤k−1. For sources in this range, w and a have their full interior R options whenever R exists, since p≤3≤k−3. The upper choices on L are excluded only by their lower endpoints, and the upper choices on R go to L because p+δ≤5≤k−1. Thus these four matrices give a fixed row product α starting at e_0 transposed.
- For 4≤p≤k−3 every column in the working window [p−2,p+2] has both positions. The table has w and a on both rows, and every upper host in both directions using its fixed offset δ. Every option is the relative translation or reflection already displayed. The retirement test is the same two-slot test at offset −2. The resulting constant matrix is M. There are k−6 such columns, with zero when k=6.
- At p=k−2,k−1,k,k+1,k+2 the farthest left window column is at least k−4≥2. Thus the left end imposes no missing slot. Relative to k, the option limits and missing right columns are fixed, including both flush stages. Every lower threshold for an L source to an upper host that could apply, 2+δ≤4, is satisfied at any of these existing L columns since k−2≥4. R options respect exactly the table's upper cutoffs. These five matrices give a fixed column product β ending at e_0.

Consequently Z_k=α M^(k−6) β for k≥6. Small k=3,4,5 use the same table and mask rule directly, as formal polynomials. In particular, in the formal parameter z,

    sum_(k≥3) Z_k z^(k−3)
      = Z_3 + z Z_4 + z^2 Z_5 + z^3 α (I−z M)^(-1) β.

The formal matrix inverse is the geometric series and is rational over the field of rational functions in the host indeterminates, since the determinant of I−z M has constant term one. Neither the exceptional polynomials nor the stable matrices are evaluated by this assertion. It gives a rational generating series for the exact fixed-exterior allocations. A simpler set of closed-form quota inequalities is left open.

## 6. Symbolic controls

**D143 and D144 recovery.** Use the D144 four-parameter family with r,t,p,q≥0 and g≥2t+r+2p+3q. Write p,q here only for the two pair counts. Reserve R_k at u and R_(k−1) at b_3 as fixed images. Define the reflection R(x)=2k−x on paired columns [2,k−2]. The t mixed cycles use two consecutive columns each and are L_x→R_x→L_(x+1)→L_x at hosts u,b_2,a. Then use r reflection pairs at u, p reflection pairs at b_2 and q reflection pairs at b_3. A pair at upper shift δ uses L_(x+δ)↔R_x in a block of δ+1 consecutive columns beginning at x. All blocks use disjoint paired columns and have total width 2t+r+2p+3q. Give every other coordinate a fixed image at w. These are valid arcs in the table and reproduce exactly the D144 placement with boundary rule 2, including the two low outer coordinates and the last low coordinate outside the paired columns. Their counts at w,a,u,b_2,b_3 are (s−2−2r−3t−2p−2q,t,1+2r+t,t+2p,1+2q). At p=q=0 the original D143 named cycles and intermediate reservations are recovered. Each construction contributes a positive term at its exact quota monomial. This is a term existence proof, with no coefficient evaluation.

**D144 adverse quota vector.** For every k≥3 prescribe (1,s−3,1,0,1). Aggregate balance gives x=0 and y=g, and the global quota parity expression is s+7, which is even. However L_0 has only its w arc, which consumes destination L_0. At L_1 the a arc would hit L_0 a second time and no upper host is eligible. Hence w is required at both sources, forcing a factor X_w^2 in every accepted term. The prescribed vector fails the exact criterion.

**Strict separation from both D144 boundary choices.** For each integer r≥0 choose g=r+1 and hence k=r+4 and s=2r+7. Prescribe the vector (3,0,1+2r,2,1) at the respective physical hosts. Use R_k fixed at u and R_(k−1) fixed at b_3. At every p∈[2,k−3] exchange L_p and R_p through u. These are r disjoint reflection pairs. Exchange L_(k−1) and R_(k−2) through b_2. Indeed k−1 satisfies the L-source window for δ=1 and the reverse image is p+1=k−1 when p=k−2. The two directions have the correct crossing and noncrossing images. Fix L_0, L_1 and L_(k−2) at w. This uses every position exactly once and produces the specified quota on the same named exterior, so the coefficient is positive. It works at r=0 with no u pairs.

For D144 boundary rule 2 the resulting counts would need r u pairs and one b_2 pair. They cost r+2 columns, strictly more than g=r+1. For boundary rule 1 the two middle sources exhaust b_2's quota and the residual b_3 quota is odd. The rule then demands one b_3 mixed cycle, which uses two a assignments, although q_a=0. Its computed M_2 is −2. Both deterministic rules reject the entire family. This discrimination uses genuine eligible boundary incidences without changing the host labels, crossing demand or embedding.

## 7. Named composition and scope

For any admitted vector the extraction supplies the first-section reservations from the declared block data and the independently supplied exterior before either section is emitted. Let I_1 consist exactly of sources assigned to u or a, and let J_1 be the set of their images. The used labels in the declared block alphabet are

    [2,c+1] ⊔ [c+s+2,n+s+2] ⊔ {1,m−2} ⊔ (d+I_1).

The used differences are

    [1,d−1] ⊔ [d+s,n+s] ⊔ [n+s+1,n+s+2] ⊔ (d+J_1).

Both remaining sets are the exact complements in [0,m] and [1,m]. The first-stage crossings have weights [d+s,n+s], [n+s+1,n+s+2] and d+(J_1∩[K,s−1]), disjointly. These formulas include all old incidences and the actual exterior edges vu and ua. The actual new frontier is u at m−2. Its only edge to the next section is uw, of weight m−2=n+s+3 with w at zero. The second section emits the complementary named leaves and the remaining three exterior vertices. These first-boundary inventories require no solved old graph extension or independent assumption about intermediate ranks. They are calculated from the independent exterior labels and gap transfer arcs, before constructing the completed labeling of the original graph.

The complete exterior crosses with spectrum [n+s+1,m]. The table enforces actual gap crossing weights [d+K,d+s−1] and noncrossing weights [d,d+K−1]. Combine these with the old bands. The used labels and differences fill both full alphabets, and the exact crossings at C=c+K have weight spectrum [d+K,m]. D143 therefore returns its D134 p=1 data at the physical frontier w with the same polarity. For a maximum-frontier input use the simultaneous complements of D143 and complement the cut consistently. Those maps preserve all differences, names and memberships.

On a finite list of admitted blocks the oriented increase is 2K in size and K in the cut and threshold, with the same exact frontier polarity. At every step require the inherited size inequality. The quota criterion depends only on the fixed exterior, k and the declared vector. An independently supplied D134 initializer can be chosen large enough for a finite declared list as in D143. Induction gives closure and termination for the list. Since each block preserves actual cut membership, the composition of later translations is the D143 sum of lower shifts plus the sum of gap shifts on the upper side. At intermediate first-section boundaries apply the same later shifts to the appropriate sides, and shift only the displayed crossing weights. This yields immutable final labels and exact resource accounting as in D143, with no grafting or change of the original named graph.

The necessity and sufficiency apply to all prescribed physical gap quotas on this fixed five-vertex exterior and to the stated embedding only. D144's sufficient arbitrary-width packet theorem and its earlier scope are preserved. Independent exterior supply for other physical targets, and exact transfer geometry for other exteriors or variable widths, are separate questions. The recurrence is a symbolic result, with no numerical evaluation, placement sweep, or claim about arbitrary lobster gracefulness.
