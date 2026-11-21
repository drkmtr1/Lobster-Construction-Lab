# B2-NONADJACENT-SEED-P5-001: explicit unequal-family supplier

**Disposition:** ACCEPT a fixed, independently checked port-5 alpha seed and its explicit solver-free supplier-to-consumer composition for `q=1,r=2,z0=z1=0` and every integer `K>=2`. An earlier, separately verified finite witness covers `K=1` using a different adjacent-port interface. The reduction below is independently reviewed for `K>=6`. This is a restricted family result, not a universal lobster theorem, human peer review, formal certificate, or historical novelty claim. Starting checkpoint: `360d56444e553c44aa593c6b76222244fe339f41`.

## Named graph and exact finite task

The original eight-vertex seed graph is the actual profile `[[1],[2],[]]`, digest `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`. Its seven edges are

```text
s:0--s:1       s:0--b:0:0       b:0:0--l:0:0:0
s:1--b:1:0     b:1:0--l:1:0:0   b:1:0--l:1:0:1   s:1--s:2
```

The low class A is `s:1,b:0:0,l:1:0:0,l:1:0:1`, bijectively labeled `0..3`; the high class B is `s:0,b:1:0,l:0:0:0,s:2`, bijectively labeled `4..7`. The physical port alone is pinned `h(s:2)=5`. No root pin, extra branch-order restriction, branch-symmetry quotient, automorphism quotient, or complement quotient is imposed; all named branch identities are retained. The candidate space contains exactly `4! * 3! = 144` named admissible assignments; this is the domain size, not a claim that the DFS examined all of them.

One first-witness DFS case, one worker, with limits 10,000 assignment nodes, 2 seconds cooperative, eight vertices and 2,000,000 bytes per JSON output, returned **SAT** after 9 nodes. It stopped on its first witness: `exhausted=false`, exact count `null`, verified lower bound 1. No exact solution count is claimed and the negative-only oracle was not run. The new immutable pin input is `examples/nonadjacent_seed_p5_001_pins.json`. Exact inputs, output, source snapshot and independently checked certificates are in `evidence/runs/b2-nonadjacent-seed-p5-001-20261121-dfs/`.

The witness on the caller-retained graph is

| Actual vertex | Label |
|---|---:|
| `s:0` | 6 |
| `s:1` | 1 |
| `s:2` | 5 |
| `b:0:0` | 0 |
| `l:0:0:0` | 7 |
| `b:1:0` | 4 |
| `l:1:0:0` | 2 |
| `l:1:0:1` | 3 |

In the order displayed above, the actual seven edge differences are `5,6,7,3,2,1,4`, exactly `1..7`. The vertex labels are exactly `0..7`, A/B domains and the port pin hold. The independent original-target certificate and direct explicit-edge check passed. Two fresh separate mathematical reviewer sessions also checked the original target, witness, formulas, and restrictions; these are AI reviews, not human peer review or proof-assistant verification.

## Necessary reduction when K>=6

For integer `K>=6`, let the exact B2 target have profile `[[1],[2]]+[[]]*(K+1)` and final edge count `m=K+7`. Suppose a valid labeling of precisely its eight-vertex prefix uses differences `K+1..K+7`, leaves unused labels `[ell,ell+K-1]`, and has physical port `f(s:2)=ell+K+1`. No alpha condition or root pin is assumed in this implication.

The difference `K+7` forces both labels `0` and `K+7` to be assigned to original prefix vertices; hence `1<=ell<=7`. The port must lie inside `0..K+7`, sharpening this to `ell<=6`. The assigned labels are exactly the two nonempty blocks

```text
L = [0,ell-1],     H = [ell+K,K+7].
```

Each block has span at most six, while every original prefix edge has difference at least `K+1>=7`; every edge therefore crosses the blocks. The connected original seed graph has the named A/B bipartition above, both classes of size four. Its only proper two-colorings assign the entire low block to one class and the high block to the other, forcing `ell=4`. Because the physical port belongs to B and its prescribed label is `ell+K+1`, it lies in H, so B is high and A low.

