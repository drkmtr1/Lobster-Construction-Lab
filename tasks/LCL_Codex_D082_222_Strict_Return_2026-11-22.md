# Lobster Construction Lab — D082 Bounded Research Task

**Proposed task ID:** `LCL-R241-222-STRICT-RETURN-001`

Act as the mathematical research and verification team for Lobster Construction Lab.

I authorize **one bounded research task** to investigate whether the exact original two-center pair `[[2,2],[2]]` can independently supply a normalized alpha graceful state with physical R241 offsets `(1,0)`, suitable for composition with D080's accepted `H(a)` bridge.

## 1. Mandatory recovery and integrity checks

Work in:

`C:\Users\Will\Projects\Lobster_Construction_Lab`

Before changing any files:

1. Read `AGENTS.md`, `STATE.md`, the D081 handoff, and the relevant mathematical and verification records.
2. Verify local HEAD, actual GitHub `main`, tracking branch, working-tree status, and the latest handoff.
3. Confirm that the last accepted published commit is `ec058da9fe0c834978cc5de927cd96f5b0ca2e68`. If a newer commit or conflicting task exists, STOP and report the discrepancy.
4. Read the accepted D078–D081 proofs, the original R241 join, the D080 `H(a)` supplier, and the retained nonadjacent path consumer.
5. Verify the existing checker and historical source identities. Preserve all previous evidence and failed hypotheses.

Both upstream repositories remain read-only:

- MDL: `858a8c1fcfda87ba40bb1adee498a6131504a803`
- MDL Bounded Search: `e48b94eec4091b4fe189e325cab2eda464409943`

Preserve the deferred D076 proposal without executing it.

## 2. Exact mathematical question

Investigate the original named lobster

`T = [[2,2],[2]]`

It contains:

- Physical spine `s:0--s:1`.
- Two distinct centers at `s:0`, each having two indexed terminal leaves.
- One center at `s:1`, having two indexed terminal leaves.
- Exactly 11 vertices and 10 edges.

Under the alpha orientation with `s:0` low and `s:1` high, the prescribed state is

`A(11,6;1,0)`

with:

- Low labels `0..5`.
- High labels `6..10`.
- Physical entrance `f(s:0)=1`.
- Physical exit `f(s:1)=6`.
- Every original edge crossing the alpha cut.
- Original-edge differences exactly `1..10`.

The remaining five low labels and four high labels give exactly

`5! × 4! = 2,880`

named assignments under this prescription.

The primary question is whether at least one assignment gives the required normalized state.

Do not change the physical ports, quotient distinguishable vertices, insert connectors, or replace the original graph with an isomorphic proxy.

## 3. Mathematical investigation

First look for a structural solution or obstruction using weighted-degree sums, actual incidences, extremal edge differences, alpha-cut constraints, and required difference partitions.

If a valid labeling exists:

1. Provide every original named vertex and its integer label.
2. Prove the exact vertex-label and difference bijections.
3. Verify the physical entrance and exit.
4. Establish an independently supplied fixed module `B=A(11,6;1,0)`.
5. Apply the retained R241 theorem with old `B=T` and new `A=H(a)`, for every integer `a>=1`.

The conditional joined family is

`J(a) = [[2,2],[2],[a],[a+1]]`.

If the seed succeeds, verify rather than assume the proposed return:

`A(2a+16,a+8;1,1)`.

Prove the single actual connector `s:1--s:2`, port equality `y_B=x_A=0`, complete label and difference bands, returned physical ports, original spine witness, and finite termination.

Only if that construction is established, evaluate repeated compatibility with accepted `(1,1)` modules, normalized alpha gracefulness at `L=0`, and the retained ordinary-graceful suffix consumer for `L>=2`. Keep `L=1` as a limitation of the prescribed interface unless separately proved otherwise.

Do not claim a general three-center quota theorem merely from this fixed seed.

If the prescribed state is impossible, seek a concise analytic proof identifying the exact obstruction. Preserve the scope: impossibility at `(1,0)` does not imply the tree is nongraceful or that another port fails.

