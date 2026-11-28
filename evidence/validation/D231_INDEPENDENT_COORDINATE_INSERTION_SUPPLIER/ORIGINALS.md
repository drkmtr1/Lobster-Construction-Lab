# D231 — Independently specified named graphs

For a profile with four sections, create spine vertices s:0 through s:3, branch b:i:a for each zero-based entry a in section i, and exactly its declared number of terminals l:i:a:e in increasing zero-based index e. The original T has edges between consecutive spine vertices, from s:i to each b:i:a, and from b:i:a to each l:i:a:e. The fold S replaces only s:0--b:0:0 by s:1--b:0:0 and s:3--b:3:0 by s:2--b:3:0. Spine reversal changes the section index i to 3−i and keeps all other indices. This defines the two graphs independently of rows, labels and discovery.

## Prescribed hand controls

Both controls use h=10, ℓ=2, j=15, pairs 1 and 9 on the left, pairs 2 through 8 and slots 10,11,12 on the right. The h=6 source used for normalization checks is fixed at F=11 and S2. Slots and reserves at h=10 use the accepted D230 marking. Left exterior b:0:0 is L1, left interiors b:1:0 and b:1:1 are H1,L9, and right exterior b:3:0 is L10. For each list below, its order fixes the indexed right interior roles b:2:0 through b:2:14.

| Control | Ordered profile | Ordered right interior roles |
|---|---|---|
| Sparse Q=9 | `[[1],[1,1],[9,9,1,1,1,1,1,1,1,1,1,1,1,1,1],[1]]` | L3,H3,L2,L4,H2,H4,L5,L6,L7,L8,L12,H5,H6,H7,H8 |
| Independent (7,3,19,5) | `[[7],[7,1],[3,19,5,3,19,5,1,1,1,1,1,1,1,1,1],[1]]` | L2,L3,L4,H2,H3,H4,L5,L6,L7,L8,L12,H5,H6,H7,H8 |

## Canonical named graphs for any later authorized finite-key diagnostic

A numerical placement is an ordered pair-quota tuple (q₁,q₂,q₃,q₄). Its canonical named profile at h=10 is
```text
[[q1],[q1,1],[q2,q3,q4,q2,q3,q4,1,1,1,1,1,1,1,1,1],[1]].
```
The role order is the independent-insertion control order above, regardless of the returned row ordering. Original T and fold S use the declared incidence construction. Equal values within the tuple do not distinguish extra numerical placements. Different placements are numerical tests, irrespective of whether physical tree shapes coincide. A positive at any placement discharges its numerical aggregate key. This is a check of exact finite return and one named reconstruction, with no redefinition of the original and no test of unmarked gracefulness.
