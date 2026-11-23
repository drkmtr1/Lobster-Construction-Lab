# Original R241 composition of D087 and D089

[Evidence and reproduction](../evidence/validation/LCL_R241_2B2_3B3_JOINT_001/README.md) · [D087](R241_2B2_SYMBOLIC_PORT34.md) · [D089](R241_3B3_PORT45_SYMBOLIC.md) · [Adopted R241.1](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** For every pair of integers a,b≥2, the exact named original `[[2,a],[2],[3,b],[3]]` independently supplies A(a+b+20,a+b+9;3,5), witnessed by the actual path s:0–s:1–s:2–s:3.

## Original components and R241.1 hypotheses

The first two sections induce old block B, the D087 original `[[2,a],[2]]`. Keep all its names. Its independently supplied alpha map f_B has order n_B=a+9, low size p_B=a+4 and actual ports L_B=s:0 and U_B=s:1 labeled 3 and a+8=p_B+4. The last two sections induce new block A, the D089 original `[[3,b],[3]]`. For A, add two to the local section index in each spine, center and terminal name. The branch and terminal indices remain the same. This assigns L_A to actual s:2 and U_A to actual s:3, with local labels 4 and b+10=p_A+5 at n_A=b+11 and p_A=b+5. The two renamed vertex sets are disjoint because their section sets are disjoint. Both formulas supply the input maps directly for all a,b≥2, and their ports are within the required local classes. Specifically, the lows contain 3 and 4 respectively and the highs have sizes five and six, so offsets four and five are admissible.

The exact target has four spine vertices, six distinct centers and a+b+10 distinctly indexed terminal leaves. Its edges are the three actual spine edges, six attachments and a+b+10 terminal edges. The two induced components together account for all vertices and all but the sole cross-component edge s:1–s:2. Every named center and leaf retains its prescribed parent and unique attachment incidence. Thus N=a+b+20 and m=N−1=a+b+19. The original connector is U_B–L_A and the compatibility equation is y_B=4=x_A. This is the binary orientation in the [adopted source](../references/upstream/mdl/N241_relational_ports.md), with later block A and earlier block B. The local s:0–s:1 witnesses are paths between their respective physical ports.

## Placement and complete vertex inventory

Use F=f_A+p_B in A, F=f_B on B's low class and F=f_B+n_A on B's high class. Here are the resulting labels, with j ranging over exactly the indexed terminals of each named center.

| Original name | Global label |
|---|---|
| s:0 | 3 |
| s:1 | a+b+19 |
| s:2 | a+8 |
| s:3 | a+b+14 |
| b:0:0 and l:0:0:j, 0≤j<2 | a+b+16 and 1+j |
| b:0:1 and l:0:1:j, 0≤j<a | a+b+15 and 4+j |
| b:1:0 and l:1:0:j, 0≤j<2 | 0 and a+b+17+j |
| b:2:0 and l:2:0:j, 0≤j<3 | a+b+10 and a+5+j |
| b:2:1 and l:2:1:j, 0≤j<b | a+b+9 and a+9+j |
| b:3:0 and l:3:0:j, 0≤j<3 | a+4 and a+b+11+j |

| Group | Local alphabet | Global alphabet |
|---|---|---|
| B low | [0,a+3] | [0,a+3] |
| A low | [0,b+4] | [a+4,a+b+8] |
| A high | [b+5,b+10] | [a+b+9,a+b+14] |
| B high | [a+4,a+8] | [a+b+15,a+b+19] |

Each placement is a translation on its class, so injective there. Each band starts one above the previous band's end. The first starts at zero and the last ends at m. Thus every label [0,m] occurs once. The first two bands are the global lows [0,P−1] at P=p_A+p_B=a+b+9. The last two bands are the highs [P,m]. Each internal edge crosses P because its original low and high endpoints retain these classes. The connector crosses from s:1 in B's high band to s:2 in A's low band.

## Complete edge inventory

Translation of both endpoints in A preserves the whole local spectrum [1,b+10]. On each internal edge of B, the high endpoint gains n_A=b+11 while its low endpoint stays fixed. The resulting spectrum is [b+12,a+b+19]. The connector fills the intervening singleton. In local terms its weight is (p_B+y_B+n_A)−(p_B+x_A)=n_A. On its actual named endpoints it is F(s:1)−F(s:2)=(a+b+19)−(a+8)=b+11. It is the sole edge connecting the two disjoint components and occurs once. The two intervals and that singleton are consecutive and disjoint, and they exhaust [1,m] with multiplicity one. Every incidence is consumed, with unused label and difference inventories both empty.

## Physical return and termination

The joined tree connects two disjoint trees by one edge, so it is connected and acyclic. The two witnessed paths and the connector concatenate into the simple original path s:0–s:1–s:2–s:3. Each center is one edge from its designated spine section, and each terminal is two edges from the spine through its actual center, its only neighbor. These are also the shortest distances. The returned physical entrance and exit are L_B and U_A. Their labels are 3 and a+b+14=P+5 respectively. This proves the asserted state for both independently variable quotas, including a=b=2.

To supply it, check a,b are integers at least two, emit both original components by their finite indexed formulas, map A's section names, apply the translations once per vertex and emit the one cross-component incidence in its original position. The loops terminate after O(a+b) indexed operations and output records. No normalization or label choice depends on the existence of a solution on the joined tree. The returned offset five differs from the entrances three and four of D087 and D089, so these components do not directly continue this returned state under the stated R241 placement. The theorem addresses this four-section original.

## Boundary verification

At a=b=2 the graph has 24 vertices, 23 edges, cut 13 and physical spine labels (3,23,10,18). The actual connector has weight 13. The A internal spectrum is [1,12], and the shifted B internal spectrum is [14,23]. The four label bands are [0,5], [6,12], [13,18] and [19,23]. The boundary record verifies the exact named ledger and edge multiplicities. The interval and incidence argument above proves the quantified result.
