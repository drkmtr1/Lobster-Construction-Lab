# D212 original definitions frozen before labeling

All originals below use their listed names and incidences. There is one actual existing terminal at every listed center. Expansions retain existing terminal index zero and allocate additional indices starting at one.

All B bases have spine `s:0,s:1,s:2,s:3`, with its three consecutive edges. Each listed center of name `b:i:j` is adjacent to `s:i` and to its own terminal `l:i:j:0`. These are the only remaining edges. The (j) indices are actual ordered roles. Every listed center is a required host.

| Base | Exact profile | Actual centers | Actual terminals | Vertices | Edges |
|---|---|---|---|---:|---:|
| B2 | `[[1],[1,1],[1],[1]]` | `b:0:0,b:1:0,b:1:1,b:2:0,b:3:0` | `l:0:0:0,l:1:0:0,l:1:1:0,l:2:0:0,l:3:0:0` | 14 | 13 |
| B3 | `[[1],[1,1,1],[1],[1]]` | `b:0:0,b:1:0,b:1:1,b:1:2,b:2:0,b:3:0` | `l:0:0:0,l:1:0:0,l:1:1:0,l:1:2:0,l:2:0:0,l:3:0:0` | 16 | 15 |
| B4 | `[[1],[1,1,1,1],[1],[1]]` | `b:0:0,b:1:0,b:1:1,b:1:2,b:1:3,b:2:0,b:3:0` | `l:0:0:0,l:1:0:0,l:1:1:0,l:1:2:0,l:1:3:0,l:2:0:0,l:3:0:0` | 18 | 17 |

The fixed control original is the four-edge path with consecutive named vertices P0,P1,P2,P3,P4 and only its four consecutive edges. Its witnessing spine for the positive expansion is the singleton P2. The actual branch centers there are P1 and P3, with existing terminals P0 and P4 respectively. The adverse control keeps the same named path and tests attachment ports P0 and P4. It makes no assertion about those same vertices being branch centers for the positive witness.
