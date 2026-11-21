# Start here — Windows 11 and Codex

## 1. Put the project in its own folder

Extract the ZIP so that `AGENTS.md` and `00_SETUP.cmd` are directly inside:

```text
C:\Users\Will\Projects\Lobster_Construction_Lab
```

Your existing MDL folders can remain where they are. This package is a curated derivative with its own instructions, mathematics, code and state. It has no remote repository configured.

## 2. Use an existing compatible Python

Use **64-bit CPython 3.12 or 3.13**. If your machine already has Python 3.13.5, it is within this supported range; you need not reinstall it to start. Check in PowerShell:

```powershell
py -0p
py -3.13 --version
```

If needed, obtain Python from [python.org](https://www.python.org/downloads/windows/). The [official Windows guide](https://docs.python.org/3.13/using/windows.html) explains interpreter selection. Select a compatible version already available on the machine where practical. Do not change system permissions or PowerShell execution policy for this project.

## 3. Create the local environment

**Easiest:** double-click `00_SETUP.cmd`. It tries Python 3.13, then 3.12, then `python`, checks the version/bitness, and creates `.venv` in this folder. It installs no optional math libraries.

Equivalent PowerShell commands, using Python 3.13:

```powershell
Set-Location 'C:\Users\Will\Projects\Lobster_Construction_Lab'
py -3.13 scripts\setup_env.py
.\.venv\Scripts\python.exe -m lcl doctor
```

Use `py -3.12` in the setup command if that is your available interpreter. Calling the environment's Python directly avoids activation-script policy issues. `scripts/setup.ps1` is also included for environments that already permit local PowerShell scripts; it does not alter policy. The `.cmd` or direct Python path remains available if `.ps1` is blocked.

## 4. Run the end-to-end example

Double-click `01_DEMO.cmd`, or run:

```powershell
.\.venv\Scripts\python.exe -m lcl demo
```

It reads `examples/h010.json`, expands the declared original graph, computes an H010 labeling, checks it independently, then writes `record.json`, the exact input and a source snapshot under a new `runs/demo-...` directory. A successful summary says `independently_verified: true`. The JSON includes every original edge, every label, graph/config/source identities and versions.

## 5. Validate the core and inspect state

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m lcl status
```

The corresponding launchers are `02_VALIDATE.cmd` and `03_STATUS.cmd`. Missing optional libraries produce skipped optional tests or an explicit unavailable status, while core checks remain usable. Test counts depend on which optional dependencies are installed; see the release validation report for the executed environment.

## 6. Add optional engines only when useful

The core constructors, DFS, dynamic programming, R226, checker and oracle work without them.

```powershell
# SMT cross-checking of exact finite constraints:
.\.venv\Scripts\python.exe -m pip install -r requirements-smt.txt

# Graph diagnostics and isomorphism comparisons:
.\.venv\Scripts\python.exe -m pip install -r requirements-graph.txt

# Exact symbolic identity assistance:
.\.venv\Scripts\python.exe -m pip install -r requirements-symbolic.txt

# Or all three deliberately selected adapters:
.\.venv\Scripts\python.exe -m pip install -r requirements-optional.txt
.\.venv\Scripts\python.exe -m lcl diagnostics
```

Pinned versions are NetworkX 3.7, SymPy 1.14.0, mpmath 1.3.0 and z3-solver 5.4.1.0. The adapters have actually been exercised on Linux/Python 3.12. Current package metadata supports the documented Windows/x64 path, but no Windows runtime test was performed here. Package sources and compatibility details are in `docs/DEPENDENCIES_RESEARCH.md`.

## 7. Open the folder in Codex

In the desktop app choose Codex and open the extracted local folder. The official [quickstart](https://learn.chatgpt.com/docs/quickstart) describes choosing a folder and starting a Codex chat; the [Windows guide](https://learn.chatgpt.com/docs/windows/windows-app) describes native Windows/PowerShell support. Keep your existing permission settings.

Give Codex this first message:

> Read AGENTS.md and STATE.md. Inspect the release validation record and current project files. Continue the one next action in STATE.md using the declared bounded scope. Preserve the original target, distinguish restricted failures from nongracefulness, and report any changed assumptions with the evidence paths. Do not push, publish or start an indefinite campaign.

Codex uses the actual local files. The ChatGPT Project provides the research conversation and uploaded context; exchanging a message alone does not synchronize its uploads with this directory. Follow `chatgpt_project/SETUP.md`.

## 8. Run a deliberate finite diagnostic

`04_PILOT.cmd` runs only the four declared target/interface pairs. The equivalent command is:

```powershell
.\.venv\Scripts\python.exe -m lcl pilot configs\b2_pilot.json
```

It creates a new run each time unless `--resume` is supplied. The release already includes one validation run, so reproducing it is optional unless your local setup or a change needs checking. Read its interpretation before treating results as new research. See `docs/OPERATIONS.md` for exact resume/retry commands.

## Troubleshooting and recovery

If `py` is unavailable but `python --version` reports a supported interpreter, use `python scripts\setup_env.py`. If Python opens the Microsoft Store instead of running, select the installed interpreter explicitly or follow the official Python setup guide.

If an optional installation fails, continue with the core and retain the exact installation error. Do not label an unavailable solver as a mathematical failure. If `.venv` is incomplete, rename that environment directory for inspection, then rerun setup; keep project code and evidence intact.

Press Ctrl+C to cancel a search. Completed case records remain. Resume only with matching source, configuration and environment. A stale `RUNNING.lock` requires checking that the corresponding process has stopped before renaming the lock; do not remove a live run's lock.

## Linux validation path

For reproducibility in a Linux environment:

```bash
python3 scripts/setup_env.py
.venv/bin/python -m lcl demo
.venv/bin/python -m unittest discover -s tests -v
```

The release does not bundle a virtual environment, Python installer or downloaded third-party package.
