# D218 independent reserved-mark transfer supplier

**PROVED WITHIN EXACT SCOPE.** The exact named original `[[p],[q_1,...,q_ell],[r_1,...,r_j],[t]]` has a graceful labeling supplied through the D217 marked fold on the entire declared parity domain. The two positive odd flank quotas vary independently. The left list has even size ℓ≥2 and exactly one positive even quota. The right list has odd size j≥3 and exactly one or two positive even quotas. All other interior quotas are positive odd, and ℓ+j≥7. Each quota magnitude is independent within its specified parity. Physical spine reversal gives the reflected domain on the actual names. [Named hand control](../evidence/validation/D218_RESERVED_MARK_TRANSFER_SUPPLIER/HAND_CONTROL.md)

## 1. Exact names, marks and initial inventories

Use the named spine `s:0--s:1--s:2--s:3`. The b- and l-names use the original zero-based section, branch and terminal indices. The subscripts of q and r in the profile specify their ordered entries. Each original branch has a positive quota. Distinguish the actual two spine-end vertices `s:0,s:3`, which are leaves in the folded source, from all terminal names.

Let R=ℓ+j+4=2h+1 count the off-root slots, consisting of the ℓ+j+2 actual branch vertices and the two spine-end leaves. Then h≥5. Let F=p+t+Σqᵢ+Σrᵢ count the actual terminals, and m=R+1+F=2h+2+F. This is the edge count of both the original T and its D217 fold S. The F terminal labels will be placed by a transfer sequence on the 2h−1 positive-quota hosts. The two spine ends receive zero of these terminals. There are at least two positive even quotas, so F≥(2h−1)+2=2h+1. This gives m≥4h+3≥23.

Give the actual roots `s:1,s:2` labels 0,m. The R distinct slot labels are [1,h+1] and [m−h,m−1]. The remaining labels [h+2,m−h−1] have length F. The labels therefore fill [0,m] disjointly. Assign slots to their actual names by Section 3. Initially join 0 to m, join every slot to m, and join all F actual terminals to the actual slot of label 1. This initial tree has the following difference inventory.

| Actual initial edge type | Differences |
|---|---|
| Root edge | {m} |
| Slot edges to m from [1,h+1] | [m−h−1,m−1] |
| Slot edges to m from [m−h,m−1] | [1,h] |
| Terminal edges at label 1 | [h+1,m−h−2] |

These intervals and the singleton partition [1,m]. Every slot is outside the entire terminal interval. The two reserved spine-end labels are a=m−1 and b=5. The two exterior branch labels are c=2 and d=3. The marks x=0, y=m, a=m−1, b=5, c=2, d=3 are distinct because h≥5 and m≥23. The temporary attachments supply the proof using exactly the original vertex set.

## 2. Exact transfer lemma and parity schedule

Suppose an interval [L,U] of terminal labels is currently attached to one actual host v. The distinct next host w has no terminals from it, and both fixed host labels are outside [L,U]. Let Q be the quota to retain at v, with 0≤Q<U−L+1. Keep λ lowest and μ highest labels, λ+μ=Q, and transfer the remaining leaves to w. The moved interval is [L+λ,U−μ]. Its old and new attachment-weight multisets agree exactly when its endpoints sum to v+w. To see necessity, on the same side of a nonempty moved interval the two hosts give different minimum weights, obtained at the same endpoint. On opposite sides equality of the minimum weights equates the distance from the low host to the lower endpoint with the distance from the high host to the upper endpoint. This gives the endpoint sum, even for a singleton. Once that sum holds, z↦v+w−z permutes the interval and preserves the multiset. Thus the unique end counts for this interval transfer are

```text
Δ = v+w−(L+U)
λ = (Q+Δ)/2
μ = (Q−Δ)/2.
```

