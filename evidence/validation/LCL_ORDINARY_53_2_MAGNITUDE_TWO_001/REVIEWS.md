# Separate D110 reviews

## Mathematics review

Reviewer `/root/d110_math_review` · **ACCEPT** the proof · **REJECT** the scoped interface.

The reviewer examined the actual proof, frozen D108 original and D106 controls, then the exact saved result and command receipt. They independently derived the signed sum and same-parity requirement and confirmed that label 13 can appear only at a right terminal or the sole reversed left terminal. The two right-terminal cases force the label of a right terminal to equal the label of the distinct second left center. The first-left reversal case forces both weight 9 and weight 11 to occur twice on the identified original incidences. The second-left reversal case is impossible by `107<111`. The proof excludes only the specified three pins and sole −2 interface.

The reviewed result SHA-256 is `1dac19ab9806c48fb1e70c0707efa1fc3fda854c099de65bb768bc9e04dfeeda`. The controls agree with independent arithmetic, including the two changed signed values, −1 to −2 and +11 to +10, and the two duplicated and omitted weights of the gate-only fixture.

## Implementation review

Reviewer `/root/d110_impl_review` · **PASS**.

Before preflight and invocation the reviewer inspected the actual proof, producer, separate auditor, preflight, contract and frozen configuration, including variable definitions and all case and control assertions. The review checked the unchanged original-target verifier path, exact named graph and runtime, 179 repository bindings, four task source bindings, case exhaustiveness, repeat multiplicities, and the independent pin and sign checks. The review cleared the frozen inputs for the one official sequence.

Afterward the reviewer independently hashed the actual preflight, command and result inputs and verified the result digest above. They checked the three structural cases, three scalar rows, unchanged checker results, all four actual probes, preserved historical dispositions, the runtime identity and the recorded 0.1875 process-CPU and 0.21349420002661645 in-process wall seconds. The complement independently fails the signed checks. The magnitude-two fixture passes the signed gate and the ordinary checker reports the two expected difference-inventory defects. The resource counts and observed evidence sizes are within limits. Both reviews were read-only and neither reran task code.
