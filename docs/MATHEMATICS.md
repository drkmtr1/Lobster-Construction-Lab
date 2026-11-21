# Mathematical specification and interfaces

## 1. Exact target

A lobster is a finite simple tree with a supporting path such that every vertex is at distance at most two from that path. The supporting path is a representation witness, not an extra edge set. An explicit graph may supply one; otherwise two simultaneous leaf-removal rounds must leave a path, with the implementation retaining the last nonempty one-/two-vertex core for small trees. The independent checker separately checks the same mathematical property.

For `m` original edges, a certificate `f` must satisfy:

\[
f:V\longrightarrow\{0,\ldots,m\}\text{ bijective},\qquad
\{|f(u)-f(v)|:uv\in E\}=\{1,\ldots,m\}
\]

with every difference occurring once. The singleton has one vertex, no edges, and label zero. Integer labels are exact; JSON booleans are rejected. A larger graceful graph containing the target is a different result.

## 2. Profiles and physical identities

A profile is a nonempty list of sections. Section `i` corresponds to spine vertex `s:i`. Each entry `q` creates a branch vertex `b:i:j` attached to `s:i` and `q` terminal leaves `l:i:j:0,...,l:i:j:q-1` attached to that branch. Thus `q=0` is a direct leaf, `q=1` is a two-edge branch, and an empty section still supplies its spine vertex. Trailing empty sections are significant.

For `t` sections,

\[
m=(t-1)+\sum_{i,j}(q_{ij}+1),\qquad |V|=m+1.
\]

For example `[[2,0],[1],[],[]]` has one two-terminal branch and one direct leaf at `s:0`, one one-terminal branch at `s:1`, then two additional spine vertices. Its edge count is `3+(3+1)+2=9`.

The profile order names physical branches; search does not silently sort, quotient or identify them. `graph_digest` canonicalizes listing order of named vertices/undirected edges while preserving profile, spine and roles. It is an identity checksum, not an isomorphism identifier or a cryptographic signature.

## 3. Exact partial state

For a partial assignment `f` to a set `A`, record used vertex labels, used differences on edges with both ends in `A`, the unused label set `R`, unused difference set `D`, and physical frontier vertices incident to unassigned vertices. Partial validity establishes distinctness so far. It does not establish completion.

`verify_partial` returns these sets independently. `interval_boundary` additionally requires a specified assigned port, every unfinished incidence at that actual port, `R=[ell,ell+K-1]`, `D=[1,K]`, and active label `ell-1` or `ell+K`. The unfinished topology must be supplied separately. In the B2 family it is an exact K-edge path; in a generalized application a proof must identify a suitable consumer.

## 4. Implemented construction domains

See `CONSTRUCTION_IMPLEMENTATION.md` for complete formulas and source links.

| Routine | Input domain | What it supplies |
|---|---|---|
| `caterpillar(profile)` | Every branch entry is zero; includes singleton | Entire labeling by endpoint interval consumption |
| `l007(q,r,z)` | `q,r>=1`, `z>=0`; profile `[[q]*r+[0]*z,[]]` | Independently supplied equal-branch cluster and terminal next edge |
| `l010(qs,z,suffix_profile)` | Positive branch sizes, all-zero-entry suffix with K>=1, high-label budget at least last center | One branched section plus complete caterpillar suffix |
| `h010(qs,z,suffix_profile)` | `Q=sum(qs)<=K+2`, `z>=max(0,K+2+Q-q_last-len(qs))`, same suffix type | Denser high-label placement and complete suffix |
| `two_section_padded(q,r,z0,z1,K)` | `q,r,K>=1`, `z1>=K+1`, `z0>=r+z1+K+3` | Two actual branched sections, shifted return interval, and complete K-edge path |
| `two_section_balanced(q,K)` | `q,K>=1`, both branch sizes q, no direct leaves | Independently supplied prefix with `R=[q+2,K+q+1]`, actual active label `K+q+2`, and complete path |
| `two_section_unit(K)` | `K>=1`; balanced q=1 specialization | Convenience wrapper for the same proved construction |
| `complete_two_host(graph,core_labels,hosts)` | Connected fixed core; all missing vertices are original leaves at the two assigned distinct hosts | R226 constructive completion or exact fixed-core obstruction |

