# Proof obligations for B2-P1 and its continuation

This file defines the mathematical duties behind [RESEARCH_PLAN.md](../docs/RESEARCH_PLAN.md). It preserves the independently recalculated baseline corollary and path-consumer argument, and specifies the obligations for a future broader supplier. It does not replace the project's authoritative theorem or finding status records. Source IDs refer to [SOURCES.md](../docs/SOURCES.md).

## 1. Quantified supplier target

Specify a nonempty infinite set

\[
\mathcal D\subseteq\{(q,r,z_0,z_1,K):q,r,K\ge1,\ z_0,z_1\ge0\}.
\]

An independent supplier `F` accepts one tuple in `D`, constructs the exact B2-P1 graph in the final alphabet `0..m`, and returns labels on the prefix together with an interval position and side. Its totality claim is

\[
\forall p\in\mathcal D,\quad F(p)\text{ terminates and meets obligations P01--P08.}
\]

The algorithm and its domain must be explicit. A condition saying “there exists a successful prefix,” “the coefficient is positive,” or “a full solver succeeds” is not the independent input-supply conclusion. A conditional R226 consumer may be part of the construction only if the supplier proves that its required core, palettes and quotas are actually obtainable for every allowed tuple. [U04]

## 2. Obligations attached to every claimed supplier

| ID | Obligation | What would falsify or fail to establish it |
|---|---|---|
| P01 — target | Construct the exact named profile `[[q]+[0]*z0,[r]+[0]*z1]+[[]]*(K+1)`, with `m=q+r+z0+z1+K+4` | Added/removed connector edges, lost direct leaves, collapsed empty spine sections, or changed named incidences |
| P02 — assigned set | Assign exactly all vertices except `s:3,...,s:K+2`; include physical `s:2` | An unlabeled prefix leaf or a different return vertex hidden by isomorphism |
| P03 — labels | Prefix labels are distinct integers in the final alphabet `0..m` | Collision, out-of-range label, Boolean-as-integer input, or proof using a smaller intermediate alphabet without a valid embedding |
| P04 — differences | On every actual assigned edge, differences are distinct and their set is `[K+1,m]` | An omitted edge, duplicate difference, or leftover difference inventory other than `[1,K]` |
| P05 — residual labels | Unused labels are exactly `[ell,ell+K-1]`, with active label `ell+K` or `ell-1` in `0..m` | Merely matching cardinalities, a hole in the interval, or an active label inside it |
| P06 — physical boundary | The unfinished graph is the actual K-edge path starting at `s:2`; all assigned/unassigned crossing edges use that port | A resource-valid state whose remaining incidence is branched or attached at another assigned vertex |
| P07 — independence | Supply labels, choices, and any allocation inputs from parameters without first solving the complete target | Deleting a suffix from a full solver witness, assuming a compatible core exists, or using a finite table without a proved transport argument covering the claimed domain |
| P08 — continuation | The stated consumer labels every suffix vertex, uses exactly `[1,K]`, preserves the prefix, and terminates | A consumer that changes an undeclared prefix label, adds edges, or requires another unproved input |
| P09 — quantified domain | The proof covers every parameter tuple claimed, including equality bounds and parity cases | A formula checked only for a finite sample or a parameter restriction missing from the theorem statement |
| P10 — comparison | Compare with applicable retained formulas and known sufficient regimes; distinguish new state supply from ordinary-family novelty | Promoting a direct retained composition as a new mathematical advance or asserting literature priority without research |

P04 and P05 are set equalities, not a requirement to use the same unused label and difference values. The shifted label interval is intentional. P06 is additional to the numerical `interval_boundary` predicate; that function checks inventories and crossing-port incidence, not a theorem about every remaining topology.

## 3. Explicit shifted-interval path consumer

This elementary calculation supplies P08 for the exact B2-P1 suffix. It uses the existing endpoint-interval idea in U03, translated or reflected in the label alphabet.

Write `a=ell`. Let `w0=s:2`, `wj=s:(j+2)` for `1<=j<=K`. The only unfinished edges are `w(j-1)--wj`. Suppose unused labels are `[a,a+K-1]` and unused differences are `[1,K]`.

### Active endpoint above the interval

If `f(w0)=a+K`, assign

\[
f(w_j)=
\begin{cases}
a+(j-1)/2,&j\text{ odd},\\
a+K-j/2,&j\text{ even}.
\end{cases}
\]

The values alternate the lowest and highest remaining labels: `a, a+K-1, a+1, a+K-2, ...`. Odd and even positions occupy disjoint consecutive subintervals whose union is `[a,a+K-1]`. For every `j=1,...,K`, direct substitution gives

\[
|f(w_{j-1})-f(w_j)|=K-j+1.
\]

