# 1RT2 two-host validation

Run identity `B4-1RT2-TWO-HOST-COMPATIBILITY-001-20261121`

## Checked records

| Record | Parameters in run order | Orders |
|---|---|---|
| Retained normalized controls (r,t) | (2,3), (5,3), (2,4), (2,5) | 17, 20, 18, 19 |
| New normalized prefixes (r,t) | (3,4), (3,5), (5,5) | 19, 20, 22 |
| New completed targets (r,t,K) | (3,4,2), (3,4,3), (3,5,4), (5,5,5) | 21, 22, 24, 27 |

Eleven graph records passed, seven of them new. The (3,4) completions
share one hash-bound normalized prefix. Twelve exact-type and range
probes were rejected before graph construction. The validator and
independent arithmetic audit add zero solver queries, enumeration,
or historical replay. Five route and subdivision comparisons reuse
the saved prefix/control states, and the audit adds zero cases.
One worker, order at most 27 and 2,000,000 bytes per result bound
the campaign.

## Reproduce in a disposable parent checkout

1. Verify the commit containing this bundle. In a checkout on or after
   publication, `git log --diff-filter=A --format=%H -- <path-to-this-README>`
   identifies the introduction commit. Resolve it before moving into the
   disposable checkout.
2. Create a disposable checkout at the validator's required parent,
   `eb5745483186287b20bcf155cf4e5265dbfc20a5`. Copy the exact
   blobs for the following paths from the introduction commit into
   that checkout without advancing its HEAD.
   - `research/ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md`
   - `research/B4_1RT2_TWO_HOST_COMPATIBILITY.md`
   - This directory's `config.json`, `validate.py`, and `audit.py`.
3. Leave this task's `validation/` directory and `audit_result.json`
   absent. Preserve the archived evidence separately. Extract raw Git blobs
   with a byte-capable method, such as Python's subprocess and pathlib.
4. From the checkout root, use the
   [project-local Python](../../../docs/OPERATIONS.md) for the PowerShell
   [commands](commands.json) in order, one saved command per PowerShell
   process because each ends with `exit $LASTEXITCODE`. The validator
   checks HEAD and uses exclusive output creation. The audit reads the new validation records
   and writes `audit_result.json` exclusively. Both use UTF-8 mode.

The [identity record](validation/identity.json) hashes the configuration,
scripts, both proofs, retained certificate/original pairs and source
snapshots. The snapshots preserve exact execution bytes. Source
comparisons permit CRLF-to-LF normalization while recorded hashes and the
[evidence manifest](MANIFEST.json) use raw bytes. A replay on a checkout
with different line endings may produce different snapshot or run-output
hashes. It must verify the same scoped arithmetic and record identities.
The parent states.py ends with a blank line. The snapshot retains it
byte-for-byte and its path-specific Git attribute allows that final blank line.

The [summary](validation/summary.json), [routes](validation/routes.json),
[audit](audit_result.json), and [reviews](REVIEWS.md) preserve the
finite results and limits. The [family proof](../../../research/B4_1RT2_TWO_HOST_COMPATIBILITY.md)
and [compatibility proof](../../../research/ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md) carry the quantifiers.

The [prior task erratum](../../../docs/REPRODUCTION_ERRATA.md#b4-1r32-k1-rooted-core-001)
corrects that task's checkout instructions additively.
