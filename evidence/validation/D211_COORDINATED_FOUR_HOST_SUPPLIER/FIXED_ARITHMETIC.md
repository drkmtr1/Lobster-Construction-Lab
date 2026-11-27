# D211 prescribed fixed hand arithmetic

The six [named originals](ORIGINALS.md) were frozen independently of these assignments. Each tuple is in actual original vertex or edge order, with terminals in increasing index within each actual parent. In each flank tuple the first entry is the fixed original index zero. All arithmetic below is manual.

## Skeleton and residual inventories

| Control | Spine L,x,y,R | Centers in physical order J,3,2,H,5 | Fixed left and right terminal labels |
|---|---|---|---|
| 1 | (0,24,4,22) | (23,3,2,20,5) | (8,19) |
| 2 | (0,26,4,24) | (25,3,2,22,5) | (10,21) |
| 3 | (0,28,4,26) | (27,3,2,24,5) | (10,23) |
| 4 | (0,30,4,28) | (29,3,2,26,5) | (11,25) |
| 5 | (0,32,4,30) | (31,3,2,28,5) | (11,27) |
| 6 | (0,30,4,28) | (29,3,2,26,5) | (10,25) |

| Control | Three spine differences | Five attachment differences | Two fixed terminal differences |
|---|---|---|---|
| 1 | (24,20,18) | (23,21,22,16,17) | (15,14) |
| 2 | (26,22,20) | (25,23,24,18,19) | (15,16) |
| 3 | (28,24,22) | (27,25,26,20,21) | (17,18) |
| 4 | (30,26,24) | (29,27,28,22,23) | (18,20) |
| 5 | (32,28,26) | (31,29,30,24,25) | (20,22) |
| 6 | (30,26,24) | (29,27,28,22,23) | (19,20) |

| Control | Exact unused labels X | Exact unused differences D |
|---|---|---|
| 1 | {1,21} ∪ ([6,18] minus {8}) | [1,13] ∪ {19} |
| 2 | {1,23} ∪ ([6,20] minus {10}) | [1,14] ∪ {17,21} |
| 3 | {1,25} ∪ ([6,22] minus {10}) | [1,16] ∪ {19,23} |
| 4 | {1,27} ∪ ([6,24] minus {11}) | ([1,19] minus {18}) ∪ {21,25} |
| 5 | {1,29} ∪ ([6,26] minus {11}) | ([1,21] minus {20}) ∪ {23,27} |
| 6 | {1,27} ∪ ([6,24] minus {10}) | [1,18] ∪ {21,25} |

Both residual sizes by row are 14,16,18,20,22,20, exactly the named terminals remaining after the one fixed terminal per flank.

## Selections and boundary checks

| Control | Provisional (q₀,a₀,b₀) | Applicable (j,k,K) | I | U | Required retained or reserved labels | Selected T |
|---|---|---|---|---|---|---|
| 1 | (8,4,2) | (—,8,—) | [9,14] | — | Retain {11,12} at host 3 | ∅ |
| 2 | (6,6,4) | (0,10,18) | [11,14] | ∅ | V=∅ | {11,14} |
| 3 | (6,6,6) | (0,10,20) | [11,16] | {13,16} | V={11,13,14,16} | V |
| 4 | (6,8,6) | (1,11,21) | [12,17] | {15,16} | V=[13,16] | V |
| 5 | (6,8,8) | (1,11,23) | [12,19] | [15,18] | V=[13,18] | V |
| 6 | (10,6,4) | (0,10,22) | [11,18] | — | Retain {14,15} at host 3 | {11,18} |

In controls 1 and 6 the retained pair splits first between 2 and H, exchanging weights (8,9) and (11,12), respectively. Their split σ-pair {7,m−6} exchanges weights 5 and 2 across the four hosts. Controls 2–5 also use {9,m−8}, exchanging 7 and 4. Controls 4 and 5 use the first complete pair at host 2, {8,23} and {8,25}, respectively. Their two exchanged weights are {6,21} and {6,23}. The midpoint goes to J for control 3 at label 16 and weight 11, and for control 5 at label 18 and weight 13. The other labels of U go to host 5, so control 3 sends label 13 and weight 8 to host 5. Control 4 sends (15,16) with weights (10,11), and control 5 sends (15,16,17) with weights (10,11,12).

## Complete original terminal certificates

| Control | Left flank J | q-center 3 | a-center 2 | b-center H | Right flank 5 |
|---|---|---|---|---|---|
| 1 | (8,18) | (9,10,13,14,15,16) | (1,6,11,21) | (12,17) | (19,7) |
| 2 | (10,18,20) | (6,12,13,15,16,17) | (1,8,19,23) | (11,14) | (21,7,9) |
| 3 | (10,16,20,22) | (6,12,15,17,18,19) | (1,8,21,25) | (11,14) | (23,7,9,13) |
| 4 | (11,8,22,23,24) | (6,12,17,18,19,20) | (1,10,21,27) | (13,14) | (25,7,9,15,16) |
| 5 | (11,8,18,24,25,26) | (6,12,19,20,21,22) | (1,10,23,29) | (13,14) | (27,7,9,15,16,17) |
| 6 | (10,24) | (6,12,13,16,17,19,20,21) | (1,8,9,14,23,27) | (11,15,18,22) | (25,7) |

Control 3 agrees with the Director's indexed certificate, including both fixed terminal positions. Absolute differences at the actual parents, in the same tuple order, are as follows.

| Control | Left flank J | q-center 3 | a-center 2 | b-center H | Right flank 5 |
|---|---|---|---|---|---|
| 1 | (15,5) | (6,7,10,11,12,13) | (1,4,9,19) | (8,3) | (14,2) |
| 2 | (15,7,5) | (3,9,10,12,13,14) | (1,6,17,21) | (11,8) | (16,2,4) |
| 3 | (17,11,7,5) | (3,9,12,14,15,16) | (1,6,19,23) | (13,10) | (18,2,4,8) |
| 4 | (18,21,7,6,5) | (3,9,14,15,16,17) | (1,8,19,25) | (13,12) | (20,2,4,10,11) |
| 5 | (20,23,13,7,6,5) | (3,9,16,17,18,19) | (1,8,21,27) | (15,14) | (22,2,4,10,11,12) |
| 6 | (19,5) | (3,9,10,13,14,16,17,18) | (1,6,7,12,21,25) | (15,11,8,4) | (20,2) |

In each row, omitting index zero at each flank leaves precisely X in the first table of terminal tuples and precisely D in the second, with multiplicity one in both. The listed original center and spine labels and the fixed terminals supply the complementary labels. The spine and attachment differences and the fixed terminal differences likewise supply the complementary weights. Thus the complete alphabets are [0,m] and [1,m] for each original. No executable verification, solver, search or checker was used.