They are nonnegative integers exactly when Q≥|Δ| and Q≡Δ mod 2. Both are at most Q and their sum is smaller than the interval size, so the residual is nonempty. Any empty retained end contributes no labels. Reflection pairs every moved label with a unique moved label, including a possible fixed midpoint. The actual changed attachment difference at w on leaf z is |w−z|=|v−(v+w−z)|. This is a permutation of the old differences on exactly the moved leaves. The old and new actual edges join the same leaf name to distinct hosts outside the interval. All other edge differences and labels persist. Moving degree-one vertices between fixed vertices of the connected nonterminal tree maintains a tree and creates no duplicate edges. The end counts are necessary for this symmetric cut of the interval. They supply the stated transfer by actual arithmetic.

Use the following list of distinct positive hosts, in order:
```text
1, m−2, 2, m−3, 3, m−4, 4, m−5,
then k, m−k for k=6,…,h,
then h+1.
```
It omits exactly the reserved slots m−1 and 5, and contains 2h−1 positive hosts. For h=5 the middle list is empty, and m−5 transfers directly to the final host 6. In either case the next host after m−5 is 6. The initial interval has endpoint sum m+1. Each move changes that sum to the current adjacent host sum. The full progression is recorded below.

| Departure and recipient | New sum | Δ from the preceding sum |
|---|---:|---:|
| 1 → m−2 | m−1 | −2 |
| m−2 → 2 | m | +1 |
| 2 → m−3 | m−1 | −1 |
| m−3 → 3 | m | +1 |
| 3 → m−4 | m−1 | −1 |
| m−4 → 4 | m | +1 |
| 4 → m−5 | m−1 | −1 |
| m−5 → 6 | m+1 | +2 |
| k → m−k for 6≤k≤h | m | −1 |
| m−k → k+1 for 6≤k≤h, including the final h+1 | m+1 | +1 |

In the repeated rows the two moves alternate for each k. Thus host 1 requires a positive even quota with minimum 2, and m−5 requires the same. All other nonfinal hosts require positive odd quotas with minimum 1. At each step the interval length is the total of the current and subsequent prescribed quotas. Retaining the current Q and moving the rest leaves a nonempty interval because a later positive quota remains. The last h+1 receives exactly its quota and keeps the whole remaining interval, with no parity constraint. This gives 2h−2 transfers and a final retention. None of their requirements imposes a relationship between quota magnitudes. In particular the computation works for either possible parity of m.

## 3. Assign all slots and recover the folded source

Place the actual branch and spine-end names in the complementary pairs (k,m−k), 1≤k≤h, and the unpaired slot h+1 as follows.

| Slots | Actual names or permitted group |
|---|---|
| 1, m−1 | Unique left even branch, `s:0` |
| 2, m−2 | `b:0:0`, one left odd branch |
| 3, m−3 | `b:3:0`, one right odd branch |
| 5, m−5 | `s:3`, one right even branch |
| h+1 | One remaining right branch |

If the right list has one even quota, its branch at m−5 is the even one. There are at least two right odd branches, so use one at m−3 and another at h+1. If the right list has two evens, assign them to m−5 and h+1. There is then at least one right odd branch for m−3. In both cases every other right branch has odd quota. On the left, ℓ≥2 ensures an odd branch at m−2, leaving ℓ−2 odd branches. The flanks have their input positive odd quotas p and t at labels 2 and 3. Thus all nonfinal departure quotas obey Section 2.

The available pair indices are {4}∪[6,h], of size h−4. Allocate (ℓ−2)/2 of these pairs to the remaining left interior names and (j−3)/2 to the remaining right names. These are nonnegative integers with sum (ℓ+j−5)/2=h−4. Their slots exactly accommodate the remaining odd quotas in each group. For a deterministic procedure, one can pick required parity representatives in original index order, use the earliest remaining pair indices for the left group, and distribute the leftover names of each group in index order to its slots. The displayed assignments only choose labels for named vertices. They do not reorder the actual original branch lists.

