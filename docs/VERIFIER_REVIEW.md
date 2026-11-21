# Independent verifier and bounded counting oracle

## What the verifier establishes

`lcl.verify.verify_certificate(original_graph, labels, expected_graph_digest=None)` checks a finite assignment against the supplied **original named graph**. A successful report establishes that this assignment is a graceful labeling of that graph. It does not establish a general construction, a theorem for a family, an extendible prefix, or an independent supplier.

The verifier uses the Python standard library and imports no model builder, constructor, allocation routine, search solver, or dynamic programming implementation. Its profile reconstruction is a separate implementation of the graph specification. This separation helps catch a shared mistake in a constructor and its graph model; it cannot eliminate every possible specification or implementation error.

For a profile graph it independently rebuilds the canonical physical vertices, spine, branch centers, terminals, incidence, and roles. It compares named edges, not only the number of edges, degree sequence, or unlabeled isomorphism class. A branch with zero terminals remains the canonical branch vertex. Trailing empty sections remain spine vertices. Role index values must have the exact integer type; Python's equality between `True` and `1` does not make them interchangeable here.

For an explicit graph without a profile, vertices and undirected edges specify the target. The graph must be a nonempty simple tree. A declared spine must be a simple path with every vertex at distance at most two from it. Without a spine the verifier deletes leaves simultaneously twice and checks that the remaining core is a path, allowing an empty core. Explicit role metadata, if present, must cover every actual vertex and is bound into the digest; canonical physical role semantics require a profile.

For a full certificate, every actual vertex must appear once in the labeling. Each label must be a true Python `int`, not a Boolean, float, or string, and the values must be exactly `0..m`. Every original edge is inspected. The absolute endpoint differences must be exactly `1..m`, once each. The singleton convention is the label `0` with no edges and no differences. No alpha-labeling, root-zero, or other extra restriction is imposed.

## Binding the original target

Always retain the original input graph outside the solver result and pass that graph to the verifier. Verifying only a graph copied from an untrusted result would let an altered target replace the requested target.

The optional expected digest strengthens the API boundary: retain a digest of the original input before computation, then require it during certificate verification. Digest contents are canonical JSON with sorted named vertices and sorted undirected edge pairs, plus any supplied profile, spine, and roles. Unrelated metadata and `schema_version` are excluded. Vertex-list order and edge-list order do not affect identity; physical profile and role changes do. The digest is a target identity check, not a signature or an attestation that any computation occurred.

`verify_graph` provides the same independent graph ingestion checks in a JSON-safe report. It intentionally does not silently repair malformed input, infer a different physical profile, collapse an isomorphic graph, or change a supplied spine.

## Partial assignments

`verify_partial` checks injectivity, label range, and the distinct differences of edges whose endpoints are already assigned. It reports used and unused labels, used and unused differences, and the assigned frontier vertices that still have unassigned neighbors. A fully assigned valid result is marked `complete`.

A valid partial result does **not** imply that a completion exists. The four-vertex path with its two middle vertices pinned to `0` and `3` illustrates the distinction: the partial certificate is valid, but exhaustive enumeration of its two remaining labels yields zero completions. The unrestricted named path still has four graceful labelings. Neither this failed core nor any other restricted search can establish nongracefulness of the underlying tree.

## Direct permutation oracle

`lcl.oracle.permutation_oracle` is deliberately small and simple. It enumerates all permutations of labels not already pinned onto vertices not already pinned. Each full assignment is tested directly on the original edges. It shares graph ingestion with `verify_graph`; it does not call the certificate-success routine or share search pruning, constructor logic, or dynamic programming state. Its independence is therefore independence of assignment enumeration and spectrum checks, not complete isolation of every input-validation function.

Counts refer to **named bijections**. Graph automorphisms and label complementation are not quotiented out. There are no hidden root pins, alpha conditions, or symmetry reductions. Explicit pins and domains are recorded in the result. Domains filter the permutations; `permutation_domain_size` counts permutations before that domain filter, and `attempted_permutations` includes filtered candidates. Empty domains and pin/domain contradictions establish an empty restricted assignment set immediately and report their reason.

| Result | Meaning |
|---|---|
| `SAT`, `exhausted=true`, `count` | The declared finite assignment set was exhausted and has this exact positive named count. |
| `EXHAUSTED_NO_SOLUTION`, `exhausted=true`, `count=0` | The declared unrestricted or explicitly restricted finite assignment set has no valid assignment. This is a computation report, not a formal negative certificate. |
| `INCOMPLETE`, `count_lower_bound` | A limit stopped evaluation; any witness remains available, and the reported count is only a lower bound. |
| `INVALID_INPUT` | The target, restrictions, or limits were malformed; no count conclusion is made. |

A positive witness found during an interrupted count is still independently checkable, but the overall enumeration result remains `INCOMPLETE`. A cap reached without a witness never becomes a zero-solution conclusion.

The defaults permit at most eight vertices, 100,000 attempted permutations, and five seconds. The permutation and time checks are cooperative between iterations. There is no operating-system memory limit, forced wall-clock termination, or parallel worker management in this oracle. Graph ingestion and one iteration are not preempted midway. Permutation growth is factorial, so this implementation is a small-instance control for the other methods, not a scalable discovery engine.

## Validation performed

The component tests were executed on Linux with Python 3.12.14. They are standard-library `unittest` tests and do not execute upstream MDL code.

```text
python3 -m unittest discover -s tests -p 'test_verifier.py' -q
python3 -m unittest discover -s tests -p 'test_oracle.py' -q
```

The verifier has 12 tests. The oracle has eight tests. Their independent explicit-graph fixtures check these unrestricted named counts:

| Target | Count |
|---|---:|
| Singleton | 1 |
| Two-vertex path | 2 |
| Four-vertex path | 4 |
| Six-vertex path | 24 |
| Six-vertex spider with leg lengths 2, 2, 1 | 16 |

Negative tests cover role swapping, substituted incidence, an altered valid graph with a mismatched retained digest, Boolean role indices, Boolean and noninteger labels, repeated labels and differences, loops, duplicate edges, disconnected graphs, cycles, an invalid declared spine, and a nonlobster with three arms of length three. A graceful subdivided claw whose displayed assignment is not alpha is accepted. A profile with an enormous terminal count and a tiny actual graph is rejected before expanding that profile.

Oracle tests distinguish restricted failure from unrestricted success, inspect explicit domains, cover every cap, check that a cap equal to the complete permutation count permits exact exhaustion, and verify that an interrupted enumeration with a witness retains only a count lower bound. Separate integration checks on five boundary and mixed profiles confirmed agreement between `model.graph_digest` and the independent verifier digest, including preserved trailing empty sections.

These checks establish the tested finite behavior. They are not a proof that the implementation is defect-free, do not prove the lobster conjecture, and do not constitute a Windows execution test. Future verifier changes should retain these controls and receive review separate from any constructor or solver change that motivates them.
