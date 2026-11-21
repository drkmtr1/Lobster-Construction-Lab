# B2-UNEQUAL-SEED-001: independent review of the seed falsifier

**Disposition (final, filled at close):** exhausted restricted negative — the proposed seed does not exist under exactly the declared restrictions. Analytic obstruction confirmed; bounded DFS and direct-permutation oracle both exhausted with 0 solutions; separate reviewer challenge with no unresolved objections. See section 8.
**Task owner:** `research/NEXT_TASK.md`. **Baseline:** session start commit `6d0f8d2` (working tree clean); baseline tag `lcl-v0.1.0-baseline` → `36ea1603` (its parent), untouched.
**Scope:** one named eight-vertex auxiliary target, one declared restriction set, one bounded DFS run, one direct-permutation oracle run, one independent analytic review. No successor search is launched from this note.

## 1. Exact target and restrictions

Profile `[[1],[2],[]]` (eight vertices, seven edges, `m=7`), the prefix through `s:2` of the unequal B2 family `q=1,r=2,z0=z1=0` with no appended path. Actual original edges:

1. `s:0 -- s:1`
2. `s:0 -- b:0:0`
3. `b:0:0 -- l:0:0:0`
4. `s:1 -- b:1:0`
5. `b:1:0 -- l:1:0:0`
6. `b:1:0 -- l:1:0:1`
7. `s:1 -- s:2`

Restrictions (all deliberate and explicit; encoded in `examples/unequal_seed_pins.json` and `examples/unequal_seed_domains.json`):

- Low side A = `s:1, b:0:0, l:1:0:0, l:1:0:1` bijectively labeled `0..3`.
- High side B = `s:0, b:1:0, l:0:0:0, s:2` bijectively labeled `4..7`.
- Physical port pin `h(s:2) = 4`.
- No further root pin, no complement quotient, no branch-symmetry assumption, no automorphism quotient.

Every edge joins one A-vertex to one B-vertex (edges 1,2,4,7 from the table above; 3,5,6 likewise), so for any admissible assignment every edge difference equals `high label − low label` with high ≥ 4 and low ≤ 3; no absolute-value ambiguity is possible.

The constrained candidate space is `4! · 3! = 144` named assignments after the pin; the declared DFS limit is 10,000 attempted assignments, 2.0 s cooperative, one worker, eight vertices; the oracle uses the same caps as its permutation cap.

## 2. The proposed analytic obstruction (as received)

Let `a=h(s:0)`, `b=h(b:1:0)`, `c=h(l:0:0:0)`, `x=h(b:0:0)`.

1. Alpha separation and the required difference 1 force `h(s:1)=3`.
2. The three other high labels permute `{5,6,7}`; the remaining low labels permute `{0,1,2}`.
3. Summing the seven original-edge differences gives `a+2b−x=18`.
4. The only admissible triples `(a,b,x)` are `(5,7,1)`, `(6,7,2)`, `(7,6,1)`.
5. Each triple duplicates difference 4 on two actual original edges.

## 3. Independent recomputation (researcher role, this session)

**Step 1.** The seven differences must be exactly `{1,...,7}`, so difference 1 occurs. With `h(s:2)=4`, the vertices `s:0,b:1:0,l:0:0:0` carry `{5,6,7}`. Every edge except `s:1--s:2` joins one of these three vertices (high ≥ 5) to a low vertex (≤ 3), hence has difference ≥ 2. Only `s:1--s:2` can carry difference 1: `4 − h(s:1) = 1`, so `h(s:1) = 3`. Confirmed.

**Step 2.** By the domain bijections: `{a,b,c} = {5,6,7}` with `a+b+c = 18`, and with `y := h(s:1) = 3` the remaining low labels `{x, u, v} = {h(b:0:0), h(l:1:0:0), h(l:1:0:1)}` permute `{0,1,2}` with `x+u+v = 3`. Confirmed.

**Step 3.** The per-edge differences (high − low, signs fixed by the cut):

