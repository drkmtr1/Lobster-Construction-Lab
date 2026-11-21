# Experiments, verification, and recovery

## Commands

Run from the project root, using its environment's Python. Below `python` means `.\.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on Linux.

```text
python -m lcl doctor
python -m lcl demo
python -m lcl construct examples/l007.json
python -m lcl construct examples/two_section_padded.json
python -m lcl construct examples/two_section_balanced.json
python -m lcl allocate examples/r226.json
python -m lcl solve examples/p4.json --engine dfs --count
python -m lcl solve examples/p4.json --engine dp
python -m lcl solve examples/p4.json --engine oracle
python -m lcl solve examples/p4.json --engine z3
python -m lcl solve examples/p4.json --pins examples/p4_bad_core_pins.json --count
python -m lcl pilot configs/b2_pilot.json
python -m lcl status
python -m lcl context --out handoff_001.md
```

Each construction/solve/allocation writes a new `runs/` directory by default. Use `--out <new-directory>` for an explicit destination. Existing evidence is preserved: an existing single-run output directory is an error. `verify <original-graph-file> <record-or-label-file>` checks against a separately supplied original; it does not trust a target introduced only by a solver.

The core returns exit code zero for a properly recorded finite result, including an incomplete or restricted negative. Inspect the JSON status before drawing a mathematical conclusion. Invalid input, unavailable engines and quarantined positive outputs have nonzero CLI outcomes except where a pilot checkpoint explicitly reports its stop reason; check that reason as well. Ctrl+C outside a controlled engine returns 130.

## Declared limits

These are deliberately conservative **design limits**, not benchmarks or guarantees about Will's hardware.

| Profile | Cases / worker count | Search budget | Memory/output controls |
|---|---|---|---|
| Smoke (`smoke.json`) | One case, one worker | 10,000 node/transition attempts, 2 seconds, 8 vertices | DP 2,000 states/layer; default record <=2 MB |
| Small reference (`reference.json`) | One case, one worker | 200,000 attempts, 5 seconds, 12 vertices | DP 20,000 states/layer; oracle additionally <=8 vertices; record <=2 MB |
| Initial B2 (`b2_pilot.json`) | Four declared pairs/invocation, one worker | 50,000 attempts and 2 seconds/case; 16 vertices; 20-second invocation budget | DFS has no state cache; 2 MB/attempt, at most 8 MB case JSON/invocation plus small snapshots/checkpoint |
| Larger research | No default campaign | A new explicit config and stated mathematical question | Select state/case/time/output budgets before running; compare actual use first |

DFS has recursion bounded by the vertex cap, integer masks and per-level candidate lists; it does not retain the entire search tree. DP bounds each of its old/new maps by `max_states`, so both maps may coexist, along with representative histories and arbitrary-precision counts. The state limit is a structural memory control, not an exact byte ceiling. For the initial profiles, set a planning memory envelope of 512 MiB per worker; monitor actual process use before increasing limits. The code does not enforce that envelope as an operating-system limit. Z3 receives its own 512 MiB internal memory parameter, timeout and `rlimit`; that is also not a process/container limit. The 128 GB installed memory is not a reason to expand an uninformative search.

The node field has method-specific meaning: DFS counts attempted assignments; DP counts transitions considered; the permutation oracle uses the same numeric cap as a permutation cap; Z3 receives it as solver resource units. These are not directly comparable performance metrics.

Timing is cooperative. Python engines check at search/transition boundaries; Z3 bounds its solving call. Graph parsing, model construction, snapshots, checking and disk I/O add overhead. The invocation budget reduces the next case's solver allowance and prevents starting another case once the time is gone; it is not an OS-enforced kill deadline. Ctrl+C or an external process stop remains available. No process spawns an additional worker automatically.

