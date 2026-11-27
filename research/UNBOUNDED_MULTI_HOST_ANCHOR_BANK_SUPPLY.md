# D226 — Unbounded multi-host odd-quota supply by moving terminal assignments

**PROVED WITHIN THE BANK-CAPACITY DOMAIN, PENDING DIRECTOR REVIEW.** For h≥6, even ℓ≥2 and odd j≥3 with ℓ+j=2h−3, take the named original `[[p],[q_1,...,q_ell],[r_1,...,r_j],[t]]`. All quotas are independently positive odd integers, with one chosen even-side interior quota at least 2h+3 and one chosen odd-side interior quota at least 2h−5. The other quotas, including both exterior ones, are arbitrary positive odd integers. The construction admits the sharper role-dependent bounds in Section 5 and includes physical reversal. The number of independently variable physical hosts is unbounded. [Named hand control](../evidence/validation/D226_UNBOUNDED_MULTI_HOST_ANCHOR_BANK_SUPPLY/HAND_CONTROLS.md)

## 1. Exact original, folded skeleton and independent unit supplier

The actual original T has consecutive spine vertices `s:0,s:1,s:2,s:3`. Each indexed branch `b:i:a` attaches to `s:i` and each `l:i:a:e` to that same branch, for 0≤e<Q at its declared quota Q. The two flank lists have one entry each. The folded tree S has the same named vertices and changes only `s:0--b:0:0` to `s:1--b:0:0` and `s:3--b:3:0` to `s:2--b:3:0`. The original is a lobster by its literal spine. Both graphs are trees because every off-spine branch attaches once to the spine and its terminals attach only to that branch.

There are 2h−1 branches, F terminal names and m=2h+2+F edges. Set the labels of `(s:1,s:2,s:0,s:3,b:0:0,b:3:0)` to (0,m,m−h+1,h+1,1,h). Use low slots [1,h+2] and high slots [m−h+1,m−1]. For k=1,…,h−1, put the entire pair {k,m−k} on a single folded root. The three unpaired low slots h,h+1,h+2 go right. Left needs (ℓ+2)/2 pairs and right (j−1)/2 pairs, totaling h−1. Put pairs 1 and h−1 left and pair 3 right. These are distinct at h≥6. The required capacities are at least two left pairs and one right pair, so any remaining unforced pairs fill the remaining places. For definiteness select unused pair indices in increasing order to fill the left count.

Pair 1 contains the left exterior center L₁ and even-side interior H₁. Pair h−1 contains the left spine end at high offset h−1 and low host L_(h−1). Pair 3 contains odd-side interiors L₃ and H₃. The unpaired right slots are the right exterior L_h, the right spine end h+1 and the right interior L_(h+2). Assign the selected even-side and odd-side bank names to H₁ and L₃ respectively, then assign each other actual interior name of each group in original order to its unoccupied slots in increasing label order, for example. The sharper theorem permits any lawful role assignment. High labels move with m at fixed offsets. These moves never exchange physical roles.

Each pair contributes attachment weights {k,m−k} at either folded root. Unpaired slots contribute [m−h−2,m−h] and the middle spine edge gives m. Hence the full folded skeleton spectrum, including all three spine edges, is [1,h−1]∪[m−h−2,m]. Folded exterior weights are 1 and m−h. The two literal original attachments give |m−h+1−1|=m−h and |h+1−h|=1. This exchange works for any F, so the original has the same complete skeleton spectrum. All other original and folded edges coincide. The six marks stay distinct since F≥2h−1 and m≥4h+1. [D217 fixed-label reconstruction](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source)

The terminal labels z must fill [h+3,m−h] and the terminal differences d must fill [h,m−h−3]. Put i=z−(h+3), w=d−h. The two required alphabets are [0,F−1]. The actual low host L_k of label k and high host H_k of label m−k satisfy
```text
L_k: w = i+3−k
H_k: w = F−1−k−i.
```
Every low is below the full terminal interval and every high above it, so these formulas are exact absolute endpoint differences. The active low labels are [1,h+2] except h+1, and high offsets are [1,h−2]. A complete allocation means a bijection between the two alphabets by such rows, each row at one actual host. For every subsequent growth step, label coverage then follows by adjoining the fixed-format skeleton labels and weight coverage follows by adjoining the skeleton spectrum just proved.

