# Independent mathematical review of B2-UNEQUAL-SEED-001

## Disposition

**ACCEPT the restricted nonexistence theorem and the conditional transport argument. REVISE two descriptions of their supporting evidence.**

This review reads the actual supplied `research/B2_UNEQUAL_SEED.md`, the target/pin/domain/limits JSON files, `research/PROOF_OBLIGATIONS.md` section 3, and the supplied `b2_review_scratch.py`. It does not run the queued pin sweep, change the repository, or independently certify the original Windows execution environment. Enumeration and provenance are reviewed separately by the parent reviewer.

## Exact mathematical scope

The seven edges are exactly those listed in the supplied seed note. The low class is
`{s:1,b:0:0,l:1:0:0,l:1:0:1}` with labels `0..3`; the high class is
`{s:0,b:1:0,l:0:0:0,s:2}` with labels `4..7`. The only additional pin is `h(s:2)=4`.
The three supplied JSON inputs match this scope. Each listed edge crosses these classes. No branch exchange or complement quotient is used in the argument.

## Clean analytic proof

Write

- `a=h(s:0)`, `b=h(b:1:0)`, `c=h(l:0:0:0)`;
- `y=h(s:1)`, `x=h(b:0:0)`, `u=h(l:1:0:0)`, `v=h(l:1:0:1)`.

Every edge difference is high minus low. A difference of 1 can therefore only join the vertices labeled 4 and 3. The vertex labeled 4 is `s:2`, whose sole incident seed edge is `s:1--s:2`. Consequently `y=3`. Thus `a,b,c` permute `5,6,7`, and `x,u,v` permute `0,1,2`.

In original-edge order the seven differences are

`a-y, a-x, c-x, b-y, b-u, b-v, 4-y`.

Their sum is

`S = 2a+3b+c+4-3y-2x-u-v`.

The degrees are: high vertices `s:0` degree 2, `b:1:0` degree 3, `l:0:0:0` degree 1, `s:2` degree 1; low vertices `s:1` degree 3, `b:0:0` degree 2, and the two `b:1:0` leaves degree 1 each. Hence all coefficients and signs above are correct.

Substitute `y=3`, `u+v=3-x`, and `c=18-a-b`. Then

`S=a+2b-x+10`.

Gracefulness requires `S=1+...+7=28`, so `a+2b-x=18`.

If `b=5`, the equation requires `a-x=8`, impossible. If `b=6`, the only admissible solution is `a=7,x=1`. If `b=7`, the admissible solutions are `a=5,x=1` and `a=6,x=2`. Thus the complete list is

| `(a,b,c,x)` | Remaining low labels `{u,v}` | Difference multiset |
|---|---|---|
| `(5,7,6,1)` | `{0,2}` | `{1,2,4,4,5,5,7}` |
| `(6,7,5,2)` | `{0,1}` | `{1,3,3,4,4,6,7}` |
| `(7,6,5,1)` | `{0,2}` | `{1,3,4,4,4,6,6}` |

Both named assignments of the two remaining low labels are included in each row. Swapping those leaves merely swaps the last two corresponding edge values, so the multiset table is a proof covering both assignments, not an enumeration quotient.

In the first two rows, `s:0--b:0:0` and `s:1--b:1:0` both have difference 4. In the third row, `s:0--s:1`, `b:0:0--l:0:0:0`, and the `b:1:0` leaf edge ending at label 2 all have difference 4. Every possible graceful candidate therefore repeats a difference. No graceful labeling satisfies the declared restrictions.

This is an ordinary mathematical proof of restricted nonexistence. It is neither a proof-assistant result nor a nongracefulness proof for the unrestricted tree.

## Conditional all-K transport

For a hypothetical seed with the stated properties and any integer `K>=1`, retain labels `0..3` on the low class and add `K` to every high label. The used labels become `0..3` and `K+4..K+7`, all distinct and within `0..K+7`. Every original seed edge still joins a high and a low vertex, so its difference increases by exactly `K`. Hypothetical seed differences `1..7` therefore become `K+1..K+7`.

Exactly the interval `[4,K+3]` and the differences `1..K` remain unused. The physical port `s:2` has label `K+4`, exactly one above that interval. The only uncompleted edges are the original path edges from `s:2` through `s:(K+2)`.

For `a=4`, label the `j`th new path vertex by `a+(j-1)/2` when `j` is odd, and by `a+K-j/2` when `j` is even. Odd positions occupy the lower `ceil(K/2)` labels; even positions occupy the upper `floor(K/2)` labels. These intervals are disjoint and cover all remaining labels. For either parity the `j`th edge difference is `K-j+1`. Therefore all remaining labels and differences are used once, and the consumer terminates after exactly `K` steps. This includes `K=1`.

The proof is valid for every positive integer `K`. Finite tests are not needed to justify the quantifier. However, the stipulated seed does not exist. Consequently this gives no unconditional supplier for the unequal family and discharges no P07 independence obligation. The supplied note gives the correct disposition.

