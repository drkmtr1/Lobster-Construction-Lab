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

## B3-UNPADDED-K1-001 and the all-K corollary

**ACCEPT** for all positive integers `q,r,t` on the exact original zero-padding profile `[[q],[r],[t],[],[]]`. The named formula gives an alpha graceful labeling. The prefix supplies `R={q+2}`, `D={t+3}`, and physical `s:3=q+t+5`, and the original `s:3--s:4` edge consumes the singleton resources. The proof is a project corollary of retained R241 and L008 with a directly proved left component and an explicitly proved last-vertex extension of the right component. Separate AI reviewers accepted the mathematics and implementation. [Proof](B3_UNPADDED_K1.md) · [Validation](../evidence/validation/B3_UNPADDED_K1_001/README.md) · D027

For every positive integer `q,r,t,K`, the exact original unpadded profile `[[q],[r],[t]]+[[]]*(K+1)` admits a graceful labeling. Select the direct singleton for K=1 and the accepted four-case rule for K>=2. The branches retain distinct resource contracts and consumers, including the earlier adjacent branch on its original domain. This corollary establishes ordinary gracefulness for the stated family. Padding, multiple positive branches per section, further sections, and arbitrary repetition remain separate.

## B4-UNPADDED-UNIT-001

**ACCEPT** for the exact original `[[1],[1],[1],[1]]+[[]]*(K+1)` profile with integer K>=1, excluding booleans. A fixed R241 seed with a directly proved left component and class-reflected L008 right component supplies the shifted prefix. Its unused labels and differences are `[6,K+5]` and `1..K`, with the actual above-side adjacent port `s:4=K+6`. The retained consumer completes the named path. The full labeling is alpha with low-class size `6+(K+1)//2`. Separate AI reviewers accepted the proof and implementation. Evidence includes one separate fixed seed and 12 completed targets, audited on those same saved targets. Other branch sizes on four sections, padding, extra branches, further sections and arbitrary repetition remain separate proof duties. [Proof](B4_UNPADDED_UNIT.md) · [Validation](../evidence/validation/B4_UNPADDED_UNIT_001/README.md) · D028

## 10. Finite validation and current literature

The authoritative executed results are in `evidence/validation/VALIDATION_REPORT.md` and its linked JSON records. Positive witnesses are bound to original graphs and requested restrictions. Count controls and the four B2 pairs have only their stated finite meaning. They do not prove a new supplier family.

The [current literature note](../docs/LITERATURE_UPDATE.md) records the author-posted subcubic Lean archive, almost-graceful asymptotics and graceful supertree construction with their exact inspection limits. All three small pilot profiles fall within the subcubic archive's stated ordinary-gracefulness scope; the prescribed interval/port condition is an additional question. The source was inspected, not locally rebuilt in Lean. No exhaustive worldwide novelty or status audit is claimed.

## 11. Promotion criteria

New findings must name their quantifiers/domain, independent inputs, unchanged original topology, returned physical interface, proof/verification evidence, applicable sources and remaining dependencies. Universal coverage requires a coverage and termination argument, not a large finite record. Keep unproved candidate statements in proof obligations and preserve failed attempts in the failure ledger.

## B4-UNPADDED-111T-001

**ACCEPT** for the exact zero-padding profile `[[1],[1],[1],[t]]+[[]]*(K+1)`
with integers `t>=2,K>=1`, excluding booleans. At K=1 the direct singleton
uses `R={4}`, `D={t+3}`, and `s:4=t+7`; the complete labeling is alpha
with low-class size t+6. For K>=2 set a=t+5. The shifted seed supplies
`R=[a,a+K-1]` and `D=[1,K]` at physical `s:4=a+K+1`. The retained
nonadjacent consumer completes the original path. The full K>=2 claim is
ordinary gracefulness. The R241 and L008 derivations use the actual
`s:2--s:3` join with two directly verified left components. The unit
route retains its adjacent contract and alpha conclusion for t=1, giving
ordinary-gracefulness coverage for all positive t,K on this exact profile.
Separate AI mathematical and implementation reviews accepted. There are
12 completed original targets and an audit of those same 12, with two
left-component certificates counted separately. [Proof](B4_UNPADDED_111T.md)
· [Validation](../evidence/validation/B4_UNPADDED_111T_001/README.md) · D029

## B4-UNPADDED-1121-001

**ACCEPT** for the exact unpadded `[[1],[1],[2],[1]]+[[]]*(K+1)` profile
with integer K>=1, excluding booleans. An explicit extension of the
B4-111T left component puts `l:2:0:1` at the original `b:2:0`.
R241 restores the original `s:2--s:3` edge to the reflected L008
right component and yields a 14-vertex seed with low-class size 6.
Shifting its eight highs leaves `R=[6,K+5]`, `D=[1,K]`, and actual
`s:4=K+6`. The adjacent consumer labels the original suffix and the
complete alpha low-class size is `6+(K+1)//2`. Separate AI
mathematical and implementation reviews accepted. The 12 original
targets passed and their same-certificate audit passed. The left
component and the fixed seed each have a separate certificate.
[Proof](B4_UNPADDED_1121.md) · [Validation](../evidence/validation/B4_UNPADDED_1121_001/README.md) · D030

