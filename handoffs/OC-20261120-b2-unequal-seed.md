# OpenChamber checkpoint: OC-20261120-b2-unequal-seed

**Review status:** PENDING_CODEX_REVIEW  
**Task ID:** B2-UNEQUAL-SEED-001  
**Local working tree / branch:** `C:/Users/Will/Projects/Lobster_Construction_Lab`, branch `main`  
**Last accepted base commit or tag:** session start commit `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685` ("Add OpenChamber handoff protocol v0.1.1"; working tree clean at start); baseline tag `lcl-v0.1.0-baseline` → `36ea1603602491bf3c1c5b81ed4c23aaa2210e70` ("Baseline: Lobster Construction Lab v0.1.0", the start commit's parent); tag untouched  
**OpenChamber checkpoint commit:** the unique commit on `main` since base `6d0f8d23` (message: "B2-UNEQUAL-SEED-001: exhausted restricted negative; retain all-K transport conditional-only; queue pin sweep (PENDING_CODEX_REVIEW)"), local only, not pushed. Its exact hash is not self-contained in this file; obtain it with `git rev-parse HEAD` from a clean tree (or `git log --oneline 6d0f8d23..main`).  
**OpenChamber session/model (if known):** provider `llama-local`, model `qwen38-27b-q5`; separate reviewer subagent session `ses_e02d40103ffeUjxWFNq0LZjw7R` (same local model family; a separate session's review, not external peer review and not a formal certificate)  
**Completion date and time zone:** November 21, 2026, Pacific/Honolulu (run timestamps UTC, 2026-11-21T08:14:41Z)

## Precise mathematical target and restrictions

- Original named profile/graph and source identity: profile `[[1],[2],[]]` via `examples/unequal_seed.json`; eight named vertices, seven actual edges (listed in `research/B2_UNEQUAL_SEED.md` section 1); original graph digest `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`.
- Claim or candidate: does the named prefix admit a graceful labeling under exactly the declared restrictions (bounded negative question), plus the separately assessed conditional all-K high-side-shift transport.
- Physical root/port/branch order/alpha constraints: A-side `s:1, b:0:0, l:1:0:0, l:1:0:1` bijectively labeled `0..3`; B-side `s:0, b:1:0, l:0:0:0, s:2` bijectively labeled `4..7`; physical port pin `h(s:2)=4`; no further root pin, no complement quotient, no symmetry assumption, no automorphism quotient.
- Supplier, consumer or exploratory status: exploratory bounded negative + conditional identity; no supplier promoted or implemented; no P07 obligation discharged.

## Actions actually executed

- Commands from the project root:
  - `.\.venv\Scripts\python.exe -m lcl solve examples\unequal_seed.json --engine dfs --pins examples\unequal_seed_pins.json --domains examples\unequal_seed_domains.json --limits configs\unequal_seed_limits.json`
  - the same command with `--engine oracle`
  - preflight: `python -m lcl doctor`; `python -m unittest discover -s tests` (110 tests, 6 skipped for absent optional dependencies, exit 0); `python -m lcl demo` (CONSTRUCTED, independently verified, record `runs/demo-20261121T080206Z-c0688252`).
- Environment/dependency versions: CPython 3.13.17 (AMD64), Windows-11-10.0.26200-SP0, package v0.1.0, no optional dependencies (z3/networkx/sympy absent); shared source snapshot sha256 `2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd` (identical in both records).
- Time, node, memory, output, concurrency budgets: one worker, one eight-vertex target, at most 10,000 attempted assignments, 2.0 s cooperative time limit, 2,000-state cap, 2 MB record cap (`configs/unequal_seed_limits.json`). No escalation.
- Complete / incomplete / interrupted status: both declared runs **completed as exhausted** (`exhausted=true`, no limit stop). DFS: 65 nodes, elapsed 0.0003 s. Oracle: 5,040/5,040 permutations (144 domain-admissible), elapsed 0.0043 s.

## Evidence and independent checks

- Named witness/negative record, tracked evidence paths and hashes (the `runs/` directory is Git-ignored local work; identifiers are preserved in tracked files):
  - DFS negative: `runs/dfs-20261121T081441Z-0a3c9a64/record.json` — record sha256 `f03d968e014e17d37382ef60a1836177497e388b86d779501fbe6b9dc0071f05`; config sha256 `949e505923d13323e3cb76628773bdee09ed9fee600a49ed88adbb3c7611bdb6`; status `EXHAUSTED_NO_SOLUTION`, count 0, witness null, `hidden_symmetry_reduction=false`, scope `restricted`, `universal_claim=false`.
  - Oracle negative: `runs/oracle-20261121T081441Z-a5f3c783/record.json` — record sha256 `d8c0359adc279d46e5aaffc6cd7affbf7aa70304f659dbc572f5f2eaf978a489`; config sha256 `d0603cf8cf345118b4cddc7423fc573cc576e06e7b77c6b62a3c0c3d8f9673ec`; status `EXHAUSTED_NO_SOLUTION`, count 0, 5,040/5,040 permutations, 144 domain-admissible, witness null, `symmetry_reduction=null` ("named bijections; no symmetry quotient"), `universal_claim=false`.
  - Tracked analytic + review record: `research/B2_UNEQUAL_SEED.md` (sections 1–8).
- Independent original-graph checker result: both records' `original_graph` inspected edge-by-edge against the named target; identical graph digest `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`; `consistency_errors` empty in both; no connector or substituted topology.
- Separate oracle, reviewer, proof or source review (actually performed):
  - Direct permutation oracle cross-check of the exhaustive negative (record above).
  - Separate reviewer subagent challenge (read-only; own independent enumeration of all 144 restricted assignments with no project solver code; scratch script outside the project at `C:\Users\Will\AppData\Local\Temp\opencode\b2_review_scratch.py`, retained for the record): per-item verdicts (a)–(h) all CONFIRMED; no counterexample or missed case; two minor reporting omissions in the note's step 5 corrected (the third 4 in triple `(7,6,5,1)` is unconditional — difference 4 occurs three times there — and the secondary duplicates 5×2 in triple 1 / 6×2 in triple 3 are now reported); the reviewer disclosed and corrected its own scratch-check slip (108 apparent mismatches from applying the `y=3`-restricted identity to `y≠3` assignments; 0 violations on the correct slice).
- Regression results and their exact scope: preflight suite 110 tests (6 skipped, exit 0) and demo CONSTRUCTED/independently-verified, on source snapshot `2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd`. No `lcl/` source, checker, pruning, symmetry or configuration change in this task, so no semantic regression scope beyond the unchanged suite.

## Changed files and provenance

- `git --no-pager log --oneline <base>..HEAD` summary: one OpenChamber checkpoint commit on `main` since base `6d0f8d2` (this handoff and the record updates below); no push.
- Tracked changed files; uncommitted and untracked status: new `research/B2_UNEQUAL_SEED.md`; edited `research/FINDINGS.md`, `research/FAILED_HYPOTHESES.md`, `research/PROOF_OBLIGATIONS.md`, `research/DECISIONS.md`, `research/NEXT_TASK.md`, `STATE.md`; new `handoffs/OC-20261120-b2-unequal-seed.md` (this file). After staging, no other uncommitted or untracked files.
- Changed algorithm, checker, pruning, symmetry, or assumptions: none. No code change; the negative required no checker change. The seed template was not weakened or revised — its exact restrictions are preserved and recorded.
- Earlier baseline/failed evidence preserved at: `evidence/validation/` (frozen release runs, untouched); prior failure-ledger entries unchanged; baseline tag `lcl-v0.1.0-baseline` untouched.

## Scoped result and next action

- Result and scope: under exactly the declared restrictions (A/B domain bijections `0..3`/`4..7` + pin `h(s:2)=4`, no other quotient), the named eight-vertex prefix `[[1],[2],[]]` **has no graceful labeling**. Established by a confirmed analytic obstruction (difference 1 forces `h(s:1)=3`; `a+2b−x=18` admits only the triples `(5,7,1)`, `(6,7,2)`, `(7,6,1)`; every resulting assignment duplicates difference 4 on at least two actual edges) and by an exhausted bounded DFS plus an exhausted direct permutation oracle on the same original graph digest. This is not a nongracefulness certificate for the unrestricted tree, for any other restriction set, or for the K≥1 unequal family. The all-K high-side-shift transport is retained as a conditional identity only (correct if the seed existed; antecedent false); it discharges no P07 obligation and is not implemented. No universal, novelty or formal-verification claim is made.
- Remaining proof or reproduction obligation: P07 for the unequal family remains open. Queued (not executed) alternative: the pin sweep `h(s:2) ∈ {5,6,7}` on the same named target under the same alpha domains and the same declared bounded protocol, with the oracle cross-check rule per exhaustive negative — see `research/NEXT_TASK.md`.
- Proposed review disposition (Codex decides): PENDING_CODEX_REVIEW
- Exactly one next action: Codex acceptance review per `docs/CODEX_RETURN_PROMPT.md` — independently adjudicate the analytic argument, the run records and the record updates (ACCEPT / REVISE / REJECT) before any promotion. The queued pin sweep begins only after that decision.

No remotely pushed work, paid usage, system security changes or indefinite research are authorized by this template.
