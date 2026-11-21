# B3-UNPADDED-Q1-R2-001 handoff

This bounded task was completed November 21, 2026, Pacific/Honolulu, on local `main`. The starting accepted revision was `e74285d893408b5474319bcfcbe6aad2fd1297a3` with a clean tree and locally recorded `origin/main` at `23ab238149fab5ddd05cee60a649fa4c21752dbc`. Resolve the new local checkpoint by the Git revision that introduced this handoff. The user authorized a local commit. The baseline tag and the three earlier B3 commits are preserved.

## Accepted result

For fixed q=1,r=2 and integers `t>=3,K>=2`, the direct alpha seed in `research/B3_UNPADDED_Q1_R2.md` labels the original prefix of `[[1],[2],[t]]+[[]]*(K+1)` at zero padding. The fixed `t=1` seed also derives the formula by prescribed leaf attachment at the least-high `b:2:0`. The high-side shift leaves `R=[a,a+K-1]`, `D=1..K` and physical port `s:3=a+K+1` with `a=t+4`. The retained nonadjacent recurrence completes the original path.

For positive integers q,r,t and K>=2, the deterministic selection is the q>=r branch, the q<r and t<=q+1 branch, the q<r and t>=q+2 and r>=3 branch, or the exceptional q=1,r=2,t>=3 branch. All four domains are disjoint and exhaust the exact zero-padding family. The adjacent branch retains its adjacent port and K=1 domain. The other K=1 cases, padding, multiple positive branches per section, further sections, and arbitrary repetition are separate.

## Review and evidence

Separate AI reviewers accepted the mathematical proof and implementation. The explicit base-prefix certificate passed once on the original 11-vertex, 10-edge graph and was recorded separately. All 12 declared original completed targets passed seed, prefix and full certificate checks. The separate arithmetic audit passed on the same 12 saved targets. The 41 targeted methods, CLI fixture and retained demo passed. Commands, runtime, configuration, snapshots and results are in `evidence/validation/B3_UNPADDED_Q1_R2_001/`. See D026 and the authoritative findings and proof duties.

## One next action

**With a new bounded scope decision, formulate a `K=1` construction question for the original unpadded three-section family with `q>=r>=1,t>=1`**, retaining the named graph and the original edge from `s:3` to `s:4`.
