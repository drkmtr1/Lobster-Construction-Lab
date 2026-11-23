# Dual-block structural obstruction at physical exit s:4=8

## Exact original and cut predicates

Let P be the [D066 named original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json), `[[2],[2],[2],[2],[]]`, with 17 vertices, 16 edges and digest `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`. Its consecutive spine edges, the four attachments s:i–b:i:0 for i=0,1,2,3, and both terminal edges b:i:0–l:i:0:j for j=0,1 are all the original edges. The witness W=b:0:0–s:0–s:1–s:2–s:3–s:4 lies on these edges. The first host is on W, the second and zero hosts are each one edge from it, and every vertex is within distance two. All terminal names and indices are retained.

Consider any normalized alpha-graceful labeling with physical s:4=8 and Z=b:2:0=0. Let A=b:0:0, a=f(A) and B=f(b:1:0). The alpha classes alternate from high s:4 along the actual incidences. The eight lows biject onto [0,7] and the nine highs onto [8,16]. Their complete named degree groups are:

| Class | Degree three | Degree two | Degree one |
|---|---|---|---|
| Low | A, Z, s:1, s:3 | ∅ | l:1:0:0, l:1:0:1, l:3:0:0, l:3:0:1 |
| High | s:2, b:1:0, b:3:0 | s:0 | s:4, l:0:0:0, l:0:0:1, l:2:0:0, l:2:0:1 |

Since zero is occupied at Z, a ranges from 1 through 7. The second host is high and distinct from the exit, so B ranges from 9 through 16. The [upper-block condition](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis) selects all edges E_U incident to highs with labels ≥u for 9≤u≤16. It requires the complete weight interval [u−a,16]. The [lower-block condition](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md#supplied-state-and-hypotheses) selects all edges E_L incident to lows with labels <d for a<d≤8. It requires [B−d+1,16]. For E_U every selected high has only low neighbors below u. For E_L every selected low has only high neighbors at least d. In either set each original edge has exactly one selected endpoint.

## Counts and the exceptional upper cut

The d lower-selected lows include A and Z. If k_d of s:1,s:3 are also selected, their incident-edge count is d+4+2k_d, since these are the only four degree-three lows. The lower interval has length 16−B+d, so B=12−2k_d. The values 8,10,12 exhaust that equation, and the distinct high exit occupies 8. Only 10 and 12 survive.

The 17−u selected highs must supply 17−u+a edges. Their degree excess above one per vertex must be a. At u=9 all highs except s:4=8 are selected. Their excess is 1+2+2+2=7, forcing a=7. Then d=8 and both spine lows are selected, giving k_d=2 and B=8, a collision with the exit. As a separate check, difference one can only come from labels 8 and 7 across this alpha cut. The exit has sole neighbor s:3, so f(s:3)=7 and a=7 itself would repeat that label. Therefore u≥10 for any joint supplier.

## Forced s:2 and containment of original edges

For every permitted upper selection with positive excess a, s:2 must be selected. Suppose otherwise. Weight 16 can only come from labels 0 and 16. The actual neighbors of Z are s:2 and the two third terminals. Therefore the high labeled 16 is a third terminal, and its sole edge has weight 16. Now descend through the weights w from 15 to u. Any edge of weight w must have high label at least w. A larger high label cannot supply it, since each larger label has already been forced to a third terminal with just its own larger weight. Thus the high label is w, its low endpoint is Z, and the high is a third terminal since s:2 was assumed excluded. This argument also covers u=16 by its base alone. It forces all upper-selected highs to be degree-one third terminals, contradicting excess a>0.

The weight map on the actual original edges is injective and exhausts [1,16]. If the complete intervals hold, each selected edge set must be the inverse image of its interval. Thus E_U⊆E_L when u−a≥B−d+1, and E_L⊆E_U in the reverse inequality. Equality of starts gives equality of edge sets.

## Named contradictions for B=10 and B=12

**B=10.** The lower equation gives k_d=1. Since u≥10 and d≥a+1,
```
u−a ≥ 10−a ≥ 11−d = B−d+1 .
```
Hence E_U⊆E_L, including equality. The selected s:2 is incident to both s:1 and s:3 on the original spine. Both must be lower-selected, which would give k_d=2.

**B=12.** Here k_d=0 and at most the six nonspine lows can be selected, so d≤6. If E_U⊆E_L, the two actual spine edges at selected s:2 again force both spine lows, a contradiction. This branch includes equal tails. Otherwise E_L⊆E_U with strict inclusion. The lower-selected A and Z have six distinct high neighbors, namely s:0, s:2 and the two first and two third terminals. All six must be upper-selected, giving 17−u≥6 and u≤11. The second host with label 12 is then also upper-selected and is distinct from those six. Seven selected highs together with u≥10 force u=10.

These seven highs exhaust the upper selection. Their excess is five, from s:0, s:2 and b:1:0, so a=5. Since a<d≤6, d=6 and the lower selection is exactly the six nonspine lows. The two unselected highs at u=10 are the exit and b:3:0, occupying labels 8 and 9 respectively. Both fourth terminals are lower-selected, but their actual edges to b:3:0 are upper-unselected. This contradicts E_L⊆E_U.

## Disposition

**ACCEPT the structural obstruction and REJECT joint supply in this exact domain.** The normalized alpha orientation, pins s:4=8 and b:2:0=0, free first-host label and the two complete same-ledger predicates are part of the conclusion. The proof gives no ordinary nongracefulness result. A future supplier for an adjacent-exit interface would still require an independently justified original-path consumer and both exact inventories. D066–D070 and D073 keep their scopes. The [bounded audit](../evidence/validation/B4_D073_U8_DUAL_BLOCK_STRUCTURAL_001/README.md) checks the named premises and boundary arithmetic without a numerical tuple sweep or label enumeration. The D066 and D070 certificates are retained controls at their archived exit values.
