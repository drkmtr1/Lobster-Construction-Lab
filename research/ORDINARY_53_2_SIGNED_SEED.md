# D108 — Obstruction to the prescribed signed seed on ordered [[5,3],[2]]

The exact ordered profile `[[5,3],[2]]` has physical spine `s:0--s:1`. The centers `b:0:0`, `b:0:1` and `b:1:0` have five, three and two indexed terminals. The two left centers attach to `s:0` and the right center to `s:1`. Each terminal has just its named center as neighbor. Relative to the [D105 original](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json), the only change is the new fifth terminal `l:0:0:4` at `b:0:0`. This gives 15 named vertices and 14 distinct edges. The original spine still witnesses the required distance bound of two. [Archived target](../evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json)

Suppose an ordinary graceful labeling on this exact graph gives `s:0=0`, `s:1=14` and `b:1:0=1`. Orient all edges from the traversal class containing `s:0`, and suppose the sole negative signed difference is −1 on `l:0:0:3 → b:0:0`. Write A and B for the first and second left-center labels, P and Q for the two right-terminal labels, and m=14. The specified reversal forces the label at `l:0:0:3` to be A+1.

## Signed degree sum

The even-distance class is the entrance, right center and all eight left terminals. The odd-distance class is the exit, two left centers and two right terminals. Degrees at the entrance, exit, first left center, second left center and right center are 3, 2, 6, 4 and 3. Every terminal has degree one.

All labels sum to 105. The odd class labels sum to 14+A+B+P+Q, so the even class labels sum to 91−A−B−P−Q. Even weighted excess degree contributes 2 at the right center and zero at the entrance. The even weighted sum is therefore 93−A−B−P−Q. On the odd side, the weighted sum is 28+6A+4B+P+Q. The difference of the weighted sums equals the sum of head labels minus tail labels over the actual oriented edges, regardless of alpha separation. Replacing the single absolute weight 1 by −1 gives required signed sum 105−2=103. Equating yields

```text
7A+5B+2(P+Q)=168.
```

In particular A and B have the same parity.

## Exhaustive split by label 13

The spine and right attachment already give weights 14 and 13. Either left center carrying label 13 would repeat weight 13 on its own attachment to the zero entrance. The only label larger than 13 is 14, already at the exit. Thus a left terminal labeled 13 would yield a negative incidence and must be the designated reversed terminal. All other available vertices are right terminals. This exhausts the locations of label 13 without fixing an index for either right-terminal value.

### I. Label 13 at a right terminal

That terminal supplies difference 12 against right-center label 1. Any left center labeled 12 would repeat it against the zero entrance. Hence A,B≤11. Writing P=13 and Q for the other label without assigning terminal indices, the signed equation reduces to 7A+5B+2Q=142. Since Q≤12, the center expression is at least 118.

For distinct even center labels, the two largest available values are 10 and 8. The maximum 7·10+5·8=110 uses the larger coefficient at the larger label. For an odd pair other than {9,11}, the larger label is at most 11 and the smaller at most 7. Its weighted sum is at most 7·11+5·7=112 by the same coefficient comparison. Neither bound reaches 118. The two remaining ordered rows give the contradictions below.

| A | B | Forced Q | Right-terminal difference | Repeated weight on the second left attachment |
| ---: | ---: | ---: | ---: | ---: |
| 11 | 9 | (142−122)/2=10 | 10−1=9 | 9−0=9 |
| 9 | 11 | (142−118)/2=12 | 12−1=11 | 11−0=11 |

The right-terminal edge carrying Q and the second left attachment are distinct original incidences in either ordering of the right terminals.

### II. Label 13 at the designated reversed terminal

Because the reversed terminal label is A+1, we get A=12. The signed equation gives 5B+2(P+Q)=84. B is even, distinct from A, and at most 10. The two right-terminal labels are distinct and at most 11 because 12, 13 and 14 are already used. Hence P+Q≤11+10=21. This gives 5B≥84−42=42, so B=10.

Label 11 remains unused by the nonterminals and the reversed terminal. On any other first-left terminal it gives difference 12−11=1, repeating the absolute weight 1 on the designated negative edge. At a second-left terminal it gives signed difference 10−11=−1, creating a second negative edge. Thus 11 must be a right terminal, where its difference is 11−1=10. This repeats the weight 10 on the second left attachment from s:0. The two conflicting incidences are distinct for either right-terminal index.

Both cases contradict the specified interface on this exact graph. This excludes the prescribed seed while leaving ordinary gracefulness under other label or signed-edge constraints undecided. [D107](ORDINARY_43R_EXTREME_SPINE.md) remains the separate quantified construction with fixed left quotas 4 and 3. [Case records and independent audit](../evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/result.json)