A domain rejection is a statement about the recipe, not the tree's graceful existence. R226 supplies a consumer; its successful core is an input obligation. The padded routine is a reviewed project corollary of retained L010 prefix arithmetic. The balanced routine has a separate exact label/edge-partition proof in `research/B2_BALANCED_SUPPLIER.md`; it supplies an infinite zero-padding domain directly from parameters. Neither is a newly adopted upstream theorem or a novelty determination.

## 5. Search and exact counts

The DFS considers bijections of the supplied **named** vertices. Its minimum-remaining-values rule changes the next vertex to visit; it removes no assignment. It prunes only reused labels and zero, repeated or out-of-range completed-edge differences. Explicit pins/domains add declared restrictions. No root-zero, alpha, automorphism or complement quotient is active by default.

The permutation oracle enumerates complete assignments in a separate implementation and tests the full edge spectrum. It is factorial and reserved for tiny comparisons. Counts include both complementary labelings and all distinct named permutations. For retained controls, `G(P4)=4`, `G(P6)=24`, and the six-vertex spider with legs 2,2,1 has count 16; these are reproduced in the validation evidence.

The dynamic program processes a fixed vertex order. At each layer a state is

\[
(\text{used-label mask},\ \text{used-difference mask},\ \text{ordered live-frontier labels}).
\]

Its coefficient counts distinct named histories. Two histories can merge because future legality depends exactly on these inventories and labels of already assigned neighbors that still have unfinished edges. Forgotten vertex values cannot appear on a future edge. Every new edge is charged when its later endpoint is assigned. At the final layer, `n=m+1` distinct vertex labels in `0..m` and `m` distinct differences in `1..m` give the exact target sets. See the separate `SEARCH_REVIEW.md` for the argument and examples showing that omitting any of the three components can change completion counts.

This is a faithful evaluation of the exact resource-counting formulation. The two masks grow with the graph; no constant-size state or polynomial-time universal solver is claimed. A nonzero count supplies finite existence. An exact general recurrence alone does not prove its count is positive on every lobster.

## 6. SMT encoding and status semantics

The optional Z3 adapter assigns one integer variable per original vertex, restricted to its declared subset of `0..m`, makes all vertex variables distinct, and makes the absolute differences on all actual edges distinct in `1..m`. That is equivalent to graceful labeling of this fixed tree within the declared restrictions. It returns a model, UNSAT on that encoding, or an incomplete status when bounded. The independent checker tests every returned model. No independently checked UNSAT proof object is produced.

| Status | Meaning |
|---|---|
| `CONSTRUCTED` | A recipe produced labels; record must also include independent certificate success |
| `SAT` | A finite witness was found; exact count exists only if exhaustive counting completed |
| `EXHAUSTED_NO_SOLUTION` | Declared finite search exhausted, or SMT returned UNSAT; scope and evidence method remain explicit |
| `RESTRICTED_INFEASIBLE` | R226's supplied fixed core/hosts cannot be completed under that theorem's conditions |
| `INCOMPLETE` | A bound or interruption stopped the decision; any saved count is only a lower bound |
| `UNAVAILABLE` | An optional engine is missing; no mathematical conclusion |
| `INVALID_INPUT` / `ERROR` | Malformed data or an operational/input failure |
| `QUARANTINED` | Claimed positive output failed independent checking or had no witness |

Public input helpers may raise `ValueError` on malformed restrictions or unsupported domains. The CLI reports these as input errors. No restriction is silently repaired.

## 7. Supplier versus discovery evidence

`b2_restrictions` and `extract_b2_candidate` are tools for finite diagnosis. They require the exact two-section topology and independently verify the full labeling before extraction. Their output explicitly says `independent_supplier: false`.

To promote a proposed supplier, give a rule using only the stated input structure/parameters; prove range, distinct labels, exact edge-difference partition, returned inventory, actual port identity, continuation and termination for all parameters in its domain. Compare the domain with the retained padded baseline and applicable external literature. Repeatability requires the next consumer's assumptions to follow from the previous return state.
