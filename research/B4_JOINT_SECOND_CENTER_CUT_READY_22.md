# B4-JOINT-SECOND-CENTER-CUT-READY-22-001

## Exact question and structural choices

The retained original is `C(2,2)=[[2],[2],[],[2],[],[]]`.
Its six physical spine vertices have five consecutive
edges. Centers at sections 0,1,3 attach to those exact
spine vertices and each carries its two named terminals.
The resulting tree has 15 vertices and 14 edges. Its
sole numerical pin is physical s:2=14. There is no
alpha, terminal-order or symmetry restriction.

The weight 14 must occur between s:2 and its sole
zero-labeled neighbor, either s:1 or s:3. Start by
trying to realize a cut c=13 with s:0=13 as the other
upper vertex. The two upper vertices are nonadjacent,
each of degree two. Thus exactly four original edges
cross, so the necessary tail is [11,14]. The second
host must have b=2 to give c-b=11. This is a derived
choice for this construction.

If s:3=0, the remaining two adjacent spine weights
are 14-s:1 and 13-s:1. With s:1=1 they are 13,12
and the attachment s:0--b:0:0 must supply 11,
requiring b:0:0=2 and colliding with b:1:0.
With s:1=2 it collides directly, and s:1>=3 would
give a crossing weight at most 10. Hence this
particular cut/upper-vertex plan fails on that
zero side. Other plans on the s:3=0 side remain open.

Choose s:1=0. Then its edges to s:2=14 and s:0=13
supply weights 14 and 13. The other two crossing
edges must give 11 and 12. Choose s:3=3 to give 11
and b:0:0=1 to give 12. The reversed assignment of
those weights would give s:3=2, already used by
b:1:0. This leaves b:1:0=2 as the physical low-side
insertion host.

## Independent lower-block completion

The four top weights and weight 2 at s:1--b:1:0
are now assigned. The free labels are [4,12].
Choose first terminals 11 and 8 at b:0:0=1 for
weights 10 and 7. Weight 9 must come from a right
attachment to s:3=3: the remaining free alphabet
is {4,5,6,7,9,10,12} of span eight, and the second
host 2 would need the already assigned 11. Choose
b:3:0=12 for that attachment and its first terminal 4
for weight 8. The unassigned labels are {5,6,7,9,10}
and the outstanding weights are {1,3,4,5,6}.

Label 10 cannot be a second terminal, a fourth
terminal, or s:4, as these give already used weights
8,2,7 respectively. Put it at s:5. Choose s:4=9
to supply 6 at s:3--s:4 and 1 at s:4--s:5.
The unassigned labels {5,6,7} now supply exactly
3 and 4 at the second host 2 and 5 at the fourth
host 12. The explicit ledger is therefore:

| Named vertices | Labels in order | Original differences in order |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | 13,0,14,3,9,10 | 13,14,11,6,1 |
| b:0:0,l:0:0:0,l:0:0:1 | 1,11,8 | 12,10,7 |
| b:1:0,l:1:0:0,l:1:0:1 | 2,5,6 | 2,3,4 |
| b:3:0,l:3:0:0,l:3:0:1 | 12,4,7 | 9,8,5 |

The spine weights follow the consecutive edges.
Each branch row lists its attachment weight, then
its terminal weights. The label and difference
multisets are exactly [0,14] and [1,14], with
the maximum at physical s:2. Every old named
incidence is used. The original spine witnesses
every center within one edge and each terminal
within two. This supplies an alternative ledger
with no solver result or completed lift as input.

## Complete second-host spectrum on this ledger

The [accepted ordinary criterion](B4_JOINT_22_CUT_COMPAT.md)
uses edges with exactly one endpoint below c. A
positive batch keeps noncrossing weights, shifts
crossing weights by h, and contributes a fresh
interval [d0,d0+h-1] at the host. The initial
difference is d0=c-b if b<c and d0=b-c+1 otherwise.
The old crossing spectrum must be exactly [d0,m].
The latter host side is the
[ordinary high-side lemma](ORDINARY_CUT_LEAF_INSERTION.md);
the new seed uses the low-side part of the criterion.

The edge of weight w crosses exactly when its
smaller label is below c and its larger label is at
least c. The rows below retain every named crossing
interval. The saved audit expands them to full
crossing edge ledgers and both difference spectra.

| Weight | Actual original edge | Cuts c |
|---:|---|---|
| 1 | s:4--s:5 | 10 |
| 2 | s:1--b:1:0 | 1..2 |
| 3 | b:1:0--l:1:0:0 | 3..5 |
| 4 | b:1:0--l:1:0:1 | 3..6 |
| 5 | b:3:0--l:3:0:1 | 8..12 |
| 6 | s:3--s:4 | 4..9 |
| 7 | b:0:0--l:0:0:1 | 2..8 |
| 8 | b:3:0--l:3:0:0 | 5..12 |
| 9 | s:3--b:3:0 | 4..12 |
| 10 | b:0:0--l:0:0:0 | 2..11 |
| 11 | s:2--s:3 | 4..14 |
| 12 | s:0--b:0:0 | 2..13 |
| 13 | s:0--s:1 | 1..13 |
| 14 | s:1--s:2 | 1..14 |

