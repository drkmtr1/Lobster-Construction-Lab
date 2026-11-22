# B3-UNPADDED-K1-001

**Independent AI mathematical review — ACCEPT.** The named formula, direct singleton completion, and R241/L008 derivation agree for every positive integer `q,r,t`. The four previously reviewed branches cover the same family for `K>=2`. This is a project proof review, with no claim of formal verification, human peer review, or historical novelty.

**Independent AI implementation and evidence review — ACCEPT.** The implementation preserves the exact graph and named labels, checks the original singleton edge and both inventories, then verifies the completion against the original graph. The reviewer inspected strict admission, target binding, the separate arithmetic audit, and the saved receipts for precisely 12 targets. [Validation record](../evidence/validation/B3_UNPADDED_K1_001/README.md)

## Original target and labeling

For integers `q,r,t>=1` with zero padding and `K=1`, the exact original profile is `[[q],[r],[t],[],[]]`. There are five spine vertices `s:0,...,s:4`, three centers `b:i:0` attached to `s:i` for `i=0,1,2`, and the original leaves `l:i:0:j` on their own centers in counts `q,r,t`. The four consecutive spine edges, three attachment edges, and `q+r+t` terminal edges give `m=q+r+t+7` edges and `m+1` vertices. The prefix consists of every original vertex except `s:4`. That vertex's only incident edge is the original `s:3--s:4`.

Set `P=q+t+4`. Assign the following prefix labels from the parameters:

```text
b:1:0=0       s:0=1             l:0:0:j=j+2       for 0<=j<q
s:2=q+3       l:2:0:j=q+4+j     for 0<=j<t
b:2:0=P       s:3=P+1           b:0:0=P+2         s:1=P+3
l:1:0:j=P+4+j                  for 0<=j<r
```

The exact prefix contract below assigns `s:4=q+2`. This preserves the original root label `s:0=1` and every named leaf's index.

In the full labeling, the vertex label blocks in order are `{0}`, `{1}`, `[2,q+1]`, `{q+2}`, `{q+3}`, `[q+4,q+t+3]`, `[P,P+3]`, and `[P+4,m]`. The three leaf ranges use one label per index, with lengths `q,t,r` respectively. All blocks are consecutive and disjoint, and the last upper endpoint is `P+4+(r-1)=m`. Thus all vertices receive distinct labels and the full alphabet is `0..m`.

The actual low class consists of `b:1:0,s:0,s:2,s:4` and the first and third branches' leaves. It has `P` vertices labeled `[0,P-1]`. The high class consists of `s:1,s:3,b:0:0,b:2:0` and the middle branch's leaves. It has `r+4` vertices labeled `[P,m]`. Consecutive spine vertices alternate classes, the high first and third centers join only low vertices, and the low middle center joins only high vertices. Every original edge crosses the cut.

## Original-edge differences

| Original edges | Difference calculation | Values |
|---|---|---|
| `b:2:0--l:2:0:j` for `0<=j<t` | `P-(q+4+j)=t-j` | `[1,t]` |
| `s:2--b:2:0` | `P-(q+3)` | `t+1` |
| `s:2--s:3` | `P+1-(q+3)` | `t+2` |
| `s:3--s:4` | `P+1-(q+2)` | `t+3` |
| `s:1--s:2` | `P+3-(q+3)` | `t+4` |
| `b:0:0` to `s:0` and the first leaves | `P+2-x` for neighbor labels `x=1..q+1` | `[t+5,q+t+5]` |
| `s:0--s:1` | `P+3-1` | `q+t+6` |
| `b:1:0` to `s:1` and the middle leaves | Neighbor labels `P+3..m` minus zero | `[q+t+7,m]` |

The table lists every original edge once. Within each indexed group the values vary injectively, and the groups partition `1..m` consecutively. This and the vertex partition prove alpha gracefulness.

At `q=1` the first leaf has label 2 and its star uses the two differences `t+5,t+6`. At `r=1` the middle leaf is labeled `m=q+t+8` and its star uses the two differences `m-1,m`. At `t=1` the single third leaf has label `q+4` and its edge has difference 1. When all three minima coincide, `P=6` and `m=10`. The spine labels are `1,9,4,7,3`, the center labels are `8,0,6`, and the leaves in section order have labels `2,10,5`. The table then gives the four singleton values immediately after 1, the first-star range `6..7`, the edge of difference 8, and the middle-star range `9..10`. The formulas use only positivity and their own branch indices. The comparisons between branch sizes used in earlier suppliers play no role in this proof.

## Singleton completion

Omit only `s:4` from the label partition and omit only the row for `s:3--s:4` from the difference partition. The original prefix labels the other `m` vertices and gives `m-1` distinct prefix differences. The unused sets are exactly `R={q+2}` and `D={t+3}`, and the physical port is `s:3=q+t+5`. Since `|(q+t+5)-(q+2)|=t+3`, placing the unused label on the original `s:4` uses the unused difference and preserves every prefix label. The construction consists of finite leaf loops and the single terminal assignment. The explicit formulas determine the prefix from parameters before completion.

The adjacent interval predicate at `K=1` requires `D={1}` and an adjacent port. Here the missing difference and port-to-label distance are both `t+3>=4`. The nonadjacent path consumer requires its own supplied boundary and `K>=2`. The earlier [B2 singleton](B2_UNPADDED_K1.md) uses `R={q+4}`, `D={q+3}`, and `s:2=1` on a different original graph.

## R241 derivation on the same named graph

Cut the original edge `s:1--s:2`. The left component B contains `s:0,s:1` and their attached branches. The right component A contains `s:2,s:3,s:4` and the third branch. They partition the exact target vertices.

### Independent component B

