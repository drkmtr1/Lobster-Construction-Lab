# Evidence review — B2-UNEQUAL-SEED-001

## Disposition

**ACCEPT the supplied DFS/oracle records as internally consistent, source-matched evidence for the exact restricted seed question. REVISE evidence preservation and minor reporting before closing the local handoff.** This is an inspection of an exported bundle plus the preserved release source, not authentication of the user's live Windows Git repository.

Both uploaded review ZIPs are byte-identical: SHA-256 `a2def9c494ff49d7dbe89ca10416b1da804e82052c9a79db773ae50c819e2b97`. The bundle has 21 files. No uploaded file was changed.

## Checks actually performed

- Read the supplied STATE, AGENTS, return instructions, handoff, original proof note, inputs, both full records, Git exports, reviewer scratch, and the relevant hash-matched release code.
- Recomputed both canonical record hashes, both configuration hashes, and both source-inventory hashes. Every check passed.
- Compared all 21 source-inventory files to the preserved v0.1.0 project byte-for-byte; all match. Shared inventory SHA-256: `2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd`.
- Independently expanded the uploaded profile into the exact named original graph, including physical roles/spine and all seven incidences. It equals both stored original graphs. Recomputed graph digest: `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`.
- Compared uploaded pins, domains, and limits with both record configurations and caller-retained restrictions. They match exactly. The oracle's `alpha_required=false` means no additional generic alpha test: the explicit vertex domains already impose the required alpha separation.
- Read the DFS pruning and oracle enumeration implementations. DFS MRV only changes assignment order; its pruning rejects repeated vertex labels or edge differences, all necessary exclusions. `count_requested=false` can stop at a witness, but no witness was found, so full exhaustion establishes exact zero. The independent oracle enumerates 7! = 5,040 assignments after fixing the one pin, then filters the domains; precisely 4! times 3! = 144 satisfy those domains. These are different counters, not inconsistent scope.
- The DFS reports 65 attempted partial assignments, not 65 complete candidate labelings. Its record is exhausted with count zero and no stop reason. The oracle reports 5,040 of 5,040 permutations, exhausted with reason EXHAUSTED and count zero. Reported elapsed times are 0.0002966000174637884 and 0.004339300008723512 seconds. Those runtime measurements are record content; this forensic review did not rerun the solvers.
- The configured limits are 10,000 assignments/permutations, 2.0 seconds cooperatively, and eight vertices. `max_states=2000` is present in the shared Limits object but is not an active DFS/oracle memory cap. The 2,000,000-byte output cap comes from `atomic_json`, not the four-key limits file. Uploaded records are only 7,150 and 7,328 bytes. The code is sequential within each solver; no claim about host-wide scheduling is established by these records.
- Dates are consistent at the stated timezone granularity: the run timestamps `2026-11-21T08:14:41Z` correspond to November 20 at 22:14:41 Hawaii time; the checkpoint was authored and amended after midnight November 21 Hawaii time. A November 20 handoff identifier and November 21 completion date therefore do not conflict.
- Reconstructed all eight changed Markdown files from the archived baseline and exported patch after repairing the export encoding. Every reconstructed postimage equals the uploaded bytes, every old blob prefix matches the preserved baseline, every new blob prefix matches the uploaded file. Counts are exactly eight files, 246 inserted lines and 27 removed lines. No source/configuration/checker change appears in that patch.

## Hash terminology

The `record_sha256` field hashes canonical JSON with that field omitted. It is not the SHA-256 of the complete serialized `record.json` file. Both types validate, with distinct values:

| Record | Canonical payload hash (`record_sha256`) | Raw file SHA-256 |
|---|---|---|
| DFS | `f03d968e014e17d37382ef60a1836177497e388b86d779501fbe6b9dc0071f05` | `1c84fcf14fe4f591455db0c0c4a0522ccc2f2c644791f1361c4fea03b88dbf44` |
| Oracle | `d8c0359adc279d46e5aaffc6cd7affbf7aa70304f659dbc572f5f2eaf978a489` | `0504e38a259a648e0f648b4ab1e5be4789d3b28de396b69710cfe394e2c88d11` |

