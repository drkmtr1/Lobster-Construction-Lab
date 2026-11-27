# D225 — Named hand controls

## Original definitions

Each profile below defines its own original (T) before the label tables are evaluated. For each, the vertices are the four names `s:0` through `s:3`, the indexed names `b:i:j` in the declared section lists, and the terminal names `l:i:j:k` with (0≤k<Q_{ij}). The edges are the three consecutive spine edges, every `s:i--b:i:j`, and every `b:i:j--l:i:j:k`. Its source (S) uses the same names and replaces only `s:0--b:0:0` and `s:3--b:3:0` by `s:1--b:0:0` and `s:2--b:3:0`.

- A, unit, has profile `[[1],[1,1],[1,1,1,1,1,1,1],[1]]`, 25 edges and 26 vertices.
- A, enlarged, has profile `[[1],[3,5],[1,1,1,1,1,7,1],[1]]`, 37 edges and 38 vertices.
- B, unit, has profile `[[1],[1,1,1,1,1,1],[1,1,1],[1]]`, 25 edges and 26 vertices.
- B, enlarged, has profile `[[1],[3,1,1,1,1,1],[7,1,5],[1]]`, 37 edges and 38 vertices.

All four have (h=6). The source and original of each have the same vertex count. Tables list literal labels and absolute differences in terminal-index order, retaining index zero through each lift and appending the newly allocated indices.

## A. Two selected left branches, anchored rightmost index

The unit spine is (20,0,25,7), with edge differences (20,25,18). The low terminal prefix rows at hosts 4 and 6 have ((i,w)=(1,0),(4,1)). The sole high suffix row is ((6,2)) at offset 2. At cut (5,3), the two shared recipients are low 5 and high offset 3. Their old rows are ((8,6)) and ((2,5)). Use (G=8), with fresh relative input pair ({0,7}) at low 5 and the other three pairs at high offset 3. This gives quotas 3 and 7. Then use (t=2) for high offset 1. Its four fresh inputs are (0,1,20,21), with weights (21,20,1,0). The old low-3 identity lands at (22,22). The enlarged spine is (32,0,37,7), with differences (32,37,30).

| Branch | Unit center | Unit terminals | Unit terminal differences | Enlarged center | Enlarged terminals | Enlarged terminal differences |
|---|---:|---|---|---:|---|---|
| b:0:0 | 1 | 14 | 13 | 1 | 24 | 23 |
| b:1:0 | 5 | 17 | 12 | 5 | 27,16,23 | 22,11,18 |
| b:1:1 | 24 | 9 | 15 | 36 | 11,9,10,29,30 | 25,27,26,7,6 |
| b:2:0 | 2 | 16 | 14 | 2 | 26 | 24 |
| b:2:1 | 3 | 19 | 16 | 3 | 31 | 28 |
| b:2:2 | 4 | 10 | 6 | 4 | 12 | 8 |
| b:2:3 | 8 | 18 | 10 | 8 | 28 | 20 |
| b:2:4 | 21 | 12 | 9 | 33 | 14 | 19 |
| b:2:5 | 22 | 11 | 11 | 34 | 13,17,18,19,20,21,22 | 21,17,16,15,14,13,12 |
| b:2:6 | 23 | 15 | 8 | 35 | 25 | 10 |
| b:3:0 | 6 | 13 | 7 | 6 | 15 | 9 |

The 11 unit terminal labels are exactly ([9,19]) and their actual differences exactly ([6,16]). The source attachment weights in table order are (1,5,24,23,22,21,17,4,3,2,19). With the spine weights they give ([1,5]∪[17,25]). The two original attachments have weights (|20−1|=19) and (|7−6|=1). The 23 enlarged terminal labels are ([9,31]) and the differences ([6,28]). The enlarged source attachment weights are (1,5,36,35,34,33,29,4,3,2,31), which together with the spine give ([1,5]∪[29,37]). Restoration gives (|32−1|=31) and (|7−6|=1). In each case the displayed spine and centers fill exactly the complement of the terminal labels in the full vertex alphabet.

