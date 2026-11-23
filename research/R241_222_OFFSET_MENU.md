# Physical R241 offset menu on original `[[2,2],[2]]`

[Evidence and reproduction](../evidence/validation/LCL_R241_222_OFFSET_MENU_001/README.md) · [D082 strict state](R241_222_STRICT_RETURN.md) · [Adopted R241](../references/upstream/mdl/N241_relational_ports.md)

## Exact physical domain

The retained D082 original has spine s:0–s:1, both named first centers b:0:0 and b:0:1 at s:0, and b:1:0 at s:1. Each center has its own terminal indices 0 and 1. This accounts for all 11 vertices and 10 edges. The spine edge is a witness from entrance to exit. The three centers and all six terminals lie respectively one and two edges from it.

The forced low class contains s:0, b:1:0 and the four first-section terminals. Its labels are 0 through 5. The high class consists of s:1, b:0:0, b:0:1 and the two second-section terminals, with labels 6 through 10. The cut is 6. Write `x=f(s:0)`, `e=f(s:1)=6+y`, `z=f(b:1:0)`, and let A and B be the values at the two respective first centers.

## Structural exclusions

Every alpha edge weighs high minus low. At degree one the high and low alphabet sums contribute `40-15=25`. The actual excess degrees above one are one at the high s:1, two each at the high first centers, and two each at the low s:0 and b:1:0. Thus gracefulness requires
```text
55 = 25 + e + 2(A+B-x-z) = 31 + y + 2(A+B-x-z).
```
All twelve pairs with odd y are excluded. For even y this forces `z=A+B-x-12+y/2`.

The remaining argument examines only the six unordered *numerical* center pairs available for each even y. This is a finite table of necessary incidence conditions. Each pair covers both orders on the two named centers. Each right terminal value pair also covers both named orders, because both terminals attach to z and both differences must occur. No terminal assignment is searched or quotiented. To see why each test applies, let `a<b` list the two candidate first-center values and let `c<d` be the two other high values after removing e, a and b. The actual spine, first attachments, right attachment and two right terminal edges give the six compulsory differences
```text
V = (e-x, a-x, b-x, e-z, c-z, d-z).
```
The four first terminal labels must be `Q=[0,5] minus {x,z}`. If z is unavailable, or if V repeats a value, the state is impossible. Otherwise the four left terminal weights must be the complement of V in [1,10]. For each such weight w, an actual first terminal would have to carry either a−w at the center labelled a or b−w at the center labelled b. When neither value belongs to Q, weight w is missing. This includes the extremal weights 1 and 10 whenever V has not already supplied them. The tests do not assume that their failure to exclude a pair supplies a labeling.

In each row below, the six columns refer to the following candidate pairs in order:

| y | Candidate numerical center pairs |
|---|---|
| 0 | (7,8), (7,9), (7,10), (8,9), (8,10), (9,10) |
| 2 | (6,7), (6,9), (6,10), (7,9), (7,10), (9,10) |
| 4 | (6,7), (6,8), (6,9), (7,8), (7,9), (8,9) |

`L` means z falls outside [0,5] or equals x. `Rw` means weight w repeats in V. `Mw` means w is missing from V and neither a−w nor b−w is in Q. `W` marks a candidate independently supplied below. Each entry follows by substituting in the displayed formulas. For example at (1,0) with a=8 and b=10, z=5 and V=(5,7,9,1,2,4). Weight 3 is missing, and its only possible terminal labels would be 5 and 7, neither in Q={0,2,3,4}. This also recovers the retained D082 obstruction without replaying its enumeration.

| (x,y) | Pair 1 | Pair 2 | Pair 3 | Pair 4 | Pair 5 | Pair 6 |
|---|---|---|---|---|---|---|
| (0, 0) | R6 | R6 | M2 | M3 | L | L |
| (0, 2) | R6 | R6 | M1 | M2 | L | L |
| (0, 4) | R7 | R6 | M1 | M2 | L | L |
| (1, 0) | R7 | R5 | R5 | M1 | M3 | L |
| (1, 2) | L | R5 | R5 | R6 | M2 | L |
| (1, 4) | R6 | R7 | M2 | R6 | M2 | L |
| (2, 0) | R5 | L | R5 | R4 | M1 | W |
| (2, 2) | M7 | L | R4 | R5 | R5 | L |
| (2, 4) | R8 | L | R7 | R6 | M1 | M3 |
| (3, 0) | M1 | M1 | R4 | R5 | L | R3 |
| (3, 2) | L | R6 | R5 | R6 | L | M4 |
| (3, 4) | W | M10 | R6 | R4 | L | R6 |
| (4, 0) | L | M1 | M1 | R5 | R4 | R5 |
| (4, 2) | L | M9 | R6 | R5 | R6 | L |
| (4, 4) | L | M8 | R6 | M1 | R6 | R4 |
| (5, 0) | L | L | M10 | M2 | R5 | R4 |
| (5, 2) | L | L | M10 | M1 | R5 | R5 |
| (5, 4) | L | L | M9 | M1 | R5 | R4 |

