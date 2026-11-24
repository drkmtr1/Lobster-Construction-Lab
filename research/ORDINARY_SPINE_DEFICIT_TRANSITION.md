# D131 — Repeatable ordinary-graceful spine deficit transition

## Exact input state

Supply a finite named tree P with n edges and an ordinary graceful labeling g onto `[0,n]`, together with a nonempty ordered simple witnessing spine. Every vertex is within distance two of the spine. Let v be its actual last vertex, and set `delta=n−g(v)`. Exact integer labels give `0≤delta≤n`. The state retains the original graph and incidences, the full labeling, the two consumed inventories, the ordered witness and the named frontier. The deficit only summarizes the arithmetic needed at the next connector. No universal fixed-size compression or arbitrary prefix supply is assumed.

For an original indexed by sections, retain all original indices and append at the next section index. The new spine vertex, center and indexed terminals must have fresh names and the declared roles. For a general named prefix the same proof uses the supplied ordered witness and fresh names for these same incidences. Internal signs and the number of old centers are unrestricted. In particular a D112-compatible seed has delta zero. D112 requires the exact degree-two exit with prescribed neighbor labels 0 and 1, and grows a current branch at that same exit. Here the input need only have the stated ordinary graceful state with its ordered spine and actual deficit. The output advances the spine, and the three D112 pins are unnecessary.

## Single transition and exact admission

Let r be an exact positive integer with r≥delta, and m=n+r+2. Append the next spine vertex w, its center z and r indexed terminal leaves at z. The only new incidences are vw, wz and the r distinct terminal edges. Their endpoints and freshness leave every old vertex, edge, role and multiplicity unchanged. Adding w, z and each terminal in order as a pendant gives a tree with m edges and m+1 vertices. The extended ordered spine is simple. The old witness is its prefix, so every old distance to the witness remains at most two. The new center and terminals have distance one and two.

The independently reserved label palette is `{0} ⊔ [n+2,m]` and the reserved differences are `[n+1,m]`. They depend only on n and r, without assigning any suffix label. Reflect every old vertex by `f(x)=n+1−g(x)`. This gives exactly `[1,n+1]` once each. The reflection negates each signed old difference in the same direction and preserves every old absolute difference. Hence the consumed old spectrum is exactly `[1,n]`.

Assign `f(z)=0` and `f(w)=n+2+delta`. Index k from 0 through r−1. The terminal rule is `n+2+k+indicator(k≥delta)`, since the omitted element of `[n+2,m]` is exactly at zero-based position delta. For k<delta the terminal block is `[n+2,n+1+delta]`, and for k≥delta it is `[n+3+delta,m]`. At delta=0 the first block is empty and every index is shifted. At delta=r the second block is empty and no index is shifted. These rules give every member of the reserved label set once, including the two distinguished labels.

The reflected frontier is `f(v)=1+delta`. The actual connector vw has weight `(n+2+delta)−(1+delta)=n+1`. The attachment wz and r terminal edges have weights equal to the labels of w and the terminals, since all meet the zero at z. Thus that star supplies `[n+2,m]` exactly once. Together with the connector and the unchanged weights on actual old incidences, both full alphabets are exhausted with multiplicity one.

Under the fixed reflection, zero-centered star and reserved palettes, w must have a label in `[n+2,m]`. Since `1+delta≤n+1`, its connector is positive from the old frontier to w and the prescribed weight n+1 forces `f(w)=n+2+delta`. This lies in the interval exactly when r≥delta. Equivalently, assigning the other reserved labels to the star forces some high value at w and uses all high weights on the star, leaving precisely n+1 for the connector. If delta>r then the required label exceeds m, and this prescribed transition is inadmissible. This is a restriction of the specified embedding and assignment contract. It gives no exclusion for other embeddings or ordinary gracefulness.

## Returned state and finite closure

The actual new frontier w is the last vertex of the extended witness. Its only neighbors in the completed prefix are v and z. Its deficit is
```
delta_new = m − (n+2+delta) = r−delta.
```
Thus `0≤delta_new≤r≤m`, and the complete normalized state has the same required form at size m. The central label is zero in this normalized state, and the predecessor label is `1+delta`, so the broader contract works without assuming the D112 pins. Later applications preserve all current names and incidences, including those at w.

For a finite list of exact positive quotas `r_1,...,r_k`, put `n_0=n` and use the given `delta_0`. Define
```
n_i = n_(i−1)+r_i+2
delta_i = r_i−delta_(i−1)
```
and admit exactly the lists with `r_i≥delta_(i−1)` at each step. Necessity is the single-step admission calculation. Sufficiency follows by induction: the initial state is supplied and each admitted step proves both full normalized inventories, the exact named frontier and its bounds at the next size. An equality step returns deficit zero. The empty list leaves the supplied state unchanged. For a D112-compatible seed, the first positive quota is admitted. On a constant quota r the deficits alternate r and zero. More generally, for nondecreasing positive quotas the bound `delta_i≤r_i≤r_(i+1)` admits every next step. For arbitrary finite lists the recurrence gives the exact test, with no claim of automatic admission. In particular a drop below the current deficit fails even if the next quota is positive. Each successful step consumes one list entry, so the procedure terminates after k steps.

## Fixed final alphabet with immutable assigned labels