For F₀=2h−1, use D225 §4's four unit bases h=6,7,8,9 and its uniform h→h+4 step. This gives one row on each active numeric host and the row (F₀−1,F₀−1) at L₃. In the step, omitting old L₄ at (1,0) and the old maximum L₃ leaves the carried inputs [4,F₀+2] except 5 and weights [1,F₀−2] after the input translation by 4. Shift corresponding old low labels and high offsets by 4. Both affine rules hold at F₀+8. Restore the bottom and top rows and use the same eight-row packet from D225, whose new low and high weight declines partition [1,8]. Thus the same unit alphabets and maximum identity return, independent of physical pair placement. D225's shared-gap use of these marks needed pair h−3 on the right to put its high recipient there. D226 has no such recipient condition. Moving a whole pair before naming the unit rows preserves the two attachment weights as a set and leaves each numeric host's terminal rows valid. No cut hypothesis is used after initialization. [D225 bases and recurrence](THREE_INTERIOR_ODD_QUOTA_SUPPLIER.md#4-full-two-left-pair-supplier-for-h6)

Here and below integer intervals with reversed endpoints are empty. A row carries its actual existing terminal name throughout the construction. New rows are given the next terminal indices at their receiving host, in increasing order of their current input for that operation. The graph at a stage is the subgraph retaining the appropriate initial indices at each host. Only the final prescribed quantities of terminals are emitted.

## 2. A top identity block for growing any high host

Suppose the current allocation at F contains the top k identity rows (a,a) at L₃ for a∈[F−k,F−1], and H_k is an actual active branch. Let u≥0 and F′=F+2u. Move the k rows in order to the new top [F+2u−k,F+2u−1] in both coordinates. Translate all other rows by (u,u). For an ordinary low row w−i persists, and for an ordinary high row i+w increases by 2u just as F does. The moved block stays on identity host L₃. The old rows thus occupy [u,F+u−k−1] plus the new top block in each coordinate. This leaves
```text
[0,u−1] and [F+u−k,F+2u−k−1].
```
They are disjoint since k≤F. The actual new H_k reflection in F+2u−1−k sends the lower interval in reverse order onto the upper and vice versa. Give the 2u fresh indices to that host. This fills the exact vacant weights and preserves every old quota and incidence. It works for u=0 with empty fresh sets and unchanged old rows. The top k identity rows return, so the bank can service any finite sequence of offsets in nonincreasing order, by taking just the top k needed at a step. The construction guarantees those k after the step. It need not preserve a longer top interval when moving only its upper part. For k=1 this is D225's anchored high-host operation, with no shared-cut requirement.

## 3. Manufacture of the two banks

**At L₃.** Starting at the unit size F₀, give L₃ its full requested 1+2r quota. Shift each old row by (r,r) and put the r lowest and r highest new indices at L₃ by identity, as in D225's symmetric lift. The translated old maximum at F₀+r−1 and the new upper indices [F₀+r,F₀+2r−1] form a contiguous top identity block of r+1 rows. This uses exactly the target L₃ quota and no later operation increases that quota. In decreasing order, reach all requested high offsets k≥2 with k≤r+1 using Section 2. The top identity row remains available at the end.

**At H₁.** Apply Section 2 with k=1 and width v. At the new size M=F+2v, the fresh H₁ assignments are the lower indices [0,v−1] and their images [M−v−1,M−2] under reflection in M−2. In particular the host now contains both banks
```text
(a,M−2−a) and (M−2−a,a),   0≤a<v.
```
They are disjoint since F≥2h−1≥11. It is enough to start with the one top identity at L₃. If v=0 the construction makes no claim of newly supplied H₁ rows. The installable block length here is guaranteed by this installment itself. Any previously available H₁ rows remain on their actual host, with potentially changed coordinates.

## 4. Low-host growth and regeneration

Take an actual L_(3+d) with d≥1 and suppose the allocation at F has the top identity at L₃ and the H₁ rows (a,F−2−a) for 0≤a<d. These premises imply d≤F−1. Keep these d high input indices fixed, move their weights by 2u, move the top identity to F+2u−1, and translate all other rows by (u,u). This keeps the H₁ equation for the distinguished rows and all other affine relations, by the same sums and differences as in Section 2. The resulting occupied pieces and their complements are
```text
                 distinguished high    other old            top identity
inputs occupied  [0,d−1]               [d+u,F+u−2]          {F+2u−1}
weights occupied [F+2u−d−1,F+2u−2]     [u,F+u−d−2]          {F+2u−1}

inputs fresh     [d,d+u−1]             [F+u−1,F+2u−2]
weights fresh    [0,u−1]               [F+u−d−1,F+2u−d−2].
```
The input pieces occur in the order distinguished high, low fresh, other old, high fresh, top. The weight pieces occur in the order low fresh, other old, high fresh, distinguished high, top. Within each alphabet these intervals abut and partition the entire range. The two fresh intervals in each alphabet have length u and are disjoint since d≤F−1. The case d=F−1 just empties the middle occupied intervals. The actual map w=i−d sends the first input interval exactly to the first fresh weight interval and the second to the second. In particular all weights stay nonnegative and have no duplicates. Assign these fresh 2u rows to L_(3+d), keeping every old terminal at its old host and preserving the top identity and all d distinguished rows on H₁. At u=0 no row changes. Smaller d may use prefixes of this same bank.