Leave low labels unchanged and subtract K from every high label. The same named vertices and seven original edges now have A labels `0..3`, B labels `4..7`, and edge differences `1..7` exactly once. The physical port becomes `(4+K+1)-K=5`. Thus every stated nonadjacent prefix for K>=6 compresses to a graceful alpha seed satisfying the declared A/B domains and port-5 pin; the compressed labeling need not equal the particular displayed witness. No complement or counting quotient is used. This necessity has not been claimed for K=2..5, and six is only a sufficient threshold for the reduction.

## Explicit supply and path completion for K>=2

For **any** graceful alpha seed `h` satisfying the declared A/B domains and `h(s:2)=5`, leave A labels unchanged and add K to every B label. Every original prefix edge crosses the cut, so its difference increases by exactly K: the seed's `1..7` become `K+1..K+7`. The unused labels are `[4,K+3]`, the unused differences are `1..K`, and the port is `K+5=4+K+1`. This holds for every integer `K>=2`; the accepted nonadjacent consumer completes the original path. No particular choice among the port-5 seeds is required for this implication.

Fix the verified witness above as finite constants; no solver or successful full target labeling is an input to the construction. The high-side shift assigns the actual prefix vertices directly by

```text
s:0=K+6       s:1=1       s:2=K+5
b:0:0=0       l:0:0:0=K+7
b:1:0=K+4     l:1:0:0=2   l:1:0:1=3
```

These labels are exactly `0..3` and `K+4..K+7`, distinct within `0..K+7`. On the seven original edges in the order above, differences are `K+5,K+6,K+7,K+3,K+2,K+1,K+4`: exactly `K+1..K+7`. Therefore unused labels are exactly `[4,K+3]`, unused differences are `1..K`, and actual port `s:2=K+5=4+K+1` is two above the interval. The only unfinished incidences are the original path `s:2--s:3--...--s:(K+2)`.

The independently accepted recurrence in `research/B2_NONADJACENT_CONSUMER.md` takes that actual path, with `ell=4`, uses exactly these remaining labels/differences, and preserves the prefix. Its proof covers every K>=2, so this fixed finite seed plus symbolic transport is an **independent supplier and graceful construction on the stated infinite family**, not a solver-derived prefix chosen anew for each K. For K>=6, the reduction above also makes existence of this precise interface equivalent to existence of a port-5 alpha seed satisfying the declared domains; the displayed fixed witness supplies the converse.

Deterministic, non-search checks at K=2,3,6,10 verified the supplied original graphs, resource inventories and completed certificates; these checks use the project graph builder, consumer and verifier, so they are not implementation-independent verification of those components and do not replace the quantified proof. The seed's explicit-edge arithmetic was also checked separately by reviewer sessions. The accepted `interval_boundary` still describes the different adjacent-port interface and was not changed.

## K=1 and remaining scope

The exact nonadjacent interface cannot work at K=1: its sole suffix edge would have difference 2. Separately, the existing release pilot has `q=1,r=2,K=1,ell=1`, above-side adjacent port, and the original-graph labeling `s:0=4,s:1=8,s:2=2,s:3=1,b:0:0=6,l:0:0:0=3,b:1:0=0,l:1:0:0=5,l:1:0:1=7`. Its actual edge differences are exactly `1..8`. This previously known finite witness was separately rechecked with project components and by the mathematical reviewers; no new K=1 constructor is claimed. Together, that existing witness and the K>=2 construction establish ordinary graceful labelings for this specific profile family for every positive K, with different interfaces.

No pin 6 or 7 was investigated, and the superseded three-pin sweep was not executed. The new p=5 witness does not erase the accepted p=4 restricted negative or the different K>=6 adjacent-port obstruction. General unequal branch sizes, further branched suffixes, repeatable transitions, and universal lobster coverage remain open.

The retained `independent_verify.py` creates only the fixed new filename `independent_verification.json` and refuses to overwrite it; it does not offer an output-path argument. To replay without altering historical evidence, use a separate isolated project copy with this run directory and inputs, including the original `evidence/validation/release_final/pilot/cases/31da62597181ea39545cd89689e591113261ea7c9c7af56e60383894da947a57.attempt-0001.json`; omit the existing verification result only from that new copy, and run the saved script there. The saved verification receipt records its own and input hashes but not the verification-time hashes of imported `lcl` modules; a separate reviewer confirmed that the current source and the 22-file DFS snapshot match. Do not interpret that later comparison as a cryptographic attestation of the verification process itself.
