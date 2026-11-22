# Retained constructions and the R226 consumer

## What is implemented

The code supplies direct constructions, a unit-size convenience alias, and a structural completion API. They include retained formulas, a padded composition, and separate zero-padding suppliers with their own domains and interfaces. Each construction calculates labels directly from parameters and its specified topology. R226 takes independently supplied core labels and completes a precisely described two-host leaf attachment when its exact conditions pass. None of these APIs selects a convenient complete labeling and then presents a fragment of that answer as a general input rule.

| API | Independently supplied input | Successful output | Scope boundary |
|---|---|---|---|
| `caterpillar(profile)` | Exact ordered profile with every branch size zero | Complete graceful labeling | Supplied spine representation only |
| `l007(q, r, z=0)` | Positive branch size `q`, positive number `r`, nonnegative direct-leaf count `z` | Complete graceful labeling | One uniform cluster and its terminal next-spine edge |
| `l010(qs, z, suffix_profile)` | Positive ordered branch sizes, sufficient direct-leaf count, an exact all-direct-leaf suffix | Complete graceful labeling | One branched section; the stated separated-block budget must hold |
| `h010(qs, z, suffix_profile)` | Positive ordered branch sizes, sufficient direct-leaf count, an exact all-direct-leaf suffix | Complete graceful labeling | One branched section; both packed-interval conditions must hold |
| `two_section_padded(q,r,z0,z1,K)` | Two positive branch sizes, specified direct-leaf counts satisfying both budgets, a positive pure-path suffix length | Complete graceful labeling | A composition corollary of retained L010 prefixes under the stated budgets |
| `two_section_balanced(q,K)` | Equal positive branch sizes `q`, no direct leaves, positive suffix length `K` | Complete graceful labeling | Project-derived symbolic supplier; unequal sizes are outside its domain |
| `two_section_nonadjacent(q,r,K)` | Any positive q,r, no direct leaves, K>=2 | Complete graceful labeling | Independent formula supplies a two-above port and exact original path consumer |
| `two_section_k1(q,r)` | Any positive integers q,r, no direct leaves, K=1 | Complete graceful labeling | Retained R241 specialization; singleton R={q+4}, D={q+3}, physical port s:2=1 |
| `three_section_nonadjacent(q,r,t,K)` | Integers q>=r>=1, t>=1, K>=2, no direct leaves | Complete graceful labeling | Three original branches and s:3 path; R241/L008 corollary with independent left supplier |
| `three_section_qltr_adjacent(q,r,t,K)` | Integers 1<=q<r, 1<=t<=q+1, K>=1, no direct leaves | Complete graceful labeling | Original adjacent port s:3=a+K; R241 with a direct left supplier and class-reversed L008 |
| `three_section_qltr_large_t(q,r,t,K)` | Integers 1<=q<r, r>=3, t>=q+2, K>=2, no direct leaves | Complete graceful labeling | Explicit parity alpha seed, high-side shift and original nonadjacent port s:3=a+K+1 |
| `three_section_q1_r2(t,K)` | Integers t>=3, K>=2, fixed q=1, r=2 and zero padding | Complete graceful labeling | Fixed alpha seed, prescribed leaf extension and original nonadjacent port s:3=t+K+5 |
| `three_section_k1(q,r,t)` | Positive integers q,r,t, K=1 and zero padding | Complete graceful labeling | Direct singleton R={q+2}, D={t+3} at s:3=q+t+5 |
| `four_section_unit(K)` | Positive integer K, four successive unit branches and zero padding | Complete alpha graceful labeling | Adjacent interval R=[6,K+5], D=1..K at s:4=K+6 |
| `four_section_111t(t,K)` | Integers t>=2 and K>=1, original branch sizes 1,1,1,t and zero padding | Complete graceful labeling, alpha for K=1 | At s:4, use the singleton R={4}, D={t+3} for K=1 or the above-side nonadjacent interval for K>=2 |
| `two_section_unit(K)` | Positive suffix length `K` | Complete graceful labeling | Alias for `two_section_balanced(q=1,K=K)` |
| `complete_two_host(graph, core_labels, hosts)` | Original target, connected labeled core, two distinct physical hosts | Exact fixed-core completion or restricted obstruction | Does not supply the core labeling, host choice, or a palette partition |

