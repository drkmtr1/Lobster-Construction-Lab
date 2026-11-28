# D231 — Independent coordinate insertion and the unequal-pair finite kernel

**Unbounded supplier proved, residual finite obligation open.** A returning S2 packet exists for every unordered positive odd four-tuple with maximum at least 19. A shorter set of cuts also supplies every normalized key with maximum at least 11 and a further five keys of maximum nine. The normalized returning problem has 165 keys before known positives are removed. The exact frozen residual has 29 keys and 322 distinct placements. [Independent graph definitions](../evidence/validation/D231_INDEPENDENT_COORDINATE_INSERTION_SUPPLIER/ORIGINALS.md) · [Named checks](../evidence/validation/D231_INDEPENDENT_COORDINATE_INSERTION_SUPPLIER/HAND_CONTROLS.md)

## 1. Reflected block coordinates

Retain D230's S2 source of size F≥11 and numerical growth h→h+4. Shift inherited host offsets by four and transport ordinary rows by (n,n−4), omitting one old row at L₃ and one at L₄. Their shifted roles L₇,L₈ require one replacement each. The new complete size is F+2n. In the original tagged coordinates subtract F from each upper coordinate. Before return, the lower input and weight sets are [0,n−1]∪{n+2} and [0,n−5]∪{n−3}; the upper sets are [n−1,2n−1] and [n−5,2n−1]. Returning L₄:(2,1) and L₃:(F+2n−1,F+2n−1) removes the lower 2 and 1 and the upper tagged maximum 2n−1 on each side. For n=4 the lower weight return 1 is the isolated point n−3, so no lower weight remains. The even packet widths in the finite kernel are n=4 or n≥6. [Accepted D230 transport](PARAMETERIZED_INDEPENDENT_PAIR_QUOTA_GROWTH.md#2-returning-s2-transport-at-arbitrary-width)

Now reflect each upper tagged coordinate u to y=2n−4−u, within its own input or weight block. The upper input interval becomes [−2,n−3], and the upper weight interval becomes [−2,n+1]. The lower sets are unchanged. This is a separate bijection on each resource and does not identify lower and upper copies of any integer. For a low row the old tagged displacement is 3−k. For a high row one endpoint is upper and the old tagged sum is 2n−1−k. Subtraction from 2n−4 gives:
```text
LL Lk: x → x+3−k
UU Lk: y → y+k−3
LU Hk: x → x+k−3
UL Hk: y → y+3−k.
```
These equations hold for every residual row, including replacements at L₇ and L₈ on either admissible low track. Their conversion back preserves the actual affine endpoint equations. Both return rows are outside these residual sets.

## 2. Sparse supplier at offset 3

Let Q≥9 odd and n=Q+3 even. Give quota Q to both roles at offset 3, and quota one to each other new role. Put in the seven disjoint exceptional rows:
```text
LL L1 (1,3)       LL L2 (3,4)      LU H4 (4,5)
UL H1 (5,7)       LL L8 (7,2)      LU H2 (n+2,n+1)
UU L7 (n−4,n).
```
The displacements in this order are 2,1,1,2,−5,−1,4, exactly their reflected rules. In the lower inputs these use 1,3,4,7,n+2, and in the lower weights they use 3,4,7,2. In the upper inputs they use 5,n−4, and in the upper weights they use 5,n+1,n. Each list is inside its tagged inventory and has no repeat for n≥12.

After those deletions, write `D={0,6,n−3}∪[8,n−5]`. The remaining lower inputs are D∪{5,n−4,n−2,n−1}, and the lower weights are D∪{5}. The remaining upper inputs are D∪{−2,−1,1,2,3,4,7}, and the upper weights add {n−4,n−2,n−1} to those upper inputs. These unions are disjoint within each track. In particular n=12 gives [8,7] empty and D={0,6,9}. For every larger even n the displayed interval has n−12 entries, giving |D|=n−9, also valid at n=12.

