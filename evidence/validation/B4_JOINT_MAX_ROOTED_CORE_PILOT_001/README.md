# Bounded joint maximum-rooted core pilot

The exact named [joint original](validation/core_original.json)
has profile `[[2],[2],[],[2],[],[]]` and is preserved before
the [first-witness query](validation/query_started.json).
The unchanged DFS reached 100,000 assignment nodes in about
0.774 seconds and returned [INCOMPLETE](validation/raw_query.json).
The only pin is physical s:2=14. There were no extra domains
or exact counting, no retry and no historical replay.

The two [retained control ledgers](validation/controls.json)
include every original edge, the unchanged checker receipts,
and complete crossing weights for both hosts on their respective
originals at cuts c=0..14 including two endpoint comparisons.
The [independent arithmetic audit](audit_result.json) reconstructs
the named graphs and calculates the crossing spectra by edge
contribution over each straddled cut. It runs no search.
The three graph records are the two retained controls and
the joint original. No completed t=2 graph was supplied.

The [execution identity](validation/identity.json) records raw
runtime source hashes, raw retained reference hashes, and task
input hashes. Comparisons of production source snapshots to the
parent normalize CRLF to LF. The DFS library serializes its
default max_states=20,000, a field unused by DFS. The raw
budget and search snapshots retain their inherited trailing
blank lines through narrowly scoped whitespace attributes.
The actual DFS caps are 15 vertices, 100,000 nodes and six
cooperative seconds.
The conditional completed checker cap is order 18. Each result
has a 2,000,000-byte write cap.

## Reproduce in a disposable parent checkout

1. Locate the commit adding this README with
   `git log --diff-filter=A --format=%H -- <this-README-path>`.
2. Make a disposable checkout at `f67418a57906f4f37b3d20d12a800373db571e0a`.
   Copy the exact Git blobs for this directory's `run.py`,
   `audit.py`, `config.json` and `commands.json` to the same paths
   without advancing HEAD. Use byte-preserving extraction.
3. Leave `validation/` and `audit_result.json` absent.
   From the repository root use [project-local Python](../../../docs/OPERATIONS.md)
   and the [saved commands](commands.json) in separate PowerShell
   processes in the recorded order. The run opens a fresh output
   directory and writes a named start marker before solving.
4. Preserve the published results. A reproduction is a separate
   execution and has its own cooperative timing receipt.

[Proof and scope](../../../research/B4_JOINT_MAX_ROOTED_CORE_PILOT.md) ·
[Command receipts](command_receipts.json) ·
[Separate AI reviews](REVIEWS.md) · [Manifest](MANIFEST.json)
