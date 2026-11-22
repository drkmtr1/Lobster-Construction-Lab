# B4-JOINT-23-MAX-ROOTED-CORE-001

## Named original and structural split

The exact original is `C(2,3)=[[2],[3],[],[2],[],[]]`.
It has six named spine vertices s:0 through s:5 and five
consecutive spine edges. The centers at sections 0, 1, 3
attach to s:0, s:1, s:3 respectively and carry 2, 3, 2
original terminals. No branch is present at section 2.
These are 16 vertices and 15 edges. The original spine
witnesses every center within one edge and every terminal
within two. Only physical s:2 is pinned, with label 15.

Weight 15 needs labels 15 and 0. The only original
neighbors of s:2 are s:1 and s:3, so one and only one is
zero. Weight 14 can use {0,14} or {1,15}; weight 13 can
use {0,13}, {1,14}, or {2,15}. In Case A (s:1=0), a
further zero edge is either s:1--s:0 or s:1--b:1:0,
and the other root neighbor is s:3. In Case B (s:3=0),
a further zero edge is either s:3--s:4 or s:3--b:3:0,
and the other root neighbor is s:1. There is no
orientation or ordering constraint on terminals and
no requirement to put 14 on the other root edge.

## Retained comparisons and a scoped Case A dead end

The accepted [C(2,2)](B4_JOINT_22_DIRECT_LEDGER.md)
uses s:3=0, s:1=1, s:0=13 and s:2=14. The original
edges s:2--s:3, s:2--s:1 and s:1--s:0 carry 14,13,12.
The first host 2 contributes 11,10,9 via its attachment
and two terminals; the second host 9 contributes 8,5,1
via its attachment and two terminals. The fourth host
6 contributes 6,3,4 and the right path contributes 7,2.
The accepted [C(3,2)](B4_JOINT_22_CUT_COMPAT.md)
preserves both second and fourth host ledgers and the
right path. The first host remains 2. Its attachment and
three terminal weights are 12,11,10,9, and the three high
spine weights increase to 15,14,13. The latter top three
and its first attachment and first two terminal weights
can guide C(2,3). The lower weights and the remaining
labels must be reallocated. The D059 second-host
failures on both fixed retained ledgers remain separate.
The [q-only](B4_Q1T2_K1_ROOTED_CORE.md) and
[r-only](B4_1R32_K1_ROOTED_CORE.md) cores supply different
first- or second-branch specializations when the other
branch has size one, with different numerical premises.

For Case A, test the partial allocation s:1=0, s:3=1,
s:4=14, s:5=2, b:3:0=3, and its two named terminals
13,12. Together with s:2=15 it uses weights
{2,9,10,12,13,14,15}. The left labels [4,11] and
remaining weights {1,3,4,5,6,7,8,11} must cover the
two left branches and s:0--s:1. Weight 11 must be
at a zero neighbor because any two remaining labels
differ by at most seven. If b:1:0=11 is chosen, weight
8 forces s:0=8 for the same reason. Choosing b:0:0=4
then consumes 4 on s:0--b:0:0, but makes pending
weight 7 impossible. Among the left labels only
{4,11} yields seven and these two centers are
nonadjacent. This rejects these stated choices and
leaves other Case A arrangements open. No complete
graph other than the declared core and two lifts is
introduced for this diagnostic.

## Independent Case B construction

Choose s:3=0 and s:1=1, giving 15 and 14 at the
root. Put s:0=14 for weight 13 and first host b:0:0=2
for weight 12. Its two prescribed terminals take 13,12
for weights 11,10. The labels [3,11] and weights [1,9]
remain for the second and fourth branches and s:4,s:5.
Use b:1:0=10, b:3:0=8, s:4=7, giving weights 9,8,7.
The free labels are {3,4,5,6,9,11}. Weight 6 is
now possible only at 10--4 among these terminal slots
and the s:4--s:5 slot. Choose the remaining second
terminals at 5 and 9 for weights 5 and 1. The fourth
terminals at 6 and 11 give 2 and 3, leaving s:5=3 for
weight 4. This allocates every remaining label and
weight by the original named edges. It uses no lifted
target or solver result.

| Named vertices in order | Labels | Differences on original edges in order |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | 14,1,15,0,7,3 | 13,14,15,7,4 |
| b:0:0,l:0:0:0,l:0:0:1 | 2,13,12 | 12,11,10 |
| b:1:0,l:1:0:0,l:1:0:1,l:1:0:2 | 10,4,5,9 | 9,6,5,1 |
| b:3:0,l:3:0:0,l:3:0:1 | 8,6,11 | 8,2,3 |

Branch differences start with the actual spine attachment
and then use terminals in the given name order. The
spine row uses consecutive original edges. The labels
are a bijection to [0,15] and the differences exhaust
[1,15] once. All named incidences and the spine witness
stay fixed. The physical maximum is s:2=15.

## Conditional lift, now supplied for fixed q=2,r=3

