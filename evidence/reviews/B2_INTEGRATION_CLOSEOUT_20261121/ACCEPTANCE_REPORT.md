# Acceptance review of the B2 integration checkpoint

**Date:** November 21, 2026, Pacific/Honolulu.  
**Reviewed export:** `5fb2fa108835720c829cafd5095983f3c0f6198d`.  
**Reported last accepted baseline:** `36ea1603602491bf3c1c5b81ed4c23aaa2210e70`.  
**Overall decision:** **ACCEPT the substantive mathematics, preserved evidence, handoff overlay and ignore-rule correction. REVISE a small set of metadata, replay and scope descriptions.** No seed research needs to be repeated.

The uploaded file was `LCL_Codex_Acceptance_Review.zip`, 351,779 bytes, raw SHA-256 `38d34f9426a8e84a3a05c21e3714e8800ebecb32fbc2f461bf276f7af6a9e096`. This review operates on that export, earlier reviewed artifacts, and the preserved release source. It does not modify or independently query Will's Windows checkout.

## 1. Outcome and practical meaning

OpenChamber successfully carried the research findings into the project. The historical negative records are now included in the exported tracked evidence. The adopted proof body is exactly the earlier reviewed argument. The queued pin sweep is explicitly superseded, and the proposed nonadjacent-port consumer remains unproved and unexecuted.

The remaining issues are small and concrete. They concern evidence paths, repeatable checking, accurate descriptions of existing small-case knowledge, and preservation of exact bytes across Git checkouts. They do not overturn the seed proof or the K>=6 theorem and do not justify restarting the experiments or launching a broad review cycle.

The included `corrections/closeout.patch` prepares ten targeted file changes against this checkpoint. It has been applied and checked in an isolated project copy. The actual user repository and every supplied file remain unchanged.

## 2. Claim-by-claim decisions

| Claim or change | Decision | Basis and limit |
|---|---|---|
| p=4 restricted seed negative | **ACCEPT** | The original proof is sound; restrictions and raw evidence are unchanged. |
| Conditional all-K high-side transport | **ACCEPT as conditional only** | Correct transformation and consumer, with an impossible antecedent; no supplier follows. |
| K>=6 interval/adjacent-port obstruction | **ACCEPT** | Adopted proof body matches the prior reviewed 7,038 bytes; no initial alpha assumption; both port sides covered. |
| Superseding the p=5/6/7 pin sweep as a repair of the unchanged construction | **ACCEPT** | The port would be wrong for the existing consumer; K=1 fails; the old interface is impossible for K>=6. |
| Preservation of the actual raw records and review payloads | **ACCEPT** | All 21 preserved payloads match expected bytes, including their reconstructed Git blobs. |
| `.gitignore` change from `runs/` to `/runs/` | **ACCEPT** | It keeps root runtime output ignored and permits the nested curated copies. |
| OpenChamber handoff overlay | **ACCEPT as instructions** | Scope, original-target fidelity, evidence, review and stopping instructions are coherent. This is not a runtime test of a service. |
| Literal paths in `RAW_FILE_MANIFEST.json` | **REVISE** | Old prefixes do not name the files now present; values match after explicit path correction. |
| Routine replay using the historical integration checker | **REVISE** | It depends on Downloads/Temp/original runs and rewrites its historical result. Preserve it; use a new direct custody checker. |
| “K=1..5 undetermined” and unqualified “not sharp” summaries | **REVISE** | K=1 already has a saved positive interface witness; threshold sharpness has not been established. |
| Proposed nonadjacent-port consumer | **CANDIDATE ONLY** | It is meaningful as a different interface, but no all-parameter consumer or matching seed is established here. |

These are scientific and content decisions on the supplied material. Local acceptance markers, a new commit, and live Git checks must still be recorded in the actual checkout. If OpenChamber applies the closeout before Codex is available, it should report this external review accurately and retain the requested pending-Codex workflow marker.

## 3. Verification actually performed

### Evidence integrity

The independent custody audit found:

- 58 of 58 files listed in the collection CSV match their recorded hashes.
- Both original run records, both copied run configurations and all four input/restriction/limit files match their expected contents.
- Both canonical record digests and configuration digests recompute correctly.
- The 13 imported review-pack files match the earlier delivered pack byte-for-byte.
- Every entry of the complete original 55-entry review-pack manifest matches the original returned ZIP, including the file set.
- Both source inventories match the preserved release: **15 `lcl/` Python files plus six requirements/package files**, 21 in total.
- Both graph digests and recorded targets agree.
- The historical integration script matches the script hash in its stored result.
- The older independent seed checker and its saved 144-assignment output are unchanged.

See `analysis/evidence_custody_review.md` and `analysis/integration_evidence_audit.json`.

### Isolated replay of the new integration checker

The reviewer read the 14,894-byte integration script before running it. Its source remained unchanged. An isolated project copy was assembled from the uploaded records and hash-matched release source, and the complete original returned review ZIP was extracted separately. Only runtime paths were redirected: project root, pack root, scratch location and output location.