## B4-UNPADDED-1211-001

**ACCEPT** for the exact zero-padding `[[1],[2],[1],[1]]+[[]]*(K+1)`
profile for integer K>=1, excluding booleans. Two within-class
exchanges and a prescribed leaf at `b:1:0` supply the left component
with exit offset one. R241 restores the original `s:2--s:3` edge
to reflected L008, producing the 14-vertex seed with low-class size
7. Shifting its highs supplies `R=[7,K+6]`, `D=[1,K]` and actual
`s:4=K+7`. The retained adjacent completion gives a full alpha
low-class size `7+(K+1)//2`. Separate AI reviews accepted. The 12
completed certificates and their same-target audit passed. The
relabeled and expanded components and the fixed seed have separate
certificates. [Proof](B4_UNPADDED_1211.md) · [Validation](../evidence/validation/B4_UNPADDED_1211_001/README.md) · D031

## B4-UNPADDED-2111-001

**ACCEPT** for integer K>=1, excluding booleans, on the exact
ordered zero-padding profile `[[2],[1],[1],[1]]+[[]]*(K+1)`.
Extending the fixed R241/L008 unit skeleton at physical `b:0:0=0`
adds the edge to `l:0:0:1=13` and leaves both port identities
intact. The shifted prefix distinguishes root label m-1 and
new leaf label m. It supplies `R=[6,K+5]`, `D=[1,K]`, and physical
`s:4=K+6`. The retained adjacent consumer gives an alpha completion
with low-class size `6+(K+1)//2` and cutoff one less. Separate AI
reviews accepted. The 12 original targets, their same-certificate
audit and one separate fixed seed certificate passed.
[Proof](B4_UNPADDED_2111.md) · [Validation](../evidence/validation/B4_UNPADDED_2111_001/README.md) · D032

## Conditional zero-port extension and B4-UNPADDED-3111-001

**ACCEPT.** From an independently supplied witnessed alpha state
A(n,p0;0,y), any finite number h>=0 of prescribed fresh leaves may
be appended at the same physical label-zero port, preserving old
labels, both ports, offsets and the witness. Their labels and new
differences are n..n+h-1. The high-side shift reserves the two
path inventories. Adjacent completion applies at y=0 on the
actual original K-edge path and gives low-class size p0+ceil(K/2).

From the retained unit seed this proves the exact zero-padding
`[[q],[1],[1],[1]]+[[]]*(K+1)` family alpha graceful for all integers
q,K>=1, with p0=6 and actual port s:4=K+6 after the shift.
The general-q result is symbolic. The only new executable route
is the exact q=3 construction, `four_section_3111(K)`, for integers
K>=1 excluding booleans. The 12 declared targets, audit of those same
certificates, and one separately recorded seed passed. Separate
AI mathematics and implementation reviews accepted.
[Lemma and corollary](ALPHA_ZERO_PORT_LEAF_EXTENSION.md) ·
[3111 proof](B4_UNPADDED_3111.md) · [Validation](../evidence/validation/B4_UNPADDED_3111_001/README.md) · D033

## Conditional minimum-high extension and B4-UNPADDED-1311-001

**ACCEPT.** For a supplied witnessed alpha state A(n,p;x,y), prescribed
fresh leaves at the same actual minimum-high host within one edge of
the witness give A(n+h,p+h;x,y) for each integer h>=0. The ports and
witness are preserved, including under finite ordered batches.
The h=1 insertion appears in the retained 1211 left component.

Minimum-high extension in the left component before R241 and
zero-port extension at the returned first center after composition
prove alpha gracefulness of `[[q],[r],[1],[1]]+[[]]*(K+1)` for
all positive integers q,r,K. The actual adjacent port is
`s:4=K+r+5` and completed low-class size is r+5+ceil(K/2).
New executable coverage is only `four_section_1311(K)` for
positive integer K, excluding booleans. Twelve original targets
and their same-certificate audit passed. One expanded left component
and one fixed prefix seed passed separately. Separate AI reviews accepted.
[Proofs](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md) · [1311 proof](B4_UNPADDED_1311.md)
· [Validation](../evidence/validation/B4_UNPADDED_1311_001/README.md) · D034

## Conditional upper-block insertion and B4-UNPADDED-QR21-001

**ACCEPT.** At a supplied label-one host within one edge of the
witness, the upper-block insertion preserves both ports and their
offsets. It requires all incident differences on the selected
high block to be [c-1,n-1] with multiplicity one. After h prescribed
additions the threshold is c+h, selecting the same physical block with
the updated complete incident multiset. This gives finite same-host
closure with the extra predicate retained.

