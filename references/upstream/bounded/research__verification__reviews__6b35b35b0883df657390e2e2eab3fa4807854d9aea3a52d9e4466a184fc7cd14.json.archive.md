# P005 independent counterexample review

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/verification/reviews/6b35b35b0883df657390e2e2eab3fa4807854d9aea3a52d9e4466a184fc7cd14.json](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/reviews/6b35b35b0883df657390e2e2eab3fa4807854d9aea3a52d9e4466a184fc7cd14.json)  
Commit: `e48b94eec4091b4fe189e325cab2eda464409943`  
Verified source Git blob: `4706e96f90cc6b9693bfef63fe2b24963943986e`  
Curated scope: Complete file at the pinned commit. Historical review/provenance limits remain part of the source record.

## Source lines 1–28

[Pinned source range](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/reviews/6b35b35b0883df657390e2e2eab3fa4807854d9aea3a52d9e4466a184fc7cd14.json#L1-L28)

{
  "recorded_at": "2026-11-15T02:45:33.022362+00:00",
  "review": {
    "checks_performed": [
      "Checked live and immutable blob SHA-256 for all four submitted artifacts and checked claim and gate file hashes; did not run the P004 replay or independently re-enumerate the checkpoint.",
      "Reconstructed prefix labels 1,2,4, used differences 1,2, unused labels {0,3,5,6,7,8,9}, unused differences {3,4,5,6,7,8,9}, and root-realizable differences {3,4,5}.",
      "Verified separately feasible one-leaf branch 4-0-3, two-leaf branch 4-9-(0,3), and two-edge suffix 4-0-3 against the original resources; the witnesses may overlap because the assumptions only ask for separate feasibility.",
      "Verified all unused differences individually occur on allowable residual endpoint pairs: 3,5,6,7,8,9 via 0-x for x=3,5,6,7,8,9, and 4 via 4-0.",
      "Independently checked the impossibility: 9 can only use 0-9; alternatives to 0-8 for difference 8 and 0-7 for difference 7 use saturated fixed-prefix vertices 1 or 2. Thus label 0 requires neighbors 9,8,7. The only unassigned vertex of degree three is the two-leaf branch center, which must already be adjacent to root 4, leaving only two other neighbors. Other unassigned vertices have degree at most two."
    ],
    "completed_at": "2026-11-15T02:44:39Z",
    "disposition": "COUNTEREXAMPLE_VERIFIED",
    "provenance": "Separate collaboration-agent adversarial review of the frozen claim and immutable evidence; not independent human peer review or formal proof-assistant verification.",
    "resource_limits": "Read-only mathematical argument and bounded artifact hashes; no computational search or replay performed by reviewer.",
    "results": "COUNTEREXAMPLE_VERIFIED by an explicit finite graph argument. The conclusion refutes the stated implication for the exact fixed prefix and residual topology. It does not imply that the underlying unrestricted tree is nongraceful, prove minimality, or verify the external audit's 254/258 totals.",
    "review_id": "P005-prefix-124-independent-review",
    "review_scope": "Counterexample to separate component feasibility plus root supply and individual difference support for the fixed m=9 path prefix and specified residual topology, not unrestricted tree gracefulness.",
    "reviewer_id": "collaboration-review-p005",
    "reviewer_role": "math_correctness_verifier",
    "reviewer_run_id": "P005-prefix-124-separate-review",
    "software_versions": "Direct combinatorial review; PowerShell Get-FileHash for artifact hash comparisons; no solver execution.",
    "source_hashes": "Four frozen artifacts match submission SHA-256 values; claim file and MCV gate hashes match their submission values.",
    "submission_id": "b59a8bd5b460005fe09351fd93564a8459fe7f3b1805158e793ae70551b58e2d",
    "unresolved_objections": []
  },
  "schema_version": 1,
  "submission_id": "b59a8bd5b460005fe09351fd93564a8459fe7f3b1805158e793ae70551b58e2d"
}

---