| Edge | Difference |
|---|---|
| `s:0--s:1` | `a−y` |
| `s:0--b:0:0` | `a−x` |
| `b:0:0--l:0:0:0` | `c−x` |
| `s:1--b:1:0` | `b−y` |
| `b:1:0--l:1:0:0` | `b−u` |
| `b:1:0--l:1:0:1` | `b−v` |
| `s:1--s:2` | `4−y` |

Sum `= 2a + 3b + c − 3y − 2x − u − v + 4` (degree coefficients: on the high side, `s:0`:2, `b:1:0`:3, `l:0:0:0`:1, and `s:2`:1, whose fixed pin label 4 is the displayed `+4` constant; on the low side, `b:0:0`:2, `s:1`:3, and the two terminal leaves `l:1:0:0` and `l:1:0:1` at degree 1 each. The displayed sum and the identity below are unchanged by this descriptive correction — see the section 9 review addendum). Substituting `y=3` and `u+v = 3−x`: sum `= 2a+3b+c − 9 − 2x − (3−x) + 4 = 2a+3b+c − x − 8`. Using `a+b+c = 18`: sum `= a + 2b + 10 − x`. Setting the sum equal to `1+...+7 = 28` gives `a + 2b − x = 18`. Confirmed.

**Step 4.** Case split on `b ∈ {5,6,7}` (with `a−x = 18−2b`):

- `b=5`: `a−x = 8`; but `a ≤ 7` and `x ≥ 0` give `a−x ≤ 7`. No solution.
- `b=6`: `a−x = 6`; `a=5 ⇒ x=−1` impossible; `a=7 ⇒ x=1`, `c=5`. Triple `(7,6,1)`.
- `b=7`: `a−x = 4`; `a=5 ⇒ x=1`, `c=6`; `a=6 ⇒ x=2`, `c=5`. Triples `(5,7,1)`, `(6,7,2)`.

Exactly the three claimed triples; no other case exists because `b` is exhausted. Confirmed.

**Step 5.** Full difference lists for each triple (`u,v` range over the two remaining low labels; both orderings listed). Corrections from the section 4 review are marked *(reviewer correction)*.

- `(a,b,c,x) = (5,7,6,1)`, `(u,v) ∈ {(0,2),(2,0)}`: differences `2,4,5,4,7,5,1` or `2,4,5,4,5,7,1`. Difference 4 occurs twice (edges `s:0--b:0:0`, `s:1--b:1:0`), and *(reviewer correction)* difference 5 also occurs twice (edge `b:0:0--l:0:0:0` with `c−x=5`, and the `b:1:0` leaf carrying label 2 with `7−2=5`), in both orderings. Duplicate.
- `(6,7,5,2)`, `(u,v) ∈ {(0,1),(1,0)}`: differences `3,4,3,4,7,6,1` or `3,4,3,4,6,7,1`. Difference 4 occurs twice (edges `s:0--b:0:0`, `s:1--b:1:0`), and difference 3 also occurs twice (edges `s:0--s:1`, `b:0:0--l:0:0:0`), in both orderings. Duplicate.
- `(7,6,5,1)`, `(u,v) ∈ {(0,2),(2,0)}`: differences `4,6,4,3,6,4,1` or `4,6,4,3,4,6,1`. *(Reviewer correction)* difference 4 occurs **three** times, unconditionally: edges `s:0--s:1` (`a−y=4`) and `b:0:0--l:0:0:0` (`c−x=4`), plus always one of the two `b:1:0` leaf edges, because with `x=1` and `y=3` fixed the remaining low labels `{u,v}={0,2}` both sit at those leaves and the leaf carrying 2 gives `6−2=4`. *(Reviewer correction)* difference 6 also occurs twice (edge `s:0--b:0:0` with `a−x=6`, and the `b:1:0` leaf carrying label 0 with `6−0=6`), in both orderings. Duplicate.

In every admissible triple, difference 4 occurs on at least two actual original edges, while a graceful labeling requires each difference in `1..7` exactly once. **Conclusion of the analytic argument: the restricted seed does not exist.** The proposed argument is correct in every step as stated; the independent recomputation found no error in the coefficients, signs, assignments, or case exhaustion.

