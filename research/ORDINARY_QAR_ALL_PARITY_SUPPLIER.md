# D117 — All-parity ordinary graceful supply for three independent quotas

For every independently chosen pair of exact integers q≥5 and a≥3 and every exact integer r≥2, ordered `[[q,a],[r]]` has a direct ordinary graceful labeling with `s:0=0`, `s:1=m`, `b:1:0=1` and `m=q+a+r+4`. The construction has no alpha or internal signed-edge restriction. Write `n=q+a+6` for the seed edge count. Thus `m=n+r−2`. All left labels and seed resources below are computed using n.

## Named seed and its independent core

The spine is `s:0--s:1`. The left centers `b:0:0,b:0:1` attach to `s:0` and the right center `b:1:0` to `s:1`. Each of the q, a and r terminals at those centers has a distinct original name `l:i:j:k`, with index k starting at zero, and a single edge to its own center. The original graph is connected and acyclic because each center or terminal joins the earlier tree by just one edge. It has `q+a+r+5=m+1` vertices and m edges including the spine and three attachments. The named spine witnesses distance one for every center and exactly two for every terminal. The seed is the same named original with r=2, having n edges.

Select `b:0:0` as the numerical lower host if q is even and `b:0:1` otherwise. The higher host is the other center. Let ell and h denote their full quotas. No names, physical roles or incidences change under this choice. Supply the seed core directly from n and the selected lower host.

| Actual vertices | Labels in order |
| --- | --- |
| `s:0,s:1` | 0, n |
| Lower host, higher host, `b:1:0` | 2, n−2, 1 |
| Lower-host terminal indices 0 and ell−1 | 3, n−1 |
| `l:1:0:0,l:1:0:1` | n−4, n−3 |

The two reserved lower indices are distinct since ell≥3. These vertices form a connected nine-vertex tree with the spine, three attachments and four actual terminal edges. Since n≥14, the labels are exactly the disjoint bands `[0,3] ⊔ [n−4,n]`. The spine and the three attachments in lower, higher and right order have weights n, 2, n−2 and n−1. The two lower-host terminal edges supply 1 and n−3, and the two right terminal edges supply n−5 and n−4. These are all eight distinct weights `{1,2} ⊔ [n−5,n]`. The core requires no prior complete labeling. The residual label and difference intervals are `R=[4,n−5]` and `D=[3,n−6]`, each of size n−8. The vacant original slots are the lower-host indices 1 through ell−2 and the higher-host indices 0 through h−1, with quotas ell−2 and h.

## All-parity seed allocation

Put `p=ell−2`, `j=floor(p/2)`, `epsilon=p mod 2`, `u=floor((n−1)/2)`, `c=u−4`, and eta equal to one if n is even and zero otherwise. Every residual label x lies strictly between 2 and n−2. Thus the two possible weights are `d_L(x)=x−2` and `d_H(x)=n−2−x`. The map `d_H` bijects R onto D, and reflection `rho(x)=n−x` exchanges the two options wherever the reflected label is considered. At label 4 the lower weight 2 is occupied. The higher option n−6 is available, so 4 gives a forced higher half-edge. Its mate n−4 is occupied.

Reflection preserves `[5,n−5]`, where both options lie in `[3,n−7]`. The complete pairs have representatives `x=5,...,u`, with partners `n−x>u`, and supply exactly c parallel-pair components. If n is even, the distinct integer midpoint n/2 lies in `[5,n−5]` and gives one loop at weight n/2−2 with both host options. If n is odd there is no integer fixed point. The difference vertices of each orbit are exactly its image under the bijective `d_H`. They are disjoint between components and together with the forced vertex cover D. Each pair has two labels and two difference vertices, and each singleton component has one of each. Every label has an eligible option. These facts give component balance, distinct actual hosts and incidences, and the full palettes for [R226 revision 2](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout).

The forced contribution to the lower count is zero. By R226 its attainable integral counts are `2k+e` with integers `0≤k≤c`, `0≤e≤eta`. To choose `k=j,e=epsilon`, note that `u=(n−1−eta)/2` and `j=(ell−2−epsilon)/2`. With n=ell+h+6,

```text
c−j = (h−1−eta+epsilon)/2.
```

| Parity of q, a | Lower quota ell, higher quota h | eta | epsilon | c−j |
| --- | --- | ---: | ---: | --- |
| even, odd | q, a | 0 | 0 | (h−1)/2 |
| odd, even | a, q | 0 | 0 | (h−1)/2 |
| even, even | q, a | 1 | 0 | (h−2)/2 |
| odd, odd | a, q | 1 | 1 | (h−1)/2 |

Here h≥3 and ell≥3. Each row has a nonnegative integer margin, j≥0 and `0≤epsilon≤eta`. Therefore the attained lower quota is `2j+epsilon=ell−2`, with no comparison between q and a.

Allocate the j innermost pairs and the midpoint exactly when epsilon=1 to the lower host. In interval notation this is

