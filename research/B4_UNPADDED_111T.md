# B4-UNPADDED-111T-001

For all integers `t>=2` and `K>=1`, the original zero-padding profile
`[[1],[1],[1],[t]]+[[]]*(K+1)` has an explicit graceful labeling. Booleans
are excluded from the constructor domain. The K=1 labeling is alpha.
The K>=2 completion is claimed graceful, and its unshifted prefix seed is alpha.

## Target and two supplied prefixes

The spine is `s:0--...--s:(K+4)` with K+5 vertices. Each `b:i:0`
attaches to `s:i`, and its original `l:i:0:j` attaches to that center.
There are four centers and t+3 leaves, so the order is t+K+12 and the
edge count is m=t+K+11. Include all branches and `s:0` through `s:4`
in the prefix. The unassigned names are exactly `s:5` through `s:(K+4)`.
Their incident edges are exactly the K consecutive edges of the original
path starting at `s:4`, and only `s:4--s:5` crosses the prefix boundary.

| Original vertex | K>=2 | K=1 |
|---|---:|---:|
| s:0 | K+t+10 | t+12 |
| s:1 | 1 | 2 |
| s:2 | K+t+7 | t+9 |
| s:3 | 4 | 5 |
| s:4 | K+t+6 | t+7 |
| b:0:0 | 2 | 0 |
| l:0:0:0 | K+t+9 | t+11 |
| b:1:0 | K+t+11 | t+10 |
| l:1:0:0 | 0 | 1 |
| b:2:0 | 3 | 3 |
| l:2:0:0 | K+t+8 | t+8 |
| b:3:0 | K+t+5 | t+6 |
| l:3:0:j, 0<=j<t | 5+j | 6+j |

For K>=2, set a=t+5. The labels 0 through 4 are on `l:1:0:0`,
`s:1`, `b:0:0`, `b:2:0`, `s:3` in that order. The fourth leaves
extend this block through aâˆ’1. The seven other prefix vertices in
increasing label order are `b:3:0`, `s:4`, `s:2`, `l:2:0:0`,
`l:0:0:0`, `s:0`, `b:1:0`. They use [a+K,m]. The blocks are disjoint
and contain t+12 labels for the t+12 assigned vertices.

For K=1, labels 0 through 3 are on `b:0:0`, `l:1:0:0`, `s:1`,
`b:2:0`. Label 5 is on `s:3` and the fourth leaves give [6,t+5].
The seven high vertices in increasing label order are `b:3:0`, `s:4`,
`l:2:0:0`, `s:2`, `b:1:0`, `l:0:0:0`, `s:0`, using [t+6,t+12].
Only label 4 is missing. Assign it to `s:5` for the full bijection.
Every edge crosses the cut at t+6: the spine alternates high, low, high,
low, high, low; centers alternate low, high, low, high; each leaf is
opposite its center. Hence the full alpha low-class size is t+6.

## Original-edge differences and completion

For K>=2 the fourth terminal edges have weights K+tâˆ’j, so use [K+1,K+t].
For K=1 those weights are tâˆ’j, giving [1,t]. For every remaining original
prefix edge and the sole final edge at K=1, subtract the lower entry of
the displayed formula from the higher:

| Edge | K>=2 | K=1 |
|---|---:|---:|
| s:3--b:3:0 | K+t+1 | t+1 |
| s:3--s:4 | K+t+2 | t+2 |
| s:4--s:5 | unfinished | t+3 |
| s:2--s:3 | K+t+3 | t+4 |
| s:2--b:2:0 | K+t+4 | t+6 |
| b:2:0--l:2:0:0 | K+t+5 | t+5 |
| s:1--s:2 | K+t+6 | t+7 |
| b:0:0--l:0:0:0 | K+t+7 | t+11 |
| s:0--b:0:0 | K+t+8 | t+12 |
| s:0--s:1 | K+t+9 | t+10 |
| s:1--b:1:0 | K+t+10 | t+8 |
| b:1:0--l:1:0:0 | K+t+11 | t+9 |

Each edge occurs once. For K=1 the prefix misses exactly D={t+3} and
R={4}. The actual port `s:4=t+7` joins `s:5=4` with difference
t+7âˆ’4=t+3. One assignment consumes both singleton resources and leaves
the prefix intact.

For K>=2 the prefix uses exactly [K+1,m] in differences, leaving
D=[1,K], R=[a,a+Kâˆ’1], and physical `s:4=a+K+1`. Apply the retained
[nonadjacent consumer](B2_NONADJACENT_CONSUMER.md) on the original path.
Its normalized Câ‚‚=(3,1,0), Câ‚ƒ=(4,1,0,2), Câ‚„=(5,1,2,0,3) each start at
K+1, exhaust [0,Kâˆ’1] once after the port and have differences 1..K.
For K>=5 reflect C_(Kâˆ’3) through x â†¦ Kâˆ’2âˆ’x. Its original start
becomes 0, and its remaining entries cover [2,Kâˆ’2]. Prepend K+1,1,Kâˆ’1
to the entire reflection, including 0. The three new edges have weights
K,Kâˆ’2,Kâˆ’1; the reflection's edges still use 1..Kâˆ’3, including its first
edge from 0. The new entries 1,Kâˆ’1 and the reflected entries exhaust
[0,Kâˆ’1] without repetition. Repeated reduction by three reaches a base.
Translate the normalized entries by a and assign entry i only to
`s:(4+i)` for 1<=i<=K. Entry zero equals the actual port label. Exactly
K assignments consume both inventories and preserve the prefix. For
example at K=2 the high-parity suffix vertex `s:6` receives a, below
the low-parity vertex `s:5` at a+1. The completed labeling need not
remain alpha.