For positive shift +d at L_(3−d), exchange input and weight coordinates **during the arithmetic only**. A low shift changes sign and a high row's sum equation is unchanged. The needed physical H₁ assignments before the operation are now (F−2−a,a) for 0≤a<d. Apply the preceding construction in the transposed coordinates and exchange them back. Its fresh actual inputs are [0,u−1]∪[F+u−d−1,F+2u−d−2] and actual weights [d,d+u−1]∪[F+u−1,F+2u−2]. The actual +d map sends each interval to its corresponding weight interval. All ordinary rows again satisfy their actual host rules. The new allocation retains the top identity and the returned high rows (F+2u−2−a,a) for the chosen d. This guarantee is for this orientation. The opposite orientation can be lost. For instance the first positive shift of width u>0 places its own row at i=0, so H₁ cannot have input 0 then. The schedule below provides the second orientation by a fresh H₁ enlargement. Neither transposition nor any other move changes the existing indexed edges.

## 5. Full operation order and exact admission

With a lawful role assignment as in Section 1 let Q be the requested quota at each actual branch and put
```text
K = max({1} ∪ {k≥2 : Q_(H_k)>1})
P = max({0} ∪ {3−k : k<3, Q_(L_k)>1})
D = max({0} ∪ {k−3 : k>3, Q_(L_k)>1})
r = (Q_(L_3)−1)/2
s = (Q_(H_1)−1)/2.
```
Here only actual branches enter the sets, and all half-increments are nonnegative integers. It suffices that r+1≥K and s≥P+D. Use the following order.

1. Build the unit assignment and set L₃ to its final quota. Grow each H_k with k≥2 whose quota exceeds one, in decreasing offset order, by its exact prescribed difference from one. Section 2 preserves enough identity rows for the next smaller offset.
2. At H₁ spend the first half-width P using just the top identity. This gives the transposed H₁ bank of depth P. Grow every positive-shift low host in decreasing displacement by its own prescribed increment. Section 4 preserves the orientation and enough depth for each subsequent smaller displacement.
3. At H₁ spend the remaining half-width s−P. The top identity survived, so the new rows from Section 3 supply a bank of depth at least D in the needed orientation. Grow each negative-shift low host in decreasing displacement by its own prescribed increment.
4. Emit the complete indexed labeling of S. Restore exactly the two original exterior attachments with the same labels.

An empty host class contributes no growth steps. In particular P=0 needs no inaugural H₁ manufacture and D=0 needs no bank for the final phase, though H₁ still receives its entire requested quota. A zero H₁ installment is valid. Only L₃'s initial phase increases its quota and only the two H₁ installments increase its quota. Every other growing host is visited once. The number of growth operations is finite, at most one for each host except H₁ which uses two. The unit recurrence takes exactly (h−h₀)/4 steps for the matching base h₀. Every traversal and new interval is finite for each finite input. Quota magnitudes are independent subject to admission. The prescription introduces exactly the prescribed original terminal indices, with each original edge attached to its required physical vertex. To reverse the physical spine send each name `s:i`, `b:i:a`, `l:i:a:e` to its counterpart with section 3−i and the other indices fixed. The entire original and folded incidence maps and the two restoration edges transport under that bijection.

Every active high offset is at most h−2, the largest possible P is 2 at L₁, and the largest D is h−1 at L_(h+2). Thus r≥h−3 and s≥h+1 suffice for every admissible role assignment, giving the uniform sufficient bank quotas 2h−5 at L₃ and 2h+3 at H₁. Unit flanks mean L₁ and L_h need no growth. Then P≤1, so Q_(H₁)≥2h+1 suffices with the same L₃ bound. This applies also when j=3 and all remaining pairs besides 3 lie left. There is no imposed pair h−3 side restriction. The nonunit-flank control meets the two uniform thresholds exactly.

## 6. Limits and comparison

The exact hypotheses of the individual transports are the stated block of top identities or the stated extreme reflected rows at the time the transport is used. The two sufficient quota inequalities guarantee those blocks through this schedule. Favorable preexisting assignments, other orders with different transports, or other geometries need not have those quota minima. The full arbitrary-quota domain without bank capacity is outside this theorem except where other retained constructions apply. No classification of that complement is asserted.

