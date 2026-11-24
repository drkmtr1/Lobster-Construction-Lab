# D110 — Location-free magnitude-two obstruction on ordered [[5,3],[2]]

Use the [frozen D108 original](../evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json), graph digest `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8` and file SHA-256 `9dbdfd6226c94c821951bc0ca701c18e4a0e1b671324afa84b0431fec36aca0c`. Its spine is `s:0--s:1`. The first and second left centers `b:0:0` and `b:0:1` attach to `s:0` and have five and three indexed terminals. The right center `b:1:0` attaches to `s:1` and has two indexed terminals. These are the original 15 vertices and 14 distinct edges. Every center is one edge from the spine and each terminal is two edges away.

Assume an ordinary graceful labeling with `s:0=0`, `s:1=14`, `b:1:0=1` and exactly one signed difference −2 at an actual left terminal. Orient edges from the traversal class containing `s:0`. Write A,B for the left-center labels and P,Q for the right-terminal labels.

## Signed degree identity and case exhaustion

The class of `s:0` consists of that vertex, the right center and the eight left terminals. The other class contains `s:1`, the two left centers and the two right terminals. The degrees of `s:0`, `s:1`, `b:0:0`, `b:0:1` and `b:1:0` are 3,2,6,4,3, respectively. All terminals have degree one. The label sum is 105. The unweighted sum in the first class is 91−A−B−P−Q, and its degree corrections are 0 at `s:0` and 2 at the right center. Its weighted sum is 93−A−B−P−Q. The other class has weighted sum 28+6A+4B+P+Q. Subtracting the first weighted sum from the second gives the actual signed edge sum by incidence counting. Negating the unique absolute weight 2 in [1,14] changes the sum by −4, so the signed sum is 101. Therefore

```text
7A + 5B + 2(P+Q) = 166.
```

The coefficients 7 and 5 are odd and the right-hand side is even, so A and B have the same parity. No ordering of labels by traversal class is assumed.

The spine and right attachment already supply weights 14 and 13. A left center carrying 13 would repeat weight 13 on its attachment to `s:0=0`. If a left terminal carries 13 it must be the reversed terminal because its neighbor then carries less than 13. The vertices pinned at 0, 14 and 1 are unavailable. This leaves exactly three cases for 13, by the two left-center groups and the right-terminal group. This reasoning does not assign any terminal index. Within a center, permuting terminal labels preserves the signed and absolute difference multisets and the three pinned vertices.

## I. Label 13 on a right terminal

That right-terminal edge has weight 12. The left-center labels are at most 11 because either center carrying 12 would repeat it against the entrance. Put P=13 and let Q denote the other right-terminal label. Then Q≤12 and 7A+5B+2Q=140, which gives 7A+5B≥116.

The largest same-parity even pair bound is 7·10+5·8=110, and the odd pair bound outside {9,11} is 7·11+5·7=112, as in [D109](ORDINARY_53_2_FREE_REVERSAL.md). In each case the maximum pairs the larger coefficient with the larger available label. The bounds leave only the two orders of {9,11}.

| A | B | Forced Q | Distinct physical vertices with the same label |
| ---: | ---: | ---: | --- |
| 11 | 9 | (140−122)/2=9 | `b:0:1` and the right terminal carrying Q |
| 9 | 11 | (140−118)/2=11 | `b:0:1` and the right terminal carrying Q |

Either right terminal could carry Q, but both are distinct from `b:0:1`. Both rows violate injectivity.

## II. Label 13 on the reversed first-left terminal

The signed difference A−13=−2 forces A=11. Substitution gives 5B+2(P+Q)=89. Right-terminal labels cannot be 11, 13 or 14 and must be distinct. Their largest sum is 12+10=22. Thus 5B≥89−44=45, so B≥9. Since B is odd, distinct from 11 and less than 13, B≤9. This forces B=9 and P+Q=22, hence {P,Q}={10,12}.

At right-center label 1, the two right-terminal edges have weights 9 and 11. The second-left attachment `s:0--b:0:1` already carries weight 9 and the first-left attachment `s:0--b:0:0` carries weight 11. The right-terminal incidences are distinct from each other and from both attachments. Thus the four forced incidences give multiplicities 2 and 2 for weights 9 and 11, respectively. The right-terminal ordering is irrelevant. These repeats suffice regardless of the remaining edge differences.

## III. Label 13 on the reversed second-left terminal

The signed difference B−13=−2 forces B=11. Now 7A+2(P+Q)=111. Equal parity and the labels 11, 13 and 14 already used imply that A is odd and at most 9. As above, P+Q≤22. Thus the largest possible left-hand side is at most 7·9+2·22=107, strictly below 111. No scalar row survives this case.

All three cases fail. This excludes only the location-free single magnitude-two interface under the three pins on this original. Other interfaces and ordinary gracefulness without these constraints remain undecided. [D107](ORDINARY_43R_EXTREME_SPINE.md), [D108](ORDINARY_53_2_SIGNED_SEED.md) and D109 retain their accepted scopes. [Independent audit](../evidence/validation/LCL_ORDINARY_53_2_MAGNITUDE_TWO_001/result.json)
