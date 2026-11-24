# D110 verification evidence

The [proof](../../../research/ORDINARY_53_2_MAGNITUDE_TWO.md) excludes exactly one negative signed difference of −2 on any left terminal of the [frozen D108 original](../LCL_ORDINARY_53_2_SIGNED_SEED_001/original.json) with `s:0=0`, `s:1=14` and `b:1:0=1`. The original is ordered `[[5,3],[2]]`. Its canonical digest is `915f7ff845db575f2be0b87e587c2236d935eabfc674e9bd99e8bce1358033f8`.

The [independent audit](result.json) records the named original incidences, traversal classes, weighted degree identity, three structural cases and three surviving scalar rows. Two rows force the second left center and a right terminal to share a label. The third forces weights 9 and 11 twice each on four distinct edges. The remaining structural case is ruled out by the bound `107<111`.

The unchanged checker accepted the retained D106 certificate on its own original. That certificate satisfies the location-free magnitude-one predicate and fails magnitude two. All four declared probes on the D106 original gave their expected outcomes.

| Probe | Ordinary checker | Independently evaluated interface |
| --- | --- | --- |
| Wrong digest | Reject | Digest rejection tested through the unchanged checker |
| Within-center terminal swap | Accept | Pins and magnitude one pass. Magnitude two fails. |
| Global complement | Accept | Pins (14,0,13) fail. The 13 negative signed edges also fail the required pattern. |
| Swap left terminal 11 and right terminal 12 | Reject | Pins pass. The sole negative signed difference is −2 at the named left terminal, so the magnitude-two predicate passes. |

The last probe repeats weights 2 and 10 twice each and omits 1 and 11. It was used only to check that the signed predicate can succeed independently of ordinary verification. No new certificate or original was produced.

One [parse-only preflight](preflight_receipt.json) checked 179 repository bindings, task source hashes, unique intended function definitions, project-local Python 3.13.17 and vacant outputs, with no task imports or bytecode. One [official invocation](command_receipt.json) used 0.1875 process-CPU seconds, 0.21349420002661645 in-process wall seconds and 0.5696443 externally supervised wall seconds. The run used one worker, one retained positive recheck and four declared probes. All solver, assignment enumeration, search, additional profile, join, historical replay, retry, restart and successor experiment counts were zero.

See the [contract](CONTRACT.md), [configuration](config.json), [separate reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json).

## Reproduction under separate authorization

Run from the project root in a disposable checkout with vacant output paths, the pinned Python runtime and a 60-second external deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_53_2_MAGNITUDE_TWO_001/preflight.py 6a0fc2b4b2bf54582186ef23016d66ad8ee438314fa8573f23fac03e4e774b92
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_ORDINARY_53_2_MAGNITUDE_TWO_001/run.py
```
