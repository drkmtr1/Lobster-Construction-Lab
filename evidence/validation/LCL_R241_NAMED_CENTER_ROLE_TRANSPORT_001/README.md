# D098 named center-role transport evidence

`LCL-R241-NAMED-CENTER-ROLE-TRANSPORT-001` · November 23, 2026, Pacific/Honolulu · parent `d4602d5c5fca487992e3efc4f6f572e82c8d99ad`.

[Frozen contract](CONTRACT.md) · [Symbolic proof](../../../research/R241_NAMED_CENTER_ROLE_TRANSPORT.md) · [Named target original](original.json) · [Certificate and independent audit](result.json) · [Syntax preflight](preflight_receipt.json) · [Execution receipt](command_receipt.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**ACCEPT** A(q+a+r+5,q+a+2;a+1,a+2) on exact ordered `[[q,a],[r]]` for exact integers q>r≥a≥2. The explicit D097 source-to-target transport fixes both spine endpoints and the entire right section and swaps the left-center role and terminal group indices together. The audit reconstructs and checks all 13 named vertices and 12 incidences in each direction, including the weight of every paired edge.

| Sole new original | q=4, a=2, r=2 |
| --- | --- |
| Retained D086 source | `[[2,4],[2]]`, agrees pointwise with D097 |
| Independently built ordered target | `[[4,2],[2]]` |
| Vertices, edges, cut | 13, 12, 8 |
| Physical spine labels and offsets | (3,12), (3,4) |
| Actual center labels | (8,9,0) in target order |
| Terminal labels by target group | (4,5,6,7), (1,2), (10,11) |
| Target edge differences in original order | 9, 5, 4, 3, 2, 1, 6, 8, 7, 12, 10, 11 |
| Ascending difference groups | [1,4], {5}, {6}, [7,8], {9}, [10,11], {12} |
| Unused inventories | Both empty |
| Source graph digest | `7b10b6b54067ddd72ab79eb80eaaa8be69a0e40dd5d7fd0c31f8c41cb68ef2bf` |
| Target graph digest | `c602b9934b690cf8bc23e1533840815d1f0ebdc3156f51c361b66c014d9480a0` |
| Target ledger ID | `66750924e7057c3b304ac56021039b3fcded589741ab5b25d2930e8f25ddd658` |

The unchanged checker rechecked the retained positive and separately verified the transported target against its own digest. It rejected use of the source digest as the target identity. The physical interface rejected a changed port declaration. The transport check rejected exchanging the images of the two source terminals with index zero at opposite left centers. This corrupted map remains bijective and replaces two actual target incidences by two wrong-center edges. The independent audit lists all four changes.

One parse-only preflight checked four task inputs and 30 source pins. The sole official sequence used 0.171875 process-CPU seconds with one worker, one new target and certificate, one retained source recheck and three adverse probes. Joins, solvers, enumeration, retries, restarts and replays were zero. At intake 84 retained manifest entries matched. D083 and D093 each retain their original **INCOMPLETE** and separate **PASS** records. The D088 scoped exclusion, baseline tag and peeled commit, and both upstream main pins were preserved.

## Reproduction

Use a disposable worktree at the parent with the pinned project-local runtime. Copy the frozen task sources, configuration, contract, proof and applicable Git attributes into their recorded paths. Leave the four generated receipt and result paths vacant. Run the parse-only preflight once, and proceed only after PASS.

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_NAMED_CENTER_ROLE_TRANSPORT_001/preflight.py aef125a2cc37df74e8ac653d8577572c2bdf3e7c59e30a8f287a6b4b200c4545
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_NAMED_CENTER_ROLE_TRANSPORT_001/run.py
```

The regenerated ordered graph identities, inverse map, actual edge weights, certificate and audit should match. Invocation paths and process time describe the particular run.
