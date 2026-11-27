# Independent review and terminal verification

The initial audit and each candidate review covered native Windows lifecycle, runtime and admission, IPC and durability, scientific integration and unchanged domain, and resources and custody. Reviewers inspected actual files. Their work was read-only. Revisions V1 and V2 stayed inactive after blocking findings. The V3 and V4 approvals applied to one inert qualification invocation each. [V1 review](V1_REVIEW.json) · [V2 review](V2_REVIEW.json) · [V3 review](V3_REVIEW.json) · [V4 review](V4_REVIEW.json)

## Final native and custody decision

**Blocked.** The native reviewer independently matched V4's startup and pre-grant snapshots, bounded Job notifications, retained-handle creation and image evidence, two final empty PID lists, and signaled worker identity. The second process is identified by basename `conhost.exe`, PID 29684. Its separate exit code and creating call were not recorded. The known Job flags exclude breakaway. The original worker's exit code `0xE2040001` is the recorded supervisor stop. [V4 phase](V4_RUN/positive-primary-phase.json) · [Microsoft Job behavior](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)

The custody reviewer independently checked the V3 and V4 controller PIDs and observed exits. Both had exit code 2 with no outer timeout. V3 had 10 immutable run artifacts totaling 11,464 bytes. V4 had seven totaling 11,100 bytes. Both mirrored the retained operative source runs byte for byte. On V4, the reviewed terminal seal binds the exact five prior artifacts and the terminal file. Zero-active Job snapshots agree. No protected repository, historical artifact or accepted phase status was reopened. [V3 evidence](V3_OUTCOME.json) · [V4 seal](V4_RUN/seal.json) · [Final outcome](RESULT.json)

## Implementation scope at stop

Independent runtime review verified all 42 latest project bindings, 2,628 installed runtime identity rows, and the vacant official output and authorization paths. Scientific integration review independently compared the exact frozen configuration and ten source/input identities. The gated official code uses the same sequencing and custody infrastructure as the inert cases. It preserves both rank classes, named 32- and 41-edge inputs and deterministic 48-edge verification. The official branch was never activated. The two inert probes established permitted partial observations. The unentered matrix controls have no native observation. A never-executed candidate cannot qualify by static review or unit tests alone.

The task is closed under its four-version limit. Windows documentation motivates testing a detached console process with otherwise identical application and Job controls under a future authorization. The reviewed evidence supplies no result for that variant. [Process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags) · [Assessment](ASSESSMENT.md)
