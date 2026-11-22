# B4-JOINT-MAX-ROOTED-CORE-PILOT-001

## Original and question

The frozen [named core](../evidence/validation/B4_JOINT_MAX_ROOTED_CORE_PILOT_001/validation/core_original.json)
has profile `[[2],[2],[],[2],[],[]]`. It has six named spine
vertices, consecutive edges s:0--s:1 through s:4--s:5,
and the original centers and two terminals at each of
sections 0, 1 and 3. Section 2 retains physical s:2 but
has no branch. This is a tree of order 15 with 14 edges.

The sole pin is f(s:2)=14. Gracefulness demands a
bijection to [0,14] and the complete original-edge
multiset [1,14]. For difference 14 the endpoints must
be labeled 0 and 14. Since only s:1 and s:3 neighbor
s:2, one of them must have label 0. This follows from
the required spectrum. The query leaves both cases open,
with no alpha condition, symmetry quotient or domains.

## Retained controls and exact one-cut transfer

The [q-only proof](B4_Q1T2_K1_ROOTED_CORE.md) supplies
`[[2],[1],[],[2],[],[]]`; the [r-only proof](B4_1R32_K1_ROOTED_CORE.md)
uses the retained `[[1],[2],[],[2],[],[]]` base. Both original
digests and ledgers were rechecked. Each has labels [0,13],
weights [1,13], and the maximum at original s:2. The
q-only core has zero at s:3 and its other insertion host
b:1:0=8. The r-only core has zero at s:1 and its other
insertion host b:0:0=4.

For a one-leaf insertion at host of label b, shift every
old label at least c by 1 and give the new physical leaf
label c. Both old ends of a noncrossing edge shift together
or stay fixed. Each crossing edge gains 1 in difference.
If the host is below c the new difference is d0=c-b,
using the ordinary arithmetic in the q-only proof. If
the host is at or above c the new difference is d0=b-c+1
by the [ordinary cut rule](ORDINARY_CUT_LEAF_INSERTION.md).
The labels still partition [0,14]. For the old spectrum
[1,13], write S(j)=1 for a crossing weight j and 0
otherwise, with S(0)=0. The resulting multiplicity of
each j in [1,13] is

```
1 - S(j) + S(j-1) + 1_(j=d0).
```

If graceful, this is 1 for every j, forcing the whole
crossing spectrum [d0,13] by upward induction. When
d0=14 that spectrum is empty. The converse follows
from the disjoint bands of unchanged old, new, and
shifted old differences. This proof applies to the
exact shift and inserted leaf at the named host.

The [control ledgers](../evidence/validation/B4_JOINT_MAX_ROOTED_CORE_PILOT_001/validation/controls.json)
give every complete crossing spectrum for c=1..13
and check the all-shift and no-shift endpoints c=0,14
as arithmetic comparisons. At an endpoint there are
no old crossings and the new edge would have to give
14. This would require b=13 at c=0 or b=0 at c=14,
neither of which holds at the two tested hosts. A c outside
[0,14] is an invalid fresh label. At c=14 the maximum
would be at the new leaf. Every proper cut shifts s:2
from 13 to 14, preserving the rooted condition. No cut
matches the required spectrum on either retained
ledger. For example, at c=4 the q-only host needs
[5,13] but the crossings include 4, and the r-only
host needs [1,13] but the crossings omit 2. These are
failed transfers of two specific ledgers. They do not
rule out other graceful labelings or imply a statement
about compatibility of growth operations.

## One bounded query and disposition

The original was frozen before calling the unchanged
production DFS once. One worker used a vertex cap of
15, 100,000 assignment nodes, and a cooperative six-second
time limit. The engine received only the pin s:2=14, an
empty explicit domain map, and count=False. It uses
minimum remaining values to choose visit order, and
prunes label reuse and already-closed edges whose
differences are zero, out of range or already present.
These are necessary constraints on any extension;
there is no code fixing one zero-neighbor branch.

**INCOMPLETE (max_nodes).** The run stopped at 100,000
nodes after 0.7740053000161424 seconds with witness=null,
exhausted=false, count=null, and count_lower_bound=0.
The named rooted feasibility question remains open.
The [raw receipt](../evidence/validation/B4_JOINT_MAX_ROOTED_CORE_PILOT_001/validation/raw_query.json)
and [independent audit](../evidence/validation/B4_JOINT_MAX_ROOTED_CORE_PILOT_001/audit_result.json)
bind the limits, original and source identities. There
was no retry, alternate query or historical replay.

## Conditional boundary

No joint core was supplied, so no completed t=2
original was constructed. The accepted maximum-rooted
lift remains conditional here: translation by one would
retain old weights [1,14], and a restored third zero
center would require the original s:2--b:2:0 attachment
of weight 15. The uninstantiated lift does not establish
the fixed q=r=2 family for any t. Repeatable first growth,
repeatable second growth and compatibility on a joint
seed remain unassessed. Joint supply at arbitrary q,r
and K>=2 continuation remain separate obligations.
