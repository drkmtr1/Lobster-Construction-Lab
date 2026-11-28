# D232 — Named hand certificates and adverse controls

The graph and role names are fixed in [ORIGINALS.md](ORIGINALS.md). The construction below uses reflected packet arithmetic. The terminal differences in the final tables are actual absolute endpoint subtractions. No search, task import or protected checker is involved.

## Source and ordinary transport

The retained D231 source at h=6, F=11 has these input/weight rows:

| Source role | (i,w) | Shifted role | A (n′=12) | B (n′=26) | C (n′=41) |
|---|---|---|---|---|---|
| L1 | (5,7) | L5 | (17,15) | (31,29) | (46,44) |
| L2 | (7,8) | L6 | (19,16) | (33,30) | (48,45) |
| L3 | (10,10) | L7 | omitted | omitted | omitted |
| L4 | (2,1) | L8 | omitted | omitted | omitted |
| L5 | (8,6) | L9 | (20,14) | (34,28) | (49,43) |
| L6 | (3,0) | L10 | (15,8) | (29,22) | (44,37) |
| L8 | (9,4) | L12 | (21,12) | (35,26) | (50,41) |
| H1 | (0,9) | H5 | (12,17) | (26,31) | (41,46) |
| H2 | (6,2) | H6 | (18,10) | (32,24) | (47,39) |
| H3 | (4,3) | H7 | (16,11) | (30,25) | (45,40) |
| H4 | (1,5) | H8 | (13,13) | (27,27) | (42,42) |

The source table uses every input and weight 0 through 10 once. The low offsets yield w−i=3−k and the high rows sum to 10−k. The ordinary columns add n′ to inputs and n′−4 to weights.

## Packet arithmetic

The seven exceptional rows use the proof's exact formulas with n replaced by n′ in each control. The eight one-track identities are unchanged. The lower and reflected upper coordinates are interpreted with their own tags.

- **A.** The sparse width is 12. The forced LU crossings are at 8,10,11. The only double positions, 0,6,9, are identities on both tracks. This yields A=8+2·3+1=15 and B=3. There are no added chains.
- **B.** Start at n=20, A=B=17. Use the eight reserved coordinates 8 through 15, leaving the doubles 0,6,17 for crossings. The next table gives all enlarged chains. The extra doubles become 0,6,23; the forced LU coordinates become 22,24,25. At L3 there are eight single identities, eight retained high-chain closure identities, and one return. At H3 there are six rows from the unused doubles, eight retained low-chain closure crossings, and three forced LU rows.
- **C.** Start at n=20, A=19 and B=15. Allocate double 0 to identities and doubles 6,17 to crossings beyond the reserved banks. After growth the unused doubles are 0,6,38 and the forced LU coordinates are 37,39,40. L3 has the eight single identities, two unused double identities, eight high-chain closure identities and one return. H3 has four unused double crossings, eight low-chain closure crossings and three forced rows.

| Host | B signed progressions | C signed progressions |
|---|---|---|
| L1 | (8,10), (9) | (8,10), (9) |
| H1 | (11,13), (12) | (11,13), (12,14) |
| L2 | (14,15) | (15,16,17,18) |
| H2 | (16,17) | (19,20,21,22,23) |
| L4 | (19,18) | (29,28,27,26,25,24) |
| H4 | (21,20) | (36,35,34,33,32,31,30) |

These consume their entire intervals on all four tagged inventories. Each move along a progression yields two rows at its named host. For example the C L4 chain contributes LL differences of index −1 and UU differences of reflected index +1, with retained LU H3 at 24 and UL H3 at 29. The C H4 chain has LU displacement +1 and UL displacement −1, with retained LL L3 at 36 and UU L3 at 30. Singleton chains have only their two closures. The B and C growth totals are 6 and 21 positions, so n′=26 and 41.

For A, B, C respectively the reflected upper coordinates become 31−y, 59−y, 89−y. The inherited L7 replacements before unreflection are UU (8,12), (22,26), (37,41), giving normalized (23,19), (37,33), (52,48). Each L8 replacement is LL (7,2). Return L4 is (2,1) in all three cases. The L3 maximum returns are (34,34), (62,62), (92,92). With the ordinary transport these are complete allocations at F′=35,63,93.

## Complete named labels and actual terminal edge differences

The following table completely labels both T and S for each control. In each terminal tuple, the r-th label is the label of l:i:k:r, starting at r=0. The weights following the slash are in that same order, obtained by subtracting the center label from a low-host terminal or subtracting a high-host terminal from its center. A low center Lk has label k and a high center Hk has label m−k. This interprets every named center even when the terminal tuple has more than one entry. The normalized rows underlying the table use z=13+i and actual difference 10+w.

