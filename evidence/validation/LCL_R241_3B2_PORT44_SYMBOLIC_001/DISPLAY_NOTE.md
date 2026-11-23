# Post-run PowerShell display incident

The single official Python command in [command_receipt.json](command_receipt.json) finished with exit 0 and recorded PASS, with the independent audit also PASS. After it returned, the PowerShell wrapper tried to summarize the already-written result using `ConvertFrom-Json` without `-AsHashtable`. PowerShell reported:

> Cannot convert the JSON string because it contains keys with different casing. Please use the -AsHashTable switch instead. The key that was attempted to be added to the existing key 'A' was 'a'.

The wrapper returned 1 from this post-run display step. Raw receipt and result were preserved. A subsequent read-only PowerShell parse with `-AsHashtable` confirmed the saved result's SHA-256 `d94f46b596a2f5bf9eeb28bef587ad348c84155082dda82c74369521e5a9e4a5`, audit PASS, and the ten extremal records. No Python invocation, retry, audit repair or modification to the saved records occurred in that readback.
