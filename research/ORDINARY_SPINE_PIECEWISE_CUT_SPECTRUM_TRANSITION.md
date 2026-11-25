# D134 — Repeatable piecewise cut-spectrum spine transition

## Exact cut-shift identity

Supply a named ordinary graceful prefix with n edges, labeling g onto `[0,n]`, ordered witnessing spine and actual last vertex v. Let the next section have h≥3 fresh centers with exact positive terminal quotas totaling Q, with n≥h+Q and `m=n+h+Q+1`. The fresh section has one spine vertex w and Q terminals at their named physical hosts. Its edges are the connector vw, the h attachments from w and the Q terminal edges. Adding these vertices as pendants in that order preserves the old incidences and gives a tree with m edges. The old spine extended by w witnesses distance at most two. New centers and terminals are at distances one and two. All intervals below denote exact integer intervals, with a reversed interval empty.

For an exact cut `1≤c≤n`, let C consist of the weights of the actual original edges with one label below c and the other at least c. Gracefulness identifies each weight with a unique old incidence. For integers `A≥0`, `s≥1` and `A+s≤h+Q+1`, translate the low and high label groups by A and A+s. The old label bands are `[A,A+c−1]` and `[A+c+s,A+n+s]`. They are disjoint, in range and strictly ordered. Their complementary label bands are `[0,A−1]`, `[A+c,A+c+s−1]` and `[A+n+s+1,m]`.

A noncrossing edge has both endpoints moved by the same amount. Its difference is unchanged even if both endpoints are high. Every crossing edge gains s in absolute difference, since its higher endpoint moves s farther. Thus the old weight multiset consists of `[1,n] minus C` and `C+s`, each internally injective. The combined multiset is injective exactly when their intersection is empty, or equivalently every d in C with d+s≤n has d+s in C. All resulting weights lie in `[1,m]` by the translation bound. The complementary weight set is
```
(C minus (C+s)) ⊔ ([n+1,m] minus (C+s)).
```
This is the exact residual weight palette in the injective case. In the collision case it is only the unused set, and the repeated old incidence already prevents a graceful extension. The criterion uses crossing edges and needs no alpha separation.

## Stronger input state and reserved palettes

Fix an exact integer p≥1 and let `h=2p+1`. Supply the full ordinary prefix and its named frontier at either 0 or n, retaining its polarity. Write directed label coordinates G=g for a zero frontier and G=n−g for a maximum frontier, so G(v)=0. In G require a declared cut `1≤c≤n` with actual crossing spectrum `[d,n]`, where `d=c+p+1≤n`. The corresponding actual cut for g is c in the low-frontier case and n+1−c in the high-frontier case. Complement interchanges sides at those corresponding cuts and preserves the set of crossing edges. This state carries both full inventories, the actual cut, all incidences and labels, and the ordered spine and physical port. The deficit alone does not supply the crossing premise.

In oriented coordinates set `F(x)=h+G(x)+Q indicator(G(x)≥c)` on old vertices. Their label bands are `[h,h+c−1]` and `[h+c+Q,h+n+Q]`. Set `F(w)=m` and give the centers labels j at their physical indices `j=0,...,h−1`. Reserve all terminal labels `x_i=h+c+i` for `0≤i<Q`. These five bands, from zero centers through low old labels, gap, high old labels and w, fill `[0,m]` exactly. They are specified before the terminal allocation.

By the cut-shift identity the old weights fill `[1,d−1] ⊔ [d+Q,n+Q]` exactly. Their independent residual palette is `[d,d+Q−1] ⊔ [n+Q+1,m]`. Since F(v)=h, the actual connector vw has weight n+Q+1. The attachments to centers j have weights m−j, exhausting `[n+Q+2,m]`. The terminal labels are above every new center. A terminal with gap index i at host j has absolute weight `x_i−j=d+i+p−j`, because h=2p+1 and d=c+p+1. The terminal assignment must consume normalized coordinates `[0,Q−1]` exactly once.

