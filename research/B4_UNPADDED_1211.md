# B4-UNPADDED-1211-001

For every integer `K>=1`, the exact original unpadded profile
`[[1],[2],[1],[1]]+[[]]*(K+1)` has a direct alpha graceful labeling.
The constructor excludes booleans.

## Exact graph and supplied prefix

The spine has K+5 vertices `s:0,...,s:(K+4)`. The four centers
`b:i:0` attach to their respective `s:i`. There are five terminal
leaves, including `l:1:0:0` and `l:1:0:1`, both incident to
`b:1:0`. The K+4 spine edges, four attachments and five terminal
edges give m=K+13. The prefix contains 14 vertices and 13 edges,
including all four branches and the spine through `s:4`.
Only `s:5,...,s:(K+4)` are unassigned. Their incident edges are
the K consecutive original spine edges from `s:4`, with sole
prefix-crossing edge `s:4--s:5`.

| Named vertices in order | Labels in order |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+13,2,K+10,6,K+7 |
| b:0:0,l:0:0:0 | 0,K+12 |
| b:1:0,l:1:0:0,l:1:0:1 | K+9,3,4 |
| b:2:0,l:2:0:0 | 1,K+11 |
| b:3:0,l:3:0:0 | K+8,5 |

The low vertices, in label order, are `b:0:0`, `b:2:0`, `s:1`,
`l:1:0:0`, `l:1:0:1`, `l:3:0:0`, `s:3`, using [0,6].
The highs are `s:4`, `b:3:0`, `b:1:0`, `s:2`, `l:2:0:0`,
`l:0:0:0`, `s:0`, using [K+7,K+13]. Each prefix edge crosses
these disjoint classes. Subtraction on the original incidences gives:

| Original edge | Difference |
|---|---:|
| s:3--s:4 | K+1 |
| s:3--b:3:0 | K+2 |
| b:3:0--l:3:0:0 | K+3 |
| s:2--s:3 | K+4 |
| b:1:0--l:1:0:1 | K+5 |
| b:1:0--l:1:0:0 | K+6 |
| s:1--b:1:0 | K+7 |
| s:1--s:2 | K+8 |
| s:2--b:2:0 | K+9 |
| b:2:0--l:2:0:0 | K+10 |
| s:0--s:1 | K+11 |
| b:0:0--l:0:0:0 | K+12 |
| s:0--b:0:0 | K+13 |

All four prefix spine edges, four attachments and five leaf edges
occur once. Thus R=[7,K+6], D=[1,K], and the existing physical
port is `s:4=K+7`, just above R.

## Adjacent suffix and completed alpha classes

