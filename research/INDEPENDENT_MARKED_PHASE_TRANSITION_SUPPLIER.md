# D219 independent marked supply through a one-to-two-interval transition

**PROVED WITHIN EXACT SCOPE.** A selectable single-to-two-interval switch supplies the prescribed D217 marks for two unbounded positive-quota domains on the exact named four-section original. Domain A admits unbounded numbers of even interior quotas with positive odd flanks under the stated count conditions. Domain B admits independently positive even quotas everywhere, with at least one right interior quota at least four. There is an exact constructive admission rule for the declared phase recipe. Physical spine reversal and the no-switch D218 option are retained. [Named hand controls](../evidence/validation/D219_MARKED_PHASE_TRANSITION_SUPPLIER/HAND_CONTROLS.md)

## 1. Exact equal-length trimming lemma

Intervals are integer intervals. Begin with ordered, disjoint active terminal intervals [L,U], [V,W], with U<V, equal length n>0 and common cross-sum L+W=U+V=σ. All active terminals are attached to the actual current host v. The distinct next host w and v have labels outside the active palette. In the construction below they are outside its hull. They denote both fixed hosts and their labels where used in the arithmetic. Use the jump Δ=v+w−σ.

Retaining Q=2a terminals at v, keep a in each interval by trimming λ below and a−λ above the first transferred interval, and ν below and a−ν above the second. Thus with integer 0≤λ,ν≤a the moved intervals are
```text
[L+λ, U−a+λ] and [V+ν, W−a+ν].
```
Both have length n−a, positive exactly when a<n. Their cross-sums equal σ−a+λ+ν, so they equal v+w exactly when λ+ν=a+Δ. The integer sum of two choices in [0,a] ranges over every integer in [0,2a]. Hence the exact necessary and sufficient conditions for this nonempty equal-length reflected trimming are 0≤a<n and a≥|Δ|, with a integral. For example, λ=max(0,Δ) and ν=a+min(0,Δ) work under these conditions. They include a=0 when Δ=0. If a given trim is inadmissible, nothing about a different terminal geometry, a different ordering or ordinary gracefulness follows.

The retained labels count a per interval and have no intersection with either moved interval. The two moved intervals stay disjoint because they are subintervals of disjoint originals. Reflection in the sum v+w maps each onto the other, even when either has length one. For a moved terminal of label z, the new actual difference at w is |w−z|=|v−(v+w−z)|. This bijects the new differences with those on the actual moved edges at v, with multiplicity one in a graceful input. The label of each terminal and every unmoved incidence stay fixed. Each moved terminal name loses its unique edge at v and gains its edge at w. The next host is outside the terminal set, so the move maintains the tree. The returned active palette is attached to w and satisfies the same equal-length and cross-sum invariant. This is a necessity statement for the reflected trimming prescription, with no claim about arbitrary moves between general palettes.

A contiguous active interval [L,U] of length 2n splits at L+n into [L,L+n−1] and [L+n,U]. They have equal lengths, are disjoint and have cross-sums L+U. Splitting changes no labels or incidences.

## 2. Marked initialization, host jumps and phase invariant

Use the exact original `[[p],[q_1,...,q_ell],[r_1,...,r_j],[t]]`, keeping all its named vertices, original indices and positive quotas. Take even ℓ≥2, odd j≥3 and ℓ+j≥7. The original has spine `s:0--s:1--s:2--s:3`, with `b:i:u` and `l:i:u:e` in original zero-based order. Let R=ℓ+j+4=2h+1 count the branch slots and the two spine-end slots, F be the sum of the quotas, and m=2h+2+F be the edge count. Here h≥5. The actual roots `s:1,s:2` start at 0,m. Give the R slots [1,h+1] and [m−h,m−1], with actual `s:0,s:3` at m−1 and 5. The left and right exterior branch labels are 2 and 3. The six marks are therefore (0,m,m−1,5,2,3) in the D217 order. All quotas are positive, so F≥2h−1 and the numerical bands are separated.

