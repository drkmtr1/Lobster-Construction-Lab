# Lobster Construction Lab

**A working research starter for turning retained graceful-labeling constructions into independently supplied, repeatable transitions.** Version 0.1.0, prepared November 20, 2026 (Hawaiʻi). The repository snapshots are pinned in `UPSTREAM_NOTICE.md`.

For a tree with `m` edges, assign the numbers `0..m` once each to its vertices. Every actual edge then receives the absolute difference of its endpoint labels. The tree is graceful when those differences are exactly `1..m`, each once. A lobster is a tree with a path within distance two of every vertex.

Our input is the tree's structure, not just its size. A universal answer could be an algorithm or a collection of proved construction rules; it need not be one short equation. This project pursues rules that build a piece and return usable labels, differences and attachment points for the next piece.

## Start here

On Will's Windows 11 computer, extract this folder to:

```text
C:\Users\Will\Projects\Lobster_Construction_Lab
```

Double-click **`00_SETUP.cmd`**, then **`01_DEMO.cmd`**. The first creates only a project-local virtual environment; the second constructs a declared H010 example, checks every original edge independently and saves its evidence. Read `START_HERE.md` for exact PowerShell commands, optional libraries and the ChatGPT setup pack.

The core needs no third-party Python packages. Use 64-bit CPython 3.12 or 3.13. Linux/Python 3.12 was executed for release validation; Windows instructions and launchers have been reviewed but were not executed on Will's machine.

## What works now

| Component | Mathematical role | External dependency |
|---|---|---|
| `lcl/model.py` | Exact named profiles/graphs, tree/lobster validation, target identities | None |
| `lcl/constructors.py` | Caterpillar, L007, L010/H010; padded composition and zero-padding balanced two-section supplier | None |
| `lcl/allocation.py` | Constructive R226 two-host completion for an independently fixed core | None |
| `lcl/search.py` | Bounded exact DFS with explicit restrictions and no hidden root/alpha assumption | None |
| `lcl/dp.py` | Exact frontier counts retaining label mask, difference mask and frontier values | None |
| `lcl/verify.py` | Separately implemented original-target certificate and partial-state checker | None |
| `lcl/oracle.py` | Direct permutation enumeration for small independent comparisons | None |
| `lcl/states.py` | Shifted interval/physical-port boundary and explicitly exploratory B2 extraction | None |
| `lcl/records.py`, `experiments.py` | Immutable attempts, source snapshots and bounded case-level resume | None |
| `lcl/engines.py` | Optional SMT existence check, topology diagnostics, exact symbolic identities | Z3 / NetworkX / SymPy only when selected |

The padded baseline is a newly written implementation and reviewed corollary of retained L010 formulas. A second, independently derived formula now removes the direct-leaf padding for the balanced family: equal positive terminal counts at the two branched sections, with arbitrary positive path length. Its proof is `research/B2_BALANCED_SUPPLIER.md`. Neither result is a universal lobster construction or a historical novelty claim. All construction domains and returned states appear in `docs/CONSTRUCTION_IMPLEMENTATION.md`.

## First scientific direction

Study two consecutive branched sections followed by a path. The padded retained composition and the new zero-padding balanced supplier give explicit comparison baselines. The next target is the smallest unequal pair of branch sizes, using a bounded fixed-prefix seed question and a proved label-shift template. See `research/NEXT_TASK.md` for the exact single task and `STATE.md` for its current disposition.

The four-pair diagnostic in `configs/b2_pilot.json` is intentionally small. Its two first cases use the same tree and different return intervals, exposing the distinction between a failed boundary prescription and a nongraceful tree. A solver-produced prefix stays finite exploratory evidence until an independent construction and quantified proof exist.

## Where each kind of information lives

| Need | Authoritative file |
|---|---|
| Current objective and one next action | `STATE.md` |
| Precise research target, milestones and stop criteria | `docs/RESEARCH_PLAN.md` |
| Definitions, profiles, interfaces, counting convention | `docs/MATHEMATICS.md` |
| Accepted retained/project findings | `research/FINDINGS.md` |
| Failed hypotheses and adverse controls | `research/FAILED_HYPOTHESES.md` |
| Open and discharged proof duties | `research/PROOF_OBLIGATIONS.md` |
| Method choices, costs and primary sources | `docs/METHOD_SELECTION.md`, `docs/SOURCES.md` |
| Current literature overlap and inspection limits | `docs/LITERATURE_UPDATE.md` |
| Commands, limits, cancellation and recovery | `docs/OPERATIONS.md` |
| Dependencies, compatibility, troubleshooting | `START_HERE.md`, `docs/DEPENDENCIES_RESEARCH.md` |
| Agent work and algorithm-change rules | `AGENTS.md`, `research/DECISIONS.md` |
| Source copies and pinned provenance | `references/`, `UPSTREAM_NOTICE.md` |
| Executed validation and limitations | `evidence/validation/VALIDATION_REPORT.md` |
| ChatGPT Project instructions/context/kickoff | `chatgpt_project/` |

Run `python -m lcl --help` for the command list. The software does not schedule itself or run an indefinite campaign. A new ChatGPT Project must be created manually from the supplied pack; GitHub synchronization and cross-agent handoff are described in `docs/REPOSITORY_CONTINUITY.md`.
