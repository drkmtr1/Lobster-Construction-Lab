# Codex handoff — D097 three-quota alpha supplier

November 23, 2026, Pacific/Honolulu · `LCL-R241-QAR-ALPHA-SUPPLIER-001` · parent `7da574dbcef308f9d0f9340a7735844bdc00182f`.

**ACCEPT** A(q+a+r+5,q+a+2;q+1,q+2) on ordered named `[[q,a],[r]]` for exact integers q,a≥2 and r≥q. At r=q, the original edge groups partition [1,a+2q+4]. Further named right terminals take consecutive new labels and differences at physical `b:1:0=0`, preserving all old labels and incidences, cut, physical ports and the spine. The high class has r+3 vertices, so the specific exit offset q+2 fits exactly when r≥q. The formulas specialize pointwise to D096 and to D089 at q=r=3, with D087 at q=r=2.

[Proof](../research/R241_QAR_ALPHA_SUPPLIER.md) · [Evidence and reproduction](../evidence/validation/LCL_R241_QAR_ALPHA_SUPPLIER_001/README.md) · [Separate reviews](../evidence/validation/LCL_R241_QAR_ALPHA_SUPPLIER_001/REVIEWS.md) · [Manifest](../evidence/validation/LCL_R241_QAR_ALPHA_SUPPLIER_001/MANIFEST.json)

The sole new original `[[4,2],[4]]` has 15 vertices and 14 edges, cut eight, spine labels 5 and 14, offsets (5,6), and both unused inventories empty. The unchanged checker, independent audit, D089 and D096 controls and all three adverse rejections passed. Both separate read-only reviews accepted. One official worker used 0.09375 process-CPU seconds with zero joins, solvers, assignment visits, retries or replays. Historical evidence, scoped exclusions, D083 and D093 original and versioned records, deferred D076, baseline and upstream pins remain preserved.

**ADVANCE** by testing a physical port choice that could admit smaller right quotas relative to the first ordered center. For the proposed slice r≥a and q>r, exit offset a+2 fits the high class while q+2 exceeds it. Transport through the named first-section center roles is a separate obligation. **Project instructions KEEP.**

Resolve this checkpoint from the handoff's introducing commit and independently verify GitHub main.

## One next action

Under separate authorization, prove or refute transfer of D097 to exact ordered `[[q,a],[r]]` on the uncovered slice r≥a≥2 and q>r, at offsets (a+1,a+2). Check the named transport from `[[a,q],[r]]` by exchanging the first-section center roles and their indexed terminal groups while keeping the spine and right center fixed. Use at most one boundary original `[[4,2],[2]]`, with no joins, solvers or assignment enumeration.
