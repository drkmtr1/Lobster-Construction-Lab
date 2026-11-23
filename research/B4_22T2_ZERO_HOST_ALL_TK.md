# Third-center zero-host extension and original-path completion

## Independent normalized supply

[The D066 construction](B4_K2_ALPHA_PREFIX_S4_9.md) gives the following ledger before the suffix is added. Take the exact named prefix P₂ = `[[2],[2],[2],[2],[]]`. Its spine is s:0 through s:4. At each section i=0,1,2,3, the center b:i:0 attaches to s:i and both terminals l:i:0:0 and l:i:0:1 attach to b:i:0. The rows list labels in that physical order and differences in edge order (spine order or attachment followed by terminal indices).

| Original vertices | Labels | Original edge differences |
|---|---|---|
| s:0 through s:4 | 10, 2, 16, 7, 9 | 8, 14, 9, 2 |
| First center and terminals | 6, 12, 13 | 4, 6, 7 |
| Second center and terminals | 14, 1, 4 | 12, 13, 10 |
| Third center and terminals | 0, 15, 11 | 16, 15, 11 |
| Fourth center and terminals | 8, 3, 5 | 1, 5, 3 |

The columns give `0..16` and `1..16` once each. The low vertices are s:1, s:3, b:0:0, b:2:0, l:1:0:0, l:1:0:1, l:3:0:0 and l:3:0:1, labeled `0..7`. The spine alternates high, low, high, low, high. The first and third attachments go from high spine to low center and then high leaves. The second and fourth go from low spine to high center and then low leaves. Every edge crosses at 8.

Use the actual witness path W = b:0:0–s:0–s:1–s:2–s:3–s:4. Its ends are the distinct physical ports L=b:0:0 with label 6 and U=s:4 with label 9, giving A(17,8;6,1). The original third center z=b:2:0 has label zero and is one edge from W through s:2. The other off-path centers are adjacent to their spine vertices. All terminals are within two edges of W.

## Indexed growth and closure

For exact integer t≥2, Pₜ = `[[2],[2],[t],[2],[]]` is obtained by adding the fresh terminals l:2:0:j for 2≤j<t, each only at the original z. Adding these leaves preserves connectivity, acyclicity and every old named incidence. In the [conditional alpha zero-host rule](ALPHA_ZERO_HOST_LEAF_EXTENSION.md), n=17, h=t−2 and the one-based addition index is i=j−1. Keep every old label and assign n+i−1=15+j to each fresh leaf. Its edge to z uses the same difference. Old labels and differences are `[0,16]` and `[1,16]`. Fresh labels and differences are `[17,t+14]`, empty at t=2. Both full alphabets are thus exhausted once each. Every fresh leaf is high, crosses to z and is at distance two from W. L, U and z retain their identities and labels. The returned state is A(t+15,8;6,1), with low and high alphabets `[0,7]` and `[8,t+14]`.

After a fresh terminals have been added in name order, the order is 17+a and the host and witness satisfy the same premises. In a further batch, leaf i has global index j=2+a+i−1 and receives 17+a+i−1=15+j. Earlier labels and incidences remain fixed. Induction on finite batches gives pointwise agreement for every partition in prescribed name order, including empty batches. Each finite t calls for exactly t−2 insertions.

## High shift and original suffix

For exact integer K≥2, the full original T(t,K) = `[[2],[2],[t],[2]]+[[]]*(K+1)` has t+K+15 vertices and m=t+K+14 edges. The added sections from s:5 to s:(K+4) are empty. Their only incident edges are the consecutive K edges of the actual spine from s:4, and the sole assigned-to-unassigned edge is s:4–s:5. Extending W through that spine suffix is a full witness.

Leave all low labels fixed and shift every high by K. The shifted labels exhaust `[0,7] ∪ [K+8,m]`. Each assigned edge crosses the alpha cut in Pₜ and its high-minus-low difference increases by K. The assigned differences exhaust `[K+1,m]`. The exact complements are R=`[8,K+7]` and D=`[1,K]`, and physical s:4 is K+9, two above max(R).

Apply the numerical recurrence of the [B2 consumer](B2_NONADJACENT_CONSUMER.md) and its [D067 transfer to the B4 spine](B4_2222_NONADJACENT_ALL_K.md). Its three bases C₂=(3,1,0), C₃=(4,1,0,2), C₄=(5,1,2,0,3) have differences (2,1), (3,1,2), (4,1,2,3), and entries after the port equal `0..K−1` once each. For K≥5 write the shorter sequence as (K−2,x₁,…,xₖ₋₃) and prepend K+1,1,K−1 to its reflection under x↦K−2−x. The reflection starts at 0 and the remaining reflected labels are precisely `2..K−2`, disjoint from 1,K−1,0. The three edges up to 0 give K,K−2,K−1. The edge from 0 to K−2−x₁ is the reflection of the first old edge. It and the rest of the reflected path give `1..K−3` once each. This proves the exact inventories by strong induction. K decreases by three to a base, so the construction terminates.

Assign the ith suffix vertex s:(4+i) the entry 8+C_K[i] for 1≤i≤K. The initial entry 8+C_K[0]=K+9 agrees with the already assigned s:4. The new labels and differences consume R and D once each on the actual original incidences and preserve all prefix labels. This proves ordinary gracefulness on the specified exact-integer t,K≥2 domain. The mathematical sequence uses the verified original path contract. The public B2 implementation retains its narrower s:2 and checked-graph domain.

At K=1 this interface leaves R={8}, D={1}, and s:4=10, so the only pending edge would have weight 2. The failure is specific to this shifted prefix interface.

## Disjoint selector for positive t and K

For fixed first and second sizes 2 and fourth size 2, [D037](B4_UNPADDED_QR12.md#original-completion-for-all-qrk1) supplies t=1 for every positive K by its QR12 construction. For t≥2 and K=1, [D062](B4_JOINT_NESTED_CUT_TWO_HOST.md#exact-k1-zero-host-lift) supplies the maximum-rooted ordinary core and zero-host lift with q=r=2. For t,K≥2 use the construction above. The three disjoint cases prove ordinary gracefulness for this exact family for all positive integers t,K. The alpha-prefix supply established here has t≥2. Its original-path consumer has K≥2.

The bounded records and separate AI reviews are in [the evidence bundle](../evidence/validation/B4_22T2_ZERO_HOST_ALL_TK_001/README.md).
