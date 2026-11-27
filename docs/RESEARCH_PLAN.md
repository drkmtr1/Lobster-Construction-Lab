# Research plan: supply a reusable two-section boundary

**Purpose:** turn retained constructions into a precise next mathematical question. This document specifies the investigation and its comparison baselines; measured run results belong in the experiment artifacts. `STATE.md` is the authoritative current task/status record, and the findings and failed-hypothesis records own actual results. Method and source IDs are in [METHOD_SELECTION.md](METHOD_SELECTION.md) and [SOURCES.md](SOURCES.md).

## Current universal-proof strategy

Use the [D207 strategic assessment](../research/D207_INDEPENDENT_SUPPLIER_ARCHITECTURE.md) and its [supplier and domain inventory](../research/D207_SUPPLIER_INVENTORY.md) for the dependency map, compatibility conditions and research roadmap. The immediate mathematical priority is independently compatible ordinary suppliers, with initial state, actual ports, resource allocation and structural coverage developed together. The detailed two-section plan below remains the historical baseline for those specific constructions. STATE.md owns the single current action.

D208 develops the separately authorized reverse traversal of admitted boundary-root blocks from an independent ordinary component. D207's fixed-order monotone continuation proposal remains deferred under the Director revision. [D208 theorem](../research/ORDINARY_SPINE_REVERSE_BLOCK_COMPOSITION.md)

## 1. What progress should mean

The project already has parameterized constructions and exact consumers. Its first research objective is an **independent supplier**: a rule that labels an actual branched prefix from the input parameters and leaves a provably usable state at the next physical spine vertex. A supplier must not depend on first solving the whole target and extracting its successful prefix.

The target need not be a closed-form equation. An explicit terminating construction with a proof over a stated infinite family would qualify. It may choose its interval position, choose its side, or relabel earlier vertices if its theorem permits that. A finite witness, a new solver, a larger table, and an infinite-family construction are different kinds of progress.

The immediate family is deliberately small enough to expose the compatibility issue. There is no claim that its ordinary gracefulness or any eventual returned interface would be historically new. The starter profiles lie within the degree-three scope of the newly inspected primary certificate archive E10; its statement does not prescribe the B2 return interface. Review its actual construction before claiming a new finite-rule method. See the literature checkpoint in [METHOD_SELECTION.md](METHOD_SELECTION.md).

During assembly, the independent-supplier objective was reached for the balanced zero-padding domain described below. The next selected work is the smallest unequal seed task in `research/NEXT_TASK.md`; the first four-pair diagnostic is completed release evidence. Do not restart it as an unperformed campaign.

## 2. B2-P1: exact input, prefix and output

For integers `q,r,K >= 1` and `z0,z1 >= 0`, build

```text
[[q] + [0]*z0, [r] + [0]*z1] + [[] for _ in range(K+1)]
m = q + r + z0 + z1 + K + 4
```

The spine is `s:0, s:1, ..., s:K+2`. One positive branch at `s:0` has `q` terminal leaves; one at `s:1` has `r`. The direct leaves counted by `z0,z1` are actual target vertices. The assigned prefix consists of every vertex except `s:3,...,s:K+2`. Its last physical port is `s:2`. Exactly `K` suffix vertices and `K` suffix edges remain.

An interval supplier returns the prefix labeling `f`, an integer interval start `ell`, and a side:

\[
R=[\ell,\ell+K-1],\qquad D=[1,K],
\]

\[
f(s:2)=\ell+K\quad\text{(above)},\qquad
f(s:2)=\ell-1\quad\text{(below)}.
\]

Here `R` is the unused vertex-label set and `D` is the unused difference set. The interval and active label must lie within `0..m`. Every assigned label and every assigned-edge difference is distinct. The sole edge from assigned to unassigned vertices is the original edge `s:2--s:3`.

The returned object must include the final graph identity, the exact prefix labeling, the physical port, both inventories, and the supplier's parameter domain. A representation change cannot replace the target with an expanded connector graph.

