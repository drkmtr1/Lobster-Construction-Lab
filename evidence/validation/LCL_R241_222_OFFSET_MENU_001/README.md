# D084 physical offset menu — evidence and reproduction

`LCL-R241-222-OFFSET-MENU-001` · November 22, 2026, Pacific/Honolulu · verified parent `b29a443b2d20a270aa3bb62afb27b9fa9b72643c`.

[Proof and 6-by-5 matrix](../../../research/R241_222_OFFSET_MENU.md) · [Machine-readable menu and independent audit](result.json) · [Receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

The single original under study is the [retained D082 original](../LCL_R241_222_STRICT_RETURN_001/strict_original.json), digest `aeab9d0451058925b074e17bf57eeb76e9ac843b7e8e4ba5daca8c02d7e23801`. The second retained graph is the D081 F(2) checker control on its own original. Both new named ledgers remain on the first graph. The two verified pairs are (2,0) and (3,4). There are 28 proved exclusions and no unresolved pairs in the exact prescribed alpha orientation. The [frozen inputs](menu_source.json) supply these two explicit ledgers and the center-case table used in the written proof.

The official one-process verifier called the unchanged checker on the two witnesses and the D081 F(2) control, retained the D082 (1,0) negative without replay, and recorded three adverse rejections. A false graph digest and a terminal swap causing weights 6 and 9 to repeat reached the unchanged checker. An incorrect physical-offset declaration reached the task-local port check, since physical offsets are outside the generic checker's interface. The independent standard-library audit rebuilt the named incidences, checked all 30 menu records and verified the 108 numerical center cases behind the proof table. It independently checked both full certificates and the controls. Numerical center cases are necessary-condition checks with four first terminals unassigned. No solver, search, new original identity, assignment enumeration, join, restart, or retry was used. One worker used 0.09375 combined process-CPU seconds, sampled before the final receipt write.

## Reproduction

For separately authorized reproduction, create a disposable checkout at the recorded parent. Copy the exact published bytes of `run.py`, `audit.py`, `config.json`, `menu_source.json` and the bundle `.gitattributes` into their original paths. Also copy the [proof](../../../research/R241_222_OFFSET_MENU.md) and the repo-root `.gitattributes` as recorded at the published D084 checkpoint. Keep HEAD at the parent, validate the recorded SHA and the raw [configuration](config.json) pins, and leave both `result.json` and `command_receipt.json` absent in the new evidence directory. The official invocation's shell checked HEAD, tracking and local source hashes before launch. Use the documented project-local Python 3.13.17, with the same bound runtime executable hash. From the project root run:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_222_OFFSET_MENU_001/run.py
```

The one invocation runs checker verification followed by independent arithmetic. It produces new receipts with reproduction-specific timing. Preserve archived evidence and do not rerun it in the main checkout.
