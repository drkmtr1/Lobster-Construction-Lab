# B4-12T2-ZERO-HOST-SUPPLIER-001 evidence

[Proof](../../../research/B4_12T2_ZERO_HOST_SUPPLIER.md) · [Configuration](config.json) · [Identity](validation/identity.json) · [Commands](commands.json) · [Reviews](REVIEWS.md) · [Byte manifest](MANIFEST.json)

| Evidence | Exact cases | Orders | Outcome |
|---|---|---|---|
| New normalized prefixes | t=3,4,5 | 17,18,19 | All three passed; t=3 is the fixed seed |
| New completed originals | (t,K)=(3,2),(3,3),(4,4),(5,5) | 19,20,22,24 | All four passed |
| Retained control | The accepted normalized r=2 ledger of 1R22 | 16 | Original certificate passed; port-preserving upper insertion failed the exact premise |
| Invalid-input probes | True, float, string, and below-minimum integer for each of t,K | No graph | All eight rejected |

The validator saves each new exact original named graph and digest
before assigning labels. Both t=3 completions use the same recorded
normalized certificate. The validator checks the shifted prefix,
actual s:4, both complements and every pending edge before invoking
the unchanged numeric helper. It verifies the completed labeling
against that retained original.

The [batch comparison](validation/batch_comparison.json) compares the
direct t=5 normalized labels, one batch of two from t=3 and two batches
of one through the already declared t=4 prefix. It checks pointwise
equality, original incidences and the unchanged ports, host and witness.
The validator then shifts and completes the one declared (5,5) target.
There are no extra normalized or completed cases.

The [independent audit](audit_result.json) reconstructs names, roles and
incidence multiplicities, recomputes original identities and spectra,
and checks witnesses, both complements, the suffix, the one retained
control, all guards and the normalized batch comparison. It imports
neither LCL nor the validator and adds zero cases. [Summary](validation/summary.json)

One worker, a 24-vertex cap, and a 2,000,000-byte record cap applied.
The largest completed certificate was 7,390 bytes. CPython 3.13.17 on
Windows ran the two scripts once each. No solver queries, computational
enumeration, historical replays, or production modifications occurred.

The manifest, frozen proof, scripts, config and snapshots bind raw bytes.
Retained JSON requires raw equality. The audit accepts a uniform LF or
CRLF comparison only for retained Markdown. The adjacent argument is
identified by its raw parent Git content because its owning proof-
obligation ledger is updated at closeout. Staged snapshot bytes match
working source bytes, with a separate normalized-text comparison to
the parent Git sources where applicable.

For reproduction, use a separate checkout at the recorded parent and
the documented project-local Python. Copy the exact proof, config
and both scripts and leave the output directory unused. Run the
recorded commands from the project root in order. The archived outputs
are exclusive and remain immutable.
