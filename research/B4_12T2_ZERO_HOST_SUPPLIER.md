# B4-12T2-ZERO-HOST-SUPPLIER-001

## Original seed and direct ledger

The seed has exact ordered profile `[[1],[2],[3],[2],[]]`.
The five vertices s:0 through s:4 have four consecutive
spine edges. At each i=0,1,2,3 the original center b:i:0
attaches to s:i, and its l:i:0:j attach to that center in
counts 1,2,3,2. This accounts for 17 vertices and 16
original edges. With physical s:4 high, the bipartition
has lows s:1,s:3,b:0:0,b:2:0 and the four second and fourth
terminals. The other nine vertices are high.

Supply the largest four labels at the neighbors of the
zero host b:2:0: put 16 at s:2 and 13,14,15 on the three
third terminals. Their respective edges give 16,13,14,15.
Choose the nonadjacent normalized exit s:4=9. Give its
neighbor s:3 label 4 and s:1 label 7 to obtain weights
5,12,9 on s:3--s:4, s:2--s:3, s:1--s:2. Set the second
center to 8 at its neighbor s:1=7, and give its terminals
6 and 5 for weights 1,2,3 in attachment-then-terminal
order. Put 11 at s:0 and use the first center at 1 with
terminal 12, giving weights 4 on the first spine edge
and 10,11 on that branch. The remaining high 10 on the
fourth center and lows 2,3 on its leaves give 6,8,7.
These choices assign a fully checked ledger on the exact
named seed by arithmetic alone.

| Original vertices in order | Seed labels | Original edge differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 11,7,16,4,9 | 4,9,12,5 |
| b:0:0,l:0:0:0 | 1,12 | 10,11 |
| b:1:0,l:1:0:0,l:1:0:1 | 8,6,5 | 1,2,3 |
| b:2:0,l:2:0:0,l:2:0:1,l:2:0:2 | 0,13,14,15 | 16,13,14,15 |
| b:3:0,l:3:0:0,l:3:0:1 | 10,2,3 | 6,8,7 |

The rows list the consecutive spine weights and then
the attachment and terminal weights at each branch. The
eight low values are 0..7 once and the nine high values
are 8..16 once. These are the exact bipartition classes
above. Every original edge crosses the cut and the listed
weights use 1..16 exactly once. This verifies the alpha
seed, independently of any solver result.

Take L=b:0:0=1, U=s:4=9 and Z=b:2:0=0. The actual path
W=b:0:0--s:0--s:1--s:2--s:3--s:4 is present. The first
terminal lies one edge off W. Each other center is one
edge off W with all its leaves two edges away. In
particular Z is one edge away through s:2. The result is
A(17,8;1,1) with distinct physical L, U and Z. Label 1
at L is a returned value of the exhibited ledger.

## Restricted comparison with the retained r=2 ledger

The [retained normalized r=2 certificate](../evidence/validation/B4_UNPADDED_1R22_SUPPLIER_001/validation/normalized-r2.json)
uses the exact 16-vertex `[[1],[2],[2],[2],[]]` prefix.
It has low size 8, Z=b:2:0=3 and U=s:4=9. This is the
sole retained certificate rechecked in the new campaign.