```text
S_L = [u−j+1,u] ⊔ [n−u,n−u+j−1] ⊔ M_epsilon
S_H = R minus S_L
```

Here `M_epsilon={n/2}` when epsilon=1 and is empty otherwise. For j>0, the first interval starts at least at 5 by j≤u−4. Its reflected interval ends at most at n−5. They are disjoint since u<n−u. Each has j labels. When j=0 both intervals are empty by the endpoint convention, and the midpoint rule alone determines the lower list. If selected, the midpoint is available and distinct from both paired intervals. Thus `rho(S_L)=S_L`, it contains exactly `ell−2` labels, and S_H contains exactly h, including 4. In the even–even case the available midpoint belongs to S_H.

Place S_L in increasing order at lower indices 1 through ell−2. Place S_H in increasing order at higher indices 0 through h−1. All reserved core labels stay fixed. This consumes R once, extending the seed to the full alphabet `[0,n]`. Independently of the quota projection, `d_L=d_H∘rho` on S_L, so the multisets `d_L(S_L)` and `d_H(S_L)` are equal. The respective lower and higher weights partition D by bijectivity of d_H. Together with the core weights, they supply each seed weight from 1 through n once.

For odd–odd inputs, the lower host is `b:0:1`, ell=a, and the midpoint is t=n/2 with u=t−1. The two bands and selected midpoint combine to `[t−j,t+j]`, including j=0, exactly [D115](ORDINARY_QA_2_ODD_ODD_COMPLEMENTARY_SUPPLIER.md)'s indexed placement. In the other three cases epsilon=0, and the host rule, core and both bands agree pointwise with [D116](ORDINARY_QA_2_PARITY_COMPLEMENTARY_SUPPLIER.md). In particular at even q and a=3, [D114](ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER.md) is recovered. These are symbolic identities of the named seed labelings.

## Exact indexed right growth

In the seed, `s:1` ends the witnessing spine and its exact neighbors are `s:0` and `b:1:0`. Their labels are 0 and 1, the latter is off the spine, and the exit carries n, the maximum. These are [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s physical premises. At current right quota k≥2, suppose its exit is labeled `n+k−2`. To increase the quota to k+1, the exact original adds only `l:1:0:k` joined to `b:1:0`. D112 gives that terminal the old maximum `n+k−2` and raises the exit by one. All old names, terminal indices, roles and actual incidences persist. The newly named terminal is precisely the next indexed leaf, the exit neighborhood is unchanged, and the same physical premises hold. Induction from k=2 gives the direct final formula at right quota r. Retain all seed labels except the exit, put `s:1=m`, and give each new `l:1:0:k` its label `n+k−2` for `2≤k≤r−1`. No left option uses m.

## Direct final inventories and signed properties

The seed vertices other than the exit supply `[0,n−1]` once, the new terminals supply `[n,m−1]`, and the exit supplies m. This disjoint partition is exactly `[0,m]`. The unchanged seed edges have weights `[1,n−2]` because the only altered old edges are the spine and right attachment, with seed weights n and n−1. The new right-terminal edges, against label 1, have weights n+k−3, giving `[n−1,m−2]`. The final right attachment and spine give m−1 and m. These four groups are disjoint and exhaust `[1,m]` with multiplicity one. When r=2 the two inserted intervals are empty, m=n and the seed itself is returned. This direct inventory argument does not require a numerical extension check.

Under orientation from the traversal class of `s:0`, the even class contains `s:0`, `b:1:0` and all left terminals. The other class contains `s:1`, both left centers and all right terminals. Exactly the lower-host terminal incidences carry negative signed differences, since their terminal labels exceed 2. These differences are −1, the sequence of `2−x` for the increasing S_L list, and `3−n` in lower-host index order. All higher-host leaves are below their host. Both changed exit edges and every new right-terminal edge remain positive, so right growth introduces no negative incidence. These signs describe the output.

Validate exact integer type for q,a,r with the stated lower bounds, rejecting booleans, nonintegers and out-of-domain integers. Evaluate the seed role rule and emit its core and residual labels with one pass over R. Emit the right-terminal indices and the final exit as prescribed. Each named vertex and incidence is produced in its finite index range. This takes O(q+a+r) indexed output operations and terminates without any search.

## Retained agreements and scope

At (q,a)=(5,3), n=14, j=0 and epsilon=1. The same left lists, centers and first two right labels as D111 persist while `s:1=14+r−2=r+12`. Each additional terminal k has label `14+k−2=12+k`. Hence the complete `[[5,3],[r]]` formula agrees with D112 for every r≥2. The two retained numeric evaluations are D111 at (5,3,2) and D114 at (6,3,2). The archived D105-to-D106 transition in D112 corroborates the growth lineage. The symbolic proof establishes the quantified statement. D107's q=4 result keeps its separate domain. Additional physical center multiplicity and arbitrary spine composition are separate obligations.
