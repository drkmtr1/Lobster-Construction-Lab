# D102 — Right-zero-host obstruction on ordered [[4,3],[2]]

Fix the exact named [D099 original](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json), digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. The physical spine is `s:0--s:1`. The left centers `b:0:0` and `b:0:1` attach to `s:0` and have respectively four and three indexed terminal neighbors. The right center `b:1:0` attaches to `s:1` and has two indexed terminal neighbors. Every terminal has just its designated center as neighbor. The 14 vertices and 13 edges form the original tree with all centers and terminals one and two steps from the spine, respectively.

Suppose the original admits an alpha labeling with low alphabet 0 through 8, high alphabet 9 through 13, and physical right center label zero. Its low class consists of the entrance, the right center and the seven left terminals. Its high class consists of the exit, both left centers and both right terminals. Write x and Y for the free spine labels, A and B for the ordered left-center labels and z=0 for the right-center label.

## Original incidences force the spine weight

The 13 edges partition into the spine singleton, five edges at `b:0:0`, four at `b:0:1`, and three at `b:1:0`. Each center group includes its attachment and all and only its indexed terminal edges. Centers are pairwise nonadjacent, so the groups are disjoint.

Weight 13 has the unique numerical representation 13−0. Thus label 13 is on a neighbor of the right center, either `s:1` or one of the right terminals. Both A and B belong to [9,12] and are distinct. Let M=max(A,B). Required weight M is within [1,13]. The three right-center edges have weights equal to their high labels, all distinct from A and B. Every left-center edge has a positive low endpoint, since the right center occupies zero and is not adjacent to either left center. Its difference is at most M−1. The spine is the sole remaining incidence, which forces Y−x=M. The argument applies to all indexed terminal orders and uses no choice of numerical exit.

## Signed degrees exclude both orders

Every edge crosses the cut, so summing its high label minus low label is equivalent to summing the signed degree times each label. Counting each label once contributes 55−36=19. The original degrees of the entrance, exit, first left center, second left center and right center are 3,2,5,4,3. Every terminal contributes only its degree-one term. The required sum is 1+…+13=91, giving

```text
91 = 19 + Y + 4A + 3B − 2x − 2z.
```

With z=0 and x=Y−M this becomes `4A+3B+2M=72+Y`. The two strict orders exhaust the distinct center labels.

| Order | Lower bound on 4A+3B+2M | Upper bound on 72+Y |
| --- | --- | --- |
| A>B | 6A+3B ≥ 6·10+3·9 = 87 | 85 |
| B>A | 4A+5B ≥ 4·9+5·10 = 86 | 85 |

Both bounds use distinct high labels at least nine and the positive coefficients in the corresponding order. Even a high port of thirteen cannot close either gap. The required equality is impossible.

**Disposition.** The obstruction covers the specified right-zero host and cut-9 orientation on this exact graph for every entrance and exit in the corresponding classes. Other host constraints, orientations, quota triples and ordinary gracefulness are outside this proof. D097–D101 keep their respective domains and dispositions. The executable corroboration checks the frozen original and the two deductions. [Evidence](../evidence/validation/LCL_R241_43_2_RIGHT_ZERO_HOST_001/README.md).
