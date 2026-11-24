# D124 — Independent even outer quotas on the modified shared-middle core

For exact even integers $q,c\ge6$ with $q\ne c$, the ordered original `[[q,3,c],[2]]` admits the explicit ordinary graceful labeling below. Its fixed physical pins are `s:0=0`, `s:1=m=q+c+10`, `b:1:0=1`. The proof's numerical identities also give pointwise agreement with D123 on the diagonal. Throughout, intervals denote inclusive integer intervals.

## Original and fixed core

The path `s:0--s:1` is the witnessing spine. The three physical left centers X, M, Z have indices 0, 1 and 2 and respective quotas $q,3,c$. The right center `b:1:0` has quota two. Each center is adjacent to its own spine vertex and each leaf to its indexed center alone. There are $q+c+5$ terminal edges, four attachments and one spine edge, hence $m=q+c+10$ edges and $m+1$ vertices. These attachments yield a tree with distances 0, 1 and 2 from the spine for spine vertices, centers and terminals respectively. In particular $m$ is even and at least 22.

The spine carries 0 and $m$. The X, M, Z and right centers carry $2,m-6,m-4,1$. Reserve $m-3$ at X index 0, $m-5$ at M index 0 and $m-1,m-2$ at the right indices 0 and 1. The ten named vertices induce a tree whose nine differences in original order are
$$
m,\ 2,\ m-5,\ m-6,\ 1,\ m-4,\ m-1,\ m-2,\ m-3.
$$
The label partition of the core is $[0,2]\sqcup[m-6,m]$ and its weight partition is $\{1,2\}\sqcup[m-6,m]$, with no repeats. Thus $R=D=[3,m-7]$ and each has $q+c+1$ members. Vacant quotas at X, M and Z are $q-1,2,c$.

For any graceful labeling, $|f(v)-f(w)|\equiv f(v)+f(w)\pmod 2$, and the total label and difference sums are equal. Therefore the excess-degree weighted sum $\sum_v(\deg v-1)f(v)$ must be even. Here the terminal terms vanish and the entrance is zero. The exit and right center contribute $m+2$. The left contribution is $q f(X)+3 f(M)+c f(Z)$. Each term is even under the prescribed labels. Full feasibility follows from the actual difference partitions below. D122 concerns its own distinct fixed core, which uses weight one between labels $m-4,m-5$. Here weight one is at M with endpoint labels $m-6,m-5$.

## Complementary intervals and reservations

Set $t=(m-2)/2$, $b=t-q/2=c/2+4$, and $e=t+q/2=q+c/2+4$. All endpoints are integral. We have $b\ge7$, $m-7-e=c/2-1\ge2$, and $b+e=m-2$. The interval $I=[b,e]$ contains exactly $q+1$ labels and contains $t-2,t,t+2$ because $q/2\ge3$. Its complement $J=[3,b-1]\sqcup[e+1,m-7]$ has component interval lengths $c/2+1$ and $c/2-1$. Both lengths are at least two and sum to $c$. The bounds use $q,c$ independently and hold in each unequal order. The reversal $w(x)=m-4-x$ is a bijection $R\to D$ and takes I onto $[b-2,e-2]$.

Using X/M for A and M/Z for B, reserve
$$
(R_A,D_A)=(I\setminus\{t\},w(I)\setminus\{t-4\}),\qquad
(R_B,D_B)=(J\cup\{t\},w(J)\cup\{t-4\}).
$$
Because $t-4=w(t+2)\in w(I)$, the label transfer and difference transfer each leave disjoint full residual partitions. A has $q$ resources of each type and B has $c+1$. These reservations are prescribed directly by the parameters.

## Batch A — Reflection and deletion

The actual X and M options for $x\in I$ are $d_X(x)=x-2$ and $d_M(x)=m-6-x$, since every such label lies between the hosts. In the symbolic reference interval with difference set $w(I)$, X is always eligible. The M weights of $e-1,e$ are $b-3,b-4$, below $b-2$. On $[b,e-2]$, reflection $\rho(x)=m-4-x=2t-2-x$ exchanges the options and preserves the interval. The unique midpoint $t-1$ contributes a loop at $t-3$, with two host tags on a single label resource. Each other orbit consists of two reflected labels and two distinct difference vertices. With the bijection $d_X:I\to w(I)$, the resulting half-edges, parallel pairs and loop exhaust the reference difference set.