The label-only transfer recursion now gives an explicit retained set of the required size for each actual branch. Bind its labels in increasing order to its original terminal indices. This can be done before forming the initial tree. All these same terminal names are temporarily joined to host 1, and transfers reattach each named terminal according to its assigned label until it reaches its final host. Each later host begins without terminal leaves, each prior host keeps its prescribed leaves, and the fixed slot attachments to m are untouched during this phase. Terminal sets are disjoint and partition the original terminal alphabet.

Move precisely the left pairs, including the two designated pairs (1,m−1) and (2,m−2), from root m to root 0. Move both actual slot components of each such pair with their terminal incidences intact. The slots are outside the root edge and their components are disjoint before the move. For a pair (k,m−k), the two actual root weights change from (m−k,k) to (k,m−k). Every moved component still has one root attachment, so all differences and all vertex labels remain valid. The right pairs, the right final host h+1 and the connector 0--m stay fixed.

The left spine-end leaf `s:0` is now joined to `s:1`; the right spine-end leaf `s:3` remains joined to `s:2`. The left exterior branch and every left interior branch have parent `s:1`. The right exterior branch and every right interior branch have parent `s:2`. Thus the exact graph is the named D217 folded source S, with all three original spine edges and every original terminal index and parent. The fold attachments are from labels 0 to 2 and m to 3, with differences (2,m−3).

Restore just the two outward attachments. Their endpoint differences are |m−1−2|=m−3 and |5−3|=2. The weights exchange and every other incidence and label remains, proving the bijection and difference partition on the actual original. This directly meets the accepted [D217 iff](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source). The proof uses no ordinary diameter-five existence theorem to fill its marks. All assignment and transfer steps terminate for each finite input.

## 4. Boundary and reversal checks

When h=5, ℓ+j=7. The allowed ordered sizes are (2,5) and (4,3). The only remaining pair (4,m−4) is assigned wholly right in the first case and wholly left in the second. At m−5 the active interval has sum m−1 and the next label is 6. The jump is +2 even at this minimum. The final quota at 6 can be odd or even, so both right-even-count cases work for both multiplicity allocations. In particular j=3 with two even quotas uses its only odd branch at m−3, both even slots as stated and no other right pairs. For arbitrarily large allowed sizes and magnitudes, pair availability uses only counts and the inequalities in Section 2 use only the stated parity and its minimum. The operating intervals may grow freely.

The control `[[1],[2,1],[1,2,1,1,1],[1]]` has h=5, F=11 and m=23. Its exact indexed labels, transfer sequence and both resulting 23-weight inventories are checked separately. The proof uses this as a hand check rather than an existence assumption. [Exact control](../evidence/validation/D218_RESERVED_MARK_TRANSFER_SUPPLIER/HAND_CONTROL.md)

For physical reversal, apply the construction in the orientation where the even-sized interior group is read first. Transport along the actual map `s:i ↦ s:(3−i)`, `b:i:j ↦ b:(3−i):j` and `l:i:j:e ↦ l:(3−i):j:e` between the two readings. The physical spine edges and the two rewires are carried to their respective original incidences, and each section's internal index order is preserved. In the reversed physical reading the spine tuple is (5,m,0,m−1) and the exterior branch labels are (3,2). The exchanged weights occur in reverse order. This proves coverage of the reflected domain without any assumption of equal quotas or of graph symmetry.

## 5. Retained mechanisms, ordinary coverage and next scope

