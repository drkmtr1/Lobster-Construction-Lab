# B4-UNPADDED-1311-001

The exact original unpadded profile `[[1],[3],[1],[1]]+[[]]*(K+1)`
has a direct alpha graceful labeling for integer K>=1. The public
constructor excludes booleans and other noninteger inputs. This is
the q=1,r=3 instance of the [symbolic family proof](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md#symbolic-unpadded-family-qr11).

## Original graph and direct prefix

The spine has K+5 consecutive vertices s:0,...,s:(K+4).
Four centers attach to their named s:0 through s:3. The first,
third and fourth branches have one leaf each, and all three
leaves l:1:0:0, l:1:0:1 and l:1:0:2 attach to b:1:0.
There are K+15 vertices and m=K+14 edges. The 15-vertex prefix
contains the spine through s:4 and all branches. The remaining
vertices s:5,...,s:(K+4) have exactly the original consecutive
K-edge path from s:4 as their incident edges. The sole crossing
edge is s:4--s:5.

| Named vertices | Supplied labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+14,2,K+11,7,K+8 |
| b:0:0,l:0:0:0 | 0,K+13 |
| b:1:0,l:1:0:0,l:1:0:1,l:1:0:2 | K+10,3,4,5 |
| b:2:0,l:2:0:0 | 1,K+12 |
| b:3:0,l:3:0:0 | K+9,6 |

The lows in label order are b:0:0, b:2:0, s:1, the three
middle leaves in order, l:3:0:0 and s:3. They use [0,7].
The highs in label order are s:4, b:3:0, b:1:0, s:2,
l:2:0:0, l:0:0:0 and s:0. They use [K+8,K+14], and
the original root receives m. These disjoint blocks cover
the prefix once and every original prefix edge crosses them.

| Original prefix edge | Difference |
|---|---:|
| s:3--s:4 | K+1 |
| s:3--b:3:0 | K+2 |
| b:3:0--l:3:0:0 | K+3 |
| s:2--s:3 | K+4 |
| b:1:0--l:1:0:2 | K+5 |
| b:1:0--l:1:0:1 | K+6 |
| b:1:0--l:1:0:0 | K+7 |
| s:1--b:1:0 | K+8 |
| s:1--s:2 | K+9 |
| s:2--b:2:0 | K+10 |
| b:2:0--l:2:0:0 | K+11 |
| s:0--s:1 | K+12 |
| b:0:0--l:0:0:0 | K+13 |
| s:0--b:0:0 | K+14 |

The table accounts for four prefix spine edges, four attachments
and six terminal edges exactly once. Taking complements in 0..m
and 1..m gives R=[8,K+7] and D=[1,K], with physical s:4=K+8.

## Derived seed and completion

The retained relabeled left seed is A(9,4;0,1). Add two leaves at
its minimum-high b:1:0 using the supplied-host rule. The resulting
11-vertex left has low-class size 6, ports b:0:0=0 and s:2=7,
minimum high b:1:0=6, and old witness b:0:0--s:0--s:1--s:2.
Its differences exhaust 1..10. R241 joins it to reflected L008
along exactly s:2--s:3. The shifts are six to A and four to the
left highs, with connector difference 4. The 15-vertex prefix
seed uses 0..14 and 1..14, with low-class size 8 and actual
ports b:0:0=0 and s:4=8. The concatenated witness ends at s:4.
The executable evidence records the expanded left and prefix
as separate arithmetic certificates. The direct supplier is
the seed with K added to each high.

The adjacent helper starts at index 4 and writes only the original
suffix. It takes the lowest remaining label at odd positions
j=2i+1, namely 8+i, and the highest at even j=2i>0, namely
K+8-i. The two sets are [8,7+ceil(K/2)] and [8+ceil(K/2),K+7].
They partition R, with the even set empty at K=1. An odd step
follows K+8-i, including the starting port at i=0, and uses
difference K-2i. An even step follows 8+i-1 and uses K-2i+1.
Thus every original step j uses K-j+1. After exactly K assignments
both inventories are exhausted and all prefix labels are preserved.

Prefix lows and odd suffix positions fill 0..p-1, where
p=8+ceil(K/2). Prefix highs and even suffix positions fill
p..m. The prefix crosses the cut and the path alternates
across it from high s:4, so the full labeling is alpha with
cutoff p-1. At K=1 the original last edge joins s:4=9 and s:5=8
using R={8}, D={1}, and p=9. The unchanged original-target
checker verifies the construction. The CLI graph ceiling is
K<=9985 and the record-size cap applies separately. The
executable route is exact 1311 only.
