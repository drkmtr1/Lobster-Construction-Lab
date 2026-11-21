# OpenChamber setup for Lobster Construction Lab

Scope: project-local OpenChamber/OpenCode workflow alongside Codex. This does not install OpenChamber, change model/provider credentials, change operating-system security settings, connect GitHub, modify upstream repositories or start research.

## Prerequisites

- Verify the extracted LCL project at `C:\Users\Will\Projects\Lobster_Construction_Lab` contains `AGENTS.md`, `STATE.md`, `research/NEXT_TASK.md` and the `.git` directory.
- Confirm `git --no-pager log -1 --oneline`, `git status`, and `git tag --list` show the local baseline `lcl-v0.1.0-baseline` at commit `36ea160` (unless a later reviewed LCL baseline is separately recorded).
- Run `00_SETUP.cmd` and `02_VALIDATE.cmd` if local Python setup/validation has not been performed. The release executed on Linux; Windows validation is a local task.

## OpenChamber project

1. Open OpenChamber Desktop. Select `+` at the top of the session sidebar (or **Add project** from the command palette).
2. Choose **the existing local LCL folder**. Do **not** clone a second copy and do not extract the v0.1.0 ZIP again into the project directory.
3. Check the active project folder, current Git branch and working tree. Do not launch a research Session Goal yet.
4. OpenCode automatically reads project `AGENTS.md` and discovers `.opencode/skills/*/SKILL.md` when supported. Mention `@lcl-bounded-research` or `@lcl-handoff` explicitly if auto-selection is uncertain.

Primary references: https://docs.openchamber.dev/projects/ , https://opencode.ai/docs/instructions , https://opencode.ai/docs/skills/ .

## Attach a model independently of Codex allocation

In OpenChamber Desktop, open **Settings → Providers → Add provider → Other / Custom**. An OpenAI-compatible local llama.cpp endpoint on the same EVO machine can use:

- Provider ID: `evo-local` (chosen locally; not an upstream ID)
- Display name: `EVO llama.cpp`
- Base URL: `http://127.0.0.1:8081/v1`
- Model ID: **copy the exact ID returned by your running server**, not an assumed GGUF filename.
- API key: For a local unauthenticated loopback llama.cpp endpoint, a non-secret placeholder such as `local-only` may be used if the UI requires a key. Do not put actual provider secrets in project files.

Before entering a model ID, in PowerShell run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8081/v1/models" | Select-Object -ExpandProperty data | Select-Object id
```

If this fails, start or troubleshoot the existing llama.cpp server. Do not assume a particular model is loaded or change the installation on your behalf. The model must support OpenCode's tool-call format; API responsiveness alone does not establish it. For long coding sessions, a 4,096-token context may be inadequate. Consider a measured `-c 16384` or larger setting only after checking supported context, capacity and responsiveness. Preserve `--jinja` and the model's correct chat template when using the existing server. Keep the server bound to `127.0.0.1`; do not expose it publicly for this workflow.

Pick the connected model in the chat's model selector. Run a **read-only tool test** first: ask the agent to report the first heading of `AGENTS.md` and the current `git status --short` using actual file/shell tools. Then a bounded Python test. A model that only writes plausible prose without working tool calls is not ready to edit the lab.

References: https://docs.openchamber.dev/providers/ , https://opencode.ai/docs/models/ .

## Permissions, agents, skills and MCP

- For the first sessions use **Ask every time** permissions via the shield control, not **Accept everything**. **Important:** this mode asks only when an OpenCode rule has the effect `ask`; by default, many shell and edit actions are already allowed. Inspect the chosen agent's tool rules in **Settings → Agents**, and explicitly set `shell` and `edit` actions to `ask` if you want to approve those actions individually. `Settings → Sessions → Permissions` controls new sessions. Permission prompts do not establish mathematical correctness.
- Do not enable automatic Session Goals, scheduled tasks or Multi-run until normal bounded handoff works. If used later, explicitly set a finite task, compute/time limits and a stop condition. Isolate parallel write-producing runs in separate Git worktrees.
- The two project-local skills are supplied in `.opencode/skills/`. No global skill installation is required.
- **No MCP server or third-party skill is required for first research.** Python, Git, the existing source excerpts and standard library are sufficient. Add an MCP only for a specific task; scope it to the project in Settings → MCP and approve any credential or outbound-data access separately. GitHub integration is optional, not a substitute for local commits/checker evidence.

References: https://docs.openchamber.dev/permissions/ , https://docs.openchamber.dev/session-goals/ , https://docs.openchamber.dev/mcp/ .

## Safe first session (no research changes)

Paste `docs/OPENCHAMBER_FIRST_PROMPT.md`. Review the output: the project path, Git baseline, project state, Python availability, tool-call execution and no unintended changes. Finish or stop this session before beginning `B2-UNEQUAL-SEED-001`.

## Workflow and review

- OpenChamber does one declared task in `STATE.md`, writing actual evidence and a handoff in `handoffs/`, guided by `docs/OPENCHAMBER_HANDOFF.md`.
- The handoff is marked `PENDING_CODEX_REVIEW` for consequential results. OpenChamber may preserve a local Git commit, but does **not** tag it Codex-accepted or silently promote a theorem on its own.
- When Codex is available, give it `docs/CODEX_RETURN_PROMPT.md`. Codex reviews actual committed and uncommitted changes, original-graph mathematics, independent checker, and handoff. Record an acceptance, revision or rejection in the project authority files.
- Never let both clients edit the same live working directory at once.

The most recent reviewed `STATE.md` remains authoritative for the next action. This add-on does not rewrite or declare completion of that task.
