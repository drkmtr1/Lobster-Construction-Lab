# Selected literature update and applicability

**Checked:** 2026-11-21 UTC / 2026-11-20 Hawaiʻi. This is a bounded check of three primary sources. It is not an exhaustive literature review, a priority determination, or a statement about the current status of every version of the lobster conjecture.

## 1. A finite certificate for subcubic lobsters

Akram Younso's [Zenodo v2 record, November 3, 2026](https://zenodo.org/records/23932907) claims a graceful-labeling theorem for every finite lobster with maximum degree at most three. Its [source archive](https://zenodo.org/records/23932907/files/subcubic-lobsters-lean-proof.zip) includes Lean sources and a 6,104-row certificate. We downloaded it, checked the table's size/hash against its README, and inspected the graph theorem, coverage file and relevant certificate/assembly passages. The precise hashes and dependency pins are in [SOURCES.md](SOURCES.md), entry E10.

The inspected graph statement uses a finite simple tree, maximum degree three, and a witnessing path within distance two of every vertex. It concludes bijections for vertex labels and actual unordered edge differences. This avoids treating an encoded word theorem alone as a theorem about arbitrary graphs.

The method is especially relevant here. Bounded exploration proposes a finite collection of transition states; a separate check requires closure and acceptance for every outgoing letter. A general coverage argument then handles arbitrary finite words. That separates **finding a candidate invariant** from **certifying that it covers all lengths**. It does not turn an arbitrary collection of successful small examples into a proof.

**Inspection limit:** we did not build Lean or audit every proof dependency. Three source checks use `native_decide`, and the README identifies compiler-trusted evaluation. The author record reports that independent peer review has not yet occurred. “Primary source inspected” must not be rewritten as “independently reproduced formal proof.”

### Exact relevance to the starter pilot

The pilot uses three profiles, `(q,r)=(1,1),(1,2),(2,1)`, with no direct leaves and `K=1`, across four prescribed interface pairs. Their branch-center degrees are `q+1,r+1<=3`; `s:1` has degree three and the other spine degrees are smaller. They therefore lie within the archive's stated ordinary-gracefulness scope.

Its headline theorem does not require our particular `s:2` port and returned interval. The pilot tests that additional interface requirement, including two different intervals on the same graph. It is not new ordinary-family coverage. Before proposing another finite-rule construction, compare its states and joining rules with this source. Sizes `q>=3` or `r>=3` leave the cited degree bound, but that observation alone establishes no novelty.

## 2. Asymptotic gracesize

Shoham Letzter, Alexey Pokrovskiy and Ella Williams, [*On the gracesize of trees*, arXiv:2511.11331v2](https://arxiv.org/abs/2511.11331v2), revised July 31, 2026, state that for each fixed `epsilon>0`, all sufficiently large `n`-vertex trees have a bijective labeling with at least `(1-epsilon)n` distinct edge differences.

**Inspection:** primary abstract and version metadata only. This is an almost-graceful result; LCL requires all `n-1` differences exactly once. It could motivate later near-solution or repair questions, but the abstract does not supply our exact prefix boundary or a collision-removal construction. No implementation or runtime consequence is inferred here.

## 3. Graceful supertrees

Obinna Okechukwu, [*Graceful supertrees with at most 2m-diam(T) edges*, arXiv:2611.01340v1](https://arxiv.org/abs/2611.01340v1), submitted October 31, 2026, states an explicit graceful supertree construction. Its abstract gives `M=2m-h-t_h+1` edges for a rooted input of height `h` with `t_h` farthest vertices, yielding the displayed diameter bound.

**Inspection:** primary abstract and metadata only. A graceful supertree may introduce vertices and enlarge the label alphabet. Restricting its labeling to the original tree need not give labels `0..m` or differences `1..m`. LCL may investigate its reflection/resource ideas later, but an exact-target reconstruction theorem would still be required. This source does not discharge that obligation merely by containing the requested tree.

These sources sharpen the comparison work: inspect relevant established interfaces first, distinguish near/full labeling, and preserve the original graph throughout any claimed construction.
