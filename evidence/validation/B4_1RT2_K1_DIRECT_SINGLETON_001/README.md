# 1RT2 direct K=1 singleton evidence

Run identity `B4-1RT2-K1-DIRECT-SINGLETON-001-20261121`

| Checked records | Parameters | Orders |
|---|---|---|
| Retained cores | r=3,4,5 | 15,16,17 |
| Retained completed control | (r,t,K)=(3,3,1) | 19 |
| New completed targets | (3,4,1), (3,5,1), (4,4,1), (5,6,1) | 20,21,21,24 |

Eight graph records passed the unchanged original-target checker.
The new originals were saved and digested before labeling. Each
completed certificate binds its retained core and records the
direct prefix, both exact complements, physical active port,
original final assignment, and the full ordinary cut spectra.
The first complete target records all nineteen actual differences.

The one-batch and two-unit-batch comparisons reuse the `(3,3,1)`,
`(3,4,1)` and `(3,5,1)` records. Eight invalid pairs failed
before graph expansion. One altered expected digest was rejected
on the existing `(3,4,1)` original. The independent arithmetic
audit rechecks the same records and adds zero cases. The run used
one worker, a cap of 24 vertices per graph and 2,000,000 bytes per
result, and zero solver queries, labeling enumeration or historical
replays.

## Reproduction in a disposable parent checkout

Use the corrected [parent-checkout procedure](../../../docs/REPRODUCTION_ERRATA.md)
with this task's own paths.

1. Identify the commit containing this bundle, for example with
   `git log --diff-filter=A --format=%H -- <path-to-this-README>`
   on or after publication.
2. Create a disposable checkout at the recorded parent
   `3e10c022f834cfae053aaef9581697bf6c21002d`. Copy the exact Git
   blobs for `research/B4_1RT2_K1_DIRECT_SINGLETON.md`
   and this evidence directory's `config.json`, `validate.py`
   and `audit.py` to their original paths without advancing HEAD.
   Capture the bytes of `git show <checkpoint>:<path>` with a
   byte-capable tool such as Python subprocess and pathlib.
3. Leave this task's `validation/` directory and
   `audit_result.json` absent. Keep the archived bundle intact.
4. From the checkout root, use [project-local Python](../../../docs/OPERATIONS.md)
   and run the saved [commands](commands.json) in order, one saved
   command per PowerShell process because each ends in
   `exit $LASTEXITCODE`. The validator checks HEAD and creates
   the output directory exclusively. The audit reads the saved
   records and writes its receipt exclusively.

The [identity](validation/identity.json) binds source, code, configuration,
proof, runtime, and retained records. Source snapshots preserve observed
execution bytes. Source comparisons to the parent may normalize CRLF to
LF. The [manifest](MANIFEST.json) binds raw bytes without normalization.
The [summary](validation/summary.json), [growth comparison](validation/growth.json),
[adverse check](validation/adverse.json), [audit](audit_result.json)
and [reviews](REVIEWS.md) preserve the finite outcomes. The
[proof](../../../research/B4_1RT2_K1_DIRECT_SINGLETON.md) supplies the quantifiers.
