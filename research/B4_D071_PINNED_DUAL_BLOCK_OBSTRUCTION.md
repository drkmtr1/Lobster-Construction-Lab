# Structural obstruction to the pinned 2222 dual-block interface

## Exact state and incidence counts

Let P be the exact [D066 named original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json), `[[2],[2],[2],[2],[]]`, with graph digest `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`. For i=0,1,2,3 there is the actual spine edge s:i–s:(i+1), the attachment s:i–b:i:0, and both terminal edges b:i:0–l:i:0:j for j=0,1. These are all 16 original edges. The witness W=b:0:0–s:0–s:1–s:2–s:3–s:4 uses those incidences, and every vertex is within distance two. The second host b:1:0 and zero host b:2:0 are one edge from W. The names and terminal indices remain distinct.

Consider any normalized alpha-graceful labeling whose low class is [0,7] and high class [8,16], with actual first host and low port A=b:0:0 labeled 5, Z=b:2:0 labeled 0 and high exit U=s:4 labeled 9. Write B for the label of actual second host b:1:0. Alternating from high s:4 gives the following complete degree groups.

| Side | Degree 3 | Degree 2 | Degree 1 |
|---|---|---|---|
| Low | b:0:0, b:2:0, s:1, s:3 | ∅ | l:1:0:0, l:1:0:1, l:3:0:0, l:3:0:1 |
| High | s:2, b:1:0, b:3:0 | s:0 | s:4, l:0:0:0, l:0:0:1, l:2:0:0, l:2:0:1 |

Assume both complete predicates of the [upper-block](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis) and [lower-block](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md#supplied-state-and-hypotheses) rules hold on this same labeling. Let E_U(u) contain all edges from highs at least u, and E_L(d) all edges from lows below d. The upper cut u is 10 through 16 by the fixed exit. The lower cut d is 6 through 8 by the low port and class size. On each cut every selected edge has exactly one selected endpoint, because the selected vertices lie in one alpha class and the opposite endpoint lies strictly on the other side of the numerical cut. Thus each actual edge is counted once.

The lower selection contains exactly d lows, including A and Z of degree three. Of the other d−2, only s:1 and s:3 can have degree greater than one. If k_d of these two qualify, the count is d+4+2k_d. Since the required tail [B−d+1,16] has 16−B+d weights, equality implies B=12−2k_d. This leaves B=8,10,12. At d=8 both spine lows are selected, so B=8. At d=7 at least one spine low is selected because there are only six nonspine lows.

For the upper cut, 17−u selected highs must contribute 22−u edges to match [u−5,16]. Thus their degree excess over one per vertex is five. The positive excesses are one at s:0 and two at each of s:2, b:1:0, b:3:0. The sole way to sum to five is selecting s:0 and exactly two of those three degree-three highs. In particular at least three highs are selected, so u≤14.

## The two selected edge sets are nested

Each original difference occurs once. The edges of either selected set are therefore exactly the inverse image of its complete weight interval under the same injective difference map. If u−5≥B−d+1 then E_U(u) is contained in E_L(d). If u−5≤B−d+1 then E_L(d) is contained in E_U(u), and equality gives identical edge sets. Each containment constrains the actual opposite endpoints of the included edges.

## Contradictions for all remaining host labels

**B=10.** Here k_d=1, so d is 6 or 7. The lower start is 5 or 4, while u−5≥5. Hence every upper-selected edge is also lower-selected. The selected s:0 forces its actual neighbor s:1 to lie below d. At least one of s:2 and b:3:0 is selected, since two degree-three highs are selected and only b:1:0 lies outside that pair. Both s:2 and b:3:0 touch physical s:3, forcing it below d as well. This gives k_d=2, a contradiction. The same inclusions hold when the starts coincide.

**B=12.** Now k_d=0 and d=6. The six lower-selected vertices are A, Z and the four second and fourth terminals. The neighbors of A and Z give s:0, s:2 and all four high terminals. The remaining selected lows also meet b:1:0 and b:3:0. Thus their selected edges meet all eight highs other than s:4. For u≤12 the lower tail [7,16] lies inside the upper tail, including equality at u=12. This would force all eight of those highs to be selected at u, which allows at most seven. For u≥13 the upper tail lies inside the lower tail. But the upper-selected s:0 has edge s:0–s:1, and s:1 is unselected at d=6. Both regimes contradict the required inclusion.

**B=8.** The second host and exit are excluded at every upper cut. The selected degree pattern forces s:0, s:2 and b:3:0 to be upper-selected. Any other unselected high is therefore a first or third terminal with label in [10,u−1]. By gracefulness and the complete upper tail, the unselected edges have weights exactly [1,u−6]. For u≥13 at least three terminals are unselected besides the two pinned high labels, but only two can be first terminals. At least one is a third terminal at Z=0 and contributes a weight at least ten. This exceeds u−6, since u≤14.

For u=10,11,12 an unselected third terminal would also exceed u−6. So the terminals with labels from 10 to u−1 are all first terminals at A=5, contributing exactly [5,u−6], empty at u=10. The remaining unselected edges are the three edges at b:1:0 and the unique edge s:4–s:3. These must use exactly [1,4]. The second host labeled 8 cannot give difference 3 because low label 5 is at A, which is not one of its neighbors (s:1 and the two second terminals). Therefore the exit edge gives difference 3, forcing s:3=6. The second host then cannot give difference 2 because s:3 is also not its neighbor. The exit edge has already used difference 3. This leaves difference 2 without a source.

## Disposition and evidence basis

**ACCEPT — PINNED DUAL-BLOCK STRUCTURAL OBSTRUCTION.** The three cases exhaust the host labels permitted by lower counting. Hence no normalized alpha-graceful labeling of the exact named 2222 original with these three pins supplies both complete block premises. This addresses joint supply for these pins and cuts. Other pins, other transitions and ordinary gracefulness remain open to their own results. D070's first/third-host theorem, D071's distinct negative on the D070 family, and D062 retain their scope. Even a seed supplying both predicates elsewhere would require a separate compatibility and joint-inventory proof.

The [audit](../evidence/validation/B4_D071_PINNED_DUAL_BLOCK_OBSTRUCTION_001/README.md) checks the original incidence groups, both archived co-original ledgers, the six D071 receipts and the arithmetic for the proof cases. Its numerical table is limited to (u,d,B). The universal result follows from the structural argument.
