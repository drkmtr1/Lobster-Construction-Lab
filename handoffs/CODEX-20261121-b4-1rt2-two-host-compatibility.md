# Continuity handoff for B4-1RT2-TWO-HOST-COMPATIBILITY-001

- Date: 2026-11-21, Pacific/Honolulu.
- Repository and branch: drkmtr1/Lobster-Construction-Lab, main.
- Accepted parent: `eb5745483186287b20bcf155cf4e5265dbfc20a5`.
- Checkpoint: resolve the commit containing this handoff via Git.
  The external closeout supplies verified local and actual remote
  main identities, status and preserved baseline tag.

## Research disposition

**ACCEPT** conditional finite-interleaving compatibility of
minimum-high and zero-host insertions with both supplied hosts
and the same named ports and witness. The
[compatibility proof](../research/ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md)
and [family proof](../research/B4_1RT2_TWO_HOST_COMPATIBILITY.md) give normalized
A(r+t+12,r+6;1,1) on `[[1],[r],[t],[2],[]]` for exact
r>=3,t>=4, and ordinary completion for K>=2 with
R=[r+6,r+K+5], D=[1,K], physical s:4=r+K+7.
The retained cases give ordinary gracefulness of the exact
(1,r,t,2) family over positive r,t at K>=2. The
flat third-terminal formula is rejected for its collision
at index 3. The K=1 corner r>=3,t>=4 remains open.

## Work and checks

[Evidence](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/README.md)
checks four retained normalized controls, three new prefixes
and four new completed targets. Twelve invalid triples were
rejected before expansion. The arithmetic audit rechecks the
same eleven graph records and five route and subdivision
comparisons. The limits were one worker, 27 vertices and
2,000,000 bytes per result. The run used zero solver queries,
enumeration or historical replays.

Separate read-only AI mathematical and evidence reviews accepted.
The mathematical reviewer requested a formatting correction
before proof-byte capture. The frozen prior evidence is unchanged.
The additive [reproduction erratum](../docs/REPRODUCTION_ERRATA.md#b4-1r32-k1-rooted-core-001)
corrects only the prior checkout instructions. The new task's
evidence README specifies its own required parent and fresh outputs.

Production and upstream paths were preserved. The public LCL
repository is the authorized publication target. Verify baseline
tag object fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d and peeled commit
36ea1603602491bf3c1c5b81ed4c23aaa2210e70.

## One next action

**With a new bounded scope decision, prove a direct singleton supplier for `[[1],[r],[t],[2],[],[]]` with exact integers `r>=3,t>=4`**, using the accepted ordinary maximum-rooted cores and preserving physical `s:4` and both inventories.
