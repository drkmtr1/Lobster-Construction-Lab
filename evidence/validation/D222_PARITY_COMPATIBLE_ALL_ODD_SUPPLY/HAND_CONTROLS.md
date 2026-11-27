# D222 named hand controls

## Named graph definitions

The profiles in this record specify the graphs before any labels are assigned. Both T and S have the three edges s:0--s:1, s:1--s:2, s:2--s:3. At position u of section i, with indices starting at zero, place b:i:u and attach its specified number of indexed terminals l:i:u:e to it. T attaches every b:i:u to s:i. S changes only s:0--b:0:0 and s:3--b:3:0 to s:1--b:0:0 and s:2--b:3:0. These are their entire named incidence lists. For the matching-based construction below, only T is used. Table tuples are in ascending terminal index order.

## 1. Director seed

The profile is `[[1],[1,1],[1,1,1,1,1],[1]]`, with h=5, F=9, m=21. The spine labels in original order are (20,0,21,7). The three actual spine weights are (20,21,14). The two separate attachment columns specify the rest of each actual skeleton.

| Center name | Label | Terminal label | Terminal weight | S attachment | T attachment |
|---|---:|---:|---:|---|---|
| b:0:0 | 3 | 9 | 6 | s:1, 3 | s:0, 17 |
| b:1:0 | 1 | 14 | 13 | s:1, 1 | s:1, 1 |
| b:1:1 | 18 | 10 | 8 | s:1, 18 | s:1, 18 |
| b:2:0 | 2 | 11 | 9 | s:2, 19 | s:2, 19 |
| b:2:1 | 5 | 15 | 10 | s:2, 16 | s:2, 16 |
| b:2:2 | 6 | 13 | 7 | s:2, 15 | s:2, 15 |
| b:2:3 | 17 | 12 | 5 | s:2, 4 | s:2, 4 |
| b:2:4 | 19 | 8 | 11 | s:2, 2 | s:2, 2 |
| b:3:0 | 4 | 16 | 12 | s:2, 17 | s:3, 3 |

The roots and slots give {0,21}∪[1,7]∪[17,20]. The terminal labels fill [8,16] and the terminal weights fill [5,13] once. Either attachment column together with the three spine weights gives [1,4]∪[14,21] once. Therefore each graph has exact alphabet [0,21] and spectrum [1,21]. The changed edges exchange weights |0−3|=3 and |21−4|=17 as |20−3|=17 and |7−4|=3. This verifies the marked certificate. Ordinary unit-quota gracefulness already follows from the perfect matching consisting of branch terminal edges and s:0--s:1, s:2--s:3.

As an adverse geometry control on the same unit quotas, use the old bands [1,6]∪[16,20]. Their exact sum is 5·21+6=111, which is odd. A valid fold plus restoration at roots 0,21 would require that sum even. The imbalance-three bands instead give sum 4·21+3·6=102.

## 2. Independent growth at three actual hosts

Take `[[3],[1,1],[1,1,1,3,1],[3]]`, so α=β=r=1, F=15 and m=27. This is also the proposed matched control for the unentered discriminator. Insert G=4 first. At cuts (3,2) give the local orbit {0,3} to host 4 and the local orbit {1,2} to high m−4. In global normalized coordinates (i,w) these give (3,2),(6,5) and (4,4),(5,3), respectively. Amplify host 3 afterward by centrally translating every index and weight by one and adding outer rows (0,0),(14,14) at 3. The final spine labels are (26,0,27,7), with weights (26,27,20).

| Center name | Label | Terminal labels | Terminal weights | S attachment | T attachment |
|---|---:|---|---|---:|---:|
| b:0:0 | 3 | (8,10,22) | (5,7,19) | 3 | 23 |
| b:1:0 | 1 | (19) | (18) | 1 | 1 |
| b:1:1 | 24 | (11) | (13) | 24 | 24 |
| b:2:0 | 2 | (16) | (14) | 25 | 25 |
| b:2:1 | 5 | (20) | (15) | 22 | 22 |
| b:2:2 | 6 | (18) | (12) | 21 | 21 |
| b:2:3 | 23 | (13,14,17) | (10,9,6) | 4 | 4 |
| b:2:4 | 25 | (9) | (16) | 2 | 2 |
| b:3:0 | 4 | (12,15,21) | (8,11,17) | 23 | 3 |

