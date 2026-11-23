# Fixed (5,3) return obstruction on original `[[4],[2]]`

[Evidence and reproduction](../evidence/validation/LCL_R241_42_PORT53_RETURN_001/README.md) · [D090 composition](R241_2B2_3B3_JOINT.md) · [D078 supplier](R241_PAIRED_BRANCHED_SPINE.md) · [Adopted R241.1](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** The exact named original `[[4],[2]]` cannot supply A(10,6;5,3) with physical entrance s:0 and exit s:1 in the alpha orientation with s:0 low.

## Original graph and pins

The only spine edge is s:0–s:1. The only center attachments are s:0–b:0:0 and s:1–b:1:0. The center b:0:0 has the four original terminals l:0:0:j for 0≤j<4. The center b:1:0 has the two original terminals l:1:0:j for 0≤j<2. Each terminal has only its named center as neighbor. The two spine names, two center names and six indexed leaves are distinct and give ten vertices and nine edges. Every center and terminal is at distance one and two, respectively, from the original spine, which is a witness. Each center and leaf attaches once, so the original is a tree.

With s:0 low, the connected tree forces low vertices s:0, b:1:0 and the four first-section terminals. The four highs are s:1, b:0:0 and the two second-section terminals. Each listed edge has one endpoint in each class. A candidate normalized state bijectively uses [0,5] on the lows and [6,9] on the highs. Its physical labels are s:0=5 and s:1=6+3=9.

## Extremal-weight contradiction

Each pair below is (higher label, lower label). With alphabet [0,9], a weight w can only arise at (w+i,i) for 0≤i≤9−w. In these four levels all pairs cross the cut numerically. Whether they exist as edges depends on the original incidences.

| Required weight | All numerical pairs | Original-incidence consequence |
| --- | --- | --- |
| 9 | (9,0) | The sole vertex of label 9 is s:1. Its only neighbors are s:0=5 and b:1:0. Hence z=f(b:1:0)=0. |
| 8 | (8,0), (9,1) | Label 9 has neighbors 5 and 0. A right terminal must carry 8, because the neighbors of zero are s:1 and the two right terminals. |
| 7 | (7,0), (8,1), (9,2) | The right terminal labeled 8 is adjacent only to zero. Label 9 has no neighbor labeled 2. The other right terminal must carry 7. |
| 6 | (6,0), (7,1), (8,2), (9,3) | Zero has all its neighbors labeled 9, 8 and 7. The terminals carrying 7 and 8 are adjacent only to zero. The vertex carrying 9 is adjacent only to 5 and 0. Every listed pair is unavailable. |

This accounts for all ten numerical pairs and both possible assignments of 8 and 7 to the two named right terminals. Both terminal orders have the same forced incidences. No weight-six edge can exist, contrary to the required complete spectrum.

## Separate signed-degree contradiction

This argument uses the shared maximum-edge deduction z=0 and does not use the forcing of weights eight and seven. In an alpha labeling each edge contributes its high endpoint label minus its low endpoint label. Summing once per actual incidence, each vertex label is therefore weighted by its degree and signed by class. The degree-one high sum minus low sum is (6+7+8+9)−(0+1+2+3+4+5)=15. The actual spine vertices have degree two each, so their degree excess contributes 9−5=4. With A=f(b:0:0), the first center has degree five and adds 4A, while the second center has degree three and subtracts 2z. Every terminal has degree one. Hence gracefulness would require
```text
45 = 1+2+...+9 = 19+4A−2z
2A−z = 13.
```
At z=0 the left side of the second identity is even. Thus there is no integer A. In particular the candidate packet's inference A=6 from this equation is incorrect. The exact rational value would be 13/2, outside the label alphabet.

The separate incidence argument for the top three weights also establishes the packet's proposed repeated-weight diagnostic, with a corrected dependency. Given the forced right terminal palette {7,8}, the remaining high label 6 belongs to the first center by the alpha classes. The first terminal palette is then {1,2,3,4}. Its differences are {5,4,3,2}, the first attachment contributes 1 and the original spine contributes 4. The right attachment and terminals contribute {9,8,7}. Thus the sorted difference multiset is [1,2,3,4,4,5,7,8,9], with a repeated 4, missing 6 and sum 43. This derives the diagnostic from the actual incidence constraints with no prescribed terminal order. It also explains why the forced center label can occur in that diagnostic while violating the independent required edge sum.

## Scope

**ACCEPT** the structural obstruction and **REJECT — EXCLUDED** the simultaneously prescribed state on this original, cut and orientation. The [D078 independent M(a,b) supplier](R241_PAIRED_BRANCHED_SPINE.md#independently-supplied-modules) includes this exact two-section graph at offsets (1,1). Those ports do not take D090's exit offset five or return its entrance three. The [D090 theorem](R241_2B2_3B3_JOINT.md) and the independent D087 and D089 suppliers retain their stated domains. This exclusion concerns a single proposed return interface. Further compatible supply and repeatability remain open.