As in [D218](INDEPENDENT_RESERVED_MARK_TRANSFER_SUPPLIER.md#1-exact-names-marks-and-initial-inventories), initially attach all slots to m and all actual terminals of labels [h+2,m−h−1] to slot 1, with the actual root edge 0--m. The terminal alphabet has length F. Along with the slots and roots it partitions [0,m]. Subtracting at m from the low slots gives [m−h−1,m−1], and subtracting the high slots from m gives [1,h]. The terminal edges at 1 give [h+1,m−h−2]. With the weight m these form a disjoint partition of [1,m]. This initial graceful tree uses precisely the original vertex set with temporary terminal and slot parents.

The positive host sequence is
```text
1,m−2,2,m−3,3,m−4,4,m−5,
then (k,m−k) for k=6,…,h,
then h+1.
```
It comprises 2h−1 distinct hosts, excluding only m−1 and 5 from the slot list. The initial sum of the active interval endpoints is m+1. Each transfer returns the current adjacent host sum as the new endpoint sum or cross-sum. Thus the jumps depend only on consecutive hosts and are independent of the trimming choices and the phase. The adjacent sums through m−5 alternate m−1,m,m−1,m,m−1,m,m−1. The next host is 6, including at h=5 where it is final, and that adjacent sum is m+1. Each later low-high pair has sum m, followed by a sum m+1 to the next low. Consequently the jumps are
```text
−2,+1,−1,+1,−1,+1,−1,+2,
then −1,+1 for each k=6,…,h.
```

Before a switch use the D218 one-interval rule, with end counts (Q+Δ)/2 and (Q−Δ)/2. The retained quota must be at least |Δ| and have its parity. The nonempty active remainder is contiguous and has endpoint sum v+w. After an optional switch before any positive host, require even quotas at that host and every later one, including the final. The current active length is the sum of these quotas and hence positive even. Split it into equal adjacent intervals as in Section 1. The active palette thereafter is two equal-length ordered intervals whose cross-sum is the preceding adjacent host sum, or m+1 if the split is at the first host. Apply Section 1 at each nonfinal even quota. Its half a satisfies a<n because the total remaining quota of the later hosts is positive even. The final host keeps all active labels with no more transfer. If the switch is at the final host, the split is available exactly when that quota is even and changes no edges. With no switch the final positive quota is unrestricted.

| Nonfinal departure | Single interval requirement | Two intervals requirement |
|---|---|---|
| Ordinary, magnitude 1 | Positive odd | Positive even, at least 2 |
| Special, magnitude 2 at 1 and m−5 | Positive even, at least 2 | Positive even, at least 4 |

Inductively each departed host retains precisely its quota and every remaining terminal is in the active palette. All future hosts are distinct slots outside the initial terminal interval. The disjoint retained and active labels partition the terminal alphabet at every step, and each move permutes exactly its old edge weights. A split leaves the weight multiset unchanged. The active palette always has the sum of remaining quotas as its size. Hence the procedure reaches final retention in finitely many steps, with a graceful seed whose terminal allocations meet all prescribed quotas.

## 3. Exact admission of quota counts and named relocation

The fixed complementary pairs and last slot have the following roles. Each listed branch gets its actual quota, and neither spine-end leaf is an active host.

| Slot or pair | Actual roles |
|---|---|
| 1, m−1 | One left interior branch, `s:0` |
| 2, m−2 | Left flank `b:0:0`, one left interior branch |
| 3, m−3 | Right flank `b:3:0`, one right interior branch |
| 5, m−5 | `s:3`, one right interior branch |
| h+1 | One remaining right interior branch |

For a proposed switch, inspect each actual slot's departure and its phase to obtain the parity and minimum from Section 2. At the final slot use the even-only rule after a switch or choose either parity for a no-switch input. The fixed flank quotas are tested at slots 2 and 3. For the mandatory interior roles first pick any required quota of at least four before allocating other even roles from its actual section. There is at most one such role per section, at 1 on the left or m−5 on the right. All other even minima are two and every odd minimum is one. Thus choosing a qualifying large even branch first leaves exactly the counts needed to test the remaining roles, without any further magnitude condition. If a qualifying branch or a parity count is absent, this choice of phase and final parity is infeasible.

The free pairs have indices {4}∪[6,h]. Pair 4 appears at consecutive active slots m−4,4, in that order. For k≥6 each free pair appears at consecutive slots k,m−k. Both departures in every free pair are ordinary. Relative to the single phase boundary a pair is OO, OE or EE. A straddling pair needs its earlier slot odd and later slot even. Because all free pairs occupy disjoint consecutive blocks, at most one can straddle. In particular an OE at pair 4 has its high slot odd. Any OE in the later list instead has its low slot odd.

Write A,B,C for the numbers of free OO, OE, EE pairs, respectively. Let L_O,L_E,R_O,R_E be the unused counts of actual branches after the mandatory roles. First require L_O+R_O=2A+B and L_E+R_E=B+2C. Assigning a,b,c free pairs of each type to the left is possible exactly under
```text
0≤a≤A, 0≤b≤B, 0≤c≤C,   a,b,c integral,
2a+b=L_O,   b+2c=L_E.
```
Necessity follows from the number of required parities per pair. For sufficiency select that many pairs of each type, choose the earliest in the host list if a deterministic choice is needed, and send every other pair right. The two total equations give the exact right parity counts by subtraction. Match each actual remaining branch to a slot of its parity in its own section, taking names in index order. This meets all minimum quotas because free pairs have only ordinary jumps. It uses the exact ℓ−2 remaining slots on the left and j−3 on the right, since summing the respective parity equations counts them. Together with the mandatory allocations this proves necessity and constructive sufficiency for each declared phase recipe. The finite menu of phase positions and count choices depends only on quota counts and minimum tests. It neither tries numerical vertex labelings nor changes the original order of branches.

With the assignments known the interval recursion determines the final retained palette at every actual host. Bind its sorted labels to that branch's original terminal indices before the initial temporary attachments. All those names then follow the transfer rule and end at their prescribed branches. Move precisely the left complementary slot pairs, including (1,m−1) and (2,m−2), from m to 0. Their actual two attachment weights change (m−k,k) to (k,m−k). Each moved component keeps its internal named incidences. The right pairs and the final slot stay at m. This gives exactly the named D217 fold, including all three original spine edges. The two folded exterior weights are (2,m−3). Restoring the actual two original outward edges exchanges them, since |m−1−2|=m−3 and |5−3|=2. It keeps the complete label and difference inventories by the accepted [D217 criterion](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source). Physical reversal uses the D218 index-preserving map `s:i ↦ s:(3−i)`, `b:i:u ↦ b:(3−i):u`, `l:i:u:e ↦ l:(3−i):u:e` and takes the two outward attachments with it.

## 4. Domain A with unbounded even interior counts

Take p,t positive odd and retain the above size hypotheses and their physical reversal. Suppose the left and right numbers of even quotas satisfy 1≤E_L≤ℓ−1 and 2≤E_R≤j−1. Reserve left even at 1, left odd at m−2, right odd at m−3, right even at m−5 and right even at h+1. These exist by the stated inequalities. No even quota at least four is needed. The remaining even and odd counts are
```text
e_L=E_L−1,      e_R=E_R−2,
o_L=ℓ−2−e_L,    o_R=j−3−e_R.
```
They are nonnegative, with each side's o and e of the same parity because ℓ−2,j−3 are even. Assume
```text
(e_L mod 2)+(e_R mod 2) ≤ 1,
floor(o_L/2)+floor(o_R/2) ≥ 1.
```
On each actual side form floor(o/2) OO pairs and floor(e/2) EE pairs. If its counts are odd, the residual odd and even form one OE. The first inequality gives at most one OE across both sides. The second provides at least one OO for index 4. These pairs account for exactly h−4 free pairs and satisfy the per-side capacity equations. Choose one OO pair for index 4, then order the later pairs from index 6 upward as the remaining OO pairs, the optional OE with its low slot odd, and the EE pairs.

Stay in the single interval through the special departure at m−5. The earlier departures are permitted because both flanks and m−2,m−3,m−4,4 are odd and 1,m−5 are even. After m−5, switch immediately before the first even slot among later free pairs and the even final host. Any remaining odd slots precede it, including the low slot of an OE. The suffix is entirely even. All its jumps are ordinary, so the minima are met. If that first even is the final host, the split is a terminal split as described in Section 2. Thus the advertised sufficient domain holds for arbitrary magnitudes of the specified parity.

For h=5, the two size splits are (2,5) and (4,3). There is only pair 4, so the inequalities force it OO and e_L=e_R=0. It belongs right for the first split and left for the second. The switch may be at the even final slot 6, and both special jumps remain in the single interval. For larger h the proof includes no OE, a last OE with no EE, and no later free pairs after all the OO pairs. The conditions are exact for the stated grouping with index 4 assigned OO and an even final slot. They are used here as sufficient conditions for the full phase recipe, which also permits other switch positions where appropriate. Counts of positive even quotas can grow on both sides, for example with e_L=ℓ−4 and e_R=j−3 for all even ℓ≥4 and odd j≥3. In that family o_L=2 and o_R=0, so the two tests hold.

## 5. Domain B with all quotas independently even

Now let every actual branch quota, including p,t, be positive even, and suppose some right interior quota is at least four. Assign that quota to m−5 before assigning any other right interior role. All pairs can be filled as in Section 3 with the remaining even quotas, and the last slot takes a remaining right even quota. Use the single interval for the first departure at 1, with Δ=−2 and a positive even quota at least two. The remaining active length is even, as every remaining actual quota is even. Split before m−2 and use the two-interval rule for every later transfer. All ordinary jumps have magnitude one and each such Q is at least two. The special jump +2 at m−5 is permitted by the assigned quota at least four. The final keeps both intervals, and every nonfinal active residual is positive by Section 2. This works for both h=5 splits as well as all larger sizes, independently of every even magnitude subject to the one stated minimum. In the reversed physical original that minimum transfers to the odd-sized interior side.

For entirely even inputs, the minimum-four condition on some right quota is also necessary within this fixed recipe. An even second quota at m−2 cannot be retained in one interval at jump +1, so any admissible switch has already occurred by that departure. The later jump +2 at the right slot m−5 therefore requires a≥2 there.

The entirely quota-two case is adverse for the declared architecture. A split at the first host fails its magnitude-two jump with a=1. The switch must follow the first departure and precede the second. Later the magnitude-two jump at m−5 fails a≥2 because its quota is also two. No declared switch or no-switch choice works on this host order. This obstruction is for the fixed equal-length trimming recipe and the given order. It leaves other palettes, orders, marks and ordinary gracefulness undecided. [Positive and adverse hand records](../evidence/validation/D219_MARKED_PHASE_TRANSITION_SUPPLIER/HAND_CONTROLS.md)

## 6. Retained mechanisms and architectural reassessment

The exact pinned [N145 arithmetic for Hrnčiar–Haviar Case 1.1.1](../references/upstream/mdl/N145_retained_record.md#actual-hh-extreme-center-inputs) uses the all-at-m graceful inventory, an odd single-interval phase and an even two-interval phase. Its positive-one move trims with (λ,ν)=(a,1), and its negative-one move uses (a−1,0). Both are instances of Section 1. N145 switches after an odd-quota phase on its full alternating host list. The D219 combination uses the D218 reserved spine-end slots and their unequal jumps, enables the independent trimming formula for those jumps, and proves the precise named D217 restoration with the fixed marks. The ordinary source theorem does not supply those marks. The Hrnčiar–Haviar publisher abstract is accessible through its index, but the direct PDF returned HTTP 403 and the earlier local original is unavailable. The arithmetic comparison rests on the pinned previously inspected case, and this proof establishes every used step independently. No historical priority or complete literature nonoverlap follows. [Hrnčiar–Haviar primary publication](https://www.sciencedirect.com/science/article/pii/S0012365X00002338)

The conserved attachment differences in each terminal move and paired component move use the established fixed-label reflection identities. The final two-edge exchange is the exact D217 restoration. D217 supplied marked finite and two-parameter families. D218 removed the fixed multiplicity and retained a parity-limited single interval. D219 broadens independently even quotas and flanks through the even suffix, without requiring additional safe cuts or extracting any solution from the eventual original. [Mishra–Panigrahi component moving, pp. 259–260](https://dml.cz/bitstream/handle/10338.dmlcz/140703/MathBohem_135-2010-3_3.pdf#page=4)

Across the three investigations the most consequential remaining supply obligation is independently constructing an admissibly marked source for freely interleaved quota parities and small even quotas, or decomposing them into components that compose with those marks. This is separate from testing another fixed parity family. The restoration itself conserves the two weights by an exact criterion. The current difficulty is the compatibility of marks, host motion and both inventories during independent supply. The one-switch recipe constrains mixed pairs and the special jump and supplies no move back to a single interval after an even suffix starts. Arbitrary parity profiles, zero quotas, smaller sizes and composition of independently labeled ordinary clusters are outside the established phase result. An architecture that supplies marks with another host order, richer terminal palettes or a separate compatible decomposition should be compared on its ability to handle that obligation. No successor is selected.

A narrowly falsifiable diagnostic question for Director consideration is whether the exact all-quota-two profile `[[2],[2,2],[2,2,2,2,2],[2]]` has a graceful D217 folded source with precisely the marks (0,30,29,5,2,3), allowing all assignments to the other named vertices and imposing no transfer order or palette rule. This one 30-edge target separates failure of the equal-length trimming recipe from failure of the fixed mark itself. A witness would establish the stronger marked source on this target, and a separately justified complete negative would concern these marks only. This is an assessment of diagnostic leverage, not a selected task. No preparation or execution occurred.

All accepted earlier scopes and the historical incomplete, held and deferred records remain as recorded, including all three D212 certificate dispositions.
