# OpenChamber → Codex handoff protocol

## Boundary and authority

This protocol applies to every OpenChamber task that changes LCL mathematics, code, tests, evidence or research state. It does not imply that Codex monitors OpenChamber automatically. An OpenChamber session and Codex session read the same project files only when pointed to the same project folder (or to a separately reconciled worktree).

`STATE.md` owns the current objective and exactly one next action. `research/FINDINGS.md`, `FAILED_HYPOTHESES.md`, `PROOF_OBLIGATIONS.md`, and `DECISIONS.md` each own their specified facts. `handoffs/` stores **individual review requests**, not a competing state ledger. `runs/` is Git-ignored; consequential evidence needed for review must be copied/recorded with immutable identifiers in a tracked evidence path before a checkpoint commit.

## Before OpenChamber begins

1. Ensure no Codex/OpenChamber worker is writing the same working tree.
2. Read `AGENTS.md`, `STATE.md`, the exact next task, and relevant primary sources/proofs.
3. Capture `git status --short`, `git rev-parse HEAD`, last reviewed commit or baseline tag, and any existing uncommitted work. Do not hide pre-existing changes or blend unrelated edits into a review request.
4. Declare: exact hypothesis, input domain/restrictions, target physical topology, proof obligation, case/compute budgets, output and stop criteria.
5. Use a separate local branch/worktree for risky exploratory algorithms when justified. Never change upstream repositories; Git and GitHub actions for this project are authorized under `docs/REPOSITORY_CONTINUITY.md`.

## During the bounded task

- Preserve original graph, named vertices, branch identities, physical attachment ports and both resource inventories.
- Save witnesses, counterexamples, run limits and verifier output. An incomplete result remains incomplete; a restricted negative is not ordinary nongracefulness.
- Preserve prior baselines and failed evidence; changes to semantics, pruning, symmetry, correctness, completeness or checker need separate review.
- Keep results traceable to source/config/checker identity. Do not silently depend on prior conversation context or an untracked `runs/` directory.

## At the checkpoint

1. Run project tests relevant to the changed algorithms; do not silently widen the declared experiment.
2. Record the exact changed paths and existing/uncommitted Git changes, including any generated tracked evidence.
3. Write `handoffs/OC-YYYYMMDD-short-id.md` using `handoffs/HANDOFF_TEMPLATE.md`, filling in actual result and commands. Do not invent PASS status when a tool/test is unavailable.
4. Mark consequential new results as **`PENDING_CODEX_REVIEW`**. Provisional findings can be recorded with explicit evidence level, but do not present an AI review as a formal proof or historical novelty.
5. Update existing authoritative state and scientific records as appropriate, leaving exactly one next action. If no mathematical progress, state that precisely.
6. Preserve a local checkpoint commit on the current work branch **after reviewing staged files**; commits do not mean mathematical acceptance. Synchronize the reviewed checkpoint under `docs/REPOSITORY_CONTINUITY.md`; do not apply an acceptance tag. Record the checkpoint SHA in a subsequent receipt or resolve it from Git as described there.
7. Stop. Do not launch a successor task, continuing Session Goal, scheduled run or unlimited exploration.

## When Codex returns

1. Confirm OpenChamber jobs stopped and working tree is stable.
2. Start from the **last accepted** checkpoint (or `lcl-v0.1.0-baseline` for the first review), not necessarily the newest commit.
3. Inspect `git log <base>..HEAD`, `git diff <base>..HEAD`, `git diff`, `git diff --cached`, `git status --short`, and untracked paths. A clean working tree does not mean no intervening changes.
4. Inspect code, actual mathematical source arguments and real original-target certificates. Cross-check the exact claimed domain and all constraints. Run relevant bounded tests or separately structured exact checks as justified.
5. Issue **ACCEPT**, **REVISE**, or **REJECT** per consequential claim/change. Record reviewer identity, evidence level, accepted commit hash and remaining proof obligation. Self-review must be labeled self-review; distinct model roles alone do not imply external peer review or formal checking.
6. Correct/adopt authoritative records. Preserve failures, and leave one next action. If the code or checker changes during review, that change itself needs suitable regression review.

For first review against tag: `git --no-pager log --oneline lcl-v0.1.0-baseline..HEAD` and `git --no-pager diff --stat lcl-v0.1.0-baseline..HEAD`.