The original relabeled nine-vertex left graph supplies the
predicate at c=7. Upper-block growth, minimum-high extension,
the original R241/L008 join and zero-port extension in that order
prove the exact unpadded `[[q],[r],[t],[1]]+[[]]*(K+1)` family
alpha graceful for positive integers q,r,t,K. Completed low-class
size is r+5+ceil(K/2). Only the t=2 route
`four_section_qr21(q,r,K)` was added and finitely validated.
All 12 declared targets, their same-certificate audit, and three
separate auxiliary certificates passed. Separate AI reviews accepted.
[Insertion and symbolic proof](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md)
· [QR21 proof](B4_UNPADDED_QR21.md) · [Validation](../evidence/validation/B4_UNPADDED_QR21_001/README.md) · D035

## B4-FOURTH-2-SUPPLY-001

**ACCEPT.** With low entrance s:3=1 the exact five-vertex right
component cannot supply either allowed high exit. States
A(5,3;2,0) and A(5,3;0,1) exist on the same original graph.
The retained left exit offset one is incompatible with this
right component under the unchanged R241 rule.

The direct witnessed A(14,7;1,0) seed supplies the complete
upper-block predicate at c=12. Prescribed first leaves at the
label-one center preserve that predicate and port offsets.
The original adjacent suffix gives alpha gracefulness for
`[[q],[1],[1],[2]]+[[]]*(K+1)` for positive integers q,K.
The only new executable route is `four_section_q112(q,K)`.
Twelve original certificates and their same-target audit
passed, with one separate 14-vertex seed in the completed run.

The four restricted first-witness DFS queries on the exact
1212 and 1122 prefixes each found a verified finite candidate.
There are two above-side offsets per target and no exact solution
counts. These diagnostics leave arbitrary (q,r,t,2) supply open.
[Proof](B4_FOURTH_2_SUPPLY.md) · [Validation](../evidence/validation/B4_FOURTH_2_SUPPLY_001/README.md)
· [Diagnostics](../evidence/validation/B4_FOURTH_2_SUPPLY_001/DIAGNOSTICS.md) · D036

## B4-UNPADDED-QR12-001

**ACCEPT** the conditional lower-block insertion, including same-host
finite closure with fixed threshold and descending fresh-name
assignment. The full supplied incident multiset, physical ports
and witness are part of its hypotheses.

