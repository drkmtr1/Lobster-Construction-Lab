# D225 — Three-interior odd-quota supplier

**PARTIAL POSITIVE WITH ONE HELD BOUNDARY.** The two-even-side/one-odd-side distribution is supplied throughout the registered domain. The one-even-side/two-odd-side distribution is supplied when j≥5 or h=6. Its separate j=3,h≠6 boundary remains held. All three chosen quotas are independently arbitrary positive odd integers on the supplied domains. The result uses exact named originals and includes physical reversal. [Named controls](../evidence/validation/D225_THREE_INTERIOR_ODD_QUOTA_SUPPLIER/HAND_CONTROLS.md).

## 1. Named geometry and the two-host insertion

Let T have the literal spine s:0--s:1--s:2--s:3, the two unit exterior branches, ℓ even and at least two interior positions at s:1, and j odd and at least three at s:2. The actual branch b:i:u attaches to s:i, and each l:i:u:e attaches to its own indexed branch. In the folded S move only the two exterior center edges inward to s:1 and s:2. Every original terminal parent, all three spine edges and all actual names are retained. Use h=(ℓ+j+3)/2≥5 and F for the terminal count, so m=2h+2+F. At unit size F=2h−1.

In the imbalance-three geometry the inner roots are 0,m. Use slots [1,h+2] and [m−h+1,m−1], with each complementary pair {k,m−k} assigned wholly to one folded root and the three unpaired lows h,h+1,h+2 on the right. This requires (ℓ+2)/2 left pairs and (j−1)/2 right pairs, totaling h−1. A pair contributes both its complementary weights irrespective of side. The unpaired attachment weights are [m−h−2,m−h], and the middle spine edge gives m. At any grown size the skeleton has weights [1,h−1]∪[m−h−2,m], before restoring the exterior edges. The residual terminal labels z are [h+3,m−h] and differences [h,m−h−3]. Thus i=z−(h+3) and w=difference−h each fill [0,F−1], with exact endpoint equations
```text
low k:       w=i+3−k
high m−k:    w=F−1−k−i .
```
All low slots are below every terminal label and all high slots above them. Hence no absolute-value choice is implicit in these equations. [D222 slot arithmetic](PARITY_COMPATIBLE_ALL_ODD_SUPPLY.md#2-complementary-bands-with-general-imbalance).

For a compatible cut (I,W), each low row has i≥I iff w≥W, and each high row has i≥I iff w<W. Increase F and m by G, and add G to the old i≥I and w≥W. The old rows satisfy the same affine rules at the new F, and the unused gaps start at I,W. A low recipient with W−I=3−k uses the identity on the two fresh intervals in local coordinates. A high recipient with I+W=F−k′ uses reflection in G−1. For G=2(α+β), assign any α of the reflected pairs to the low and the other β to the high. The pairs ensure a bijection on both gaps, giving independent increments 2α and 2β. At zero width both gaps are empty. At every stage a row stays on its named host, every old terminal can keep its index, and the new terminals at a host occupy the appended indices. [D223 shared insertion and exact dedicated-gap obstruction](AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY.md#2-shared-insertion-and-its-exact-limitations).

In the markings used below write (0,m,a,b,c,d) on the actual ordered vertices (s:1,s:2,s:0,s:3,b:0:0,b:3:0). Each marking satisfies a−c=m−d and b−d=c. The two actual exterior differences exchange c and m−d in the restoration from S to T. All weight and label identities are interpreted at the current m. If m grows, the high reserve a and each high host move with m at their old offsets while the other marks remain fixed for the chosen h. Thus the exchange persists. A complete residual permutation combined with these skeleton identities gives exact label [0,m] and weight [1,m] alphabets, with no change to any other incidence. [D217 reconstruction criterion](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source).

## 2. Director's symmetric third-host lift

Given any complete allocation at the current F on such an admissible fixed-h skeleton, suppose low 3 is an actual branch. Let t≥0. Increase F and m by 2t and give each old terminal row coordinates (i+t,w+t). For low hosts, w−i persists. For high hosts, i+w and F both grow by 2t, so the high equation with fixed offset persists. High numerical labels, including the high reserve, move by 2t, and each low label remains the same. The old rows fill [t,F+t−1] in both alphabets. Give the unused intervals [0,t−1]∪[F+t,F+2t−1] to the actual low 3 by w=i. Their disjoint union has exactly 2t rows. For t=0 both intervals are empty.

The labels of old terminals may change while their actual indexed incidences and parents stay fixed. Append the 2t new terminal names solely at low 3. Every requested quota and both numerical palettes then hold. The paired slots and unpaired low slots have the skeleton spectrum of Section 1 at the new m. The two D217 exterior edges still exchange their weights by the stated marker equations. This proves the exact named T at the final quotas. The construction uses one shared insertion first and then this sequential symmetric outer operation. It does not alter the D223 obstruction for multiple distinct dedicated intervals with fixed affine offsets.

For any of the constructions, physical reversal sends s:i, b:i:u and l:i:u:e to the corresponding vertices with section 3−i and leaves u,e fixed. That bijection sends every edge to its physical counterpart. Thus all differences and the two actual restoration edges transport to the reversed graph.

## 3. Whole-pair relocation on D224 and the exact direct coverage

Reuse D224's alternative unit permutation for h≥5 with a=m−(h−1), b=h+1, c=1, d=h and cut (h−1,3). Its four unit bases and h→h+4 induction are valid on the numerical hosts before assigning pairs to physical sides. Left pairs 1 and h−1 are compulsory to supply the left exterior and left reserve, and right pair h−3 is compulsory to put the high recipient m−(h−3) on the right. The low recipient is h−1 on the left. All three unpaired lows stay right. The third low 3 is distinct from m−(h−3) and from h−1, and is never a mark. Only its pair side is to be selected. [D224 seed and recurrence](TWO_LEFT_PAIR_PARITY_ADAPTED_SUPPLIER.md#3-new-two-left-pair-marking-with-a-high-suffix-row).

- **One chosen left and two chosen right.** Place pair 3 on the right along with pair h−3. If h≠6 these are distinct and require at least two right pairs, equivalent to j≥5. At h=6 both roles use pair 3: low 3 and high m−3 remain distinct recipients and both are right interiors. One right pair suffices, including the boundary (ℓ,j)=(6,3). In each case the left requires at least its two compulsory pairs. The remaining unforced pairs fill the remaining nonnegative pair counts, whose sum equals the number available.
- **Two chosen left and one chosen right via D224.** If h≠6 and ℓ≥4, put pair 3 on the left in addition to 1 and h−1, while pair h−3 stays right. Three left pairs and one right pair suffice under the stated multiplicities. Pair 3 differs from both compulsory left pairs because h≥5, and differs from h−3 in this case. The remaining positions use the unforced pairs in the required numbers.
- **Two chosen left at h=6 with ℓ≥4.** Use the actual D223 Section 6 seed, with a=m−4,b=6,c=1,d=5, cut (6,2), left pairs 1,4,3 and mandatory right pair 5. The left high receiver m−3 and low 3 are the two interior hosts of pair 3. The right low receiver 7 is unpaired and differs from its reserve 6 and exterior host 5. The exchange is 1↔m−5 and persists; the extra pair 2 can be placed to fit either registered split (4,5) or (6,3). [D223 Section 6 construction](AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY.md).
- **Two chosen left at h=5 with ℓ=2.** Apply accepted D223 Section 3B with r=0 to keep the left flank unit. Its two left roles have quotas 3+2u and 1+2v; the right role has 1+2β and the other hosts remain unit. Give the smaller enlarged left quota the first role, so v≥u+1 implies its required v≥u+(u mod 2). Either selected left quota one is supplied by Section 3A, allowing either actual name to occupy the enlarged role. The same Section 3B also has its accepted pair-2 companion at (4,3). [D223 h=5 packets](AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY.md#3-the-h5-cycle-suppliers).

In each pair-allocation case, take the prescribed pairs first and allocate the rest in increasing index order until the left count is filled. Assign the actual selected names to distinct recipient slots on their own sides before assigning unselected names. The unit permutation is unchanged by pair relocation. It only fixes terminal labels and actual differences at numerical hosts. Moving a whole pair changes its two folded attachment weights from k,m−k to m−k,k, or conversely. It leaves terminal weights, marks and exterior reconstruction intact. Use Section 1 for the first two increments and Section 2 for the third. All three nonnegative widths, including any zeros, are independently permitted.

For ℓ=2, D224 has exactly its two compulsory left pairs, so moving the distinct pair 3 left exceeds capacity when h≠6. At h=6 pair 3 is already needed for the right recipient. This is a scope boundary of this relocation, not a nonexistence result. At j=3,h≠6 the analogous right relocation also exceeds its one available right pair. This second boundary is held as directed.

## 4. Full two-left-pair supplier for h≥6

This closes the primary bottleneck with ℓ=2. Use the same D224 alternative marking and actual pairs 1,h−1 on the left, with no other left pair. One chosen left interior is low h−1 and the other is high m−1. Both are genuine interior hosts: the left exterior is low 1 and the other slot of pair h−1 is the spine reserve. The selected right interior is high m−(h−3), in a right pair. All these roles are distinct at h≥6. Low 3 is an ordinary unit right interior. The right exterior d=h and reserve b=h+1 occupy unpaired right slots; the last unpaired h+2 is another right interior. The actual restoration exchange is 1↔m−h, since a−1=m−h and b−h=1. The complete skeleton and terminal alphabets are those of Section 1.

The original D224 permutation is replaced by a unit permutation on the same numeric hosts, still with cut (I,W)=(h−1,3). The changes give low 3 the top identity row and put the sole high suffix at offset h−4. For N=2h−1=F at unit size, require
```text
low 4:           (i,w)=(1,0)
low h:           (i,w)=(h−2,1)
high m−(h−4):    (i,w)=(h,2)
low 3:           (i,w)=(N−1,N−1).
```
These are four distinct hosts and rows for h≥6. They satisfy the affine equations. The two low-prefix rows occupy weights 0,1. The high suffix lies above the input cut and supplies the remaining weight 2. The high recipient m−(h−3) is a different right host and stays in the prefix. The low recipient h−1 and this high recipient satisfy W−I=3−(h−1) and I+W=N−(h−3). Meanwhile high m−1 remains the unit left host for the eventual third enlargement.

### Four direct unit bases

For the other high rows the table gives (offset k,input i). For other low rows it gives (host k,input decline J=N−1−i). On either kind define Q=N−1−w. Thus Q=i+k for the high rows and Q=J+k−3 for the low rows. These are actual differences, not abstract free assignments.

| h | High prefix (k,i) | Upper lows (k,J), excluding low 3 |
|---:|---|---|
| 6 | (1,0),(3,2),(4,3) | (1,5),(2,3),(5,2),(8,1) |
| 7 | (1,0),(2,2),(4,3),(5,4) | (1,4),(2,6),(5,1),(6,3),(9,2) |
| 8 | (1,4),(2,0),(3,3),(5,5),(6,2) | (1,3),(2,5),(5,1),(6,4),(7,7),(10,2) |
| 9 | (1,4),(2,0),(3,5),(4,2),(6,3),(7,6) | (1,3),(2,5),(5,1),(6,4),(7,8),(8,6),(11,2) |

These high inputs are exactly [0,h−3] except 1. The low declines are exactly [1,h−1] except h−2. The first four rows supply the omitted prefix indices 1,h−2, the omitted suffix decline h−2 at the high suffix, and upper decline zero at low 3. Thus every index occurs once. The high and low upper weight-decline sets in the table are respectively {1,5,7} and {2,3,4,6} for h=6, {1,4,7,9} and {2,3,5,6,8} for h=7, {2,5,6,8,10} and {1,3,4,7,9,11} for h=8, and {2,5,6,8,9,13} and {1,3,4,7,10,11,12} for h=9. Each pair partitions [1,2h−5]. With the top decline zero and the three lower weights, this gives all weights. Every remaining numeric host appears exactly once. The high-prefix rows have w≥3, the listed upper lows exceed both thresholds, and the four stipulated rows have the required threshold positions. Hence the whole cut is compatible in all four bases.

### Repeatability from h to h+4

On the unit instance set h′=h+4, N′=N+8. Shift all old low host labels and high offsets by four, including the two reserve slots. Omit the old row at low 4, (1,0), and the old row at low 3, (N−1,N−1). Carry every other row by (i,w)→(i+4,w). This keeps every low relation since i and k grow equally. It keeps every high relation since N and i+k grow by eight. The carried inputs are [4,N+2] except 5. The carried weights are [1,N−2]. Reassign (1,0) to the new low 4 and (N+7,N+7) to the new low 3. The vacant indices are {0,2,3,5} and [N+3,N+6], the latter having new input declines J=1,2,3,4. The vacant weights [N−1,N+6] have declines Q=1 through 8. The unused low hosts are 1,2,7,8, including the two shifted old hosts whose rows were omitted. The new high offsets are 1,2,3,4.

| Host | New input | Weight decline Q |
|---|---:|---:|
| low 1 | J=3 | 1 |
| low 2 | J=4 | 3 |
| low 7 | J=1 | 5 |
| low 8 | J=2 | 7 |
| high offset 1 | i=3 | 4 |
| high offset 2 | i=0 | 2 |
| high offset 3 | i=5 | 8 |
| high offset 4 | i=2 | 6 |

Directly Q=J+k−3 or Q=i+k on the respective rows. The new hosts and both vacant palettes are used once. The new cut is (I+4,3). Old carried thresholds retain their truth values, the four new highs are below the new input cut and have weights ≥3, and the four new lows are above both thresholds. The returned low 3 is again the top identity and low 4 has its old below-cut row. The other low-prefix row moves from low h to low h′ with (i,w)=(h′−2,1), and the unique high suffix moves to offset h′−4 with (h′,2). The old reserves shift to the new h′+1 and high offset h′−1. The left and right shared receivers shift to their corresponding h′−1 and h′−3 slots. Assign left exterior 1 and right exterior h′ as before. This recurrence acts on a unit numerical assignment before mapping to final physical names. It need not carry an unselected old physical name to the same role at a different auxiliary size.

For any h≥6 start at the unique base in {6,7,8,9} congruent to h modulo four. After finitely many steps assign the two actual left names in either prescribed order to low h−1 and high m−1, and the selected actual right name to high offset h−3. Assign unselected right names in original order to the remaining right slots in increasing label order. No ordering of quota magnitudes is required. First use the shared cut to grow low h−1 and high offset h−3 independently. The top row at low 3 is above both cuts, hence remains the maximum identity row of the grown palettes. This row permits the third enlargement below.

### Anchored enlargement at high offset 1

Let F now denote the size after the shared insertion. Enlarge by 2t for any t≥0. Translate all rows except the top identity row by (t,t), and move that identity row from (F−1,F−1) to (F+2t−1,F+2t−1) at the same low 3. The usual low and high equations hold under the translation, and the moved row remains an identity. The indices and weights of old rows now use [t,F+t−2] together with {F+2t−1}. The unused pieces in both alphabets are
```text
[0,t−1] and [F+t−1,F+2t−2].
```
At the actual high host with offset 1 the new formula is w=F+2t−2−i. This reflection exchanges those two pieces exactly. Assign all 2t unused inputs to that high host. It is the second chosen left interior. Only its quota increases; the moved identity row remains at the unit right interior low 3. Both pieces are empty at t=0. Label and weight coverage, all old terminal indices and actual incidences, and the affine equations persist. The marks change only through m on the high reserve, and the exterior exchange remains 1↔m−h, so the construction yields the entire named original and its reversal.

Thus the three quotas are independently 1+2α and 1+2t on the left and 1+2β on the right. A one-shot allocation outputs the original indexed vertices and their labels after the finite recurrence and the two explicit insertion operations. Its use of the top identity to free a shifted reflected complement is a sequential transport, with a change in the old identity row's placement. It does not change D223's dedicated-gap result.

## 5. Exact closure

The primary ℓ=2,h≥6 two-left/one-right bottleneck is closed in full by Section 4. The h=5 ℓ=2 case is already covered by the accepted packet supplier, and the other two-left cases follow from the pair placements in Section 3. For one-left/two-right, the proved domain is every registered split with j≥5 or h=6. The exact remainder of this study is the separate held one-left/two-right stratum j=3,h≠6, with all three selected quotas genuinely enlarged. The checked D223 and D224 suppliers cover their precise two-quota and additional packet scopes. They do not furnish an arbitrary-three-quota supplier for that held stratum in this pass. This makes no global classification or novelty claim. The requested primary bottleneck was solved, and no investigation or diagnostic for the held boundary is opened here.

No numerical discovery, dormant diagnostic preparation, solver, protected checker, scientific execution or dependency installation was used. Retain the accepted earlier scopes, historical incomplete dispositions, held closure and insertion obligations, and deferred D207. No successor is selected.
