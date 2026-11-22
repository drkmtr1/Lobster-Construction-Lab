# Conditional compatibility of minimum-high and zero-host growth

Start with an independently supplied named tree and witnessed alpha
state `A(n,p;x,y)`. The labeling `g` uses `0..n-1` and its actual
edge differences are `1..n-1`, each once. Every edge crosses the cut
between `[0,p-1]` and `[p,n-1]`, where `1<=p<n`. Its actual
distinct ports `L,U` have labels `x,p+y` with `0<=x<p` and
`0<=y<n-p`. The actual `L`-to-`U` path `W` is within distance two
of every vertex. At the supplied physical hosts require
`g(H)=p`, `g(Z)=0`, and distance at most one from `W` at each.
The labels force `H!=Z`. The hypotheses allow `H=U` when `y=0`
and `Z=L` when `x=0`.

For exact integers `h,k>=0`, take ordered lists of pairwise distinct
fresh names `u_1,...,u_h` and `v_1,...,v_k`, disjoint from each other
and the original vertices. Add only `H--u_i` and `Z--v_j`. Each leaf
is connected by one edge, so the enlarged graph remains a tree and
retains every original named incidence. All additions use these
same physical hosts and preserve the order within each list.

Use the [minimum-high extension](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md)
for the H leaves and the [zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
for the Z leaves. The former keeps Z at zero, increases the order and
cut by the number of additions, and puts H at the new minimum high.
The latter keeps H at the minimum high and leaves the cut unchanged.
Both keep the path W and the distances of old vertices to it, since
adding a pendant leaf cannot change a path between old vertices.
Every new leaf is within two edges of W through its host. Each
operation therefore preserves the other operation's premises.

If H growth is first, it shifts the original highs by h and gives the
u_i labels p+i-1. The order is then n+h, so the v_j receive n+h+j-1.
If Z growth is first, the v_j initially receive n+j-1, above the
original high labels. H growth shifts them by h along with every
original high, and gives the u_i the same labels p+i-1. Therefore
both orders give these pointwise assignments:

| Vertices | Labels | Complete label band |
|---|---|---|
| Original lows | g | [0,p-1] |
| New H leaves u_i | p+i-1 | [p,p+h-1] |
| Original highs | g+h | [p+h,n+h-1] |
| New Z leaves v_j | n+h+j-1 | [n+h,n+h+k-1] |

The bands partition `[0,n+h+k-1]`. The H-leaf difference is
`(p+h)-(p+i-1)=h-i+1`, covering `[1,h]`. Original edges have exactly
one high endpoint, and their shifted differences cover `[h+1,n+h-1]`.
The Z-leaf differences equal their labels and cover
`[n+h,n+h+k-1]`. The disjoint bands exhaust the new difference
alphabet. With cut `p+h`, original lows and H leaves are low,
and original highs and Z leaves are high. Every edge crosses the
cut. Bands with no additions are empty, including both when
`h=k=0`, which gives the identity.

Return `A(n+h+k,p+h;x,y)` with the same physical `L,U,H,Z,W`
and labels `x,p+h+y,p+h,0`, respectively. The low offset remains
in range as the low class grows, and the high class has size
`n-p+k`, so the high offset stays in range too. The formulas
also hold in the allowed port/host coincidence cases.

## Finite interleavings

After any finite sequence of batches that has added a H leaves and
b Z leaves in their own prescribed orders, maintain

```text
N=n+a+b, P=p+a
original lows g, original highs g+a
u_i=p+i-1       (1<=i<=a)
v_j=n+a+j-1     (1<=j<=b)
```

This is the supplied state at a=b=0. A further H batch of size d
raises every current high by d, including all earlier Z leaves.
It fixes earlier H leaves because they are below P. Its i-th fresh
name gets `P+i-1=p+(a+i)-1`, and the new a is a+d. A further Z
batch of size d leaves all old labels fixed. Its j-th fresh name
gets `N+j-1=n+a+(b+j)-1`, and the new b is b+d.
The hosts, witness and pairs of offsets keep their premises after
each step. This proves the invariant and state `A(N,P;x,y)`
by induction on the finite list of batches. The two lists specify
every new edge, so all interleavings with the same totals agree
on labels at every named vertex and on the exact named graph.
Every requested finite construction terminates after h+k leaf
additions. Empty batches act as identities.

The lemma assumes both hosts are independently supplied on
one state. It supplies no relabeling to create either host and
places no restriction on terminal-name permutations beyond
the specified pointwise ordering.
