# D224 — Two-left-pair parity-adapted odd supply

**PROVED FOR THE FULL REGISTERED DOMAIN.** The Director's marks and cuts are legal for every registered h and admit the required h=9 and h=10 unit controls. Their specific all-high-prefix return is impossible once W≥6. A different two-left-pair marking, with the low recipient on the left and one high row outside the input prefix, supplies the full unbounded domain by an explicit h→h+4 construction. [Named controls](../evidence/validation/D224_TWO_LEFT_PAIR_PARITY_ADAPTED_SUPPLIER/HAND_CONTROLS.md).

## 1. Original graph, skeleton and insertion

For h≥9 the registered original T has spine s:0--s:1--s:2--s:3, a unit branch at each exterior vertex, two interior branches on the left, and j=2h−5 on the right. At branch b:i:u install its specified terminals l:i:u:e on that same actual parent in original index order. The two independently odd quotas are on any chosen actual interior branches, one per side. Other quotas are unit. First compute a unit labeling and then enlarge those two branches. The folded source S moves just the two exterior centers from s:0 and s:3 inward to s:1 and s:2. The other original edges remain literal, including all three spine edges. Use marks (0,m,a,b,c,d) on (s:1,s:2,s:0,s:3,b:0:0,b:3:0) and F=2h−1, m=2h+2+F=4h+1 at unit size.

