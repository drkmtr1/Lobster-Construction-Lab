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

## 5. B2-UNEQUAL-SEED-001: exhausted restricted negative

**Disposition: ACCEPT — independently reviewed restricted negative at revision `2cfb2df`; see [Codex acceptance review](B2_CODEX_ACCEPTANCE_REVIEW.md) and D018.** The named eight-vertex prefix `[[1],[2],[]]` (the seven actual edges listed in [B2_UNEQUAL_SEED.md](B2_UNEQUAL_SEED.md) section 1), subject to exactly the declared restrictions — A-side `s:1,b:0:0,l:1:0:0,l:1:0:1` bijectively labeled `0..3`, B-side `s:0,b:1:0,l:0:0:0,s:2` bijectively labeled `4..7`, physical port pin `h(s:2)=4`, and no further root pin, complement quotient, symmetry assumption or automorphism quotient — **has no graceful labeling**.

The proposed analytic obstruction is correct in every step: difference 1 forces `h(s:1)=3`; the sum identity `a+2b−x=18` admits only `(a,b,x) ∈ {(5,7,1),(6,7,2),(7,6,1)}`; in all six resulting assignments difference 4 is duplicated on at least two actual original edges (three times in the third triple). The declared bounded DFS (65 nodes of the 10,000 cap) and the independent direct permutation oracle (5,040/5,040 permutations, 144 domain-admissible, 0 graceful) both exhausted the declared scope with 0 solutions on the same original graph digest. A separate reviewer subagent challenge confirmed every step; two minor reporting omissions in the record's step 5 were corrected (both strengthen the obstruction).

Scope: this falsifies exactly this alpha/physical-port template. It is not a nongracefulness certificate for the unrestricted eight-vertex tree, for any other restriction set, or for the unequal B2 family at any K. The all-K high-side-shift transport is retained as a conditional identity only (its antecedent is false) and discharges no P07 obligation. Failure-ledger entry: F-UNEQUAL-SEED; decision: D015; full record: [B2_UNEQUAL_SEED.md](B2_UNEQUAL_SEED.md).

## 6. B2-INTERFACE-OBSTRUCTION: the all-K adjacent-port interface is impossible for K>=6

**Disposition: ACCEPT — independently reviewed scoped interface obstruction at revision `2cfb2df`; see [Codex acceptance review](B2_CODEX_ACCEPTANCE_REVIEW.md) and D018.** For `q=1`, `r=2`, `z0=z1=0` and every integer `K>=6`, the exact eight-vertex prefix through `s:2` of the B2-P1 tree (profile `[[1],[2]]+[[]]*(K+1)`, the seven original edges of [B2_UNEQUAL_SEED.md](B2_UNEQUAL_SEED.md) section 1) admits **no** injective labeling in the final alphabet `0..K+7` with unused labels exactly `[ell,ell+K-1]`, prefix-edge differences exactly `K+1..K+7` (equivalently unused differences `1..K`), and physical port `f(s:2)=ell+K` or `f(s:2)=ell-1`, for any `ell` and either side. No alpha condition is assumed and no root label is pinned.

Argument in outline (full proof with scope in [B2_INTERFACE_OBSTRUCTION.md](B2_INTERFACE_OBSTRUCTION.md)): the maximum difference `K+7` forces labels `0` and `K+7` into the prefix, giving `1<=ell<=7`; the assigned labels are therefore two blocks `0..ell-1` and `ell+K..K+7`, each of span at most six; for `K>=6` every prefix edge must cross between the blocks; the connected prefix's `4/4` bipartition forces `ell=4`; subtracting `K` from the high block yields a graceful alpha labeling of the original seed graph; the above-side port becomes exactly the forbidden p=4 seed, and the below-side port becomes, after complementing labels by `7-g`, the same forbidden seed (a proof map, not a counting quotient). Both sides are impossible.

