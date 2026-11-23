# D074 exit-eight dual-block evidence

[Proof](../../../research/B4_D073_U8_DUAL_BLOCK_STRUCTURAL.md) · [Intake](INTAKE.md) · [Separate reviews](REVIEWS.md)

The unchanged checker validates both retained D066 and D070 alpha certificates on their single original and rejects one deliberately wrong expected graph digest. Both retained labels at physical s:4 are 9. The independent audit reconstructs all named parent incidences and edge multiplicities. It checks the degree counts, the u=9 collision and weight-one boundary, the named premises for descending weights and containment, and the forced excluded fourth-terminal edges. It records the actual archived D070 cut sets separately from the conditional edge sets in the structural proof.

The proof covers all allowed labels and cuts. The audit uses no numerical (a,d,u,B) tuple sweep, no label search and no new original. The retained control script is copied byte for byte from D073. The arithmetic audit imports neither that script nor production code.

## Reproduction

Use a disposable checkout at `8bf03ba3a2e3df850e893b153f5d5a6384820986`. Leave HEAD there and copy the exact Git blob bytes of this proof and the bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `verify_controls.py`, and `audit.py` to their published paths. Keep the retained archived inputs in place. The configuration records the exact Python version and executable hash.

With generated outputs absent, run [the two commands](commands.json) once in order from the repository root. Stop on a failure and preserve all records. Both scripts exclusively create output files. The [official receipts](command_receipts.json) record the single-worker sequence, and the audit totals measured process CPU including input setup. The byte manifest covers every bundle file except itself, plus the external proof.
