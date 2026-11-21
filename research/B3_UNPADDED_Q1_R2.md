# B3-UNPADDED-Q1-R2-001

**Independent AI mathematical review: ACCEPT** on the stated domain. The review checked the exact original incidences, both seed label intervals, every seed difference, the prescribed leaf extension, the high-side shift, the physical suffix, and the four-case coverage argument. The proof supplies this family directly from its parameters. Evidence checks the stated cases, with no claim of formal verification, human peer review, or historical novelty.

**Independent AI implementation and evidence review: ACCEPT** on the same domain. The reviewer checked exact integer admission, fixed branch counts, the separate assignment to `l:2:0:0`, seed and shifted inventories, suffix indexing and prefix preservation. The reviewer checked that the one base-prefix certificate is separate from the 12 completed-target certificates and their arithmetic audit. [Validation record](../evidence/validation/B3_UNPADDED_Q1_R2_001/README.md)

## Original target and seed

Fix `q=1,r=2`, zero padding, and integers `t>=3,K>=2`. The target is `[[1],[2],[t]]+[[]]*(K+1)`. It has `K+4` consecutive spine vertices `s:0,...,s:(K+3)`, three centers `b:i:0` joined to `s:i` for `i=0,1,2`, and the original named terminal leaves of counts `1,2,t` at those centers. There are `m=t+K+9` edges: `K+3` spine edges, three center attachments, and `t+3` terminal edges. The prefix through `s:3`, including all branches, has `M+1=t+10` vertices and `M=t+9` edges. The unassigned vertices are exactly `s:4,...,s:(K+3)`. Their incident edges are exactly the original `K` consecutive edges starting at `s:3`, with `s:3--s:4` the only edge crossing from assigned to unassigned vertices.

Put `a=t+4`. For the seed lemma allow every integer `t>=1`. The same named assignment gives

```text
s:0 = 0       l:0:0:0 = 1      l:2:0:0 = 2      b:1:0 = 3      s:2 = 4
l:2:0:j = j+4 for 1 <= j < t
b:2:0 = a     s:3 = a+1        l:1:0:0 = a+2    l:1:0:1 = a+3
b:0:0 = a+4   s:1 = a+5 = M
```

The five fixed low labels are `0..4`, and the `t-1` later third leaves occupy `5..t+3`, an empty interval at `t=1`. These disjoint groups give the actual low class `[0,a-1]` with `a=t+4` vertices. The six displayed high labels give `[a,M]`. Both classes are injectively labeled, their intervals are disjoint and exhaust `0..M`, and the counts total `a+6=M+1`. The spine classes from `s:0` through `s:3` alternate low, high, low, high. The first and third centers are high and are joined to low spine vertices and low leaves. The middle center is low and joins a high spine vertex and high leaves. These are all original prefix edges, so each crosses the alpha cut and has difference given by high minus low.

| Original prefix edge | Difference from the formula | Values |
|---|---|---|
| `b:2:0--l:2:0:j` for `1<=j<t` | `a-(j+4)=t-j` | `1..t-1` |
| `s:2--b:2:0` | `a-4` | `t` |
| `s:2--s:3` | `a+1-4` | `t+1` |
| `b:2:0--l:2:0:0` | `a-2` | `t+2` |
| `b:1:0--l:1:0:0` | `a+2-3` | `t+3` |
| `b:1:0--l:1:0:1` | `a+3-3` | `t+4` |
| `s:1--s:2` | `a+5-4` | `t+5` |
| `s:1--b:1:0` | `a+5-3` | `t+6` |
| `b:0:0--l:0:0:0` | `a+4-1` | `t+7` |
| `s:0--b:0:0` | `a+4-0` | `t+8` |
| `s:0--s:1` | `a+5-0` | `t+9=M` |

The first row varies injectively over its interval. Its `t-1` edges and the ten singleton rows account for all `M` edges exactly once. The difference blocks are disjoint and exhaust `1..M`. This proves the seed lemma on the original prefix for every `t>=1`.

## Fixed seed and conditional leaf extension

At `t=1` the seed graph is `[[1],[2],[1],[]]`, with 11 vertices and ten edges. Its labels are

```text
s:0=0  s:1=10  s:2=4  s:3=6
b:0:0=9  b:1:0=3  b:2:0=5
l:0:0:0=1  l:1:0:0=7  l:1:0:1=8  l:2:0:0=2
```

The first row of the difference table is empty, and the ten singleton rows give `1..10` in order. The least high vertex is the actual third center `b:2:0=5`, and the actual port `s:3=6` has offset one from it.

The transport requires an independently supplied alpha labeling with low interval `[0,L-1]`, high interval `[L,U]`, and the prescribed attachment vertex labeled `L`, the least high value. To attach `delta>=0` new leaves at that vertex, keep the low labels, increase all old high labels by `delta`, and assign the new leaves the interval `[L,L+delta-1]`. Every old difference increases by `delta`, from `1..U` to `delta+1..U+delta`, because every old edge crosses classes. The shifted attachment has label `L+delta`, so the new leaf edges use exactly `1..delta`. The old high labels now start at `L+delta`. Relative offsets among high vertices remain fixed. This calculation relies on the actual attachment vertex being least high.

