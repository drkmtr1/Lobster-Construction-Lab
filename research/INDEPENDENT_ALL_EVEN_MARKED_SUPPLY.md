# D221 — Independent all-even marked supply

**PROVED WITHIN EXACT SCOPE.** Every original `[[p],[q_1,...,q_ell],[r_1,...,r_j],[t]]` with independently positive even quotas, even ℓ≥2, odd j≥3 and ℓ+j≥7 admits an explicitly supplied graceful labeling. The result includes physical spine reversal. The proof combines the retained D219 domain with two new transfer orders and a four-host joint allocation that leaves a contiguous remainder. [Named hand controls](../evidence/validation/D221_INDEPENDENT_ALL_EVEN_MARKED_SUPPLY/HAND_CONTROLS.md).

## 1. Original incidence and numerical resources

In the original T the spine is s:0--s:1--s:2--s:3. Branch vertex b:i:u at position u of section i is attached to s:i. Each terminal l:i:u:e is attached to b:i:u, with the unchanged original zero-based index e. The lists in the profile specify the original branch names and quotas before any label is assigned. The folded tree S moves only b:0:0 and b:3:0 inward to s:1 and s:2, respectively. The two graphs have the same named vertex set. In both, branches attach singly to the spine and keep all terminal incidences. When the two restored differences exchange the two folded differences, gracefulness of S gives gracefulness of T with labels fixed. [D217 reconstruction criterion](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source).

Write ℓ+j=2h−3, so h≥5. There are 2h−1 positive branch hosts, F=p+t+Σq_i+Σr_j terminals, 2h+1 slots (hosts and two spine ends), and m=2h+2+F edges. In particular F≥4h−2 and m≥6h. Give roots s:1,s:2 labels 0,m. In all new constructions the slots use [1,h+1] ∪ [m−h,m−1]. Each complementary pair {k,m−k} for k∈[1,h] is assigned wholly to one folded root. The unpaired slot h+1 belongs to the right root. Then each pair yields weights k,m−k in either assignment, the unpaired slot gives m−h−1, and the literal root edge gives m. The skeleton spectrum is [1,h] ∪ [m−h−1,m]. There must be (ℓ+2)/2 whole pairs on the left and (j+1)/2 on the right. These counts include the flank at each root and the two spine ends as slots.

The remaining labels z are [h+2,m−h−1] and weights d are [h+1,m−h−2]. In normalized coordinates i=z−(h+2) and w=d−(h+1), both ranges are [0,F−1]. A low host k maps w=i−(k−1). A high host m−k maps w=F−1−k−i. These formulas follow by absolute subtraction at the actual hosts, which are outside the whole terminal interval. Drift of a high label with m is accounted for by the second formula. Specifying complementary pair assignments and exact terminal sets at all hosts supplies every named vertex. When assigning any available slots to indexed branches of given quotas, choose the lowest available index among equally eligible names, and assign terminal labels to the actual indices in increasing order. Temporary transfers may instead transport leaves to their final indices after the sets are calculated. This transport preserves every final host and quota. Empty integer intervals below represent no labels.

## 2. Four independent growth parameters on the D220 skeleton

