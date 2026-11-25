# D136 interleaved rotation-packet allocation

**ACCEPT** the coefficient-one capacity theorem at parent `298a477eb8ec482caa649304d65eb529f78d3edf`. Complete rotation packets use every coordinate and no middle quota. At most 2p−1 weighted mass matches leave fewer than 2p(2p−1) actual residual tokens for the D135 cycles. The resulting deterministic two-band packing is sufficient at Q≥N+(2p−1)(2p(p−1)+1). The strict symbolic improvement family and exact D134 closure are proved. [Proof](../../../research/ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md)

## Verification

- Rechecked D105 and D130 against their frozen original owners with the unchanged checker and separate incidence reconstruction.
- Inspected exactly their two maximum cuts. D105 crosses at weights {12,13} and D130 at {19,20}, on the actual spine exit and right attachment.
- Reconciled D104 and D131–D135 archive bindings. The two official phases ran once each on project-local Python 3.13.17, using 0.84375 process-CPU seconds and 1.7173414 supervised wall seconds combined. Both standard-error files are empty.
- No new original, certificate, allocation, permutation, initialization, transition or suffix list was generated. The quantified proof supplies the mathematical result.

## Controls

1. The unchanged checker rejects the wrong expected D105 original digest.
2. At a=b=p and p≥2, occupied residue classes are disjoint even where spans overlap. Packet width 2p saves p(p−1) coordinates. Repeating a residue cycle would reuse actual coordinates.
3. At z=ab−1 for a nonempty match, the floor reserves zero packets and rounding upward overdraws one unit of mass. Integer residual counts come from aggregate actual consumption, with equal residual signed masses.
4. A strict interior split of a packet has crossing arcs both ways. Its full permutation and displacement counts persist, while the required crossing band fails.

The prior D134 symmetric and D135 displacement-cycle suppliers retain their separate sufficient domains. [Result](result.json) · [Command receipt](command_receipt.json) · [Preflight supervision](preflight_supervision.json) · [Verification supervision](verification_supervision.json) · [Reviews](REVIEWS.md) · [Manifest](MANIFEST.json)