Use the one-track identities at L₃ on upper −2,−1,1,2,3,4,7 and lower 5. Use the three forced LU H₃ crossings at n−4,n−2,n−1. At each double-track coordinate in D one may use either two L₃ identities or two H₃ crossings, exhausting the coordinate once in each input and weight block. Choose (n−6)/2 doubles for crossings and the remaining (n−12)/2 for identities. This is a nonnegative split summing to |D|. H₃ receives 3+2(n−6)/2=n−3=Q; L₃ receives 8+2(n−12)/2=n−4=Q−1 residual rows and its prescribed maximum return. L₄ has only its lower return. All other demands and both replacements were consumed by the exceptions. This proves every (1,1,Q,1) at the stated Q. The Q=9 named 57-edge control supplies the offset-3 key of the former D230 proposal symbolically, so that comparison is superseded without preparation or execution.

## 3. Independent cut insertion for a large quota

For Q≥19 let n=Q+3≥22 and reserve double identities at {8,9,10,11,13}∈D. Its capacity (n−12)/2≥5 suffices. Fill the rest deterministically with the remaining number of double identities at the smallest remaining eligible coordinates and use double crossings elsewhere. Use the following aligned lower and upper cuts, immediately before their coordinates:
```text
pair 1 first       lower 10   upper 8
pair 1 second      lower 11   upper 9
pair 2             lower 12   upper 11
pair 4             lower 13   upper 14
```
Each cut inserts the same nonnegative width in the two tracks, applied to both inputs and weights. Its lower and upper cuts occur in the same order. For a row with endpoints in the same track, they must be either both below or both at/above that track's cut. For a mixed row use the two corresponding cuts. The low-coordinate exceptional rows are entirely below all relevant cuts, and the high-coordinate exceptions are entirely above them; this includes the UU L₇ from n−4 to n. The forced H₃ crossings at n−4,n−2,n−1 are above all cuts. Identities automatically agree, even when the lower and upper maps differ. An H₃ double crossing at x can disagree only between a lower cut and its upper counterpart. The four disagreement coordinate sets are {8,9}, {9,10}, {11} and {13}. All are reserved to identities. Thus every old row's signed displacement is unchanged after applying the sum of its cut increases, in the reflected equations. This argument applies simultaneously to arbitrary cut widths. In contrast, a double H₃ crossing at coordinate 8 and a positive first pair-1 width give different indicators at lower 10 and upper 8.

The embedding at either track is t↦t+Σ_j p_j·1(t≥cut_j), where p_j is its insertion width. In the lower track all cuts exceed the missing 2 and 1 and occur at or before the end-plus-one n−4 of the lower weight interval. In the upper track they lie in both intervals or at an upper end-plus-one. In each interval, every new integer is either an embedded old coordinate or one of the inserted positions, with a unique choice. Lower holes 1 and 2 stay pinned and isolated values n+2,n−3 shift by the total increment; upper beginnings −2 remain fixed and their endpoints grow by that increment. This proves that the expanded residual sets are exactly the new n′ sets from §1, without importing any new rows outside the displayed gaps. Every new lower and upper gap start differs from its counterpart by the original cut offset because earlier insertions have equal widths and the same order.

Let k∈{1,2,4} and s=3−k. For lower positions x,x+s with upper partners y=x−s,y+s the four new rows are
```text
LL Lk   x   → x+s
LU Hk   x+s → y+s
UU Lk   y+s → y
UL Hk   y   → x .
```
Each of the two positions per track occurs once as input and once as weight. Their four signed differences are s,−s,−s,s, exactly the table in §1. Thus each packet of four rows increments the two host quotas by two. For k=2 and 4 use consecutive pairs in the even-length insertions, choosing x to be the first position when s=1 and the second when s=−1. For k=1 an increment p divisible by four uses width p only at the first cut, pairing (0,2),(1,3) in each consecutive block of four positions. For p≡2 mod 4 use p−1 first and one at the second cut. The first p−2 positions already group into fours. The last first-gap position and the second-gap position have separation two, because exactly one old coordinate lies between them in both tracks. This applies at p=2, giving one split pair, and p=6, giving one block of four followed by that split pair. The width-zero option inserts nothing on either track.

