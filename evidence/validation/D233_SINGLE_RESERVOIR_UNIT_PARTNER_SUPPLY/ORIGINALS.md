# D233 — Frozen named originals, folds and reversals

All controls and prospective packet placements use the retained D233-independent D232 canonical role map, with h=10, even side ℓ=2, odd side j=15, pair indices 1 and 9 on the even side and indices 2 through 8 on the odd side. The immutable old source is h=6, F_old=11, at S2. The equations, packet rows and labels are not used to define these graphs.

| Physical section | Ordered numerical roles at actual branch indices |
|---|---|
| 0 | L1 |
| 1 | H1,L9 |
| 2 | L2,L3,L4,H2,H3,H4,L5,L6,L7,L8,L12,H5,H6,H7,H8 |
| 3 | L10 |

For ordered new low demands `(a1,a2,A,a4)` and high demands `(b1,b2,B,b4)`, the graph profile is `[[a1],[b1,1],[a2,A,a4,b2,B,b4,1,1,1,1,1,1,1,1,1],[1]]`. Section i contains the center b:i:k at every displayed branch index k, with precisely the stated quota of indexed vertices l:i:k:r starting at r=0. The original edges are exactly the three edges s:i--s:(i+1), the center incidences s:i--b:i:k, and the terminal incidences b:i:k--l:i:k:r. The fold deletes just s:0--b:0:0 and s:3--b:3:0 and inserts s:1--b:0:0 and s:2--b:3:0. The reversed graph transports any vertex name by replacing its section i by 3−i and keeps both branch and terminal indices. Apply this name bijection to both edge sets separately.

| Control | L1,L2,L3,L4 | H1,H2,H3,H4 | Edges |
|---|---|---|---:|
| A | 1,1,1,1 | 1,1,17,1 | 57 |
| B | 3,5,1,7 | 1,1,17,1 | 69 |
| C | 3,3,9,3 | 3,3,17,3 | 77 |
| H1, quota five | 1,1,1,1 | 5,1,1,1 | 45 |
| H1, quota seven | 1,1,1,1 | 7,1,1,1 | 47 |
| L3 boundary, quota five | 1,1,5,1 | 1,1,1,1 | 45 |
| L4 counterexample, quota five | 1,1,1,5 | 1,1,1,1 | 45 |
| Adverse single three at H1 | 1,1,1,1 | 3,1,1,1 | 43 |
| Matched adverse ordered low-3 | 1,1,17,1 | 1,1,1,1 | 57 |

For B use consecutive low banks L1 at 4,5, L2 at 6, L4 at 7. Insert respectively 1,2,3 coordinates after these banks. For C use L1 at 4,5, H1 at 6,7, L2 at 8, H2 at 9, L4 at 10, H4 at 11 and insert one coordinate per bank. Remaining doubles are allocated by the proof. The named 57-edge A has its dominant center on the right. The earlier D232 adverse at L3 gives the same quota multiset and a different indexed branch assignment. The two small positive controls have their dominant center at b:1:0 on the left.

Any future finite diagnostic uses exactly the named definition above applied to the ordered numerical placement, independently of a witness. These are lift controls for the packet model. A numerical aggregate is a multiset of four pairs of shape (1,q), while the frozen names distinguish physical placements even when profiles agree after reordering.
