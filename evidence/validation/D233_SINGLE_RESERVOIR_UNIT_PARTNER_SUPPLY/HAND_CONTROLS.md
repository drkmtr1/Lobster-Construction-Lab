# D233 — Indexed deterministic hand certificates

Use the actual graph definitions and roles in [ORIGINALS.md](ORIGINALS.md). Each column lists exact rows for a named original, its fold and both physical reversals. No scientific program or protected checker was called.

## Reflected choices and hand lift

The retained old S2 unit rows in numerical order are L1:(5,7), L2:(7,8), L3:(10,10), L4:(2,1), L5:(8,6), L6:(3,0), L8:(9,4), H1:(0,9), H2:(6,2), H3:(4,3), H4:(1,5). Their two inventories are 0 through 10. Shift offsets by four, omit L3 and L4, and add (n′,n′−4) to each carried row. The new anchors are L4:(2,1) and L3:(F′−1,F′−1), F′=11+2n′. For a reflected upper coordinate y undo reflection as F′−4−y. Lower coordinates are already actual normalized values.

- A starts at n=12, D={0,4,5,6,7,9}, all six doubles crossing. Forced crossings at 1,3,8,10,11 bring H3 to 17. No chains. F′=35.
- B starts at the same n and D, and inserts 1,2,3 positions. The three banks become L1:[4,6] with progression (4,6) and singleton 5, L2:(7,8,9), L4:(13,12,11,10). The unused crossing doubles are 0,15 and the forced singles become 1,3,14,16,17. This preserves H3=17, with retained closures at all four progressions. The one L3 row is its anchor. Final n′=18 and F′=47.
- C starts at n=16, D={0,13}∪[4,11]. Assign the high-host banks four identity doubles, the low-host banks four crossing doubles and the two extra coordinates 0,13 crossing. The new progressions are L1:(4,6),(5); H1:(7,9),(8); L2:(10,11); H2:(12,13); L4:(15,14); H4:(17,16). The unused crossing doubles move to 0,19; the forced singles to 1,3,18,20,21. The eight closing identity rows and anchor yield A=9. Four crossing doubles are retained via closures, two via the unused coordinates and five singles remain, so B=17. Final n′=22 and F′=55. This uses all eight safe starting coordinates. The stated uniform bound's minimum sum is 26; (9,17) and n=16 give a saturated safe interval for these six bank requests.

In A, B and C the L7 and L8 reflected rows are respectively (−2,2) and (n′−4,n′+1), both UU. Undoing gives the respective normalized pairs (33,29),(23,18); (45,41),(29,24); and (53,49),(33,28). Insert the exact anchors. These checks account for the omissions and returns independently of the final spectrum.

### Small dominant H1 controls

| Width | UU rows in L1,L2,L7,L8 order | UL H1 | LU H1 | LU H2, H3, H4 |
|---:|---|---|---|---|
| 6 | (2,0),(−1,−2),(3,7),(0,5) | (−2,0),(1,3) | (4,2),(5,3),(8,6) | (0,−1),(1,1),(3,4) |
| 7 | (3,1),(−1,−2),(4,8),(1,6) | (−2,0),(0,2),(2,4) | (1,−1),(4,2),(5,3),(9,7) | (6,5),(0,0),(3,4) |

At n=6 LU exhausts lower inputs {0,1,3,4,5,8}, UL fills lower weights {0,3}, and the UU and UL inputs together fill [−2,3]. UU weights {−2,0,5,7} and LU weights {−1,1,2,3,4,6} partition [−2,7]. At n=7 LU exhausts {0,1,3,4,5,6,9}, UL fills {0,2,4}, and the UU and UL inputs partition [−2,4]. UU weights {−2,1,6,8} and LU weights {−1,0,2,3,4,5,7} partition [−2,8]. The displayed displacements are respectively −2,−1,4,5 for the UU rows, +2 for UL H1, −2 for LU H1, and −1,0,1 for the remaining LU rows. H1 uses exactly five or seven rows. The L7/L8 normalized pairs are (16,12),(19,14) and (17,13),(20,15); the top L3 returns are (22,22) and (24,24). Lower L4 returns to (2,1).