Scope limits: the threshold 6 is sufficient, not claimed sharp; `K=1` is feasible at `ell=1`, above, by the preserved pilot; `K=2..5` are not adjudicated here; this is an obstruction to the particular returned interface at the exact prefix — not a nongracefulness proof for the full tree, for any other family, or for any other restriction set; the balanced `q=r` supplier and the padded construction (different parameter domains) are unaffected. Provenance: new deduction of an independent external acceptance review of checkpoint `0f0a39c` (pack `LCL_B2_Independent_Review_2026-11-21`, custody at `evidence/reviews/B2_UNEQUAL_SEED_001/`), challenged there by two separate reasoning agents and independently re-derived step by step by the integrating session. Failure-ledger entry F-INTERFACE-K6; decision D016.

## 7. B2-NONADJACENT-CONSUMER-001: conditional path completion

**Disposition: ACCEPT — separate proof and implementation review.** For every integer `K>=2` and integer `ell`, a valid supplied prefix with actual port `s:2=ell+K+1`, unused labels `[ell,ell+K-1]`, unused differences `1..K` and the exact original K-edge path from `s:2` can be completed without changing the prefix. The K−3 recurrence, induction, physical requirements and independent reviewer disposition are in [B2_NONADJACENT_CONSUMER.md](B2_NONADJACENT_CONSUMER.md). For K=1 the sole edge would have difference 2, so this particular interface cannot be consumed.

The separate helper `lcl.consumers.complete_nonadjacent_path` validates the caller-supplied original graph, prefix and exact path, and the unchanged certificate verifier checks the complete result. `interval_boundary` remains the adjacent-port predicate. This consumer is not itself an independent supplier; the separate port-5 seed and supplier are recorded in the next finding. No historical novelty, formal verification or universal-lobster claim is made. Decision D019; finite regression and reviewer receipts: `evidence/validation/B2_NONADJACENT_CONSUMER_001/`.

## 8. B2-NONADJACENT-SEED-P5-001: explicit unequal-family supply

**Disposition: ACCEPT — explicit independent supplier for `q=1,r=2,z0=z1=0` and all integer `K>=2`.** One bounded first-witness DFS found the fixed alpha seed on the original eight-vertex prefix with physical port `s:2=5`; separate original-graph, domain and edge checks verified it. The result is SAT, not exhausted, exact count unknown, lower bound 1; 144 is the total number of domain-admissible named assignments, not the number tested. Fixing the verified finite seed and shifting its high-side labels by K gives direct prefix formulas, exact inventories `[4,K+3]` and `1..K`, and physical port `K+5`; the accepted nonadjacent path consumer completes the original target for all K>=2 without a solver input. The complete proof, exact labels, reduction and reviewers are in [B2_NONADJACENT_SEED_P5.md](B2_NONADJACENT_SEED_P5.md), with preserved run and verification in `evidence/runs/b2-nonadjacent-seed-p5-001-20261121-dfs/`. Decision D020.

For K>=6 the precise nonadjacent interface forces `ell=4` and compresses on original named incidences to a port-5 alpha seed of the declared type; conversely the displayed fixed witness supplies the interface for all K>=2. The separate existing K=1 adjacent-port witness remains a finite checked result, not a new K=1 constructor. Together these establish gracefulness of this exact family for all positive K. The adjacent-port obstruction and p=4 negative are unaffected. The p=5 result alone did not address other unequal profiles; the separate construction in §9 extends the zero-padding domain. The broader lobster problem remains open; no novelty claim or p=6/7 search is made.

## 9. B2-UNPADDED-ALL-QR-001: explicit two-section supply

**Disposition: ACCEPT — independently supplied zero-padding prefix for every integer `q,r>=1`, `K>=2`.** On the exact named profile `[[q],[r]]+[[]]*(K+1)`, the explicit formula in [B2_UNPADDED_ALL_QR.md](B2_UNPADDED_ALL_QR.md) assigns prefix labels exactly `[0,r+1] ∪ [K+r+2,m]` and actual prefix-edge differences exactly `[K+1,m]`. It supplies unused labels `[r+2,K+r+1]`, unused differences `1..K`, and original physical port `s:2=K+r+3`; the accepted nonadjacent path consumer completes the original target without changing the prefix. The proof is symbolic, and the new parameterized implementation is `two_section_nonadjacent`. Decision D021; targeted original-target evidence: `evidence/validation/B2_UNPADDED_ALL_QR_001/`.

