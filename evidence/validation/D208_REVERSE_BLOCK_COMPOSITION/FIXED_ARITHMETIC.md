# D208 prescribed fixed arithmetic

The four originals and their actual parent incidences are specified below before the label tables. The calculations are direct substitutions and endpoint subtractions by hand. The independent mathematical reviewer checked the exact saved records separately. No solver, search, executable verification, protected checker or historical campaign was used.

## 1. Named originals

In the local control let the reversed spine s:0,s:1,s:2 be the new pendant entry e, old w, old u, respectively. Its only branches are the three unit centers at s:1 and the four unit centers at s:2. For an actual section i and center index j the center name is b:i:j and its indexed terminal name is l:i:j:t, with t from 0 through its original quota minus one. Spine edges are just the consecutive spine edges. The attachment of a center is to s:i and each terminal is attached to its indexed center. For the block, reading the sections in reverse maps the original w group to s:1 and the original u group to s:2. Their internal order and actual parent identities are unchanged.

For the assembled controls use the original forward indices. Begin with s:0=v₀ with no off-spine children. In block i the original four-center section is s:(2i−1)=u_i and the original three-center section is s:2i=w_i. The remaining two sections are s:(2r+1)=x, the attaching endpoint of the supplied receiver, and s:(2r+2)=y. This gives the following exact original profiles.

| Control | Profile from original s:0 | Edges |
|---|---|---:|
| Local | ((),(1,1,1),(1,1,1,1)) | 16 |
| D105 one block | ((),(1,1,1,1),(1,1,1),(4,3),(2)) | 30 |
| D105 two blocks | ((),(1,1,1,1),(1,1,1),(1,1,1,1),(1,1,1),(4,3),(2)) | 46 |
| D117 boundary | ((),(1,1,1,1),(1,1,1),(5,3),(2)) | 31 |

The D105 receiver is exactly the separately supplied 13-edge original in D105, with only the section indices shifted in the chain. The D117 boundary uses independently supplied (q,a,b)=(5,3,2) and one block, so its receiver has 14 edges. In each chain the initial empty section and its actual spine edge are present. These are the four controls of the symbolic task.

## 2. Local reverse block

Use the D206 local labeling with entry 8, first receiver u=9 and last receiver w=0. The reverse assignment is e=8,w=9,u=0. At w the original indexed centers have labels (5,6,7), with the corresponding unit terminals (10,12,15). At u the centers have labels (11,13,14,16), with corresponding unit terminals (4,3,2,1).

| Incidence in reversed spine or local indexed order | Actual new differences |
|---|---|
| e–w, w–u | 1,9 |
| w to centers | 4,3,2 |
| w centers to their own terminals | 5,6,8 |
| u to centers | 11,13,14,16 |
| u centers to their own terminals | 7,10,12,15 |

The exact lower side [0,8] comprises u,e, the three w centers and the four u terminals. The upper side [9,16] comprises w, its three terminals, and the four u centers. Every actual edge crosses at 9. The subtractions exhaust [1,16], including connector (8,9) of weight 1. Entry and exit are actual labels 8 and 0.

## 3. Label assignments in the three original chains

The spine rows below are in original forward name order, including the singleton entry at s:0.

| Original | Full spine labels | Actual consecutive spine differences |
|---|---|---|
| D105 one block | (30,0,22,8,21) | (30,22,14,13) |
| D105 two blocks | (46,0,38,8,30,16,29) | (46,38,30,22,14,13) |
| D117 boundary | (31,0,23,8,22) | (31,23,15,14) |

For each u or w row, the entries of the terminal list correspond to the indexed centers in order, one terminal per center.

| Original and actual group | Center labels | Own terminal labels |
|---|---|---|
| D105 one, u₁ | (24,26,27,29) | (4,3,2,1) |
| D105 one, w₁ | (5,6,7) | (23,25,28) |
| D105 two, u₁ | (40,42,43,45) | (4,3,2,1) |
| D105 two, w₁ | (5,6,7) | (39,41,44) |
| D105 two, u₂ | (32,34,35,37) | (12,11,10,9) |
| D105 two, w₂ | (13,14,15) | (31,33,36) |
| D117 boundary, u₁ | (25,27,28,30) | (4,3,2,1) |
| D117 boundary, w₁ | (5,6,7) | (24,26,29) |

