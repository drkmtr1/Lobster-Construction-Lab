# B4-JOINT-NESTED-CUT-TWO-HOST-001 evidence

Two originals were built once: the order-18 C(3,4) core and its order-20 t=1 lift. The two
retained originals are the D061 alternative C(2,2) seed and D060 C(2,3).
The D059 result is bound by raw hash to its archived manifest and was not replayed.
Three routes share the one C(3,4) original. The arithmetic audit checks two cuts
on each of six label states without creating extra original records. The single
wrong-digest probe reuses the retained C(2,2) original. There were zero solver calls and
zero labeling-enumeration nodes. See [the proof](../../../research/B4_JOINT_NESTED_CUT_TWO_HOST.md).

## Reproduction

In a disposable checkout at parent `67130f845fe327175a9d6d1821ec54652f55fe70`, use the documented project-local
Python 3.12/3.13. Copy the exact Git blob bytes of the proof, `scope-intake.md`,
`config.json`, `commands.json`, `validate.py`, and `audit.py` from the commit
that publishes this bundle to their recorded paths. Keep HEAD at the parent.
Leave this bundle's `validation/` and `audit_result.json` absent. Run the
PowerShell commands in [commands.json](commands.json) once in recorded order
from the repository root, using a separate process for each `exit`-terminated
command. Preserve the archived outputs. Timing and runtime
identity fields may differ on another run.

`validation/identity.json` records the runtime, source hashes, and configuration
bindings. `command_receipts.json` records the actual invocations and exit results.
`MANIFEST.json` hashes raw bytes and excludes only itself within this bundle.
