# D103 — Zero-entrance obstruction on ordered [[4,3],[2]]

Use the exact named [D099 original](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json), digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. The physical spine is `s:0--s:1`. The centers `b:0:0`, `b:0:1`, `b:1:0` attach to `s:0`, `s:0`, `s:1` respectively, with four, three and two indexed terminals. Each terminal is adjacent only to its center. These 14 vertices and 13 edges give the original tree with all centers one step from the spine and all terminals two steps away.

Seek a graceful alpha labeling with low alphabet [0,8], high alphabet [9,13], `s:0=0` and `s:1` free. Traversing the original from the low entrance makes the right center and seven left terminals low. The exit, both left centers and both right terminals are high. Let A, B, z denote the three center labels in the order above and Y the exit label. Then A, B and Y are distinct high labels and z∈[1,8]. Only the pair (13,0) can give weight 13. The three actual neighbors of the entrance carry A, B and Y, hence 13∈{A,B,Y}.

## Signed degree and exhaustive reduction

Every edge contributes its high endpoint label minus its low endpoint label. Counting each label once contributes 55−36=19. The original degrees at the entrance, exit and three centers are 3, 2, 5, 4 and 3, respectively. Each terminal has degree one. The excess over degree one therefore contributes Y+4A+3B−2z, with zero contribution from the pinned entrance. Since the required total is 1+…+13=91, we get

```text
2z = 4A + 3B + Y − 72, with 2z ∈ {2,4,6,8,10,12,14,16}.
```

There are 3·4·3=36 distinct ordered high triples containing 13, because its position is unique and the other two slots take distinct values in [9,12]. The following disjoint reductions cover every triple.

- **A=13.** Then 2z=3B+Y−20≥3·9+10−20=17. If B≥10, even Y=9 gives at least 19. Neither bound permits z≤8.
- **B=13.** Then 2z=4A+Y−33. For A=9, possible Y are 10, 11 and 12, giving 13, 14 and 15. Only Y=11 survives, with z=7. For A=10, possible Y are 9, 11 and 12, giving 16, 18 and 19. Only Y=9 survives, with z=8. For A≥11, the lower bound is 20.
- **Y=13.** Then 2z=4A+3B−59, so B is odd. For B=9, the values A=10,11,12 give 8,12,16 and survive. For B=11, the values A=9,10,12 give 10,14,22, of which the first two survive. B ranges over [9,12] in this order case.

## Seven contradictions on named incidences

Let H be the increasing pair of high labels outside {A,B,Y}. Those labels occupy the two right terminals in some order. The spine and three attachments contribute Y, A, B and Y−z, then the two right-terminal edges contribute H[0]−z and H[1]−z, listed by label. These six incidences are distinct. The remaining seven edges are exactly the four first-left terminal edges and the three second-left terminal edges. Their low endpoints take the palette L=[1,8]∖{z}, with no assumption about its division or internal order.

For a missing weight w, a left terminal at the first center would have to carry A−w, and one at the second center would have to carry B−w. The table gives both necessary values and the reason neither is available in L. Each listed missing weight is absent from the six fixed weights in its row. The repeat witnesses refer to two fixed named incidences, independent of terminal order.

| A | B | Y | z | H | Six fixed weights | Contradiction |
| ---: | ---: | ---: | ---: | --- | --- | --- |
| 9 | 11 | 13 | 5 | 10,12 | 13,9,11,8,5,7 | Weight 12 requires −3 or −1. Both are below 1. |
| 9 | 13 | 11 | 7 | 10,12 | 11,9,13,4,3,5 | Weight 2 requires 7 or 11. Label 7 is z, and 11 is outside the low alphabet. |
| 10 | 9 | 13 | 4 | 11,12 | 13,10,9,9,7,8 | Weight 9 occurs on `s:0--b:0:1` and `s:1--b:1:0`. |
| 10 | 11 | 13 | 7 | 9,12 | 13,10,11,6,2,5 | Weight 12 requires −2 or −1. Both are below 1. |
| 10 | 13 | 9 | 8 | 11,12 | 9,10,13,1,3,4 | Weight 2 requires 8 or 11. Label 8 is z, and 11 is outside the low alphabet. |
| 11 | 9 | 13 | 6 | 10,12 | 13,11,9,7,4,6 | Weight 12 requires −1 or −3. Both are below 1. |
| 12 | 9 | 13 | 8 | 10,11 | 13,12,9,5,2,3 | Weight 1 requires 11 or 8. Label 11 is outside the low alphabet, and 8 is z. |

The fixed repeat multiplicities are empty in six rows and {9:2} in the repeated row. Missing weights and repeated weights each contradict the required spectrum. The seven rows exhaust the necessary constraints and exclude the requested cut-9 zero-entrance state with the exit free. Other zero positions, other cuts and ordinary gracefulness are outside this proof. [Evidence](../evidence/validation/LCL_R241_43_2_ZERO_ENTRANCE_001/README.md).
