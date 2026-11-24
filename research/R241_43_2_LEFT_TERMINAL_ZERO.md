# D104 — Left-terminal zero obstruction on ordered [[4,3],[2]]

Use the frozen named [D099 original](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json), digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. The spine is `s:0--s:1`. The first and second left centers `b:0:0`, `b:0:1` attach to `s:0` and have four and three indexed terminals. The right center `b:1:0` attaches to `s:1` and has two indexed terminals. Each terminal has precisely its own center as neighbor. These incidences form a connected tree on 14 vertices and 13 edges. Its bipartition has one class of size nine, consisting of `s:0`, `b:1:0` and the seven left terminals, and the other of size five.

Suppose the size-nine class has labels [0,8] and the size-five class labels [9,13], with all differences [1,13] occurring once. Let x,Y be the labels of `s:0`, `s:1` and A,B,z those of the centers in the order above. The hypothesis is zero at any left terminal, with no other pin.

## The extremal incidences

Difference 13 requires labels 0 and 13 on adjacent vertices. The left terminal carrying zero has only its designated center as neighbor, forcing label 13 onto that center. Denote its terminal quota by t and the other left center's label by C. The low label x is positive.

For each integer j from 0 to x−1, the vertex labeled j must be a terminal of the center labeled 13. The assertion for j=0 follows from the pin and the maximum difference. For j>0 require difference 13−j. If its high endpoint has label h<13, its low label would be h−(13−j)<j. A nonnegative label below j is already on a forced terminal by induction. Its only neighbor carries 13, precluding h<13. Thus the edge for 13−j must use high label 13 and low label j. The actual neighbors of that center are its terminals and the entrance carrying x. Since j<x, the new forced label is on one of those terminals. The induction treats each terminal index by the same unique-neighbor property.

Consequently x distinct labels 0 through x−1 occupy t actual terminal positions, giving 1≤x≤t. The right center is outside those positions and z differs from x, so x<z≤8. For A=13 the quota is t=4, and for B=13 it is t=3.

## Signed degrees and exact scalar reduction

The degrees at `s:0`, `s:1`, `b:0:0`, `b:0:1` and `b:1:0` are 3, 2, 5, 4 and 3. The other nine vertices have degree one. Every difference is the high label minus the low label, so the signed sum is the degree-one contribution 55−36=19 plus Y+4A+3B−2x−2z. This sum must equal 91. Therefore

```text
2(x+z)=4A+3B+Y−72
       =3C+Y−20 for A=13
       =4C+Y−33 for B=13.
```

There are 12 ordered pairs C,Y from [9,12] for each location of 13. With S=(4A+3B+Y−72)/2, parity requires S integral and z=S−x. For integral S the full range is

```text
max(1,S−8) ≤ x ≤ min(t,floor((S−1)/2)).
```

The lower bound enforces z≤8. The upper bounds enforce x≤t and x<z. For A=13 parity leaves (C,Y,S)=(9,11,9),(10,12,11),(11,9,11),(12,10,13). The last row has empty range. For B=13 parity makes Y odd. For Y=9, C=10,11,12 gives S=8,10,12. For Y=11, C=9,10,12 gives S=7,9,13. The ranges for S=12 and 13 are empty in this center case. These restrictions cover all 24 role pairs and all 84 associated choices of x before rejection.

## Residual palettes

Let H be the increasing pair of unused high labels. These labels occupy the right terminals in either order. The spine, three attachments and two right-terminal edges give Y−x, A−x, B−x, Y−z, H[0]−z, H[1]−z. The induction adds the x distinct weights 13−j for j in [0,x−1] on the left terminals of the maximum center. Let W include all six fixed differences and those x forced differences, with multiplicities. All remaining original edges are the other 7−x left-terminal edges. Their low endpoints exhaust L=[x+1,8]∖{z}. For a missing weight w it is enough that w is absent from W and that neither of the only possible remaining low endpoints, 13−w and C−w, lies in L. This checks both left centers even if the maximum center has no remaining position.

The table lists every feasible scalar row in groups. Within each row the x, z and w entries correspond in order. Substitution gives w absent from W and both candidate endpoints outside L for each triple. The full expanded checks are in the [case records and incidence audit](../evidence/validation/LCL_R241_43_2_LEFT_TERMINAL_ZERO_001/result.json), including fixed multiplicities and unordered terminal palettes.

| Center with 13 | C | Y | x | z | Missing w |
| --- | ---: | ---: | --- | --- | --- |
| A | 9 | 11 | 1,2,3,4 | 8,7,6,5 | 1,2,3,4 |
| A | 10 | 12 | 3,4 | 8,7 | 2,1 |
| A | 11 | 9 | 3,4 | 8,7 | 3,1 |
| B | 9 | 11 | 1,2,3 | 6,5,4 | 3,4,9 |
| B | 10 | 9 | 1,2,3 | 7,6,5 | 1,1,1 |
| B | 10 | 11 | 1,2,3 | 8,7,6 | 2,1,1 |
| B | 11 | 9 | 2,3 | 8,7 | 3,1 |

For example, B=13, C=9, Y=11 and x=3 gives z=4, H=(10,12), W=(8,6,10,7,6,8,13,12,11) and L={5,6,7,8}. Weight 9 is absent from W, and its candidate endpoints 4 and 0 are consumed. All 19 rows have a missing-weight witness. Any additional fixed repeats are recorded as separate evidence within their row.

## Consequence for both alpha orientations

[D102](R241_43_2_RIGHT_ZERO_HOST.md) and [D103](R241_43_2_ZERO_ENTRANCE.md) use the same frozen D099 original and the same size-nine low class. They exclude zero on the right center and on `s:0`, respectively. The present result excludes zero at every left terminal, exhausting all nine vertices of that low class. Thus the cut with nine low labels is impossible.

In a connected tree every division into two classes crossing all edges is the tree's unique bipartition up to exchange. A hypothetical alpha labeling with the size-five class low uses [0,4] on that class and [5,13] on the size-nine class. The complement g(v)=13−f(v) would preserve the original graph, label bijection and all differences while assigning [0,8] to the size-nine class and [9,13] to the size-five class. This contradicts the cut-nine result without a second cut test. The exact original therefore admits no alpha labeling. Ordinary gracefulness remains undecided by this result.
