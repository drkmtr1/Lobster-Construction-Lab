# B4-UNPADDED-1R22-SUPPLIER-001

## Exact graph and supplied interface

On `[[1],[r],[2],[2],[]]`, the five spine vertices s:0 through s:4
have their four original consecutive edges. The four centers b:i:0
attach to s:i for i=0,1,2,3. The r+5 terminals keep their original
names l:i:0:j and attach to those centers in counts 1,r,2,2.
There are n=r+14 vertices and r+13 edges. All parameters in the
theorem are exact integers, with Booleans excluded.

With s:4 high, the low vertices are s:1,s:3,b:0:0,b:2:0 and every
second or fourth terminal. The high vertices are s:0,s:2,s:4,
b:1:0,b:3:0, the first terminal and the two third terminals.
Every edge crosses these classes, of sizes p=r+6 and 8. The
actual path W=b:0:0--s:0--s:1--s:2--s:3--s:4 contains the spine
and original first center. Its first terminal lies one edge
away. All other centers lie one edge away and their terminals
two, including the additional second leaves. Use L=b:0:0,
U=s:4 and this W throughout.

## Why the retained lower-block instances cannot be imported

In [QR12](B4_UNPADDED_QR12.md), the actual second center has
base label 10 and threshold c=4. The entire incidence set of
lows below 4 has weights [7,14]. It includes the third
attachment and its one terminal edge through b:2:0=3. A second
terminal at that selected vertex adds another incidence, and the
alphabet changes. The complete predicate must be supplied again
on the new labeled graph. It cannot be inherited just from the
shape of the second branch.

