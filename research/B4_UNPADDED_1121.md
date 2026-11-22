# B4-UNPADDED-1121-001

For every integer `K>=1`, the exact original unpadded profile
`[[1],[1],[2],[1]]+[[]]*(K+1)` has a direct alpha graceful labeling.
The constructor excludes booleans.

## Original graph and prefix

There are K+5 consecutive spine vertices `s:0,...,s:(K+4)`, four
centers `b:i:0` attached at their respective `s:i`, and five terminal
leaves. Both `l:2:0:0` and `l:2:0:1` attach to `b:2:0`. The order is
K+14 and the K+4 spine edges and nine branch edges give m=K+13. The
prefix consists of spine indices 0 through 4 and all branches, with 14
vertices and 13 edges. Only `s:5` through `s:(K+4)` remain unassigned.
Their incident edges are exactly the consecutive path from `s:4`. The
sole edge with exactly one unassigned endpoint is `s:4--s:5`.

| Named vertices in order | Supplied labels in order |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+12,1,K+9,5,K+6 |
| b:0:0,l:0:0:0 | 2,K+11 |
| b:1:0,l:1:0:0 | K+13,0 |
| b:2:0,l:2:0:0,l:2:0:1 | 3,K+10,K+8 |
| b:3:0,l:3:0:0 | K+7,4 |

The six low vertices in increasing label order are `l:1:0:0`, `s:1`,
`b:0:0`, `b:2:0`, `l:3:0:0`, `s:3`, using [0,5]. The eight highs
are `s:4`, `b:3:0`, `l:2:0:1`, `s:2`, `l:2:0:0`, `l:0:0:0`,
`s:0`, `b:1:0`, using [K+6,K+13]. Each original prefix edge crosses
these classes. Subtracting the smaller label from the larger gives:

| Original edge | Absolute difference |
|---|---:|
| s:3--s:4 | K+1 |
| s:3--b:3:0 | K+2 |
| b:3:0--l:3:0:0 | K+3 |
| s:2--s:3 | K+4 |
| b:2:0--l:2:0:1 | K+5 |
| s:2--b:2:0 | K+6 |
| b:2:0--l:2:0:0 | K+7 |
| s:1--s:2 | K+8 |
| b:0:0--l:0:0:0 | K+9 |
| s:0--b:0:0 | K+10 |
| s:0--s:1 | K+11 |
| s:1--b:1:0 | K+12 |
| b:1:0--l:1:0:0 | K+13 |

These are all four prefix spine edges, four attachments and five
terminal edges, each once. The remaining label interval is R=[6,K+5],
the remaining difference interval is D=[1,K], and the actual existing
port is `s:4=K+6`, one above R.

## Adjacent completion and alpha threshold

