# ChatGPT Project setup pack

**Name:** Lobster Construction Lab  
**Description:** Research independently supplied graceful constructions and repeatable transitions for lobster trees, with a separate Codex workspace for exact algorithms and reproducible evidence.

The native ChatGPT Project was not created by this delivery: no callable capability to create that particular object was available. The pack is complete for manual setup. Creating a Space or a website would be a different object.

## Create the project

1. In ChatGPT, choose **New project** in the sidebar and enter the name above.
2. Open the project's **more options (•••) → Project settings** and paste the entire contents of `PROJECT_INSTRUCTIONS.md` into its instructions.
3. Upload `UPLOAD_CONTEXT.md`. Also upload the source-linked audit from `references/MDL_General_Construction_Review_2026-11-20.md`, `docs/RESEARCH_PLAN.md`, `docs/METHOD_SELECTION.md` and `docs/LITERATURE_UPDATE.md` if space permits. These five files form the suggested initial context set. Upload a current generated handoff instead of stale context when work advances.
4. Paste the contents of `KICKOFF.md` as the first message.

These steps follow the official [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) guidance inspected for this build. Product UI and account limits can change; the materials remain plain Markdown. The instructions use an **8,000-character design budget**; `PACK_METADATA.json` records the measured Unicode character count. That is a project design choice, not a claim about a universal product limit.

## ChatGPT and Codex responsibilities

ChatGPT explains the strategy, researches sources, proposes and critiques mathematical claims, and prepares concrete task packets. Codex works in `C:\Users\Will\Projects\Lobster_Construction_Lab`, reads `AGENTS.md`/`STATE.md`, changes code, executes bounded checks and preserves evidence. Either can review, but consequential claims should receive a genuinely separate review role where available.

The two folders do not automatically synchronize merely because they share a name. After a meaningful Codex session, run `python -m lcl context --out handoff_002.md` using a fresh filename; bring that file and the relevant report/certificate back to ChatGPT. After a ChatGPT proof or design discussion, send Codex the exact accepted statement, source citations, assumptions, output contract and bounded verification request. Codex should update the authoritative local records before further experiments.

## Suggested task packet

Specify: objective ID; exact original graph family/domain; existing baseline; proposed input/output state; restrictions; proof obligation; files to change; declared runtime/case/node/state/output caps; independent checker/comparison; what counts as success; what would falsify the claim; and the expected handoff files. Use the live state rather than asking each session to rediscover the entire history.

Do not paste credentials into either workspace. Private upstream source links require the user's existing authorized GitHub access; the ZIP includes curated mathematical excerpts for offline continuity.
