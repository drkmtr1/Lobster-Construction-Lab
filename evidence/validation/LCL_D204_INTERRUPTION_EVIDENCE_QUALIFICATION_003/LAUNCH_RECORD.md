# Proposed one-shot D204 scientific launch and Owner authorization

The V9 qualification covers the exact frozen supervisor on the observed Windows host. This record is an authorization draft. No active approval exists. Run only after the Owner separately approves the scientific execution and the fresh repository and runtime admission checks pass.

## Command for the separately authorized session

The fixed task is `LCL-D204-INTERRUPTION-EVIDENCE-QUALIFICATION-003`. The fresh scientific run uses `d204-science-v9` and writes only to `evidence/runs/d204-science-v9`. The approval and ref receipt must occupy `runs/d204-science-v9-approval.json` and `runs/d204-science-v9-live-refs.json` under that authorization. Use the already installed exact base CPython 3.13.17 AMD64 binary.

```powershell
Set-Location -LiteralPath 'C:\Users\Will\Projects\Lobster_Construction_Lab'
$basePython = & .\.venv\Scripts\python.exe -I -S -B -c 'import sys; print(sys._base_executable)'
& $basePython -I -S -B .\research\d204_readiness_v9\entry.py LCL-D204-INTERRUPTION-EVIDENCE-QUALIFICATION-003 official fea8700e37f7a51ca30f0b79558a91b23457f63c6ebfbc28786a664cda895dc7 '<sha256-of-separate-Owner-approval>'
```

The ref sidecar contains `task`, `run`, `checked_unix` as an integer and `refs` with `lcl_main`, `mdl_head`, `bounded_search_head`, `tag` and `peel`. In the newly authorized admission session, obtain live read-only ref observations, confirm the clean local and remote approved head, and confirm a vacant run identity. The observed refs and the live-ref receipt must match the approval and be at most 900 seconds old on entry. Use the same frozen runtime and dependencies. The entry checks the committed ready marker and freeze, all archived native qualification receipts required by its gate, the explicit fresh authorization, and exact input/source bytes.

The future approval contains `intent = AUTHORIZE_ONE_D204_SCIENTIFIC_RUN`, `task`, `run = d204-science-v9`, `freeze = fea8700e37f7a51ca30f0b79558a91b23457f63c6ebfbc28786a664cda895dc7`, `qualification_sha256` of the committed V9 readiness receipt, `approved_repository_head` of the reviewed checkpoint, `live_ref_receipt_sha256`, `verified_live_refs`, the exact `limits` map from the freeze and the Owner's nonempty `owner_authorization` text. The placeholder in the command is the hash of that future approval record.

## Owner authorization draft

> I authorize exactly one D204 scientific execution with V9 under the accepted Windows measured-acceptance contract and the approved checkpoint, runtime, freeze and readiness receipt. Use the new d204-science-v9 identity and the independently supplied 32-edge prefix on the exact 41-edge original. Keep frontier 0, induced old cut 14, physical cuts 18 and 19, threshold C+2, both rank classes and 8,518,360 prospective cut-geometry occurrences. Use the 48-edge original only for deterministic continuation verification. Bind the exact accepted logical counters, 172,800 CPU and 259,200 elapsed seconds for primary, 345,600 CPU and 432,000 elapsed seconds for audit, sequential one-worker operation and the shared 128,000,000-byte evidence ceiling. Use the 250 ms target, 2,000 ms observed-gap maximum, 60-second CPU and elapsed early reserves, 10-second cleanup reserve and 65,536-byte terminal evidence reservation within that ceiling. Enforce native Job user CPU protection, sampled combined CPU and elapsed supervision, and mandatory final measured acceptance. Run primary once. Admit independent audit only after valid primary exhaustion. Preserve candidate and receipt before same-phase independent verification. Observe the accepted interruption, discrepancy, incomplete and failure dispositions. Stop after the one authorized result. No retry, scope expansion or successor is authorized.

[Qualification receipt](V9_FINAL_QUALIFICATION.json) · [Exact freeze](V9_FREEZE.json)