## Required reporting corrections

### 1. Misclassified vertex in a parenthetical degree explanation

In `research/B2_UNEQUAL_SEED.md` section 3, Step 3, the parenthesis says that `s:2`:1 is on the low side. It is on the high side. The displayed formula already incorporates it correctly as `+4`, so the calculation and conclusion are unaffected. Replace the parenthesis with the complete high/low degree listing given above. The unqualified claim that every descriptive detail is correct should be adjusted accordingly.

### 2. Supplied reviewer scratch retains the disclosed earlier identity-check error

The supplied `b2_review_scratch.py` compares `S` with `a+2*b-x+10` inside its loop over all 144 restricted assignments. That formula is valid only after imposing `y=3`; the unrestricted expression is `S=a+2*b-x-2*y+16`. The scratch file therefore still describes the initial faulty check disclosed in section 4. Its full enumeration of graceful candidates is logically independent of this diagnostic and remains correctly defined; its `y=3` per-case table and path-consumer formulas are also correct.

The note says a corrected run gave zero mismatches on the `y=3` slice, but that corrected code/output is not in this supplied scratch file. Preserve the earlier scratch as historical evidence, then supply a separately identified corrected check and its output, or explicitly identify the supplied script as the earlier version and rely on the new independent acceptance-review check. Do not silently rewrite the historical scratch and pretend it produced the original result.

## Remaining duty

Find an independently supplied state for the unequal family that meets a proved continuation interface, or revise the continuation theorem with an explicit valid domain. The accepted negative removes this particular alpha/physical-port template. It does not decide any other pin or restriction set. No queued successor was executed during this review.

## Appendix: independently challenged consequence proposed during acceptance review

**Origin:** the parent reviewer proposed this deduction during the present review. It is not an OpenChamber finding in the supplied checkpoint. This reviewer independently challenged its reductions, threshold, graph identity, and both port sides and found the argument valid. No successor experiment was run.

**Claim.** For the original `q=1,r=2,z0=z1=0` B2 family and every integer `K>=6`, the prefix consisting of the original eight vertices through `s:2` cannot return all three of the following:

1. Exactly the unused labels `R=[ell,ell+K-1]` within the full alphabet `0..K+7`.
2. Exactly the unused differences `D=1..K`.
3. The original physical port labeled immediately below or above that interval: `f(s:2)=ell-1` or `f(s:2)=ell+K`.

Here the prefix labeling is injective and its seven actual edge differences are pairwise distinct, as required of a partial graceful labeling. The claim allows `ell` and the boundary side to be outputs, and does not assume alpha separation in advance.

**Proof.** Suppose such a returned state existed. Let `m=K+7`. Since exactly `1..K` remain unused, the original seven prefix edges must realize exactly `K+1..K+7`. In particular an original prefix edge realizes difference `m`, which forces both labels `0` and `m` onto prefix vertices. Thus the unused interval contains neither endpoint, giving `1<=ell<=7`.

The eight used labels are precisely the two blocks

`L={0,...,ell-1}` and `H={ell+K,...,K+7}`.

Their spans are `ell-1` and `7-ell`, each at most 6. Since `K>=6`, every required prefix difference is at least `K+1>=7`. Therefore no original prefix edge can have both endpoints in either block. Every edge crosses `L/H`.

The original eight-vertex prefix is connected and has the unique bipartition (up to reversing its two classes) given by the declared low/high classes in the seed problem, each of cardinality four. Therefore the `L/H` cut assigns exactly four vertices to each block. As every used label is assigned once, `ell=4`.

Compress the upper block by subtracting `K` from every high label, leaving lower labels unchanged. This is a bijection from the eight assigned labels onto `0..7`. Every edge crosses the blocks, so each prefix difference decreases by exactly `K`, leaving exactly `1..7`. Thus the compressed prefix is a graceful alpha labeling of the same named graph.

If the port was above the unused interval, it had label `K+4`, so compression gives `h(s:2)=4`. Its physical bipartition class is consequently the high class, and the result is exactly the already-forbidden seed.

If the port was below the interval, it had label 3. Its physical bipartition class is then the low class. After compression apply the global complement `x -> 7-x`. This preserves all edge differences, makes the original physical class containing `s:2` the high class, and gives `h(s:2)=7-3=4`. Again the resulting labeling is exactly the forbidden seed. Complementation here proves an implication between hypothetical witnesses; it is not an implicit quotient of counted assignments.

Both cases contradict the accepted seed obstruction. Hence no such state exists for `K>=6`.

**Scope and consequences.** This excludes the specified original eight-vertex prefix/interface for all sufficiently long suffixes. It does not exclude graceful labelings of the full original tree, other prefix boundaries, noninterval resource inventories, different remaining-difference sets, or a different continuation rule. It also does not decide the cases `1<=K<=5`; the sufficient threshold 6 is not asserted to be sharp. A mere change of the interval position or its adjacent boundary side cannot supply the unchanged interface for every positive `K`.
