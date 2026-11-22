# B4-JOINT-NESTED-CUT-TWO-HOST-001

## Exact original and initial crossings

Use the unchanged D061 alternative ledger on the
[immutable named C(2,2) original](../evidence/validation/B4_JOINT_22_DIRECT_LEDGER_001/validation/core_original.json)
and its [certificate](../evidence/validation/B4_JOINT_SECOND_CENTER_CUT_READY_22_001/validation/alternative-r2.json).
The seed f0 has six original spine vertices with labels
13,0,14,3,9,10 at s:0 through s:5. In center, first
terminal, second terminal order the three branches at
sections 0,1,3 have labels (1,11,8), (2,5,6), (12,4,7).
There is no branch at section 2. The labels are [0,14]
once each. The spine is an actual witness: each center
is one edge away and each terminal two edges away.

Divide the named original vertices by seed label:
low [0,6], middle [7,12], high [13,14]. These blocks
describe shifts and do not assert an alpha cut.
The table checks every original edge and its weight.
Each edge crosses a threshold when its smaller label
is below the threshold and its larger label is at least
the threshold.

| Original edge | Seed weight | Endpoint blocks |
|---|---:|---|
| s:4--s:5 | 1 | middle, middle |
| s:1--b:1:0 | 2 | low, low |
| b:1:0--l:1:0:0 | 3 | low, low |
| b:1:0--l:1:0:1 | 4 | low, low |
| b:3:0--l:3:0:1 | 5 | middle, middle |
| s:3--s:4 | 6 | low, middle |
| b:0:0--l:0:0:1 | 7 | low, middle |
| b:3:0--l:3:0:0 | 8 | middle, low |
| s:3--b:3:0 | 9 | low, middle |
| b:0:0--l:0:0:0 | 10 | low, middle |
| s:2--s:3 | 11 | high, low |
| s:0--b:0:0 | 12 | high, low |
| s:0--s:1 | 13 | high, low |
| s:1--s:2 | 14 | low, high |

