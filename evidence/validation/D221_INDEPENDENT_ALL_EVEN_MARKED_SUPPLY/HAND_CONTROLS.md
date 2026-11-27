# D221 named hand controls

## Independent graph definitions

The four main verification profiles and the pair-relocated companion below define T before labeling. Each has the three literal spine edges on s:0 through s:3. The entry at section i and zero-based position u defines b:i:u and its prescribed number of terminals l:i:u:e at zero-based indices e. The branch attaches to s:i and all its terminals attach to that branch. The folded source S differs only in the two exterior branch attachments, to s:1 and s:2 respectively. These rules determine all named vertices and both edge sets, with no numerical data needed to define either. The tables list terminal labels and weights in original index order. For an interior center its attachment weight is common to both graphs.

## 1. Simultaneous growth at all four D220 roles

Take T=`[[4],[4,4],[2,2,2,2,2],[4]]`, with α=β=s=r=1. The input has 26 terminals, 38 edges and 39 vertices. The spine labels in order are (37,0,38,5) with weights (37,38,33). A grows F from 18 to 22, giving fresh normalized indices [9,12] and weights [7,10]. The reflected local pairs are {0,3} and {1,2}. Assign the first to host 3 using identity, producing (i,w)=(9,7),(12,10), and the second to high offset 2 using reflection, producing (10,9),(11,8). The distinguished high row is (0,19) and the top host-1 rows are (20,20),(21,21). After B at s=1 the distinguished row is (0,21) and the top rows are (22,22),(23,23). Host 2 adds (1,0),(21,20) and every earlier row other than the three anchors shifts by (1,1). C shifts every B row by (1,1) and adds (0,0),(25,25) at host 1.

| Center name | Label | Terminal labels | Actual terminal weights | S attachment | T attachment |
|---|---:|---|---|---:|---:|
| b:0:0 | 2 | (9,16,28,29) | (7,14,26,27) | 2 | 35 |
| b:1:0 | 1 | (7,30,31,32) | (6,29,30,31) | 1 | 1 |
| b:1:1 | 36 | (8,19,20,24) | (28,17,16,12) | 36 | 36 |
| b:2:0 | 4 | (17,26) | (13,22) | 34 | 34 |
| b:2:1 | 6 | (14,15) | (8,9) | 32 | 32 |
| b:2:2 | 33 | (12,13) | (21,20) | 5 | 5 |
| b:2:3 | 34 | (11,23) | (23,11) | 4 | 4 |
| b:2:4 | 35 | (10,25) | (25,10) | 3 | 3 |
| b:3:0 | 3 | (18,21,22,27) | (15,18,19,24) | 35 | 2 |

The terminal labels give exactly [7,32] and the weights give [6,31]. With the two root labels and slot bands, both vertex alphabets are [0,38]. The skeleton weights are [1,5]∪[32,38] in both graphs, with the displayed swap (2,35) to (35,2), so the complete spectra are [1,38].

For the companion `[[4],[4,4,2,2],[2,2,2],[4]]` at the same size, keep the exterior and spine rows. The ordered left interior center labels are (1,36,4,34), using the terminal tuple at each of those labels above. The ordered right labels are (6,33,35) with their same tuples. This explicitly lifts to all its original names. The moved pair {4,34} contributes (34,4) before and (4,34) after the move. The exact label and weight partitions are unchanged.

## 2. Flexible marks at the even-h boundary

Take T=`[[2],[2,2],[2,2,2,2,2,2,2],[2]]`, with h=6, F=22 and m=36. The spine labels (35,0,36,7) give weights (35,36,29). Pairs indexed 1 and 3 go left. The positive host order is (1,34,2,33,3,32,4,31,5,30,6). First retain (28,29) at 1, leaving [8,27]. Split into [8,17] and [18,27]. Subsequent moves alternate retaining one lower endpoint from each interval at a +1 jump and one upper endpoint from each at a −1 jump. The chronological retentions are
```text
34:(8,18)   2:(17,27)   33:(9,19)   3:(16,26)   32:(10,20)
4:(15,25)   31:(11,21)  5:(14,24)   30:(12,22)  6:(13,23) final
```

| Center name | Label | Terminal labels | Actual terminal weights | S attachment | T attachment |
|---|---:|---|---|---:|---:|
| b:0:0 | 3 | (16,26) | (13,23) | 3 | 32 |
| b:1:0 | 1 | (28,29) | (27,28) | 1 | 1 |
| b:1:1 | 33 | (9,19) | (24,14) | 33 | 33 |
| b:2:0 | 2 | (17,27) | (15,25) | 34 | 34 |
| b:2:1 | 5 | (14,24) | (9,19) | 31 | 31 |
| b:2:2 | 6 | (13,23) | (7,17) | 30 | 30 |
| b:2:3 | 30 | (12,22) | (18,8) | 6 | 6 |
| b:2:4 | 31 | (11,21) | (20,10) | 5 | 5 |
| b:2:5 | 32 | (10,20) | (22,12) | 4 | 4 |
| b:2:6 | 34 | (8,18) | (26,16) | 2 | 2 |
| b:3:0 | 4 | (15,25) | (11,21) | 32 | 3 |

