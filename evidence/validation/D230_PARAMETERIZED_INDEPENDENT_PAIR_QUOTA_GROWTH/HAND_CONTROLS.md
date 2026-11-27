# D230 — Named hand controls

The target profiles, physical branch indices, fold and numerical role assignment below are fixed before evaluating the rows. Each number in a terminal tuple is assigned to the corresponding original increasing terminal index. Each displayed difference comes from actual endpoint subtraction. These two controls use only fixed hand arithmetic.

## 1. Independently fixed originals and fold

For q=2 and q=5 use h=10, ℓ=2, j=15 and the exact same ordered role assignment:
```text
original profile = [[q],[q,1],[q,q,q,q,q,q,1,1,1,1,1,1,1,1,1],[1]]
left pairs = 1,9
right pairs = 2,3,4,5,6,7,8
unpaired slots 10,11,12 on the right
```
The respective terminal counts are 27 and 51, and the originals have 49 and 73 edges. The ordered spine labels are (m−9,0,m,11). The original has the three actual spine edges, one edge from s:i to each indexed b:i:a listed in the tables, and one edge between b:i:a and each named l:i:a:e for its declared quota and no other edges. In the fold move exactly s:0--b:0:0 to s:1--b:0:0 and s:3--b:3:0 to s:2--b:3:0. These rules specify both separate graphs even before any labels are assigned. The fixed role and folded attachment weight at each branch are as follows. The remaining folded skeleton edges are the spine edges of weights (m−9,m,m−11).

| Branch | Role | Folded attachment difference |
|---|---|---:|
| b:0:0 | L1 | 1 |
| b:1:0 | H1 | m−1 |
| b:1:1 | L9 | 9 |
| b:2:0 | L2 | m−2 |
| b:2:1 | L3 | m−3 |
| b:2:2 | L4 | m−4 |
| b:2:3 | H2 | 2 |
| b:2:4 | H3 | 3 |
| b:2:5 | H4 | 4 |
| b:2:6 | L5 | m−5 |
| b:2:7 | L6 | m−6 |
| b:2:8 | L7 | m−7 |
| b:2:9 | L8 | m−8 |
| b:2:10 | L12 | m−12 |
| b:2:11 | H5 | 5 |
| b:2:12 | H6 | 6 |
| b:2:13 | H7 | 7 |
| b:2:14 | H8 | 8 |
| b:3:0 | L10 | m−10 |

Use the D228 independently supplied h=6, F=11, S2 allocation as the source. Its complete row record in (i,w) coordinates is
```text
L1 (5,7), L2 (7,8), L3 (10,10), L4 (2,1), L5 (8,6), L6 (3,0), L8 (9,4)
H1 (0,9), H2 (6,2), H3 (4,3), H4 (1,5).
```
The two columns each give 0,…,10. The L displacements are 2,1,0,−1,−2,−3,−5, and the H sums are 9,8,7,6. Omit L3 and L4, and shift the other nine offsets by four. For q=2 translate their rows by (8,4). For q=5 translate by (20,16). The resulting old rows, in order L5,L6,L9,L10,L12,H5,H6,H7,H8, are
```text
q=2: (13,11),(15,12),(16,10),(11,4),(17,8),(8,13),(14,6),(12,7),(9,9)
q=5: (25,23),(27,24),(28,22),(23,16),(29,20),(20,25),(26,18),(24,19),(21,21).
```
The replacement L7/L8 rows are (21,17),(20,15) at q=2 and (30,26),(41,36) at q=5. These are the corresponding upper replacement rows after lifting. [D228 S2 source](../../../research/FINITE_STATE_BINARY_MULTIPLICITY_GROWTH.md) · [D229 S2 packets](../D229_HOMOGENEOUS_PAIR_FINITE_KERNEL_SUPPLY/HAND_CONTROLS.md)

## 2. P₂ original and folded certificate, m=49

Use the n=8 packet in the proof and add F=11 to each upper tagged coordinate. The new anchor rows at L4 and L3 are (2,1) and (26,26). At h=10 convert coordinates by z=13+i and difference=10+w. The actual spine labels are (40,0,49,11) with differences (40,49,38).

| Branch | Center label | Terminal labels in original index order | Actual terminal differences in that order |
|---|---:|---|---|
| b:0:0 | 1 | (13,35) | (12,34) |
| b:1:0 | 48 | (18,20) | (30,28) |
| b:1:1 | 9 | (29) | (20) |
| b:2:0 | 2 | (17,31) | (15,29) |
| b:2:1 | 3 | (38,39) | (35,36) |
| b:2:2 | 4 | (15,37) | (11,33) |
| b:2:3 | 47 | (16,23) | (31,24) |
| b:2:4 | 46 | (14,36) | (32,10) |
| b:2:5 | 45 | (19,32) | (26,13) |
| b:2:6 | 5 | (26) | (21) |
| b:2:7 | 6 | (28) | (22) |
| b:2:8 | 7 | (34) | (27) |
| b:2:9 | 8 | (33) | (25) |
| b:2:10 | 12 | (30) | (18) |
| b:2:11 | 44 | (21) | (23) |
| b:2:12 | 43 | (27) | (16) |
| b:2:13 | 42 | (25) | (17) |
| b:2:14 | 41 | (22) | (19) |
| b:3:0 | 10 | (24) | (14) |