## 4. One bounded computational diagnostic

Use CPU-only project-local Python 3.12/3.13, with the standard library and existing project tools. Do not install packages or invoke paid models.

Run an exact, nonquotiented enumeration of the 2,880 prescribed assignments, using the original named graph and fixed physical port conditions.

Every positive assignment must pass the unchanged independent original-target checker.

For negative assignments, preserve a sound falsifier such as two distinct original edge indices having an identical difference. Preserve complete factorial-rank coverage before reporting an exhaustive zero.

Use these controls:

- Retained D081 `[[1,2],[2]]` at `(1,0)` as a positive physical-port control.
- Retained D081 `[[1,2],[1]]` at `(1,0)` as a negative prescribed-state control.
- A false graph digest, false physical offset, and false difference inventory as adverse rejection tests.

Do not launch an alternative-port sweep if the selected state fails. Do not repeat D081's completed enumeration as new research.

### Fixed execution limits

- One worker.
- At most 2,880 new named-assignment visits.
- At most eight new original-graph identities, including any conditional compositions.
- Three adverse checks.
- At most 30 combined process-CPU seconds.
- At most 2 MB per evidence record and 8 MB total new evidence.
- No solver calls, automatic retries, replay campaigns, or increased limits.
- One official producer execution and one independent audit.

A resource-limit interruption is `INCOMPLETE`, not UNSAT.

## 5. Independent verification and reviews

Assign separate read-only mathematical and implementation reviewers after the producer completes.

The mathematical reviewer must independently challenge the prescribed alpha state, any structural obstruction, positive certificate, R241 port equality, original connector, all-parameter composition, closure, and suffix inventories.

The implementation reviewer must inspect original graph construction, full enumeration coverage, named indices, checker independence, control validity, runtime receipts, resource limits, hashes, and historical preservation.

Do not use one research agent's summary as independent proof verification.

Maintain distinct graph digests and labeling ledger IDs.

Any change to algorithms, pruning, quotients, symmetry, or checker semantics requires explicit justification and separate review. Prefer leaving the baseline checker unchanged.

## 6. Evidence and repository closeout

Create a new task-specific proof and evidence directory using the project's established D081 conventions.

Save the exact task specification, frozen configuration, source and runtime identities, original graph records, complete positive certificates, negative receipts, arithmetic audit, independent reviews, execution receipt, and SHA-256 manifest.

Update the authoritative records as applicable:

- `research/FINDINGS.md`
- `research/FAILED_HYPOTHESES.md`
- `research/PROOF_OBLIGATIONS.md`
- `research/DECISIONS.md`
- `STATE.md`
- The matching new file under `handoffs/`

Preserve every accepted previous theorem, original certificate, historical failure, and `INCOMPLETE` record.

Commit and synchronize only Lobster Construction Lab to GitHub `main` using the authorized repository-continuity procedure. Verify local HEAD, actual remote HEAD, clean working tree, and matching handoff. Never routinely force-push or edit either upstream repository.

## 7. Required final report and STOP

Report:

1. **Scientific disposition:** ACCEPT, REVISE, REJECT, or INCOMPLETE, separately for the fixed-port state and any conditional composition theorem.
2. **Progress assessment:** The exact new structural capability established, or the precise fixed-port restriction falsified.
3. **Strategic decision:** CONTINUE, ADVANCE, PIVOT, or REVISE, with the mathematical reason.
4. **Remaining obligation:** The highest-impact unresolved gap toward arbitrary multi-center lobster sections.
5. **One next action:** Exactly one bounded, falsifiable proposal recorded in the updated `STATE.md`, not automatically executed.
6. **Verification:** Named assignment totals, checker and audit results, separate reviews, CPU use, artifact hashes, Git SHA, local/remote identity and historical preservation.
7. **Project instructions:** KEEP or UPDATE NEEDED, with justification.

**STOP after this one task.**

Do not automatically begin the proposed successor, broaden the search, or initiate an ongoing research campaign.