## 4. Independent reviewer challenge

**Reviewer:** a separate general-purpose subagent session (OpenChamber; same local model family as this session). This is a separate session's review, not external peer review and not a formal certificate. It ran in a read-only role: it read this note (§§1–5) and the three JSON restriction files, recomputed every step in its own notation, checked the declared edge set against the project's own `build_graph([[1],[2],[]])` (exactly the 8 vertices and 7 edges of section 1), and ran its own independent brute-force enumeration of all 144 restricted assignments with no project solver code (scratch script outside the project: `C:\Users\Will\AppData\Local\Temp\opencode\b2_review_scratch.py`, now preserved byte-for-byte at `evidence/reviews/B2_UNEQUAL_SEED_001/pack/supplied/b2_review_scratch.py`; no project file was written). The preserved scratch is the **earlier diagnostic version**: it applies the `y=3`-restricted identity `S=a+2b−x+10` to all 144 assignments, which is the source of the disclosed 108 apparent mismatches (disclosed below). The corrected general identity is `S=a+2b−x−2y+16`, which holds with 0 mismatches across all 144 assignments; it is verified by the pack's independent check (`evidence/reviews/B2_UNEQUAL_SEED_001/pack/independent_seed_check.json`) and by this integration's own check H4 (`evidence/reviews/B2_UNEQUAL_SEED_001/verification_result.json`).

**Method:** step-by-step recomputation in the reviewer's own notation; independent enumeration of the full 144 named assignments after the pin (no symmetry quotient); arithmetic verification of the section 5 consumer lemma for K = 1..12 (both parities, including K = 1) and of the transport mechanics for K = 1..7; vertex-by-vertex check of the pins/domains files and of the consumption semantics in `lcl/search.py` and `lcl/oracle.py`.

**Per-item verdicts:**

