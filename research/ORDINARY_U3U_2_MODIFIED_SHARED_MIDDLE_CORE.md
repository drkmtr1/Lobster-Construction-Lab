# D123 modified shared-middle core

For each exact even integer $u\ge6$, the ordered original `[[u,3,u],[2]]` admits the ordinary graceful labeling below, with `s:0=0`, `s:1=m=2u+10`, and `b:1:0=1`. Each of two independently reserved R226 batches supplies one of the two vacant terminals at the physical middle center.

## Named core and parity

The witnessing spine is `s:0--s:1`. Its three left centers X, M, Z have physical indices 0, 1, 2 with quotas $u,3,u$. Its right center has quota 2. The complete tree is formed by adjoining centers to the corresponding spine endpoints and the indexed terminals to their own centers. It has $2u+11$ vertices and $2u+10$ edges. Spine vertices, centers and terminals are respectively at distances 0, 1 and 2 from the spine.

On the spine use labels 0 and $m$, and on X, M, Z and the right center use $2,m-6,m-4,1$. Reserve labels $m-3$ and $m-5$ at index zero of X and M respectively, and $m-1,m-2$ at right indices zero and one. These ten vertices induce a connected tree. In original order the nine core weights are $m,2,m-5,m-6,1,m-4,m-1,m-2,m-3$. In particular, weight one is on M's reserved terminal with endpoint labels $m-6,m-5$. The D118 and D122 core has weight one between labels $m-4,m-5$. A label-preserving incidence transport preserves that endpoint pair, so the new core is independently specified. D122 still excludes its prescribed fixed labeled core at $q=c=u,a=3$, since $u>u-4$.

The distinct core labels are $[0,2]\sqcup[m-6,m]$; its distinct weights are ${1,2}\sqcup[m-6,m]$. The residual inventories are $R=D=[3,m-7]$, both of size $2u+1$, and the vacant quotas at X, M, Z are $u-1,2,u$. For any ordinary graceful labeling, $\sum_v(deg(v)-1)f(v)$ is even because $|f(v)-f(w)|\equiv f(v)+f(w)\pmod2$ and the label sum equals the difference sum. The terminal coefficients vanish and the entrance contributes zero. The exit and right center contribute $m+2$ and the left centers contribute $u f(X)+3f(M)+u f(Z)$, all even with the specified core. The construction below verifies the full spectrum.

## Independently reserved palettes

Put $t=u+4=(m-2)/2, b=t-u/2=u/2+4, e=t+u/2=3u/2+4$. These are integers, $b\ge7$, $m-7-e=u/2-1\ge2$, and $b+e=m-2$. Set $I=[b,e]$ and $J=R\setminus I$. The endpoints of I are at distance $u/2\ge3$ from $t$, so $t-2,t,t+2\in I$. I has $u+1$ labels. The two parts $[3,b-1]$, $[e+1,m-7]$ of J have lengths $u/2+1$, $u/2-1$, respectively, giving $u$ labels. The affine map $w(x)=m-4-x$ reverses R onto D, and $w(I)=[b-2,e-2]$.

Reserve $R_A=I\setminus\{t\}$, $D_A=w(I)\setminus\{t-4\}$ for X/M and $R_B=J\cup\{t\}$, $D_B=w(J)\cup\{t-4\}$ for M/Z. Since $t-4=w(t+2)\in w(I)$, the transfer of one label and one difference gives disjoint full residual partitions. The reservations are functions of the parameter and do not require a solved whole tree.

## Batch A

Throughout I the labels lie strictly between X and M. The weights at X and M are $x-2$ and $m-6-x$. For the reference label interval I and difference interval $w(I)$ the X option is always eligible. The M weights for $e-1,e$ are $b-3,b-4$, below the reserved minimum $b-2$. On the remaining interval $[b,e-2]$ the reflection $\rho(x)=m-4-x=2t-2-x$ exchanges the options and preserves that interval because the endpoints sum to $m-4$. Each distinct reflected pair uses two distinct difference vertices with opposite host tags, and the midpoint $t-1$ has both options equal to $t-3$. The bijection $d_X:I\to w(I)$ ensures that these component vertices are disjoint and exhaust $w(I)$.

