# B4-FOURTH-2-SUPPLY-001

## Restricted right-component compatibility

The original graph `[[2],[]]` has physical entrance s:3, exit s:4,
center b:3:0, and leaves l:3:0:0 and l:3:0:1. Its edges are
s:3--s:4, s:3--b:3:0 and the two terminal edges at b:3:0. The
bipartition with s:3 low puts s:3 and both leaves low and s:4
and the center high. An alpha labeling therefore has low labels
0,1,2 and high labels 3,4.

Fix entrance s:3=1. If s:4=3, the center is 4 and the leaf
with label 2 makes difference 2, already used by s:3--s:4.
If s:4=4, the center is 3 and the leaf with label 0 makes
difference 3, again already used by s:3--s:4. These cover both
exit offsets. No state A(5,3;1,y) exists for this graph with
the prescribed entrance and exit.

On the same graph two feasible assignments are:

| State | s:3 | s:4 | b:3:0 | l:3:0:0 | l:3:0:1 | Differences in the edge order above |
|---|---:|---:|---:|---:|---:|---|
| A(5,3;2,0) | 2 | 3 | 4 | 0 | 1 | 1,2,4,3 |
| A(5,3;0,1) | 0 | 4 | 3 | 1 | 2 | 4,3,2,1 |

Each is a bijection onto 0..4 and every edge crosses the
stated cut. The original edge s:3--s:4 witnesses the two ports,
with the center one step away and each leaf two steps away.
The [retained left component](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md#composition-in-the-supplied-order)
has exit offset one. Under [R241](../references/upstream/mdl/N241_relational_ports.md)
the right entrance offset must match it to give connector
difference five between the exact original ports. With the two
feasible states above, the connector differences would instead
be four and six. The needed entrance-one state is ruled out
on this component. The obstruction concerns this prescribed
R241 join and leaves ordinary gracefulness of the full target
unrestricted. The [111T construction](B4_UNPADDED_111T.md)
already supplies ordinary gracefulness on its own exact unit-left
family, using separate contracts for K=1 and K>=2.

## Direct alternative seed and conditional insertion

On the original graph `[[1],[1],[1],[2],[]]`, label the five
spine vertices in order (13,0,8,6,7). Assign the center and
leaves in each branch, in name order, as (1,12), (10,3),
(2,11), (9,4,5). The low vertices in label order are
s:1, b:0:0, b:2:0, l:1:0:0, l:3:0:0, l:3:0:1, s:3.
The highs in label order are s:4, s:2, b:3:0, b:1:0,
l:2:0:0, l:0:0:0, s:0. The disjoint blocks exhaust 0..13
and each original edge crosses. The spine edges supply (13,8,2,1).
The attachment and terminal differences in branch order are
(12,11), (10,7), (6,9), (3,5,4). Thus all four spine edges
and nine branch edges give 1..13 once.

The actual witness is b:0:0--s:0--s:1--s:2--s:3--s:4.
The first leaf is one step from b:0:0. Each other center
is one step from its spine vertex and each of its leaves
is two steps away, including both fourth terminals. This
supplies A(14,7;1,0) at actual L=b:0:0=1 and U=s:4=7.

Use the [accepted upper-block insertion](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md)
at actual z=L=1 on the witness with c=12>7. The only vertices
at or above c are s:0=13 and l:0:0:0=12. All of their original
incident edges are s:0--s:1, s:0--b:0:0, and b:0:0--l:0:0:0,
with differences 13,12,11. This is the full required multiset.

For integer q>=1 append h=q-1 leaves l:0:0:j for 1<=j<q at
b:0:0. Only s:0 and l:0:0:0 gain h, becoming q+12 and q+11,
and new leaf j receives 11+j. Every other normalized label
stays as above. The graph is exactly `[[q],[1],[1],[2],[]]`
and the state is A(q+13,7;1,0). The original difference
bands are [1,10] unchanged, [11,q+9] from new edges, and
[q+10,q+12] from changed old edges. The inserted band is
empty at q=1. The threshold is now c+h=q+11 and still selects
just those two old vertices. Thus successive additions at
that same physical host preserve the incident predicate and
agree with the given batch in name order. The witness remains
valid with every new leaf one step from it. This is an
application of the existing conditional rule to a new supplied
state.

## Exact symbolic Q112 family

For every positive integer q,K take the exact target
`[[q],[1],[1],[2]]+[[]]*(K+1)`. Its order is K+q+13,
with m=K+q+12 edges. Only s:5,...,s:(K+4) lie outside the
prefix. All their incident edges are the original consecutive
path from s:4, and the sole edge crossing the prefix boundary
is s:4--s:5.

Raise all seed highs by K. The direct formula is:

| Named vertices | Prefix labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+q+12,0,K+8,6,K+7 |
| b:0:0,l:0:0:0 | 1,K+q+11 |
| l:0:0:j (1<=j<q) | K+11+j |
| b:1:0,l:1:0:0 | K+10,3 |
| b:2:0,l:2:0:0 | 2,K+11 |
| b:3:0,l:3:0:0,l:3:0:1 | K+9,4,5 |

The original alpha split implies used labels [0,6] and [K+7,m].
Every original prefix difference increases by K. The three
bands above therefore fill [K+1,m] exactly once. The unused
inventories are R=[7,K+6] and D=[1,K]. The actual port is
s:4=K+7, immediately above R.

The retained [adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
takes the low endpoint at odd j=2i+1, giving 7+i, and the
high endpoint at even j=2i>0, giving 7+K-i. These produce
[7,6+ceil(K/2)] and [7+ceil(K/2),K+6]. At K=1 the second
set is empty. The intervals partition R. The predecessor of
an odd step has label 7+K-i, including the initial port for
i=0, giving difference K-2i. The predecessor of an even
step has label 7+i-1, giving difference K-2i+1. Both equal
K-j+1. Exactly K assignments consume D and preserve the
prefix. With p=7+(K+1)//2, prefix lows and odd suffix
positions use 0..p-1, and prefix highs and even positions
use p..m. Every original edge crosses the cutoff p-1.
At K=1, R={7}, D={1}, s:4=8, s:5=7 and p=8. To witness
the completed topology extend the prefix path through the
original suffix.

The executable route is `four_section_q112(q,K)` for positive
exact integers, on this ordered profile. CLI graph preflight
requires q+K<=9987, with the 2,000,000-byte record cap applied
separately. The theorem covers only (q,1,1,2). The two
[bounded diagnostics](../evidence/validation/B4_FOURTH_2_SUPPLY_001/DIAGNOSTICS.md)
are finite evidence for different prefixes. Arbitrary (q,r,t,2)
supply remains open.
