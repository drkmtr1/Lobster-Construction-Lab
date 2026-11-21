> **Local adoption record — November 21, 2026, Pacific/Honolulu.** Adopted from the independent external B2 review pack into this project's authoritative records by the bounded integration task `OC-20261121-b2-review-integration`. The body below is the pack note **verbatim and unmodified** (the pack note's title line is retained as this file's single title; its original status line — "It has not been written into Will's local authoritative research records" — describes the pack's state at review time and is superseded by this header).
> **Source:** `evidence/reviews/B2_UNEQUAL_SEED_001/pack/B2_INTERFACE_OBSTRUCTION.md` — 7038 bytes, raw SHA-256 `1234e5336d26ffc4aabb17f92e5b64d15aa63e2f9d54f7c8fcd934cc16df8f6f`, byte-verified against the pack's `MANIFEST.json` (checks F1/F2 of `evidence/reviews/B2_UNEQUAL_SEED_001/verification_result.json`).
> **Adoption check (this session):** before adoption, the integration session re-derived the argument step by step in its own notation and confirmed all six proof steps (extreme-label forcing, interval bounds, block spans, edge crossing for K>=6, the connected 4/4 coloring forcing ell=4, compression, and both port cases including the complement). The pack records two further separate agent challenges; their notes are preserved at `evidence/reviews/B2_UNEQUAL_SEED_001/pack/analysis/math_review.md` and `evidence/reviews/B2_UNEQUAL_SEED_001/pack/analysis/next_step_review.md`.
> **Status:** PROVISIONAL_INTEGRATION_PENDING_CODEX_REVIEW — a reviewed proof note adopted into the records; not yet an independently accepted project theorem, not external peer review, and not a formal certificate.
> **Scope limits (as adopted):** the threshold 6 is sufficient, not claimed sharp; K=1..5 are undetermined; this is an obstruction to the particular returned interface at the exact eight-vertex prefix — not a nongracefulness proof for the full tree, for any other family, or for any other restriction set; the balanced `q=r` supplier and the padded construction (different parameter domains) are unaffected. The full scope discussion is in the section "Scope and practical consequences" below.

# B2 unequal-family interval-interface obstruction

**Review date:** November 21, 2026, Pacific/Honolulu.  
**Status:** new analytic deduction from this acceptance review; independently challenged by two separate reasoning agents. It is not an OpenChamber run result, a proof-assistant certificate, an external peer review, or a historical novelty claim. It has not been written into Will's local authoritative research records.

## Plain-language meaning

The completed seed test rules out one small labeling arrangement. The argument below shows why that failure matters beyond the small test. Once the unfinished path has at least six edges, the proposed division of labels and edge differences forces the prefix back into exactly the small arrangement that was proved impossible.

Consequently, allowing the constructor to choose a different interval position or switch above/below cannot rescue this particular interface for every path length. The broader search for graceful labelings can continue through a different interface or construction.

## Exact claim

Let `q=1`, `r=2`, `z0=z1=0`, and let `K>=6` be an integer. The original B2-P1 tree has profile

```python
[[1], [2]] + [[] for _ in range(K + 1)]
```

It has `m=K+7` edges. Its prefix through the physical vertex `s:2` is the eight-vertex graph `[[1],[2],[]]`, with these seven original edges:

1. `s:0 -- s:1`
2. `s:0 -- b:0:0`
3. `b:0:0 -- l:0:0:0`
4. `s:1 -- b:1:0`
5. `b:1:0 -- l:1:0:0`
6. `b:1:0 -- l:1:0:1`
7. `s:1 -- s:2`

There is **no** injective prefix labeling `f` in the final alphabet `0..m` satisfying all of the following, for any integer `ell`:

- The unused labels are exactly `[ell, ell+K-1]`.
- The seven prefix-edge differences are distinct and exactly `K+1..K+7`, equivalently the unused differences are `1..K`.
- The physical port satisfies `f(s:2)=ell+K` or `f(s:2)=ell-1`.

No alpha condition is assumed in this claim. No root label is pinned. Both interval sides and every allowable interval position are included.

## Dependency: the reviewed seed obstruction

The supplied `research/B2_UNEQUAL_SEED.md` proves nonexistence of a graceful seed with

\[
A=\{s:1,b:0:0,l:1:0:0,l:1:0:1\}\longrightarrow\{0,1,2,3\},
\]