For the original path write `w_j=s:(4+j)` for 0<=j<=K. The retained
[above-side adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
starts at the high port `w_0` and alternates taking the lowest unused
label on odd steps and the highest on even steps. After a low step the
current port is just below the residual interval, and after a high
step it is just above it, until the interval is empty. The implementation
uses the retained adjacent helper with start index 4 and all subsequent
sections empty.

On an odd step j=2i+1 the assigned label is 6+i. On a positive even
step j=2i the assigned label is 6+K-i. The denominators in the
equivalent formulas (j-1)/2 and j/2 divide exactly. Write
p=6+ceil(K/2). Odd steps supply [6,p-1] in increasing order and
positive even steps supply [p,K+5] in decreasing order. At K=1
the even block is empty. The blocks partition R. On an odd step,
the predecessor is 6+K-i, including the given port when i=0.
The difference is K-2i. On an even step, the predecessor is
6+i-1 and the difference is K-2i+1. Each equals K-j+1, which
exhausts D in decreasing order. Exactly K assignments suffice,
and they write only the original unassigned suffix vertices.

The full low class consists of the low prefix and odd suffix
vertices and has precisely labels 0..p-1. The full high class
consists of the high prefix and positive even suffix vertices
and has labels p..K+13. Every prefix edge crosses the cut, and
the suffix alternates across it beginning at the high port.
The full labeling is therefore alpha. At K=1, R={6}, D={1},
`s:4=7`, and `s:5=6`, giving difference 1 on the sole unfinished
original edge. The fixed seed below has low-class size 6, whereas
the completed labeling has size p.

## Derivation of the fixed seed at the original cut

Remove only the original edge `s:2--s:3` from the prefix for the
purpose of constructing its labels. The left component B contains
the first three sections. Begin with the published nine-vertex
[B4-111T left component](B4_UNPADDED_111T.md#derivation-on-the-original-cut)
for its K>=2 construction. Its spine values are (7,1,4) and the
three center/leaf pairs are (2,6), (8,0), (3,5). These label 0..8
once, with low class 0..3 and high class 4..8. The actual spine
differences are 6,3 and the attachment and terminal pairs are
(5,4), (7,8), (1,2), exhausting 1..8.

The designated attachment `b:2:0=3` is the largest low label.
Keep the four old low labels, increase the five old high labels
by one, and add the prescribed original leaf `l:2:0:1=4` at
that center. All old edges cross the original classes and their
differences increase to 2..9. The new edge crosses from 3 to 4
and supplies difference 1. The old highs fill 5..9 and the new
high fills 4. In B the spine now has (8,1,5), the first two
center/leaf pairs are (2,7), (9,0), and the third center and
its two named leaves have (3,6,4). Here n_B=10, p_B=4,
`L_B=b:0:0=2` and `U_B=s:2=5` have offsets (2,1).
The actual witness is `b:0:0--s:0--s:1--s:2`. The first leaf
is one step off it, the other centers are one step off it, and
the remaining leaves, including both third-branch leaves, are
two steps off it. This supplies B independently for the exact
larger topology during seed design.

The right component A is the [B4-unit reflected L008 component](B4_UNPADDED_UNIT.md#retained-r241l008-derivation-of-the-fixed-seed).
L008 with q=1 and z=0 gives `s:3=0,l:3:0:0=1,b:3:0=2,s:4=3`.
Reflect low labels by x -> 1-x and high labels by x -> 5-x.
For any high-low difference d=h-l, the result is
(5-h)-(1-l)=4-d. This permutes 1..3 and keeps the two classes.
The new labels on `s:3,s:4,b:3:0,l:3:0:0` are (1,2,3,0).
The actual edges of A give differences 1 on the spine, 2 on
the attachment and 3 on the terminal edge. With n_A=4 and
p_A=2, the actual ports `L_A=s:3=1,U_A=s:4=2` have offsets
(1,0). Their original edge witnesses A, with its center and
leaf at distances one and two. [Pinned L008 archive](../references/upstream/bounded/research__LEMMAS.md.archive.md)
· MDL_Bounded_Search `e48b94eec4091b4fe189e325cab2eda464409943`,
`research/LEMMAS.md`, line 21

The retained R241 rule applies with A right and B left because
x_A=y_B=1. It restores exactly `L_A--U_B=s:3--s:2`, adding
p_B=4 to all A labels and n_A=4 to the B high labels while
keeping B lows fixed. The resulting blocks are B low [0,3],
A low [4,5], A high [6,7], and B high [8,13]. The A spectrum
remains 1..3, the connector gives 9-5=4 and the B spectrum
becomes 5..13. The seed has low-class size 6 and returned
actual ports `b:0:0=2` and `s:4=6` with offsets (2,0).
The two witnesses concatenate along the restored edge. Substitution
gives the displayed prefix with the K terms omitted. Raising its
eight high labels by K shifts each original prefix difference by
exactly K and gives precisely the supplied prefix. This seed is
arithmetic on the original prefix graph `[[1],[1],[2],[1],[]]`.
[Operative retained R241 and adoption](../references/upstream/mdl/N241_relational_ports.md)
· MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md`, lines 4364–4405 and 4488–4505

## Scope

This project corollary uses a prescribed leaf extension at a specific
largest-low vertex and retained R241/L008. The path consumer takes the
already supplied prefix unchanged. The B4-unit branch uses the same
adjacent resource contract with a different seed, and B4-111T has
different branch placements and singleton/nonadjacent contracts.
These results leave other profiles, arbitrary repetition and universal
lobster coverage open. The fixed seed and completed targets have
separate certificates. The proof establishes the quantifier over K,
and the bounded evidence checks the implementation. Historical novelty
is outside the claim.
