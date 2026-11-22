# B4-1R32-MINIMUM-HIGH-SUPPLIER-001

## The actual retained seed and its two hosts

The [retained 1232 seed](B4_12T2_ZERO_HOST_SUPPLIER.md#original-seed-and-direct-ledger)
has ordered profile `[[1],[2],[3],[2],[]]`. Its five spine
vertices s:0 through s:4 have four consecutive edges. Each
b:i:0 at i=0,1,2,3 attaches to its original s:i, and its
terminal names l:i:0:j attach only to that center, in counts
1,2,3,2. This gives 17 vertices and 16 edges.

| Named vertices in order | Retained labels | Original edge differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 11,7,16,4,9 | 4,9,12,5 |
| b:0:0,l:0:0:0 | 1,12 | 10,11 |
| b:1:0,l:1:0:0,l:1:0:1 | 8,6,5 | 1,2,3 |
| b:2:0,l:2:0:0,l:2:0:1,l:2:0:2 | 0,13,14,15 | 16,13,14,15 |
| b:3:0,l:3:0:0,l:3:0:1 | 10,2,3 | 6,8,7 |

The first row uses spine order. Each branch row lists its
attachment weight and then its terminal weights in name
order. These account for all sixteen original edges,
with weights [1,16] once. The labels use [0,16] once,
with exactly s:1,s:3,b:0:0,b:2:0 and the second and fourth
terminals below 8. This is the actual bipartition class
opposite s:4. Every edge crosses the cut. In particular the
two old second terminals have labels 6 and 5 in the given
order.

Physical L=b:0:0 has label 1, U=s:4 has label 9, H=b:1:0
has the minimum high label 8 and Z=b:2:0 has label 0.
The actual path W=b:0:0--s:0--s:1--s:2--s:3--s:4
contains L and the spine. Its first terminal neighbor
lies one edge away. Each of the other centers is one
edge from W and each of their terminals is two edges
away. In particular H and Z are one edge from W via s:1
and s:2, respectively. The seed is A(17,8;1,1), and H
satisfies the exact minimum-high extension premise.
The bounded run rechecks this one retained certificate
against its separately preserved original.

## Prescribed growth and full normalized spectra

For exact integer r>=3, let h=r-2. Apply the retained
[minimum-high extension](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md#supplied-state-and-finite-closure)
once at physical H. Keep each original low, raise each
original high by h, and add exactly the fresh l:1:0:j
for 2<=j<r, each at H. At global index j, the extension's
one-based fresh index is j-1; the new label is therefore
8+(j-1)-1=j+6. In full named form:

| Named vertices in order | Normalized labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | r+9,7,r+14,4,r+7 |
| b:0:0,l:0:0:0 | 1,r+10 |
| b:1:0,l:1:0:0,l:1:0:1 | r+6,6,5 |
| l:1:0:j for 2<=j<r | j+6 |
| b:2:0 | 0 |
| l:2:0:j for 0<=j<3 | r+11+j |
| b:3:0,l:3:0:0,l:3:0:1 | r+8,2,3 |

Old lows occupy [0,7], fresh lows [8,r+5], and the
shifted original highs [r+6,r+14]. Each value occurs
once. The old edges have one original high endpoint,
so they each gain h and use [r-1,r+14]. The fresh
edges at H have weights (r+6)-(j+6)=r-j, exactly
[1,r-2] in descending name order. These disjoint bands
cover all weights on the original prefix. Each new
leaf is low under p=r+6 and attaches only to the
minimum high H. All old edges retain their crossing
of the enlarged alpha classes. The exact prefix
has five spine vertices, four centers and r+6
terminal leaves, hence r+15 vertices.

The added leaf edges preserve connectivity, acyclicity
and all old incidences. The same path W remains, with
both H and Z one edge away and each new leaf two
edges away. The unchanged L label is 1, physical U
has r+7=p+1, H has r+6=p, and unchanged Z has zero.
The result is A(r+15,r+6;1,1). The high size stays nine.

## Finite closure in named order

At any intermediate second-branch count r_0>=2 the
current order is r_0+15 and low size p_0=r_0+6. The
same actual H has the minimum high label p_0. The
actual ports have 1 and p_0+1, the witness persists,
and the original Z remains zero one edge from W.
The previously inserted second leaves are now low,
so later batches leave them fixed. These facts
discharge the retained extension hypotheses again.

In a later batch, the u-th fresh name has global index
j=r_0+u-1 and receives p_0+u-1=j+6. Original highs gain
the sum of batch sizes, original lows stay, and every
fresh vertex gets its same direct-formula value at the
same physical center. Inducting over any finite number
of ordered batches gives pointwise agreement and takes
exactly r-2 additions. An empty batch keeps the state.
The retained r=2 ledger is the zero-addition control.

The unchanged zero host and its witness distance are
returned data. The [zero-host lemma](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
uses precisely those physical hypotheses along with
the supplied alpha state. No third-branch growth is
applied or promoted here.

## Updated high shift and original suffix

For exact integers r>=3,K>=2 take the full original
`[[1],[r],[3],[2]]+[[]]*(K+1)`, of order K+r+15 and
size m=K+r+14. Its only vertices not in the normalized
prefix are s:5 through s:(K+4). The sections are empty
there, so the only incidences touching those vertices
are the original K consecutive spine edges from s:4.
The sole crossing edge is original s:4--s:5.

Raise every high label under the updated cut p=r+6 by K.
The assigned labels are now [0,r+5] union [K+r+6,m].
Every original prefix edge gains K from its high endpoint,
so the assigned weights are [K+1,m] once. Taking complements
in the full alphabets gives R=[r+6,r+K+5] and D=[1,K].
The physical s:4 has value r+K+7, two above the maximum of R.

If the former cut 8 were used, each fresh low and H would
both be shifted. The fresh edges would then keep their
[1,r-2] weights, including 1, contrary to D=[1,K].
The missing label interval in that particular wrong shift
would also start at 8 rather than r+6. This rules out
that shift as the stated resource supplier.

Use the [retained numerical recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof).
Its bases C_2=(3,1,0), C_3=(4,1,0,2) and
C_4=(5,1,2,0,3) have first entry K+1, suffix [0,K-1]
once and weights [1,K] once for their lengths. For K>=5
write C_(K-3)=(K-2,x_1,...,x_(K-3)). The new sequence is

```text
C_K=(K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3)).
```

Reflection fills [2,K-2], complementary to 1,K-1,0.
It sends the shorter port K-2 to the new 0, so the
bridge from 0 and the subsequent tail edges include
all reflected weights [1,K-3]. The first three edges
give K,K-2,K-1. Induction proves the two inventories
and terminates by reducing K by three to a base.

Translate C_K by r+6. Its first entry equals the existing
physical s:4. Its remaining entries assign the original
s:5 through s:(K+4) in order. These K assignments use R
and D exactly once on the actual original path and
preserve every prefix label. This proves ordinary
gracefulness of the full original. The bounded harness
checks the B4 contract before calling only the unchanged
numeric helper. The B2 graph wrapper keeps its
narrower physical s:2 scope.

At K=1 this same shift leaves R={r+6}, D={1} and
s:4=r+8. The only finishing edge would have weight
2. This is only an interface restriction. At K=2,
the suffix including the port has labels r+9,r+7,r+6.
Its two endpoints are in the same bipartition class
and bracket the other-class middle label. Thus this
completed labeling admits no alpha cut. The alpha
claim is for the normalized prefix.

## Exact coverage and bounded evidence

For r=1 and K>=2 the retained [Q1T2 supplier](B4_UNPADDED_Q1T2.md)
at q=1,t=3 uses R=[7,K+6], D=[1,K], physical s:4=K+8.
At r=2 the retained [12T2 supplier](B4_12T2_ZERO_HOST_SUPPLIER.md)
at t=3 uses R=[8,K+7], D=[1,K], physical s:4=K+9.
These two and the present r>=3 route cover all positive r
at K>=2 on the exact ordered (1,r,3,2) family. The
[retained r=2 singleton](B4_12T2_K1_ROOTED_CORE.md)
has its own R={6}, D={6}, s:4=12. The r>=3,K=1
family and simultaneous arbitrary second- and third-
branch sizes remain separate obligations.

[Bounded evidence](../evidence/validation/B4_1R32_MINIMUM_HIGH_SUPPLIER_001/README.md)
checks three new normalized prefixes, four exact
completed originals and one retained recheck. The
normalized r=5 comparison uses one batch of three and
unit batches through the saved r=3 and r=4 prefixes.
The same-record audit and batch comparison add zero cases.