Write `w_j=s:(4+j)` for 0<=j<=K. Starting at the high physical
port, the retained [above-side adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
takes the low endpoint at odd steps and the high at even steps.
Each low step puts the new port immediately below the remaining
interval and each high step puts it immediately above. There is
no remaining interval after the Kth assignment. The existing
`_consume_suffix` runs from index 4 on this branch-free suffix
and writes only `w_1,...,w_K`.

On odd steps j=2i+1 the label is 7+i and on positive even steps
j=2i it is 7+K-i. Put p=7+ceil(K/2). The odd steps use [7,p-1]
once in increasing order and the even steps use [p,K+6] once in
decreasing order. They partition R, with the even block empty
at K=1. The predecessor of an odd step is 7+K-i, including
the port at i=0, so the difference is K-2i. The predecessor
of an even step is 7+i-1, so the difference is K-2i+1. Each
gives K-j+1, exhausting D in descending order without changing
the prefix. The low prefix plus odd suffix uses 0..p-1 and
the high prefix plus positive even suffix uses p..K+13. The
path alternates across that cut from its high start and the
prefix edges already cross it. The complete labeling is alpha.

At K=1, R={7}, D={1}, `s:4=8`, `s:5=7`. The original last edge
uses difference 1. The completed low-class size is 8. The
fixed seed has low-class size 7.

## R241 derivation on the original cut

Cut the original edge `s:2--s:3` in the fixed prefix. For left
component B begin with the published [B4-unit left component](B4_UNPADDED_UNIT.md#retained-r241l008-derivation-of-the-fixed-seed).
Its spine labels are (8,2,5), with center/leaf pairs (0,7),
(6,1), (3,4). Their alpha classes use 0..3 and 4..8. Its
spine differences are (6,3), and branch attachment/terminal
pairs are (8,7), (4,5), (2,1), exhausting 1..8.

On the same named graph exchange `b:1:0` with `l:2:0:0` in label
only (6 and 4) and exchange `l:1:0:0` with `b:2:0` in label only
(1 and 3). Each exchange stays within its own alpha class.
Afterward the branch-1 pair is (2,1) and branch-2 pair is (4,5).
All spine and branch-0 differences are unchanged, so the
relabeling is still alpha graceful. The actual `b:1:0` has
the minimum high label 4.

Raise all five old highs by one, leaving 0..3 fixed. All old
differences gain one to fill 2..9. Place label 4 on the original
second middle leaf `l:1:0:1`, at `b:1:0=5`, which gives the
new difference 1. The classes are now 0..4 and 5..9. The
resulting B has spine (9,2,6), branch-0 pair (0,8), branch-1
center and named leaves (5,3,4), and branch-2 pair (1,7).
Here n_B=10, p_B=5, `L_B=b:0:0=0`, and `U_B=s:2=6`.
The new exit offset is 6-5=1, the same as the previous 5-4.
The actual witness is `b:0:0--s:0--s:1--s:2`. The branch-0 leaf
and the other centers are one edge away, and both middle leaves
and the branch-2 leaf are two edges away. This extends at a
minimum-high center and enlarges the low class, whereas the
[B4-1121 extension](B4_UNPADDED_1121.md#derivation-of-the-fixed-seed-at-the-original-cut)
used a largest-low center and enlarged the high class.

Right component A is L008 at q=1, z=0, with `s:3=0,l:3:0:0=1`,
`b:3:0=2,s:4=3` before reflecting. The low map x -> 1-x and
high map x -> 5-x transform the difference h-l into
(5-h)-(1-l)=4-(h-l), permuting 1..3. The resulting labels on
`s:3,s:4,b:3:0,l:3:0:0` are (1,2,3,0). The spine,
attachment and terminal edges give 1, 2, 3. With n_A=4 and
p_A=2, the offsets of the actual ports `L_A=s:3,U_A=s:4`
are x_A=1 and y_A=0. The original edge `s:3--s:4` witnesses A
with the center and leaf one and two edges away. [Retained L008](../references/upstream/bounded/research__LEMMAS.md.archive.md)
· MDL_Bounded_Search `e48b94eec4091b4fe189e325cab2eda464409943`,
`research/LEMMAS.md`, line 21

Apply R241 to A and B at x_A=y_B=1, restoring exactly
`L_A--U_B=s:3--s:2`. Add p_B=5 to A, leave B lows fixed and
add n_A=4 to B highs. The blocks are B low [0,4], A low [5,6],
A high [7,8], B high [9,13]. The difference blocks are A's
1..3, the connector difference (6+4)-(1+5)=4, and B's 5..13.
The witnesses concatenate along the restored edge. The combined
low-class size is 7 and the actual returned ports are
`b:0:0=0` and `s:4=7` with offsets (0,0). The resulting labels
are exactly the table with K terms omitted. This is a fixed
seed on the prefix graph `[[1],[2],[1],[1],[]]`. Raising its
seven high labels by K increases every original prefix
difference by K and gives precisely the displayed supplier.
[Retained R241 and disposition](../references/upstream/mdl/N241_relational_ports.md)
· MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md`, lines 4364–4405 and 4488–4505

## Scope

This is a project corollary of the retained composition with a
directly checked local relabeling and prescribed leaf extension.
The public constructor starts at K=1. Seed design supplies the
prefix before consumption, which preserves it. The proof concerns
only the stated ordered zero-padding profile. Other profiles,
arbitrary transitions, arbitrary repetition, historical novelty,
and universal lobster coverage are outside this claim.