**Observed result:** all 33 recorded entries reproduced successfully, including the checker's own fixed 144-assignment loop with zero graceful witnesses and zero general-identity mismatches. No successor pin, K-case or family search was run. The historical result was not overwritten.

The exact description of those 33 entries is **31 predicate checks plus two informational raw configuration-hash observations**, B3 and B4. Those two are deliberately recorded with `pass=True`; D1 and D2 separately verify the configuration contents. This is a reporting qualification, not a failure of the scientific check.

See `replay/portable_verification_result.json` and `replay/REPLAY_PROVENANCE.json`. This is a Linux replay on reconstructed, source-matched inputs; it is not a new observation of the original Windows execution.

### Git content reconstruction

The exported patches had reversible CP437/UTF-8 text damage from the PowerShell export pipeline. Both were recovered, and their preimages and postimages were checked against the preserved sources and uploaded files. No source-file corruption was found, and no new upload is needed.

The reconstructed changes match the Owner report:

- Latest integration: **35 files, 7,408 additions, 14 deletions**.
- Entire accepted-baseline-to-current export: **44 files, 7,835 additions, 28 deletions**.
- All 25 curated evidence files are included in the tracked inventory.
- All eight raw files and thirteen pack files are currently byte-identical to their Git blobs.
- No changes appear to the mathematical `lcl/` core, tests, original input restrictions, target or solver configuration.

The three handoff-overlay files omitted from direct copying were recovered in full from the new-file patch entries and checked by Git blob identity. Their content was reviewed. See `analysis/git_review.md` and `analysis/git_patch_audit.json`.

No `.git` object database or live refs were supplied. The exports consistently identify HEAD `5fb2fa1...` and baseline `36ea1603...`, but this review does not independently authenticate live branch/tag state, parent links, clean status, or absence of a push on the user machine.

## 4. First correction: the manifest points at old folder names

The local directory layout is:

```text
raw/...
pack/...
```

The manifest instead records:

```text
runs-and-inputs/...
review-pack/...
```

None of its 21 literal preserved-file paths exists under those old names. After mapping `runs-and-inputs/` to `raw/` and `review-pack/` to `pack/`, every recorded size and hash matches. The two keys in `canonical_record_fields` need the same correction.

The evidence is present. The error is its address in the metadata. The prepared patch corrects the keys and records why they changed, without changing any payload size or hash. The historical manifest remains preserved by the prior commit and the uploaded archive.

## 5. Second correction: verify the curated copies directly

The historical checker compares the original root-level runs with the complete external Downloads pack and a hard-coded Temp scratch script. It does not check the curated `raw/` and `pack/` directories against `RAW_FILE_MANIFEST.json`. That is why its 33 successful entries did not expose the wrong manifest paths.

It also writes to `verification_result.json` beside itself. The README acknowledges that a replay overwrites this historical output, so describing it simply as read-only is imprecise. The recorded original script and output should remain unchanged.

The new `verify_preserved_b2_evidence.py` instead:

- Reads the actual tracked raw/pack payloads directly.
- Requires the manifest to name exactly the preserved set.
- Checks every payload size and raw hash.
- Checks copied pack members against the original pack manifest without pretending the selected local subset is the complete pack.
- Rechecks canonical record/config identities and the 21-file source inventory.
- Confirms saved scripts' identities and saved result scope.
- Creates only a user-named **new** output; it refuses to overwrite an existing file.
- Imports no project code, uses only the standard library, and performs no labeling enumeration.

The current source must still match the recorded source bytes; the tool reports changes rather than silently treating a different source snapshot as the same run.

### Focused validation of the correction

The proposed patch passed `git apply --check` and actual application in an isolated fixture using `core.autocrlf=true`. The new custody checker then produced:

| Situation | Observed result |
|---|---|
| Uncorrected supplied snapshot | Rejected the 21 stale paths, missing exact-set match, two stale canonical references and absent scoped EOL rules |
| Corrected snapshot | **72/72 predicate checks passed** |
| One newline appended to a saved record, leaving its parsed JSON unchanged | Correctly rejected the changed raw bytes |
| Attempt to reuse an existing output filename | Refused with a nonzero exit |

All 21 historical payloads remained unchanged after testing. A separate reviewer inspected the new tool and accepted its semantics for this scope. See `validation/VALIDATION_SUMMARY.json` and `analysis/portable_checker_review.md`.

The H-loop comment in the historical integration script says `x+u+v=3-y`; its unrestricted total is `6-y`. The executed formula `S=a+2*b-x-2*y+16` is correct. The historical script is retained with its known hash, and the discrepancy is documented rather than silently editing the source that produced the historical result.

## 6. Third correction: preserve exact evidence bytes across checkouts

The `/runs/` ignore change is correct. A separate issue is line-ending conversion: a tracked file can change from LF to CRLF on checkout while retaining the same mathematical text but acquiring a different raw SHA-256.

No versioned `.gitattributes` was present in the 1,063 tracked paths. An isolated Git test used an actual historical record and pack README:

| Test | Record bytes | README bytes |
|---|---|---|
| `core.autocrlf=true`, no attributes | Changed | Changed |
| Same setting, scoped `-text` attributes | Preserved | Preserved |

