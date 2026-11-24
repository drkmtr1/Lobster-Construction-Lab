# D112 — Sign-independent extreme-spine growth

## Conditional theorem

Let T be a finite lobster with m edges, a supplied ordinary graceful labeling f onto `[0,m]` and a specified witnessing spine S. Let u, v and c be distinct actual vertices. The terminal endpoint v of S has predecessor u on S, c lies off S, and the full neighbor set of v is `{u,c}`. Suppose `f(u)=0`, `f(v)=m` and `f(c)=1`. The two distinct incidences at v imply `m≥2`.

Adjoin one fresh named vertex w and the single edge cw. Define `f'(v)=m+1`, `f'(w)=m`, and `f'(x)=f(x)` for every old vertex x other than v. Freshness preserves the original vertex names and designated attachment and spine roles, and makes cw a new incidence of multiplicity one. Every old edge, including uv and vc, keeps its endpoints and multiplicity. The degree of the designated host c increases by one. In particular, a degree-one host is permitted and becomes degree two. The extended graph is connected through c. A cycle through w would require two incident edges at w, and a cycle avoiding w would already be in T. Therefore the extended graph is a tree.

S remains the same named path. Adding a leaf changes no distance among old vertices. Since c is adjacent to v on S and is off S, its distance to S is one. Every path from w to S goes through c, so w has distance exactly two. The old witnessing bound persists and S witnesses the extended lobster.

The old vertices other than v carry exactly `[0,m−1]`. The new vertex w and the raised v carry the distinct labels m and m+1. This gives the disjoint vertex-label partition `[0,m−1] ⊔ {m} ⊔ {m+1}`. The only two old edges incident to the changed label are uv and vc, and the following computations exhaust the changed and fresh incidences.

| Actual incidence | Old weight | New weight |
| --- | ---: | ---: |
| uv | m | m+1 |
| vc | m−1 | m |
| cw | Fresh edge | m−1 |

The old weight bijection leaves exactly `[1,m−2]` on all unchanged edges. The interval is empty when m=2, since the two edges at v then exhaust T. The new edge inventory is the disjoint union `[1,m−2] ⊔ {m−1,m,m+1}`, with every weight occurring once. Thus f' is ordinary graceful.

The same path still ends at v with predecessor u, the neighbors of v are still exactly u and c, and c is still off the path. Their labels are 0, m+1 and 1 at u, v and c respectively, with m+1 the new edge count. These are the original hypotheses at the new size. For any given finite list of distinct fresh terminal names, induct on its length. The empty list leaves the supplied original intact. Each next name is fresh in the current graph, and one application preserves the inventories, spine and prerequisites for the rest. This process terminates after exactly one extension per name. Neither the proof nor the hypothesis uses an alpha separation or a signed-edge condition. This is conditional growth from a supplied input.

## Independently supplied application to ordered [[5,3],[r]]

Use the [D111 construction](ORDINARY_53_2_DIRECT_SEED.md), its [retained certificate](../evidence/validation/LCL_ORDINARY_53_2_DIRECT_SEED_001/result.json) and the [frozen original](../evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json). The original graph digest is `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8` and its raw SHA-256 is `9dbdfd6226c94c821951bc0ca701c18e4a0e1b671324afa84b0431fec36aca0c`. The certificate ledger is `75aaf6544d6832894a567f2a8b07a1bfb3f9a4cf1860f90534044b4c892584d6`. The specified path is `s:0--s:1`, the exit's only neighbors are `s:0` and the off-spine `b:1:0`, and the three labels are 0, 14 and 1 at `s:0,s:1,b:1:0`.

For every exact integer r≥2, the ordered original has two spine vertices, three centers, eight indexed left terminals and r indexed right terminals. The left centers attach to `s:0`, the right center attaches to `s:1`, and every terminal is adjacent to its named center alone. The three center attachments, the spine edge and all terminal edges give `m=r+12`, with `r+13` vertices. The names and roles of the two left groups are fixed, and the right indices are exactly `0..r−1`.

| Vertex or group | Label in the original index order |
| --- | --- |
| `s:0,s:1` | `0,r+12` |
| `b:0:0,b:0:1,b:1:0` | `12,2,1` |
| `l:0:0:0` through `l:0:0:4` | `4,5,6,8,9` |
| `l:0:1:0` through `l:0:1:2` | `3,7,13` |
| `l:1:0:0,l:1:0:1` | `10,11` |
| `l:1:0:k` for `2≤k≤r−1` | `k+12` |

At r=2 the two spine labels, three centers and all three terminal groups agree pointwise with D111. The last row is empty. At quota r, adjoining `l:1:0:r` at `b:1:0` extends its right index interval by exactly one and preserves every existing name, role and edge. The theorem gives this next terminal label m=r+12, raises `s:1` to r+13, and keeps every other label. This is precisely the indexed formula at r+1. The initial and inductive graphs have the same spine and the required exit neighbors throughout.

An independent inventory check uses the following exact partitions. All the fixed labels other than the exit give `[0,13]` once. The indexed new terminals give `[14,r+11]`, and the exit supplies r+12. The following edge groups are disjoint in both incidences and weights.

| Actual incidence group | Absolute differences |
| --- | --- |
| Left attachments in section order | 12, 2 |
| First left terminals in index order | 8, 7, 6, 4, 3 |
| Second left terminals in index order | 1, 5, 11 |
| Right terminals at indices 0 and 1 | 9, 10 |
| Right terminals at indices `2..r−1` | `k+11` in index order, giving `[13,r+10]` |
| Right attachment | r+11 |
| Actual spine edge | r+12 |

The first four rows give `[1,12]` once, and the remaining rows give the rest of `[1,r+12]` once. At r=2, both indexed intervals `[14,r+11]` and `[13,r+10]` are empty. All indexed center and leaf incidence counts follow from the displayed ranges.

The direct algorithm first requires exact integer type and r≥2, rejecting booleans and nonintegers. It then emits the fixed named spine and centers, the fixed left groups and the right group with exactly r indexed leaves, with labels as above. One pass over the right indices terminates with r+13 vertex labels and r+12 incidences, using O(r) indexed output operations. No numeric profile beyond the retained controls is needed for the proof.

Orient from the traversal class of `s:0`. The even class contains the entrance, the right center and all left terminals, and the odd class contains the exit, the left centers and all right terminals. On this application the negative incidences are precisely the three second-left terminal edges directed into center 2 from labels 3, 7 and 13. Their signed differences are −1, −5 and −11. Every other directed difference is positive by the formula, including each newly adjoined edge from 1 to k+12. Thus these signs are consequences throughout this family, and the D108–D110 exclusions retain their single-reversal scopes.

## Relationship to retained results

[D105](ORDINARY_43_2_EXTREME_SPINE.md) and [D106](ORDINARY_43_3_EXTREME_SPINE.md) record the concrete addition from `[[4,3],[2]]` to `[[4,3],[3]]`. The added named terminal is `l:1:0:2` at `b:1:0`, with the same spine and the change `13→14` at `s:1`. These archived data corroborate the local change. [D107](ORDINARY_43R_EXTREME_SPINE.md) already proves the quantified fixed-left `[[4,3],[r]]` supplier and its sole signed reversal using this weight transfer. D112 abstracts and proves the exact local hypotheses independently of the rest of the graph and its signs, then applies them to the separately constructed D111 seed. D107 retains its earlier family and signed conclusion. Arbitrary compatible seed supply, arbitrary left quotas and composition remain separate obligations.
