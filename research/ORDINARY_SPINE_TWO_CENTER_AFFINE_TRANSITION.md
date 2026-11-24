# D132 — Two-center affine ordinary spine transition

## State and topology

Use [D131](ORDINARY_SPINE_DEFICIT_TRANSITION.md)'s supplied named ordinary graceful prefix P with n edges, its full labeling g onto `[0,n]`, its ordered witnessing spine and its actual last spine vertex v. Retain both consumed inventories and all names, labels and incidences in the supplied state. The exact integer deficit is `delta=n−g(v)`, with `0≤delta≤n`. No alpha condition, signed-edge condition or assumption of universal prefix supply is needed.

At the next section index append one fresh spine vertex w, two fresh physical centers with independently specified exact positive integer quotas q and a, and their fresh terminals at each original physical index. The only old-to-new incidence is vw. The new section has two attachments from w to its centers and the q+a distinct pendant incidences. Thus it adds precisely `q+a+3` vertices and the same number of edges, including vw, and the total edge count is `m=n+q+a+3`. Adding each new vertex successively as a pendant preserves connectedness and acyclicity. The old witnessing spine is a prefix of the extended simple spine. Old vertices remain within distance two of it and new centers and terminals have distance one and two respectively. Every old original incidence and its multiplicity is preserved. Use the physical section, center and terminal indices without changing either center's name or ordering.

## Canonical two-center construction

Use one of the two old-prefix embeddings below. Each is an integer affine isometry sending the old alphabet bijectively onto `[2,n+2]`.

| Mode | Embedding | Effective incoming coordinate κ |
| --- | --- | --- |
| Reflection | `psi(x)=n+2−x` | δ |
| Translation | `psi(x)=2+x` | n−δ |

In either case the embedded frontier label is `2+κ`. All original absolute weights remain `[1,n]`, since the common affine isometry preserves absolute differences even when it reverses their signed values. Reserve the suffix labels `{0,1} ⊔ [n+3,m]` and weights `[n+1,m]` before assigning anything. These are exact complements of the old resources and depend only on the declared sizes.

A mode is admitted when κ is one of q,a. Prefer reflection if admitted. Otherwise choose translation when admitted. Assign center label one to a matching physical quota, using the smaller physical index if both match. Assign zero to the other center. This rule selects two distinct actual center names, and each keeps precisely its own terminal indices. Set `f(w)=n+3+κ`. Assign the increasing interval `[n+3,n+2+κ]` to the actual terminals at the center labeled one and `[n+4+κ,m]` to those at the center labeled zero. Their sizes are κ and q+a−κ, the actual required quotas in each role, even when the original quotas are unequal or both match. These intervals partition the high block with `{f(w)}`, so together with the two distinct center labels and the old block the entire alphabet is consumed once.

| Actual incidence group | Absolute spectrum |
| --- | --- |
| Old prefix edges | `[1,n]` |
| Connector vw | `(n+3+κ)−(2+κ)=n+1` |
| Terminals at center one | `[n+2,n+1+κ]` |
| Attachment to center one | `n+2+κ` |
| Attachment to center zero | `n+3+κ` |
| Terminals at center zero | `[n+4+κ,m]` |

Every new weight in the table is the label of a high endpoint minus its actual lower label. Each entry is used once because the translated terminal intervals have no repeated labels and the two attachments occupy their stated singletons. The ordered blocks are consecutive and disjoint, proving ordinary gracefulness. The return frontier is w, with exact neighbors v and the two centers. Its normalized deficit is `m−f(w)=q+a−κ`, the quota of the other physical center. This is a positive integer at most m. It satisfies D131's larger state contract. The degree-three output has a different physical interface from D112's degree-two state.

## Exact canonical admission and forced terminal assignment

Fix an old embedding with image `[2,n+2]` and the stipulated center labels 0,1. Write `H=[n+3,m]`, let y=f(w) and let b be the physical quota of the center labeled one. The high labels H occur at w and precisely the terminals. All internal suffix weights lie in `[n+2,m]` since each high label meets zero or one. Thus the actual connector must have the otherwise missing weight n+1. As y exceeds the inherited frontier label, `y−(2+κ)=n+1`, so `y=n+3+κ`.

