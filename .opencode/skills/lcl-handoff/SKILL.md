---
name: LCL Handoff to Codex
description: Preserve a scoped OpenChamber research checkpoint, Git diff, independently checked evidence, and a PENDING_CODEX_REVIEW report for later Codex acceptance.
---

# Skill: finish and hand off, not continue indefinitely

Read `docs/OPENCHAMBER_HANDOFF.md` and `handoffs/HANDOFF_TEMPLATE.md`. Ensure no further experiments remain active. Document original topology/restrictions, exact commands and limits, outcome, independent checker/cross-check evidence, changes to mathematical assumptions, source+config+environment versions, and concrete tracked result paths. `runs/` is Git-ignored; keep reviewable consequential evidence in tracked `evidence/` or in a separately identified immutable copy.

Use `git status`, `git diff`, `git log` and untracked-file checks. Do not assume a clean working tree means no commits. Update only authoritative research records required by this outcome. Mark consequential claims PENDING_CODEX_REVIEW. Preserve local work in a reviewed Git checkpoint commit when appropriate; do not push, publish, overwrite previous negative evidence, silently approve your own novel theorem or start a successor task. Leave one next action for the Codex acceptance review.