| Named center | Role | A labels / weights | B labels / weights | C labels / weights |
|---|---|---|---|---|
| b:0:0 | L1 | 14 / 13 | 14,21,62 / 13,20,61 | 14,21,92 / 13,20,91 |
| b:1:0 | H1 | 39 / 17 | 26,61,67 / 58,23,17 | 26,27,90,91,97 / 88,87,24,23,17 |
| b:1:1 | L9 | 33 / 24 | 47 / 38 | 62 / 53 |
| b:2:0 | L2 | 16 / 14 | 16,27,57 / 14,25,55 | 16,28,29,30,84,85,86 / 14,26,27,28,82,83,84 |
| b:2:1 | L3 | 13,18,19,22,35,37,38,40,41,42,43,44,45,46,47 / 10,15,16,19,32,34,35,37,38,39,40,41,42,43,44 | 18,24,25,29,34,52,55,59,60,65,68,69,70,71,73,74,75 / 15,21,22,26,31,49,52,56,57,62,65,66,67,68,70,71,72 | 13,18,24,25,32,49,72,79,88,89,95,98,99,100,101,102,103,104,105 / 10,15,21,22,29,46,69,76,85,86,92,95,96,97,98,99,100,101,102 |
| b:2:2 | L4 | 15 / 11 | 15,32,54 / 11,28,50 | 15,38,39,40,41,42,74,75,76,77,78 / 11,34,35,36,37,38,70,71,72,73,74 |
| b:2:3 | H2 | 27 / 28 | 30,41,56 / 53,42,27 | 33,34,35,36,56,80,81,82,83 / 80,79,78,77,57,33,32,31,30 |
| b:2:4 | H3 | 21,23,24 / 33,31,30 | 13,19,22,23,28,31,35,36,37,38,49,53,58,63,64,66,72 / 69,63,60,59,54,51,47,46,45,44,33,29,24,19,18,16,10 | 19,22,23,31,37,50,51,52,53,64,73,87,93,94,96 / 93,90,89,81,75,62,61,60,59,48,39,25,19,18,16 |
| b:2:5 | H4 | 17 / 36 | 17,33,51 / 64,48,30 | 17,43,44,45,46,47,48,66,67,68,69,70,71 / 94,68,67,66,65,64,63,45,44,43,42,41,40 |
| b:2:6 | L5 | 30 / 25 | 44 / 39 | 59 / 54 |
| b:2:7 | L6 | 32 / 26 | 46 / 40 | 61 / 55 |
| b:2:8 | L7 | 36 / 29 | 50 / 43 | 65 / 58 |
| b:2:9 | L8 | 20 / 12 | 20 / 12 | 20 / 12 |
| b:2:10 | L12 | 34 / 22 | 48 / 36 | 63 / 51 |
| b:2:11 | H5 | 25 / 27 | 39 / 41 | 54 / 56 |
| b:2:12 | H6 | 31 / 20 | 45 / 34 | 60 / 49 |
| b:2:13 | H7 | 29 / 21 | 43 / 35 | 58 / 50 |
| b:2:14 | H8 | 26 / 23 | 40 / 37 | 55 / 52 |
| b:3:0 | L10 | 28 / 18 | 42 / 32 | 57 / 47 |

Example endpoint checks include C H3's extreme listed terminals 19 and 96 at center 112, giving 93 and 16, and C L2's terminal 86 at center 2, giving 84. The exact terminal label sets in A, B and C are [13,47], [13,75], [13,105]. The exact terminal difference sets from these edge subtractions are [10,44], [10,72], [10,102], respectively.

## Complete named skeletons, restoration and reversal

In spine order the labels are (48,0,57,11), (76,0,85,11), (106,0,115,11). The skeleton labels in each case are [0,12] and [m−9,m]. The three spine edge weights in their physical order are (m−9,m,m−11), by subtracting the adjacent labels. The folded branch-edge weights by section, with the original branch indices, are

| Section | Every weight in branch index order |
|---|---|
| 0 | 1 |
| 1 | m−1, 9 |
| 2 | m−2,m−3,m−4,2,3,4,m−5,m−6,m−7,m−8,m−12,5,6,7,8 |
| 3 | m−10 |

Here the section 0 edge is from the 0 root and section 3 from the m root, with their named centers fixed. The other section 1 weights are absolute differences at root 0 and the section 2 weights at root m. The folded skeleton weights are exactly [1,9] and [m−12,m]. Together with the terminal table, this gives the whole spectrum 1 through m in each named fold, one occurrence each.

In the original, s:0--b:0:0 instead has weight (m−9)−1=m−10 and s:3--b:3:0 has weight 11−10=1. The named exchange is 1 with 47,75,105 respectively. All other endpoints and differences above apply unchanged in the originals. Terminal indices are retained, and the reverse certificate takes each label to the vertex with section 3−i and identical branch and terminal index. In physical spine order the reverse labels are (11,57,0,48), (11,85,0,76), (11,115,0,106). The reverse graphs have each listed edge with reversed section indices, the same spectra, and the two exterior differences swapped by the conjugate restoration. These formulas specify both reverse certificates for every name, using the two distinct edge sets.

## Adverse arithmetic

- **Insufficient crossing capacity.** At A=99, B=3, a1=3 and the five other off-reservoir quotas unit, n=54 and there are no crossing doubles. The required L1 progression would need two crossing doubles. The spare identity capacity cannot be substituted in the stated low-host chain, whose two closures are H3 rows.
- **Insufficient identity capacity.** At A=9, B=99, b1=3 and the other off-reservoir quotas unit, n=57 and no identity double exists. The H1 chain would need two. Both cases show a failed sufficient admission test without classifying packet feasibility.
- **Unsuitable placement.** Swap the two whole right pairs 2 and 3 of C. The designated reservoirs now carry A=7, B=9, which cannot start the sparse construction. The original placement on these same actual physical branches supplies the exact original. Numerical role placement matters.
- **Exact ordered packet exclusion.** For the separately fixed 57-edge adverse target in [ORIGINALS.md](ORIGINALS.md) set A=17 and B=1. At n=12, the four high rows all travel LU. Reflected displacement sums require all L1, L2, L7 and L8 residual rows to be UU. Then the lower available weight 2 has no incoming row: LL could only be identity at L3, and its input 2 is absent. The proof establishes this for every odd A≥7 with all seven other quotas unit at those ordered roles, including arbitrary allocation of their rows.