## Full terminal labels and endpoint differences

Below each entry is **i-list / w-list** in original terminal index order, starting at r=0 within each branch. Thus it explicitly gives the actual vertex label `13+i` and the actual incident edge difference `10+w` for every named terminal. A low center's label is its offset k and its absolute difference is 13+i−k; a high center's label is m−k and its absolute difference is m−k−13−i. The w lists are the resulting endpoint subtractions minus ten. For example in C at H3 the terminal index with i=0 has actual labels 13 and 74, giving 61; its listed w is 51. In B at L4 with i=33 the endpoint difference is 46−4=42.

| Named center and role | A | B | C | H1=5 | H1=7 |
|---|---|---|---|---|---|
| b:0:0 L1 | 30 / 32 | 4,37,42 / 6,39,44 | 4,45,50 / 6,47,52 | 17 / 19 | 18 / 20 |
| b:1:0 H1 | 14 / 19 | 20 / 25 | 9,24,44 / 44,29,9 | 4,5,8,18,21 / 17,16,13,3,0 | 1,4,5,9,19,21,23 / 22,19,18,14,4,2,0 |
| b:1:1 L9 | 20 / 14 | 26 / 20 | 30 / 24 | 14 / 8 | 15 / 9 |
| b:2:0 L2 | 32 / 33 | 7,8,34,35,44 / 8,9,35,36,45 | 10,40,52 / 11,41,53 | 20 / 21 | 22 / 23 |
| b:2:1 L3 | 34 / 34 | 46 / 46 | 7,8,12,17,35,38,42,43,54 / 7,8,12,17,35,38,42,43,54 | 22 / 22 | 24 / 24 |
| b:2:2 L4 | 2 / 1 | 2,11,12,13,31,32,33 / 1,10,11,12,30,31,32 | 2,15,37 / 1,14,36 | 2 / 1 | 2 / 1 |
| b:2:3 H2 | 29 / 3 | 41 / 3 | 13,39,49 / 39,13,3 | 0 / 20 | 6 / 16 |
| b:2:4 H3 | 0,1,3,4,5,6,7,8,9,10,11,22,24,25,26,27,31 / 31,30,28,27,26,25,24,23,22,21,20,9,7,6,5,4,0 | 0,1,3,5,6,9,10,14,15,16,17,28,30,36,38,39,43 / 43,42,40,38,37,34,33,29,28,27,26,15,13,7,5,4,0 | 0,1,3,5,6,11,14,18,19,20,21,32,36,41,46,47,51 / 51,50,48,46,45,40,37,33,32,31,30,19,15,10,5,4,0 | 1 / 18 | 0 / 21 |
| b:2:5 H4 | 28 / 2 | 40 / 2 | 16,34,48 / 34,16,2 | 3 / 15 | 3 / 17 |
| b:2:6 L5 | 17 / 15 | 23 / 21 | 27 / 25 | 11 / 9 | 12 / 10 |
| b:2:7 L6 | 19 / 16 | 25 / 22 | 29 / 26 | 13 / 10 | 14 / 11 |
| b:2:8 L7 | 33 / 29 | 45 / 41 | 53 / 49 | 16 / 12 | 17 / 13 |
| b:2:9 L8 | 23 / 18 | 29 / 24 | 33 / 28 | 19 / 14 | 20 / 15 |
| b:2:10 L12 | 21 / 12 | 27 / 18 | 31 / 22 | 15 / 6 | 16 / 7 |
| b:2:11 H5 | 12 / 17 | 18 / 23 | 22 / 27 | 6 / 11 | 7 / 12 |
| b:2:12 H6 | 18 / 10 | 24 / 16 | 28 / 20 | 12 / 4 | 13 / 5 |
| b:2:13 H7 | 16 / 11 | 22 / 17 | 26 / 21 | 10 / 5 | 11 / 6 |
| b:2:14 H8 | 13 / 13 | 19 / 19 | 23 / 23 | 7 / 7 | 8 / 8 |
| b:3:0 L10 | 15 / 8 | 21 / 14 | 25 / 18 | 9 / 2 | 10 / 3 |

