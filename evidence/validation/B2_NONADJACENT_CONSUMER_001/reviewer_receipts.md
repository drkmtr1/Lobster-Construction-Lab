# Separate reviewer scratch receipts

These are exact scripts and reported stdout from separate reviewer sessions. They were run once in memory and are recorded here without replaying or inventing identities. They support finite checks only; the proof is in `research/B2_NONADJACENT_CONSUMER.md`. The reviewers used PowerShell here-strings piped to `python -`; interpreter versions were not captured. No scratch output files were written. Times below are tool-reported wall times, not measured solver runtimes.

## Direct recurrence, K=2..100

Exit status 0, tool wall time 0.7 s. No project imports.

```python
def seq(k):
    if k == 2: return (3,1,0)
    if k == 3: return (4,1,0,2)
    if k == 4: return (5,1,2,0,3)
    old = seq(k-3)
    return (k+1,1,k-1,0,*[k-2-v for v in old[1:]])
for k in range(2,101):
    c = seq(k)
    assert len(c)==k+1 and c[0]==k+1
    assert sorted(c[1:])==list(range(k))
    assert sorted(abs(a-b) for a,b in zip(c,c[1:]))==list(range(1,k+1))
print('K=2..100: all three invariants hold')
for k in (2,3,4,5,6,7,8):
    c=seq(k)
    print('K=',k,'labels=',c,'differences=',tuple(abs(a-b) for a,b in zip(c,c[1:])))
```

```text
K=2..100: all three invariants hold
K= 2 labels= (3, 1, 0) differences= (2, 1)
K= 3 labels= (4, 1, 0, 2) differences= (3, 1, 2)
K= 4 labels= (5, 1, 2, 0, 3) differences= (4, 1, 2, 3)
K= 5 labels= (6, 1, 4, 0, 2, 3) differences= (5, 3, 4, 2, 1)
K= 6 labels= (7, 1, 5, 0, 3, 4, 2) differences= (6, 4, 5, 3, 1, 2)
K= 7 labels= (8, 1, 6, 0, 4, 3, 5, 2) differences= (7, 5, 6, 4, 1, 2, 3)
K= 8 labels= (9, 1, 7, 0, 5, 2, 6, 4, 3) differences= (8, 6, 7, 5, 3, 4, 2, 1)
```

## Implementation versus direct recurrence

Exit status 0, tool wall time 1.3 s. This reviewer imported the then-current `lcl.consumers` and unchanged verifier; no script-level source hash was recorded. The later declared regression has a full source snapshot and exact hashes.

```python
from copy import deepcopy
from lcl.consumers import complete_nonadjacent_path, _nonadjacent_path_labels
from lcl.verify import verify_certificate

def reference(k):
    base={2:(3,1,0),3:(4,1,0,2),4:(5,1,2,0,3)}
    if k in base: return base[k]
    old=reference(k-3)
    return (k+1,1,k-1,0,*(k-2-x for x in old[1:]))

for k in range(2,101):
    for ell in (0,1,7):
        assert _nonadjacent_path_labels(k,ell) == [x+ell for x in reference(k)]
    edges=[['p0','s:2'],['p0','p1']]+[[f's:{i}',f's:{i+1}'] for i in range(2,k+2)]
    graph={'vertices':['p0','p1']+[f's:{i}' for i in range(2,k+3)],'edges':edges}
    prefix={'p0':0,'p1':k+1,'s:2':k+2}
    graph_before,prefix_before=deepcopy(graph),deepcopy(prefix)
    full=complete_nonadjacent_path(graph,prefix,k,1)
    assert graph==graph_before and prefix==prefix_before and verify_certificate(graph,full)['valid']
print('PASS K=2..100: affine sequence vs direct recurrence at ell=0,1,7; caller graph certificate and immutability at ell=1')
```

```text
PASS K=2..100: affine sequence vs direct recurrence at ell=0,1,7; caller graph certificate and immutability at ell=1
```

## Exploratory finite fixture discovery

A separate implementation-design reviewer also ran the following finite *first-witness* scratch search on the exact original `q=1,r=2,z0=z1=0` B2 profiles at K=2,3,4. It was not the superseded p=5/6/7 seed sweep. It tested interval positions in the shown fixed ranges, both distance-two port orientations, and permutations of the seven remaining prefix labels, stopping each K at its first positive. Maximum possible work is 18 × 7! permutations per K; actual attempts were **not counted**. Its direct output below records three below-side finite prefixes only. The script did not capture its interpreter version or source hashes; tool wall time was 1.2 s. It establishes no exhaustive count, supplier, p=5 seed or all-K claim. The K=2 prefix was reflected into the above-side test fixture and checked against the retained original graph by the project tests.

```python
from itertools import permutations
from lcl.model import build_graph
for K in (2,3,4):
 g=build_graph([[1],[2]]+[[]]*(K+1)); m=len(g['edges']); tail={f's:{i}' for i in range(3,K+3)}; verts=[v for v in g['vertices'] if v not in tail and v!='s:2']; edges=[(u,v) for u,v in g['edges'] if u not in tail and v not in tail]
 found=False
 for a in range(m-K+2):
  rem=set(range(a,a+K))
  for port in (a-2,a+K+1):
   if port not in range(m+1): continue
   pool=set(range(m+1))-rem-{port}
   for p in permutations(pool):
    lab=dict(zip(verts,p)); lab['s:2']=port
    if {abs(lab[u]-lab[v]) for u,v in edges}==set(range(K+1,m+1)):
     print('K=',K,'start=',a,'port=',port,'prefix=',lab); found=True; break
   if found: break
  if found: break
 if not found: print('K=',K,'no prefix in this exact limited distance-2 port selection')
```

Reported output, transcribed as mappings:

```text
K=2 start=3 port=1 prefix={'s:0':6,'b:0:0':2,'l:0:0:0':8,'s:1':9,'b:1:0':0,'l:1:0:0':5,'l:1:0:1':7,'s:2':1}
K=3 start=3 port=1 prefix={'s:0':0,'b:0:0':10,'l:0:0:0':6,'s:1':9,'b:1:0':2,'l:1:0:0':7,'l:1:0:1':8,'s:2':1}
K=4 start=4 port=2 prefix={'s:0':1,'b:0:0':11,'l:0:0:0':0,'s:1':10,'b:1:0':3,'l:1:0:0':8,'l:1:0:1':9,'s:2':2}
```