## Symmetric quotas and the split-preserving allocation

For each exact integer ell from 1 to p prescribe equal quotas b_ell≥1 at physical indices p−ell and p+ell. At p prescribe b_0≥1. Thus `Q=b_0+2 sum(b_ell)` over the positive ell. Set `B=sum((ell+1)b_ell)` over the same range and `k=(n+Q+2−2c)/2`. Require k integral and `B≤k≤Q`.

In increasing ell, take b_ell disjoint consecutive blocks of length ell+1 from the next unused gap index, starting at zero. For a block starting at i, assign index i to physical p−ell and i+ell to p+ell. Put all its ell−1 interior labels at physical p. The formula for the normalized terminal difference swaps the coordinates of i and i+ell and fixes every interior coordinate. Thus the complete block consumes precisely its own coordinate interval. The blocks cover exactly `[0,B−1]` and are disjoint. Assign all remaining indices to p, fixing their coordinates. This yields all Q terminal differences exactly. At the two symmetric hosts for a given ell the count is b_ell each. The middle gets all Q indices except two endpoints per block, giving b_0. This proof includes length two blocks, with no interiors. All blocks lie in `[0,k−1]`, so the terminal permutation preserves both index bands `[0,k−1]` and `[k,Q−1]` separately.

Emit labels in increasing gap-index order at each physical host's consecutive terminal indices. This preserves the names, physical order and every actual incidence. The connector, h attachments and Q terminal incidences have the disjoint spectra just proved, which together with the old spectra give all `[1,m]` exactly. No terminal or center at any completed section remains pending.

## Reusable return and polarity

Before reorienting choose `c_out=h+c+k`. The old low band ends below c_out and the old high band starts at least at c_out since k≤Q. Every new center is below the cut and w is at or above it, since `c_out≤h+n+Q=m−1`. A new terminal edge crosses exactly when i≥k. The connector crosses because its old endpoint of label h is below c_out. Since the allocation preserves the two bands separately, the full crossing spectrum at c_out is
```
[d+k,d+Q−1] ⊔ [d+Q,n+Q] ⊔ [n+Q+1,m] = [d+k,m].
```
The first interval is empty when k=Q. The noncrossing spectrum is exactly `[1,d+k−1]`.

If the actual input frontier is zero, use F as the actual output. The actual old shifts below and above the actual old cut are h and h+Q. The actual return cut is c_out and w carries m. If the actual input frontier is n, use m−F as the actual output. The actual return cut is m+1−c_out and w carries zero. An old actual label below n+1−c had G≥c, so in this case `m−F=g+1`. At or above the actual input cut it had G<c, giving `m−F=g+Q+1`. Thus both actual transformations are separately translated, strictly increasing bands, with high shift minus low shift exactly Q. In the second case the two complements exchange sides twice, so actual low and high membership is retained in both cases. In particular a vertex at the cut belongs to the high band by the strict below-cut convention.

The next oriented frontier is zero in both cases. In those oriented coordinates
```
n_new = m
c_new = m+1−c_out = c+k
d_new = d+k.
```
The equality for c_new follows from `2k=n+Q+2−2c`. The crossing set is unchanged by complement with the corresponding cut. Therefore `d_new−c_new=p+1` and `n_new−2c_new=h−1`. The oriented cut is positive, and d_new≤n+Q<m since d≤n and k≤Q. Hence all oriented and actual cut bounds hold. The physical port is the actual new last spine vertex with opposite polarity. Its exact neighbors are the old port and its h centers. The actual normalized labels and weights remain full bijections.

## Finite closure

