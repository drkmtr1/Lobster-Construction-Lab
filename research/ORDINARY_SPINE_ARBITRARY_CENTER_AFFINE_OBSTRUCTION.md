# D133 — Arbitrary-center obstruction to a single affine spine transition

## Exact domain

Let P be a supplied [D131](ORDINARY_SPINE_DEFICIT_TRANSITION.md) ordinary graceful prefix with n edges, labeling g onto `[0,n]`, nonempty ordered witnessing spine and actual last vertex v. Append one fresh named spine vertex w, h distinct fresh centers at w and their actual indexed terminal leaves. Write r_1,...,r_h for the exact positive terminal quotas of the physical centers and set Q=sum(r_j). Assume exact integers h≥3 and n≥h+Q. The only new edges are the connector vw, h attachments from w and Q pendant incidences. Their total is h+Q+1, so the final edge count is `m=n+h+Q+1`. Every old incidence survives. The declared extension is a tree by successive pendant additions, and its extended ordered spine witnesses the lobster distance bound. Neither the physical center order nor any old internal sign is restricted.

**Theorem.** No ordinary graceful extension in this domain can transform the supplied old labeling by a single integer affine isometry.

## Reduction to the two complementary label intervals

Assume there is such an extension f. The old image is a consecutive interval `[L,L+n]` within `[0,m]`, and every old absolute difference is unchanged, so the old spectrum is exactly `[1,n]`. The remaining labels are the lower interval `[0,L−1]` and the upper interval `[L+n+1,m]`. They contain h+Q+1 labels in total. Each nonempty interval separately has width at most h+Q, hence at most n. No new internal edge can have both endpoints in one such interval, since a new edge difference must be strictly greater than n. Equality at n=h+Q is covered by this strict inequality. The suffix has internal edges, which also implies both intervals are nonempty.

The actual internal suffix tree is connected. Its bipartition has all h centers in one class, and w together with all Q terminals in the other. Interval membership is itself a proper two-coloring by the preceding argument. On a connected tree the coloring is fixed by any one vertex, so the two interval memberships equal the two classes up to exchange. All remaining labels are used once and therefore the interval of the centers has h elements. If it is the upper interval, globally complement labels by `x↦m−x`. This exchanges the intervals, preserves absolute differences and incidences, and keeps the old embedding affine isometric. With the centers in the lower interval, the partitions are forced to be
```
centers       [0,h−1]
old vertices  [h,n+h]
w, terminals  [n+h+1,m]
```
Which physical center gets a particular low label is still arbitrary at this point.

## Exact connector and necessary return

In the canonical interval the affine modes are `psi(x)=n+h−x` and `psi(x)=h+x`. Their slopes and image fix their offsets. With `delta=n−g(v)`, set `kappa=delta` in reflection and `kappa=n−delta` in translation. The inherited frontier label is `h+kappa`. Independently of any suffix assignment, the complementary labels and weights are `[0,h−1] ⊔ [n+h+1,m]` and `[n+1,m]`. Every internal suffix edge joins a low center label to a high value and has difference at least `(n+h+1)−(h−1)=n+2`. Thus the original connector vw must supply n+1. Since w is higher than any old label, this forces `f(w)=n+h+1+kappa`, so `0≤kappa≤Q`. The normalized return deficit would be `m−f(w)=Q−kappa`. It is a necessary value under the assumed extension in the canonical orientation. It does not supply a return state.

## Exact residual bands and sums

Write the high label of index i as `x_i=n+h+1+i` for `0≤i≤Q`. Index kappa is w and all other high indices belong to actual named terminals. The high index i is a label coordinate, independent of the terminal's physical name and local index. If the terminal belongs to a center whose numerical label is j, its absolute difference, minus the common base n+2, is `i+h−1−j`. Since each center occurs once and has exactly one attachment to w, those h attachments occupy the coordinates `[kappa,kappa+h−1]`, each once. All internal differences are exactly `[n+2,m]`, giving the full coordinate interval `[0,Q+h−1]`. Consequently the actual terminal coordinates partition precisely
```
[0,kappa−1] ⊔ [kappa+h,Q+h−1].
```

