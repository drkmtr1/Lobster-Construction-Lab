# 1342 relaxed-host bounded seed experiment

Run identity `B4-1342-RELAXED-HOST-SEED-001-20261122`

**EXHAUSTED RESTRICTED NEGATIVE** for the named 1342 original
with low labels [0,8], high labels [9,18], physical b:2:0=0,
s:4=10, a=g(b:0:0) in 2..8 and c in 11..18, requiring the full
selected incidence spectrum [c-a,18]. The independent
[presearch review](presearch_review.json) accepted the necessary
prefilter and edge-band equivalence before labeling search.
The [prefilter receipts](validation/prefilter.json) preserve every
one of the 56 pairs and the reason for each of the 33 exclusions.

All 23 admitted pairs and their 68 named subset stages exhausted.
The shared budget consumed 13,171 assignment nodes and
1.1086707999929786 seconds. There were no interrupted, unstarted,
limit or SAT statuses. Exact counting was disabled. The run
checked two retained graphs, 1342 and the 1122 positive control.
The latter supplies the exact spectrum [5,14]. There were no
new graphs, new graceful targets or historical replays. The
ten invalid parameter tests precede search. No positive
transport was promoted.

The [search summary](validation/search_summary.json) links the
original digest, limits, sources, prefilter and controls. The
`validation/pairs/` directory retains every pair start,
subset start and terminal event, and pair result. The
[arithmetic audit](audit_result.json) independently reconstructs
the named originals, admitted subset sets and receipt order,
counters, caps and identities. It adds zero solver calls,
labeling replays or graph cases. The audit checks custody and
arithmetic; the completeness claim also depends on the reviewed
task-local DFS and its [coverage proof](../../../research/B4_1342_RELAXED_HOST_SEED_RESULT.md).

## Reproduction in a disposable parent checkout

1. Identify the commit introducing this bundle with
   `git log --diff-filter=A --format=%H -- <this-README-path>`.
2. Create a disposable checkout at parent
   `bb7927bcf85d6d32b9bde5b1904c6b43ec6b6a8e`. Copy the exact Git
   blobs for `research/B4_1342_RELAXED_HOST_SEED.md`,
   `research/B4_1342_RELAXED_HOST_SEED_RESULT.md` and this directory's
   `config.json`, `presearch_review.json`, `seed_search.py`,
   `run.py` and `audit.py` to their recorded paths. Keep HEAD
   at the parent. Use a byte-capable Git extraction.
3. Leave `validation/` and `audit_result.json` absent in the
   disposable checkout. The published run stays frozen.
4. Use [project-local Python](../../../docs/OPERATIONS.md) from
   the repository root and the [recorded commands](commands.json)
   in order, each in a separate PowerShell process because it
   ends in `exit $LASTEXITCODE`. The run and audit create
   their outputs exclusively, and a replay has its own runtime
   and timing receipts.

The [runtime and source identity](validation/identity.json),
[separate reviews](REVIEWS.md) and [raw-byte manifest](MANIFEST.json)
preserve the exact published run. Source comparisons to the parent
allow CRLF-to-LF normalization. The recorded hashes use raw bytes.