All table terminal labels give [13,39], and the terminal weights give [10,36]. The center and spine labels comprise [0,12]∪[40,49]. Branch attachment weights in table order in S are (1,48,9,47,46,45,2,3,4,44,43,42,41,37,5,6,7,8,39). Along with the spine these give [1,9]∪[37,49]. In T only the first and last branch attachments change: |40−1|=39 and |11−10|=1. The two actual differences exchange 1 and 39. Both entire graphs have vertex spectrum [0,49] and actual weight spectrum [1,49].

## 3. P₅ original and folded certificate, m=73

Use the retained D229 P₃ at n=12 and augment that packet once with the parameterized rule. Here its residual coordinates move by eight in each tagged block. The new return rows are (2,1) and (50,50); the augmentation's fresh upper base is F+2n+8=43. Thus, for example, L3's residual upper identity at tagged old (12,12) reaches (31,31) and the fresh upper identity at local (−1,−1) reaches (42,42). Its other residual identity rows are the translated old lower (13,13) and fresh lower (5,5). L4's residual rows are (15,14),(34,33) from the old packet and (10,9),(7,6) from the augmentation. H1's three translated rows are (22,27),(19,30),(32,17), and its two fresh rows are (49,0),(47,2). Those five sums are all 49. The full named rows below record the remaining hosts and capacities. The actual spine labels are (64,0,73,11), with differences (64,73,62).

| Branch | Center label | Terminal labels in original index order | Actual terminal differences in that order |
|---|---:|---|---|
| b:0:0 | 1 | (21,48,50,57,59) | (20,47,49,56,58) |
| b:1:0 | 72 | (32,35,45,60,62) | (40,37,27,12,10) |
| b:1:1 | 9 | (41) | (32) |
| b:2:0 | 2 | (19,24,52,53,61) | (17,22,50,51,59) |
| b:2:1 | 3 | (18,26,44,55,63) | (15,23,41,52,60) |
| b:2:2 | 4 | (15,20,23,28,47) | (11,16,19,24,43) |
| b:2:3 | 71 | (17,27,29,46,58) | (54,44,42,25,13) |
| b:2:4 | 70 | (13,22,25,49,56) | (57,48,45,21,14) |
| b:2:5 | 69 | (14,16,30,31,51) | (55,53,39,38,18) |
| b:2:6 | 5 | (38) | (33) |
| b:2:7 | 6 | (40) | (34) |
| b:2:8 | 7 | (43) | (36) |
| b:2:9 | 8 | (54) | (46) |
| b:2:10 | 12 | (42) | (30) |
| b:2:11 | 68 | (33) | (35) |
| b:2:12 | 67 | (39) | (28) |
| b:2:13 | 66 | (37) | (29) |
| b:2:14 | 65 | (34) | (31) |
| b:3:0 | 10 | (36) | (26) |

The table consumes [13,63] in terminal labels and [10,60] in terminal differences. The center and spine labels use [0,12]∪[64,73]. In S the branch attachments by table order have differences (1,72,9,71,70,69,2,3,4,68,67,66,65,61,5,6,7,8,63). The three spine differences complete [1,9]∪[61,73]. The first and last branch attachments in T instead have |64−1|=63 and |11−10|=1. All other edges give precisely their S differences. Both graphs have vertex spectrum [0,73] and weight spectrum [1,73].

For each of the two controls the complete reversed named certificate is the corresponding table with section index i replaced by 3−i on every vertex name, and spine tuples (11,49,0,40) and (11,73,0,64), respectively. Branch indices, terminal tuples and differences stay the same under this bijection. The new left attachment is the reverse of the former right, and the new right the reverse of the former left. Both actual original and folded spectra therefore hold in the reversed orientation.

## 4. Restricted adverse arithmetic

At n=4, try increasing only one pair by two using the uniform within-block +2 transport of every old residual row. The old lower input 0 is present and is distinct from the L4 anchor, and would land on the required returned input 2. This fails before choosing any fresh rows. For an increase of four, the more permissive p≥3 vacancy lemma gives lower inputs {0,1,3,6}, weights {0,2,3,5}, and both upper offsets [−1,2] in fresh base F+12. The isolated lower input 6 can only be completed as L4:(6,5). If pair 4 alone grows, neither L4 nor H4 can fill upper weight 2: L4 needs upper input 3, and H4 needs lower input −3. The restriction is the uniform internal shift and reserved returns. These controls do not decide the corresponding freely allocated returning packets or graceful originals.
