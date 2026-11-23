# D089 symbolic (4,5) supplier

`LCL-R241-3B3-PORT45-SYMBOLIC-001` · November 23, 2026, Pacific/Honolulu · parent `507dff9d301521a6e533f0c68f920da82f770a59`.

[Proof](../../../research/R241_3B3_PORT45_SYMBOLIC.md) · [Named boundary original](original.json) · [Certificate, controls and independent audit](result.json) · [Official receipt](command_receipt.json) · [Reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** A(b+11,b+5;4,5) on the exact named `[[3,b],[3]]` original for every integer b≥2. The formula supplies all labels and differences independently of a complete-target solution. The proof covers the full parameter domain. The b=2 boundary certificate corroborates the named construction.

| Boundary item | Value |
|---|---|
| Order, size and cut | 13, 12 and 7 |
| Physical entrance and exit | s:0=4 and s:1=12 |
| Canonical original graph digest | `b23da76e59640ebf2259fe83b04c1b67df992df785519f79e6c4bb0f470d267a` |
| Distinct labeling ledger ID | `ea5f7023ab16e35c974077a26ace977dc78d2f0b9886d797c048f99fc10ece3e` |
| Edge weights in original order | 8, 4, 7, 6, 5, 3, 2, 1, 12, 9, 10, 11 |

One worker ran the one official producer and independent-audit sequence in 0.171875 process-CPU seconds. It froze one new named original before labeling, verified its one certificate, rechecked the D087 b=5 and D086 b=4 certificates on their own originals and bound the D088 scoped negative by the retained hashes. The unchanged original-target checker rejected the false digest and terminal swap. The separate physical-port gate rejected the false (4,4) declaration. Swapping l:0:0:0 and l:0:1:0 repeats weights 3 and 6 twice each and omits 2 and 7. There were zero complete-assignment visits, search states, search nodes, solver calls, joins, retries, restarts or replays.

An initial PowerShell preflight stopped before Python because the shell wrapper misparsed CRLF-delimited hash output. The corrected wrapper checked the same pinned source hashes and confirmed all three official output paths were vacant. Only one Python invocation occurred.

## Reproduction

For a separately authorized reproduction, use a disposable checkout at parent `507dff9d301521a6e533f0c68f920da82f770a59`. At their original paths copy the exact published `run.py`, `audit.py`, `config.json`, bundle `.gitattributes`, [proof](../../../research/R241_3B3_PORT45_SYMBOLIC.md) and root `.gitattributes`. Keep HEAD at the recorded parent. Check the three input hashes in the receipt and the retained source and runtime hashes in the configuration against the raw bytes. Use the configured project-local Python executable. Leave `original.json`, `result.json` and `command_receipt.json` absent. From the checkout root run once:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_3B3_PORT45_SYMBOLIC_001/run.py
```

The command creates the three output files in order. The independent standard-library audit runs inside the same process and is saved in `result.json`. Compare scientific results, source identities and scope to the archive. Runtime timing and path fields reflect the fresh environment.
