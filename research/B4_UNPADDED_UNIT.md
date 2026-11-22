# B4-UNPADDED-UNIT-001

**Independent AI mathematical review — ACCEPT** for the domain below. The review checked the original named graph, both prefix inventories, the R241/L008 substitution and returned ports, the completion for both parities including K=1, and the completed alpha threshold.

**Independent AI implementation and evidence review — ACCEPT** on the same domain. The reviewer inspected named graph construction, exact CLI preflight, the unchanged adjacent consumer's start at `s:4`, prefix preservation, and the verified alpha split. The reviewer checked the separate seed record and the matching identities and results for the same 12 completed targets in the regression and arithmetic audit. [Validation record](../evidence/validation/B4_UNPADDED_UNIT_001/README.md)

## The exact original graph and prefix

For every integer `K>=1`, excluding booleans, the original profile `[[1],[1],[1],[1]]+[[]]*(K+1)` admits an alpha graceful labeling. The graph has `K+5` consecutive spine vertices `s:0,...,s:(K+4)`, four centers `b:i:0` joined to `s:i`, and four leaves `l:i:0:0` joined to their respective centers, for `i=0,1,2,3`. Its `K+4` spine edges and eight branch edges give `m=K+12`. The prefix has 13 vertices, consisting of the first five spine vertices and the four original branches. Only the last `K` spine vertices are unassigned. Their incident edges are the original consecutive path from `s:4`, with the sole crossing edge `s:4--s:5`.

Supply these labels directly from `K` on the original named prefix.

| Named vertex or pair | Prefix labels in the displayed order |
|---|---|
| `s:0,s:1,s:2,s:3,s:4` | `K+12,2,K+9,5,K+6` |
| `b:0:0,l:0:0:0` | `0,K+11` |
| `b:1:0,l:1:0:0` | `K+10,1` |
| `b:2:0,l:2:0:0` | `3,K+8` |
| `b:3:0,l:3:0:0` | `K+7,4` |

In increasing label order the six low vertices are `b:0:0,l:1:0:0,s:1,b:2:0,l:3:0:0,s:3`. They use exactly `[0,5]`. The seven high vertices in increasing label order are `s:4,b:3:0,l:2:0:0,s:2,b:1:0,l:0:0:0,s:0`. They use exactly `[K+6,K+12]`. Each original prefix edge crosses these sets. Direct subtraction gives the following differences on all twelve edges.

| Original prefix edges | Absolute differences in order |
|---|---|
| Spine through `s:4` | `K+10,K+7,K+4,K+1` |
| `s:0--b:0:0`, `b:0:0--l:0:0:0` | `K+12,K+11` |
| `s:1--b:1:0`, `b:1:0--l:1:0:0` | `K+8,K+9` |
| `s:2--b:2:0`, `b:2:0--l:2:0:0` | `K+6,K+5` |
| `s:3--b:3:0`, `b:3:0--l:3:0:0` | `K+2,K+3` |

Each offset from 1 through 12 occurs once. The prefix leaves `R=[6,K+5]` and `D=[1,K]` with `s:4=K+6`, exactly one above the maximum element of `R`. Both inventories are supplied before applying the retained adjacent path consumer.

## Completion and the alpha classes

Let `w_j=s:(4+j)` for `0<=j<=K`. Begin at the assigned high port `w_0`. Take the lowest available label at the first new vertex, the highest at the second, and alternate. After taking a low endpoint the new port is just below the remaining interval. After taking a high endpoint it is just above the remaining interval. Thus the adjacent endpoint invariant holds at every step until the interval is empty. The current code's adjacent helper `_consume_suffix` takes a start index, and on this branch-free suffix it traverses the original spine from index 4 and adds one vertex per original edge. [Retained adjacent argument](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)

The resulting assignments are `f(w_(2i+1))=6+i` and `f(w_(2i))=6+K-i` when the respective positions are in the suffix. The odd positions use `[6,5+ceil(K/2)]` in increasing order. The positive even positions use `[6+ceil(K/2),K+5]` in decreasing order. The second interval is empty at K=1. These disjoint intervals partition `R`. On an odd step `j=2i+1` the preceding value is `6+K-i`, including `w_0` for `i=0`, and the difference is `K-2i`. On an even step `j=2i` the preceding value is `6+i-1`, and the difference is `K-2i+1`. Both expressions give `K-j+1`, so all missing differences appear once. The process makes exactly `K` assignments and preserves every prefix label. For K=1 specifically, `R={6}`, `D={1}`, `s:4=7`, and `s:5=6` realize difference 1 on the actual last edge.

