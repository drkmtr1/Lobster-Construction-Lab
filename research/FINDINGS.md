# Retained findings and project dispositions

This file owns scientific findings. See the [preceding detailed audit](../references/MDL_General_Construction_Review_2026-11-20.md) for broader explanations and pinned primary links, and [source provenance](../references/upstream/MANIFEST.json) for exact excerpt identities. Upstream mathematical reviews are retained reviews, not a claim of human peer review or formal certification.

## 1. Construction assets retained from MDL

| Finding | Actual useful result | Limitation / implementation disposition |
|---|---|---|
| [N33](../references/upstream/mdl/N033_retained_record.md) | Explicit label formula for every parameter in a fixed family (h>=8), with a complete difference inventory | A real infinite construction; restricted topology, not a universal lobster formula. Preserved as reference, not reimplemented in v0.1 |
| [N68](../references/upstream/mdl/N068_retained_record.md), [N69](../references/upstream/mdl/N069_retained_record.md), [N70](../references/upstream/mdl/N070_retained_record.md) | Fresh-label and patch/tile constructions, including success on a family obstructing an earlier model | Shows why a failed fixed labeling model should be redesigned rather than mistaken for a nongraceful target |
| [N107](../references/upstream/mdl/N107_retained_record.md) | Independent compatible-input supply under paired-profile restrictions, with explicit allocation/permutation machinery | Arbitrary unpaired profiles remain outside the supplied domain; retained reference |
| [N121](../references/upstream/mdl/N121_retained_record.md) | Arbitrary-length unequal-factor composition with all positive odd terminal sizes, odd first branch degree and even later branch degrees in its stated domain | Genuine independently supplied composition, with parity assumptions and known-source overlap |
| [N135](../references/upstream/mdl/N135_retained_record.md), [N141](../references/upstream/mdl/N141_retained_record.md) | Exact binary recurrence/capacity criterion and assignment within a restricted loop model | Model-specific finite state, not lossless finite compression of all lobster states |
| [N145](../references/upstream/mdl/N145_retained_record.md) | Paired unequal-order composition with two actual ports | Pairing and correct physical interfaces are required |
| [R226](../references/upstream/mdl/N226_R226_two_host_completion.md) | Exact constructive two-host leaf completion through balanced difference components, reflected pairs and host quotas | Implemented. Core labels and the original residual palettes are inputs; fixed-core failure is restricted |
| [R232](../references/upstream/mdl/N232_R232_joint_allocation.md) | Joint completion under reserved palette partitions, forest, parity and capacity conditions | Coordinates several consumers; does not independently supply a general successful palette partition. Preserved, not implemented |
| [R241](../references/upstream/mdl/N241_relational_ports.md), [R246](../references/upstream/mdl/N246_reconstruction_and_count_correction.md) | Reusable relational ports, independently supplied modules and actual-leaf attachments under exact compatibility | Useful alternative composition route; alpha/design/domain conditions remain. Preserved, not implemented |
| [R243](../references/upstream/mdl/N243_fixed_leaf_connectors.md) | Fixed-leaf connectors and exact offset ranges | Connector insertion changes the target; any application must reconstruct the original target separately |
| [R244](../references/upstream/mdl/N244_contraction_corrections.md), [R248](../references/upstream/mdl/N248_component_palette_reflection.md) | Conditional reconstruction and palette-preserving source transformations | Require an appropriate source and a reachability/reconstruction argument; no universal target supply |
| [N240](../references/upstream/mdl/N240_resource_algebra_counting.md) and exact recurrence | Exact named graceful-labeling count using label/difference resource exclusion | The new DFS/DP evaluate finite instances. General positivity and useful universal state compression remain unproved here |

## 2. Construction assets retained from Bounded Search

The [mathematical specification](../references/upstream/bounded/MATHEMATICS.md.archive.md), [lemmas](../references/upstream/bounded/research__LEMMAS.md.archive.md), [hypotheses](../references/upstream/bounded/research__HYPOTHESES.md.archive.md) and [proof/review sources](../references/upstream/README.md) preserve exact domains.

