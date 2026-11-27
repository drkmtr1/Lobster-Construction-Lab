# D223 named hand controls

## 1. Actual graph definitions

Each profile below fixes the target T before assigning numbers. Its spine edges are s:0--s:1, s:1--s:2 and s:2--s:3. In section i, branch entry u gives vertex b:i:u adjacent to s:i and its specified number of terminals l:i:u:e, e from zero up to quota minus one, attached to that center. The folded source S on the same names changes only the two exterior center attachments inward to s:1 and s:2. Each terminal tuple is in increasing actual index order. In the tables, a single interior attachment weight is common to S and T.

## 2. Exact D222 discriminator positive

Use T=`[[3],[3,3],[1,1,1,1,1],[1]]`, h=5,F=15,m=27. Its spine labels in original order are (26,0,27,7) and its actual spine weights are (26,27,20).

| Center name | Label | Terminal labels | Actual terminal weights | S attachment | T attachment |
|---|---:|---|---|---|---|
| b:0:0 | 3 | (8,15,22) | (5,12,19) | s:1, 3 | s:0, 23 |
| b:1:0 | 1 | (12,17,19) | (11,16,18) | s:1, 1 | s:1, 1 |
| b:1:1 | 24 | (11,16,18) | (13,8,6) | s:1, 24 | s:1, 24 |
| b:2:0 | 2 | (9) | (7) | s:2, 25 | s:2, 25 |
| b:2:1 | 5 | (14) | (9) | s:2, 22 | s:2, 22 |
| b:2:2 | 6 | (20) | (14) | s:2, 21 | s:2, 21 |
| b:2:3 | 23 | (13) | (10) | s:2, 4 | s:2, 4 |
| b:2:4 | 25 | (10) | (15) | s:2, 2 | s:2, 2 |
| b:3:0 | 4 | (21) | (17) | s:2, 23 | s:3, 3 |

The terminal labels occupy [8,22] and their weights [5,19]. The roots and slots give the full complementary alphabet. With the three spine edges, the actual S and T attachment spectra are each [1,4]∪[20,27]. Thus the complete alphabets are [0,27] and both spectra [1,27], with the two actual exterior weights exchanged 3↔23. No other incidences change. In the packet construction the instance starts with u=0,v=1,β=0 and F=13. The one outer reflected pair of [2,7] leaves [3,6]. After enlarging low 3 by two, these are exactly the named assignments above.

## 3. Odd packet branch and a unit case with no cross-interior shared gap

For the packet branch u=1,v=2,β=1,r=0 take T=`[[1],[5,5],[1,1,1,3,1],[1]]`, h=5,F=19,m=31. In normalized coordinates the two initial cycles are 0→1→15→0 and 14→16→18→17→14. The interval [2,13] has sum 15. The last single packet is 2→4→11→13→2 with added pair 3↔12. The remaining [5,10] uses the tail pair 8↔10 and identity 6, with {5,7,9} at high m−4. The actual spine is (30,0,31,7), with weights (30,31,24).

| Center name | Label | Terminal labels | Terminal weights | S attachment | T attachment |
|---|---:|---|---|---:|---:|
| b:0:0 | 3 | (14) | (11) | 3 | 27 |
| b:1:0 | 1 | (10,16,19,22,24) | (9,15,18,21,23) | 1 | 1 |
| b:1:1 | 28 | (11,12,20,21,23) | (17,16,8,7,5) | 28 | 28 |
| b:2:0 | 2 | (8) | (6) | 29 | 29 |
| b:2:1 | 5 | (18) | (13) | 26 | 26 |
| b:2:2 | 6 | (25) | (19) | 25 | 25 |
| b:2:3 | 27 | (13,15,17) | (14,12,10) | 4 | 4 |
| b:2:4 | 29 | (9) | (20) | 2 | 2 |
| b:3:0 | 4 | (26) | (22) | 27 | 3 |

The terminal alphabets are [8,26] for labels and [5,23] for weights, and skeleton weights are [1,4]∪[24,31]. The roots and slots complete [0,31], and both graphs have spectrum [1,31].