At n′=n+p₁+p₂+p₄ undo reflection with 2n′−4, add F on the upper track, and join the unchanged-width-rule conveyed source rows at (n′,n′−4). The two replacements have persisted and give the inherited quotas at L₇,L₈. Install the exact two new S2 anchors at (2,1) and (F+2n′−1,F+2n′−1). They were outside the enlarged residual sets. Equation conversion in §1 and exact vacancy lifting then give all terminal rows, both inventories and both host counts at the new size F+2n′. There is no parity assumption on F. This supplies independent even increments 0,2,4,… at pairs 1,2,4 with Q fixed, proving every ordered (q₁,q₂,Q,q₄) of positive odd entries with Q≥19. Moving a largest quota to offset 3 gives the claimed unordered scope. This is an existence choice of numerical placement, subject to the actual physical role and quota match when applied to a tree. At any lawful full physical assignment the D230 skeleton and literal exterior exchange persist, and the exact section-index reversal supplies its reverse. The procedure has finitely many symbolic selections and row emissions.

## 4. Smaller cuts and the exact residual kernel

The same construction permits a shorter cut list when one of the four quotas is one. Put that unit at offset 1. For n≥14 use pair 2 at (lower 8, upper 7) and pair 4 at (lower 9, upper 10), skipping zero widths. The exceptions below the cuts still agree: in particular L₈ has lower endpoints 7,2, and the cross from upper 5 to lower 7 is below both. The upper exceptional input n−4 of L₇ and all forced crossings are at least 10. The cuts have the same order and lie within the bounds for the interval argument. The first disagreement coordinate would be 7, where the sparse allocation has only the upper identity and never an H₃ crossing. Reserve the double identity at 9 to handle the second. Here 9∈[8,n−5] and (n−12)/2≥1. The four-row construction works with s=±1, independent of how many positions were inserted at the earlier cut. Thus **all normalized tuples with d≥11 are positive**. At n=12 the pair-2 cut (8,7) alone is also valid: the lower weight cut at 8 is end-plus-one, all lower holes stay fixed, the high exceptions and forced crossings are at/above the relevant cuts, and coordinate 7 still has no crossing. Its single independent enlargement supplies (1,1,c,9) for odd 1≤c≤9 after placement at pair 2. These are verified with the same exact inventory and anchor return. This refinement concerns normalized requests, not a stronger universal d≥11 threshold without a unit.

For an arbitrary unordered positive odd request, first use §3 if its maximum is ≥19. Otherwise sort and subtract its minimum minus one from each entry. This even decrement produces a=1 and d≤17. A positive at any placement of the normalized tuple yields the desired original numerical quota tuple at that placement by repeated accepted D230 uniform +2 augmentation, with the same source and returned S2. This implication suffices for universal returning supply. Failure of a normalized key would not exclude its larger translated requests, which might have another construction.

There are nine odd values 1,…,17. With a=1, the other three are a size-three multiset from these nine values. There are C(11,3)=165 keys. The raw maximum n=1+17+17+17=52 gives 104 residual rows and 105 frames in row-by-row recursion including the root. The unit comes from D229's S2 U packet. D230 homogeneous positives normalize to that same key. The D229 S2 cap and D228 state-changing positives do not authorize an S2 return. The sparse Q=9,11,13,15,17 keys are included in the direct positives here.

More exactly, d≥11 accounts for 165−C(7,3)=130 keys (the complement uses the five odd values up to nine). Five distinct d=9 keys have b=1 and are supplied by the shorter single cut, and the unit adds one. There remain precisely the following 29 unclassified aggregate keys in the registration:
```text
19:  a=1, 1≤b≤c≤d≤7, all odd, excluding (1,1,1,1).
10:  a=1, 3≤b≤c≤d=9, all odd.
```
The first group has 4⁴−3⁴−1=174 distinct ordered placements. The second has 4(4³−3³)=148, since exactly one position equals one and a nine must occur. Together they give 322 legal ordered placements, each retaining one quota for each matched pair. The actual residual maximum is n=1+9+9+9=28, i.e. 56 residual rows and 57 primary frames including the root. One positive placement resolves the aggregate. A negative requires all its distinct placements to be independently excluded. The static preparation uses this smaller complete residual domain. No claim about nonbinary cap/core supply, heterogeneous pairs, arbitrary physical odd-quota universality or unmarked graceful impossibility follows from the reduction.
