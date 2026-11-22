# B4-UNPADDED-111T-001 continuity handoff

Completed November 21, 2026, Pacific/Honolulu, on `main` of
`drkmtr1/Lobster-Construction-Lab`. The accepted base and parent of this
handoff checkpoint is `294f415df2a53f13161b56d5888ed4b0c118f7a0`.
Identify the new checkpoint by the Git commit introducing this handoff.
The closeout session report supplies its exact local and remote SHAs.

## Catch-up synchronization

Before research, the clean local branch was six commits ahead of the
fetched GitHub `main` at `23ab238149fab5ddd05cee60a649fa4c21752dbc`.
The six evidence manifests and 487 changed evidence files were checked
against their hashes and tracked Git bytes. Seven ignored completed run
directories matched frozen tracked evidence, and the extracted closeout
packet matched its committed archive byte for byte. The separate Q8
maintenance packet is outside this project's evidence. No required
artifact was missing. Historical checkers were left to their preserved
records. A normal fast-forward published the six commits, with actual
`refs/heads/main` verified at `294f415df2a53f13161b56d5888ed4b0c118f7a0`.
All six were verified in its ancestry:

- `aac7f84dc8d2c3518248e8aeae109ec23decbbae`
- `db72b4dc45510c830c582bc994543d539c223a13`
- `e74285d893408b5474319bcfcbe6aad2fd1297a3`
- `a1e8a15de2f33c5de877a941612c657a62d48747`
- `a5a58fe1ad2b58e93ea1a4dc9a74d956973adcad`
- `294f415df2a53f13161b56d5888ed4b0c118f7a0`

The remote and local `lcl-v0.1.0-baseline` tag peeled to
`36ea1603602491bf3c1c5b81ed4c23aaa2210e70`. No tag was moved.

## Accepted finding and evidence

See `STATE.md`, D029 and `research/B4_UNPADDED_111T.md`. For integers
t>=2 and K>=1, the explicit constructor gives a graceful labeling on
exactly `[[1],[1],[1],[t]]+[[]]*(K+1)` with zero padding. At K=1
`s:4=t+7` consumes singleton resources `R={4}`, `D={t+3}` along the
original final edge, giving an alpha labeling with low-class size t+6.
For K>=2 the prefix has `R=[t+5,t+K+4]`, `D=[1,K]`, and
`s:4=t+K+6`; the retained nonadjacent consumer completes the original
path. The original unit construction covers t=1 with its adjacent
alpha contract. Separate mathematical and implementation AI reviews
both accepted. The CLI graph ceiling is t+K<=9988, with the existing
record byte limit applied separately.

`evidence/validation/B4_UNPADDED_111T_001/` freezes original targets,
configurations, source, runtime, certificates, audits, reviews, exact
commands and SHA-256 manifest. The bounded campaign used one worker,
75 vertices and 2 MB per result. It passed all 12 declared original
targets. The audit retry passed on those same saved targets and the
earlier order-sensitive audit attempt is preserved. Two left
component certificates, 53 targeted test methods, both CLI examples
and the retained demo passed separately. No solver search, enumeration
or expanded target campaign was used. No provisional claim is promoted.
Proof duties for other sizes among the first three branches, padding,
multiple branches, further sections and arbitrary repetition remain
in `research/PROOF_OBLIGATIONS.md`.

## One next action

**With a new bounded scope decision, formulate a construction question for the exact unpadded `[[1],[1],[2],[1]]+[[]]*(K+1)` profile with integer `K>=1`**, retaining the physical `s:4` and both resource inventories.