The patch adds only this local file:

`evidence/reviews/B2_UNEQUAL_SEED_001/.gitattributes`

```gitattributes
raw/** -text
pack/** -text
verify_b2_review_pack.py -text
```

This protects the archived payloads and the historical script whose raw hash is recorded, without changing global Git settings. The historical result JSON is preserved unchanged by this patch; its previously observed working-copy CRLF versus Git LF distinction remains documented. Git's official documentation states that unsetting `text` disables end-of-line conversion for the matching paths: https://git-scm.com/docs/gitattributes . The actual user machine's current Git configuration was not supplied; the isolated test demonstrates the relevant portability behavior and the remedy.

Current payload blobs already have the correct bytes, so no history rewrite or renormalization campaign is needed. See `analysis/git_behavior_check.json`.

## 7. Fourth correction: retain the already-known K=1 success

Several new summaries say `K=1..5` is undetermined. That overstates what is unknown. The K>=6 theorem does not decide those smaller cases, but the preserved release already has a positive `q=1,r=2,K=1,ell=1`, above-side interface.

The saved certificate uses:

| Physical vertex | Label |
|---|---:|
| `s:0` | 4 |
| `s:1` | 8 |
| `s:2` | 2 |
| `s:3` | 1 |
| `b:0:0` | 6 |
| `l:0:0:0` | 3 |
| `b:1:0` | 0 |
| `l:1:0:0` | 5 |
| `l:1:0:1` | 7 |

Its eight actual edge differences are exactly `1..8`. Its seven prefix differences are `2..8`; the remaining label is `1`, the remaining difference is `1`, and the physical port is `2`. This is exactly the old adjacent-port contract at K=1. The saved certificate was read and arithmetically checked; no pilot search was repeated.

The source record is `evidence/validation/release_final/pilot/cases/31da62597181ea39545cd89689e591113261ea7c9c7af56e60383894da947a57.attempt-0001.json`, raw SHA-256 `8c956fd5b770d9e3f3f7d433b5477d981dd6805e9fae5577cb8810bfa5a3a021`. A copy is included at `analysis/preserved_K1_positive_record.json` for this review.

Use this qualification:

> The K>=6 argument does not settle smaller K. The preserved K=1, ell=1, above-side pilot is feasible; K=2..5 are not adjudicated here. The threshold six is sufficient; sharpness is not established.

This keeps the existing positive evidence visible and avoids claiming that six is known to be a nonoptimal threshold. It does not weaken the theorem. The imported proof body already correctly qualifies what its own argument does not decide; the patch preserves that body and updates only the new summaries/header.

## 8. Additional description clarifications

The earlier input ZIP and returned review ZIP are distinct:

| Archive | Bytes | Raw SHA-256 |
|---|---:|---|
| Original input, retained inside the returned pack as `original_upload.zip` | 66,234 | `a2def9c494ff49d7dbe89ca10416b1da804e82052c9a79db773ae50c819e2b97` |
| `LCL_B2_Independent_Review_2026-11-21.zip` | 240,684 | `285e37061efb911fd696013c358f682bbbbf9e915a470a113e411f1813075a38` |

The seed-note addendum currently names the returned pack next to the original input's size/hash. Its wording can be understood, but the patch explicitly distinguishes the two identities.

The evidence README also overstates why the omitted earlier `supplied/` tree is redundant: it included Git exports and formerly ignored records, not just already tracked project files. The new README states the actual preservation scope: eight raw files and thirteen selected pack files, with full-pack provenance retained separately.

Historical handoffs and verification artifacts remain historical records. A local closeout decision should point to these corrections rather than pretending every earlier description was already exact.

## 9. Next research direction and remaining duty

The candidate nonadjacent-port consumer is a coherent change of interface: retain unused labels `[ell,ell+K-1]` and differences `1..K`, but allow the starting port `ell+K+1`. Its K=1 exclusion is immediate, since the sole remaining edge would have difference two. No claim for all K>=2 or of a matching seed has been established in this acceptance review.

That candidate should become a separate bounded proof task after the local acceptance/closeout is recorded. Its quantified consumer proof and an independently supplied compatible seed are separate obligations. More seed searches without the consumer theorem would not establish an all-parameter construction.

For now, the single manageable next action is the local closeout in `OPENCHAMBER_CLOSEOUT_PROMPT.md`: apply/reconcile the small patch, run the custody check once into a new output, record the external review and actual local changes, preserve the baseline, and stop. No repeat of the p=4 research, four-pair pilot, full release suite or pin sweep is required.

## 10. Deliverable boundaries

The patch is prepared against exported checkpoint `5fb2fa1...`; it has not been applied to the user's project. If the checkout has advanced, reconcile it rather than reset or overwrite newer work. The pack includes exact input archives, the evidence and mathematical review notes, replay and correction-validation outputs, proposed changed files, the patch and the local closeout prompt.

No universal lobster result, ordinary nongracefulness, historical novelty, or formal verification is claimed. The accepted scoped findings are unchanged, and the remaining construction duty requires a genuinely revised interface with a proved continuation.