The terminal labels are exactly [8,29], complementing the 15 skeleton labels. The terminal weights are [7,28], complementing the actual skeleton spectrum [1,6]∪[29,36]. All 37 labels and all 36 edges are accounted for on each graph. Restoration exchanges 3 and 32.

## 3. Odd h with the exceptional reserve index e=4

Take T=`[[2],[2,4,2,2],[2,2,2],[2]]`, with h=5, F=20 and m=32. Left pairs are 1,2,4. The spine labels (28,0,32,6) give (28,32,26). Split the initial interval [7,26] into [7,16] and [17,26] at host 1. The host order is (1,31,2,30,3,29,4,27,5). The successive returning sums are 32,33,32,33,32,33,31,32. At 4 the exceptional jump −2 retains two upper labels from each interval. Just before that move the palette is [10,13]∪[20,23]. It moves [10,11]∪[20,21] to 27, whose +1 jump leaves one lower endpoint from each interval and moves (11,21) to 5.

| Center name | Label | Terminal labels | Actual terminal weights | S attachment | T attachment |
|---|---:|---|---|---:|---:|
| b:0:0 | 1 | (16,26) | (15,25) | 1 | 27 |
| b:1:0 | 2 | (15,25) | (13,23) | 2 | 2 |
| b:1:1 | 4 | (12,13,22,23) | (8,9,18,19) | 4 | 4 |
| b:1:2 | 30 | (8,18) | (22,12) | 30 | 30 |
| b:1:3 | 31 | (7,17) | (24,14) | 31 | 31 |
| b:2:0 | 3 | (14,24) | (11,21) | 29 | 29 |
| b:2:1 | 27 | (10,20) | (17,7) | 5 | 5 |
| b:2:2 | 29 | (9,19) | (20,10) | 3 | 3 |
| b:3:0 | 5 | (11,21) | (6,16) | 27 | 1 |

The terminal label alphabet is [7,26] and the terminal spectrum is [6,25]. The other 13 labels are the slots and roots, and the remaining weights [1,5]∪[26,32] arise on the actual skeleton in each graph. The exterior weights 1 and 27 exchange under restoration.

## 4. One four-host step at odd h and an adverse late-repair comparison

Take T=`[[2],[2,2],[2,2,2,2,2,2,2,2,2],[2]]`, with h=7, F=26 and m=42. Left pairs are 1 and 3. The spine labels (41,0,42,7) give (41,42,35). With initial Z=9,v=1,N=26 and D=1,K=4, the joint step at 1,2,40,39 uses terminal labels [9,12]∪[31,34]. Their eight weights are [8,9]∪[28,33]. It returns the contiguous interval [13,30] at anchor 3, with weights [10,27] and endpoint sum 43. The relative D220 pattern gives actual low roles (3,4,5,6,8) and high roles (38,37,36,35) in order of increasing high offset. This gives the following full named certificate.

| Center name | Label | Terminal labels | Actual terminal weights | S attachment | T attachment |
|---|---:|---|---|---:|---:|
| b:0:0 | 3 | (29,30) | (26,27) | 3 | 38 |
| b:1:0 | 1 | (33,34) | (32,33) | 1 | 1 |
| b:1:1 | 39 | (10,31) | (29,8) | 39 | 39 |
| b:2:0 | 2 | (11,32) | (9,30) | 40 | 40 |
| b:2:1 | 5 | (22,27) | (17,22) | 37 | 37 |
| b:2:2 | 6 | (21,26) | (15,20) | 36 | 36 |
| b:2:3 | 8 | (18,19) | (10,11) | 34 | 34 |
| b:2:4 | 35 | (16,17) | (19,18) | 7 | 7 |
| b:2:5 | 36 | (15,23) | (21,13) | 6 | 6 |
| b:2:6 | 37 | (14,25) | (23,12) | 5 | 5 |
| b:2:7 | 38 | (13,24) | (25,14) | 4 | 4 |
| b:2:8 | 40 | (9,12) | (31,28) | 2 | 2 |
| b:3:0 | 4 | (20,28) | (16,24) | 38 | 3 |

The terminal label and weight sets are [9,34] and [8,33], respectively. The slots and roots fill the rest of [0,42], and the two actual skeletons have [1,7]∪[34,42]. The outer edges exchange weights 3 and 38, giving full spectra [1,42].

For comparison on these same named graphs, first retaining (33,34) at low 1 by a single transfer leaves [9,32] at high 40. Split into [9,20] and [21,32]. Three successive quota-two trims retain (9,21) at 40, (20,32) at 2 and (10,22) at 39. The active low 3 receives [11,19]∪[23,31], with cross-sum 42, length nine per band and actual weight lanes [8,16] and [20,28]. Here v=3,r=4, A={0,1,2,3,5} and B={1,2,3,4}. The sum requirement is 11+10=21, while the four largest indices (5,6,7,8) exceed the four smallest (0,1,2,3) in sum by 20. This rejects a simultaneous late allocation on those lanes and those remaining hosts. The contiguous positive above supplies the same target without those lane premises.

All checks were by hand. No diagnostic, scientific program, original-target checker or solver was used.