The sum of the internal suffix differences counts each high label once and y a second time on the other attachment. Each edge to one subtracts one, with b+1 such edges including that attachment. Hence the sum is `sum(H)+y−(b+1)`. The exact required sum of `[n+2,m]` is `sum(H)+(n+2)`. Equating them yields `y=n+3+b` and therefore b=κ. In particular κ must equal an actual physical quota.

For every high label x below y, the weight x−1 must appear. Starting with the least x=n+3, it can only come from x at center one because x−1 is outside H. In ascending order the only other candidate is x−1 at center zero, which was already forced to center one. Neither attachment has so small a weight. Thus every high label below y goes to center one. For each x above y, the weight x must appear. Starting at m, the only candidate is x at center zero because x+1 is outside H. In descending order the alternative x+1 at center one was already forced to center zero. Neither attachment is above y. Hence the upper interval goes entirely to center zero. These hand proofs force the label sets for any assigned center roles. The constructive rule specifies their increasing physical index order. The proof does not require a bound on n beyond the input state.

## Converse for all affine isometries at large prefix size

Suppose `n≥q+a+2` and a successful extension transforms every old label by one affine isometry of the line, restricting to the exact integer alphabet. Its image is a consecutive block `[L,L+n]`. The only labels available for the suffix are the two complementary intervals, of total size q+a+3. Each individual interval has width at most q+a+2 whenever nonempty. The old edges already use precisely `[1,n]`. Thus no new internal edge can have both endpoint labels in one interval. This remains true at equality n=q+a+2 because a new weight must exceed n strictly. The suffix has internal edges, so both intervals are nonempty.

The actual internal suffix tree is connected. Membership in either interval is a proper bipartition, so the two intervals correspond exactly to its two bipartition classes, up to swapping. One class consists of the two centers, both adjacent to w. The other consists of w and every terminal. All labels in each interval are used, so the center interval has two labels. If the centers occupy the upper interval, complement the entire output by `x↦m−x`. This preserves every absolute difference, all names, and affine isometry of the old labeling, while exchanging the roles of the lower and upper intervals. With centers lower, that interval is exactly `{0,1}` and the old block is `[2,n+2]`. The only affine modes on that old block are precisely the displayed translation and reflection, since the range fixes the offset in either slope. Here n is positive. Apply the canonical necessity just proved.

Conversely, if `{δ,n−δ} ∩ {q,a}` is nonempty, the canonical construction gives an extension under an affine isometry. This proves the exact all-affine classification under the size bound, including equality. Without the bound the canonical positive result still applies, and the other affine placements are unresolved when the canonical modes fail. A restricted affine obstruction makes no claim about other relabelings or ordinary gracefulness of the extended tree.

## Reusable mixed lists and policy

In the common D131 state, the one-center reflection for section `[r]` admits `r≥δ` and returns `r−δ` for exact positive r. The two-center reflection for `[q,a]` admits exactly δ equal to q or a and returns the other quota. The translation mode replaces δ by `n−δ` when testing equality and returns `q+a−(n−δ)`. Each admitted step produces the full normalized alphabets and the actual extended witness with its returned deficit. Consequently a finite mixed list with an admitted mode at every stage closes by induction. The empty list is the supplied state. The same conclusion holds when following the deterministic preference along a list that it admits.

At a single two-center step the deterministic policy succeeds whenever either canonical mode is admitted. This local fact does not equate deterministic admission of an entire list with existence of an admitted mode plan. If both modes are available, the returns can differ. For example, under the symbolic state conditions `q<a`, `δ=q` and `n=q+a`, reflection returns a while translation returns q. A subsequent D131 quota equal to q would admit the latter return and fail the former. This is a conditional comparison of the scalar rules with no numerical extension. In particular an explicitly selected alternative admissible policy may be used for the list, instead of claiming the fixed preference solves all existence-of-plan questions.

