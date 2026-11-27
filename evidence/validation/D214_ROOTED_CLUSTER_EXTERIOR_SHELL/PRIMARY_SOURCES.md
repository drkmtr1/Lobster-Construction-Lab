# D214 primary-source assessment

## Exact rooted existence dependency

Frank Van Bussel, *Towards the Graceful Tree Conjecture*, M.Sc. thesis, Graduate Department of Computer Science, University of Toronto, 2000. The Library and Archives Canada copy has 168 PDF pages, 8,374,543 bytes and SHA-256 `62bc2296c29e5c6d305d626c3c1cbab720d0afcb4f524fc5037bae9c5a9c356e`. Its printed page numbers are offset by eleven in the one-based PDF page numbering for the cited sections. The publicly accessible direct PDF was retrieved and rendered for visual inspection. [Official thesis PDF](https://www.nlc-bnc.ca/obj/s4/f2/dsk1/tape3/PQDD_0011/MQ53395.pdf) · [Library entry](https://central.bac-lac.gc.ca/.item?app=Library&id=MQ53395&oclc_number=1006929582&op=pdf)

| Printed page | One-based PDF page | Relevance |
|---|---:|---|
| 17–18 | 28–29 | Definition 1.13 and Theorem 1.14 give within-class reversal and the canonical one-vertex amalgamation. |
| 102 | 113 | Definition 4.1 gives value 0 at the actual unique center in the even-diameter case. The odd-diameter convention is irrelevant here. |
| 109 and 112 | 120 and 123 | Section 4.2.1 treats separate center-degree-two cases and defines branch size as its terminal count. Section 4.2.2, Theorem 4.5 explicitly covers diameter four and center degree **≥3**. |
| 113–115 | 124–126 | Closed configurations use consecutive unused vertex and weight intervals. The proof sets up endpoint assignments and starts with an explicit at-least-three branch count. |
| 122–123 | 133–134 | Corollary 4.10 finishes the odd-degree case. The even-degree case begins its construction and explains where trivial branches are handled. |
| 124–132 | 135–143 | The even-degree proof uses reductions based on size and parity, with special treatments of residual small cases and the all-size-one case. The conclusion on printed page 132 again gives the at-least-three scope. |
| 136 | 147 | The later ubiquitous-gracefulness proof explicitly invokes Theorem 4.5 when the center degree is three. Its additional noncenter exceptions are outside the present dependence. |

Rendered page 123 unambiguously prints the weak inequality. The searchable extraction of the archival copy sometimes shows a strict greater-than sign or OCR-corrupted digits. The printed statement, proof setup, conclusion and later explicit degree-three use resolve the ambiguity. D214 uses the established Theorem 4.5 as an existence theorem. We inspected the statement, definitions, proof organization and boundary checks, without reproducing each construction in the thesis. The arbitrary positive qᵢ need no parity or equality constraint in that theorem. A trivial branch in the thesis is a leaf attached directly to the center. The D214 central cluster has none.

Frank Van Bussel, “0-Centred and 0-ubiquitously graceful trees,” *Discrete Mathematics* **277** (1–3), 193–218, 28 February 2004, DOI `10.1016/S0012-365X(03)00152-3`. The public publisher abstract corroborates the center-zero definition and the diameter-at-most-four assertion subject to an exception class. The detailed premise and exception boundary used in D214 were checked in the author's primary thesis. The journal body was not used as a separately verified proof. [Publisher article and abstract](https://www.sciencedirect.com/science/article/pii/S0012365X03001523) · [DOI](https://doi.org/10.1016/S0012-365X%2803%2900152-3)

## Composition attribution

Thesis Theorem 1.14 starts with a vertex-disjoint alpha operand and an ordinary graceful operand, both zero at their chosen attachment vertices. It first reverses the numbering within each alpha class, then stretches its high labels and translates the other operand. The D214 shell is supplied already in the resulting maximum-low orientation. Reversing each alpha class first makes its root zero, so the source operation yields the same shared-root arithmetic. The thesis presents canonical amalgamation in its historical discussion of established constructions. D214's scope is the named-family realization and the supplied exterior shell. No original priority is claimed for the amalgamation operation, central existence, shell or resulting family.

[Primary D214 manuscript](../../../research/ROOTED_CLUSTER_EXTERIOR_SHELL_COMPOSITION.md)