## Derivation on the original cut

Cut the existing edge `s:2--s:3`, using left component B and right
component A. The retained [R241 excerpt and disposition](../references/upstream/mdl/N241_relational_ports.md)
identify MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md`, operative lines 4364â€“4405 and
adoption at 4488â€“4505. The retained [L008 archive](../references/upstream/bounded/research__LEMMAS.md.archive.md)
records `research/LEMMAS.md` at MDL_Bounded_Search commit
`e48b94eec4091b4fe189e325cab2eda464409943`, line 21. Both operative
arguments were read at the pinned commits. R241 joins actual `L_A--U_B`
when `x_A=y_B`. It adds p_B to all A labels, adds n_A to the B high
labels and leaves B low labels fixed. The resulting actual ports are
`L_B,U_A`.

| Left B local vertices | K>=2 seed | K=1 |
|---|---|---|
| s:0,s:1,s:2 | 7,1,4 | 8,2,5 |
| b:0:0,l:0:0:0 | 2,6 | 0,7 |
| b:1:0,l:1:0:0 | 8,0 | 6,1 |
| b:2:0,l:2:0:0 | 3,5 | 3,4 |

In each column the nine labels are 0..8 once, and the actual edges
cross the cut p_B=4. The spine weights in both are 6 and 3. The three
attachment/terminal pairs are (5,4),(7,8),(1,2) in the first column and
(8,7),(4,5),(2,1) in the second. Both spectra are 1..8.
The actual witness is `b:0:0--s:0--s:1--s:2`; all other vertices lie
within two steps of it. Its endpoints `L_B=b:0:0`, `U_B=s:2`
have labels (2,4) and offsets (2,0) in the first column, and labels
(0,5) and offsets (0,1) in the second. The zero-labeled leaf in the
first column is a different physical vertex. Its path to `s:2` leaves
`l:0:0:0` at distance three.

For K>=2, the right A is L008 at branch size t and zero padding:
`s:3=0`, fourth leaves `1+j`, `b:3:0=t+1`, `s:4=t+2`. The
low labels are 0..t, their neighbors are high, and the terminal,
attachment and spine edges use [1,t], t+1 and t+2 respectively.
Here n_A=t+3, p_A=t+1 and the witnessing edge `s:3--s:4` gives
actual ports and offsets (0,1). All vertices are within two steps
of this edge. R241 applies at equality 0 and restores precisely
`s:2--s:3`. The right labels gain 4 and the left highs gain t+3.
The connector gives t+3; the left spectrum becomes [t+4,t+11].
The result has low size a and actual returned ports `b:0:0=2`,
`s:4=t+6` with offsets (2,1). This supplies the displayed
arithmetic seed with the K terms removed. Its seven high labels
become the displayed prefix upon adding K. Each original edge goes
from low to high, so every difference increases by K.

For K=1, translate the same L008 component by one and include the
original `s:5=0` adjacent to `s:4`, whose original L008 label was
maximum. The resulting labels on `s:3`, fourth leaves, `b:3:0`,
`s:4` are 1, `2+j`, t+2, t+3. The old differences 1..t+2 are
unchanged, and the last edge supplies t+3. Now n_A=t+4, p_A=t+2,
actual ports `s:3,s:4` have offsets (1,1), and `s:5` is at distance
one from their witnessing edge. R241 applies at equality 1. A gains
4, B's highs gain t+4, the actual connector gives t+4, and B supplies
[t+5,t+12]. The actual returned ports are `b:0:0=0`, `s:4=t+7`
with offsets (0,1). This gives exactly the full formula above,
including `s:5=4`. In both derivations the original cut alone is
restored and the two witnessing paths concatenate.

## Scope and source comparison

This is a project corollary of retained R241 and L008 using the
directly verified left components. The extension in the K=1
component uses the physical maximum-labeled vertex supplied by
L008. The K=1 prefix uses a singleton difference t+3. The K>=2
prefix uses the nonadjacent interval consumer. The retained
[B4 unit construction](B4_UNPADDED_UNIT.md) handles t=1 through its
above-side adjacent contract and retains its full-alpha conclusion.
Together the two constructors prove ordinary gracefulness of
the exact profile for all positive t,K. The B2 and B3 constructors
retain their respective original targets and physical ports.
All three B4 contracts retain their own definitions.

Other branch sizes in the first three sections, padding, multiple
positive branches, further sections and arbitrary repetition remain
separate obligations. This is symbolic project mathematics with
bounded corroboration and separate AI review. It makes no claim of
historical novelty, human peer review or proof-assistant verification.