All implementation uses exact Python integers and standard-library containers. No numerical approximation, optimizer tolerance, or solver extraction is part of these APIs. Constructor domain failures raise `ValueError`. They do not establish nongracefulness.

The exceptional B3 CLI method `three_section_q1_r2` admits exactly the keys `t` and `K`. Its independently declared profile must match the original fixed branch counts `1,2,t`. For K=1, `three_section_k1` admits exactly `q,r,t` and the original profile `[[q],[r],[t],[],[]]`. The five constructors cover all positive `q,r,t,K` on the zero-padding B3 profile. [Deterministic selection rule](../research/B3_UNPADDED_K1.md#deterministic-selection-for-every-positive-path-length)

The B4 CLI method `four_section_unit` admits exactly the parameter `K` and requires the caller's original `[[1],[1],[1],[1]]+[[]]*(K+1)` profile. The existing 10,000-vertex CLI limit gives `K<=9987`; the direct constructor has no such preflight cap. [B4 proof](../research/B4_UNPADDED_UNIT.md)

The B4 CLI method `four_section_111t` admits exactly `t` and `K` on the declared `[[1],[1],[1],[t]]+[[]]*(K+1)` target. Its 10,000-vertex graph limit gives `t+K<=9988`. The inherited result byte cap also applies. Choose `four_section_unit` for t=1 and `four_section_111t` for t>=2. [B4 111t proof](../research/B4_UNPADDED_111T.md)

## The exact target remains part of the input

In a profile, section `i` corresponds to spine vertex `s:i`. Entry `q` at branch position `j` supplies vertex `b:i:j`, joined to `s:i`, and `q` terminal vertices `l:i:j:k`, each joined to that branch center. A zero entry is a direct leaf represented by its branch ID. Positive branch sizes are not silently sorted, branches are not collapsed by symmetry, and trailing empty spine sections are preserved.

For a profile with `k` sections, its edge count is

\[
m=(k-1)+\sum_{i,j}(1+q_{i,j}).
\]

`validate_graph` checks a finite simple connected tree, a supplied or inferred supporting spine, and agreement of every profile vertex, incidence, and role. Inference uses two simultaneous leaf-pruning rounds and retains the last nonempty small core. Every target vertex must be within two edges of the supporting spine. A graph may instead be supplied by explicit named vertices and edges, with no profile. The R226 wrapper accepts these lobster targets even though the retained mathematical theorem has a broader finite-tree domain.

The SHA-256 identity includes original vertex IDs, undirected edges, and any supplied `profile`, `spine`, and `roles`. Sorting vertex/edge listings or reversing an edge's endpoint order does not change the identity. Changing the named topology or its supplied representation does. Vertex labels, source citations, and other result metadata are outside the graph digest. A certificate must still be checked against the independently held original target; a digest provided by an untrusted result is not that independent specification.

## Caterpillar interval construction

Maintain unused labels

\[
R=[\ell,r]\cap\mathbb Z,
\]

unused differences `1..N`, where `N=r-ell+1`, and current spine label `ell-1` or `r+1`. Give each direct leaf the far endpoint of the unused interval. Its edge consumes difference `N`; the same spine label remains just outside the shortened interval. Give the next spine vertex the far endpoint in the same way; its label is immediately outside the opposite end of the new interval. Each step consumes exactly one actual vertex label and one actual edge difference.

The complete constructor starts at label zero with `R=1..m`. The zero-edge singleton is accepted and receives label zero. The routine intentionally rejects a positive branch size in the supplied representation, even if the underlying tree has another caterpillar spine. The retained source gives this endpoint proof in [MATHEMATICS.md, section 6](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/MATHEMATICS.md#6-caterpillar-interval-baseline).

## L007: an equal-size local cluster

For `q>=1`, `r>=1`, and `z>=0`, write `s=q+1`. The exact profile is `[[q]*r + [0]*z, []]`, with

\[
m=sr+z+1.
\]

The root gets zero. In one-based branch indices, center `i` gets `s*i`, and its terminal leaf `j` gets `s*(r-i)+j`. The next spine vertex gets `sr+1`; direct leaves get `sr+2..m`.

This covers every label and edge difference once. It supplies no later suffix budget: there is only the one terminal next-spine edge in the target. That distinction is recorded in the returned claim scope. The formula and retained proof are [L007 in LEMMAS.md](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md).

## L010 and H010: one branched section with a specified suffix

Let `qs=[q1,...,qr]` have positive entries and let `suffix_profile` contain only zero entries. Its internal edge count is

\[
K=(\text{number of suffix sections}-1)+\text{number of suffix direct leaves},
\]

and `K>=1` is required. The complete target profile is `[qs+[0]*z] + suffix_profile`, so

\[
m=K+1+\sum_i q_i+r+z.
\]

Both formulas put zero at the first root and `K+1` at the next spine vertex. A positive branch uses a consecutive leaf interval `A_i=[t_i,t_i+q_i-1]` and center `b_i=2*t_i+q_i-1`. Reflection around that center sends the leaf interval to itself, so the branch's leaf-label inventory and its branch-edge differences agree. The center label is also the difference on its root edge. Unused labels in `K+2..m` go to the prescribed direct leaves. This leaves labels and differences exactly `1..K` with current label `K+1`, which the caterpillar suffix consumes.

For **L010**, use `t_1=K+2` and `t_(i+1)=b_i+1`. The actual final alphabet must satisfy `m>=b_r`. This is a sufficient budget for this formula; it is not a lower bound on all graceful labelings. Its [retained L010 statement](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md) includes `K=1`, `qs=[1,2]`, and `z=8`, giving a 15-edge target.

For **H010**, write `Q=sum(qs)` and pack the leaf intervals using `t_i=K+2+sum(q_j for j<i)`. Check both

\[
Q\le K+2,
\qquad
z\ge\max(0,K+2+Q-q_r-r).
\]

These conditions keep all centers distinct from all leaf intervals and within `0..m`. The [retained H010 proof input](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/H010-proof.txt) gives `K=1`, `qs=[1,2]`, `z=2`: centers 6 and 9, terminal leaves 3 and 4,5, direct leaves 7,8, next-spine label 2, and final suffix label 1. This is a 9-edge target, with exactly the user-supplied two direct leaves. The implementation does not add padding vertices to an original target in order to make a formula fit.

These suffix APIs preserve the ordered input. They do not optimize branch order or claim minimum padding, and they do not accept an arbitrary further branched suffix.

## Two padded sections: a composition baseline

The interval interface is more general than `R=Q`: the label interval may be `[ell,r]`, while differences remain `1..K`, with an active endpoint just outside that label interval. Translation preserves differences, and reflection can switch which interval endpoint is active. A future supplier experiment must compare its claimed advance with suitable normalized or reflected composition of the retained constructions. A target having two branched sites, by itself, does not establish a new construction beyond that baseline.

`two_section_padded(q,r,z0,z1,K)` implements one concrete composition, derived during project assembly from the displayed retained L010 prefix formulas and the caterpillar invariant. This derivation was independently recalculated by the implementation and methods roles. It is a project corollary with finite implementation checks, not an additional upstream retained lemma, a novelty finding, or formal verification.

The exact target profile is

```python
[[q] + [0]*z0, [r] + [0]*z1] + [[] for _ in range(K + 1)]
```

Require `q,r,K>=1`. Set

\[
K_1=r+z_1+K+2,
\qquad z_1\ge K+1,
\qquad z_0\ge K_1+1.
\]

There is no additional upper bound on `q` or `r`. These inequalities concern the supplied direct leaves: the routine never changes the target to satisfy them. The complete graph has `m=q+r+z0+z1+K+4` edges.

**First prefix.** With one positive branch of size `q` and pending edge budget `K1`, the L010 prefix uses leaf interval `[K1+2,K1+q+1]`, center `2*K1+q+3`, root zero, and next-spine label `K1+1`. The available alphabet has maximum `m=K1+q+z0+2`, so the center budget is equivalent to `z0>=K1+1`. The prefix leaves unused labels and differences `1..K1`. This prefix identity does not assume the untouched pending topology is a caterpillar.

**Second prefix.** In local coordinates, the second branch of size `r`, its `z1` direct leaves, its next-spine edge, and the final `K` path edges form a `K1`-edge target. The same one-branch prefix is valid because `z1>=K+1`. Map each of its assigned local labels `g` to

\[
f=K_1+1-g.
\]

This map sends its local root zero to the already assigned physical vertex `s:1` at `K1+1`. It preserves every edge difference, uses only the first prefix's available labels, and places `s:2` at `K1-K`. The remaining interface is exactly

\[
R=[K_1-K+1,K_1],\qquad D=\{1,\ldots,K\},\qquad f(s:2)=K_1-K.
\]

**Final path.** The active label is one below the remaining label interval, so the ordinary endpoint invariant completes the specified `K` edges. Both prefix snapshots and their remaining inventories are returned in the trace and independently checked in tests.

For example, `q=r=K=1`, `z1=2`, and `z0=7` meet both budget bounds with equality and give 16 edges. The spine labels are `0,7,5,6`; the two positive-branch centers are 16 and 1. The second prefix leaves label 6 and difference 1 for the final edge. This example illustrates the recipe boundary, not the smallest possible graceful target.

```python
from lcl.constructors import two_section_padded
from lcl.verify import verify_certificate

result = two_section_padded(q=1, r=1, z0=7, z1=2, K=1)
report = verify_certificate(result["graph"], result["labels"], result["graph_digest"])
assert report["valid"], report["errors"]
```

The implementation uses a dedicated prefix helper. It does not pass a branched suffix to `l010()`, whose full-constructor domain remains unchanged. The source formulas remain [L010](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md) and the [caterpillar interval proof](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/MATHEMATICS.md#6-caterpillar-interval-baseline); the two-stage composition above is the project's explicit inference from them.

## Equal branch sizes without padding

`two_section_balanced(q,K)` supplies the exact profile `[[q],[q]]+[[] for _ in range(K+1)]` for every integer `q>=1` and `K>=1`. There are no direct-leaf padding vertices. This is a new project derivation, recorded with its separate mathematical review in [B2_BALANCED_SUPPLIER.md](../research/B2_BALANCED_SUPPLIER.md); it is not an additional upstream retained lemma or a historical novelty claim.

Set `m=K+2*q+4`. Supply the first three spine labels and both branch centers directly:

\[
f(s_0)=m,\quad f(b_0)=0,\quad f(s_1)=q+1,
\quad f(b_1)=K+q+3,\quad f(s_2)=K+q+2.
\]

For zero-based terminal indices `j=0,...,q-1`, give the first branch's leaf `j` label `K+q+4+j` and the second branch's leaf `j` label `j+1`. Their actual prefix edges have the following differences:

| Actual edge group | Difference inventory |
|---|---|
| `s1—s2` | `K+1` |
| `s1—b1` | `K+2` |
| `b1` to its terminal leaves | `K+3..K+q+2` |
| `s0—s1` | `K+q+3` |
| `b0` to its terminal leaves | `K+q+4..K+2*q+3` |
| `s0—b0` | `m=K+2*q+4` |

These disjoint blocks fill `K+1..m`. The prefix labels fill the disjoint intervals `0..q+1` and `K+q+2..m`, leaving exactly

\[
R=[q+2,K+q+1],\qquad D=\{1,\ldots,K\},\qquad f(s_2)=K+q+2.
\]

The active label is one above the remaining label interval, so the retained endpoint invariant completes the specified `K` path edges. The formula takes only `q,K`; it does not extract a prefix from a previously completed labeling or run a solver. The result records the complete independently supplied prefix and resource interface, which the tests check separately from the final witness.

`two_section_unit(K)` is the `q=1` wrapper. It gives the original unit-case spine prefix `K+6,2,K+3` and leaves labels `3..K+2` for the path. The balanced family covers every positive `q,K` in its stated domain, while unequal branch sizes and arbitrary branched suffixes remain outside this constructor. Both CLI methods pass through the bounded ingestion guards before expansion.

## R226: extract a fixed-core completion without search

The input target contains a connected labeled core. Every unassigned actual vertex must be a leaf whose only neighbor is one of the two distinct already-labeled hosts. The original target determines the two quotas, including zero quotas. Hosts need not be adjacent. Core labels must be injective integers in the final `0..m` alphabet, and actual core-edge differences must be distinct. No complete graceful starting labeling is an input.

Order the hosts by label `a<b`. Let `X` be unused labels and `D` unused differences. Every unused label `x` has eligible host options with differences `abs(x-a)` and `abs(x-b)` that belong to `D`. Build a difference multigraph with all vertices in `D`, including isolated ones:

- No eligible option rejects the fixed instance.
- One option gives a forced half-edge.
- Two distinct differences give an ordinary edge with host tags.
- Two equal differences give the one possible midpoint loop, preserving both host choices.

For every connected component, the number of label edges, including loops and half-edges, must equal its number of difference vertices. Under the retained absolute-difference geometry, each balanced component is a tree with one half-edge, a unicyclic component with one reflected parallel pair, or a unicyclic component with the midpoint loop.

The implementation roots trees at the half-edge or cycle and assigns every noncycle edge outward. These assignments are forced. A parallel pair's two label values must go together to one host; splitting the pair is not another valid orientation. A midpoint label can go to either host. If `A0` counts forced assignments to the lower-labeled host, `c` counts pair components, and `eta` is zero or one for the midpoint, its attainable integral quotas are exactly

\[
\{A_0+2j+\varepsilon:0\le j\le c,\;0\le\varepsilon\le\eta\}.
\]

The fractional projection is `[A0,A0+2c+eta]`. After all row and balance checks, an integer quota needs interval membership and, when there is no midpoint, the appropriate parity. The algorithm selects the necessary number of whole pairs, assigns the midpoint if present, then maps each host's allocated values to its original named leaves in sorted order. Core labels and every original incidence remain fixed.

The allocation stage takes `O(Q log Q)` time and `O(Q)` auxiliary storage for `Q` unassigned leaves. Validating and hashing the complete named tree adds `O(n log n)` time and `O(n)` storage. This is structural extraction, with no exponential solver, backtracking, hidden timeout, or optimization fallback.

The source is [R226.1 revision 2 and its subsequent review and closeout](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n226-researcher). The retained closeout adopted a written proof with separate AI mathematical review. The code is an implementation of that retained result, not formal verification, qualified human review, a novelty finding, or a general lobster construction.

### Result meanings

| Status | Meaning |
|---|---|
| `SAT` | A full completion of the exact target extends every supplied core label. The independent checker must validate the returned witness. |
| `RESTRICTED_INFEASIBLE` | That exact supplied core and actual host quotas admit no completion under the R226 theorem. Other core labelings remain unexcluded. |
| `INVALID_INPUT` | The supplied graph, core labeling, or pending-vertex shape falls outside this API's stated domain. |

Each result records the fixed core, physical hosts, target digest, actual quotas when available, source, and scope limitations. Development assertions check the final inventory locally; they are not presented as the independent verifier.

The N224 control is retained explicitly: core path `U-A-B-V` with labels `3,1,5,0`, plus one pending leaf at each of `A,B`, leaves `X={2,4}` and `D={1,3}`. One reflected pair allows host totals zero or two, so the requested total one fails. The same target is graceful with `(A,B,U,V,Xleaf,Yleaf)=(0,5,1,2,4,3)`. This makes the distinction between fixed-core failure and ordinary nongracefulness concrete.

## Validation performed

The construction/model and allocation test modules contain 30 test methods, including:

- Independent certificate checks for the singleton, paths, direct-leaf profiles, 48 L007 parameter cases, and H010/L010 documented and varied-suffix cases.
- The composed two-section recipe at its budget boundary, with larger branch sizes and extra padding, including independent checks of both prefix resource inventories.
- The equal-branch formula with zero padding across nine `(q,K)` combinations, unit-alias checks, domain rejection, and independent full-witness and prefix-inventory checks. These finite checks accompany the symbolic argument; they do not replace it.
- Exact target checks for original incidences, branch roles, trailing empty sections, Boolean rejection, and digest identity.
- R226 comparison against direct enumeration for all 120 ordered core-label cases on nine tiny two-host targets, with at most four unassigned leaves per instance.
- Further nonadjacent-host comparisons, the documented N224 obstruction, a graceful labeling of its same target, zero-completion cases, midpoint choices, and forced half-edges.

These finite implementation controls do not prove the retained theorems or extend their domains. The independent verifier has its own graph reconstruction and edge/label checking code; it imports no constructor, allocation routine, or model validation function.


## Conditional nonadjacent path consumer

`lcl.consumers.complete_nonadjacent_path(graph, prefix_labels, K, ell)` accepts a caller-supplied original graph supported by `verify_partial` (including its lobster requirement) and a compatible partial labeling, validates the exact named path from `s:2`, inventories and nonadjacent port, and returns a new complete label mapping checked on that original graph. Its domain is integer `K>=2` and an integer `ell` compatible with the graph's final alphabet. The conditional mathematical proof applies to any original tree meeting its assumptions. The helper does not supply the prefix. The separate recurrence, proof and K=1 exclusion are in [B2_NONADJACENT_CONSUMER.md](../research/B2_NONADJACENT_CONSUMER.md); the existing adjacent-port `interval_boundary` is unchanged.


## All-q,r unpadded two-section supplier

`two_section_nonadjacent(q,r,K)` constructs the exact unpadded two-section graph for positive integer `q,r` and integer `K>=2`. Its prefix trace carries the physical port, prefix labels, and both unused inventories; the unchanged nonadjacent consumer completes the original path. The CLI constructor method of the same name requires an independently declared `profile` and exact `q,r,K` parameters, and rejects oversized targets before expansion. Its algebra, comparisons and K=1 limitation are in [B2_UNPADDED_ALL_QR.md](../research/B2_UNPADDED_ALL_QR.md).

`two_section_k1(q,r)` is a separate R241/R212-B specialization for `[[q],[r],[],[]]`. Its prefix trace leaves the singleton label `q+4` and difference `q+3` at original `s:2=1`; it assigns the final vertex `s:3=q+4`. CLI method `two_section_k1` requires the caller's independently declared profile and exact `q,r` parameter keys; the preflight rejects invalid integers and a vertex count above its cap before expansion. The theorem and source derivation are in [B2_UNPADDED_K1.md](../research/B2_UNPADDED_K1.md). Neither K>=2 behavior nor the adjacent `interval_boundary` predicate is redefined.

`three_section_nonadjacent(q,r,t,K)` requires integer `q>=r>=1`, `t>=1`, `K>=2` and the original zero-padding profile with three branches. Its directly supplied prefix records `[a,a+K-1]`, `1..K`, and physical `s:3=a+K+1`, where `a=q+t+3`. It validates the original remaining incidences, applies the existing recurrence sequence to the s:3 path, and checks the completed graph; the caller must verify against its independently retained original target. CLI admission requires exactly `q,r,t,K` and rejects invalid or oversized parameters before target expansion. See [B3_UNPADDED_QGE_R.md](../research/B3_UNPADDED_QGE_R.md). The public B2 `complete_nonadjacent_path` retains its s:2 contract.
