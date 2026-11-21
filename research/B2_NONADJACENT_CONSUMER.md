# B2-NONADJACENT-CONSUMER-001: nonadjacent path consumer

**Disposition:** ACCEPTED as a conditional consumer for integer `K>=2`, after separate mathematical and implementation review. It supplies no prefix. No historical novelty, formal verification or arbitrary-lobster theorem is claimed. Starting checkpoint: `3a7179495c08ae7e79f81e4fb76ee9164310f840`.

## Claim and physical contract

Let integer `K>=2` and integer `ell` be given. In a valid partial labeling of the caller-retained original tree, write the K-edge path as `w_0--w_1--...--w_K`, with physical port `w_0=s:2`. Suppose the only unassigned vertices are the actual path vertices `w_1,...,w_K`, and the only edges incident to them are those original path edges. In the canonical B2 profile, `w_i=s:(i+2)`. Suppose the unused labels are exactly `[ell,ell+K-1]`, the unused differences are exactly `1..K`, and the assigned physical port is `f(s:2)=ell+K+1`. All assigned labels and actual assigned-edge differences are already valid and distinct in the final alphabet `0..m`; in particular the declared interval and port must fit that alphabet.

Then the K path vertices can be labeled using exactly the unused labels and differences, leaving every prefix label unchanged. This is conditional on the full physical and resource contract. It neither constructs a compatible prefix nor establishes that one exists for the unequal family.

## Construction and proof

Use normalized sequences `C_2=(3,1,0)`, `C_3=(4,1,0,2)`, and `C_4=(5,1,2,0,3)`. For `K>=5`, write the already constructed shorter sequence as `C_(K-3)=(K-2,x_1,...,x_(K-3))` and define

```text
C_K = (K+1, 1, K-1, 0, K-2-x_1, ..., K-2-x_(K-3)).
```

Claim by strong induction that `C_K` has `K+1` entries, starts at `K+1`, has suffix entries exactly `0..K-1` once each, and has consecutive absolute differences exactly `1..K` once each. The three bases have suffix/difference lists `(1,0)/(2,1)`, `(1,0,2)/(3,1,2)` and `(1,2,0,3)/(4,1,2,3)`, respectively.

For `K>=5`, the induction hypothesis gives `{x_i}=0..K-4`. Thus the reflected tail `{K-2-x_i}` is exactly `2..K-2`, disjoint from the new suffix entries `1,K-1,0`; together they are exactly `0..K-1`. The new first three edges have differences `K,K-2,K-1`. Reflection `x -> K-2-x` maps the entire old sequence `(K-2,x_1,...)` to `(0,K-2-x_1,...)`. Hence the bridge from the new 0 to the transformed tail, together with all later tail edges, reproduces **all** the old differences `1..K-3`. These sets partition `1..K`, including the boundary case `K=5`. Every recursive argument decreases by three to one of `2,3,4`, so the construction terminates.

Translate every entry by `ell`. The first entry is the existing port `ell+K+1`; place the remaining entries in order on the actual path vertices `w_1,...,w_K`. Translation preserves differences; the suffix uses exactly the unassigned interval once. Its differences are exactly the unused `1..K`, disjoint from the existing prefix differences. No prefix label or original edge changes, so the result is a graceful labeling on the caller's original target.

At `K=1`, the only unused label is `ell`, while the prescribed port is `ell+2`; the only remaining actual edge would have difference 2, not the required 1. Thus this exact interface is impossible for K=1; other interfaces are not ruled out.

## Relation to retained consumer and implementation

The earlier path consumer in `PROOF_OBLIGATIONS.md` uses an endpoint immediately above or below the unused interval and alternates its extreme labels. The present above-side port is **two** above the interval. It is a different conditional contract; `lcl.states.interval_boundary` remains unchanged and correctly rejects this nonadjacent state. No generalized predicate or branch-topology consumer is asserted.

`lcl.consumers.complete_nonadjacent_path(graph, prefix_labels, K, ell)` implements this contract as a separate helper **on graphs accepted by `verify_partial`**, including that checker's lobster requirement, with the specific original path names `w_i=s:(i+2)`. The mathematical argument above applies to any original tree satisfying the stated path and labeling conditions, regardless of the other path vertices' names; the helper has this narrower validation domain. It validates the original graph and prefix, both exact inventories, the physical port, and the exact named remaining edges; returns a new mapping; and checks the result against the supplied original graph with the unchanged independent verifier. Its iterative affine-reflection unrolling implements the recurrence without Python recursion depth. The caller must retain its own original graph and independently verify any produced certificate; this helper does not discover a prefix.

## Review and evidence

The recurrence and proof were separately rederived and challenged by fresh Codex reviewer sessions; a separate reviewer inspected the actual implementation. **Disposition: ACCEPT** the conditional theorem and helper on their stated domains. The reviewer requested a **REVISE** of the implementation's narrower graph/name scope; that clarification is incorporated above. The reviewers are AI sessions, not human peer review or proof-assistant certification. In particular, they checked all three bases, the bridge edge in the induction, original named incidences, resource completeness, and the K=1 exception. `tests/test_nonadjacent_consumer.py` covers original graph certificates and adverse inputs; bounded independent Python regression and reviewer scratch receipts are in `evidence/validation/B2_NONADJACENT_CONSUMER_001/`. Finite checks corroborate the proof but do not replace induction.

The earlier restricted p=4 negative and K>=6 adjacent-port obstruction remain unchanged. A subsequent bounded task independently supplied a compatible prefix for `q=1,r=2,z0=z1=0,K>=2` using a fixed port-5 seed; see `research/B2_NONADJACENT_SEED_P5.md`. The consumer itself does not supply that prefix, and broader unequal profiles remain separate obligations. The superseded pin sweep was not executed.