Do not report the canonical values as whole-file checksums. Existing note wording `record sha256` is consistent with the field, but an archival manifest should explicitly label the scheme and include the raw values.

## Revisions and limits

1. **Preserve actual evidence bytes in the reviewed repository.** The handoff states that the two runs are Git-ignored, and the checkpoint patch contains no JSON records. Their path and checksum in a tracked note cannot reconstruct the record after local cleanup or a fresh clone. The uploaded archive now preserves a copy for this review; the local handoff rule still calls for tracked reviewable evidence. Copy the two unchanged records, exact input/config files, and reviewer material into a versioned evidence directory, with a manifest of raw hashes and source identity. Preserve the historical `runs/` files. The full run `source/` directories and run `config.json` files were not uploaded; the record source inventories nevertheless match the full preserved release sources available here.

2. **Correct the patch export, not the source files.** `checkpoint.diff` contains CP437-decoded UTF-8 mojibake such as `Γêê` for `∈`. This is completely reversible in the supplied file: decoding its UTF-8 text, re-encoding as CP437, then decoding as UTF-8 restores the patch. No replacement characters are present. The actual uploaded Markdown files are intact. `analysis/checkpoint.normalized.diff` is the recovered UTF-8/LF patch; all eight images were verified. A future export can use Git's direct `--output` option to avoid the native-command-to-PowerShell text decoding path.

3. **Retain and label the reviewer diagnostic slip.** The included `b2_review_scratch.py` still evaluates the identity specialized to `y=3` on all 144 assignments, causing the 108 mismatches that the note explicitly discloses. Its no-witness enumeration is independent of that faulty diagnostic and is valid. The note's claimed corrected slice run is not represented by a corrected script or stdout in this bundle. Preserve this original scratch file; add a corrected, separately named verification artifact if the project wants a reproducible identity-check appendix. Do not erase the disclosure or describe the supplied scratch script itself as clean on that diagnostic.

4. **A minor proof-note typo remains.** In §3 Step 3 the parenthetical degree inventory places `s:2` on the low side. It is high, with positive contribution +4. The displayed sum is correct; correcting the prose does not change the proof.

5. **Keep local Git acceptance scoped.** The bundle contains a text history and an empty status export, not Git objects/refs. It reports checkpoint `0f0a39c4d8d97d211782d1a1d81aeba5e0481319`, previous `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685`, baseline `36ea1603602491bf3c1c5b81ed4c23aaa2210e70`. The content diff is consistent; live branch, tag, parent links, clean status and no-push claims were not independently queried from the user's machine. The hash self-reference correction is appropriate. Local Codex should record its eventual acceptance against the actual checkout and a new review commit.

6. **Do not upgrade preflight reporting.** The bundle reports 110 tests with six skipped and successful doctor/demo, but does not include their stdout or the demo record. Report those as OpenChamber's preflight report. The current seed evidence can be reviewed without replaying the full release suite. `certificate=null` is expected for a negative; the checker did not issue an unsatisfiability certificate. Exhaustive solver/oracle evidence and the separate analytic argument establish the scoped result.

7. **The current next-action text needs coordination.** `STATE.md` leads with the pin sweep, conditionally gated on acceptance, while the handoff says acceptance review is the immediate action. This is not evidence that an unauthorized sweep ran. For recovery clarity, record one immediate next action and keep later proposals explicitly separate. The mathematical suitability of the proposed sweep is assigned to the other reviewer.

## Machine-readable audit

See `analysis/evidence_audit.json` for input checksums, record check booleans, environment as reported, full source identity, original digest, and all eight patch blob identities. All implemented content-integrity checks passed. No successor seed pins were tested and no original files or repository files were modified by this reviewer.