At the returned invariant `n−2c=h−1`, the split for the next section is `k=(h+Q+1)/2`. For fixed odd h and the stated positive symmetric quotas, require Q even, `Q≥h+1`, `B≤(h+Q+1)/2` and `n≥h+Q`. Then k is integral, B≤k, and k≤Q follows from Q≥h+1. All step premises hold. The proof returns the same invariant with flipped polarity and increases the prefix size by h+Q+1. Therefore any finite list with these conditions at its successive sizes closes by induction, including the empty list. A given admitted vector continues to meet its scalar conditions at every repetition, and the size inequality persists since the size increases. This proves arbitrary finite repetition. The proof does not supply arbitrary changes of multiplicity or nonsymmetric quotas. Each forward step has a finite named output and the number of steps is fixed by the list.

## Independent symbolic initialization for every fixed odd h

Supply a graceful prefix with n_0 edges and actual maximum frontier, as in the retained D105 or D130 sources. Choose c_0≥p+2 with `c_0+p≥n_0`, `c_0+p−n_0` even, and `c_0+p+1≥p(p+3)/2`. There are arbitrarily large integers in the required parity class. Put `N=3c_0+p−1` and `K=N−n_0=2t−1`, so `t=(3c_0+p−n_0)/2≥c_0`. Declare K actual empty new spine sections in the target. They are physical path extensions with new named incidences.

Translate the full old labeling by t. Its labels fill `[t,n_0+t]` and its differences remain `[1,n_0]`. From the new physical endpoint backwards, use label j at path position 2j and label N−j at position 2j+1, starting at position zero and ending at position K=2t−1. The last label is `N−(t−1)=n_0+t`, exactly the translated old frontier. The K fresh vertices, which exclude that already supplied endpoint, fill `[0,t−1] ⊔ [n_0+t+1,N]`. Each edge from position u to u+1 for 0≤u<K has absolute difference N−u. Thus the K fresh edges fill `[n_0+1,N]` and the full original is graceful with frontier zero. Appending an actual path preserves the lobster witness.

At cut c_0, all translated old labels lie at or above c_0. The only low labels are the first c_0 small entries on the new path, at positions 0,2,...,2c_0−2. Every high entry is at least c_0. Hence the crossing edges are exactly the initial path edges with starting positions 0 through 2c_0−2. This includes the case t=c_0, where the last such edge reaches the old frontier. Their spectrum is `[N−2c_0+2,N]`. Consequently `d_0=c_0+p+1` with d_0≤N.

Choose the first piecewise section with `Q_0=c_0+p+1`, b_ell=1 for all positive ell and `b_0=Q_0−2p≥3`. Then `B=p(p+3)/2≤Q_0`, the split formula returns `k=Q_0`, and `N−h−Q_0=2c_0−2p−3≥1`. This meets every single-step premise and returns the closed invariant. To see that a repeatable vector is available there, choose the symbolic subsequent total `Q_*=2Q_0`, again with b_ell=1 for positive ell and middle quota `Q_*−2p`. It is positive, even, and at least h+1. The split is at least Q_0≥B. The returned size `N+h+Q_0+1` is at least h+Q_* since `N+1≥Q_0`. All successive repetitions are consequently admitted. This derivation supplies an infinite parameter domain without evaluating an initializer or extension numerically.

The initial translation and subsequent actual old-label embeddings are strictly increasing. Alpha separation on the fixed old incidences would require all labels in one of the two bipartition classes to precede all labels in the other. Strictly increasing maps preserve the two possible separation tests, so D105's failure of either separation persists on those very labels and incidences. This observation concerns the retained labeling under the embedding. It gives no conclusion about a different labeling of the extended original.

## Immutable final-alphabet realization

Fix a finite admitted list after a supplied boundary, which may be the initialized prefix. At boundary i let `n_i,d_i,C_i` be its edge count, first crossing weight and actual cut. Let `S_i` be the sum of all **subsequent** inserted gaps Q_j and `A_i` the sum of their actual lower-band shifts. Use zero sums at the last boundary. Actual cut membership of every existing vertex is preserved at every later boundary. Thus one fixed vertex gains exactly each later low shift and, if it is above or at C_i, each later gap. The composite on its boundary label x is
```
H_i(x)=x+A_i                     for x<C_i
H_i(x)=x+A_i+S_i                 for x≥C_i.
```
If e_i is the actual embedding from boundary i−1 to i, then `H_(i−1)(x)=H_i(e_i(x))` on all previously supplied vertices by membership preservation and the sum recurrences. Write a vertex only when first supplied, composing its local label with the precomputed H_i. Already emitted physical labels therefore agree exactly with later embeddings and remain immutable. This applies to both physical endpoints of the next actual connector.