Since b:1:0=2, at c<=2 the required tail starts
at 3-c and at c>=3 it starts at c-2. The proper
cut c=13 matches exactly [11,14]. At c=1..7 a
required weight 3,1,1,2,5,5,5 respectively is
absent. At c=8..11 an extra weight 5,5,1,5
respectively crosses. At c=12 weight 10 is missing
and at c=14 weight 12 is missing. The full rows
are in the [independent audit](../evidence/validation/B4_JOINT_SECOND_CENTER_CUT_READY_22_001/audit_result.json).

At c=0 all old endpoints shift and no old edge
crosses. To append the entire fresh maximum
difference band there would require b=14, impossible
for this physical host with s:2=14. At c=15 no old
endpoint shifts and the matching condition would
require b=0. The host cannot be the zero vertex
since zero is at s:1 or s:3, and even if it were,
the new maximum would be on a fresh leaf, violating
the rooted requirement. Cuts outside 0..15 cannot
create the required label alphabet with this rule.

## Repeatable second growth at fixed q=2

For any exact integer h>=0 put r=h+2. At c=13
shift only s:0 and s:2 by h. The prescribed
additional terminals l:1:0:j, 2<=j<r, attach only
at b:1:0 and take labels 11+j. The exact core is
`C(2,r)=[[2],[r],[],[2],[],[]]`. The original
spine becomes r+11,0,r+12,3,9,10. The other original
labels stay in their displayed names, and the new
second terminals fill [13,r+10]. The fixed, fresh,
and shifted labels are [0,12], [13,r+10], and
[r+11,r+12]. The old noncrossings, fresh edges,
and shifted old crossings supply [1,10], [11,r+8],
and [r+9,r+12]. The new intervals are empty at r=2.
These partitions prove gracefulness for every r>=2.
Physical s:2 carries the maximum r+12.

The updated cut is c'=r+11 and the same two original
vertices are above or at it. Their four crossings
are [r+9,r+12], while the old and new terminals
are below c'. Its low host stays 2, so c'-2=r+9
and the complete crossing premise persists. A later
batch shifts the same two original vertices and
fills labels starting at c'. The fresh name with
index j still has label 11+j. Hence batches grouped
in the same terminal-name order agree pointwise.
All old branches and the spine remain fixed, and
new leaves lie two edges from the spine by their
original center. This construction does not need
the output at r=3 to coincide with the accepted
C(2,3) ledger.

## Original lift and actual resources

For every exact integer r>=2,t>=1, translate the
core by one and attach b:2:0=0 at original s:2.
Attach each prescribed l:2:0:j at b:2:0 for
0<=j<t with label r+14+j. The exact completed
target is `[[2],[r],[t],[2],[],[]]` with r+t+14
vertices and maximum r+t+13. The label intervals
are {0}, [1,r+13], and [r+14,r+t+13]. The weight
intervals are [1,r+12], {r+13} on the original
center attachment, and [r+14,r+t+13] on the fresh
terminal incidences. Both partitions are complete.
In particular the physical root's translated label
r+13 provides the new attachment weight.

Withhold physical s:5. The numerical exit at s:4
is 10. Since the translated s:5 label is 11 and
its only incidence is the edge from s:4, the actual
complements are R={11}, D={1}. Assign s:5=11,
consuming both on the original sole pending edge.
This establishes the K=1 family at fixed q=2.
No K>=2 or simultaneous joint growth follows.

## Direct corollary on the retained r=3 family

The [independent Case B C(2,3) seed and c=12 proof](B4_JOINT_23_MAX_ROOTED_CORE.md)
give first growth for h=q-2, q>=2. Their maximum
at s:2 is 15+h=q+13, while s:4=7 and s:5=3 stay.
Translation by one and restoring zero at b:2:0
give labels {0}, [1,q+14], [q+15,q+t+14].
Old differences [1,q+13] are preserved, the
actual attachment gives q+14, and zero-host
leaves give [q+15,q+t+14]. Thus
`[[q],[3],[t],[2],[],[]]` is gracefully supplied
for all integers q>=2,t>=1,K=1. With only s:5
missing the boundary is R=D={4} at s:4=8.
This accepts the symbolic composition without
a new experiment. It uses the earlier r=3
first-growth ledger, separate from this task's
second-growth ledger.

## Strategy

**ADVANCE** a narrow, read-only Construction Synthesis
pilot as the next proposed bounded action. The
mathematical advance supplies an independently verified
second-center transition and a new all-r,t K=1 slice.
The verified first- and second-growth directions use
different named ledgers, so a pilot can distinguish
their premises and register the exact proved coverage.
Commutation, a shared transition state, and simultaneous
q>=3,r>=4 supply remain open. A focused inventory has
priority over another generalization test at this point.
No catalog migration or successor was started.

[Evidence](../evidence/validation/B4_JOINT_SECOND_CENTER_CUT_READY_22_001/README.md) records the retained
C(2,2), C(2,3) controls and D059 adverse interface,
two new originals, and one deliberately wrong digest.
The bounded checks use zero DFS queries.