## B. The j=3 boundary at h=6, symmetric outer lift

Use the same marks as A, with two fewer right complementary pairs. Left pairs are 1, 2, 4 and 5. The right pair is 3 and the unpaired low slots are 6, 7 and 8. In the unit source, assign the following normalized rows to the marked and actual named roles. In both tables high labels are shown as their actual current value.

| Branch | Unit center | Unit (i,w) | Enlarged center | Enlarged terminals | Enlarged terminal differences |
|---|---:|---|---:|---|---|
| b:0:0 | 1 | (8,10) | 1 | 26 | 25 |
| b:1:0 | 5 | (7,5) | 5 | 25,17,22 | 20,12,17 |
| b:1:1 | 2 | (6,7) | 2 | 24 | 22 |
| b:1:2 | 4 | (10,9) | 4 | 28 | 24 |
| b:1:3 | 21 | (3,3) | 33 | 15 | 18 |
| b:1:4 | 23 | (2,6) | 35 | 14 | 21 |
| b:1:5 | 24 | (1,8) | 36 | 13 | 23 |
| b:2:0 | 3 | (0,0) | 3 | 12,9,10,11,29,30,31 | 9,6,7,8,26,27,28 |
| b:2:1 | 8 | (9,4) | 8 | 27 | 19 |
| b:2:2 | 22 | (5,2) | 34 | 23,18,19,20,21 | 11,16,15,14,13 |
| b:3:0 | 6 | (4,1) | 6 | 16 | 10 |

In the unit case (z=i+9) and (d=w+6). The listed rows use each index and weight (0,…,10) once, and substitution gives every absolute difference (d). At cut (5,3) use (G=6), with pair ({0,5}) at low 5 and the other two pairs at high 22 before updating its label. This gives quotas 3 and 5. The resulting (F=17), and the symmetric shift (t=3) fills fresh inputs and weights ([0,2]∪[20,22]) at low 3, giving quota 7. The unit spine and exchange are those of A. Its source attachment weights are (1,5,2,4,21,23,24,3,17,22,19). The enlarged spine and exchange are those of A at 37 edges. The enlarged source attachment weights are (1,5,2,4,33,35,36,34,29,3,31). The terminal labels and differences in the two cases are respectively ([9,19]), ([6,16]) and ([9,31]), ([6,28]). The explicit attachments together with the spine weights fill their complements, so both source and original have the complete edge alphabet. In each case the terminal labels, spine and centers fill the complete vertex alphabet.

## Boundaries and recurrence check

- For the anchored recurrence from (h=6) to (h=10), the carried inputs are [4,13] except 5 with weights ([1,9]). The fresh high rows in increasing offsets (1,2,3,4) have ((i,w)=(3,14),(0,16),(5,10),(2,12)). The fresh low rows at (1,2,7,8) have ((i,w)=(15,17),(14,15),(17,13),(16,11)). They obey the actual affine rules at (F=19) and fill the four small inputs (0,2,3,5) and the four large inputs (14,15,16,17), with weights (10,…,17). The restored bottom and top rows are (1,0) and (18,18). The carried low 10 row is (8,1); the carried high offset 6 row is (10,2). The cut is (9,3).
- At j=3 and h≠6, the direct D224 placement needs two distinct right pairs (3,h−3) while the right has capacity one. At ℓ=2 it also cannot put pair 3 on the left in addition to the two compulsory pairs. Control A uses a distinct lift at an already available high recipient and never needs pair 3 on the left.
- For positive anchored width, leaving the old top identity at its uniform translation would make the highest fresh index (F+2t−1) unusable at high offset 1, because its would-be weight is (-1). The anchor move removes exactly that endpoint from the residual set. Widths zero in either lift produce empty inserted intervals and unchanged old rows.
- Reversing the spine maps the name (s:i) to (s:3−i) and maps centers and terminals by the same section reversal with their branch and terminal indices unchanged. The 3,5,7 controls therefore retain each weight at its corresponding reversed edge and can put the chosen quotas on either physical orientation.
