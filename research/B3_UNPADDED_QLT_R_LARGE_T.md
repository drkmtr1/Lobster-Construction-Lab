# B3-UNPADDED-QLT-R-LARGE-T-001

**Independent AI mathematical review: ACCEPT** on the stated domain. The review checked the definition on every named vertex, the full label and difference partitions including empty groups, the shift of the high class, and the exact original path continuation. The mathematical review is separate from the implementation and evidence review. The finding makes no claim of historical novelty, human peer review, or formal verification.

**Independent AI implementation and evidence review: ACCEPT** on the same domain. The reviewer checked named assignments, strict direct and CLI admission, the exact path from `s:3`, prefix preservation, and original-target verification. The saved seed, partial and full certificates and the separate arithmetic audit agree on the 12 declared targets. [Validation record](../evidence/validation/B3_UNPADDED_QLT_R_LARGE_T_001/README.md)

## Original target and seed

Take integers `1<=q<r`, `r>=3`, `t>=q+2`, and `K>=2`, excluding booleans. The zero-padding profile is `[[q],[r],[t]]+[[]]*(K+1)` in the declared order. The spine vertices `s:0,...,s:(K+3)` have their consecutive edges. A center `b:i:0` is attached to `s:i` for `i=0,1,2`, and each center is joined to its own named terminal leaves, of counts `q,r,t` in that order. There are `K+4` spine vertices, three centers and `q+r+t` leaves. The prefix through `s:3` contains all branches and has `M+1` vertices and `M=q+r+t+6` edges. The whole graph has `m=M+K` edges and `m+1` vertices. The unassigned vertices `s:4,...,s:(K+3)` have exactly the original consecutive `K`-edge path from `s:3` as their incident edges, and the sole edge crossing the boundary is `s:3--s:4`.

Put `H=q%2`, `J=(q-H)//2`, `a=q+t+3`, and `d=t-H`. In particular `q=2J+H` and `a=d+2H+2J+3`. Assign the seed `h` by the following named formulas. Each branch's index ranges are disjoint and cover its own leaves.

```text
b:1:0 = 0                    s:0 = 2H+2             s:2 = 2H+2J+3
b:2:0 = a                    s:3 = a+1              b:0:0 = a+2
s:1   = a+2H+4

l:0:0:j = 2j+1                 for 0 <= j < J
l:0:0:j = 2(j-J+1)             for J <= j < J+H
l:0:0:j = 2H+4+2(j-J-H)        for J+H <= j < q

l:1:0:j = a+3+j                for 0 <= j < 2H+1
l:1:0:j = a+4+j                for 2H+1 <= j < r

l:2:0:j = 2J+1+2j              for 0 <= j <= H
l:2:0:j = q+j+3                for H+1 <= j < t
```

The parity parameters are determined by `q`. The selected domain makes the middle and third index breaks valid because `r>=2H+1` and `t>=H+1`. The named ordering is part of the formula.

## Seed label partition

The odd first leaves use the `J` odd labels from `1` through `2J-1`. The `H+1` early third leaves continue the odd sequence from `2J+1` through `2J+2H+1`. The even first leaves use `2,4,...,2H` and `2H+4,2H+6,...,2H+2J+2`, with respective counts `H` and `J`. The value `s:0=2H+2` fills their gap. The odd and even blocks therefore occupy `1..2J+2H+2`, with every label used once. The center `b:1:0` gives `0`, `s:2` gives the next label `2J+2H+3`, and the late third leaves fill `[2J+2H+4,q+t+2]`. This proves that `s:0`, `s:2`, `b:1:0` and the first and third leaves use exactly `[0,a-1]`.

The centers `b:2:0` and `b:0:0`, with `s:3`, use `a,a+2` and `a+1`, respectively. The two middle leaf blocks use `[a+3,a+2H+3]` and `[a+2H+5,a+r+3]`. The fixed value `s:1=a+2H+4` fills their gap, so these `r+1` vertices use `[a+3,M]` because `M=a+r+3`. Thus `s:1`, `s:3`, `b:0:0`, `b:2:0` and the middle leaves occupy `[a,M]`. The two classes are disjoint and each block is injective. Their counts `a` and `r+4` sum to `M+1`, accounting for every original prefix vertex.

When `H=0`, the block of `H` even first leaves is empty, `s:0=2`, only one third leaf is early, and only one middle leaf precedes the label at `s:1`. When `J=0`, `q=1` and `H=1`, so the first odd and last even blocks are both empty. The remaining first leaf has label `2`, and `s:0=4` fills the even set `2,4`. The early third leaves supply `1,3`. This case requires no inequality such as `H<=J`. At `r=2H+1`, the second middle block is empty and `s:1=M`. For every larger `r`, the fixed `s:1=a+2H+4` stays in place and the second middle block extends to the new `M`.

## Original seed edge partition

Every original prefix edge joins a low and a high vertex. The spine classes in order from `s:0` to `s:3` are low, high, low, high. The first and third centers are high and meet only low neighbors, and the middle center is low and meets only high neighbors. The difference of each edge is its high label minus its low label.