The `(q,r)=(1,2)` prefix is exactly the earlier p=5 construction. For `q=r` the existing balanced supplier covers the same graph family with a different adjacent-port labeling and also covers K=1; the padded L010 composition needs direct leaves and does not apply here. This result expands the project’s supplied zero-padding parameter domain but makes no historical novelty or universal-lobster claim. K=1 is outside this formula/consumer theorem; no K=1 search was run in this task. An independently supplied prefix and actual path are the stated construction, not a general branched-suffix or repeatable-transition theorem.

## B2-UNPADDED-K1-001: R241 singleton completion and combined coverage

**Disposition: ACCEPT** after separate AI mathematical and implementation reviews. For every integer `q,r>=1`, the explicit labeling in [B2_UNPADDED_K1.md](B2_UNPADDED_K1.md) gracefully labels the original `[[q],[r],[],[]]` target, with `m=q+r+5`. Its prefix excluding `s:3` leaves `R={q+4}`, `D={q+3}`, and physical port `s:2=1`; the actual final edge consumes exactly these singleton resources. It is an explicit corollary of retained R241 binary composition and the R212-B module, with the original edge `s:0--s:1` as connector. The previously accepted K>=2 construction uses instead `R=[r+2,K+r+1]`, `D=1..K`, and port `s:2=K+r+3`. By cases, the exact unpadded profile `[[q],[r]]+[[]]*(K+1)` is graceful for all positive integer `q,r,K`. This is ordinary-family coverage, not a common prescribed-boundary theorem, historical novelty, human review or formal verification. The adjacent-port P04/P05/P08 obligations and previous scoped obstructions remain unchanged. Decision D022; 12 prescribed original-target certificates and an audit of those same certificates are preserved under `evidence/validation/B2_UNPADDED_K1_001/`.

## B3-UNPADDED-QGE-R-001: reviewed three-section supplier

**Disposition: ACCEPT**, after separate AI mathematical and implementation reviews, for integers `q>=r>=1`, `t>=1`, `K>=2`, zero padding, and exactly `[[q],[r],[t]]+[[]]*(K+1)`. The explicit named prefix in [B3_UNPADDED_QGE_R.md](B3_UNPADDED_QGE_R.md) uses original-edge differences `[K+1,m]` and leaves `R=[a,a+K-1]`, `D=[1,K]`, physical `s:3=a+K+1`, where `a=q+t+3`. The accepted recurrence completes the original path from `s:3` without changing the prefix. The proof is a project corollary of retained R241 and L008 plus a directly proved left-component supplier; no historical novelty is claimed. The separate B3 constructor applies the sequence to `s:3`; it does not broaden the existing B2 fixed-`s:2` helper. Decision D023; 12 original-target cases and a separate audit of those same certificates: `evidence/validation/B3_UNPADDED_QGE_R_001/`.

The domain `q<r` is outside this formula, not proved nongraceful. K=1 requires a different boundary; padding, extra branches, a fourth branched section and arbitrary repetition remain unproved here. Finite tests corroborate the symbolic proof. The earlier B2 resource contracts, scoped negatives and obstructions are unchanged; this review is not human peer review or formal verification.

## B3-UNPADDED-QLT-R-ADJACENT-001

**ACCEPT** for the exact zero-padding profile `[[q],[r],[t]]+[[]]*(K+1)` with integers `1<=q<r`, `1<=t<=q+1`, and `K>=1`. The independent prefix returns labels `[a,a+K-1]`, differences `1..K`, and adjacent port `s:3=a+K`, where `a=q+t+3`. The retained adjacent completion uses the original path, including its single edge for K=1. The proof applies R241 to the directly proved left component and the class-reversed L008 labeling. Separate AI mathematical and implementation reviews accepted the proof and implementation. The 12 original-target certificates and a separate arithmetic audit of those same 12 corroborate the proof. These reviews are at project AI review scope. See [proof](B3_UNPADDED_QLT_R_ADJACENT.md), [evidence](../evidence/validation/B3_UNPADDED_QLT_R_ADJACENT_001/README.md), and D024.

