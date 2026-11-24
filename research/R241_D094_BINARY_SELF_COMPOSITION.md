# One binary self-composition of D094

[Evidence and reproduction](../evidence/validation/LCL_R241_D094_BINARY_SELF_COMPOSITION_001/README.md) · [Accepted D094 supplier](R241_D090_D093_JOINT.md) · [Adopted R241.1](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** For eight independently chosen exact integers a,b,c,d,e,f,g,h≥2, the exact named original
```text
[[2,a],[2],[3,b],[3],[3],[3,d],[2],[2,c],[2,e],[2],[3,f],[3],[3],[3,h],[2],[2,g]]
```
supplies A(a+b+c+d+e+f+g+h+80,a+b+e+f+40;3,3), with its original sixteen-section spine as witness.

## Original graph and independent input states

Construct all sixteen vertices s:i, 0≤i<16, and exactly the fifteen edges s:i–s:(i+1), 0≤i<15. For row i of the displayed original, take the listed ordered center quotas. If the quota at position j is q, add b:i:j and its edge to s:i, then all distinct l:i:j:k and their edges to b:i:j, for 0≤k<q. The resulting graph has sixteen spine vertices, twenty-four centers and a+b+c+d+e+f+g+h+40 leaves. The edge groups have fifteen, twenty-four and a+b+c+d+e+f+g+h+40 members. These groups contain no repeated incidence because the original center and leaf names are distinct and each has one parent. Attaching each center and leaf by one edge to the spine or its center leaves a connected acyclic graph.

The induced subgraph in sections 0–7 is the exact D094 original for a,b,c,d. Use it as old B with its local label map f_B and physical endpoints L_B=s:0 and U_B=s:7. For the second D094 original with parameters e,f,g,h, use new A with local map f_A. Add eight to each local section index in its spine, center and terminal names. This preserves every branch index j, terminal index k and actual incidence in A, whose embedded endpoints are L_A=s:8 and U_A=s:15. The name map from B is the identity. Thus the component vertex sets are disjoint, their induced edge sets use all the original edges except the single actual cross-component edge U_B–L_A=s:7–s:8, and their witnesses are the corresponding sections of the original spine.

The accepted D094 formulas independently supply the two local alpha states:
```text
n_B = a+b+c+d+40      p_B = a+b+20      (x_B,y_B) = (3,3)
n_A = e+f+g+h+40      p_A = e+f+20      (x_A,y_A) = (3,3)
```
Each low and high class has size at least 24, so all offsets lie within the required local classes. In particular f_B(U_B)=p_B+3 and f_A(L_A)=3. The required physical equality y_B=x_A=3 holds on the named endpoints.

## Four global label bands

Apply the adopted R241.1 binary placement to these original names. Keep each B low label, add n_A to each B high label, and add p_B to every embedded A label. The domain partition assigns a value exactly once to each original vertex. The four local label bijections are translated to the following bands, where N=n_B+n_A, P=p_B+p_A and m=N−1.

| Actual group | Global labels | Length |
| --- | --- | --- |
| B lows | [0,p_B−1] | p_B |
| A lows | [p_B,P−1] | p_A |
| A highs | [P,p_B+n_A−1] | n_A−p_A |
| B highs | [p_B+n_A,N−1] | n_B−p_B |

Each start after the first is one above the preceding end. Thus all labels in [0,m] are used exactly once, with the first two groups forming the lows [0,P−1] and the last two forming the highs [P,m]. This gives P=a+b+e+f+40. Every internal edge retains a low and a high endpoint under the placement, and the actual connector joins B high to A low.

## Actual connector and complete difference inventory

Both endpoints of an A internal edge gain p_B, leaving difference d_A unchanged. On a B internal edge only the high label gains n_A, so its positive difference grows from d_B to d_B+n_A. The connector endpoints become
```text
F(s:7) = p_B+3+n_A
F(s:8) = p_B+3
```
and the edge therefore has weight n_A=e+f+g+h+40. The component edge bijections and the single cross-component incidence give exactly these original-weight groups:

| Named original edges | Global differences |
| --- | --- |
| A internal, sections 8–15 | [1,n_A−1] |
| Actual s:7–s:8 | {n_A} |
| B internal, sections 0–7 | [n_A+1,N−1] |

Each local spectrum has multiplicity one. The translated groups are disjoint and consecutive, and the singleton fills the unique gap. Their union exhausts [1,m] once each. Both unused inventories are empty.

## Returned ports, physical witness and termination

The two originally supplied paths and the one connector give the simple original path s:0–s:1–…–s:15. Each center is adjacent to its own original spine vertex, and each terminal is two edges from the spine through its only center neighbor. The physical entrance label is F(s:0)=3. The physical exit has label F(s:15)=p_B+p_A+3=P+3, hence the returned offsets are (3,3).

A direct algorithm checks the eight exact integers, emits the ordered original, instantiates the accepted D094 label formulas separately at a,b,c,d and e,f,g,h, embeds the second name set and translates the three input classes once. The quota loops visit the prescribed finite names once and terminate after O(a+b+c+d+e+f+g+h) indexed operations and output records. The connector is emitted in the original spine edge list, and the procedure requires only the parameters and accepted formulas.

The all-two boundary has N=96, m=95 and P=48. Its connector endpoints have labels 75 and 27, and the physical entrance and exit labels are 3 and 51. The difference bands are [1,47], {48}, [49,95]. This finite check tests the exact specialization. The general finite-list closure rule already belongs to R241.1. The contribution here is the original named two-block specialization with eight independent quotas and its boundary verification.