| Original edge group | Direct difference calculation | Values |
|---|---|---|
| `b:2:0--l:2:0:j`, `H+1<=j<t` | `a-(q+j+3)=t-j` | `[1,d-1]` |
| `s:2--b:2:0` | `a-(2H+2J+3)` | `d` |
| `s:2--s:3` | `a+1-(2H+2J+3)` | `d+1` |
| `b:0:0` to its even first leaves and `s:0` | `a+2` minus each even label from `2` through `2H+2J+2` | `{d+3,d+5,...,a}` |
| `b:2:0--l:2:0:j`, `0<=j<=H` | `a-(2J+1+2j)=d+2H+2-2j` | `{d+2,d+4,...,d+2H+2}` |
| `s:1--s:2` | `a+2H+4-(2H+2J+3)` | `d+2H+4` |
| `b:0:0` to its odd first leaves | `a+2-(2j+1)` for `0<=j<J` | `{d+2H+6,d+2H+8,...,a+1}` |
| `s:0--s:1` | `a+2H+4-(2H+2)` | `a+2` |
| `b:1:0` to `s:1` and every middle leaf | Its neighbors' labels minus `0` | `[a+3,M]` |

The early third group ends at `d+2H+2`, then `s:1--s:2` takes `d+2H+4`. When `J>0`, the odd first leaf group starts at `d+2H+6` and ends at `a+1=d+2H+2J+4`. At `J=0`, that group is empty and the edge `s:1--s:2` itself takes `a+1`. The three groups together give the full progression from `d+2` to `a+1` by twos. The other progression from `d+3` to `a` fills each intervening value. They are disjoint and give exactly `[d+2,a+1]`. Combining the other groups gives `[1,d-1]`, then `d,d+1`, then this interleaved interval, then `a+2` and `[a+3,M]`. Each labeled group is injective, and the rows account for the three spine edges and all branch attachments and terminal edges exactly once. This proves difference multiplicity one on `1..M`. Along with the label partition and cross-class incidences, this proves the seed is an alpha labeling of the original prefix.

## Shift and nonadjacent continuation

Keep the low labels and add `K` to the entire high class. The high interval moves from `[a,M]` to `[a+K,m]`, while the low interval stays `[0,a-1]`. Every prefix edge crosses the alpha classes, so its difference increases by exactly `K` and the shifted differences are `[K+1,m]`. The original physical port `s:3` moves from `a+1` to `a+K+1`. The unused labels are `[a,a+K-1]` and the unused differences are `1..K`. The port is two above the upper end of the interval, so it is a nonadjacent state under the existing boundary definitions.

Use the normalized path sequence `C_K=(c_0,...,c_K)` with `C_2=(3,1,0)`, `C_3=(4,1,0,2)`, and `C_4=(5,1,2,0,3)`. The bases each start at `K+1`, use the other values `0..K-1` once, and have consecutive absolute differences `1..K` once. If `K>=5` and `C_(K-3)=(K-2,x_1,...,x_(K-3))`, set

```text
C_K = (K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3)).
```

The reflected entries `K-2-x_i` use `2..K-2` once by induction, and the newly inserted `1,K-1,0` complete the other entries. The first three differences are `K,K-2,K-1`. Reflection maps the old starting value `K-2` to the new `0`, so the edge leaving `0` and all following edges reproduce the old differences `1..K-3` once, including the edge to the first reflected entry. Recursion decreases `K` by three to a base. This is the retained recurrence, expressed for the present physical graph. [Nonadjacent path proof](B2_NONADJACENT_CONSUMER.md#construction-and-proof)

Translate by `a` and place `a+c_i` on `s:(3+i)` for `1<=i<=K`. The initial value `a+c_0` is the already assigned `s:3=a+K+1`. Translation preserves the consecutive differences, the suffix covers exactly `[a,a+K-1]`, and the assignment leaves all prefix labels intact. The completed named graph has labels `0..m` and edge differences `1..m` once each. At `K=1` this same boundary would force the last edge to join `a+2` and `a`, giving difference `2` when the unused difference is `1`. The restriction is on this boundary; ordinary gracefulness for other interfaces remains a separate question.

## Relationship to the accepted B3 suppliers

This formula independently supplies labels from the given parameters by the direct alpha and original-edge argument above. It has no input from a solver, a seed search, or a successful whole-target labeling. The earlier `q>=r` and `q<r, t<=q+1` formulas were derived by R241 component composition with L008 or a class-reversed L008 labeling. The present formula uses the same high-class shift and nonadjacent path recurrence as the earlier `q>=r` branch, and the earlier adjacent branch retains its adjacent port. [R241-based nonadjacent B3 proof](B3_UNPADDED_QGE_R.md) · [R241-based adjacent B3 proof](B3_UNPADDED_QLT_R_ADJACENT.md)

For odd `q`, `r>=2H+1` means `r>=3`. Among positive `q<r`, the only pair excluded by that bound is `(q,r)=(1,2)`. At that pair the displayed formula puts `s:1=a+6` above `M=a+5`, which is outside this supplier's admission. The project result and constructor are limited to the selected domain even where algebraic conditions are weaker. The formula establishes no nongracefulness result for excluded parameters.

For `K>=2`, the three suppliers together cover every positive integer `q,r,t` except `q=1,r=2,t>=3`. Specifically, `q>=r` uses the original nonadjacent B3 branch for every `t>=1`. The region `q<r,t<=q+1` uses the adjacent B3 branch, which also covers `K=1`. The remaining region `q<r,t>=q+2` with `r>=3` uses the present nonadjacent B3 branch. The uncovered region is a calculation of supplier coverage. `K=1` outside the adjacent branch, padding, additional positive branches, further sections, and arbitrary repetition remain separate obligations.
