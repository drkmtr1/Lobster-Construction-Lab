# Structural obstruction on the original `[[2,2],[3]]` at physical offsets (1,0)

[Authorized scope](../tasks/LCL_Codex_D083_223_Strict_Return_2026-11-22.md) · [Verified intake](../evidence/validation/LCL_R241_223_STRICT_RETURN_001/INTAKE.md) · [Evidence](../evidence/validation/LCL_R241_223_STRICT_RETURN_001/README.md)

## Named original and cut

The 12 vertices have 11 actual edges. They are the spine s:0–s:1, attachments from s:0 to b:0:0 and b:0:1 and from s:1 to b:1:0, two terminal edges at each of b:0:0 and b:0:1, and three terminal edges at b:1:0. Every terminal has just its own center as neighbor. The original spine witnesses each center at distance one and each terminal at distance two.

The alpha orientation with s:0 low forces b:1:0 and all four first-section terminals to be low. The six high names are s:1, b:0:0, b:0:1 and the three second-section terminals. Thus cut 6 uses exactly low labels 0 through 5 and high labels 6 through 11. Prescribed offsets (1,0) give s:0=1 and s:1=6. Put A=f(b:0:0), B=f(b:0:1) and z=f(b:1:0).

## Signed degree sum and necessary cases

All actual edges have one high and one low endpoint. Summing their high-minus-low differences amounts to the degree-weighted high sum minus the degree-weighted low sum. Counting degree one at every vertex first gives high alphabet sum 51 and low alphabet sum 15. The remaining contributions come from these five named vertices.

| Physical vertex | Degree | Signed correction above degree one |
| --- | ---: | ---: |
| s:1 | 2 | +6 |
| b:0:0 | 3 | +2A |
| b:0:1 | 3 | +2B |
| s:0 | 3 | −2 |
| b:1:0 | 4 | −3z |

The seven terminal degrees are one. These degrees total 22, twice the 11 actual edges. Consequently the sum is `(51+6+2A+2B)−(15+2+3z)=40+2(A+B)−3z`. Gracefulness requires the sum of 1 through 11, namely 66. The equation is therefore `2(A+B)−3z=26`.

The high pin leaves A and B distinct in {7,8,9,10,11}. The low pin gives z∈{0,2,3,4,5}, and parity makes z even. At z=0, A+B would have to be 13, below the minimum 7+8=15. At z=2, the required sum is 16, with pair {7,9}. At z=4, the sum is 19, with pairs {8,11} and {9,10}. These unordered numerical pairs are evidence about feasible values of the two named centers. Both assignments of each pair to the two actual centers remain included.

## Extremal edge contradiction

Difference 11 requires the adjacent pair of labels 0 and 11. Label 11 cannot be at s:1 because of its pin. If it were at a second-section terminal, its sole neighbor would be b:1:0, whose label is 2 or 4. Thus 11 must occur at one of the first-section centers. Its spine neighbor has label 1, so to realize weight 11 a terminal of that very center would have to be 0.

Only {A,B}={8,11} at z=4 includes 11. This leaves exactly {7,9,10} for the three named second-section terminals. Whichever of them receives 9, its edge to b:1:0=4 has weight 5. The original spine s:0–s:1 already has weight 5. These are distinct original edges. The argument is unchanged if the first-section center labels are reversed or if the indexed terminals take their available labels in another order.

This contradiction proves the exact prescribed state impossible. It concerns those normalized physical pins and orientation. No other-ports or ordinary-gracefulness claim follows.

## Consequence for the task

The proof eliminates the full pinned domain without visiting complete named assignments. The bounded run records the original, rechecks the retained D081 positive at (1,0), binds the D082 negative without replay, and exercises three adverse gates on retained inputs. Its independent arithmetic audit reconstructs all original incidences, verifies the degree coefficients, recovers the three necessary numerical cases and checks the extremal and repeated weights.

The proposed J(a) construction needs this exact B state before using R241 with D080 H(a). That prerequisite fails, so the proposed route ends here. No J(a), repeat join or suffix from this seed is constructed. The retained theorem joins separately supplied alpha states when the old physical exit offset equals the new physical entrance offset. That conditional rule and D080's witnessed H(a) supplier still apply on their established domains. [Pinned R241](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [D080 bridge](R241_ZERO_TO_ONE_BRIDGE.md)
