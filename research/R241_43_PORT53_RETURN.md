# Fixed (5,3) return obstruction on original `[[4],[3]]`

[Evidence and reproduction](../evidence/validation/LCL_R241_43_PORT53_RETURN_001/README.md) · [D091 fixed return](R241_42_PORT53_RETURN.md) · [D090 composition](R241_2B2_3B3_JOINT.md) · [D078 supplier](R241_PAIRED_BRANCHED_SPINE.md#independently-supplied-modules) · [Adopted R241.1](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** The exact named original `[[4],[3]]` cannot supply A(11,6;5,3) with physical entrance s:0 and exit s:1 in the alpha orientation with s:0 low.

## Original topology and prescribed alpha orientation

The spine s:0–s:1 has exactly one center attached at each end, b:0:0 at s:0 and b:1:0 at s:1. The first center has exactly the four original terminal names l:0:0:j for 0≤j<4. The second has exactly the three original terminal names l:1:0:j for 0≤j<3. Each terminal is adjacent only to its own center. All names and incidences are distinct. Thus two spine vertices, two centers and seven terminals give eleven vertices, and one spine edge, two attachments and seven terminal edges give ten edges. The attachments add one edge per new vertex and thus form a tree. The original spine witnesses every center at distance one and every terminal at distance two.

Every original edge must cross the alpha cut. With s:0 low, connectedness and the alternating incidences force s:0, b:1:0 and the four first-section terminals to be the six lows. The five highs are s:1, b:0:0 and the three right terminals. Hence the low and high alphabets are exactly [0,5] and [6,10]. The prescribed physical offsets give f(s:0)=5 and f(s:1)=6+3=9.

## Necessary signed sum and all numerical center cases

Write A=f(b:0:0) and z=f(b:1:0). In an alpha labeling each actual edge contributes its high endpoint label minus its low endpoint label. Summing over edges counts each vertex label with its signed degree. The degree-one high sum is 40 and the low sum is 15. Both spine degrees are two. The respective center degrees are five and four because each center has one spine attachment and its own terminal edges. Every leaf has degree one. The signed corrections above degree one are therefore −5 at s:0, +9 at s:1, +4A at the first center and −3z at the second center. Gracefulness requires
```text
55 = 1+2+...+10 = 40−15−5+9+4A−3z = 29+4A−3z
4A−3z = 26.
```

The pinned high label 9 leaves A in {6,7,8,10}, and the pinned low label 5 leaves z in {0,1,2,3,4}. The four possible values of A give all necessary numerical center cases.

| A | 4A−26 | Required z=(4A−26)/3 | In the low alphabet with pin 5 reserved? |
| --- | --- | --- | --- |
| 6 | −2 | −2/3 | No |
| 7 | 2 | 2/3 | No |
| 8 | 6 | 2 | Yes |
| 10 | 14 | 14/3 | No |

Thus A=8 and z=2. This condition uses the sum of all required weights and no ordering assumption on terminal labels.

## Original-edge contradictions

The remaining high palette is {6,7,10}. All three labels must occur at the three distinct right-terminal names, in some order. The right terminal of label six has only the center of label two as neighbor, giving difference four. The spine edge between labels five and nine independently gives difference four. The two edges are distinct actual incidences for every terminal ordering. A weight cannot appear twice in the required bijection.

For the separate maximum-weight check, the remaining low palette is {0,1,3,4} on the four first-section terminals. In [0,10] only labels 0 and 10 can realize difference ten. They lie at a first-section terminal and a right terminal, respectively. Both are leaves adjacent only to their own centers, so there is no edge between them. The required weight ten is absent. The two incidence contradictions share only the previously forced center labels and physical pins; neither requires the other.

The full forced palettes also determine each edge group's weights without assigning any terminal order. Spine, left attachment and right attachment give 4, 3 and 7. The first terminal weights are {8,7,5,4}, and the right terminal weights are {4,5,8}. Their sorted multiset is [3,4,4,4,5,5,7,7,8,8]. It sums to 55, demonstrating why the signed sum alone would leave the center pair, while 4 occurs three times and 10 is among the missing weights.

## Scope and relation to the compatible return

**ACCEPT** the structural proof and **REJECT — EXCLUDED** the specified (5,3) state on this original and alpha cut. D078's M(4,3) independently supplies the same original with offsets (1,1), physical s:0=1 and s:1=7. This is a different interface. The D090 four-section construction retains its accepted (3,5) state for every integer a,b≥2. A module with entrance five and exit three would satisfy the numerical R241 matches, with actual connectors and inventories still to be proved for any composed original. This result excludes only this candidate module. D091's distinct maximum-exit obstruction on `[[4],[2]]` and its corrected algebra retain their own scope.