The explicit 1212 labeling and both incident predicates discharge
the initial hypotheses. Second-branch growth followed by first-branch
upper-block growth gives the exact ordered family
`[[q],[r],[1],[2]]+[[]]*(K+1)` for positive integers q,r,K,
using Q112 at r=1. Its adjacent s:4 consumes R=[r+6,K+r+5]
and D=[1,K], with completed alpha low size r+6+ceil(K/2).
Twelve declared completed targets and the same-target audit passed,
with one separate 1212 seed. Two separate AI reviews accepted the
corrected proof and implementation. General (q,r,t,2) remains open.
[Conditional rule](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
· [Family proof](B4_UNPADDED_QR12.md)
· [Evidence](../evidence/validation/B4_UNPADDED_QR12_001/README.md) · D037

## B4-THIRD-ZERO-HOST-SEED-001

**ACCEPT** the fixed-low obstruction on the exact original
`[[1],[1],[t],[2],[]]` prefix for all integers t>=3 with the
retained seven named lows, the alpha cut, and adjacent physical
s:4=7. The other highs start free. The spectrum forces the root
and rules out difference M-2, where M=t+12.

**ACCEPT, conditional** the arithmetic of maximum-label leaf
extension at a supplied zero host within one edge of the actual
witness. The two physical ports and offsets are preserved whether
or not the host is the low port. Ordered batches agree pointwise.

**ACCEPT, restricted computation** the zero count for one
exhausted named 1122 alpha DFS at b:2:0=0 and s:4=7. All other
labels were free within their classes. The run visited 17,514
nodes without reaching a limit. The independent audit checked
the original, retained control and receipt. It added zero
queries. The query supplied no new seed, so there is no new
all-t,K theorem or direct completed target. Other suppliers
remain open.
[Proof and scope](B4_THIRD_ZERO_HOST_SEED.md)
· [Conditional extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
· [Evidence](../evidence/validation/B4_THIRD_ZERO_HOST_SEED_001/README.md) · D038

## B4-THIRD-ZERO-HOST-NONADJACENT-001

**ACCEPT** the fixed explicit 1122 seed and its original-edge
ledger. One exact first-witness DFS at b:2:0=0 and s:4=8
returned SAT after 2,368 nodes, with count null and lower bound
one. The normalized seed gives A(15,7;4,1) at physical
b:0:0 and s:4. Its zero host is distinct from its low port
and one edge from the supplied witness.

**ACCEPT** ordinary gracefulness for the exact original
`[[1],[1],[t],[2]]+[[]]*(K+1)` for integers t>=2,K>=2.
The zero-host extension, high shift and retained recurrence
use the actual s:4 path and both inventories. The K=2
suffix (10,8,7) rules out a blanket alpha claim. This exact
resource interface fails at K=1. The retained t=1 and
adjacent t=2 evidence keep their existing scope.

One retained control was rechecked. Four declared direct
targets passed and the independent audit of those same
four added zero targets or queries. Separate AI reviews
accepted. No public route was added.
[Proof and scope](B4_THIRD_ZERO_HOST_NONADJACENT.md)
· [Evidence](../evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001/README.md) · D039

## B4-THIRD-ZERO-HOST-K1-001

**ACCEPT** the single derived complete control on the original
`[[1],[1],[2],[2],[],[]]`. The retained adjacent prefix was
lifted by shifting its highs by one and assigning the actual
s:5=7. The control is graceful and has b:2:0=2.

**ACCEPT, conditional** the ordinary zero-host extension
arithmetic, including the named K=1 leaf formula 14+j and
singleton resource transport if a complete zero-host seed
is supplied. The alpha zero-host theorem keeps its own
hypotheses.

**INCOMPLETE** the only complete-target first-witness DFS
with sole pin b:2:0=0. It reached max_nodes at 100,000
nodes with no witness, no exhaustion and no exact count.
The control and receipt passed the arithmetic/custody audit.
It added zero targets or queries. Separate AI reviews
accepted this scope. The one full control certificate
represents one distinct parameter case. There is no
new seed, growth check or combined all-positive theorem.
[Proof and scope](B4_THIRD_ZERO_HOST_K1.md)
· [Evidence](../evidence/validation/B4_THIRD_ZERO_HOST_K1_001/README.md) · D040

## B4-THIRD-ZERO-HOST-K1-DIRECT-001

**ACCEPT** the exact terminal-maximum reduction, physical leaf
transport and reversible 13-vertex core lift. The explicit
supplier gives ordinary gracefulness on `[[1],[1],[t],[2],[],[]]`
for every positive integer t. The singleton is R={5}, D={6}
at s:4=11 and assigning original s:5=5 completes it. The path
(3,4,8) excludes an alpha threshold for this particular labeling.

**ACCEPT** the exhaustive ordinary-gracefulness case split
for `[[1],[1],[t],[2]]+[[]]*(K+1)` at all positive integers t,K.
Use the direct singleton for K=1, Q112 at q=1 for t=1,K>=2,
and the retained nonadjacent zero-host construction for t,K>=2.

One auxiliary core and four completed K=1 originals passed,
including t=2 counted once. The audit, same-target batch and
both separate AI reviews added zero targets or solver queries.
The historical original-bound DFS stays INCOMPLETE at the
node cap. This result is independent direct evidence.
[Proof and selector](B4_THIRD_ZERO_HOST_K1_DIRECT.md)
· [Evidence](../evidence/validation/B4_THIRD_ZERO_HOST_K1_DIRECT_001/README.md) · D041

## B4-UNPADDED-Q1T2-001

**ACCEPT** conditional general low-host upper-block insertion
with the full incident difference multiset [c-a,n-1].
It preserves the actual ports, witness and low size, and
returns threshold c+h and the corresponding full predicate.
Repeated batches in the same name order agree pointwise.

**ACCEPT** pointwise compatibility with growth at a distinct
supplied zero host. In the zero-first order the new zero
leaves join the selected set before the upper shift. In the
upper-first order they enter above the returned threshold.
The final named graphs, labels and incident spectrum agree.

**ACCEPT** ordinary gracefulness of the exact original
`[[q],[1],[t],[2]]+[[]]*(K+1)` for exact integers q>=1,t>=2,K>=2.
The normalized state is A(q+t+12,7;4,1), with threshold q+8
and selected spectrum [q+4,q+t+11]. Its high shift supplies
R=[7,K+6], D=[1,K] at physical s:4=K+8. The actual path
uses the retained recurrence. The K=1 interface restriction
and K=2 alpha-threshold counterexample continue to apply.

Six new completed targets passed. One retained seed recheck,
one retained completed q=1 control and 12 domain rejections
are separate. The same-target comparisons, independent audit,
and two separate read-only AI reviews added zero targets or
solver queries. The historical K1 receipts remain INCOMPLETE.
[Insertion proof](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
· [Family proof](B4_UNPADDED_Q1T2.md)
· [Evidence](../evidence/validation/B4_UNPADDED_Q1T2_001/README.md) · D042

## B4-Q1T2-K1-ROOTED-CORE-001

**REJECT** the fixed retained q=1 labeling's one-leaf single-cut
template at b:0:0=3. Every candidate cut fails its necessary
crossing spectrum. Zero-host growth by fresh maxima is also
unavailable with the original s:2 pinned to the maximum, since
zero must be at a physical neighbor of s:2. These restrictions
leave other graceful relabelings available.

**ACCEPT** the explicit rooted core for each exact integer q>=2
on `[[q],[1],[],[2],[],[]]`. Relabel the retained topology, then
increase the labels of s:0 and s:2 by q-1. Prescribed first
leaves fill between the fixed labels and those two vertices.
The edge partition [1,8], [9,q+7], [q+8,q+11] realizes all
core differences and puts q+11 at the original s:2.

**ACCEPT** the translated core and zero third host for all exact
integers q,t>=2 at K=1 on `[[q],[1],[t],[2],[],[]]`. The
original final edge completes R={5}, D={1} at physical s:4=6
by s:5=5. The singleton difference is derived. With the retained
t=1, q=1 and K>=2 constructions, ordinary gracefulness now
holds on the exact (q,1,t,2) family for all positive q,t,K,
each case with its own interface. The new construction has no
alpha claim.

Four completed originals, three distinct auxiliary cores and
ten domain rejections passed. The same-record independent audit
and two read-only AI reviews added no cases. There were zero
solver queries and zero enumeration. The original historical
DFS remains INCOMPLETE.
[Proof and selector](B4_Q1T2_K1_ROOTED_CORE.md)
· [Evidence](../evidence/validation/B4_Q1T2_K1_ROOTED_CORE_001/README.md) · D043

## B4-UNPADDED-1R22-SUPPLIER-001

**REJECT** the second-center lower-block template on the two
saved 1122 diagnostic ledgers and the distinct third zero-host
ledger. Their complete selected incidence multisets fail for
every allowed threshold. The failure is specific to those
fixed labelings and that insertion premise.

**ACCEPT** the independently supplied normalized alpha state
A(r+14,r+6;r+4,1) on `[[1],[r],[2],[2],[]]` for every exact
integer r>=2. The explicit base puts the maximum at b:1:0 and
zero at its original terminal. Fixed-cut growth preserves the
single maximum incident edge at c=1 and moves the actual low
port to r+4. Finite insertion preserves all named incidences and
the actual witness, and keeps the exit at p+1 for p=r+6.

**ACCEPT** ordinary gracefulness for the exact full profile
`[[1],[r],[2],[2]]+[[]]*(K+1)` for integers r,K>=2. Raising
the normalized highs by K leaves R=[r+6,r+K+5], D=[1,K],
and physical s:4=r+K+7. The unchanged nonadjacent sequence
completes the original K-edge path. The K=1 case remains
outside this interface. The normalized alpha cut is not
claimed for the completed labels.

The four completed cases, three distinct prefixes, two retained
diagnostic rechecks and eight domain rejections passed. The
same-record audit and separate read-only AI reviews add zero
cases. No solver calls, labeling enumeration or production
changes occurred.
[Proof](B4_UNPADDED_1R22_SUPPLIER.md)
· [Evidence](../evidence/validation/B4_UNPADDED_1R22_SUPPLIER_001/README.md) · D044

## B4-1R22-K1-ROOTED-CORE-001

**ACCEPT** the explicit graceful labeling of the exact
`[[1],[],[2],[2],[],[]]` auxiliary core with s:1=0. Its
14 labels and 13 original weights fill their respective
alphabets. The derived s:4=8 and s:5=3 determine the
terminal weight 5.

**ACCEPT** the conditional rooted-core lift and its instantiation
for every exact integer r>=2 on `[[1],[r],[2],[2],[],[]]`.
Translate the rooted core by r, put the maximum r+14 on b:1:0,
and use zero and descending positive labels on the second
terminals. The original attachment has weight 14, followed
by [15,r+13] on nonzero terminals and r+14 on the zero edge.
The direct prefix leaves R={r+3}, D={5}, and actual s:4=r+8
on the sole original edge to s:5.

**ACCEPT** repeatable named second-branch growth and ordinary
gracefulness of the exact (1,r,2,2) family for all positive
integers r,K. Keep the retained r=1 constructions and the
r,K>=2 nonadjacent construction under their own interfaces.
The separate retained-prefix one-step high-shift restriction
keeps its original K=1 scope.

One core certificate and four completed cases passed the
unchanged checker and independent arithmetic audit. Four
invalid inputs were rejected. The same r=4 named comparison
adds zero cases. Separate read-only AI reviews accepted.
There were zero solver queries, computational enumeration
or historical search replays.
[Proof and selector](B4_1R22_K1_ROOTED_CORE.md)
· [Evidence](../evidence/validation/B4_1R22_K1_ROOTED_CORE_001/README.md) · D045

## B4-12T2-ZERO-HOST-SUPPLIER-001

**ACCEPT** the explicit 17-vertex alpha seed on
`[[1],[2],[3],[2],[]]` with Z=b:2:0 at zero. The physical
L=b:0:0 has label 1, U=s:4 has label 9, and the witness
passes through L and the whole prefix spine. The exact
seed state is A(17,8;1,1).

**ACCEPT** the retained zero-host lemma application for
exact integer t>=3, giving A(t+14,8;1,1) with all original
labels preserved and pointwise ordered-batch closure.
For exact t>=3,K>=2 the high shift leaves R=[8,K+7],
D=[1,K] and physical s:4=K+9. The nonadjacent numeric
path sequence proves ordinary gracefulness on the exact
ordered (1,2,t,2) family. Together with the separate
retained t=1 and t=2 interfaces this covers all positive
t at K>=2. The t>=3,K=1 case remains open.

**REJECT** the port-preserving upper-block premise only
on the specified retained 1222 ledger at the actual
third host. At c=14 the counts agree but the spectrum is
{8,12,13,14,15} instead of [11,15].

Three normalized prefixes, four completed targets, one
retained recheck and eight invalid-input probes passed.
The same-record audit, normalized batch comparison and
two separate read-only AI reviews added zero cases. No
solver queries, enumeration or historical replay occurred.
[Proof](B4_12T2_ZERO_HOST_SUPPLIER.md)
· [Evidence](../evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/README.md) · D046

## B4-12T2-K1-ROOTED-CORE-001

**ACCEPT** the conditional ordinary crossing-cut leaf insertion.
When the complete crossing spectrum is [b-c+1,m], raising
the upper labels by h and supplying the named leaves at the
upper host gives a graceful labeling. The raised cut retains
old crossing edges and adds precisely the new leaf edges.
Physical labels follow the actual shift, and ordered finite
batches agree pointwise.

**ACCEPT** the single insertion on the retained rooted core
`[[1],[1],[],[2],[],[]]`. Its six crossing edges at cut 2 use
[7,12]. Adding l:1:0:1 at label 2 yields the exact 14-vertex
`[[1],[2],[],[2],[],[]]` core with physical s:2=13 and
complete crossing spectrum [7,13] at cut 3. Counting all
upper incidences is rejected on the retained core.

**ACCEPT** the conditional and instantiated lift for integer
t>=3 at K=1 on the exact original `[[1],[2],[t],[2],[],[]]`.
The translated core and restored third branch leave R={6},
D={6} at physical s:4=12 and complete with s:5=6. Named
third-leaf growth preserves every earlier assignment. The
four-case selector with the retained branches proves ordinary
gracefulness of the exact (1,2,t,2) family for all positive
integers t,K.

One retained recheck, one new core and four completed
targets passed, with four invalid probes rejected. Both
read-only AI reviews accepted. The same-record audit and
t=5 batch comparison add zero cases. No solver, enumeration
or historical replay ran.
[Insertion lemma](ORDINARY_CUT_LEAF_INSERTION.md)
· [Lift and selector](B4_12T2_K1_ROOTED_CORE.md)
· [Evidence](../evidence/validation/B4_12T2_K1_ROOTED_CORE_001/README.md) · D047

## B4-1R32-MINIMUM-HIGH-SUPPLIER-001

**ACCEPT** the retained 1232 seed as a supplied
minimum-high instance at actual b:1:0=8, one edge from
the witness. Its third center stays zero. The extension
adds only the named second leaves, keeping the old lows
and shifting the old highs. At fixed third size three,
the normalized state is A(r+15,r+6;1,1) for exact integer
r>=3, with finite named batch closure at the same host.

**ACCEPT** the updated shift and original nonadjacent
path completion for exact r>=3,K>=2 on
`[[1],[r],[3],[2]]+[[]]*(K+1)`. The resources are
R=[r+6,r+K+5], D=[1,K] and physical s:4=r+K+7.
Together with the retained r=1 and r=2 routes this
gives ordinary gracefulness for the exact (1,r,3,2)
family over all positive r at K>=2. The r>=3,K=1
singleton is outside this route.

**REJECT** using the seed's cut 8 in the final shift.
That fixed transformation keeps the fresh edge weights
[1,r-2] assigned and violates the required inventories.

One retained recheck, three new normalized prefixes,
four completed targets and eight invalid-input probes
passed. The audit and same-prefix comparison add zero
cases. Separate read-only AI reviews accepted, with
zero solver calls, labeling enumeration or historical
search replays.
[Proof](B4_1R32_MINIMUM_HIGH_SUPPLIER.md)
· [Evidence](../evidence/validation/B4_1R32_MINIMUM_HIGH_SUPPLIER_001/README.md) · D048

## B4-1R32-K1-ROOTED-CORE-001

**ACCEPT** the ordinary core `[[1],[r],[],[2],[],[]]`
for exact integer r>=3, with physical s:2=r+11.
The retained 14-vertex core supplies the complete
crossing premise at cut 3. The new core returns cut
r+1 with crossings [7,r+11] and noncrossings [1,6].

**ACCEPT** the fixed-third-size-three lift and direct
K=1 singleton on `[[1],[r],[3],[2],[],[]]`. It leaves
R={r+4}, D={6} at physical s:4=r+10 and assigns
s:5=r+4 on the sole crossing edge. The full graceful
labeling returns cut r+2 with crossings [7,r+15]
and noncrossings [1,6]. Finite same-host growth on
the core and the full target agrees pointwise in either
order with the lift, including the prescribed leaf names.

**ACCEPT** the exact ordinary-gracefulness selector
for (1,r,3,2) over all positive integers r,K. The
retained r=1 and r=2 singletons and three K>=2
nonadjacent cases retain their own interfaces.
Simultaneous arbitrary second and third sizes remain open.

One retained core, three new cores, three completed targets
and four invalid-input probes passed. Same-record comparisons,
the audit and two read-only AI reviews added zero cases.
No solver, enumeration, replay or production edits.
[Proof](B4_1R32_K1_ROOTED_CORE.md)
· [Evidence](../evidence/validation/B4_1R32_K1_ROOTED_CORE_001/README.md) · D049

## B4-1RT2-TWO-HOST-COMPATIBILITY-001

**ACCEPT** conditional compatibility of minimum-high and zero-host
leaf growth on one supplied witnessed alpha state. Every finite
interleaving with prescribed names yields the same named labeling
and incidences and preserves both host predicates, actual ports,
offsets and witness.

**ACCEPT** A(r+t+12,r+6;1,1) on the exact normalized (1,r,t,2)
prefix for exact integers r>=3,t>=4, and ordinary original-path
completion for K>=2. The shifted prefix leaves R=[r+6,r+K+5]
and D=[1,K] at physical s:4=r+K+7. The disjoint selector gives
ordinary gracefulness of the exact family for all positive r,t
at K>=2. The K=1 corner r>=3,t>=4 requires separate supply.

**REJECT** extending the old third-terminal formula to index 3,
because it duplicates s:2. Use the proved piecewise formula.

Four retained normalized controls, three new normalized prefixes,
four new completed targets and twelve invalid-input probes passed.
Both separate AI reviews accepted. The same-record audit and five
route and subdivision comparisons add zero graph cases. No solver,
enumeration, historical replay or production change.
[Lemma](ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md)
· [Family proof](B4_1RT2_TWO_HOST_COMPATIBILITY.md)
· [Evidence](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/README.md) · D050

## B4-1RT2-K1-DIRECT-SINGLETON-001

**ACCEPT** the direct singleton and ordinary gracefulness of
`[[1],[r],[t],[2],[],[]]` for exact integers r>=3,t>=4. The
independently supplied maximum-rooted core translates by one.
The restored third center is zero, its attachment has weight
r+12, and its terminal edges have weights [r+13,r+t+12].
The original s:4=r+10 leaves R={r+4}, D={6}, consumed by
s:5=r+4 on the sole unfinished edge.

**ACCEPT** finite named third growth and restricted ordinary
two-host compatibility on these completed states. At cut r+2
the full crossing and noncrossing spectra are [7,r+t+12] and
[1,6]. Second-host crossing-cut insertion and third zero-host
growth preserve both premises and agree pointwise under finite
interleavings with the prescribed leaf orders.

**ACCEPT** the seven-case selector for ordinary gracefulness of
the exact ordered (1,r,t,2) family for all positive integers r,t,K.
Its separate cases retain their own boundary contracts.

Three retained cores, one retained completed control and four
new completed targets passed, with eight pre-expansion domain
rejections and one wrong-digest rejection. Both read-only AI
reviews and the same-record audit accepted the bounded checks.
Batch comparisons and the adverse check add no graph cases. No
solver, enumeration or replay ran.
[Proof](B4_1RT2_K1_DIRECT_SINGLETON.md)
· [Evidence](../evidence/validation/B4_1RT2_K1_DIRECT_SINGLETON_001/README.md) · D051

## B4-1342-UPPER-BLOCK-OBSTRUCTION-001

**ACCEPT** the retained named alpha states and complete incidence
checks. With H=b:0:0=1 and U=s:4=10, the fixed 1342 thresholds
11..18 have selected-edge counts 13,10,8,7,6,5,4,1 against
required 9,8,7,6,5,4,3,2. The retained 1122 positive control
with H=4, U=8 and c=9 supplies the ten weights [5,14].

**ACCEPT** the necessary difference-sum condition. Every
affected original edge gains h and the new edges run from
c-1 through c+h-2. The excess sum is h*(s_c+c-20).
**REJECT** the exact fixed-ledger first-branch operation at
all permitted thresholds and every positive integer h.
Supply by another labeling or interface remains open.
The existing all-positive (1,r,t,2) theorem stays in scope.

Two retained rechecks and one new attempted original give
three distinct graph records. Eight one-leaf assignments on
the same original were correctly rejected. Five invalid
threshold values were rejected before evaluating incidences.
Independent audit and separate AI reviews added zero cases.
No solver, labeling enumeration or historical replay ran.
[Proof](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)
· [Evidence](../evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/README.md) · D052

## B4-1342-ALL-LEDGER-PINNED-OBSTRUCTION-001

**ACCEPT A.** For any normalized graceful alpha labeling of
`[[1],[3],[4],[2],[]]` with low labels [0,8], high labels
[9,18] and b:0:0=1, b:2:0=0, s:4=10, the complete selected
edge count s_c differs from 20-c at every c=11..18.
The first two thresholds have minimum degrees 13 and 10.
At c>=13 equality would select degree-two s:0 and exclude
s:2. Descending from the maximum difference then forces
every selected high vertex to be a terminal at the pinned
zero. That contradicts selection of s:0.

**ACCEPT B.** The signed edge-sum defect h*(s_c+c-20) is
nonzero for every exact integer h>=1. **REJECT** the exact
prescribed port-preserving insertion throughout this pinned
class. The class contains the retained 1342 certificate.
This supersedes the proposed three-pin relabeling direction,
while preserving the separate fixed-ledger evidence and
the accepted all-positive (1,r,t,2) theorem.

The two retained originals, including the 1122 positive
spectrum [5,14], passed. The same-record audit verified
eight structural threshold cases and five guard rejections.
No new graphs, assignments, solver queries, labeling
enumeration or historical replay occurred.
[Proof](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)
· [Evidence](../evidence/validation/B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION_001/README.md) · D053

## B4-1342-RELAXED-HOST-SEED-001

**ACCEPT** the necessary structural prefilter and exact edge-band
equivalence. The degree excess is a, s:2 must be selected, and
unselected zero-neighbor labels fit below c-a with 10 unavailable.
The three checks exclude 33 of the 56 a=2..8,c=11..18 pairs.

**EXHAUSTED RESTRICTED NEGATIVE.** One exact task-local DFS
exhausted all 23 survivors and 68 named subsets on the original
1342 graph at b:2:0=0 and s:4=10, with low classes [0,8] and
high classes [9,18] and full selected spectrum [c-a,18].
It used 13,171 assignment nodes and 1.109 cooperative seconds
without hitting either cap. This is a reviewed implementation
exhaustion result for the exact predicate under those pins.
No witness exists within that scope. The prior label-one
obstruction and all-positive (1,r,t,2) construction are preserved.

Both retained controls rechecked, including [5,14] on 1122.
Ten invalid inputs were rejected before search. Two separate
AI reviews and the independent audit added no graph cases or
searches. With no seed, the conditional transport and the
two optional graph checks did not run.
[Prefilter proof](B4_1342_RELAXED_HOST_SEED.md)
· [Result and coverage](B4_1342_RELAXED_HOST_SEED_RESULT.md)
· [Evidence](../evidence/validation/B4_1342_RELAXED_HOST_SEED_001/README.md) · D054

## B4-1342-U9-STRUCTURAL-OBSTRUCTION-001

**ACCEPT** the analytic obstruction on exact named 1342 with
alpha labels [0,8] and [9,18], b:2:0=0, physical s:4=9,
host a=2..8 and c=10..18. The degree excess, forced labels
and zero-neighbor edges reduce 63 pairs to six unique named
selected sets. Each contradicts its required difference band.

**ACCEPT** that the operation requires the complete selected
spectrum [c-a,18] for every positive h, including a fresh band
extending above 18. **REJECT** the prescribed first-host
upper-block insertion throughout this exact domain. Alpha
existence without the insertion predicate remains outside the
proof. The all-positive (1,r,t,2) theorem remains accepted.

The two retained controls, all six residual cases and 15
invalid-input probes passed independent arithmetic audit.
There were zero new graphs, insertion attempts, solver
queries, graceful-labeling enumerations or historical replays.
[Proof](B4_1342_U9_STRUCTURAL_OBSTRUCTION.md)
· [Evidence](../evidence/validation/B4_1342_U9_STRUCTURAL_OBSTRUCTION_001/README.md) · D055

## B4-1342-U9-A1-ANALYTIC-CLOSEOUT-001

**ACCEPT Claims A and B.** For the exact named 1342 graceful
alpha domain with bands [0,8] and [9,18], physical b:2:0=0,
b:0:0=1 and s:4=9, the selected incidence count cannot be
20-c at any integer c=10..18. The first three thresholds
fail the degree bound. All later ones force s:0 and exclude
s:2, contradicting the descent through the original zero-host
differences. The necessary spectrum [c-1,18] therefore fails
and the prescribed operation fails for every positive batch.

The combined rejected domain has exact host labels a=1..8
at physical s:4=9 (analytic) and s:4=10 (analytic at a=1,
reviewed predicate exhaustion at a=2..8 with analytic batch
necessity). This disposition concerns the specified operation
and pins. The ordinary all-positive (1,r,t,2) construction
remains accepted.

Nine thresholds and both retained originals passed the
independent arithmetic audit and separate AI reviews. Zero
new profiles, queries, labeling enumeration or historical
replay. [Proof](B4_1342_U9_A1_ANALYTIC_CLOSEOUT.md)
· [Evidence](../evidence/validation/B4_1342_U9_A1_CLOSEOUT_001/README.md) · D056

## B4-JOINT-MAX-ROOTED-CORE-PILOT-001

**ACCEPT** the two retained comparison cores and their
complete original-edge ledgers. Neither fixed labeling
supplies one-leaf crossing-cut insertion at its other
physical branch center at any cut. **REJECT** those two
exact transfers. Their failure concerns the stated operation.

**INCOMPLETE** for the exact named `[[2],[2],[],[2],[],[]]`
core with sole pin s:2=14 and ordinary graceful differences.
The sole first-witness DFS stopped at max_nodes=100,000
after about 0.774 seconds, with no witness and no exhaustion.
The two possible zero neighbors s:1 and s:3 remained in the
query. Feasibility is open. The conditional t=2 lift and
joint-growth assessment were not activated.

The independent arithmetic audit checked three graph records
and added no query. No repeat or historical replay occurred.
[Proof](B4_JOINT_MAX_ROOTED_CORE_PILOT.md)
· [Evidence](../evidence/validation/B4_JOINT_MAX_ROOTED_CORE_PILOT_001/README.md) · D057
