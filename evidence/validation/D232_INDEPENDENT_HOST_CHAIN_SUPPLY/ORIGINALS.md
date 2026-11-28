# D232 — Independently fixed named original and fold definitions

Every control uses h=10, even side ℓ=2, odd side j=15, left pairs 1 and 9, and right pairs 2 through 8 plus the three unpaired slots. The original T has spine s:0--s:1--s:2--s:3, each indexed branch center b:i:k adjacent to its actual s:i, and terminals l:i:k:r for 0≤r<quota adjacent only to b:i:k. The fold S replaces just s:0--b:0:0 by s:1--b:0:0 and s:3--b:3:0 by s:2--b:3:0. The names and incidences are fixed without reference to labels. Physically reverse by taking section i to 3−i, keeping every within-section and terminal index unchanged.

The numerical roles, written in order for the named branch indices of each section, are
```text
s:0   L1
s:1   H1 L9
s:2   L2 L3 L4 H2 H3 H4 L5 L6 L7 L8 L12 H5 H6 H7 H8
s:3   L10
```
The common source is the retained h=6, F=11 returning S2 unit allocation from D231. In every control m=33+sum of the eight new quotas. Only the new roles have their prescribed non-unit quotas; the eleven inherited roles have one terminal each, including the L7 and L8 replacements.

| Control | Low quotas | High quotas | Exact profile by section | Edges |
|---|---|---|---|---:|
| A | (1,1,15,1) | (1,1,3,1) | [[1],[1,1],[1,15,1,1,3,1,1,1,1,1,1,1,1,1,1],[1]] | 57 |
| B | (3,3,17,3) | (3,3,17,3) | [[3],[3,1],[3,17,3,3,17,3,1,1,1,1,1,1,1,1,1],[1]] | 85 |
| C | (3,7,19,11) | (5,9,15,13) | [[3],[5,1],[7,19,11,9,15,13,1,1,1,1,1,1,1,1,1],[1]] | 115 |

For B and C the banks are in the order L1 at [8,9], H1 at [10,11], L2 at {12}, H2 at {13}, L4 at {14}, H4 at {15}. B inserts one coordinate at each bank. C inserts respectively one through six coordinates. This is an independently specified deterministic choice, with the remaining double coordinates allocated by the proof. Control A inserts none.

For the focused adverse with low (1,1,17,1) and high (1,1,1,1), keep the exact same graph naming rule and B/C role order. Its profile is [[1],[1,1],[1,17,1,1,1,1,1,1,1,1,1,1,1,1,1],[1]]. It has 57 edges. Its exclusion proved here concerns the fixed ordered numerical returning S2 interface, and its original graph is specified independently of that exclusion.