The two [retained 1122 diagnostic ledgers](../evidence/validation/B4_FOURTH_2_SUPPLY_001/DIAGNOSTICS.md)
can be checked more strongly. For c in [1,7], let S_c consist
of the vertices with labels below c. All of them are low,
so no two are adjacent and the size of their full incident set
is the cumulative sum of their degrees in ascending label order.
The [lower-block premise](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
requires the entire multiset [b-c+1,14], of size 14-b+c,
where b is the actual b:1:0 label.

| Saved ledger | b | Physical s:4 | Cumulative degrees at c=1,...,7 | Required counts at c=1,...,7 |
|---|---:|---:|---|---|
| 1122 adjacent | 11 | 7 | 3,5,8,9,10,11,14 | 4,5,6,7,8,9,10 |
| 1122 nonadjacent | 14 | 8 | 3,6,7,9,10,11,14 | 1,2,3,4,5,6,7 |

Only the adjacent c=2 has the right count. Its selected low
vertices are s:1=0 and b:0:0=1. Their original incidence weights
are 14,9,11 and 13,12, respectively. The premise requires
[10,14], so the weight 9 replaces the required 10. Neither fixed
ledger works at any cut, even without requiring x<c. These are
failures of two specified labeled templates.

The [third zero-host seed](B4_THIRD_ZERO_HOST_NONADJACENT.md#explicit-seed-and-witness)
is a different nonadjacent ledger, with b:1:0=11 and b:2:0=0.
Its degree sums at c=1,...,7 are 3,6,7,8,10,13,14, which also
miss the required counts 4,5,6,7,8,9,10 at every cut.
Its existing [Q1T2 application](B4_UNPADDED_Q1T2.md) grows first
and third terminals by a different incidence predicate. The
[previous K=1 rooted core](B4_Q1T2_K1_ROOTED_CORE.md)
gives an ordinary supplier whose exhibited labels do not have
an alpha cut. That result is left unchanged.

## Independent normalized ledger

Use the following explicit base on the exact r=1 prefix.
An edge row lists attachment then terminals, except the spine row
which lists consecutive spine edges. The r=1 ledger is an
arithmetic base for the proof, outside the new executable campaign.

| Named vertices in order | Base labels | Original edge weights |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 13,1,12,6,8 | 12,11,6,2 |
| b:0:0,l:0:0:0 | 5,10 | 8,5 |
| b:1:0,l:1:0:0 | 14,0 | 13,14 |
| b:2:0,l:2:0:0,l:2:0:1 | 2,9,11 | 10,7,9 |
| b:3:0,l:3:0:0,l:3:0:1 | 7,3,4 | 1,4,3 |

To obtain the constants, choose the original second terminal as
the zero vertex and its center as the maximum. The maximum minus
one must then use s:1=1 at that center. Place 13,12 at s:0,s:2
to give weights 12,11 there. Use s:3=6, s:4=8 and b:3:0=7 to
supply weights 2 and 1, with s:2--s:3 of weight 6. Putting
2 at b:2:0 and 5 at b:0:0 gives the attachment weights 10 and
8. The remaining low values 3,4 give fourth leaf weights 4,3.
The remaining high values 9,10,11 give the terminal weights
7,5,9 at the indicated centers. This gives the displayed
constants and uses no solution as input.

The table uses [0,6] once on precisely the listed lows and
[7,14] once on the eight highs. Its listed weights are exactly
[1,14] once on the 14 actual original edges. It supplies
A(15,7;5,1) with physical ports and W as above.

## Fixed-cut growth and direct formula

The cut c=1 selects exactly the original second terminal
l:1:0:0. Its unique edge joins it to b:1:0=14, so the entire
selected incident spectrum is {14}=[b-c+1,14], and the host is
one edge from W. The retained lower-block theorem preserves
x by requiring x<c, which fails here because x=5. We use its
arithmetic and prove the actual changing low port directly.

Let h=r-1. Keep the original zero leaf at zero and raise all
other old labels by h. Add exactly the named leaves l:1:0:j at
b:1:0 for 1<=j<=h, assigning h+1-j. In direct form:

| Named vertices | Normalized labels g_r |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | r+12,r,r+11,r+5,r+7 |
| b:0:0,l:0:0:0 | r+4,r+9 |
| b:1:0,l:1:0:0 | r+13,0 |
| l:1:0:j for 1<=j<r | r-j |
| b:2:0,l:2:0:0,l:2:0:1 | r+1,r+8,r+10 |
| b:3:0,l:3:0:0,l:3:0:1 | r+6,r+2,r+3 |

The original zero and fresh labels [1,h] are followed by the
six shifted positive lows [h+1,h+6] and the eight shifted
highs [h+7,h+14]. These disjoint bands exhaust [0,r+13].
Every old edge crosses the new cut at p=h+7=r+6, and each
new low leaf is adjacent only to the high host. Old edges other
than the original zero leaf edge keep the weights [1,13] listed
above because both endpoints shift equally. The new terminal
of index j has weight (r+13)-(r-j)=13+j. The new weights fill
[14,r+12], and the old zero edge now gives r+13. This partitions
every original difference once, including the single new
weight 14 at r=2. At h=0 the new bands are empty and the
ledger is the identity. Each attachment preserves connectivity,
acyclicity and all old named incidences.

The first center moves to r+4 below p and the actual s:4
moves to r+7=p+1. All original witness edges stay and the
new terminals lie two steps from W. The state is therefore
A(r+14,r+6;r+4,1). The maximum and zero stay at the same two
physical vertices. After each finite batch only the original
zero terminal is below c=1. Its full incident spectrum is
the singleton containing the new maximum and the host remains
adjacent to the witness. If an earlier batch of size a is
followed by one of size b, its positive labels gain b, including
the i-th new label a+1-i which becomes a+b+1-i. The j-th
name in the later batch receives b+1-j, equal to
a+b+1-(a+j). The original zero remains fixed. Thus finite
successive batches agree pointwise with one concatenated batch
in the same order. The formula terminates after the fixed old
ledger and exactly r-1 specified additions.

## High shift and original-path completion

For integer r>=2 and K>=2 the full original target has
profile `[[1],[r],[2],[2]]+[[]]*(K+1)`, order K+r+14 and
m=K+r+13 original edges. The unassigned vertices after the
prefix are exactly s:5,...,s:(K+4). These sections are empty
and their only original incidences are the K consecutive
spine edges from s:4. The sole crossing edge is s:4--s:5.

Raise every normalized high by K, keeping every low fixed.
The used labels are [0,p-1] and [p+K,m]. Each original
prefix difference rises by K, giving [K+1,m] once. Hence
R=[r+6,r+K+5]=[p,p+K-1], D=[1,K] and physical s:4=p+K+1.
This is the above-side nonadjacent case for every allowed r.

Use the [numeric recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof)
C_2=(3,1,0), C_3=(4,1,0,2), C_4=(5,1,2,0,3).
For K>=5 write C_(K-3)=(K-2,x_1,...,x_(K-3)).
Then C_K=(K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3)).
The bases have suffix labels 0..K-1 and differences 1..K
once each for their lengths. The reflected tail fills
[2,K-2], complementary to 1,K-1,0. Its differences including
the bridge from 0 are [1,K-3], since 0 is the reflection of
the shorter port. The first three differences are K,K-2,K-1.
This proves the recurrence by induction, reducing K by three
until a base.

Translate C_K by p. Its first entry is exactly the existing
physical port s:4. Assign its K remaining entries in order
to the actual s:5,...,s:(K+4), changing no prefix label.
The assignments exhaust R, and their original path differences
exhaust D. They terminate after K assignments, proving ordinary
gracefulness on the exact stated full domain. The bounded
harness validates the B4 boundary before calling the numeric
helper. The public graph wrapper is specialized to s:2.

At K=1 this particular interface leaves {p}, {1}, and port
p+2, so its only possible edge would have weight two. The K=1
family remains outside this construction. At K=2 the three
path labels p+3,p+1,p have their same-class endpoints bracketing
the middle label, excluding an alpha cut for that completed
labeling. The alpha theorem here concerns the normalized
prefix. No arbitrary first-, third- or fourth-branch growth
follows from this supplier.

[Bounded evidence](../evidence/validation/B4_UNPADDED_1R22_SUPPLIER_001/README.md)
covers four completed originals, three normalized prefixes and
two retained diagnostic rechecks. The symbolic proof establishes
the quantifiers. No search, enumeration or historical replay
was used.
