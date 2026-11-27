# D210 fixed hand arithmetic

The [original identities](ORIGINALS.md) were fixed before evaluating these assignments. Each spine and center tuple is in original order, and each terminal tuple is in increasing original terminal index at its actual center. The partial tree includes both flank terminals and the other nine skeleton vertices. Center attachment differences follow the original center order.

## Partial tree and exact residuals

| Control | Spine labels | Center labels | Left and right flank terminal labels |
|---|---|---|---|
| A | (0,22,4,20) | (21,3,2,18,5) | (8,17) |
| B | (0,23,4,21) | (22,3,2,19,5) | (8,18) |
| C | (0,25,4,23) | (24,3,2,21,5) | (10,20) |
| D | (0,28,4,26) | (27,3,2,24,5) | (11,23) |
| E | (0,22,4,20) | (21,3,2,18,5) | (8,17) |

| Control | Three spine differences | Five attachment differences | Two flank terminal differences |
|---|---|---|---|
| A | (22,18,16) | (21,19,20,14,15) | (13,12) |
| B | (23,19,17) | (22,20,21,15,16) | (14,13) |
| C | (25,21,19) | (24,22,23,17,18) | (14,15) |
| D | (28,24,22) | (27,25,26,20,21) | (16,18) |
| E | (22,18,16) | (21,19,20,14,15) | (13,12) |

Taking exact complements of the eleven assigned labels and ten listed differences gives the following residuals. The rows have respectively 12,13,15,18,12 entries in each residual.

| Control | Unused labels | Unused differences |
|---|---|---|
| A | {1,19} ∪ ([6,16] minus {8}) | [1,11] ∪ {17} |
| B | {1,20} ∪ ([6,17] minus {8}) | [1,12] ∪ {18} |
| C | {1,22} ∪ ([6,19] minus {10}) | [1,13] ∪ {16,20} |
| D | {1,25} ∪ ([6,22] minus {11}) | ([1,17] minus {16}) ∪ {19,23} |
| E | {1,19} ∪ ([6,16] minus {8}) | [1,11] ∪ {17} |

## Base evaluation and transfer

| Control | Branch parameters | Base S₂ | Base S₃ | Base S_H | Eligible I | Selected S |
|---|---|---|---|---|---|---|
| A | a=4 | {1,6,7,19} | [9,14] | {15,16} | [9,12] | ∅ |
| B | a=4 | {1,6,7,20} | [9,15] | {16,17} | [9,13] | {9,13} |
| C | j=0, K=17 | {1,7,8,9,18,22} | {6} ∪ [11,16] | {17,19} | [11,13] | {12} |
| D | j=1, K=19 | {1,7,8,9,10,19,21,25} | {6} ∪ [12,18] | {20,22} | [12,15] | {12,15} |
| E | a=4 | {1,6,7,19} | [9,14] | {15,16} | [9,12] | No invariant singleton |

B uses the pair 9↔13 under ρ(z)=22−z, retaining differences {6,10}. C uses the midpoint 12 under ρ(z)=24−z, retaining difference 9. D uses the pair 12↔15 under ρ(z)=27−z, retaining differences {9,12}. A needs no transfer.

## Complete named certificates for A–D

Combine each row with its own partial tree above. The three tuples below go to `l:1:0:e`, `l:1:1:e`, and `l:2:0:e` respectively, in increasing e at each of the three indexed parents.

| Control | q-terminal labels | a-terminal labels | b-terminal labels |
|---|---|---|---|
| A | (9,10,11,12,13,14) | (1,6,7,19) | (15,16) |
| B | (10,11,12,14,15) | (1,6,7,20) | (9,13,16,17) |
| C | (6,11,13,14,15,16) | (1,7,8,9,18,22) | (12,17,19) |
| D | (6,13,14,16,17,18) | (1,7,8,9,10,19,21,25) | (12,15,20,22) |

Direct subtraction against the actual parent labels gives the matching difference tuples.

| Control | q-terminal differences | a-terminal differences | b-terminal differences |
|---|---|---|---|
| A | (6,7,8,9,10,11) | (1,4,5,17) | (3,2) |
| B | (7,8,9,11,12) | (1,4,5,18) | (10,6,3,2) |
| C | (3,8,10,11,12,13) | (1,5,6,7,16,20) | (9,4,2) |
| D | (3,10,11,13,14,15) | (1,5,6,7,8,17,19,23) | (12,9,4,2) |

Within each row the label tuples are disjoint and exhaust its unused labels. The difference tuples are disjoint and exhaust its unused differences. The two complements then give complete label and difference alphabets [0,m] and [1,m] with every prescribed actual quota.

## E is an adverse transfer control only

This original has q=5, a=4, b=3 and m=22. The base weight inventory agrees with A, but one label must move from host 3 to H=18. On all of S₃=[9,14], the weight change from moving a single label z exchanges z−3 for 18−z. Equality would need 2z=21. On I=[9,12] the only orbits are {9,12} and {10,11}, and there is no fixed point. Thus the one-label transfer cannot preserve the difference inventory. The earlier D209 adjacent-top formula already supplies the ordinary original at these quotas since a+1=b+2. This check makes no additional assignment to E.

All five controls were evaluated by hand. No executable check, search, solver or checker was used.