From any supplied deficit-zero seed, take independently chosen exact positive integers `p_0,...,p_k`. The initial `[p_0]` D131 step returns p_0. At the next `[p_(i−1),p_i]` section, reflection is admitted with κ=p_(i−1) and returns p_i. Induction gives exactly the displayed successive deficits, with equal quotas handled by the physical tie rule. For k=0 only the initial one-center step is required. The deterministic reflection preference follows this plan. This symbolic family permits any finite length and independent adjacent positive parameters, without instantiating a numerical suffix.

## Fixed-final-alphabet realization

For any admitted finite list, precompute the sizes n_i, deficits δ_i, physical role choices and affine coefficients of the selected modes. Each local embedding `psi_i` maps `[0,n_(i−1)]` injectively into `[0,n_i]`, using the D131 block `[1,n_(i−1)+1]` or the D132 block `[2,n_(i−1)+2]`. Its complement within `[0,n_i]` is exactly its local fresh label reservation. The local difference reservation is always `[n_(i−1)+1,n_i]`.

Define Ψ_i as the composition of all later modes in application order, with the last mode outermost. At the final boundary Ψ_final is the identity and `Ψ_(i−1)=Ψ_i∘psi_i`. All these maps are affine isometries. Repeated inclusion sends `Ψ_i([0,n_i])` into the final alphabet. Initially write the old supplied labels after Ψ_0. At step i write only the new vertices under their local assignments followed by Ψ_i. An already written vertex whose previous normalized label was x has value `Ψ_(i−1)(x)=Ψ_i(psi_i(x))`, so no physical label changes. Because Ψ_i is injective, the mapped fresh reservation is disjoint from the old used block and their union is `Ψ_i([0,n_i])`. This also places both actual connector endpoints in the same isometric image, preserving its difference. Every new difference belongs to the independently reserved upper interval, and together with the unchanged old weights the used difference inventory is `[1,n_i]`.

Thus at each boundary i the exact remaining labels and weights are `[0,n_final] minus Ψ_i([0,n_i])` and `[n_i+1,n_final]`. The actual named frontier is the last supplied spine vertex with final label `Ψ_i(n_i−δ_i)`. Each completed section has all of its center and terminal incidences supplied. Only the actual next spine connector crosses from assigned to unassigned vertices, if another section remains. All other pending incidences lie entirely in later sections. In the final alphabet both residual sets are empty. A finite scan plans the admitted steps, accumulating affine coefficient pairs backwards uses constant indexed operations per step, and forward emission visits each final vertex and edge once. The total number of indexed output operations is linear in final tree size.

## Scope and comparisons

D131 supplies the one-center operation and fixed-final-alphabet construction used here. [D112](ORDINARY_EXTREME_SPINE_GROWTH.md) grows a branch at an unchanged degree-two extreme exit, while D132 advances to a new degree-three exit with a deficit. D105 supplies an ordinary graceful seed on the actual [D104 non-alpha target](R241_43_2_LEFT_TERMINAL_ZERO.md), with the retained D106–D107 families using the different branch-growth interface. D130 supplies a deficit-zero seed with three physical left centers.

[R241.1](../references/upstream/mdl/N241_relational_ports.md#n241-full-review) composes independently supplied alpha blocks with a relational equality of physical port offsets and moves one entire spectral band. [D078](R241_PAIRED_BRANCHED_SPINE.md) supplies its own compatible paired one-center alpha blocks with a separate empty-tail consumer. [N121](../references/upstream/mdl/N121_retained_record.md) supplies unequal clustered height-two factors under its stated degree and terminal parity conditions. [N135](../references/upstream/mdl/N135_retained_record.md) and [N141](../references/upstream/mdl/N141_retained_record.md) develop ordered loop allocation and factor-inventory criteria within their restricted composition model. Here the entire supplied ordinary prefix undergoes a single isometry, its weights remain in the lower band and its multi-center history supplies no additional admission condition. No universal prefix supply, arbitrary sequence of independent two-center sections, or historical novelty is established.
