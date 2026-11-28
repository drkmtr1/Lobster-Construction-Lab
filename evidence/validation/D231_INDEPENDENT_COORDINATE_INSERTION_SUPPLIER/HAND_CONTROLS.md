# D231 — Named hand controls and adverse cut

The named profiles, exact branch indices and roles, original incidences, fold and reversal are fixed in [ORIGINALS.md](ORIGINALS.md). Every terminal tuple in this record is in original index order, and its next tuple gives the actual endpoint differences in the same order. At h=10 a terminal row (i,w) decodes as label 13+i and difference 10+w. With F=11 the reflected upper coordinate y decodes to actual index 11+2n−4−y on its own track.

## 1. Source, transported rows and skeleton

The independent h=6,S2 source is the retained D228 unit record:
```text
L1 (5,7)   L2 (7,8)   L3 (10,10)   L4 (2,1)   L5 (8,6)  L6 (3,0)  L8 (9,4)
H1 (0,9)   H2 (6,2)   H3 (4,3)     H4 (1,5).
```
Both columns give 0,…,10, the seven low shifts are 2,1,0,−1,−2,−3,−5 and the high sums 9,8,7,6. After omitting L3/L4 and shifting offsets, the carried rows in order L5,L6,L9,L10,L12,H5,H6,H7,H8 are:
```text
n=12: (17,15),(19,16),(20,14),(15,8),(21,12),(12,17),(18,10),(16,11),(13,13)
n=34: (39,37),(41,38),(42,36),(37,30),(43,34),(34,39),(40,32),(38,33),(35,35).
```
These use respectively (12,8) and (34,30) translations. At either final size the named spine labels are (m−9,0,m,11), and its weights are (m−9,m,m−11). Folded attachments to left hosts L1,H1,L9 have weights 1,m−1,9. At the right root any low Lk has folded attachment m−k and any high Hk has k, including the flank L10 with m−10. This gives [1,9]∪[m−12,m] in the fold. In the original only b:0:0 and b:3:0 attachments change, to weights |m−9−1|=m−10 and |11−10|=1.

## 2. Q=9 sparse control, m=57

At n=12 the double-track coordinates {0,6,9} all cross. The forced LU crossings are 8,10,11. The L3 rows are the seven upper and one lower identities, with the top returned identity at index 34. Upper reflection decodes by 31−y. Thus the carried replacements L7 and L8 are (23,19),(7,2), L4 returns (2,1), and the seven exceptional rows decode with no repeats. The spine is (48,0,57,11), with actual edge weights (48,57,46).

| Named branch | Role | Center | Terminals | Terminal differences |
|---|---|---:|---|---|
| b:0:0 | L1 | 1 | (14) | (13) |
| b:1:0 | H1 | 56 | (39) | (17) |
| b:1:1 | L9 | 9 | (33) | (24) |
| b:2:0 | L3 | 3 | (18,37,40,41,42,43,45,46,47) | (15,34,37,38,39,40,42,43,44) |
| b:2:1 | H3 | 54 | (13,19,21,22,23,24,35,38,44) | (41,35,33,32,31,30,19,16,10) |
| b:2:2 | L2 | 2 | (16) | (14) |
| b:2:3 | L4 | 4 | (15) | (11) |
| b:2:4 | H2 | 55 | (27) | (28) |
| b:2:5 | H4 | 53 | (17) | (36) |
| b:2:6 | L5 | 5 | (30) | (25) |
| b:2:7 | L6 | 6 | (32) | (26) |
| b:2:8 | L7 | 7 | (36) | (29) |
| b:2:9 | L8 | 8 | (20) | (12) |
| b:2:10 | L12 | 12 | (34) | (22) |
| b:2:11 | H5 | 52 | (25) | (27) |
| b:2:12 | H6 | 51 | (31) | (20) |
| b:2:13 | H7 | 50 | (29) | (21) |
| b:2:14 | H8 | 49 | (26) | (23) |
| b:3:0 | L10 | 10 | (28) | (18) |

Terminal labels partition [13,47] and their subtractions partition [10,44]. Spine and branch labels partition [0,12]∪[48,57]. Folded attachments in table order are (1,56,9,54,3,55,53,2,4,52,51,50,49,45,5,6,7,8,47). Including the three spine weights gives [1,9]∪[45,57]. The original endpoints exchange 1↔47. The exact original and fold are each graceful; their full reversed certificates are obtained by replacing the section index with 3−i and using spine (11,57,0,48). This resolves the exact former comparison at offset 3.

## 3. Independent (7,3,19,5) control, m=101