Apply it with `L=5,U=10,delta=t-1`. Keep the five old low labels. Shift the six old high labels into `[t+4,t+9]` and place the prescribed new third leaves at `l:2:0:j=j+4` for `1<=j<t`. These labels fill `[5,t+3]` in original index order. Old differences become `[t,t+9]`, new differences are `[1,t-1]`, and the actual coordinates remain `b:2:0=a`, `s:3=a+1`. At `t=1` the extension adds no labels or edges. This independently recovers the direct formula for the whole seed family. Its justification here is the displayed fixed seed and arithmetic of the prescribed extension.

## High-side shift and original-path continuation

Keep low labels and shift the six high labels by `K`. The prefix now has

```text
s:0=0           s:1=t+K+9        s:2=4            s:3=t+K+5
b:0:0=t+K+8     b:1:0=3          b:2:0=t+K+4
l:0:0:0=1       l:1:0:0=t+K+6    l:1:0:1=t+K+7   l:2:0:0=2
l:2:0:j=j+4 for 1<=j<t
```

The shifted high interval is `[a+K,m]` and the low interval is `[0,a-1]`. Every original prefix difference rises by `K`, giving `[K+1,m]`. Thus the unused vertex labels are exactly `[a,a+K-1]`, the unused differences are `1..K`, and the physical port is `s:3=a+K+1`. It lies two above the last unused label, so the adjacent predicate rejects this boundary.

Use the retained normalized sequence `C_K`. For `K=2,3,4`, the sequences `(3,1,0)`, `(4,1,0,2)` and `(5,1,2,0,3)` have initial value `K+1`, suffix labels `0..K-1` and consecutive differences `1..K`, each once. For `K>=5`, the recurrence starts with `K+1,1,K-1,0` and appends the reflection `K-2-x_i` of the suffix of `C_(K-3)`. Inductively the appended labels are exactly `2..K-2`, so the normalized suffix is a bijection onto `0..K-1`. The first three edges give `K,K-2,K-1`. The reflection sends the old initial value `K-2` to the new `0`, so the bridge from `0` to the reflected suffix and the following edges give exactly the old differences `1..K-3`. Decreasing `K` by three reaches a base in finitely many steps. [Retained nonadjacent path proof](B2_NONADJACENT_CONSUMER.md#construction-and-proof)

If `C_K=(c_0,...,c_K)`, assign `s:(3+i)=a+c_i` for `1<=i<=K`. The initial value `a+c_0` agrees with the existing label at `s:3`. Translation preserves differences, the original path uses each unused label and difference once, and the prefix remains fixed. The completed original target is graceful. At `K=1` this contract would leave `a` as the only label for the edge from `a+2`, so that edge would have difference 2 while the only unused difference would be 1. This is a restriction of the contract.

The publicly selected construction is `three_section_q1_r2(t,K)` for integer `t>=3,K>=2`, with zero padding and the named branch counts `(1,2,t)`. The seed lemma includes `t=1,2` without expanding that public domain. The fixed `t=1` certificate concerns the base prefix. The 12 completed-target certificates and their audit corroborate the proof within their declared bounds.

## Coverage and deterministic constructor selection

Take any integers `q,r,t>=1` and `K>=2` with the exact zero-padding profile `[[q],[r],[t]]+[[]]*(K+1)`. Set `a=q+t+3`. Select the first applicable row. Each returns unused labels `[a,a+K-1]` and differences `1..K` on the original graph.

| Case | Constructor | Physical port and consumer |
|---|---|---|
| `q>=r` | [`three_section_nonadjacent(q,r,t,K)`](B3_UNPADDED_QGE_R.md) | `s:3=a+K+1`, nonadjacent |
| `q<r` and `t<=q+1` | [`three_section_qltr_adjacent(q,r,t,K)`](B3_UNPADDED_QLT_R_ADJACENT.md) | `s:3=a+K`, adjacent |
| `q<r`, `t>=q+2` and `r>=3` | [`three_section_qltr_large_t(q,r,t,K)`](B3_UNPADDED_QLT_R_LARGE_T.md) | `s:3=a+K+1`, nonadjacent |
| `q=1,r=2,t>=3` | `three_section_q1_r2(t,K)` | `s:3=a+K+1`, nonadjacent |

The rows are disjoint. Once `q>=r` and `t<=q+1` are excluded, the parameters satisfy `q<r` and `t>=q+2`. If `r>=3` also fails, positivity gives `r=2,q=1` and `t>=3`. Each row supplies the hypotheses of its own consumer. Consequently every exact original profile in this parameter range is graceful. The first and third branches share the nonadjacent continuation with this fourth branch. The adjacent branch retains its own boundary and also applies at `K=1` on its original domain. Other `K=1` cases, padding, multiple positive branches per section, further sections, and arbitrary repetition remain separate.