For the two additional low-side boundary witnesses, use the n=6 H1=5 column as a table template. Keep precisely the carried L5,L6,L9,L10,L12,H5,H6,H7,H8 rows. Replace the other cells by the following lists. These use the low-3 and low-4 constructions in the manuscript, the latter with c=1.

| Role | Dominant L3=5 | Dominant L4=5 |
|---|---|---|
| L1 | 16 / 18 | 18 / 20 |
| L2 | 18 / 19 | 17 / 18 |
| L3 | 0,3,20,21,22 / 0,3,20,21,22 | 22 / 22 |
| L4 | 2 / 1 | 1,2,4,16,20 / 0,1,3,15,19 |
| L7 | 19 / 15 | 21 / 17 |
| L8 | 17 / 12 | 19 / 14 |
| H1 | 8 / 13 | 0 / 21 |
| H2 | 4 / 16 | 8 / 12 |
| H3 | 5 / 14 | 3 / 16 |
| H4 | 1 / 17 | 5 / 13 |

The i and w columns each partition [0,F′−1] for F′=35,47,55,23,25,23,23 respectively. The number of entries at every named center agrees with its independently fixed quota. The terminal labels are therefore [13,m−10] and terminal differences [10,m−13] in each case.

## Complete skeleton, restoration and reversal

Spine labels (s:0,s:1,s:2,s:3) are (m−9,0,m,11). In A, B, C, the positive H1 controls and both new low controls these are respectively (48,0,57,11), (60,0,69,11), (68,0,77,11), (36,0,45,11), (38,0,47,11) and (36,0,45,11) twice. Include all center labels using their roles, as above. The skeleton labels form [0,12]∪[m−9,m] exactly, and the three spine weights in order are (m−9,m,m−11).

The folded attachment at b:0:0 has weight 1 from root 0; the folded attachments at b:1:0 and b:1:1 have weights m−1 and 9 from that root. At the sequence of actual names b:2:0 through b:2:14, all from root m, the weights in order are
`(m−2,m−3,m−4,2,3,4,m−5,m−6,m−7,m−8,m−12,5,6,7,8)`.
At b:3:0 its fold attachment from root m weighs m−10. These actual edge subtractions and the three spine weights form [1,9]∪[m−12,m]. Together with the terminal table this proves each complete folded spectrum. The actual original's renamed attachments at s:0 and s:3 use labels m−9 and 11, giving m−10 and 1, respectively. Their exact exchange is 1↔47, 1↔59, 1↔67, 1↔35, 1↔37, 1↔35 and 1↔35. The remaining edges are the very same indexed endpoint pairs. Transport the displayed labels by section i→3−i to give every label of both reversed graphs. Their reversed spine tuple is (11,m,0,m−9), and the incidence bijection preserves each checked difference and conjugates the marked exchange.

To check the earlier exact dominant-17 original, use the A table with every label of b:2:4 and its terminals transported to b:2:1 and vice versa. Those two branch groups have the same physical parent. The named folded parent there is still s:2, and the exterior exchange is still 1↔47. The branch index exchange gives the literal earlier D232 target, its fold and both reversals.

## Adverse calculations

The single quota three has width 5 for every numerical placement. The returning L4 output 1 is occupied by the carried ordinary row from old weight 0. The pre-anchor lower weight set is only {0,2}. This is an architecture exclusion despite the separate D229 binary whole-original supply. At width 12 the earlier ordered dominant L3=17 exclusion holds via the corrected full moment, and the preceding H3=17 positive supplies its named physical graph. The proposed lower-only displacement calculation would also reject the explicit L3=5 and L4=5 controls; the four LU input terms explain that false implication.