For a unit-quota imbalance-three allocation, a low-only block using the same set of indices as weights has zero sum of its row displacements, since both column sums coincide. Low 1 and low 2 are the only positive shifts (+2,+1), each available at most once. There is only one row of shift zero (low 3). Three distinct negative shifts have total magnitude at least 1+2+3=6, exceeding the entire positive budget of 3. The block therefore uses at most two positive, two negative and one zero row, or five rows. Equality in this count would require precisely shifts +2,+1,0,−1,−2. This bound concerns low-only invariant blocks at unit quotas in the claimed slot geometry. It places no capacity bound on packets involving highs, geometries with other offsets, variable quotas, or arbitrary graceful allocations.

D212 requires actual safe cuts and jointly matched dedicated gaps. D213 bounds that exact certification on its own family. D226 works with a complete affine resource bijection and moves old assignments across several stage-dependent intervals, including moving extreme rows independently of the ordinary translations. It neither invokes D212 nor changes D213. D216 reflects whole pooled branch components and tests two invariant palettes, whereas here all actual terminal parents are fixed and the new terminal rows are allocated by explicit affine maps. D221 also moves extreme identity and distinguished high rows at fixed host offsets in its four-parameter enlargement. Its subsequent constructions prove the full positive-even quota family with different geometry and transport premises. D223 supplies the affine laws and the precise separate-gap incompatibility, D224 the marking, and D225 the unit maximum, recurrence, symmetric identity manufacture and k=1 high operation. The successive movable banks reuse those premises where appropriate without assuming independent dedicated-gap insertions. This is a project-level mathematical comparison with the cited proofs. No historical priority is claimed. [D212](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md) · [D213](ALL_CENTER_SAFE_GAP_STRUCTURAL_LIMIT.md) · [D216](JOINT_POOLED_CLUSTER_REFLECTION.md) · [D221](INDEPENDENT_ALL_EVEN_MARKED_SUPPLY.md#2-four-independent-growth-parameters-on-the-d220-skeleton) · [D223](AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY.md#2-shared-insertion-and-its-exact-limitations) · [D224](TWO_LEFT_PAIR_PARITY_ADAPTED_SUPPLIER.md#3-new-two-left-pair-marking-with-a-high-suffix-row) · [D225](THREE_INTERIOR_ODD_QUOTA_SUPPLIER.md)

## 7. Retained two-interior corollary with arbitrary positive integer quotas

Keep unit flanks, even ℓ≥2, odd j≥3 and h≥5. Choose one actual branch in each interior, give those two arbitrary independently positive integer quotas, and keep every other quota one.

- **Odd and odd.** Use accepted D223 and D224, with D222 covering a unit boundary.
- **Opposite parity.** Use the explicit D224 §3 numerical unit bases and recurrence for h≥5 with cut (I,W)=(h−1,3), left pairs 1 and h−1 and right pair h−3. Their affine rows are independent of whole-pair side placement. The remaining pairs can fill any registered split, because left has capacity at least two pairs and right at least one. The recipients L_(h−1) and H_(h−3) are actual opposite-side interiors. Let A and B be the two requested increments from unit. Exactly one increment is odd, so G=A+B is odd. The local reflected gap of length G has one fixed singleton and otherwise pairs. Assign the singleton to the odd increment and divide the pairs to make exactly A and B, including zero on the even side if requested. This is precisely D222's singleton rule at these verified shared cuts. The old affine transport preserves each old assignment by the cut inequalities, even when m changes parity. The skeleton and the exchange 1↔m−h follow from the same endpoint identities for both parities of m.
- **Even and even.** D218 admits exactly one positive even interior quota on the even side and one on the odd side. Unit flanks, unit other quotas and the stated multiplicities meet its conditions, with physical reversal.

Assign either selected numerical role to its chosen actual indexed branch on that side. This proves the two-quota corollary, including named unit boundaries and reversal. It changes no general mixed-parity or same-side-two-quota scope. [D218](INDEPENDENT_RESERVED_MARK_TRANSFER_SUPPLIER.md) · [D222 singleton rule](PARITY_COMPATIBLE_ALL_ODD_SUPPLY.md#one-insertion-shared-by-host-4-and-high-host-m4) · [D223](AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY.md) · [D224 explicit unit geometry](TWO_LEFT_PAIR_PARITY_ADAPTED_SUPPLIER.md#3-new-two-left-pair-marking-with-a-high-suffix-row)