The prior q>=r, K>=2 branch retains the nonadjacent port `a+K+1`. The q<r region with `t>=q+2` lies outside the adjacent construction, with gracefulness unresolved by this result. Padding, extra positive branches, further sections and arbitrary repetition are separate duties. No historical novelty is claimed.

## B3-UNPADDED-QLT-R-LARGE-T-001

**ACCEPT** for the exact original zero-padding profile `[[q],[r],[t]]+[[]]*(K+1)` with integers `1<=q<r`, `r>=3`, `t>=q+2`, and `K>=2`. The direct parity seed has labels `0..M` and original prefix differences `1..M`, where `M=q+r+t+6`. Its high-side shift leaves unused labels `[a,a+K-1]`, differences `1..K`, and nonadjacent physical port `s:3=a+K+1`, where `a=q+t+3`. The retained recurrence completes the original path. Separate AI reviewers accepted the proof and implementation. The seed and full certificates were checked on 12 declared original targets, and a separate arithmetic audit passed on the same saved targets. See [proof](B3_UNPADDED_QLT_R_LARGE_T.md), [evidence](../evidence/validation/B3_UNPADDED_QLT_R_LARGE_T_001/README.md), and D025.

For K>=2, combining this domain with the earlier q>=r nonadjacent branch and the q<r, t<=q+1 adjacent branch leaves exactly `q=1,r=2,t>=3` outside the three suppliers. This is a coverage statement only. K=1 outside the adjacent domain, padding, added branches, further sections, and arbitrary repetition remain separate.

## B3-UNPADDED-Q1-R2-001 and the four-case corollary

**ACCEPT** for `q=1,r=2`, integers `t>=3,K>=2`, zero padding and the exact original profile `[[1],[2],[t]]+[[]]*(K+1)`. The seed assigns `0..M` and uses original prefix differences `1..M` with `M=t+9`. The fixed `t=1` prefix and the prescribed leaf extension at the least-high third center give a second derivation of the seed. The high-side shift supplies unused labels `[a,a+K-1]`, unused differences `1..K`, and nonadjacent physical port `s:3=a+K+1`, with `a=t+4`. The retained recurrence completes the original path. Separate AI reviewers accepted the proof and implementation. One base-prefix certificate is recorded separately from the 12 completed original targets and the audit of those same 12. See [proof](B3_UNPADDED_Q1_R2.md), [evidence](../evidence/validation/B3_UNPADDED_Q1_R2_001/README.md), and D026.

The four disjoint supplier domains exhaust positive integers `q,r,t` and `K>=2` on the original zero-padding profile `[[q],[r],[t]]+[[]]*(K+1)`. Select the first applicable constructor for `q>=r`, for `q<r,t<=q+1`, for `q<r,t>=q+2,r>=3`, or for the remaining `q=1,r=2,t>=3`. This proves ordinary gracefulness for the exact family. Each branch retains its own resource contract and consumer. Remaining K=1 cases outside the adjacent domain, padding, multiple positive branches per section, further sections, and arbitrary repetition require separate results.

## 10. Finite validation and current literature

The authoritative executed results are in `evidence/validation/VALIDATION_REPORT.md` and its linked JSON records. Positive witnesses are bound to original graphs and requested restrictions. Count controls and the four B2 pairs have only their stated finite meaning. They do not prove a new supplier family.

The [current literature note](../docs/LITERATURE_UPDATE.md) records the author-posted subcubic Lean archive, almost-graceful asymptotics and graceful supertree construction with their exact inspection limits. All three small pilot profiles fall within the subcubic archive's stated ordinary-gracefulness scope; the prescribed interval/port condition is an additional question. The source was inspected, not locally rebuilt in Lean. No exhaustive worldwide novelty or status audit is claimed.

## 11. Promotion criteria

New findings must name their quantifiers/domain, independent inputs, unchanged original topology, returned physical interface, proof/verification evidence, applicable sources and remaining dependencies. Universal coverage requires a coverage and termination argument, not a large finite record. Keep unproved candidate statements in proof obligations and preserve failed attempts in the failure ledger.