Thus every remaining label and every remaining difference is used once. The prefix is unchanged.

### Active endpoint below the interval

If `f(w0)=a-1`, reflect the preceding values through the map `x -> 2a+K-1-x`. Equivalently,

\[
f(w_j)=
\begin{cases}
a+K-1-(j-1)/2,&j\text{ odd},\\
a-1+j/2,&j\text{ even}.
\end{cases}
\]

The labels alternate `a+K-1, a, a+K-2, a+1, ...`; differences remain `K,K-1,...,1`. Reflection preserves pairwise differences and the interval. This proof handles `K=1` and both parities without an additional endpoint assumption.

This is a path-consumer argument. Replacing the path by an arbitrary branched suffix is a different theorem, even if both resource sets have the same sizes.

## 4. Written retained-composition baseline

**Evidence level:** a derived project corollary, independently recalculated by the methods and implementation roles during assembly. It is implemented as `two_section_padded`, with implementation checks described separately in [CONSTRUCTION_IMPLEMENTATION.md](../docs/CONSTRUCTION_IMPLEMENTATION.md) and the verification record. It is not an additional upstream retained lemma, formal verification, or a historical novelty claim. It makes the retained-overlap comparison precise.

### 4.1 One-positive-branch prefix block

Use local parameters: `M>=1` unfinished edges, one branch with `q>=1` terminal leaves, and `z>=M+1` direct leaves. Let

\[
N=M+q+z+2,\quad t=M+2,\quad b=2M+q+3,\quad A=[M+2,M+q+1].
\]

Label the local root zero, the branch center `b`, the named terminal leaves bijectively by `A`, and the outgoing next-spine vertex `M+1`. Use every remaining value in `[M+2,N]` once on the named direct leaves.

The branch interval has `q` labels. The center lies strictly above it, since

\[
b-(M+q+1)=M+2>0.
\]

It lies within the final local alphabet because

\[
N-b=z-M-1\ge0.
\]

The high interval contains `N-M-1=q+z+1` values; after removing `q` terminal labels and one center, exactly `z` remain for the direct leaves. No missing or extra direct leaf is created.

Reflection by `b` permutes `A`:

\[
b-A=A.
\]

The root-to-center difference is `b`; the branch's terminal differences are precisely `A`; each direct-root edge uses its direct-leaf label as difference; the outgoing edge has difference `M+1`. All labels and differences in `[M+1,N]` are consumed exactly once, leaving labels and differences `[1,M]` and active label `M+1`.

This is the one-branch specialization of the retained L010 formula. H010 uses the same formula on its more restricted one-branch domain. The calculation does not require `q<=M+2`; that generic H010 condition is unnecessary for this single-branch specialization. [U03]

Crucially, the calculation concerns only this prefix and its outgoing vertex. It does not assume the internal topology of the unfinished `M`-edge tree. Completion of that tree requires a separate consumer. This is why the calculation can be used to investigate composition while the existing complete-constructor API still requires its stated caterpillar suffix.

### 4.2 Apply the first block

For B2-P1 put `K1=r+z1+K+2` and assume

\[
z_0\ge K_1+1,\qquad z_1\ge K+1.
\]

The full edge count satisfies `m=K1+q+z0+2`. Apply the preceding prefix block with `M=K1` to `s:0`, its branch, its direct leaves, and outgoing vertex `s:1`. The used high values/differences are `[K1+1,m]`; the root uses zero. Its only remaining port is `s:1`, with label `K1+1`. The remaining unused labels and differences are exactly `[1,K1]`.

### 4.3 Apply and embed the second block

Consider the unfinished tree rooted at `s:1` in a local alphabet `0..K1`. Its local edge count is `K1=K+r+z1+2`. Apply the one-branch prefix calculation with `M=K`, branch size `r`, and direct-leaf count `z1`. Write its local labels as `g`, with `g(s:1)=0` and `g(s:2)=K+1`.

Map each local assigned label to the actual label

\[
f=K_1+1-g.
\]

The local root maps to the already assigned `s:1=K1+1`. Every other local label is in `1..K1`, so its image is also in `1..K1` and cannot collide with the first block. The map is injective and preserves every absolute difference on actual second-block edges. The second block consumes differences `[K+1,K1]`, disjoint from the first block's `[K1+1,m]`.

Unused local labels `[1,K]` map exactly to `[K1-K+1,K1]`; unused differences remain `[1,K]`. The actual return label is

\[
f(s:2)=K_1+1-(K+1)=K_1-K,
\]

one below the returned interval. Section 3 finishes the exact suffix path. These label/difference partitions, rather than an appeal to separately graceful pieces, establish the intended compatibility calculation.

### 4.4 Review boundary and regression duties

