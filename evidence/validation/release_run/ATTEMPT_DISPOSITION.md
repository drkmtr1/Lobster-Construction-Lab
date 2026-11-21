# Preserved first release-validation attempt

The first validation script completed all 13 subprocess commands and the independent B2 oracle control. All 106 unit tests passed. The script's final aggregation then failed because it expected a positive R226 certificate from an example whose supplied fixed core was actually infeasible.

The example was the four-vertex path profile `[[0],[0]]` with core labels `s:0=0,s:1=1`. R226 correctly returned `RESTRICTED_INFEASIBLE`; this is visible in `allocation/record.json`. No solver or verifier was weakened. The intended positive example was corrected to the feasible fixed core `s:0=0,s:1=2`, and the aggregator now handles an absent certificate without crashing.

This complete attempt is preserved. The definitive final validation is in the sibling `release_verified/` directory. These old records keep their original data and paths; they are not relabeled as passing results or used to claim a positive construction.
