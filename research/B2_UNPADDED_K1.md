# B2-UNPADDED-K1-001: direct singleton completion

**Disposition: ACCEPT** for the exact domain below after separate AI mathematical and implementation reviews; neither was a human referee or formal proof checker. Original-target validation is recorded in [the evidence package](../evidence/validation/B2_UNPADDED_K1_001/README.md). This is an explicit corollary of retained R241/R212-B, with no claim of historical novelty. The source reviewer initially misidentified the returned low port and corrected that review: it is `s:2`, not `b:1:0`.

## Exact target and labeling

Let `q,r` be integers with `q>=1`, `r>=1`; booleans are excluded. The original named profile is `[[q],[r],[],[]]`, without direct leaves, so its spine is `s:0,s:1,s:2,s:3` and its edge count is `m=q+r+5`. Branch `b:0:0` is attached to `s:0`, with named leaves `l:0:0:j` for `0<=j<q`; branch `b:1:0` is attached to `s:1`, with named leaves `l:1:0:j` for `0<=j<r`. No edge, vertex, or attachment is added, removed, or identified.

Assign

```text
s:0 = 3             s:1 = q+5       s:2 = 1       s:3 = q+4
b:0:0 = q+3         l:0:0:0 = 2     l:0:0:j = j+3  (1<=j<q)
b:1:0 = 0           l:1:0:j = q+6+j               (0<=j<r)
```

These are explicit parameter formulas; they do not require a full-target solver, a searched prefix, a root pin imposed on other labelings, or a symmetry quotient. The named branch and leaf order above is part of the construction.

## Vertex inventory

The vertices `b:1:0,s:2,l:0:0:0,s:0` have labels `0,1,2,3`. The other first-branch leaves, in increasing index, have labels `[4,q+2]`, followed by `b:0:0=q+3`, `s:3=q+4`, and `s:1=q+5`. The second-branch leaves have labels `[q+6,m]`. These blocks are disjoint and cover exactly `0..m`.

When `q=1`, the range `1<=j<q` and its interval `[4,q+2]` are empty; the adjacent singleton values still cover the entire alphabet. When `r=1` the last block contains one label. All endpoint claims therefore include both lower boundaries.

## Differences on the original edges

| Actual edge or group | Absolute difference(s) |
|---|---|
| `b:0:0--l:0:0:j`, `1<=j<q` | `q-j`, i.e. `[1,q-1]` in reverse index order |
| `s:0--b:0:0` | `q` |
| `b:0:0--l:0:0:0` | `q+1` |
| `s:0--s:1` | `q+2` |
| `s:2--s:3` | `q+3` |
| `s:1--s:2` | `q+4` |
| `s:1--b:1:0` | `q+5` |
| `b:1:0--l:1:0:j`, `0<=j<r` | `[q+6,m]`, in increasing index order |

For `q=1` the first row is empty; the next row supplies difference 1. The table lists every actual edge exactly once, and its disjoint difference blocks cover `1..m`. Together with the vertex inventory this proves the named graph graceful, for every stated pair `(q,r)`. The formulas contain only the finite index ranges `1<=j<q` and `0<=j<r`; each assignment and the final edge are computed in finitely many integer steps, so the construction terminates.

## Prefix and physical singleton contract

Remove only `s:3` from the complete assignment. The assigned prefix contains every other original vertex, with its unique crossing edge `s:2--s:3`. Its unused vertex labels and edge differences are

```text
R = {q+4},  D = {q+3},  physical port s:2 = 1.
```

The remaining original path has one edge; assigning `s:3=q+4` consumes the one unused label and gives exactly the one unused difference. This contract is independently supplied by the explicit prefix and is a direct singleton continuation. It is **not** the adjacent-port contract of P04/P05 in [PROOF_OBLIGATIONS.md](PROOF_OBLIGATIONS.md): here `D` is not `{1}` and the port is `q+3` away from the unused label. The earlier adjacent endpoint consumer is not invoked or generalized.

## Derivation from retained R241 components

The formula also follows from the retained binary alpha composition in [R241's mathematical return](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405), at pinned commit `858a8c1fcfda87ba40bb1adee498a6131504a803`; its [separate review](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4447-L4479) and [corrected final disposition](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4488-L4505) govern its status, rather than the return's historical pending header. The local preserved source is [N241_relational_ports.md](../references/upstream/mdl/N241_relational_ports.md).

Use two disjoint labeled components, with the physical connector `s:0--s:1`:

* Component A is the star on `s:0,b:0:0,l:0:0:j`. Give it `n_A=q+2`, `p_A=q+1`; local labels `s:0=1`, `b:0:0=q+1`, `l:0:0:0=0`, `l:0:0:j=j+1` for `1<=j<q`. Its low port is `L_A=s:0` with offset `x_A=1`; its high port is **`U_A=b:0:0`**, with `y_A=0`. The star's labels and differences cover its alphabets, its edges cross the low/high cut, and the actual path `s:0--b:0:0` witnesses it.
* Component B has `b:1:0=0`, `s:2=1`, `s:3=2`, `s:1=3`, and `l:1:0:j=4+j` locally. Thus `n_B=r+4`, `p_B=2`; choose **`L_B=Z=s:2`** with `x_B=1`, and `U_B=P=s:1` with `y_B=1`. This is the retained R212-B module with `u=2`, `h=1`, and its local branch parameter `q'=r`: `C=b:1:0`, `Z=s:2`, `Y=s:3`, `P=s:1`, and `X_j=l:1:0:j`. The direct-leaf group is empty. The actual edge `Z--P` is its witness.

The required equality `x_A=y_B=1` holds. R241 shifts all A labels by `p_B=2`, leaves B's low labels unchanged, shifts B's high labels by `n_A=q+2`, and joins the actual edge `L_A--U_B`, which is `s:0--s:1`. The A internal differences remain `1..q+1`, the restored edge has difference `q+2`, and the B internal differences shift to `q+3..m`. Direct substitution gives precisely the labeling above, including `s:3=q+4` and `b:0:0=q+3`. Its returned ports are `L_B=s:2` and `U_A=b:0:0`; they are distinct actual vertices, not the connector endpoints. This component calculation establishes source overlap; the complete original-edge proof above is independently inspectable without relying on that composition. The retained source records upstream Git blob `faca17cfa4c484127413762adc0c36b771a18f71` at that commit.

## Comparison and scope

The existing [balanced supplier](B2_BALANCED_SUPPLIER.md) already covers `q=r=t`, `K=1` with `R={t+2}`, `D={1}`, and adjacent port `t+3`. It is a different labeling and boundary. The accepted [all-q,r unpadded supplier](B2_UNPADDED_ALL_QR.md) covers every `q,r>=1`, `K>=2`, using `D=1..K` and a different nonadjacent physical-port contract. Combining that result with the direct K=1 proof gives ordinary gracefulness for every positive integer `q,r,K` on the exact profile `[[q],[r]] + [[] for _ in range(K+1)]`, by cases; it does not create a single common boundary contract.

No conclusion is asserted for nonzero padding, additional branches or branched suffixes, arbitrary lobsters, or historical priority. The source overlap and separate AI review are not human peer review or formal verification.
