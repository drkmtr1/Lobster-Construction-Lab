# D111 — Direct ordinary graceful seed on ordered [[5,3],[2]]

Use the [frozen D108 original](../evidence/validation/LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json). Its canonical digest is `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8` and its raw SHA-256 is `9dbdfd6226c94c821951bc0ca701c18e4a0e1b671324afa84b0431fec36aca0c`. The spine is `s:0--s:1`. The centers `b:0:0`, `b:0:1`, `b:1:0` attach respectively to `s:0`, `s:0`, `s:1`, and have 5, 3, and 2 indexed terminal neighbors. Every terminal has just its named center as neighbor. This is a connected tree with 15 named vertices and 14 actual edges. Its centers and terminals are at distances one and two from the original spine.

We construct a vertex bijection onto `[0,14]` with all 14 absolute differences on the actual edges exactly `[1,14]`, at `s:0=0`, `s:1=14`, `b:1:0=1`. The existence question has no alpha or internal sign constraint.

## Supply the core and leave six terminal positions

The three pins reserve weight 14 on the spine and weight 13 on the right attachment. Choose the two left-center labels 12 and 2 in ordered quota roles, supplying weights 12 and 2 against the entrance. Prescribe `l:0:1:2=13` and `l:0:1:0=3`. Their edges to center 2 provide 11 and 1. Prescribe `l:1:0:0=10` and `l:1:0:1=11`, giving 9 and 10 against the right center 1.

These nine distinct labels are `{0,1,2,3,10,11,12,13,14}`. The eight actual core-edge weights are `{1,2,9,10,11,12,13,14}`, each once. The core is still a tree: the omitted vertices are six named terminals, five at `b:0:0` and one at `b:0:1`. The residual label set is `R={4,5,6,7,8,9}`, and the residual difference set is `D={3,4,5,6,7,8}`.

## Allocate the two-host resources

Every x in R lies strictly between the center labels 2 and 12, so its possible weights are `d_A(x)=12−x` and `d_B(x)=x−2`. They sum to 10. Reflection `x↦14−x` interchanges the two weights. Its paired eligible rows, sole eligible option and midpoint are as follows.

| Residual labels | Weights at A=12 | Weights at B=2 | Allocation |
| --- | --- | --- | --- |
| 5, 9 | 7, 3 | 3, 7 | Both to A |
| 6, 8 | 6, 4 | 4, 6 | Both to A |
| 4 | 8 | 2, already used | To A |
| 7 | 5 | 5 | To B |

The first pair consumes `{3,7}`, the second consumes `{4,6}`, the forced choice consumes `{8}`, and the midpoint consumes `{5}`. These are disjoint and cover D. A receives five labels and B receives one. In increasing order at the five vacant A positions the labels are `(4,5,6,8,9)`. The only vacant B position is `l:0:1:1`, which receives 7. Thus the indexed groups are `(4,5,6,8,9)`, `(3,7,13)`, and `(10,11)`. The finite prescription uses only the original core and these four fixed allocation groups. Adding the six terminal assignments consumes each remaining vertex label and each remaining difference once. The core and these terminal incidences exhaust the named graph. Both remaining inventories are empty.

This realizes the geometry in the retained [R226.1 revision 2](../references/upstream/mdl/N226_R226_two_host_completion.md), adopted at the pinned MDL source. Its independently supplied core is a tree with eight edges, injective labels in `[0,14]` and distinct core differences. The labeled hosts are distinct actual vertices, ordered low B then high A, with residual quotas one and five. The complete residual difference multigraph has two parallel-pair components on `{3,7}` and `{4,6}`, a forced half-edge on `{8}` and a midpoint loop on `{5}`. Each component has as many labels as difference vertices. The forced lower-host count is zero, the two parallel components each permit zero or two there, and the midpoint permits one there. Thus quota one at B is realized by the midpoint, with both pairs and the forced singleton at A. The exhibited allocation already proves the finite supply. R226 concerns allocation with a supplied core and palettes, and this construction supplies those inputs only for this original.

## Signed-incidence diagnostic

In the original edge order (spine, then each center's attachment and indexed terminals) orient from the traversal class containing `s:0`. The signed ledger is

```text
14 | 12,8,7,6,4,3 | 2,−1,−5,−11 | 13,9,10
```

The three negative edges are exactly `l:0:1:0 → b:0:1`, `l:0:1:1 → b:0:1`, and `l:0:1:2 → b:0:1`. The even class contains the entrance, the right center and the eight left terminals. The odd class contains the exit, the two left centers and the two right terminals. The nonterminal degrees in order entrance, exit, first left center, second left center, right center are 3, 2, 6, 4, 3. With A and B the two left-center labels and P,Q the right-terminal labels, the weighted sums on the even and odd classes are `93−A−B−P−Q` and `28+6A+4B+P+Q`. They evaluate to 58 and 129. Their difference equals the signed edge sum `71 = 105−2(1+5+11)`. Equivalently,

```text
7A+5B+2(P+Q) = 7·12+5·2+2(10+11) = 170−2(1+5+11) = 136.
```

This diagnostic follows from the certificate. Ordinary acceptance requires the vertex and absolute-difference bijections and the three specified pins. The three negative edges place the witness outside each of the single-reversal domains in [D108](ORDINARY_53_2_SIGNED_SEED.md), [D109](ORDINARY_53_2_FREE_REVERSAL.md), and [D110](ORDINARY_53_2_MAGNITUDE_TWO.md). D107 retains its separate right-growth theorem. The D111 result is a finite seed and a candidate premise for a future sign-independent growth argument.
