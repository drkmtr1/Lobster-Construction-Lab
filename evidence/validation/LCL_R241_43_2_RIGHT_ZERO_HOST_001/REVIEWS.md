# D102 independent read-only reviews

## Mathematical review — ACCEPT

Reviewer `d102_math_review` independently inspected the actual proof, frozen D099 original, audit source, result and execution receipt. The spine, two left stars and right star exhaust the 13 named incidences with multiplicities 1, 5, 4 and 3. The right zero host forces cut classes of sizes 9 and 5 and places label 13 at a right-center neighbor. The right-star weights exclude both left-center labels, and every left-star weight is strictly below M. This forces weight M on the spine for all allowed ports and terminal orders.

The reviewer also summed incidence groups directly. The left terminals contribute 4A+3B−36+x+z. The right terminals contribute 55−A−B−Y−2z. Adding the spine and three attachments yields 19+Y+4A+3B−2x−2z. With z=0 and Y−x=M the two orders require respectively at least 87 and 86 against at most 85. The actual case records, alpha classes and incidence lists agree. The result rejects the exact right-zero-host state and leaves D097–D101 in their respective scopes.

The D098 leaf swap replaces its weight-4 and weight-8 edges with weights 7 and 5. The existing 7 and 5 edges remain, giving both repeats and both omissions. The saved control and execution records corroborate the proof and its stated scope.

## Implementation review — PASS

Reviewer `d102_impl_review` inspected the actual source, independent auditor, unchanged checker, frozen D099 and D098 records, preflight, execution receipt and result. Before invocation the reviewer independently checked the assertion logic, the two computed order bounds, the intended failure paths, and the absence of singleton-repeat or dictionary-order assumptions.

The audit reconstructs the original 13 edges with their exact roles and multiplicities, derives the bipartition by traversal and recomputes the signed-degree and order bounds. The D098 recheck uses its distinct graph digest and ledger ID. The real gates reject a wrong digest, a declared right zero host carrying 3, and a label-alphabet-preserving swap with repeat multiplicities {5:2, 7:2} and missing weights 4 and 8.

All 65 repository-relative input hashes, four frozen task source and contract hashes, runtime pin, linked preflight and result hashes and eight historical status receipts matched. The one parse-only preflight lists each intended definition once, vacant outputs and zero task imports. No bytecode cache occurred in the bundle. The official receipt records one worker and invocation, two order rows, one retained positive and three adverse controls at 0.171875 process-CPU seconds and 0.1843304000212811 in-process wall seconds. New graph identities, certificates, exit tests, solver calls, searches, assignments, joins, replays, retries and restarts are all zero. The execution receipt SHA-256 is `c6f08b35304281c394a68a52d52d63490656ea24d70ded781e284c806b7f0beb`, and the result SHA-256 is `487f94dce4fe1aab26db110ece9a17814decf47108ee1bacf46e09dba4bd88af`. No consequential issue was found.

Both assessments were read-only. They provide independent review and executable corroboration of the stated mathematical argument.
