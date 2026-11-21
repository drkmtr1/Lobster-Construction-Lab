# Continuity handoff: GitHub synchronization maintenance

- Scope: repository continuity and synchronization only; no new mathematical research.
- Repository: `drkmtr1/Lobster-Construction-Lab`, branch `main`; this handoff is `handoffs/CONTINUITY_20261121.md`.
- Starting commit: `5fb2fa108835720c829cafd5095983f3c0f6198d`; last accepted research baseline: `lcl-v0.1.0-baseline` (`36ea160`).
- Checkpoint commit: locate the commit introducing this handoff using `git log --follow -- handoffs/CONTINUITY_20261121.md`; verify its contents. Its final local/remote SHA is reported in the session closeout, not guessed in this file.
- Starting tree: clean; no remote configured. The designated GitHub repository was verified public and empty before the initial push. Final synchronization must be verified externally after the commit.

## Research status

- `STATE.md` retains the scientific objective and sole next action. The balanced zero-padding supplier and padded baseline are adopted only on their stated domains; see `research/FINDINGS.md` and `research/PROOF_OBLIGATIONS.md`.
- The pinned unequal seed restricted negative, conditional-only transport, evidence custody and K>=6 adjacent-port interface obstruction remain pending independent Codex acceptance. See `research/B2_UNEQUAL_SEED.md`, `research/B2_INTERFACE_OBSTRUCTION.md` and `handoffs/OC-20261121-b2-review-integration.md`. The superseded pin sweep was not executed.
- The unequal independent supplier and a revised compatible interface remain open. `research/PROOF_OBLIGATIONS.md` is authoritative.
- This maintenance task makes no new mathematical claim. Historical run evidence remains subject to its original restrictions and review status.

## Work and checks

- Continuity rules, agent instructions and templates were updated. Six ignored local runs, including two validation runs from this task, are byte-verified copies under `evidence/runs/`; `evidence/runs/MANIFEST_20261121.json` records all 138 file hashes and sizes. No run artifacts were intentionally excluded except transient locks and caches; none were present in the six copies.
- Windows project-local Python 3.13.17: `python -m unittest discover -s tests -v` passed 110 tests with six optional-dependency skips; `python -m lcl demo` constructed and independently verified the 14-vertex example; `python -m lcl solve examples/p4.json --engine dfs --count --limits configs/smoke.json` returned SAT, count 4, with independent verification. These are maintenance validation checks, not a new research campaign. UTF-8 mode was enabled for CLI output.
- The target repository is public. `UPSTREAM_NOTICE.md` preserves provenance and records that upstream trees had no tracked licenses and were private. The owner authorized synchronization to the named repository; no new license is asserted. The tracked tree and copied runs were scanned for common credential patterns; this is not a complete security or legal audit.

## One next action

Carry out the independent Codex acceptance review of the provisional integration checkpoint, as specified in `STATE.md` and `docs/CODEX_RETURN_PROMPT.md`.
