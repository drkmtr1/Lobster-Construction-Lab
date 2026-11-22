# B4-UNPADDED-QR12-001

## Explicit original 1212 base

The prefix [[1],[2],[1],[2],[]] has five original spine vertices
s:0 through s:4, four attached centers b:i:0, and six named
terminal leaves. Its four spine edges, four attachments and six
terminal edges give order 15 and size 14. The constants agree with
the [saved adjacent witness](../evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1212-adjacent.json).
The following direct ledger proves the supplied base without a
solver input or another search.

| Original vertices in order | Labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | 14,0,11,7,8 |
| b:0:0,l:0:0:0 | 1,13 |
| b:1:0,l:1:0:0,l:1:0:1 | 10,4,5 |
| b:2:0,l:2:0:0 | 3,12 |
| b:3:0,l:3:0:0,l:3:0:1 | 9,2,6 |

The low labels appear once in order on s:1, b:0:0, l:3:0:0,
b:2:0, l:1:0:0, l:1:0:1, l:3:0:1, s:3. The highs in order
are s:4, b:3:0, b:1:0, s:2, l:2:0:0, l:0:0:0, s:0. Every
original edge crosses this cut. The original spine weights are
(14,11,4,1). For each branch, list the attachment then its named
terminal weights, giving (13,12), (10,6,5), (8,9), (2,7,3).
These use 1..14 once.

Actual L=b:0:0 has label 1 and actual U=s:4 has label 8.
Take W=b:0:0--s:0--s:1--s:2--s:3--s:4. The first terminal
is one edge from W. The remaining centers are one edge from W
and their terminals two edges away. This is A(15,8;1,0).

The high host b:1:0=10 is adjacent to s:1 in W. At c=4,
the vertices below c are precisely the four vertices in this
ledger. All their original incidences are:

| Selected vertex | Original neighbors and differences |
|---|---|
| s:1 | s:0 (14), s:2 (11), b:1:0 (10) |
| b:0:0 | s:0 (13), l:0:0:0 (12) |
| l:3:0:0 | b:3:0 (7) |
| b:2:0 | s:2 (8), l:2:0:0 (9) |

They exhaust [7,14]=[10-4+1,14]. The two vertices at least
12 are s:0 and l:0:0:0. Their full incidence list consists of
s:0--s:1, s:0--b:0:0, b:0:0--l:0:0:0, with weights
14,13,12. This is the base upper predicate at b:0:0=1.

## Second growth then first growth