The handed-down [D222 unit seed](../D222_PARITY_COMPATIBLE_ALL_ODD_SUPPLY/HAND_CONTROLS.md#1-director-seed) is an adverse shared-gap control in its own h=5 geometry. At its verified marks the two actual left interior roles are low 1 and high offset 3. An all-unit seed has three high rows and F=9, so both a low recipient and a high offset must be even by the necessary cut congruences. Neither left interior can receive a shared insertion with a right interior on that particular skeleton, although the actual labeling is graceful on both graphs. This is separate from the h=8 adverse cut on a positive h=8 seed.

## 4. h=6 named seed and unequal growth

For the (2,7) unit profile, use spine (23,0,25,6) with weights (23,25,19). For its growth example give b:1:1 quota five and b:2:2 quota three, all others one, with h=6,F=17,m=31. The grown spine is (29,0,31,6), with weights (29,31,25). Put G=6 at I=7,W=3, give the orbit {0,5} to low 7 and the other two orbits to high m−1. The two configurations are shown together. Each table entry is center label / terminal labels / terminal weights.

| Center | Unit seed | Grown original |
|---|---|---|
| b:0:0 | 2 / (18) / (16) | 2 / (24) / (22) |
| b:1:0 | 1 / (16) / (15) | 1 / (22) / (21) |
| b:1:1 | 24 / (14) / (10) | 30 / (14,17,18,19,20) / (16,13,12,11,10) |
| b:2:0 | 3 / (11) / (8) | 3 / (11) / (8) |
| b:2:1 | 5 / (19) / (14) | 5 / (25) / (20) |
| b:2:2 | 7 / (13) / (6) | 7 / (13,16,21) / (6,9,14) |
| b:2:3 | 8 / (15) / (7) | 8 / (15) / (7) |
| b:2:4 | 20 / (9) / (11) | 26 / (9) / (17) |
| b:2:5 | 21 / (12) / (9) | 27 / (12) / (15) |
| b:2:6 | 22 / (10) / (12) | 28 / (10) / (18) |
| b:3:0 | 4 / (17) / (13) | 4 / (23) / (19) |

In actual branch table order the S attachment weights are (2,1,24,22,20,18,17,5,4,3,21) at m=25, and (2,1,30,28,26,24,23,5,4,3,27) at m=31. The T attachment weights exchange only the first and last entries, by subtracting from actual s:0 and s:3. The two terminal alphabets for the seed are [9,19] and [6,16], and for the grown labels are [9,25] and [6,22]. The spine and exact attachments complete both spectra to [1,25] and [1,31]. The actual label partitions complete [0,25] and [0,31]. In the seed the low rows below both thresholds occur at labels 3,7,8 and the high rows all have i<7,w≥3, as obtained by subtracting 9 from terminal labels and 6 from weights. The other splits use the same numerical rows and move only whole unforced pairs, each with two unit quotas.

## 5. h=7 named seed and unequal growth

For the (2,9) unit profile, use spine (28,0,29,9) with weights (28,29,20). For the growth example set b:1:1 to five and b:2:4 to three, leaving all other quotas one. The grown spine is (34,0,35,9), with weights (34,35,26). Use I=7,W=2, G=6, giving the orbit {0,5} to low 8 and the two other pairs to high m−4.

| Center | Unit label / terminals / weights | Grown label / terminals / weights |
|---|---|---|
| b:0:0 | 4 / (11) / (7) | 4 / (11) / (7) |
| b:1:0 | 1 / (20) / (19) | 1 / (26) / (25) |
| b:1:1 | 25 / (14) / (11) | 31 / (14,18,19,20,21) / (17,13,12,11,10) |
| b:2:0 | 2 / (17) / (15) | 2 / (23) / (21) |
| b:2:1 | 3 / (21) / (18) | 3 / (27) / (24) |
| b:2:2 | 6 / (22) / (16) | 6 / (28) / (22) |
| b:2:3 | 7 / (19) / (12) | 7 / (25) / (18) |
| b:2:4 | 8 / (16) / (8) | 8 / (16,17,22) / (8,9,14) |
| b:2:5 | 23 / (13) / (10) | 29 / (13) / (16) |
| b:2:6 | 24 / (15) / (9) | 30 / (15) / (15) |
| b:2:7 | 26 / (12) / (14) | 32 / (12) / (20) |
| b:2:8 | 27 / (10) / (17) | 33 / (10) / (23) |
| b:3:0 | 5 / (18) / (13) | 5 / (24) / (19) |

The S attachment weights in branch table order are (4,1,25,27,26,23,22,21,6,5,3,2,24) at m=29 and (4,1,31,33,32,29,28,27,6,5,3,2,30) at m=35. The T attachment lists exchange the first and last entries by the actual endpoint subtractions. The terminal labels and weights are [10,22] and [7,19] for the seed, [10,28] and [7,25] after growth. The exact alphabets and spectra are [0,m] and [1,m] on both graphs. Subtracting 10,7 gives the normalized seed rows. The low-prefix rows are those at 4,8, and all highs have i<7,w≥2. A whole unforced pair with its unit quotas can move to any prescribed side in the other size splits.

## 6. The exact h=8 interface

Specify the (2,11) unit profile with the graph definition in Section 1. It has 33 edges and 34 vertices. The spine labels (31,0,33,8) give weights (31,33,25).

| Center | Label | Terminal label | Terminal weight | S attachment | T attachment |
|---|---:|---:|---:|---:|---:|
| b:0:0 | 3 | 24 | 21 | 3 | 28 |
| b:1:0 | 2 | 20 | 18 | 2 | 2 |
| b:1:1 | 30 | 16 | 14 | 30 | 30 |
| b:2:0 | 1 | 23 | 22 | 32 | 32 |
| b:2:1 | 4 | 13 | 9 | 29 | 29 |
| b:2:2 | 6 | 25 | 19 | 27 | 27 |
| b:2:3 | 7 | 22 | 15 | 26 | 26 |
| b:2:4 | 9 | 19 | 10 | 24 | 24 |
| b:2:5 | 10 | 18 | 8 | 23 | 23 |
| b:2:6 | 26 | 15 | 11 | 7 | 7 |
| b:2:7 | 27 | 14 | 13 | 6 | 6 |
| b:2:8 | 28 | 11 | 17 | 5 | 5 |
| b:2:9 | 29 | 17 | 12 | 4 | 4 |
| b:2:10 | 32 | 12 | 20 | 1 | 1 |
| b:3:0 | 5 | 21 | 16 | 28 | 3 |

The actual terminal label and weight alphabets are [11,25] and [8,22]. The roots and slots complete [0,33], and the spine and attachments fill [1,7]∪[23,33] in both graphs. The original exchange is 3↔28, with all other endpoints untouched. Subtract 11 from terminal labels and 8 from weights for the normalized rows. Among low rows, exactly those at 4,9,10 are below input 9 and output 3. All high rows are below input 9 and at or above output 3. The actual receivers are b:2:4 at low 9 and b:1:1 at high offset 3. Section 2 of the manuscript supplies the all-width proof. As a finite enlargement check, G=4 puts normalized fresh rows (9,3),(12,6) at low 9 and (10,5),(11,4) at high offset 3. The other rows shift above the cuts by four, the high labels and root m shift by four, and the two recipients have quota three each. The old and new resources partition [0,18] in both normalized alphabets.

At the adverse cut (8,4), b:2:4 has normalized old row (8,2). Transporting i but leaving w fixed violates the required low difference formula for any positive width. This happens even though the recipient equations for low 7 and high offset 3 hold there. The successful cut (9,3) and its witness supersede the dormant preparation condition.

## 7. Unbounded series and a first induction step

The exact table of three unit bases in the manuscript has normalized rows for every physical host. To emit the named graphs for each base, use spine labels (m−(h−2),0,m,h), exterior centers (1,h−1), left pairs (1,h−2,h−3), right pair h−1, and allocate the remaining pairs to meet the actual side counts. In the first left recipient position use the high offset h−3. In the first right recipient position use low h+1, and assign all remaining unit interior names in increasing numerical slot order. At each host the actual unit terminal label is h+3+i, its actual weight h+w. These rules specify every named edge and label, including for the (4,3) base.

For an explicit induction control take h=5 to h=8 in that series, with F changing 9→15. The reserves on the unit h=8 graph are a=27,b=8 and exterior marks c=1,d=7. Its new low indices 1,3,5 use i=12,13,14 and w=14,13,12, respectively. The new high offsets 1,2,3 use i=2,3,1 and w=11,9,10. Low 2 is (0,1). The carried base rows use indices [4,11] and differences [0,8] minus 1. Thus the complete resources are [0,14]. The new cut is (8,2) and the recipients are low 9 and high offset 5. On the (4,9) original the left interior labels in the described naming rule are (28,5,6,32). The remaining right interior labels are (9,2,3,4,10,26,29,30,31). The given numerical rows and actual difference map explicitly determine their indexed terminals. The roots and slots give skeleton weights [1,7]∪[23,33], and the affine rows give [8,22] for the terminal edges. Restoring the two attachments exchanges 1 and 26 because 27−1=26=33−7 and 8−7=1. This is an example of the repeatable step with different allowed marks, not another registered diagnostic.

All evidence is exact proof or hand arithmetic. No scientific module, numerical search, solver, protected checker or diagnostic was used.
