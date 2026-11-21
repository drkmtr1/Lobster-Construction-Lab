# Codex task: reconcile and record the B2 acceptance review

**Scope:** one bounded local acceptance-and-record task in the existing Lobster Construction Lab checkout. Read this review pack as evidence. Do not start the queued pin sweep, a new search campaign, a remote push, an upstream edit, or an installation.

## 1. Reconcile the authoritative checkout

Read the current `STATE.md`, `AGENTS.md`, `docs/CODEX_RETURN_PROMPT.md`, `docs/OPENCHAMBER_HANDOFF.md`, the current handoff and relevant research records. Locate the actual last accepted baseline, then review all intervening committed and uncommitted changes. The supplied review concerns checkpoint `0f0a39c4d8d97d211782d1a1d81aeba5e0481319` after `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685`; its diff covers those two revisions. If the earlier handoff overlay has not been accepted, include it in the local review. Do not infer acceptance from a clean tree or from a session-start label.

Preserve the baseline tag `lcl-v0.1.0-baseline` at `36ea1603602491bf3c1c5b81ed4c23aaa2210e70`, prior runs, failed hypotheses, source and checker. If the checkout has advanced, account for its changes without resetting them. Keep OpenChamber and Codex from simultaneously writing the same tree.

Read `REVIEW_REPORT.md`, `B2_INTERFACE_OBSTRUCTION.md`, the three notes in `analysis/`, and the independent check artifacts from this pack. Compare the supplied records with their original local files. The pack is evidence, not a replacement project.

## 2. Adjudicate the completed seed task

Independently assess and explicitly ACCEPT/REVISE/REJECT:

- The exact p=4 restricted negative on the original named prefix, with the existing A/B domains and no extra pins or symmetry quotient.
- The conditional all-K high-side shift and original path-consumer formula, retained conditional-only because the required seed does not exist.
- The raw records, canonical hashes, input/configuration identity, matching source inventory and complete count scope.

The supplied DFS/oracle records already decide the task, and the review pack includes a new independent 144-assignment check with zero witnesses. Reuse this evidence. Rerun only a narrowly justified check if a concrete discrepancy remains; do not repeat the four-pair validation or full release suite merely as ritual.

## 3. Independently check the new interface obstruction

Review the full proof in `B2_INTERFACE_OBSTRUCTION.md`, including every endpoint and orientation case:

> For q=1, r=2, z0=z1=0 and every K>=6, the exact eight-vertex prefix through s:2 cannot leave unused labels [ell,ell+K-1], unused differences 1..K, and physical port ell-1 or ell+K, for any ell or side.

Check that difference m forces labels 0 and m into the prefix; both used-label blocks then have span at most 6; all edges must cross for K>=6; the connected 4/4 bipartition forces ell=4; high-block compression gives the forbidden p=4 seed directly on the above side, and after complementation on the below side.

No alpha condition is assumed initially. Complementation here is a proof implication, not a counting quotient. The threshold 6 is sufficient, not asserted sharp. This is not ordinary nongracefulness. The proof has already received two separate agent challenges in this review; record your own local disposition accurately. No K>=6 search is needed to replace the quantified proof.

## 4. Preserve and correct the evidence

Create one tracked, clearly scoped evidence directory, for example `evidence/reviews/B2_UNEQUAL_SEED_001/`. Copy the two historical run records and exact target/pin/domain/limits files byte-for-byte; preserve the original `runs/` files. Include an explicit raw SHA-256 manifest and distinguish raw-file hashes from the canonical `record_sha256` fields. Include the review output, independent checker script, new proof and reviewer notes in appropriate tracked locations.

Preserve the historical `b2_review_scratch.py` as an earlier diagnostic version. It applies the y=3-specialized identity to all 144 assignments. Cite the new independent check, whose general identity is `S=a+2*b-x-2*y+16`, rather than describing the old scratch as fully corrected.

Correct the degree-list typo in `research/B2_UNEQUAL_SEED.md` §3 Step 3: s:2 is a high-side vertex of degree 1, contributing +4; the equation itself is correct. Label the historical reviewer slip explicitly. Keep the original failed evidence and restriction set.

The raw exported `checkpoint.diff` has reversible encoding damage; `analysis/checkpoint.normalized.diff` was recovered and checked against all eight uploaded postimages. Do not treat the export issue as corrupted Markdown source. If you export another diff, prefer Git's direct `--output` path over a PowerShell native-output decoding pipeline.

## 5. Update the authoritative owners consistently

- `research/FINDINGS.md`: record accepted scoped seed and interface results, with exact domains and proof references.
- `research/FAILED_HYPOTHESES.md`: preserve F-UNEQUAL-SEED and add the separate failure of the all-K interval/adjacent-port objective; do not broaden either to nongracefulness.
- `research/PROOF_OBLIGATIONS.md`: distinguish the impossible old interface for q=1, r=2, K>=6 from open duties for a genuinely revised interface. Retain the conditional transport and valid balanced/padded constructions.
- `research/DECISIONS.md`: record the acceptance disposition, evidence custody and why the pin-sweep-as-repair plan is superseded. Preserve D015 as history rather than silently rewriting it.
- `research/NEXT_TASK.md`: preserve the former proposal as superseded and explain that p>=5 gives port K+p, whereas the existing consumer requires the adjacent port K+4; K=1 gives suffix difference p-3 instead of 1. Do not execute the sweep.
- `STATE.md`: record actual review disposition and exactly one subsequent scoped action. A proposed future direction is to formulate and prove/refute a nonadjacent-port path consumer before searching for a seed. Keep that task proposed and unexecuted in this review.
- Handoff/review record: distinguish reviewed mathematics from local code execution, and identify checkpoint 0f0a39c... as the reviewed source. Record the status for each consequential claim rather than applying blanket acceptance to an unsuitable next-task proposal.

A possible future consumer question is an interval [ell,ell+K-1], differences 1..K, and endpoint ell+K+1 for an explicit K-domain beginning at K=2; K=1 would need separate treatment for any all-positive-K construction. This is a candidate question only. Do not assume the consumer or a matching seed exists, and do not start that task during this handoff reconciliation.

## 6. Verification, checkpoint and stopping condition

Review the final diff for correct claims, unchanged original topology/checker/algorithm, preserved evidence bytes, explicit scope, and one next action. Since this is a records-and-proof task, avoid unrelated dependency or algorithm changes.

Make a local review commit if this is consistent with the checkout's current workflow. Keep the baseline tag unchanged. Report the new commit hash after committing; do not amend repeatedly to embed a commit's own final hash into itself.

Return a concise Owner report with claim-by-claim ACCEPT/REVISE/REJECT, exact changed files, evidence paths, checks actually executed, remaining obligation, and one next action. Stop. No automatic successor research.
