# D096 independent right-center quota via the physical zero host

[Evidence](../evidence/validation/LCL_R241_2AR_ZERO_HOST_001/README.md) · [D087 supplied state](R241_2B2_SYMBOLIC_PORT34.md) · [Retained zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)

For independently chosen exact integers \(a,r\ge2\), the exact ordered original `[[2,a],[r]]` supplies \(A(a+r+7,a+4;3,4)\) by direct construction.

## Original names, incidences and labels

Use the physical spine `s:0–s:1` and the three centers `b:0:0`, `b:0:1`, and `b:1:0`, attached to their designated sections. Each center has respectively 2, a, or r leaves, and each leaf's name specifies its section, branch and index. The spine and the three center attachments are present once each. The terminal edges join each indexed leaf only to its named center. With two spine vertices, three centers and 2+a+r terminals there are N=a+r+7 vertices and N−1=a+r+6 edges. Adding leaves and centers by a single edge each produces a connected acyclic graph.

| Names | Label |
| --- | --- |
| `s:0`, `s:1` | 3, a+8 |
| `b:0:0`, `b:0:1`, `b:1:0` | a+5, a+4, 0 |
| `l:0:0:j`, 0 ≤ j < 2 | 1+j |
| `l:0:1:j`, 0 ≤ j < a | 4+j |
| `l:1:0:k`, 0 ≤ k < r | a+7+k if k≥2, a+6+k if k<2 |

On the retained original at r=2 these are exactly the D087 labels, in its indexed order. The extension preserves all old named vertices, labels and incidences by keeping the first two right terminals in place. Only the names with 2≤k<r are fresh. The actual new edges are all `b:1:0–l:1:0:k`. No spine vertex, branch center, or earlier terminal changes roles.

## Extension hypotheses and complete inventories

D087 supplies an independently witnessed \(A(n,p;3,4)\), with n=a+9, p=a+4, 1≤p<n, and distinct actual ports with labels 3 and p+4. The offsets satisfy 0≤3<p and 0≤4<n−p. Its original spine witnesses all vertices within distance two. Its physical host `b:1:0` has label zero and is distance one from that spine by the existing attachment to `s:1`. The r−2 fresh names are pairwise distinct and attach only to this host. The retained zero-host theorem therefore applies with h=r−2. Its i-th added leaf, i=k−1, receives n+i−1=a+7+k.

The old labels exhaust [0,a+8] bijectively. For r>2 the new labels start at a+9 and end at a+r+6, with step one and r−2 elements. Their band is disjoint from the old label band, and together they give [0,N−1]. All old differences are unchanged and exhaust [1,a+8] by D087. Each added edge at the zero host has difference equal to the new leaf's label, so these differences also exhaust [a+9,a+r+6]. The two difference bands are disjoint and cover [1,N−1]. Both unused inventories are empty.

The low alphabet [0,a+3] and its vertices remain fixed. The old high alphabet [a+4,a+8] is extended by the fresh band to [a+4,N−1]. All old edges still cross p=a+4, and each new edge joins a high leaf to the low zero host. The actual ports remain `s:0=3` and `s:1=a+8=p+4`, so the returned offsets are (3,4) even when the exit ceases to be the maximum. Every center remains distance one from the physical spine. Every terminal is distance two through its own center. For r=2 the new index range is empty, both new bands are interpreted as empty, and the state is exactly D087's.

## Direct algorithm and scope

Check that a and r are exact integers at least two. Emit the two spine vertices, their edge, and the three centers with their attachments and labels. Emit each named terminal and its edge once by the bounded indexed loops in the table. There are a+r+2 terminal iterations and constant additional work, giving O(a+r) indexed operations. The only mathematical inputs are the quotas and the explicit D087 formula.

This specializes the existing zero-host theorem to an exact named family with independently varying a and r. It holds at offsets (3,4). [D083](R241_223_STRICT_RETURN.md) excludes offsets (1,0) on the same topology as the a=2,r=3 boundary, with pins `s:0=1`, `s:1=6`. The positive pins at that boundary are `s:0=3`, `s:1=10`, so both findings stand. The fixed first-center quota 2 remains a restriction. No join, historical novelty or unrestricted lobster result is claimed.