Start with Q=19 and n=22. Reserve all five double identities at 8,9,10,11,13. The remaining double coordinates {0,6,12,14,15,16,17,19} all cross. Forced LU crossings start at 18,20,21. Insert widths 5 and 1 at the two pair-1 cuts, width 2 at pair 2 and width 4 at pair 4. The final n′ is 34, F′=79 and m=101. Upper reflection now decodes by 75−y. The four aligned starts for the new lower/upper blocks are (10,8),(16,14),(18,17),(21,22). The fresh four-row cycles are specified by their (x,y,s) triples:
```text
pair 1: (10,8,2), (11,9,2), (14,12,2)
pair 2: (18,17,1)
pair 4: (22,23,−1), (24,25,−1).
```
In the split third pair of positions at pair 1, the second-gap lower start is 11+5=16 and its upper start is 9+5=14. Pair 2 sees both earlier widths, and pair 4 sees all earlier widths. The old coordinate between the split positions is 15 on the lower track and 13 on the upper track. This verifies the distance-two pair explicitly.

The old double identities at 8,9,10,11,13 map to lower 8,9,15,17,25 and upper 13,15,16,19,21. The double crossings in both tracks map to 0,6,20,26,27,28,29,31, and the three forced LU crossings map to 30,32,33. The high exceptional H2 and L7 become (36,40) and (45,41) in actual indices, while L8 remains (7,2). Return (2,1) at L4 and (78,78) at L3. The spine is (92,0,101,11) with weights (92,101,90).

| Named branch | Role | Center | Terminals | Terminal differences |
|---|---|---:|---|---|
| b:0:0 | L1 | 1 | (14,23,24,27,74,77,78) | (13,22,23,26,73,76,77) |
| b:1:0 | H1 | 100 | (25,26,29,76,79,80,83) | (75,74,71,24,21,20,17) |
| b:1:1 | L9 | 9 | (55) | (46) |
| b:2:0 | L2 | 2 | (16,31,70) | (14,29,68) |
| b:2:1 | L3 | 3 | (18,21,22,28,30,38,67,69,72,73,75,81,84,85,86,87,89,90,91) | (15,18,19,25,27,35,64,66,69,70,72,78,81,82,83,84,86,87,88) |
| b:2:2 | L4 | 4 | (15,35,37,64,66) | (11,31,33,60,62) |
| b:2:3 | H2 | 99 | (32,49,71) | (67,50,28) |
| b:2:4 | H3 | 98 | (13,19,33,39,40,41,42,43,44,45,46,57,59,60,61,62,68,82,88) | (85,79,65,59,58,57,56,55,54,53,52,41,39,38,37,36,30,16,10) |
| b:2:5 | H4 | 97 | (17,34,36,63,65) | (80,63,61,34,32) |
| b:2:6 | L5 | 5 | (52) | (47) |
| b:2:7 | L6 | 6 | (54) | (48) |
| b:2:8 | L7 | 7 | (58) | (51) |
| b:2:9 | L8 | 8 | (20) | (12) |
| b:2:10 | L12 | 12 | (56) | (44) |
| b:2:11 | H5 | 96 | (47) | (49) |
| b:2:12 | H6 | 95 | (53) | (42) |
| b:2:13 | H7 | 94 | (51) | (43) |
| b:2:14 | H8 | 93 | (48) | (45) |
| b:3:0 | L10 | 10 | (50) | (40) |

Terminal labels partition [13,91], and terminal differences partition [10,88]. The branches and spine consume [0,12]∪[92,101] in labels. The folded branch attachments in table order have differences (1,100,9,99,98,97,2,3,4,96,95,94,93,89,5,6,7,8,91). Along with the spine these give [1,9]∪[89,101]. The original exchanges 1↔91 at its prescribed pair of edges. The full reversed certificates replace each section index by 3−i and use spine (11,101,0,92). Every branch and terminal index and corresponding edge difference is transported.

## 4. Adverse crossing and boundary checks

At the first pair-1 cuts 10 lower and 8 upper a double H3 crossing at coordinate 8 is legal in the unexpanded sparse supply if 8 was chosen for crossings. It has lower indicator zero and upper indicator one. A positive width on that cut alone changes its displacement, so the two identical-coordinate H3 crossings cease to match the actual H3 rule. Reserving identities exactly where those cut indicators can disagree removes the obstruction. The p=2 split gives just two fresh positions at lower 10,12 and upper 8,10. At p=4 one contiguous block uses positions relative to the gap start (0,2),(1,3), with no second gap. All zero widths leave the supplied sparse rows untouched. These statements concern this insertion alignment, not general feasibility of a packet with a different allocation.
