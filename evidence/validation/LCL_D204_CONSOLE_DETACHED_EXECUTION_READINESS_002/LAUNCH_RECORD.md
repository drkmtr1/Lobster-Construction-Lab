# Prepared D204 scientific launch and held authorization draft

**Held after the V8 interruption qualification stop.** The implementation below is frozen and independently reviewed as infrastructure. The Windows qualification marker required by its official entry is absent. The command has never been run against D204 and no scientific approval is being issued. [Current outcome](RESULT.json) · [V8 freeze](V8_FREEZE.json)

## Bound operation

The controller runs from the LCL repository root on the exact installed base CPython 3.13.17 AMD64 path reported by the existing project-local venv. It uses `-I -S -B`. The worker's command, CWD, image validation, startup files, module bytes, original inputs, accepted limits and handles are fixed by the V8 source and freeze. The only intended scientific write root for V8 is the vacant `evidence/runs/d204-science-v8`. The fixed approval and independent Git receipt paths are `runs/d204-science-v8-approval.json` and `runs/d204-science-v8-live-refs.json`. The local Git executable is the existing `Program Files/Git/cmd/git.exe`. No packages, configuration changes or scientific options are required by the code. Native qualification remains the missing prerequisite.

The exact V8 command shape is retained for review. The placeholder denotes the SHA-256 of an explicit new Owner approval after qualification. This revision cannot meet its qualification prerequisite on the retained evidence.

```powershell
Set-Location -LiteralPath 'C:\Users\Will\Projects\Lobster_Construction_Lab'
$basePython = & .\.venv\Scripts\python.exe -I -S -B -c 'import sys; print(sys._base_executable)'
& $basePython -I -S -B .\research\d204_readiness_v8\entry.py LCL-D204-CONSOLE-DETACHED-EXECUTION-READINESS-002 official e8fff596bcd685a0924699840e751d4f4fd32d0baceb71b8aeb4bffc23ac2183 '<approved-approval-sha256>'
```

For a future qualified revision, immediately before requesting authorization, capture the raw ref output from the three verified read-only operations in their bounded admission session. Confirm the local exact approved HEAD, a clean worktree, baseline tag and peel, and vacant output/approval paths. Convert the observed results into the checked integer UNIX timestamp and named `refs` map that the actual approved launcher requires. Bind the exact JSON sidecar to the Owner approval by SHA-256. The V8 gate requires it to be at most 900 seconds old and saves its exact bytes within the evidence budget.

```powershell
git ls-remote --exit-code origin refs/heads/main refs/tags/lcl-v0.1.0-baseline 'refs/tags/lcl-v0.1.0-baseline^{}'
git ls-remote --exit-code https://github.com/drkmtr1/Math-Discovery-Lab.git HEAD
git ls-remote --exit-code https://github.com/drkmtr1/MDL_Bounded_Search.git HEAD
```

## Authorization text to hold until readiness

> I authorize one D204 scientific execution on the exact frozen 32-edge prefix and 41-edge target under the accepted arbitrary coordinated-gap domain. Use only the independently qualified checkpoint, matching freeze and exact future approval and live-ref bindings. Preserve frontier 0, induced old cut 14, physical cut 18 or 19, threshold C+2, both ranks and all 8,518,360 prospective cut-geometry occurrences. The 48-edge target is deterministic verification only. Use the accepted native Windows measured-acceptance policy and unchanged counters, times and 128,000,000-byte total. Run primary once. Run independent audit only after duly reconciled primary exhaustion. Preserve the candidate and its receipt before same-phase verification. Stop on any incomplete, resource, evidence or verification failure or on a complete disposition. Do not retry, escalate, broaden the scientific scope, or start D205.

The future approval record binds `intent = AUTHORIZE_ONE_D204_SCIENTIFIC_RUN`, task, fresh exact run ID, freeze hash, qualification receipt hash, expected approved repository head, hash of the fresh live-ref receipt, verified ref fields, the full frozen limits map and the actual Owner authorization. Readiness and Owner authorization must both exist for any run. This held text and reference command confer neither. The V8 gate has no final qualification marker. The held text is ineligible for submission as a scientific approval.