For every exact integer t>=1, translate the core values
by one. Add the original center b:2:0=0 and its actual
edge to s:2, and attach exactly the original names
l:2:0:j for 0<=j<t at b:2:0 with labels 17+j. The
target is `[[2],[3],[t],[2],[],[]]` with t+17 vertices
and maximum t+16. Label blocks {0}, [1,16],
[17,t+16] are distinct and exhaustive. Translation
preserves [1,15]. The original third attachment gives
16 because physical s:2 has label 16, and the terminal
edges give [17,t+16] at zero. Thus the actual weight
partition is [1,15], {16}, [17,t+16]. The old spine
witnesses the added center and terminals through their
prescribed named incidences.

Withhold only s:5. It has sole original neighbor s:4.
The actual label complement is R={4}, because the
translated s:5 is 4; the weight complement is D={4},
because f(s:4)=7 and f(s:5)=3 on the core. The physical
exit after translation is s:4=8. Assign s:5=4, using
both resources on the last original edge. This proof
covers all t>=1 at fixed q=2,r=3,K=1. The bounded
examples t=1 and t=2 corroborate it.

## Crossing interfaces on the supplied core

For each original edge, the row below gives all integer
cuts c with exactly one endpoint below c. These are
complete edge-incidence data for c=0..16, with empty
crossing sets at the endpoints.

| Physical edge | Weight | Cuts c |
|---|---:|---|
| b:1:0--l:1:0:2 | 1 | 10 |
| b:3:0--l:3:0:0 | 2 | 7..8 |
| b:3:0--l:3:0:1 | 3 | 9..11 |
| s:4--s:5 | 4 | 4..7 |
| b:1:0--l:1:0:1 | 5 | 6..10 |
| b:1:0--l:1:0:0 | 6 | 5..10 |
| s:3--s:4 | 7 | 1..7 |
| s:3--b:3:0 | 8 | 1..8 |
| s:1--b:1:0 | 9 | 2..10 |
| b:0:0--l:0:0:1 | 10 | 3..12 |
| b:0:0--l:0:0:0 | 11 | 3..13 |
| s:0--b:0:0 | 12 | 3..14 |
| s:0--s:1 | 13 | 2..14 |
| s:1--s:2 | 14 | 2..15 |
| s:2--s:3 | 15 | 1..15 |

By the [established cut criterion](B4_JOINT_22_CUT_COMPAT.md),
if a host label b is below the cut then d0=c-b;
otherwise d0=b-c+1. An insertion batch of positive size
is graceful exactly when the crossing spectrum is
[d0,15]. The [bounded audit](../evidence/validation/B4_JOINT_23_MAX_ROOTED_CORE_001/audit_result.json)
records every named crossing edge and both spectra for
both hosts. At b:0:0=2, the only matching cuts are
6,12,13,14 with tails [4,15], [10,15], [11,15], [12,15].
At b:1:0=10 there is no matching cut. For c=0,16 the
required tail is nonempty with no crossings. At c=1,2
weight 10 is missing. At c=3, c=4..6, and c=7..8 the
crossings include unwanted 7, 4, and 2 respectively.
At c=9,10,11,12,13,14,15 the missing weights
2,2,1,2,3,4,5 respectively already refute the tails.
This second-host rejection is confined to this fixed
C(2,3) ledger and the prescribed crossing-cut operation.

Cut 12 at the first host gives a verified repeatable
interface by the low-side part of the accepted rule.
For a batch h>=0, the four named original vertices
s:0,s:2,l:0:0:0,l:0:0:1 rise by h. Only those four
are at or above the updated cut 12+h. The fresh
first-terminal indices j=2,...,h+1 take labels 10+j.
Their host stays at 2, below the cut. The six old
crossings now use [10+h,15+h] and are exactly the
crossings at 12+h, since all new leaves are below it.
Thus the premise persists, and the same prescribed
name order gives pointwise agreement of successive
batches with the combined batch. The empty batch is
the original ledger. Physical s:2 carries 15+h, still
the maximum; the original s:4 and s:5 labels stay
7 and 3. The operation acts only at the first host
with r=3 fixed. No extra growth graph or generalized
lift was generated. The second-host spectrum does not
supply a repeatable r-transition or joint compatibility.

## Strategy and scope

This is a new independent finite seed and a proved
infinite t-lift for fixed q=2,r=3,K=1. The audited
first-center premise is an additional repeatable
instance of an accepted rule. The retained q-only,
r-only and r=2 families use their own named sources
and domains. There is no historical priority claim.
General C(2,r) supply, compatibility of both growth
directions and K>=2 remain open.

**CONTINUE** with one structural second-growth test.
A future rule registry can record the second proven
seed and the first-host interface without inventing
a new generic rule. A future coverage atlas can add
the precise fixed-seed lift. Any synthesis hypothesis
requiring unmodified first-/second-cut commutation
on these ledgers lacks a second-host transition.
Defer catalog promotion and any migration until
after the selected structural test. No catalog work
is part of this task.