Fix an admitted finite list. Precompute the sizes and deficits by the stated recurrence. Write `psi_i(x)=n_(i−1)+1−x` as an affine map on the integers. It maps the preceding alphabet `[0,n_(i−1)]` exactly to `[1,n_(i−1)+1]⊂[0,n_i]`. For `0≤i≤k`, set `Psi_i=psi_k ∘ ... ∘ psi_(i+1)` with `Psi_k=id`. Composition is evaluated right to left, so `Psi_(i−1)=Psi_i ∘ psi_i`. Every `Psi_i` is an affine isometry with slope ±1. Nesting of each domain image gives `Psi_i([0,n_i])⊆[0,n_k]`.

Place each supplied prefix label g(x) directly at the final label `Psi_0(g(x))`. At step i use the local rule at size `n_(i−1)` and deficit `delta_(i−1)` for the fresh vertices only, followed by `Psi_i`. An old physical vertex with normalized value x just before step i has already been assigned `Psi_(i−1)(x)`. Its value according to the reflected step and subsequent embedding would be `Psi_i(psi_i(x))`, exactly the same integer. Therefore no final label already written is changed. All actual absolute edge differences are those computed in each normalized step, since absolute difference is invariant under the affine isometry applied to both endpoints. This includes the crossing connector, whose old endpoint reached the same final value by the embedding identity.

Consequently at completed section boundary i the used labels and differences, remaining inventories and frontier label are exactly
```
used labels       = Psi_i([0,n_i])
used differences  = [1,n_i]
R_i               = [0,n_k] minus Psi_i([0,n_i])
D_i               = [n_i+1,n_k]
frontier          = actual v_i
frontier label    = Psi_i(n_i−delta_i)
```
The new label reservation is `Psi_i({0} ⊔ [n_(i−1)+2,n_i])`. The old used labels are `Psi_i([1,n_(i−1)+1])` by the embedding identity. Their disjoint union is `Psi_i([0,n_i])`, because `Psi_i` is injective. The new difference reservation `[n_(i−1)+1,n_i]` is disjoint from `[1,n_(i−1)]` and extends it to `[1,n_i]`. The size recurrence determines both reservations before any suffix assignment or suffix edge construction. The deficits determine the chosen frontier labels inside those palettes. Subtracting these disjoint additions from the previous residual inventories gives the displayed new residuals.

At boundary i<k, the only unfinished edge incident to the assigned prefix in the declared final target is the actual next connector `v_i v_(i+1)`. Every center and terminal of a completed section already has all its incidences. All other unfinished edges lie entirely in later sections. At i=k the identity embedding leaves both residual inventories empty. For k=0 the same formulas put the already complete prefix in its original normalized alphabet. The affine embeddings can be accumulated backwards with one coefficient pair per step. A forward pass then assigns each original vertex and incidence once in the final alphabet. These symbolic arguments prove closure without any numerical extension.

## Comparison with retained results

- [D112](ORDINARY_EXTREME_SPINE_GROWTH.md) preserves the extreme-pinned degree-two spine exit and grows its existing off-spine branch. D131 advances the physical frontier and reflects the entire normalized prefix. The D112 interface supplies deficit zero and is a sufficient starting contract.
- [D104–D107](ORDINARY_43_2_EXTREME_SPINE.md) distinguish the non-alpha `[[4,3],[2]]` target from its ordinary graceful extreme-port seed, the one retained growth example and the indexed right-terminal family. D105 gives a usable deficit-zero input on a target with no alpha labeling by [D104](R241_43_2_LEFT_TERMINAL_ZERO.md). [D130](ORDINARY_2AC_2_MODIFIED_CORE_CLASSIFICATION.md) independently provides a three-left-center deficit-zero input.
- [R241.1](../references/upstream/mdl/N241_relational_ports.md#n241-full-review) combines supplied alpha modules at actual matching ports with relational equality of offsets. It shifts the old high class to move its weights into a higher band. D131 uses an ordinary prefix and a zero-centered star, keeps old absolute weights unchanged and admits the next section by a deficit inequality. [D078](R241_PAIRED_BRANCHED_SPINE.md) supplies one-center paired blocks at matching offsets and a distinct empty-trailing-section consumer. Its normalized alpha prefix covers its stated quota classes, including unrestricted positive one-center sequences when supplied from the beginning by its own construction.
- [N121](../references/upstream/mdl/N121_retained_record.md) supplies strongly labeled height-two factors in its odd terminal-quota domain and composes unequal factors with the stated first and later root-degree conditions. Its factor-internal weights collectively occupy the lower band, and its actual spine weights occupy the higher band under the prescribed alternating root labels. [N135](../references/upstream/mdl/N135_retained_record.md#n1353--exact-binary-loop-allocation-criterion) uses residue closure and strict local quota capacity in a restricted chronological four-child loop model. [N141](../references/upstream/mdl/N141_retained_record.md#n1412--complete-criterion-proof-separate-review-and-director-disposition) uses a restricted quota-class automaton and inventories of actual factor branches to construct admissible ordered allocations within that model. Those results supply different whole-factor families and criteria. D131's arithmetic interface starts from a supplied ordinary prefix, appends one center and gives exact admission in its own placement. It implies no inclusion between the general graph domains or historical priority.

This is a conditional reusable ordinary spine transition. Independent supply for arbitrary starting prefixes and extension to additional centers in a new section remain separate obligations.