For the [general-host upper-block rule](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
with this host and this retained exit fixed, the threshold
c is 10,...,15. Every selected high contributes its
degree to the distinct incident-edge count, since all
original edges cross the cut. In descending label order
the selected highs from 15 down to 10 are b:1:0, s:0,
s:2, l:2:0:1, l:0:0:0, l:2:0:0 with degrees 3,2,3,1,1,1.

| c | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---:|---:|---:|---:|---:|---:|
| Actual incident count | 11 | 10 | 9 | 8 | 5 | 3 |
| Required count 19-c from [c-3,15] | 9 | 8 | 7 | 6 | 5 | 4 |

At c=14 the only selected highs are physical s:0=14 and
b:1:0=15. Their neighbors are s:1=2 and b:0:0=6 for s:0,
and s:1=2 and the second terminals 0,1 for b:1:0.
The five differences are 12,8,13,15,14, rather than
the required [11,15]. The full premise therefore fails
at every allowed cut for this one fixed ledger, host
and port-preserving insertion. It has no implication
for other labelings or ordinary gracefulness.

## All-t normalized extension

Let t>=3 be an exact integer. Apply the retained
[zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
to the newly supplied state, with h=t-3 fresh leaves
l:2:0:j for 3<=j<t and their only new edges at Z. The
base supplies zero at Z, distance one to W, and an
alpha labeling with physical ports as required by that
lemma. Keep all seed labels and assign j+14 to each
fresh leaf in increasing name-index order. These leaves
have labels [17,t+13], and their differences equal their
labels at the unchanged zero host. All seed labels
[0,16] and all seed differences [1,16] remain.
Thus labels [0,t+13] and differences [1,t+13] each
occur once. Each fresh vertex is high adjacent to Z
in the same low class of size 8, two edges from W.
The exact normalized profile is `[[1],[2],[t],[2],[]]`
and its state is A(t+14,8;1,1) with the same Z, L, U
and W. Added leaves preserve every existing edge,
connectivity and acyclicity.

At t=3 the new band is empty and the operation is the
identity. After any finite batch the same host and all
premises persist; at current order t+14, the next leaf
of index t gets the next label t+14. An earlier batch
leaves all its entries fixed, and a later batch assigns
the same next labels in the same order as one combined
batch. Repeating this argument gives named pointwise
agreement for any finite partition of t-3 additions.
There is no dependence on a new seed at larger t.

## High shift and original path

For exact integers t>=3, K>=2, the full original
`[[1],[2],[t],[2]]+[[]]*(K+1)` has K+t+14 vertices and
m=K+t+13 edges. Raise every high label by K. The prefix
label set becomes [0,7] union [K+8,m]. Each prefix edge
crosses the normalized cut, so its difference rises by
K and the prefix differences are [K+1,m] once each.
The actual inventories are R=[8,K+7], D=[1,K], at
physical s:4=K+9. Every prefix vertex and original
prefix edge retains its named incidence. All empty
suffix sections after s:4 contain no branches, so the
only unassigned vertices are s:5 through s:(K+4).
Their exact incidences are the original consecutive
K-edge path from s:4 with sole crossing s:4--s:5.

For comparison the [adjacent formula](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
would require existing port 8+K and use alternating
interval ends. The supplied y=1 gives port 9+K.
Use [the nonadjacent numeric recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof)
C_2=(3,1,0), C_3=(4,1,0,2), C_4=(5,1,2,0,3).
For K>=5, write C_(K-3)=(K-2,x_1,...,x_(K-3)). Then
C_K=(K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3)).
The three bases have suffix entries 0..K-1 and
differences 1..K. Inductively the reflected values
fill [2,K-2], complementary to the other three suffix
entries 1,K-1,0. Reflection of the old path beginning
at K-2 includes the bridge from the new 0 and preserves
weights [1,K-3]. The preceding three new weights are
K,K-2,K-1. Decreasing K by three terminates at a base.

Translate by 8. The first entry is exactly the
already assigned s:4, and the K remaining entries
assign the actual s:5,...,s:(K+4) in order. The two
inventories are consumed once on those original
vertices and edges. No prefix label is reassigned.
The construction therefore terminates after the fixed
seed, t-3 new leaves, finite high shift and K suffix
assignments, giving ordinary gracefulness. The harness
first checks the actual B4 incidence and both resources
and then uses the unchanged numeric helper. The public
B2 graph wrapper remains specialized to physical s:2.

At K=2, the labels along the original suffix including
the physical port are 11,9,8. The endpoints belong to
one bipartition class and bracket 9 in the other, so the
completed labeling has no alpha threshold in this case.
At K=1 the selected interface would give R={8}, D={1},
and s:4=10, leaving an edge of weight two. Only this
interface is ruled out there.

## Exact coverage with the retained families

At first branch one and second branch two, the accepted
[QR12 construction](B4_UNPADDED_QR12.md) for t=1 covers
all K>=1 with adjacent s:4=K+8, R=[8,K+7] and D=[1,K].
At t=2 and K>=2 the [accepted 1R22 supplier](B4_UNPADDED_1R22_SUPPLIER.md)
has the same numerical nonadjacent resources as the
present construction and its own normalized ledger.
At t=2,K=1 the [retained rooted-core singleton](B4_1R22_K1_ROOTED_CORE.md)
has R={5}, D={5}, s:4=10. Together with the present
t>=3,K>=2 construction this covers the exact ordered
(1,2,t,2) family for every positive t at K>=2. At K=1
only t=1 and t=2 are covered by these results. The
[third zero-host construction with second branch one](B4_THIRD_ZERO_HOST_NONADJACENT.md)
uses low size 7 and its own exact seed. Simultaneous
second and third growth, other fourth sizes and general
B4 or lobster coverage remain separate.

[Bounded evidence](../evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/README.md)
checks three normalized prefixes including the fixed
seed once, four original completions, and one retained
certificate recheck. The same-record arithmetic audit
and normalized batch comparison add zero cases.