For each receiver row the ordered centers are the first two at x and the last at y. Each parenthetical terminal group remains at that actual center.

| Receiver in original chain | Center labels | Indexed terminal groups in center order |
|---|---|---|
| D105 one | (18,17,9) | (10,11,16,19); (12,13,14); (15,20) |
| D105 two | (26,25,17) | (18,19,24,27); (20,21,22); (23,28) |
| D117 boundary | (20,10,9) | (12,13,14,16,17); (11,15,21); (18,19) |

The first two receiver rows apply translations 8 or 16 to the D105 primary supplier. For the D117 boundary, the local root labels are 0,14. Its local centers are (12,2,1), with terminal groups (4,5,6,8,9), (3,7,13), (10,11). In D117's exact odd/odd case the second left center is the lower role. The reflection choice at its sole unfilled index takes the midpoint 7. Adding 8 gives precisely the last row above.

## 4. Actual endpoint differences and partitions

The receiver's spine edge is already listed in Section 3. The remaining receiver edges have the following weights, independent of the stated translation.

| Receiver | x attachments in order, then y attachment | Terminal differences in original parent and terminal order |
|---|---|---|
| D105 one and two | (10,9,12) | (8,7,2,1); (5,4,3); (6,11) |
| D117 boundary | (12,2,13) | (8,7,6,4,3); (1,5,11); (9,10) |

Together with the spine weight 13 or 14, these span the respective receiver band [1,13] or [1,14]. For each block, its two spine edges for reverse installation are the adjoining original connector x_iw_i and the original internal u_iw_i. The following remaining edges follow by subtraction from the named table.

| Original and block | x_iw_i and u_iw_i | w_i attachments | w_i terminals | u_i attachments | u_i terminals | Full block band |
|---|---|---|---|---|---|---|
| D105 one, 1 | (14,22) | (17,16,15) | (18,19,21) | (24,26,27,29) | (20,23,25,28) | [14,29] |
| D105 two, 2 | (14,22) | (17,16,15) | (18,19,21) | (24,26,27,29) | (20,23,25,28) | [14,29] |
| D105 two, 1 | (30,38) | (33,32,31) | (34,35,37) | (40,42,43,45) | (36,39,41,44) | [30,45] |
| D117 boundary, 1 | (15,23) | (18,17,16) | (19,20,22) | (25,27,28,30) | (21,24,26,29) | [15,30] |

Every listed full band occurs with multiplicity one. The connector endpoint labels in the original forward orientation are (22,8) for the one-block D105 case, (30,16) and (38,8) when adjoining the two D105 blocks in reverse processing order, and (23,8) for the D117 boundary. The initial singleton adds exactly weight 30, 46 or 31 respectively, with actual endpoint u₁=0.

| Original | Labels in original receiving block 1 | Labels in receiving block 2 if present | Labels in the independent right receiver | Label at the initial singleton |
|---|---|---|---|---|
| D105 one | [0,7] ∪ [22,29] | — | [8,21] | 30 |
| D105 two | [0,7] ∪ [38,45] | [8,15] ∪ [30,37] | [16,29] | 46 |
| D117 boundary | [0,7] ∪ [23,30] | — | [8,22] | 31 |

These disjoint intervals and singleton partition each full label alphabet. At every right-to-left boundary the installed label and weight inventories are the unions for the already installed groups, and the pending inventories are the exact complements of these unions. For D105 two, for example, the initial installed receiver uses [16,29] and [1,13]. After block 2 the installed resources are [8,37] and [1,29]. After block 1 they are [0,45] and [1,45]. The singleton uses the last label and the last weight 46. The exact original connector is present for each step, and no earlier adjacency or assigned name is discarded.

[Primary D206 block](../../../research/ORDINARY_SPINE_BOUNDARY_ROOT_JOINT_BLOCK.md) · [D105 receiver](../../../research/ORDINARY_43_2_EXTREME_SPINE.md) · [D117 supplier](../../../research/ORDINARY_QAR_ALL_PARITY_SUPPLIER.md) · [D208 proof](../../../research/ORDINARY_SPINE_REVERSE_BLOCK_COMPOSITION.md)