The [accepted low-host cut rule](B4_JOINT_22_CUT_COMPAT.md#named-seed-and-the-complete-cut-condition)
starts fresh differences at c minus the actual host label.
At c1=7 the physical first host b:0:0=1 needs [6,14].
The low-to-middle and low-to-high edges give this exact
tail. At c2=13 the physical second host b:1:0=2 needs
[11,14], realized by precisely the low-to-high edges.
This independently rechecks both initial cut hypotheses.
In particular no old edge joins middle and high.
Counting every incidence to an upper vertex would include
same-side edges at the first cut, such as s:4--s:5.

## Two batches and the complete named spectrum

Fix exact integers q,r>=2, let h=q-2, k=r-2 and
m=q+r+10=14+h+k. Retain all old incidences and
attach only l:0:0:j for 2<=j<q at b:0:0 and
l:1:0:j for 2<=j<r at b:1:0. This is the exact
named original C(q,r)=[[q],[r],[],[2],[],[]].
There are 15+h+k vertices and 14+h+k edges.
Adding each leaf keeps the graph a tree and preserves
the same physical spine witness.

For old v set
`f(v)=f0(v)+h*I[f0(v)>=7]+k*I[f0(v)>=13]`.
Assign fresh first terminal j value j+5 and fresh
second terminal j value h+11+j. Each band is filled
once, with an inverted interval denoting the empty
set:

| Named vertex group | Resulting labels |
|---|---|
| Old low | [0,6] |
| Fresh first terminals | [7,6+h] |
| Old middle | [7+h,12+h] |
| Fresh second terminals | [13+h,12+h+k] |
| Old high | [13+h+k,14+h+k] |

These bands partition [0,m]. The physical s:2 was
the unique old vertex with label 14, so it keeps
the maximum at m. Both insertion hosts stay low
with labels 1 and 2.

For edges with both ends in one old block, the
increments cancel. A low-to-middle edge gains h
because only the larger endpoint shifts. A
low-to-high edge gains h+k for the same reason.
The new terminals each have just their prescribed
host edge. This proves the complete actual-edge
partition:

| Named edge group | Resulting weights |
|---|---|
| Old same-block edges (seed weights 1..5) | [1,5] |
| Fresh first-terminal edges | [6,5+h] |
| Old low-to-middle edges (seed weights 6..10) | [6+h,10+h] |
| Fresh second-terminal edges | [11+h,10+h+k] |
| Old low-to-high edges (seed weights 11..14) | [11+h+k,14+h+k] |

In particular q=2 or r=2 has the appropriate empty
fresh band, and h=k=0 recovers the seed. These
arguments prove gracefulness without alpha separation.

## Returned cuts and finite interleavings

After h first and k second additions, set a=7+h
and b=13+h+k. The current vertex blocks are determined
by these cuts and the label table. The first cut a
is crossed by the old low-to-middle edges, the old
low-to-high edges, and the fresh second-terminal
edges. Fresh first-terminal edges stay below it.
Thus the weights crossing a are exactly [6+h,m],
which is [a-1,m] for the physical first host 1.
At b only the two original high vertices are upper.
The only crossings are the four old low-to-high
edges, with weights [11+h+k,m]=[b-2,m]. The second
host 2 meets its full premise. The cut identities
continue to hold even if a fresh band is empty.

Starting at any such (h,k), a further first batch
of size u shifts exactly old middle, old high, and
the already present second terminals. The host-1
new names with global indices j=h+2 through h+u+1
receive labels j+5 by filling from a. All earlier
first terminals remain fixed. Both cuts advance by
u and the expression becomes the claimed state at
(h+u,k).

A further second batch of size v shifts exactly
the original high vertices. Earlier first and second
terminals stay fixed. Its new names j=k+2 through
k+v+1 receive h+11+j by filling from b. Only the
second cut advances, by v, and the expression becomes
the claimed state at (h,k+v). In either operation
the full required crossing tail has already been proved
at the current state. An empty batch is the identity.

Induct on any finite sequence of these batches, keeping
the same terminal-name order separately at each host.
After each step the labels depend only on the two
counts and named indices. In particular growing first
then second agrees pointwise with growing second then
first. In the latter order, first growth raises the
already created second-terminal labels by exactly the
amount that is built into their formula in the former
order. This is a simultaneous repeatable interface
for the exact supplied ledger, including cross-host
interleavings, and uses no additional graph assumptions.

## Exact K=1 zero-host lift

For every exact integer t>=1 translate the core by
one. Restore b:2:0=0 at the actual missing branch
and attach it to original s:2. Give l:2:0:j the
label m+2+j for 0<=j<t, with each named terminal
attached only at b:2:0. The exact full target is
`[[q],[r],[t],[2],[],[]]` with q+r+t+12 vertices
and M=m+t+1 edges. Label bands {0}, [1,m+1],
[m+2,M] are complete. Translation keeps old weights
[1,m], the restored s:2--b:2:0 gives m+1, and the
terminal edges at zero give [m+2,M]. This proves
ordinary gracefulness and preserves original incidences
and the spine witness.

To obtain the prefix, omit only s:5. Core values
at s:4 and s:5 are 9+h and 10+h, so their translated
values are q+8 and q+9. The only pending edge is the
original s:4--s:5. The actual complements are
R={q+9} and D={1}, with physical s:4=q+8. Assigning
s:5=q+9 consumes those resources, with every earlier
label unchanged.

The proof gives all positive t and q,r>=2 for K=1.
The retained [q=1 family](B4_1RT2_K1_DIRECT_SINGLETON.md#selection-for-all-positive-rtk)
and [r=1 family](B4_Q1T2_K1_ROOTED_CORE.md#family-coverage-and-validation-scope)
cover their own remaining positive parameters at K=1
and K>=2. Thus the exact ordered four-branch K=1 family
with fourth size two is covered for all positive q,r,t
by selection among these proofs. The retained
[t=1 family](B4_UNPADDED_QR12.md#original-completion-for-all-qrk1)
also covers all positive q,r,K. For K>=2 those retained
results still handle q=1, r=1, or t=1. This new singleton
argument supplies no K>=2 continuation with q,r,t>=2.
No historical priority or arbitrary lobster theorem is
claimed.

## Bounded evidence and strategy

The [evidence](../evidence/validation/B4_JOINT_NESTED_CUT_TWO_HOST_001/README.md) checks only C(3,4)
and its t=1 original as new graph records. It rechecks the
D061 and D060 positive originals and binds the D059
fixed-ledger negative without replay. That negative was
on different named label ledgers and remains valid.
The quantified result follows from the partitions and
returned-cut invariant above.

The authorized interim strategy deferred cataloging for
this proof. The accepted same-ledger interaction is now
a concrete catalog entry with actual premises, an
independent supplier and exact K=1 coverage. The proposed
next action is a read-only catalog pilot. No catalog
migration or successor was executed.