- **L007:** independently supplies an equal-branch cluster and its terminal next edge for `q,r>=1,z>=0`; no later suffix is supplied. Implemented.
- **L010:** a one-branched-section high-label construction with an explicit sufficient budget and a caterpillar suffix. Implemented.
- **H010:** a denser branch-interval placement under its sum and direct-leaf conditions, returning the actual endpoint interval for a caterpillar suffix. Implemented.
- **Caterpillar interval consumer:** consumes a supplied interval from an actual endpoint. Implemented, including singleton and path cases.

The previous finite P004 campaign's 680 fixed-prefix cases, 160 successful joint completions and 520 failures describe that archived scope; they are not a census of all lobsters or isomorphism classes. No old campaign was resumed. Failures and adopted corrections are preserved in `FAILED_HYPOTHESES.md` and the archived counterexample ledger.

## 3. B2-BASELINE-COMP: reviewed project corollary

**Disposition: adopted as a restricted project baseline.** Independent reasoning roles recalculated the composition of two one-positive-branch L010 prefixes. For arbitrary `q,r,K>=1`, let `K1=r+z1+K+2`; require `z1>=K+1` and `z0>=K1+1`. Reflection of the second local labeling returns

\[
R=[K_1-K+1,K_1],\quad D=[1,K],\quad f(s:2)=K_1-K.
\]

The exact remaining K-edge path has an explicit endpoint-interval completion. `two_section_padded` implements this from parameters with no whole-solution search. Its independent tests check complete and partial certificates, domain boundaries and larger branch sizes beyond the generic H010 bound. The proof calculation is in `PROOF_OBLIGATIONS.md`.

This is a derived use of retained formulas, not a new upstream statement, a formalized proof or a historical novelty claim. The real next gap is a useful smaller-budget domain or broader repeatable interface.

## 4. B2-BALANCED-SUPPLY: independent zero-padding family

**Disposition: adopted as a reviewed project construction.** For every integer `t,K>=1`, set `q=r=t,z0=z1=0` and `m=2t+K+4`. Label the seven vertex roles (with t leaves in each leaf group) by

```text
s:0 = m                         b:0:0 = 0
l:0:0:j = K+t+4+j               for j=0,...,t-1
s:1 = t+1                       b:1:0 = K+t+3
l:1:0:j = j+1                   for j=0,...,t-1
s:2 = K+t+2
```

These are explicit formulas from the parameters. They use labels `0..t+1` and `K+t+2..m`; their actual edge differences partition `K+1..m`. The unused label interval is `[t+2,K+t+1]`, unused differences are `1..K`, and actual port `s:2` is labeled one above the interval. The endpoint path consumer finishes the original target.

Two separate reasoning roles checked the symbolic label/edge partitions. `two_section_balanced(t,K)` implements the rule and `two_section_unit(K)` is its t=1 specialization. The full proof, exact domain and source-overlap caution are in [B2_BALANCED_SUPPLIER.md](B2_BALANCED_SUPPLIER.md). This supplies a genuine parameterized zero-padding interface, rather than only finite extraction. No historical novelty, formal proof-assistant check or universal lobster result is claimed. The next selected question is the unequal pair (1,2), specified in `NEXT_TASK.md`.

## 5. Finite validation and current literature

The authoritative executed results are in `evidence/validation/VALIDATION_REPORT.md` and its linked JSON records. Positive witnesses are bound to original graphs and requested restrictions. Count controls and the four B2 pairs have only their stated finite meaning. They do not prove a new supplier family.

The [current literature note](../docs/LITERATURE_UPDATE.md) records the author-posted subcubic Lean archive, almost-graceful asymptotics and graceful supertree construction with their exact inspection limits. All three small pilot profiles fall within the subcubic archive's stated ordinary-gracefulness scope; the prescribed interval/port condition is an additional question. The source was inspected, not locally rebuilt in Lean. No exhaustive worldwide novelty or status audit is claimed.

## 6. Promotion criteria

New findings must name their quantifiers/domain, independent inputs, unchanged original topology, returned physical interface, proof/verification evidence, applicable sources and remaining dependencies. Universal coverage requires a coverage and termination argument, not a large finite record. Keep unproved candidate statements in proof obligations and preserve failed attempts in the failure ledger.