The pair $\{t-2,t\}$ uses $\{t-4,t-2\}$. The label $t-2$ has X weight $t-4$ and M weight $t-2$, and the label $t$ has the exchanged options. Deleting the label $t$ and weight $t-4$ changes only this component, leaving $t-2$ forced to M at weight $t-2$. The reference interval $[b,e-2]$ has $q-1$ entries, one of which is the midpoint. Removing one of its $(q-2)/2$ pairs leaves $(q-4)/2$ intact pairs. Altogether there are two forced X half-edges, one forced M half-edge, those parallel pairs and one loop. Each component is balanced and every retained label has an eligible option. With X first, the exact integral projection is $\{2+2j+\epsilon:0\le j\le(q-4)/2,\ j\in\mathbb Z,\ \epsilon\in\{0,1\}\}$, since each pair must take a common host and the loop can take either host.

Select all pairs and the midpoint for X. Then X receives $I\setminus\{t-2,t\}$ and M receives $\{t-2\}$, with quotas $(q-1,1)$. The X weights are $[b-2,e-2]\setminus\{t-4,t-2\}$, and M supplies $t-2$. This independently consumes $D_A$ once.

## Batch B — Forced translation chains

Both hosts exceed every reserved label, so $d_Z(x)=w(x)$ and $d_M(x)=w(x+2)$. The M weight of $t$ is $t-4$ and its Z weight is $t-2\in w(I)\setminus\{t-4\}$. Thus only M is eligible for $t$. A J label could supply that same M difference only at $x=t$, or at Z only at $x=t+2$. Neither belongs to J. The special half-edge therefore stands alone.

For a J label Z is always eligible. M is eligible exactly when $x+2\in J$, by injectivity of $w$ and isolation of $t-4$. Identify difference vertices $w(x)$ with coordinates $x\in J$. The nonloop edges connect a coordinate to its successor by two when present. The gap I has $q+1\ge7$ entries, so the connected chains are exactly the two nonempty parity chains in each of J's two intervals. A chain with $n$ entries has $n$ difference vertices, $n-1$ ordinary edges and one Z half-edge at its maximum coordinate. For a singleton this means one vertex and a single half-edge. No loops or parallel edges arise here. These four components and the isolated M half-edge exhaust $D_B$ and satisfy balance, with no labels lacking options.

On each chain, the smallest coordinate can be supplied only from its own label using Z. Once that label is consumed, the next vertex can only obtain its own label using Z. This continues to the end, forcing every assignment. The same extraction roots at the half-edge vertex and assigns each ordinary edge away from that root as in R226 Section 5. The integral M projection is exactly $\{1\}$, with only $t$ at M. The quotas are $(1,c)$, and by direct calculation the two hosts supply $\{t-4\}\sqcup w(J)=D_B$, once each.

## Named reconstruction, signs and specialization

Use the following terminal lists in physical index order, retaining the core spine and center labels.

| Host | Terminal list |
|---|---|
| X | $m-3$, followed by the increasing list of $I\setminus\{t-2,t\}$ |
| M | $m-5,t-2,t$ |
| Z | the increasing list of J |
| Right center | $m-1,m-2$ |

A fills X indices $1,\ldots,q-1$ and M index 1. B fills M index 2 and Z indices $0,\ldots,c-1$. The batches share only the unchanged M host and their actual slots are disjoint. They fill every original vacancy exactly once. Each batch has two distinct core hosts, actual leaf incidences and exact integral quotas. Both label palettes consist of distinct integers avoiding the hosts and both equally sized difference palettes consist of distinct positive integers. Their disjoint partitions complement the independently labeled tree core, and all positive-quota hosts are one edge from the same witnessing spine. These are the hypotheses of [R226 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). The explicit spectra above also independently establish the full label and actual difference bijections $[0,m]$ and $[1,m]$, without changing any original vertex or incidence.

Orient from the class containing the entrance. The left terminals and right center lie in that class, and the left centers, exit and right terminals lie in the other. Every X terminal label exceeds 2. The reserved M terminal exceeds M by one, while its other labels $t-2,t$ are below $m-6$, since $m-6-t=t-4>0$. All Z terminal labels are below Z, all right terminal labels exceed one and all signed spine and attachment differences are positive. This yields exactly $q$ negative incidences into X from its terminals, plus the reserved weight-one M incidence with sign minus. The exit is the terminal endpoint, has exact neighbors `s:0` and `b:1:0` carrying 0 and 1 with the latter off the spine, and carries maximum $m$. This verifies [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s physical premises.

When $q=c=u$, the values $m,t,b,e$ become $2u+10,u+4,u/2+4,3u/2+4$. The core, both palettes, ordered allocations and slot ranges then agree pointwise with [D123](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) for every accepted u. The kernel rejects booleans, nonintegers, odd inputs and inputs below six. The official task restricts the new evaluation to the single unequal original and uses equality only in its declared retained comparison. Finite ordered scans of I and J and the fixed number of indexed outputs per remaining vertex take $O(q+c)$ indexed operations. The proven new scope is the stated unequal domain.
