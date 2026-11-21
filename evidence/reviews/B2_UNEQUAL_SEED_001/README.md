# Tracked evidence: external B2 independent review pack (B2-UNEQUAL-SEED-001)

**Created:** November 21, 2026, Pacific/Honolulu, by the bounded integration task `OC-20261121-b2-review-integration`.
**Status of everything in this directory:** PROVISIONAL_INTEGRATION_PENDING_CODEX_REVIEW. This directory preserves review evidence and one new adopted proof note; it is not an independent Codex acceptance review, not external peer review, and not a formal certificate.

## Purpose

An independent outside session (CPython 3.12.14, Linux; a different machine from this checkout) reviewed the export of OpenChamber checkpoint `0f0a39c4d8d97d211782d1a1d81aeba5e0481319` (following `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685`) and returned the pack `LCL_B2_Independent_Review_2026-11-21`. This directory is the tracked custody location for:

1. The two historical run records and their exact inputs, preserved byte-for-byte (the `runs/` directory is Git-ignored; before this copy, the records existed only on this machine plus inside the review pack's ZIP).
2. The review pack's core deliverables (report, new proof note, Codex prompt, README, manifest, independent check script/result, three analysis notes, the reviewer scratch).
3. This integration's own verification of the pack and of the local evidence.

## Layout

| Path | Content |
|---|---|
| `raw/runs/dfs-20261121T081441Z-0a3c9a64/` | Byte copy of the historical DFS negative (`record.json` + `config.json`) |
| `raw/runs/oracle-20261121T081441Z-a5f3c783/` | Byte copy of the historical oracle negative (`record.json` + `config.json`) |
| `raw/examples/unequal_seed{,_pins,_domains}.json` | Byte copies of the exact target/pin/domain inputs |
| `raw/configs/unequal_seed_limits.json` | Byte copy of the limits input |
| `pack/REVIEW_REPORT.md` | The pack's complete review: verdicts, corrections, provenance limits |
| `pack/B2_INTERFACE_OBSTRUCTION.md` | The pack's new K≥6 interface obstruction (adopted verbatim into `research/B2_INTERFACE_OBSTRUCTION.md`) |
| `pack/CODEX_REVIEW_AND_RECORD_PROMPT.md` | The pack's follow-up task description for Codex |
| `pack/README.md`, `pack/MANIFEST.json` | Pack layout and raw-byte checksum manifest (55 entries) |
| `pack/independent_seed_check.py` / `.json` | The pack's standard-library 144-assignment audit and its observed result |
| `pack/analysis/` | `math_review.md`, `next_step_review.md` (the two agent challenges of the new proof), `evidence_review.md`, `evidence_audit.json`, `checkpoint.normalized.diff` (recovered UTF-8 patch; the raw exported `checkpoint.diff` is not preserved here — see below) |
| `pack/supplied/b2_review_scratch.py` | The earlier reviewer scratch, preserved as the diagnostic version (see `research/B2_UNEQUAL_SEED.md` §4) |
| `verify_b2_review_pack.py` | This integration's read-only verification script (33 checks) |
| `verification_result.json` | Observed result: 33/33 passed (CPython 3.13.17, Windows-11, 2026-11-21T16:32:41Z; script SHA-256 `448d9bfb3f2d535ff0686a280651ccd811a16268044de8c707c8ef39033fd3b3`) |
| `RAW_FILE_MANIFEST.json` | Raw SHA-256 of every preserved byte copy in this directory |

**Not copied (deliberate):** the pack's `original_upload.zip` (66,234 bytes; preserved by hash only: raw SHA-256 `a2def9c494ff49d7dbe89ca10416b1da804e82052c9a79db773ae50c819e2b97`; the unpacked contents are byte-verified against its MANIFEST, checks F1/F2); the pack's `supplied/` tree other than the scratch (those 21 files are byte-identical to the project's own tracked files at the reviewed checkpoint and are verified per-file, checks A1–A7 and E1–E3); the pack's `context/` (a copy of `docs/RESEARCH_PLAN.md`, already tracked). The original download location `C:\Users\Will\Downloads\LCL_B2_Independent_Review_2026-11-21\` remains the machine-local source for the zip and the full `supplied/` tree.

## Hash schemes (do not conflate)

- **Raw file SHA-256** (`RAW_FILE_MANIFEST.json`, pack `MANIFEST.json`): SHA-256 of the file's bytes on disk.
- **`record_sha256`** (a field inside each `record.json`): SHA-256 of the canonical JSON (sorted keys, compact separators, UTF-8) of the record **with the `record_sha256` field omitted**, as computed by `lcl.records.save_single`. It is not a whole-file hash; recomputing it requires omitting the field (checks C1/C2).
- **`config_sha256`** (a field inside each `record.json`): canonical digest of the parsed config **object**, not of the `config.json` file bytes (checks D1/D2).
- **Source inventory** `2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd`: digest over the 21 tracked `lcl/` + requirements + pyproject files (checks E1–E3).
- **Graph digest** `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`: digest of `build_graph([[1],[2],[]])`, embedded in both records (checks G1–G3).

Canonical values for the two preserved records (also in `RAW_FILE_MANIFEST.json`):

| Record | `record_sha256` (canonical) | `config_sha256` (canonical) |
|---|---|---|
| `raw/runs/dfs-20261121T081441Z-0a3c9a64/record.json` | `f03d968e014e17d37382ef60a1836177497e388b86d779501fbe6b9dc0071f05` | `949e505923d13323e3cb76628773bdee09ed9fee600a49ed88adbb3c7611bdb6` |
| `raw/runs/oracle-20261121T081441Z-a5f3c783/record.json` | `d8c0359adc279d46e5aaffc6cd7affbf7aa70304f659dbc572f5f2eaf978a489` | `d0603cf8cf345118b4cddc7423fc573cc576e06e7b77c6b62a3c0c3d8f9673ec` |

## Verification actually performed

`verify_b2_review_pack.py` (read-only; modifies no source, checker, configuration, or target; runs no solver) executed 33 checks, all passed:

- **A1–A7** byte identity, local vs pack: both `record.json`, all four input JSONs, the reviewer scratch.
- **B1–B10** raw SHA-256 of both records, both configs (reported only), the pack zip, the four inputs, the scratch.
- **C1–C2** canonical `record_sha256` recomputation (field omitted).
- **D1–D2** `config_sha256` recomputation from the local config objects.
- **E1–E3** source inventory digest + 21-file byte match against the pack `source_snapshot/` + per-file record hashes.
- **F1–F2** all 55 pack MANIFEST entries (bytes + SHA-256); manifest set == pack file set.
- **G1–G3** graph digest from a fresh `build_graph([[1],[2],[]])`; both records' embedded `original_graph` equal to the fresh build.
- **H1–H4** this integration's own 144-assignment enumeration of the p=4 restricted negative (independent of the DFS record, the oracle record, and the pack script): exactly 144 domain-admissible assignments, **0 graceful**, 36 with `h(s:1)=3`, 0 general-identity mismatches (`S=a+2b−x−2y+16`).

No discrepancy was found between the pack, the local records, and the local source.

## Replay commands (optional)

From the project root, with the project virtual environment:

```powershell
.\.venv\Scripts\python.exe evidence\reviews\B2_UNEQUAL_SEED_001\verify_b2_review_pack.py
```

An optional first argument names a different pack root; the default is the local download path. Note: a replay **rewrites** `verification_result.json` (timestamp, platform fields); review the diff before committing any replay.

The pack's own seed audit (standard library only; imports no project code; refuses to overwrite an existing result file) can be replayed from the original download location, which still holds the full `supplied/` tree:

```powershell
cd C:\Users\Will\Downloads\LCL_B2_Independent_Review_2026-11-21\LCL_B2_Independent_Review
python .\independent_seed_check.py --supplied .\supplied --out .\independent_seed_check_local.json
```

Python 3.12/3.13. The observed output is already preserved at `pack/independent_seed_check.json`; replaying is optional.

## Provenance notes

- The repository `.gitignore` originally ignored every directory named `runs` (pattern `runs/`), which silently excluded the curated byte copies in `raw/runs/` above from tracking (confirmed with `git check-ignore`). This integration scoped that pattern to the repository-root working directory (`/runs/`), the directory whose local work it was written for; only two directories named `runs` exist in the repository (the root working directory and this evidence copy), so nothing else changed. The change is recorded in decision D016.
- The pack's exported `checkpoint.diff` (not preserved here) carries reversible CP437/UTF-8 mojibake from a PowerShell native-output export; the recovered, verified patch is `pack/analysis/checkpoint.normalized.diff` (all eight postimages verified against the archived preimages; 246 additions, 27 deletions; no source/checker/configuration change in that patch). Future diff exports should use Git's `--output` path.
- The historical `b2_review_scratch.py` is the **earlier diagnostic version**: it applies the `y=3`-restricted identity `S=a+2b−x+10` to all 144 assignments (the source of the disclosed 108 apparent mismatches). It is preserved unchanged; the corrected general identity check is cited in `research/B2_UNEQUAL_SEED.md` §4.
- The pack does not contain Git objects or refs; it does not certify this checkout's live branch, tag, parent links, or absence of a push. Git state was verified locally for this integration (HEAD `0f0a39c`, clean tree, tag `lcl-v0.1.0-baseline` at `36ea1603` untouched).
