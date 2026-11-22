# B4-UNPADDED-QR21-001

For all positive integers q,r,K the exact original unpadded profile
`[[q],[r],[2],[1]]+[[]]*(K+1)` is alpha graceful. This is the t=2
case of the [upper-block family proof](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md#exact-symbolic-qrt1-family).
Only this specialization has a new executable route.

## Original graph and direct prefix

The K+5 consecutive spine vertices, four original centers and
q+r+3 terminal leaves give q+r+K+12 vertices and m=q+r+K+11
edges. Each center b:i:0 attaches to s:i. Its original named
leaves l:i:0:j stay at that center. In particular both
l:2:0:0 and l:2:0:1 attach to b:2:0. The prefix includes all
branches and spine through s:4. The only remaining vertices
are s:5,...,s:(K+4). Their only incident edges comprise the
original K-edge path from s:4, with sole crossing s:4--s:5.

| Named vertices | Direct supplied labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+r+12,2,K+r+8,r+4,K+r+5 |
| b:0:0,l:0:0:0 | 0,K+r+11 |
| l:0:0:j (1<=j<q) | K+r+12+j |
| b:1:0,l:1:0:j (0<=j<r) | K+r+7,3+j |
| b:2:0,l:2:0:0,l:2:0:1 | 1,K+r+9,K+r+10 |
| b:3:0,l:3:0:0 | K+r+6,r+3 |

The root is m-(q-1), so it receives m at q=1. At q>1 the
last extra first leaf receives m. The lows are 0,1,2,
the r middle leaves 3..r+2, and r+3,r+4, filling [0,r+4].
The highs in order are s:4, b:3:0, b:1:0, s:2, the two
third leaves, the original first leaf, and the root,
followed by the extra first leaves. They fill [K+r+5,m].
Every original prefix edge crosses the two blocks.

| Original edges | Difference block |
|---|---|
| s:3--s:4, s:3--b:3:0, b:3:0--l:3:0:0, s:2--s:3 | K+1 through K+4 in order |
| b:1:0--l:1:0:j (0<=j<r) | K+r+4-j, using [K+5,K+r+4] |
| s:1--b:1:0, s:1--s:2, s:2--b:2:0 | K+r+5 through K+r+7 in order |
| b:2:0--l:2:0:0, b:2:0--l:2:0:1 | K+r+8 and K+r+9 |
| s:0--s:1, b:0:0--l:0:0:0, s:0--b:0:0 | K+r+10 through K+r+12 in order |
| b:0:0--l:0:0:j (1<=j<q) | K+r+12+j, using [K+r+13,m] |

The ledger includes the four original prefix spine edges, four
attachments and all q+r+3 leaf edges. It partitions [K+1,m],
including the empty last block when q=1. Thus R=[r+5,K+r+4],
D=[1,K] and the original s:4=K+r+5 is just above R.

## Completion and scope

Set a=r+5. The unchanged adjacent helper begins at physical
index 4. The original suffix gets a+i at odd j=2i+1 and
a+K-i at even j=2i>0. These labels fill the disjoint sets
[a,a+ceil(K/2)-1] and [a+ceil(K/2),a+K-1]. Each original
suffix edge uses K-j+1 by subtracting its consecutive
labels. Exactly K assignments exhaust both inventories
and preserve the prefix. Prefix lows and odd suffix
positions use 0..p-1 for p=r+5+ceil(K/2), while prefix highs
and even positions use p..m. The original edges cross this
cut. At K=1 the last edge joins s:4=r+6 to s:5=r+5 and
p=r+6. The full cutoff is p-1.

The executable constructor takes q,r,K, checks positive exact
integers and uses the direct prefix with the unchanged original
checker. It certifies the full alpha cut. The CLI graph ceiling
is q+r+K<=9988, with the separate 2,000,000-byte record cap.
The mathematical quantifiers hold independently of those limits.
The q=r=1 graph already lies in 1121 coverage. Its new-route
certificate may differ pointwise from 1121, whose accepted
constructor and evidence remain valid.
