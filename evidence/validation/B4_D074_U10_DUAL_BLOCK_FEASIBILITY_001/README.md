# D075 exit-ten dual-block evidence

[Proof](../../../research/B4_D074_U10_DUAL_BLOCK_FEASIBILITY.md) · [Intake](INTAKE.md) · [Separate reviews](REVIEWS.md)

The two archived D066 and D070 maps have distinct ledger IDs on a shared named original. Both pass the unchanged checker and the wrong expected digest is rejected. Their physical exit is 9. The independent audit reconstructs named roles and incidences, verifies the 19 necessary count pairs, and checks the local residual arithmetic and the K=2 gate. It also validates the original incidence and difference alphabets of the archived controls. The result for exit ten is symbolic and supplies no candidate ledger or suffix graph. The raw diagnostic includes the arithmetic of each residual subtraction required by the proof.

## Reproduction

Use a disposable checkout at `c14ffe773d67f528bd948d2a4d09f256836d4571` and keep HEAD at that parent. Copy the exact Git bytes of the external proof plus this bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `verify_controls.py`, `audit.py` and `run.py` into their published paths. The config records the executable identity and raw source hashes. Keep the archived controls at their retained paths.

With all generated output names absent, run the driver command in [commands.json](commands.json) once from the repository root using the recorded project-local runtime. It checks absent outputs before either command, runs stages sequentially and preserves a command receipt even on failure. Stop on a failure and preserve saved output. The [official receipt](command_receipts.json) records the combined measured process CPU, including setup. The manifest binds all bundle files except itself, plus the external proof.