| Item | Verdict |
|---|---|
| (a) all seven edges cross the A/B cut, so every difference is unambiguously `high − low` | CONFIRMED (by hand, by enumeration, and against the project builder) |
| (b) difference 1 forces `h(s:1)=3`; no other edge can carry 1 under the pin | CONFIRMED (36 of the 144 assignments have `h(s:1)=3`, and difference 1 then appears only on `s:1--s:2`; 0 assignments with `h(s:1)≠3` contain difference 1 anywhere) |
| (c) sum identity `a+2b−x=18`, every degree coefficient, sign and constant term | CONFIRMED (recomputed from scratch; 0 identity violations across the 36 assignments of the `y=3` slice. The identity is the `y=3`-restricted form; the general form for `y≠3` is `S = a+2b−x−2y+16`. The note substitutes `y=3` first, so its presentation is correct) |
| (d) case exhaustion yields exactly `(5,7,1)`, `(6,7,2)`, `(7,6,1)` | CONFIRMED (every `b`-case rechecked including rejected subcases; the independent enumeration found exactly these three solutions, each realized by the two `(u,v)` orderings) |
| (e) duplicate difference 4 on at least two actual original edges for every `(u,v)` | CONFIRMED (full difference table for all six (triple, `(u,v)`) combinations; 4 appears at least twice in every case) |
| (f) missed cases, sign/coefficient errors, hidden assumptions, implicit symmetry quotient | NONE FOUND (the chain is a sequence of necessary conditions covering the whole restricted space; the reviewer's own enumeration of all 144 assignments found 0 graceful witnesses) |
| (g) conditional all-K transport (injectivity/range, +K on every prefix difference, unused `[4,K+3]`, unused `1..K`, port `K+4` one above, consumer with a = 4 terminating in K steps) | CONFIRMED (consumer lemma verified arithmetically for K = 1..12; transport mechanics verified for K = 1..7; full target has K+8 vertices and K+7 edges) |
| (h) pins/domains files match the declared restrictions exactly (nothing extra, nothing missing) | CONFIRMED (files checked vertex-by-vertex; consumption semantics and the `no symmetry quotient` counting convention confirmed in both engines and both records) |

**Objections raised and resolution.** The reviewer raised no objection to the argument. It noted two minor reporting omissions in section 3 step 5, each of which *strengthens* the obstruction:

1. For triple `(7,6,5,1)` the third edge carrying 4 is not conditional: with `x=1` fixed at `b:0:0` and `y=3` fixed, the remaining low labels `{u,v}={0,2}` both sit at the two `b:1:0` leaves, so the leaf carrying 2 always contributes `6−2=4` — difference 4 occurs **three** times, not two.
2. Secondary duplicates were unreported: difference 5 twice in triple `(5,7,6,1)` and difference 6 twice in triple `(7,6,5,1)`.

Both are corrected in step 5 above, marked *(reviewer correction)*. The reviewer also disclosed its own scratch-check slip: an initial run applied the `y=3`-restricted identity to `y≠3` assignments and reported 108 apparent "identity mismatches"; the corrected run on the `y=3` slice gives 0 violations. No error in the note resulted from it.

**Overall review verdict.** (1) The analytic argument is correct and establishes that no graceful labeling of this named eight-vertex prefix exists under exactly the declared restrictions; the reviewer's own independent enumeration of all 144 restricted assignments found 0 graceful witnesses. (2) The conditional all-K transport holds as stated, and the section 5 disposition — retained as a conditional identity only, discharging no P07 obligation, not promoted, not implemented — is the correct one. (3) Scope reservations (agreed): this falsifies only this exact named prefix under exactly these restrictions — not the unrestricted eight-vertex tree, not any other restriction set, and not the K≥1 family members (whose antecedent is now vacuous).

## 5. Conditional all-K transport (assessed separately)

For a hypothetical valid seed `h` and every integer `K ≥ 1`, define `h_K` by: low-side labels unchanged; every high-side label increased by `K`; the appended original `K`-edge path `s:2--s:3--...--s:(K+2)` unlabeled. Claimed returned state: full target edge count `m = K+7`; unused labels `[4, K+3]`; unused differences `1..K`; physical port `s:2` labeled `K+4`, side above; consumer the original path.

Verification (all steps conditional on the seed's existence):

- **Injectivity and range.** Low labels are exactly `0..3`; high labels are exactly `K+4..K+7`. The two sets are disjoint for `K ≥ 1` and their union has eight distinct labels inside `0..K+7`. The full target has `8+K` vertices and `K+7` edges. Confirmed.
- **Prefix differences.** Every prefix edge crosses the A/B cut (section 1), so each prefix difference increases by exactly `K`. The seed differences `1..7` become exactly `K+1..K+7`, all distinct. Confirmed.
- **Unused inventories.** Unused labels: `0..K+7` minus `{0..3} ∪ {K+4..K+7}` is exactly `[4, K+3]`. Unused differences: `1..K+7` minus `K+1..K+7` is exactly `1..K`. Confirmed.
- **Boundary.** The only prefix-to-suffix edge is the original `s:2--s:3`. The active label is `h_K(s:2) = K+4`, one above the unused interval `[4, K+3]` (side: above). Confirmed.
- **Completion and termination.** Section 3 of `PROOF_OBLIGATIONS.md` (active endpoint above the interval) applies with `a = 4`: it alternately takes the lowest and highest unused label, produces differences `K, K−1, ..., 1` exactly once, consumes every unused label, and terminates after exactly `K` steps. Confirmed.

**Status:** the transformation is a correct conditional identity: *if* the seed existed, it would supply every `K ≥ 1` of the declared family. Since section 3 (and the validation below) establish that the seed does not exist, this is **retained as a conditional identity only**. It discharges no P07 independence obligation, is not promoted, and is not implemented as a supplier.

## 6. Bounded DFS run (declared validation)

- **Command (from project root):** `.\.venv\Scripts\python.exe -m lcl solve examples\unequal_seed.json --engine dfs --pins examples\unequal_seed_pins.json --domains examples\unequal_seed_domains.json --limits configs\unequal_seed_limits.json`
- **Input identities:** target `examples/unequal_seed.json` (profile `[[1],[2],[]]`), pins `examples/unequal_seed_pins.json` (`s:2=4`), domains `examples/unequal_seed_domains.json`, limits `configs/unequal_seed_limits.json` (`max_nodes=10000`, `time_limit=2.0`, `max_vertices=8`, `max_states=2000`).
- **Original target:** 8 named vertices, 7 edges exactly as listed in section 1; graph digest `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`. No connector or substituted topology: the record's `original_graph` was inspected edge-by-edge against the named target, `consistency_errors` is empty.
- **Environment:** CPython 3.13.17 (CPython, AMD64), Windows-11-10.0.26200-SP0, package v0.1.0, no optional dependencies. Source snapshot sha256 `2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd`; config sha256 `949e505923d13323e3cb76628773bdee09ed9fee600a49ed88adbb3c7611bdb6`.
- **Result:** status `EXHAUSTED_NO_SOLUTION`, count `0`, `exhausted=true`, witness `null`, `nodes=65` of the 10,000-node cap, elapsed ≈ 0.0003 s. No time or node limit stop. Counting convention: named bijections, no symmetry quotient (`hidden_symmetry_reduction=false`, scope `restricted`).
- **Checker:** no positive certificate exists to verify (negative result); the record's `negative_evidence` states "implementation exhaustion on declared scope; no formal negative certificate". The independent cross-check is section 7.
- **Record:** `runs/dfs-20261121T081441Z-0a3c9a64/record.json` (record sha256 `f03d968e014e17d37382ef60a1836177497e388b86d779501fbe6b9dc0071f05`). `runs/` is Git-ignored local work; this section plus the handoff preserve the identifiers in tracked files.

## 7. Direct-permutation oracle cross-check

- **Command:** same target/pins/domains/limits with `--engine oracle`.
- **Result:** status `EXHAUSTED_NO_SOLUTION`, count `0`, `exhausted=true`, reason `EXHAUSTED`, `attempted_permutations=5040` of `permutation_domain_size=5040` (7! over the seven unpinned labels; cap 10,000), elapsed ≈ 0.0043 s. Of the 5,040 enumerated permutations, exactly the `4!·3! = 144` assignments satisfying the domain restrictions were admissible; none is graceful. No symmetry quotient (`symmetry_reduction=null`, "named bijections; no symmetry quotient").
- **Same original target:** graph digest `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2` (identical to section 6); `consistency_errors` empty.
- **Proof status (record's own):** "finite computation; not a formal negative certificate".
- **Record:** `runs/oracle-20261121T081441Z-a5f3c783/record.json` (record sha256 `d8c0359adc279d46e5aaffc6cd7affbf7aa70304f659dbc572f5f2eaf978a489`, config sha256 `d0603cf8cf345118b4cddc7423fc573cc576e06e7b77c6b62a3c0c3d8f9673ec`, source snapshot `2dfe3231...` identical to section 6).

The DFS exhaustion (65 nodes) and the oracle's full enumeration (5,040/5,040 permutations, 144 domain-admissible, 0 graceful) agree: **the restricted seed does not exist.**

## 8. Disposition and remaining duty

**Disposition: exhausted restricted negative (the declared bounded validation completed).** The proposed analytic obstruction is correct in every step — independently recomputed in section 3 and challenged in section 4 with no unresolved objections (two minor reporting omissions corrected). The declared bounded DFS run and the independent direct-permutation oracle both exhausted the declared scope with 0 solutions (65 nodes; 5,040/5,040 permutations with 144 domain-admissible; no time or node limit stop), agreeing on the same original graph digest.

**What is established.** There is no graceful labeling of the named eight-vertex prefix `[[1],[2],[]]` (the exact seven edges of section 1) subject to exactly the declared restrictions: A-side `0..3` and B-side `4..7` bijective domains, pin `h(s:2)=4`, and no further root pin, complement quotient, symmetry assumption, or automorphism quotient. The obstruction mechanism is precise: difference 1 forces `h(s:1)=3`; the sum identity `a+2b−x=18` admits only `(a,b,x) ∈ {(5,7,1),(6,7,2),(7,6,1)}`; in all six resulting assignments difference 4 is duplicated (twice in two triples, three times in the third).

**What is not established (explicit scope limits).**

- This is **not** a nongracefulness certificate for the unrestricted eight-vertex tree, for any other restriction set, or for the unequal B2 family at any K. A restricted negative is not nongracefulness.
- The all-K high-side-shift transport (section 5) is retained as a **conditional identity only**: correct that a seed, if it existed, would supply every `K ≥ 1` of the declared family; its antecedent is false, so it discharges no P07 obligation, is not promoted, and is not implemented.
- Neither record nor analysis is a formal negative certificate or a proof-assistant check; the records' own status is "finite computation / implementation exhaustion on declared scope; no formal negative certificate."
- No universal lobster gracefulness, historical novelty, or formal-verification claim is made.

**Remaining duty (historical task-close wording; the queued sweep was superseded without execution by D016, accepted by D018).** The original B2 objective — a usable original-graph boundary for two unequal branched sections beginning at q=1, r=2 with arbitrary positive K — remains open: this template (alpha domains + pin `s:2=4`) is one falsified instantiation. The queued next task is one specific alternative port rule on the same named target: sweep the remaining port pins `h(s:2) ∈ {5,6,7}` under the same alpha domains and the same declared bounded protocol (see `research/NEXT_TASK.md`; queued, not executed).

## 9. Post-task review addendum (November 21, 2026)

**Historical status at integration:** PROVISIONAL_INTEGRATION_PENDING_CODEX_REVIEW. Everything added in this section and the companion note was the product of an independent external review, provisionally integrated by `OC-20261121-b2-review-integration`. The later independent Codex review accepted the scoped claims and intervening revision `2cfb2df`; see `research/B2_CODEX_ACCEPTANCE_REVIEW.md` and D018. Neither review is human peer review or a formal certificate. Sections 1–8 are preserved as historical records apart from the identified descriptive corrections and the retrospective status annotation to the section 8 remaining duty; the once-queued sweep was later superseded, not executed.

**Review pack identity.** An independent outside session (CPython 3.12.14, Linux — a different machine from this checkout) reviewed the export of checkpoint `0f0a39c4d8d97d211782d1a1d81aeba5e0481319` (following `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685`) and returned `LCL_B2_Independent_Review_2026-11-21.zip` (240,684 bytes, raw SHA-256 `285e37061efb911fd696013c358f682bbbbf9e915a470a113e411f1813075a38`). That returned review pack contains a distinct `original_upload.zip`: the earlier input archive (66,234 bytes, raw SHA-256 `a2def9c494ff49d7dbe89ca10416b1da804e82052c9a79db773ae50c819e2b97`). These are two different archive identities; the project preserves the selected extracted evidence described below. Tracked custody copy: `evidence/reviews/B2_UNEQUAL_SEED_001/` — both historical run records and their exact target/pin/domain/limits inputs byte-for-byte under `raw/`, the pack deliverables under `pack/`, plus this integration's verification script, result, and raw manifest. The integration session recorded 33 successful entries (31 predicate checks and two informational raw configuration-hash observations; D1/D2 separately check configuration contents), covering A1–A7 byte identity local vs pack; B1–B10 raw SHA-256; C1–C2 canonical `record_sha256`; D1–D2 `config_sha256`; E1–E3 source inventory `2dfe3231…` and 21-file byte match; F1–F2 all 55 MANIFEST entries; G1–G3 graph digest `9198e106…` and embedded `original_graph`; H1–H4 its own independent 144-assignment enumeration: exactly 144 domain-admissible, 0 graceful, 36 with `h(s:1)=3`, 0 general-identity mismatches. Result: `evidence/reviews/B2_UNEQUAL_SEED_001/verification_result.json`. **No discrepancy was found** between the pack, the local records, and the local source.

**Descriptive corrections applied to this note (both from the pack, section 7, items B and C):**

1. §3 step 3: the degree-list parenthesis placed `s:2` on the low side; it is a high-side degree-1 vertex whose fixed pin label 4 is the displayed `+4` constant, and the two low-side terminal leaves are now listed. The displayed sum and the identity `a+2b−x=18` are unchanged.
2. §4: the preserved reviewer scratch is identified as the earlier diagnostic version (the source of the disclosed 108 apparent identity mismatches), with the corrected general identity `S=a+2b−x−2y+16` and its 0-mismatch verification cited.

**Pack verdicts (as received; local integration status):**

| Item | Pack verdict | Local integration status |
|---|---|---|
| Prescribed alpha seed with `s:2=4` | **ACCEPT** | External verdict at integration; subsequently accepted at reviewed revision `2cfb2df` (D018) |
| Original-edge fidelity and scope | **ACCEPT** | Provisionally accepted; verified against local source (checks G1–G3) |
| DFS and oracle evidence | **ACCEPT, with provenance limits** | Provisionally accepted; both records now preserved byte-for-byte in tracked `evidence/reviews/B2_UNEQUAL_SEED_001/raw/` |
| Conditional high-side shift and path consumer | **ACCEPT as conditional only** | Retained as a conditional identity only, unchanged |
| Evidence custody and minor reporting | **REVISE** | Corrections applied in this integration (tracked record copies; scratch identified; degree list corrected; hash-scheme distinctions documented in the evidence README) |
| Pin sweep as a repair of the existing all-`K` construction | **REVISE** | Queued pin sweep recorded **superseded, not executed**; see `research/NEXT_TASK.md` and decision D016 |
| New `K>=6` interface obstruction | **CONFIRMED in that review** | Adopted verbatim into `research/B2_INTERFACE_OBSTRUCTION.md`; independently re-derived step by step by the integration session; failure-ledger entry F-INTERFACE-K6 |

**New result adopted (summary; full proof in `research/B2_INTERFACE_OBSTRUCTION.md`).** For `q=1, r=2, z0=z1=0` and every `K>=6`, there is **no** injective prefix labeling of the exact eight-vertex prefix through `s:2` in the final alphabet `0..K+7` that leaves unused labels exactly `[ell, ell+K-1]`, prefix-edge differences exactly `K+1..K+7` (equivalently unused differences `1..K`), and physical port `f(s:2)=ell+K` or `f(s:2)=ell-1`, for any `ell` and either side. No alpha condition is assumed and no root label is pinned. Mechanism: the maximum difference `K+7` forces labels `0` and `K+7` into the prefix (`1<=ell<=7`); the assigned labels are two blocks of span at most six; for `K>=6` every prefix edge must cross the blocks; the connected 4/4 bipartition forces `ell=4`; compressing the high block by `K` yields a graceful alpha labeling of the original seed graph — exactly the forbidden p=4 seed on the above side, and (after complementing labels by `7-g`) on the below side. The complement is a proof map, not a counting quotient. Threshold 6 is sufficient, not claimed sharp; `K=1` is feasible at `ell=1`, above, by the preserved pilot; `K=2..5` are not adjudicated here; this is **not** a nongracefulness proof for the full tree; the balanced `q=r` supplier and the padded construction (different parameter domains) are unaffected.

**Effect on section 8's remaining duty.** The original all-`K` adjacent-port objective for `q=1,r=2,z0=z1=0` is now impossible for `K>=6`, so it should no longer be described merely as an unresolved independent-supply duty. The previously queued pin sweep `h(s:2) ∈ {5,6,7}` is recorded **superseded, not executed**: for `p ∈ {5,6,7}` the same high-side shift returns unused labels `[4,K+3]` but places the physical port at `K+p`, not the adjacent port `K+4` that the existing path consumer requires; and at `K=1` the single suffix edge would have difference `|(p+1)−4| = p−3 ∈ {2,3,4}` instead of 1. P07 for the unequal family remains open through a genuinely revised interface; a proposed, unexecuted candidate direction (nonadjacent-port path consumer) is recorded in `research/NEXT_TASK.md`. The broader problem of constructing graceful labelings for the unequal family is not refuted.