In the pair ${t-2,t}$ the X options are $t-4,t-2$, and the M options are $t-2,t-4$, respectively. Removing $t$ and $t-4$ therefore leaves $t-2$ forced to M at $t-2$. All other rows and their components remain unchanged. There are two forced X half-edges, one forced M half-edge, $(u-4)/2$ parallel pairs and one midpoint loop. Each half-edge or loop brings one label and difference, and each parallel pair brings two of each. No eligible row is empty. Under R226 with X first, each parallel pair is assigned wholly to one host, the midpoint takes either host, and the forced X contribution is two. Thus the projection is ${2+2j+\epsilon:0\le j\le(u-4)/2,\ \epsilon\in\{0,1\},\ j\in\mathbb Z}$. Use all pairs and the midpoint at X. The X allocation $I\setminus\{t-2,t\}$ has $u-1$ labels and gives $[b-2,e-2]\setminus\{t-4,t-2\}$. M takes $t-2$ and supplies the missing $t-2$. This is a multiplicity-one direct cover of $D_A$, with local quotas $(u-1,1)$.

## Batch B

Both M and Z exceed every residual label. The Z and M options are $w(x)$ and $w(x+2)$. Label $t$ has eligible M weight $t-4$, while its Z weight $t-2=w(t)$ lies in $w(I)$ and differs from $t-4$. An option at $t-4$ for a J label would require $x=t+2$ at Z or $x=t$ at M, both outside J. Thus the special label gives an isolated M half-edge.

For each $x\in J$ the Z option is eligible, and the M option is eligible exactly when $x+2\in J$. Distinct J labels give distinct difference vertices under w. Under these coordinates the ordinary edges connect consecutive step-two entries in each parity class of each interval of J. The gap I has $u+1\ge7$ labels and prevents cross-gap edges. Both intervals have at least two consecutive labels. Hence there are four nonempty chains, including a singleton chain when a parity class of an interval has size one. A chain of $n$ entries has $n$ difference vertices, $n-1$ ordinary edges and one Z half-edge at the maximum entry. No parallel pairs or loops occur.

Every component meets the R226 balance $e_K+t_K=n_K$, with all rows and all reserved difference vertices covered. In each chain the smallest coordinate can be supplied only through Z by its own label. Once it is used, the next coordinate can likewise be supplied only through Z by its own label, and this forces every label in order. Equivalently, the R226 tree extraction assigns the half-edge to its vertex and each ordinary edge away from that root, toward its Z-tagged endpoint. This gives a unique local extraction. In M/Z order the integral projection is ${1}$, with the one forced M label $t$ and every J label at Z. The exact quotas are $(1,u)$. Directly, these weights are $\{t-4\}\sqcup w(J)=D_B$.

## Original reconstruction

Use the following terminal lists in increasing index order. The core labels stay fixed.

| Host | Terminal labels |
|---|---|
| X | $m-3$, followed by the increasing list of $I\setminus\{t-2,t\}$ |
| M | $m-5,t-2,t$ |
| Z | the increasing list of J |
| Right center | $m-1,m-2$ |

The core hosts are fixed and each is adjacent to an actual spine vertex. In A, use X indices $1,\ldots,u-1$ and M index 1. In B, use M index 2 and all Z indices $0,\ldots,u-1$. The host sets intersect exactly in M, but their slots are disjoint. Together they give each original unfilled incidence once, taking the aggregate quotas to $u,3,u$. All used labels are integers, the core's two inventories are injective, both batch palettes partition the respective free inventories, and both batches realize their integral quotas and spectra. These are the original-core, palette, balance and allocation requirements of the adopted R226 revision-2 reserved-palette corollary, Section 10. Its two-host constructions add only the prescribed pendant incidences. The direct weight formulas independently give multiplicity one across the core and both batches. Thus the complete alphabets are $[0,m]$ and $[1,m]$, with no unused resources. Neither the named topology nor the witnessing spine changes.

Orient from the traversal class of `s:0`. Its members include the left terminals and the right center, while the other class contains the left centers, the exit and the right terminals. All X terminal labels exceed 2 and the reserved M leaf exceeds $m-6$ by one. The two other M leaves, $t-2,t$, lie strictly below $m-6$. All Z leaves lie below $m-4$; the spine, four attachments and both right-terminal edges are positive in this orientation. Thus exactly the $u$ X terminal incidences and the reserved M terminal incidence are negative, the latter with weight $-1$. The exit remains the last spine vertex and its exact neighbors are entrance 0 and off-spine right center 1. With maximum label $m$ this satisfies D112, whose growth operation is outside this task.

A guard checks `type(u) is int`, $u\ge6$ and $u\equiv0\pmod2$. Two bounded interval scans and the indexed writes finish in $O(u)$ output operations. The quantified proof supplies equal outer quotas in this exact orientation and core.