Set `n_B=q+r+4` and `p_B=q+2`. Give `b:1:0,s:0,l:0:0:j` the labels `0,1,j+2`, so the low class occupies `[0,q+1]`. Give `b:0:0,s:1,l:1:0:j` the labels `q+2,q+3,q+4+j`, so the high class occupies `[q+2,q+r+3]`. Each leaf's range is the original index range. The first star sees neighbor labels `1..q+1` at center `q+2`, so its differences are `[1,q+1]`. The edge `s:0--s:1` gives `q+2`. The middle star sees neighbor labels `q+3..q+r+3` at center zero, giving exactly those differences. This is the original component's full spectrum `1..n_B-1`, and all its edges cross the displayed classes. The actual ports are `L_B=s:0` with `x_B=1`, and `U_B=s:1` with `y_B=(q+3)-p_B=1`. The original path `s:0--s:1` witnesses B, because each attached vertex is at distance at most two from it.

### Independent component A from L008 and the original last vertex

Use the zero-padding instance of L008 with branch size `t` on the original subgraph through `s:3`. It gives `s:2=0`, `l:2:0:j=j+1`, `b:2:0=t+1`, and `s:3=t+2`. Its branch leaf differences are `1..t`, its branch attachment has difference `t+1`, and its original edge `s:2--s:3` has difference `t+2`. Thus the required actual attachment vertex `s:3` has the maximum label `t+2`. [Retained L008](../references/upstream/bounded/research__LEMMAS.md.archive.md) · [Pinned source, line 21](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md#L21) · source blob `f942e3b8b7628353ef7cf9d8cf53759c2eed0478`

Translate each old label by one. The old edge differences stay `1..t+2`. Assign the original `s:4` label zero and include its original edge to `s:3`, now at `t+3`. This edge supplies precisely the missing maximum difference `t+3`. The extension relies on the supplied maximum-labeled attachment vertex. In A the low vertices `s:4,s:2,l:2:0:j` have labels `0,1,j+2` and cover `[0,t+1]`. The high vertices `b:2:0,s:3` have labels `t+2,t+3`. Every edge, including the last edge, crosses the cut. Thus `n_A=t+4`, `p_A=t+2`, and A is alpha graceful. The actual ports are `L_A=s:2` with `x_A=1`, and `U_A=s:3` with `y_A=(t+3)-p_A=1`. The path `s:2--s:3` witnesses the component. The third branch's leaves lie at distance two and the original `s:4` lies at distance one.

### Composition and physical ports

The retained R241 binary rule requires `x_A=y_B`, which holds here with both equal to 1. Its connector `L_A--U_B` is exactly the cut edge `s:2--s:1`. Add `p_B=q+2` to every A label, leave the B low labels fixed, and add `n_A=t+4` to the B high labels. The resulting four label blocks in order are B low `[0,q+1]`, A low `[q+2,q+t+3]`, A high `[P,P+1]`, and B high `[P+2,m]`. In particular A's `s:4=0` becomes `q+2`, and A's `s:2`, third leaves, `b:2:0`, and `s:3` become `q+3,q+4+j,P,P+1`. B's first and middle low vertices retain their prescribed labels. B's high vertices `b:0:0,s:1,l:1:0:j` become `P+2,P+3,P+4+j`. These are precisely the full formula. A's differences stay `1..t+3`, the restored edge gives `t+4`, and B's cross-class differences gain `t+4` to give `[t+5,m]`.

The returned ports are the actual `L_B=s:0` and `U_A=s:3` at labels `1` and `P+1=q+t+5`. The combined low class size is `p_A+p_B=P`, and the output offsets are `(1,1)`. The two component witnesses and the actual restored edge give the full witnessing path `s:0--s:1--s:2--s:3`. The original `s:4` remains attached at distance one from its last vertex. This project corollary uses the retained composition, the directly proved left supplier, and the explicitly proved extension of the L008 component. The original pending source header is superseded for the adopted scope. [Retained N241](../references/upstream/mdl/N241_relational_ports.md) · [Pinned R241 proof](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [Pinned adoption](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4488-L4505) · source blob `faca17cfa4c484127413762adc0c36b771a18f71`

## Deterministic selection for every positive path length

On `[[q],[r],[t]]+[[]]*(K+1)` for positive integers `q,r,t,K`, use the first applicable row below. For the `K>=2` rows set `a=q+t+3`. Each of those rows supplies `R=[a,a+K-1]` and `D=1..K`.

| Condition | Constructor | Physical port and completion |
|---|---|---|
| `K=1` | `three_section_k1(q,r,t)` | `s:3=q+t+5`, direct singleton `R={q+2},D={t+3}` |
| `K>=2, q>=r` | `three_section_nonadjacent(q,r,t,K)` | `s:3=a+K+1`, nonadjacent |
| `K>=2, q<r, t<=q+1` | `three_section_qltr_adjacent(q,r,t,K)` | `s:3=a+K`, adjacent |
| `K>=2, q<r, t>=q+2, r>=3` | `three_section_qltr_large_t(q,r,t,K)` | `s:3=a+K+1`, nonadjacent |
| `K>=2, q=1, r=2, t>=3` | `three_section_q1_r2(t,K)` | `s:3=a+K+1`, nonadjacent |

For `K>=2`, the last row follows after the preceding three are excluded: `q<r<3` forces `q=1,r=2`, and `t>=q+2` forces `t>=3`. The rows exhaust the exact original family and each completion gives an ordinary graceful labeling. The adjacent supplier retains its earlier `K=1` boundary on its own domain. The selection above always chooses the new singleton constructor at `K=1`. Padding, multiple positive branches per section, further branched sections, and arbitrary repetition remain separate. [Accepted four-case selection proof](B3_UNPADDED_Q1_R2.md#coverage-and-deterministic-constructor-selection)