The exact retained [N145 construction](../references/upstream/mdl/N145_retained_record.md#actual-hh-extreme-center-inputs) expands Hrnčiar–Haviar Case 1.1.1. D218 shares its initial all-at-m inventory, alternating low/high host geometry, reflection of transferred terminal palettes and final moves of complementary branch pairs. In N145 the positive branch hosts use the full alternating list and the even-quota tail uses a two-interval transfer. D218 reserves two actual leaves, avoids those slots in the active order and keeps one interval. The resulting two jumps of magnitude 2 admit the specific even hosts while fixing the six numeric marks. N145's stated block case requires positive quotas with particular branch parity counts and no direct leaves at the central roots. It does not give these marked folds. The Hrnčiar–Haviar publisher abstract identifies the ordinary diameter-five result. Direct article and PDF access returned 403, and the earlier local original was unavailable in this session. The construction comparison relies on the pinned N145 arithmetic and prior access recorded there and in D217. The D218 proof is self-contained and does not infer any marked-port promise from ordinary source existence. [Primary Hrnčiar–Haviar publication](https://www.sciencedirect.com/science/article/pii/S0012365X00002338)

Reflecting the retained transfer interval pairs the unchanged leaf labels and swaps differences when their host changes. The subsequent component moves use the standard same-donor pair-sum rule of Mishra–Panigrahi, Definition 2.2 and Lemma 2.3(i), whose recipient lies outside the moved components. The last two restorations instead exchange two weights across distinct donor and recipient pairs as in D217. These are comparisons of operations. No historical novelty is claimed. [Mishra–Panigrahi, pp. 259–260](https://dml.cz/bitstream/handle/10338.dmlcz/140703/MathBohem_135-2010-3_3.pdf#page=4)

Every D218 original has diameter seven. Both exterior positive quotas produce a seven-edge path between exterior terminals, and all other vertex distances are bounded by the length-three spine plus two edges at each end. Any longest path must use both extreme spine sections at depth two, so its truncation by two edges at each end is the displayed spine. Its degrees in T are (2,ℓ+2,j+2,2). The odd-degree vertex remains interior under reversal. Thus the stated central-path degree hypothesis in the inspected Mishra–Panigrahi 2010 class, with all vertices except possibly the last even, does not apply to these originals. In addition, at least two distinct branches have even positive quotas at least two. Within any matching each such branch leaves an unmatched terminal because its terminals share one neighbor. The known lobster perfect- and almost-perfect-matching hypotheses therefore do not apply. These are checks of particular published hypotheses, with no assertion of absence of other ordinary-family overlap. [Mishra–Panigrahi, p. 257](https://dml.cz/bitstream/handle/10338.dmlcz/140703/MathBohem_135-2010-3_3.pdf#page=2) · [Matching-theorem context](https://arxiv.org/pdf/1402.3994)

[D216](JOINT_POOLED_CLUSTER_REFLECTION.md) combines a root-zero pool with a shell and later reflects whole components subject to two invariances. D218 works on the full named vertex set from the start and moves branches at fixed labels after distributing terminals. Its paired moves conserve weights directly and need no reflected component palette. The D216 all-unit family and its fixed mixed controls retain their separate premises. [D217](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md) supplied the exact restoration iff and a fixed-multiplicity construction with two quota growth parameters. D218 uses that same fixed-label restoration and independently supplies its marked source for unbounded interior multiplicities and all independently variable declared quota magnitudes. [D209](ORDINARY_SPINE_TWO_SIDED_ORDINARY_SUPPLIER.md), [D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) and [D211](ORDINARY_SPINE_COORDINATED_FOUR_HOST_SUPPLIER.md) work with the named single-right-branch profiles and their own compatible-core or simultaneous-palette premises. D218 has at least three branches on the odd-sized interior side, so it does not assert inclusion of their named domains. Both routes use exact joint inventories.

The parity restrictions are sufficient for this precise transfer order and slot assignment. A quota of the wrong parity or below |Δ| at a nonfinal host defeats that symmetric interval cut. Such failures do not exclude another order, another labeling, another marked supplier, or ordinary gracefulness. Unrestricted parity, zero quotas, smaller multiplicities and arbitrary independently labeled cluster composition remain beyond the proved D218 domain. All prior incomplete, held and deferred dispositions stay as recorded. No diagnostic was prepared or run, and no successor was selected.
