# D224 named hand controls

## 1. Original definitions and retained h=8 control

Each unit profile for size h is independently fixed as one unit branch at each exterior spine vertex, two at s:1 and 2h−5 at s:2. Spine vertices s:0,s:1,s:2,s:3 are linked consecutively. Each b:i:u is joined to s:i in T, and its l:i:u:e terminals are joined only to it. S changes only the two exterior parent edges to s:1--b:0:0 and s:2--b:3:0, preserving all other named edges. A grown target has the specifically named increased terminal counts with the same actual parents and zero-based indices. In the tables, Z lists actual terminal labels in index order, and D lists their actual absolute differences from the stated center.

The accepted D223 h=8 certificate is the parity-adapted case (c,r,d,b)=(3,2,5,8) on exactly the (2,11) original and fold. The original marks (0,33,31,8,3,5), the normalized cut (9,3), and the exact restoration exchange 3↔28 remain unchanged. The hand table verifies all 33 edge weights and the independent insertion at b:1:1 and b:2:4. The auxiliary h=8 base for the new four-step supplier is a separate construction. [Immutable D223 named control](../D223_AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY/HAND_CONTROLS.md#6-the-exact-h8-interface).

## 2. Exact proposed h=9 marking, unit quotas

Here F=17,m=37,c=2,r=5,b=9,d=7. The spine labels (32,0,37,9) give actual weights (32,37,28). Left complementary pairs are 2 and 5. Right pairs are 1,3,4,6,7,8. The table gives every unit terminal and the S and T attachment differences on their actual parent edges.

| Center | Label | Z | D | S attachment | T attachment |
|---|---:|---:|---:|---:|---:|
| b:0:0 | 2 | 23 | 21 | 2 | 30 |
| b:1:0 | 35 | 19 | 16 | 35 | 35 |
| b:1:1 | 5 | 17 | 12 | 5 | 5 |
| b:2:0 | 1 | 25 | 24 | 36 | 36 |
| b:2:1 | 3 | 28 | 25 | 34 | 34 |
| b:2:2 | 4 | 27 | 23 | 33 | 33 |
| b:2:3 | 6 | 24 | 18 | 31 | 31 |
| b:2:4 | 8 | 18 | 10 | 29 | 29 |
| b:2:5 | 10 | 21 | 11 | 27 | 27 |
| b:2:6 | 11 | 20 | 9 | 26 | 26 |
| b:2:7 | 29 | 16 | 13 | 8 | 8 |
| b:2:8 | 30 | 15 | 15 | 7 | 7 |
| b:2:9 | 31 | 14 | 17 | 6 | 6 |
| b:2:10 | 33 | 13 | 20 | 4 | 4 |
| b:2:11 | 34 | 12 | 22 | 3 | 3 |
| b:2:12 | 36 | 22 | 14 | 1 | 1 |
| b:3:0 | 7 | 26 | 19 | 30 | 2 |

The terminal alphabets are [12,28] and [9,25]. The roots and slots fill their exact label complement. The edges of the skeleton fill [1,8]∪[26,37] on each graph, with the two exterior weights exchanged by 32−2=30 and 9−7=2. Adding the terminal weights gives the full [1,37] spectra. Subtracting 12 and 9 from the two terminal alphabets gives the normalized rows. At cut (11,4), the low-prefix hosts are 5,8,10,11, the high rows all have i<11,w≥4, and the other lows lie above both cuts. The recipients are actual left b:1:0 at high offset 2 and right b:2:5 at low 10. Their offsets verify W−I=3−10 and I+W=17−2, so the shared gap permits both independent increases.

## 3. Exact proposed h=10 marking, unit quotas

Here F=19,m=41,c=3,r=4,b=10,d=7. The spine labels (37,0,41,10) give weights (37,41,31). Left complementary pairs are 3 and 4. Right pairs are 1,2,5,6,7,8,9.

| Center | Label | Z | D | S attachment | T attachment |
|---|---:|---:|---:|---:|---:|
| b:0:0 | 3 | 30 | 27 | 3 | 34 |
| b:1:0 | 38 | 13 | 25 | 38 | 38 |
| b:1:1 | 4 | 27 | 23 | 4 | 4 |
| b:2:0 | 1 | 29 | 28 | 40 | 40 |
| b:2:1 | 2 | 26 | 24 | 39 | 39 |
| b:2:2 | 5 | 31 | 26 | 36 | 36 |
| b:2:3 | 6 | 19 | 13 | 35 | 35 |
| b:2:4 | 8 | 25 | 17 | 33 | 33 |
| b:2:5 | 9 | 20 | 11 | 32 | 32 |
| b:2:6 | 11 | 23 | 12 | 30 | 30 |
| b:2:7 | 12 | 22 | 10 | 29 | 29 |
| b:2:8 | 32 | 18 | 14 | 9 | 9 |
| b:2:9 | 33 | 17 | 16 | 8 | 8 |
| b:2:10 | 34 | 16 | 18 | 7 | 7 |
| b:2:11 | 35 | 15 | 20 | 6 | 6 |
| b:2:12 | 36 | 14 | 22 | 5 | 5 |
| b:2:13 | 39 | 24 | 15 | 2 | 2 |
| b:2:14 | 40 | 21 | 19 | 1 | 1 |
| b:3:0 | 7 | 28 | 21 | 34 | 3 |

The terminal alphabets are [13,31] and [10,28], and the actual skeleton fills [1,9]∪[29,41]. Both total alphabets are [0,41] and [1,41]. The exterior exchange is 3↔34 by 37−3=34 and 10−7=3. Subtracting 13 and 10 gives the normalized rows. At (12,4) the low-prefix hosts are 6,9,11,12. All highs have i<12,w≥4, and the other lows lie above both thresholds. The two receiving names b:1:0 at high offset 3 and b:2:6 at low 11 satisfy W−I=3−11 and I+W=19−3. Both increases are independent by the shared-gap rule.

## 4. New h→h+4 supplier, named unequal quotas

Start with the new auxiliary h=5 base in the proof and take one inductive step to h=9. At unit size F=17,m=37. This alternative marking uses spine (29,0,37,10), exterior hosts 1 and 9, and left pairs 1 and 8. It has cut (8,3). Choose actual b:1:0 at low 8 and b:2:8 at high offset 6. The unit inputs at low 3 and low 9 have (i,w)=(0,0),(7,1). The high suffix at offset 6 is (8,2); all the other highs lie in the prefix with weights ≥3. Part 3 of the proof returns these rows under the four-step recurrence.

Grow the left quota from 1 to 5 and the right quota from 1 to 3 at these names. Here G=6, so F grows to 23 and m to 43. Give reflected local pairs {0,5},{1,4} to the low host, and {2,3} to the high. The fresh normalized rows at the low are (8,3),(9,4),(12,7),(13,8). At the high they are (10,6),(11,5). Old i≥8,w≥3 shift by six on their respective axes. At each beneficiary the carried original terminal is listed first, at index zero. The grown profile is `[[1],[5,1],[1,1,1,1,1,1,1,1,3,1,1,1,1],[1]]`. Spine weights at unit size are (29,37,27) and at grown spine (35,0,43,10) are (35,43,33).

| Center name | Unit center / Z / D | Grown center / Z / D |
|---|---|---|
| b:0:0 | 1 / (26) / (25) | 1 / (32) / (31) |
| b:1:0 | 8 / (24) / (16) | 8 / (30,20,21,24,25) / (22,12,13,16,17) |
| b:1:1 | 36 / (14) / (22) | 42 / (14) / (28) |
| b:2:0 | 2 / (25) / (23) | 2 / (31) / (29) |
| b:2:1 | 3 / (12) / (9) | 3 / (12) / (9) |
| b:2:2 | 4 / (28) / (24) | 4 / (34) / (30) |
| b:2:3 | 5 / (22) / (17) | 5 / (28) / (23) |
| b:2:4 | 6 / (21) / (15) | 6 / (27) / (21) |
| b:2:5 | 7 / (27) / (20) | 7 / (33) / (26) |
| b:2:6 | 11 / (23) / (12) | 11 / (29) / (18) |
| b:2:7 | 30 / (17) / (13) | 36 / (17) / (19) |
| b:2:8 | 31 / (20) / (11) | 37 / (26,22,23) / (11,15,14) |
| b:2:9 | 32 / (18) / (14) | 38 / (18) / (20) |
| b:2:10 | 33 / (15) / (18) | 39 / (15) / (24) |
| b:2:11 | 34 / (13) / (21) | 40 / (13) / (27) |
| b:2:12 | 35 / (16) / (19) | 41 / (16) / (25) |
| b:3:0 | 9 / (19) / (10) | 9 / (19) / (10) |

The exact S attachment lists in table order are (1,8,36,35,34,33,32,31,30,26,7,6,5,4,3,2,28) and (1,8,42,41,40,39,38,37,36,32,7,6,5,4,3,2,34). The T lists differ only by exchanging the first and last entries, at unit size from |29−1|=28 and |10−9|=1, and at grown size from |35−1|=34 and |10−9|=1. Both terminal alphabets check directly as [12,28] and [9,25] for the unit witness, and [12,34] and [9,31] after growth. The actual skeleton completes [1,37] on each unit graph and [1,43] on each grown graph. Roots and slots complete the vertex alphabets. This uses actual independently chosen names and unequal quotas at two hosts of opposite affine type.

Physical reversal relocates every named row to section 3−i, preserves the indices within the section and reverses the spine order. Each attached terminal keeps exactly its old center under that mapping. The two exterior restoration edges exchange their physical roles and all edge differences stay the same.

All controls are symbolic or hand arithmetic. No scientific module, numerical discovery, protected checker or solver was executed.
