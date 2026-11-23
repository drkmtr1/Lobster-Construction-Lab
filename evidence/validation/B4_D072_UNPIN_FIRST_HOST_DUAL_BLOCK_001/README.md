# D073 unpinned-first-host dual-block evidence

[Proof](../../../research/B4_D072_UNPIN_FIRST_HOST_DUAL_BLOCK.md) · [Intake](INTAKE.md) · [Truth table](TRUTH_TABLE.md) · [Proof correction](CORRECTIONS.md) · [Reviews](REVIEWS.md)

The two complete D066 and D070 archive maps are checked against the unchanged shared named original. The wrong-digest control uses the complete otherwise valid D070 map. The arithmetic audit reconstructs role parents and edge multiplicities separately, verifies the full D070 upper block and its three failed lower blocks, binds the accepted D072 result and records 1,568 allowed numerical tuples. The table records each side's degree condition and the applicable proof case. It generates zero graphs, vertex-label assignments or seeds.

## Reproduction

Use a disposable checkout at `2743854581108fb1c015710a79fec135fb558c85`. Leave HEAD there and copy the exact Git blob bytes for the proof plus this bundle's `.gitattributes`, `INTAKE.md`, `CORRECTIONS.md`, `TRUTH_TABLE.md`, `config.json`, `commands.json`, `verify_controls.py` and `audit.py` to their published paths. Keep the retained inputs in place. The configuration freezes their raw bytes, Git blobs, and Python version and executable hash.

From the repository root, run [the two commands](commands.json) once and in order with generated outputs absent. Stop on a failure and preserve output. The official driver checked those paths before either command, and both scripts exclusively create records. The recorded combined process-CPU time includes input setup. See [the official receipts](command_receipts.json). The manifest binds every bundle file except itself, plus the external proof.
