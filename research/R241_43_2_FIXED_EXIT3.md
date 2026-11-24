# D100 fixed-exit-three obstruction on the ordered 4,3,2 original

[Evidence](../evidence/validation/LCL_R241_43_2_FIXED_EXIT3_001/README.md) · [D099 original and scoped insertion result](R241_43_2_LOWER_BLOCK.md) · [D097](R241_QAR_ALPHA_SUPPLIER.md) · [D098](R241_NAMED_CENTER_ROLE_TRANSPORT.md)

**ACCEPT** the structural obstruction. **REJECT** A(14,9;x,3) on exact ordered `[[4,3],[2]]` for every integer 0≤x≤8.

## Actual graph and signed degree reduction

Use the frozen D099 graph. Its one spine edge is s:0–s:1. The left attachments join s:0 to b:0:0 and b:0:1, with four and three indexed terminals at their respective centers. The right attachment joins s:1 to b:1:0, which has two indexed terminals. Every leaf has just its designated center as its neighbor. The named graph has 14 vertices, 13 edges and the original spine as witness. In the prescribed alpha orientation the low names are s:0, b:1:0 and the seven left terminals. The high names are s:1, b:0:0, b:0:1 and the two right terminals.

Write x for the entrance label, A and B for the four- and three-leaf left center labels respectively, and z for the right center label. The physical exit s:1 is 12. Every edge difference is high label minus low label. Summing that expression on the actual edges counts each vertex label with signed degree. The high alphabet [9,13] sums to 55, and the low alphabet [0,8] sums to 36. Giving each label one signed contribution accounts for 19. Above degree one, the original degrees of s:0, s:1, b:0:0, b:0:1 and b:1:0 are 3, 2, 5, 4 and 3 in total. Their extra signed contributions are −2x, +12, +4A, +3B and −2z. Every other vertex has degree one.

The required difference sum is 91. Consequently
`91=19+12+4A+3B−2x−2z`, or `4A+3B−2(x+z)=60`.
Reducing modulo two forces B even. With 12 reserved at s:1, the only available even high label is 10. It follows that A is 9, 11 or 13 and x+z=2A−15.

## Extreme differences and all residual cases

Weight 13 can only come from labels (13,0), written here with the high first. If A=9 or 11, label 13 is a right terminal. Its sole neighbor is b:1:0, so z=0 and the signed equation fixes x=3 or 7, respectively. The first two rows in the table below exhaust both of these A cases.

For A=13, the right terminal labels are {9,11}. Now x+z=11 with x,z∈[0,8], so x takes every integer 3 through 8 with z=11−x. There is no equal integer pair, and neither label can be 0, 1 or 2.

| Required difference | All possible (high,low) representations |
| --- | --- |
| 13 | (13,0) |
| 12 | (13,1), (12,0) |
| 11 | (13,2), (12,1), (11,0) |
| 10 | (13,3), (12,2), (11,1), (10,0) |

The four-leaf left center carries 13. The entrance is nonzero, so its required neighbor 0 must be one of its own indexed terminals. That leaf has only the center labeled 13 as its neighbor, eliminating (12,0) for weight 12 and forcing label 1 onto another leaf at that center. The fixed unique neighbors of 0 and 1 eliminate (11,0) and (12,1) for weight 11, so label 2 is a third leaf there. For weight 10, the fixed neighbors of 0, 1 and 2 eliminate all representations except (13,3). No terminal ordering is assumed.

| A | x | z | Actual incidence contradiction |
| ---: | ---: | ---: | --- |
| 9 | 3 | 0 | The spine, first attachment, second attachment, right attachment and two right-terminal edges supply 9,6,7,12,11,13. Both left centers are at most 10 and all left terminal labels are positive, so their terminal edges cannot supply 10. |
| 11 | 7 | 0 | The same structural edge groups supply 5,4,3,12,9,13. Both left centers are at most 11, with positive left terminal labels, so weight 11 is absent. |
| 13 | 3 | 8 | The first attachment supplies weight 10. The four remaining low labels after fixing the entrance, right center and first-center leaves 0,1,2 are {4,5,6,7}. The right attachment has weight 4 and the right edge to label 11 has weight 3. At B=10, leaves 6 and 7 would repeat those weights. Both labels need the single unfilled first-center terminal position. |
| 13 | 4 | 7 | Label 3 must be the fourth terminal at A=13 to give weight 10. The three leaves at B=10 have palette {5,6,8}, giving differences {5,4,2}. The distinct right attachment and terminal edges have the same differences 12−7, 11−7 and 9−7. |
| 13 | 5 | 6 | The second left attachment and the right edge to label 11 both give weight 5. |
| 13 | 6 | 5 | The first left attachment and right attachment both give weight 7. |
| 13 | 7 | 4 | The spine edge and the right edge to label 9 both give weight 5. |
| 13 | 8 | 3 | Label 3 is at b:1:0, which is not adjacent to b:0:0 carrying 13. The only available representation of weight 10 lacks its original incidence. |

These eight scalar cases exhaust the permitted fixed-exit state. A missing difference or a repeat contradicts gracefulness, and the one-position shortage rules out completing that row. This conclusion applies to every alpha labeling with the stated cut, orientation and physical exit. It leaves other numerical exits and ordinary gracefulness open. The D097 and D098 suppliers and the separate D099 fixed-ledger exclusion retain their respective scopes.
