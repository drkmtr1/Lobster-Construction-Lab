# Independent review of the queued research direction

Review date: 2026-11-21. Reviewer role: next-step/interface audit. Files read: supplied `STATE.md`, `AGENTS.md`, `research/NEXT_TASK.md`, `research/B2_UNEQUAL_SEED.md`, `research/PROOF_OBLIGATIONS.md`, `research/B2_BALANCED_SUPPLIER.md`, plus relevant handoff and decision passages. No successor pin enumeration or experiment was performed. Supplied files were not edited.

## Verdict

**REVISE the queued pin-sweep plan as a route to an all-K supplier.** The completed p=4 obstruction and its conditional transport remain valid. A p=5/6/7 seed sweep is a well-defined finite diagnostic, but even a positive seed cannot satisfy the unchanged adjacent-port interface, and unchanged transport cannot work for every K>=1. The current plan needs a new continuation hypothesis before additional seed searches have a constructive purpose.

The exact duty is P05 (residual interval and adjacent active label), with consequences for P08 (continuation) and P09 (quantified domain). It is not a label-range failure under P03.

## 1. Why another port pin does not repair the same consumer

With the same alpha domains, shifting every high label by K still uses labels `[0,3]` and `[K+4,K+7]`. The unused labels remain `R=[4,K+3]` and the unused differences remain `D=[1,K]`, assuming a graceful seed. For a port pin p, however, the physical port becomes `a=K+p`.

P05 requires `a=K+4` (one above R) or `a=3` (one below R). For p in {5,6,7}, neither equation holds. The distance from a to the upper endpoint of R is `p-3`, namely 2, 3, or 4. Being somewhere above the interval is insufficient for the existing endpoint consumer.

The K=1 boundary makes this failure unavoidable for any claimed all-positive-K theorem: the only unused label is 4, the active port is p+1, and the unique suffix edge has difference `p-3`, not 1. This rules out every all-K completion using unchanged transport and prefix for those pins, independently of whether seeds exist.

More generally, if any such suffix completion exists, its first edge has difference at least `p-3`, so `K>=p-3` is necessary. This necessary condition does not prove completion for larger K, nor does it meet the original adjacent-port contract.

`NEXT_TASK.md`, “Decisions after the sweep”, correctly calls its transport suggestion preliminary, but it supplies no replacement consumer theorem and misses this immediate K=1 obstruction. Its forecast of considering an unequal supplier must be revised accordingly.

## 2. Stronger analytic consequence of the accepted seed obstruction

The root reviewer proposed the following extension. This reviewer independently checked every step; the separate mathematical reviewer also confirmed it. It is a new deduction from the uploaded proof, not a result attributed to OpenChamber's runs.

### Claim

For `q=1,r=2,z0=z1=0`, no labeling of exactly the eight-vertex prefix through physical `s:2` can satisfy P01-P06 with an interval of K unused labels and an adjacent port, for any `K>=6`. This is an interface obstruction, not nongracefulness of the full tree.

### Proof

Set `m=K+7`. Suppose such a prefix labeling exists. It assigns eight distinct labels in `0..m`, leaving precisely `R=[ell,ell+K-1]`, and its seven actual edge differences are exactly `[K+1,K+7]`.

1. Difference m occurs in the prefix. Hence both labels 0 and m occur there, so the unused interval contains neither endpoint: `1<=ell<=7`.
2. The assigned labels therefore form two nonempty blocks `L=[0,ell-1]` and `H=[ell+K,K+7]`. Their cardinalities are ell and `8-ell`; each is at most 7. Each block has width at most 6.
3. Since `K>=6`, every required prefix difference is at least `K+1>=7`. No original prefix edge can have both endpoints in the same block. All edges cross from L to H.
4. The original prefix is connected and has bipartition A=`{s:1,b:0:0,l:1:0:0,l:1:0:1}` and B=`{s:0,b:1:0,l:0:0:0,s:2}`, each with four vertices. A connected bipartite graph has only these two color classes, up to exchanging them. Therefore ell=4.
5. Leave labels in L unchanged and subtract K from labels in H. This gives a bijection onto `0..7`, and every actual edge difference decreases by exactly K, yielding differences `1..7`. It is an alpha labeling of the same named prefix.
6. If the active label was the adjacent high boundary `K+4`, the compressed physical port is 4 and B is the high class. This is exactly the impossible seed already reviewed.
7. If the active label was the adjacent low boundary 3, the compressed port is 3 and B is the low class. Complement every compressed label by `x -> 7-x`. Differences are unchanged, B becomes the high class, A becomes the low class, and the same physical port becomes 4. This again produces the impossible seed. Complement is used here as a proof implication, not as an enumeration quotient.

Both alternatives contradict the proved p=4 obstruction. Thus the stated interface is impossible for every K>=6. The threshold 6 is sufficient; no sharpness claim or conclusion about K=1..5 is made.

## 3. Consequence for the research objective

The supplied state says the precise all-positive-K adjacent-port supplier remains merely open. The new corollary shows that this exact target is unattainable for the q=1,r=2 zero-padding family: it cannot work for K>=6, irrespective of a better solver, a different interval position, reversing the side, or avoiding an explicit alpha restriction in the initial formulation.

The larger objective of graceful labelings or another useful construction remains intact. To advance it, at least one interface requirement must change: for example port adjacency, residual label shape, residual difference shape, or the position of the prefix cut. Those are distinct research decisions and should not be changed silently together.

## 4. Precise proposed revisions

- Preserve the p=4 theorem, original run bytes, failed-template restrictions, conditional identity, and pending/accepted review history.
- In `STATE.md`, make the current one next action the acceptance/correction task until locally recorded. Do not present the pin sweep as the automatic action after a gate.
- In `NEXT_TASK.md`, remove the unsupported implication that p>=5 seeds with the unchanged shift might directly provide the present all-K supplier. Retain the old proposal as a superseded proposal, with its concrete P05/K=1 obstruction.
- Record the new K>=6 interface corollary with its exact hypotheses, proof, review roles, and no claim of a sharp threshold or ordinary nongracefulness.
- Update P07 language to say this exact all-K interface cannot be independently supplied on the q=1,r=2 zero-padding family; a revised interface is required. P07 remains an appropriate duty for a revised construction.
- Do not execute the queued three-pin sweep during acceptance review.

## 5. One manageable next scope

After the review corrections are recorded, choose one replacement interface explicitly. A focused candidate is to relax only port adjacency while preserving the same residual interval, differences, topology, and physical port, and ask for a proved path consumer for a stated nonadjacent offset and a quantified K-domain. The immediate smallest hypothesis would be offset two above the upper endpoint, with K>=2 and K=1 handled separately by an already checked ordinary-family base case if its exact interface is not being claimed. No seed sweep should be promoted as construction progress until that consumer contract is proved or refuted. This is a suggested future scope, not a proved consumer or an executed task.
