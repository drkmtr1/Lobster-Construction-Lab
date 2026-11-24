# D101 maximum-label obstruction at the second left center

[Evidence](../evidence/validation/LCL_R241_42_2_MAXIMUM_HOST_001/README.md) · [Frozen D098 original and certificate](../evidence/validation/LCL_R241_NAMED_CENTER_ROLE_TRANSPORT_001/README.md) · [D099 target and insertion obstruction](R241_43_2_LOWER_BLOCK.md) · [D100 fixed-exit result](R241_43_2_FIXED_EXIT3.md)

**ACCEPT** the structural obstruction. **REJECT** the specified cut-8 alpha state on exact ordered `[[4,2],[2]]` with `b:0:1=12` and both physical spine labels free.

## Actual incidences and scalar reduction

The frozen ordered original has the spine edge s:0–s:1. The two left centers b:0:0 and b:0:1 attach to s:0 and each has its own four or two indexed leaves, respectively. The right center b:1:0 attaches to s:1 and has two indexed leaves. Every terminal is incident only to its designated center. Thus there are 13 vertices and 12 edges, and every vertex is within distance two of the actual spine. In the orientation with s:0 low, the low names are s:0, b:1:0 and the six left terminals. The high names are s:1, both left centers and the two right terminals.

Let x and Y be the labels of s:0 and s:1, A and B the left-center labels in original order, and z the right-center label. Here B=12. Orient every difference from the high endpoint to the low endpoint. Its total over all original edges is the signed degree sum. The baseline with degree one gives 50−28=22 from the alphabets [8,12] and [0,7]. The actual degrees of s:0, s:1, b:0:0, b:0:1 and b:1:0 are 3,2,5,3,3. All leaves have degree one. Using the required sum 78 gives
`78=22+4A+2B+Y−2x−2z`, hence `4A+Y−2(x+z)=32`.
Thus Y is even and, since 12 is already used, it is 8 or 10. We have x+z=2A+Y/2−16.

These are the complete high-low pairs for the three extreme weights.

| Weight | Possible (high,low) pairs |
| ---: | --- |
| 12 | (12,0) |
| 11 | (12,1), (11,0) |
| 10 | (12,2), (11,1), (10,0) |

If x>2, label 0 must be a leaf at b:0:1, since difference 12 requires adjacency to that center. Its unique neighbor has 12, so weight 11 forces 1 onto the other leaf of b:0:1. Both leaves now have unique neighbor 12, blocking (11,1) and (10,0). The pair (12,2) would require another neighbor labeled 2, although the center has its two leaves and the entrance already specified. This excludes x>2. If x=2, the same weight-12 and weight-11 forcing gives second-center palette {0,1}, and the attachment realizes weight 10. If x=1, weight 12 forces a leaf 0 at b:0:1. The scalar cases below have neither Y nor A equal to 11. Label 11 is then on a right leaf, adjacent only to b:1:0. The pair (11,1) cannot involve s:0, which has label 1, and (10,0) is blocked by the sole neighbor of 0. Hence difference 10 forces the other second-center leaf to have label 2.

For Y=8 the choices A=9,10,11 give x+z=6,8,10. With x in {0,1,2}, a sum of six permits all three entrances, eight permits 1,2, and ten permits none. For Y=10 the choices A=8,9,11 give sums 5,7,11. The first two sums permit all three entrances and the last permits none. The resulting x and z are distinct in every case. This yields exactly eleven scalar cases and excludes all others, regardless of the terminal order.

## Original edge inventory and contradictions

The six fixed weights below are in the order spine, first left attachment, second left attachment, right attachment, right leaves in increasing label order. The right-leaf palette is the unused high-label set after removing A, B and Y. Those labels have forced incidence to the right center independent of their indices.

| x | Y | A | z | Right palette | Six fixed weights | Contradiction |
|---:|---:|---:|---:|---|---|---|
| 0 | 8 | 9 | 6 | {10,11} | 8,9,12,2,4,5 | The fixed weights lack 1. Every left terminal difference is at least 9−7=2. |
| 0 | 10 | 8 | 5 | {9,11} | 10,8,12,5,4,6 | The forced first-center leaf labeled 2 and the right leaf labeled 11 both give 6. |
| 0 | 10 | 9 | 7 | {8,11} | 10,9,12,3,1,4 | The forced first-center leaf labeled 5 and the right leaf labeled 11 both give 4. |
| 1 | 8 | 9 | 5 | {10,11} | 7,8,11,3,5,6 | Neither the fixed edges nor the forced second-center palette {0,2} give 9. At the first center, zero is already used at the second center, so no leaf yields 9. |
| 1 | 8 | 10 | 7 | {9,11} | 7,9,11,1,2,4 | The first-center palette is {3,4,5,6}. Label 3 there repeats the spine's 7. |
| 1 | 10 | 8 | 4 | {9,11} | 9,7,11,6,5,7 | The first left attachment and the right terminal labeled 11 give 7. |
| 1 | 10 | 9 | 6 | {8,11} | 9,8,11,4,2,5 | The first-center palette is {3,4,5,7}. Label 4 there repeats 5 on the right edge to label 11. |
| 2 | 8 | 9 | 4 | {10,11} | 6,7,10,4,6,7 | The spine and the right terminal labeled 10 give 6. |
| 2 | 8 | 10 | 6 | {9,11} | 6,8,10,2,3,5 | The first-center palette is {3,4,5,7}. Label 4 there repeats the spine's 6. |
| 2 | 10 | 8 | 3 | {9,11} | 8,6,10,7,6,8 | The first attachment and the right terminal labeled 9 give 6. |
| 2 | 10 | 9 | 5 | {8,11} | 8,7,10,5,3,6 | The first-center palette is {3,4,6,7}. Label 4 there repeats the right attachment's 5. |

In the two x=0 rows with Y=10, weight 11 must use (12,1) on a second-center leaf. The entrance labeled 0 is adjacent only to labels A,12,10, so (11,0) is unavailable. When A=8,z=5 the complete representations for weight 9 are (12,3), (11,2), (10,1), (9,0). Labels 11 and 9 are right leaves adjacent only to z=5, and label 10 at the exit has neighbors 0 and 5. The remaining pair (12,3) forces the other second-center leaf. The second-center palette is therefore {1,3}, leaving {2,4,6,7} at the first.

When A=9,z=7 the complete representations for weight 8 are (12,4), (11,3), (10,2), (9,1), (8,0). Labels 11 and 8 are right leaves adjacent only to z=7. The exit 10 has neighbors 0 and 7, and label 1 is a leaf at center 12. Therefore (12,4) alone is possible. The second-center palette is {1,4}, leaving {2,3,5,6} at the first.

For every row in which the second-center palette is forced, the first-center palette is its complement in the low alphabet after removing x and z. Each cited repeat uses distinct actual incidences. Left and right leaf witnesses use their forced labels and center incidence, leaving the indexed positions free. The audit records all repeats among the fixed edges and any forced terminal palettes. Several cases repeat multiple weights.

## Scope and disposition

All eleven cases contradict the required bijection on the actual difference alphabet. The proof excludes the specified maximum placement even with both ports free. It leaves the D098 labeling at its original host value and other host positions outside the exclusion. The source premise for the conditional translation is absent, so no target labeling or extension was executed. D099 and D100 remain distinct restrictions on the frozen target.