For i<kappa the largest possible coordinate satisfies `i+h−1≤kappa+h−2<kappa+h`. An eligible terminal difference cannot be in the upper band, and the attachment band is occupied, so it lies in the lower band. For i>kappa the least possible coordinate is i, which satisfies `i≥kappa+1>kappa−1`. It cannot be in the lower band or in the occupied attachment band, so it lies in the upper band. The original weight bijection then makes each lower or upper band exactly the multiset consumed by its corresponding terminals.

In the lower band the required coordinates have sum `sum_(i<kappa) i`. Comparing this with the actual formula gives `sum_(i<kappa)(h−1−j_i)=0` since no coordinate is repeated. Each term is nonnegative, hence every lower index uses the center labeled h−1. In the upper band the largest coordinates `i+h−1` as i runs from kappa+1 to Q already give exactly the required upper interval. Equality with the actual sum gives `sum_(i>kappa)j_i=0`, so every upper index uses the center labeled zero. At kappa=0 the lower index set and coordinate set are empty, and the lower sum and assignment assertion are vacuous. At kappa=Q the upper sets are empty with the same convention. In either case the other band's argument still applies.

## Independent extremal-weight induction and contradiction

There is a separate derivation without using the sum identities. Sweep the required lower coordinates t upwards from 0 through kappa−1. A terminal supplying t has index i≤t because its coordinate is at least i. Every smaller i has already been forced to its own coordinate by induction. The only possible index left is i=t and its center must have j=h−1. This proves the lower assertion with the least coordinate supplying the base. Sweep the upper index i downwards from Q through kappa+1, requiring weight coordinate `i+h−1`. Any high index u supplying it must have u≥i because u+h−1 is its largest possible coordinate. The strictly larger indices already supply their own largest coordinates by induction. Only u=i remains and this forces j=0. The first extremal coordinate supplies the base, and an empty band requires no induction steps.

Thus every actual new terminal would be hosted by one of the two centers labeled zero or h−1. All h centers have distinct labels, so at h≥3 at least one actual physical center has an intermediate label from `[1,h−2]`. It receives no terminals, contradicting its prescribed positive quota. The complementary-interval reduction and global complement cover every affine offset and both slopes. This proves the obstruction throughout the exact size and multiplicity regime. It excludes extensions within the specified embedding class. It is no conclusion of nongracefulness for the original tree.

## Two-center specialization and stronger inventory interpretation

At h=2 the same band argument yields kappa terminals at center one and Q−kappa at center zero. The intermediate-center interval is empty. Matching the physical quotas is necessary. If they match, putting each high index in the forced role gives precisely the lower and upper residual bands, the two attachments occupy the gap and the connector supplies n+1. This recovers [D132](ORDINARY_SPINE_TWO_CENTER_AFFINE_TRANSITION.md)'s exact canonical admission and its all-affine classification when n≥Q+2. The condition is symbolic, and D132's separate positive construction outside that size bound retains its scope. D131's one-center positive transition also retains its exact domain.

The contradiction uses only two inventory properties of the old placement: the occupied labels form a single consecutive interval, and the actual old differences exhaust `[1,n]` with multiplicity one. Suppose a more general old relabeling retains those properties, while the old named graph remains fixed. The complementary-interval reduction, complement, connected bipartition and forced canonical intervals apply verbatim. Set kappa to `f(v)−h` in that orientation. Now the connector, band disjointness, sums and independent induction are identical, so the contradiction still follows. The affine hypothesis was used to guarantee the two old inventory properties and to express kappa in terms of the original deficit as δ or n−δ. This corollary does not require an affine hypothesis for the obstruction once the two inventories are given. It neither determines general relabeling feasibility nor excludes multi-section transitions or ordinary graceful labelings.

## Structural position

D131 and D132 retain their reusable one- and two-center transitions. Under the identical large-prefix single-section inventory regime, increasing multiplicity creates a forced shortage of eligible hosts. The older [R241 relational composition](../references/upstream/mdl/N241_relational_ports.md), [D078 paired suppliers](R241_PAIRED_BRANCHED_SPINE.md) and retained N121/N135/N141 constructions cited in D131–D132 use different input, allocation and composition contracts. They do not inherit this obstruction. A broader single-section architecture in this size regime must change at least one old inventory condition to avoid the proof. A different structural block is another way to change its premises. No general coverage or novelty claim follows.