At boundary i the used final labels are `[A_i,A_i+C_i−1] ⊔ [A_i+C_i+S_i,A_i+n_i+S_i]`. Later translations change no noncrossing absolute difference and increase each crossing difference by S_i, so the used final differences are `[1,d_i−1] ⊔ [d_i+S_i,n_i+S_i]`. The residual labels are exactly the complementary three intervals within the final label alphabet, and residual differences are `[d_i,d_i+S_i−1] ⊔ [n_i+S_i+1,n_final]`. The used label bands lie in the final alphabet because each forward step maps into the next normalized alphabet. The actual final-alphabet frontier label is its actual boundary value, zero or n_i, mapped by H_i.

For one step from n,d with Q,k and new size m, let S be the gaps still to be inserted after this step. Its final-alphabet newly consumed difference bands are
```
noncrossing terminals   [d,d+k−1]
crossing terminals      [d+k+S,d+Q−1+S]
connector/attachments   [n+Q+1+S,m+S].
```
The terminal subsets stay noncrossing or crossing by preserved membership after this step, and the connector and all attachments are crossing. The previously used bands are `[1,d−1] ⊔ [d+Q+S,n+Q+S]`. The new bands are disjoint from them and from each other, including the empty crossing-terminal band at k=Q. Their union is `[1,d+k−1] ⊔ [d+k+S,m+S]`, exactly as the returned cut predicts. The fresh label reservation is the image under H_i of the local fresh label palette in the **actual** output orientation, complementing the oriented palette for high input. Its disjointness follows from injectivity of H_i on the whole current alphabet and the local label partition. These statements account for the exact resource consumption, despite changing weights of old crossing edges during later normalized steps.

At any completed section boundary the only crossing incidence from supplied vertices to the unassigned suffix is the actual next spine connector, if a later section remains. This topological crossing is distinct from the spectral cut test on the assigned subgraph. All old terminal or center incidences within a completed section are supplied and all other pending edges lie in later sections. At the final boundary both residual alphabets are empty. Precompute sizes, cuts and polarities forward, and the two suffix sums backward. The initial prefix is translated once into its final positions. For each appended section a forward scan of its consecutive blocks and gap indices uses one counter per physical host and emits each vertex once under H_i. The operations for planning and emitting are linear in the final number of vertices and edges, including the path initializer if supplied. No reassignment sweep or numerical experiment is needed for this proof.

## Scope and comparison

The positive construction uses a gap in the old label interval and shifts a nonempty old crossing-weight band, so its old spectrum differs from `[1,n]`. Both conditions responsible for the [D133 obstruction](ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION.md) are absent. D131 and D132 retain their affine scopes and preserve old absolute weights. The retained [ordinary crossing-cut leaf insertion](ORDINARY_CUT_LEAF_INSERTION.md) uses the same crossing spectrum calculation for adding leaves at one existing host. Here a fresh spine connector and multiple new hosts are supplied and the cut and port polarity are returned for a further section. [R241](../references/upstream/mdl/N241_relational_ports.md) and [D078](R241_PAIRED_BRANCHED_SPINE.md) use alpha-state composition with their own port or tail assumptions. [R226](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) characterizes its reserved two-host inputs. This proof instead constructs disjoint coordinate transpositions across symmetric host pairs and fixed middle-host coordinates, with a chosen return split. The retained N121/N135/N141 results retain their factor, quota and model scopes. The positive D134 domain is a sufficient domain for arbitrary fixed odd multiplicity, with no classification of other piecewise embeddings or universal prefix supply.