Every even-offset row except (2,0) and (3,4) consists entirely of contradictions. The table supplies 16 additional exclusions. Together with parity, this yields 28 exclusions in the exact prescribed orientation and physical port domain.

## Explicit named witnesses

For (2,0) take e=6, a=9, b=10, z=5, c=7 and d=8. V=(4,7,8,1,2,3), so the terminal weights remaining at the first centers are {5,6,9,10}. To supply 5 use the terminal labelled 4 at the center labelled 9. Weight 6 then uses 3 at that same center. Weight 10 uses 0 at the center labelled 10, and weight 9 there uses 1. The table supplies each named index explicitly.

The second ledger is the within-class reflection of the first. Replace each low t by 5−t and each high u by 16−u on the same named vertex. This preserves both alphabets and changes each weight d=u−t to 11−d. At the actual ports it sends (x,y) to (5−x,4−y), so (2,0) becomes (3,4). The exclusion table includes both pairs and every other ordered pair individually.

| Original vertex | (2,0) | (3,4) |
|---|---:|---:|
| `s:0` | 2 | 3 |
| `b:0:0` | 9 | 7 |
| `l:0:0:0` | 4 | 1 |
| `l:0:0:1` | 3 | 2 |
| `b:0:1` | 10 | 6 |
| `l:0:1:0` | 0 | 5 |
| `l:0:1:1` | 1 | 4 |
| `s:1` | 6 | 10 |
| `b:1:0` | 5 | 0 |
| `l:1:0:0` | 7 | 9 |
| `l:1:0:1` | 8 | 8 |

Both columns use 0 through 10 and cross cut 6 on every edge. In the retained original edge order, spine first and then the center attachment and terminal edges in section and branch order, the weights are:
```text
(2,0): 4, 7, 5, 6, 8, 10, 9, 1, 2, 3
(3,4): 7, 4, 6, 5, 3,  1, 2,10, 9, 8
```
Both lists contain exactly [1,10]. These two separate ledgers share the original graph digest but have different ledger IDs.

## The complete menu

W = WITNESSED, E = EXCLUDED, U = UNRESOLVED.

| Entrance x / exit y | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | E | E | E | E | E |
| 1 | E | E | E | E | E |
| 2 | W | E | E | E | E |
| 3 | E | E | E | E | W |
| 4 | E | E | E | E | E |
| 5 | E | E | E | E | E |

Totals are **2 WITNESSED, 28 EXCLUDED, 0 UNRESOLVED**. The result supplies normalized alpha gracefulness of this original at two exact port states.

## Conditional physical compatibility

The (2,0) ledger has actual labels s:0=2 and s:1=6. Its exit matches the entrance zero at actual s:0 of [D080's H(a)](R241_ZERO_TO_ONE_BRIDGE.md#independent-replacement-ha), for each a≥1, and of D080's finite (0,0) equal-one control. With the next two-section block occupying sections 2 and 3, the connecting original edge must be s:1–s:2. The D078 zero-offset starter uses its branch center as entrance. Offset equality there does not establish that same spine join.

The (3,4) ledger has actual labels s:0=3 and s:1=10. Its exit four fails the entrance zero required by H(a) and the entrance one required by the D078 paired blocks, D080 Q(a) and D081 F(b)/R(b,a). The adopted [R212-B.1 supplier in R241](../references/upstream/mdl/N241_relational_ports.md) does match four when u=5, at its designated actual entrance Z. This match requires the actual old-exit–Z connector and the R212 witness topology. The same supplier can provide predecessors with exit h=2 or h=3, matching the respective entrances of the two witnessed states. Also, D079's [audited (2,3) ledger](../evidence/validation/LCL_R241_TWO_CENTER_PORT_001/audit_result.json) on a different original has actual spine exit offset three, matching the (3,4) entrance. The two new ledgers by themselves have exit set {0,4} and entrance set {2,3}, so neither can directly precede either on the same R241 placement.

In every eligible conditional match, the adopted theorem still needs separately supplied disjoint blocks with the actual port-to-port edge in the target and their endpoint witnesses. For old block B and next block A, the four label bands are `[0,p_B-1]`, `[p_B,p_B+p_A-1]`, `[p_B+p_A,p_B+n_A-1]` and `[p_B+n_A,n_A+n_B-1]`. They partition the labels at cut p_B+p_A. The differences fall in `[1,n_A-1]`, the connector singleton `{n_A}`, and `[n_A+1,n_A+n_B-1]`. The actual connector weight is `n_A+y_B-x_A`, giving the requisite singleton when offsets match. Repetition would additionally need a proved sequence of returned offsets and exact original incidences. This menu records compatibility only. It adds no constructed join, repeat family or suffix supplier.
