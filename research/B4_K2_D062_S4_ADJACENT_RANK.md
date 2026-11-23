# B4-K2-D062-S4-ADJACENT-RANK-001

**EXHAUSTED RESTRICTED NEGATIVE.** Both prescribed adjacent swaps and
both suffix orders fail on the retained named original. The validator
and the independent arithmetic audit checked the full grid of 684
distinct named assignments at q=r=t=K=2.

## Exact model

The [frozen pre-execution argument](../evidence/validation/B4_K2_D062_S4_ADJACENT_RANK_001/pre-run.md)
derives the 17 named prefix ranks from D062, binds the original, proves
uniqueness of the 684 maps, and checks the two physical suffix edges.
Only the exchanges (9,10) for L and (10,11) for R are included.
No edges or physical roles are changed. The argument using differences
18 and 17 excludes 51 hole pairs per template, including the distinct
ports for R={0,18}. Every excluded pair was still checked in both orders.

## Results and the only valid prefix

| Template | Hole pairs | Full cases | Prefixes repeating a difference | Valid prefixes | Graceful completions |
|---|---:|---:|---:|---:|---:|
| L | 171 | 342 | 170 | 1 | 0 |
| R | 171 | 342 | 171 | 0 | 0 |

For the sole valid prefix in L, R={11,12} and physical s:4 has label 9.
The assigned weights are [2,6] and [8,18], leaving D={1,7}.
Both orders give final weight 1 on s:5--s:6. On the original first
edge s:4--s:5, the weights are 2 and 3 respectively. Neither provides
7. Every other L prefix is already invalid on the assigned original
edges. The named ledger and exact missing and repeated multiplicities
for each complete case are retained in the [raw evidence](../evidence/validation/B4_K2_D062_S4_ADJACENT_RANK_001/README.md).

## Structural reason template R always repeats

Let x_i be the retained label at zero-based rank i. A hole is in internal
gap g if x_g is below it and x_(g+1) is above it. An edge with endpoint
ranks i<j has difference j-i plus the number of the two holes in gaps
i through j-1. Holes outside the retained extremes contribute nothing.
Template R has three assigned edges of rank span seven:

| Edge | Endpoint ranks | Internal gaps counted |
|---|---|---|
| E = s:3--s:4 | 4, 11 | [4,10] |
| F = b:0:0--l:0:0:1 | 2, 9 | [2,8] |
| G = b:3:0--l:3:0:0 | 5, 12 | [5,11] |

For these three weights to be distinct, the hole counts must be 0, 1, 2
in some order. The following named gap constraints exhaust that condition.

- If E counts both holes and F counts none, both gaps lie in {9,10}
  and G also counts both. If E counts both and G counts none, both
  gaps equal 4 and F also counts both.
- If F counts both and E counts none, both gaps lie in {2,3} and G
  also counts none. If F counts both and G counts none, the gaps are
  in {2,3,4}. E counts exactly one only with one gap at 4 and the
  other at 2 or 3. Then F weighs 9, and s:3--b:3:0 has rank span
  8 and counts the hole at 4, giving a second weight 9.
- If G counts both and E counts none, both gaps equal 11 and F also
  counts none. If G counts both and F counts none, the gaps are in
  {9,10,11}. E counts exactly one only with one gap at 11 and the
  other at 9 or 10. The edge b:0:0--l:0:0:0 has rank span 8 and
  counts gaps [2,9]. With gap 9 it weighs 9, duplicating G.
  With gap 10 it weighs 8, duplicating E.

Thus every hole pair gives a repeated assigned difference in R.
This explanation uses the actual fixed ranks and named edges. The
full case check provides separate bounded evidence for the same claim.

## Scope

**ACCEPT** the complete model, original identities, resource audit,
and the top-difference obstruction on 51 pairs per template.
**REJECT** both exact alternate rank models on this original.
Ordinary gracefulness of the tree, other rank orders, and a wider
K≥2 supplier remain open here. The D062 construction and the
earlier scoped D063 and D064 results retain their stated domains.