Put `p=6+ceil(K/2)`. The prefix low class together with the odd suffix vertices has labels `0..p-1`. The prefix high class together with the positive even suffix vertices has labels `p..m`. The prefix edges cross these classes as above, and the suffix alternates classes starting at the high physical port. Thus every original edge crosses the threshold and the completed labeling is alpha. The low-class size of the fixed seed used below is 6. The completed low-class size counts the additional odd suffix vertices.

## Retained R241/L008 derivation of the fixed seed

In the 13-vertex prefix graph, remove exactly the original edge `s:2--s:3`. The left component B contains `s:0,s:1,s:2` and branches 0, 1, and 2. Give its spine the labels `8,2,5`, and give its center/leaf pairs `(0,7),(6,1),(3,4)` in branch order. These cover `0..8` once. The spine differences are `6,3` and the attachment/terminal pairs are `(8,7),(4,5),(2,1)`. Hence the differences cover `1..8` once. The vertices `b:0:0,l:1:0:0,s:1,b:2:0` are the low class `0..3`. Direct inspection of the spine and the three branches gives a cross-class edge at every incidence. B has `n_B=9,p_B=4` with actual ports `L_B=b:0:0` at 0 and `U_B=s:2` at 5, so `x_B=0,y_B=1`. The original path `b:0:0--s:0--s:1--s:2` is a witnessing path. Its off-path leaf at branch 0 is one edge away and the remaining off-path branch vertices are at distance at most two.

The right component A contains precisely `s:3,s:4,b:3:0,l:3:0:0`. The retained L008 rule at branch size 1 and zero padding assigns `s:3=0,l:3:0:0=1,b:3:0=2,s:4=3`. Its low interval is `[0,1]` and its high interval is `[2,3]`. Reflect the low interval by `x -> 1-x` and the high interval by `x -> 5-x`. For an original high label `h` and low label `l`, the new difference is `(5-h)-(1-l)=4-(h-l)`. This permutes `1..3` and preserves the two intervals and original incidences. The resulting local assignment is `s:3=1,s:4=2,b:3:0=3,l:3:0:0=0`. Hence `n_A=4,p_A=2`, and the actual ports `L_A=s:3` and `U_A=s:4` have offsets `x_A=1,y_A=0`. The edge `s:3--s:4` witnesses A with the center and leaf at distances one and two from the edge. [Retained L008](../references/upstream/bounded/research__LEMMAS.md.archive.md) · [Pinned L008, MDL_Bounded_Search](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md#L21) · source blob `f942e3b8b7628353ef7cf9d8cf53759c2eed0478`

Use the adopted R241 binary rule with A as the right component and B as the left. The equality `x_A=y_B=1` holds. The connector `L_A--U_B` restores exactly `s:3--s:2`. Add `p_B=4` to all A labels, leave B's low labels fixed, and add `n_A=4` to B's high labels. The four consecutive label blocks are B low `[0,3]`, A low `[4,5]`, A high `[6,7]`, and B high `[8,12]`. A's internal differences remain `1..3`, the restored edge has difference `9-5=4`, and B's internal differences become `5..12`. The physical ports returned by R241 are `L_B=b:0:0` at 0 and `U_A=s:4` at 6, with offsets `(0,0)` and low-class size `p_A+p_B=6`. The witnessing paths concatenate along the actual connector into `b:0:0--s:0--s:1--s:2--s:3--s:4`. [Retained N241](../references/upstream/mdl/N241_relational_ports.md) · [Pinned R241 argument](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [Adopted R241 disposition](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4488-L4505) · source blob `faca17cfa4c484127413762adc0c36b771a18f71`

Substitution gives spine `(12,2,9,5,6)` and center/leaf pairs `(0,11),(10,1),(3,8),(7,4)`. These are the stated seed values with the `K` terms omitted. Shift its seven high labels uniformly by `K`. Its six low labels stay fixed and every edge across the seed cut gains exactly `K` in difference. This recovers the supplied prefix pointwise and sends its high physical port from 6 to `K+6`. The seed is an arithmetic composition on the named prefix graph `[[1],[1],[1],[1],[]]`, with a separate certificate from the completed targets. The public constructor's domain starts at K=1.

## Scope and comparison

This is a project corollary for four consecutive unit branches at zero padding and a positive spine suffix length. The construction uses the same adjacent interval invariant as the accepted B3 adjacent supplier, now at the original physical `s:4`. Each established B2/B3 constructor retains its own scope and resource contract. The result supplies a fixed finite composition and a parametrized path completion. Other four-section branch sizes, padding, multiple positive branches per section, further sections, and arbitrary repetition remain separate proof duties. The mathematical disposition is a separate AI proof review. Finite validation and the saved-certificate audit are recorded separately, and no historical novelty, human peer review, proof-assistant verification, or universal-lobster claim is made.