The independent recalculations check the quantified parameter domain, alphabet sizes, the single shared root, the exact edge partition, and both inventory transformations. Any implementation revision must preserve every named vertex and use the actual `s:2` port. These are narrow regression/review duties, not a reason to launch a larger search campaign. The package's dedicated prefix helper keeps this derivation separate from the complete L010/H010 APIs' narrower suffix contract.

This baseline establishes no claim for zero direct leaves, because `z1>=K+1>=2`. A violation of its sufficient bounds is not a counterexample to its construction on its domain, and is not a nongraceful tree. Repeating another block requires another quantified budget/interface calculation; arbitrary iteration is not adopted here.

## 5. Balanced supplier: discharged duties and remaining unequal seed

The [balanced-family proof](B2_BALANCED_SUPPLIER.md) establishes P01–P09 for the infinite domain `q=r=t>=1,z0=z1=0,K>=1`. It directly assigns the exact prefix; its label partition leaves `[t+2,K+t+1]`; its actual differences partition `[K+1,m]`; its active port is `s:2=K+t+2`; and Section 3's path consumer finishes in K steps. Independence follows from the explicit formulas, without solving the K-dependent whole target. Separate methods and implementation roles recalculated this argument.

The implementation and independent certificate checks are reported separately. P10 remains a scope/overlap duty for any novelty claim: the padded retained construction is compared, current subcubic coverage is recorded, and no historical priority is asserted. The proof does not discharge P01–P09 for unequal branches or a further branched suffix. `FINDINGS.md` owns accepted findings and `STATE.md` owns current work.

B2-UNEQUAL-SEED-001 is now disposed as an **exhausted restricted negative** (full record: [B2_UNEQUAL_SEED.md](B2_UNEQUAL_SEED.md)). The eight-vertex prefix with A-side `0..3` / B-side `4..7` bijective domains and pin `h(s:2)=4` has no graceful labeling: the analytic obstruction (difference 1 forces `h(s:1)=3`; `a+2b−x=18` admits only `(a,b,x)∈{(5,7,1),(6,7,2),(7,6,1)}`; every resulting assignment duplicates difference 4 on at least two actual edges) was confirmed by independent recomputation and a separate reviewer challenge, and both the declared bounded DFS and the direct permutation oracle exhausted the declared scope with 0 solutions on the same original graph digest. The falsified claim is exactly that alpha/physical-port template — not the unrestricted eight-vertex tree, not any other restriction set, and not the unequal B2 family at any K.

The proposed all-K high-side-shift transport is **retained as a conditional identity only**: it is correct that a valid seed, if one existed, would supply every `K>=1` of the declared family (unused labels `[4,K+3]`, unused differences `1..K`, port `s:2=K+4` one above, consumer terminating in K steps), but its antecedent is false, so it discharges no P07 obligation and is not implemented as a supplier. P07 remained open under that false-premise template; the separate port-5 construction below now satisfies the independent-supply requirement for the revised nonadjacent interface on `q=1,r=2,K>=2`. A successful fixed seed plus a proved parameterized transformation can satisfy P07; a different searched full-tree prefix for every K cannot establish the same quantified conclusion. The previously queued next task — the specific alternative port rule `h(s:2)∈{5,6,7}` on the same named target (see [NEXT_TASK.md](NEXT_TASK.md)) — is now **recorded superseded, not executed**: for `p∈{5,6,7}` the same high-side shift still returns unused labels `[4,K+3]` and unused differences `1..K`, but places the physical port at `K+p`, not the adjacent port `K+4` (one above the interval) that the Section 3 consumer requires, and at `K=1` the single suffix edge would have difference `p−3∈{2,3,4}` instead of 1. The full supersession reasons are in `NEXT_TASK.md` and decision D016.

The external independent acceptance review of the B2-UNEQUAL-SEED-001 checkpoint (November 21, 2026; pack custody at `evidence/reviews/B2_UNEQUAL_SEED_001/`) established a stronger scoped result, adopted as [B2_INTERFACE_OBSTRUCTION.md](B2_INTERFACE_OBSTRUCTION.md) (independently accepted at reviewed revision `2cfb2df`; D018): for `q=1,r=2,z0=z1=0` and every `K>=6`, no injective prefix labeling leaves unused labels `[ell,ell+K-1]`, unused differences `1..K`, and port `ell-1` or `ell+K` for any `ell` or side, with no alpha assumption and no root pin. The old adjacent-port interface is therefore impossible for this family at `K>=6` (threshold sufficient; sharpness not established; `K=1` has the preserved `ell=1`, above-side witness; `K=2..5` are not adjudicated here). A different interface now has a separately reviewed conditional path consumer: for integer `K>=2`, unused labels `[ell,ell+K-1]`, unused differences `1..K`, and the physical port `ell+K+1`, the recurrence in [B2_NONADJACENT_CONSUMER.md](B2_NONADJACENT_CONSUMER.md) completes the exact original K-edge path. K=1 is impossible for this interface. This is not a revision of P05's adjacent-port contract: it is a different consumer. The port-5 fixed seed now independently supplies a compatible original-graph prefix for exactly `q=1,r=2,z0=z1=0,K>=2`, via the explicit formulas and proof in [B2_NONADJACENT_SEED_P5.md](B2_NONADJACENT_SEED_P5.md). This discharges the revised nonadjacent analogue of P05 and P07/P08 for that domain, not literal adjacent-port P05. A separate previously checked K=1 witness gives ordinary gracefulness for that one case, not the nonadjacent interface. This does not change the discharged balanced duties, the retained conditional transport, or the padded construction.