At h=5 the slot scheme of D220 puts {1,2,28,29} at root 0 and {3,4,5,6,25,26,27} at root 30. In its variable-size version the high slots are m−1 through m−5. The marks in (x,y,a,b,c,d) order are (0,m,m−1,5,2,3). The folded weights 2,m−3 exchange under restoration. The seed terminal rows in normalized coordinates follow. [D220 named seed](../evidence/validation/D220_DIRECT_JOINT_FIXED_MARK_ALLOCATION/HAND_CONTROLS.md#fixed-mark-arm-a-positive).

| Host | i | w |
|---|---|---|
| 1 | 16,17 | 16,17 |
| 2 | 7,15 | 6,14 |
| 3 | 9,14 | 7,12 |
| 4 | 8,13 | 5,10 |
| 6 | 5,6 | 0,1 |
| m−5 | 3,4 | 9,8 |
| m−4 | 2,10 | 11,3 |
| m−3 | 1,12 | 13,2 |
| m−2 | 0,11 | 15,4 |

### A. Split one insertion between hosts 3 and m−2

The table gives i≥9 iff w≥7 for each low row and i≥9 iff w<7 for each high row. For any G=2(α+β)≥0, increase F from 18 to 18+G and add G to indices i≥9 and weights w≥7. For a low row, both shifts agree. For a high row the offset F grows by G, so exactly one of i and w must grow by G, as the table verifies. Both old inventories embed injectively.

The unused index and weight intervals are [9,8+G] and [7,6+G]. Locally write i=9+u, w=7+v. The low host 3 gives v=u and the high host m−2 gives v=G−1−u. The reflection has G/2 disjoint two-element orbits when G is positive even. Give α whole orbits, chosen in increasing order of their smaller element, to host 3 and the remaining β to m−2. Each assigned orbit covers its exact two coordinates on both inventories under the appropriate map. At G=0 both fresh ranges are empty. The top two indices still belong to host 1 and the row i=0,w=F−3 still belongs to m−2. This construction gives independent quotas 2+2α and 2+2β.

### B. Enlarge host 2 while moving two existing types of row

Let F be the size just returned by A and put M=F−2. Temporarily set aside the two maximum identity rows of host 1 and the distinguished high row (0,M−1) of host m−2. All other rows have index alphabet [1,M−1] and weight alphabet [0,M−2]. Increase F by 2s, and shift both coordinates of every such row by s. This preserves each low relation and preserves each high relation because i+w and F increase by 2s. Place the distinguished row at (0,M+2s−1), which is precisely the high formula with its same offset 2. Host 1's two original terminal rows now occupy indices and weights M+2s,M+2s+1, the new maxima.

The shifted rows fill indices [s+1,M+s−1] and weights [s,M+s−2]. The uncovered indices are [1,s] ∪ [M+s,M+2s−1], and their images under host 2's map w=i−1 are exactly the uncovered weights [0,s−1] ∪ [M+s−1,M+2s−2]. Give these 2s new rows to host 2. The argument also applies at s=0 with both intervals empty. It preserves the quotas set by A and all original terminal counts other than the enlarged host 2.

### C. Enlarge host 1

Increase the resulting F by 2r. Shift every existing i and w by r. The low formulas persist and the high formulas still hold by the same 2r increment in i+w and F. The fresh outer intervals [0,r−1] and [F+r,F+2r−1], using the pre-operation F, are the same on the two inventories. Give the new intervals to host 1 by the identity map. This operation works for r=0 and leaves the quotas at every other host as returned by A and B.

The prescribed order A, B, C therefore gives the entire family `[[2+2s],[2+2r,2+2β],[2,2,2,2,2],[2+2α]]` with independent α,β,s,r≥0. If retaining old terminal names in successive enlargements, carry each old row to its specified new row and append the fresh rows at new indices. This changes no old incidence and leaves all old names present. For one-shot supply the final sets can be assigned in increasing-label order to all original indices. The set of slots and their skeleton differences obey Section 1 for each new m. The changes in normalized coordinates thus give actual graceful folded and restored graphs.

For (ℓ,j)=(4,3), move the whole pair {4,m−4} from the right folded root to the left folded root, exchanging its two attachment weights. Neither is a marked exterior center or a spine end. No terminal assignment changes. Both quotas in this pair remain two, so any two of the four left indices with quota two can occupy it and the two other left quotas go at 1,m−2. The right interior hosts are m−3,m−5,6. Together with the retained D219 minimum-four route, these operations alone supply all (2,5) inputs and the stated (4,3) subdomain and their reversals.

In A, on the D220 seed the shared graph cut at label 16 in S and T has crossing spectrum [13,30]. The terminal rows give this from the two threshold equivalences above. The large skeleton differences cross it and the small ones stay on a side. The two host constants agree, since 16−3=28−16+1=13. A uses one shared gap, splitting it across two hosts by reflection orbits. D212 assigns dedicated gaps at distinct jointly compatible cuts. B and C are proved by residual inventory transport with explicit moves of assignments, rather than invoking safe-cut coefficient conditions. These results leave the D213 all-center bound intact. [D212 matched safe-gap theorem](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md) · [D213 structural limit](ALL_CENTER_SAFE_GAP_STRUCTURAL_LIMIT.md).

## 3. Even h — flexible marks

Let h≥6 be even. Set (a,b,c,d)=(m−1,h+1,h/2,h/2+1), with x=0 and y=m. Reserve a,b for the two spine ends. All six marked labels are distinct because h/2≥3, d≤h, and the low and high bands are disjoint. Put pairs of indices 1 and c on the left, and the pair of index d on the right. The pair at 1 contains a and a left interior host. The pair at c contains the left exterior host and a left interior host. The pair at d contains the right exterior host and a right interior host. Put (ℓ−2)/2 other pairs left and (j−1)/2 other pairs right. This uses exactly h pairs and the unpaired right reserve. All quotas remain attached to their named host roles.

Initially put all slots at root m and all terminals at label 1, with the root edge fixed. The slot weight bands are exactly the bands calculated in Section 1, and the terminal weights are [h+1,m−h−2]. The active interval [h+2,m−h−1] has sum m+1. Use the sequence of low k followed by high m−k−1 for k=1 through h−1, then final low h. It uses every positive host once. The successive adjacent sums alternate m−1,m, starting m−1. The first departure has jump −2, so the D218 single-interval end counts (Q−2)/2 and (Q+2)/2 apply for every positive even Q. These leave a nonempty even-length interval. Split it in halves and use the D219 equal-length two-interval rule on all later moves. At a nonfinal host Q=2a there is a positive later quota, so a is strictly smaller than the current half-length. Each later jump has magnitude one and a≥1. Choose lower end trimming counts λ,ν∈[0,a] with λ+ν=a+Δ, for example λ=max(0,Δ), ν=a+Δ−λ. The retained theorem shows the moved pair of intervals has equal positive length and the new cross-sum v+w, so reflection preserves all moved weights. Every departure leaves its quota and all final terminals stay at h. The order is finite. [D218 one-interval arithmetic](INDEPENDENT_RESERVED_MARK_TRANSFER_SUPPLIER.md#2-exact-transfer-lemma-and-parity-schedule) · [D219 equal-length rule](INDEPENDENT_MARKED_PHASE_TRANSITION_SUPPLIER.md#1-exact-equal-length-trimming-lemma).

Moving the prescribed whole pairs left exchanges their attachment weights and leaves every terminal edge at its assigned host. This gives the exact folded graph. Its marked folded weights are c,m−d. The restored weights are m−1−c=m−d and h+1−d=h−c=c. Hence every even h≥6 is supplied for all positive even quotas.

## 4. Odd h with an enlarged left interior quota — move the high reserve

This supplies the case where some left interior quota is at least four. Choose e=2 for odd h≥7 and e=4 at h=5. Reserve a=m−e on the left and b=h+1 on the right, and use
```text
c=(h+1−e)/2,   d=(h+1+e)/2 .
```
Here c,d∈[1,h], they are distinct from each other and from e. For h≥7, c≥3 and d≥5, while h=5 gives c=1,d=5. Use pairs e,c on the left and pair d on the right, and the same other-pair counts as in Section 3. At pair e the low host e receives any selected left interior quota of at least four. The high slot of pair e is the reserved left spine end. Pair c contains the left exterior host c and a left interior host m−c. Pair d supplies the right exterior host d and a right interior host m−d. The unpaired slot is the right reserve.

Use the same initialization as Section 3. The host sequence alternates low k=1 through h−1 with high m−u_k, where u_k=k for k<e and u_k=k+1 for k≥e. End at low h. These hosts are precisely the remaining slots, each once. For each k<e the adjacent sums are m,m+1 (low to high and high to next low). For k≥e they are m−1,m. Relative to initial sum m+1, the first jump is −1. All jumps have magnitude one except the change from m+1 to m−1 at low e, which is −2. In particular e=4<h when h=5 and the final return has sum m. Split the initial palette into equal halves before the first move. At every departure the D219 rule applies with a≥1, and at e with a≥2 because of the chosen quota. A later positive quota gives a strictly smaller than the active half-length. All moves preserve the spectra and produce the stated final quotas, with the last host keeping the remainder. Moving left whole pairs to 0 gives S. Because d=c+e and c+d=h+1, the restored weights m−e−c and h+1−d exchange the folded weights m−d and c.

## 5. Odd h with both interior lists all twos — joint allocation in four-host steps

For context, D219 already supplies every input with a right interior quota at least four. Sections 2 and 3 additionally supply all even h, all (2,5) and the (4,3) extension under the stated two quota-two roles. Before using Section 4, the residual consists of odd h≥7 with all right quotas two and arbitrary left quotas, and the h=5 case (4,3) with all right quotas two and fewer than two twos on the left. Section 4 supplies every odd h with any left quota at least four. It remains to handle both lists all twos, with arbitrary positive even flanks. The construction below handles that at every odd h≥5.

Use reserves a=m−1 and b=h, and put c=(h−1)/2 at the left exterior and d=(h+1)/2 at the right exterior. Then c,d are distinct indices from [2,h−1]. Assign the pairs of indices 1,c left and d,h right, using the remaining pairs to fill the required counts from Section 1. On the right the pair h contains reserve b=h and a positive right interior host m−h. Its last unpaired positive interior slot is h+1. The mandatory pairs fit even when (ℓ,j)=(2,5) or (4,3): left uses two prescribed pairs out of (ℓ+2)/2, and right uses two out of (j+1)/2. Every high host other than the reserved m−1 is an interior host of quota two. The left and right exterior host quotas are at lows c and d. Since d=c+1 and h=c+d, the folded weights c,m−d exchange on restoration via m−1−c=m−d and h−d=c.

### Four-host allocation preserving a contiguous remainder

Start with the whole terminal interval attached to low v=1 in the initialization. More generally assume the current uncommitted contiguous terminal interval is [Z,Z+N−1] with endpoint sum m+1, and its available differences are exactly [Z−v,Z+N−1−v] as if attached at low v. Previously placed leaves stay fixed. The next four actual hosts are low v, low v+1, high m−v−1 and high m−v−2. The lows require any independently positive even quotas Q₀=2D and Q₁, and both highs require two. Put K=(Q₀+Q₁+4)/2. Thus K≥4 and 1≤D≤K−3. Assume a positive tail remains after these four quotas, so N>2K.

Write i=z−Z,w=difference−(Z−v). The four maps are w=i, i−1, N−3−i, N−4−i. This follows from 2Z+N−1=m+1. Keep [K,N−K−1] for the next low host v+2, with difference coordinates [K−2,N−K−3]. The two outer index bands have size K each. Index the lower by i=b₀, and the upper by i=N−1−b₀ for b₀∈[0,K−1]. The available difference bands are [0,K−3] and [N−K−2,N−1], the latter indexed by decline N−1−w∈[0,K+1]. On lower indices the lows give low differences b₀ and b₀−1, and the highs give upper declines b₀+2,b₀+3. On upper indices the lows give upper declines b₀,b₀+1, and the highs give low differences b₀−2,b₀−3. The following assignment uses only the claimed destination lane for each row.

| Host | Lower b₀ | Upper b₀ | Low differences | Upper declines |
|---|---|---|---|---|
| v | [1,D−1] | {0,1} ∪ [4,D+2] | [1,D−1] | {0,1} ∪ [4,D+2] |
| v+1 | [D+1,K−2] | {2} ∪ [D+3,K−1] | [D,K−3] | {3} ∪ [D+4,K] |
| m−v−1 | {0,K−1} | empty | empty | {2,K+1} |
| m−v−2 | {D} | {3} | {0} | {D+3} |

The lower indices partition [0,K−1], using 0,K−1 at the first high and D at the second. The upper indices partition [0,K−1], since 0,1,2,3 are explicitly placed and the remaining intervals split at D+2. The low differences exhaust [0,K−3] via 0,1 through D−1, and D through K−3. The upper declines use 0,1,2,3, then [4,D+2], D+3, [D+4,K], and K+1. All are disjoint even for D=1 or D=K−3. At v the counts are D−1 and D+1, totaling 2D. At v+1 they are K−D−2 in each band, totaling 2(K−D−2)=Q₁. Each high receives two. These are actual differences at the specified physical hosts, including both opposite-band high assignments.

The still uncommitted interval is exactly [Z+K,Z+N−1−K], of length N−2K and endpoint sum m+1. At v+2 its actual differences give exactly the middle weight interval reserved above. Thus the same invariant is ready for the next four-host allocation. This is a joint resource reassignment on the whole available palette, with no requirement of preserving edge weights after allocating any individual row in isolation.

### Completing the odd-h original

Repeat the four-host step (h−5)/2 times, starting at v=1 and increasing v by two after each step. This fills lows 1 through h−5 and highs m−2 through m−(h−4). A positive remainder exists at every step because nine positive hosts still follow the last step. The final contiguous interval has endpoint sum m+1 and anchor low v=h−4. Its length N is exactly the sum of the nine remaining quotas. The remaining lows are v,v+1,v+2,v+3,v+5, and high offsets are v+1,v+2,v+3,v+4. Normalize with origin Z at the remaining interval and weight origin Z−v. For actual low v+k−1 and actual high m−(v+k−1), the maps are w=i−(k−1) and w=N−1−k−i. This follows by the same endpoint-sum arithmetic, and is the D220 relative host pattern of Section 2 with low roles 1,2,3,4,6 and high offsets 2,3,4,5.

At h=5 no four-host step is needed and c,d occupy relative lows 2,3. At h=7 they occupy relative lows 1,2. At h=9 the left exterior c is in a four-host step and d occupies relative low 1. For odd h≥11 both c and d occur among lows 1 through h−5. In each case the remaining non-two quotas occur only at relative lows 1,2,3, for which C, B, A supply arbitrary independent even growth. Set β=0 because every high quota is two. Thus N has exactly the required grown size, and the transported Section 2 assignment fills the remainder completely. Previous choices used disjoint label and difference intervals, and the skeleton and the exchange computed for these reserves are unchanged. This supplies all odd h in the remaining case, including the two h=5 splits, without needing any search or final separated-band repair.

## 6. Obstruction on the specified two-band repair

A different late allocation fails under the proposed resource premises. Precisely, let an active palette be the union of lower labels L+i and upper labels m−L−i for i∈[0,n−1], with the intervals disjoint and n=2r+1, r≥1. Assume all these labels lie strictly between the low hosts v+a, a∈A={0,...,r−1,r+1}, and the high hosts m−v−b, b∈B={1,...,r}. Each host requires two labels. The available weights must be those at the current low host v on that palette. Its low weight band is L−v+i and the upper band m−L−v−i. Because the label bands are strictly ordered, the lower maximum is less than the upper minimum for these weight bands. For a low host, lower labels give lower weight coordinates i−a relative to L−v, and upper labels give upper coordinates i+a measured as decline from m−L−v. For a high host, upper labels give lower weight coordinates i−b, and lower labels give upper coordinates i+b. Direct subtraction gives these statements, and all a,b are nonnegative. A lower-lane weight can only decrease from the reference band and hence cannot enter the upper band. An upper-lane weight can only increase and cannot enter the lower band. Out-of-range rows are unavailable.

Let X be lower-band indices at high hosts and Y upper-band indices at high hosts. The lower weight lane receives n−|X|+|Y| labels, so |X|=|Y|=k. There are r high hosts with quota two, so 2k=2r. The sum of the coordinates of the lower weight lane equals the full lower index sum minus sum(X) plus sum(Y) minus the sum of the shifts of its rows. The upper lane gives the same required equality with the sum of its own shifts. These shifts total 2(ΣA+ΣB) across both lanes, because each host has two rows. Thus each lane needs
```text
sum(Y)−sum(X) = ΣA+ΣB = r(r+1)+1 .
```
Yet the r largest and r smallest indices of [0,n−1] differ in sum by only r(n−r)=r(r+1). This proves impossibility of that late allocation. It does not assume one label from each lane at each host.

For example, on the all-quota-two input with Section 5's reserves, suppose the alternating order was used from 1 to an active low v with 2≤v≤h−1, using the first single-interval step and then equal-length trims. Here the last arriving sum is m, the two active intervals are reflected with cross-sum m and have length n=2(h−v)+1, the remaining number of positive hosts. Low hosts are v through h−1 and h+1, and high offsets run v+1 through h, giving precisely A and B with r=h−v. They all lie outside the initial interval. Regardless of previous trim choices, the late setup satisfies the obstruction. Section 5 instead leaves a single contiguous interval with cross-sum m+1 and its corresponding different weight resources. The late obstruction leaves whole-original joint allocation available.

## 7. Coverage and scope

For every registered input, use D219 when some right interior quota is at least four. Otherwise use Section 3 for even h, and for odd h use Section 4 if a left interior quota is at least four or Section 5 if every left quota is two. For h=5 Section 2 also supplies the stated independent-growth families. The entire registered domain is covered and its unresolved complement is empty. The construction never relies on symmetry of the quota magnitudes. Transport by the actual reversal s:i→s:(3−i), b:i:u→b:(3−i):u, l:i:u:e→l:(3−i):u:e supplies every reflected original and preserves every actual endpoint difference.

The D220 obstruction retains its exact original order and initialization. The D219 minimum-four condition remains valid for its original special jump. D221 changes the marks and order or uses joint allocations before a restrictive split. The late-lane obstruction is a restriction on supplied palettes and permitted hosts. The result makes no assertion about arbitrary parity, smaller multiplicities outside the declared domain or unrelated original profiles. The separate all-odd fixed-band observation remains held. No hybrid discriminator, program, solver, numerical search or protected checker was needed or used. [D219 retained scope](INDEPENDENT_MARKED_PHASE_TRANSITION_SUPPLIER.md#5-domain-b-with-all-quotas-independently-even) · [D220 scope](DIRECT_JOINT_FIXED_MARK_ALLOCATION.md).