The terminal label alphabet is [8,22] and the terminal weights are [5,19]. The roots and slots fill all remaining coordinates of [0,27], and the skeleton gives [1,4]∪[20,27] on each graph. The restored edges exchange 3 and 23.

For the companion `[[3],[1,1,1,1],[1,1,3],[3]]`, keep the spine and exterior entries. Give the named left interior centers in order (1,24,2,25) and the right interior centers (5,6,23), with each center retaining its terminal tuple above. In both graphs the moved pair {2,25} contributes weights (25,2) at the right root before the change and (2,25) at the left root after it. All incidences match this independently specified companion, the full alphabets remain [0,27] and the full spectra remain [1,27]. No unequal quota is moved between the physical sections.

## 3. Larger-multiplicity one-quota supply on the original itself

Take `[[1],[3,1],[1,1,1,1,1,1,1],[1]]`, with h=6 and m=27. Start from the same named unit subgraph by using only each terminal index zero. Its auxiliary contracted double star has hubs of labels 12,3, with left leaf labels (1,0,2) in physical branch order and right leaf labels 4 through 11 in order. Their complete weights are (11,12,10), (9) across the hubs, and (1,2,3,4,5,6,7,8) in the right leaf group. Lift with M₀=25 and name b:1:0 as the even endpoint of the pair at auxiliary label zero. The exact spine labels on T are (1,24,6,19), giving weights (23,18,13).

| Center name | Label | Terminal labels on T | Actual terminal weights | Actual attachment weight |
|---|---:|---|---|---:|
| b:0:0 | 23 | (2) | (21) | 22 |
| b:1:0 | 0 | (25,26,27) | (25,26,27) | 24 |
| b:1:1 | 4 | (21) | (17) | 20 |
| b:2:0 | 8 | (17) | (9) | 2 |
| b:2:1 | 10 | (15) | (5) | 4 |
| b:2:2 | 12 | (13) | (1) | 6 |
| b:2:3 | 14 | (11) | (3) | 8 |
| b:2:4 | 16 | (9) | (7) | 10 |
| b:2:5 | 18 | (7) | (11) | 12 |
| b:2:6 | 20 | (5) | (15) | 14 |
| b:3:0 | 3 | (22) | (19) | 16 |

With index zero at each branch the lifted labels are [0,25]. Every branch attachment and the middle spine edge have the twelve even weights 2 through 24. The original spine-end edges and branch terminal-zero edges give every odd weight from 1 to 25. The two extra leaves appended at b:1:0 carry 26 and 27 and give those actual differences. The graph T therefore has 28 vertices bijectively labeled [0,27] and the full spectrum [1,27]. This certificate directly uses T's exterior parents. There is no claim that this labeling supplies S or any extreme-root marks.

## 4. Small centered-peel adverse checks

At the h=5 all-unit imbalance-three inventory, F=9. To allocate one each at 3 and m−2 and return a symmetric middle interval at 4 would remove i=0,8. The restored middle at 4 would use w=0 through 6, so only w=7,8 remain. The two available labels give w=0 or 6 from i=0 and w=8 or −2 from i=8. Weight 7 is unavailable.

For the four-host candidate 3,4,m−2,m−3 with unit quotas, the outside indices are {0,1,7,8}. The remainder at 5 uses w=0 through 4, so exterior differences must be normalized weights 5 through 8. Low i=0,1 can use neither low host. Their two high alternatives give weight pairs (6,4) or (5,5). Each pair fails. These exclusions concern the proposed contiguous middle returns. The actual seed in Section 1 satisfies the same whole-original quotas.

All arithmetic in this record was checked by hand. No numerical discovery, solver, protected checker or scientific module was used.