\[
B=\{s:0,b:1:0,l:0:0:0,s:2\}\longrightarrow\{4,5,6,7\},
\]

and `h(s:2)=4`. Each map is bijective. The analytic proof and the current review's independent enumeration of all 144 permitted named assignments confirm this exact negative. The minor degree-list typo and historical scratch diagnostic do not affect the proof.

## Proof

**1. Both extreme labels must already be used.** The prefix differences include the maximum possible difference `m=K+7`. In the alphabet `0..m`, only labels `0` and `m` have difference `m`. Both must therefore occur on prefix vertices. Neither can belong to the unused interval. Consequently

\[
1\le\ell\le7.
\]

**2. The assigned labels form two short blocks.** Since exactly the `K` interval labels are unused, the eight assigned labels are precisely

\[
L=[0,\ell-1],\qquad H=[\ell+K,K+7].
\]

Both blocks are nonempty. Their spans are `ell-1` and `7-ell`, respectively, each at most six. Their cardinalities are `ell` and `8-ell`.

**3. Every original prefix edge must cross between the blocks.** An edge whose endpoint labels lie in the same block has difference at most six. Every prefix difference is at least `K+1>=7`. Therefore no prefix edge can have both endpoint labels in one block.

This is the crucial step: alpha separation follows from the resource requirements and `K>=6`; it has not been imposed as an additional search restriction.

**4. The interval position is forced.** The connected prefix has bipartition classes `A` and `B` above, both of size four. A connected graph's two-coloring is determined, up to exchanging its two classes, by the color of one vertex: propagate the opposite color across each edge. Thus the vertices receiving `L` are either exactly `A` or exactly `B`.

There must be four labels in each block, giving

\[
\ell=4.
\]

**5. Compress the gap.** Define a labeling on the same eight physical vertices by

\[
g(v)=
\begin{cases}
f(v),&f(v)\in L,\\
f(v)-K,&f(v)\in H.
\end{cases}
\]

The low labels become `0..3`; the high labels become `4..7`. Every edge crosses between them. Hence each original difference decreases by exactly `K`, and the seven differences become exactly `1..7`. Thus `g` is a graceful alpha labeling of the original seed graph.

**6. Both permitted port sides contradict the seed obstruction.**

- **Above:** `f(s:2)=ell+K=K+4`, so `g(s:2)=4`. Because the physical vertex `s:2` belongs to `B`, `B` is the high class and `A` is the low class. This is exactly the forbidden seed.
- **Below:** `f(s:2)=ell-1=3`, so `g(s:2)=3`. Now `B` is the low class and `A` is the high class. Complement every label by `h(v)=7-g(v)`. This preserves every absolute edge difference, makes `A` low and `B` high, and gives `h(s:2)=4`. Again this is exactly the forbidden seed.

Both cases are impossible. This proves the claim.

The complement in the second case is a proof map from a hypothetical witness to a forbidden witness. It is not an enumeration quotient and does not identify different named assignments in any count.

## Scope and practical consequences

- This is an obstruction to the **particular returned interface** at the exact eight-vertex prefix. It is not a nongracefulness proof for the full tree.
- The argument covers every `K>=6`. Six is a sufficient threshold; no claim of a sharp threshold is made.
- It does not determine the interface for `K=1,...,5`; the earlier positive `K=1` pilot is consistent with it and need not be rerun.
- It does not impose an initial alpha assumption. Removing an alpha flag alone cannot evade the conclusion while keeping the other interface requirements for `K>=6`.
- Relabeling the prefix, changing `ell`, or exchanging above/below cannot evade the conclusion if the final state still satisfies these same conditions.
- The balanced `q=r` supplier and padded construction have different parameter domains and remain unaffected.
- The exact objective “supply this interval/adjacent-port state for every positive `K` when `q=1,r=2,z0=z1=0`” is impossible. A revised construction objective must change at least one interface requirement or the boundary at which the prefix is returned.

One possible future relaxation is to keep the interval and difference set but allow a port farther outside the interval, accompanied by a new path-consumer proof and an explicit parameter domain. This report neither proves that consumer nor assumes a matching seed exists.

## Independent review

Two separate reasoning agents read the supplied arguments and challenged the new deduction. Both confirmed the extreme-label argument, interval bounds, block spans, connected `4/4` coloring, compression, and both port cases. Their complete notes are in `analysis/math_review.md` and `analysis/next_step_review.md`. This is separate agent review within this session, not external mathematical peer review.
