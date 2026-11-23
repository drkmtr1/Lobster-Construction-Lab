# B4-2222-NONADJACENT-ALL-K-001

**Claim.** The exact named original
`T_K=[[2],[2],[2],[2]]+[[]]*(K+1)` is ordinarily graceful for
every exact integer K≥2. The first three branch sizes are fixed
at q=r=t=2 and the fourth at 2.

## Supplied original and the high shift

Use the archived [D066 original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json)
`P=[[2],[2],[2],[2],[]]` and [its certificate](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/certificates.json).
The [direct analytic supplier](B4_K2_ALPHA_PREFIX_S4_9.md)
constructs f independently of any T_K completion.
The original has four consecutive spine edges and, at each
of sections 0 through 3, one original attachment and two
original terminal edges. The exact ledger is

| Original names in order | Labels | Edge differences |
|---|---|---|
| s:0, s:1, s:2, s:3, s:4 | 10, 2, 16, 7, 9 | 8, 14, 9, 2 |
| b:0:0, l:0:0:0, l:0:0:1 | 6, 12, 13 | 4, 6, 7 |
| b:1:0, l:1:0:0, l:1:0:1 | 14, 1, 4 | 12, 13, 10 |
| b:2:0, l:2:0:0, l:2:0:1 | 0, 15, 11 | 16, 15, 11 |
| b:3:0, l:3:0:0, l:3:0:1 | 8, 3, 5 | 1, 5, 3 |

Each branch row gives the attachment weight before its
two named terminal weights. Alternating from physical s:4
gives the eight low names s:1, s:3, b:0:0, b:2:0 and the
four terminals of branches 1 and 3. They use 0..7 once
each. The other nine names use 8..16 once each. The
consecutive spine edges alternate, each center is opposite
its original spine attachment and each terminal is opposite
its center. Each of the 16 original edges crosses the
alpha cut, and the table uses 1..16 exactly once.
The original graph digest and label-ledger ID are separate
archive identities, both rechecked by arithmetic.

The full original T_K has K+5 spine vertices, four centers
and eight leaves. It has 17+K vertices and 16+K edges. The
named induced prefix through s:4 is exactly P. The names
s:5 through s:(K+4) have no branch incidences. With only P
assigned, the pending edges are exactly the consecutive
K-edge original path beginning at s:4, with sole crossing
edge s:4--s:5. The original spine remains a witness to all
vertices at distance at most two.

Keep f on the low class and raise every high label by K.
This gives the partial labeling F_K on the same names.
Its label set is [0,7] ∪ [K+8,K+16], all distinct.
Each assigned original edge still has its high endpoint
larger by exactly K more than before, so the used edge
differences are [K+1,K+16] once each. The complements
in the actual T_K alphabets are

```text
R = [8,K+7]
D = [1,K]
F_K(s:4) = K+9 = max(R)+2.
```

Both complements have K elements. The actual port
already carries that label because f(s:4)=9 was high.

## Recurrence and the physical path

The [retained B2 theorem](B2_NONADJACENT_CONSUMER.md#construction-and-proof)
is numerical on a path subject to its full physical and
resource contract. It can be applied to any actual names
`w_i` with those incidences. Use `w_0=s:4` and
`w_i=s:(4+i)` for i=1,...,K. The public Python graph
wrapper `lcl.consumers.complete_nonadjacent_path` checks
the specialized B2 names at physical s:2 and its narrower
verified graph domain. The B4 task uses the theorem on
its own path and leaves the production implementation
unchanged. The bounded harness implements the recurrence
locally and checks the B4 names and supplies.

To prove the numerical claim independently, put

```text
C_2 = (3,1,0)
C_3 = (4,1,0,2)
C_4 = (5,1,2,0,3)
C_K = (K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3))   for K>=5,
       where C_(K-3) = (K-2,x_1,...,x_(K-3)).
```

In the three bases the suffix labels are respectively
(1,0), (1,0,2), (1,2,0,3), with differences (2,1),
(3,1,2), (4,1,2,3), including the edge from the port.
Each starts at K+1 and has suffix exactly [0,K-1].

For K≥5 use strong induction at K−3≥2. The values
x_i run through [0,K−4] exactly once. They become
[2,K−2] under reflection in the rule, and the three
other suffix values 1,K−1,0 fill the rest of [0,K−1].
Before this reflected tail, the three new edges have
weights K,K−2,K−1. The bridge from the new zero to the
first reflected entry has weight K−2−x_1. It is the
reflection of the **first** old edge from K−2 to x_1.
The other reflected edges preserve all later old
differences. Thus the bridge and later edges together
give exactly [1,K−3]. Combining the disjoint bands
gives [1,K] once each, and the port is K+1. The
recursion reduces the argument by three until it
reaches one of 2,3,4.

Translate the sequence by 8 and assign only its tail
on the actual named path. Its first entry equals
F_K(s:4), so the prefix is left unchanged. Its
remaining K entries consume exactly R and all K actual
pending edges consume exactly D. The complete label
and difference sets are therefore [0,K+16] and
[1,K+16] once each on the original T_K. This supplies
ordinary gracefulness. The alpha cut was a premise
on P. The resulting complete labeling carries no
alpha-gracefulness claim.

For K=1 the same high shift would yield
R={8}, D={1}, s:4=10. The only completion edge would
have weight 2, so this particular interface fails.
The retained [D062 K=1 theorem](B4_JOINT_NESTED_CUT_TWO_HOST.md#exact-k1-zero-host-lift)
uses its own supplier and singleton. It is unaffected.

## Scope of finite validation

The [bounded evidence](../evidence/validation/B4_2222_NONADJACENT_ALL_K_001/README.md) rechecks retained K=2
and generates only K=3,4,5,8 to exercise the other
bases and recursion. The quantified conclusion follows
from the high-shift proof and induction. Arbitrary
interior q,r,t, other fourth branches and universal
lobster gracefulness remain separate obligations.