Use the D222 imbalance-three slot bands [1,h+2] ∪ [m−h+1,m−1]. Assign each pair {k,m−k}, k∈[1,h−1], wholly to one folded root, exactly two pairs to the left. Put all three unpaired slots h,h+1,h+2 on the right. The four left slots contain two interiors, one exterior and one reserve. The 2(h−3)+3=2h−3 right slots contain j interiors, one exterior and one reserve. Complementary pairs contribute the same two weights on either side. The unpaired slots give [m−h−2,m−h], and the middle spine edge has weight m. The exact skeleton weights are [1,h−1] ∪ [m−h−2,m]. The slots and roots leave terminal labels [h+3,m−h]; the weights left are [h,m−h−3]. Subtract h+3 and h respectively to obtain the two alphabets [0,F−1]. All low hosts are below the terminal labels and all high hosts above them. The exact absolute differences therefore give the D223 row rules
```text
low k:       w=i+3−k
high m−k:    w=F−1−k−i .
```
A unit certificate has one row per actual positive host and uses each index and weight exactly once. [D222 band arithmetic](PARITY_COMPATIBLE_ALL_ODD_SUPPLY.md#2-complementary-bands-with-general-imbalance) · [D223 row and growth rules](AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY.md#2-shared-insertion-and-its-exact-limitations).

A cut (I,W) is compatible when each low row has i≥I iff w≥W and each high row has i≥I iff w<W. Increase F and m by G and translate old i≥I and old w≥W up by G. This keeps each low rule by changing both sides equally and each high rule by translating exactly one coordinate to account for the new F. The terminal and weight gaps are [I,I+G−1] and [W,W+G−1]. For low k with W−I=3−k, its map on equal local gap coordinates is the identity. For high offset k′ with I+W=F−k′, its local map is reflection in G−1. An even G=2(α+β) divides into α+β pairs under reflection, including none at G=0. Assign any α pairs to the low recipient and the rest to the high. Both palettes are filled exactly once and the chosen quotas are 1+2α and 1+2β independently. The original unit terminal can retain index zero after transport. New labels at either host fill its appended indices in increasing order. All other quotas stay unit.

In both marking families below, a is high, b unpaired low, c,d low and the identities a−c=m−d and b−d=c persist when m grows. Thus the two restored exterior edges exchange the two folded weights c,m−d at the actual endpoints. The root edge, slot spectra and terminal maps hold at the grown m as well. This gives the graceful original with all its unchanged incidences. [D217 two-edge restoration criterion](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source).

## 2. Director's parity-adapted marking and its exact barrier

Take c=2 for odd h and 3 for even h, r=h−2c, a=m−r, b=h, d=h−c. Pair indices c and r are distinct in [1,h−1] for h≥9, since odd h≥9 has r≥5 and even h≥10 has r≥4. Pair d is distinct from both and is on the right. The low b=h is unpaired and differs from c,d. The high a lies strictly between both roots and is greater than every low slot. Thus all six marks are distinct. The left pair c gives the exterior c and the interior recipient m−c. Pair r gives reserve a and the other left interior. The low recipient h+1 is an unpaired right interior. The restoration equations follow from r+c=d and b−d=c. This verifies every named slot, the complementary inventory of Section 1 and the restored edges. The retained h=8 control also fits these marks, with c=3,r=2.

Here I=(3h−3−c)/2 and W=(h+1−c)/2 are integers since c has the parity of h+1. They satisfy 0<W<I<F, W−I=2−h=3−(h+1) and I+W=F−c. For fixed parity, increasing h by two gives the proposed increments F+4,I+3,W+1,r+2. Nevertheless these cut and mark identities do not imply an allocation.

There are h−2 high rows. If P is the number with i<I, the compatible-cut count is W=I+(h−2)−2P by counting low-prefix and high-suffix outputs below W. Thus all high rows must have i<I. Exactly W low-prefix hosts must fill the lower weights [0,W−1], and the h+1−W upper lows have every input in [I,F−1].

### A first-moment obstruction

Let B be the set of numeric low-prefix hosts and S_B=Σ_{k∈B}k. The sum of their input indices is binom(W,2)+S_B−3W, since i=w+k−3. Therefore the high input sum is binom(I,2)−binom(W,2)−S_B+3W. Independently, both complete alphabets have the same sum. Summing w−i over the low and high rows gives
```text
2 Σ_high i = (h−2)(F−1)+3(h+1)−Σ_all hosts k.
```
Here k for a high host means its offset from m. The sum of all these k is
```text
(h+2)(h+3)/2 − h + h(h−1)/2 − r = h²+3+2c.
```
Thus twice the high input sum equals h²−3h+4−2c. Substituting I=W+h−2 into the prefix expression gives
```text
S_B = W(h+1)+1−h+c,
Σ_{k∈B}(h+1−k) = h−c−1 = 2W−2 .
```
The available deficit values are −1,0,2,3,...,h because the only low reserve is h. For W≥3 the minimum sum of W distinct such values is W(W−1)/2−2. This minimum exceeds 2W−2 whenever W>5. Hence no unit permutation can meet this exact cut and reserves for W≥6, even with arbitrary allocation within each part. This begins at odd h=13 and even h=14, so the proposed same-mark and same-cut h→h+2 transport cannot be repeated unboundedly. It does not constrain other cuts, reserve geometry or ordinary gracefulness. For W=5 the minimum is attained only at deficits {−1,0,2,3,4}, a necessary condition only. These h=11 and h=12 exact candidate interfaces are not separately classified here.

### Required controls on the proposed marks

At W=4 the deficit sum six permits precisely {−1,0,2,5} or {−1,0,3,4}. Indeed omitting −1 or omitting 0 makes the least possible sum exceed six, and the two other distinct entries at least two must sum to seven. The following direct rows realize the first set at h=9 and h=10. The low prefix column gives triples (host k,input i,weight w). For high rows use pairs (offset k,input i), and for upper low rows use (host k,input decline J=F−1−i). A weight decline Q=F−1−w is i+k on the high rows and J+k−3 on upper low rows, which checks each actual map.

| h | Low prefix (k,i,w) | High prefix (k,i) | Upper low (k,J) |
|---:|---|---|---|
| 9 | (5,5,3),(8,6,1),(10,9,2),(11,8,0) | (1,10),(2,7),(3,0),(4,1),(6,2),(7,3),(8,4) | (1,3),(2,5),(3,0),(4,1),(6,4),(7,2) |
| 10 | (6,6,3),(9,7,1),(11,10,2),(12,9,0) | (1,8),(2,11),(3,0),(5,1),(6,2),(7,3),(8,4),(9,5) | (1,2),(2,5),(3,1),(4,4),(5,0),(7,3),(8,6) |

At h=9 the two prefix lists together use indices [0,10] and upper low declines [0,5] give inputs [11,16]. The two upper weight-decline sets are {3,5,8,9,10,11,12} and {0,1,2,4,6,7}, together [0,12], giving weights [4,16]. At h=10 the prefix lists use [0,11] and upper input declines [0,6] give inputs [12,18]. The two upper weight-decline sets are {3,6,8,9,10,12,13,14} and {0,1,2,4,5,7,11}, together [0,14], giving weights [4,18]. At both sizes the low prefix fills [0,3]. Thus the demanded cuts (11,4) and (12,4) are compatible. Independent even enlargement follows at both sizes by Section 1 on the named receiving hosts. At h=8 the unchanged D223 control realizes the compatible cut (9,3) with the same parity-adapted marks. [Retained h=8 named control](../evidence/validation/D223_AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY/HAND_CONTROLS.md#6-the-exact-h8-interface) · [New named controls](../evidence/validation/D224_TWO_LEFT_PAIR_PARITY_ADAPTED_SUPPLIER/HAND_CONTROLS.md).

## 3. New two-left-pair marking with a high suffix row

Set a=m−(h−1), b=h+1, c=1, d=h. Put pair indices 1,h−1 on the left and every other pair on the right. The pair at 1 supplies the left exterior and the ordinary unit left interior at m−1. The pair at h−1 supplies reserve a and the chosen left interior at low h−1. All three unpaired slots are on the right: right exterior d=h, reserve b=h+1 and a unit interior h+2. The chosen right interior sits at high m−(h−3), in a right pair since 1<h−3<h−1 for h≥5. Thus both particular selected actual names can be assigned first. Assign all other right interior names in their original order to the remaining right slots in increasing label order. These marks are distinct within their bands for h≥5. The exchange is 1 with m−h, since a−1=m−h and b−h=1. The skeleton alphabets remain those of Section 1.

Seek a unit permutation with (I,W)=(h−1,3). The recipient conditions now hold at low h−1 and high offset h−3, since 3−(h−1)=W−I and I+W=h+2=F−(h−3). The cut count requires exactly one high suffix row. Maintain the following three rows, using the same input and weight normalization:
```text
low 3:           (0,0)
low h:           (h−2,1)
high m−(h−3):    (h−1,2)
```
All three satisfy their affine equations. The two low rows lie below both cuts. The high row lies in the input suffix and gives the remaining lower weight. Consequently the remaining high rows use indices [1,h−3] with weights ≥3. The remaining low rows use upper declines J=0 through h−2 and weights ≥3. The maintained row at low 3 will be used to extend the size.

### Four direct bases

For h=5,6,7,8 the following rows finish the unit permutation. The conventions (k,i) for high prefix and (k,J) for upper lows are the same as in Section 2. In each case the high input indices and the upper low declines are exactly their ranges stated above.

| h | High prefix (k,i) | Upper low (k,J) |
|---:|---|---|
| 5 | (1,2),(3,1) | (1,2),(2,3),(4,0),(7,1) |
| 6 | (1,1),(2,2),(4,3) | (1,2),(2,4),(4,0),(5,3),(8,1) |
| 7 | (1,1),(2,2),(3,3),(5,4) | (1,2),(2,4),(4,0),(5,3),(6,5),(9,1) |
| 8 | (1,1),(2,2),(3,3),(4,4),(6,5) | (1,2),(2,4),(4,0),(5,5),(6,6),(7,1),(10,3) |

The high and low upper weight declines are respectively {3,4} and {0,1,2,5} at h=5, {2,4,7} and {0,1,3,5,6} at h=6, {2,4,6,9} and {0,1,3,5,7,8} at h=7, and {2,4,6,8,11} and {0,1,3,5,7,9,10} at h=8. In each case their disjoint union is [0,2h−5], which is precisely the upper weight interval [3,F−1] measured from its far end. The maintained rows complete both alphabets. Each actual numeric host occurs once. These are auxiliary direct bases of the construction, kept separate from the accepted D223 h=8 marked witness.

### Repeatable step from h to h+4

Set h′=h+4, F′=F+8 and m′=m+16 on the unit graph. Increase every old low host and every old high offset by four. The old low reserve h+1 moves to h′+1, and the high reserve offset h−1 moves to h′−1. Carry every old row except low 3 by setting i′=i+4 and w′=w at its shifted host. This preserves the low map since k and i both increase by four, and the high map since k+i increases by eight, exactly the increase of F. The carried input set is [5,F+3] because the omitted row had i=0. Its weight set is [1,F−1] because that row had w=0. Reassign (0,0) to the new low 3.

The fresh low hosts 1,2,4 and the unfilled shifted low host 7 receive the following upper inputs. The fresh high offsets 1,2,3,4 receive the remaining lower inputs. Use T′=F′−1=F+7 for declines J=T′−i and Q=T′−w.

| Host | Input | Weight decline Q |
|---|---:|---:|
| low 1 | J=2 | 0 |
| low 2 | J=3 | 2 |
| low 4 | J=0 | 1 |
| low 7 | J=1 | 5 |
| high offset 1 | i=2 | 3 |
| high offset 2 | i=4 | 6 |
| high offset 3 | i=1 | 4 |
| high offset 4 | i=3 | 7 |

This uses exactly the remaining [1,4] ∪ [F+4,F+7] indices and the [F,F+7] weights. Directly Q=J+k−3 in the four low rows and Q=i+k in the four high rows. Thus complete input, weight and host alphabets return. The cut becomes I′=I+4 and W′=3. Carried rows preserve both threshold tests, the new high rows have i<I′ and w≥3, the new upper low rows exceed both cuts, and the reassigned low 3 remains below both. The original low h and the one high suffix offset h−3 move to h′ and h′−3. Their rows become (h′−2,1) and (h′−1,2). The low recipient h−1 moves to h′−1 and its pair is still left. The high recipient remains the sole high suffix, on the right. The actual markers and both exterior restorations at h′ follow from Section 3, with c=1 assigned to the new low 1. Other than the chosen receiving roles, the recurrence is on numerical unit slots and does not require an old physical name to keep its slot between auxiliary sizes.

For any registered h, start with the unique member of {5,6,7,8} congruent to h modulo four and take finitely many steps. Assign the final named interior branches at the two recipient slots and insert their arbitrary even increments as in Section 1. At the resulting m every specified original vertex receives one label and each terminal edge has the absolute difference used to prove the palettes. The folded skeleton and its two restored attachments complete the full [1,m] original spectrum. The only growing branches are the independently chosen names. A physical spine reversal sends s:i, b:i:u and l:i:u:e to the corresponding names with section 3−i and keeps u,e fixed. This is an isomorphism preserving every computed weight. No universal assertion about additional enlarged branches or mixed parity follows.

## 4. Disposition

D224 closes the full previously unresolved cross-interior domain with unit flanks, ℓ=2, j=2h−5 and h≥9, including independently chosen odd quotas at least three on each of the two selected branches and physical reversal. The same construction permits the unit boundary, already covered by D222. The specific proposed marking has the verified controls and the restricted W≥6 impossibility; the full positive uses a different permitted marking and recurrence. The named unequal-quota control checks both growing hosts on each actual graph. [Hand evidence](../evidence/validation/D224_TWO_LEFT_PAIR_PARITY_ADAPTED_SUPPLIER/HAND_CONTROLS.md).

There is no remaining discriminator in the registered target domain. There was no scientific numerical execution, solver, protected checker, dependency installation or dormant preparation. All accepted historical scopes, incomplete cases, held closure and insertion obligations, and deferred D207 remain separate. No successor is selected.