For r>=2, use the [lower-block insertion](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
with h=r-2, c=4 and fresh l:1:0:j for 2<=j<r at the original
b:1:0. Its chronological index is i=j-1, giving label
4+(r-2)-(j-1)=r+3-j. All old labels at least 4 rise by r-2.
The state is A(r+13,r+6;1,0) and the lower incident spectrum at
c=4 is [r+5,r+12]. The same host now has r+8 and all fresh
leaves lie two edges from W. At r=2 this step is the identity.

Now c'=r+11 selects exactly s:0=r+12 and l:0:0:0=r+11.
Their complete original incident list is unchanged by the
second-branch additions. Each of those edges has one endpoint
below 4, so each weight grew by r-2, giving [r+10,r+12].
Both port labels 1 and r+6 are below c'. The first center is
still label one and on W. These are the hypotheses of the
[upper-block rule](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md).
Apply q-1 additions l:0:0:j, 1<=j<q, in named order at that
same center. This raises the two selected values by q-1 and
puts the new leaves at r+10+j. The exact order is now
q+r+12 and the state A(q+r+12,r+6;1,0). All added first
leaves are one edge from W. At q=1 this step is the identity.

## Normalized labels and complete edge ledger

For r>=2 on [[q],[r],[1],[2],[]], the resulting formula is:

| Named vertices | Labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | q+r+11,0,r+9,r+5,r+6 |
| b:0:0,l:0:0:0 | 1,q+r+10 |
| l:0:0:j, 1<=j<q | r+10+j |
| b:1:0,l:1:0:0,l:1:0:1 | r+8,r+2,r+3 |
| l:1:0:j, 2<=j<r | r+3-j |
| b:2:0,l:2:0:0 | 3,r+10 |
| b:3:0,l:3:0:0,l:3:0:1 | r+7,2,r+4 |

Labels 0..3 stay fixed. The added second terminals fill
[4,r+1] in descending order, then the two original second
terminals, the second fourth terminal and s:3 fill [r+2,r+5].
In high label order s:4,b:3:0,b:1:0,s:2,l:2:0:0 fill
[r+6,r+10]. The added first terminals fill [r+11,r+q+9],
then l:0:0:0 and s:0 give r+q+10 and r+q+11.
These are bijections on the respective classes, with the
two added-leaf intervals empty at r=2 and q=1 respectively.

| Edges, in indicated order | Differences |
|---|---|
| s:3--s:4, s:3--b:3:0, b:3:0--l:3:0:1, s:2--s:3 | 1,2,3,4 |
| b:1:0--l:1:0:j, j=0,1,2,...,r-1 | 6,5, then [7,r+4] in increasing order |
| b:3:0--l:3:0:0, s:2--b:2:0, b:2:0--l:2:0:0, s:1--b:1:0, s:1--s:2 | r+5 through r+9 |
| b:0:0--l:0:0:j, 1<=j<q | r+10 through r+q+8 |
| b:0:0--l:0:0:0, s:0--b:0:0, s:0--s:1 | r+q+9,r+q+10,r+q+11 |

These are all original edges and fill [1,q+r+11]. The
additional second and first terminal groups have the same
empty cases as above. Every edge crosses the cut at low-class
size r+6, including the newly attached leaves.

After first growth, the old three upper incident edges are
also lower incident edges, since each meets a vertex below 4.
They rise by q-1 and the new first-leaf edges at b:0:0 enter the
lower incident set immediately below them. All smaller lower
incident weights stay. Thus the full lower incident spectrum
is [r+5,q+r+11], with the same vertices below 4, host label
r+8, and W. The upper rule returns threshold q+r+10, selecting
the same s:0 and l:0:0:0 with spectrum [q+r+9,q+r+11].
These returned predicates are for the stated order of
operations. No mixed-operation commutativity or arbitrary
attachment theorem is needed.

## Original completion for all q,r,K>=1

Take the exact ordered unpadded target
`[[q],[r],[1],[2]]+[[]]*(K+1)`. The prefix contains the five
spine vertices through s:4, the four original centers and
q+r+3 named terminals, hence N=q+r+12 vertices. Its only missing
vertices are s:5 through s:(K+4) on the original K-edge path
from s:4. Their only crossing edge is s:4--s:5. The full order
is K+q+r+12 and the size m=K+q+r+11.

For r>=2 raise every normalized high by K and leave lows
fixed. All prefix edges cross the normalized cut and so all
their differences rise by K. Thus the gapped prefix uses
[0,r+5] and [K+r+6,m], and its edges use [K+1,m]. It leaves
R=[r+6,K+r+5], D=[1,K], and the actual s:4=K+r+6 adjacent
above R. The normalized seed precedes the high shift.

For r=1 the accepted [Q112](B4_FOURTH_2_SUPPLY.md) labeling
uses [0,6] and [K+7,m], and [K+1,m] for the used weights.
It has R=[7,K+6], D=[1,K], actual s:4=K+7 and completed
low-class size 7+ceil(K/2), exactly the stated contracts
at r=1. Its label assignments are preserved, including on
the named first and fourth terminals.

In both cases let a=r+6. The [adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
assigns a+i to odd suffix position j=2i+1 and a+K-i to
positive even j=2i. Odd positions fill [a,a+ceil(K/2)-1]
and even positions fill [a+ceil(K/2),a+K-1], with the latter
empty at K=1. These ranges partition R. The preceding
label on an odd step is a+K-i, including the port for i=0,
and the preceding label on an even step is a+i-1. The
differences are therefore K-2i and K-2i+1 respectively,
both K-j+1. The K assignments use all D on the actual
suffix and change no prefix label. Prefix lows and odd suffix
positions fill [0,P-1], and prefix highs and even positions
fill [P,m], for P=r+6+ceil(K/2). Every original edge crosses
this alpha cut. At K=1, R={r+6}, D={1}, s:4=r+7,
s:5=r+6, and P=r+7. Appending the actual suffix to W
witnesses the full topology. A further exported relational
state is outside this proof.

The construction uses explicit constants followed by proved
arithmetic. [R241](../references/upstream/mdl/N241_relational_ports.md)
is a retained comparison and the [earlier join restriction](B4_FOURTH_2_SUPPLY.md#restricted-right-component-compatibility)
remains in force. This is alpha supply for the exact ordered
(q,r,1,2) family. Third-branch growth to general (q,r,t,2)
remains open. The finite campaign and separate reviews
are recorded under [QR12 evidence](../evidence/validation/B4_UNPADDED_QR12_001/README.md).