This matches the intended resource/port predicate in `lcl/states.py`. That predicate alone does not certify the unfinished topology or independent supply. For B2-P1, the graph definition supplies the unfinished path. The explicit path continuation proof is in [PROOF_OBLIGATIONS.md](../research/PROOF_OBLIGATIONS.md).

## 3. Compare a retained composition before seeking a new one

Let

\[
K_1=r+z_1+K+2.
\]

This is the number of edges in the unfinished tree rooted at `s:1` after the first branched section and its outgoing edge are labeled. A one-positive-branch L010 prefix block, with local root zero and `M` unfinished edges, works when the number `z` of direct leaves satisfies `z >= M+1`. Its formula agrees with H010's one-branch formula. L010 does not need H010's additional generic bound on the branch size. [U03]

Consequently the retained formulas give a two-block baseline on

\[
z_1\ge K+1,\qquad z_0\ge K_1+1,
\]

with arbitrary positive `q,r,K`. The first prefix returns `s:1 = K1+1` and resources `1..K1`. Apply the second local block with root value zero, then map its labels by

\[
f_{\rm actual}=K_1+1-g.
\]

Absolute differences are unchanged. The resulting state at `s:2` has

\[
R=[K_1-K+1,K_1],\quad D=[1,K],\quad f(s:2)=K_1-K.
\]

Thus `ell = r+z1+3` and the side is **below**. A shifted interval is essential to expressing this baseline naturally. The detailed calculation and its proof obligations are recorded in [PROOF_OBLIGATIONS.md](../research/PROOF_OBLIGATIONS.md). The methods and implementation roles independently recalculated it during assembly. It is a reviewed project corollary of retained formulas, implemented as `two_section_padded`; it is not an additional upstream lemma, a formal verification, or a novelty claim. See [CONSTRUCTION_IMPLEMENTATION.md](CONSTRUCTION_IMPLEMENTATION.md) and the package verification record for implementation evidence.

The existing complete L010/H010 APIs accept a caterpillar suffix. The first remaining suffix here is branched, so `two_section_padded` uses a separate prefix helper. Passing an unsupported branched suffix to a complete constructor would not be a proof.

This baseline consumes substantial direct-leaf budgets. The first useful comparison target is therefore small or zero direct-leaf regimes, or a different independently supplied boundary beyond its conditions. Failure of these sufficient bounds says nothing about ordinary gracefulness or the reach of other retained MDL constructions.

### Balanced zero-padding domain now supplied

The project subsequently derived and separately reviewed an explicit rule for `q=r=t>=1,z0=z1=0`, all `K>=1`. It leaves labels `[t+2,K+t+1]`, differences `1..K` and actual active label `s:2=K+t+2`. The formula and complete actual-edge partition proof are in [B2_BALANCED_SUPPLIER.md](../research/B2_BALANCED_SUPPLIER.md), with the accepted disposition in `research/FINDINGS.md`. `two_section_balanced(t,K)` and its unit wrapper implement it.

This removes the padded baseline's direct-leaf requirement on a specified infinite balanced domain. It does not settle unequal branch sizes or arbitrary repeated branched sections, and no historical novelty is asserted. The selected next objective is `q=1,r=2`, no direct leaves, all positive K, approached through one fixed auxiliary alpha/physical-port seed. [NEXT_TASK.md](../research/NEXT_TASK.md) owns its precise inputs, conditional transport argument, limits and outcomes.

## 4. First bounded diagnostic: four explicit target/interface pairs

The initial question is intentionally narrower than the supplier objective:

> For the four exact target/interface pairs below, with `z0=z1=0`, `K=1` and no root-label restriction, which prescribed interval states are feasible?

| Pair | `q` | `r` | `m` | Vertices | `ell`, side | Imposed suffix state |
|---|---:|---:|---:|---:|---|---|
| B2-P1-11-A1 | 1 | 1 | 7 | 8 | 1, above | `f(s:2)=2`, `f(s:3)=1` |
| B2-P1-11-A2 | 1 | 1 | 7 | 8 | 2, above | `f(s:2)=3`, `f(s:3)=2` |
| B2-P1-12-A1 | 1 | 2 | 8 | 9 | 1, above | `f(s:2)=2`, `f(s:3)=1` |
| B2-P1-21-A1 | 2 | 1 | 8 | 9 | 1, above | `f(s:2)=2`, `f(s:3)=1` |

