# R241 paired supply on an original branched spine

[Authorized task](../tasks/LCL_Codex_R241_Arbitrary_Branched_Spine_2026-11-22.md) · [Strategy](../docs/strategy/LCL_Branched_Spine_Research_Roadmap_2026-11-22.md) · [Evidence](../evidence/validation/LCL_R241_PAIRED_BRANCHED_SPINE_001/README.md)

## Exact claim and domains

Let `n≥1` and let the initial sections be `[[a_0],…,[a_(n−1)]]`. Each has one center `b:i:0` at its original spine vertex `s:i`, with the `a_i` original terminals `l:i:0:j`. All parameters are exact integers. A quota of zero gives `[0]`, with the original center serving as a direct leaf. An empty section `[]` has no center. In all three disjoint quota domains below the normalized prefix is alpha graceful with high exit `s:(n−1)=P+1`. Appending exactly `L≥2` empty sections gives an ordinarily graceful original tree by the construction below.

| Domain | Starter | Remaining blocks |
| --- | --- | --- |
| All quotas positive, either parity | First pair for even n, first section for odd n | Successive pairs |
| Even n, nonnegative quotas and at least one zero | First pair | Successive pairs |
| Odd n, first quota positive, other quotas nonnegative and at least one zero | First section | Successive pairs |

The prefix order is `N=Σ_i(a_i+2)`. Its edges are the `n−1` spine edges, `n` center attachments and `Σ_i a_i` terminal edges, totaling `N−1`. Repeating these incidences with `L` additional spine vertices and no branches gives a tree of order `N+L`. The results below use original names and exact incidence multiplicity throughout.

## Independently supplied modules

A normalized state `A(N,p;x,y)` uses one each of the labels `[0,N−1]` and the edge differences `[1,N−1]`. Each edge has one low endpoint in `[0,p−1]` and one high endpoint in `[p,N−1]`. Actual low entrance and high exit have labels `x` and `p+y`. For the R241 witness we supply a path between those actual vertices within distance two of every vertex of the module.

For `M(a,b)` at positions i and i+1 set `p=a+2` and `N_M=a+b+4`. Give `s:i,s:(i+1)` labels `1,p+1`, centers `b:i:0,b:(i+1):0` labels `p,0`, and their terminals labels `j+2` for `0≤j<a` and `p+2+j` for `0≤j<b`, respectively. The second center, incoming spine and first terminals partition the low band as `{0},{1},[2,p−1]`. The first center, outgoing spine and second terminals partition the high band as `{p},{p+1},[p+2,N_M−1]`. Every original edge crosses these classes. Its weight belongs to exactly one of the following groups.

| Original edges | Differences |
| --- | --- |
| First center to its terminals | `a−j` for `0≤j<a`, giving `[1,a]` |
| First spine vertex to first center | `a+1` |
| First spine vertex to second spine vertex | `a+2` |
| Second spine vertex to second center | `a+3` |
| Second center to its terminals | `a+4+j` for `0≤j<b`, giving `[a+4,a+b+3]` |

These exhaust `[1,N_M−1]` with no overlap. When a or b is zero its terminal band and its terminal list are empty, with the respective center attachment still present. The witness is the spine edge between the two ports. Each center is one edge from it and each terminal two. This gives `A(N_M,a+2;1,1)` for both nonnegative quotas without a supplied solution.

For `S(a)`, `a≥1`, give the first center 0, physical s:0 the label 2, terminal index 0 the label 1, and terminals of index `1≤j<a` the labels `j+2`. The highs are precisely `[1,a+1]` and every edge meets the center of label zero. Their differences are the high labels once each. The actual low entrance is b:0:0 and the actual high exit is s:0. Their edge is a witness, with every terminal one edge from the center on the path. Thus `S(a)` gives `A(a+2,1;0,1)`. At a=1 the remaining terminal band is empty. At a=0 this starter cannot have high exit 2 in a two-vertex alphabet, so the odd first-zero case is outside the supplied domain.

## R241 on the actual spine

