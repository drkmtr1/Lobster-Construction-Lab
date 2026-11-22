# B4-THIRD-ZERO-HOST-SEED-001

## Retained original and control

The exact 1122 prefix `[[1],[1],[2],[2],[]]` consists of
s:0 through s:4, the four original branch centers at their
respective spine vertices, and six original terminals at their
respective centers. The [retained adjacent certificate](../evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1122-adjacent.json)
uses the following labels. For a branch the differences are
listed in attachment-then-terminal order, with terminals in
increasing name index.

| Named vertices in order | Labels | Original edge differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 14,0,9,6,7 | 14,9,3,1 |
| b:0:0,l:0:0:0 | 1,13 | 13,12 |
| b:1:0,l:1:0:0 | 11,5 | 11,6 |
| b:2:0,l:2:0:0,l:2:0:1 | 2,10,12 | 7,8,10 |
| b:3:0,l:3:0:0,l:3:0:1 | 8,3,4 | 2,5,4 |

The labels use 0..14 once and the original weights use 1..14
once. Edges cross between the seven physical low vertices
s:1, s:3, b:0:0, b:2:0, l:1:0:0, l:3:0:0, l:3:0:1 and
the other eight vertices. The physical adjacent exit has label 7.
This control has b:2:0=2 and therefore fails the new pin b:2:0=0.
The original graph digest is
`a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc`.
The historical DFS is preserved as evidence.

## Restricted obstruction with all seven named lows fixed

Let integer t>=3 and M=t+12 on the exact original prefix
`[[1],[1],[t],[2],[]]`. Suppose it is alpha graceful with
lows [0,6], highs [7,M], the seven low labels fixed as in
the control above, and physical s:4 fixed at 7. These are
the only pins. In particular s:0 has a free high label and
all named terminal orderings are allowed within the domain.

Since every edge crosses the cut, a difference d can only
arise from a high label minus a low label. For d=2 the only
pairs (high,low) are (7,5),(8,6). Physical s:4=7 has only
prefix neighbor s:3=6, so (7,5) is impossible. Label 8 must
be a neighbor of s:3 other than s:4: s:2 or b:3:0.

For d=3 the pairs are (7,4),(8,5),(9,6). Again the exit
excludes (7,4). Neither possible label-8 vertex is adjacent
to l:1:0:0=5, excluding (8,5). Thus label 9 must go on the
other of s:2 and b:3:0. If s:2=8 and b:3:0=9, the distinct
edges s:2--b:2:0 and b:3:0--l:3:0:0 both have weight 6.
It follows that s:2=9 and b:3:0=8.

For d=6 check all possible pairs (7,1),(8,2),(9,3),
(10,4),(11,5),(12,6). The first three are nonedges at
the now fixed physical high endpoints. Label 4 occurs at
l:3:0:1 whose only neighbor b:3:0 has 8, excluding (10,4).
Label 6 occurs at s:3 whose three neighbors are fixed to
9,8,7, excluding (12,6). Thus (11,5) is required. The only
neighbor of the terminal at 5 is b:1:0, so b:1:0=11.
Its original attachment to s:1=0 uses weight 11.

The largest required difference M has endpoints 0 and M.
The only neighbors of s:1=0 are s:0, s:2=9 and b:1:0=11.
Since M>=15, s:0 must take M. This label is forced by the
spectrum and incidences. The remaining high vertices are
the first terminal and the t third terminals. Label 13 is
still unused among the assigned highs 7,8,9,11,M. It cannot
go on a third terminal at b:2:0=2 because that would give
weight 11 a second time. Therefore l:0:0:0=13 and its edge
has weight 12.

All non-third-terminal edges now have the following weights:

| Original incidences | Differences |
|---|---|
| Four spine edges in order | M,9,3,1 |
| First attachment and terminal | M-1,12 |
| Second attachment and terminal | 11,6 |
| Third attachment | 7 |
| Fourth attachment and the two named terminals | 2,5,4 |

This list is exhaustive for those twelve edges. For M>=15
it omits M-2, since M-2>=13 and is distinct from M-1,M.
A third terminal would have to take label M to make
difference M-2 at its center of label 2. That label is
already used at s:0, a contradiction.

This obstruction concerns the exact named low pins, alpha
classes and physical adjacent exit. It leaves relabelings of
the low class and ordinary gracefulness on the target open.
The proof uses the full original incidences and requires no
search on t>=3 instances.

## One zero-host adjacent seed query

On the exact original 1122 prefix the seven named low vertices
have full domain [0,6] and the other eight named vertices have
full domain [7,14]. The only pins are b:2:0=0 and s:4=7.
In particular the former low pins are absent. There is no
additional root pin, terminal-order restriction, automorphism
quotient or complement quotient.

After validating the configuration and retaining the original,
the unchanged exact DFS ran once in first-witness mode.
The limits were one worker, 15 vertices, 100,000 nodes, five
cooperative seconds and 2,000,000 bytes per result. The result was
EXHAUSTED_NO_SOLUTION after 17,514 nodes in 0.15197850001277402 s.
It exhausted the declared named restrictions with count zero,
with no witness or positive certificate. The first-witness mode
did not request counting. The zero follows from the completed
exhaustion. The independent audit rechecked the saved original,
control arithmetic, restrictions and receipt. It did not
repeat or independently exhaust the search.

This removes only the specified normalized 1122 seed with
a zero at the third center and adjacent exit at physical s:4.
The [zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
holds on its supplied hypotheses. This query did not supply
those hypotheses for the symbolic third-branch construction.
The success branch was inapplicable and produced zero new
seed certificates or direct completed targets. The accepted
[Q112](B4_FOURTH_2_SUPPLY.md) at q=1 still covers t=1, and
the retained adjacent 1122 control remains a valid prefix at
t=2 with different host label. Other relabelings and supplier
designs for t>=3 remain open.
[Saved query and audit](../evidence/validation/B4_THIRD_ZERO_HOST_SEED_001/README.md)