Pilot config files must be <=2 MB, contain at most 5,000 explicitly declared cases and at most 100 cases per invocation. Pilot/solve targets have an ingestion cap of 100 vertices, and lower engine caps normally apply. Other CLI graph/construction inputs have a 10,000-vertex and 2 MB input cap checked before expansion; output records remain capped at 2 MB. Direct formula functions can create larger graphs when called deliberately; CLI design caps do not constrain a mathematical formula's proven parameter domain.

## Reproducible records

Single-run records contain the original graph and its digest, the complete result/witness, independent checker report, exact configuration and hash, code/dependency-file hashes, environment/package versions and an immutable code snapshot. Timestamps use UTC explicitly. A source checksum detects content changes; it is not a signature or a guarantee that an environment is trustworthy.

Pilot `manifest.json` records the exact ordered case list, source inventory, environment and run signature. Each `cases/<case-id>.attempt-0001.json` is immutable. `checkpoint.json` is an atomically replaced summary reconstructed from those attempts. It is a convenience index, not a second conflicting result ledger. Verify original targets and case restrictions before using a summary count.

Case IDs hash exact parameters, including physical ordering and the chosen interface. A source/configuration/environment change creates a new run; it must not be resumed as the old run. Runtime identity covers code and dependency declarations, not research prose. The release manifest additionally hashes all packaged files.

## Cancellation and resume

Resume at **case boundaries**. The starter does not serialize an unfinished DFS stack, DP layer or SMT solver. Completed attempts remain valid evidence; an unfinished case can be retried under the same limits, retaining both attempts.

```text
python -m lcl pilot configs/b2_pilot.json --resume runs/b2-EXACT-DIRECTORY
python -m lcl pilot configs/b2_pilot.json --resume runs/b2-EXACT-DIRECTORY --retry-incomplete
python -m lcl status --run runs/b2-EXACT-DIRECTORY
```

The first skips already recorded cases. The second also retries cases whose latest attempt is `INCOMPLETE`. A repeated retry with an identical deterministic node cap may make no progress; choose a changed configuration and a new run when testing a justified change. Do not automatically double budgets.

A source or dependency change rejects resume. Keep the old run, inspect its saved source, and begin a new run with the changed environment. `RUNNING.lock` protects only that local directory against overlapping writes. If a process was killed and the lock remains, confirm it is no longer running, then rename the lock to a dated recovery note. The script never removes another live process's lock automatically.

Atomic writes protect against partially written JSON at the normal filesystem level. Sudden power loss, disk failure and network filesystem behavior are not a full durability guarantee. Back up valuable results and initialize a private local Git history when appropriate. Do not discard failed or interrupted evidence when correcting a hypothesis.

## Acceptance and review

Every positive engine/constructor result passes the independent checker against the caller-retained original target. Invalid positives are quarantined and must be investigated before further scientific interpretation. Solver failures remain scoped to pins/domains. Exhaustion is implementation evidence, not a formal independently checked negative certificate.

Run the smallest checks addressing the changed risk. Constructor changes need exact domain boundaries and adverse labels/topology checks. Pruning or DP compression changes need independent exhaustive comparisons on small named graphs and a proof of preserved completions. Verifier changes need separate review and intentional false-certificate rejection. Avoid rerunning broad campaigns merely because files were edited.

## Handoff and optional private Git setup

Update the authoritative `STATE.md` and the relevant findings/failures/obligations. Generate a fresh context file with `python -m lcl context --out <new-file.md>`. Include run IDs, exact source/config identities, unresolved questions and one next action. Uploaded ChatGPT files are snapshots; replace stale context deliberately after substantive changes.

For a later local history, from this folder:

```text
git init
git add .
git commit -m "Initialize Lobster Construction Lab from pinned MDL evidence"
```

This does not create a remote fork. Before any remote publication, review `UPSTREAM_NOTICE.md`, choose visibility/license deliberately and obtain the user's authorization. If the user authorizes a private remote later, create it empty, add its supplied URL with `git remote add origin <private-url>`, and push the reviewed local branch. No remote action is part of this release.
