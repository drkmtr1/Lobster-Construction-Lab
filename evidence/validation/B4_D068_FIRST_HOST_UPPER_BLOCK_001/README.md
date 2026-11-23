# B4-D068-FIRST-HOST-UPPER-BLOCK-001 evidence

[Proof](../../../research/B4_D068_FIRST_HOST_UPPER_BLOCK.md) · [Scope and intake](INTAKE.md) · [Reviews](REVIEWS.md)

The fixed original and labeling come from D066. A D068 completion at (t,K)=(3,2) is the second archived positive. The configuration records the exact raw inputs, their Git parent blobs, the executable identity, and the bounds. Graph digests identify named originals. Separate ledger IDs bind the labels to those digests.

Each of `cut-10.json` through `cut-16.json` retains the selected vertices, every actual crossing, complete difference multisets, the cardinality defect, and the sum calculation. The coefficient arrays encode twice the respective sums in increasing powers of h, beginning with the constant term. The independent audit reconstructs both original named graphs and all seven rows from the archived labels and its own edge reconstruction. The wrong-digest control uses the full otherwise valid D066 labeling.

## Reproduce on the recorded parent

Use a disposable checkout at `10af7560e7ca3e48d656cc9539d6c2f8dba05e31`. Copy the exact Git blob bytes of the new proof and the bundle's `.gitattributes`, `INTAKE.md`, `config.json`, `commands.json`, `produce.py`, and `audit.py` into their original paths without advancing HEAD. Reuse the recorded project-local Python 3.13.17 runtime for exact-byte reproduction. The frozen runtime guard checks the interpreter hash and version. The retained archived originals and certificates already exist at the parent.

With all output paths absent, run [the two commands](commands.json) once, in order, from the repository root. Stop if the producer fails. Keep any existing outputs and inspect the error before considering a separately authorized run. Each script exclusively creates its output records. [Command receipts](command_receipts.json) give the one official run. No solver or labeling enumeration is invoked, and no expanded graph is generated.