This is **three named profiles and four target/interface pairs**, not the complete `q,r` grid. The first two pairs deliberately compare two states on the same target. Independent development review found the first prescription infeasible and a full witness for the second; the paired control prevents that fixed-state failure from being mistaken for ordinary nongracefulness. The authoritative result, certificate and failure record belong in the findings and verification artifacts. The ordered `q,r` cases remain separate named-profile cases, and their count is not a count of distinct unrooted tree isomorphism classes.

**Initial configuration:** [configs/b2_pilot.json](../configs/b2_pilot.json) selects one DFS worker, at most 50,000 search nodes and 2 seconds per pair, a 16-vertex cap, four pairs and 20 seconds per invocation, and at most 2,000,000 bytes per attempt record. Four attempt records can therefore total up to 8 MB, plus snapshots/checkpoint data. The common limits object also carries a 20,000-state bound for state-based engines; this invocation uses DFS. The saved configuration is authoritative for a run. This diagnostic does not automatically increase sizes or restart with larger budgets. Record the graph digest, complete restrictions, limits, elapsed time, nodes, status, witness if present, and checker outcome.

The `b2_restrictions` adapter imposes the suffix interval and active endpoint on a full finite solver. In this family that is a valid finite feasibility test for the desired boundary: a graceful solution gives `K` distinct suffix differences lying in `1..K`, so the suffix uses all of them. Conversely any valid prefix with that boundary has the explicit path completion. This equivalence does not make the extracted prefix an independent supplier. Its correct classification remains `solver_derived_exploratory_prefix`.

Interpret the outcomes precisely:

- **Verified witness:** the prescribed state exists for that named finite case. Preserve both the full labeling and extracted boundary.
- **Exhausted without a witness:** the particular `ell`, above-state prescription is infeasible for that case, subject to the exact solver's correctness and restrictions. This does not exclude another interval, the below side, a different interface, or ordinary gracefulness.
- **Incomplete:** no conclusion about state existence. Keep the budget and partial evidence; do not relabel a timeout as a negative.

A run with no root restriction uses `root_label=None`; it does not mean the root is set to zero. The first pilot includes neither an alpha requirement nor a hidden symmetry quotient.

The four pairs include one shifted positive control but are not a scan across all intervals. If another prescription fails, prepare a separate small configuration that changes only the relevant assumption, for example a specified alternate `ell`/side or a bounded unrestricted witness check on that same graph. Broad interval or size scans require their own explicit bounded configuration. Routine implementation, review, and the declared bounded work remain authorized; there is no extra permission gate for each ordinary step.

## 5. Named questions and proof-dependent milestones

These IDs define work items, not live assertions of truth. Their dispositions belong in the current state and findings records.

| ID | Question or proposed claim | Evidence needed to close it |
|---|---|---|
| B2-BASELINE-COMP | What exact domain and returned state does the reviewed two-block corollary supply? | Preserve its label/edge partition proof, independent recalculation and implementation checks; record source overlap |
| B2-P1-PAIR4 | What is the feasible/infeasible/unknown disposition of each of the four explicit target/interface pairs? | Preserve checked witnesses and scoped exhaustive negatives; retain the same-target shifted positive control; incomplete results remain open |
| B2-SUPPLY-D | Can an explicit rule supply a boundary for every parameter tuple in a stated infinite domain `D` beyond an applicable retained baseline? | Independent construction, quantified proof, adversarial boundary checks and coverage comparison |
| B2-BALANCED-SUPPLY | Completed in the stated equal-branch, zero-padding domain | Preserve the explicit partition proof, independent reviews and implementation checks; no unequal or novelty extrapolation |
| B2-UNEQUAL-SEED-001 | Does the one selected unequal prefix admit the designated alpha/port seed? | Follow `NEXT_TASK.md`; a positive seed needs reviewed all-K transport, a negative remains restricted |
| B2-RELAX | Which specific prescription can be relaxed when a pair in B2-P1-PAIR4 or a candidate rule fails? | One bounded discriminating comparison and an explanation of why the changed state addresses the failure |
| B2-REPEAT | Can the supplied return state enter another genuine branched section without assuming a pre-existing full solution? | A precise transition theorem with independently available inputs and a termination/coverage argument |

