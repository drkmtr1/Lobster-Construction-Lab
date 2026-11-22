# Reproduction errata

## B4-1R32-K1-ROOTED-CORE-001

The [archived evidence README](../evidence/validation/B4_1R32_K1_ROOTED_CORE_001/README.md)
describes a checkout of the published source. The
[validator](../evidence/validation/B4_1R32_K1_ROOTED_CORE_001/validate.py)
checks that HEAD equals the recorded parent, so a checkout
at the published results checkpoint fails that guard.
Use this corrected recipe.

1. Create a disposable checkout at parent
   `648ec01f4eaca4a8f71aa162f057a870485dd93c`.
2. From [published checkpoint eb5745483186287b20bcf155cf4e5265dbfc20a5](https://github.com/drkmtr1/Lobster-Construction-Lab/commit/eb5745483186287b20bcf155cf4e5265dbfc20a5),
   copy these exact file bytes to their original paths in that
   checkout, keeping HEAD at the parent.
   - `research/B4_1R32_K1_ROOTED_CORE.md`
   - `evidence/validation/B4_1R32_K1_ROOTED_CORE_001/config.json`
   - `evidence/validation/B4_1R32_K1_ROOTED_CORE_001/validate.py`
   - `evidence/validation/B4_1R32_K1_ROOTED_CORE_001/audit.py`

   For a raw extraction, capture `git show <checkpoint>:<path>`
   as bytes and write those bytes to the destination, for example
   with Python subprocess and pathlib. Avoid PowerShell text
   redirection for byte-sensitive files.
3. Leave the task's `validation/` directory and
   `audit_result.json` absent in the disposable checkout.
4. Run from the repository root using the
   [documented project-local Python](OPERATIONS.md) and the
   [recorded commands](../evidence/validation/B4_1R32_K1_ROOTED_CORE_001/commands.json).
   Run each saved command in a separate PowerShell process from that
   root because the command ends with `exit $LASTEXITCODE`.
5. Keep the archived evidence intact. The reproduction writes
   only to the disposable checkout.

This corrects reproduction instructions. The accepted mathematics,
saved certificates, command receipts, source identities and raw
manifest remain unchanged. No replay was performed for this
erratum.
