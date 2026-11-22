# Bounded fourth-branch diagnostics

These four first-witness exact DFS queries investigate two normalized
original named prefixes. Their records are separate from the 12 Q112
completed targets and the direct 14-vertex seed. [Declared configuration](diagnostic_config.json)

## Exact graph identity and alpha domains

The five spine vertices are s:0 through s:4 with four consecutive
edges. Each center b:i:0 attaches to s:i, with original leaf names
l:i:0:j on that center for exactly the named profile. Both targets have
15 vertices and 14 edges. Fixing s:4 as high determines the unique
orientation of the tree bipartition. Even spine vertices and odd
centers are high, odd spine vertices and even centers are low, and
each terminal is opposite its center.

| Target | Low vertices | High vertices | p | Original graph SHA-256 |
|---|---|---|---:|---|
| `[[1],[2],[1],[2],[]]` | s:1, s:3, b:0:0, b:2:0, l:1:0:0, l:1:0:1, l:3:0:0, l:3:0:1 | s:0, s:2, s:4, b:1:0, b:3:0, l:0:0:0, l:2:0:0 | 8 | `fc491cb86c5a5d4e13ace9f9d53e125f6bcf7f2c1cc46ffe90d622d9d59335bb` |
| `[[1],[1],[2],[2],[]]` | s:1, s:3, b:0:0, b:2:0, l:1:0:0, l:3:0:0, l:3:0:1 | s:0, s:2, s:4, b:1:0, b:3:0, l:0:0:0, l:2:0:0, l:2:0:1 | 7 | `a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc` |

Every low vertex has domain [0,p-1] and every high vertex has domain
[p,14]. Each query pins only physical s:4. There is no implicit
complement, automorphism quotient or root pin. The unchanged DFS
runs serially with one worker, at most 16 vertices, 100,000 nodes
and five cooperative seconds per query. Each starts with first-witness
mode and the byte cap of 2,000,000.

## Query outcomes

| Query | s:4 pin | Interface | Status | Nodes |
|---|---:|---|---|---:|
| [1212 adjacent](diagnostic_results/1212-adjacent.json) | 8 | Above adjacent | SAT, verified | 9,982 |
| [1212 nonadjacent](diagnostic_results/1212-nonadjacent.json) | 9 | Above nonadjacent | SAT, verified | 4,424 |
| [1122 adjacent](diagnostic_results/1122-adjacent.json) | 7 | Above adjacent | SAT, verified | 7,234 |
| [1122 nonadjacent](diagnostic_results/1122-nonadjacent.json) | 8 | Above nonadjacent | SAT, verified | 3,373 |

Each query stopped at a first witness. The unchanged checker verified
the exact original graph and the diagnostic runner confirmed every
domain and pin against the witness. There were no exhausted negatives
and no incomplete queries. The records establish finite candidate
suppliers and give no exact solution counts or parameterized supplier.

The high shift leaves R=[p,p+K-1] and D=[1,K]. Pin p gives
s:4=p+K, the [adjacent interface](../../../research/PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
for K>=1, with alpha completion on an actual path.
Pin p+1 gives s:4=p+K+1, the [nonadjacent interface](../../../research/B2_NONADJACENT_CONSUMER.md)
for K>=2, with graceful completion. At K=1 that exact nonadjacent
interface has sole distance two and cannot use difference one. These
are the distinct conditional consumer contracts. The four finite
records do not establish symbolic second- or third-branch growth
for arbitrary (q,r,t,2).