The revised nonadjacent resource interface now has an explicit independent supplier for **all integers `q,r>=1,K>=2` with `z0=z1=0`**, not only `(q,r)=(1,2)`: see [B2_UNPADDED_ALL_QR.md](B2_UNPADDED_ALL_QR.md), finding B2-UNPADDED-ALL-QR-001 and D021. Its actual prefix uses `[0,r+1] ∪ [K+r+2,m]` and differences `[K+1,m]`, leaving `[r+2,K+r+1]`, differences `1..K`, and port `K+r+3`. This discharges P01–P04 and P06–P09 for that domain with the **revised nonadjacent analogue of P05**, not the literal adjacent-port P05. P10 remains a scoped source-comparison duty, not a novelty claim. K=1, nonzero padding, further branched suffixes and arbitrary repeated sections are outside this theorem.

For K=1 and all integer `q,r>=1`, the separately reviewed [B2-UNPADDED-K1-001](B2_UNPADDED_K1.md) explicitly supplies the original prefix with the different contract `R={q+4}`, `D={q+3}`, port `s:2=1`; the actual edge to `s:3=q+4` consumes that difference. It establishes ordinary gracefulness on its exact target and, together with the K>=2 theorem above, for every positive integer `q,r,K` at zero padding. This K=1 contract does not meet literal P04, P05 or P08, which prescribe `D={1}` and an adjacent endpoint; those restrictions retain their meanings. The balanced K=1 supplier already meets the earlier contract for `q=r`, whereas other prescribed-boundary instances require their own proof or disproof. Nonzero padding, additional branched sections, and repeatable transitions remain separate obligations. Decision D022.

The [fixed-ell=2 obstruction](B2_INTERVAL_OBSTRUCTION.md) for the unit family at K>=3 is a proved reason not to extrapolate successful small ell=2 states. It does not constrain the balanced supplier's different interval.

## 6. Falsifiers and finite evidence

The pilot contains four explicit target/interface pairs, all with `z0=z1=0`, `K=1` and no pin on `s:0`: `(q,r,ell)=(1,1,1),(1,1,2),(1,2,1),(2,1,1)`, each on the above side. There are three named profiles, not four. Every pair asks its own finite existence question; the experiment does not assume that all four answers are positive. Independent development review identified the first pair as a restricted failure and the second as a positive control on the same graph. Their exact receipts and certificate belong in the authoritative findings/verification records.

An exhaustive failure at `ell=1` refutes a claim requiring that particular state on that graph. A witness at `ell=2` demonstrates that changing the interval can matter, and proves ordinary gracefulness of that finite graph after verification. Neither result proves a general independent supplier.

For a proposed formula `F` on domain `D`, a concrete tuple in `D` producing a P01–P08 violation is a formula counterexample. A tuple outside `D` is a coverage limitation. A finite solver timeout is neither. If the theorem says that one of several interfaces works, failure of only one interface does not falsify it.

An exhausted exact search can establish a finite negative only for the correctly encoded domain and restrictions. Record the full model and independently challenge the result where practical. The independent permutation oracle is a bounded implementation cross-check; it does not certify untested sizes. A solver's unsatisfiability report is not a proof-assistant certificate in this project.

## 7. Obligations for repetition beyond the first target

To promote a two-section supplier into a repeated construction, specify a state class `S`, a transition for the next actual section, and a domain of admitted input sequences. Prove that each admitted input reaches `S`, each transition receives independently available resources and preserves its invariant, and a finite measure decreases until a terminal consumer applies.

The state must carry the physical port, actual label or normalization map, both resource inventories, remaining topology, and any quota constraints needed later. A compact normalized representation is acceptable only after its equivalence to those facts is proved. A transfer-state transition valid for one parity or capacity regime does not automatically cover another. [U06]

The project can instead find a useful global reconstruction theorem. That alternative must recover the exact requested target and quantify source reachability; it need not preserve the earlier prefix labels. The repeated-prefix route is a research choice, not an additional condition imposed on the lobster problem itself.
