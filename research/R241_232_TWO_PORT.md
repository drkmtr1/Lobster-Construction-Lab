# Two physical R241 states on original `[[2,3],[2]]`

[Evidence](../evidence/validation/LCL_R241_232_TWO_PORT_001/README.md) · [D084 predecessor](R241_222_OFFSET_MENU.md) · [Adopted R241](../references/upstream/mdl/N241_relational_ports.md)

## Original and signed sum

The exact original has spine s:0–s:1. Center b:0:0 attaches to s:0 and has two indexed terminals, b:0:1 attaches to s:0 and has three, and b:1:0 attaches to s:1 and has two. This accounts for 12 named vertices and 11 edges. The original spine edge witnesses each center at distance one and each terminal at distance two.

The orientation with s:0 low puts s:0, b:1:0 and the five first-section terminals in the low class, with labels [0,6]. The high class is s:1, b:0:0, b:0:1 and the two second-section terminals, with labels [7,11]. Write x for the entrance, e=7+y for the exit, A for the quota-two first center, B for the quota-three first center, and z for the second-section center. The actual nonterminal degrees in the order s:0, s:1, b:0:0, b:0:1, b:1:0 are 3, 2, 3, 4 and 3. The seven other degrees are one.

Every edge weighs high minus low. Summing at degree one for every vertex gives 45−21=24. The excess-degree contributions are e+2A+3B−2x−2z. Gracefulness therefore requires `66=31+y+2A+3B−2x−2z`, or `2A+3B−2z=35−y+2x`. The right side is 39 at (2,0) and 37 at (3,4). Both are odd, so B must be odd. The different coefficients distinguish the two first centers.

## Ordered center cases and residual inventories

For each state the four free high labels give 12 ordered choices (A,B) with A≠B. Let c,d be the two other free high labels, assigned to the right terminals in either order. The actual spine, the two first attachments, the right attachment and its two terminal edges force the differences
```text
V = (e−x, A−x, B−x, e−z, c−z, d−z).
```
A suitable z is forced by the signed sum and must be in [0,6] outside {x}. A repeat in V is a contradiction. With distinct V, let Q=[0,6] minus {x,z} and W=[1,11] minus the values in V. These are the actual label and weight inventories for the five left terminals. For every w in W at least one of A−w and B−w must lie in Q, since the only available left terminal edges are at those two centers. Both possible right-terminal orders give the same mandatory weights.

In the table P means parity fails, L means z is unavailable, Rw means weight w repeats on mandatory edges, and Mw means absent weight w has neither permitted terminal incidence. S marks a survivor requiring further construction. Every ordered center pair appears, with the original center identities fixed.

| (A,B) at (2,0) | z | Result | (A,B) at (3,4) | z | Result |
|---|---:|---|---|---:|---|
| (8, 9) | 2 | L | (7, 8) | — | P |
| (8, 10) | — | P | (7, 9) | 2 | R6 |
| (8, 11) | 5 | R5 | (7, 10) | — | P |
| (9, 8) | — | P | (8, 7) | 0 | S |
| (9, 10) | — | P | (8, 9) | 3 | L |
| (9, 11) | 6 | M3 | (8, 10) | — | P |
| (10, 8) | — | P | (9, 7) | 1 | M11 |
| (10, 9) | 4 | R7 | (9, 8) | — | P |
| (10, 11) | 7 | L | (9, 10) | — | P |
| (11, 8) | — | P | (10, 7) | 2 | R7 |
| (11, 9) | 5 | R5 | (10, 8) | — | P |
| (11, 10) | — | P | (10, 9) | 5 | R6 |

At (2,0) the nominal case (A,B,z)=(9,11,6) gives V=(5,7,9,1,2,4). Here Q={0,1,3,4,5} and W={3,6,8,10,11}. Weight 11 would require the zero leaf at B, but weight 3 already has no possible edge: A−3=6 is used at z, and B−3=8 is outside the low class. The other 11 ordered choices are excluded by parity, the low inventory or a repeated mandatory weight. Hence (2,0) is **EXCLUDED**.

At (3,4), the high exit is 11. Weight 11 must connect that actual exit to label zero. Its neighbors are s:0=3 and b:1:0, so z=0 is necessary. For example, (A,B,z)=(9,7,1) leaves weight 11 outside V and has no compatible terminal incidence. The sole survivor is (A,B,z)=(8,7,0). Its compulsory V is (8,5,4,11,9,10), giving Q={1,2,4,5,6} and W={1,2,3,6,7}. Weight 7 forces label 1 at center A. Weight 1 forces label 6 at center B. Weight 2 then uses label 5 at B, and weight 3 uses label 4 at B. The remaining weight 6 uses label 2 at A. Each center receives exactly its original quota.

Within-class reflection on this original would send low t to 6−t and high u to 18−u, hence (x,y) to (6−x,4−y). It does not relate the two prescribed pairs. The exclusion and witness here are independently derived.

## Explicit certificate and two-state disposition

| (x,y) | Physical port labels | Disposition |
|---|---|---|
| (2,0) | (2,7) | **EXCLUDED**, all 12 ordered center cases contradict necessary conditions |
| (3,4) | (3,11) | **WITNESSED**, explicit original ledger below |

| Actual vertex | Label |
|---|---:|
| `s:0` | 3 |
| `b:0:0` | 8 |
| `l:0:0:0` | 1 |
| `l:0:0:1` | 2 |
| `b:0:1` | 7 |
| `l:0:1:0` | 6 |
| `l:0:1:1` | 5 |
| `l:0:1:2` | 4 |
| `s:1` | 11 |
| `b:1:0` | 0 |
| `l:1:0:0` | 9 |
| `l:1:0:1` | 10 |

The named ledger assigns [0,6] and [7,11] once each to the prescribed classes. The differences in saved original edge order, with spine first then each attachment and its indexed terminals, are `8,5,7,6,4,1,2,3,11,9,10`. They exhaust [1,11]. The offsets on the actual spine edge are (3,4), so this independently supplies A(12,7;3,4) as a fixed module. The (2,0) exclusion concerns that exact orientation and prescribed ports. There is no unresolved state among the two examined pairs.

## Conditional port assessment

D080's H(a) takes entrance zero at its actual low spine vertex, so the witnessed exit four does not match. The prescribed exit-zero candidate (2,0) is excluded here. The retained [R212-B.1 module](../references/upstream/mdl/N241_relational_ports.md) has entrance u−1 at its designated vertex Z and can match exit four at u=5 if the target has that actual old-exit–Z connector and the retained witness topology. The D079 audited (2,3) ledger and the R212 module with h=3 have high exit offset three, matching the witnessed entrance at s:0 if the actual connector and both endpoint witnesses are present. The D084 (3,4) and D085 (3,4) states have the same offsets and cannot directly precede one another under this placement.

The adopted R241 rule demands old physical exit offset equal to new physical entrance offset on disjoint supplied components, with a single actual connector and a concatenable physical witness. Offset equality here records a possible input match. No join, macro, suffix or repeatable supplier is constructed.
