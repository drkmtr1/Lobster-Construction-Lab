# B2 unequal seed — independent acceptance review pack

Start with `REVIEW_REPORT.md`. The central result is: **the p=4 seed negative is correct; revise the queued plan; the original interval/adjacent-port interface is impossible for q=1, r=2, zero padding, every K>=6.** This is an interface obstruction, not a nongraceful-lobster result.

## Contents

| Path | Purpose |
|---|---|
| `REVIEW_REPORT.md` | Complete review, verdicts, explanations, evidence and corrections |
| `B2_INTERFACE_OBSTRUCTION.md` | Full new quantified proof, with scope and independent review |
| `CODEX_REVIEW_AND_RECORD_PROMPT.md` | One bounded follow-up task for the existing local checkout |
| `independent_seed_check.py` | Standard-library audit of the exact completed p=4 question |
| `independent_seed_check.json` | Observed result, all 144 named assignments, hashes and environment |
| `supplied/` | All 21 uploaded files, byte-for-byte, with normalized path separators only |
| `original_upload.zip` | The byte-identical original uploaded ZIP |
| `analysis/` | Three independent review notes, forensic JSON, recovered UTF-8 patch |
| `source_snapshot/` | The 21 preserved source files matching both historical run inventories |
| `context/` | The supplied research plan defining the original B2 interface |
| `MANIFEST.json` | Raw file hashes, source/archive identity, and packaging scope |

The supplied files and historical results are not silently edited. This pack is a review deliverable, not an installer or replacement repository. It has not changed Will's Windows checkout or started the queued pin sweep.

## Optional local reproduction

With Python 3.12/3.13, from this directory:

```powershell
python .\independent_seed_check.py --supplied .\supplied --out .\independent_seed_check_local.json
```

This checks precisely 144 assignments for p=4 with a two-second cooperative limit. It does not import project code or enumerate new pins. The output filename must not already exist. A complete observed run is already provided, so no replay is needed just to read the review.

## Applying the findings

Give `CODEX_REVIEW_AND_RECORD_PROMPT.md` to Codex in the current Lobster Construction Lab project. It asks for local reconciliation, scoped acceptance, evidence preservation and record updates, then stops before any successor research. It does not authorize remote pushes or installation.
