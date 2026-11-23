# Symbolic exclusion of the physical (4,4) state on `[[3,b],[2]]`

[Evidence and reproduction](../evidence/validation/LCL_R241_3B2_PORT44_SYMBOLIC_001/README.md) · [D087 supplier](R241_2B2_SYMBOLIC_PORT34.md) · [Adopted R241](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** For every integer b≥2, the exact named original T_b=`[[3,b],[2]]` does not supply the normalized alpha state A(b+10,b+5;4,4) with physical entrance s:0 and exit s:1. The exclusion concerns this prescribed orientation, cut and port pair.

## Named graph and forced classes

The original has spine s:0–s:1. Centers b:0:0 and b:0:1 attach to s:0, and b:1:0 attaches to s:1. The three terminal groups are l:0:0:j for j=0,1,2, l:0:1:j for 0≤j<b, and l:1:0:j for j=0,1. Each terminal has its own center as its sole neighbor. Each named center is distance one from the spine and each terminal distance two. The five nonterminal vertices and b+5 indexed terminals give N=b+10. The spine edge, three attachments and b+5 terminal edges give m=b+9. Distinct section, branch and terminal indices give each incidence multiplicity one.

With s:0 low, the crossing condition fixes the lows as s:0, b:1:0 and all b+3 first-section terminals. The five high vertices are s:1, both first-section centers, and the two right terminals. The low labels are [0,b+4] and the high labels [b+5,b+9]=[m−4,m]. The declared ports force s:0=4 and s:1=m. All subsequent deductions allow every bijection within the prescribed classes.

## Primary proof by the four largest differences

For 0≤k≤3, the representations of difference m−k have larger label m−k+i and smaller label i for 0≤i≤k. This parameterization is exhaustive because the lower label is nonnegative and the upper one at most m. At b≥2 the smaller labels are all low and the larger ones all high. There are exactly 1+2+3+4=10 representations across the four distinct differences.

1. **Weight m.** Only (m,0) is possible. The only neighbors of s:1=m are s:0=4 and b:1:0. Thus b:1:0=0, and s:1–b:1:0 supplies m.
2. **Weight m−1.** The representations are (m,1) and (m−1,0), listed high first. The first edge is absent because s:1 now has neighbors labeled 4 and 0. The label m−1 must be on a right terminal adjacent to b:1:0. Its sole incident weight is m−1.
3. **Weight m−2.** The three representations are (m,2), (m−1,1) and (m−2,0). The first violates the known neighbors of s:1. The second violates the sole neighbor zero of the terminal just identified. Thus the other right terminal must carry m−2. This uses both actual right-terminal names in an arbitrary order and exhausts that group.
4. **Weight m−3.** The four representations are (m,3), (m−1,2), (m−2,1) and (m−3,0). The first violates the neighbors 4 and 0 of s:1. The second and third violate the sole neighbor zero of their respective right terminals. The label m−3 lies at one of the two first-section centers, whose possible labels are now m−4 and m−3. Neither center is adjacent to b:1:0, the vertex labeled zero. The final representation is therefore absent as well.

This leaves a required difference absent in every permitted named assignment, for every b≥2. At the boundary b=2 the five highs are 7 through 11. The same argument forces 11, 10 and 9 on the right attachment and terminal edges and excludes 8. In particular the proof does not depend on which right-terminal index receives the larger of the two terminal values or on how the two first centers are ordered by label.

## Independent signed-degree route after the maximum edge

This route uses the same maximum-edge premise z=0 and does not require Steps 2–4 above. Write A for the label at quota-three b:0:0, B at quota-b b:0:1, and z at b:1:0. At s:0, s:1, b:0:0, b:0:1 and b:1:0 the original degrees are 3, 2, 4, b+1 and 3. The signed sum of high minus low over the edges starts with each vertex once. The high label sum is 5b+35 and the low label sum is (b+4)(b+5)/2. The excess-degree contributions of the ports give (b+9)−8=b+1, and the remaining corrections are 3A+bB−2z. Therefore
```text
(b+9)(b+10)/2 = 5b+35 − (b+4)(b+5)/2 + (b+1) + 3A+bB−2z
3A+bB−2z = b²+8b+19.
```

With z=0 set A=b+5+a and B=b+5+d for distinct a,d in {0,1,2,3}. This yields 3a+bd=4. If d=0, 3a=4 has no integral solution. If a≥2 the left side exceeds 4. If a=1, bd=1 is impossible for b≥2 and d>0. Thus a=0 and bd=4. The only cases are (b,d)=(2,2) and (4,1), each with a=0.

For each of those cases the right terminals receive the remaining two free high labels, in either index order. Before checking the left terminal edges, the spine, three attachments and two right-terminal edges have the following weight sets.

| b | A, B | Right-terminal labels | Six already determined weights | Absent required weight |
|---:|---|---|---|---:|
| 2 | 7, 9 | 8, 10 | {3,5,7,8,10,11} | 9 |
| 4 | 9, 10 | 11, 12 | {5,6,9,11,12,13} | 10 |

All remaining edges go from A or B to first-section terminal leaves. Every such terminal has label at least one because z already uses zero. In both rows the absent weight is B=max(A,B), whereas those terminal weights are at most B−1. This independently excludes the last two cases using the signed degree equation and the shared maximum-edge deduction. In particular the b=4 ordered center pair is consistent with the three largest weights. Its contradiction is the remaining gap at weight 10. The stronger preliminary suggestion of a clash with the forced placement of the top three weights for both cases would overstate that intermediate step.

## Disposition and interface scope

**ACCEPT** the analytic obstruction and **REJECT — EXCLUDED** the prescribed state across b≥2. The primary proof uses only the bounded representation lists and exact original incidences under the alpha cut and ports. The signed-degree route adds the edge-sum condition, shares only the initial maximum-edge deduction, and closes its two residual cases separately. The verified b=2 topology receipt corroborates the boundary arithmetic. The D087 and D086 positive certificates are retained controls on their own originals.

D087's exit offset four would require a supplied entrance with offset four at the actual next low vertex under R241. This proposed module cannot furnish the simultaneous entrance and exit pins. Other physical states and ordinary gracefulness on T_b lie outside this exclusion.