**Milestone 1 — retain the reviewed baseline.** Use the already recalculated composition and its implementation as the comparison baseline before treating a leaf-rich two-section example as progress. Preserve its narrow domain and source attribution. A larger search is unnecessary to establish this symbolic calculation.

**Milestone 2 — preserve discriminating finite evidence.** Run or reproduce only the declared four-pair diagnostic as needed, validate its witnesses, and resolve each prescribed-state question as far as the budget allows. The first same-target pair already has a development-review contrast to reproduce; this is not a claim of a new infinite result. Add one targeted comparison only when it answers a concrete remaining question.

**Milestone 3 — supply an explicit family.** Achieved for the balanced domain by the explicit formula. Extend through the selected unequal seed question or another precise template; keep the source of every input independent of a successful whole-target solution.

**Milestone 4 — prove or repair.** P01–P09 are discharged for the balanced formula. Discharge them separately for each proposed extension. Every failed sign case, collision or unsupported parameter becomes a precise counterexample or a corrected domain. The fixed ell=2 unit-family obstruction demonstrates why a returned interval cannot be extrapolated from small witnesses. Broaden testing only to challenge an identified risk.

**Milestone 5 — continue to another branched section.** Prove the returned state supplies the next step's actual inputs. Allow reconstruction of earlier labels when the theorem says so. Do not assume preservation of fixed earlier labels is necessary for a general construction.

## 6. Assumptions to remove deliberately

| Current restriction | Why it is present | Meaningful next relaxation |
|---|---|---|
| Large `z0,z1` in the retained composition | Guarantees high-label room in the one-branch interval formula | A stated smaller-budget or zero-direct-leaf infinite subfamily |
| Equal branch sizes in the zero-padding supplier | Makes the explicit prefix difference blocks meet exactly | The designated unequal seed or a different proved allocation/return rule |
| Fixed `ell`, above in each pilot pair | Makes each finite question concrete; one `ell=2` control exposes the effect of shifting | Let a construction select an interval and side from its parameters |
| One positive branch per section | Isolates the first genuine repeated-branch interface | Multiple unequal positive branch sizes with the same supply proof |
| A path after `s:2` | Gives an explicit, simple consumer | A proven caterpillar consumer, then a genuinely branched consumer |
| Two branched sections | Keeps the first supply obligation inspectable | A transition invariant supporting an arbitrary number of sections |
| Fixed internal formulas | Makes proof obligations visible | A finite menu or an exact structural choice rule with a proved domain |

No alpha restriction or chosen-root-zero restriction is added to unrestricted search. A constructor may use either as an explicit sufficient design choice; failure then belongs to that construction.

## 7. Continue, revise or stop this direction

**Continue** when a candidate supplies a new useful domain/interface, a falsifier identifies a repairable assumption, or a proof isolates a tractable missing lemma. **Revise** when the requested boundary is too rigid, the apparent gain is already retained composition, or a state omits a resource needed for the next step. **Stop this candidate** when it merely restates existence, repeatedly extracts prefixes from full solutions without a noncircular rule, or needs more search without a discriminating mathematical question. Stopping one candidate does not close the broader lobster objective.

Report progress through precise quantities: named finite cases completely decided; witnesses independently checked; candidate assumptions falsified; exact infinite domain proved; retained parameter regimes newly reached; distinct supplier-to-consumer obligations discharged. Also report elapsed time and resource use to assess practicality. Do not equate search volume, agent count, or raw witness count with universal-gap reduction.