Use the adopted R241.1, parts 1–2, from MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`, original blob `faca17cfa4c484127413762adc0c36b771a18f71`. Here B is the accumulated prefix, of order `N_B` and low size `P_B`, with high exit `s:(i−1)` of label `P_B+1`. A is the next independently supplied pair at i,i+1, disjoint from B, of order `N_A` and low size `p_A`. Its actual low entrance `s:i` has label 1. The only original edge between their vertices is `s:(i−1)–s:i`. In particular the R241 port equality is `y_B=x_A=1`. [Pinned original](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [Retained proof and adoption](../references/upstream/mdl/N241_relational_ports.md)

Keep the old B lows fixed, shift every A label by `P_B`, and shift only the old B highs by `N_A`. The label groups are

| Group | Interval |
| --- | --- |
| B lows | `[0,P_B−1]` |
| A lows | `[P_B,P_B+p_A−1]` |
| A highs | `[P_B+p_A,P_B+N_A−1]` |
| B highs | `[P_B+N_A,N_A+N_B−1]` |

They partition the full alphabet bijectively at the low cut `P_B+p_A`. A's actual internal differences remain `[1,N_A−1]`; each B edge gains `N_A` because its high end alone moves. The original spine connector goes from old exit `P_B+1+N_A` to new entrance `P_B+1`, giving `N_A`. The resulting difference bands `[1,N_A−1],{N_A},[N_A+1,N_A+N_B−1]` are disjoint and exhaustive. All three edge groups cross the new alpha cut. The actual entrance of B keeps its low label `x_B`, and the new exit `s:(i+1)` has `P_B+p_A+1`. The new state has offsets `(x_B,1)`.

The supplied B witness ends at `s:(i−1)`; append the actual connector and the A witness `s:i–s:(i+1)`. Disjoint original sections ensure a simple path. All previously witnessed vertices keep a path of length at most two to the witness. Both new centers and their terminals are within distances one and two of the appended spine. The union uses all and only the original edges of the longer prefix. It is connected by one edge between two trees, hence acyclic.

For even n, initialize with the first pair. For odd n, initialize with S and use pairs at indices 1,3,… . Inductively every join has the stated input offsets and returns the same exit offset, so every required connector is available. There are `n/2−1` joins in the even case, and `(n−1)/2` in the odd case. The n=1 and n=2 bases use no join, with no demand for an empty-state identity. Summing the low contributions gives `P=Σ_(j even)(a_j+2)` in the even case and `P=1+Σ_(j odd)(a_j+2)` in the odd case, with `0≤j<n`. The final state is `A(N,P;1,1)` or `A(N,P;0,1)`, respectively. Each step adds two sections, so a requested finite original prefix is supplied in finitely many steps. At L=0 this already labels the complete original.

## Exact suffix resources and termination

For `L≥2`, shift all and only prefix highs by L. The shifted prefix uses labels `[0,P−1] ∪ [P+L,N+L−1]` and differences `[L+1,N+L−1]`. Every assigned edge crosses the old alpha cut and so gains L once. The full original label and difference alphabets are `[0,N+L−1]` and `[1,N+L−1]`. Their exact complements are `R=[P,P+L−1]` and `D=[1,L]`. The assigned exit at physical `s:(n−1)` is `P+L+1`.

The remaining vertices are precisely `s:n,…,s:(n+L−1)`, with no centers or terminals. Their only incident edges are the L successive original edges starting from the assigned exit. The only prefix-to-suffix edge is thus `s:(n−1)–s:n`. Translate the [retained numerical recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof) by P on this actual path. Its bases `C_2=(3,1,0)`, `C_3=(4,1,0,2)`, `C_4=(5,1,2,0,3)` begin at `L+1` and use suffix entries `[0,L−1]` and differences `[1,L]` once each. For `L≥5`, prepend `(L+1,1,L−1)` to the full reflection of `C_(L−3)` by `u↦L−2−u`. The reflected sequence starts at 0 and has remaining entries `[2,L−2]`. With 1 and `L−1` these give the exact suffix. The three new differences to the reflected zero are `L,L−2,L−1`. The bridge from that zero to the next reflected entry is the first edge of the smaller sequence after reflection, so together with later reflected edges it supplies `[1,L−3]` once each. Decreasing L by three ends at a base.

The translated initial entry agrees with the assigned exit. The remaining entries use R once each and the L actual pending edges use D once each. The labels and weights therefore exhaust the full original alphabets without changing the prefix. This proves ordinary gracefulness with the suffix. The alpha claim applies to the normalized prefix. The full original spine is also a lobster witness. At L=1, the same high shift gives only `R={P}`, `D={1}` and port `P+2`, so its required edge would have weight two. This excludes that interface at L=1. The proof uses numerical recurrence reuse as in [D067](B4_2222_NONADJACENT_ALL_K.md#recurrence-and-the-physical-path). The public B2 wrapper retains its specialized physical `s:2` contract.

## Comparison and exact limits

This uses R241's existing conditional composition with explicit supplier modules whose offsets do not depend on the two quotas. R241's R212-B.1 application used a different physical module and related neighboring quotas. No change to the adopted theorem or its original disposition is implied. With four initial sections and B4's convention `L=K+1`, the all-positive construction covers every positive branch tuple at K≥1. The T4 case at K=1 already lies in [D062's ordinary construction](B4_JOINT_NESTED_CUT_TWO_HOST.md), and [D060 archived that named original](../evidence/validation/B4_JOINT_23_MAX_ROOTED_CORE_001/validation/lift-t2-original.json). T5 at L=3 uses its own retained original with D076's distinct ledger. C_3 is a base, while T8 at L=5 exercises the reflected bridge. These distinctions correct the informal T4 and T7 descriptions in the immutable packet without changing its grid.

The supplied domain has exactly one center per initial section. It excludes arbitrary multiple centers, internal empty sections, and the odd first-zero regime. The equality failure for the fixed R241 placement and the L=1 failure for the specified suffix interface give no nongracefulness conclusion. No historical priority or universal lobster claim is made.
