# B4-JOINT-22-DIRECT-LEDGER-001

## Original and necessary constraints

On the exact named `[[2],[2],[],[2],[],[]]` core, the spine
has six vertices and five edges. At sections 0, 1 and 3
the original branch adds a center, an attachment to the
spine, two terminals and their two edges to the center.
There is no branch at section 2. Thus there are 15 vertices
and 14 edges. The desired maximum is physical s:2=14.
The edge of weight 14 has endpoints labeled 0 and 14.
The only s:2 neighbors are s:1 and s:3, so exactly one
carries zero. This exhausts the structural split.

For difference 13 the only unordered label pairs are
{0,13} and {1,14}. For 12 they are {0,12}, {1,13}, and
{2,14}. Hence once the root edge of weight 14 is used:

- In Case A, with s:1=0, a remaining zero-edge of weight
  13 or 12 must lie on s:1--s:0 or s:1--b:1:0. A root
  edge of weight 13 or 12 on the other side needs s:3=1
  or s:3=2 respectively.
- In Case B, with s:3=0, a remaining zero-edge of weight
  13 or 12 must lie on s:3--s:4 or s:3--b:3:0. A root
  edge of weight 13 or 12 on the other side needs s:1=1
  or s:1=2 respectively.
- In either case the option {1,13} for weight 12 must
  lie on an original edge. For example, if the other
  root neighbor is assigned 1, its nonroot neighbors
  are the only possible sites for its partner 13.
  In Case A they are s:4 and b:3:0. In Case B they
  are s:0 and b:1:0.

These constraints leave options for weight 13 at zero
as well as at the root. The two constructions below each
choose the root option. This choice is local to the ledger.
No alpha restriction or terminal sorting is used.

## Two direct candidate ledgers

Retained [q-only](B4_Q1T2_K1_ROOTED_CORE.md) and
[r-only](B4_1R32_K1_ROOTED_CORE.md) cores were independently
rechecked as ordinary graceful on their original 14 vertices,
with maximum 13 at s:2. Their [already rejected fixed-ledger
transfers](B4_JOINT_MAX_ROOTED_CORE_PILOT.md) remain separate.
These candidates assign the two centers and their terminal
weights jointly. They use no completed lift and no query.

### Case A, zero at s:1

Choose s:3=1 for weight 13, s:4=13 for 12, and s:5=2
for 11. Set b:3:0=3 with its two named terminals at 12
and 11 to supply weights 2,9,8 on that branch. This uses
weights {2,8,9,11,12,13,14}. Remaining labels are [4,10]
and remaining weights are {1,3,4,5,6,7,10} on the two
left branches and s:0--s:1. Choose b:1:0=10 and s:0=7
for their zero edges, and b:0:0=4 for weight 3 to s:0.
The remaining labels are {5,6,8,9}; put 5 and 9 at
the first two terminals to get 1 and 5, then 6 and 8
at the second two to get 4 and 2. This complete
candidate is falsified. The two branches demand weight
6, which could only be achieved by a terminal labeled
10 at center 4 or by a terminal labeled 4 at center
10 within the remaining alphabet. Both labels are
already centers. Weight 6 is missing and 2 occurs twice.
This disposition concerns the displayed joint choices.

### Case B, zero at s:3

Choose s:1=1 for weight 13 and s:0=13 for 12 on
s:0--s:1. Set b:0:0=2 for weight 11 and give its
prescribed terminals labels 12 and 11 for weights 10
and 9. This consumes [9,14], leaving labels [3,10]
and weights [1,8]. The remaining three attachments
are b:1:0 to s:1=1, b:3:0 to s:3=0 and s:4 to
s:3=0. Assign their weights 8,6,7 by choosing
b:1:0=9, b:3:0=6 and s:4=7. The only remaining
way to realize weight 5 is 9--4 at the second host.
Finish its other terminal with label 8 for weight 1.
The remaining labels {3,5,10} then supply weights
3 and 4 as terminals 3 and 10 at the fourth host 6,
and 2 by s:5=5 at s:4=7. This assigns each
actual vertex and consumes the entire weight inventory.

### Complete named inventories

Triples in a branch row list the center and terminals
in physical name order. Its weights list the original spine
attachment, then the two exact terminal edges in that order.
The spine row lists consecutive original edges.

| Named vertices | A labels | A weights | B labels | B weights |
|---|---|---|---|---|
| s:0, s:1, s:2, s:3, s:4, s:5 | 7,0,14,1,13,2 | 7,14,13,12,11 | 13,1,14,0,7,5 | 12,13,14,7,2 |
| b:0:0, l:0:0:0, l:0:0:1 | 4,5,9 | 3,1,5 | 2,12,11 | 11,10,9 |
| b:1:0, l:1:0:0, l:1:0:1 | 10,6,8 | 10,4,2 | 9,4,8 | 8,5,1 |
| b:3:0, l:3:0:0, l:3:0:1 | 3,12,11 | 2,9,8 | 6,3,10 | 6,3,4 |

Both use every label in [0,14] once, so neither leaves an
unused label. Both put 14 at physical s:2. A uses each
weight in [1,5] and [7,14], with a second copy of weight
2. The first repeated weight in the displayed edge order
occurs at s:3--b:3:0. Unused weights are {6}. B uses
[1,14] once each and leaves no unused weight. This directly
supplies the fixed core. The bounded Case A failure
establishes no obstruction to other labelings in that case.

## All-positive-t lift at fixed q=r=2, K=1

Use only verified Case B. For each exact integer t>=1
translate every core label by one. Add original b:2:0=0
with its original attachment to physical s:2. Add the
t original l:2:0:j at b:2:0 with labels 16+j, for
0<=j<t. Translation leaves every old difference unchanged.
Only the third attachment and those t terminal edges are
new. Each new leaf has precisely its named incidence, and
the new center connects the restored branch to the same
original tree. There are t+16 vertices and t+15 edges.

The labels partition as {0}, [1,15], [16,t+15] and the
differences as [1,14], {15}, [16,t+15]. The single
difference 15 comes from the translated physical
s:2=15 meeting b:2:0=0. The remaining new edge weights
equal their terminal labels at host zero. Both disjoint
partitions exhaust their alphabets and include t=1.
The original spine remains a witness: every center
is one edge from it and every terminal is two edges away.

Withhold only physical s:5 from this formula. The sole
pending edge is the original s:4--s:5. The completed label
inventory loses exactly R={f(s:5)+1}={6} and the completed
weight inventory loses D={|f(s:4)-f(s:5)|}={2}. At physical
s:4 the prefix has g(s:4)=8. Assign s:5=6 to consume the
remaining label and difference 2 without changing any
prefix label. This is the direct K=1 boundary for these
fixed q=r=2 targets. Joint supply at arbitrary q,r and
K>=2 continuation remain separate.

## Bounded evidence and disposition

[Evidence](../evidence/validation/B4_JOINT_22_DIRECT_LEDGER_001/README.md) binds the two candidates to
the same separately frozen 15-vertex original. The unchanged
checker rejects A, accepts B, and rejects B with a deliberately
wrong expected digest. A separate arithmetic audit reconstructs
all named graphs and ledgers. The only new completed graph is
t=2 of order 18. The earlier DFS receipt remains INCOMPLETE
as a historical run. This construction makes zero solver
queries and uses zero labeling-enumeration nodes.
