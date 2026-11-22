# B4-THIRD-ZERO-HOST-K1-001

## Complete original and one derived control

The exact original `[[1],[1],[2],[2],[],[]]` has physical spine
s:0 through s:5, four original branch centers and six original
terminal leaves. The five original spine edges, four attachments,
and six terminal edges give 16 named vertices and 15 edges.
Its complete graph digest is
`fce6e5676ab825e344c5f217ace9855e4f1e5dc4c88f8a71e9563093daae1a9c`.

The [retained adjacent certificate](../evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1122-adjacent.json)
is the 15-vertex prefix with digest
`a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc`.
On that prefix raise every label at or above 7 by one and keep
all labels below 7. The original prefix edges cross its alpha cut,
so their differences rise from 1..14 to 2..15. The original final
spine edge has labels s:4=8 and s:5=7, yielding difference 1.
Thus the following newly derived complete control has labels 0..15
and original differences 1..15, each once. In the branch rows the
differences are in attachment-then-terminal order.

| Named vertices in order | Labels | Original-edge differences |
|---|---|---|
| s:0, s:1, s:2, s:3, s:4, s:5 | 15,0,10,6,8,7 | 15,10,4,2,1 |
| b:0:0, l:0:0:0 | 1,14 | 14,13 |
| b:1:0, l:1:0:0 | 12,5 | 12,7 |
| b:2:0, l:2:0:0, l:2:0:1 | 2,11,13 | 8,9,11 |
| b:3:0, l:3:0:0, l:3:0:1 | 9,3,4 | 3,6,5 |

Its b:2:0=2 fails the new host pin. This is one derived certificate
on the exact complete original. It establishes ordinary gracefulness
of that finite target using a different host label. The historical
search was not replayed.

## Sole query and disposition

The unchanged DFS took only the pin b:2:0=0 and an empty
explicit domain map. The effective domain at that host was {0}
and all other effective domains were 0..15. The query scope was
restricted by this single pin. It used neither alpha restrictions
nor any root, exit, final-label, final-difference, terminal-order,
automorphism or complement restriction.

The one execution used first-witness mode, one worker, at most
16 vertices, 100,000 assignment nodes, five cooperative seconds,
and 2,000,000 bytes per result. The generic max_states field is
20,000 and unused by DFS. The original and domain expansion,
source, runtime, schema checks and conditional growth plan were
frozen before search.

The [original-bound query](../evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json)
returned INCOMPLETE with reason max_nodes after 100,000 assignment
nodes in 0.8123459999915212 seconds. It reports exhausted=false,
count=null, count_lower_bound=0 and no witness. The zero lower bound
does not decide feasibility. The restriction thus remains open.
The query supplied no zero-host seed or singleton outputs, so the
conditional growth branch and both direct checks were inapplicable.
The retained [t=1 adjacent supplier](B4_FOURTH_2_SUPPLY.md) and
[t>=2,K>=2 nonadjacent supplier](B4_THIRD_ZERO_HOST_NONADJACENT.md)
retain their exact domains. No combined all-positive-t,K theorem
follows from this task.

## Conditional ordinary zero-host extension

Suppose a gracefully labeled named tree of order n has an
actual prescribed host z with label zero. Attach h pairwise
distinct fresh named leaves at z for integer h>=0, keeping
all old vertices, incidences and labels. Each new vertex has
one edge to z, preserving connectedness and acyclicity.
Give leaf i, for 1<=i<=h, label n+i-1. The old and new labels
occupy the disjoint consecutive bands [0,n-1] and [n,n+h-1].
The old differences stay [1,n-1], and the new edge incident
to leaf i has difference n+i-1 because its other endpoint
has label zero. Thus the full original spectrum becomes
[1,n+h-1], each once. This ordinary argument requires no alpha
threshold, port, or witness data. The arithmetic is shared by
the [alpha zero-host result](ALPHA_ZERO_HOST_LEAF_EXTENSION.md),
whose alpha and witness conclusions require its own hypotheses.

The host label stays zero. After k additions the graph has
order n+k, so the next fresh leaf receives n+k. This gives
finite closure and exactly h additions, with h=0 the identity.
If a first batch has h_1 leaves, the j-th leaf of the next
batch receives n+h_1+j-1, its label in the concatenated batch.
All first-batch labels remain, proving pointwise agreement.

For the stated K=1 family, *if* a complete 16-vertex seed
with b:2:0=0 is supplied, add t-2 named leaves l:2:0:j,
2<=j<t, at that original host with labels 14+j. The first
fresh label is 16, and the fresh band 16..t+13 is empty at
t=2. The resulting original is exactly `[[1],[1],[t],[2],[],[]]`
of order t+14 and size t+13. The old complete labels and
edge differences together with the fresh band give precisely
0..t+13 and 1..t+13. The old spine remains within two edges of
every vertex, including each added leaf through the third
center. In particular, after k additions the next label is
16+k.

For such a seed g let a=g(s:5), u=g(s:4), d=|u-a|.
Removing the assignment at s:5 from the grown labeling leaves
used labels [0,t+13] minus {a} and used differences [1,t+13]
minus {d}. The only unfinished incidence is the actual edge
s:4--s:5. The returned singleton would be R={a}, D={d},
physical s:4=u, and assigning s:5=a consumes both resources.
This arithmetic permits d to be the actual edge difference
and needs no interval predicate, shift or recurrence. The
current incomplete query leaves these values undetermined.

[Saved evidence](../evidence/validation/B4_THIRD_ZERO_HOST_K1_001/README.md)
