# D109 — Location-free magnitude-one obstruction on ordered [[5,3],[2]]

Use the [frozen D108 original](../evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json), graph digest `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8`. The physical spine `s:0--s:1` has two left centers at `s:0` with five and three indexed terminals and one right center at `s:1` with two indexed terminals. Every terminal has exactly one edge to its own center. The 15 vertices and 14 distinct edges have distance at most two from the spine.

Assume an ordinary graceful labeling with `s:0=0`, `s:1=14`, `b:1:0=1` and exactly one negative signed difference −1 on a left-terminal incidence. Orient all edges from the class containing `s:0`. Let A and B be the two left-center labels and P and Q the right-terminal labels.

## Terminal indices and signed degree sum

A permutation of the terminal labels within one center permutes only the signed differences on that center's leaf edges. Those terminals all have the same traversal parity and the same sole neighbor. Therefore the vertex-label bijection, absolute difference multiset, three pins, count and magnitude of negative differences, and their membership in left-terminal incidences are preserved. The names and role records of the original stay fixed. This permits reasoning by center group and edge weight without counting named labelings. It does not interchange the two left-center roles.

The even class contains `s:0`, the right center and the eight left terminals. The odd class contains `s:1`, both left centers and both right terminals. Their respective unweighted label sums are 91−A−B−P−Q and 14+A+B+P+Q, since the total is 105. Degrees at `s:0`, `s:1` and the three centers in the order above are 3,2,6,4,3. All terminal degrees are one. Thus the even weighted sum is 93−A−B−P−Q and the odd weighted sum is 28+6A+4B+P+Q. The signed sum is their difference and must equal the absolute sum 105 with the lone weight one negated, namely 103. Therefore

```text
7A + 5B + 2(P+Q) = 168
```

and the two left-center labels have equal parity. No label separation is needed for the degree identity.

## Label 13 gives three cases

The original spine and right attachment already carry weights 14 and 13. A left center labeled 13 would repeat weight 13 on its entrance attachment. The only label above 13 is pinned to the exit. Thus a left terminal labeled 13 is on the unique reversed incidence. The only places left for 13 are a right terminal, the reversed terminal of the first left center, and the reversed terminal of the second left center.

### I. Label 13 at a right terminal

As in [D108](ORDINARY_53_2_SIGNED_SEED.md), the right-terminal edge of label 13 supplies weight 12. Neither left center can carry 12. Write P=13 and Q for the other right label, so Q≤12 and 7A+5B≥142−24=118. For distinct even labels at most 11 the maximum is 7·10+5·8=110. For an odd pair other than {9,11}, the larger label is at most 11 and the smaller at most 7, yielding a bound of 7·11+5·7=112. Both bounds pair the larger label with the larger coefficient. Thus the two surviving orders (A,B)=(11,9),(9,11) force Q=10,12 respectively. The right edge for Q has weight Q−1, which repeats B on the second-left attachment `s:0--b:0:1` in each row (weights 9 and 11). The incidences are distinct whichever right index carries Q. None of these deductions requires a fixed reversal location.

### II. Label 13 at the reversed terminal of the first left center

The reversed edge gives A−13=−1, hence A=12. The reduced equation is 5B+2(P+Q)=84. Both right labels are at most 11 and distinct, giving P+Q≤21. With B even and distinct from 12, we have B≤10, while 5B≥84−42=42. Thus B=10. This is D108's center-group argument with the reversed terminal index free. Label 11 on a different first-left terminal repeats weight 1. On a second-left terminal it creates another negative signed difference −1. Hence label 11 is right-terminal, with weight 10 against label 1, repeating the distinct second-left attachment of weight 10.

### III. Label 13 at the reversed terminal of the second left center

Now B−13=−1 gives B=12, so 7A+2(P+Q)=108. The distinct right labels still satisfy P+Q≤11+10=21 because 12, 13 and 14 are consumed. Hence 7A≥66. A is even by parity, distinct from B=12, and at most 11, so A=10 is forced. The nonterminal labels and reversed terminal label leave 11 unused. If 11 occupies any first-left terminal, its signed difference is 10−11=−1, a second negative edge. If 11 occupies a second-left terminal distinct from the reversed one, its signed difference is 12−11=1, repeating the absolute weight on the reversed edge. Thus 11 must occupy a right terminal, where 11−1=10 repeats the weight on the distinct first-left attachment `s:0--b:0:0`. Both possible indices have the same witness.

All three cases fail. The exact exclusion is the magnitude-one signed interface with the three specified pins on the frozen ordered original. Ordinary gracefulness with different restrictions remains undecided by this proof. D108 remains the earlier fixed-incidence obstruction, and [D107](ORDINARY_43R_EXTREME_SPINE.md) remains proved for its fixed left quotas. [Independent audit](../evidence/validation/LCL_ORDINARY_53_2_FREE_REVERSAL_001/result.json)
